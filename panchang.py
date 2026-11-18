"""
The daily panchangam - tithi, vara, nakshatra, yoga, karana - plus the
sunrise-bound periods a Tamil calendar prints beside them: Rahu kalam,
yamagandam, kuligai and the 24 horai.

Every limb here is a slice of a steadily increasing angle:

    tithi      (Moon - Sun)  in 12 deg slices    30 a lunar month
    karana     (Moon - Sun)  in  6 deg slices    60, half a tithi each
    nakshatra   Moon         in 13 deg 20' slices 27
    yoga       (Moon + Sun)  in 13 deg 20' slices 27

None of those angles ever runs backwards - the Moon is always faster than
the Sun, and neither is ever vakri - so a limb ends exactly once, at the
moment its angle reaches the next multiple of its slice. That moment is
found by stepping forward until the angle passes it and then bisecting to
well under a second. The same search run backwards gives when a limb began.

The day itself is the Hindu day: sunrise to the next sunrise, not midnight
to midnight. The vara is the weekday of that sunrise, and everything shown
is "what was running at sunrise, and what followed before the next one" -
the way a printed panchangam reads.

Sunrise is the one place a convention has to be chosen, and printed
calendars disagree:

    "drik"   the upper limb of the Sun touching the horizon, with refraction
             - what almanac and newspaper tables give, and Drik-style
             panchangams. The default.
    "hindu"  the centre of the disc on the true horizon, no refraction -
             Swiss Ephemeris' BIT_HINDU_RISING, the traditional siddhantic
             rule. About two to three minutes later than "drik" in the
             tropics; more at higher latitudes.

The Rahu kalam, yamagandam, kuligai and horai all hang off sunrise and
sunset, so they shift with the choice too.

Concurrency: Swiss Ephemeris keeps its ephemeris path and sidereal mode as
process-wide state, and Kerykeion resets the latter when it finishes a
subject. compute() sets both itself, so the caller must hold app.SWE_LOCK
for the whole call - nothing in this module takes it, to keep it free of
any import from app.py.
"""

from datetime import date as _date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import swisseph as swe
import kerykeion

# Kerykeion's own ephemeris files, so a panchangam and a chart built on the
# same instant read the same Moon.
EPHE_PATH = str(Path(kerykeion.__file__).parent / "sweph")
FLAGS = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

RISING_FLAGS = {
    "drik": 0,
    "hindu": swe.BIT_HINDU_RISING,
}
DEFAULT_RISING = "drik"

TITHI_SPAN = 12.0
KARANA_SPAN = 6.0
NAKSHATRA_SPAN = 360.0 / 27.0
YOGA_SPAN = 360.0 / 27.0
RASI_SPAN = 30.0

# The fourteen tithis each paksha shares; the fifteenth is Purnima in the
# bright half and Amavasya in the dark one.
TITHI_NAMES = [
    "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi",
    "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dvadashi",
    "Trayodashi", "Chaturdashi",
]

YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda",
    "Sukarma", "Dhriti", "Shula", "Ganda", "Vriddhi", "Dhruva", "Vyaghata",
    "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti",
]

# Seven movable karanas cycle eight times through half-tithis 2..57; the
# first half of Shukla Pratipada and the last three halves of the month are
# the four fixed ones.
MOVABLE_KARANAS = ["Bava", "Balava", "Kaulava", "Taitila", "Gara", "Vanija", "Vishti"]

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

# The Tamil solar month is named by the rasi the Sun is in.
TAMIL_MONTHS = [
    "Chithirai", "Vaikasi", "Aani", "Aadi", "Aavani", "Purattasi",
    "Aippasi", "Karthigai", "Margazhi", "Thai", "Maasi", "Panguni",
]

