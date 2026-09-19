"""
Vedic (Jyotish) Birth Chart Web App
------------------------------------
A small Flask app with a form (name, date/time of birth, latitude,
longitude, timezone) and a "Generate" button that renders South Indian
and/or North Indian style Rashi (D1) and Navamsa (D9) natal charts, plus
Nakshatra, Vimshottari Dasha, and "houses involved" breakdowns.

Combines two free, open-source Python libraries:
  1. Kerykeion  -> sidereal (Lahiri ayanamsa) planetary positions via the
                   Swiss Ephemeris.
  2. jyotichart -> pure-Python SVG renderer for South Indian (square) and
                   North Indian (diamond) chart styles.

Birth location:
  Type a birth city and press "Confirm place" - the server geocodes it with
  geopy's Nominatim (OpenStreetMap) backend and fills the latitude and
  longitude boxes for you. Both fields stay editable, so you can still type
  coordinates by hand if the lookup misses or the service is down.
  The IANA timezone is entered separately;
  https://en.wikipedia.org/wiki/List_of_tz_database_time_zones has the
  names (e.g. Asia/Kolkata, America/New_York).

Progressive Web App:
  The app ships a manifest, a small offline-capable service worker, and
  generated app icons, so it can be "installed" from a mobile or desktop
  browser (Chrome/Edge: menu -> Install app; iOS Safari: Share -> Add to
  Home Screen) and then opens full-screen like a native app. Installing
  is entirely optional - the app works the same in a regular browser tab.

Setup:
    pip install flask kerykeion jyotichart geopy

Run:
    python app.py
    then open http://127.0.0.1:5050 in your browser (or your machine's
    LAN IP, e.g. http://192.168.x.x:5050, to try it on a phone). Port
    5050 (not 5000) to avoid clashing with macOS's AirPlay Receiver,
    which listens on port 5000 by default.
"""

import os
import re
import json
import base64
import tempfile
import urllib.parse
from functools import wraps
from flask import (
    Flask, request, render_template_string, redirect, url_for, Response,
    jsonify, session,
)

from kerykeion import AstrologicalSubject
import jyotichart as chart

import db as storage
import i18n

try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderServiceError, GeocoderTimedOut
except ImportError:  # geopy is optional - without it the app just loses lookup
    Nominatim = None
    GeocoderServiceError = GeocoderTimedOut = Exception

try:
    import chart_pdf
except ImportError:  # reportlab/svglib missing - the app loses only PDF export
    chart_pdf = None

app = Flask(__name__)

# Signs session cookies (used for the admin login). Set a real SECRET_KEY
# env var in production - anyone who can guess this can forge an admin
# session, so the fallback below is only OK for local development.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-secret-change-me")

storage.init_db()

# Password for the /admin panel. Set ADMIN_PASSWORD in the environment
# before deploying - the fallback here is only for local development.
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
if not ADMIN_PASSWORD:
    ADMIN_PASSWORD = "admin"
    print(
        "WARNING: ADMIN_PASSWORD is not set - the /admin panel is using the "
        "insecure default password 'admin'. Set ADMIN_PASSWORD before deploying."
    )


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)
    return wrapped

# One shared geocoder. Nominatim (OpenStreetMap) is free and needs no API key,
# but it does require a descriptive user_agent and is rate limited to roughly
# one request per second - fine for a "Confirm place" button a human clicks.
_geolocator = Nominatim(user_agent="vedic-birth-chart-app", timeout=10) if Nominatim else None


