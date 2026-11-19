# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

A sidereal (Lahiri) Vedic astrology web app: one Flask process, no build step, no
test suite. Pages are Jinja templates held as Python strings inside `app.py` —
except the client-side slabs, which live as their own files and are read at
import: `chart_playground.html`, `strength_panel.html`, and the three shell
parts `ui_theme.html`, `ui_shell.html`, `ui_icons.html`.
Every user-facing string is bilingual (English / Tamil).

Two libraries do the heavy lifting: **Kerykeion** (planetary positions via Swiss
Ephemeris) and **jyotichart** (pure-Python SVG chart renderer). Neither computes
Nakshatra, Vimshottari Dasha, Navamsa, or any divisional chart — all of that is
written by hand in `app.py`.

---

## Environment

**Only `/opt/anaconda3/bin/python3` has the dependencies installed.** Plain
`python3`, Homebrew, and `/usr/local` Pythons all fail with
`ModuleNotFoundError: No module named 'jyotichart'`. Always use the absolute path:

```bash
/opt/anaconda3/bin/python3 app.py          # serves on 127.0.0.1:5050
```

`playwright` is installed in that same interpreter, with Chromium already
downloaded — it is the only way to exercise the page's JavaScript.

`ADMIN_PASSWORD` and `SECRET_KEY` are read from the environment; unset means an
insecure default plus a startup warning (harmless in dev). `DATABASE_URL`
(`db.py`) selects Postgres over the local SQLite file.

---

## File map

| File | Lines | Role |
|---|---|---|
| `app.py` | ~5.7k | Everything: astrology math, all HTML/CSS/JS templates, all routes |
| `strength_panel.html` | ~3.6k | The Strength (Balam) tab, injected into the results page |
| `chart_playground.html` | ~2.8k | A standalone page; served verbatim by `/play-with-chart` |
| `sky_simulation.html` | ~1.3k | The other standalone page: the geocentric sky simulation, served verbatim by `/sky` |
| `dasha_clock.html` | ~910 | The Dasha Clock overlay, injected into the results page |
| `ui_theme.html` | ~880 | The design layer: tokens, graha colours, light theme, mobile shell, injected at the end of every `<head>` |
| `ui_shell.html` | ~460 | The shell's chrome and behaviour: menu, bottom tabs, saved charts, city type-ahead, theme switch; injected at the end of every `<body>` |
| `ui_icons.html` | ~90 | The stroked icon sprite, injected at the top of every `<body>` |
| `i18n.py` | ~1.8k | `TERMS` (vocabulary inside data) + `UI` (fixed labels), en/ta |
| `chart_pdf.py` | ~750 | ReportLab A4 export of the results page |
| `porutham.py` | ~620 | The ten Tamil marriage-compatibility checks (pure lookups, no ephemeris) |
| `jathagam.py` | ~344 | Chart-level marriage checks that need a full horoscope |
| `vargas.py` | ~180 | The sixteen divisional charts' rules (D1–D60), Parashara; pure, no ephemeris |
| `varga_chakra.html` | ~420 | The Varga Chakra page (`/varga-chakra`): all sixteen vargas, picker + table |
| `db.py` | ~137 | SQLAlchemy storage for saved birth details |
| `muhurtham.py` | ~310 | Muhurtham rules (vivaham / griha pravesham / vahana): tables + window judging; pure, no ephemeris |
| `muhurtham.html` | ~650 | The Muhurtham finder page (`/muhurtham`): best three dates + a calendar of reasons |

`app.py` reads these HTML files at **import time**: `chart_playground.html`
(`PLAYGROUND_HTML`), `strength_panel.html` (`STRENGTH_PANEL_HTML`),
`dasha_clock.html` (`DASHA_CLOCK_HTML`), `varga_chakra.html` (`VARGA_CHAKRA_HTML`) and `sky_simulation.html`
(`SKY_SIM_HTML`), plus the shell parts described below where they exist.
`python app.py` runs with the reloader, but it only watches `.py` files — editing
any of those pages needs a manual restart. An `app.py` edit happens to
restart it too, but do not rely on that.

The three shell parts are injected into **both** `PAGE_TEMPLATE` and
`PORUTHAM_TEMPLATE`, at fixed points: `{{ ui_theme | safe }}` right after the
page's own `</style>` (so every rule in it wins), `{{ ui_icons | safe }}`
immediately inside `<body>` (the `<symbol>`s the `<use href="#i-…">`
references resolve against), and `{{ ui_shell | safe }}` just before
`</body>`. `ui_shell.html` is defensive about what exists — the same file
serves the empty form, the results page and the porutham page.

`local.db` is tracked and holds real saved records. Anything that exercises
`/save` writes to it, so check `git status` before assuming a diff is yours.

---

## Navigating `app.py`

Line numbers drift as you edit — **grep the anchor** when one looks wrong.