# Python's weekday() is Monday = 0; the vara list and the tables below are
# Sunday = 0, as the panchangam counts.
VARAS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
VARA_LORDS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# Which eighth of the daytime (1-based, sunrise to sunset) each period holds,
# Sunday first. With a 6:00 sunrise and an 18:00 sunset these give the
# familiar fixed times - Rahu kalam 7:30-9:00 on a Monday, 16:30-18:00 on a
# Sunday - but they are computed from the real day length, as calendars do.
RAHU_KALAM_PART = [8, 2, 7, 5, 6, 4, 3]
YAMAGANDAM_PART = [5, 4, 3, 2, 1, 7, 6]
KULIGAI_PART = [7, 6, 5, 4, 3, 2, 1]

# The Chaldean order - the grahas by how slowly they move. Each horai is
# ruled by the next in this list; twenty-four steps on, the first horai of
# the following day lands on the next day's own lord, which is where the
# names of the weekdays come from.
CHALDEAN = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]

_J2000 = datetime(2000, 1, 1, 12, tzinfo=timezone.utc)
_SECOND = 1.0 / 86400.0


class PanchangError(ValueError):
    """Raised with an i18n key when a day cannot be computed - in practice,
    a place so far north or south that the Sun does not rise or set."""


# ---------------------------------------------------------------------------
# Time conversion
# ---------------------------------------------------------------------------

def _jd(dt_utc):
    return 2451545.0 + (dt_utc - _J2000).total_seconds() / 86400.0


def _dt(jd, zone):
    return (_J2000 + timedelta(days=jd - 2451545.0)).astimezone(zone)


def _iso(jd, zone):
    """Local wall time with its offset, to the second. The page rounds to the
    minute for display; the offset lets it compare against the clock."""
    if jd is None:
        return None
    return _dt(jd, zone).replace(microsecond=0).isoformat()


def _local_midnight_jd(day, zone):
    return _jd(datetime(day.year, day.month, day.day, tzinfo=zone).astimezone(timezone.utc))


# ---------------------------------------------------------------------------
# Positions and the limb angles
# ---------------------------------------------------------------------------

def _sun_moon(jd):
    sun = swe.calc_ut(jd, swe.SUN, FLAGS)[0][0]
    moon = swe.calc_ut(jd, swe.MOON, FLAGS)[0][0]
    return sun, moon


def _elongation(jd):
    sun, moon = _sun_moon(jd)
    return (moon - sun) % 360.0


def _moon(jd):
    return swe.calc_ut(jd, swe.MOON, FLAGS)[0][0]


def _sun(jd):
    return swe.calc_ut(jd, swe.SUN, FLAGS)[0][0]


def _yoga_angle(jd):
    sun, moon = _sun_moon(jd)
    return (moon + sun) % 360.0


def _signed(a):
    """An angle folded into (-180, 180]."""
    return (a + 180.0) % 360.0 - 180.0


