/* BMS Study Guide — shared behaviour (no dependencies, works offline and from file://).
   Theme toggle, mobile menu, search, print, progress tracking, fault scenarios,
   abbreviation tooltips, "continue where you left off", service worker. */
(function () {
  'use strict';
  var doc = document.documentElement;
  var ROOT = doc.getAttribute('data-root') || '';
  var PAGE = doc.getAttribute('data-page') || '';
  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function store(k, v) { try { if (v === undefined) return JSON.parse(localStorage.getItem(k)); localStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; } }

  /* ---------- Theme ---------- */
  var themeBtn = $('#themeBtn');
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var t = doc.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    doc.setAttribute('data-theme', t);
    try { localStorage.setItem('bms-theme', t); } catch (e) {}
  });

  /* ---------- Print: open every answer so the printout is complete ---------- */
  var printBtn = $('#printBtn');
  if (printBtn) printBtn.addEventListener('click', function () { window.print(); });
  window.addEventListener('beforeprint', function () {
    $$('details').forEach(function (d) { d.setAttribute('data-was-open', d.open ? '1' : '0'); d.open = true; });
  });
  window.addEventListener('afterprint', function () {
    $$('details').forEach(function (d) { d.open = d.getAttribute('data-was-open') === '1'; });
  });

  /* ---------- Mobile menu ---------- */
  var menuBtn = $('#menuBtn'), side = $('#sidebar'), scrim = $('#scrim');
  function setMenu(open) { if (!side) return; side.classList.toggle('open', open); if (scrim) scrim.classList.toggle('show', open); }
  if (menuBtn) menuBtn.addEventListener('click', function () { setMenu(!side.classList.contains('open')); });
  if (scrim) scrim.addEventListener('click', function () { setMenu(false); });
  var activeLink = side && $('a.active', side);
  if (activeLink && activeLink.scrollIntoView) activeLink.scrollIntoView({ block: 'center' });

  /* ---------- Progress (stored only in this browser) ---------- */
  var PKEY = 'bms-progress';
  function progress() { return store(PKEY) || {}; }
  function paint() {
    var p = progress();
    $$('[data-progress-id]').forEach(function (el) { el.classList.toggle('is-done', !!p[el.getAttribute('data-progress-id')]); });
    $$('[data-progress-of]').forEach(function (el) {
      var ids = el.getAttribute('data-progress-of').split(',').filter(Boolean);
      var n = ids.filter(function (i) { return p[i]; }).length;
      var bar = $('.bar i', el); if (bar) bar.style.width = (ids.length ? Math.round(n * 100 / ids.length) : 0) + '%';
      var lab = $('.plabel', el); if (lab) lab.textContent = n + ' of ' + ids.length + ' pages done';
    });
    var btn = $('#doneBtn');
    if (btn) {
      var d = !!p[PAGE];
      btn.classList.toggle('is-done', d);
      btn.textContent = d ? '✓ Done — click to undo' : 'Mark this page as done';
      var chip = $('#doneChip'); if (chip) chip.hidden = !d;
    }
  }
  var doneBtn = $('#doneBtn');
  if (doneBtn) doneBtn.addEventListener('click', function () {
    var p = progress();
    if (p[PAGE]) delete p[PAGE]; else p[PAGE] = Date.now();
    store(PKEY, p); paint();
  });
  paint();

  /* ---------- Continue where you left off ---------- */
  var url = doc.getAttribute('data-url');
  if (PAGE && url) store('bms-last', { u: url, t: document.title.split(' | ')[0] });
  var cont = $('#continue'), last = store('bms-last');
  if (cont && last && last.u) {
    var a = $('a', cont); a.href = ROOT + last.u; $('.ct', cont).textContent = last.t;
    cont.classList.add('show');
  }

  /* ---------- Fault scenarios ---------- */
  $$('.scenario').forEach(function (s) {
    var ans = +s.getAttribute('data-answer'), opts = $$('.s-opt', s), fb = $('.s-feedback', s);
    opts.forEach(function (b) {
      b.addEventListener('click', function () {
        if (s.classList.contains('answered')) return;
        s.classList.add('answered');
        var ok = +b.getAttribute('data-i') === ans;
        b.classList.add(ok ? 'correct' : 'wrong');
        opts[ans].classList.add('correct');
        $('.verdict', fb).textContent = ok ? 'Correct.' : 'Not quite.';
        fb.hidden = false;
      });
    });
    var retry = $('.s-retry', s);
    if (retry) retry.addEventListener('click', function () {
      s.classList.remove('answered'); fb.hidden = true;
      opts.forEach(function (b) { b.classList.remove('correct', 'wrong'); });
    });
  });

  /* ---------- Abbreviation tooltips (first use on each page) ---------- */
  var ABBR = window.BMS_ABBR, art = $('article');
  if (ABBR && art) {
    var keys = Object.keys(ABBR).sort(function (a, b) { return b.length - a.length; });
    var src = '\\b(' + keys.map(function (k) { return k.replace(/[.*+?^${}()|[\]\\\/]/g, '\\$&'); }).join('|') + ')\\b';
    var SKIP = { H1: 1, H2: 1, H3: 1, A: 1, ABBR: 1, CODE: 1, BUTTON: 1, SCRIPT: 1, STYLE: 1, SUMMARY: 1, TH: 1 };
    var walker = document.createTreeWalker(art, NodeFilter.SHOW_TEXT, null, false), nodes = [], n;
    while ((n = walker.nextNode())) {
      var ok = true;
      for (var el = n.parentNode; el && el !== art; el = el.parentNode) {
        if (SKIP[el.nodeName] || el.namespaceURI === 'http://www.w3.org/2000/svg' || (el.classList && el.classList.contains('no-abbr'))) { ok = false; break; }
      }
      if (ok) nodes.push(n);
    }
    var seen = {};
    nodes.forEach(function (node) {
      var text = node.nodeValue, re = new RegExp(src, 'g'), m, frag = null, lastI = 0;
      while ((m = re.exec(text))) {
        if (seen[m[1]]) continue;
        seen[m[1]] = 1;
        frag = frag || document.createDocumentFragment();
        frag.appendChild(document.createTextNode(text.slice(lastI, m.index)));
        var ab = document.createElement('abbr');
        ab.className = 'ab'; ab.tabIndex = 0; ab.setAttribute('data-full', ABBR[m[1]]); ab.textContent = m[1];
        frag.appendChild(ab);
        lastI = m.index + m[1].length;
      }
      if (frag) { frag.appendChild(document.createTextNode(text.slice(lastI))); node.parentNode.replaceChild(frag, node); }
    });
    var tip = document.createElement('div'); tip.id = 'abTip'; document.body.appendChild(tip);
    var showTip = function (t) {
      tip.textContent = t.getAttribute('data-full');
      var r = t.getBoundingClientRect();
      tip.classList.add('show');
      var w = tip.offsetWidth, left = Math.max(8, Math.min(r.left, window.innerWidth - w - 8));
      var top = r.bottom + 6; if (top + tip.offsetHeight > window.innerHeight - 8) top = r.top - tip.offsetHeight - 6;
      tip.style.left = left + 'px'; tip.style.top = top + 'px';
    };
    var hideTip = function () { tip.classList.remove('show'); };
    document.addEventListener('mouseover', function (e) { if (e.target.classList && e.target.classList.contains('ab')) showTip(e.target); });
    document.addEventListener('mouseout', function (e) { if (e.target.classList && e.target.classList.contains('ab')) hideTip(); });
    document.addEventListener('focusin', function (e) { if (e.target.classList && e.target.classList.contains('ab')) showTip(e.target); });
    document.addEventListener('focusout', hideTip);
    window.addEventListener('scroll', hideTip, { passive: true });
  }

  /* ---------- Search ---------- */
  var overlay = $('#searchOverlay'), input = $('#searchInput'), results = $('#searchResults'), active = -1;
  function render(q) {
    var IDX = window.BMS_INDEX || [];
    q = q.trim().toLowerCase(); active = -1;
    if (!q) { results.innerHTML = '<div class="s-empty">Search page titles and key terms &mdash; try <b>PT1000</b>, <b>DDC</b> or <b>interposing relay</b>.</div>'; return; }
    var words = q.split(/\s+/);
    var scored = IDX.map(function (e) {
      var t = e.t.toLowerCase(), k = (e.k || '').toLowerCase(), s = 0;
      for (var i = 0; i < words.length; i++) {
        if (t.indexOf(words[i]) !== -1) s += 3; else if (k.indexOf(words[i]) !== -1) s += 1; else return null;
      }
      return { e: e, s: s };
    }).filter(Boolean).sort(function (a, b) { return b.s - a.s; }).slice(0, 30);
    if (!scored.length) { results.innerHTML = '<div class="s-empty">No matches.</div>'; return; }
    results.innerHTML = scored.map(function (x) {
      return '<a class="s-res" href="' + ROOT + x.e.u + '"><div class="rt">' + x.e.t + '</div><div class="rs">' + x.e.s + '</div></a>';
    }).join('');
  }
  function openSearch() { if (!overlay) return; overlay.classList.add('open'); input.value = ''; render(''); input.focus(); }
  function closeSearch() { overlay.classList.remove('open'); }
  var sBtn = $('#searchBtn'); if (sBtn) sBtn.addEventListener('click', openSearch);
  if (overlay) {
    overlay.addEventListener('click', function (e) { if (e.target === overlay) closeSearch(); });
    input.addEventListener('input', function () { render(input.value); });
  }
  document.addEventListener('keydown', function (e) {
    var tag = document.activeElement && document.activeElement.tagName;
    if (e.key === '/' && tag !== 'INPUT' && tag !== 'TEXTAREA' && overlay && !overlay.classList.contains('open')) { e.preventDefault(); openSearch(); return; }
    if (!overlay || !overlay.classList.contains('open')) { if (e.key === 'Escape') setMenu(false); return; }
    var items = $$('.s-res', results);
    if (e.key === 'Escape') closeSearch();
    else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      active = e.key === 'ArrowDown' ? Math.min(active + 1, items.length - 1) : Math.max(active - 1, 0);
      items.forEach(function (it, i) { it.classList.toggle('active', i === active); });
      if (items[active]) items[active].scrollIntoView({ block: 'nearest' });
    } else if (e.key === 'Enter' && items.length) { window.location.href = items[Math.max(active, 0)].href; }
  });

  /* ---------- Offline support (only when served over http/https) ---------- */
  if ('serviceWorker' in navigator && /^https?:/.test(location.protocol)) {
    window.addEventListener('load', function () { navigator.serviceWorker.register(ROOT + 'sw.js').catch(function () {}); });
  }
})();
