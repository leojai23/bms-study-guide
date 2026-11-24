# -*- coding: utf-8 -*-
"""Builds the whole BMS Study Guide site from build-scripts/content/*.

    python build-scripts/build.py

Writes: index.html, level-1/**, assets/js/search-index.js, assets/js/abbr-data.js, sw.js.
Safe to re-run at any time; every generated file is overwritten."""
import hashlib
import importlib
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


def optional(name):
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as e:
        if e.name != name:
            raise
        return None


CONTENT = {n: optional(f"m{n}") for n in range(1, 7)}
CONTENT = {k: v for k, v in CONTENT.items() if v}
LABS = optional("labs")
CHEAT = optional("cheatsheet")
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
# Collect content
# --------------------------------------------------------------------------

def collect():
    pages = []          # ordered (module, page) for every topic page with content
    for m in S.MODULES:
        mod = CONTENT.get(m["num"])
        if not mod:
            continue
        by_id = {p["id"]: p for p in mod.PAGES}
        for pid, slug, title in m["pages"]:
            p = by_id.get(pid)
            if p:
                assert p["slug"] == slug, f"slug mismatch for {pid}"
                assert p["title"] == title, f"title mismatch for {pid}: {p['title']!r} vs {title!r}"
                pages.append((m, p))
    return pages


def warmups_for(pages, k):
    """One question from each of the three previous topic pages (rotating which one)."""
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


def schedule_order():
    return [i for _w, _f, days in S.WEEKS for d in days for i in d]


# --------------------------------------------------------------------------
# Reviews, final test, glossary
# --------------------------------------------------------------------------

def review_body(rid, week, page_map, built):
    root = C.depth_root(C.item_url(rid))
    _w, focus, days = S.WEEKS[week - 1]
    ids = [i for d in days for i in d if i in page_map]
    rows = []
    for i in ids:
        _m, p = page_map[i]
        rows.append((f'<a href="{root}{C.item_url(i)}">{i.replace("-", ".")}</a>', p["title"], p["one_line"]))
    recap = C.table(["Page", "Topic", "In one line"], rows, "plain")
    mixed = []
    for n, i in enumerate(ids):
        qs = page_map[i][1]["questions"]
        mixed.append((qs[(n * 2 + week) % len(qs)], i))
    practice = "".join(
        f'<li><p class="q">{q}</p><div class="from" style="font-size:.76rem;color:var(--muted)">from {i.replace("-", ".")}</div>'
        f'<details><summary>Show answer</summary><div class="a">{a}</div></details></li>' for (q, a), i in mixed)
    mods = sorted({int(i.split("-")[0]) for i in ids})
    quiz_links = " ".join(
        f'<a class="btn ghost" href="{root}{C.module_url(n)}#quiz">Module {n} quiz &rarr;</a>'
        for n in mods if n in CONTENT and getattr(CONTENT[n], "QUIZ", None)
        and all(p[0] in built for p in S.MODULES[n - 1]["pages"]))
    labs_this_week = [i for d in days for i in d if i.startswith("L")]
    lab_note = ""
    if labs_this_week:
        lab_note = C.callout("note", "Labs this week", "<p>" + ", ".join(
            f'<a href="{root}{C.item_url(i)}">{C.item_title(i)}</a>' for i in labs_this_week) +
            ". Finish them before moving on — they turn the theory into something you can show.</p>")
    return (f"<p>Week {week} covered <strong>{focus}</strong>. Spend this session consolidating, not "
            "learning new material.</p>"
            + C.steps([
                "<strong>Recap (10 min).</strong> Read the one-line summary of each page below. For any you cannot explain in your own words, re-read that page's “How it works”.",
                "<strong>Mixed practice (15 min).</strong> Answer one question from each page, out of order. Mixing topics is harder — and that is what makes it stick.",
                "<strong>Module quiz (15 min).</strong> Take the quiz and note the topics behind any wrong answers.",
                "<strong>Fix the gaps (10 min).</strong> Revisit the pages behind your wrong answers.",
            ])
            + '<h2 id="recap">Recap</h2>' + recap
            + '<h2 id="practice">Mixed practice</h2><ol class="qa">' + practice + "</ol>"
            + lab_note
            + ('<h2 id="quiz">Quiz</h2><p>' + quiz_links + "</p>" if quiz_links else ""))