def _crossing(angle_fn, target, jd, step, forward=True):
    """The instant `angle_fn` reaches `target`, searching from `jd` forwards
    (or backwards). The angle must be increasing and `target` within one
    slice ahead (behind), which a step well under a slice guarantees."""
    def past(t):
        d = _signed(angle_fn(t) - target)
        return d >= 0 if forward else d < 0

    a = jd
    b = jd + (step if forward else -step)
    for _ in range(400):
        if past(b):
            break
        a, b = b, b + (step if forward else -step)
    else:  # pragma: no cover - would need an angle that stopped moving
        raise PanchangError("pan.err_generic")
    # Whichever way it searched, lo is short of the target and hi is past it.
    lo, hi = (a, b) if forward else (b, a)
    while hi - lo > _SECOND / 10:
        mid = (lo + hi) / 2
        if _signed(angle_fn(mid) - target) >= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def _segments(angle_fn, span, count, day_start, day_end, step):
    """Every slice of `angle_fn` that is running at some point between
    `day_start` and `day_end`, each with its index and when it began and
    ended - the first may have begun the day before, the last may end after."""
    out = []
    idx = int(angle_fn(day_start) // span) % count
    start = _crossing(angle_fn, idx * span, day_start, step, forward=False)
    t = day_start
    for _ in range(8):
        end = _crossing(angle_fn, ((idx + 1) % count) * span, t, step)
        out.append({"index": idx, "start": start, "end": end})
        if end >= day_end:
            break
        idx, start, t = (idx + 1) % count, end, end + _SECOND
    return out


# ---------------------------------------------------------------------------
# Naming the slices
# ---------------------------------------------------------------------------

def tithi_info(index):
    """0..29 -> paksha, name and the 1..15 count within the paksha."""
    paksha = "Shukla" if index < 15 else "Krishna"
    n = index % 15
    if n == 14:
        name = "Purnima" if paksha == "Shukla" else "Amavasya"
    else:
        name = TITHI_NAMES[n]
    return {"paksha": paksha, "name": name, "number": n + 1}


def karana_name(index):
    """0..59, counted in half-tithis from the new Moon."""
    if index == 0:
        return "Kimstughna"
    if index == 57:
        return "Shakuni"
    if index == 58:
        return "Chatushpada"
    if index == 59:
        return "Naga"
    return MOVABLE_KARANAS[(index - 1) % 7]


# ---------------------------------------------------------------------------
# Sunrise, sunset and the day's frame
# ---------------------------------------------------------------------------

def _event(jd, body, rsmi, lng, lat, rising):
    """The next rise or set of `body` after `jd`, or None if it does not
    happen (a circumpolar Sun or Moon)."""
    res, tret = swe.rise_trans(jd, body, rsmi | RISING_FLAGS[rising], (lng, lat, 0.0))
    if res != 0:
        return None
    return tret[0]


def _sun_frame(day, lat, lng, zone, rising):
    """Sunrise and sunset on the local date `day`, and the sunrise after."""
    midnight = _local_midnight_jd(day, zone)
    rise = _event(midnight, swe.SUN, swe.CALC_RISE, lng, lat, rising)
    if rise is None or _dt(rise, zone).date() != day:
        raise PanchangError("pan.err_polar")
    sset = _event(rise, swe.SUN, swe.CALC_SET, lng, lat, rising)
    nxt = _event(sset, swe.SUN, swe.CALC_RISE, lng, lat, rising) if sset else None
    if sset is None or nxt is None:
        raise PanchangError("pan.err_polar")
    return rise, sset, nxt


def _within_day(jd, day, zone):
    return jd if jd is not None and _dt(jd, zone).date() == day else None


def _tamil_date(day, sunset, lat, lng, zone, rising):
    """The Tamil solar month and the day of it. A month begins on the day
    the Sun enters its rasi if that happens before sunset, otherwise on the
    day after - so the month in force on a day is the Sun's rasi at sunset."""
    sign = int(_sun(sunset) // RASI_SPAN)
    sankranti = _crossing(_sun, sign * RASI_SPAN, sunset, 1.0, forward=False)
    k_day = _dt(sankranti, zone).date()
    k_sunset = _event(_local_midnight_jd(k_day, zone), swe.SUN, swe.CALC_SET, lng, lat, rising)
    first = k_day if (k_sunset is not None and sankranti < k_sunset) else k_day + timedelta(days=1)
    return {"month": TAMIL_MONTHS[sign], "day": (day - first).days + 1,
            "sankranti": _iso(sankranti, zone)}


def vedic_today(lat, lng, tz, rising=DEFAULT_RISING, now=None):
    """The date whose Hindu day contains `now`: yesterday, until today's
    sunrise. Caller holds the ephemeris lock."""
    zone = ZoneInfo(tz)
    now = now or datetime.now(timezone.utc)
    local = now.astimezone(zone)
    swe.set_ephe_path(EPHE_PATH)
    rise = _event(_local_midnight_jd(local.date(), zone), swe.SUN, swe.CALC_RISE, lng, lat, rising)
    if rise is not None and _jd(now.astimezone(timezone.utc)) < rise:
        return local.date() - timedelta(days=1)
    return local.date()


# ---------------------------------------------------------------------------
# The whole day
# ---------------------------------------------------------------------------

def compute(day, lat, lng, tz, rising=DEFAULT_RISING):
    """The panchangam for the Hindu day that begins at sunrise on `day`
    (a datetime.date) at the given place. Times are local ISO strings with
    their UTC offset. Caller must hold the ephemeris lock."""
    if rising not in RISING_FLAGS:
        rising = DEFAULT_RISING
    zone = ZoneInfo(tz)
    swe.set_ephe_path(EPHE_PATH)
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    rise, sset, next_rise = _sun_frame(day, lat, lng, zone, rising)
    iso = lambda jd: _iso(jd, zone)

    def periods(angle_fn, span, count, step, describe):
        rows = []
        for seg in _segments(angle_fn, span, count, rise, next_rise, step):
            row = describe(seg["index"])
            row.update(index=seg["index"], start=iso(seg["start"]), end=iso(seg["end"]))
            rows.append(row)
        return rows

    tithis = periods(_elongation, TITHI_SPAN, 30, 0.25, tithi_info)
    karanas = periods(_elongation, KARANA_SPAN, 60, 0.125, lambda i: {"name": karana_name(i)})
    nakshatras = periods(_moon, NAKSHATRA_SPAN, 27, 0.25, lambda i: {})
    yogas = periods(_yoga_angle, YOGA_SPAN, 27, 0.25, lambda i: {"name": YOGA_NAMES[i]})
    moon_rasis = periods(_moon, RASI_SPAN, 12, 0.5, lambda i: {"sign": SIGNS[i]})

    # Python counts Monday = 0; the panchangam counts Sunday = 0.
    vara = (day.weekday() + 1) % 7

    # Day and night each split into eight; the three periods are daytime ones.
    part = (sset - rise) / 8.0

    def kalam(table):
        n = table[vara] - 1
        return {"start": iso(rise + n * part), "end": iso(rise + (n + 1) * part)}

    # Twelve unequal hours from sunrise to sunset, twelve more to the next
    # sunrise, starting from the vara's own lord.
    horai = []
    lord = CHALDEAN.index(VARA_LORDS[vara])
    day_h, night_h = (sset - rise) / 12.0, (next_rise - sset) / 12.0
    for i in range(24):
        a = rise + i * day_h if i < 12 else sset + (i - 12) * night_h
        b = a + (day_h if i < 12 else night_h)
        horai.append({"lord": CHALDEAN[(lord + i) % 7], "start": iso(a), "end": iso(b),
                      "night": i >= 12})

    midnight = _local_midnight_jd(day, zone)
    moonrise = _within_day(_event(midnight, swe.MOON, swe.CALC_RISE, lng, lat, rising), day, zone)
    moonset = _within_day(_event(midnight, swe.MOON, swe.CALC_SET, lng, lat, rising), day, zone)

    return {
        "date": day.isoformat(),
        "lat": lat, "lng": lng, "tz": tz, "rising": rising,
        "vara": VARAS[vara],
        "vara_lord": VARA_LORDS[vara],
        "sunrise": iso(rise), "sunset": iso(sset), "next_sunrise": iso(next_rise),
        "moonrise": iso(moonrise), "moonset": iso(moonset),
        "tithi": tithis,
        "nakshatra": nakshatras,
        "yoga": yogas,
        "karana": karanas,
        "moon_rasi": moon_rasis,
        "sun_rasi": SIGNS[int(_sun(rise) // RASI_SPAN)],
        "tamil": _tamil_date(day, sset, lat, lng, zone, rising),
        "rahu_kalam": kalam(RAHU_KALAM_PART),
        "yamagandam": kalam(YAMAGANDAM_PART),
        "kuligai": kalam(KULIGAI_PART),
        "horai": horai,
        "ayanamsa": round(swe.get_ayanamsa_ut(rise), 6),
    }
