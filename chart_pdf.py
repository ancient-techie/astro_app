"""
PDF export for the Vedic birth chart app.
----------------------------------------
Renders the same data the results page shows - birth details, Rashi (D1) and
Navamsa (D9) charts, the Dasha-Bhukti periods around today, and the
Nakshatra/pada table - into a printable A4 document.

The charts arrive as SVG markup from jyotichart; svglib turns each one into a
ReportLab drawing so they stay vector art in the PDF instead of a screenshot.

The export follows the page's language toggle. Tamil needs two things beyond
a font that carries the glyphs:

  * complex-script shaping - mark attachment (ு, ூ) and pre-base reordering
    (ெ, ே, ொ). ReportLab drives HarfBuzz for this when uharfbuzz is
    installed AND the paragraph style asks for it (shaping=1). Without both,
    "சூரியன்" prints as "சஉரியன ்", so _tamil_font() refuses Tamil and the
    document falls back to English rather than reading wrong.

  * a face that actually has the glyphs. Tamil MN and friends carry Latin
    too, but not "°" or "·" - see TAMIL_MISSING_SUBSTITUTES and _para().

    pip install reportlab svglib uharfbuzz
"""

import io
import os
import re
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfbase.ttfonts import TTFont, shapeStr
from reportlab.graphics.shapes import String
from reportlab.platypus import (
    KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

from svglib.svglib import svg2rlg

import i18n

# Print palette: the app's gold accent, darkened enough to stay legible on
# white paper, over near-black text rather than the screen theme's cream.
GOLD = colors.HexColor("#a8862a")
GOLD_SOFT = colors.HexColor("#f3ecd8")
INK = colors.HexColor("#1c1a2e")
MUTED = colors.HexColor("#6b687f")
RULE = colors.HexColor("#d8d3c2")

PAGE_SIZE = A4
MARGIN = 16 * mm
CONTENT_WIDTH = PAGE_SIZE[0] - 2 * MARGIN

# ReportLab lays out one glyph per code point unless it can hand the run to
# HarfBuzz, which it only does when uharfbuzz is importable. Ask ReportLab
# itself rather than importing uharfbuzz here - it is the one that has to do
# the shaping, and it decides at import time. getattr, not attribute access:
# ReportLab only grew this in 5.x, and on an older one the export should lose
# Tamil, not fail to import and take the whole app down with it.
SHAPING_AVAILABLE = getattr(ttfonts, "uharfbuzz", None) is not None

# Characters a Tamil face is unlikely to carry. Latin-only runs (dates,
# coordinates, "11°22.7'") are drawn in Helvetica instead, which has them;
# these cover the few that sit inside an otherwise Tamil sentence, where
# swapping the face would break shaping.
TAMIL_MISSING_SUBSTITUTES = {
    "·": "-",     # middle dot, used as a separator in the subtitle
    "°": " deg ",  # degree sign
    "→": "->",
    "–": "-",     # en dash, separating the two halves of a Dasha-Bhukti line
}

# Where to look for a Tamil-capable TrueType face, most specific first.
# .ttc collections are fine - TTFont takes a subfont index, and index 0 is
# the regular weight in every collection listed here. Note that "Tamil Sangam
# MN.ttc" is deliberately absent: macOS ships it with PostScript outlines,
# which ReportLab cannot embed ("postscript outlines are not supported").
TAMIL_FONT_CANDIDATES = [
    ("/System/Library/Fonts/Supplemental/Tamil MN.ttc", 0),
    ("/usr/share/fonts/truetype/noto/NotoSansTamil-Regular.ttf", 0),
    ("/usr/share/fonts/truetype/tamil/NotoSansTamil-Regular.ttf", 0),
    ("/usr/share/fonts/truetype/Lohit-Tamil.ttf", 0),
    ("/usr/share/fonts/truetype/lohit-tamil/Lohit-Tamil.ttf", 0),
    ("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 0),
]

TAMIL_FONT_NAME = "VedicTamil"

# None = not looked up yet; False = looked and found nothing.
_tamil_font_cache = None


def _tamil_font():
    """Register and return a Tamil-capable font name, or None if none exists.

    Returns None unless the font can also be *shaped*: an embedded Tamil face
    with no HarfBuzz behind it produces transposed text, which is worse than
    an English fallback.

    The lookup runs once per process; a miss is cached too, so a server
    without a Tamil font doesn't stat the same paths on every export.
    """
    global _tamil_font_cache
    if _tamil_font_cache is not None:
        return _tamil_font_cache or None

    if not SHAPING_AVAILABLE:
        _tamil_font_cache = False
        return None

    for path, index in TAMIL_FONT_CANDIDATES:
        if not os.path.exists(path):
            continue
        try:
            face = TTFont(TAMIL_FONT_NAME, path, subfontIndex=index)
            if not face.shapable:
                continue  # embeddable but unshapable - would print transposed
            pdfmetrics.registerFont(face)
        except Exception:
            continue  # unreadable or not a usable TTF - try the next candidate
        # One weight is enough: bold-facing a Tamil face by substitution
        # looks worse than letting the regular weight carry the headings.
        pdfmetrics.registerFontFamily(
            TAMIL_FONT_NAME,
            normal=TAMIL_FONT_NAME, bold=TAMIL_FONT_NAME,
            italic=TAMIL_FONT_NAME, boldItalic=TAMIL_FONT_NAME,
        )
        _tamil_font_cache = TAMIL_FONT_NAME
        return TAMIL_FONT_NAME

    _tamil_font_cache = False
    return None


def _styles(font=None, bold_font=None):
    """Paragraph styles for one export.

    Returns each role twice: "role" in the document's own face, and
    "role_latin" always in Helvetica. _para() picks between them per string,
    because a Tamil face has no "°" and Helvetica has no Tamil - see
    TAMIL_MISSING_SUBSTITUTES.
    """
    latin = _style_set("Helvetica", "Helvetica-Bold", shaping=0)
    if not font:
        # No Tamil in play: both halves are the same Helvetica styles.
        styles = dict(latin)
    else:
        # A Tamil run has no separate bold face, so both roles use the same
        # file; sizes and colours still separate the heading levels. shaping=1
        # is what routes the run through HarfBuzz - without it the marks and
        # pre-base vowels come out in code-point order, which reads wrong.
        styles = _style_set(font, bold_font or font, shaping=1)
    styles.update({f"{role}_latin": style for role, style in latin.items()})
    return styles


def _style_set(font, bold_font, shaping):
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "VTitle", parent=base["Title"], fontName=bold_font,
            fontSize=22, leading=26, textColor=INK, spaceAfter=2,
            shaping=shaping,
        ),
        "subtitle": ParagraphStyle(
            "VSubtitle", parent=base["Normal"], fontName=font,
            fontSize=9.5, leading=13, textColor=MUTED, alignment=TA_CENTER,
            shaping=shaping,
        ),
        "section": ParagraphStyle(
            "VSection", parent=base["Heading2"], fontName=bold_font,
            fontSize=12, leading=15, textColor=GOLD,
            spaceBefore=14, spaceAfter=6,
            shaping=shaping,
        ),
        "cell": ParagraphStyle(
            "VCell", parent=base["Normal"], fontName=font,
            fontSize=8.5, leading=11, textColor=INK,
            shaping=shaping,
        ),
        # Table cells hold Paragraphs, and a Paragraph carries its own colour -
        # a TEXTCOLOR table command can't reach inside it. So header and
        # highlighted rows need styles of their own.
        "cell_head": ParagraphStyle(
            "VCellHead", parent=base["Normal"], fontName=bold_font,
            fontSize=8.5, leading=11, textColor=colors.white,
            shaping=shaping,
        ),
        "cell_strong": ParagraphStyle(
            "VCellStrong", parent=base["Normal"], fontName=bold_font,
            fontSize=8.5, leading=11, textColor=INK,
            shaping=shaping,
        ),
        "chart_label": ParagraphStyle(
            "VChartLabel", parent=base["Normal"], fontName=bold_font,
            fontSize=9, leading=12, textColor=INK, alignment=TA_CENTER,
            spaceAfter=3,
            shaping=shaping,
        ),
        # One Dasha-Bhukti period reads as a headline and a dates line under
        # it. "period_current" is what replaces the highlighted table row -
        # gold and bold is the only thing separating today's period from the
        # rest, so it has to carry on its own.
        "period": ParagraphStyle(
            "VPeriod", parent=base["Normal"], fontName=font,
            fontSize=10, leading=13, textColor=INK, spaceBefore=7,
            shaping=shaping,
        ),
        "period_current": ParagraphStyle(
            "VPeriodCurrent", parent=base["Normal"], fontName=bold_font,
            fontSize=10, leading=13, textColor=GOLD, spaceBefore=7,
            shaping=shaping,
        ),
        "period_meta": ParagraphStyle(
            "VPeriodMeta", parent=base["Normal"], fontName=font,
            fontSize=8.5, leading=11, textColor=MUTED, leftIndent=12,
            spaceBefore=1,
            shaping=shaping,
        ),
        # The houses each lord of a period activates, one line per lord under
        # the period's dates.
        "period_houses": ParagraphStyle(
            "VPeriodHouses", parent=base["Normal"], fontName=font,
            fontSize=8, leading=10.5, textColor=INK, leftIndent=12,
            spaceBefore=1,
            shaping=shaping,
        ),
        "subsection": ParagraphStyle(
            "VSubsection", parent=base["Normal"], fontName=bold_font,
            fontSize=10, leading=13, textColor=INK,
            spaceBefore=12, spaceAfter=5,
            shaping=shaping,
        ),
        "note": ParagraphStyle(
            "VNote", parent=base["Normal"],
            fontName=font if font != "Helvetica" else "Helvetica-Oblique",
            fontSize=7.5, leading=10, textColor=MUTED, spaceBefore=4,
            shaping=shaping,
        ),
    }


