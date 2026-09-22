"""
Thirumana Porutham - the ten traditional Tamil marriage-compatibility checks.
----------------------------------------------------------------------------
Tamil families run these ten "poruthams" over the bride's and groom's birth
star (nakshatra) and moon sign (rashi) before a marriage is fixed. Nothing
here needs an ephemeris: every rule is a lookup or a count over the 27-star
and 12-sign cycles, so this module is pure data + arithmetic with no Flask
and no Kerykeion import. app.py feeds it the Moon's nakshatra and sign, which
it already computes for the birth chart.

The ten, in the order they are traditionally read out:

  1. Dina          - longevity and day-to-day wellbeing of the couple
  2. Gana          - temperament (divine / human / demonic natures)
  3. Mahendra      - progeny and the family line
  4. Stree Deergha - the bride's prosperity and long married life
  5. Yoni          - physical and sexual compatibility (animal symbols)
  6. Rasi          - harmony between the two moon signs
  7. Rasi Athipathi- friendship between the lords of those moon signs
  8. Vasya         - mutual attraction and influence
  9. Rajju         - longevity of the husband; the single most weighted check
 10. Vedha         - mutually "piercing" star pairs, read as an affliction

Every check returns one of three classical verdicts - "good" (uthamam),
"medium" (madhyamam) or "bad" (adhamam). Sources differ on the finer
gradings; where they do, the rule actually applied is spelled out in the
comment above each function so it can be checked against a family's own
panchangam rather than being buried in a table.

Counting convention: a "count" from star A to star B is inclusive of both
ends (A itself is 1), going forward through the cycle and wrapping around.
Most of the ten count from the *bride's* star to the *groom's*, which is why
the argument order matters and the functions take (groom, bride) explicitly.
"""

# ---------------------------------------------------------------------------
# The cycles these rules run over
# ---------------------------------------------------------------------------
# Same 27 names and 12 sign abbreviations app.py uses - the English name is
# the lookup key everywhere in this app (i18n translates at display time).

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]

SIGN_ORDER = [
    "Ari", "Tau", "Gem", "Can", "Leo", "Vir",
    "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis",
]

# Verdicts, worst to best. Scores are the classical half-mark for a partial
# match, so ten checks add up to a 0-10 total.
GOOD, MEDIUM, BAD = "good", "medium", "bad"
VERDICT_SCORE = {GOOD: 1.0, MEDIUM: 0.5, BAD: 0.0}


# A star spans 13°20' and a sign 30°, so eighteen of the 27 sit wholly
# inside one rashi and the other nine straddle a boundary - Krittika falls in
# Aries for its first pada and Taurus for the rest, and so on. Deriving the
# map from the two spans keeps it honest; sampling each pada's midpoint names
# every sign the star touches without tripping over the boundary itself.
NAKSHATRA_SPAN = 360.0 / 27.0


