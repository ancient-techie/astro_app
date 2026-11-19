"""
Muhurtham - choosing a good time for a vivaham, a griha pravesham or a new
vehicle, from the panchangam and the person's own janma nakshatra.

Pure rules, no ephemeris: every input is a day already worked out by
panchang.compute(), so the only astronomy in a muhurtham is the
panchangam's. The tables below are the whole of the judgement, kept as
data so a family's own tradition can be written in without touching the
logic. They follow Muhurta Chintamani as Tamil calendars read it; where
printed panchangams differ (and they do), the table is the place to change.

The unit is a window, not a date. A tithi or nakshatra often changes
mid-morning, so a date judged as a whole would recommend a day whose good
star ended at nine. Each day's daylight - sunrise to sunset - is cut at
every edge of a tithi, nakshatra, yoga, karana or Moon rasi, and at the
edges of Rahu kalam, yamagandam and kuligai (which are dropped outright).
Every piece is judged on its own; neighbours that judge identically are
joined back together, and a piece shorter than one muhurta (48 minutes) is
not offered.

A judgement is a list of reasons, each an i18n key plus the terms and
numbers it needs, never an English sentence - the page builds the text, so
it reads the same in Tamil.
"""

from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# The rules
# ---------------------------------------------------------------------------

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]
SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# A muhurtham names the stars it may be held under; any other star is not
# "less good", it is not prescribed.
EVENTS = {
    "vivaham": {
        "nakshatras": {"Rohini", "Mrigashira", "Magha", "Uttara Phalguni", "Hasta", "Swati",
                       "Anuradha", "Mula", "Uttara Ashadha", "Uttara Bhadrapada", "Revati"},
        "good_varas": {"Monday", "Wednesday", "Thursday", "Friday"},
        "avoid_varas": {"Tuesday", "Saturday"},
        # Aadi, Purattasi and Margazhi are kept free of weddings and house
        # warmings in Tamil practice, whatever the day's limbs say.
        "avoid_months": {"Aadi", "Purattasi", "Margazhi"},
    },
    "griha_pravesham": {
        "nakshatras": {"Rohini", "Mrigashira", "Uttara Phalguni", "Chitra", "Anuradha",
                       "Uttara Ashadha", "Uttara Bhadrapada", "Revati"},
        "good_varas": {"Monday", "Wednesday", "Thursday", "Friday"},
        "avoid_varas": {"Tuesday", "Sunday"},
        "avoid_months": {"Aadi", "Purattasi", "Margazhi"},
    },
    "vahana": {
        "nakshatras": {"Ashwini", "Punarvasu", "Pushya", "Hasta", "Chitra", "Swati",
                       "Anuradha", "Shravana", "Dhanishta", "Shatabhisha", "Revati"},
        "good_varas": {"Monday", "Wednesday", "Thursday", "Friday"},
        "avoid_varas": {"Tuesday"},
        "avoid_months": set(),
    },
}

# Tithis by their 1..15 count in the paksha (15 is Purnima or Amavasya).
# Rikta - "empty" - tithis, and Ashtami, are never chosen; Tamil practice
# holds Ashtami and Navami apart more firmly than the texts do.
REJECT_TITHIS = {4: "mu.r.tithi_rikta", 9: "mu.r.tithi_rikta", 14: "mu.r.tithi_rikta",
                 8: "mu.r.tithi_ashtami"}
GOOD_TITHIS = {2, 3, 5, 7, 10, 11, 12, 13}

# Vyatipata and Vaidhriti spoil the whole of their span. The others in the
# second set are classed harsh - the texts spoil only their opening ghatis,
# which a window cannot see, so they count against a window but do not bar it.
REJECT_YOGAS = {"Vyatipata", "Vaidhriti"}
HARSH_YOGAS = {"Vishkambha", "Atiganda", "Shula", "Ganda", "Vyaghata", "Vajra", "Parigha"}

# Tara bala: the day's star counted from the janma star, in nines.
TARA_NAMES = ["Janma", "Sampat", "Vipat", "Kshema", "Pratyak",
              "Sadhana", "Naidhana", "Mitra", "Parama Mitra"]
REJECT_TARAS = {3, 5, 7}
GOOD_TARAS = {2, 4, 6, 8, 9}

# Chandra bala: the Moon's rasi counted from the natal Moon's. The 8th is
# chandrashtamam and bars the window; 4th and 12th count against it.
GOOD_CHANDRA = {1, 3, 6, 7, 10, 11}
WEAK_CHANDRA = {4, 12}

SCORE = {
    "nak_good": 4, "vara_good": 2, "tithi_good": 2, "tithi_shukla": 1,
    "tara_good": 2, "tara_parama": 1, "tara_janma": -2,
    "chandra_good": 2, "chandra_weak": -1,
    "yoga_good": 1, "yoga_harsh": -2, "krishna_late": -1,
}

MIN_WINDOW = timedelta(minutes=48)