# jyotichart sets its type through CSS classes in an SVG <style> block, and
# svglib doesn't read those - it only looks at presentation attributes, so
# every label silently falls back to Helvetica and Tamil comes out as .notdef
# boxes. Writing font-family onto each <text> element is what svglib does
# read, and the style block's size/weight still apply everywhere else.
_SVG_TEXT_TAG_RE = re.compile(r"<text\b(?![^>]*\bfont-family=)")


def _apply_svg_font(svg_markup, font):
    return _SVG_TEXT_TAG_RE.sub(f'<text font-family="{font}"', svg_markup)


def _shape_drawing_text(node, font):
    """Pre-shape the Tamil labels inside a chart drawing.

    The graphics canvas draws String objects straight through drawString,
    which only shapes when rlbidi is installed - so the planet abbreviations
    would come out unshaped ("சூ" as "ச" + a loose "ூ") even though the
    surrounding tables are fine. A ShapedStr carries its own HarfBuzz output
    and is honoured wherever it lands, so shape the text here instead of
    relying on the drawing path to do it.
    """
    for item in getattr(node, "contents", ()):
        if isinstance(item, String):
            if _has_tamil(item.text):
                item.fontName = font
                item.text = shapeStr(item.text, font, item.fontSize)
        else:
            _shape_drawing_text(item, font)


