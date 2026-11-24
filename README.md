# BMS Study Guide

Vendor-neutral study guides for Building Management Systems (BMS), built as a static website that works offline, prints cleanly and tracks progress in the browser.

**Level 1 – BMS Fundamentals** (4 weeks, 45–60 min a day): architecture, HVAC plant, sensors and field devices, DI/DO/AI/AO wiring, BACnet and Modbus, and control logic. One example unit, **AHU-01**, is followed through every module, and the five labs build its complete control package.

| Part | Content |
|---|---|
| 1. BMS Architecture | 6 pages |
| 2. HVAC Control Fundamentals | 7 pages |
| 3. Sensors and Field Devices | 8 pages |
| 4. Digital and Analog I/O | 6 pages |
| 5. BMS Communication Protocols | 5 pages |
| 6. BMS Control Logic | 6 pages |
| Practical labs | 5 labs with model answers (wiring diagram, point list + CSV, sequence, 4–20 mA loop, Modbus) |
| Reviews and tests | 3 weekly reviews, 6 module quizzes, 30-question final test |
| Reference | Glossary (all key terms + abbreviations) and a printable cheat sheet |
| Interactive tools | Analog scaling, NTC/PT1000, subnet checker, Modbus decoder, PID playground, AHU-01 sequence stepper |

Live site: https://leojai23.github.io/bms-study-guide/

## Open it

Open `index.html` in a browser. Everything works from the file system, including search. Offline caching (service worker) turns on when the site is served over http(s), for example with GitHub Pages or `python -m http.server`.

## Build

Pages are generated. Edit the content files, not the HTML.

```
python build-scripts/build.py
```

Plain Python 3, no packages to install. Re-run after any change; it rewrites every generated file.

## Layout

```
index.html                     home (generated)
level-1/                       all Level 1 pages, labs, reviews, glossary, cheat sheet (generated)
assets/css/site.css            all styling: light + dark themes, phone layout, print
assets/js/site.js              search, theme, menu, progress, quizzes, checklists, tooltips
assets/js/tools.js             the six interactive tools
assets/js/search-index.js      generated
assets/js/abbr-data.js         generated
sw.js                          offline cache list (generated)
build-scripts/
  build.py                     builds everything
  bms_common.py                page templates + helpers (tables, callouts, SVG diagrams, quizzes, tools)
  syllabus.py                  modules, page titles, labs, 4-week schedule
  content/m1.py … m6.py        module content: PAGES, MODULE_INTRO, QUIZ, FINAL
  content/labs.py              the five labs + the AHU-01 point list (single source for Labs 1–2 and the CSV)
  content/cheatsheet.py        cheat sheet
  content/ahu01.py             the AHU-01 example: schematic + device list
  content/abbreviations.py     abbreviation tooltips (also listed in the glossary)
```

## Editing content

Each topic page is one dictionary in `content/mN.py` with: `id`, `slug`, `title` (must match `syllabus.py`),
`objectives`, `one_line`, `why`, `body`, `ahu01`, `on_site`, `faults`, `terms`, `scenarios`, `questions`.
Each module also has `QUIZ` (module quiz) and `FINAL` (its five final-test questions), written with `mcq(...)`.
Diagrams are small Python functions that return inline SVG using the helpers in `bms_common.py`.
Interactive tools are placed with `tool("scale" | "rtd" | "subnet" | "modbus" | "pid" | "ahuseq", ...)`.

Weekly review pages, the glossary, search index, previous/next links and the offline cache are generated
automatically. Run the build after every change.

## Adding Level 2

Add a second syllabus (modules, schedule) and content folder following the same pattern, and a card on the
home page. The page templates are level-agnostic apart from the `LV` path prefix in `bms_common.py`.

## Adding vendor notes later

Each page dict accepts an optional `vendor_notes` list of `(vendor, html)` pairs. The section only appears when it has content, for example:

```python
vendor_notes=[("Brand X controllers", "<p>The run LED blinks once a second when the program is running.</p>")]
```

## Sources

General industry practice and open standards: ISO 16484 (building automation and control systems), ASHRAE 135 / ISO 16484-5 (BACnet), and the Modbus application protocol specification. On site, always follow the manufacturer's documentation, the project specification and local electrical regulations.
