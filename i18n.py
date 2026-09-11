"""
Tamil / English translations for the whole app.
-----------------------------------------------
Two kinds of strings live here:

  TERMS - astrological vocabulary that also appears inside *data*: planet
          names, their chart abbreviations, rashi names, the 27 nakshatras,
          dasha level names, conjunction tiers. Looked up by the English
          key the rest of the app already uses, so no calculation code has
          to change - `SIGN_NAME_MAP["Sag"]` still yields "Saggitarius" and
          the translation happens at display time.

  UI    - every fixed label, hint, button and heading on the pages.

Both dictionaries are shipped to the browser as-is by the /i18n.js route in
app.py, so the Jinja templates, the inline page scripts and
chart_playground.html all translate against exactly the same data. Nothing
here imports Flask - it's a plain data module.

Keys are English; every language sub-dict must use the same key set. A
missing key falls back to the English string (and then to the key itself),
so a half-finished translation degrades instead of breaking.
"""

LANGUAGES = ("en", "ta")
DEFAULT_LANGUAGE = "en"

# Human-readable name of each language, in that language - used for the
# toggle buttons themselves, which are never translated.
LANGUAGE_NAMES = {"en": "English", "ta": "தமிழ்"}


# ---------------------------------------------------------------------------
# TERMS - vocabulary that shows up inside generated data
# ---------------------------------------------------------------------------
# Layout is TERMS[kind][lang][english_key] -> translated string, which makes
# the browser-side lookup a plain three-level index (see I18N.term()).

TERMS = {
    # Full graha names, as used in tables, dasha rows and the analysis text.
    "planet": {
        "en": {
            "Sun": "Sun", "Moon": "Moon", "Mars": "Mars", "Mercury": "Mercury",
            "Jupiter": "Jupiter", "Venus": "Venus", "Saturn": "Saturn",
            "Rahu": "Rahu", "Ketu": "Ketu",
            "Ascendant": "Ascendant",
            "Ascendant (Lagna)": "Ascendant (Lagna)",
            "Asc": "Asc",
        },
        "ta": {
            "Sun": "சூரியன்",
            "Moon": "சந்திரன்",
            "Mars": "செவ்வாய்",
            "Mercury": "புதன்",
            "Jupiter": "குரு",
            "Venus": "சுக்கிரன்",
            "Saturn": "சனி",
            "Rahu": "ராகு",
            "Ketu": "கேது",
            "Ascendant": "லக்னம்",
            "Ascendant (Lagna)": "லக்னம்",
            "Asc": "லக்",
        },
    },

    # Short codes drawn inside the chart boxes. Kept to at most two Tamil
    # glyph clusters so they still fit the fixed jyotichart coordinates -
    # these are the standard panchangam abbreviations and stay mutually
    # distinct (சூ / சந் / செ / சுக் / சனி all read differently at a glance).
    "planet_abbr": {
        "en": {
            "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
            "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa",
            "Rahu": "Ra", "Ketu": "Ke", "Ascendant": "Asc",
        },
        "ta": {
            "Sun": "சூ",
            "Moon": "சந்",
            "Mars": "செ",
            "Mercury": "பு",
            "Jupiter": "கு",
            "Venus": "சுக்",
            "Saturn": "சனி",
            "Rahu": "ரா",
            "Ketu": "கே",
            "Ascendant": "லக்",
        },
    },

    # Rashi names. Keyed by the spellings already baked into the app -
    # including SIGN_NAME_MAP's "Saggitarius" typo - plus the correct
    # "Sagittarius" the playground page uses, so both resolve.
    "sign": {
        "en": {
            "Aries": "Aries", "Taurus": "Taurus", "Gemini": "Gemini",
            "Cancer": "Cancer", "Leo": "Leo", "Virgo": "Virgo",
            "Libra": "Libra", "Scorpio": "Scorpio",
            "Saggitarius": "Saggitarius", "Sagittarius": "Sagittarius",
            "Capricorn": "Capricorn", "Aquarius": "Aquarius", "Pisces": "Pisces",
        },
        "ta": {
            "Aries": "மேஷம்",
            "Taurus": "ரிஷபம்",
            "Gemini": "மிதுனம்",
            "Cancer": "கடகம்",
            "Leo": "சிம்மம்",
            "Virgo": "கன்னி",
            "Libra": "துலாம்",
            "Scorpio": "விருச்சிகம்",
            "Saggitarius": "தனுசு",
            "Sagittarius": "தனுசு",
            "Capricorn": "மகரம்",
            "Aquarius": "கும்பம்",
            "Pisces": "மீனம்",
        },
    },

    # The 27 nakshatras, in the traditional Tamil star names.
    "nakshatra": {
        "en": {name: name for name in [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
            "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
            "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
            "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
            "Uttara Bhadrapada", "Revati",
        ]},
        "ta": {
            "Ashwini": "அசுவினி",
            "Bharani": "பரணி",
            "Krittika": "கார்த்திகை",
            "Rohini": "ரோகிணி",
            "Mrigashira": "மிருகசீரிடம்",
            "Ardra": "திருவாதிரை",
            "Punarvasu": "புனர்பூசம்",
            "Pushya": "பூசம்",
            "Ashlesha": "ஆயில்யம்",
            "Magha": "மகம்",
            "Purva Phalguni": "பூரம்",
            "Uttara Phalguni": "உத்திரம்",
            "Hasta": "அஸ்தம்",
            "Chitra": "சித்திரை",
            "Swati": "சுவாதி",
            "Vishakha": "விசாகம்",
            "Anuradha": "அனுஷம்",
            "Jyeshtha": "கேட்டை",
            "Mula": "மூலம்",
            "Purva Ashadha": "பூராடம்",
            "Uttara Ashadha": "உத்திராடம்",
            "Shravana": "திருவோணம்",
            "Dhanishta": "அவிட்டம்",
            "Shatabhisha": "சதயம்",
            "Purva Bhadrapada": "பூரட்டாதி",
            "Uttara Bhadrapada": "உத்திரட்டாதி",
            "Revati": "ரேவதி",
        },
    },

    # Vimshottari sub-period names. Tamil astrology uses its own ladder:
    # தசை (dasha) -> புக்தி (bhukti) -> அந்தரம் -> சூட்சுமம்.
    "dasha_level": {
        "en": {
            "Mahadasha": "Mahadasha", "Antardasha": "Antardasha",
            "Pratyantardasha": "Pratyantardasha", "Sookshma Dasha": "Sookshma Dasha",
        },
        "ta": {
            "Mahadasha": "மகா தசை",
            "Antardasha": "புக்தி",
            "Pratyantardasha": "அந்தரம்",
            "Sookshma Dasha": "சூட்சுமம்",
        },
    },

    # How tight a conjunction is (see CONJUNCTION_ORB_TIERS in app.py).
    "conj_tier": {
        "en": {"Exact": "Exact", "Tight": "Tight", "Close": "Close", "Wide": "Wide"},
        "ta": {
            "Exact": "சரியான",
            "Tight": "நெருக்கமான",
            "Close": "அருகில்",
            "Wide": "விரிவான",
        },
    },

    # Row labels in the PDF's Dasha-Bhukti window (build_dasha_bhukti_window).
    "period_role": {
        "en": {
            "Previous": "Previous", "Current": "Current",
            "Upcoming": "Upcoming", "Then": "Then",
        },
        "ta": {
            "Previous": "\u0bae\u0bc1\u0ba9\u0bcd\u0ba9\u0bc8\u0baf\u0ba4\u0bc1",
            "Current": "\u0ba4\u0bb1\u0bcd\u0baa\u0bcb\u0ba4\u0bc1",
            "Upcoming": "\u0b85\u0b9f\u0bc1\u0ba4\u0bcd\u0ba4\u0ba4\u0bc1",
            "Then": "\u0baa\u0bbf\u0ba9\u0bcd\u0ba9\u0bb0\u0bcd",
        },
    },

    # Playground vocabulary: sign element / modality / direction, planet
    # dignity, and the colour names used by the Sign Colours dashboard.
    "element": {
        "en": {"fire": "Fire", "earth": "Earth", "air": "Air", "water": "Water"},
        "ta": {
            "fire": "நெருப்பு",
            "earth": "பூமி",
            "air": "காற்று",
            "water": "நீர்",
        },
    },
    "modality": {
        "en": {"movable": "Movable", "fixed": "Fixed", "mutable": "Mutable"},
        "ta": {
            "movable": "சரம்",
            "fixed": "ஸ்திரம்",
            "mutable": "உபயம்",
        },
    },
    "direction": {
        "en": {"east": "East", "south": "South", "west": "West", "north": "North"},
        "ta": {
            "east": "கிழக்கு",
            "south": "தெற்கு",
            "west": "மேற்கு",
            "north": "வடக்கு",
        },
    },
    # The playground page addresses planets by short code ('Mon', 'Mar',
    # 'Jup'...) rather than by full name, so it needs its own key set - one
    # for the full name shown in prose, one for the token drawn on the chart.
    "pg_planet": {
        "en": {
            "Sun": "Sun", "Mon": "Moon", "Mar": "Mars", "Mer": "Mercury",
            "Jup": "Jupiter", "Ven": "Venus", "Sat": "Saturn",
            "Rahu": "Rahu", "Ketu": "Ketu", "Asc": "Ascendant",
        },
        "ta": {
            "Sun": "\u0b9a\u0bc2\u0bb0\u0bbf\u0baf\u0ba9\u0bcd",
            "Mon": "\u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0ba9\u0bcd",
            "Mar": "\u0b9a\u0bc6\u0bb5\u0bcd\u0bb5\u0bbe\u0baf\u0bcd",
            "Mer": "\u0baa\u0bc1\u0ba4\u0ba9\u0bcd",
            "Jup": "\u0b95\u0bc1\u0bb0\u0bc1",
            "Ven": "\u0b9a\u0bc1\u0b95\u0bcd\u0b95\u0bbf\u0bb0\u0ba9\u0bcd",
            "Sat": "\u0b9a\u0ba9\u0bbf",
            "Rahu": "\u0bb0\u0bbe\u0b95\u0bc1",
            "Ketu": "\u0b95\u0bc7\u0ba4\u0bc1",
            "Asc": "\u0bb2\u0b95\u0bcd\u0ba9\u0bae\u0bcd",
        },
    },
    "pg_planet_abbr": {
        "en": {
            "Sun": "Sun", "Mon": "Mon", "Mar": "Mar", "Mer": "Mer",
            "Jup": "Jup", "Ven": "Ven", "Sat": "Sat",
            "Rahu": "Rahu", "Ketu": "Ketu", "Asc": "Asc",
        },
        "ta": {
            "Sun": "\u0b9a\u0bc2",
            "Mon": "\u0b9a\u0ba8\u0bcd",
            "Mar": "\u0b9a\u0bc6",
            "Mer": "\u0baa\u0bc1",
            "Jup": "\u0b95\u0bc1",
            "Ven": "\u0b9a\u0bc1\u0b95\u0bcd",
            "Sat": "\u0b9a\u0ba9\u0bbf",
            "Rahu": "\u0bb0\u0bbe",
            "Ketu": "\u0b95\u0bc7",
            "Asc": "\u0bb2\u0b95\u0bcd",
        },
    },

    # Stana Bala dignity labels, exactly as getStanaBala() emits them.
    "stana_label": {
        "en": {
            "Exaltation": "Exaltation", "Debilitation": "Debilitation",
            "Moola Trikona": "Moola Trikona", "Own Sign": "Own Sign",
            "Neutral": "Neutral", "Neutral (Jup/Sat)": "Neutral (Jup/Sat)",
            "Friend's House": "Friend's House", "Enemy House": "Enemy House",
            "Debilitation (Neecha Bhanga)": "Debilitation (Neecha Bhanga)",
        },
        "ta": {
            "Exaltation": "\u0b89\u0b9a\u0bcd\u0b9a\u0bae\u0bcd",
            "Debilitation": "\u0ba8\u0bc0\u0b9a\u0bae\u0bcd",
            "Moola Trikona": "\u0bae\u0bc2\u0bb2\u0ba4\u0bcd\u0ba4\u0bbf\u0bb0\u0bbf\u0b95\u0bcb\u0ba3\u0bae\u0bcd",
            "Own Sign": "\u0b86\u0b9f\u0bcd\u0b9a\u0bbf",
            "Neutral": "\u0b9a\u0bae\u0bae\u0bcd",
            "Neutral (Jup/Sat)": "\u0b9a\u0bae\u0bae\u0bcd (\u0b95\u0bc1\u0bb0\u0bc1/\u0b9a\u0ba9\u0bbf)",
            "Friend's House": "\u0ba8\u0b9f\u0bcd\u0baa\u0bc1 \u0bb5\u0bc0\u0b9f\u0bc1",
            "Enemy House": "\u0baa\u0b95\u0bc8 \u0bb5\u0bc0\u0b9f\u0bc1",
            "Debilitation (Neecha Bhanga)": "\u0ba8\u0bc0\u0b9a\u0bae\u0bcd (\u0ba8\u0bc0\u0b9a\u0baa\u0b99\u0bcd\u0b95\u0bae\u0bcd)",
        },
    },

    # Per-planet colour names shown on the Sign Colours dashboard.
    "planet_colour": {
        "en": {
            "Sun": "Orangish Gold", "Mon": "Silver-White (phase-dependent)",
            "Mar": "Vivid Red", "Jup": "Bright Gold", "Sat": "Royal Blue",
            "Ven": "Pinkish White", "Rahu": "Deep Black",
            "Ketu": "Reddish Brown-Black", "Mer": "Neon Green",
        },
        "ta": {
            "Sun": "\u0b86\u0bb0\u0b9e\u0bcd\u0b9a\u0bc1 \u0ba4\u0b99\u0bcd\u0b95\u0bae\u0bcd",
            "Mon": "\u0bb5\u0bc6\u0bb3\u0bcd\u0bb3\u0bbf \u0bb5\u0bc6\u0ba3\u0bcd\u0bae\u0bc8 (\u0b95\u0bb2\u0bc8\u0b95\u0bcd\u0b95\u0bc7\u0bb1\u0bcd\u0baa)",
            "Mar": "\u0b95\u0b9f\u0bc1\u0bae\u0bcd \u0b9a\u0bbf\u0bb5\u0baa\u0bcd\u0baa\u0bc1",
            "Jup": "\u0baa\u0bbf\u0bb0\u0b95\u0bbe\u0b9a \u0ba4\u0b99\u0bcd\u0b95\u0bae\u0bcd",
            "Sat": "\u0b85\u0b9f\u0bb0\u0bcd \u0ba8\u0bc0\u0bb2\u0bae\u0bcd",
            "Ven": "\u0b87\u0bb3\u0b9e\u0bcd\u0b9a\u0bbf\u0bb5\u0baa\u0bcd\u0baa\u0bc1 \u0bb5\u0bc6\u0ba3\u0bcd\u0bae\u0bc8",
            "Rahu": "\u0b95\u0bb0\u0bc1\u0bae\u0bcd \u0b95\u0bb0\u0bc1\u0baa\u0bcd\u0baa\u0bc1",
            "Ketu": "\u0b9a\u0bc6\u0bae\u0bcd\u0baa\u0bb4\u0bc1\u0baa\u0bcd\u0baa\u0bc1 \u0b95\u0bb0\u0bc1\u0baa\u0bcd\u0baa\u0bc1",
            "Mer": "\u0baa\u0bb3\u0bbf\u0b9a\u0bcd \u0baa\u0b9a\u0bcd\u0b9a\u0bc8",
        },
    },

    # Dig Bala hint shown beside each planet on that dashboard.
    "dig_info": {
        "en": {
            "Mon": "Best at 4th (Kendra)", "Ven": "Best at 4th (Kendra)",
            "Jup": "Best at 1st (Lagna)", "Mer": "Best at 1st (Lagna)",
            "Sat": "Best at 7th", "Mar": "Best at 10th (MC)",
            "Sun": "Best at 10th (MC)",
            "Rahu": "No Dig Bala", "Ketu": "No Dig Bala",
        },
        "ta": {
            "Mon": "\u0b9a\u0bbf\u0bb1\u0ba8\u0bcd\u0ba4\u0ba4\u0bc1 4\u0b86\u0bae\u0bcd (\u0b95\u0bc7\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0bae\u0bcd)",
            "Ven": "\u0b9a\u0bbf\u0bb1\u0ba8\u0bcd\u0ba4\u0ba4\u0bc1 4\u0b86\u0bae\u0bcd (\u0b95\u0bc7\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0bae\u0bcd)",
            "Jup": "\u0b9a\u0bbf\u0bb1\u0ba8\u0bcd\u0ba4\u0ba4\u0bc1 1\u0b86\u0bae\u0bcd (\u0bb2\u0b95\u0bcd\u0ba9\u0bae\u0bcd)",
            "Mer": "\u0b9a\u0bbf\u0bb1\u0ba8\u0bcd\u0ba4\u0ba4\u0bc1 1\u0b86\u0bae\u0bcd (\u0bb2\u0b95\u0bcd\u0ba9\u0bae\u0bcd)",
            "Sat": "\u0b9a\u0bbf\u0bb1\u0ba8\u0bcd\u0ba4\u0ba4\u0bc1 7\u0b86\u0bae\u0bcd",
            "Mar": "\u0b9a\u0bbf\u0bb1\u0ba8\u0bcd\u0ba4\u0ba4\u0bc1 10\u0b86\u0bae\u0bcd",
            "Sun": "\u0b9a\u0bbf\u0bb1\u0ba8\u0bcd\u0ba4\u0ba4\u0bc1 10\u0b86\u0bae\u0bcd",
            "Rahu": "\u0ba4\u0bbf\u0b95\u0bcd \u0baa\u0bb2\u0bae\u0bcd \u0b87\u0bb2\u0bcd\u0bb2\u0bc8",
            "Ketu": "\u0ba4\u0bbf\u0b95\u0bcd \u0baa\u0bb2\u0bae\u0bcd \u0b87\u0bb2\u0bcd\u0bb2\u0bc8",
        },
    },
}


