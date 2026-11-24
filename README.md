# BMS Study Guide

Vendor-neutral study guides for Building Management Systems (BMS), built as a static website that works offline, prints cleanly and tracks progress in the browser.

**Level 1 – BMS Fundamentals** (4 weeks, 45–60 min a day): architecture, HVAC plant, sensors and field devices, DI/DO/AI/AO wiring, BACnet and Modbus, and control logic. One example unit, **AHU-01**, is followed through every module, and the five labs build its complete control package.

| Module | Status |
|---|---|
| 1. BMS Architecture | ✅ 6 pages |
| 2. HVAC Control Fundamentals | planned |
| 3. Sensors and Field Devices | planned |
| 4. Digital and Analog I/O | planned |
| 5. BMS Communication Protocols | planned |
| 6. BMS Control Logic | planned |
| Labs, planner, glossary | planned |

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
level-1/                       Level 1 pages (generated)
assets/css/site.css            all styling, light + dark themes, print
assets/js/site.js              search, theme, menu, progress, quizzes, tooltips
assets/js/search-index.js      generated
assets/js/abbr-data.js         generated
sw.js                          offline cache list (generated)
build-scripts/
  build.py                     builds everything
  bms_common.py                page templates + helpers (tables, callouts, SVG diagrams)
  syllabus.py                  modules, page titles, labs, 4-week schedule
  content/m1.py                Module 1 content (one dict per page)
  content/ahu01.py             the AHU-01 example: schematic + device list
  content/abbreviations.py     abbreviation tooltips (and later the glossary)
```

## Adding a module

1. Write `build-scripts/content/mN.py` with a `PAGES` list. Copy the shape of a page in `m1.py`: `id`, `slug`, `title`, `objectives`, `one_line`, `why`, `body`, `ahu01`, `on_site`, `faults`, `terms`, `scenarios`, `questions`. Use the `id` and `slug` from `syllabus.py`.
2. Add `import mN` and `N: mN` to `CONTENT` in `build.py`.
3. Run the build. Pages missing content show as "soon" automatically.

## Adding vendor notes later

Each page dict accepts an optional `vendor_notes` list of `(vendor, html)` pairs. The section only appears when it has content, for example:

```python
vendor_notes=[("Brand X controllers", "<p>The run LED blinks once a second when the program is running.</p>")]
```

## Sources

General industry practice and open standards: ISO 16484 (building automation and control systems), ASHRAE 135 / ISO 16484-5 (BACnet), and the Modbus application protocol specification. On site, always follow the manufacturer's documentation, the project specification and local electrical regulations.
