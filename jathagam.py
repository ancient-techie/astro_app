"""
Jathaga porutham - the chart-level marriage checks that sit behind the ten.
---------------------------------------------------------------------------
The ten poruthams in porutham.py need only a birth star and a moon sign. The
checks here need the whole chart, which is why a Tamil astrologer asks for
the full jathagam before saying anything final:

  Sevvai dosham  - Mars in the houses that afflict marriage, counted from
                   the Lagna, from the Moon and from Venus, together with
                   the classical cancellations
  7th bhava      - the house of marriage itself: its sign, who occupies it,
                   who aspects it
  7th athipathi  - the lord of that house and where it has gone
  Sukran / Guru  - Venus and Jupiter, the two karakas for married life

Like porutham.py this module is pure: it takes plain sign names and gives
back plain dicts, with no Flask, no Kerykeion and no ephemeris of its own.
app.py reads the sidereal positions off the chart it has already built and
hands them over. That keeps every rule below testable on its own and legible
next to the source it came from.

Houses are whole-sign throughout, matching the rest of the app: the
Ascendant's sign is the 1st house, the next sign the 2nd, and so on.

Where traditions differ the rule applied is named in the comment above it.
Two choices worth stating up front, because they change results:

  * Aspects are the classical seven grahas' whole-sign drishti, the same
    table app.py uses elsewhere. Rahu and Ketu are counted where they sit
    but are not given aspects of their own, since texts disagree on those.
  * Benefic and malefic are taken in their simple form. The Moon's and
    Mercury's natures are really conditional, so a reading that turns on
    either is flagged rather than asserted.
"""

import porutham

# ---------------------------------------------------------------------------
# Shared tables
# ---------------------------------------------------------------------------

SIGN_ORDER = porutham.SIGN_ORDER
SIGN_LORD = porutham.SIGN_LORD

GRAHAS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
CLASSICAL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# Signs each graha rules, exalts in, and falls in.
OWN_SIGNS = {
    "Sun": ["Leo"], "Moon": ["Can"], "Mars": ["Ari", "Sco"],
    "Mercury": ["Gem", "Vir"], "Jupiter": ["Sag", "Pis"],
    "Venus": ["Tau", "Lib"], "Saturn": ["Cap", "Aqu"],
}
EXALTATION = {
    "Sun": "Ari", "Moon": "Tau", "Mars": "Cap", "Mercury": "Vir",
    "Jupiter": "Can", "Venus": "Pis", "Saturn": "Lib",
}
DEBILITATION = {
    "Sun": "Lib", "Moon": "Sco", "Mars": "Can", "Mercury": "Pis",
    "Jupiter": "Cap", "Venus": "Vir", "Saturn": "Ari",
}

# Whole-sign drishti, as house offsets counted forward from the graha's own
# house (0 would be its own house and is left out). Every graha has the 7th;
# Mars, Jupiter and Saturn add their special aspects.
ASPECT_OFFSETS = {
    "Sun": [6], "Moon": [6], "Mercury": [6], "Venus": [6],
    "Mars": [3, 6, 7],
    "Jupiter": [4, 6, 8],
    "Saturn": [2, 6, 9],
}

# Simple natures. Mercury and the Moon are conditional in practice, so
# anything resting on them is reported as "qualified" rather than settled.
MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
BENEFICS = {"Jupiter", "Venus", "Mercury", "Moon"}
CONDITIONAL_NATURE = {"Mercury", "Moon"}


def house_of(sign, reference_sign):
    """Whole-sign house number (1-12) of `sign`, counted from `reference_sign`."""
    return ((SIGN_ORDER.index(sign) - SIGN_ORDER.index(reference_sign)) % 12) + 1


def sign_at_house(reference_sign, house):
    """The sign standing in a given house from a reference sign."""
    return SIGN_ORDER[(SIGN_ORDER.index(reference_sign) + house - 1) % 12]


def dignity(graha, sign):
    """Exalted / own / debilitated / neutral, as a translation key suffix."""
    if EXALTATION.get(graha) == sign:
        return "exalted"
    if DEBILITATION.get(graha) == sign:
        return "debilitated"
    if sign in OWN_SIGNS.get(graha, ()):
        return "own"
    return "neutral"