### Python half (1 – 1750)

| ≈Line | Anchor to grep | What |
|---|---|---|
| 163 | `# Progressive Web App` | manifest, **service worker**, generated icons |
| 295 | `# /i18n.js - the shared` | `I18N_RUNTIME_JS`, the browser-side translation runtime |
| 596 | `PLAYGROUND_HTML = _f.read()` | the playground file, read at import |
| 605 | `STRENGTH_PANEL_HTML = _f.read()` | the Strength panel file, read at import |
| 639 | `# Astrology helpers` | `SIGN_ORDER`, `PLANETS`, `build_vedic_subject`, `house_from_signs` |
| 714 | `def build_rashi_positions` | `{code: sign}` map — feeds both the playground URL and the Strength tab |
| ~735 | `PLANET_COLORS` | one colour per graha; the source of truth for the chart glyphs, the `--pl-*` tokens in `ui_theme.html` and the Strength panel's series |
| ~760 | `def _apply_chart_palette` | writes the navy/gold palette straight onto `chartcfg` (South and North spell the same settings differently in `updatechartcfg`, so the dict keys are used instead) |
| ~800 | `def _style_chart_svg` | rewrites the finished SVG: bigger type, hairline rules, and the retrograde `℞` split into its own muted `<tspan>` |
| 750 | `def _localize_chart_svg` | swaps the English captions jyotichart writes into its own SVG, then calls `_style_chart_svg` on **both** paths |
| 793 | `def _add_chart_planets` | places 9 grahas on a chart object, each in its `PLANET_COLORS` hue; **shared by every renderer** |
| 856 | `# Gochar (transit) chart` | `render_reference_chart_svg`, `render_gochar_pair_svgs`, `build_gochar_context` |
| 1036 | `# Divisional (varga) charts` | `chart_longitudes`, `build_varga_positions`, `render_varga_chart_svg`; D9 is a thin wrapper |
| 1122 | `# Nakshatra (star)` | `nakshatra_details`, `build_star_table`, combustion |
| 1212 | `# "Houses Involved"` | `RULERSHIP`, `ASPECT_OFFSETS`, `build_dasha_house_map` |
| 1316 | `# 3-7-11 connection` | `build_marriage_links` |
| 1422 | `# Conjunctions` | by-orb and by-sign grouping |
| 1610 | `# Vimshottari Mahadasha` | `build_dasha_table`, `build_sub_periods`, `build_antardashas` |

### Templates (1755 – 5240)

| ≈Line | Anchor | What |
|---|---|---|
| 1755 | `PAGE_TEMPLATE = """` | the main generator + results page |
| 1777–2669 | `<style>` | all of that page's CSS |
| 2686 | `<form class="card form-card` | the birth-details form (collapsible once a chart exists) |
| 2782 | `class="result-tabs"` | the Chart / Strength tab bar |
| 2978 | `data-pane="strength"` | where `{{ strength_panel \| safe }}` is injected |
| 2800+ | `<div class="section-title">` | results sections, in page order |
| 2985–3700 | `const DASHA_ORDER = [` | the dasha / houses / marriage / gochar IIFE |
| 3710–4090 | — | second `<script>`: form collapse, results tabs, geocoding, save, PWA install |
| 4107 | `PORUTHAM_TEMPLATE` | the 10-porutham page |
| 5109 | `ADMIN_LOGIN_TEMPLATE` | admin pages |

### Inside the big IIFE (2984 – 3700)

Function declarations are hoisted, so definition order does not constrain call
order. Grep these banners:

- `// ── 3-7-11 (marriage) box` — `currentChain`, `marriageChecks`, `upcomingMatches`
- `// ── Gochar (transit) panel + popup` — `gocharDefaultDate`, `gocharPanelHTML`, `gocharModalHTML`, `fetchGochar`
- `tbody.addEventListener("click"` — the single row-click handler feeding all five boxes
- `function chainAt(` (~3120) — the lords running on **any** date, memoised.
  `currentChain(today)` is now a thin wrapper. Three things are exposed to the
  Strength panel from here (~3147): `window.strengthChainAt` and
  `window.strengthChainsAt`, which is how its slider walks the dasa → bhukti →
  antara, and `window.strengthFullSpan`, the whole Vimshottari run, which is
  the slider's widest setting.

Shared helpers near the top: `planet()`, `sign()`, `ordinal()`, `isoDate()`,
`addDays()`, `computeSubPeriods()` (the JS twin of `build_sub_periods`).

### Routes (all near the end)

`index` · `build_chart_context` · `generate` · `gochar` · `varga_chakra_page` · `varga` · `transit_positions` ·
`download_pdf` · `porutham_page` · `places` · `geocode` · `admin_*`