def _svg_drawing(svg_markup, max_width, max_height=None, font=None):
    """Turn one chart's SVG markup into a ReportLab drawing scaled to fit."""
    drawing = svg2rlg(io.BytesIO(svg_markup.encode("utf-8")))
    if drawing is None or not drawing.width or not drawing.height:
        return None

    if font:
        _shape_drawing_text(drawing, font)

    scale = max_width / drawing.width
    if max_height:
        scale = min(scale, max_height / drawing.height)

    drawing.scale(scale, scale)
    drawing.width *= scale
    drawing.height *= scale
    return drawing


def _section(styles, text):
    """A gold section heading with a hairline rule under it."""
    rule = Table([[""]], colWidths=[CONTENT_WIDTH], rowHeights=[1])
    rule.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.8, GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return [_para(styles, text, "section"), rule, Spacer(1, 6)]


def _details_block(styles, form, ascendant, navamsa_ascendant, lang):
    """Birth details as two side-by-side label/value columns."""
    place = form.get("city") or "-"
    coords = f"{form.get('lat', '')}, {form.get('lng', '')}".strip(", ")
    sign = lambda name: i18n.term("sign", name, lang) if name else "-"

    left = [
        (i18n.t("form.dob", lang), form.get("date") or "-"),
        (i18n.t("form.tob", lang), form.get("time") or "-"),
        (i18n.t("form.city", lang), place),
    ]
    right = [
        (i18n.t("pdf.coordinates", lang), coords or "-"),
        (i18n.t("form.tz", lang), form.get("tz") or "-"),
        (i18n.t("pdf.ayanamsa", lang), i18n.t("pdf.ayanamsa_value", lang)),
    ]

    rows = []
    for (l_label, l_value), (r_label, r_value) in zip(left, right):
        rows.append([
            _para(styles, l_label, bold=True),
            _para(styles, l_value),
            _para(styles, r_label, bold=True),
            _para(styles, r_value),
        ])
    rows.append([
        _para(styles, i18n.t('pdf.rashi_asc', lang), bold=True),
        _para(styles, sign(ascendant)),
        _para(styles, i18n.t('pdf.navamsa_asc', lang), bold=True),
        _para(styles, sign(navamsa_ascendant)),
    ])

    label_w = CONTENT_WIDTH * 0.20
    value_w = CONTENT_WIDTH * 0.30
    table = Table(rows, colWidths=[label_w, value_w, label_w, value_w])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GOLD_SOFT),
        ("BOX", (0, 0), (-1, -1), 0.6, RULE),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def _charts_block(styles, charts, lang, font=None):
    """Charts two to a row, each under its own label.

    Each row is its own table rather than one tall grid, so a four-chart
    export (style "both") can break between the D1 and D9 pairs instead of
    shunting a whole half-empty row onto the next page.

    `charts` entries carry one SVG per language (see app.build_chart_context);
    this picks the one matching `lang` and falls back to the first available.
    """
    if not charts:
        return []

    per_row = 2 if len(charts) > 1 else 1
    cell_width = CONTENT_WIDTH / per_row

    cells = []
    for card in charts:
        svgs = dict(card["svgs"])
        svg = svgs.get(lang) or next(iter(svgs.values()), None)
        if svg is None:
            continue
        if font:
            svg = _apply_svg_font(svg, font)
        drawing = _svg_drawing(svg, cell_width - 12, max_height=78 * mm, font=font)
        if drawing is None:
            continue
        label = i18n.t(card["label_key"], lang)
        cells.append([_para(styles, label, "chart_label"), drawing])

    flowables = []
    for i in range(0, len(cells), per_row):
        row = cells[i:i + per_row]
        while len(row) < per_row:          # pad a trailing odd chart
            row.append("")
        table = Table([row], colWidths=[cell_width] * per_row, hAlign="LEFT")
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        flowables.append(table)
    return flowables