def final_body():
    items = []
    for n in sorted(CONTENT):
        items += getattr(CONTENT[n], "FINAL", [])
    return ("<p>This test covers all six modules — five questions from each. Take it in one sitting, without "
            "looking back at the pages. <strong>24 or more out of 30</strong> means you are ready for Level 2; "
            "below that, revisit the modules where you lost marks (the explanation under each answer names the page).</p>"
            + C.quiz_html("final", items, "Final test")), len(items)


def glossary_body(pages):
    entries = {}
    for m, p in pages:
        for term, d in p["terms"]:
            key = strip(term).strip()
            if key.lower() not in entries:
                entries[key.lower()] = (key, d, p["id"], p["slug"], p["title"])
    for ab, full in ABBR.items():
        if ab.lower() not in entries:
            entries[ab.lower()] = (ab, full, None, None, None)
    groups = {}
    for k in sorted(entries, key=lambda s: re.sub(r"[^a-z0-9]", "", s) or s):
        letter = re.sub(r"[^a-z0-9]", "", k)[:1].upper() or "#"
        if letter.isdigit():
            letter = "0–9"
        groups.setdefault(letter, []).append(entries[k])
    root = C.depth_root(C.item_url("GL"))
    out = ['<p>Every key term from the topic pages, plus the abbreviations used across the guide. Each term links to '
           'the page that explains it. Type to filter.</p>',
           '<input type="search" id="glossaryFilter" class="glossary-filter" placeholder="Filter terms… e.g. relay, BACnet, 4–20">']
    for letter, items in groups.items():
        out.append(f'<h2 class="letter">{letter}</h2><dl class="terms">')
        for term, d, pid, slug, title in items:
            src = (f'<a class="src" href="{root}{C.page_url(pid, slug)}">{pid.replace("-", ".")} {title}</a>' if pid
                   else '<span class="src" style="color:var(--muted)">abbreviation</span>')
            out.append(f'<dt data-gterm>{term}</dt><dd>{d}{src}</dd>')
        out.append("</dl>")
    return "".join(out), len(entries)


# --------------------------------------------------------------------------
# Level overview and home
# --------------------------------------------------------------------------

def item_link(root, iid, built):
    title = C.item_title(iid)
    if iid in built:
        return f'<a data-progress-id="{iid}" href="{root}{C.item_url(iid)}">{title}</a>'
    return f'<span class="soon">{title}</span>'