`/places?q=` is the birth-city type-ahead: geopy for the candidates,
`timezonefinder` (via `_tz_at`) for each one's IANA zone. Because a suggestion
carries its coordinates **and** its timezone, picking one fills all three
fields — which is what let latitude, longitude and timezone move into a
closed `<details class="advanced">`. `/geocode` still exists and now returns
`tz` as well.

`build_chart_context(form)` assembles everything the results page and the PDF
both need — start there for any change to what the page displays.

`/transit-positions` is the Strength tab's data source: same birth payload as
`/gochar`, but signs only, no SVGs. `build_vedic_subject` costs ~0.7 ms, so one
request returns the exact scrubbed date **and** up to 366 sampled dates across a
period (`_TRANSIT_MAX_SAMPLES`, ~5464). Read its `transit_time` from its own
field, never the payload's `time` — that one is the *birth* time.

---

## Divisional charts (vargas)

`vargas.py` holds every division rule, each written the way BPHS states it
(start sign by odd/even, movable/fixed/dual or element), with Hora and
Trimsamsa as their own tables. All sixteen match PyJHora's *Parashara*
methods, which are JHora's defaults **except D2**: JHora defaults to PVR's
parivritti Hora, this app uses the classical Simha/Kataka one. D60 counts from
the sign itself.

The results page shows D1 and D9 only. Its "Varga Chakra" button re-posts
the birth details (like the PDF button) to `POST /varga-chakra`, a page of its
own (`varga_chakra.html`, opened in a new tab). That route fills two JSON
placeholders - `__VARGA_BIRTH__` and `__VARGA_TABLE__`, every point's rasi in
all sixteen vargas - and the page draws charts one varga at a time from
`POST /varga` (`{...birth payload, d}`), cached for the visit. A render is
~2 ms, so drawing on demand is about page weight (4 SVGs a varga), not speed.
A GET has no birth details and shows the page's own empty state.

`navamsa_sign` used to floor `deg // (30/9)`, which put exact part boundaries
(10.000°, 20.000°…) one part early; `varga_index` computes `deg * n / 30`.
Real longitudes never land on a boundary, and the D1/D9 SVGs were verified
byte-identical across the change.

## Muhurtham finder

`/muhurtham` (GET, or POST from the results page's "Muhurtham" button,
which re-posts the birth details like Varga Chakra does; the route reduces
them to the janma nakshatra and Moon rasi and fills `__MU_JANMA__`). The
page asks `POST /muhurtham-data` `{event, start, end, lat, lng, tz,
janma: {nakshatra 0..26, rasi 0..11}}` - at most 92 days. The star is
optional; without it tara bala and chandrashtamam are skipped and the page
says so.

The days come from `panchang.compute` (~6 ms each, `SWE_LOCK` taken per day
so a long search never holds up a chart); **all the judgement is in
`muhurtham.py`**, as tables at its top (`EVENTS`, `REJECT_TITHIS`,
`REJECT_YOGAS`, `HARSH_YOGAS`, tara and chandra sets, `SCORE`). Change a
tradition there, not in the logic. The unit is a **window**: daylight cut at
every limb edge, with the three kalams removed, neighbours that judge alike
joined, under 48 minutes dropped. Reasons are `{key, tone, terms, params}` -
`terms` are `[kind, key]` pairs the page passes through `I18N.term` before
`I18N.t(key)`, so every reason needs an `mu.r.*` string in both languages.
Not yet checked: lagna shuddhi, Guru/Shukra moudyam, both partners' stars.

## Navigating `strength_panel.html`

The Strength (Balam) tab. Injected into `PAGE_TEMPLATE` as
`{{ strength_panel | safe }}` — **Jinja does not re-parse the value of a
variable**, so this file's `${...}` template literals and braces arrive intact.
That is the whole reason it is a separate file: it escapes the three-layer
problem below entirely.

| ≈Line | What |
|---|---|
| 20–573 | `<style>`, scoped under `#strengthPanel` |
| 575 | `<template id="strengthPanelTpl">` — one chart panel |
| 675 | `<div id="strengthPanel">` — slider, spark chart, compare table, panels |
| 709+ | `<script>` |
| 1043 | `createStrengthChart` — the copied chart factory |
| 2912 | `computeDrikBala` — the only new astrology in the file |
| 2989+ | `STRENGTH PANEL ORCHESTRATION` — the IIFE that drives everything |
| 3086 | `pureStrength` — Stana 40% + (Dig+Nisa)/2 25% + Drik 35%, no Subathuva |
| 3190 | `CHAIN_WEIGHTS` — Mahadasa ×8, Bhukti ×4, Antara ×2, Sookshma ×1, others ×0.5 |
| 3255 | `renderSparkline` — both the per-graha and combined views |
| 3027 | `sliderScope` / `spanOf` — how far the slider reaches |

