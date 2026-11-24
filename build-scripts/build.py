# -*- coding: utf-8 -*-
"""Builds the whole BMS Study Guide site from build-scripts/content/*.

    python build-scripts/build.py

Writes: index.html, level-1/**, assets/js/search-index.js, assets/js/abbr-data.js, sw.js.
Safe to re-run at any time; every generated file is overwritten."""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "content"))

import syllabus as S                     # noqa: E402
import bms_common as C                   # noqa: E402
import ahu01                             # noqa: E402
from abbreviations import ABBR           # noqa: E402
import m1                                # noqa: E402

CONTENT = {1: m1}                        # add m2..m6 here as they are written
LV = C.LV
WRITTEN = []


def write(rel, text):
    path = os.path.join(C.REPO, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    WRITTEN.append(rel)


def strip(s):
    return re.sub(r"<[^>]+>", "", s)


# --------------------------------------------------------------------------
# Collect pages
# --------------------------------------------------------------------------

def collect():
    pages = []          # ordered (module, page) for every page with content
    for m in S.MODULES:
        mod = CONTENT.get(m["num"])
        if not mod:
            continue
        by_id = {p["id"]: p for p in mod.PAGES}
        for pid, slug, title in m["pages"]:
            p = by_id.get(pid)
            if p:
                assert p["slug"] == slug, f"slug mismatch for {pid}"
                p.setdefault("title", title)
                pages.append((m, p))
    return pages


def warmups_for(pages, k):
    """One question from each of the three previous pages (rotating which one)."""
    out = []
    for back in (1, 2, 3):
        j = k - back
        if j < 0:
            break
        _m, p = pages[j]
        qs = p["questions"]
        q, a = qs[(k + back) % len(qs)]
        out.append((q, a, f'{p["id"].replace("-", ".")} {p["title"]}'))
    return out


# --------------------------------------------------------------------------
# Level overview and home
# --------------------------------------------------------------------------

def item_link(root, iid, built_map):
    if iid in built_map:
        url, title = built_map[iid]
        return f'<a data-progress-id="{iid}" href="{root}{url}">{iid.replace("-", ".")} {title}</a>'
    for m in S.MODULES:
        for pid, _s, title in m["pages"]:
            if pid == iid:
                return f'<span class="soon">{pid.replace("-", ".")} {title}</span>'
    for lid, _s, title in S.LABS:
        if lid == iid:
            return f'<span class="soon">{title}</span>'
    return f'<span class="soon">{S.REVIEWS.get(iid, iid)}</span>'


def level_index(built, built_map):
    url = f"{LV}/index.html"
    root = C.depth_root(url)
    all_ids = ",".join(sorted(built))

    mod_cards = []
    for m in S.MODULES:
        ids = [p[0] for p in m["pages"] if p[0] in built]
        weeks = sorted({w for w, _f, days in S.WEEKS for d in days for i in d if i.split("-")[0] == str(m["num"])})
        wk = "Week " + "–".join(str(w) for w in (weeks[0], weeks[-1])) if weeks and weeks[0] != weeks[-1] else (f"Week {weeks[0]}" if weeks else "")
        if ids:
            mod_cards.append(
                f'<a class="mcard" href="{root}{C.module_url(m["num"])}"><span class="k">Module {m["num"]} · {wk}</span>'
                f'<h3>{m["title"]}</h3><p>{m["blurb"]}</p>'
                f'<div class="foot progress" data-progress-of="{",".join(ids)}"><div class="bar"><i></i></div><span class="plabel"></span></div></a>')
        else:
            mod_cards.append(
                f'<div class="mcard soon"><span class="k">Module {m["num"]} · {wk}</span><h3>{m["title"]}</h3>'
                f'<p>{m["blurb"]}</p><div class="foot"><span class="chip">Coming soon · {len(m["pages"])} pages</span></div></div>')

    weeks_html = []
    day = 0
    for w, focus, days in S.WEEKS:
        rows = []
        for items in days:
            day += 1
            links = "".join(item_link(root, i, built_map) for i in items)
            rows.append(f'<li><span class="day">Day {day}</span><span class="items">{links}</span></li>')
        weeks_html.append(f'<div class="week"><h3>Week {w} <small>{focus}</small></h3><ol>{"".join(rows)}</ol></div>')

    labs = "".join(f'<li><span class="soon"><span class="n">{lid}</span><span>{title.split(" · ", 1)[1]}</span>'
                   f'<span class="d">coming soon</span></span></li>' for lid, _s, title in S.LABS)

    main = f"""<div class="wide">
<div class="crumbs"><a href="{root}index.html">Home</a> &rsaquo; Level 1</div>
<p class="eyebrow">Level 1</p>
<h1>{S.LEVEL['title']}</h1>
<p class="lede">{S.LEVEL['goal']}</p>
<div class="meta"><span class="chip">{S.LEVEL['duration']}</span><span class="chip">6 modules · {sum(len(m['pages']) for m in S.MODULES)} pages</span><span class="chip">5 practical labs</span><span class="chip">Vendor-neutral</span></div>
<div class="progress" data-progress-of="{all_ids}" style="max-width:28rem"><div class="bar"><i></i></div><span class="plabel"></span></div>
<div class="continue" id="continue"><a class="btn" href="#">Continue: <span class="ct"></span> &rarr;</a></div>

<h2 id="how-to-use">How to use this guide</h2>
<p>Each day is one sitting of 45–60 minutes. Follow the same routine every day:</p>
<div class="routine">
  <div><b>2 min</b><span>Warm-up: answer the three questions from earlier pages at the top of the page.</span></div>
  <div><b>30–40 min</b><span>Read the page. Study each diagram before reading the text below it.</span></div>
  <div><b>10 min</b><span>Check yourself: try the fault scenario and the questions before opening the answers.</span></div>
  <div><b>1 min</b><span>Mark the page as done. Your progress is saved in this browser.</span></div>
</div>
<p>Every page has the same shape, so you always know where to look: <strong>After this page you can</strong> → <strong>In one line</strong> → <strong>Why it matters</strong> → <strong>How it works</strong> → <strong>Follow AHU-01</strong> → <strong>On site</strong> → <strong>Common faults</strong> → <strong>Key terms</strong> → <strong>Check yourself</strong>. Dotted-underlined abbreviations show their meaning when you hover over or tap them.</p>

<h2 id="ahu-01">Meet AHU-01</h2>
<p>Instead of learning each topic in isolation, you will follow one real-world example through the whole level: <strong>AHU-01</strong>, an air handling unit cooling the 3rd-floor offices of a commercial building. Module by module you will learn its plant, its sensors, its wiring, its communication and its control logic — and in the labs you will produce its complete control package.</p>
{ahu01.figure()}
{ahu01.device_table()}
<p><strong>Its job:</strong> hold the offices at 24 °C from 08:00 to 19:00, Monday to Saturday; bring in enough fresh air for the people inside; stop safely on a fire alarm; and alarm on any failure.</p>

<h2 id="modules">Modules</h2>
<div class="cards">{''.join(mod_cards)}</div>

<h2 id="schedule">4-week schedule</h2>
<p>Most days cover one or two pages. Day 7 of each week is for review and a short quiz. Labs sit in the week you learn the theory behind them. If a day runs over, simply continue the next day — understanding matters more than the calendar.</p>
{''.join(weeks_html)}

<h2 id="labs">Practical labs</h2>
<p>Together, the five labs produce a complete control package for AHU-01. Labs 4 and 5 can be done on a laptop with free tools — no hardware needed.</p>
<ol class="pagelist">{labs}</ol>

<h2 id="about">About this guide</h2>
<div class="note"><p>This guide is <strong>vendor-neutral</strong>. It is based on general industry practice and open standards — ISO 16484 (building automation), ASHRAE 135 (BACnet) and the Modbus specification — so it applies whichever brand of BMS you work with. Vendor-specific notes may be added to pages later. On site, always follow the manufacturer's documentation, the project specification and local electrical regulations.</p></div>
</div>"""
    side = C.sidebar(root, built, current="level")
    return url, C.shell(url, f"Level 1: {S.LEVEL['title']}", main, side,
                        desc="Level 1 BMS Fundamentals: architecture, HVAC, field devices, I/O, protocols and control logic.")


def home(built):
    url = "index.html"
    total = sum(len(m["pages"]) for m in S.MODULES)
    main = f"""<div class="wide">
<p class="eyebrow">Building Management Systems</p>
<h1>BMS Study Guide</h1>
<p class="lede">Practical, vendor-neutral study guides for Building Management Systems — from sensors and wiring to protocols and control logic, explained step by step with one example air handling unit followed all the way through.</p>
<div class="continue" id="continue"><a class="btn" href="#">Continue: <span class="ct"></span> &rarr;</a></div>
<div class="cards">
  <a class="mcard" href="{LV}/index.html"><span class="k">Level 1 · 4 weeks</span><h3>BMS Fundamentals</h3>
  <p>Architecture, HVAC plant, sensors and field devices, DI/DO/AI/AO wiring, BACnet and Modbus, and basic control logic. {total} pages and 5 practical labs.</p>
  <div class="foot progress" data-progress-of="{','.join(sorted(built))}"><div class="bar"><i></i></div><span class="plabel"></span></div></a>
  <div class="mcard soon"><span class="k">Level 2</span><h3>Planned</h3><p>The next level will build on Level 1. Its topics will be added here.</p><div class="foot"><span class="chip">Coming later</span></div></div>
  <div class="mcard soon"><span class="k">Vendor notes</span><h3>Planned</h3><p>Brand-specific notes for controllers and tools, added to the relevant pages.</p><div class="foot"><span class="chip">Coming later</span></div></div>
</div>
<p style="color:var(--muted);font-size:.86rem">Works offline once opened, prints cleanly, and keeps your progress in this browser only.</p>
</div>"""
    return url, C.shell(url, C.SITE, main, None, desc="Vendor-neutral BMS study guides.")


# --------------------------------------------------------------------------
# Static files
# --------------------------------------------------------------------------

def search_index(entries):
    return "window.BMS_INDEX=" + json.dumps(entries, ensure_ascii=False, separators=(",", ":")) + ";\n"


def abbr_js():
    return "window.BMS_ABBR=" + json.dumps(ABBR, ensure_ascii=False, separators=(",", ":")) + ";\n"


def service_worker(files):
    digest = hashlib.sha1()
    for rel in sorted(files):
        with open(os.path.join(C.REPO, *rel.split("/")), "rb") as f:
            digest.update(f.read())
    version = digest.hexdigest()[:10]
    precache = json.dumps(["./" + f for f in sorted(files)], indent=0)
    return f"""// Generated by build-scripts/build.py — do not edit by hand.
const CACHE = 'bms-sg-{version}';
const PRECACHE = {precache};

self.addEventListener('install', e => {{
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
}});
self.addEventListener('activate', e => {{
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
}});
// Network first (fresh content when online), cache as the offline fallback.
self.addEventListener('fetch', e => {{
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request).then(resp => {{
      if (resp && resp.ok) {{ const copy = resp.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); }}
      return resp;
    }}).catch(() => caches.match(e.request))
  );
}});
"""


# --------------------------------------------------------------------------

def main():
    pages = collect()
    built = {p["id"] for _m, p in pages}
    when = S.schedule_lookup()
    built_map = {p["id"]: (C.page_url(p["id"], p["slug"]), p["title"]) for _m, p in pages}
    entries = [{"t": "BMS Study Guide — home", "u": "index.html", "s": "Home", "k": ""},
               {"t": "Level 1: BMS Fundamentals — overview & 4-week schedule", "u": f"{LV}/index.html",
                "s": "Level 1", "k": "schedule planner AHU-01 example labs how to use"}]

    for k, (m, p) in enumerate(pages):
        prev = built_map[pages[k - 1][1]["id"]] if k > 0 else None
        nxt = built_map[pages[k + 1][1]["id"]] if k + 1 < len(pages) else None
        prev = (prev[0], f'{pages[k - 1][1]["id"].replace("-", ".")} {prev[1]}') if prev else None
        nxt = (nxt[0], f'{pages[k + 1][1]["id"].replace("-", ".")} {nxt[1]}') if nxt else None
        url, html = C.topic_page(m, p, built, prev, nxt, warmups_for(pages, k), when.get(p["id"]))
        write(url, html)
        entries.append({"t": f'{p["id"].replace("-", ".")} {p["title"]}', "u": url,
                        "s": f'Module {m["num"]} · {m["title"]}',
                        "k": " ".join(strip(a) for a, _b in p["terms"])})

    for m in S.MODULES:
        mod = CONTENT.get(m["num"])
        if not mod:
            continue
        url, html = C.module_index(m, built, when, getattr(mod, "MODULE_INTRO", ""))
        write(url, html)
        entries.append({"t": f'Module {m["num"]}: {m["title"]}', "u": url, "s": "Level 1", "k": m["blurb"]})

    url, html = level_index(built, built_map)
    write(url, html)
    url, html = home(built)
    write(url, html)

    write("assets/js/search-index.js", search_index(entries))
    write("assets/js/abbr-data.js", abbr_js())
    statics = ["assets/css/site.css", "assets/js/site.js", "manifest.json", "icon.svg"]
    write("sw.js", service_worker(WRITTEN + statics))
    print(f"Built {len(pages)} topic pages, {len(WRITTEN)} files in total.")


if __name__ == "__main__":
    main()