def tara(janma_nak, day_nak):
    """1..9 - the tara of `day_nak` counted from `janma_nak` (both 0..26)."""
    return ((day_nak - janma_nak) % 27) % 9 + 1


def chandra_house(janma_rasi, moon_rasi):
    """1..12 - the Moon's rasi counted from the natal Moon's (both 0..11)."""
    return (moon_rasi - janma_rasi) % 12 + 1


# ---------------------------------------------------------------------------
# Judging one window
# ---------------------------------------------------------------------------

def _reason(key, tone, terms=None, **params):
    return {"key": key, "tone": tone, "terms": terms or {}, "params": params}


def judge(event, janma_nak, janma_rasi, vara, month, tithi, nak_index, yoga, karana, moon_rasi):
    """(blocks, reasons, score) for one stretch of time with fixed limbs.
    `tithi` is panchang.tithi_info()'s dict plus its 0..29 `index`."""
    rules = EVENTS[event]
    blocks, reasons, score = [], [], 0
    nak = NAKSHATRA_NAMES[nak_index]

    if month in rules["avoid_months"]:
        blocks.append(_reason("mu.r.month_bad", "bad", {"month": ["tamil_month", month]}))

    if vara in rules["avoid_varas"]:
        blocks.append(_reason("mu.r.vara_bad", "bad", {"vara": ["vara", vara]}))
    elif vara in rules["good_varas"]:
        score += SCORE["vara_good"]
        reasons.append(_reason("mu.r.vara_good", "good", {"vara": ["vara", vara]}))

    if nak in rules["nakshatras"]:
        score += SCORE["nak_good"]
        reasons.append(_reason("mu.r.nak_good", "good", {"nak": ["nakshatra", nak]}))
    else:
        blocks.append(_reason("mu.r.nak_not", "bad", {"nak": ["nakshatra", nak]}))

    n = tithi["number"]
    t_terms = {"tithi": ["tithi", tithi["name"]], "paksha": ["paksha", tithi["paksha"]]}
    if tithi["index"] == 29:
        blocks.append(_reason("mu.r.tithi_amavasya", "bad", t_terms))
    elif n in REJECT_TITHIS:
        blocks.append(_reason(REJECT_TITHIS[n], "bad", t_terms))
    else:
        if n in GOOD_TITHIS or tithi["index"] == 14:
            score += SCORE["tithi_good"]
            reasons.append(_reason("mu.r.tithi_good", "good", t_terms))
        if tithi["paksha"] == "Shukla":
            score += SCORE["tithi_shukla"]
            reasons.append(_reason("mu.r.shukla", "good"))
        elif n > 5:
            score += SCORE["krishna_late"]
            reasons.append(_reason("mu.r.krishna_late", "bad", t_terms))

    if yoga in REJECT_YOGAS:
        blocks.append(_reason("mu.r.yoga_bad", "bad", {"yoga": ["yoga", yoga]}))
    elif yoga in HARSH_YOGAS:
        score += SCORE["yoga_harsh"]
        reasons.append(_reason("mu.r.yoga_harsh", "bad", {"yoga": ["yoga", yoga]}))
    else:
        score += SCORE["yoga_good"]
        reasons.append(_reason("mu.r.yoga_good", "good", {"yoga": ["yoga", yoga]}))

    if karana == "Vishti":
        blocks.append(_reason("mu.r.vishti", "bad"))

    if janma_nak is not None:
        tr = tara(janma_nak, nak_index)
        tr_terms = {"tara": ["tara", TARA_NAMES[tr - 1]]}
        if tr in REJECT_TARAS:
            blocks.append(_reason("mu.r.tara_bad", "bad", tr_terms, n=tr))
        elif tr in GOOD_TARAS:
            score += SCORE["tara_good"] + (SCORE["tara_parama"] if tr == 9 else 0)
            reasons.append(_reason("mu.r.tara_good", "good", tr_terms, n=tr))
        else:
            score += SCORE["tara_janma"]
            reasons.append(_reason("mu.r.tara_janma", "bad", tr_terms, n=tr))

    if janma_rasi is not None:
        h = chandra_house(janma_rasi, moon_rasi)
        r_terms = {"rasi": ["sign", SIGNS[moon_rasi]]}
        if h == 8:
            blocks.append(_reason("mu.r.chandrashtama", "bad", r_terms))
        elif h in GOOD_CHANDRA:
            score += SCORE["chandra_good"]
            reasons.append(_reason("mu.r.chandra_good", "good", r_terms, house=h))
        elif h in WEAK_CHANDRA:
            score += SCORE["chandra_weak"]
            reasons.append(_reason("mu.r.chandra_weak", "bad", r_terms, house=h))

    return blocks, reasons, score


# ---------------------------------------------------------------------------
# Cutting a day into windows
# ---------------------------------------------------------------------------

def _at(rows, moment):
    """The row of a panchang limb list running at `moment`."""
    for r in rows:
        if r["_s"] <= moment < r["_e"]:
            return r
    return None