def _table_style():
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("BOX", (0, 0), (-1, -1), 0.6, RULE),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, RULE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, GOLD_SOFT]),
    ])


def _star_block(styles, star_table, lang):
    """Planet / sign / degree / nakshatra / pada / lord."""
    header = [
        i18n.t(key, lang) for key in
        ("th.planet", "th.sign", "th.degree", "th.nakshatra", "th.pada", "th.nak_lord")
    ]
    rows = [[_para(styles, h, "cell_head") for h in header]]

    for row in star_table:
        # The web table marks combust planets with a fire emoji, which the
        # standard PDF fonts can't draw - spell it out instead.
        name = i18n.term("planet", row["planet"], lang)
        if row.get("combust"):
            name = f"{name} ({i18n.t('pdf.combust', lang)})"
        rows.append([
            _para(styles, name),
            _para(styles, i18n.term("sign", row["sign"], lang)),
            _para(styles, row["degree"]),
            _para(styles, i18n.term("nakshatra", row["nakshatra"], lang)),
            _para(styles, row["pada"]),
            _para(styles, i18n.term("planet", row["lord"], lang)),
        ])

    widths = [w * CONTENT_WIDTH for w in (0.22, 0.15, 0.13, 0.22, 0.08, 0.20)]
    table = Table(rows, colWidths=widths, repeatRows=1)
    table.setStyle(_table_style())
    return table