**The slider has two reaches** (`sliderScope`, and `spanOf()` / `applySpan()`).
`full` — the default — spans the whole Vimshottari run via
`window.strengthFullSpan`, so dragging crosses from one Mahadasa into the next.
`period` narrows to the tapped row, for picking a date inside one bhukti.
Tapping a dasha row narrows automatically; the boot call passes `fromTap=false`
so the page opens on the whole run. **The span drives the slider, the date
input and the curve together** — otherwise the marker could sit outside the
line it marks.

**It is a copy.** The scoring engine and chart factory were lifted from
`chart_playground.html`, which stays **byte-identical** — assert that
(`len(/play-with-chart) == 162805`) after touching either file. Keeping the copy
close to the original is deliberate so the two still diff cleanly.

Consequences worth knowing:

- **The dignity tables now live in four places**: `chart_playground.html`
  (~645), `strength_panel.html` (~773), `sky_simulation.html` (grep `graha bala`)
  and `jathagam.py:54-61`. A fix to one needs the other three.
- `build_rashi_positions(subject)` is the bridge — it already returns exactly
  the `{code: sign}` map the engine consumes, for a transit subject as much as a
  natal one. **No new position code was needed, and none should be added.**
- **Transits are scored in the natal frame by overriding `Asc`** in the
  placements map with the natal Lagna (or natal Moon) sign. The engine derives
  every house as `((signIdx - ascSIdx + 12) % 12) + 1`, so that one substitution
  reframes the whole chart with no engine change.
- The combined curve weights each graha by the seat it holds **on that sampled
  day**, not by one fixed chain — otherwise the whole line would jump every time
  the slider moved.

---

## Navigating `sky_simulation.html`

The sky simulation — `/sky`, linked from the app bar. The one feature in the
app that has nothing to do with a chart: graha longitudes are geocentric, so
they read the same from anywhere on earth, and the page asks the reader for
nothing. Nine grahas run at their own gati around a sidereal rasi wheel, with
vakri loops, asta and Chandra's paksha visible as they happen.

**The server is the only ephemeris.** `POST /sky-positions` (`app.py`, grep
`# Sky simulation ephemeris`) returns evenly spaced frames of
`{graha: [longitude, degrees-a-day]}`, read straight from Swiss Ephemeris
(`_sky_frames`) with exactly Kerykeion's settings - its `sweph` files, Lahiri,
`FLG_SWIEPH|FLG_SPEED|FLG_SIDEREAL`, the true node. A full Kerykeion subject
per frame made a window take ~6 s on Render and froze the wheel;
`_sky_frame_kerykeion` is kept as the reference to compare against (they agree
to 0.00004°). Kerykeion gives both the position **and** the speed, which is the
whole trick: a position and a tangent at each sample let the page join two
samples with a cubic Hermite, so motion is smooth between frames and a vakri
station lands where it belongs instead of being rounded to the nearest sample.
The response also carries `COMBUSTION_ORBS` and `NAKSHATRA_NAMES` so neither
table is copied into JS — `app.py` stays the only place either lives.

It is POST, not GET, so the service worker never touches it: the page asks for
a new window every few seconds of running and none of those URLs is worth a
cache entry.

| ≈Line | Anchor to grep | What |
|---|---|---|
| 66 | `<style>` | chrome follows the theme, the wheel stays night in both |
| 505 | `var CX = 520` | the wheel's geometry: ring radii, `GRAHAS`, `PATH_DAYS` |
| 595 | `function buildDefs` | the standing parts — sectors, ticks, rasi labels, rings, earth |
| 706 | `var node = {}` | the nine SVG graha nodes |
| 744 | `var rows = {}` | the readout table |
| 839 | `function histSpec` | how far back and how finely the history reaches |
| 850 | `stepMinutesFor` | the running window's spacing, by pace |
| 980 | `function sampleFrom` | the cubic Hermite |
| 1037 | `function drawTrails` | the paths |
| ~1140 | `the light in the rasis` | the light mix, ported from the playground |
| 1087 | `moonPhasePath` | the paksha |
| 1108 | `function render` | one instant onto the wheel, and the table |
| 1232 | `── transport` | the buttons, then the loop |

Things worth knowing before changing it:

- **Two windows, both replaced rather than patched.** The *running* window is
  fine-grained (5 min to 12 h a frame, chosen by the pace) and a few seconds of
  playback long; the *history* window is coarse (1 to 20 days a frame) and a
  year to twenty years long, and exists only so a path can reach back far
  enough to show a vakri loop. Either is replaced wholesale when the playhead
  nears its edge, and the old one keeps drawing until the new one lands, so
  nothing stalls mid-run.
- **The paths are read back out of those windows every frame, never
  accumulated.** An earlier version traced points as the clock ran; it drew the
  same path differently depending on whether you ran to a moment or jumped to
  it, and its fixed point budget eventually evicted the history. Sampling
  afresh costs ~900 Hermite evaluations a frame and is worth it.
