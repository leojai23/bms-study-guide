# -*- coding: utf-8 -*-
"""Page templates and content helpers for the BMS Study Guide.
Plain Python 3, no third-party packages. Imported by build.py and the content files."""
import html as _html
import math
import os
import re

import syllabus as S

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "BMS Study Guide"
LV = S.LEVEL["slug"]

# --------------------------------------------------------------------------
# Content helpers (used by content/mN.py)
# --------------------------------------------------------------------------

def esc(s):
    return _html.escape(s, quote=True)


def table(headers, rows, cls=""):
    th = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tbl-wrap"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'


def steps(items):
    return '<ol class="steps">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def bullets(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def callout(kind, label, body):
    """kind: note | tip | warn"""
    if not body.lstrip().startswith("<"):
        body = f"<p>{body}</p>"
    return f'<div class="{kind}"><span class="label">{label}</span>{body}</div>'


def cards(items):
    """items: [(heading, text)]"""
    return '<div class="grid2">' + "".join(
        f'<div class="card"><h4>{h}</h4><p>{t}</p></div>' for h, t in items) + "</div>"


def fig(svg, caption, small=False):
    cls = "diagram small" if small else "diagram"
    return f'<figure class="{cls}">{svg}<figcaption>{caption}</figcaption></figure>'


# ---- SVG primitives -------------------------------------------------------

def svg(w, h, inner, label):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}" '
            f'xmlns="http://www.w3.org/2000/svg">{inner}</svg>')


def defs(mid):
    """Arrow markers: url(#mid) grey, url(#mid-a) accent, url(#mid-r) red."""
    m = ('<marker id="{id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
         'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="{c}"/></marker>')
    return ("<defs>" + m.format(id=mid, c="d-arrow") + m.format(id=mid + "-a", c="d-arrow-a")
            + m.format(id=mid + "-r", c="d-arrow-r") + "</defs>")