# ---------------------------------------------------------------------------
# UI - fixed page text
# ---------------------------------------------------------------------------
# Placeholders are written as {name} and filled in by I18N.t(key, params)
# in the browser (or str.format on the server).

_EN = {
    # -- shell / navigation --------------------------------------------------
    "app.title": "Vedic Birth Chart",
    "app.subtitle": "Sidereal · Lahiri ayanamsa",
    "app.page_title": "Vedic Birth Chart Generator",
    "nav.admin": "Admin",
    "nav.install": "Install",
    "lang.label": "Language",

    # -- birth-details form --------------------------------------------------
    "form.name": "Name",
    "form.city": "Birth city",
    "form.city_placeholder": "e.g. Mumbai, India",
    "form.confirm_place": "Confirm place",
    "form.dob": "Date of birth",
    "form.now": "Now",
    "form.tob": "Time of birth",
    "form.lat": "Latitude",
    "form.lng": "Longitude",
    "form.latlng_hint": "Filled in automatically by “Confirm place”, or type them in yourself.",
    "form.tz": "Timezone (IANA name)",
    "form.tz_hint": "e.g. Asia/Kolkata, America/New_York, Europe/London",
    "form.style": "Chart style",
    "form.style_south": "South Indian",
    "form.style_north": "North Indian",
    "form.style_both": "Both",
    "form.submit": "Generate Chart",
    "form.save": "Save details",

    # -- inline status messages ---------------------------------------------
    "geo.idle": "Type a city and hit “Confirm place” to fill in the coordinates.",
    "geo.need_city": "Enter a birth city first.",
    "geo.looking": "Looking up {place}…",
    "geo.failed": "Lookup failed.",
    "geo.offline": "Lookup failed – check your connection.",
    "save.idle": "Saves this person's details so they show up in the admin panel – doesn't generate a chart.",
    "save.need_name": "Enter a name first.",
    "save.saving": "Saving…",
    "save.ok": "Saved – visible in the admin panel now.",
    "save.failed": "Could not save.",
    "save.offline": "Could not save – check your connection.",

    # -- results header ------------------------------------------------------
    "results.error": "Error:",
    "results.placeholder": "Fill in the birth details and tap “Generate Chart” to see the natal chart here.",
    "meta.rashi_asc": "Rashi Asc:",
    "meta.navamsa_asc": "Navamsa Asc:",
    "meta.playground": "Play with Chart",
    "meta.download_pdf": "Download PDF",
    "meta.download_pdf": "Download PDF",

    # -- chart cards ---------------------------------------------------------
    "chart.south_d1": "South Indian Chart (Rashi / D1)",
    "chart.north_d1": "North Indian Chart (Rashi / D1)",
    "chart.south_d9": "South Indian Navamsa Chart (D9)",
    "chart.north_d9": "North Indian Navamsa Chart (D9)",
    "chart.retro_hint": "Retrograde planets are marked “(R)” on the Rashi (D1) charts. Navamsa (D9) doesn't conventionally mark retrograde.",
    # Used for the labels jyotichart draws in the centre of a South Indian
    # chart, which _localize_chart_svg swaps on the finished markup.
    "chart.word": "Chart",
    "chart.rashi": "Rashi",
    "chart.navamsa": "Navamsa",

    # -- nakshatra table -----------------------------------------------------
    "section.star": "Planetary & Star (Nakshatra) Details",
    "star.hint": "Combust planets (too close to the Sun) are marked with \U0001F525 next to their name.",
    "th.planet": "Planet",
    "th.sign": "Sign",
    "th.degree": "Degree",
    "th.nakshatra": "Nakshatra",
    "th.pada": "Pada",
    "th.nak_lord": "Nakshatra Lord",

    # -- dasha table ---------------------------------------------------------
    "section.dasha": "Vimshottari Mahadasha",
    "dasha.hint": "Tap any row to expand its sub-periods (Antardasha → Pratyantardasha → Sookshma Dasha). Tap again to collapse.",
    "dasha.footnote": "Computed with the standard Vimshottari algorithm (120-year cycle, 9 planetary lords) based on the Moon's Nakshatra at birth. Not provided by Kerykeion or jyotichart directly – neither library computes Nakshatra or Dasha.",
    "th.lord": "Lord",
    "th.start": "Start",
    "th.end": "End",
    "th.years": "Yrs",

    # -- houses involved -----------------------------------------------------
    "section.houses": "Houses Involved",
    "houses.hint": "Tap a Mahadasha row to see the houses its lord activates (placement, aspects, and lordship – or for Rahu/Ketu, the houses ruled by every planet connected to it), along with that period's date range. Tap an Antardasha row to see both the Mahadasha and Antardasha lords together, or a Pratyantardasha row to add its lord as well – each with its own sub-period dates.",
    "houses.placeholder": "Tap a Mahadasha, Antardasha or Pratyantardasha row above.",
    "houses.no_data": "No house data available.",
    "phrase.lord_of": "Lord of",
    "phrase.placement": "Placement",
    "phrase.aspects": "Aspects",
    "phrase.dispositor": "Dispositor",
    "phrase.of": "of",
    "phrase.dispositor_none": "Dispositor – none",
    "phrase.conjunct": "Conjunct",
    "phrase.aspected_by": "Aspected by",
    "phrase.none": "none",
    "phrase.house": "House",
    "phrase.houses": "Houses",

    # -- conjunctions --------------------------------------------------------
    "section.conj_degree": "Conjunctions – By Degree (Orb)",
    "conj_degree.hint": "Grahas (and the Ascendant) within 10° of each other, worked out from actual longitude – not just a shared sign. Two bodies a couple of degrees apart but straddling a sign boundary still count; two bodies in the same sign but many degrees apart do not. See “By Sign” below for the traditional whole-sign view.",
    "conj_degree.none": "No conjunctions within 10° in this chart.",
    "section.conj_sign": "Conjunctions – By Sign (Rashi)",
    "conj_sign.hint": "The traditional whole-sign yuti: every pair of grahas (and the Ascendant) sharing a sign, however many degrees apart within it – with that gap shown alongside, so a tight 2° pairing and a loose 25° one in the same sign aren't lumped together as equivalent.",
    "conj_sign.none": "No two bodies share a sign in this chart.",
    "conj.signs_label": "Sign(s)",
    "conj.apart": "apart",

    # -- admin ---------------------------------------------------------------
    "admin.login_page_title": "Admin sign in – Vedic Birth Chart",
    "admin.login_title": "Admin sign in",
    "admin.password": "Password",
    "admin.sign_in": "Sign in",
    "admin.wrong_password": "Wrong password.",
    "admin.page_title": "Admin – Stored Birth Details",
    "admin.stored": "Stored birth details",
    "admin.new_chart": "New chart",
    "admin.log_out": "Log out",
    "admin.unknown_city": "Unknown city",
    "admin.dob": "Date of birth",
    "admin.tob": "Time of birth",
    "admin.latlng": "Lat, Lng",
    "admin.timezone": "Timezone",
    "admin.saved_at": "Saved",
    "admin.go_to_chart": "Go to chart",
    "admin.empty": "No records saved yet – generate a chart on the main page to see it here.",

    # -- PDF export ----------------------------------------------------------
    "pdf.subtitle": "Vedic (Jyotish) Birth Chart \u00b7 Sidereal \u00b7 Lahiri ayanamsa",
    "pdf.birth_details": "Birth Details",
    "pdf.charts_heading": "Rashi (D1) & Navamsa (D9) Charts",
    "pdf.bhukti_heading": "Vimshottari Dasha-Bhukti",
    # One period, spelled out over two lines - see chart_pdf._bhukti_lines.
    "pdf.bhukti_line": "{role} · {maha} {maha_label} – {antar} {antar_label}",
    "pdf.bhukti_dates": "{start} → {end} · {years} {years_unit}",
    "pdf.years_unit": "years",
    "pdf.bhukti_note": "The period marked in gold is the Mahadasha-Antardasha running on {date}, listed with the preceding period and the next two.",
    # The next level down: the current Bhukti split into its nine Antarams.
    "pdf.antaram_heading": "{level} periods within {maha} {maha_label} – {antar} {antar_label}",
    "pdf.antaram_note": "The row in gold is the {level} running on {date}.",
    "pdf.houses_note": "Houses are counted from the Rashi Ascendant. A graha activates the house it sits in, the houses it aspects and the houses it rules; Rahu and Ketu have no aspects or signs of their own, so they work through the planets connected to them.",
    "pdf.generated": "Generated {timestamp} \u00b7 positions from the Swiss Ephemeris via Kerykeion.",
    "pdf.coordinates": "Coordinates",
    "pdf.ayanamsa": "Ayanamsa",
    "pdf.ayanamsa_value": "Lahiri (sidereal)",
    "pdf.rashi_asc": "Rashi Ascendant",
    "pdf.navamsa_asc": "Navamsa Ascendant",
    "pdf.combust": "combust",
    "pdf.page": "Page",

    # -- playground: chrome --------------------------------------------------
    "pg.page_title": "Play with Chart – Vedic Birth Chart",
    "pg.back": "Back to Generator",
    "pg.title": "South Indian Birth Chart",
    "pg.clear": "Clear Chart",
    "pg.ray_opacity": "Aspect Ray Opacity",
    "pg.grahas": "Grahas",
    "pg.col_planet": "Planet",
    "pg.col_arrow_title": "Show aspect arrows",
    "pg.col_color_title": "Show sign colors",
    "pg.all": "All",
    "pg.legend": "Drag planets into chart, or tap one then tap a house.<br>Tap a placed planet to remove it.<br><br><span style=\"color:#d4af37\">{asc}</span> = house 1.",

    # -- playground: compare mode -------------------------------------------
    "pg.compare": "Compare Charts",
    "pg.compare_exit": "Single Chart",
    "pg.compare_hint": "Two independent charts - drag, drop and score each one on its own.",
    "pg.chart_a": "Chart A",
    "pg.chart_b": "Chart B",
    "pg.copy_a_b": "Copy A \u2192 B",
    "pg.copy_b_a": "Copy B \u2192 A",
    "pg.swap_ab": "Swap A \u21c4 B",
    "pg.sync_tabs": "Sync tabs",
    "pg.sync_tabs_title": "Keep both charts on the same dashboard tab",

    # -- playground: dashboards ---------------------------------------------
    "pg.tab_good": "Goodness",
    "pg.tab_bad": "Badness",
    "pg.tab_well": "Wellness",
    "pg.tab_plan": "Subathuva",
    "pg.tab_stana": "Stana Bala",
    "pg.tab_dig": "Dig+Nish Bala",
    "pg.tab_total": "Total Strength",
    "pg.tab_sigcol": "Sign Colors",
    "pg.panel_good": "Goodness Dashboard",
    "pg.panel_bad": "Badness Dashboard",
    "pg.panel_well": "Wellness Dashboard",
    "pg.panel_plan": "Subathuva — Planet Wellness",
    "pg.panel_stana": "Stana Bala (Positional Strength)",
    "pg.panel_dig": "Dig Bala + Nish Bala",
    "pg.panel_total": "Total Planet Strength",
    "pg.panel_sigcol": "Sign Color Breakdown",
    "pg.no_data": "Place planets to see analysis.",
    "pg.no_data_colors": "Place planets to see sign colors.",

    # -- playground: table + section labels ---------------------------------
    "pg.rank": "#",
    "pg.sign": "Sign",
    "pg.house": "House",
    "pg.score": "Score",
    "pg.strength": "Strength",
    "pg.total": "Total",
    "pg.planet": "Planet",
    "pg.placed_in": "Placed in",
    "pg.status": "Status",
    "pg.sources": "Sources",
    "pg.good": "Good",
    "pg.bad": "Bad",
    "pg.net": "Net",
    "pg.by_element": "By Element",
    "pg.by_modality": "By Modality",
    "pg.by_direction": "By Direction",
    "pg.all_signs": "All Signs",
    "pg.strongest": "Strongest",
    "pg.weakest": "Weakest",
    "pg.stana_bala": "Stana Bala",
    "pg.dig_bala": "Dig Bala",
    "pg.nish_bala": "Nish Bala",
    "pg.not_placed": "Not placed",
    "pg.no_dig_bala": "No Dig Bala",
    "pg.best_at": "Best at {house}",
    "pg.house_from_sun": "House {n} from Sun (clockwise)",
    "pg.new_moon": "New Moon — No Light",
    "pg.nth_from_sun": "{n} from Sun",
    "pg.color": "Color",
    "pg.layers": "Layers",
    "pg.base": "Base",
    "pg.h": "H",
    "pg.no_data_simple": "No data.",
    "pg.none_simple": "None.",
    "pg.signs_goodness": "Signs Goodness",
    "pg.signs_badness": "Signs Badness",
    "pg.signs_wellness": "Signs Wellness",
    "pg.elements": "Elements",
    "pg.modality": "Modality",
    "pg.direction": "Direction",
    "pg.planet_goodness": "Planet Goodness",
    "pg.planet_badness": "Planet Badness",
    "pg.planet_wellness": "Planet Wellness (Good \u2212 Bad)",
    "pg.influences": "Influences",
    "pg.moon_phase": "Moon Phase",
    "pg.moon_darkness": "Moon Darkness",
    "pg.moon_not_dark": "Moon is not in dark phase.",
    "pg.moon_color_note": "Moon color at current phase",
    "pg.full_moon": "Full Moon",
    "pg.new_moon_short": "New Moon",
    "pg.waxing": "Waxing ({pct}%)",
    "pg.waning": "Waning ({pct}%)",
    "pg.second_from_sun": "2nd from Sun",
    "pg.twelfth_from_sun": "12th from Sun",
    "pg.dig_bala_info": "Dig Bala Info",
    "pg.dig": "Dig",
    "pg.nish": "Nish",
    "pg.combined": "Combined",
    "pg.dig_nish": "Dig+Nish",
    "pg.subathuva": "Subathuva",
    "pg.combined_strength": "Combined Planet Strength",
    "pg.total_strength": "Total Strength",
    "pg.stana_note": "Score: Exaltation=100 \u00b7 Moola Trikona=80 \u00b7 Own Sign=60 \u00b7 Friend=40 \u00b7 Neutral=30 \u00b7 Enemy=20 \u00b7 Debilitation=0 \u00b7 \U0001F504 = Neecha Bhanga (cancelled debilitation) \u2192 35",
    "pg.dig_note": "Dig Bala = directional strength (0\u2013100 based on distance from ideal house). Nish Bala = temporal strength based on day/night nature and house placement. Combined = average of both.",
    "pg.total_note": "Total = (Subathuva wellness \u00d7 40%) + (Stana Bala \u00d7 35%) + (Dig+Nish Bala \u00d7 25%)",
    "pg.default_parchment": "Default Parchment",
    "pg.no_influence": "No planetary influence \u2014 default parchment",
    "pg.aspect_tag": "(aspect)",
    "pg.placed_tag": "(placed)",
    "pg.aspect_overlay": "Default (aspect overlay)",
    "pg.moon_brightness": "Moon {pct}% Brightness",
    "pg.full_moon_silver": "Full Moon Silver-White",
    "pg.new_moon_dark": "New Moon Dark",
    "pg.show_arrows_for": "Show aspect arrows for {planet}",
    "pg.show_colors_for": "Show sign colors for {planet}",
    "pg.src_moon_dark": "Moon-dark",
    "pg.src_moon_self": "Moon-self",
    "pg.src_moon_dark_self": "Moon-dark-self",
    "pg.src_ketu_mitig": "Ketu-mitig",
    "pg.src_moon_kendra": "Moon-kendra",

    # -- playground: Moon Kendra Light --------------------------------------
    "pg.moon_kendra_light": "Moon Kendra Light",
    "pg.moon_kendra_title": "Light the 1st, 4th, 7th and 10th houses from the Moon with its current brightness",
    "pg.moon_kendra_note": "Mercury, Venus, Sun and Jupiter in a kendra (1st, 4th, 7th, 10th) from the Moon gain up to {pts} points of Subathuva goodness, in proportion to the Moon's light. Saturn, Mars, Rahu and Ketu gain nothing.",
    "pg.moon_kendra_none": "No Mercury, Venus, Sun or Jupiter in a kendra from the Moon.",
    "pg.moon_kendra_dark": "New Moon - no light, so the kendras gain nothing.",
    "pg.moon_kendra_place": "Place the Moon to light its kendras.",

    # -- playground: Connections tab ----------------------------------------
    "pg.tab_conn": "Connections",
    "pg.panel_conn": "Connection Checks",
    "pg.conn_need_asc": "Place the Ascendant to find the houses.",
    "pg.conn_2911": "2-9-11 Connection",
    "pg.conn_lord": "lord",
    "pg.conn_pair": "Houses",
    "pg.conn_links": "How they connect",
    "pg.conn_status": "Status",
    "pg.conn_yes": "Connected",
    "pg.conn_no": "Not connected",
    "pg.link_same_lord": "{planet} rules both the {a} and the {b}",
    "pg.link_exchange": "Exchange: {p1} (lord of {a}) and {p2} (lord of {b}) sit in each other's houses",
    "pg.link_in": "{planet} (lord of {a}) sits in the {b}",
    "pg.link_aspect_house": "{planet} (lord of {a}) aspects the {b} ({n} aspect)",
    "pg.link_aspect_lord": "{planet} (lord of {a}) aspects {other} (lord of {b}) ({n} aspect)",
    "pg.link_conj": "{p1} (lord of {a}) and {p2} (lord of {b}) together in {sign}",
    "pg.conn_2911_full": "All three pairs are connected - a full 2-9-11 connection.",
    "pg.conn_2911_chain": "Two of the three pairs are connected, so the 2nd, 9th and 11th are all linked.",
    "pg.conn_2911_partial": "Only the {a} and the {b} are connected; the third house stands apart.",
    "pg.conn_2911_none": "No connection between the 2nd, 9th and 11th.",
    "pg.conn_off_chart": "Not on the chart yet: {planets} - links through them can't be checked.",
    "pg.conn_2911_note": "Houses are counted from the Ascendant. Two houses connect when their lords exchange signs, when one lord sits in or aspects the other's house, when one lord aspects the other, when the lords are conjunct, or when one planet rules both.",
    "pg.conn_subha": "Subathuvam in the 8th & 12th",
    "pg.conn_house": "House",
    "pg.subha_from": "Subathuvam from",
    "pg.subha_yes": "Subathuvam",
    "pg.subha_none": "None",
    "pg.subha_in": "{planet} in the house",
    "pg.subha_aspect": "{planet} - {n} aspect",
    "pg.subha_both": "Both the 8th and the 12th have subathuvam.",
    "pg.subha_only": "Only the {n} has subathuvam.",
    "pg.subha_neither": "Neither the 8th nor the 12th has subathuvam.",
    "pg.subha_moon_yes": "Moon counts - {phase}.",
    "pg.subha_moon_no": "Moon doesn't count - {phase}. Only a full Moon, or one waxing past the 7th phase, gives subathuvam.",
    "pg.subha_moon_need_sun": "Moon not counted - place the Sun to find its phase.",
    "pg.conn_subha_note": "A house has subathuvam when Jupiter, Venus, or a Moon that is full or waxing past the 7th phase sits in it or aspects it. From signs alone, that Moon is the 5th or 6th sign from the Sun (waxing) or the 7th (full).",
    "pg.on_chart": "{planet} (on chart)",
}