- **A stretch of path is painted vakri because the ephemeris said so** — each
  sampled point carries its own gati. Inferring direction from the difference
  between two drawn points looks equivalent and is not: the two windows unwrap
  longitude from different starting points, and a seam between them reads as
  one enormous step backwards.
- A path spirals inward as it ages (`TRAIL_DEPTH`), which is what keeps a vakri
  loop legible instead of drawing over itself.
- **The sector wedges are addressable** (`<path class="sky-sector"
  data-sign="Aries">`), and the light mix is painted into `#sky-fx` above them.
- Aries 0° is at the top and the rasis run clockwise.

### Two modes

`Simulation` is everything above. `Snapshot` (`setMode`, grep `modes:`) holds
the same wheel still at a wall-clock moment in a place - default Chennai,
13.0827 N 80.2707 E, Asia/Kolkata. `POST /sky-snapshot` turns date + time + tz
into the UTC instant and returns the Lagna for lat/lng; the page then simply
`jumpTo`s that instant, so every layer, the table and the bala read it as they
read a running sky. The place adds the Lagna spoke and bhava numbers
(`drawLagna`). Place lookup is `/geocode` (lat/lng only - there is no
coordinates-to-timezone lookup, so the zone is picked by hand).

**`SWE_LOCK` (app.py) guards every Swiss Ephemeris call.** Kerykeion ends each
subject with `swe.close()`, which resets the process-wide sidereal mode to
Fagan-Bradley - 0.88 deg off Lahiri. Without the lock, a chart built on one
thread while `_sky_frames` ran on another shifted every graha in that window by
exactly that much (5 of 6 snapshots, before the fix). Anything new that calls
`swisseph` directly must take it.

### Graha bala

The box beside the wheel (toggle `tgBala`): subha, papa and sthana bala for
the nine, live. `computePlanetScores`, `getStanaBala`, `hasNeechaBhanga` and the
Moon-kendra gain are **lifted whole from the playground**, in its short codes,
so the same rasis score identically on both pages - verified over 20,000
random skies. Two things are this page's own: Rahu and Ketu hold the sthana
bala of their rasi's lord (read where that lord stands), and bars run on fixed
scales (300 / 300 / 100) so one only moves when its own graha's lot changes.
Scores count whole rasis, Chandra's paksha included, so `renderBala` only
recomputes when a graha changes rasi; the paksha percentage in the text is the
true elongation.

**Dig bala** is the playground's `getDigBala`, a fourth bar. It needs a Lagna:
a snapshot uses the server's; the simulation works one out live in the page
(`lagnaAt` - sidereal time and the ecliptic at the place's latitude, less the
Lahiri `ayanamsa` that `/sky-positions` now returns), because a Lagna changes
rasi every couple of hours - far too fast to fetch. It agrees with Kerykeion's
first house to 0.011 deg over 1850-2350 and latitudes to 60 deg. The place is
the snapshot's (Chennai until changed). Rahu and Ketu have no dig bala - the
playground gives them none - though they still hold their lord's sthana bala.

The controls and toggles sit in `.sky-dock`, sticky at the top.

### The light mix

Each rasi is washed with the light of the grahas standing in it and the grahas
aspecting it, added together. **The rules are the playground's, lifted whole**
(`chart_playground.html`, grep `ASPECT RULES` and `updateCellColors`), because
the same sky must not read differently on the kattam and on the wheel:

- `aspectOffsets` is the playground's `getAspectOffsets` - Sani `[1,3,7,10]`,
  Guru `[1,5,7,9]`, Sevvai `[1,4,7,8]`, Surya/Sukra/Budha `[1,7]`, Rahu/Ketu
  `[1]`, Chandra `[1,7]` or `[1,6,7,8]` at 6/7/8 signs from Surya, `[1]` dark.
  Offset 1 is the graha's own rasi, which is how a conjunction lights a rasi
  twice over without any separate rule.
- The `mix` values on `GRAHAS` are the playground's `PLANET_BASE[...].mix`.
  **A colour changed in one belongs changed in the other** - that is now a
  fourth place the two pages have to agree, alongside the dignity tables.
- Chandra's colour is the playground's dark-to-light ramp over its paksha.

Two deliberate differences, both because this page knows more than a kattam
does:

- **Phase is read off the true elongation**, not rounded to whole signs. It is
  the same formula - the playground's 1..13 sign count, evaluated continuously
  - but the drawn crescent and the light it throws would otherwise disagree on
  screen.
- The contributions are **added as light** (summed, then capped on the
  brightest channel so the hue of the mixture survives) rather than stacked as
  translucent layers. The alpha still follows the playground's stack,
  `1 - (1 - 0.62)^n`, so two grahas on a rasi read as two.