def level_index(built):
    url = f"{LV}/index.html"
    root = C.depth_root(url)
    all_ids = ",".join(sorted(i for i in built if i not in ("GL", "CS")))

    mod_cards = []
    for m in S.MODULES:
        ids = [p[0] for p in m["pages"] if p[0] in built]
        weeks = sorted({w for w, _f, days in S.WEEKS for d in days for i in d if i.split("-")[0] == str(m["num"])})
        wk = (f"Weeks {weeks[0]}–{weeks[-1]}" if weeks and weeks[0] != weeks[-1] else (f"Week {weeks[0]}" if weeks else ""))
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
            links = "".join(item_link(root, i, built) for i in items)
            rows.append(f'<li><span class="day">Day {day}</span><span class="items">{links}</span></li>')
        weeks_html.append(f'<div class="week"><h3>Week {w} <small>{focus}</small></h3><ol>{"".join(rows)}</ol></div>')

    labs = []
    for lid, _s, title in S.LABS:
        name = title.split(" · ", 1)[1]
        if lid in built:
            labs.append(f'<li data-progress-id="{lid}"><a href="{root}{C.item_url(lid)}"><span class="n">{lid}</span>'
                        f'<span>{name}</span><span class="d">{LABS.LABS[lid]["time"]} <span class="tick">&#10003;</span></span></a></li>')
        else:
            labs.append(f'<li><span class="soon"><span class="n">{lid}</span><span>{name}</span><span class="d">coming soon</span></span></li>')

    refs = []
    for iid, desc in (("GL", "Every key term and abbreviation, with a link to the page that explains it."),
                      ("CS", "One printable page: signal ranges, sensor tables, Modbus and BACnet essentials, RS485 rules.")):
        if iid in built:
            refs.append(f'<a class="mcard" href="{root}{C.item_url(iid)}"><span class="k">Reference</span><h3>{C.item_title(iid)}</h3><p>{desc}</p></a>')

    main = f"""<div class="wide">
<div class="crumbs"><a href="{root}index.html">Home</a> &rsaquo; Level 1</div>
<p class="eyebrow">Level 1</p>
<h1>{S.LEVEL['title']}</h1>
<p class="lede">{S.LEVEL['goal']}</p>
<div class="meta"><span class="chip">{S.LEVEL['duration']}</span><span class="chip">6 modules · {sum(len(m['pages']) for m in S.MODULES)} pages</span><span class="chip">5 practical labs</span><span class="chip">Weekly reviews + final test</span><span class="chip">Vendor-neutral</span></div>
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
<p>Every page has the same shape, so you always know where to look: <strong>After this page you can</strong> → <strong>In one line</strong> → <strong>Why it matters</strong> → <strong>How it works</strong> → <strong>Follow AHU-01</strong> → <strong>On site</strong> → <strong>Common faults</strong> → <strong>Key terms</strong> → <strong>Check yourself</strong>. Dotted-underlined abbreviations show their meaning when you hover over or tap them. Green-edged boxes are interactive tools — use them.</p>

<h2 id="ahu-01">Meet AHU-01</h2>
<p>Instead of learning each topic in isolation, you will follow one real-world example through the whole level: <strong>AHU-01</strong>, an air handling unit cooling the 3rd-floor offices of a commercial building. Module by module you will learn its plant, its sensors, its wiring, its communication and its control logic — and in the labs you will produce its complete control package.</p>
{ahu01.figure()}
{ahu01.device_table()}
<p><strong>Its job:</strong> hold the offices at 24 °C from 08:00 to 19:00, Monday to Saturday; bring in enough fresh air for the people inside; stop safely on a fire alarm; and alarm on any failure.</p>

<h2 id="modules">Modules</h2>
<div class="cards">{''.join(mod_cards)}</div>

<h2 id="schedule">4-week schedule</h2>
<p>Most days cover one or two pages. Day 7 of each week is for review and a quiz. Labs sit in the week you learn the theory behind them. If a day runs over, simply continue the next day — understanding matters more than the calendar. Ticks appear as you mark pages done.</p>
{''.join(weeks_html)}

<h2 id="labs">Practical labs</h2>
<p>Together, the five labs produce a complete control package for AHU-01. Labs 4 and 5 can be done on a laptop with free tools — no hardware needed.</p>
<ol class="pagelist">{''.join(labs)}</ol>
{f'<h2 id="reference">Reference</h2><div class="cards">{"".join(refs)}</div>' if refs else ''}

<h2 id="about">About this guide</h2>
<div class="note"><p>This guide is <strong>vendor-neutral</strong>. It is based on general industry practice and open standards — ISO 16484 (building automation), ASHRAE 135 (BACnet) and the Modbus specification — so it applies whichever brand of BMS you work with. Vendor-specific notes may be added to pages later. On site, always follow the manufacturer's documentation, the project specification and local electrical regulations.</p></div>
</div>"""
    side = C.sidebar(root, built, current="level")
    return url, C.shell(url, f"Level 1: {S.LEVEL['title']}", main, side,
                        desc="Level 1 BMS Fundamentals: architecture, HVAC, field devices, I/O, protocols and control logic.")