_TA = {
    # -- shell / navigation --------------------------------------------------
    "app.title": "வேத ஜாதகம்",
    "app.subtitle": "நிரயன · லாகிரி அயனாம்சம்",
    "app.page_title": "வேத ஜாதக உருவாக்கி",
    "nav.admin": "நிர்வாகம்",
    "nav.install": "நிறுவு",
    "lang.label": "மொழி",

    # -- birth-details form --------------------------------------------------
    "form.name": "பெயர்",
    "form.city": "பிறந்த ஊர்",
    "form.city_placeholder": "எ.கா. மும்பை, இந்தியா",
    "form.confirm_place": "இடத்தை உறுதி செய்",
    "form.dob": "பிறந்த தேதி",
    "form.now": "இப்போது",
    "form.tob": "பிறந்த நேரம்",
    "form.lat": "அட்சரேகை",
    "form.lng": "தீர்க்கரேகை",
    "form.latlng_hint": "“இடத்தை உறுதி செய்” தானாக நிரப்பும்; நீங்களே தட்டச்சும் செய்யலாம்.",
    "form.tz": "நேர மண்டலம் (IANA பெயர்)",
    "form.tz_hint": "எ.கா. Asia/Kolkata, America/New_York, Europe/London",
    "form.style": "ஜாதக வகை",
    "form.style_south": "தென்னிந்தியம்",
    "form.style_north": "வடஇந்தியம்",
    "form.style_both": "இரண்டும்",
    "form.submit": "ஜாதகம் உருவாக்கு",
    "form.save": "விவரங்களைச் சேமி",

    # -- inline status messages ---------------------------------------------
    "geo.idle": "ஊரின் பெயரைத் தட்டச்சு செய்து “இடத்தை உறுதி செய்” அழுத்தினால் இடத்து தகவல் நிரப்பப்படும்.",
    "geo.need_city": "முதலில் பிறந்த ஊரைச் சேர்க்கவும்.",
    "geo.looking": "{place} தேடப்படுகிறது…",
    "geo.failed": "தேடல் தோல்வியடைந்தது.",
    "geo.offline": "தேடல் தோல்வி – இணைப்பைச் சரிபார்க்கவும்.",
    "save.idle": "இந்த நபரின் விவரங்களைச் சேமித்து நிர்வாகப் பக்கத்தில் காட்டும் – ஜாதகம் உருவாக்காது.",
    "save.need_name": "முதலில் பெயரைச் சேர்க்கவும்.",
    "save.saving": "சேமிக்கப்படுகிறது…",
    "save.ok": "சேமிக்கப்பட்டது – நிர்வாகப் பக்கத்தில் பார்க்கலாம்.",
    "save.failed": "சேமிக்க முடியவில்லை.",
    "save.offline": "சேமிக்க முடியவில்லை – இணைப்பைச் சரிபார்க்கவும்.",

    # -- results header ------------------------------------------------------
    "results.error": "பிழை:",
    "results.placeholder": "பிறப்பு விவரங்களை நிரப்பி “ஜாதகம் உருவாக்கு” அழுத்தினால் ஜாதகம் இங்கே தோன்றும்.",
    "meta.rashi_asc": "ராசி லக்னம்:",
    "meta.navamsa_asc": "நவாம்ச லக்னம்:",
    "meta.playground": "ஜாதகத்துடன் விளையாடு",
    "meta.download_pdf": "PDF பதிவிறக்கு",
    "meta.download_pdf": "PDF பதிவிறக்கு",

    # -- chart cards ---------------------------------------------------------
    "chart.south_d1": "தென்னிந்திய ஜாதகம் (ராசி / D1)",
    "chart.north_d1": "வடஇந்திய ஜாதகம் (ராசி / D1)",
    "chart.south_d9": "தென்னிந்திய நவாம்சம் (D9)",
    "chart.north_d9": "வடஇந்திய நவாம்சம் (D9)",
    "chart.retro_hint": "வக்கிர கிரகங்கள் ராசி (D1) ஜாதகத்தில் “(வ)” எனக் குறிக்கப்படுகின்றன. நவாம்சத்தில் (D9) வக்கிரம் குறிப்பதில்லை.",
    "chart.word": "ஜாதகம்",
    "chart.rashi": "ராசி",
    "chart.navamsa": "நவாம்சம்",

    # -- nakshatra table -----------------------------------------------------
    "section.star": "கிரக & நட்சத்திர விவரங்கள்",
    "star.hint": "சூரியனுக்கு மிக அருகில் உள்ள (அஸ்தமனமான) கிரகங்கள் பெயருக்கு முன் 🔥 குறியுடன் காட்டப்படுகின்றன.",
    "th.planet": "கிரகம்",
    "th.sign": "ராசி",
    "th.degree": "பாகை",
    "th.nakshatra": "நட்சத்திரம்",
    "th.pada": "பாதம்",
    "th.nak_lord": "நட்சத்திர அதிபதி",

    # -- dasha table ---------------------------------------------------------
    "section.dasha": "விம்சோத்தரி மகா தசை",
    "dasha.hint": "எந்த வரிசையையும் தட்டினால் அதன் உட்காலங்கள் விரியும் (புக்தி → அந்தரம் → சூட்சுமம்). மீண்டும் தட்டினால் மூடும்.",
    "dasha.footnote": "பிறப்பின் சந்திர நட்சத்திரத்தை அடிப்படையாகக் கொண்ட நிலையான விம்சோத்தரி முறை (120 ஆண்டு சுழற்சி, 9 கிரக அதிபதிகள்) பயன்படுத்திக் கணக்கிடப்பட்டது. Kerykeion அல்லது jyotichart இதைத் தருவதில்லை.",
    "th.lord": "அதிபதி",
    "th.start": "தொடக்கம்",
    "th.end": "முடிவு",
    "th.years": "ஆண்டு",

    # -- houses involved -----------------------------------------------------
    "section.houses": "சம்பந்தப்பட்ட வீடுகள்",
    "houses.hint": "மகா தசை வரிசையைத் தட்டினால் அந்த அதிபதி தூண்டும் வீடுகள் (இருப்பு, பார்வை, ஆட்சி – ராகு/கேதுவிற்கு அவற்றுடன் தொடர்புடைய கிரகங்கள் ஆளும் வீடுகள்) அந்தக் கால எல்லையுடன் காட்டப்படும். புக்தி வரிசையைத் தட்டினால் மகா தசை மற்றும் புக்தி அதிபதிகள் இரண்டும் சேர்ந்து காட்டப்படும். அந்தர வரிசையைத் தட்டினால் அந்தர அதிபதியும் சேர்த்துக் காட்டப்படும்.",
    "houses.placeholder": "மேலே உள்ள மகா தசை, புக்தி அல்லது அந்தர வரிசையைத் தட்டவும்.",
    "houses.no_data": "வீடு தகவல் இல்லை.",
    "phrase.lord_of": "ஆட்சி",
    "phrase.placement": "இருப்பு",
    "phrase.aspects": "பார்வை",
    "phrase.dispositor": "ராசி அதிபதி",
    "phrase.of": "ஆளும்",
    "phrase.dispositor_none": "ராசி அதிபதி – இல்லை",
    "phrase.conjunct": "சேர்க்கை",
    "phrase.aspected_by": "பார்க்கப்படுவது",
    "phrase.none": "இல்லை",
    "phrase.house": "வீடு",
    "phrase.houses": "வீடுகள்",

    # -- conjunctions --------------------------------------------------------
    "section.conj_degree": "சேர்க்கைகள் – பாகை அடிப்படையில்",
    "conj_degree.hint": "உண்மையான தீர்க்கரேகையை வைத்துக் கணக்கிடப்பட்டது – வெறுமனே ஒரே ராசி என்பதால் அல்ல. 10°க்குள் உள்ள கிரகங்கள் (மற்றும் லக்னம்) சேர்க்கையாகக் கொள்ளப்படுகின்றன. பாரம்பரிய ராசி அடிப்படையிலான பார்வைக்கு கீழே காண்க.",
    "conj_degree.none": "இந்த ஜாதகத்தில் 10°க்குள் எந்தச் சேர்க்கையும் இல்லை.",
    "section.conj_sign": "சேர்க்கைகள் – ராசி அடிப்படையில்",
    "conj_sign.hint": "பாரம்பரிய ராசி சேர்க்கை: ஒரே ராசியில் உள்ள எல்லா கிரக ஜோடிகளும் (லக்னம் உட்பட), அவற்றின் பாகை இடைவெளியுடன் – இறுக்கமான 2° சேர்க்கையும் தளர்வான 25° சேர்க்கையும் ஒன்றாகக் கருதப்படாமல் இருக்கும்.",
    "conj_sign.none": "இந்த ஜாதகத்தில் இரண்டு கிரகங்கள் ஒரே ராசியில் இல்லை.",
    "conj.signs_label": "ராசி(கள்)",
    "conj.apart": "இடைவெளி",

    # -- admin ---------------------------------------------------------------
    "admin.login_page_title": "நிர்வாக உள்நுழைவு – வேத ஜாதகம்",
    "admin.login_title": "நிர்வாக உள்நுழைவு",
    "admin.password": "கடவுச்சொல்",
    "admin.sign_in": "உள்நுழை",
    "admin.wrong_password": "தவறான கடவுச்சொல்.",
    "admin.page_title": "நிர்வாகம் – சேமித்த பிறப்பு விவரங்கள்",
    "admin.stored": "சேமித்த பிறப்பு விவரங்கள்",
    "admin.new_chart": "புதிய ஜாதகம்",
    "admin.log_out": "வெளியேறு",
    "admin.unknown_city": "ஊர் தெரியவில்லை",
    "admin.dob": "பிறந்த தேதி",
    "admin.tob": "பிறந்த நேரம்",
    "admin.latlng": "அட்சம், தீர்க்கம்",
    "admin.timezone": "நேர மண்டலம்",
    "admin.saved_at": "சேமிக்கப்பட்டது",
    "admin.go_to_chart": "ஜாதகத்திற்குச் செல்",
    "admin.empty": "இதுவரை எந்த பதிவும் சேமிக்கப்படவில்லை – முதன்மைப் பக்கத்தில் ஒரு ஜாதகம் உருவாக்கினால் இங்கே தோன்றும்.",

    # -- PDF export ----------------------------------------------------------
    "pdf.subtitle": "\u0bb5\u0bc7\u0ba4 \u0b9c\u0bbe\u0ba4\u0b95\u0bae\u0bcd \u00b7 \u0ba8\u0bbf\u0bb0\u0baf\u0ba9 \u00b7 \u0bb2\u0bbe\u0b95\u0bbf\u0bb0\u0bbf \u0b85\u0baf\u0ba9\u0bbe\u0bae\u0bcd\u0b9a\u0bae\u0bcd",
    "pdf.birth_details": "\u0baa\u0bbf\u0bb1\u0baa\u0bcd\u0baa\u0bc1 \u0bb5\u0bbf\u0bb5\u0bb0\u0b99\u0bcd\u0b95\u0bb3\u0bcd",
    "pdf.charts_heading": "\u0bb0\u0bbe\u0b9a\u0bbf (D1) & \u0ba8\u0bb5\u0bbe\u0bae\u0bcd\u0b9a\u0bae\u0bcd (D9) \u0b9c\u0bbe\u0ba4\u0b95\u0b99\u0bcd\u0b95\u0bb3\u0bcd",
    "pdf.bhukti_heading": "\u0bb5\u0bbf\u0bae\u0bcd\u0b9a\u0bcb\u0ba4\u0bcd\u0ba4\u0bb0\u0bbf \u0ba4\u0b9a\u0bc8-\u0baa\u0bc1\u0b95\u0bcd\u0ba4\u0bbf",
    # One period, spelled out over two lines - see chart_pdf._bhukti_lines.
    "pdf.bhukti_line": "{role} \u00b7 {maha} {maha_label} \u2013 {antar} {antar_label}",
    "pdf.bhukti_dates": "{start} \u2192 {end} \u00b7 {years} {years_unit}",
    "pdf.years_unit": "\u0b86\u0ba3\u0bcd\u0b9f\u0bc1\u0b95\u0bb3\u0bcd",
    "pdf.bhukti_note": "{date} \u0b85\u0ba9\u0bcd\u0bb1\u0bc1 \u0ba8\u0b9f\u0bc8\u0baa\u0bc6\u0bb1\u0bc1\u0bae\u0bcd \u0bae\u0b95\u0bbe \u0ba4\u0b9a\u0bc8-\u0baa\u0bc1\u0b95\u0bcd\u0ba4\u0bbf \u0b95\u0bbe\u0bb2\u0bae\u0bcd \u0ba4\u0b99\u0bcd\u0b95 \u0ba8\u0bbf\u0bb1\u0ba4\u0bcd\u0ba4\u0bbf\u0bb2\u0bcd \u0b95\u0bbe\u0b9f\u0bcd\u0b9f\u0baa\u0bcd\u0baa\u0b9f\u0bcd\u0b9f\u0bc1\u0bb3\u0bcd\u0bb3\u0ba4\u0bc1; \u0b85\u0ba4\u0bb1\u0bcd\u0b95\u0bc1 \u0bae\u0bc1\u0ba9\u0bcd\u0ba9\u0bc8\u0baf \u0b95\u0bbe\u0bb2\u0bae\u0bc1\u0bae\u0bcd \u0b85\u0b9f\u0bc1\u0ba4\u0bcd\u0ba4 \u0b87\u0bb0\u0ba3\u0bcd\u0b9f\u0bc1\u0bae\u0bcd \u0b95\u0bbe\u0b9f\u0bcd\u0b9f\u0baa\u0bcd\u0baa\u0b9f\u0bcd\u0b9f\u0bc1\u0bb3\u0bcd\u0bb3\u0ba9.",
    "pdf.antaram_heading": "{maha} {maha_label} \u2013 {antar} {antar_label}: {level} \u0b95\u0bbe\u0bb2\u0b99\u0bcd\u0b95\u0bb3\u0bcd",
    "pdf.antaram_note": "{date} \u0b85\u0ba9\u0bcd\u0bb1\u0bc1 \u0ba8\u0b9f\u0bc8\u0baa\u0bc6\u0bb1\u0bc1\u0bae\u0bcd {level} \u0ba4\u0b99\u0bcd\u0b95 \u0ba8\u0bbf\u0bb1\u0ba4\u0bcd\u0ba4\u0bbf\u0bb2\u0bcd \u0b95\u0bbe\u0b9f\u0bcd\u0b9f\u0baa\u0bcd\u0baa\u0b9f\u0bcd\u0b9f\u0bc1\u0bb3\u0bcd\u0bb3\u0ba4\u0bc1.",
    "pdf.houses_note": "\u0bb5\u0bc0\u0b9f\u0bc1\u0b95\u0bb3\u0bcd \u0bb0\u0bbe\u0b9a\u0bbf \u0bb2\u0b95\u0bcd\u0ba9\u0ba4\u0bcd\u0ba4\u0bbf\u0bb2\u0bbf\u0bb0\u0bc1\u0ba8\u0bcd\u0ba4\u0bc1 \u0b8e\u0ba3\u0bcd\u0ba3\u0baa\u0bcd\u0baa\u0b9f\u0bc1\u0b95\u0bbf\u0ba9\u0bcd\u0bb1\u0ba9. \u0b92\u0bb5\u0bcd\u0bb5\u0bca\u0bb0\u0bc1 \u0b95\u0bbf\u0bb0\u0b95\u0bae\u0bc1\u0bae\u0bcd \u0ba4\u0bbe\u0ba9\u0bcd \u0b87\u0bb0\u0bc1\u0b95\u0bcd\u0b95\u0bc1\u0bae\u0bcd \u0bb5\u0bc0\u0b9f\u0bc1, \u0baa\u0bbe\u0bb0\u0bcd\u0b95\u0bcd\u0b95\u0bc1\u0bae\u0bcd \u0bb5\u0bc0\u0b9f\u0bc1\u0b95\u0bb3\u0bcd, \u0b86\u0bb3\u0bc1\u0bae\u0bcd \u0bb5\u0bc0\u0b9f\u0bc1\u0b95\u0bb3\u0bcd \u0b86\u0b95\u0bbf\u0baf\u0bb5\u0bb1\u0bcd\u0bb1\u0bc8\u0ba4\u0bcd \u0ba4\u0bc2\u0ba3\u0bcd\u0b9f\u0bc1\u0b95\u0bbf\u0bb1\u0ba4\u0bc1; \u0bb0\u0bbe\u0b95\u0bc1, \u0b95\u0bc7\u0ba4\u0bc1\u0bb5\u0bc1\u0b95\u0bcd\u0b95\u0bc1 \u0b9a\u0bca\u0ba8\u0bcd\u0ba4 \u0baa\u0bbe\u0bb0\u0bcd\u0bb5\u0bc8\u0baf\u0bcb \u0bb0\u0bbe\u0b9a\u0bbf\u0baf\u0bcb \u0b87\u0bb2\u0bcd\u0bb2\u0bbe\u0ba4\u0ba4\u0bbe\u0bb2\u0bcd \u0b85\u0bb5\u0bb1\u0bcd\u0bb1\u0bc1\u0b9f\u0ba9\u0bcd \u0ba4\u0bca\u0b9f\u0bb0\u0bcd\u0baa\u0bc1\u0b9f\u0bc8\u0baf \u0b95\u0bbf\u0bb0\u0b95\u0b99\u0bcd\u0b95\u0bb3\u0bcd \u0bb5\u0bb4\u0bbf\u0baf\u0bbe\u0b95\u0b9a\u0bcd \u0b9a\u0bc6\u0baf\u0bb2\u0bcd\u0baa\u0b9f\u0bc1\u0b95\u0bbf\u0ba9\u0bcd\u0bb1\u0ba9.",
    "pdf.generated": "{timestamp} \u0b85\u0ba9\u0bcd\u0bb1\u0bc1 \u0b89\u0bb0\u0bc1\u0bb5\u0bbe\u0b95\u0bcd\u0b95\u0baa\u0bcd\u0baa\u0b9f\u0bcd\u0b9f\u0ba4\u0bc1 \u00b7 Kerykeion \u0bb5\u0bb4\u0bbf Swiss Ephemeris \u0ba4\u0bb0\u0bb5\u0bc1.",
    "pdf.coordinates": "\u0b85\u0b9f\u0bcd\u0b9a\u0bae\u0bcd, \u0ba4\u0bc0\u0bb0\u0bcd\u0b95\u0bcd\u0b95\u0bae\u0bcd",
    "pdf.ayanamsa": "\u0b85\u0baf\u0ba9\u0bbe\u0bae\u0bcd\u0b9a\u0bae\u0bcd",
    "pdf.ayanamsa_value": "\u0bb2\u0bbe\u0b95\u0bbf\u0bb0\u0bbf (\u0ba8\u0bbf\u0bb0\u0baf\u0ba9)",
    "pdf.rashi_asc": "\u0bb0\u0bbe\u0b9a\u0bbf \u0bb2\u0b95\u0bcd\u0ba9\u0bae\u0bcd",
    "pdf.navamsa_asc": "\u0ba8\u0bb5\u0bbe\u0bae\u0bcd\u0b9a \u0bb2\u0b95\u0bcd\u0ba9\u0bae\u0bcd",
    "pdf.combust": "\u0b85\u0bb8\u0bcd\u0ba4\u0bae\u0ba9\u0bae\u0bcd",
    "pdf.page": "\u0baa\u0b95\u0bcd\u0b95\u0bae\u0bcd",

    # -- playground: chrome --------------------------------------------------
    "pg.page_title": "ஜாதகத்துடன் விளையாடு – வேத ஜாதகம்",
    "pg.back": "உருவாக்கிக்குத் திரும்பு",
    "pg.title": "தென்னிந்திய ஜாதகம்",
    "pg.clear": "ஜாதகத்தை அழி",
    "pg.ray_opacity": "பார்வைக் கோட்டு அடர்த்தி",
    "pg.grahas": "கிரகங்கள்",
    "pg.col_planet": "கிரகம்",
    "pg.col_arrow_title": "பார்வை அம்புகளைக் காட்டு",
    "pg.col_color_title": "ராசி நிறங்களைக் காட்டு",
    "pg.all": "அனைத்தும்",
    "pg.legend": "கிரகங்களை ஜாதகத்திற்கு இழுக்கவும், அல்லது ஒன்றைத் தொட்டபின் ஒரு வீட்டைத் தொடவும்.<br>வைத்த கிரகத்தைத் தொட்டால் நீக்கலாம்.<br><br><span style=\"color:#d4af37\">{asc}</span> = 1ஆம் வீடு.",

    # -- playground: compare mode -------------------------------------------
    "pg.compare": "ஜாதகங்களை ஒப்பிடு",
    "pg.compare_exit": "ஒற்றை ஜாதகம்",
    "pg.compare_hint": "இரண்டு தனித்த ஜாதகங்கள் - ஒவ்வொன்றையும் தனியே இழுத்து, வைத்து, அளவிடலாம்.",
    "pg.chart_a": "ஜாதகம் A",
    "pg.chart_b": "ஜாதகம் B",
    "pg.copy_a_b": "A \u2192 B நகல்",
    "pg.copy_b_a": "B \u2192 A நகல்",
    "pg.swap_ab": "A \u21c4 B மாற்று",
    "pg.sync_tabs": "தாவல்கள் ஒத்திசை",
    "pg.sync_tabs_title": "இரண்டு ஜாதகங்களையும் ஒரே தாவலில் வை",

    # -- playground: dashboards ---------------------------------------------
    "pg.tab_good": "நன்மை",
    "pg.tab_bad": "தீமை",
    "pg.tab_well": "நலன்",
    "pg.tab_plan": "சுபத்துவம்",
    "pg.tab_stana": "ஸ்தான பலம்",
    "pg.tab_dig": "திக்+நிச பலம்",
    "pg.tab_total": "மொத்த பலம்",
    "pg.tab_sigcol": "ராசி நிறங்கள்",
    "pg.panel_good": "நன்மை பலகை",
    "pg.panel_bad": "தீமை பலகை",
    "pg.panel_well": "நலன் பலகை",
    "pg.panel_plan": "சுபத்துவம் — கிரக நலன்",
    "pg.panel_stana": "ஸ்தான பலம் (இடப் பலம்)",
    "pg.panel_dig": "திக் பலம் + நிச பலம்",
    "pg.panel_total": "மொத்த கிரக பலம்",
    "pg.panel_sigcol": "ராசி நிற பகுப்பாய்வு",
    "pg.no_data": "பகுப்பாய்வைக் காண கிரகங்களை வைக்கவும்.",
    "pg.no_data_colors": "ராசி நிறங்களைக் காண கிரகங்களை வைக்கவும்.",

    # -- playground: table + section labels ---------------------------------
    "pg.rank": "#",
    "pg.sign": "ராசி",
    "pg.house": "வீடு",
    "pg.score": "மதிப்பெண்",
    "pg.strength": "பலம்",
    "pg.total": "மொத்தம்",
    "pg.planet": "கிரகம்",
    "pg.placed_in": "இருப்பு",
    "pg.status": "நிலை",
    "pg.sources": "காரணங்கள்",
    "pg.good": "நன்மை",
    "pg.bad": "தீமை",
    "pg.net": "நிகரம்",
    "pg.by_element": "பூதம் வாரியாக",
    "pg.by_modality": "தன்மை வாரியாக",
    "pg.by_direction": "திசை வாரியாக",
    "pg.all_signs": "அனைத்து ராசிகள்",
    "pg.strongest": "மிக பலம்",
    "pg.weakest": "மிகக் குறைவு",
    "pg.stana_bala": "ஸ்தான பலம்",
    "pg.dig_bala": "திக் பலம்",
    "pg.nish_bala": "நிச பலம்",
    "pg.not_placed": "வைக்கப்படவில்லை",
    "pg.no_dig_bala": "திக் பலம் இல்லை",
    "pg.best_at": "சிறந்தது {house}",
    "pg.house_from_sun": "சூரியனிலிருந்து {n}ஆம் வீடு (வலமாக)",
    "pg.new_moon": "அமாவாசை — ஒளி இல்லை",
    "pg.nth_from_sun": "சூரியனிலிருந்து {n}",
    "pg.color": "நிறம்",
    "pg.layers": "அடுக்குகள்",
    "pg.base": "அடிப்படை",
    "pg.h": "\u0bb5\u0bc0",
    "pg.no_data_simple": "\u0ba4\u0b95\u0bb5\u0bb2\u0bcd \u0b87\u0bb2\u0bcd\u0bb2\u0bc8.",
    "pg.none_simple": "\u0b8e\u0ba4\u0bc1\u0bb5\u0bc1\u0bae\u0bcd \u0b87\u0bb2\u0bcd\u0bb2\u0bc8.",
    "pg.signs_goodness": "\u0bb0\u0bbe\u0b9a\u0bbf \u0ba8\u0ba9\u0bcd\u0bae\u0bc8",
    "pg.signs_badness": "\u0bb0\u0bbe\u0b9a\u0bbf \u0ba4\u0bc0\u0bae\u0bc8",
    "pg.signs_wellness": "\u0bb0\u0bbe\u0b9a\u0bbf \u0ba8\u0bb2\u0ba9\u0bcd",
    "pg.elements": "\u0baa\u0bc2\u0ba4\u0b99\u0bcd\u0b95\u0bb3\u0bcd",
    "pg.modality": "\u0ba4\u0ba9\u0bcd\u0bae\u0bc8",
    "pg.direction": "\u0ba4\u0bbf\u0b9a\u0bc8",
    "pg.planet_goodness": "\u0b95\u0bbf\u0bb0\u0b95 \u0ba8\u0ba9\u0bcd\u0bae\u0bc8",
    "pg.planet_badness": "\u0b95\u0bbf\u0bb0\u0b95 \u0ba4\u0bc0\u0bae\u0bc8",
    "pg.planet_wellness": "\u0b95\u0bbf\u0bb0\u0b95 \u0ba8\u0bb2\u0ba9\u0bcd (\u0ba8\u0ba9\u0bcd\u0bae\u0bc8 \u2212 \u0ba4\u0bc0\u0bae\u0bc8)",
    "pg.influences": "\u0ba4\u0bbe\u0b95\u0bcd\u0b95\u0b99\u0bcd\u0b95\u0bb3\u0bcd",
    "pg.moon_phase": "\u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0 \u0b95\u0bb2\u0bc8",
    "pg.moon_darkness": "\u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0 \u0b87\u0bb0\u0bc1\u0bb3\u0bcd",
    "pg.moon_not_dark": "\u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0ba9\u0bcd \u0b87\u0bb0\u0bc1\u0ba3\u0bcd\u0b9f \u0ba8\u0bbf\u0bb2\u0bc8\u0baf\u0bbf\u0bb2\u0bcd \u0b87\u0bb2\u0bcd\u0bb2\u0bc8.",
    "pg.moon_color_note": "\u0ba4\u0bb1\u0bcd\u0baa\u0bcb\u0ba4\u0bc8\u0baf \u0b95\u0bb2\u0bc8\u0baf\u0bbf\u0bb2\u0bcd \u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0 \u0ba8\u0bbf\u0bb1\u0bae\u0bcd",
    "pg.full_moon": "\u0baa\u0bc6\u0bb3\u0bcd\u0bb3\u0bbf \u0bb5\u0bbf\u0bb3\u0b95\u0bcd\u0b95\u0bc1",
    "pg.new_moon_short": "\u0b85\u0bae\u0bbe\u0bb5\u0bbe\u0b9a\u0bc8",
    "pg.waxing": "\u0bb5\u0bb3\u0bb0\u0bcd\u0baa\u0bbf\u0bb1\u0bc8 ({pct}%)",
    "pg.waning": "\u0ba4\u0bc7\u0baf\u0bcd\u0baa\u0bbf\u0bb1\u0bc8 ({pct}%)",
    "pg.second_from_sun": "\u0b9a\u0bc2\u0bb0\u0bbf\u0baf\u0ba9\u0bbf\u0bb2\u0bbf\u0bb0\u0bc1\u0ba8\u0bcd\u0ba4\u0bc1 2\u0b86\u0bae\u0bcd",
    "pg.twelfth_from_sun": "\u0b9a\u0bc2\u0bb0\u0bbf\u0baf\u0ba9\u0bbf\u0bb2\u0bbf\u0bb0\u0bc1\u0ba8\u0bcd\u0ba4\u0bc1 12\u0b86\u0bae\u0bcd",
    "pg.dig_bala_info": "\u0ba4\u0bbf\u0b95\u0bcd \u0baa\u0bb2 \u0bb5\u0bbf\u0bb5\u0bb0\u0bae\u0bcd",
    "pg.dig": "\u0ba4\u0bbf\u0b95\u0bcd",
    "pg.nish": "\u0ba8\u0bbf\u0b9a",
    "pg.combined": "\u0b92\u0bb0\u0bc1\u0b99\u0bcd\u0b95\u0bbf\u0ba3\u0bc8\u0ba8\u0bcd\u0ba4\u0ba4\u0bc1",
    "pg.dig_nish": "\u0ba4\u0bbf\u0b95\u0bcd+\u0ba8\u0bbf\u0b9a",
    "pg.subathuva": "\u0b9a\u0bc1\u0baa\u0ba4\u0bcd\u0ba4\u0bc1\u0bb5\u0bae\u0bcd",
    "pg.combined_strength": "\u0b92\u0bb0\u0bc1\u0b99\u0bcd\u0b95\u0bbf\u0ba3\u0bc8\u0ba8\u0bcd\u0ba4 \u0b95\u0bbf\u0bb0\u0b95 \u0baa\u0bb2\u0bae\u0bcd",
    "pg.total_strength": "\u0bae\u0bca\u0ba4\u0bcd\u0ba4 \u0baa\u0bb2\u0bae\u0bcd",
    "pg.stana_note": "\u0bae\u0ba4\u0bbf\u0baa\u0bcd\u0baa\u0bc6\u0ba3\u0bcd: \u0b89\u0b9a\u0bcd\u0b9a\u0bae\u0bcd=100 \u00b7 \u0bae\u0bc2\u0bb2\u0ba4\u0bcd\u0ba4\u0bbf\u0bb0\u0bbf\u0b95\u0bcb\u0ba3\u0bae\u0bcd=80 \u00b7 \u0b86\u0b9f\u0bcd\u0b9a\u0bbf=60 \u00b7 \u0ba8\u0b9f\u0bcd\u0baa\u0bc1=40 \u00b7 \u0b9a\u0bae\u0bae\u0bcd=30 \u00b7 \u0baa\u0b95\u0bc8=20 \u00b7 \u0ba8\u0bc0\u0b9a\u0bae\u0bcd=0 \u00b7 \U0001F504 = \u0ba8\u0bc0\u0b9a\u0baa\u0b99\u0bcd\u0b95\u0bae\u0bcd \u2192 35",
    "pg.dig_note": "\u0ba4\u0bbf\u0b95\u0bcd \u0baa\u0bb2\u0bae\u0bcd = \u0b9a\u0bbf\u0bb1\u0ba8\u0bcd\u0ba4 \u0bb5\u0bc0\u0b9f\u0bcd\u0b9f\u0bbf\u0bb2\u0bbf\u0bb0\u0bc1\u0ba8\u0bcd\u0ba4\u0bc1 \u0b89\u0bb3\u0bcd\u0bb3 \u0ba4\u0bc2\u0bb0\u0ba4\u0bcd\u0ba4\u0bc8 \u0bb5\u0bc8\u0ba4\u0bcd\u0ba4 \u0ba4\u0bbf\u0b9a\u0bc8\u0baa\u0bcd \u0baa\u0bb2\u0bae\u0bcd (0\u2013100). \u0ba8\u0bbf\u0b9a \u0baa\u0bb2\u0bae\u0bcd = \u0baa\u0b95\u0bb2\u0bcd/\u0b87\u0bb0\u0bb5\u0bc1 \u0ba4\u0ba9\u0bcd\u0bae\u0bc8 \u0bae\u0bb1\u0bcd\u0bb1\u0bc1\u0bae\u0bcd \u0bb5\u0bc0\u0b9f\u0bcd\u0b9f\u0bc1 \u0b87\u0bb0\u0bc1\u0baa\u0bcd\u0baa\u0bc8 \u0bb5\u0bc8\u0ba4\u0bcd\u0ba4 \u0b95\u0bbe\u0bb2 \u0baa\u0bb2\u0bae\u0bcd. \u0b92\u0bb0\u0bc1\u0b99\u0bcd\u0b95\u0bbf\u0ba3\u0bc8\u0ba8\u0bcd\u0ba4\u0ba4\u0bc1 = \u0b87\u0bb0\u0ba3\u0bcd\u0b9f\u0bbf\u0ba9\u0bcd \u0b9a\u0bb0\u0bbe\u0b9a\u0bb0\u0bbf.",
    "pg.total_note": "\u0bae\u0bca\u0ba4\u0bcd\u0ba4\u0bae\u0bcd = (\u0b9a\u0bc1\u0baa\u0ba4\u0bcd\u0ba4\u0bc1\u0bb5 \u0ba8\u0bb2\u0ba9\u0bcd \u00d7 40%) + (\u0bb8\u0bcd\u0ba4\u0bbe\u0ba9 \u0baa\u0bb2\u0bae\u0bcd \u00d7 35%) + (\u0ba4\u0bbf\u0b95\u0bcd+\u0ba8\u0bbf\u0b9a \u0baa\u0bb2\u0bae\u0bcd \u00d7 25%)",
    "pg.default_parchment": "\u0b87\u0baf\u0bb2\u0bcd\u0baa\u0bc1 \u0ba8\u0bbf\u0bb1\u0bae\u0bcd",
    "pg.no_influence": "\u0b95\u0bbf\u0bb0\u0b95 \u0ba4\u0bbe\u0b95\u0bcd\u0b95\u0bae\u0bcd \u0b87\u0bb2\u0bcd\u0bb2\u0bc8 \u2014 \u0b87\u0baf\u0bb2\u0bcd\u0baa\u0bc1 \u0ba8\u0bbf\u0bb1\u0bae\u0bcd",
    "pg.aspect_tag": "(\u0baa\u0bbe\u0bb0\u0bcd\u0bb5\u0bc8)",
    "pg.placed_tag": "(\u0bb5\u0bc8\u0ba4\u0bcd\u0ba4\u0ba4\u0bc1)",
    "pg.aspect_overlay": "\u0b87\u0baf\u0bb2\u0bcd\u0baa\u0bc1 (\u0baa\u0bbe\u0bb0\u0bcd\u0bb5\u0bc8 \u0bae\u0bc7\u0bb2\u0b9f\u0bc1\u0b95\u0bcd\u0b95\u0bc1)",
    "pg.moon_brightness": "\u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0ba9\u0bcd {pct}% \u0b92\u0bb3\u0bbf",
    "pg.full_moon_silver": "\u0baa\u0bc6\u0bb3\u0bcd\u0bb3\u0bbf \u0bb5\u0bbf\u0bb3\u0b95\u0bcd\u0b95\u0bc1 \u0bb5\u0bc6\u0ba3\u0bcd\u0bae\u0bc8",
    "pg.new_moon_dark": "\u0b85\u0bae\u0bbe\u0bb5\u0bbe\u0b9a\u0bc8 \u0b87\u0bb0\u0bc1\u0bb3\u0bcd",
    "pg.show_arrows_for": "{planet} \u0baa\u0bbe\u0bb0\u0bcd\u0bb5\u0bc8 \u0b85\u0bae\u0bcd\u0baa\u0bc1\u0b95\u0bb3\u0bc8\u0b95\u0bcd \u0b95\u0bbe\u0b9f\u0bcd\u0b9f\u0bc1",
    "pg.show_colors_for": "{planet} \u0bb0\u0bbe\u0b9a\u0bbf \u0ba8\u0bbf\u0bb1\u0b99\u0bcd\u0b95\u0bb3\u0bc8\u0b95\u0bcd \u0b95\u0bbe\u0b9f\u0bcd\u0b9f\u0bc1",
    "pg.src_moon_dark": "\u0b9a\u0ba8\u0bcd-\u0b87\u0bb0\u0bc1\u0bb3\u0bcd",
    "pg.src_moon_self": "\u0b9a\u0ba8\u0bcd-\u0ba4\u0bbe\u0ba9\u0bc7",
    "pg.src_moon_dark_self": "\u0b9a\u0ba8\u0bcd-\u0b87\u0bb0\u0bc1\u0bb3\u0bcd-\u0ba4\u0bbe\u0ba9\u0bc7",
    "pg.src_ketu_mitig": "\u0b95\u0bc7\u0ba4\u0bc1-\u0ba4\u0ba3\u0bbf\u0baa\u0bcd\u0baa\u0bc1",
    "pg.src_moon_kendra": "\u0b9a\u0ba8\u0bcd-\u0b95\u0bc7\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0bae\u0bcd",

    # -- playground: Moon Kendra Light --------------------------------------
    "pg.moon_kendra_light": "\u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0 \u0b95\u0bc7\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0 \u0b92\u0bb3\u0bbf",
    "pg.moon_kendra_title": "\u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0ba9\u0bbf\u0bb2\u0bbf\u0bb0\u0bc1\u0ba8\u0bcd\u0ba4\u0bc1 1, 4, 7, 10\u0b86\u0bae\u0bcd \u0bb5\u0bc0\u0b9f\u0bc1\u0b95\u0bb3\u0bc8 \u0b85\u0ba4\u0ba9\u0bcd \u0ba4\u0bb1\u0bcd\u0baa\u0bcb\u0ba4\u0bc8\u0baf \u0b92\u0bb3\u0bbf\u0baf\u0bc1\u0b9f\u0ba9\u0bcd \u0b92\u0bb3\u0bbf\u0bb0\u0b9a\u0bcd \u0b9a\u0bc6\u0baf\u0bcd",
    "pg.moon_kendra_note": "\u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0ba9\u0bc1\u0b95\u0bcd\u0b95\u0bc1\u0b95\u0bcd \u0b95\u0bc7\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0ba4\u0bcd\u0ba4\u0bbf\u0bb2\u0bcd (1, 4, 7, 10) \u0b89\u0bb3\u0bcd\u0bb3 \u0baa\u0bc1\u0ba4\u0ba9\u0bcd, \u0b9a\u0bc1\u0b95\u0bcd\u0b95\u0bbf\u0bb0\u0ba9\u0bcd, \u0b9a\u0bc2\u0bb0\u0bbf\u0baf\u0ba9\u0bcd, \u0b95\u0bc1\u0bb0\u0bc1 \u0b86\u0b95\u0bbf\u0baf\u0bb5\u0bc8 \u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0 \u0b92\u0bb3\u0bbf\u0b95\u0bcd\u0b95\u0bc1 \u0b8f\u0bb1\u0bcd\u0baa \u0b9a\u0bc1\u0baa\u0ba4\u0bcd\u0ba4\u0bc1\u0bb5 \u0ba8\u0ba9\u0bcd\u0bae\u0bc8\u0baf\u0bbf\u0bb2\u0bcd \u0b85\u0ba4\u0bbf\u0b95\u0baa\u0b9f\u0bcd\u0b9a\u0bae\u0bcd {pts} \u0baa\u0bc1\u0bb3\u0bcd\u0bb3\u0bbf\u0b95\u0bb3\u0bcd \u0baa\u0bc6\u0bb1\u0bc1\u0bae\u0bcd. \u0b9a\u0ba9\u0bbf, \u0b9a\u0bc6\u0bb5\u0bcd\u0bb5\u0bbe\u0baf\u0bcd, \u0bb0\u0bbe\u0b95\u0bc1, \u0b95\u0bc7\u0ba4\u0bc1 \u0baa\u0bc6\u0bb1\u0bbe\u0ba4\u0bc1.",
    "pg.moon_kendra_none": "\u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0ba9\u0bc1\u0b95\u0bcd\u0b95\u0bc1\u0b95\u0bcd \u0b95\u0bc7\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0ba4\u0bcd\u0ba4\u0bbf\u0bb2\u0bcd \u0baa\u0bc1\u0ba4\u0ba9\u0bcd, \u0b9a\u0bc1\u0b95\u0bcd\u0b95\u0bbf\u0bb0\u0ba9\u0bcd, \u0b9a\u0bc2\u0bb0\u0bbf\u0baf\u0ba9\u0bcd, \u0b95\u0bc1\u0bb0\u0bc1 \u0b8e\u0ba4\u0bc1\u0bb5\u0bc1\u0bae\u0bcd \u0b87\u0bb2\u0bcd\u0bb2\u0bc8.",
    "pg.moon_kendra_dark": "\u0b85\u0bae\u0bbe\u0bb5\u0bbe\u0b9a\u0bc8 - \u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0ba9\u0bc1\u0b95\u0bcd\u0b95\u0bc1 \u0b92\u0bb3\u0bbf \u0b87\u0bb2\u0bcd\u0bb2\u0bc8, \u0b8e\u0ba9\u0bb5\u0bc7 \u0b95\u0bc7\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0b99\u0bcd\u0b95\u0bb3\u0bc1\u0b95\u0bcd\u0b95\u0bc1\u0baa\u0bcd \u0baa\u0bb2\u0bae\u0bcd \u0b87\u0bb2\u0bcd\u0bb2\u0bc8.",
    "pg.moon_kendra_place": "\u0b95\u0bc7\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0b99\u0bcd\u0b95\u0bb3\u0bc8 \u0b92\u0bb3\u0bbf\u0bb0\u0b9a\u0bcd \u0b9a\u0bc6\u0baf\u0bcd\u0baf \u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0ba9\u0bc8 \u0b9c\u0bbe\u0ba4\u0b95\u0ba4\u0bcd\u0ba4\u0bbf\u0bb2\u0bcd \u0bb5\u0bc8\u0b95\u0bcd\u0b95\u0bb5\u0bc1\u0bae\u0bcd.",

    # -- playground: Connections tab ----------------------------------------
    "pg.tab_conn": "\u0ba4\u0bca\u0b9f\u0bb0\u0bcd\u0baa\u0bc1\u0b95\u0bb3\u0bcd",
    "pg.panel_conn": "\u0ba4\u0bca\u0b9f\u0bb0\u0bcd\u0baa\u0bc1 \u0b9a\u0bcb\u0ba4\u0ba9\u0bc8\u0b95\u0bb3\u0bcd",
    "pg.conn_need_asc": "\u0bb5\u0bc0\u0b9f\u0bc1\u0b95\u0bb3\u0bc8\u0b95\u0bcd \u0b95\u0ba3\u0bcd\u0b9f\u0bb1\u0bbf\u0baf \u0bb2\u0b95\u0bcd\u0ba9\u0ba4\u0bcd\u0ba4\u0bc8 \u0bb5\u0bc8\u0b95\u0bcd\u0b95\u0bb5\u0bc1\u0bae\u0bcd.",
    "pg.conn_2911": "2-9-11 \u0ba4\u0bca\u0b9f\u0bb0\u0bcd\u0baa\u0bc1",
    "pg.conn_lord": "\u0b85\u0ba4\u0bbf\u0baa\u0ba4\u0bbf",
    "pg.conn_pair": "\u0bb5\u0bc0\u0b9f\u0bc1\u0b95\u0bb3\u0bcd",
    "pg.conn_links": "\u0b8e\u0baa\u0bcd\u0baa\u0b9f\u0bbf \u0b87\u0ba3\u0bc8\u0b95\u0bbf\u0ba9\u0bcd\u0bb1\u0ba9",
    "pg.conn_status": "\u0ba8\u0bbf\u0bb2\u0bc8",
    "pg.conn_yes": "\u0ba4\u0bca\u0b9f\u0bb0\u0bcd\u0baa\u0bc1 \u0b89\u0ba3\u0bcd\u0b9f\u0bc1",
    "pg.conn_no": "\u0ba4\u0bca\u0b9f\u0bb0\u0bcd\u0baa\u0bc1 \u0b87\u0bb2\u0bcd\u0bb2\u0bc8",
    "pg.link_same_lord": "{planet} {a}, {b} \u0b87\u0bb0\u0ba3\u0bcd\u0b9f\u0bc1\u0b95\u0bcd\u0b95\u0bc1\u0bae\u0bcd \u0b85\u0ba4\u0bbf\u0baa\u0ba4\u0bbf",
    "pg.link_exchange": "\u0baa\u0bb0\u0bbf\u0bb5\u0bb0\u0bcd\u0ba4\u0bcd\u0ba4\u0ba9\u0bc8: {p1} ({a} \u0b85\u0ba4\u0bbf\u0baa\u0ba4\u0bbf), {p2} ({b} \u0b85\u0ba4\u0bbf\u0baa\u0ba4\u0bbf) \u0b92\u0bb0\u0bc1\u0bb5\u0bb0\u0bcd \u0bb5\u0bc0\u0b9f\u0bcd\u0b9f\u0bbf\u0bb2\u0bcd \u0bae\u0bb1\u0bcd\u0bb1\u0bb5\u0bb0\u0bcd",
    "pg.link_in": "{planet} ({a} \u0b85\u0ba4\u0bbf\u0baa\u0ba4\u0bbf) {b} \u0bb5\u0bc0\u0b9f\u0bcd\u0b9f\u0bbf\u0bb2\u0bcd",
    "pg.link_aspect_house": "{planet} ({a} \u0b85\u0ba4\u0bbf\u0baa\u0ba4\u0bbf) {b} \u0bb5\u0bc0\u0b9f\u0bcd\u0b9f\u0bc8\u0baa\u0bcd \u0baa\u0bbe\u0bb0\u0bcd\u0b95\u0bcd\u0b95\u0bbf\u0bb1\u0ba4\u0bc1 ({n} \u0baa\u0bbe\u0bb0\u0bcd\u0bb5\u0bc8)",
    "pg.link_aspect_lord": "{planet} ({a} \u0b85\u0ba4\u0bbf\u0baa\u0ba4\u0bbf) \u2192 {other} ({b} \u0b85\u0ba4\u0bbf\u0baa\u0ba4\u0bbf) \u0bae\u0bc0\u0ba4\u0bc1 {n} \u0baa\u0bbe\u0bb0\u0bcd\u0bb5\u0bc8",
    "pg.link_conj": "{p1} ({a} \u0b85\u0ba4\u0bbf\u0baa\u0ba4\u0bbf), {p2} ({b} \u0b85\u0ba4\u0bbf\u0baa\u0ba4\u0bbf) {sign} \u0bb0\u0bbe\u0b9a\u0bbf\u0baf\u0bbf\u0bb2\u0bcd \u0b9a\u0bc7\u0bb0\u0bcd\u0b95\u0bcd\u0b95\u0bc8",
    "pg.conn_2911_full": "\u0bae\u0bc2\u0ba9\u0bcd\u0bb1\u0bc1 \u0b9c\u0bcb\u0b9f\u0bbf\u0b95\u0bb3\u0bc1\u0bae\u0bcd \u0b87\u0ba3\u0bc8\u0ba8\u0bcd\u0ba4\u0bc1\u0bb3\u0bcd\u0bb3\u0ba9 - \u0bae\u0bc1\u0bb4\u0bc1\u0bae\u0bc8\u0baf\u0bbe\u0ba9 2-9-11 \u0ba4\u0bca\u0b9f\u0bb0\u0bcd\u0baa\u0bc1.",
    "pg.conn_2911_chain": "\u0bae\u0bc2\u0ba9\u0bcd\u0bb1\u0bbf\u0bb2\u0bcd \u0b87\u0bb0\u0ba3\u0bcd\u0b9f\u0bc1 \u0b9c\u0bcb\u0b9f\u0bbf\u0b95\u0bb3\u0bcd \u0b87\u0ba3\u0bc8\u0ba8\u0bcd\u0ba4\u0bc1\u0bb3\u0bcd\u0bb3\u0ba9; \u0b8e\u0ba9\u0bb5\u0bc7 2, 9, 11\u0b86\u0bae\u0bcd \u0bb5\u0bc0\u0b9f\u0bc1\u0b95\u0bb3\u0bcd \u0bae\u0bc2\u0ba9\u0bcd\u0bb1\u0bc1\u0bae\u0bcd \u0ba4\u0bca\u0b9f\u0bb0\u0bcd\u0baa\u0bbf\u0bb2\u0bcd \u0b89\u0bb3\u0bcd\u0bb3\u0ba9.",
    "pg.conn_2911_partial": "{a}, {b} \u0bb5\u0bc0\u0b9f\u0bc1\u0b95\u0bb3\u0bcd \u0bae\u0b9f\u0bcd\u0b9f\u0bc1\u0bae\u0bc7 \u0b87\u0ba3\u0bc8\u0ba8\u0bcd\u0ba4\u0bc1\u0bb3\u0bcd\u0bb3\u0ba9; \u0bae\u0bc2\u0ba9\u0bcd\u0bb1\u0bbe\u0bb5\u0ba4\u0bc1 \u0bb5\u0bc0\u0b9f\u0bc1 \u0ba4\u0ba9\u0bbf\u0ba4\u0bcd\u0ba4\u0bc1 \u0b89\u0bb3\u0bcd\u0bb3\u0ba4\u0bc1.",
    "pg.conn_2911_none": "2, 9, 11\u0b86\u0bae\u0bcd \u0bb5\u0bc0\u0b9f\u0bc1\u0b95\u0bb3\u0bc1\u0b95\u0bcd\u0b95\u0bc1 \u0b87\u0b9f\u0bc8\u0baf\u0bc7 \u0ba4\u0bca\u0b9f\u0bb0\u0bcd\u0baa\u0bc1 \u0b87\u0bb2\u0bcd\u0bb2\u0bc8.",
    "pg.conn_off_chart": "\u0b87\u0ba9\u0bcd\u0ba9\u0bc1\u0bae\u0bcd \u0b9c\u0bbe\u0ba4\u0b95\u0ba4\u0bcd\u0ba4\u0bbf\u0bb2\u0bcd \u0b87\u0bb2\u0bcd\u0bb2\u0bc8: {planets} - \u0b85\u0bb5\u0bb1\u0bcd\u0bb1\u0bbf\u0ba9\u0bcd \u0bb5\u0bb4\u0bbf\u0baf\u0bbe\u0ba9 \u0ba4\u0bca\u0b9f\u0bb0\u0bcd\u0baa\u0bc1\u0b95\u0bb3\u0bc8\u0b9a\u0bcd \u0b9a\u0bb0\u0bbf\u0baa\u0bbe\u0bb0\u0bcd\u0b95\u0bcd\u0b95 \u0bae\u0bc1\u0b9f\u0bbf\u0baf\u0bbe\u0ba4\u0bc1.",
    "pg.conn_2911_note": "\u0bb5\u0bc0\u0b9f\u0bc1\u0b95\u0bb3\u0bcd \u0bb2\u0b95\u0bcd\u0ba9\u0ba4\u0bcd\u0ba4\u0bbf\u0bb2\u0bbf\u0bb0\u0bc1\u0ba8\u0bcd\u0ba4\u0bc1 \u0b8e\u0ba3\u0bcd\u0ba3\u0baa\u0bcd\u0baa\u0b9f\u0bc1\u0b95\u0bbf\u0ba9\u0bcd\u0bb1\u0ba9. \u0b85\u0ba4\u0bbf\u0baa\u0ba4\u0bbf\u0b95\u0bb3\u0bcd \u0baa\u0bb0\u0bbf\u0bb5\u0bb0\u0bcd\u0ba4\u0bcd\u0ba4\u0ba9\u0bc8 \u0b9a\u0bc6\u0baf\u0bcd\u0ba4\u0bbe\u0bb2\u0bcb, \u0b92\u0bb0\u0bc1 \u0b85\u0ba4\u0bbf\u0baa\u0ba4\u0bbf \u0bae\u0bb1\u0bcd\u0bb1\u0bb5\u0bb0\u0bbf\u0ba9\u0bcd \u0bb5\u0bc0\u0b9f\u0bcd\u0b9f\u0bbf\u0bb2\u0bcd \u0b87\u0bb0\u0bc1\u0ba8\u0bcd\u0ba4\u0bbe\u0bb2\u0bcb \u0b85\u0ba4\u0bc8\u0baa\u0bcd \u0baa\u0bbe\u0bb0\u0bcd\u0ba4\u0bcd\u0ba4\u0bbe\u0bb2\u0bcb, \u0b92\u0bb0\u0bc1 \u0b85\u0ba4\u0bbf\u0baa\u0ba4\u0bbf \u0bae\u0bb1\u0bcd\u0bb1\u0bb5\u0bb0\u0bc8\u0baa\u0bcd \u0baa\u0bbe\u0bb0\u0bcd\u0ba4\u0bcd\u0ba4\u0bbe\u0bb2\u0bcb, \u0b85\u0ba4\u0bbf\u0baa\u0ba4\u0bbf\u0b95\u0bb3\u0bcd \u0b9a\u0bc7\u0bb0\u0bcd\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0bc1\u0ba8\u0bcd\u0ba4\u0bbe\u0bb2\u0bcb, \u0b85\u0bb2\u0bcd\u0bb2\u0ba4\u0bc1 \u0b92\u0bb0\u0bc7 \u0b95\u0bbf\u0bb0\u0b95\u0bae\u0bcd \u0b87\u0bb0\u0ba3\u0bcd\u0b9f\u0bc8\u0baf\u0bc1\u0bae\u0bcd \u0b86\u0ba3\u0bcd\u0b9f\u0bbe\u0bb2\u0bcb \u0b87\u0bb0\u0ba3\u0bcd\u0b9f\u0bc1 \u0bb5\u0bc0\u0b9f\u0bc1\u0b95\u0bb3\u0bc1\u0bae\u0bcd \u0b87\u0ba3\u0bc8\u0b95\u0bbf\u0ba9\u0bcd\u0bb1\u0ba9.",
    "pg.conn_subha": "8, 12\u0b86\u0bae\u0bcd \u0bb5\u0bc0\u0b9f\u0bc1\u0b95\u0bb3\u0bbf\u0bb2\u0bcd \u0b9a\u0bc1\u0baa\u0ba4\u0bcd\u0ba4\u0bc1\u0bb5\u0bae\u0bcd",
    "pg.conn_house": "\u0bb5\u0bc0\u0b9f\u0bc1",
    "pg.subha_from": "\u0b9a\u0bc1\u0baa\u0ba4\u0bcd\u0ba4\u0bc1\u0bb5\u0bae\u0bcd \u0ba4\u0bb0\u0bc1\u0bb5\u0ba4\u0bc1",
    "pg.subha_yes": "\u0b9a\u0bc1\u0baa\u0ba4\u0bcd\u0ba4\u0bc1\u0bb5\u0bae\u0bcd \u0b89\u0ba3\u0bcd\u0b9f\u0bc1",
    "pg.subha_none": "\u0b87\u0bb2\u0bcd\u0bb2\u0bc8",
    "pg.subha_in": "{planet} \u0bb5\u0bc0\u0b9f\u0bcd\u0b9f\u0bbf\u0bb2\u0bcd \u0b89\u0bb3\u0bcd\u0bb3\u0ba4\u0bc1",
    "pg.subha_aspect": "{planet} - {n} \u0baa\u0bbe\u0bb0\u0bcd\u0bb5\u0bc8",
    "pg.subha_both": "8, 12 \u0b87\u0bb0\u0ba3\u0bcd\u0b9f\u0bc1 \u0bb5\u0bc0\u0b9f\u0bc1\u0b95\u0bb3\u0bc1\u0b95\u0bcd\u0b95\u0bc1\u0bae\u0bcd \u0b9a\u0bc1\u0baa\u0ba4\u0bcd\u0ba4\u0bc1\u0bb5\u0bae\u0bcd \u0b89\u0ba3\u0bcd\u0b9f\u0bc1.",
    "pg.subha_only": "{n} \u0bb5\u0bc0\u0b9f\u0bcd\u0b9f\u0bbf\u0bb1\u0bcd\u0b95\u0bc1 \u0bae\u0b9f\u0bcd\u0b9f\u0bc1\u0bae\u0bcd \u0b9a\u0bc1\u0baa\u0ba4\u0bcd\u0ba4\u0bc1\u0bb5\u0bae\u0bcd \u0b89\u0ba3\u0bcd\u0b9f\u0bc1.",
    "pg.subha_neither": "8, 12 \u0b87\u0bb0\u0ba3\u0bcd\u0b9f\u0bc1 \u0bb5\u0bc0\u0b9f\u0bc1\u0b95\u0bb3\u0bc1\u0b95\u0bcd\u0b95\u0bc1\u0bae\u0bcd \u0b9a\u0bc1\u0baa\u0ba4\u0bcd\u0ba4\u0bc1\u0bb5\u0bae\u0bcd \u0b87\u0bb2\u0bcd\u0bb2\u0bc8.",
    "pg.subha_moon_yes": "\u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0ba9\u0bcd \u0b95\u0ba3\u0b95\u0bcd\u0b95\u0bbf\u0bb2\u0bcd \u0b89\u0ba3\u0bcd\u0b9f\u0bc1 - {phase}.",
    "pg.subha_moon_no": "\u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0ba9\u0bcd \u0b95\u0ba3\u0b95\u0bcd\u0b95\u0bbf\u0bb2\u0bcd \u0b87\u0bb2\u0bcd\u0bb2\u0bc8 - {phase}. \u0baa\u0bcc\u0bb0\u0bcd\u0ba3\u0bae\u0bbf \u0b85\u0bb2\u0bcd\u0bb2\u0ba4\u0bc1 7\u0b86\u0bae\u0bcd \u0ba4\u0bbf\u0ba4\u0bbf\u0b95\u0bcd\u0b95\u0bc1\u0baa\u0bcd \u0baa\u0bbf\u0ba9\u0bcd \u0bb5\u0bb3\u0bb0\u0bcd\u0baa\u0bbf\u0bb1\u0bc8\u0b9a\u0bcd \u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0ba9\u0bcd \u0bae\u0b9f\u0bcd\u0b9f\u0bc1\u0bae\u0bc7 \u0b9a\u0bc1\u0baa\u0ba4\u0bcd\u0ba4\u0bc1\u0bb5\u0bae\u0bcd \u0ba4\u0bb0\u0bc1\u0bae\u0bcd.",
    "pg.subha_moon_need_sun": "\u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0ba9\u0bcd \u0b95\u0ba3\u0b95\u0bcd\u0b95\u0bbf\u0bb2\u0bcd \u0b87\u0bb2\u0bcd\u0bb2\u0bc8 - \u0b85\u0ba4\u0ba9\u0bcd \u0b95\u0bb2\u0bc8\u0baf\u0bc8 \u0b85\u0bb1\u0bbf\u0baf \u0b9a\u0bc2\u0bb0\u0bbf\u0baf\u0ba9\u0bc8 \u0bb5\u0bc8\u0b95\u0bcd\u0b95\u0bb5\u0bc1\u0bae\u0bcd.",
    "pg.conn_subha_note": "\u0b95\u0bc1\u0bb0\u0bc1, \u0b9a\u0bc1\u0b95\u0bcd\u0b95\u0bbf\u0bb0\u0ba9\u0bcd, \u0b85\u0bb2\u0bcd\u0bb2\u0ba4\u0bc1 \u0baa\u0bcc\u0bb0\u0bcd\u0ba3\u0bae\u0bbf / 7\u0b86\u0bae\u0bcd \u0ba4\u0bbf\u0ba4\u0bbf\u0b95\u0bcd\u0b95\u0bc1\u0baa\u0bcd \u0baa\u0bbf\u0ba9\u0bcd \u0bb5\u0bb3\u0bb0\u0bcd\u0baa\u0bbf\u0bb1\u0bc8\u0b9a\u0bcd \u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0ba9\u0bcd \u0b92\u0bb0\u0bc1 \u0bb5\u0bc0\u0b9f\u0bcd\u0b9f\u0bbf\u0bb2\u0bcd \u0b87\u0bb0\u0bc1\u0ba8\u0bcd\u0ba4\u0bbe\u0bb2\u0bcb \u0b85\u0ba4\u0bc8\u0baa\u0bcd \u0baa\u0bbe\u0bb0\u0bcd\u0ba4\u0bcd\u0ba4\u0bbe\u0bb2\u0bcb \u0b85\u0ba8\u0bcd\u0ba4 \u0bb5\u0bc0\u0b9f\u0bcd\u0b9f\u0bbf\u0bb1\u0bcd\u0b95\u0bc1\u0b9a\u0bcd \u0b9a\u0bc1\u0baa\u0ba4\u0bcd\u0ba4\u0bc1\u0bb5\u0bae\u0bcd \u0b89\u0ba3\u0bcd\u0b9f\u0bc1. \u0bb0\u0bbe\u0b9a\u0bbf\u0b95\u0bb3\u0bc8\u0b95\u0bcd \u0b95\u0bca\u0ba3\u0bcd\u0b9f\u0bc1 \u0baa\u0bbe\u0bb0\u0bcd\u0b95\u0bcd\u0b95\u0bc1\u0bae\u0bcd\u0baa\u0bcb\u0ba4\u0bc1, \u0b85\u0ba8\u0bcd\u0ba4\u0b9a\u0bcd \u0b9a\u0ba8\u0bcd\u0ba4\u0bbf\u0bb0\u0ba9\u0bcd \u0b9a\u0bc2\u0bb0\u0bbf\u0baf\u0ba9\u0bbf\u0bb2\u0bbf\u0bb0\u0bc1\u0ba8\u0bcd\u0ba4\u0bc1 5 \u0b85\u0bb2\u0bcd\u0bb2\u0ba4\u0bc1 6\u0b86\u0bae\u0bcd \u0bb0\u0bbe\u0b9a\u0bbf (\u0bb5\u0bb3\u0bb0\u0bcd\u0baa\u0bbf\u0bb1\u0bc8) \u0b85\u0bb2\u0bcd\u0bb2\u0ba4\u0bc1 7\u0b86\u0bae\u0bcd \u0bb0\u0bbe\u0b9a\u0bbf (\u0baa\u0bcc\u0bb0\u0bcd\u0ba3\u0bae\u0bbf).",
    "pg.on_chart": "{planet} (\u0b9c\u0bbe\u0ba4\u0b95\u0ba4\u0bcd\u0ba4\u0bbf\u0bb2\u0bcd)",
}