Everything is behind toggles: the mix itself, Chandra's kendras, the aspect
rays, a strength slider, and one chip a graha for whose light is counted.
`renderLight` is gated on a signature (every graha's rasi, Chandra's
brightness, the controls) so it only runs when something changed; `drawRays`
is not, because a ray starts at the graha and the graha is always moving.

To check a change to it, compute the expected mix independently from the rules
above and compare against the rendered gradients - `gradLight0..11`, whose
middle stop carries the colour and the alpha. Allow a unit per channel: the
page rounds with `Math.round`, which is not Python's `round`.

## The shell: theme, chrome, icons

Three files carry everything the pages share above the level of one page's
own content. They are separate files for the same reason
`chart_playground.html` is — Jinja never re-parses a variable's value, so a
media query can hold a brace and a template literal can hold `${}` without a
thought.

- **`ui_theme.html`** — one `<style>`, injected last, so it wins. It holds
  the design tokens (`--pl-sun` … `--pl-ketu` matching `PLANET_COLORS`;
  `--font-display` / `--font-ui`; the `--fs-*` size scale, which steps up
  ~1.1× under `html[data-lang="ta"]` and switches to Noto Sans Tamil), the
  light theme under `html[data-theme="light"]`, and the mobile shell
  (drawer, bottom tab bar, saved-charts sheet, graha cards, six result tabs,
  splash and busy overlays).
- **`ui_shell.html`** — the drawer, bottom tab bar, saved-charts sheet and
  busy overlay markup, plus one IIFE holding all of their behaviour. It
  exposes `window.openSavedCharts(handler)`, `window.saveChartLocally(entry)`,
  `window.savedChartCount()`, `window.wirePlaceField(...)` and
  `window.showBusy()` for the page scripts to use.
- **`ui_icons.html`** — a hidden `<svg>` of `<symbol>`s, used as
  `<svg class="ico"><use href="#i-menu"/></svg>`. The nav used to be
  labelled with emoji, which every platform draws differently.

**Typography rule:** Cinzel (`--font-display`) is for page and section
titles only. Labels, buttons, tables and badges are `--font-ui`. A rule in
the page's own CSS that sets Cinzel on a small element is overridden by the
long selector list at the top of `ui_theme.html` — if you add such an
element, add it to that list rather than fighting it locally. Watch
specificity: `.meta-pill.pdf-btn` (0,2,0) beats a bare `.meta-pill`.

**Themes.** `LANG_BOOT_SCRIPT` stamps `data-theme` on `<html>` before the
first paint, so there is no flash of the wrong one; **dark is the default**
and "auto" is a choice in the menu, not the fallback. The charts stay navy
in both themes: a rasi chart is a drawing and should look like itself
wherever it is read.

**Browser state** lives entirely in `localStorage`, never on the server:
`vedic-chart-lang`, `vedic-theme`, `vedic-form-collapsed`,
`vedic-saved-charts` (the family's charts — re-opened by re-POSTing to
`/generate`, the same stateless path a typed one takes) and
`vedic-install-dismissed`.

---

## The three-layer string problem

`PAGE_TEMPLATE` is a **non-raw Python string** holding **Jinja** holding
**HTML/CSS/JS**. Every edit passes through all three. The traps:

- **Python eats backslash escapes.** `\U0001F525` in the source becomes 🔥 in the
  output; `›` becomes ›. To emit a literal backslash to the browser (a JS
  regex, say), double it: `/\\{(\\w+)\\}/g` in source → `/\{(\w+)\}/g` in JS.
- **Jinja owns `{{`, `{%`, `{#`.** JS template literals (`${...}`) are fine, but
  never let two braces touch: write `Object.assign({}, x)` — never `{{`.
- **`| tojson`** is the safe way to hand server data to JS
  (`<script id="gocharBirthData" type="application/json">{{ form | tojson }}</script>`).
  Larger blobs use `json.dumps` in the route plus `| safe`.
- **The escape hatch:** a big slab of client-side HTML/CSS/JS belongs in its own
  file, read at import and injected with `| safe`, exactly as
  `chart_playground.html` and `strength_panel.html` are. Jinja does not re-parse
  a variable's value, so none of the traps above apply inside such a file. Pay
  the manual-restart cost instead of the escaping cost.

After any edit inside a template, syntax-check both layers:

```bash
/opt/anaconda3/bin/python3 -c "import ast,io; ast.parse(io.open('app.py',encoding='utf-8').read())"
```

and extract the inline `<script>` blocks to `node --check` them (see below).

---

## i18n contract

Adding any user-visible string means adding a key to **both** `_EN` and `_TA` in
`i18n.py`. Enforce with:

```bash
/opt/anaconda3/bin/python3 -c "import i18n; print(i18n.missing_keys())"   # must print {}
```

`i18n.py` is edited most reliably by script with `\uXXXX` escapes rather than by
pasting Tamil text — but **match what is already in the file**: existing values
contain real `–`, `→` and Tamil characters, so an `old` string written with
`\\u2013` will not match. Use a single backslash so Python decodes it first.