def home(built):
    url = "index.html"
    total = sum(len(m["pages"]) for m in S.MODULES)
    done_ids = ",".join(sorted(i for i in built if i not in ("GL", "CS")))
    main = f"""<div class="wide">
<p class="eyebrow">Building Management Systems</p>
<h1>BMS Study Guide</h1>
<p class="lede">Practical, vendor-neutral study guides for Building Management Systems — from sensors and wiring to protocols and control logic, explained step by step with one example air handling unit followed all the way through.</p>
<div class="continue" id="continue"><a class="btn" href="#">Continue: <span class="ct"></span> &rarr;</a></div>
<div class="cards">
  <a class="mcard" href="{LV}/index.html"><span class="k">Level 1 · 4 weeks</span><h3>BMS Fundamentals</h3>
  <p>Architecture, HVAC plant, sensors and field devices, DI/DO/AI/AO wiring, BACnet and Modbus, and control logic. {total} pages, 5 practical labs, weekly reviews and a final test.</p>
  <div class="foot progress" data-progress-of="{done_ids}"><div class="bar"><i></i></div><span class="plabel"></span></div></a>
  <div class="mcard soon"><span class="k">Level 2</span><h3>Planned</h3><p>The next level will build on Level 1. Its topics will be added here.</p><div class="foot"><span class="chip">Coming later</span></div></div>
  <div class="mcard soon"><span class="k">Vendor notes</span><h3>Planned</h3><p>Brand-specific notes for controllers and tools, added to the relevant pages.</p><div class="foot"><span class="chip">Coming later</span></div></div>
</div>
<p style="color:var(--muted);font-size:.86rem">Works offline once opened, prints cleanly, and keeps your progress in this browser only.</p>
</div>"""
    return url, C.shell(url, C.SITE, main, None, desc="Vendor-neutral BMS study guides.")