UI = {"en": _EN, "ta": _TA}


# ---------------------------------------------------------------------------
# Server-side lookup helpers (the browser has its own copies in /i18n.js)
# ---------------------------------------------------------------------------

def t(key, lang=DEFAULT_LANGUAGE, **params):
    """Translated UI string for `key`, falling back to English then the key."""
    text = UI.get(lang, {}).get(key) or UI[DEFAULT_LANGUAGE].get(key) or key
    return text.format(**params) if params else text


def term(kind, key, lang=DEFAULT_LANGUAGE):
    """Translated vocabulary item, falling back to English then the key."""
    group = TERMS.get(kind, {})
    return group.get(lang, {}).get(key) or group.get(DEFAULT_LANGUAGE, {}).get(key) or key


def planet_abbr(label, lang=DEFAULT_LANGUAGE):
    """Chart-box abbreviation for a graha, e.g. "Su" / "சூ"."""
    return term("planet_abbr", label, lang)


def ordinal(n, lang=DEFAULT_LANGUAGE):
    """House ordinal - "3rd" in English, "3ஆம்" in Tamil (twin of I18N.ordinal)."""
    if lang == "ta":
        return f"{n}ஆம்"
    suffix = "th" if 11 <= n % 100 <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def ordinal_list(numbers, lang=DEFAULT_LANGUAGE):
    """"3rd, 7th" - twin of I18N.ordinalList."""
    return ", ".join(ordinal(n, lang) for n in numbers)


# Suffix appended to a retrograde planet's chart glyph - "(R)" in English,
# "(வ)" for வக்கிரம் in Tamil.
RETROGRADE_SUFFIX = {"en": "(R)", "ta": "(வ)"}


def missing_keys():
    """Keys present in English but absent from another language.

    Handy in a REPL when adding strings - `i18n.missing_keys()` should stay
    empty. Not used at runtime.
    """
    report = {}
    for lang in LANGUAGES:
        if lang == DEFAULT_LANGUAGE:
            continue
        missing = sorted(set(UI[DEFAULT_LANGUAGE]) - set(UI.get(lang, {})))
        for kind, group in TERMS.items():
            missing += [
                f"{kind}:{k}"
                for k in sorted(set(group[DEFAULT_LANGUAGE]) - set(group.get(lang, {})))
            ]
        if missing:
            report[lang] = missing
    return report