Two dictionaries, different purposes:

- `TERMS[kind][lang][key]` — vocabulary that appears *inside data*: `planet`,
  `planet_abbr` (chart glyphs), `sign`, `nakshatra`, `dasha_level`, plus the
  playground's own `pg_planet`, `pg_planet_abbr`, `stana_label`, `dig_info`.
- `UI[lang][key]` — fixed labels. `{name}` placeholders work on both sides
  (`i18n.t(key, lang, **params)` / `I18N.t(key, params)`).

Both ship to the browser whole via `/i18n.js`. In markup:

| Attribute | Effect |
|---|---|
| `data-i18n="key"` | `textContent = t(key)` |
| `data-i18n-html="key"` | `innerHTML = t(key)` (value contains markup) |
| `data-i18n-attr="aria-label:key"` | `setAttribute`; semicolon-separated pairs |
| `data-i18n-term="planet:Sun"` | `textContent = term(kind, value)` |
| `data-i18n-ordinal="3"` | "3rd" / "3ஆம்" |

`I18N.apply(root)` re-translates a subtree; `I18N.onChange(fn)` fires on a
language switch. **Text built with interpolated values must be rebuilt by hand
in an `onChange` handler** — `apply()` would overwrite it with the raw template.

Charts are rendered once per language and both copies are sent, with CSS showing
the live one (`.chart-svg[data-lang-svg]`). That makes the toggle instant.

**Write in the domain's vocabulary, not the tool's.** The Strength tab says
*bala*, *dasa*, *gochar*, *rasi*, *sthana*, *drishti*, *subha/papa*, *graha* —
not "plotted", "sampled", "curve", "aliased", "axis". Match that in new strings.

**`/i18n.js` is served network-first by the service worker** (`# Progressive Web
App`, ~163). It used to be cache-first, which meant a stale copy could outlive
the strings it held and every unknown key rendered as its own raw name
(`st.spark_title` on screen instead of the label). If you ever see raw keys in a
browser, that is the cause — not a missing translation. Check the server first:

```bash
/opt/anaconda3/bin/python3 -c "import app; print('KEY' in app.I18N_JS)"
```

Note `I18N_JS` is built **once at import**, so mutating `i18n.UI` at runtime
does not change what `/i18n.js` serves. Bump `CACHE_NAME` when changing anything
else in `SHELL_URLS`.

---

## Verifying a change

There is no test suite. These are the checks worth running.

**Routes still answer** — the fastest broad smoke test:

```bash
/opt/anaconda3/bin/python3 - <<'EOF'
import app as A
c = A.app.test_client()
form = {"name":"T","city":"Mumbai","date":"1990-05-12","time":"10:30",
        "lat":"19.0760","lng":"72.8777","tz":"Asia/Kolkata","style":"both"}
for name, r in [("/", c.get("/")), ("/generate", c.post("/generate", data=form)),
                ("/download-pdf", c.post("/download-pdf", data=dict(form, lang="ta"))),
                ("/porutham", c.get("/porutham")), ("/i18n.js", c.get("/i18n.js")),
                ("/play-with-chart", c.get("/play-with-chart")),
                ("/transit-positions", c.post("/transit-positions", json=dict(form,
                    period_start="2026-01-01", period_end="2026-12-31",
                    exact_date="2026-06-15", timeline=True)))]:
    print(name, r.status_code, len(r.get_data()))
EOF
```

**Nothing scrolls sideways.** The app bar used to measure 445px on a 369px
screen. Assert it in any Playwright run, at 369px and again after switching
to Tamil:

```python
assert pg.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 1")
```

**The sky simulation still answers.** `/sky` is a static page, but
`/sky-positions` is not — check a window comes back, and that it still agrees
with the app's own tables for the same instant (signs, nakshatra, pada,
retrograde and combustion all have a second source in `build_star_table`):

```python
frame = c.post("/sky-positions", json={"start": "2026-10-10T12:00",
                                       "step_minutes": 60, "count": 1}).get_json()["frames"][0]
# the same instant as a Mumbai chart at 17:30 IST
subj = A.build_vedic_subject("X", 2026, 10, 10, 17, 30, 19.076, 72.8777, "Asia/Kolkata", "Mumbai")
star = {r["planet"]: r for r in A.build_star_table(subj)}
assert star["Venus"]["nakshatra"] == A.nakshatra_details(frame["Venus"][0])["name"]
```

Worth driving with Playwright after any change to it: let it run, assert the
nine grahas actually moved, hold and confirm they stop, step by a year and
back, scrub the date field, walk every pace forward and in reverse, flip all
four toggles, switch language, and check at 369px. A cheap invariant that
catches a broken path: the Sun, Chandra and (usually) Sevvai must have an
**empty** vakri path, and Rahu and Ketu must have an empty margi one.