def _parse(rows):
    for r in rows:
        r["_s"], r["_e"] = datetime.fromisoformat(r["start"]), datetime.fromisoformat(r["end"])
    return rows


def day_windows(day, event, janma_nak, janma_rasi, tithi_info):
    """Every judged window of daylight on one panchang day, joined where
    neighbours judge alike. `tithi_info` is panchang.tithi_info."""
    rise = datetime.fromisoformat(day["sunrise"])
    sset = datetime.fromisoformat(day["sunset"])
    limbs = {k: _parse([dict(r) for r in day[k]])
             for k in ("tithi", "nakshatra", "yoga", "karana", "moon_rasi")}
    kalams = [(datetime.fromisoformat(day[k]["start"]), datetime.fromisoformat(day[k]["end"]))
              for k in ("rahu_kalam", "yamagandam", "kuligai")]

    edges = {rise, sset}
    for rows in limbs.values():
        for r in rows:
            edges.update((r["_s"], r["_e"]))
    for a, b in kalams:
        edges.update((a, b))
    edges = sorted(e for e in edges if rise <= e <= sset)

    pieces = []
    for a, b in zip(edges, edges[1:]):
        mid = a + (b - a) / 2
        if any(ka <= mid < kb for ka, kb in kalams):
            continue
        t = _at(limbs["tithi"], mid)
        nk = _at(limbs["nakshatra"], mid)
        yg = _at(limbs["yoga"], mid)
        kr = _at(limbs["karana"], mid)
        mr = _at(limbs["moon_rasi"], mid)
        if not all((t, nk, yg, kr, mr)):
            continue
        tinfo = dict(tithi_info(t["index"]), index=t["index"])
        blocks, reasons, score = judge(event, janma_nak, janma_rasi, day["vara"],
                                       day["tamil"]["month"], tinfo, nk["index"],
                                       yg["name"], kr["name"], mr["index"])
        pieces.append({
            "_s": a, "_e": b, "blocks": blocks, "reasons": reasons, "score": score,
            "limbs": {"tithi": tinfo["name"], "paksha": tinfo["paksha"],
                      "nakshatra": NAKSHATRA_NAMES[nk["index"]], "yoga": yg["name"],
                      "karana": kr["name"], "moon_rasi": SIGNS[mr["index"]]},
        })

    # Join neighbours that touch and say the same thing - a karana changing
    # from Bava to Balava should not split a good morning in two.
    def sig(p):
        return repr((p["blocks"], p["reasons"], p["score"]))
    joined = []
    for p in pieces:
        if joined and joined[-1]["_e"] == p["_s"] and sig(joined[-1]) == sig(p):
            joined[-1]["_e"] = p["_e"]
        else:
            joined.append(p)

    out = []
    for p in joined:
        p["minutes"] = round((p["_e"] - p["_s"]).total_seconds() / 60)
        p["start"], p["end"] = p.pop("_s").isoformat(), p.pop("_e").isoformat()
        out.append(p)
    return out


def judge_day(day, event, janma_nak, janma_rasi, tithi_info):
    """One day's verdict: its clear windows best first, or - when none is
    clear - what stood in the way of the window that came closest."""
    windows = day_windows(day, event, janma_nak, janma_rasi, tithi_info)
    clear = [w for w in windows if not w["blocks"] and w["minutes"] >= MIN_WINDOW.total_seconds() / 60]
    clear.sort(key=lambda w: (-w["score"], -w["minutes"], w["start"]))
    summary = {
        "date": day["date"], "vara": day["vara"], "tamil": day["tamil"],
        "sunrise": day["sunrise"], "sunset": day["sunset"],
        "rahu_kalam": day["rahu_kalam"], "yamagandam": day["yamagandam"],
        "kuligai": day["kuligai"],
    }
    if clear:
        summary.update(status="clear", score=clear[0]["score"], windows=clear)
        return summary
    blocked = [w for w in windows if w["blocks"]]
    if blocked:
        closest = min(blocked, key=lambda w: (len(w["blocks"]), -w["score"]))
        summary.update(status="blocked", score=None, blocks=closest["blocks"], windows=[])
    else:
        # Every window cleared the rules but none lasted a muhurta.
        summary.update(status="blocked", score=None,
                       blocks=[_reason("mu.r.too_short", "bad")], windows=[])
    return summary


def find(days, event, janma_nak, janma_rasi, tithi_info, top=3):
    """Judge every day; the best `top` clear days, one window each."""
    if event not in EVENTS:
        raise ValueError("mu.err_event")
    judged = [judge_day(d, event, janma_nak, janma_rasi, tithi_info) for d in days]
    clear = [d for d in judged if d["status"] == "clear"]
    clear.sort(key=lambda d: (-d["score"], -d["windows"][0]["minutes"], d["date"]))
    return {"days": judged, "top": [d["date"] for d in clear[:top]]}