def aspecting(positions, target_sign):
    """Which classical grahas cast a whole-sign aspect on this sign."""
    found = []
    for graha, offsets in ASPECT_OFFSETS.items():
        seat = positions.get(graha)
        if not seat:
            continue
        if any(sign_at_house(seat, offset + 1) == target_sign for offset in offsets):
            found.append(graha)
    return found


def occupants(positions, sign, skip=()):
    """Which grahas sit in this sign."""
    return [g for g in GRAHAS
            if g not in skip and positions.get(g) == sign]


# ---------------------------------------------------------------------------
# Sevvai dosham (Chevvai / Mangal dosha)
# ---------------------------------------------------------------------------
# Mars sitting in the 1st, 2nd, 4th, 7th, 8th or 12th afflicts married life.
# Tamil practice counts those houses three times over - from the Lagna, from
# the Moon and from Venus - and a hit from any of the three raises it.

DOSHA_HOUSES = (1, 2, 4, 7, 8, 12)

# The classical exemptions: Mars in these signs, in these houses, is held to
# cause no dosham at all.
DOSHA_EXEMPT_SIGNS = {
    1: {"Ari"},
    2: {"Gem", "Vir"},
    4: {"Ari", "Sco"},
    7: {"Can", "Cap"},
    8: {"Sag", "Pis"},
    12: {"Tau", "Lib"},
}


def sevvai_dosham(positions, ascendant):
    """Is Mars afflicting this chart's married life, and is it cancelled?

    Returns the houses Mars falls in from each of the three reference
    points, every cancellation that applies, and a severity of
    "none" / "cancelled" / "present".
    """
    mars = positions["Mars"]

    # Mars counted from each reference point that exists in this chart.
    seats = {}
    for name, reference in (("lagna", ascendant),
                            ("moon", positions.get("Moon")),
                            ("venus", positions.get("Venus"))):
        if reference:
            seats[name] = house_of(mars, reference)

    hits = {name: house for name, house in seats.items() if house in DOSHA_HOUSES}

    cancellations = []
    if hits:
        # 1. Mars strong in its own sign or exalted.
        mars_dignity = dignity("Mars", mars)
        if mars_dignity in ("own", "exalted"):
            cancellations.append(f"jathagam.cancel.mars_{mars_dignity}")

        # 2. The house-and-sign exemptions, applied per reference point: an
        #    exempt placement simply does not raise the dosham there.
        if all(mars in DOSHA_EXEMPT_SIGNS.get(house, set()) for house in hits.values()):
            cancellations.append("jathagam.cancel.exempt_sign")

        # 3. Jupiter with Mars, or aspecting it, restrains it.
        if positions.get("Jupiter") == mars:
            cancellations.append("jathagam.cancel.jupiter_conjunct")
        elif "Jupiter" in aspecting(positions, mars):
            cancellations.append("jathagam.cancel.jupiter_aspect")

    if not hits:
        severity = "none"
    elif cancellations:
        severity = "cancelled"
    else:
        severity = "present"

    return {
        "severity": severity,
        "mars_sign": mars,
        "mars_dignity": dignity("Mars", mars),
        "houses": seats,        # every reference point, afflicting or not
        "hits": hits,           # only the ones that land on a dosha house
        "cancellations": cancellations,
    }


# ---------------------------------------------------------------------------
# The 7th bhava and its lord
# ---------------------------------------------------------------------------


def seventh_house(positions, ascendant):
    """The house of marriage: its sign, lord, occupants and aspects."""
    sign = sign_at_house(ascendant, 7)
    lord = SIGN_LORD[sign]
    lord_sign = positions.get(lord)

    sitting = occupants(positions, sign)
    looking = aspecting(positions, sign)
    # The 7th lord aspecting its own house from elsewhere is a supporting
    # factor worth naming separately from the rest.
    influences = [g for g in sitting + looking if g != lord]

    return {
        "sign": sign,
        "lord": lord,
        "lord_sign": lord_sign,
        "lord_house": house_of(lord_sign, ascendant) if lord_sign else None,
        "lord_dignity": dignity(lord, lord_sign) if lord_sign else None,
        "occupants": sitting,
        "aspected_by": looking,
        "malefics": [g for g in influences if g in MALEFICS],
        "benefics": [g for g in influences if g in BENEFICS],
        # Named so the page can say a reading leans on a conditional nature
        # rather than quietly counting it as settled.
        "conditional": [g for g in influences if g in CONDITIONAL_NATURE],
    }