**The playground is untouched.** Anything that edits `strength_panel.html` or
the light mix in `sky_simulation.html` must
leave `/play-with-chart` byte-identical — a single assertion catches a stray
edit to the original:

```python
assert len(c.get("/play-with-chart").get_data()) == 162805
```

**No raw i18n keys reached the page.** Cheap, and catches a key added to the
markup but not to `i18n.py`:

```python
raw = pg.evaluate(r'''() => (document.body.innerText.match(/\b(st|pg|form)\.[a-z_]+\b/g) || [])''')
assert not raw, raw
```

**Charts did not silently change.** Any edit touching `_add_chart_planets`,
`_localize_chart_svg`, `_style_chart_svg`, `_apply_chart_palette` or a renderer
should leave the natal charts byte-identical unless you meant otherwise.
Hash them before and after (`git stash` or a `git show HEAD:app.py` copy in a temp
dir gives the "before"):

```python
import hashlib, tempfile, app as A
s = A.build_vedic_subject("T", 1990, 5, 12, 10, 30, 19.076, 72.8777, "Asia/Kolkata", "Mumbai")
with tempfile.TemporaryDirectory() as d:
    for style in ("south", "north"):
        for lang in ("en", "ta"):
            _, svg = A.render_chart_svg(s, style, d, lang)
            print(style, lang, hashlib.sha256(svg.encode()).hexdigest()[:16])
```

**JavaScript actually runs.** Nothing in the page's JS is exercised by a route
test. Start the server on a spare port, then drive it with Playwright — fill the
form, submit, assert on the rendered DOM, and collect `pageerror` / `console`
errors, which is what catches a broken template literal:

```python
pg.on("pageerror", lambda e: errs.append(str(e)))
pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
```

To syntax-check the inline scripts without a browser, regex the `<script>` blocks
out of a rendered `/generate` response into files and `node --check` each.

Chart-affecting maths should also be spot-checked against the page's own tables —
e.g. every graha's rendered box against its row in the positions table. The
Strength tab has its own cross-checks worth repeating: every sign from
`/transit-positions` must match the `/gochar` rows for the same date, and every
house shown must match `house_from_signs`.

Worth driving with Playwright after any Strength-tab change: switch to the tab,
tap a dasha row, expand to Sookshma, drag the slider (the breadcrumb should walk
the dasa → bhukti → antara), flip Lagna/Chandra, tick and untick grahas, switch
to the Combined view, switch language, and drag a planet on a chart.

---

## Conventions worth keeping

- **Stateless pages.** Nothing lives in the session. The PDF button re-POSTs the
  birth details; the gochar popup posts a server-rendered `{{ form | tojson }}`
  blob rather than reading the form inputs, so editing the form without pressing
  Generate cannot desync a result from the chart on screen.
- **jyotichart reports failure by returning a string**, not by raising. Check for
  `"Success"`, or a bad draw surfaces later as a missing-file error.
- Its South and North classes are **not symmetric**: `SouthChart` writes caption
  text into the SVG (`Chart : Lagna`, translated by `_localize_chart_svg`) that
  `NorthChart` omits entirely. Anything that must be visible in both styles
  belongs in the surrounding HTML, not the chart. The same asymmetry runs deeper
  in the unused `*TransitChart` classes — only the South one has
  `set_transit_details` — so `hasattr`-guard any call if you reach for them.
- **The birth form collapses** once a chart exists, so results get the full
  width. State lives in `localStorage["vedic-form-collapsed"]`; the summary line
  is built from the **live inputs**, not the server's values, because it
  describes the form rather than the result.
- **Chart glyphs cannot simply be made bigger.** jyotichart lays out up to
  nine planets per house at fixed coordinates roughly 30px apart, tuned for
  its own 14px type; past about 16px they write over each other. The centre
  caption is the exception — it has a 235×156 box to itself. The other half
  of making a chart readable on a phone is in `ui_theme.html`, where a chart
  card cancels the page gutter and the drawing is simply rendered wider.
- **The retrograde `℞` is a `<tspan>`,** so it can be painted a quieter
  colour than the glyph it follows. svglib has no tspan support, so
  `chart_pdf._flatten_svg_tspans` folds it back in before the PDF is drawn.
- **`SIGN_NAME_MAP` misspells Sagittarius** (`"Saggitarius"`). That is baked into
  the app's data; `SIGN_NAME_FULL` is the corrected variant used only by the
  playground page. Do not "fix" the former.
- Comments here explain **why**, not what. Match that.

---

## Note

`~/.codex/` exists on this machine (it contains a `skills/` directory). If you
want its user-level items available in Claude Code, reply `/import` to scan and
list what is importable, then `/import --yes=<digest>` to apply. If `/import` is
not available on this surface, run `claude import` from a terminal.