@app.route("/geocode", methods=["POST"])
def geocode():
    """Look up a place name and return its latitude/longitude as JSON."""
    place = (request.form.get("place") or "").strip()

    if not place:
        return jsonify({"error": "Enter a birth city first."}), 400
    if _geolocator is None:
        return jsonify({"error": "geopy is not installed (pip install geopy)."}), 500

    try:
        location = _geolocator.geocode(place)
    except (GeocoderServiceError, GeocoderTimedOut):
        return jsonify({"error": "Lookup service unavailable, enter coordinates manually."}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if location is None:
        return jsonify({"error": f'Could not find "{place}".'}), 404

    return jsonify({
        "lat": round(location.latitude, 6),
        "lng": round(location.longitude, 6),
        "address": location.address,
    })


@app.route("/save", methods=["POST"])
def save_details():
    """Explicit "Save details" button - stores the current form values so
    they show up in /admin. Separate from /generate on purpose: generating a
    chart should not silently persist anything unless the user asks for it.
    """
    form = {
        "name": (request.form.get("name") or "").strip(),
        "city": (request.form.get("city") or "").strip(),
        "date": request.form.get("date", ""),
        "time": request.form.get("time", ""),
        "lat": request.form.get("lat", ""),
        "lng": request.form.get("lng", ""),
        "tz": (request.form.get("tz") or "").strip(),
        "style": request.form.get("style", "south"),
    }

    if not form["name"]:
        return jsonify({"error": "Enter a name first."}), 400

    try:
        record_id = storage.save_birth_record(form)
    except Exception as db_err:
        return jsonify({"error": f"Could not save: {db_err}"}), 500

    return jsonify({"ok": True, "id": record_id})

# ---------------------------------------------------------------------------
# Progressive Web App: manifest, service worker, and app icons
# ---------------------------------------------------------------------------
# Everything needed to install this as a PWA is generated/embedded right
# here (no separate /static folder) so the whole app stays one file. Icons
# are pre-rendered PNGs (violet-to-pink gradient with a gold zodiac-wheel
# motif), base64-encoded below; the manifest and service worker are served
# as plain strings with the correct content type.

APP_NAME = "Vedic Birth Chart"
APP_SHORT_NAME = "VedicChart"
THEME_COLOR = "#0b0d17"

ICON_192_B64 = "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"
ICON_512_B64 = "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"
ICON_512_MASKABLE_B64 = "iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAA5oElEQVR42u3da5ckxX0n4Kg6/hretb/K2pZve9YX5gISEggkcYeBZrhKxzfEvZkBBhBIgNDFEjODfXZf+HhtWdpv1vuCzqK6OrMqMzIyMzLjiXN8DAq6u7orK55f/DMicvU/f/+9kxBOQlNbhTBi30n090z7ek4m+v13+lcnE78fVd/JxO9H/+sj6XW1Opn4/Th/nU7zfsRfH4O81tXJxO/H9ONH7PUx6LWzOpn4/Zhu/Nh3fUxu3SqENfzhD3/4wx/+8C8L/xBOwhr+8Ic//OEPf/iXhX8IoT4AwB/+8Ic//OEP/+XiXxsA4A9/+MMf/vCH/7LxX+0GAPjDH/7whz/84b98/M9UAOAPf/jDH/7wh38Z+G8CAPzhD3/4wx/+8C8H/xBCWMMf/vCHP/zhD/+y8N9UAOAPf/jDH/7wh385+DcGAPjDH/7whz/84b9c/GsDAPzhD3/4wx/+8F82/iNsA4Q//OEPf/jDH/654X+mAgB/+MMf/vCHP/zLwH8TAOAPf/jDH/7wh385+IcwyDZA+MMf/vCHP/zhnzP+mwoA/OEPf/jDH/7wLwf/xgAAf/jDH/7whz/8l4t/bQCAP/zhD3/4wx/+y8Y/0TZA+MMf/vCHP/zhPyf8z1QA4A9/+MMf/vCHfxn4bwIA/OEPf/jDH/7wLwf/EKK3AcIf/vCHP/zhD/+54r+pAMAf/vCHP/zhD/9y8G8MAPCHP/zhD3/4w3+5+NcGAPjDH/7whz/84b9s/M8FAPjDH/7whz/84b98/M+cAwB/+MMf/vCHP/zLwH9TAYA//OEPf/jDH/7l4B/C3m2A8Ic//OEPf/jDf4n4byoA8Ic//OEPf/jDvxz8GwIA/OEPf/jDH/7wXzL+NQEA/vCHP/zhD3/4Lx3/nQAAf/jDH/7whz/8S8B/axsg/OEPf/jDH/7wLwX/0woA/OEPf/jDH/7wLwn/EE5inwYIf/jDH/7whz/854r/aQUA/vCHP/zhD3/4l4R/YwCAP/zhD3/4wx/+y8W/NgDAH/7whz/84Q//ZeN/LgDAH/7whz/84Q//5ePf8mmA8Ic//OEPf/jDf0n4byoA8Ic//OEPf/jDvxz8Qwj7twHCH/7whz/84Q//5eG/qQDAH/7whz/84Q//cvDfGwDgD3/4wx/+8If/MvFvDADwhz/84Q9/+MN/ufjXBgD4wx/+8Ic//OG/bPxXocM5APCHP/zhD3/4w38Z+J+pAMAf/vCHP/zhD/8y8N8EAPjDH/7whz/84V8O/iGE+McBwx/+8Ic//OEP/3niv6kAwB/+8Ic//OEP/3LwbwwA8Ic//OEPf/jDf7n41wYA+MMf/vCHP/zhv2z8e24DhD/84Q9/+MMf/nPE/0wFAP7whz/84Q9/+JeB/yYAwB/+8Ic//OEP/3LwD6HzNkD4wx/+8Ic//OE/d/w3FQD4wx/+8Ic//OFfDv6NAQD+8Ic//OEPf/gvF/8QQvg9+MMf/vPH/6UvXgtjtr+/8Az84Q//GeO/CiGsLvz+uyfwhz/888T/5ZFhT93+4cJV+MMf/hniH7YDAPzhD/9p8J878rHtHy9chT/84T8R/psAAH/4w3/46+OVQqHv2v4pWTCAP/zhv69vdXHrFgD84Q//NNfHq7BP2l7qfCsB/vCH/6G+nQAAf/jDP+b6AP647YengQD+8Id/fN9WAIA//OHftu/VL16lcEbt5U0ggD/84d+678sAAH/4w/9Q32vQn0kYeBr+8Id/i77Vxd9/5wT+8If/+T7gL6O9choI4A9/+J+1bhMA4A9/+EN/6e3VnTAAf/iXin+oKgDwh3/J+L++APR/cHoy31jv1d/dfn1xYQD+8C8J/xBCWF3augUAf/iXgv9c0P/+Hc+eeV/mdrb/D26/MYu/82t7KgPwh/8S8d8bAOAP/6XhnzP6L55CX8qDfb6fcTDYDgPwh/9S8W8MAPCH/5Lwzwn+F7dn9G1/j4Ke6vdiRsHg9UNVAfjDf8b41wYA+MN/Cfi/kQH6L+xg75G+cX05hILXd6sC8If/zPE/FwDgD/+54z8l/C/EzO7h3/n6eOH2m5O9x29ceBr+8F8G/tsBAP7wnzP+U8D//KH79vAf5fp4foJA8MbFI/jDf9b4byoA8If/HPGfEv1Brx34R18fU4SBN3fCAPzhPwf8QwhhdXmAbYDwh/+Q+I8J//ORZX34hywe6fvciIHgzRGqAvCHfyr89wYA+MM/N/zfHAn+51qU9uGfP/67/c+OFAbevHgEf/hnj39jAIA//HMa3MeA/7kUK/bhny3+u22MMHBcc2sA/vDPBf/aAAB/+OcyuE8BP/yXj/923zMjBgH4wz8n/M8FAPjDP4fBfWj4n7vjuajrA/7Lwn+3DR0G3mpYLAh/+E+C/3YAgD/8px7ch4b/2Tuei74+4L9s/Lf7ro4YBOAP/6nw31QA4A//peL/7B3P9b4+4F8O/rvj2NVbx4OFAPjDf0r8QwhhdWfkNkD4wz/F4D4G/PCHfwz+231PDxQErtXeFoA//IfHf28AgD/8hxzcx4If/vDvi/92Gz4IwB/+4+DfGADgD/+hBvch4K9DH/7wT43/bt/RAGHg+sWn4A//UfCvDQDwh/9c8H9ms6gP/vAfF//tljoI1IUA+MM/Nf7nAgD84T/E4H48APxDXR/wh3/s9xwqCMAf/oPgvx0A4A//1IP7UPDDH/654b/d91TiIPB2w20B+MO/789c3XlgGyD84T81/s/UruiHP/zzwz8MFAR2QwD84Z/iZ67u2rMNEP7w7zq4Dwk//OE/F/y3+55MHATgD/9UP3MNf/jDH/7wH+73v9ZwBHBMe+LWW/CHf7K+xgoA/OHfdnAfGn74w3+u+O+2lNWAd7ZuC8Af/lHbAO/adw4A/OE/Ev7PHNzLD3/4zxv/7fHjyp6ZfNcQAH/4R/fd1XQOAPzhPwL+V1vt5Yc//JeD/3ZLEQTe7bRLAP7w/6rvTACAP/zb9B1/8UqS2Qv84V8y/ilDwG4QgD/8W20DvGv3HAD4w39g/K+2PsgH/vBfNv7bfU8kqgbAH/5t+9bwhz/84Q//afEPofnAny7tsdoQAX/41/etvl7dAoA//Bv6UsIPf/jD//D3fTxBNeDGxafgD/+9fWv4wx/+8Id/PviHcHaLX2x79DREwB/+jdsAv/7f3j7J+Q8C//nif7XzEb7whz/8d1vfasB7F5+EP/zrx7LdAAB/+Kee9cMf/vDv9zMfS3BLYDsIwB/+q90KAPzhn3rWD3/4wz/dz3wsQTUA/vCv+tbwhz/84Q///PEPofnQn7btkVvX4A//TVvDH/7whz/888e/ajd6hoCHG0IA/MvCP4QQVt+oWQQIf/j3gR/+8If/OK/n0R63BN5vuSYA/svEf28AgP/y8X9rgFk//OEP/3Gvj0cPlPUPtQ8adgnAf9n4h7C1BgD+8Ic//OE/L/xDaN7m17Y91PeWAPxniX9tBQD+8I+BH/7wh//418du3yM9qgEfxNwSgP988d+tAMAf/vCHP/zniX/fakBVCYB/GfiHMMo2QPjDH/7wh//Q+Fft/QQhAP7Lx38TAOAPf/jDH/7zx3+VIAQ8WBMC4L88/EMIYXX3YNsA4T93/J++47mswiH80/W9ePuN493/5uULV4/gP3/8d9vDkesCfnQaIuC/TPw3FQD4wx/+Zc78g5n/ovHvUw148NY1+C8Y/8YAAH/4w780/Cd+P+A/CP5V/weRIeCBqnoA/8XhXxsA4A9/+MMf/svBv2r9QgD8l4Z/4m2A8Ic//OeA/7QDOPynwL93CLh5Hf4Lw/9MBQD+8Ic//OG/XPyr9qOeIQD+y8B/EwDgD3/4l41/GPv9gP8k+K96hoDv1YQA+M8T/xBCWMMf/vAvDf8T+BeMf99KwHYIgP988d9UAOAPf/jDH/7l4J8iBMB/3vg3BgD4wx/+8If/svGv+j6MDAHfbVgTAP954F8bAOAPf/jDH/5l4F+1Dy+lCQHwnw/+5wIA/OEP/+Xjb7U//OtO+Pvw0pVeIQD+88L/zDkA8Ic//OEP/zLxr9pHPUMA/OeD/6YCAP/54B+7lQv+8I+9duBfBv6rniEA/vPCP4RW2wDhnxP+xxGzf/jDH/7w7/Jgn5gQ8J3oMwLgPwX+mwoA/OEPf/jDH/4pQwD888a/MQDAH/7whz/8y8W/6vtxZAiAf/741wYA+MMf/vCHP/yrFhMC7j94RgD8p8b/XACAP/zhv3z8rfaHf9fvmSIEwD8v/Gu2AcI/J/xjGvzhD3/4p8S/aj/psTsA/vnhv6kAwD9P/LvO/uEPf/jDfwj8V5Eh4P4z6wHgnxP+IWy2AcJ/7vhP8YGB/3Lw7/Vewb8I/GPbfTevwz9D/E8rAPBfAv5X73gO/vCHP/wHxz/mVsB9N9+Gf2b4h3DS/WmA8M/rnj/84Q9/+I8980+zHgD+U+J/WgGAf074d539wx/+8If/mPhX/R93DAH33Xwb/hnhfy4AwB/+8Ic//OHf9rV2DQHf3rkVAP/p8G/9NED454d/GPkDA3+r/eEP/74LAutCAPynwX9TAYB/XoN7n9k//OEPf/iPic3HWa4HgH+bsWwN/+kH9+MvXoU//CfF/+DXwR/+e/o+ibgVAP9p8d9UAOAPf/jDH/7wj//ak/DJpSc6XVv3DrIeAP5dxrI1/OeD/5hpGf7whz/8Y5/qFxsC4D8e/o0BAP7jDu59Zv/whz/84Z8L/l2rAPCfDv/aAAD/cQb3FKV/+MMf/vDPaea/CiF8GnErAP7j478KHc4BgD/84b8M/K32h/9Q+Fetawi4J3o9APz7jGXr4f5Y8E9R9k//euAPf/jDfzj8xxvn4N93LFsP88eCf9Pg3nf2D3/4h4E+P/CHf0r8+1QB4D88/iEcOAcA/vCHfyH45zCYwn9RM/9VCOGnESEA/uPgv6kAwH+cwb1Pgz/84Q//OeGfusE/Lf6NAQD+6Qf3PrN/+MMf/vCfK/5dqwDfqlkQCP/0+NcGAPiPO7jDH/7wh//SZ/4/7X0+APyHGMsSbAOE/6HB/c3IE//gD/+coIY//Id6PU1VAPgPh/+ZCgD888C/mv3DH/6DYWO1P/wnwP+zqFsB8B9yLOuxDRD+Kcv+8If/lPiH0T/L8C9x5v9Zj1sB8E9/fazhP9zgHlP6hz/8R8b/CP7wz6HsX9e+efMd+A84lkVsA4R/6pl/NfuHP/wnwv8I/vAfC/+fTfbAIPi3CgDw7z+4d5n9wx/+Gcz8j+AP/7Hejy4hoKoCwD/96+mwDRD+Q8z8+78e+MO/G/5Xbx3X/vdPn/7v8If/FGO9mf/4Y1nLbYDw7zK4d5n9P1PzpD/4w39s/HdDAPzhP/T70aUKcHfNWgD4j7INEP5D4d/vYoE//NPiX7Wjmv8O/vCfcjFgXQiAf/++NfynKfvvm/3DH/5T4V8XAuAP/6H6fn7p8YEmSPBv07eGf7rBPcXsH/7wnxr/7RAAf/gP19f9TIq7b74D/4R9a/iPP/Nvmv3DH/654F+1pxq+Hv7wT4V/bBUA/v371vBPM7j3XfgHf/jnhn9TCIA//FPP/LuEgG+kOhyocPxrAgD8h575p/rAwB/+Y+C/GwLgD/+xy/5m/qNsA4R/7ODeZ/YPf/hPjH/r//ipvd8X/vCPx38VQvhFRBUA/v361vA384d/8fi3/qIna78//OHfD38z/2k+O2v498M/dvYPf/hnNvOPDAHwh386/LtUAb7e9XAg+J8by9bwj8d/uOQKf/gPh//xxfoHAL518aj19/gyBMAf/uPP/KP+NvCvHcvWY76ApeH/RsTsH/7wzxH/uBDwFvzhnxz/X0ZWAeDffSxbj/UCzPzhD/+88Y8JAVdqQgD84R+Lf/KxFf57x7L1GC9gifh3nf3DH/5zwL/6edciQwD84Z8C/18mWAsA//1j2bkAAH8zf/gvH/+2r6VrCIA//Mee+Qcz/2j8z5wDAP9h8H/24ON+4Q///PCPCQFPNKwJgD/8Y77vL2OPCIZ/K/w3FQD4d/s93kj20B/4wz8P/Pe1axefig4B8If/GI8Rvqu6DQD/1viHEIbZBmjmD3/4LwP/aqvf9YgQAH/4j4G/mX8c/psKAPzbf98us/9nGx/6A3/4zwf/ql3vUQmAP/xj+v65w22Auz5/F/4dr4/14H8sM3/4w3/2+MeEgMeTbBGEv5l/inEX/qFNAIB/c3+f2T/84T93/Kv2dmQIgD/8Y/q6VAHu3KkCwL/D44Dhb+YP/+Xjn+KRvl1DAPzhP3ZVAP4dHgcM/3QX4bPnHvoDf/gvB/+YSsBjnbYIwh/+Z/t+1XFLIPw7PA4Y/oe/7+sRW//gD//54B/3tX1CAPzhP8TM/87IxYCl4R9Cj22AZv7wnyP+L9x+4xj+Mddyc987ESEgR/wfuHXtGP7zxj+Mdu3MH/9NBQD++/te77j4D/454x/CC7ffPIZ/Gvyr9k7v2wF54P/l/4d/jvj/6vJjra+xyx0WA5aKf2MAgL+Z/1LxD5t/f/MY/ml/xy4h4NEzISCTmf9pe+Dm9WP4ZzbzPzCWmfnHfd917z8W/DftuTueg3+mH5iXLzx97lD757cqAfBP8zu+2zkE5IV/CCF8eOnKEfzzxP/XHaoA8D/ct+71xyoA/26L/+Cf8wemTQgoZbV/GPBv3i0EXIM//AeZ+V/esxgQ/h22AZr5jz+Tgv8w18cre0KArX7p3o8uIeCRW9fgD/+k+Kcdl5eJ/6YCAP/++D93x7Pwz/wDs2oRAuCfrq9PCIA//Jv6ut4GgH9z3xr+zX2v93jsL/zzvj7qQsBzEWsCloL/UNjeiAgB8Id/qsnapV5HAy8b/00FAP5pZ//wn8f10SYEwL9/340EtwPgD//tr/s8ogoA//Ot/TkAheGf//nT8O97faxCCK/uCQHwT9d34+KTrX/uwxFrAuBv5g//7n3tzgEoEP/Xoo/+hf9c8K/aqx1uB8A//vp4r0cIgD/8Y9ulTkcDl4N/bQCAf7dWlf/hP++z/etCwLM1IQD+cddH1RcTAuAP/7r2efLFgGXhvwqHzgGAv5l/Afi3DQFW+/fDP/QIAfCHf8qqAPx3KgDw/6p1Kf/Df1lP9XutIQTAPw3+MSHgoZoQAH/4d2kXt24DwP+rtoZ/fJJ8vmbvP/zni/8mANaEgGf2bRFcAP5hgOvj0Ne9HxkC4A//qt3sfTRwufiHUHcOAPx7N/jPF/8uIQD+8fhXrWsIgD/8043LZeO/qQDAH/7wP99e3xMC4N8f/5gQ8OCeLYLwh3/7Bv+zAQD+X878Bjr9D/7zwn91KATAPwn+KUIA/OHfpl3YrAOA/9kAAP/O7fkOp//Bf57476sEXL11fAz/NPhX/R9EhAD4w/9Wp3UA8N/uW8N/2AET/vPGv00IsNo/3fvRNQTAv2z88zjrYp74h9VJu8cBl4L/q4lP/4P/MvCv+t64eFQXAuCf+P3oEgJCCEfwh3/bduHzG/A/fV9CaPE44HJm/ietL6LnW5z+B/9l4V99YHZCwNFS8A+R18dQ78ePuoUA+BeO/62epwKWiH8IBx4HDH8zf/iHc6v9T0MA/Ad+PzqEgCP4m/nDv/tYts7lDwJ/+M8B/xCWVfbPFf+ulYAHbl6HP/zh33EsW+fwB8kB/1e/eG26iwn+8Id/Y1/bEPC9mhAA/zLw73Kd3/H5Dfg3BQAz//3thcjjf+EPf/j36mv1x98OAfAvC//bvY8FLgv/w08DhL+ZP/w74x9COD7aOifAav9kj/RtHQLgb+YP//34n6kAwB/+8E+Df/UPR7eOj+GfDP9O7bsNawLgv2T8+4/tJeG/CQCl49/n/j/84b+R/+L5jQFP7ZwYmCv+YSb4f3jpSnQIgD/8q/a3W+sASsU/hFG2AeaNf5dB8YUOx//Cv0z8j2sOC9oNAfDv90jfjyJCAPzLwP+Ly4+a+a/aW7ce8w8yZ/zN/OHfdub/1p4QAP+Q5JG+H/WoBMB/mfhPux5gfvg3BgD4wx/+cfivWoQA+PfDPyYEfCdiTQD84b9k/GsDAPzhD/9++O+rBDxZGwLgH/tUvx/3CAHwh3/J+A+0DXBe+L/SYQEg/OHfFv/2ISCX62Pa96PPU/1iQgD8y8Y/hBD+pmYhYEn4n6kAmPnvby/GHAAEf4f8hBCuNYYA+PfFP0UlAP7Lwj92IWBp+G8CAPxD+gsG/vDf+uf6EPDWcU6IT/J+1LTYB/t0CQH37z02GP5znvkPf0tgGfiHkGwbIPzhD/9DfXUh4EpNCCgJ/93Zf9+n+v0kMgTAH/6l4b+pAJSK/yCLAeEP/z191y4+tTcElIx/qt+xawiAP/xLxL8xAMAf/vBPj391z/96QwiY4vrICf+PLl05SvXzuoSA+25ehz/8i8O/NgCUhP/LEUcAwx/+ffCvWl0IeKJhTQD8435etxDwNvwLwz+EEP661U6AZeJ/LgCY+de3agcA/OGfAv8uIWBJD/YZE/+q/+OIEAD/+eP/L8l2AiwX/zPnAMDfzB/+4+Fftbf3hAD4p3mtH/eoBMB/njP/NLcElo3/pgIAf/jDf3z8Vy1CwFj4h4E/y1PhHxMCvl0TAuAP/6XhH0KnbYBl4h/gD/8B8d9XCXg8yRZB+Fftk8gQAH/4LxH/TQUA/vCH/3T4tw0B8O//Wj+59ESnEAB/+C8V/8YAAH/4w39c/Ku+dxpCAPxTvNaTziHg3oY1AfBfBv6hYPxrA0Ap+LfdAvj97WcAwB/+A+JftboQ8FinLYLwb8I/RFQC7k26RRD+Y41l/9pyJ8BffX6jSPzPBYBS8I8aGOEP/xHw7xICrPbv91S/TyNCAPznM/OfMgDPAf892wDhD3/4T4V/1d7dEwLgn+aRvp8muB0Af/jPEf9NBQD+8Id/XvivWoQA+PfDPyYE3BO1RRD+8M8P/xDObQOEfxYXBPzhf6AS8OiZENAf/77v1Vzxr9pPI0MA/OE/V/w3FQD453yxwL9k/A+HAPj3xX8VGQLgD/85478VAOAPf/jnin/Vd6M2BFzrtEXw4VvXwsO3roUQwtHu/z1061p46Mu+4vCPqQR8a+8WQfjPBf9JxvoM8D8NAPCHP/xzx79qdSHgkRqEt7+uQv/hLdz3tSoIPNjw3y8V/xQhAP7wnwv+IZy0fxrgkvDPfz0A/OHf3Hfj4pMHQ8Dq7Gw/uj24EwSWjn/V91lECIB/XvhneUsgI/xbPw0Q/vCHf167Qd7bEwIq/FO2B29dKwb/qnUPAfCH/3zwDyGE1WP//fikNPxfankK4A8uPAN/+GeH/2rPzP+0HYXhWhH4b7d79uz/320/v/Q4/DMby/7q8/davXf/5/IjReEfwoGnAZr5wx/++eLfUAkYEv9z33/p+IcQws86VAK+efMd+Gc6lpn5n7R/GiD84Q//vPGvCQFD438mBJSA/6pHCID/fPAfcyzLBf+9AaB0/McLBvCHfzz+W31j4X+w0rA0/FNUAuAP/9zwbwwA8Ic//OeDf+oFf23b925eLwb/mBBwd00IgD/8c8G/NgAsHv/VyTQXBPzhvyD860LA0vGv+uoW+rUJAfAfH/9Jbv/OBP9VCO3PAVgK/nmsB4A//Pvjn1MrBf/qdXQNAfCHf274n6kAwB/+8J8X/lPP/uuqACXgX7UuIeAbDWsC4A//qfDfBAD4wx/+Zv5jVgXmjn+KEAB/+E+JfwgHzgGAP/zhD3/47z/h7xcRIQD+eeHf628zU/w3FQD4Dx0M4A//tPjnUv6v2ndbLgZcGv5V+0WC2wHwh/+Y+DcGAPjDH/5m/mb+3c727xICvt5liyD84T8A/iGE8HvwXw7+L95+4zjMr3U5wOb46NYcf8XJ/25jVQG8OR3em9MQMLu/2ReXH01+CNRQ+A92+3cB+CfeBjgP/MdbDzDPZ2DnjD9XtJm044E+A1k3+M8L/xCSbQOEP/zhr2mlhgD4zw//TQCAP/wNkJom4MK/HPxD6L0NEP654D/TYCAEaPCH/+T4H/wdF4h/CDWLAOEfe9FPj//LF64e5bzav+nrnm6/sO/orYtHHX+P5az23+5/KLNtgCGE8JOtxwMvebX/vr59W/x226++3DVwlGIss9of/iNuA4T/HD4wc8A/hBDevNh+wvTUTlgoEf9lzArhn2osgz/8Y/vWqT4w8Id/nw/McUQIKBn/Dy4+mdvsH/7wzw7/Xrd/F45/xDbA+eOfdj0A/FN+YI57VALM/M384Q9/+HfrW/f9wMAf/ik/MF1CwJO1IaAM/Of5OGD4wx/+ueC/CQDwh39OT8J6KzoElIX/jzK5DfDxafkf/vCH/3zwD6HVNkD4w3+8D8wqOgSY+efW4A//ueAfCsR/UwGAf9sG/zHwj6sEvFUk/lNXAZpm//CH/6zwn/z9GB//xgAAf/hPjX9MCLhSEwJKmPl/OFEIgD/84T9f/GsDAPzhnwv+Vd+1yBBQAv5bfWOfKHcMf/jnjv94p8DOD/9zAaAE/LtfEPCfEv+qdQ0BJeH/wK1rxyOHgOMQQrh/5/G/8Ic//OeD/5lzAErC/+8vPNPqQvi726/DPwP8Y0LAEw1rAhaM/1iVgDPfvwoB8Id/jvj/5efvtXrf/u3Oh4vDf1MBMPMfdpCGf7q+axefig4BBeAfPrp05eijPdvy+rSPL10JH2+d978bAuAPfzP/+eAfwmYbIPzhnz/+1QfmekQIKAX/rX9Ojv/WP58LAfft3A6AP/zhnzf+pxUA+OcZDOC/7wNzvUclYOn4b4eAvkHgdNZf97/XhIC3j+EP/7nhH0b/LOeBfwgnsU8DhD/8p8M/JgQ8nmSL4Hzw3/66H1+6svm/Nu0nl66EnzTAv/19P2kIAfCHP/zzx/+0AlAe/nnfEoB/lw/M25EhoBT8d9tWEDje/b8K/vav9SR8cumJcz//21uVAPjDH/554n8uAMAf/nPCfxUZAkrFP+1r/eoaaRMC4A//uYz1peBfsw0Q/vCfF/4xlYDHOm0RhP8+/Kv26Z4QAH/4T/J6VifwP3B9rMe9QOEP//T4pwgB8O//SN9PO9wOgD/84T8t/iG0ehog/OGfP/5V3zsRIQD+bX+Pw4N7XQi4tyYEwB/+8J8W/00FoDz8T8I/XLja6sL4we034D8T/Kv2Tu/bAfCPwb9tCIA//MfA/y9+/X6r9/bfT08BLA3/xgCwdPz7Nvjni39MCHj0TAiAfx/8q76fNoQA+MM/p5n/MGP9PPCvDQCl4D/2iVHwHw//qr3bOQTAPwX+VasLAfdEbxGEP/zhn/r6WA93gcIf/tPhv4oKAdfgH9I+2KdNCIA//OE/Pv6ttwHCH/5zxD+mEvDIrWuLx7/vav+u3/OzPSEA/vAfeyyDf4dtgPCH/5zxTxEC4N//d/ysw+0A+MMf/sPjH8KBbYDw/7J9v/dOAPhP/YFZhRBuRISAUvAfY3CvCwHfatwiCH/4x49lf95yB0DJ+G8qAKXi/48ttwLCf/74V+1GgtsB8I/vOxQC4A//MWf+1RbAEvHfGwBKmPkPf0sA/jnh/1UIeLL1e/1wxJqAeeI/3vvxs4YQAH/4K/uPh39jAIA//JeKf/W+vNcjBMC/f19dCPhmwmOD4Q9/+B/uS/M4YPjDf0b4V30xIaDP63ng1rVj+B8KAe/0PjYY/vDv20rAfxVSPA4Y/vCfIf6hRwiIxX/3f//w0pWjaVf7T9/38wMhAP7wh/9w10e/xwEXgn8IIbzYaicA/OeEf0wIeKgmBMTinwc2U/edhJ9ferw2BMAf/jFjWcwOgBLx3wSAkvH/p2Q7AeA/R/yrvvcjQ8A88T/pcZ2nxf+rSsD5EHB3ze0A+MM/1STv/+48BKg0/EOIfRzwgmb+aW4JwH/O+FetawiAfxr8u4QA+MM/9VheKv6bCgD84V86/jEh4ME9WwTh3w3/qv1iTwiAP/zhn/ZndtsGCH/4Lxj/FCEA/vH4r1qEAPjDH/7pfmb7bYDw31kICP8l4l/1fxARAuDfH/99lYBvbIUA+MO/ru/POiwALB3/9tsAF47/S50XAsJ/yfhXrWsImAv+U6327/q1TSEA/vDvO/P/j50FgCXif6YCYOYPf/ifb11CQAjhCP5p8K/6fnk+BBzBH/7DnAFQFv6bAFA6/mOfmAb/eeBftR91DwFHc8N/sGs1wdn+WyEA/vCHfxhjGyD8a9sLt9+Ef0H4r+JCQHjg5nX4J3ywD/zhf6jvz6IPACoT/00FAP4h/LDDOgD4l4V/ZCUgfK8mBMDf8b7wn3bmf/b+f7n41wcAM//oBv/l4p8iBMAf/vAfBv+467xs/M8HAPjDH/5t+o67hgD4D4v/ufcE/vCHf4dtgPBv3Z4/XQcA//Lw39rqd9wlCHy3YU2A1f7p8L+rOicA/sXh/6ed7v/D/+w2QPiHVQjh5YgHA8G/SPw37cNLV1pfK7shAP7pZ/53RTxFEP7lzPz/486H4L/1z2v4D1MqhX8R+B+tQggfRYSA3PDv91qmu+f/q5rDgu78/N3j1GMA/OeP/1R+ZHt9rE4inwa4WPzbH5m6exsA/mXiX7WPelQC4B+H/9Y/HwwB8F8u/n8avf2vbPy/rADA/8zrePnC09NeTPCfHf4xIeA7EWsC4H8e/2ow+/XlxxpDAPzN/EMI4T/vfAj+O+/LepoLdL4zf/jDf9/X/bhHCIB/HP7V99wXAuBfNv5m/ufxrw0ApeO/mupigv/s8V/1CAHw74d/2BMCLteEAPjDv3T82z8NEP617bmtdQDwh3+qSsDQ+C/9kJ9DIQD+y8E/9v4//HcqAPD/qr3ScR0A/OFf17qEgPv3HhsM/7b4Vz/v84YQAP/l4N9lwrZ9/x/+X7U1/JX94Z8e/6rvJ5EhYGz8D/9N53e8b10IuBS5JgD+88XfzL/569bw79eebdgOCH/4V61rCIB/f/y7hgD4zw//r3Us/8P/fBtpG+D88H+1x3ZA+MN/t3UJAffdvA7/hA/2uXkgBMB/2TP//xzo9L+5498YAErHf9BbAvAvDv+4EPA2/BPgvzoQAuC/bPzN/Ls8DRD+URdZdRsA/vA/9Fo/jggB8E/z+9eFgIutjw2Gf074f23C0/+Wgv+5AAD/s63LbQD4w7/ta/24RyVgnPdqefh3CQHwX8bMP4QQfpP49L8l4X/mHAD492vP7FsMCH/477QuIeDbNSEA/vHvx609IQD++ePfd/YP/51zAOA/TIM//Pf1fxIZAoa7JbB8/FctQgD85z/zh3+7r13Df397LXI3APzh3+ZrP7n0RKcQMPZ6gCXiv68ScGETAuCfJ/7tn9uyW/6Hf805APBPN2g+s70YEP7wP9h30jkE3NuwJgD+cb/H/hAA/9zw/9qvPzDzT4R/YwCAf88V1PDPCv8QQvjw4pNHOeIfIioB9ybaIlg6/lXf7Z0QcPvyo0fwzw//sbcBLh3/2gAA//P9XW4DXI09GRD+A39gvkQ/R/yrvk8jQgD80/weVQiAf774/0mH2X9V/od/h3MA4D+fx07Cvxv+1WvJFf+qfZrgdsDYf/O541+9L/A38y8J/57bAMvC//U+iwHhnwX+w/3N0+AfEwLuidoiWM5q/1kN7vBPgv9vehz9WxL+mwoA/NOWUq/eOoY//KPwr9pPI0MA/OG/RPy7lP/h3/77ruE/n/On4V8G/qvIENAH/66/I/zhn9vMv8+YXCL+mwoA/Nv1dbkN8PStY/jDv/fg3iUEfGvvFkH4w3+e+HeZ/f9XxNG/peLfGADgP5/FgPBfLv4pQgD84W/mD/+e2wDhX7U3IqsA8Id/n9fzWUQIgD/8545/39k//HtvA4R/mw+MmT/8h8K/at1DAPzhb+YP/+a+Nfy7f2DeuHgEf/iPin9MCPhmA9pW+8N/afj/V4dz/+Hfahsg/PvO/EMI4SjxYkD4l4t/1X7WIwTAH/5zwf9PBjj3H/6ttgHCPwX+Zv7wH+r3jwkBXWda8If/VPgPsf0a/q22AcK/zQfmzQ63AY4SLAaEP/xXCSsB8Id/zvj/ccTiP/j33gYI/74fGDN/+I/5XnUJAXe3RB3+8DfzXz7+OwEA/l0/MLFVAPjDP2Xfz3cR7hEC4A//qfHvOvuHf+9tgPAfcuYfn1zhD/9DfV++jhQhAP7wN/MvB//TbYDw7/OB6VIFeGqnCgB/+KfAv2pdQkAI4ejAv8Mf/qPj32X2/9uGY3/h3378WOf4gZnTzH+Y5Ap/+HfDv2cIgD/8ZzXz7z6+wr9u/Fjn9oGZI/7HHasA8If/EPhX/b/oVwmAP/wnwT/V7B/+7cePNfzHnfkH+MN/QPyr1jEEwB/+Zv6F4b+pAMC///fsUgV4snZHAPzhnwb/1CEA/vAfGv8Us3/4dx8/1jl8YEqc+Z8NAfCHf1r8q/bLniEA/vDPCX8z/7Tjx3rqD8xS8F+FEN7qUAWAP/yHxn/VMwTAH/5D49+1/bbVI3/h32b8WIVWjwOG/1BVgScPLAiEP/z74h9bCYA//MfAv+/sH/7x+J+pAMA/zc+LqwLAH/7D4d81BMAf/rnN/Otm//Dvh/8mAMA/7c/rEgKu3HoL/vAfHP+q758PhAD4w38s/Pss/IN/f/xDGGUbYHll/z6JF/7wHwr/qjWFAPjDfyz8046R8I/Bf1MBgH/6vmsRVQD4w39o/Lfa8d5/hz/8B8T/jyJn//BPh39jAID/+Km27lYA/OE/8N/nGP7wzxl/M//h8K8NAPBP13ctwYJA+MN/4EAKf/iPhn/XVs3+4Z8e/4G2AcI/tj2xUwWAP/xHfT3wh//A+MfM/uE/DP5nKgDwH2LgOwnXLz4VFQLgD/88zoiAP/ynwf+3dz4E/wHx3wQA+A+Df9XfNQTAH/45VargD/+xrzn4D49/CMm2AcK/ywfmUHu8YUEg/OEPf/jPEf+us3/4D4//pgIA/+Hx71oFeLz3egD4wx/+8J8f/r87d94//IfAvzEAwH+amX+61wN/+MMf/tPj37/Bfyj8awMA/IfBfxVCeDuiCgB/+A+x2h/+8B8D/36zf/gPiX+PbYDwj/3AdA0Bj3VaDwB/+B/G32p/+MMf/mcqAPAfHv9UDf7whz/8c8a/X4P/GPhvAgD8x8W/TxUA/vAfAv8w2rUD/xLwj5/9w38s/EPotA0Q/ik/MO9EhAD4wx/+8Ic//FP9vHXMBwb+05TKHj23HgD+8Ic//OeLf3bXR0H4NwYA+I+Df9cqAPzhD3/454p/TPty9g//KfCvDQDwH3fm3zUEfFkFgD/84Q//vPCPK/3Dfyr8zwUA+I+Lf9X3bucQcA3+8LfaH/7wh3+va2cN/2nxj22P3LoGf/jDH/6zwz+r66Ng/DcVAPhPj/+7vdYDwB/+/fAPSa8d+JeCf0z73Z0Pwj8D/EM4tw0Q/lPO/LuGgO0qAPzhD3/4j41/99I//HPBf1MBgP/0+Fd9NyJCAPzhD3/4wx/+XX+PNfzzwT+2PdywHgD+8Ic//HPAf/rPK/xDfQCAf27434hYD1AXAuAPf/jDPwf8q9k//PPBP4ST2KcBwn/YvpNw4+KToU+DP/zH+SzDvyT8Y0Il/PPEf882QPhPiX/V917HEFBVAeAPf/jDf4jf8X9E3veHf374h9D5aYDwHwv/2JZkPQD84Q9/+PfEP4vrA/57r481/PPG/72IWwEP9VkPAP8i8e/2XsEf/u1m//DPF/9NBQD+ec/8+4YA+MMf/vCHP/xDmwAA/7zK/qsQwvuRIQD+8Ic//OEP/9AmAMA/P/yrFhMCHmzzzAD4wx/+8Id/UfifCwDwzxf/lCEA/vCHP/zhXzb+rbcBwj8P/Pu0B+u2CMK/SPyt9od/avwnvz7gH3V9rAf/Y8E/Of4fRB4SdKYSAH/4wx/+ifD/f1vn/MN/HviHcGAbIPzzw3/VMwQ8cOsa/OHfosEf/vBfMv6bCgD854V/30rAAzevTXiBwh/+8Ic//KfGf28AgH/e+PcPAdfhD3/4wx/+heLfGADgPw/8q74fRYaA7928Dn/4wx/+8C8Q/9oAAP954V+1VCEA/qXiP/X7AX/4w3/s62Od6wcG/t2/tm8IgH+pq/3hD3/4l4b/mQoA/OeNf9U+THw7AP7whz/84b88/DcBAP7LwH/VMwR8tyYEwL8M/KcNFPCHP/ynuD7W8F8W/tW/fHjpSu8QAH/4wx/+8F8m/psKAPyXhX/1WvqEAPiXccIf/OEP/zLxbwwA8J8//tW/fhQZAr4TuSYA/vCHP/zhnz/+IYSw+qc/eO0E/svEf7vtW+R3qP1kK0TAfxn4W/C3fPz/KBJ++BeCf+i6DRD+s8Q/9KgEbFcD4A9/+MMf/svAP4Qu2wDhP1v8q/bjBCEA/vCHP/zhP3/8NwEA/svHf5UgBNy/d5sg/OEPf/jDfy74hxDC6qWdNQDwXy7+2+27PdYEhBDCx5euwB/+8M9kcO8DP/zLxH9TAYB/Wfj3rQScrQbAH/7whz/854Z/YwUA/svGf7fvOz2qAZ9cegL+8If/DPH/3Z0PTnt9wH96616q2wYI/2LwTxECqiAAf/jDf5yxrO+sH/7wr98GCP/i8A/h7F7/mHbfzbfhD3/4wx/+M8E/hN1tgPAvEv+qfdwzBHy7JgTAH/7whz/887Ru9dIfvHYCf/hv99/f83ZACCF8OugtAfjDvyz8+8IPf/jX9a1++AevncAf/nWtbxD46c4CQfjDH/7j4/+701X+8If/uf/th3/46gn84d/Ud1+CasB2EIA//OHfri/VrB/+8F81jGPrSV8A/LPGP4Tz2/xi2r2nawPgD3/4wx/+eeBfWwGAP/ybTvjbt9K/bfusJlDAH/7wTw8//OG/F//Q9WmA8C8W/xC+XNjXt92zEyLgD3/4wx/+4+N/pgIAf/i3Pdv/2wkqASGE8LM9gQL+8C8F/xTwwx/+XfHfBAD4wz/mwT4pgsDPGm8JwB/+8G8H/0P5XB/wnw3+IYSwerlhFwD84d/m6+5NXA2AP/xLwP+Pk8364Q//OPz3BgD4w7/tz0wVAkII4eeXHoc//BeLfyr44Q//vvg3BgD4wz/mZw4ZBOAP/znjnx7+jK4P+M8S/xDC+XMA4A//2J/5WYJdAlX75s134A9/+MMf/gPhf64CAH/4p3o99ySsBvyi4bYA/OGfM/7DwA9/+CfCfzsAwB/+qV9PyhCwGwTgD/9c8U8JP/zhPxT+mwoA/OE/5PvxrcRB4JepFwrCH/4JBvdh4Yc//NPiH0IIq1cG2AYIf/jX9Q0dBOAP/ynwTw3/b+98KN/rA/6LwX9vAIA//IfoSx0CqiAAf/iPjf+fJIYf/vAfE//GAAB/+A/94d1e5Z+y/XPbqgD84R8xuA+BfgV/1tcH/BeHf20AgD/8x/zwDhkE4A//VPgPDT/84T82/ucCAPzhP/aHt+q/e6Ag8KvdBYPwh3+HwX0M+OEP/0nw3w4A8If/VPhXbagQsAkDlx+DP/wPDu5DoQ9/+OeE/6YCAH/4T41/GDEI/PryY/CH/7n35Wsjww9/+E+JfwghrF6N3AYIf/gPgf923zcGDgJVGIB/ufh/7dfvD36N1cEPf/hPjf/eAAB/+E+J/3YbIwh83rEqAP954z8l/PCHfw74NwYA+MM/F/y3+74+QhCowgD8l4f/GOgfgh/+8M8F/9oAAH/454j/dhsrCIQQws3e6wXgPyX+fzoS+iGE8F+1h/jAH/554n8uAMAf/rnjP1UQqNqtmkAA/3zwHxP8bfjjPsvwh/+E+G8HAPjDf0747/bdNXEYgP90+E+JfvxnGf7wnxb/TQUA/vCfM/7bH5q7Pn83TNVubwIB/IfE/88mAL8JfvjDf674hxDC6rU92wDhD/854b/dd+eEQaBqX1x+FP4J8J8S/H3wwx/+c8b/QACAP/znif9uyyEMbIcC+De3P88A+6r95sCiPvjDf8747wkA8If/MvDf7rucURDYbf+SLBjMA/+coK+DP/1nGf7wzwv/hgAAf/gvD//dlnMY2G7/2ikY5If/X2QMfR36w3yW4Q///PCvCQDwh//y8d/tuzSTMLCv/e/Lj4z6fvzl5+/N/m/2m4j7+vCH/2LwPxsA4A//8vAPCwwDWnP7zx739eEP/yXhv1UBgD/84b/bf1EYWAz643+W4Q//vPE/DQCvnMAf/vA/3HdBIJgd+NNgA3/4549/CCdh9fofvnIy+R8E/vDPHP/da/XC5zdIm1H7j4FK+/CH/1LxDyE0BwD4wx/+7Qf3OwSCkcF/eNLBHf7wnzv+jQEA/vCHf7/B/W8FggHBn3Zwhz/8l4B/bQCAP/zhP8zg/jdCQav2f3ewz2lwhz/8F4P/bgCAP/zhP/7g/teFBoN/P4U+7m8Hf/jDvw/+ZyoA8Ic//PMb3P9q5uHg3xtL933+PvCHP/z74h9CCL8Hf/jDP9/Bve0Jf/9r5JP5/q3X7B3+8If/1PiHEMLqjdG2AcIf/vDv8+Gd7PWsTiZ+P+APf/inxj+EENbwhz/84Q9/+MO/LPwbAwD84Q9/+MMf/vBfLv61AQD+8Ic//OEPf/gvG//VbgCAP/zhD3/4wx/+y8f/TAUA/vCHP/zhD3/4l4H/JgDAH/7whz/84Q//cvAPIYQ1/OEPf/jDH/7wLwv/TQUA/vCHP/zhD3/4l4N/YwCAP/zhD3/4wx/+y8W/NgDAH/7whz/84Q//ZeOfYBsg/OEPf/jDH/7wnxv+ZyoA8Ic//OEPf/jDvwz8NwEA/vCHP/zhD3/4l4N/CFHbAOEPf/jDH/7wh/+c8d9UAOAPf/jDH/7wh385+DcGAPjDH/7whz/84b9c/GsDAPzhD3/4wx/+8F82/ucCAPzhD3/4wx/+8F8+/mfOAYA//OEPf/jDH/5l4L+pAMAf/vCHP/zhD/9y8A+hcRsg/OEPf/jDH/7wXyr+mwoA/OEPf/jDH/7wLwf/mgAAf/jDH/7whz/8l47/TgCAP/zhD3/4wx/+JeC/FQDgD3/4wx/+8Id/KfifbgOEP/zhD3/4wx/+JeEfwkns0wDhD3/4wx/+8If/XPEPIeppgPCHP/zhD3/4w3/O+IfQ+WmA8Ic//OEPf/jDf+74NwYA+MMf/vCHP/zhv1z8awMA/OEPf/jDH/7wXzb+5wIA/OEPf/jDH/7wXz7+LZ4GCH/4wx/+8Ic//JeG/6YCAH/4wx/+8Ic//MvBP4QD2wDhD3/4wx/+8If/8vDfVADgD3/4wx/+8Id/OfjvDQDwhz/84Q9/+MN/mfg3BgD4wx/+8Ic//OG/XPxrAwD84Q9/+MMf/vBfNv6r0OEcAPjDH/7whz/84b8M/M9UAOAPf/jDH/7wh38Z+G8CAPzhD3/4wx/+8C8H/xB6PA4Y/vCHP/zhD3/4zxP/TQUA/vCHP/zhD3/4l4N/YwCAP/zhD3/4wx/+y8W/NgDAH/7whz/84Q//ZeMfvw0Q/vCHP/zhD3/4zxb/MxUA+MMf/vCHP/zhXwb+mwAAf/jDH/7whz/8y8E/hC7bAOEPf/jDH/7wh/8i8N9UAOAPf/jDH/7wh385+DcGAPjDH/7whz/84b9c/GsDAPzhD3/4wx/+8F82/vu3AcIf/vCHP/zhD/9F4n+mAgB/+MMf/vCHP/zLwH8TAOAPf/jDH/7wh385+Iewuw0Q/vCHP/zhD3/4Lx7/TQUA/vCHP/zhD3/4l4P/VwEA/vCHP/zhD3/4F4P/lwEA/vCHP/zhD3/4F4X/ahXC/wd7V5vQJ6boUwAAAABJRU5ErkJggg=="
ICON_APPLE_180_B64 = "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"
ICON_FAVICON_32_B64 = "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAC2klEQVR42rWXwW7TQBCG/137NXLIu3BB4tTGTqNKqOJSItqS1i0lQuJU1RXECXEKVVWJAxcaO0WIB+CCeK7lYK+73szYTlrmUu12vd/OzD+TXfGs9RkSChKAhIKT/5UAHKEUNS+Fta5+XpTGej8BuAxcOYI+1BrwbL9sLEy4hIJrQVTu+WPCTc9VDi8O4q4DH91dgLKzzkkV3PRcOXk0hNeaNQr79C7EKhZ5AQfXewsJQHRb8crwd5unZNiHi1FpXewdcXD9jRC9VsyqffbjvNjszeZbMufvFx+jsHMc2GEfpOPi22v/kIJnonwIXOb/p3J+6R0W3+8mE06kSnJhbwJ3kK3jBHft3x+CqxBZlfM6eB6BoELt+OoPAAA7yZSukIfAT3PRBWlUpXZ8818DALaTeDladp1r4wRnw7UdpGM4APrpJKIEB0MvZrRcGwJLWOZGYec4GC5GEYDALHk97qcT3PiDgElV2TF9SKrDcXWuc271nNKYa8lpdx8AsDG/NFJlaaDwvibnVfYi+cT+HpQOKSwNLC1YA67teTIle4PpoJ53yQW54JgwR0QalqyXxHotAOBX91VACdF1iOajBWd6EaQRmXPO0u4+HKjAFBwlRFlXgvq0sXfUOAU53OoNVoVRVXDWOQEADBcjsr1eZf09Wgf+9PYLAOD3Vp+vgqqGoZvMjT8IdHul4N58FtlwW19sFVQ2DIFSk9Ht1fb8Z3cvsCFsCWoNmDmPvExjg3Rcd5nAd/+gMux63ZPbKwDAn62XJbgDQFYJbi+dsHCjcqK14WYV2DlvcJkoX0gq4LDCXvoF5h4N5mWirr3Wwf/2drmHjxBh+wIOrGuZFfadZLpSqWljw35//RfiQzu0Hw1kzrez1trYmsAlFMSoHeoFqk5werwxvyShS02Gh0NCCQeAGLfP7RdLkyfWUs6p+Tq4hIJrhV0Ur6T/Axf2vMu9WIp7++PABT0P/AM4pSC7sPntSgAAAABJRU5ErkJggg=="

MANIFEST_JSON = json.dumps({
    "name": APP_NAME,
    "short_name": APP_SHORT_NAME,
    "description": "Sidereal Vedic birth charts (Rashi & Navamsa), Nakshatra, and Vimshottari Dasha.",
    "start_url": "/",
    "scope": "/",
    "display": "standalone",
    "background_color": THEME_COLOR,
    "theme_color": THEME_COLOR,
    "orientation": "portrait-primary",
    "icons": [
        {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "/icon-512-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
})

# Minimal offline-friendly service worker:
#  - App-shell (the "/" GET page) and static assets are cached on install.
#  - Static GET requests (manifest, icons, this script) use cache-first.
#  - Navigations (page loads) use network-first with a cached-shell
#    fallback, so a flaky connection still shows something instead of the
#    browser's default offline error.
#  - POST requests (/generate, the chart form submit) always need the
#    server and are never intercepted.
SERVICE_WORKER_JS = """
const CACHE_NAME = "vedic-chart-v12";
const SHELL_URLS = [
  "/",
  "/play-with-chart",
  "/i18n.js",
  "/manifest.json",
  "/icon-192.png",
  "/icon-512.png",
  "/icon-512-maskable.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(SHELL_URLS)).catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((names) =>
      Promise.all(names.filter((n) => n !== CACHE_NAME).map((n) => caches.delete(n)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return; // never intercept form POSTs

  if (req.mode === "navigate") {
    event.respondWith(
      fetch(req).catch(() => caches.match("/"))
    );
    return;
  }

  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, copy));
          return res;
        })
        .catch(() => cached);
    })
  );
});
"""


def _icon_response(b64_data):
    return Response(base64.b64decode(b64_data), mimetype="image/png")


@app.route("/manifest.json")
def manifest():
    return Response(MANIFEST_JSON, mimetype="application/manifest+json")


@app.route("/service-worker.js")
def service_worker():
    return Response(SERVICE_WORKER_JS, mimetype="application/javascript")


# ---------------------------------------------------------------------------
# /i18n.js - the shared Tamil/English runtime
# ---------------------------------------------------------------------------
# Every page (the generator, both admin pages, and chart_playground.html)
# loads this one script, so all of them translate against the single set of
# dictionaries in i18n.py rather than keeping their own copies.
#
# Markup contract:
#   data-i18n="key"                   -> textContent = t(key)
#   data-i18n-html="key"              -> innerHTML   = t(key)   (string has markup)
#   data-i18n-attr="placeholder:key"  -> setAttribute, semicolon-separated pairs
#   data-i18n-term="kind:Value"       -> textContent = term(kind, "Value")
#
# Anything built at runtime (dasha rows, the dashboards) calls I18N.t /
# I18N.term directly and re-renders from an I18N.onChange callback.
#
# The chosen language lives in localStorage and is stamped onto
# <html data-lang="..."> by I18N.boot() before first paint, which is also
# what the dual-rendered chart SVGs are toggled on (see the [data-lang-svg]
# rules in PAGE_TEMPLATE).

I18N_RUNTIME_JS = """
window.I18N = (function () {
  "use strict";

  var UI = __UI_JSON__;
  var TERMS = __TERMS_JSON__;
  var LANGS = __LANGS_JSON__;
  var NAMES = __NAMES_JSON__;
  var DEFAULT = "__DEFAULT_LANG__";
  var STORAGE_KEY = "vedic-chart-lang";

  var current = DEFAULT;
  var listeners = [];

  function stored() {
    try {
      var saved = window.localStorage.getItem(STORAGE_KEY);
      return LANGS.indexOf(saved) !== -1 ? saved : null;
    } catch (err) {
      return null; // private mode / storage disabled - just use the default
    }
  }

  function fill(text, params) {
    if (!params) return text;
    return text.replace(/\\{(\\w+)\\}/g, function (match, name) {
      return Object.prototype.hasOwnProperty.call(params, name) ? params[name] : match;
    });
  }

  // Translated UI string. Falls back to English, then to the key itself, so
  // an untranslated key shows up as text instead of "undefined".
  function t(key, params) {
    var table = UI[current] || {};
    var text = table[key];
    if (text === undefined) text = (UI[DEFAULT] || {})[key];
    if (text === undefined) text = key;
    return fill(text, params);
  }

  // Translated vocabulary item, e.g. term("planet", "Jupiter").
  function term(kind, key) {
    var group = TERMS[kind];
    if (!group) return key;
    var table = group[current] || {};
    var text = table[key];
    if (text === undefined) text = (group[DEFAULT] || {})[key];
    return text === undefined ? key : text;
  }

  // House ordinals: "3rd" in English, "3ஆம்" in Tamil.
  function ordinal(n) {
    if (current === "ta") return n + "\\u0b86\\u0bae\\u0bcd";
    var suffixes = ["th", "st", "nd", "rd"];
    var v = n % 100;
    return n + (suffixes[(v - 20) % 10] || suffixes[v] || suffixes[0]);
  }

  function ordinalList(arr) {
    return arr.map(ordinal).join(", ");
  }

  function applyAttrs(el) {
    // "placeholder:form.city_placeholder;title:pg.col_arrow_title"
    el.getAttribute("data-i18n-attr").split(";").forEach(function (pair) {
      var sep = pair.indexOf(":");
      if (sep === -1) return;
      var attr = pair.slice(0, sep).trim();
      var key = pair.slice(sep + 1).trim();
      if (attr && key) el.setAttribute(attr, t(key));
    });
  }

  // Re-translate every tagged node under `root` (default: the document).
  function apply(root) {
    var scope = root || document;
    scope.querySelectorAll("[data-i18n]").forEach(function (el) {
      el.textContent = t(el.getAttribute("data-i18n"));
    });
    scope.querySelectorAll("[data-i18n-html]").forEach(function (el) {
      el.innerHTML = t(el.getAttribute("data-i18n-html"));
    });
    scope.querySelectorAll("[data-i18n-attr]").forEach(applyAttrs);
    scope.querySelectorAll("[data-i18n-term]").forEach(function (el) {
      var spec = el.getAttribute("data-i18n-term");
      var sep = spec.indexOf(":");
      if (sep === -1) return;
      el.textContent = term(spec.slice(0, sep), spec.slice(sep + 1));
    });
    if (!root) {
      var titleEl = document.querySelector("title[data-i18n]");
      if (titleEl) document.title = t(titleEl.getAttribute("data-i18n"));
    }
  }

  function set(lang) {
    if (LANGS.indexOf(lang) === -1 || lang === current) return;
    current = lang;
    try {
      window.localStorage.setItem(STORAGE_KEY, lang);
    } catch (err) {
      /* not fatal - the switch still works for this page view */
    }
    document.documentElement.setAttribute("data-lang", lang);
    document.documentElement.setAttribute("lang", lang);
    syncButtons();
    apply();
    listeners.forEach(function (fn) {
      try {
        fn(lang);
      } catch (err) {
        console.error("i18n listener failed", err);
      }
    });
  }

  function syncButtons() {
    document.querySelectorAll("[data-lang-btn]").forEach(function (btn) {
      var active = btn.getAttribute("data-lang-btn") === current;
      btn.classList.toggle("active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }

  // Called from an inline <head> script so the right language is on
  // <html> before the page paints - no flash of English.
  function boot() {
    current = stored() || DEFAULT;
    document.documentElement.setAttribute("data-lang", current);
    document.documentElement.setAttribute("lang", current);
  }

  function onChange(fn) {
    listeners.push(fn);
  }

  function ready() {
    boot();
    syncButtons();
    apply();
    document.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-lang-btn]");
      if (btn) set(btn.getAttribute("data-lang-btn"));
    });
  }

  boot();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ready);
  } else {
    ready();
  }

  return {
    t: t,
    term: term,
    ordinal: ordinal,
    ordinalList: ordinalList,
    apply: apply,
    set: set,
    boot: boot,
    onChange: onChange,
    names: NAMES,
    languages: LANGS,
    get lang() {
      return current;
    },
  };
})();
"""


def _build_i18n_js():
    """Bake the dictionaries into I18N_RUNTIME_JS once, at import time."""
    return (
        I18N_RUNTIME_JS
        .replace("__UI_JSON__", json.dumps(i18n.UI, ensure_ascii=False))
        .replace("__TERMS_JSON__", json.dumps(i18n.TERMS, ensure_ascii=False))
        .replace("__LANGS_JSON__", json.dumps(list(i18n.LANGUAGES)))
        .replace("__NAMES_JSON__", json.dumps(i18n.LANGUAGE_NAMES, ensure_ascii=False))
        .replace("__DEFAULT_LANG__", i18n.DEFAULT_LANGUAGE)
    )


I18N_JS = _build_i18n_js()


@app.route("/i18n.js")
def i18n_js():
    return Response(I18N_JS, mimetype="application/javascript; charset=utf-8")


# The language toggle, shared verbatim by every page. Each page styles
# `.lang-switch` itself so the control sits naturally in its own header.
LANG_SWITCH_HTML = """
<div class="lang-switch" role="group" aria-label="Language">
  <button type="button" data-lang-btn="en" aria-pressed="true">English</button>
  <button type="button" data-lang-btn="ta" aria-pressed="false">&#2980;&#2990;&#3007;&#2996;&#3021;</button>
</div>
"""

# Shared styling for that toggle - injected into each page's <style> block
# so the three templates stay visually consistent without a stylesheet file.
LANG_SWITCH_CSS = """
  .lang-switch {
    flex-shrink: 0;
    display: inline-flex;
    gap: 2px;
    padding: 3px;
    border: 1.5px solid rgba(212,175,55,0.45);
    border-radius: 999px;
    background: rgba(212,175,55,0.06);
  }
  .lang-switch button {
    padding: 5px 11px;
    font-family: 'Cinzel', serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: rgba(224,213,197,0.7);
    background: transparent;
    border: none;
    border-radius: 999px;
    cursor: pointer;
    white-space: nowrap;
    transition: background 0.15s, color 0.15s;
  }
  .lang-switch button:hover { color: #e0c477; }
  .lang-switch button.active {
    background: linear-gradient(135deg, #d4af37 0%, #f0d878 100%);
    color: #1c1710;
    box-shadow: 0 2px 10px rgba(212,175,55,0.35);
  }
  /* Tamil glyphs carry more detail per character than Latin, so a small
     size bump keeps them comfortably legible at the same layout width. */
  html[data-lang="ta"] body { font-size: 15px; }
"""

# Inline <head> snippet: stamps the saved language onto <html> before the
# first paint, so a Tamil user never sees a flash of English (and the
# CSS-toggled chart SVGs pick the right variant immediately).
LANG_BOOT_SCRIPT = """
<script>
  (function () {
    try {
      var saved = window.localStorage.getItem("vedic-chart-lang");
      if (saved === "en" || saved === "ta") {
        document.documentElement.setAttribute("data-lang", saved);
        document.documentElement.setAttribute("lang", saved);
      }
    } catch (err) {}
  })();
</script>
"""

# Expose the toggle markup, its CSS and the boot script to every template,
# so no render call has to pass them around. `t` renders the English text
# that ships in the HTML - the browser re-renders it from the same key the
# moment /i18n.js runs, so server and client never disagree.
app.jinja_env.globals["lang_switch"] = LANG_SWITCH_HTML
app.jinja_env.globals["lang_switch_css"] = LANG_SWITCH_CSS
app.jinja_env.globals["lang_boot"] = LANG_BOOT_SCRIPT
app.jinja_env.globals["t"] = i18n.t
app.jinja_env.globals["term"] = i18n.term


# "Play with Chart" - a standalone drag-and-drop South Indian chart page
# (chart_playground.html, copied from the original horoscope-builder
# prototype). It reads its planet positions from a `?positions=` JSON query
# param via client-side JS (see build_playground_url), so the file itself
# never needs server-side templating - it's served as-is.
_PLAYGROUND_HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chart_playground.html")
with open(_PLAYGROUND_HTML_PATH, "r", encoding="utf-8") as _f:
    PLAYGROUND_HTML = _f.read()


@app.route("/play-with-chart")
def play_with_chart():
    return Response(PLAYGROUND_HTML, mimetype="text/html")


@app.route("/icon-192.png")
def icon_192():
    return _icon_response(ICON_192_B64)


@app.route("/icon-512.png")
def icon_512():
    return _icon_response(ICON_512_B64)


@app.route("/icon-512-maskable.png")
def icon_512_maskable():
    return _icon_response(ICON_512_MASKABLE_B64)


@app.route("/apple-touch-icon.png")
def apple_touch_icon():
    return _icon_response(ICON_APPLE_180_B64)


@app.route("/favicon.png")
def favicon():
    return _icon_response(ICON_FAVICON_32_B64)


# ---------------------------------------------------------------------------
# Astrology helpers (same logic as the standalone script, with the sign-name
# mismatch and the house-calculation bug fixed)
# ---------------------------------------------------------------------------

SIGN_ORDER = [
    "Ari", "Tau", "Gem", "Can", "Leo", "Vir",
    "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis",
]
SIGN_NAME_MAP = {
    "Ari": "Aries", "Tau": "Taurus", "Gem": "Gemini", "Can": "Cancer",
    "Leo": "Leo", "Vir": "Virgo", "Lib": "Libra", "Sco": "Scorpio",
    "Sag": "Saggitarius", "Cap": "Capricorn", "Aqu": "Aquarius", "Pis": "Pisces",
}

PLANETS = {
    "sun": (chart.SUN, "Su"),
    "moon": (chart.MOON, "Mo"),
    "mars": (chart.MARS, "Ma"),
    "mercury": (chart.MERCURY, "Me"),
    "jupiter": (chart.JUPITER, "Ju"),
    "venus": (chart.VENUS, "Ve"),
    "saturn": (chart.SATURN, "Sa"),
}

# Different Kerykeion versions have used different attribute names for the
# lunar node - try them in order so this keeps working across versions.
NODE_ATTR_CANDIDATES = [
    "mean_north_lunar_node", "mean_node",
    "true_north_lunar_node", "true_node",
]


def get_rahu_data(subject):
    for attr in NODE_ATTR_CANDIDATES:
        data = getattr(subject, attr, None)
        if data is not None:
            return data
    raise AttributeError(
        "Could not find lunar node data on this Kerykeion subject. "
        f"Tried: {NODE_ATTR_CANDIDATES}"
    )


def build_vedic_subject(name, year, month, day, hour, minute, lat, lng, tz_str, city="Unknown"):
    """Create a sidereal (Lahiri) Kerykeion subject, fully offline (no GeoNames call)."""
    return AstrologicalSubject(
        name=name,
        year=year, month=month, day=day, hour=hour, minute=minute,
        lat=lat, lng=lng, tz_str=tz_str, city=city,
        online=False,
        zodiac_type="Sidereal",
        sidereal_mode="LAHIRI",
    )


def house_from_signs(planet_sign_abbr, ascendant_sign_abbr):
    """Whole-sign house number (1-12) of a planet, relative to the Ascendant's sign."""
    asc_idx = SIGN_ORDER.index(ascendant_sign_abbr)
    planet_idx = SIGN_ORDER.index(planet_sign_abbr)
    return ((planet_idx - asc_idx) % 12) + 1


# SIGN_NAME_MAP above misspells Sagittarius ("Saggitarius") - that's already
# baked into other pages of the app, so it's left alone there, but the
# playground page's sign list is spelled correctly and needs the fix.
SIGN_NAME_FULL = dict(SIGN_NAME_MAP, Sag="Sagittarius")

# Kerykeion attribute name -> short planet code used on the "Play with
# Chart" playground page (chart_playground.html).
PLAYGROUND_PLANET_CODE = {
    "sun": "Sun", "moon": "Mon", "mars": "Mar", "mercury": "Mer",
    "jupiter": "Jup", "venus": "Ven", "saturn": "Sat",
}


def build_rashi_positions(subject):
    """Sun..Saturn, Rahu, Ketu and the Ascendant's Rashi (D1) sign, keyed by
    the short planet codes the playground page's chart expects - e.g.
    {"Asc": "Aries", "Sun": "Leo", "Mon": "Taurus", ...}.
    """
    ascendant_abbr = subject.first_house["sign"]
    positions = {"Asc": SIGN_NAME_FULL[ascendant_abbr]}
    for attr, code in PLAYGROUND_PLANET_CODE.items():
        sign_abbr = getattr(subject, attr)["sign"]
        positions[code] = SIGN_NAME_FULL[sign_abbr]

    rahu_sign = get_rahu_data(subject)["sign"]
    positions["Rahu"] = SIGN_NAME_FULL[rahu_sign]
    rahu_idx = SIGN_ORDER.index(rahu_sign)
    ketu_sign = SIGN_ORDER[(rahu_idx + 6) % 12]
    positions["Ketu"] = SIGN_NAME_FULL[ketu_sign]
    return positions


def build_playground_url(subject):
    """URL for the 'Play with Chart' button - the Rashi positions travel as
    a JSON query param the playground page's own JS reads on load."""
    positions = build_rashi_positions(subject)
    return "/play-with-chart?positions=" + urllib.parse.quote(json.dumps(positions))


# jyotichart writes each label as a single <text> node with no nested
# markup, which makes the handful of English words it adds itself (the "Asc"
# marker and the centre "Chart : Lagna" line) safe to swap by exact content
# match. Doing it on the finished markup rather than through the library's
# own `language=` argument keeps this working on jyotichart versions that
# predate that argument, and Tamil isn't one of its supported languages
# anyway (it ships english/kannada/hindi only).
_SVG_TEXT_NODE_RE = re.compile(r"(<text\b[^>]*>)([^<]*)(</text>)")


def _localize_chart_svg(svg_markup, lang):
    """Translate the labels jyotichart generates on its own.

    Planet glyphs are already passed in translated, so they never match a key
    here; the person's name is left alone for the same reason.
    """
    if lang == i18n.DEFAULT_LANGUAGE:
        return svg_markup

    replacements = {
        "Asc": i18n.term("planet_abbr", "Ascendant", lang),
        "Chart : Lagna": f"{i18n.t('chart.word', lang)} : {i18n.t('chart.rashi', lang)}",
        "Chart : Navamsa": f"{i18n.t('chart.word', lang)} : {i18n.t('chart.navamsa', lang)}",
    }

    def replace(match):
        content = match.group(2).strip()
        return match.group(1) + replacements.get(content, match.group(2)) + match.group(3)

    return _SVG_TEXT_NODE_RE.sub(replace, svg_markup)


def _read_chart_svg(output_dir, filename):
    """Read back the SVG jyotichart just wrote, whatever encoding it used.

    jyotichart's draw() has been observed writing UTF-16 (with BOM) on some
    systems and plain UTF-8 on others, so detect and decode accordingly.
    """
    svg_path = os.path.join(output_dir, f"{filename}.svg")
    with open(svg_path, "rb") as f:
        raw_bytes = f.read()

    if raw_bytes.startswith(b"\xff\xfe") or raw_bytes.startswith(b"\xfe\xff"):
        return raw_bytes.decode("utf-16")
    if raw_bytes.startswith(b"\xef\xbb\xbf"):
        return raw_bytes.decode("utf-8-sig")
    return raw_bytes.decode("utf-8", errors="replace")


def render_chart_svg(subject, style, output_dir, lang=i18n.DEFAULT_LANGUAGE):
    """Build a South/North Indian chart with jyotichart and return the raw SVG markup.

    Planet glyphs are drawn in `lang` - "Su"/"Mo"/"Ma" in English, "சூ"/"சந்"/"செ"
    in Tamil. Retrograde classical planets get a retrograde marker appended
    directly to their glyph on the chart itself (e.g. "Ma(R)" / "செ(வ)")
    instead of relying on a separate table column.
    """
    ascendant_abbr = subject.first_house["sign"]
    ascendant_full = SIGN_NAME_MAP[ascendant_abbr]
    retro_suffix = i18n.RETROGRADE_SUFFIX.get(lang, i18n.RETROGRADE_SUFFIX["en"])

    ChartClass = chart.SouthChart if style == "south" else chart.NorthChart
    mychart = ChartClass("Lagna", subject.name, IsFullChart=True)
    mychart.set_ascendantsign(ascendant_full)

    for attr, (planet_const, symbol) in PLANETS.items():
        planet_data = getattr(subject, attr)
        sign_abbr = planet_data["sign"]
        house_num = house_from_signs(sign_abbr, ascendant_abbr)
        is_retro = planet_data.get("retrograde", False)
        glyph = i18n.planet_abbr(symbol_to_label(symbol), lang)
        display_symbol = f"{glyph}{retro_suffix}" if is_retro else glyph
        mychart.add_planet(planet_const, display_symbol, house_num, retrograde=is_retro)

    rahu_data = get_rahu_data(subject)
    rahu_sign = rahu_data["sign"]
    rahu_house = house_from_signs(rahu_sign, ascendant_abbr)
    mychart.add_planet(chart.RAHU, i18n.planet_abbr("Rahu", lang), rahu_house, retrograde=True)

    rahu_idx = SIGN_ORDER.index(rahu_sign)
    ketu_sign = SIGN_ORDER[(rahu_idx + 6) % 12]
    ketu_house = house_from_signs(ketu_sign, ascendant_abbr)
    mychart.add_planet(chart.KETU, i18n.planet_abbr("Ketu", lang), ketu_house, retrograde=True)

    # Turn off the default aspect glyph overlay (☉ ☾ ♂ ☿ ♃ ♀ ♄ ☊ ☋) so only
    # the plain planet abbreviations (Su, Mo, Ma, ... Ra, Ke - with the
    # retrograde marker appended where it applies) and the Asc marker show.
    mychart.updatechartcfg(aspect=False)

    filename = f"{subject.name.replace(' ', '_')}_{style}indian_chart_{lang}"
    mychart.draw(output_dir, filename)

    return ascendant_full, _localize_chart_svg(_read_chart_svg(output_dir, filename), lang)


# ---------------------------------------------------------------------------
# Navamsa (D9) divisional chart
# ---------------------------------------------------------------------------
# Neither Kerykeion nor jyotichart compute divisional (varga) charts -
# Kerykeion only exposes D1 (Rashi) sign/degree data, and jyotichart is
# purely an SVG renderer that will happily draw whatever sign/house data
# it's given. So the D9 sign for each point is derived here from the D1
# absolute longitude, and then rendered with the same jyotichart renderer
# used for the Rashi chart.

NAVAMSA_SPAN = 30.0 / 9  # 3°20' - each sign is divided into 9 navamsas


def navamsa_sign(abs_pos):
    """Return the D9 (Navamsa) sign abbreviation for a sidereal longitude.

    Each 30° sign is split into 9 navamsas of 3°20' each. Combining the
    sign index with the navamsa index via (sign_index * 9 + navamsa_index)
    % 12 reproduces the classical rule - movable signs' navamsas start
    from themselves, fixed signs' start from the 9th sign, and dual signs'
    start from the 5th sign - without needing to branch on sign type.
    """
    abs_pos = abs_pos % 360.0
    sign_index = int(abs_pos // 30)
    degree_in_sign = abs_pos % 30
    navamsa_index = int(degree_in_sign // NAVAMSA_SPAN)
    navamsa_index = min(navamsa_index, 8)  # guard against float rounding right at 30°
    d9_index = (sign_index * 9 + navamsa_index) % 12
    return SIGN_ORDER[d9_index]


def build_navamsa_positions(subject):
    """D9 sign for the Ascendant and every graha, keyed by the same planet
    labels used elsewhere ('Sun', 'Moon', ... 'Rahu', 'Ketu') plus
    'Ascendant'."""
    positions = {"Ascendant": navamsa_sign(subject.first_house["abs_pos"])}

    for attr, (_, symbol) in PLANETS.items():
        label = symbol_to_label(symbol)
        p = getattr(subject, attr)
        positions[label] = navamsa_sign(p["abs_pos"])

    rahu_data = get_rahu_data(subject)
    positions["Rahu"] = navamsa_sign(rahu_data["abs_pos"])
    ketu_abs_pos = (rahu_data["abs_pos"] + 180.0) % 360.0
    positions["Ketu"] = navamsa_sign(ketu_abs_pos)

    return positions


def render_navamsa_chart_svg(subject, style, output_dir, navamsa_positions,
                             lang=i18n.DEFAULT_LANGUAGE):
    """Build a South/North Indian Navamsa (D9) chart with jyotichart, the
    same way render_chart_svg builds the D1 (Rashi) chart, except house
    placement comes from each point's D9 sign rather than its D1 sign.

    Retrograde status is a D1 (Rashi) concept and isn't conventionally
    marked on divisional charts, so no retrograde suffix is added here.
    """
    ascendant_abbr = navamsa_positions["Ascendant"]
    ascendant_full = SIGN_NAME_MAP[ascendant_abbr]

    ChartClass = chart.SouthChart if style == "south" else chart.NorthChart
    mychart = ChartClass("Navamsa", subject.name, IsFullChart=True)
    mychart.set_ascendantsign(ascendant_full)

    for attr, (planet_const, symbol) in PLANETS.items():
        label = symbol_to_label(symbol)
        sign_abbr = navamsa_positions[label]
        house_num = house_from_signs(sign_abbr, ascendant_abbr)
        mychart.add_planet(planet_const, i18n.planet_abbr(label, lang), house_num, retrograde=False)

    rahu_house = house_from_signs(navamsa_positions["Rahu"], ascendant_abbr)
    mychart.add_planet(chart.RAHU, i18n.planet_abbr("Rahu", lang), rahu_house, retrograde=True)

    ketu_house = house_from_signs(navamsa_positions["Ketu"], ascendant_abbr)
    mychart.add_planet(chart.KETU, i18n.planet_abbr("Ketu", lang), ketu_house, retrograde=True)

    mychart.updatechartcfg(aspect=False)

    filename = f"{subject.name.replace(' ', '_')}_{style}indian_navamsa_chart_{lang}"
    mychart.draw(output_dir, filename)

    return ascendant_full, _localize_chart_svg(_read_chart_svg(output_dir, filename), lang)


# ---------------------------------------------------------------------------
# Nakshatra (star) calculations
# ---------------------------------------------------------------------------
# Neither Kerykeion nor jyotichart compute Nakshatra/Pada, Vimshottari Dasha,
# or combustion - Kerykeion only exposes raw sidereal longitude (abs_pos),
# and jyotichart is purely an SVG renderer. All of this is derived here
# directly from well-defined, deterministic formulas.

NAKSHATRA_SPAN = 360.0 / 27.0   # 13°20' each
PADA_SPAN = NAKSHATRA_SPAN / 4  # 3°20' each

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]

# The 9 Vimshottari lords, repeated 3x across the 27 nakshatras
DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
DASHA_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17,
}
NAKSHATRA_LORDS = (DASHA_ORDER * 3)  # 27 entries, aligned to NAKSHATRA_NAMES

DAYS_PER_YEAR = 365.2425  # average Gregorian year, standard approximation used for Dasha math

# Classical "Asta" (combustion) orbs: how close (in degrees) a planet needs
# to be to the Sun to be considered combust. Mercury and Venus have tighter
# orbs while retrograde. The Sun itself, the Ascendant, and the shadow
# planets Rahu/Ketu are never checked.
COMBUSTION_ORBS = {
    "Moon": 12.0,
    "Mars": 17.0,
    "Mercury": {"direct": 14.0, "retrograde": 12.0},
    "Jupiter": 11.0,
    "Venus": {"direct": 10.0, "retrograde": 8.0},
    "Saturn": 15.0,
}


def circular_diff(a, b):
    """Shortest angular distance (0-180) between two 0-360 degree longitudes."""
    diff = abs(a - b) % 360.0
    return min(diff, 360.0 - diff)


def is_combust(label, planet_abs_pos, sun_abs_pos, retrograde):
    """Is this planet within its classical combustion orb of the Sun?"""
    orb = COMBUSTION_ORBS.get(label)
    if orb is None:
        return False
    if isinstance(orb, dict):
        orb = orb["retrograde"] if retrograde else orb["direct"]
    return circular_diff(planet_abs_pos, sun_abs_pos) <= orb


def deg_to_dms(deg):
    """Format a 0-30 degree float as D°M'."""
    d = int(deg)
    m = (deg - d) * 60
    return f"{d}\u00b0{m:04.1f}'"


def nakshatra_details(abs_pos):
    """Given a sidereal absolute longitude (0-360), return nakshatra name, pada, and lord."""
    abs_pos = abs_pos % 360.0
    idx = int(abs_pos // NAKSHATRA_SPAN)
    deg_in_nakshatra = abs_pos % NAKSHATRA_SPAN
    pada = int(deg_in_nakshatra // PADA_SPAN) + 1
    return {
        "name": NAKSHATRA_NAMES[idx],
        "pada": pada,
        "lord": NAKSHATRA_LORDS[idx],
        "degree_in_nakshatra": deg_to_dms(deg_in_nakshatra),
    }


SYMBOL_LABELS = {
    "Su": "Sun", "Mo": "Moon", "Ma": "Mars", "Me": "Mercury",
    "Ju": "Jupiter", "Ve": "Venus", "Sa": "Saturn",
}


def symbol_to_label(symbol):
    return SYMBOL_LABELS.get(symbol, symbol)


# ---------------------------------------------------------------------------
# "Houses Involved" - which houses a dasha lord activates
# ---------------------------------------------------------------------------
# Whole-sign rulerships (sidereal), keyed by planet label -> ruled sign
# abbreviations (matches SIGN_ORDER).
RULERSHIP = {
    "Sun": ["Leo"], "Moon": ["Can"],
    "Mars": ["Ari", "Sco"], "Mercury": ["Gem", "Vir"],
    "Jupiter": ["Sag", "Pis"], "Venus": ["Tau", "Lib"], "Saturn": ["Cap", "Aqu"],
}
# Inverse lookup: sign abbreviation -> its ruling planet's label
SIGN_LORD = {sign: label for label, signs in RULERSHIP.items() for sign in signs}

CLASSICAL_LABELS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# Whole-sign aspect offsets (drishti), counted forward from a planet's own
# house (0 = own house, already covered separately as "placement" so it's
# left out here). Every graha has the universal 7th-house aspect (offset 6);
# Mars, Jupiter and Saturn additionally have their classical special
# aspects.
ASPECT_OFFSETS = {
    "Sun": [6], "Moon": [6], "Mercury": [6], "Venus": [6],
    "Mars": [3, 6, 7],       # 4th, 7th, 8th houses from itself
    "Jupiter": [4, 6, 8],    # 5th, 7th, 9th houses from itself
    "Saturn": [2, 6, 9],     # 3rd, 7th, 10th houses from itself
}


def build_dasha_house_map(subject, ascendant_abbr):
    """For each of the 9 Vimshottari dasha lords, work out which houses (from
    the Ascendant) it 'activates':
      - Classical grahas (Sun..Saturn): placement, houses aspected (7th for
        all, plus Mars/Jupiter/Saturn's extra special aspects), and houses
        ruled (lordship).
      - Rahu/Ketu: they have no aspects or rulership of their own, so
        instead we list every planet connected to them - the dispositor of
        the sign they occupy, any planet conjunct with them (same house),
        and any planet whose aspect lands on their house - and, for each of
        those connected planets, the houses *that planet* rules.
    """
    placements = {}
    signs = {}
    for attr, (_, symbol) in PLANETS.items():
        label = symbol_to_label(symbol)
        p = getattr(subject, attr)
        signs[label] = p["sign"]
        placements[label] = house_from_signs(p["sign"], ascendant_abbr)

    result = {}
    for label in CLASSICAL_LABELS:
        placement_house = placements[label]
        offsets = ASPECT_OFFSETS[label]
        aspects = sorted({((placement_house - 1 + off) % 12) + 1 for off in offsets})
        lordship = sorted({house_from_signs(sign, ascendant_abbr) for sign in RULERSHIP[label]})
        result[label] = {
            "type": "classical",
            "placement": placement_house,
            "aspects": aspects,
            "lordship": lordship,
        }

    rahu_data = get_rahu_data(subject)
    rahu_sign = rahu_data["sign"]
    rahu_house = house_from_signs(rahu_sign, ascendant_abbr)

    rahu_idx = SIGN_ORDER.index(rahu_sign)
    ketu_sign = SIGN_ORDER[(rahu_idx + 6) % 12]
    ketu_house = house_from_signs(ketu_sign, ascendant_abbr)

    for node_label, node_house, node_sign in (
        ("Rahu", rahu_house, rahu_sign),
        ("Ketu", ketu_house, ketu_sign),
    ):
        # planet label -> {"roles": [...], "houses": [...]}
        connections = {}

        dispositor = SIGN_LORD.get(node_sign)
        if dispositor:
            entry = connections.setdefault(dispositor, {"roles": [], "houses": result[dispositor]["lordship"]})
            entry["roles"].append("dispositor")

        for label in CLASSICAL_LABELS:
            if placements[label] == node_house:
                entry = connections.setdefault(label, {"roles": [], "houses": result[label]["lordship"]})
                entry["roles"].append("conjunct")
            if node_house in result[label]["aspects"]:
                entry = connections.setdefault(label, {"roles": [], "houses": result[label]["lordship"]})
                entry["roles"].append("aspecting")

        connection_list = [
            {"planet": label, "roles": data["roles"], "houses": data["houses"]}
            for label, data in connections.items()
        ]

        result[node_label] = {
            "type": "node",
            "placement": node_house,
            "sign": SIGN_NAME_MAP[node_sign],
            "connections": connection_list,
        }

    return result


# ---------------------------------------------------------------------------
# 3-7-11 connection - marriage timing
# ---------------------------------------------------------------------------
# The 3rd, 7th and 11th from the Ascendant are the houses read for marriage.
# A period supports marriage when its Dasha, Bhukti and Antaram lords each
# connect to one of them: by sitting in it, aspecting it, ruling it,
# exchanging signs with its lord, or sitting in one sign with its lord.
# Rahu/Ketu have no aspects or signs of their own, so they connect through
# the planets tied to them - dispositor, conjunction, aspect - the same links
# build_dasha_house_map lists for them.
MARRIAGE_HOUSES = (3, 7, 11)


def build_marriage_links(subject, house_map):
    """Every way each of the nine dasha lords touches the 3rd, 7th or 11th.

    Returns {lord label: [{"house": 7, "how": "placement", "via": None}, ...]}
    - `how` is placement / aspect / lordship / exchange / conjunct for the
    classical grahas, and dispositor / conjunct / aspecting for Rahu/Ketu, with `via`
    naming the planet the link runs through. An empty list means the lord
    has no 3-7-11 connection. `house_map` is build_dasha_house_map()'s result.
    """
    signs = {
        symbol_to_label(symbol): getattr(subject, attr)["sign"]
        for attr, (_, symbol) in PLANETS.items()
    }
    targets = set(MARRIAGE_HOUSES)

    def link(house, how, via=None):
        return {"house": house, "how": how, "via": via}

    result = {}
    for label, info in house_map.items():
        links = []
        if info["placement"] in targets:
            links.append(link(info["placement"], "placement"))
        if info["type"] == "classical":
            links += [link(h, "aspect") for h in info["aspects"] if h in targets]
            links += [link(h, "lordship") for h in info["lordship"] if h in targets]
            # Exchange (parivartana): this lord sits in a sign `partner` rules
            # while `partner` sits in one of this lord's signs, so each takes
            # on the other's houses.
            partner = SIGN_LORD.get(signs[label])
            if partner and partner != label and signs[partner] in RULERSHIP[label]:
                links += [link(h, "exchange", partner)
                          for h in house_map[partner]["lordship"] if h in targets]
            # Conjunction: sharing a sign with the lord of the 3rd, 7th or 11th.
            for other in CLASSICAL_LABELS:
                if other != label and signs[other] == signs[label]:
                    links += [link(h, "conjunct", other)
                              for h in house_map[other]["lordship"] if h in targets]
        else:
            for conn in info["connections"]:
                for role in conn["roles"]:
                    links += [link(h, role, conn["planet"]) for h in conn["houses"] if h in targets]
        result[label] = links
    return result


def build_star_table(subject):
    """One row per graha (+ Ascendant): sign, degree, nakshatra, pada, nakshatra lord.

    Retrograde is shown on the chart itself now (see render_chart_svg), not in
    this table. Combust planets (too close to the Sun) get a small fire
    marker prepended to their name instead.
    """
    rows = []
    sun_abs_pos = subject.sun["abs_pos"]

    def add_row(label, sign_abbr, degree_in_sign, abs_pos, retro, check_combustion=True):
        nak = nakshatra_details(abs_pos)
        combust = check_combustion and is_combust(label, abs_pos, sun_abs_pos, retro)
        # The English name doubles as the translation key - the page renders
        # it inside a data-i18n-term span and the combustion marker sits
        # outside, so switching language doesn't disturb the marker.
        rows.append({
            "planet": label,
            "sign": SIGN_NAME_MAP[sign_abbr],
            "degree": deg_to_dms(degree_in_sign),
            "nakshatra": nak["name"],
            "pada": nak["pada"],
            "lord": nak["lord"],
            "combust": combust,
        })

    asc = subject.first_house
    add_row("Ascendant (Lagna)", asc["sign"], asc["position"], asc["abs_pos"], False, check_combustion=False)

    for attr, (_, symbol) in PLANETS.items():
        p = getattr(subject, attr)
        label = symbol_to_label(symbol)
        add_row(label, p["sign"], p["position"], p["abs_pos"], p.get("retrograde", False),
                 check_combustion=(label != "Sun"))

    rahu_data = get_rahu_data(subject)
    add_row("Rahu", rahu_data["sign"], rahu_data["position"], rahu_data["abs_pos"], True, check_combustion=False)

    rahu_idx = SIGN_ORDER.index(rahu_data["sign"])
    ketu_abs_pos = (rahu_data["abs_pos"] + 180.0) % 360.0
    ketu_sign = SIGN_ORDER[(rahu_idx + 6) % 12]
    ketu_degree_in_sign = ketu_abs_pos % 30.0
    add_row("Ketu", ketu_sign, ketu_degree_in_sign, ketu_abs_pos, True, check_combustion=False)

    return rows


# ---------------------------------------------------------------------------
# Conjunctions - grahas (and the Ascendant) grouped by actual degree
# separation, not merely by shared sign. Two bodies a couple of degrees
# apart but straddling a sign boundary (e.g. 29 deg Aries / 1 deg Taurus)
# are conjunct; two bodies in the same sign but many degrees apart are not.
# ---------------------------------------------------------------------------

# Widest orb (in degrees) at which two bodies still count as conjunct, with
# tighter bands called out separately so a 20' pairing reads differently
# from a near-9-degree one.
CONJUNCTION_ORB_TIERS = [
    (1.0, "Exact"),
    (3.0, "Tight"),
    (6.0, "Close"),
    (10.0, "Wide"),
]

# Rank used to show the tightest conjunctions in a chart first.
_CONJUNCTION_TIER_RANK = {label: i for i, (_, label) in enumerate(CONJUNCTION_ORB_TIERS)}


def conjunction_tier(diff):
    """Classify an angular separation into a conjunction tier, or None if
    it's wider than the maximum orb (i.e. not a conjunction at all)."""
    for limit, label in CONJUNCTION_ORB_TIERS:
        if diff <= limit:
            return label
    return None


def gather_chart_bodies(subject):
    """The Ascendant plus every graha (7 classical + Rahu/Ketu), each as
    (label, sign_abbr, degree_in_sign, abs_pos). Shared by both conjunction
    views below.
    """
    bodies = []  # (label, sign_abbr, degree_in_sign, abs_pos)

    asc = subject.first_house
    bodies.append(("Ascendant", asc["sign"], asc["position"], asc["abs_pos"] % 360.0))

    for attr, (_, symbol) in PLANETS.items():
        p = getattr(subject, attr)
        label = symbol_to_label(symbol)
        bodies.append((label, p["sign"], p["position"], p["abs_pos"] % 360.0))

    rahu_data = get_rahu_data(subject)
    bodies.append(("Rahu", rahu_data["sign"], rahu_data["position"], rahu_data["abs_pos"] % 360.0))

    rahu_idx = SIGN_ORDER.index(rahu_data["sign"])
    ketu_sign = SIGN_ORDER[(rahu_idx + 6) % 12]
    ketu_abs_pos = (rahu_data["abs_pos"] + 180.0) % 360.0
    bodies.append(("Ketu", ketu_sign, ketu_abs_pos % 30.0, ketu_abs_pos))

    return bodies


def build_conjunctions(subject):
    """Group the Ascendant and every graha into conjunction clusters based
    on actual longitude, with a 10 degree maximum orb.

    Returns a list of clusters (2+ bodies each), tightest first. Each
    cluster lists its members (sorted by longitude, with sign + degree) and
    every conjunct pair within it (sorted tightest-first).
    """
    bodies = gather_chart_bodies(subject)

    info = {
        label: {"sign": sign, "degree": deg_to_dms(deg), "abs_pos": pos}
        for label, sign, deg, pos in bodies
    }

    # Edge between any two bodies within orb; a chain of near-conjunctions
    # (A-B within orb, B-C within orb) is grouped into one cluster even if
    # A and C themselves are wider apart than the orb.
    labels = [b[0] for b in bodies]
    adjacent = {label: [] for label in labels}
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            label_a, label_b = bodies[i][0], bodies[j][0]
            diff = circular_diff(info[label_a]["abs_pos"], info[label_b]["abs_pos"])
            if conjunction_tier(diff) is not None:
                adjacent[label_a].append(label_b)
                adjacent[label_b].append(label_a)

    visited = set()
    clusters = []
    for label in labels:
        if label in visited or not adjacent[label]:
            continue
        stack, members = [label], set()
        while stack:
            cur = stack.pop()
            if cur in members:
                continue
            members.add(cur)
            visited.add(cur)
            stack.extend(n for n in adjacent[cur] if n not in members)
        clusters.append(members)

    results = []
    for members in clusters:
        ordered = sorted(members, key=lambda l: info[l]["abs_pos"])

        pairs = []
        member_list = sorted(members)
        for i in range(len(member_list)):
            for j in range(i + 1, len(member_list)):
                a, b = member_list[i], member_list[j]
                diff = circular_diff(info[a]["abs_pos"], info[b]["abs_pos"])
                tier = conjunction_tier(diff)
                if tier is not None:
                    pairs.append({"a": a, "b": b, "orb": deg_to_dms(diff), "tier": tier, "_diff": diff})
        pairs.sort(key=lambda p: p["_diff"])
        for p in pairs:
            del p["_diff"]

        signs_seen = []
        for label in ordered:
            sign_name = SIGN_NAME_MAP[info[label]["sign"]]
            if not signs_seen or signs_seen[-1] != sign_name:
                signs_seen.append(sign_name)

        results.append({
            "members": [
                {"planet": label, "sign": SIGN_NAME_MAP[info[label]["sign"]], "degree": info[label]["degree"]}
                for label in ordered
            ],
            "pairs": pairs,
            # Kept as a list rather than a pre-joined string so each sign
            # name can be translated individually on the page.
            "signs": signs_seen,
            "tightest_tier": pairs[0]["tier"] if pairs else None,
        })

    results.sort(key=lambda c: _CONJUNCTION_TIER_RANK.get(c["tightest_tier"], 99))
    return results


def build_sign_conjunctions(subject):
    """Group the Ascendant and every graha by shared sign (rashi) - the
    traditional whole-sign 'yuti', where any two bodies in the same sign
    count as conjunct regardless of how many degrees apart they sit within
    it. Each group lists its members (sorted by degree) and every pairwise
    degree difference, tightest first.

    This complements build_conjunctions(): that one can miss a same-sign
    pair sitting 25 degrees apart (arguably not a "real" conjunction) and
    catches a cross-boundary pair a sign-only view would miss - here every
    same-sign pair is shown, with its degree gap made explicit so it's easy
    to see just how tight (or loose) each one actually is.
    """
    bodies = gather_chart_bodies(subject)

    groups = {}  # sign_abbr -> [(label, degree_in_sign), ...]
    for label, sign, deg, _abs_pos in bodies:
        groups.setdefault(sign, []).append((label, deg))

    results = []
    for sign, members in groups.items():
        if len(members) < 2:
            continue
        ordered = sorted(members, key=lambda m: m[1])

        pairs = []
        member_list = sorted(members, key=lambda m: m[0])
        for i in range(len(member_list)):
            for j in range(i + 1, len(member_list)):
                a_label, a_deg = member_list[i]
                b_label, b_deg = member_list[j]
                diff = abs(a_deg - b_deg)
                pairs.append({"a": a_label, "b": b_label, "diff": deg_to_dms(diff), "_diff": diff})
        pairs.sort(key=lambda p: p["_diff"])
        for p in pairs:
            del p["_diff"]

        results.append({
            "sign": SIGN_NAME_MAP[sign],
            "_sign_rank": SIGN_ORDER.index(sign),
            "members": [{"planet": label, "degree": deg_to_dms(deg)} for label, deg in ordered],
            "pairs": pairs,
        })

    results.sort(key=lambda r: r["_sign_rank"])
    for r in results:
        del r["_sign_rank"]
    return results


# ---------------------------------------------------------------------------
# Vimshottari Mahadasha calculation
# ---------------------------------------------------------------------------

def build_dasha_table(subject, birth_dt):
    """
    Standard Vimshottari Mahadasha sequence: the Moon's nakshatra at birth
    determines both the starting lord and how much of that lord's period is
    already 'used up' (based on degrees already traversed through the
    nakshatra). Returns the current lord's balance period plus the next 8
    full periods (one complete cycle through all 9 lords from birth).
    """
    from datetime import timedelta

    moon = subject.moon
    abs_pos = moon["abs_pos"] % 360.0
    idx = int(abs_pos // NAKSHATRA_SPAN)
    fraction_elapsed = (abs_pos % NAKSHATRA_SPAN) / NAKSHATRA_SPAN

    start_lord_idx = DASHA_ORDER.index(NAKSHATRA_LORDS[idx])
    balance_years = DASHA_YEARS[DASHA_ORDER[start_lord_idx]] * (1 - fraction_elapsed)

    rows = []
    cursor = birth_dt

    # First entry: balance of the lord active at birth
    lord = DASHA_ORDER[start_lord_idx]
    end = cursor + timedelta(days=balance_years * DAYS_PER_YEAR)
    rows.append({
        "lord": lord,
        "start": cursor.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
        "years": f"{balance_years:.2f}",
        "years_exact": balance_years,
    })
    cursor = end

    # Remaining 8 lords at full duration, completing one cycle from birth
    for step in range(1, 9):
        lord = DASHA_ORDER[(start_lord_idx + step) % 9]
        full_years = DASHA_YEARS[lord]
        end = cursor + timedelta(days=full_years * DAYS_PER_YEAR)
        rows.append({
            "lord": lord,
            "start": cursor.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d"),
            "years": f"{full_years:.2f}",
            "years_exact": float(full_years),
        })
        cursor = end

    return rows


def build_sub_periods(lord, start_dt, years):
    """The nine Vimshottari sub-periods inside any one period - Antardashas
    inside a Mahadasha, Pratyantardashas inside an Antardasha, and so on.

    Same math the results page runs client-side (see computeSubPeriods in
    PAGE_TEMPLATE): the sequence starts with the parent period's own lord and
    walks DASHA_ORDER, each sub-lord taking the share of the parent that
    matches its own share of the 120-year cycle.
    """
    from datetime import timedelta

    start_idx = DASHA_ORDER.index(lord)
    cursor = start_dt
    periods = []
    for step in range(9):
        sub_lord = DASHA_ORDER[(start_idx + step) % 9]
        sub_years = years * DASHA_YEARS[sub_lord] / 120.0
        end = cursor + timedelta(days=sub_years * DAYS_PER_YEAR)
        periods.append({"lord": sub_lord, "start": cursor, "end": end, "years": sub_years})
        cursor = end
    return periods


def build_antardashas(lord, start_dt, years):
    """The nine Antardasha (bhukti) sub-periods inside one Mahadasha."""
    return [
        {"maha": lord, "antar": p["lord"], "start": p["start"], "end": p["end"], "years": p["years"]}
        for p in build_sub_periods(lord, start_dt, years)
    ]


def build_dasha_bhukti_window(dasha_table, now, before=1, after=2):
    """Dasha-Bhukti periods around `now`: the one running today, `before`
    previous ones, and `after` upcoming ones - four rows in total by default.

    The current row also carries the next level down: its nine Pratyantardasha
    (Antaram) periods, under "antaram", with the one covering `now` flagged.
    """
    from datetime import datetime as _dt

    periods = []
    for row in dasha_table:
        start_dt = _dt.strptime(row["start"], "%Y-%m-%d")
        periods.extend(build_antardashas(row["lord"], start_dt, row["years_exact"]))

    current_idx = next(
        (i for i, p in enumerate(periods) if p["start"] <= now <= p["end"]), None
    )
    if current_idx is None:
        # `now` sits outside the cycle the table covers - before birth, or past
        # the 120 years it spans. Anchor on the nearest end so the PDF still
        # prints a sensible run of periods instead of blowing up.
        current_idx = 0 if now < periods[0]["start"] else len(periods) - 1

    window = []
    for i in range(max(0, current_idx - before), min(len(periods), current_idx + after + 1)):
        p = periods[i]
        if i < current_idx:
            role = "Previous"
        elif i == current_idx:
            role = "Current"
        elif i == current_idx + 1:
            role = "Upcoming"
        else:
            role = "Then"
        entry = {
            "role": role,
            "maha": p["maha"],
            "antar": p["antar"],
            "start": p["start"].strftime("%Y-%m-%d"),
            "end": p["end"].strftime("%Y-%m-%d"),
            "years": f"{p['years']:.2f}",
        }
        if i == current_idx:
            entry["antaram"] = [
                {
                    "lord": sub["lord"],
                    "start": sub["start"].strftime("%Y-%m-%d"),
                    "end": sub["end"].strftime("%Y-%m-%d"),
                    "years": f"{sub['years']:.3f}",
                    "is_current": sub["start"] <= now <= sub["end"],
                }
                for sub in build_sub_periods(p["antar"], p["start"], p["years"])
            ]
        window.append(entry)
    return window


# ---------------------------------------------------------------------------
# Web page
# ---------------------------------------------------------------------------

PAGE_TEMPLATE = """
<!DOCTYPE html>
<!-- data-lang is what every translated rule keys off; the boot script in
     <head> overwrites it from localStorage before the first paint, and this
     default keeps the page readable even with JavaScript off. -->
<html lang="en" data-lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title data-i18n="app.page_title">Vedic Birth Chart Generator</title>
<meta name="description" content="Generate sidereal Vedic (Jyotish) birth charts - Rashi and Navamsa, Nakshatra, and Vimshottari Dasha.">
<meta name="theme-color" content="#0b0d17">
{{ lang_boot | safe }}
<script src="/i18n.js"></script>
<link rel="manifest" href="/manifest.json">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="VedicChart">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #12111e;
    --surface: #1a1830;
    --surface-2: #211f38;
    --surface-3: #282546;
    --border: rgba(212,175,55,0.25);
    --text: #e0d5c5;
    --muted: rgba(224,213,197,0.65);
    --muted-2: rgba(224,213,197,0.4);
    --primary: #d4af37;
    --primary-2: #e0c477;
    --primary-grad: linear-gradient(135deg, #d4af37 0%, #f0d878 100%);
    --primary-grad-soft: linear-gradient(135deg, rgba(212,175,55,0.16) 0%, rgba(224,196,119,0.16) 100%);
    --on-primary: #1c1710;
    --gold: #d4af37;
    --danger-bg: rgba(255,50,30,0.1);
    --danger-border: rgba(255,80,60,0.6);
    --danger-text: #ff8877;
    --radius-lg: 20px;
    --radius-md: 14px;
    --radius-sm: 10px;
    --safe-b: env(safe-area-inset-bottom, 0px);
    --safe-t: env(safe-area-inset-top, 0px);
  }
  * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
  html { -webkit-text-size-adjust: 100%; }
  body {
    margin: 0;
    min-height: 100vh;
    font-family: 'Lato', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background:
      radial-gradient(ellipse at 20% -10%, #1a1535 0%, #0c1030 60%, var(--bg) 100%);
    background-attachment: fixed;
    color: var(--text);
    padding-top: var(--safe-t);
    overscroll-behavior-y: contain;
    -webkit-font-smoothing: antialiased;
  }
  a { color: var(--primary-2); }

  /* Top app bar */
  .app-bar {
    position: sticky;
    top: 0;
    z-index: 30;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: calc(14px + var(--safe-t)) 16px 14px;
    background: rgba(18, 17, 30, 0.72);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-bottom: 1px solid var(--border);
  }
  .app-bar__icon {
    width: 34px; height: 34px;
    border-radius: 10px;
    flex-shrink: 0;
    box-shadow: 0 4px 14px rgba(212,175,55,0.35);
  }
  .app-bar__titles { flex: 1; min-width: 0; }
  .app-bar__title {
    font-family: 'Cinzel', serif;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    color: var(--gold);
    text-shadow: 0 0 16px rgba(212,175,55,0.35);
  }
  .app-bar__subtitle {
    font-size: 11.5px;
    color: var(--muted);
    margin: 1px 0 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .install-btn {
    flex-shrink: 0;
    display: none;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    font-family: 'Cinzel', serif;
    font-size: 11.5px;
    font-weight: 600;
    letter-spacing: 0.06em;
    color: var(--primary-2);
    background: rgba(212,175,55,0.08);
    border: 1.5px solid rgba(212,175,55,0.5);
    border-radius: 999px;
    cursor: pointer;
    transition: all 0.2s;
  }
  .install-btn.visible { display: inline-flex; }
  .install-btn:hover { background: rgba(212,175,55,0.18); border-color: var(--gold); color: #ffe060; }
  .install-btn:active { transform: scale(0.96); }

  .admin-btn {
    flex-shrink: 0;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 14px;
    font-family: 'Cinzel', serif;
    font-size: 11.5px;
    font-weight: 600;
    letter-spacing: 0.06em;
    color: #a9c3ff;
    background: rgba(90,140,255,0.08);
    border: 1.5px solid rgba(120,170,255,0.5);
    border-radius: 999px;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.2s;
  }
  .admin-btn:hover { background: rgba(90,140,255,0.18); border-color: #7aa2ff; color: #cfe0ff; }
  .admin-btn:active { transform: scale(0.96); }

  .layout {
    max-width: 1180px;
    margin: 0 auto;
    padding: 18px 16px calc(48px + var(--safe-b));
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  @media (min-width: 960px) {
    .layout {
      display: grid;
      grid-template-columns: 380px 1fr;
      align-items: start;
      padding-top: 28px;
    }
    .form-card { position: sticky; top: 92px; }
  }

  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 20px;
    box-shadow: 0 0 30px rgba(0,0,0,0.35);
  }
  .form-card { padding: 22px 20px 20px; }

  .field-label {
    display: block;
    font-family: 'Cinzel', serif;
    font-size: 11.5px;
    font-weight: 600;
    color: var(--muted);
    margin: 16px 0 7px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  .field-label:first-of-type { margin-top: 0; }

  input[type="text"], input[type="date"], input[type="time"], input[type="number"] {
    width: 100%;
    padding: 12px 13px;
    background: var(--surface-2);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--text);
    font-family: 'Lato', sans-serif;
    font-size: 16px; /* >=16px prevents iOS auto-zoom on focus */
    transition: border-color 0.15s, box-shadow 0.15s;
    -webkit-appearance: none;
    appearance: none;
    color-scheme: dark;
  }
  input::placeholder { color: var(--muted-2); }
  input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 4px rgba(212, 175, 55, 0.18);
  }

  .row { display: flex; gap: 10px; }
  .row > div { flex: 1; min-width: 0; }

  small.hint {
    display: block;
    color: var(--muted-2);
    font-size: 11.5px;
    margin-top: 6px;
    line-height: 1.45;
  }

  /* Segmented control for chart style */
  .segmented {
    display: flex;
    gap: 4px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 4px;
    margin-top: 6px;
  }
  .segmented input {
    position: absolute;
    width: 1px; height: 1px;
    opacity: 0;
    pointer-events: none;
  }
  .segmented label {
    flex: 1;
    text-align: center;
    padding: 10px 4px;
    font-family: 'Cinzel', serif;
    font-size: 11.5px;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: var(--muted);
    border-radius: 8px;
    cursor: pointer;
    transition: 0.15s;
    user-select: none;
  }
  .segmented input:checked + label {
    background: var(--primary-grad);
    color: var(--on-primary);
    box-shadow: 0 4px 14px rgba(212, 175, 55, 0.35);
  }
  .segmented input:focus-visible + label { outline: 2px solid var(--primary); outline-offset: 2px; }

  /* Birth-city field + its "Confirm place" lookup button, side by side. */
  .place-row {
    display: flex;
    gap: 8px;
    align-items: stretch;
  }
  .place-row input { flex: 1; min-width: 0; }
  button.confirm-btn {
    flex: 0 0 auto;
    margin-top: 6px;
    padding: 0 16px;
    background: var(--surface-2);
    color: var(--text);
    font-family: 'Cinzel', serif;
    font-weight: 600;
    font-size: 12px;
    letter-spacing: 0.03em;
    white-space: nowrap;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: transform 0.12s, opacity 0.12s, border-color 0.12s;
  }
  button.confirm-btn:hover { border-color: var(--primary); }
  button.confirm-btn:active { transform: scale(0.98); }
  button.confirm-btn[disabled] { opacity: 0.6; cursor: progress; }

  /* "Date of birth" label + its "Now" shortcut button, side by side. */
  .field-label-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
  }
  .field-label-row .field-label { margin: 0; }
  button.now-btn {
    flex: 0 0 auto;
    padding: 2px 10px;
    background: var(--surface-2);
    color: var(--text);
    font-family: 'Cinzel', serif;
    font-weight: 600;
    font-size: 11px;
    letter-spacing: 0.03em;
    white-space: nowrap;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: transform 0.12s, opacity 0.12s, border-color 0.12s;
  }
  button.now-btn:hover { border-color: var(--primary); }
  button.now-btn:active { transform: scale(0.98); }

  .geo-status { display: block; margin-top: 6px; font-size: 12px; color: var(--muted); }
  .geo-status.ok { color: var(--primary); }
  .geo-status.bad { color: #ff6655; }

  button.save-btn {
    width: 100%;
    margin-top: 10px;
    padding: 12px;
    background: transparent;
    color: var(--text);
    font-family: 'Cinzel', serif;
    font-weight: 600;
    font-size: 13px;
    letter-spacing: 0.04em;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: transform 0.12s, border-color 0.12s, opacity 0.12s;
  }
  button.save-btn:hover { border-color: var(--primary); }
  button.save-btn:active { transform: scale(0.98); }
  button.save-btn[disabled] { opacity: 0.6; cursor: progress; }

  .save-status { display: block; margin-top: 6px; font-size: 12px; color: var(--muted); }
  .save-status.ok { color: var(--primary); }
  .save-status.bad { color: #ff6655; }

  button.submit-btn {
    width: 100%;
    margin-top: 22px;
    padding: 15px;
    background: var(--primary-grad);
    color: var(--on-primary);
    font-family: 'Cinzel', serif;
    font-weight: 700;
    font-size: 14.5px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border: none;
    border-radius: var(--radius-sm);
    cursor: pointer;
    box-shadow: 0 8px 24px rgba(212, 175, 55, 0.35);
    transition: transform 0.12s, box-shadow 0.12s, opacity 0.12s;
  }
  button.submit-btn:active { transform: scale(0.98); box-shadow: 0 4px 14px rgba(212, 175, 55, 0.3); }

  .results { min-height: 200px; }
  .placeholder-card {
    text-align: center;
    padding: 56px 24px;
    color: var(--muted);
    font-size: 14px;
  }
  .placeholder-card .ph-icon { font-size: 34px; margin-bottom: 10px; opacity: 0.7; color: var(--gold); }

  .error {
    background: var(--danger-bg);
    border: 1px solid var(--danger-border);
    color: var(--danger-text);
    padding: 14px 16px;
    border-radius: var(--radius-md);
    font-size: 14px;
  }
  .error b { color: #fff; }

  .meta-card {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 18px;
  }
  .meta-pill {
    background: var(--surface-2);
    border: 1px solid var(--border);
    color: var(--muted);
    font-size: 12.5px;
    padding: 7px 12px;
    border-radius: 999px;
  }
  .meta-pill b { color: var(--text); font-weight: 700; }
  .meta-pill.accent {
    background: var(--primary-grad-soft);
    border-color: rgba(212, 175, 55, 0.35);
    color: var(--text);
  }
  .meta-pill.playground-btn {
    background: var(--primary-grad);
    border-color: transparent;
    color: var(--on-primary);
    font-family: 'Cinzel', serif;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-decoration: none;
    cursor: pointer;
    transition: transform 0.12s, box-shadow 0.12s;
    box-shadow: 0 4px 14px rgba(212, 175, 55, 0.3);
  }
  .meta-pill.playground-btn:hover { transform: translateY(-1px); box-shadow: 0 8px 20px rgba(212, 175, 55, 0.4); }
  .meta-pill.playground-btn:active { transform: scale(0.98); }

  /* The PDF button lives in its own form (it POSTs the birth details back to
     the server), so the wrapper has to stay invisible inside the pill row. */
  .pdf-form { display: contents; }
  .meta-pill.pdf-btn {
    background: var(--surface-3);
    border-color: rgba(212, 175, 55, 0.45);
    color: var(--text);
    font-family: 'Cinzel', serif;
    font-weight: 700;
    letter-spacing: 0.03em;
    cursor: pointer;
    transition: transform 0.12s, border-color 0.12s, color 0.12s;
  }
  .meta-pill.pdf-btn:hover { border-color: var(--primary); color: var(--primary-2); transform: translateY(-1px); }
  .meta-pill.pdf-btn:active { transform: scale(0.98); }

  .charts-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 16px;
    margin-bottom: 8px;
  }
  @media (min-width: 640px) {
    .charts-grid { grid-template-columns: 1fr 1fr; }
  }
  .chart-card {
    background: #efe4c9;
    border-radius: var(--radius-md);
    padding: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.35), 0 0 0 1px rgba(212,175,55,0.2);
  }
  .chart-card h3 {
    margin: 0 0 10px;
    color: #7a5c10;
    font-family: 'Cinzel', serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.03em;
  }
  .chart-card svg { width: 100%; height: auto; display: block; margin: 0 auto; }

  .section-title {
    font-family: 'Cinzel', serif;
    color: var(--gold);
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.06em;
    margin: 30px 0 4px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .section-title::before {
    content: "";
    width: 4px; height: 16px;
    border-radius: 3px;
    background: var(--primary-grad);
    display: inline-block;
  }

  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th, td {
    text-align: left;
    padding: 10px 12px;
    border-bottom: 1px solid var(--border);
    white-space: nowrap;
  }
  th {
    font-family: 'Cinzel', serif;
    color: var(--muted);
    font-weight: 700;
    font-size: 10.5px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    background: var(--surface-2);
    position: sticky;
    top: 0;
  }
  tbody tr:hover td { background: var(--surface-2); }
  .table-wrap {
    overflow-x: auto;
    margin-bottom: 12px;
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    background: var(--surface);
    -webkit-overflow-scrolling: touch;
  }
  .table-wrap table { margin: 0; }
  .dasha-current td { background: var(--primary-grad-soft) !important; }

  .dasha-row { cursor: pointer; user-select: none; touch-action: manipulation; }
  /* The row feeding the Houses Involved and 3-7-11 boxes - on a phone those
     boxes update below the fold, so the tapped row itself shows the pick. */
  .dasha-row.dasha-selected > td { font-weight: 700; color: var(--text); }
  .dasha-row.dasha-selected > td:first-child { box-shadow: inset 3px 0 0 var(--primary-2); }
  .toggle-arrow {
    display: inline-block;
    width: 14px;
    color: var(--primary-2);
    transition: transform 0.15s ease;
  }
  .dasha-row.expanded > td:first-child .toggle-arrow { transform: rotate(90deg); }
  .dasha-row.level-1 { background: rgba(212, 175, 55, 0.05); }
  .dasha-row.level-2 { background: rgba(212, 175, 55, 0.09); }
  .dasha-row.level-3 { background: rgba(212, 175, 55, 0.13); }
  .dasha-row.level-1 td:first-child { padding-left: 26px; }
  .dasha-row.level-2 td:first-child { padding-left: 42px; }
  .dasha-row.level-3 td:first-child { padding-left: 58px; cursor: default; }
  .dasha-row.level-3:hover td { background: inherit; }

  .houses-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 16px;
    font-size: 13px;
  }
  .houses-box .placeholder-small { color: var(--muted); text-align: center; padding: 10px 0; }
  .houses-box-row { display: flex; flex-wrap: wrap; gap: 10px; }
  .houses-box-row .planet-block { flex: 1 1 260px; margin-bottom: 0; }
  .dasha-level-block { margin-bottom: 16px; }
  .dasha-level-block:last-child { margin-bottom: 0; }
  .dl-heading {
    font-family: 'Cinzel', serif;
    color: var(--primary-2);
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 8px;
  }
  .dl-period {
    color: var(--muted);
    font-weight: 500;
    text-transform: none;
    letter-spacing: normal;
    font-size: 11px;
    margin-left: 6px;
  }
  .planet-block {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 10px 12px;
    margin-bottom: 8px;
  }
  .planet-block:last-child { margin-bottom: 0; }
  .planet-name { font-family: 'Cinzel', serif; font-weight: 700; margin-bottom: 6px; }
  .planet-line { font-weight: 600; color: var(--text); }
  .detail-line { padding: 2px 0; color: var(--text); }
  .detail-line .dl-label { display: inline-block; min-width: 88px; color: var(--muted); }
  .detail-line em { color: var(--muted); font-style: normal; font-size: 11px; }
  .muted-line { color: var(--muted); font-size: 12px; }

  /* 3-7-11 (marriage) box */
  .m-caption { color: var(--muted); font-size: 12px; margin-bottom: 10px; }
  .m-links { margin: 0; padding-left: 18px; }
  .m-links li { padding: 1px 0; }
  .m-verdict {
    margin-top: 12px;
    padding: 9px 12px;
    border-radius: var(--radius-sm);
    border-left: 3px solid var(--muted);
    background: var(--surface-2);
    font-weight: 600;
  }
  .m-verdict.on { border-left-color: #3fbf7f; }
  .m-touch { margin-top: 8px; display: flex; flex-wrap: wrap; align-items: center; gap: 6px; font-size: 12px; color: var(--muted); }
  .m-house { padding: 1px 9px; border-radius: 999px; border: 1px solid var(--border); }
  .m-house.on { color: var(--text); border-color: var(--primary-2); background: var(--primary-grad-soft); }
  .m-upcoming-title {
    margin-top: 18px;
    margin-bottom: 6px;
    font-family: 'Cinzel', serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--primary-2);
  }
  .m-upcoming-wrap { overflow-x: auto; }
  .m-upcoming { width: 100%; border-collapse: collapse; font-size: 12px; }
  .m-upcoming td { padding: 5px 6px; border-top: 1px solid var(--border); white-space: nowrap; }
  .m-upcoming tr.now td { background: var(--primary-grad-soft); font-weight: 600; }
  .m-tag {
    display: inline-block;
    margin-right: 4px;
    padding: 0 7px;
    border-radius: 999px;
    border: 1px solid var(--primary-2);
    font-size: 11px;
  }
  .m-check {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    margin-top: 8px;
    padding: 8px 12px;
    border-radius: var(--radius-sm);
    background: var(--surface-2);
    border-left: 3px solid var(--muted);
  }
  .m-check.yes { border-left-color: #3fbf7f; }
  .m-check.open { border-left-style: dashed; }
  .m-mark { font-weight: 700; min-width: 14px; }
  .m-check.yes .m-mark { color: #3fbf7f; }
  .m-check.no .m-mark, .m-check.open .m-mark { color: var(--muted); }
  .m-check-title { font-weight: 700; }

  .conj-tier {
    display: inline-block;
    margin-left: 8px;
    padding: 1px 8px;
    border-radius: 999px;
    font-family: 'Cinzel', serif;
    font-size: 9.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    vertical-align: middle;
  }
  .conj-tier-exact { background: var(--primary-grad); color: var(--on-primary); }
  .conj-tier-tight { background: var(--primary-grad-soft); color: var(--primary-2); }
  .conj-tier-close { background: var(--surface-2); border: 1px solid var(--border); color: var(--text); }
  .conj-tier-wide { background: var(--surface-2); border: 1px solid var(--border); color: var(--muted); }
  .conj-pairs { margin-top: 6px; }

  /* Each chart is rendered twice server-side - once with English glyphs,
     once with Tamil - and the toggle just swaps which copy is visible, so
     switching language is instant and needs no round trip. */
  .chart-svg[data-lang-svg] { display: none; }
  html[data-lang="en"] .chart-svg[data-lang-svg="en"],
  html[data-lang="ta"] .chart-svg[data-lang-svg="ta"] { display: block; }
{{ lang_switch_css }}
</style>
</head>
<body>

<div class="app-bar">
  <img class="app-bar__icon" src="/icon-192.png" alt="">
  <div class="app-bar__titles">
    <p class="app-bar__title" data-i18n="app.title">Vedic Birth Chart</p>
    <p class="app-bar__subtitle" data-i18n="app.subtitle">Sidereal &middot; Lahiri ayanamsa</p>
  </div>
  {{ lang_switch | safe }}
  <a class="admin-btn" href="/admin">&#9881; <span data-i18n="nav.admin">Admin</span></a>
  <button id="installBtn" class="install-btn" type="button">&#128241; <span data-i18n="nav.install">Install</span></button>
</div>

<div class="layout">
  <form class="card form-card" method="POST" action="/generate">
    <label class="field-label" for="name" data-i18n="form.name">Name</label>
    <input type="text" id="name" name="name" value="{{ form.name }}" required>

    <label class="field-label" for="city" data-i18n="form.city">Birth city</label>
    <div class="place-row">
      <input type="text" id="city" name="city" value="{{ form.city }}"
             placeholder="e.g. Mumbai, India" data-i18n-attr="placeholder:form.city_placeholder">
      <button type="button" id="confirmPlaceBtn" class="confirm-btn" data-i18n="form.confirm_place">Confirm place</button>
    </div>
    <small class="geo-status" id="geoStatus" data-i18n="geo.idle">Type a city and hit Confirm place to fill in the coordinates.</small>

    <div class="row">
      <div>
        <div class="field-label-row">
          <label class="field-label" for="date" data-i18n="form.dob">Date of birth</label>
          <button type="button" id="nowBtn" class="now-btn" data-i18n="form.now">Now</button>
        </div>
        <input type="date" id="date" name="date" value="{{ form.date }}" required>
      </div>
      <div>
        <label class="field-label" for="time" data-i18n="form.tob">Time of birth</label>
        <input type="time" id="time" name="time" value="{{ form.time }}" required>
      </div>
    </div>

    <div class="row">
      <div>
        <label class="field-label" for="lat" data-i18n="form.lat">Latitude</label>
        <input type="number" step="any" id="lat" name="lat" value="{{ form.lat }}" placeholder="19.0760" required>
      </div>
      <div>
        <label class="field-label" for="lng" data-i18n="form.lng">Longitude</label>
        <input type="number" step="any" id="lng" name="lng" value="{{ form.lng }}" placeholder="72.8777" required>
      </div>
    </div>
    <small class="hint" data-i18n="form.latlng_hint">Filled in automatically by "Confirm place", or type them in yourself.</small>

    <label class="field-label" for="tz" data-i18n="form.tz">Timezone (IANA name)</label>
    <input type="text" id="tz" name="tz" value="{{ form.tz }}" placeholder="Asia/Kolkata" required>
    <small class="hint" data-i18n="form.tz_hint">e.g. Asia/Kolkata, America/New_York, Europe/London</small>

    <label class="field-label" data-i18n="form.style">Chart style</label>
    <div class="segmented">
      <input type="radio" id="south" name="style" value="south" {{ 'checked' if form.style == 'south' else '' }}>
      <label for="south" data-i18n="form.style_south">South Indian</label>
      <input type="radio" id="north" name="style" value="north" {{ 'checked' if form.style == 'north' else '' }}>
      <label for="north" data-i18n="form.style_north">North Indian</label>
      <input type="radio" id="both" name="style" value="both" {{ 'checked' if form.style == 'both' else '' }}>
      <label for="both" data-i18n="form.style_both">Both</label>
    </div>

    <button type="submit" class="submit-btn" data-i18n="form.submit">Generate Chart</button>
    <button type="button" id="saveDetailsBtn" class="save-btn" data-i18n="form.save">Save details</button>
    <small class="save-status" id="saveStatus" data-i18n="save.idle">Saves this person's details so they show up in the admin panel - doesn't generate a chart.</small>
  </form>

  <div class="results">
    {% if error %}
      <div class="error"><b data-i18n="results.error">Error:</b> {{ error }}</div>
    {% elif charts %}
      <div class="meta-card">
        <span class="meta-pill"><b>{{ form.name }}</b></span>
        <span class="meta-pill">{{ form.date }} &middot; {{ form.time }}</span>
        <span class="meta-pill accent"><span data-i18n="meta.rashi_asc">Rashi Asc:</span>
          <b data-i18n-term="sign:{{ ascendant }}">{{ ascendant }}</b></span>
        <span class="meta-pill accent"><span data-i18n="meta.navamsa_asc">Navamsa Asc:</span>
          <b data-i18n-term="sign:{{ navamsa_ascendant }}">{{ navamsa_ascendant }}</b></span>
        {% if playground_url %}
          <a class="meta-pill playground-btn" href="{{ playground_url }}" target="_blank" rel="noopener">&#129418; <span data-i18n="meta.playground">Play with Chart</span></a>
        {% endif %}
        <!-- Re-posts the same birth details to /download-pdf, so the export
             works on its own without any JS or server-side session state.
             The hidden `lang` field carries the currently selected language
             across, so the PDF comes out in whatever the page is showing. -->
        <form class="pdf-form" method="POST" action="/download-pdf">
          {% for field in ['name', 'city', 'date', 'time', 'lat', 'lng', 'tz', 'style'] %}
            <input type="hidden" name="{{ field }}" value="{{ form[field] }}">
          {% endfor %}
          <input type="hidden" name="lang" value="en" data-lang-field>
          <button type="submit" class="meta-pill pdf-btn">&#11015; <span data-i18n="meta.download_pdf">Download PDF</span></button>
        </form>
      </div>

      <div class="charts-grid">
        {% for card in charts %}
          <div class="chart-card">
            <h3 data-i18n="{{ card.label_key }}">{{ card.label }}</h3>
            {% for code, svg in card.svgs %}
              <div class="chart-svg" data-lang-svg="{{ code }}">{{ svg | safe }}</div>
            {% endfor %}
          </div>
        {% endfor %}
      </div>
      <small class="hint" data-i18n="chart.retro_hint">Retrograde planets are marked "(R)" on the Rashi (D1) charts. Navamsa (D9) doesn't conventionally mark retrograde.</small>

      <div class="section-title"><span data-i18n="section.star">Planetary &amp; Star (Nakshatra) Details</span></div>
      <small class="hint" data-i18n="star.hint">Combust planets (too close to the Sun) are marked with \U0001F525 next to their name.</small>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th data-i18n="th.planet">Planet</th>
              <th data-i18n="th.sign">Sign</th>
              <th data-i18n="th.degree">Degree</th>
              <th data-i18n="th.nakshatra">Nakshatra</th>
              <th data-i18n="th.pada">Pada</th>
              <th data-i18n="th.nak_lord">Nakshatra Lord</th>
            </tr>
          </thead>
          <tbody>
            {% for row in star_table %}
            <tr>
              <td>{% if row.combust %}\U0001F525 {% endif %}<span data-i18n-term="planet:{{ row.planet }}">{{ row.planet }}</span></td>
              <td data-i18n-term="sign:{{ row.sign }}">{{ row.sign }}</td>
              <td>{{ row.degree }}</td>
              <td data-i18n-term="nakshatra:{{ row.nakshatra }}">{{ row.nakshatra }}</td>
              <td>{{ row.pada }}</td>
              <td data-i18n-term="planet:{{ row.lord }}">{{ row.lord }}</td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>

      <div class="section-title"><span data-i18n="section.dasha">Vimshottari Mahadasha</span></div>
      <small class="hint" data-i18n="dasha.hint">Tap any row to expand its sub-periods (Antardasha &rarr; Pratyantardasha &rarr; Sookshma Dasha). Tap again to collapse.</small>
      <div class="table-wrap">
        <table id="dashaTable">
          <thead>
            <tr>
              <th data-i18n="th.lord">Lord</th>
              <th data-i18n="th.start">Start</th>
              <th data-i18n="th.end">End</th>
              <th data-i18n="th.years">Yrs</th>
            </tr>
          </thead>
          <tbody>
            {% for row in dasha_table %}
            <tr class="dasha-row level-0 {{ 'dasha-current' if row.is_current else '' }}"
                data-level="0" data-lord="{{ row.lord }}" data-start="{{ row.start }}" data-end="{{ row.end }}" data-years="{{ row.years_exact }}">
              <td><span class="toggle-arrow">&#9656;</span><span data-i18n-term="planet:{{ row.lord }}">{{ row.lord }}</span></td>
              <td>{{ row.start }}</td>
              <td>{{ row.end }}</td>
              <td>{{ row.years }}</td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
      <small class="hint" data-i18n="dasha.footnote">
        Computed with the standard Vimshottari algorithm (120-year cycle, 9 planetary
        lords) based on the Moon's Nakshatra at birth. Not provided by Kerykeion or
        jyotichart directly - neither library computes Nakshatra or Dasha.
      </small>

      <div class="section-title"><span data-i18n="section.houses">Houses Involved</span></div>
      <small class="hint" data-i18n="houses.hint">
        Tap a Mahadasha row to see the houses its lord activates (placement,
        aspects, and lordship - or for Rahu/Ketu, the houses ruled by every
        planet connected to it), along with that period's date range. Tap
        an Antardasha row to see both the Mahadasha and Antardasha lords
        together, or a Pratyantardasha row to add its lord as well - each
        with its own sub-period dates.
      </small>
      <div id="housesInvolvedBox" class="houses-box">
        <div class="placeholder-small" data-i18n="houses.placeholder">Tap a Mahadasha, Antardasha or Pratyantardasha row above.</div>
      </div>
      <script id="dashaHouseData" type="application/json">{{ dasha_house_json | safe }}</script>

      <div class="section-title"><span data-i18n="section.marriage">3-7-11 Connection (Marriage)</span></div>
      <small class="hint" data-i18n="marriage.hint">
        For marriage timing, the Dasha, Bhukti and Antaram lords should each
        connect to the 3rd, 7th or 11th house - by sitting in it, aspecting it,
        ruling it, exchanging signs with its lord, or sitting with its lord
        (Rahu/Ketu through the planets tied to them). Shows the period running today; tap a
        Mahadasha, Antardasha or Pratyantardasha row to check another.
        Below it, two more checks: a Venus Dasha or Bhukti whose other lords
        link to 3-7-11, and a Dasha or Bhukti of the 2nd lord.
      </small>
      <div id="marriageBox" class="houses-box"></div>
      <script id="marriageData" type="application/json">{{ marriage_json | safe }}</script>

      <div class="section-title"><span data-i18n="section.conj_degree">Conjunctions &ndash; By Degree (Orb)</span></div>
      <small class="hint" data-i18n="conj_degree.hint">
        Grahas (and the Ascendant) within 10&deg; of each other, worked out from
        actual longitude - not just a shared sign. Two bodies a couple of
        degrees apart but straddling a sign boundary still count; two bodies
        in the same sign but many degrees apart do not. See "By Sign" below
        for the traditional whole-sign view.
      </small>
      {% if conjunctions %}
      <div class="houses-box houses-box-row">
        {% for c in conjunctions %}
        <div class="planet-block">
          <div class="planet-name">
            {% for m in c.members %}<span data-i18n-term="planet:{{ m.planet }}">{{ m.planet }}</span>{% if not loop.last %} + {% endif %}{% endfor %}
            <span class="conj-tier conj-tier-{{ c.tightest_tier | lower }}" data-i18n-term="conj_tier:{{ c.tightest_tier }}">{{ c.tightest_tier }}</span>
          </div>
          <div class="detail-line"><span class="dl-label" data-i18n="conj.signs_label">Sign(s)</span>{% for s in c.signs %}<span data-i18n-term="sign:{{ s }}">{{ s }}</span>{% if not loop.last %} &rarr; {% endif %}{% endfor %}</div>
          {% for m in c.members %}
          <div class="detail-line"><span class="dl-label" data-i18n-term="planet:{{ m.planet }}">{{ m.planet }}</span>{{ m.degree }} <span data-i18n-term="sign:{{ m.sign }}">{{ m.sign }}</span></div>
          {% endfor %}
          <div class="muted-line conj-pairs">
            {% for p in c.pairs %}<span data-i18n-term="planet:{{ p.a }}">{{ p.a }}</span>&ndash;<span data-i18n-term="planet:{{ p.b }}">{{ p.b }}</span>: {{ p.orb }} <span data-i18n="conj.apart">apart</span> (<span data-i18n-term="conj_tier:{{ p.tier }}">{{ p.tier }}</span>){% if not loop.last %} &middot; {% endif %}{% endfor %}
          </div>
        </div>
        {% endfor %}
      </div>
      {% else %}
      <div class="houses-box"><div class="placeholder-small" data-i18n="conj_degree.none">No conjunctions within 10&deg; in this chart.</div></div>
      {% endif %}

      <div class="section-title"><span data-i18n="section.conj_sign">Conjunctions &ndash; By Sign (Rashi)</span></div>
      <small class="hint" data-i18n="conj_sign.hint">
        The traditional whole-sign yuti: every pair of grahas (and the
        Ascendant) sharing a sign, however many degrees apart within it -
        with that gap shown alongside, so a tight 2&deg; pairing and a loose
        25&deg; one in the same sign aren't lumped together as equivalent.
      </small>
      {% if sign_conjunctions %}
      <div class="houses-box houses-box-row">
        {% for s in sign_conjunctions %}
        <div class="planet-block">
          <div class="planet-name" data-i18n-term="sign:{{ s.sign }}">{{ s.sign }}</div>
          {% for m in s.members %}
          <div class="detail-line"><span class="dl-label" data-i18n-term="planet:{{ m.planet }}">{{ m.planet }}</span>{{ m.degree }}</div>
          {% endfor %}
          <div class="muted-line conj-pairs">
            {% for p in s.pairs %}<span data-i18n-term="planet:{{ p.a }}">{{ p.a }}</span>&ndash;<span data-i18n-term="planet:{{ p.b }}">{{ p.b }}</span>: {{ p.diff }} <span data-i18n="conj.apart">apart</span>{% if not loop.last %} &middot; {% endif %}{% endfor %}
          </div>
        </div>
        {% endfor %}
      </div>
      {% else %}
      <div class="houses-box"><div class="placeholder-small" data-i18n="conj_sign.none">No two bodies share a sign in this chart.</div></div>
      {% endif %}

      <script>
        (function () {
          const DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"];
          const DASHA_YEARS = {
            Ketu: 7, Venus: 20, Sun: 6, Moon: 10, Mars: 7,
            Rahu: 18, Jupiter: 16, Saturn: 19, Mercury: 17
          };
          const DAYS_PER_YEAR = 365.2425;
          const LEVEL_ROLES = ["Mahadasha", "Antardasha", "Pratyantardasha", "Sookshma Dasha"];
          const MAX_LEVEL = LEVEL_ROLES.length - 1;
          const HOUSES_BOX_MAX_LEVEL = 2; // box reacts to Mahadasha, Antardasha and Pratyantardasha clicks

          const houseDataEl = document.getElementById("dashaHouseData");
          let DASHA_HOUSE_DATA = {};
          try {
            DASHA_HOUSE_DATA = houseDataEl ? JSON.parse(houseDataEl.textContent || "{}") : {};
          } catch (err) {
            DASHA_HOUSE_DATA = {};
          }

          // Ordinals and house lists come from the shared runtime so they
          // read "3rd, 7th" in English and "3ஆம், 7ஆம்" in Tamil.
          const ordinal = (n) => I18N.ordinal(n);
          const housesList = (arr) => I18N.ordinalList(arr);
          const planet = (label) => I18N.term("planet", label);
          const sign = (name) => I18N.term("sign", name);

          function renderPlanetBlock(label, info) {
            if (!info) {
              return `<div class="planet-block"><div class="planet-name">${planet(label)}</div>
                <div class="muted-line">${I18N.t("houses.no_data")}</div></div>`;
            }
            if (info.type === "classical") {
              return `
                <div class="planet-block">
                  <div class="planet-line">${planet(label)} = ${I18N.t("phrase.lord_of")} ${housesList(info.lordship)} = ${I18N.t("phrase.placement")} - ${ordinal(info.placement)} = ${I18N.t("phrase.aspects")} - ${housesList(info.aspects)}</div>
                </div>`;
            }
            // Rahu/Ketu: same "= clause = clause" single-line pattern as the
            // classical grahas, but built from their connections (a node has
            // no lordship/aspects of its own) - dispositor of the sign it
            // occupies, placement, any planet conjunct with it, and any
            // planet whose aspect lands on its house.
            const dispositorConn = info.connections.find((c) => c.roles.includes("dispositor"));
            const conjunctConns = info.connections.filter((c) => c.roles.includes("conjunct"));
            const aspectingConns = info.connections.filter((c) => c.roles.includes("aspecting"));
            const connStr = (conns) => conns.map((c) => `${housesList(c.houses)} (${planet(c.planet)})`).join("; ");

            const dispositorStr = dispositorConn
              ? `${I18N.t("phrase.dispositor")} (${planet(dispositorConn.planet)}) ${I18N.t("phrase.of")} ${housesList(dispositorConn.houses)}`
              : I18N.t("phrase.dispositor_none");

            let line = `${planet(label)} = ${dispositorStr} = ${I18N.t("phrase.placement")} - ${ordinal(info.placement)} ${I18N.t("phrase.house")} (${sign(info.sign)})`;
            if (conjunctConns.length) line += ` = ${I18N.t("phrase.conjunct")} - ${connStr(conjunctConns)}`;
            line += ` = ${I18N.t("phrase.aspected_by")} - ${aspectingConns.length ? connStr(aspectingConns) : I18N.t("phrase.none")}`;

            return `
              <div class="planet-block">
                <div class="planet-line">${line}</div>
              </div>`;
          }

          // Remembered so a language switch can redraw the box with whatever
          // period the user last tapped, instead of resetting it.
          let currentHousesSelection = null;

          function updateHousesBox(lords) {
            currentHousesSelection = lords;
            const box = document.getElementById("housesInvolvedBox");
            if (!box) return;
            box.innerHTML = lords.map((l) => `
              <div class="dasha-level-block">
                <div class="dl-heading">${I18N.term("dasha_level", l.role)}: ${planet(l.label)}<span class="dl-period">(${l.start} &rarr; ${l.end})</span></div>
                ${renderPlanetBlock(l.label, DASHA_HOUSE_DATA[l.label])}
              </div>`).join("");
          }

          function addDays(dateObj, days) {
            return new Date(dateObj.getTime() + days * 86400000);
          }
          function isoDate(d) {
            return d.toISOString().slice(0, 10);
          }

          function computeSubPeriods(lord, startISO, years) {
            const startIdx = DASHA_ORDER.indexOf(lord);
            let cursor = new Date(startISO + "T00:00:00Z");
            const out = [];
            for (let i = 0; i < 9; i++) {
              const subLord = DASHA_ORDER[(startIdx + i) % 9];
              const subYears = years * DASHA_YEARS[subLord] / 120;
              const end = addDays(cursor, subYears * DAYS_PER_YEAR);
              out.push({ lord: subLord, start: isoDate(cursor), end: isoDate(end), years: subYears });
              cursor = end;
            }
            return out;
          }

          const tbody = document.querySelector("#dashaTable tbody");
          if (!tbody) return;

          // ── 3-7-11 (marriage) box ──────────────────────────────────
          // Links per lord come from build_marriage_links; the periods are
          // walked here with the same computeSubPeriods the table uses.
          const marriageEl = document.getElementById("marriageData");
          let MARRIAGE_LINKS = {};
          try {
            MARRIAGE_LINKS = marriageEl ? JSON.parse(marriageEl.textContent || "{}") : {};
          } catch (err) {
            MARRIAGE_LINKS = {};
          }
          const MARRIAGE_HOUSES = [3, 7, 11];
          const UPCOMING_LIMIT = 8;
          const linksOf = (lord) => MARRIAGE_LINKS[lord] || [];
          const connects = (lord) => linksOf(lord).length > 0;
          const housesReached = (lords) =>
            MARRIAGE_HOUSES.filter((h) => lords.some((lord) => linksOf(lord).some((l) => l.house === h)));
          const linkText = (l) =>
            I18N.t("marriage.how_" + l.how, { h: ordinal(l.house), planet: l.via ? planet(l.via) : "" });
          const todayISO = () => isoDate(new Date());

          // Mahadasha -> Antardasha -> Pratyantardasha running today, as the
          // same {role, label, start, end} chain a row tap produces.
          function currentChain(today) {
            const maha = tbody.querySelector("tr.dasha-row.level-0.dasha-current");
            if (!maha) return null;
            const chain = lordChain(maha);
            let parent = { lord: maha.dataset.lord, start: maha.dataset.start, years: parseFloat(maha.dataset.years) };
            for (let level = 1; level <= 2; level++) {
              const sub = computeSubPeriods(parent.lord, parent.start, parent.years)
                .find((p) => p.start <= today && today < p.end);
              if (!sub) break;
              chain.push({ role: LEVEL_ROLES[level], label: sub.lord, start: sub.start, end: sub.end });
              parent = sub;
            }
            return chain;
          }

          // The 2nd lord (kudumba sthana) - the classical graha whose lordship
          // includes the 2nd house.
          const SECOND_LORD = Object.keys(DASHA_HOUSE_DATA).find((label) =>
            DASHA_HOUSE_DATA[label].type === "classical" && DASHA_HOUSE_DATA[label].lordship.includes(2)) || null;
          const SECOND_LORD_LIMIT = 4;

          // The three marriage checks for a chain of lords, outermost first:
          //   r1 3-7-11   - every lord links to the 3rd, 7th or 11th;
          //   r2 Venus    - Venus runs the Dasha or Bhukti (the Antaram alone
          //                 doesn't count) and every *other* lord links to
          //                 3-7-11 - Venus stands in for its own slot;
          //   r3 2nd lord - the 2nd lord runs the Dasha or Bhukti.
          // Each is "yes", "no", or "open" when a shorter chain (a Mahadasha
          // or Antardasha tap) can't decide it yet.
          function marriageChecks(lords) {
            const full = lords.length === 3;
            const r1 = lords.some((l) => !connects(l)) ? "no" : full ? "yes" : "open";
            const venusSlots = [0, 1].filter((i) => lords[i] === "Venus");
            const others = lords.filter((_, i) => !venusSlots.includes(i));
            const r2 = !venusSlots.length ? (lords.length >= 2 ? "no" : "open")
              : others.some((l) => !connects(l)) ? "no" : full ? "yes" : "open";
            const r3 = lords.slice(0, 2).includes(SECOND_LORD) ? "yes" : lords.length >= 2 ? "no" : "open";
            return { r1, r2, r3, venusSlots, others };
          }

          // The next Antaram periods (from today) that pass the 3-7-11 or the
          // Venus check, each tagged with the checks it passes.
          function upcomingMatches(today, limit) {
            const out = [];
            for (const maha of tbody.querySelectorAll("tr.dasha-row.level-0")) {
              if (maha.dataset.end < today) continue;
              for (const b of computeSubPeriods(maha.dataset.lord, maha.dataset.start, parseFloat(maha.dataset.years))) {
                if (b.end < today) continue;
                for (const a of computeSubPeriods(b.lord, b.start, b.years)) {
                  if (a.end < today) continue;
                  const lords = [maha.dataset.lord, b.lord, a.lord];
                  const c = marriageChecks(lords);
                  if (c.r1 !== "yes" && c.r2 !== "yes") continue;
                  out.push({ lords, start: a.start, end: a.end, r1: c.r1 === "yes", r2: c.r2 === "yes" });
                  if (out.length >= limit) return out;
                }
              }
            }
            return out;
          }

          // The next Dasha or Bhukti the 2nd lord runs. The check is decided
          // at those two levels, so a whole 2nd-lord Mahadasha is one window
          // rather than dozens of Antaram rows.
          function upcomingSecondLord(today, limit) {
            const out = [];
            if (!SECOND_LORD) return out;
            for (const maha of tbody.querySelectorAll("tr.dasha-row.level-0")) {
              if (maha.dataset.end < today) continue;
              if (maha.dataset.lord === SECOND_LORD) {
                out.push({ lords: [SECOND_LORD], role: LEVEL_ROLES[0], start: maha.dataset.start, end: maha.dataset.end });
              } else {
                const b = computeSubPeriods(maha.dataset.lord, maha.dataset.start, parseFloat(maha.dataset.years))
                  .find((p) => p.lord === SECOND_LORD && p.end >= today);
                if (b) out.push({ lords: [maha.dataset.lord, SECOND_LORD], role: LEVEL_ROLES[1], start: b.start, end: b.end });
              }
              if (out.length >= limit) break;
            }
            return out;
          }

          function upcomingHtml(today) {
            const tag = (key) => `<span class="m-tag">${I18N.t(key)}</span>`;
            const now = (r) => r.start <= today ? ` (${I18N.t("marriage.now")})` : "";
            const rows = upcomingMatches(today, UPCOMING_LIMIT);
            const body = rows.length
              ? `<div class="m-upcoming-wrap"><table class="m-upcoming">${rows.map((r) => `
                  <tr class="${r.start <= today ? "now" : ""}">
                    <td>${r.lords.map(planet).join(" &ndash; ")}${now(r)}</td>
                    <td>${r.start} &rarr; ${r.end}</td>
                    <td>${r.r1 ? tag("marriage.tag_3711") : ""}${r.r2 ? tag("marriage.tag_venus") : ""}</td>
                  </tr>`).join("")}</table></div>`
              : `<div class="muted-line">${I18N.t("marriage.upcoming_none")}</div>`;
            const second = upcomingSecondLord(today, SECOND_LORD_LIMIT);
            const secondBody = second.length
              ? `<div class="m-upcoming-wrap"><table class="m-upcoming">${second.map((r) => `
                  <tr class="${r.start <= today ? "now" : ""}">
                    <td>${r.lords.map(planet).join(" &ndash; ")} ${I18N.term("dasha_level", r.role)}${now(r)}</td>
                    <td>${r.start} &rarr; ${r.end}</td>
                  </tr>`).join("")}</table></div>`
              : `<div class="muted-line">${I18N.t("marriage.second_upcoming_none")}</div>`;
            return `<div class="m-upcoming-title">${I18N.t("marriage.upcoming")}</div>${body}
              <div class="m-upcoming-title">${I18N.t("marriage.second_upcoming", { planet: SECOND_LORD ? planet(SECOND_LORD) : "" })}</div>${secondBody}`;
          }

          // The Venus and 2nd-lord checks for the chain in the box, as two
          // rows under the 3-7-11 verdict.
          function extraChecksHtml(chain) {
            const lords = chain.map((l) => l.label);
            const c = marriageChecks(lords);
            const roleOf = (i) => I18N.term("dasha_level", chain[i].role);
            const mark = { yes: "&#10003;", no: "&#10007;", open: "&hellip;" };

            let venusMsg;
            if (c.venusSlots.length) {
              const role = c.venusSlots.map(roleOf).join(" & ");
              const failing = c.others.filter((l) => !connects(l));
              venusMsg = c.r2 === "yes" ? I18N.t("marriage.venus_yes", { role })
                : c.r2 === "no" ? I18N.t("marriage.venus_others_fail", { role, lords: failing.map(planet).join(", ") })
                : I18N.t("marriage.venus_open", { role });
            } else {
              venusMsg = c.r2 === "no" ? I18N.t("marriage.venus_absent") : I18N.t("marriage.venus_pick_bhukti");
            }

            let secondMsg;
            if (!SECOND_LORD) secondMsg = I18N.t("houses.no_data");
            else if (c.r3 === "yes") secondMsg = I18N.t("marriage.second_yes", { planet: planet(SECOND_LORD), role: roleOf(lords.indexOf(SECOND_LORD)) });
            else if (c.r3 === "no") secondMsg = I18N.t("marriage.second_no", { planet: planet(SECOND_LORD) });
            else secondMsg = I18N.t("marriage.second_open", { planet: planet(SECOND_LORD) });

            const row = (status, titleKey, msg) => `
              <div class="m-check ${status}">
                <span class="m-mark">${mark[status]}</span>
                <div><div class="m-check-title">${I18N.t(titleKey)}</div><div>${msg}</div></div>
              </div>`;
            return `<div class="m-upcoming-title">${I18N.t("marriage.more_checks")}</div>
              ${row(c.r2, "marriage.venus_title", venusMsg)}
              ${row(c.r3, "marriage.second_title", secondMsg)}`;
          }

          // Remembered for a redraw on a language switch, like the Houses box.
          let marriageSelection = null;

          function updateMarriageBox(chain, isCurrent) {
            marriageSelection = { chain, isCurrent };
            const box = document.getElementById("marriageBox");
            if (!box) return;
            const today = todayISO();
            if (!chain || !chain.length) {
              box.innerHTML = `<div class="placeholder-small">${I18N.t("marriage.no_current")}</div>${upcomingHtml(today)}`;
              return;
            }
            const blocks = chain.map((l) => {
              const links = linksOf(l.label);
              const body = links.length
                ? `<ul class="m-links">${links.map((x) => `<li>${linkText(x)}</li>`).join("")}</ul>`
                : `<div class="muted-line">${I18N.t("marriage.no_link")}</div>`;
              return `
                <div class="dasha-level-block">
                  <div class="dl-heading">${links.length ? "&#10003;" : "&#10007;"} ${I18N.term("dasha_level", l.role)}: ${planet(l.label)}<span class="dl-period">(${l.start} &rarr; ${l.end})</span></div>
                  <div class="planet-block">${body}</div>
                </div>`;
            }).join("");
            // A lord with no link fails the period at any depth; with every
            // lord so far linked, only the full three-level chain can pass.
            const missing = chain.filter((l) => !connects(l.label));
            const passed = !missing.length && chain.length === 3;
            const verdict = missing.length
              ? I18N.t("marriage.no", { lords: missing.map((l) => planet(l.label)).join(", ") })
              : passed ? I18N.t("marriage.yes") : I18N.t("marriage.need_antaram");
            const reached = housesReached(chain.map((l) => l.label));
            const chips = MARRIAGE_HOUSES
              .map((h) => `<span class="m-house${reached.includes(h) ? " on" : ""}">${ordinal(h)}</span>`).join("");
            box.innerHTML = `
              <div class="m-caption">${I18N.t(isCurrent ? "marriage.showing_current" : "marriage.showing_selected")}</div>
              ${blocks}
              <div class="m-verdict${passed ? " on" : ""}">${verdict}</div>
              <div class="m-touch">${I18N.t("marriage.touches")} ${chips}</div>
              ${extraChecksHtml(chain)}
              ${upcomingHtml(today)}`;
          }

          // Each row's lord plus every ancestor above it, outermost first -
          // what the Houses Involved box lists when that row is tapped.
          // Server-rendered Mahadasha rows have no stored chain; theirs is
          // just the row itself.
          function lordChain(row) {
            if (row.dataset.chain) return JSON.parse(row.dataset.chain);
            return [{ role: LEVEL_ROLES[0], label: row.dataset.lord, start: row.dataset.start, end: row.dataset.end }];
          }

          function collapseRow(row) {
            const level = parseInt(row.dataset.level, 10);
            let next = row.nextElementSibling;
            while (next && parseInt(next.dataset.level, 10) > level) {
              const toRemove = next;
              next = next.nextElementSibling;
              toRemove.remove();
            }
            row.classList.remove("expanded");
          }

          function expandRow(row) {
            const level = parseInt(row.dataset.level, 10);
            const periods = computeSubPeriods(row.dataset.lord, row.dataset.start, parseFloat(row.dataset.years));
            const parentChain = lordChain(row);
            let anchor = row;
            periods.forEach((p) => {
              const tr = document.createElement("tr");
              const childLevel = level + 1;
              tr.className = `dasha-row level-${childLevel}`;
              tr.dataset.level = childLevel;
              tr.dataset.lord = p.lord;
              tr.dataset.start = p.start;
              tr.dataset.end = p.end;
              tr.dataset.years = p.years;
              tr.dataset.chain = JSON.stringify(parentChain.concat(
                { role: LEVEL_ROLES[childLevel], label: p.lord, start: p.start, end: p.end }
              ));
              const arrow = childLevel < MAX_LEVEL
                ? '<span class="toggle-arrow">&#9656;</span>'
                : '<span class="toggle-arrow"></span>';
              // data-i18n-term lets I18N.apply() re-translate these rows on a
              // language switch without having to rebuild the tree.
              tr.innerHTML = `<td>${arrow}<span data-i18n-term="planet:${p.lord}">${planet(p.lord)}</span></td>` +
                `<td>${p.start}</td><td>${p.end}</td><td>${p.years.toFixed(3)}</td>`;
              anchor.after(tr);
              anchor = tr;
            });
            row.classList.add("expanded");
          }

          tbody.addEventListener("click", (e) => {
            const row = e.target.closest(".dasha-row");
            if (!row) return;
            const level = parseInt(row.dataset.level, 10);

            if (level <= HOUSES_BOX_MAX_LEVEL) {
              tbody.querySelectorAll(".dasha-selected").forEach((r) => r.classList.remove("dasha-selected"));
              row.classList.add("dasha-selected");
              updateHousesBox(lordChain(row));
              updateMarriageBox(lordChain(row), false);
            }

            if (level >= MAX_LEVEL) return;
            if (row.classList.contains("expanded")) {
              collapseRow(row);
            } else {
              expandRow(row);
            }
          });

          // The expanded dasha rows carry data-i18n-term, so I18N.apply()
          // handles them; the Houses Involved box is free-form prose and has
          // to be rebuilt from the last selection.
          I18N.onChange(() => {
            if (currentHousesSelection) updateHousesBox(currentHousesSelection);
            if (marriageSelection) updateMarriageBox(marriageSelection.chain, marriageSelection.isCurrent);
          });

          updateMarriageBox(currentChain(todayISO()), true);
        })();
      </script>
    {% else %}
      <div class="card placeholder-card">
        <div class="ph-icon">&#10022;</div>
        <span data-i18n="results.placeholder">Fill in the birth details and tap "Generate Chart" to see the natal chart here.</span>
      </div>
    {% endif %}
  </div>
</div>

<script>
  // "Confirm place" - geocode the typed birth city on the server (geopy /
  // Nominatim) and drop the result straight into the lat/lng inputs.
  (function () {
    const btn = document.getElementById("confirmPlaceBtn");
    const cityInput = document.getElementById("city");
    const latInput = document.getElementById("lat");
    const lngInput = document.getElementById("lng");
    const status = document.getElementById("geoStatus");
    if (!btn) return;

    // Status text is set from JS, so it can't carry a data-i18n attribute -
    // stash the key on the element instead and re-render it on a switch.
    function setStatus(msg, kind) {
      status.textContent = msg;
      status.className = "geo-status" + (kind ? " " + kind : "");
      status.removeAttribute("data-i18n");
    }

    async function confirmPlace() {
      const place = cityInput.value.trim();
      if (!place) {
        setStatus(I18N.t("geo.need_city"), "bad");
        cityInput.focus();
        return;
      }

      btn.disabled = true;
      setStatus(I18N.t("geo.looking", { place }), "");

      try {
        const res = await fetch("/geocode", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams({ place }),
        });
        const data = await res.json();

        if (!res.ok) {
          setStatus(data.error || I18N.t("geo.failed"), "bad");
          return;
        }

        latInput.value = data.lat;
        lngInput.value = data.lng;
        setStatus(data.address + " → " + data.lat + ", " + data.lng, "ok");
      } catch (err) {
        setStatus(I18N.t("geo.offline"), "bad");
      } finally {
        btn.disabled = false;
      }
    }

    btn.addEventListener("click", confirmPlace);

    // Enter inside the city box should confirm the place, not submit the form.
    cityInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        confirmPlace();
      }
    });
  })();

  // "Now" - fills the date/time fields with the current local date and time.
  (function () {
    const btn = document.getElementById("nowBtn");
    const dateInput = document.getElementById("date");
    const timeInput = document.getElementById("time");
    if (!btn) return;

    function pad(n) { return String(n).padStart(2, "0"); }

    btn.addEventListener("click", () => {
      const now = new Date();
      dateInput.value = now.getFullYear() + "-" + pad(now.getMonth() + 1) + "-" + pad(now.getDate());
      timeInput.value = pad(now.getHours()) + ":" + pad(now.getMinutes());
    });
  })();

  // "Save details" - stores the current form values in the database so they
  // show up in /admin, without generating a chart or leaving this page.
  (function () {
    const btn = document.getElementById("saveDetailsBtn");
    const status = document.getElementById("saveStatus");
    if (!btn) return;

    function setStatus(msg, kind) {
      status.textContent = msg;
      status.className = "save-status" + (kind ? " " + kind : "");
      status.removeAttribute("data-i18n");
    }

    async function saveDetails() {
      const form = btn.closest("form");
      const data = new FormData(form);

      if (!data.get("name")?.trim()) {
        setStatus(I18N.t("save.need_name"), "bad");
        document.getElementById("name").focus();
        return;
      }

      btn.disabled = true;
      setStatus(I18N.t("save.saving"), "");

      try {
        const res = await fetch("/save", {
          method: "POST",
          body: new URLSearchParams(data),
        });
        const result = await res.json();

        if (!res.ok) {
          setStatus(result.error || I18N.t("save.failed"), "bad");
          return;
        }

        setStatus(I18N.t("save.ok"), "ok");
      } catch (err) {
        setStatus(I18N.t("save.offline"), "bad");
      } finally {
        btn.disabled = false;
      }
    }

    btn.addEventListener("click", saveDetails);
  })();

  // Keep the PDF export's hidden `lang` field in step with the toggle, so
  // "Download PDF" always produces the language currently on screen.
  (function () {
    function syncLangFields(lang) {
      document.querySelectorAll("[data-lang-field]").forEach((el) => {
        el.value = lang;
      });
    }
    syncLangFields(I18N.lang);
    I18N.onChange(syncLangFields);
  })();

  // Register the service worker (enables installability + basic offline shell).
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("/service-worker.js").catch(() => {});
    });
  }

  // Optional "Install App" button, shown only when the browser actually
  // offers an install prompt (Chrome/Edge/Android). iOS Safari has no
  // programmatic prompt - users add via Share -> Add to Home Screen.
  (function () {
    const installBtn = document.getElementById("installBtn");
    let deferredPrompt = null;

    window.addEventListener("beforeinstallprompt", (e) => {
      e.preventDefault();
      deferredPrompt = e;
      installBtn.classList.add("visible");
    });

    installBtn.addEventListener("click", async () => {
      if (!deferredPrompt) return;
      installBtn.classList.remove("visible");
      deferredPrompt.prompt();
      await deferredPrompt.userChoice;
      deferredPrompt = null;
    });

    window.addEventListener("appinstalled", () => {
      installBtn.classList.remove("visible");
    });
  })();

  // After generating a chart, smoothly bring the results into view -
  // helpful on mobile where the form can push results below the fold.
  (function () {
    const results = document.querySelector(".results");
    const hasCharts = document.querySelector(".charts-grid");
    if (results && hasCharts && window.innerWidth < 960) {
      results.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  })();
</script>

</body>
</html>
"""

# ---------------------------------------------------------------------------
# Admin panel: password-gated login + a card view of every saved record.
# ---------------------------------------------------------------------------

ADMIN_LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title data-i18n="admin.login_page_title">Admin sign in - Vedic Birth Chart</title>
{{ lang_boot | safe }}
<script src="/i18n.js"></script>
<style>
  :root {
    --bg: #0b0d17; --surface: #151829; --border: #282d4c;
    --text: #f3f2fa; --muted: #9a9db8; --primary: #7c6bf2; --danger: #ff6b81;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100vh; display: flex; align-items: center; justify-content: center;
    background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }
  form {
    background: var(--surface); border: 1px solid var(--border); border-radius: 16px;
    padding: 32px; width: 100%; max-width: 340px; display: flex; flex-direction: column; gap: 14px;
  }
  h1 { margin: 0 0 4px; font-size: 1.3rem; }
  label { font-size: .85rem; color: var(--muted); }
  input[type=password] {
    width: 100%; margin-top: 4px; padding: 10px 12px; border-radius: 10px;
    border: 1px solid var(--border); background: var(--bg); color: var(--text); font-size: 1rem;
  }
  button {
    padding: 10px 12px; border-radius: 10px; border: none; background: var(--primary);
    color: #fff; font-weight: 600; cursor: pointer; font-size: 1rem;
  }
  .error { color: var(--danger); font-size: .85rem; margin: 0; }
  .lang-row { display: flex; justify-content: center; }
{{ lang_switch_css }}
</style>
</head>
<body>
<form method="POST" action="{{ url_for('admin_login') }}">
  <div class="lang-row">{{ lang_switch | safe }}</div>
  <h1 data-i18n="admin.login_title">Admin sign in</h1>
  {% if error %}<p class="error" data-i18n="{{ error }}">{{ t(error) }}</p>{% endif %}
  <div>
    <label for="password" data-i18n="admin.password">Password</label>
    <input type="password" id="password" name="password" autofocus required>
  </div>
  <input type="hidden" name="next" value="{{ next }}">
  <button type="submit" data-i18n="admin.sign_in">Sign in</button>
</form>
</body>
</html>
"""

ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" data-lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title data-i18n="admin.page_title">Admin - Stored Birth Details</title>
{{ lang_boot | safe }}
<script src="/i18n.js"></script>
<style>
  :root {
    --bg: #0b0d17; --surface: #151829; --border: #282d4c;
    --text: #f3f2fa; --muted: #9a9db8; --primary: #7c6bf2;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--text); padding: 24px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }
  .top-bar {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 20px; gap: 12px; flex-wrap: wrap;
  }
  .top-bar h1 { font-size: 1.4rem; margin: 0; }
  .top-bar .links { display: flex; gap: 10px; }
  .top-bar a {
    color: var(--muted); font-size: .85rem; text-decoration: none;
    border: 1px solid var(--border); padding: 6px 12px; border-radius: 8px;
  }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }
  .card {
    background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
    padding: 16px; display: flex; flex-direction: column; gap: 6px;
  }
  .card h2 { margin: 0 0 4px; font-size: 1.05rem; }
  .card p.city { margin: 0 0 4px; font-size: .85rem; color: var(--muted); }
  .card .row { display: flex; justify-content: space-between; font-size: .85rem; color: var(--muted); }
  .card a.go-btn {
    margin-top: 10px; text-align: center; background: var(--primary); color: #fff;
    text-decoration: none; padding: 9px 12px; border-radius: 9px; font-weight: 600; font-size: .9rem;
  }
  .empty { color: var(--muted); }
{{ lang_switch_css }}
</style>
</head>
<body>
<div class="top-bar">
  <h1><span data-i18n="admin.stored">Stored birth details</span> ({{ records|length }})</h1>
  <div class="links">
    {{ lang_switch | safe }}
    <a href="{{ url_for('index') }}" data-i18n="admin.new_chart">New chart</a>
    <a href="{{ url_for('admin_logout') }}" data-i18n="admin.log_out">Log out</a>
  </div>
</div>
{% if records %}
<div class="grid">
  {% for r in records %}
  <div class="card">
    <h2>{{ r.name }}</h2>
    {% if r.city %}
      <p class="city">{{ r.city }}</p>
    {% else %}
      <p class="city" data-i18n="admin.unknown_city">Unknown city</p>
    {% endif %}
    <div class="row"><span data-i18n="admin.dob">Date of birth</span><span>{{ r.date }}</span></div>
    <div class="row"><span data-i18n="admin.tob">Time of birth</span><span>{{ r.time }}</span></div>
    <div class="row"><span data-i18n="admin.latlng">Lat, Lng</span><span>{{ r.lat }}, {{ r.lng }}</span></div>
    <div class="row"><span data-i18n="admin.timezone">Timezone</span><span>{{ r.tz }}</span></div>
    <div class="row"><span data-i18n="admin.saved_at">Saved</span><span>{{ r.updated_at.strftime("%Y-%m-%d %H:%M") if r.updated_at else "" }}</span></div>
    <a class="go-btn" href="{{ url_for('index', record_id=r.id) }}" data-i18n="admin.go_to_chart">Go to chart</a>
  </div>
  {% endfor %}
</div>
{% else %}
<p class="empty" data-i18n="admin.empty">No records saved yet - generate a chart on the main page to see it here.</p>
{% endif %}
</body>
</html>
"""

DEFAULT_FORM = {
    "name": "Jane Doe",
    "city": "Mumbai",
    "date": "1998-11-10",
    "time": "03:45",
    "lat": "19.0760",
    "lng": "72.8777",
    "tz": "Asia/Kolkata",
    "style": "south",
}


@app.route("/", methods=["GET"])
def index():
    # ?record_id=<id> comes from the admin panel's "Go to chart" button -
    # prefill the form from a previously saved record instead of the demo
    # defaults. The chart still isn't generated until the user hits Generate.
    form = DEFAULT_FORM
    record_id = request.args.get("record_id", type=int)
    if record_id:
        record = storage.get_birth_record(record_id)
        if record:
            form = {
                "name": record["name"] or "",
                "city": record["city"] or "",
                "date": record["date"] or "",
                "time": record["time"] or "",
                "lat": record["lat"] or "",
                "lng": record["lng"] or "",
                "tz": record["tz"] or "",
                "style": record["style"] or "south",
            }

    return render_template_string(
        PAGE_TEMPLATE, form=form, charts=None, error=None,
        ascendant=None, navamsa_ascendant=None, star_table=None,
        dasha_table=None, dasha_house_json="{}", marriage_json="{}", conjunctions=None,
        sign_conjunctions=None, playground_url=None,
    )


def read_form(req):
    """Pull the birth-details fields out of a submitted form."""
    return {
        "name": req.form.get("name", "").strip() or "Chart",
        "city": req.form.get("city", "").strip(),
        "date": req.form.get("date", ""),
        "time": req.form.get("time", ""),
        "lat": req.form.get("lat", ""),
        "lng": req.form.get("lng", ""),
        "tz": req.form.get("tz", "").strip(),
        "style": req.form.get("style", "south"),
    }


def build_chart_context(form):
    """Everything the results page (and the PDF export) needs for one chart.

    Raises whatever the parsing/ephemeris code raises - callers decide how to
    show the failure.
    """
    from datetime import datetime as _dt

    year, month, day = (int(x) for x in form["date"].split("-"))
    hour, minute = (int(x) for x in form["time"].split(":"))
    lat = float(form["lat"])
    lng = float(form["lng"])

    subject = build_vedic_subject(
        name=form["name"],
        year=year, month=month, day=day, hour=hour, minute=minute,
        lat=lat, lng=lng, tz_str=form["tz"], city=form["city"] or "Unknown",
    )

    styles_to_render = (
        ["south", "north"] if form["style"] == "both" else [form["style"]]
    )

    # Each chart is drawn once per language and both copies are handed to
    # the page, which shows one and hides the other via CSS - that makes the
    # language toggle instant instead of a re-submit. jyotichart is a pure
    # string-writing renderer, so the extra pass is cheap.
    charts = []
    ascendant = None
    with tempfile.TemporaryDirectory() as tmp_dir:
        for style in styles_to_render:
            svgs = []
            for lang in i18n.LANGUAGES:
                asc, svg = render_chart_svg(subject, style, tmp_dir, lang)
                ascendant = asc
                svgs.append((lang, svg))
            label_key = "chart.south_d1" if style == "south" else "chart.north_d1"
            charts.append({
                "label_key": label_key,
                "label": i18n.t(label_key),
                "svgs": svgs,
            })

        navamsa_positions = build_navamsa_positions(subject)
        navamsa_ascendant = SIGN_NAME_MAP[navamsa_positions["Ascendant"]]
        for style in styles_to_render:
            svgs = []
            for lang in i18n.LANGUAGES:
                asc9, svg9 = render_navamsa_chart_svg(subject, style, tmp_dir, navamsa_positions, lang)
                svgs.append((lang, svg9))
            label_key9 = "chart.south_d9" if style == "south" else "chart.north_d9"
            charts.append({
                "label_key": label_key9,
                "label": i18n.t(label_key9),
                "svgs": svgs,
            })

    birth_dt = _dt(year, month, day, hour, minute)
    dasha_table = build_dasha_table(subject, birth_dt)

    # Mark whichever Mahadasha row covers today's date
    now = _dt.now()
    for row in dasha_table:
        row_start = _dt.strptime(row["start"], "%Y-%m-%d")
        row_end = _dt.strptime(row["end"], "%Y-%m-%d")
        row["is_current"] = row_start <= now <= row_end

    ascendant_abbr = subject.first_house["sign"]
    dasha_house_map = build_dasha_house_map(subject, ascendant_abbr)
    marriage_links = build_marriage_links(subject, dasha_house_map)

    return {
        "subject": subject,
        "charts": charts,
        "ascendant": ascendant,
        "navamsa_ascendant": navamsa_ascendant,
        "star_table": build_star_table(subject),
        "conjunctions": build_conjunctions(subject),
        "sign_conjunctions": build_sign_conjunctions(subject),
        "dasha_table": dasha_table,
        "bhukti_window": build_dasha_bhukti_window(dasha_table, now),
        "dasha_house_map": dasha_house_map,
        "dasha_house_json": json.dumps(dasha_house_map),
        "marriage_links": marriage_links,
        "marriage_json": json.dumps(marriage_links),
        "playground_url": build_playground_url(subject),
    }


@app.route("/generate", methods=["GET", "POST"])
def generate():
    # A plain GET here means someone refreshed the results page, followed a
    # bookmark, or hit Back/Forward - there's no submitted form data to work
    # with, so just send them back to the form instead of a 405.
    if request.method == "GET":
        return redirect(url_for("index"))

    form = read_form(request)

    try:
        ctx = build_chart_context(form)
        return render_template_string(
            PAGE_TEMPLATE, form=form, error=None,
            charts=ctx["charts"], ascendant=ctx["ascendant"],
            navamsa_ascendant=ctx["navamsa_ascendant"], star_table=ctx["star_table"],
            dasha_table=ctx["dasha_table"], dasha_house_json=ctx["dasha_house_json"],
            marriage_json=ctx["marriage_json"],
            conjunctions=ctx["conjunctions"], sign_conjunctions=ctx["sign_conjunctions"],
            playground_url=ctx["playground_url"],
        )

    except Exception as e:
        return render_template_string(
            PAGE_TEMPLATE, form=form, charts=None, error=str(e), ascendant=None,
            navamsa_ascendant=None, star_table=None, dasha_table=None, dasha_house_json="{}",
            marriage_json="{}",
            conjunctions=None, sign_conjunctions=None, playground_url=None,
        )


def _pdf_content_disposition(name):
    """Build the download header for a person's chart PDF.

    WSGI headers have to be latin-1 safe, so a name in Tamil, Devanagari, etc.
    can't go in the plain filename= value. Send an ASCII-only fallback there
    and the real name in the RFC 5987 filename*= form, which every current
    browser prefers when both are present.
    """
    full = f"{name}_vedic_chart.pdf".replace(" ", "_")

    ascii_slug = "".join(
        c for c in name if (c.isascii() and c.isalnum()) or c in " -_"
    ).strip().replace(" ", "_") or "chart"
    fallback = f"{ascii_slug}_vedic_chart.pdf"

    encoded = urllib.parse.quote(full, safe="")
    return f"attachment; filename=\"{fallback}\"; filename*=UTF-8''{encoded}"


@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    """Render the current birth details to a printable PDF.

    The results page posts the same fields /generate got, so the chart is
    recomputed here rather than cached between requests - the ephemeris work
    is quick, and it keeps the export usable straight from a bookmark or a
    saved record.
    """
    form = read_form(request)

    # The results page posts whichever language the toggle is on; anything
    # unrecognised falls back to English rather than erroring.
    lang = request.form.get("lang", i18n.DEFAULT_LANGUAGE)
    if lang not in i18n.LANGUAGES:
        lang = i18n.DEFAULT_LANGUAGE

    if chart_pdf is None:
        return (
            "PDF export needs reportlab and svglib: pip install reportlab svglib",
            500,
        )

    try:
        ctx = build_chart_context(form)
        pdf_bytes = chart_pdf.build_chart_pdf(form, ctx, lang)
    except Exception as e:
        return f"Could not build the PDF: {e}", 400

    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": _pdf_content_disposition(form["name"])},
    )


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    next_url = request.args.get("next") or request.form.get("next") or url_for("admin_panel")
    error = None
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(next_url)
        # A translation key rather than a sentence, so the login page can
        # re-render it when the language toggle is used.
        error = "admin.wrong_password"
    return render_template_string(ADMIN_LOGIN_TEMPLATE, error=error, next=next_url)


@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin_login"))


@app.route("/admin")
@admin_required
def admin_panel():
    records = storage.list_birth_records()
    return render_template_string(ADMIN_TEMPLATE, records=records)


if __name__ == "__main__":
    #app.run(debug=True, host="0.0.0.0")
    app.run(debug=True, host="127.0.0.1", port=5050)