def _house_clauses(info, lang):
    """The houses one dasha lord activates, e.g. "Lord of 2nd, 7th =
    Placement - 5th = Aspects - 11th".

    Same wording as renderPlanetBlock on the results page, built from the
    same app.build_dasha_house_map() entry, so the PDF and the Houses
    Involved box never disagree.
    """
    if not info:
        return i18n.t("houses.no_data", lang)

    placement = i18n.ordinal(info["placement"], lang)

    if info["type"] == "classical":
        return " = ".join([
            f"{i18n.t('phrase.lord_of', lang)} {i18n.ordinal_list(info['lordship'], lang)}",
            f"{i18n.t('phrase.placement', lang)} - {placement}",
            f"{i18n.t('phrase.aspects', lang)} - {i18n.ordinal_list(info['aspects'], lang)}",
        ])

    # Rahu/Ketu have no lordship or aspects of their own, so they are read
    # through the planets connected to them: "2nd, 7th (Venus); 5th (Sun)".
    def connections(role):
        return "; ".join(
            f"{i18n.ordinal_list(c['houses'], lang)} ({i18n.term('planet', c['planet'], lang)})"
            for c in info["connections"] if role in c["roles"]
        )

    dispositor = next((c for c in info["connections"] if "dispositor" in c["roles"]), None)
    if dispositor:
        clauses = [
            f"{i18n.t('phrase.dispositor', lang)} ({i18n.term('planet', dispositor['planet'], lang)})"
            f" {i18n.t('phrase.of', lang)} {i18n.ordinal_list(dispositor['houses'], lang)}"
        ]
    else:
        clauses = [i18n.t("phrase.dispositor_none", lang)]
    clauses.append(
        f"{i18n.t('phrase.placement', lang)} - {placement} {i18n.t('phrase.house', lang)}"
        f" ({i18n.term('sign', info['sign'], lang)})"
    )
    if connections("conjunct"):
        clauses.append(f"{i18n.t('phrase.conjunct', lang)} - {connections('conjunct')}")
    clauses.append(
        f"{i18n.t('phrase.aspected_by', lang)} - "
        f"{connections('aspecting') or i18n.t('phrase.none', lang)}"
    )
    return " = ".join(clauses)


def _houses_line(styles, label, house_map, lang):
    """"Venus = Lord of 2nd, 7th = ..." as one indented paragraph."""
    text = f"{i18n.term('planet', label, lang)} = {_house_clauses(house_map.get(label), lang)}"
    return _para(styles, text, "period_houses")


def _bhukti_lines(styles, bhukti_window, lang, house_map=None):
    """Previous / current / upcoming Dasha-Bhukti periods, as prose lines.

    A six-column grid of planet names and ISO dates reads like a spreadsheet
    row you have to match back to its header. Spelling each period out
    instead - "Current - Venus Mahadasha - Sun Antardasha", its dates on a
    quieter line below - carries the same six fields but can be read straight
    through, which is what someone does with four periods rather than forty.
    Under the dates, one line per lord gives the houses it activates.

    Returns bare Paragraphs, not KeepTogether groups: build_chart_pdf already
    wraps the whole section in one, and KeepTogether reports a sentinel height
    rather than a real one, so nesting them makes the outer group think it can
    never fit and break to a fresh page before every export.
    """
    maha_label = i18n.term("dasha_level", "Mahadasha", lang)
    antar_label = i18n.term("dasha_level", "Antardasha", lang)
    years_unit = i18n.t("pdf.years_unit", lang)

    flowables = []
    for p in bhukti_window:
        headline = i18n.t(
            "pdf.bhukti_line", lang,
            role=i18n.term("period_role", p["role"], lang),
            maha=i18n.term("planet", p["maha"], lang), maha_label=maha_label,
            antar=i18n.term("planet", p["antar"], lang), antar_label=antar_label,
        )
        dates = i18n.t(
            "pdf.bhukti_dates", lang,
            start=p["start"], end=p["end"],
            years=p["years"], years_unit=years_unit,
        )
        role = "period_current" if p["role"] == "Current" else "period"
        flowables.append(_para(styles, headline, role))
        flowables.append(_para(styles, dates, "period_meta"))
        if house_map:
            flowables.append(_houses_line(styles, p["maha"], house_map, lang))
            flowables.append(_houses_line(styles, p["antar"], house_map, lang))
    return flowables