def _signs_spanned(star_idx):
    start = star_idx * NAKSHATRA_SPAN
    spanned = []
    for pada in range(4):
        midpoint = start + (pada + 0.5) * (NAKSHATRA_SPAN / 4)
        sign = SIGN_ORDER[int(midpoint // 30) % 12]
        if sign not in spanned:
            spanned.append(sign)
    return spanned


# {star name: [rashi abbreviations it can fall in]} - the page uses this to
# keep the two dropdowns from offering a combination the sky cannot produce.
SIGNS_FOR_STAR = {
    name: _signs_spanned(i) for i, name in enumerate(NAKSHATRA_NAMES)
}


def is_possible_pairing(star, sign):
    """Can a birth Moon in this nakshatra actually sit in this rashi?"""
    return sign in SIGNS_FOR_STAR.get(star, ())



def star_index(name):
    return NAKSHATRA_NAMES.index(name)


def count_stars(from_star, to_star):
    """Inclusive forward count from one star to another (1-27)."""
    return ((star_index(to_star) - star_index(from_star)) % 27) + 1


def count_signs(from_sign, to_sign):
    """Inclusive forward count from one rashi to another (1-12)."""
    return ((SIGN_ORDER.index(to_sign) - SIGN_ORDER.index(from_sign)) % 12) + 1

# A pada is a quarter of a star, 3°20'. Where the star alone leaves the rashi
# ambiguous, the pada settles it outright - Krittika's first pada is in Aries
# and its other three are in Taurus - so a birth almanac quoting the pada
# pins the moon sign without needing the birth time at all.
PADA_SPAN = NAKSHATRA_SPAN / 4


def sign_for_pada(star, pada):
    """The rashi a given pada (1-4) of a nakshatra falls in."""
    if star not in SIGNS_FOR_STAR:
        raise ValueError(f"Unknown nakshatra: {star!r}")
    if pada not in (1, 2, 3, 4):
        raise ValueError(f"Pada must be 1-4, got {pada!r}")
    # Midpoint of the pada, so the arithmetic never lands exactly on a
    # boundary and tip into the neighbouring sign.
    midpoint = star_index(star) * NAKSHATRA_SPAN + (pada - 0.5) * PADA_SPAN
    return SIGN_ORDER[int(midpoint // 30) % 12]


# {star name: [rashi for pada 1, 2, 3, 4]} - handed to the page so picking a
# pada can fill the rashi in automatically.
SIGN_BY_PADA = {
    name: [sign_for_pada(name, pada) for pada in (1, 2, 3, 4)]
    for name in NAKSHATRA_NAMES
}


# ---------------------------------------------------------------------------
# 1. Dina porutham
# ---------------------------------------------------------------------------
# Count from the bride's star to the groom's and divide by 9. Remainders
# 2, 4, 6, 8 and 0 (i.e. an exact 9) are the auspicious ones; 1, 3, 5 and 7
# are rejected.

DINA_GOOD_REMAINDERS = (0, 2, 4, 6, 8)


def check_dina(groom_star, bride_star):
    count = count_stars(bride_star, groom_star)
    remainder = count % 9
    status = GOOD if remainder in DINA_GOOD_REMAINDERS else BAD
    return {
        "status": status,
        "reason": "porutham.dina.good" if status == GOOD else "porutham.dina.bad",
        "params": {"count": count, "remainder": remainder or 9},
        "chips": [
            {"label": "porutham.chip.count", "value": str(count)},
            {"label": "porutham.chip.remainder", "value": str(remainder or 9)},
        ],
    }


# ---------------------------------------------------------------------------
# 2. Gana porutham
# ---------------------------------------------------------------------------
# Each star belongs to one of three temperaments. Like pairs with like is
# best; a Rakshasa star on either side paired with a Deva star is the classic
# rejection. The table is read (groom's gana, bride's gana) - it is not
# symmetric, because a Rakshasa groom with a Manushya bride is tolerated
# while the reverse is not.

GANA_OF_STAR = {
    "Ashwini": "Deva", "Bharani": "Manushya", "Krittika": "Rakshasa",
    "Rohini": "Manushya", "Mrigashira": "Deva", "Ardra": "Manushya",
    "Punarvasu": "Deva", "Pushya": "Deva", "Ashlesha": "Rakshasa",
    "Magha": "Rakshasa", "Purva Phalguni": "Manushya", "Uttara Phalguni": "Manushya",
    "Hasta": "Deva", "Chitra": "Rakshasa", "Swati": "Deva",
    "Vishakha": "Rakshasa", "Anuradha": "Deva", "Jyeshtha": "Rakshasa",
    "Mula": "Rakshasa", "Purva Ashadha": "Manushya", "Uttara Ashadha": "Manushya",
    "Shravana": "Deva", "Dhanishta": "Rakshasa", "Shatabhisha": "Rakshasa",
    "Purva Bhadrapada": "Manushya", "Uttara Bhadrapada": "Manushya", "Revati": "Deva",
}

GANA_MATRIX = {
    ("Deva", "Deva"): GOOD,
    ("Deva", "Manushya"): MEDIUM,
    ("Deva", "Rakshasa"): BAD,
    ("Manushya", "Deva"): MEDIUM,
    ("Manushya", "Manushya"): GOOD,
    ("Manushya", "Rakshasa"): BAD,
    ("Rakshasa", "Deva"): BAD,
    ("Rakshasa", "Manushya"): MEDIUM,
    ("Rakshasa", "Rakshasa"): GOOD,
}


def check_gana(groom_star, bride_star):
    groom_gana = GANA_OF_STAR[groom_star]
    bride_gana = GANA_OF_STAR[bride_star]
    status = GANA_MATRIX[(groom_gana, bride_gana)]
    # A full match only ever comes from two stars of the same gana, so the
    # three verdicts map one-to-one onto three explanations.
    reason = {
        GOOD: "porutham.gana.same",
        MEDIUM: "porutham.gana.medium",
        BAD: "porutham.gana.bad",
    }[status]
    return {
        "status": status,
        "reason": reason,
        "params": {},
        "chips": [
            {"label": "porutham.chip.groom", "term": "gana", "value": groom_gana},
            {"label": "porutham.chip.bride", "term": "gana", "value": bride_gana},
        ],
    }


# ---------------------------------------------------------------------------
# 3. Mahendra porutham
# ---------------------------------------------------------------------------
# Count from the bride's star to the groom's; the count must land on one of
# the eight Mahendra positions. Read for children and the continuation of
# the family line.

MAHENDRA_COUNTS = (4, 7, 10, 13, 16, 19, 22, 25)


def check_mahendra(groom_star, bride_star):
    count = count_stars(bride_star, groom_star)
    status = GOOD if count in MAHENDRA_COUNTS else BAD
    return {
        "status": status,
        "reason": "porutham.mahendra.good" if status == GOOD else "porutham.mahendra.bad",
        "params": {"count": count},
        "chips": [{"label": "porutham.chip.count", "value": str(count)}],
    }


# ---------------------------------------------------------------------------
# 4. Stree Deergha porutham
# ---------------------------------------------------------------------------
# Same count, bride's star to groom's: above 13 is the full match, 7 to 13 is
# accepted as a partial one, and below 7 is rejected.


def check_stree_deergha(groom_star, bride_star):
    count = count_stars(bride_star, groom_star)
    if count > 13:
        status, reason = GOOD, "porutham.stree.good"
    elif count >= 7:
        status, reason = MEDIUM, "porutham.stree.medium"
    else:
        status, reason = BAD, "porutham.stree.bad"
    return {
        "status": status,
        "reason": reason,
        "params": {"count": count},
        "chips": [{"label": "porutham.chip.count", "value": str(count)}],
    }


# ---------------------------------------------------------------------------
# 5. Yoni porutham
# ---------------------------------------------------------------------------
# Each star carries one of 14 animal symbols with a fixed sex. Sharing the
# animal is the full match; the seven classical enemy pairs are the
# rejection; everything else is a partial match.

YONI_OF_STAR = {
    "Ashwini": ("Horse", "M"), "Bharani": ("Elephant", "M"), "Krittika": ("Sheep", "F"),
    "Rohini": ("Serpent", "M"), "Mrigashira": ("Serpent", "F"), "Ardra": ("Dog", "F"),
    "Punarvasu": ("Cat", "F"), "Pushya": ("Sheep", "M"), "Ashlesha": ("Cat", "M"),
    "Magha": ("Rat", "M"), "Purva Phalguni": ("Rat", "F"), "Uttara Phalguni": ("Cow", "M"),
    "Hasta": ("Buffalo", "F"), "Chitra": ("Tiger", "F"), "Swati": ("Buffalo", "M"),
    "Vishakha": ("Tiger", "M"), "Anuradha": ("Deer", "F"), "Jyeshtha": ("Deer", "M"),
    "Mula": ("Dog", "M"), "Purva Ashadha": ("Monkey", "M"), "Uttara Ashadha": ("Mongoose", "M"),
    "Shravana": ("Monkey", "F"), "Dhanishta": ("Lion", "F"), "Shatabhisha": ("Horse", "F"),
    "Purva Bhadrapada": ("Lion", "M"), "Uttara Bhadrapada": ("Cow", "F"), "Revati": ("Elephant", "F"),
}

# The seven mutually hostile animal pairs, covering all 14 yonis.
YONI_ENEMIES = [
    ("Horse", "Buffalo"), ("Elephant", "Lion"), ("Sheep", "Monkey"),
    ("Serpent", "Mongoose"), ("Dog", "Deer"), ("Cat", "Rat"), ("Cow", "Tiger"),
]
YONI_ENEMY_OF = {}
for _a, _b in YONI_ENEMIES:
    YONI_ENEMY_OF[_a] = _b
    YONI_ENEMY_OF[_b] = _a


def check_yoni(groom_star, bride_star):
    groom_yoni, groom_sex = YONI_OF_STAR[groom_star]
    bride_yoni, bride_sex = YONI_OF_STAR[bride_star]
    if groom_yoni == bride_yoni:
        status = GOOD
        # The same animal in its two sexes is the ideal pairing the texts
        # describe; the same animal twice over is merely a good one.
        reason = ("porutham.yoni.same_pair" if groom_sex != bride_sex
                  else "porutham.yoni.same")
    elif YONI_ENEMY_OF.get(groom_yoni) == bride_yoni:
        status, reason = BAD, "porutham.yoni.enemy"
    else:
        status, reason = MEDIUM, "porutham.yoni.neutral"
    return {
        "status": status,
        "reason": reason,
        "params": {},
        "chips": [
            {"label": "porutham.chip.groom", "term": "yoni", "value": groom_yoni},
            {"label": "porutham.chip.bride", "term": "yoni", "value": bride_yoni},
        ],
    }


# ---------------------------------------------------------------------------
# 6. Rasi porutham
# ---------------------------------------------------------------------------
# Count from the bride's moon sign to the groom's. Seven or beyond is the
# match; 2 through 6 is the rejection. The same sign on both sides passes as
# long as the stars differ - the same star in the same sign is only a partial
# match.


def check_rasi(groom_sign, bride_sign, groom_star, bride_star,
               groom_pada=None, bride_pada=None):
    """Padas only matter in the one case they can decide: the same star in
    the same sign on both sides. Sharing the pada too is read as too close a
    repetition; differing padas leave it the partial match it already was.
    Without padas the check stays where it was, at a partial match.
    """
    count = count_signs(bride_sign, groom_sign)
    if count == 1:
        if groom_star != bride_star:
            status, reason = GOOD, "porutham.rasi.same_sign"
        elif groom_pada and bride_pada and groom_pada == bride_pada:
            status, reason = BAD, "porutham.rasi.same_pada"
        elif groom_pada and bride_pada:
            status, reason = MEDIUM, "porutham.rasi.same_star_other_pada"
        else:
            status, reason = MEDIUM, "porutham.rasi.same_star"
    elif count >= 7:
        status, reason = GOOD, "porutham.rasi.good"
    else:
        status, reason = BAD, "porutham.rasi.bad"
    return {
        "status": status,
        "reason": reason,
        "params": {"count": count},
        "chips": [{"label": "porutham.chip.sign_count", "value": str(count)}],
    }


# ---------------------------------------------------------------------------
# 7. Rasi Athipathi porutham
# ---------------------------------------------------------------------------
# Compare the lords of the two moon signs using the standard natural
# friendship table. The same lord, or mutual friends, is the full match;
# mutual enmity is the rejection; a mixed reading is partial.

SIGN_LORD = {
    "Ari": "Mars", "Tau": "Venus", "Gem": "Mercury", "Can": "Moon",
    "Leo": "Sun", "Vir": "Mercury", "Lib": "Venus", "Sco": "Mars",
    "Sag": "Jupiter", "Cap": "Saturn", "Aqu": "Saturn", "Pis": "Jupiter",
}

# Natural (naisargika) relationships, read as FRIENDS[lord] / ENEMIES[lord];
# anything absent from both is neutral.
PLANET_FRIENDS = {
    "Sun": {"Moon", "Mars", "Jupiter"},
    "Moon": {"Sun", "Mercury"},
    "Mars": {"Sun", "Moon", "Jupiter"},
    "Mercury": {"Sun", "Venus"},
    "Jupiter": {"Sun", "Moon", "Mars"},
    "Venus": {"Mercury", "Saturn"},
    "Saturn": {"Mercury", "Venus"},
}
PLANET_ENEMIES = {
    "Sun": {"Venus", "Saturn"},
    "Moon": set(),
    "Mars": {"Mercury"},
    "Mercury": {"Moon"},
    "Jupiter": {"Mercury", "Venus"},
    "Venus": {"Sun", "Moon"},
    "Saturn": {"Sun", "Moon", "Mars"},
}


def _relation(a, b):
    if a == b:
        return "same"
    if b in PLANET_FRIENDS[a]:
        return "friend"
    if b in PLANET_ENEMIES[a]:
        return "enemy"
    return "neutral"


def check_rasi_athipathi(groom_sign, bride_sign):
    groom_lord = SIGN_LORD[groom_sign]
    bride_lord = SIGN_LORD[bride_sign]
    forward = _relation(groom_lord, bride_lord)
    backward = _relation(bride_lord, groom_lord)

    if forward == "same":
        status, reason = GOOD, "porutham.lord.same"
    elif "enemy" in (forward, backward):
        # One-sided enmity still counts against the match, but mutual enmity
        # is the outright rejection.
        if forward == backward == "enemy":
            status, reason = BAD, "porutham.lord.enemies"
        else:
            status, reason = BAD, "porutham.lord.one_enemy"
    elif forward == backward == "friend":
        status, reason = GOOD, "porutham.lord.friends"
    elif "friend" in (forward, backward):
        status, reason = GOOD, "porutham.lord.one_friend"
    else:
        status, reason = MEDIUM, "porutham.lord.neutral"

    return {
        "status": status,
        "reason": reason,
        "params": {},
        "chips": [
            {"label": "porutham.chip.groom_lord", "term": "planet", "value": groom_lord},
            {"label": "porutham.chip.bride_lord", "term": "planet", "value": bride_lord},
        ],
    }


# ---------------------------------------------------------------------------
# 8. Vasya porutham
# ---------------------------------------------------------------------------
# Each sign holds a natural sway over certain others. The match is present if
# either moon sign is vasya to the other (both ways is the strongest form);
# absent, the check fails.

VASYA_OF_SIGN = {
    "Ari": {"Leo", "Sco"},
    "Tau": {"Can", "Lib"},
    "Gem": {"Vir"},
    "Can": {"Sco", "Sag"},
    "Leo": {"Lib"},
    "Vir": {"Gem", "Pis"},
    "Lib": {"Cap", "Vir"},
    "Sco": {"Can"},
    "Sag": {"Pis"},
    "Cap": {"Ari", "Aqu"},
    "Aqu": {"Ari"},
    "Pis": {"Cap"},
}


def check_vasya(groom_sign, bride_sign):
    groom_draws_bride = bride_sign in VASYA_OF_SIGN[groom_sign]
    bride_draws_groom = groom_sign in VASYA_OF_SIGN[bride_sign]

    if groom_sign == bride_sign:
        status, reason = GOOD, "porutham.vasya.same"
    elif groom_draws_bride and bride_draws_groom:
        status, reason = GOOD, "porutham.vasya.mutual"
    elif groom_draws_bride:
        status, reason = GOOD, "porutham.vasya.groom"
    elif bride_draws_groom:
        status, reason = GOOD, "porutham.vasya.bride"
    else:
        status, reason = BAD, "porutham.vasya.none"

    return {"status": status, "reason": reason, "params": {}, "chips": []}


# ---------------------------------------------------------------------------
# 9. Rajju porutham
# ---------------------------------------------------------------------------
# The 27 stars map onto five parts of the body, running up from the feet to
# the head and back down, over and over. Bride and groom falling in the same
# rajju is the one rejection traditionally treated as decisive on its own -
# it is read against the husband's longevity - so it is flagged separately in
# the summary below.

RAJJU_CYCLE = ["Paadha", "Kati", "Udara", "Kanta", "Siro", "Kanta", "Udara", "Kati", "Paadha"]
# Stars 1-9 run feet -> head -> feet, and that nine-star arc repeats three
# times across the cycle, so the rajju of star n is simply position n mod 9.
RAJJU_OF_STAR = {
    name: RAJJU_CYCLE[i % 9] for i, name in enumerate(NAKSHATRA_NAMES)
}


def check_rajju(groom_star, bride_star):
    groom_rajju = RAJJU_OF_STAR[groom_star]
    bride_rajju = RAJJU_OF_STAR[bride_star]
    same = groom_rajju == bride_rajju
    return {
        "status": BAD if same else GOOD,
        "reason": "porutham.rajju.same" if same else "porutham.rajju.different",
        "params": {},
        "chips": [
            {"label": "porutham.chip.groom", "term": "rajju", "value": groom_rajju},
            {"label": "porutham.chip.bride", "term": "rajju", "value": bride_rajju},
        ],
    }


# ---------------------------------------------------------------------------
# 10. Vedha porutham
# ---------------------------------------------------------------------------
# Thirteen star pairs "pierce" each other and are avoided. Chitra is the odd
# one out - it has no vedha partner, so it always passes this check.

VEDHA_PAIRS = [
    ("Ashwini", "Jyeshtha"), ("Bharani", "Anuradha"), ("Krittika", "Vishakha"),
    ("Rohini", "Swati"), ("Mrigashira", "Dhanishta"), ("Ardra", "Shravana"),
    ("Punarvasu", "Uttara Ashadha"), ("Pushya", "Purva Ashadha"), ("Ashlesha", "Mula"),
    ("Magha", "Revati"), ("Purva Phalguni", "Uttara Bhadrapada"),
    ("Uttara Phalguni", "Purva Bhadrapada"), ("Hasta", "Shatabhisha"),
]
VEDHA_OF_STAR = {}
for _a, _b in VEDHA_PAIRS:
    VEDHA_OF_STAR[_a] = _b
    VEDHA_OF_STAR[_b] = _a


def check_vedha(groom_star, bride_star):
    pierced = VEDHA_OF_STAR.get(groom_star) == bride_star
    return {
        "status": BAD if pierced else GOOD,
        "reason": "porutham.vedha.pierced" if pierced else "porutham.vedha.clear",
        "params": {},
        "chips": [],
    }


# ---------------------------------------------------------------------------
# Putting the ten together
# ---------------------------------------------------------------------------
# Order matters only for display - it is the order a panchangam reader calls
# them out in.

PORUTHAM_ORDER = [
    "dina", "gana", "mahendra", "stree_deergha", "yoni",
    "rasi", "rasi_athipathi", "vasya", "rajju", "vedha",
]

# Rajju and Vedha are the two checks tradition treats as disqualifying on
# their own, however well the other eight score.
CRITICAL_PORUTHAMS = ("rajju", "vedha")


def match(groom_star, groom_sign, bride_star, bride_sign,
          groom_pada=None, bride_pada=None):
    """Run all ten checks for one couple.

    `*_star` are English nakshatra names as they appear in NAKSHATRA_NAMES;
    `*_sign` are three-letter rashi abbreviations from SIGN_ORDER - i.e. the
    Moon's nakshatra and sign straight out of the birth chart. `*_pada` are
    optional quarters (1-4); only Rasi porutham consults them, and only to
    separate two people born under the same star in the same sign. Returns
    the ten results in reading order plus a scored summary.
    """
    for star in (groom_star, bride_star):
        if star not in RAJJU_OF_STAR:
            raise ValueError(f"Unknown nakshatra: {star!r}")
    for sign in (groom_sign, bride_sign):
        if sign not in SIGN_LORD:
            raise ValueError(f"Unknown rashi: {sign!r}")
    for star, pada, sign in ((groom_star, groom_pada, groom_sign),
                             (bride_star, bride_pada, bride_sign)):
        if pada is not None and sign_for_pada(star, pada) != sign:
            raise ValueError(
                f"{star} pada {pada} falls in {sign_for_pada(star, pada)}, not {sign}"
            )

    raw = {
        "dina": check_dina(groom_star, bride_star),
        "gana": check_gana(groom_star, bride_star),
        "mahendra": check_mahendra(groom_star, bride_star),
        "stree_deergha": check_stree_deergha(groom_star, bride_star),
        "yoni": check_yoni(groom_star, bride_star),
        "rasi": check_rasi(groom_sign, bride_sign, groom_star, bride_star,
                           groom_pada, bride_pada),
        "rasi_athipathi": check_rasi_athipathi(groom_sign, bride_sign),
        "vasya": check_vasya(groom_sign, bride_sign),
        "rajju": check_rajju(groom_star, bride_star),
        "vedha": check_vedha(groom_star, bride_star),
    }

    results = []
    for key in PORUTHAM_ORDER:
        entry = dict(raw[key])
        entry["key"] = key
        entry["critical"] = key in CRITICAL_PORUTHAMS
        entry["score"] = VERDICT_SCORE[entry["status"]]
        results.append(entry)

    score = sum(r["score"] for r in results)
    failed_critical = [r["key"] for r in results
                       if r["critical"] and r["status"] == BAD]

    # Bands are the usual reading of a ten-check tally; a failed Rajju or
    # Vedha overrides the tally regardless of how the rest scored.
    if failed_critical:
        verdict = "blocked"
    elif score >= 7.5:
        verdict = "excellent"
    elif score >= 5.0:
        verdict = "acceptable"
    else:
        verdict = "poor"

    return {
        "results": results,
        "score": score,
        # A whole number where the halves cancel out, e.g. "7" not "7.0".
        "score_label": f"{score:g}",
        "counts": {
            GOOD: sum(1 for r in results if r["status"] == GOOD),
            MEDIUM: sum(1 for r in results if r["status"] == MEDIUM),
            BAD: sum(1 for r in results if r["status"] == BAD),
        },
        "verdict": verdict,
        "failed_critical": failed_critical,
        "total": len(results),
    }
