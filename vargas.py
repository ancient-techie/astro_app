"""The sixteen Shodasavarga divisional charts (D1 - D60), Parashara's rules.

Neither Kerykeion nor jyotichart knows about vargas: Kerykeion stops at the
sidereal longitude, and jyotichart draws whatever {graha: sign} it is handed.
So every divisional sign is derived here from the D1 longitude alone.

Most vargas cut a sign into n equal parts and count those parts on from a
starting sign; what differs between them is only where the count starts.
Each rule below is written the way the texts state it - by odd/even sign,
by movable/fixed/dual, by element - rather than folded into one clever
formula, so a rule can be checked line by line against BPHS. Two do not
divide evenly at all: D2 (Hora) and D30 (Trimsamsa), which have their own
tables.

Signs are indices 0..11 from Mesha (Aries). "Odd" means odd-numbered
counting Mesha as 1, i.e. an even index.
"""

# Mesha .. Meena in order; matches app.SIGN_ORDER.
SIGN_ORDER = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir",
              "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"]

ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO = range(6)
LIBRA, SCORPIO, SAGITTARIUS, CAPRICORN, AQUARIUS, PISCES = range(6, 12)


def _is_odd(sign):
    return sign % 2 == 0


def _modality(sign):
    """0 movable (chara), 1 fixed (sthira), 2 dual (dvisvabhava)."""
    return sign % 3


def _element(sign):
    """0 fire, 1 earth, 2 air, 3 water."""
    return sign % 4


# ---------------------------------------------------------------------------
# Where each equal-part varga starts counting, given the D1 sign.
# ---------------------------------------------------------------------------

def _start_self(sign):
    return sign


def _start_d7(sign):
    # Saptamsa: odd signs from themselves, even signs from their 7th.
    return sign if _is_odd(sign) else (sign + 6) % 12


def _start_d9(sign):
    # Navamsa: movable from itself, fixed from its 9th, dual from its 5th -
    # equivalently fire from Mesha, earth from Makara, air from Tula, water
    # from Kataka.
    return (sign, (sign + 8) % 12, (sign + 4) % 12)[_modality(sign)]


def _start_d10(sign):
    # Dasamsa: odd signs from themselves, even signs from their 9th.
    return sign if _is_odd(sign) else (sign + 8) % 12


def _start_d16(sign):
    # Shodasamsa: movable from Mesha, fixed from Simha, dual from Dhanus.
    return (ARIES, LEO, SAGITTARIUS)[_modality(sign)]


def _start_d20(sign):
    # Vimsamsa: movable from Mesha, fixed from Dhanus, dual from Simha.
    return (ARIES, SAGITTARIUS, LEO)[_modality(sign)]


def _start_d24(sign):
    # Chaturvimsamsa (Siddhamsa): odd signs from Simha, even from Kataka.
    return LEO if _is_odd(sign) else CANCER


def _start_d27(sign):
    # Bhamsa (Nakshatramsa): fire from Mesha, earth from Kataka, air from
    # Tula, water from Makara.
    return (ARIES, CANCER, LIBRA, CAPRICORN)[_element(sign)]


def _start_d40(sign):
    # Khavedamsa: odd signs from Mesha, even from Tula.
    return ARIES if _is_odd(sign) else LIBRA


def _start_d45(sign):
    # Akshavedamsa: movable from Mesha, fixed from Simha, dual from Dhanus.
    return (ARIES, LEO, SAGITTARIUS)[_modality(sign)]


def _start_d60(sign):
    # Shashtyamsa: from the sign itself (Parashara; some later authors
    # start from Mesha for every sign - JHora's default is this one).
    return sign


# ---------------------------------------------------------------------------
# The two that do not divide evenly.
# ---------------------------------------------------------------------------

def _hora(sign, deg):
    # Parashara's Hora: in an odd sign the first 15 degrees belong to the
    # Sun (Simha) and the second to the Moon (Kataka); in an even sign the
    # other way round. Every graha therefore lands in Simha or Kataka.
    first_half = deg < 15.0
    if _is_odd(sign):
        return LEO if first_half else CANCER
    return CANCER if first_half else LEO


# (upper bound in degrees, sign) - five unequal portions, each ruled by one
# of the five tara grahas and given that graha's sign of the matching
# parity. Even signs run the same portions in reverse.
_TRIMSAMSA_ODD = ((5.0, ARIES), (10.0, AQUARIUS), (18.0, SAGITTARIUS),
                  (25.0, GEMINI), (30.0, LIBRA))
_TRIMSAMSA_EVEN = ((5.0, TAURUS), (12.0, VIRGO), (20.0, PISCES),
                   (25.0, CAPRICORN), (30.0, SCORPIO))


def _trimsamsa(sign, deg):
    table = _TRIMSAMSA_ODD if _is_odd(sign) else _TRIMSAMSA_EVEN
    for upper, target in table:
        if deg < upper:
            return target
    return table[-1][1]


# ---------------------------------------------------------------------------
# The table.
# ---------------------------------------------------------------------------

# n -> (English/Sanskrit name, start rule, step between parts). Order is the
# Shodasavarga's own. `None` for the start rule marks an unequal varga, whose
# function takes (sign, degree) instead.
VARGAS = {
    1:  ("Rasi",            _start_self, 1),
    2:  ("Hora",            None,        None),
    # Drekkana: the sign, its 5th, its 9th - a step of 4 signs a part.
    3:  ("Drekkana",        _start_self, 4),
    # Chaturthamsa: the sign, its 4th, 7th, 10th - a step of 3.
    4:  ("Chaturthamsa",    _start_self, 3),
    7:  ("Saptamsa",        _start_d7,   1),
    9:  ("Navamsa",         _start_d9,   1),
    10: ("Dasamsa",         _start_d10,  1),
    12: ("Dwadasamsa",      _start_self, 1),
    16: ("Shodasamsa",      _start_d16,  1),
    20: ("Vimsamsa",        _start_d20,  1),
    24: ("Chaturvimsamsa",  _start_d24,  1),
    27: ("Bhamsa",          _start_d27,  1),
    30: ("Trimsamsa",       None,        None),
    40: ("Khavedamsa",      _start_d40,  1),
    45: ("Akshavedamsa",    _start_d45,  1),
    60: ("Shashtyamsa",     _start_d60,  1),
}

_UNEQUAL = {2: _hora, 30: _trimsamsa}

VARGA_NUMBERS = tuple(VARGAS)


def varga_name(n):
    return VARGAS[n][0]


def varga_index(abs_pos, n):
    """Sign index (0 = Mesha) of sidereal longitude `abs_pos` in the Dn chart."""
    if n not in VARGAS:
        raise ValueError(f"D{n} is not one of the sixteen vargas")

    abs_pos = abs_pos % 360.0
    sign = int(abs_pos // 30)
    deg = abs_pos - sign * 30

    if n in _UNEQUAL:
        return _UNEQUAL[n](sign, deg)

    _, start_rule, step = VARGAS[n]
    # min() guards a float that rounds to exactly 30.0 inside the sign.
    part = min(int(deg * n / 30.0), n - 1)
    return (start_rule(sign) + part * step) % 12


def varga_sign(abs_pos, n):
    """Sign abbreviation ('Ari' .. 'Pis') of `abs_pos` in the Dn chart."""
    return SIGN_ORDER[varga_index(abs_pos, n)]


def varga_positions(longitudes, n):
    """{label: sign abbreviation} in the Dn chart for {label: longitude}."""
    return {label: varga_sign(lon, n) for label, lon in longitudes.items()}