def _antaram_block(styles, period, lang, house_map=None):
    """The next level down: the current Bhukti's nine Pratyantardasha
    (Antaram) periods, each with the houses its lord activates.

    Nine rows is where a table does read better than prose, so this one is
    a grid; the row running today is outlined in gold. Returns bare
    flowables for the caller to group - see _bhukti_lines on nesting.
    """
    level = i18n.term("dasha_level", "Pratyantardasha", lang)
    heading = i18n.t(
        "pdf.antaram_heading", lang, level=level,
        maha=i18n.term("planet", period["maha"], lang),
        maha_label=i18n.term("dasha_level", "Mahadasha", lang),
        antar=i18n.term("planet", period["antar"], lang),
        antar_label=i18n.term("dasha_level", "Antardasha", lang),
    )

    # The heading already names the level, so the first column is just
    # "Lord" - "Pratyantardasha" is too long to fit it without wrapping.
    header = [i18n.t(key, lang) for key in ("th.lord", "th.start", "th.end", "phrase.houses")]
    rows = [[_para(styles, h, "cell_head") for h in header]]
    current_row = None
    for i, sub in enumerate(period["antaram"], start=1):
        cell_role = "cell_strong" if sub["is_current"] else "cell"
        if sub["is_current"]:
            current_row = i
        rows.append([
            _para(styles, i18n.term("planet", sub["lord"], lang), cell_role),
            _para(styles, sub["start"], cell_role),
            _para(styles, sub["end"], cell_role),
            _para(styles, _house_clauses((house_map or {}).get(sub["lord"]), lang)),
        ])

    widths = [w * CONTENT_WIDTH for w in (0.15, 0.14, 0.14, 0.57)]
    table = Table(rows, colWidths=widths, repeatRows=1)
    style = _table_style()
    if current_row is not None:
        style.add("BOX", (0, current_row), (-1, current_row), 1.4, GOLD)
    table.setStyle(style)

    flowables = [_para(styles, heading, "subsection"), table]
    if current_row is not None:
        flowables.append(_para(
            styles,
            i18n.t("pdf.antaram_note", lang, level=level,
                   date=datetime.now().strftime("%d %b %Y")),
            "note",
        ))
    return flowables


def _esc(value):
    """Escape for ReportLab's mini-HTML paragraph markup."""
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _has_tamil(text):
    return any("஀" <= ch <= "௿" for ch in text)


def _substitute_missing(text):
    """Swap out the characters a Tamil face doesn't carry."""
    for missing, replacement in TAMIL_MISSING_SUBSTITUTES.items():
        text = text.replace(missing, replacement)
    return text


def _para(styles, text, role="cell", bold=False):
    """One Paragraph, drawn in whichever face can actually render it.

    A Tamil face carries Latin as well, so mixed strings ("Jane Doe - வேத
    ஜாதகம்") stay on it and keep their shaping. Latin-only strings go to
    Helvetica instead, which is both better looking for figures and the only
    one of the two with a degree sign - that is what keeps "11°22.7'" intact.
    """
    text = str(text)
    if _has_tamil(text):
        text = _substitute_missing(text)
    else:
        role = f"{role}_latin"

    markup = _esc(text)
    if bold:
        markup = f"<b>{markup}</b>"
    return Paragraph(markup, styles[role])