# ---------------------------------------------------------------------------
# Sukran and Guru - the two karakas for married life
# ---------------------------------------------------------------------------
# Venus signifies the spouse and marital happiness; Jupiter signifies the
# husband in a woman's chart and is the general benefic over the match.


def karaka(positions, ascendant, graha):
    sign = positions.get(graha)
    if not sign:
        return None
    with_it = occupants(positions, sign, skip=(graha,))
    looking = [g for g in aspecting(positions, sign) if g != graha]
    afflictors = [g for g in with_it + looking if g in MALEFICS]
    return {
        "graha": graha,
        "sign": sign,
        "house": house_of(sign, ascendant),
        "dignity": dignity(graha, sign),
        "with": with_it,
        "aspected_by": looking,
        "afflicted_by": afflictors,
        "afflicted": bool(afflictors),
    }


def analyse(positions, ascendant):
    """Every chart-level marriage reading for one person."""
    return {
        "ascendant": ascendant,
        "positions": dict(positions),
        "sevvai": sevvai_dosham(positions, ascendant),
        "seventh": seventh_house(positions, ascendant),
        "venus": karaka(positions, ascendant, "Venus"),
        "jupiter": karaka(positions, ascendant, "Jupiter"),
    }


# ---------------------------------------------------------------------------
# Comparing the two charts
# ---------------------------------------------------------------------------
# These sit alongside the ten poruthams rather than inside them: they are not
# scored out of 10, because tradition does not score them that way. They are
# the things an astrologer raises after the ten have been read out.

GOOD, MEDIUM, BAD = porutham.GOOD, porutham.MEDIUM, porutham.BAD


def _dosha_match(groom, bride):
    """The one rule everyone agrees on: two afflicted charts cancel out.

    A dosham the chart's own cancellations have already answered is not a
    live one, so it is not set against a clean chart - it is still named,
    because families ask about it either way.
    """
    levels = (groom["sevvai"]["severity"], bride["sevvai"]["severity"])
    live = [level == "present" for level in levels]

    if all(live):
        return GOOD, "jathagam.sevvai.both"
    if any(live):
        return BAD, "jathagam.sevvai.one_only"
    if levels == ("none", "none"):
        return GOOD, "jathagam.sevvai.neither"
    # Nothing live on either side, but at least one chart raised a dosham
    # that its own cancellations answered.
    return GOOD, "jathagam.sevvai.cancelled"


def _seventh_lord_match(groom, bride):
    groom_lord = groom["seventh"]["lord"]
    bride_lord = bride["seventh"]["lord"]
    if groom_lord == bride_lord:
        return GOOD, "jathagam.seventh.same_lord"
    forward = porutham._relation(groom_lord, bride_lord)
    backward = porutham._relation(bride_lord, groom_lord)
    if "enemy" in (forward, backward):
        return BAD, "jathagam.seventh.enemies"
    if "friend" in (forward, backward):
        return GOOD, "jathagam.seventh.friends"
    return MEDIUM, "jathagam.seventh.neutral"


def _karaka_match(groom, bride):
    """Venus in the groom's chart and Jupiter in the bride's carry the
    heavier signification for a marriage, so those two are weighed here.
    """
    afflicted = []
    if groom["venus"]["afflicted"]:
        afflicted.append("groom")
    if bride["jupiter"]["afflicted"]:
        afflicted.append("bride")
    if not afflicted:
        return GOOD, "jathagam.karaka.clear"
    if len(afflicted) == 1:
        return MEDIUM, ("jathagam.karaka.groom_afflicted" if afflicted == ["groom"]
                        else "jathagam.karaka.bride_afflicted")
    return BAD, "jathagam.karaka.both_afflicted"


def compare(groom, bride):
    """The chart-level readings for a couple, as a short list of verdicts.

    `groom` and `bride` are analyse() results. Deliberately unscored - these
    inform the ten poruthams rather than adding to them.
    """
    checks = []
    for key, fn in (("sevvai", _dosha_match),
                    ("seventh_lord", _seventh_lord_match),
                    ("karaka", _karaka_match)):
        status, reason = fn(groom, bride)
        checks.append({"key": key, "status": status, "reason": reason})
    return {
        "checks": checks,
        "groom": groom,
        "bride": bride,
        "concerns": [c["key"] for c in checks if c["status"] == BAD],
    }