def t(x, y, s, cls="d-t", anchor="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{s}</text>'


def rect(x, y, w, h, cls="d-box", r=8, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" class="{cls}" {extra}/>'


def box(x, y, w, h, title="", sub="", cls="d-box", tcls="d-t d-tb", r=8):
    """Rectangle with a bold title and optional sub-lines (separated by |)."""
    out = rect(x, y, w, h, cls, r)
    cx = x + w / 2
    lines = sub.split("|") if sub else []
    total = (1 if title else 0) + len(lines)
    lh = 15
    y0 = y + h / 2 - (total - 1) * lh / 2
    i = 0
    if title:
        out += t(cx, y0, title, tcls)
        i += 1
    for ln in lines:
        out += t(cx, y0 + i * lh, ln, "d-ts")
        i += 1
    return out


def line(x1, y1, x2, y2, cls="d-line", end=None, start=None):
    m = ""
    if end:
        m += f' marker-end="url(#{end})"'
    if start:
        m += f' marker-start="url(#{start})"'
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"{m}/>'


def path(d, cls="d-line", end=None, start=None):
    m = ""
    if end:
        m += f' marker-end="url(#{end})"'
    if start:
        m += f' marker-start="url(#{start})"'
    return f'<path d="{d}" class="{cls}"{m}/>'


def circle(cx, cy, r, cls="d-box"):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" class="{cls}"/>'


# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

def page_url(pid, slug):
    mod = pid.split("-")[0]
    return f"{LV}/module-{mod}/{pid}-{slug}.html"


def module_url(num):
    return f"{LV}/module-{num}/index.html"


def depth_root(url):
    return "../" * url.count("/")


# --------------------------------------------------------------------------
# Shell
# --------------------------------------------------------------------------

THEME_BOOT = ("<script>(function(){try{var t=localStorage.getItem('bms-theme');"
              "if(!t){t=window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}"
              "document.documentElement.setAttribute('data-theme',t);}catch(e){}})();</script>")

ICON = {
    "menu": '<svg viewBox="0 0 24 24"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>',
    "search": '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><line x1="20.5" y1="20.5" x2="16" y2="16"/></svg>',
    "theme": '<svg viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    "print": '<svg viewBox="0 0 24 24"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>',
}


def shell(url, title, main, sidebar_html=None, page_id="", desc=""):
    root = depth_root(url)
    side = ""
    menu = ""
    if sidebar_html is not None:
        side = f'<nav class="sidebar" id="sidebar" aria-label="Contents">{sidebar_html}</nav><div class="scrim" id="scrim"></div>'
        menu = f'<button class="icon-btn menu-btn" id="menuBtn" aria-label="Open contents">{ICON["menu"]}</button>'
    full_title = title if title == SITE else f"{title} | {SITE}"
    return f"""<!DOCTYPE html>
<html lang="en" data-root="{root}" data-page="{page_id}" data-url="{url}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#2160a3">
<link rel="manifest" href="{root}manifest.json">
<link rel="icon" href="{root}icon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{root}assets/css/site.css">
{THEME_BOOT}
</head>
<body>
<header class="topbar">
  {menu}
  <a class="brand" href="{root}index.html"><span class="logo">BMS</span><span class="full">{SITE}</span></a>
  <div class="top-actions">
    <span class="search-hint">Press <kbd>/</kbd> to search</span>
    <button class="icon-btn" id="searchBtn" aria-label="Search" title="Search (/)">{ICON["search"]}</button>
    <button class="icon-btn" id="themeBtn" aria-label="Switch light/dark" title="Light / dark">{ICON["theme"]}</button>
    <button class="icon-btn" id="printBtn" aria-label="Print" title="Print this page">{ICON["print"]}</button>
  </div>
</header>
<div class="layout">
{side}
<main class="content" id="main">
{main}
</main>
</div>
<div class="overlay" id="searchOverlay" role="dialog" aria-label="Search">
  <div class="search-box">
    <input id="searchInput" type="search" placeholder="Search topics and key terms…" autocomplete="off">
    <div class="search-results" id="searchResults"></div>
  </div>
</div>
<script defer src="{root}assets/js/abbr-data.js"></script>
<script defer src="{root}assets/js/search-index.js"></script>
<script defer src="{root}assets/js/site.js"></script>
</body>
</html>
"""


# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------

def sidebar(root, built, current=None, current_module=None):
    """built: set of page ids that have content."""
    o = ['<div class="side-h">Level 1 · BMS Fundamentals</div>']
    lvl_cls = ' class="active"' if current == "level" else ""
    o.append(f'<a{lvl_cls} href="{root}{LV}/index.html"><span class="num">&#9679;</span><span>Overview, schedule &amp; AHU-01</span></a>')
    o.append('<div class="side-h">Modules</div>')
    for m in S.MODULES:
        is_open = " open" if m["num"] == current_module else ""
        ids = ",".join(p[0] for p in m["pages"] if p[0] in built)
        o.append(f'<details{is_open}><summary><span class="num">M{m["num"]}</span><span>{m["title"]}</span></summary><div>')
        for pid, slug, title in m["pages"]:
            num = pid.replace("-", ".")
            if pid in built:
                cls = "active" if pid == current else ""
                o.append(f'<a class="{cls}" data-progress-id="{pid}" href="{root}{page_url(pid, slug)}">'
                         f'<span class="num">{num}</span><span>{title}</span><span class="tick">&#10003;</span></a>')
            else:
                o.append(f'<span class="soon"><span class="num">{num}</span><span>{title}</span><span class="tag-soon">soon</span></span>')
        o.append("</div></details>")
    o.append('<div class="side-h">Practice</div>')
    for lid, _slug, title in S.LABS:
        o.append(f'<span class="soon"><span class="num">{lid}</span><span>{title.split(" · ", 1)[1]}</span><span class="tag-soon">soon</span></span>')
    o.append('<span class="soon"><span class="num">&#9679;</span><span>Glossary &amp; cheat sheet</span><span class="tag-soon">soon</span></span>')
    return "\n".join(o)


# --------------------------------------------------------------------------
# Topic page
# --------------------------------------------------------------------------

def _words(s):
    return len(re.sub(r"<[^>]+>", " ", s).split())


def reading_minutes(p):
    txt = " ".join([p["one_line"], p["why"], p["body"], " ".join(p.get("on_site", [])),
                    p.get("ahu01", ""), " ".join(a + b for a, b in p.get("terms", []))])
    return max(10, int(math.ceil(_words(txt) / 170 / 5.0) * 5))


def scenario_html(sc, key):
    opts = "".join(f'<button type="button" class="s-opt" data-i="{i}">{o}</button>'
                   for i, o in enumerate(sc["options"]))
    return f"""<div class="scenario" data-answer="{sc['answer']}" id="scenario-{key}">
<span class="label">Fault scenario · what would you do?</span>
<p class="s-prompt">{sc['prompt']}</p>
{opts}
<div class="s-feedback" hidden><span class="verdict"></span>{sc['explain']}<br><button type="button" class="s-retry">Try again</button></div>
</div>"""


def topic_page(module, page, built, prev, nxt, warmups, when):
    url = page_url(page["id"], page["slug"])
    root = depth_root(url)
    num = page["id"].replace("-", ".")
    total = len(module["pages"])
    pos = [p[0] for p in module["pages"]].index(page["id"]) + 1
    mins = reading_minutes(page)
    week, day = when if when else (None, None)

    chips = []
    if week:
        chips.append(f'<span class="chip">Week {week} · Day {day}</span>')
    chips.append(f'<span class="chip">About {mins} min</span>')
    chips.append(f'<span class="chip">Page {pos} of {total}</span>')
    chips.append('<span class="chip ok" id="doneChip" hidden>&#10003; Done</span>')

    objectives = "".join(f"<li>{o}</li>" for o in page["objectives"])

    warm = ""
    if warmups:
        items = "".join(
            f'<li>{q}<div class="from">from {src}</div><details><summary>Show answer</summary><div class="a">{a}</div></details></li>'
            for q, a, src in warmups)
        warm = (f'<details class="warmup no-abbr"><summary>Warm-up · {len(warmups)} quick question{"s" if len(warmups) > 1 else ""} from earlier pages (2 min)</summary>'
                f'<ol>{items}</ol></details>')

    on_site = ""
    if page.get("on_site"):
        on_site = ('<h2 id="on-site"><span class="h-ico">&#9874;</span>On site</h2>'
                   + bullets(page["on_site"]))

    faults = ""
    if page.get("faults"):
        faults = ('<h2 id="faults"><span class="h-ico">!</span>Common faults</h2>'
                  '<p>Read each row left to right: what you see, the usual cause, and what to check first.</p>'
                  + table(["What you see", "Likely cause", "Check first"], page["faults"], "faults"))

    ahu = ""
    if page.get("ahu01"):
        ahu = f'<div class="ahu01"><span class="label">Follow AHU-01</span>{page["ahu01"]}</div>'

    terms = "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in page["terms"])

    scen = "".join(scenario_html(sc, f"{page['id']}-{i}") for i, sc in enumerate(page.get("scenarios", [])))
    qs = "".join(
        f'<li><p class="q">{q}</p><details><summary>Show answer</summary><div class="a">{a}</div></details></li>'
        for q, a in page["questions"])

    vendor = ""
    if page.get("vendor_notes"):
        vendor = '<h2 id="vendor">Vendor notes</h2>' + "".join(
            callout("note", v, body) for v, body in page["vendor_notes"])

    pager = '<nav class="pager no-abbr" aria-label="Previous and next">'
    pager += (f'<a class="prev" href="{root}{prev[0]}"><small>&larr; Previous</small>{prev[1]}</a>'
              if prev else "<span></span>")
    pager += (f'<a class="next" href="{root}{nxt[0]}"><small>Next &rarr;</small>{nxt[1]}</a>'
              if nxt else "")
    pager += "</nav>"

    main = f"""<article>
<div class="crumbs no-abbr"><a href="{root}{LV}/index.html">Level 1</a> &rsaquo; <a href="{root}{module_url(module['num'])}">Module {module['num']} · {module['title']}</a> &rsaquo; {num}</div>
<p class="eyebrow no-abbr">Module {module['num']} · {module['title']}</p>
<h1>{num}&ensp;{page['title']}</h1>
<div class="meta no-abbr">{''.join(chips)}</div>

<div class="objectives"><span class="label">After this page you can</span><ul>{objectives}</ul></div>
{warm}
<div class="oneline"><span class="label">In one line</span><p>{page['one_line']}</p></div>

<h2 id="why"><span class="h-ico">?</span>Why it matters</h2>
{page['why']}

<h2 id="how"><span class="h-ico">&#9881;</span>How it works</h2>
{page['body']}

{ahu}
{on_site}
{faults}

<h2 id="terms"><span class="h-ico">A</span>Key terms</h2>
<dl class="terms">{terms}</dl>

<h2 id="check"><span class="h-ico">&#10003;</span>Check yourself</h2>
<p>Try each one before opening the answer.</p>
{scen}
<ol class="qa">{qs}</ol>
{vendor}

<div class="done-row"><button type="button" class="btn" id="doneBtn">Mark this page as done</button></div>
{pager}
</article>"""
    side = sidebar(root, built, current=page["id"], current_module=module["num"])
    return url, shell(url, f"{num} {page['title']}", main, side, page_id=page["id"],
                      desc=re.sub(r"<[^>]+>", "", page["one_line"]))


# --------------------------------------------------------------------------
# Module index
# --------------------------------------------------------------------------

def module_index(module, built, when_map, intro=""):
    url = module_url(module["num"])
    root = depth_root(url)
    ids = ",".join(p[0] for p in module["pages"] if p[0] in built)
    rows = []
    for pid, slug, title in module["pages"]:
        num = pid.replace("-", ".")
        w = when_map.get(pid)
        d = f"Week {w[0]} · Day {w[1]}" if w else ""
        if pid in built:
            rows.append(f'<li data-progress-id="{pid}"><a href="{root}{page_url(pid, slug)}"><span class="n">{num}</span>'
                        f'<span>{title}</span><span class="d">{d} <span class="tick">&#10003;</span></span></a></li>')
        else:
            rows.append(f'<li><span class="soon"><span class="n">{num}</span><span>{title}</span><span class="d">coming soon</span></span></li>')
    first = next((p for p in module["pages"] if p[0] in built), None)
    start = (f'<p><a class="btn" href="{root}{page_url(first[0], first[1])}">Start with {first[0].replace("-", ".")} &rarr;</a></p>'
             if first else "")
    main = f"""<article>
<div class="crumbs"><a href="{root}{LV}/index.html">Level 1</a> &rsaquo; Module {module['num']}</div>
<p class="eyebrow">Level 1 · Module {module['num']}</p>
<h1>{module['title']}</h1>
<p class="lede">{module['blurb']}</p>
<div class="progress" data-progress-of="{ids}"><div class="bar"><i></i></div><span class="plabel"></span></div>
{intro}
<h2>Pages in this module</h2>
<ol class="pagelist">{''.join(rows)}</ol>
{start}
</article>"""
    side = sidebar(root, built, current=None, current_module=module["num"])
    return url, shell(url, f"Module {module['num']}: {module['title']}", main, side, desc=module["blurb"])