def _page_furniture(canvas, doc, name, lang, font):
    """Gold rule at the top of every page, credit line and page number below."""
    canvas.saveState()
    width, height = PAGE_SIZE

    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.2)
    canvas.line(MARGIN, height - MARGIN + 6, width - MARGIN, height - MARGIN + 6)

    size = 7.5
    canvas.setFont(font or "Helvetica", size)
    canvas.setFillColor(MUTED)

    # drawString's own shaping=True path needs rlbidi, which we don't require;
    # handing it text that is already shaped works with uharfbuzz alone.
    def shaped(text):
        if font and _has_tamil(text):
            return shapeStr(_substitute_missing(text), font, size)
        return text

    canvas.drawString(
        MARGIN, MARGIN - 14, shaped(f"{name} - {i18n.t('app.title', lang)}"),
    )
    canvas.drawRightString(
        width - MARGIN, MARGIN - 14,
        shaped(f"{i18n.t('pdf.page', lang)} {canvas.getPageNumber()}"),
    )
    canvas.restoreState()


def build_chart_pdf(form, ctx, lang=i18n.DEFAULT_LANGUAGE):
    """Render the chart context to PDF bytes.

    `form` is the submitted birth-details dict; `ctx` is what
    app.build_chart_context() returns; `lang` follows the page's toggle.

    Tamil falls back to English when _tamil_font() can't supply a face that
    is both embeddable and shapable - see the note above it.
    """
    font = _tamil_font() if lang == "ta" else None
    if lang == "ta" and font is None:
        lang = i18n.DEFAULT_LANGUAGE

    name = form.get("name") or "Chart"
    styles = _styles(font)
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=PAGE_SIZE,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title=f"{name} - {i18n.t('app.title', lang)}",
        author="Vedic Birth Chart",
        subject="Sidereal (Lahiri) natal chart",
    )

    story = [
        _para(styles, name, "title"),
        _para(styles, i18n.t("pdf.subtitle", lang), "subtitle"),
        Spacer(1, 12),
    ]

    story += _section(styles, i18n.t("pdf.birth_details", lang))
    story.append(_details_block(
        styles, form, ctx.get("ascendant"), ctx.get("navamsa_ascendant"), lang,
    ))

    chart_flowables = _charts_block(styles, ctx.get("charts") or [], lang, font)
    if chart_flowables:
        story += _section(styles, i18n.t("pdf.charts_heading", lang))
        story += chart_flowables
        story.append(_para(styles, i18n.t("chart.retro_hint", lang), "note"))

    # Dasha-Bhukti sits between the charts and the Nakshatra table: it is the
    # part most people read after looking at the charts, and as prose lines it
    # is short enough to follow them on the same page.
    bhukti_window = ctx.get("bhukti_window") or []
    house_map = ctx.get("dasha_house_map") or {}
    if bhukti_window:
        block = _section(styles, i18n.t("pdf.bhukti_heading", lang))
        block += _bhukti_lines(styles, bhukti_window, lang, house_map)
        block.append(_para(
            styles,
            i18n.t("pdf.bhukti_note", lang,
                   date=datetime.now().strftime("%d %b %Y")),
            "note",
        ))
        if house_map:
            block.append(_para(styles, i18n.t("pdf.houses_note", lang), "note"))
        story.append(KeepTogether(block))

        # A separate group rather than part of the one above: together they
        # can run past a page, and KeepTogether would then push both to a
        # fresh page and leave a gap under the charts.
        current = next((p for p in bhukti_window if p.get("antaram")), None)
        if current:
            story.append(KeepTogether(_antaram_block(styles, current, lang, house_map)))

    star_table = ctx.get("star_table") or []
    if star_table:
        block = _section(styles, i18n.t("section.star", lang))
        block.append(_star_block(styles, star_table, lang))
        story.append(KeepTogether(block))

    story.append(Spacer(1, 14))
    story.append(_para(
        styles,
        i18n.t("pdf.generated", lang,
               timestamp=datetime.now().strftime("%d %b %Y, %H:%M")),
        "note",
    ))

    def on_page(canvas, doc_):
        _page_furniture(canvas, doc_, name, lang, font)

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return buffer.getvalue()