# --------------------------------------------------------------------------
# Static files
# --------------------------------------------------------------------------

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
    page_map = {p["id"]: (m, p) for m, p in pages}
    when = S.schedule_lookup()

    # Which non-topic items exist?
    built = set(page_map)
    lab_data = LABS.LABS if LABS else {}
    built |= set(lab_data)
    all_pages_done = len(pages) == sum(len(m["pages"]) for m in S.MODULES)
    for w, (rid) in enumerate(("R1", "R2", "R3"), start=1):
        week_ids = [i for d in S.WEEKS[w - 1][2] for i in d if "-" in i]
        if week_ids and all(i in page_map for i in week_ids):
            built.add(rid)
    if all_pages_done and all(getattr(CONTENT[n], "FINAL", None) for n in CONTENT):
        built.add("FT")
    if pages:
        built.add("GL")
    if CHEAT:
        built.add("CS")

    # Pager follows the study schedule, then the reference pages.
    order = [i for i in schedule_order() if i in built] + [i for i in ("GL", "CS") if i in built]
    nav = {}
    for k, iid in enumerate(order):
        prev = (C.item_url(order[k - 1]), C.item_title(order[k - 1])) if k > 0 else None
        nxt = (C.item_url(order[k + 1]), C.item_title(order[k + 1])) if k + 1 < len(order) else None
        nav[iid] = (prev, nxt)

    entries = [{"t": "BMS Study Guide — home", "u": "index.html", "s": "Home", "k": ""},
               {"t": "Level 1: BMS Fundamentals — overview & 4-week schedule", "u": f"{LV}/index.html",
                "s": "Level 1", "k": "schedule planner AHU-01 example labs how to use"}]

    # Topic pages
    for k, (m, p) in enumerate(pages):
        prev, nxt = nav[p["id"]]
        url, html = C.topic_page(m, p, built, prev, nxt, warmups_for(pages, k), when.get(p["id"]))
        write(url, html)
        entries.append({"t": f'{p["id"].replace("-", ".")} {p["title"]}', "u": url,
                        "s": f'Module {m["num"]} · {m["title"]}',
                        "k": " ".join(strip(a) for a, _b in p["terms"])})

    # Module indexes (+ module quiz)
    for m in S.MODULES:
        mod = CONTENT.get(m["num"])
        if not mod:
            continue
        quiz = getattr(mod, "QUIZ", None) if all(p[0] in page_map for p in m["pages"]) else None
        url, html = C.module_index(m, built, when, getattr(mod, "MODULE_INTRO", ""), quiz)
        write(url, html)
        entries.append({"t": f'Module {m["num"]}: {m["title"]}', "u": url, "s": "Level 1",
                        "k": m["blurb"] + (" quiz" if quiz else "")})

    # Labs
    for lid, lab in lab_data.items():
        prev, nxt = nav.get(lid, (None, None))
        w = when.get(lid)
        chips = [f"Week {w[0]} · Day {w[1]}"] if w else []
        chips.append(lab["time"])
        url, html = C.simple_page(lid, f"Practical lab {lid[1]}", C.item_title(lid).split(" · ", 1)[1],
                                  LABS.render(lid, lab, C.depth_root(C.item_url(lid))), built, prev, nxt, chips,
                                  lede=lab["lede"])
        write(url, html)
        entries.append({"t": C.item_title(lid), "u": url, "s": "Practical lab", "k": lab.get("keywords", "")})

    # Weekly reviews and final test
    for w, rid in enumerate(("R1", "R2", "R3"), start=1):
        if rid not in built:
            continue
        prev, nxt = nav[rid]
        url, html = C.simple_page(rid, f"Week {w} review", S.REVIEWS[rid], review_body(rid, w, page_map, built),
                                  built, prev, nxt, [f"Week {w} · Day {w * 7}", "About 50 min"],
                                  lede="Recap, mixed practice and the module quiz.")
        write(url, html)
        entries.append({"t": S.REVIEWS[rid], "u": url, "s": "Review", "k": "review recap quiz"})
    if "FT" in built:
        prev, nxt = nav["FT"]
        body, n = final_body()
        url, html = C.simple_page("FT", "Level 1", "Level 1 final test", body, built, prev, nxt,
                                  ["Week 4 · Day 28", f"{n} questions", "About 45 min"],
                                  lede="Thirty questions across all six modules.")
        write(url, html)
        entries.append({"t": "Level 1 final test", "u": url, "s": "Test", "k": "exam final quiz test"})

    # Glossary and cheat sheet
    if "GL" in built:
        prev, nxt = nav["GL"]
        body, n = glossary_body(pages)
        url, html = C.simple_page("GL", "Reference", "Glossary", body, built, prev, nxt, [f"{n} terms"], done=False)
        write(url, html)
        entries.append({"t": "Glossary", "u": url, "s": "Reference", "k": "terms definitions abbreviations"})
    if "CS" in built:
        prev, nxt = nav["CS"]
        url, html = C.simple_page("CS", "Reference", "Cheat sheet", CHEAT.body(C.depth_root(C.item_url("CS"))), built,
                                  prev, nxt, ["Print it: one double-sided sheet"], done=False, wide=True,
                                  lede="The numbers and rules you will look up again and again.")
        write(url, html)
        entries.append({"t": "Cheat sheet", "u": url, "s": "Reference", "k": CHEAT.KEYWORDS})

    url, html = level_index(built)
    write(url, html)
    url, html = home(built)
    write(url, html)

    extra = []
    if LABS and hasattr(LABS, "downloads"):
        for rel, text in LABS.downloads().items():
            write(rel, text)
            extra.append(rel)

    write("assets/js/search-index.js",
          "window.BMS_INDEX=" + json.dumps(entries, ensure_ascii=False, separators=(",", ":")) + ";\n")
    write("assets/js/abbr-data.js",
          "window.BMS_ABBR=" + json.dumps(ABBR, ensure_ascii=False, separators=(",", ":")) + ";\n")
    statics = ["assets/css/site.css", "assets/js/site.js", "assets/js/tools.js", "manifest.json", "icon.svg"]
    write("sw.js", service_worker(WRITTEN + statics))
    print(f"Built {len(pages)} topic pages, {len(lab_data)} labs, "
          f"{len([i for i in built if i in S.REVIEWS])} reviews/tests, {len(WRITTEN)} files in total.")


if __name__ == "__main__":
    main()
