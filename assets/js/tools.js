/* BMS Study Guide — interactive tools (no dependencies, work offline).
   A tool is any <div class="tool" data-tool="NAME"> on a page; optional data-* attributes set defaults.
   Tools: scale (analog scaling), rtd (NTC/PT1000), subnet, modbus (register decoder),
          pid (PID playground), ahuseq (AHU-01 start/stop stepper). */
(function () {
  'use strict';
  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function num(v) { var x = parseFloat(String(v).trim().replace(',', '.')); return isFinite(x) ? x : NaN; }
  function fmt(x, d) {
    if (!isFinite(x)) return '—';
    var s = x.toFixed(d == null ? 2 : d);
    if (s.indexOf('.') >= 0) s = s.replace(/0+$/, '').replace(/\.$/, '');
    return s === '-0' ? '0' : s;
  }
  function field(label, control) { return '<label class="tf"><span>' + label + '</span>' + control + '</label>'; }
  function line(cls, text) { return '<div class="' + cls + '">' + text + '</div>'; }
  var TOOLS = {};

  /* ---------------------------------------------------------------- scale */
  TOOLS.scale = function (root) {
    var d = root.dataset;
    root.innerHTML =
      '<span class="label">Try it · analog signal scaling</span>' +
      '<div class="tool-grid">' +
      field('Signal type', '<select data-k="type"><option value="4-20">4–20 mA</option><option value="0-20">0–20 mA</option><option value="0-10">0–10 V</option><option value="2-10">2–10 V</option></select>') +
      field('Range minimum', '<input data-k="lo" type="number" step="any">') +
      field('Range maximum', '<input data-k="hi" type="number" step="any">') +
      field('Units', '<input data-k="u" type="text">') +
      '</div><div class="tool-grid">' +
      field('Measured signal (mA or V)', '<input data-k="sig" type="number" step="any">') +
      field('…or engineering value', '<input data-k="eng" type="number" step="any">') +
      '</div><div class="tool-out" data-out></div>';
    var k = function (n) { return $('[data-k="' + n + '"]', root); };
    k('type').value = d.type || '4-20'; k('lo').value = d.lo || '0'; k('hi').value = d.hi || '500';
    k('u').value = d.u || 'Pa'; k('sig').value = d.sig || '12';
    var last = 'sig';
    function run() {
      var t = k('type').value, r = { '4-20': [4, 20, 'mA'], '0-20': [0, 20, 'mA'], '0-10': [0, 10, 'V'], '2-10': [2, 10, 'V'] }[t];
      var s0 = r[0], s1 = r[1], su = r[2], lo = num(k('lo').value), hi = num(k('hi').value), u = k('u').value;
      var sig, eng;
      if (last === 'eng') { eng = num(k('eng').value); sig = s0 + (eng - lo) / (hi - lo) * (s1 - s0); k('sig').value = isFinite(sig) ? fmt(sig, 3) : ''; }
      else { sig = num(k('sig').value); eng = lo + (sig - s0) / (s1 - s0) * (hi - lo); k('eng').value = isFinite(eng) ? fmt(eng, 3) : ''; }
      var out = '';
      if (isFinite(sig) && isFinite(eng) && hi !== lo) {
        out += '<div class="big">' + fmt(sig, 3) + ' ' + su + ' &nbsp;⇄&nbsp; ' + fmt(eng, 2) + ' ' + u + '</div>';
        out += line('muted', 'value = ' + fmt(lo) + ' + (' + fmt(sig, 3) + ' − ' + s0 + ') ÷ ' + (s1 - s0) + ' × (' + fmt(hi) + ' − ' + fmt(lo) + ') = ' + fmt(eng, 2) + ' ' + u);
        var pct = Math.max(0, Math.min(100, (sig - s0) / (s1 - s0) * 100));
        out += '<div class="meter"><i style="width:' + pct + '%"></i></div>';
        if (t === '4-20') {
          if (sig < 3.6) out += line('bad', 'Below 3.6 mA — treat as a fault: open circuit, broken wire, no loop power, or a failed transmitter.');
          else if (sig < 4) out += line('warn', 'Slightly below 4 mA — at or under the bottom of the range. Check zero calibration.');
          else if (sig > 21) out += line('bad', 'Above 21 mA — treat as a fault: short circuit, failed transmitter, or the sensor is over-range.');
          else if (sig > 20) out += line('warn', 'Slightly above 20 mA — the measured value is above the configured range.');
          else out += line('ok', 'Inside the live range. A broken wire would give 0 mA, which the controller can recognise as a fault.');
        } else if (t === '2-10') {
          if (sig < 1.8) out += line('bad', 'Well below the 2 V live zero — likely a broken wire, missing supply or a failed device.');
          else if (sig > 10.2) out += line('warn', 'Above 10 V — over-range or wrong signal type.');
          else out += line('ok', 'Inside the live range.');
        } else {
          if (sig <= 0.05) out += line('warn', 'At 0 — this could be a real minimum or a broken wire. With no live zero you cannot tell them apart.');
          else if (sig > s1 * 1.02) out += line('warn', 'Above the top of the range — over-range or wrong signal type.');
          else out += line('ok', 'Inside the range.');
        }
      } else out = line('muted', 'Enter a range and a value.');
      $('[data-out]', root).innerHTML = out;
    }
    root.addEventListener('input', function (e) { var n = e.target.getAttribute('data-k'); if (n === 'eng' || n === 'sig') last = n; run(); });
    run();
  };

  /* ---------------------------------------------------------------- rtd */
  var CURVES = {
    pt1000: { name: 'PT1000 (IEC 60751)', f: function (T) { var A = 3.9083e-3, B = -5.775e-7, C = -4.183e-12; return 1000 * (1 + A * T + B * T * T + (T < 0 ? C * (T - 100) * T * T * T : 0)); } },
    ntc3950: { name: '10k NTC, β = 3950', f: function (T) { return 10000 * Math.exp(3950 * (1 / (T + 273.15) - 1 / 298.15)); } },
    ntc3435: { name: '10k NTC, β = 3435', f: function (T) { return 10000 * Math.exp(3435 * (1 / (T + 273.15) - 1 / 298.15)); } }
  };
  function invert(f, R) {
    var lo = -60, hi = 200, flo = f(lo), fhi = f(hi), inc = fhi > flo;
    if (inc ? (R < flo || R > fhi) : (R > flo || R < fhi)) return NaN;
    for (var i = 0; i < 80; i++) { var m = (lo + hi) / 2, fm = f(m); if ((fm < R) === inc) lo = m; else hi = m; }
    return (lo + hi) / 2;
  }
  TOOLS.rtd = function (root) {
    root.innerHTML =
      '<span class="label">Try it · sensor resistance ⇄ temperature</span>' +
      '<div class="tool-grid">' +
      field('Sensor type', '<select data-k="type"><option value="pt1000">PT1000</option><option value="ntc3950">10k NTC (β 3950)</option><option value="ntc3435">10k NTC (β 3435)</option></select>') +
      field('Resistance measured (Ω)', '<input data-k="r" type="number" step="any">') +
      field('…or temperature (°C)', '<input data-k="t" type="number" step="any">') +
      '</div><div class="tool-out" data-out></div>';
    var k = function (n) { return $('[data-k="' + n + '"]', root); };
    k('type').value = root.dataset.type || 'pt1000'; k('t').value = '25';
    var last = 't';
    function run() {
      var c = CURVES[k('type').value], T, R, out = '';
      if (last === 'r') { R = num(k('r').value); T = invert(c.f, R); k('t').value = isFinite(T) ? fmt(T, 1) : ''; }
      else { T = num(k('t').value); R = (T >= -60 && T <= 200) ? c.f(T) : NaN; k('r').value = isFinite(R) ? fmt(R, 1) : ''; }
      if (isFinite(T) && isFinite(R)) {
        var slope = (c.f(T + 0.5) - c.f(T - 0.5));
        out += '<div class="big">' + fmt(R, 1) + ' Ω &nbsp;⇄&nbsp; ' + fmt(T, 1) + ' °C</div>';
        out += line('muted', c.name + ' · sensitivity here ≈ ' + fmt(Math.abs(slope), 2) + ' Ω per °C · 1 Ω of wiring resistance ≈ ' + fmt(1 / Math.abs(slope), 3) + ' °C error');
      } else {
        out += line('bad', 'Outside −60…200 °C for this sensor type. A very high resistance means an open circuit; near 0 Ω means a short circuit.');
      }
      out += line('warn', k('type').value === 'pt1000'
        ? 'PT1000: open circuit → reads very HIGH; short circuit → reads very LOW.'
        : 'NTC: open circuit → reads very LOW; short circuit → reads very HIGH.');
      if (k('type').value !== 'pt1000') out += line('muted', 'NTC curves differ between manufacturers. This uses the β equation and is approximate; use the maker’s table for calibration.');
      $('[data-out]', root).innerHTML = out;
    }
    root.addEventListener('input', function (e) { var n = e.target.getAttribute('data-k'); if (n === 'r' || n === 't') last = n; run(); });
    root.addEventListener('change', run);
    run();
  };

  /* ---------------------------------------------------------------- subnet */
  function ip2n(s) {
    var p = String(s).trim().split('.');
    if (p.length !== 4) return NaN;
    var n = 0;
    for (var i = 0; i < 4; i++) { if (!/^\d{1,3}$/.test(p[i])) return NaN; var o = +p[i]; if (o > 255) return NaN; n = n * 256 + o; }
    return n;
  }
  function n2ip(n) { return [n >>> 24, (n >>> 16) & 255, (n >>> 8) & 255, n & 255].join('.'); }
  function parseMask(s) {
    s = String(s).trim().replace(/^\//, '');
    var bits;
    if (/^\d{1,2}$/.test(s)) { bits = +s; if (bits > 32) return null; }
    else {
      var m = ip2n(s); if (!isFinite(m)) return null;
      var b = m.toString(2); while (b.length < 32) b = '0' + b;
      if (!/^1*0*$/.test(b)) return null;
      bits = b.indexOf('0') < 0 ? 32 : b.indexOf('0');
    }
    var mask = bits === 0 ? 0 : (0xFFFFFFFF << (32 - bits)) >>> 0;
    return { bits: bits, mask: mask };
  }
  TOOLS.subnet = function (root) {
    root.innerHTML =
      '<span class="label">Try it · same subnet or not?</span>' +
      '<div class="tool-grid">' +
      field('Device A IP address', '<input data-k="a" type="text" value="192.168.10.21">') +
      field('Device B IP address', '<input data-k="b" type="text" value="192.168.10.140">') +
      field('Subnet mask (or /prefix)', '<input data-k="m" type="text" value="255.255.255.0">') +
      '</div><div class="tool-out" data-out></div>';
    var k = function (n) { return $('[data-k="' + n + '"]', root); };
    function info(ip, m) {
      var net = (ip & m.mask) >>> 0, bc = (net | (~m.mask >>> 0)) >>> 0;
      return { net: net, bc: bc };
    }
    function run() {
      var a = ip2n(k('a').value), b = ip2n(k('b').value), m = parseMask(k('m').value), out = '';
      if (!m) { $('[data-out]', root).innerHTML = line('bad', 'The mask is not valid. Use e.g. 255.255.255.0 or /24 — the 1-bits must all be on the left.'); return; }
      var hosts = m.bits >= 31 ? (m.bits === 31 ? 2 : 1) : Math.pow(2, 32 - m.bits) - 2;
      out += line('muted', 'Mask ' + n2ip(m.mask) + ' = /' + m.bits + ' · ' + hosts.toLocaleString() + ' usable addresses per subnet');
      var rows = '';
      [['A', a], ['B', b]].forEach(function (x) {
        if (!isFinite(x[1])) { rows += '<tr><td>' + x[0] + '</td><td colspan="3">not a valid IPv4 address</td></tr>'; return; }
        var i = info(x[1], m), note = '';
        if (m.bits < 31 && x[1] === i.net) note = ' <span class="bad">(this is the network address — not usable by a device)</span>';
        if (m.bits < 31 && x[1] === i.bc) note = ' <span class="bad">(this is the broadcast address — not usable by a device)</span>';
        rows += '<tr><td>' + x[0] + '</td><td>' + n2ip(x[1]) + note + '</td><td>' + n2ip(i.net) + '</td><td>' + n2ip(i.bc) + '</td></tr>';
      });
      out += '<table class="mini"><thead><tr><th></th><th>Address</th><th>Network</th><th>Broadcast</th></tr></thead><tbody>' + rows + '</tbody></table>';
      if (isFinite(a) && isFinite(b)) {
        if (info(a, m).net === info(b, m).net) out += line('ok', 'Same subnet — the two devices can talk directly (BACnet/IP broadcasts such as Who-Is will reach both).');
        else out += line('bad', 'Different subnets — traffic must go through a router (default gateway). BACnet/IP broadcasts will not cross without a BBMD.');
      }
      $('[data-out]', root).innerHTML = out;
    }
    root.addEventListener('input', run); run();
  };

  /* ---------------------------------------------------------------- modbus */
  function reg(v) {
    v = String(v).trim();
    if (v === '') return NaN;
    var n = /^0x/i.test(v) ? parseInt(v, 16) : (/^-/.test(v) ? parseInt(v, 10) + 65536 : parseInt(v, 10));
    return (isFinite(n) && n >= 0 && n <= 65535 && /^(0x[0-9a-f]+|-?\d+)$/i.test(v)) ? n : NaN;
  }
  function hex4(n) { var s = n.toString(16).toUpperCase(); while (s.length < 4) s = '0' + s; return '0x' + s; }
  TOOLS.modbus = function (root) {
    root.innerHTML =
      '<span class="label">Try it · Modbus register decoder</span>' +
      '<div class="tool-grid">' +
      field('Register 1 (decimal or 0x hex)', '<input data-k="r1" type="text">') +
      field('Register 2 (for 32-bit values)', '<input data-k="r2" type="text">') +
      field('Scale (multiply by)', '<input data-k="sc" type="text" value="1">') +
      '</div><div class="tool-out" data-out></div>' +
      '<div class="tool-grid" style="margin-top:14px">' +
      field('Encode a float32 → two registers', '<input data-k="fv" type="text" value="23.5">') +
      '</div><div class="tool-out" data-enc></div>';
    var k = function (n) { return $('[data-k="' + n + '"]', root); };
    k('r1').value = root.dataset.r1 || '16824'; k('r2').value = root.dataset.r2 || '0';
    function run() {
      var r1 = reg(k('r1').value), r2 = reg(k('r2').value), sc = num(k('sc').value), out = '';
      if (!isFinite(sc)) sc = 1;
      if (!isFinite(r1)) { out = line('bad', 'Register 1 must be 0–65535 (or a negative number from −32768, or hex like 0x41B4).'); }
      else {
        var s16 = r1 > 32767 ? r1 - 65536 : r1, rows = '';
        rows += '<tr><td>Unsigned 16-bit</td><td>' + r1 + '</td><td>' + fmt(r1 * sc, 4) + '</td></tr>';
        rows += '<tr><td>Signed 16-bit</td><td>' + s16 + '</td><td>' + fmt(s16 * sc, 4) + '</td></tr>';
        rows += '<tr><td>Hex · binary</td><td colspan="2">' + hex4(r1) + ' · ' + ('0000000000000000' + r1.toString(2)).slice(-16).replace(/(\d{4})(?=\d)/g, '$1 ') + '</td></tr>';
        if (isFinite(r2)) {
          var A = r1 >> 8, B = r1 & 255, C = r2 >> 8, D = r2 & 255, dv = new DataView(new ArrayBuffer(4));
          var orders = [['ABCD — big-endian (Modbus default)', [A, B, C, D]], ['CDAB — word swap', [C, D, A, B]], ['BADC — byte swap', [B, A, D, C]], ['DCBA — little-endian', [D, C, B, A]]];
          orders.forEach(function (o, i) {
            o[1].forEach(function (x, j) { dv.setUint8(j, x); });
            var f = dv.getFloat32(0, false), u = dv.getUint32(0, false), s = dv.getInt32(0, false);
            rows += '<tr><td>32-bit ' + o[0] + '</td><td>float ' + (isFinite(f) ? fmt(f * sc, 4) : 'NaN') + '</td><td>uint ' + fmt(u * sc, 4) + (i === 0 ? ' · int ' + fmt(s * sc, 4) : '') + '</td></tr>';
          });
        }
        out = '<table class="mini"><thead><tr><th>Read as</th><th>Raw</th><th>× scale</th></tr></thead><tbody>' + rows + '</tbody></table>';
        out += line('muted', 'If one row gives a sensible value and the others give nonsense, that row is the data type and byte order the device uses.');
      }
      $('[data-out]', root).innerHTML = out;
      var fv = num(k('fv').value), enc = '';
      if (isFinite(fv)) {
        var dv2 = new DataView(new ArrayBuffer(4)); dv2.setFloat32(0, fv, false);
        var hi = dv2.getUint16(0, false), lo = dv2.getUint16(2, false);
        enc = 'ABCD order: register 1 = <b>' + hi + '</b> (' + hex4(hi) + '), register 2 = <b>' + lo + '</b> (' + hex4(lo) + ') · CDAB order: swap the two registers.';
      }
      $('[data-enc]', root).innerHTML = enc;
    }
    root.addEventListener('input', run); run();
  };

  /* ---------------------------------------------------------------- pid */
  TOOLS.pid = function (root) {
    root.innerHTML =
      '<span class="label">Try it · PID playground (AHU cooling valve)</span>' +
      '<p class="tool-intro">The controller opens a chilled-water valve to pull the return air temperature down to 24 °C. At 10 minutes a load arrives (people and sun, +2 K). Move the sliders and watch the response.</p>' +
      '<div class="tool-grid">' +
      field('Proportional band (K): <b data-v="pb"></b>', '<input data-k="pb" type="range" min="0.5" max="20" step="0.5" value="4">') +
      field('Integral time Ti (s, 0 = off): <b data-v="ti"></b>', '<input data-k="ti" type="range" min="0" max="900" step="10" value="0">') +
      field('Derivative time Td (s): <b data-v="td"></b>', '<input data-k="td" type="range" min="0" max="60" step="5" value="0">') +
      '</div><div class="tool-presets">Presets: <button type="button" data-p="4,0,0">P only</button><button type="button" data-p="4,240,0">P + I (good)</button><button type="button" data-p="1,40,0">Too aggressive</button><button type="button" data-p="15,900,0">Too sluggish</button></div>' +
      '<div class="pid-chart" data-chart></div><div class="tool-out" data-out></div>';
    var k = function (n) { return $('[data-k="' + n + '"]', root); };
    function sim(pb, ti, td) {
      var Kp = 100 / pb, dt = 1, N = 1200, tau = 150, L = 30, G = 0.1, T0 = 30, SP = 24;
      var pv = 27, I = 0, u = 0, hist = [], uBuf = [], prevPv = pv, res = { pv: [], u: [] };
      for (var t = 0; t <= N; t++) {
        var load = t >= 600 ? 2 : 0;
        var e = pv - SP;                                   // reverse acting: too warm → open valve
        var P = Kp * e, D = Kp * td * (pv - prevPv) / dt;
        var Inew = ti > 0 ? I + Kp * e * dt / ti : 0;
        var raw = P + Inew + D;
        u = Math.max(0, Math.min(100, raw));
        if (ti > 0 && !((raw > 100 && e > 0) || (raw < 0 && e < 0))) I = Inew;   // anti-windup
        uBuf.push(u);
        var ud = uBuf.length > L ? uBuf[uBuf.length - 1 - L] : 0;
        prevPv = pv;
        pv = pv + dt / tau * ((T0 + load - G * ud) - pv);
        res.pv.push(pv); res.u.push(u);
      }
      return res;
    }
    function run() {
      var pb = num(k('pb').value), ti = num(k('ti').value), td = num(k('td').value);
      $('[data-v="pb"]', root).textContent = fmt(pb, 1) + ' K (gain ' + fmt(100 / pb, 1) + ' %/K)';
      $('[data-v="ti"]', root).textContent = ti ? ti + ' s' : 'off';
      $('[data-v="td"]', root).textContent = td ? td + ' s' : 'off';
      var r = sim(pb, ti, td), W = 640, H = 270, x0 = 44, x1 = 600, y0 = 236, y1 = 16;
      var X = function (t) { return x0 + t / 1200 * (x1 - x0); };
      var Yt = function (v) { return y0 - (Math.max(20, Math.min(30, v)) - 20) / 10 * (y0 - y1); };
      var Yu = function (v) { return y0 - v / 100 * (y0 - y1); };
      var pv = '', uu = '';
      for (var t = 0; t <= 1200; t += 4) { pv += X(t) + ',' + Yt(r.pv[t]) + ' '; uu += X(t) + ',' + Yu(r.u[t]) + ' '; }
      var g = '';
      for (var v = 20; v <= 30; v += 2) g += '<line x1="' + x0 + '" x2="' + x1 + '" y1="' + Yt(v) + '" y2="' + Yt(v) + '" class="d-line d-thin" opacity=".25"/><text x="' + (x0 - 6) + '" y="' + Yt(v) + '" text-anchor="end" class="d-ts">' + v + '°</text>';
      for (var p = 0; p <= 100; p += 50) g += '<text x="' + (x1 + 6) + '" y="' + Yu(p) + '" text-anchor="start" class="d-ts">' + p + '%</text>';
      for (var m = 0; m <= 20; m += 5) g += '<text x="' + X(m * 60) + '" y="' + (y0 + 16) + '" text-anchor="middle" class="d-ts">' + m + ' min</text>';
      g += '<line x1="' + X(600) + '" x2="' + X(600) + '" y1="' + y1 + '" y2="' + y0 + '" class="d-line d-dash d-thin"/><text x="' + (X(600) + 4) + '" y="' + (y1 + 8) + '" class="d-ts" text-anchor="start">load +2 K</text>';
      g += '<line x1="' + x0 + '" x2="' + x1 + '" y1="' + Yt(24) + '" y2="' + Yt(24) + '" class="d-warmline" stroke-dasharray="6 5" style="stroke-width:1.5"/>';
      g += '<polyline points="' + uu + '" fill="none" style="stroke:var(--ok);stroke-width:1.6;opacity:.85"/>';
      g += '<polyline points="' + pv + '" fill="none" class="d-aline"/>';
      g += '<text x="' + (x0 + 6) + '" y="' + (y0 - 10) + '" class="d-ts" text-anchor="start"><tspan style="fill:var(--accent)">━ return air temp</tspan>   <tspan style="fill:var(--bad)">╍ setpoint 24 °C</tspan>   <tspan style="fill:var(--ok)">━ valve %</tspan></text>';
      $('[data-chart]', root).innerHTML = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="PID response chart">' + g + '</svg>';
      // metrics
      var minPv = 99, settle = 0, rev = 0, dir = 0;
      for (var i = 0; i < 600; i++) { minPv = Math.min(minPv, r.pv[i]); if (Math.abs(r.pv[i] - 24) > 0.3) settle = i; }
      for (var j = 5; j < 1200; j++) { var du = r.u[j] - r.u[j - 5]; if (Math.abs(du) > 1.5) { var nd = du > 0 ? 1 : -1; if (dir && nd !== dir) rev++; dir = nd; } }
      var off1 = r.pv[599] - 24, off2 = r.pv[1200] - 24, over = 24 - minPv, out = '';
      out += line('muted', 'Overshoot: ' + fmt(Math.max(0, over), 2) + ' K · offset before the load: ' + fmt(off1, 2) + ' K · offset at the end: ' + fmt(off2, 2) + ' K · within ±0.3 K after ' + (settle >= 599 ? 'never (in 10 min)' : fmt(settle / 60, 1) + ' min'));
      if (rev > 6) out += line('bad', 'Hunting — the valve keeps swinging. Widen the proportional band and/or lengthen the integral time.');
      else if (Math.abs(off2) > 0.3 || Math.abs(off1) > 0.3) out += line('warn', 'Offset — the temperature settles away from setpoint. ' + (ti ? 'Integral action is too slow to remove it in time; shorten Ti.' : 'P-only control always leaves an offset; add integral action (Ti).'));
      else if (settle > 420) out += line('warn', 'Sluggish — it gets there, but slowly. Narrow the proportional band or shorten Ti a little.');
      else out += line('ok', 'Good — reaches setpoint, recovers from the load and does not hunt.');
      $('[data-out]', root).innerHTML = out;
    }
    root.addEventListener('input', run);
    $$('[data-p]', root).forEach(function (b) {
      b.addEventListener('click', function () { var p = b.getAttribute('data-p').split(','); k('pb').value = p[0]; k('ti').value = p[1]; k('td').value = p[2]; run(); });
    });
    run();
  };

  /* ---------------------------------------------------------------- ahuseq */
  TOOLS.ahuseq = function (root) {
    root.innerHTML =
      '<span class="label">Try it · AHU-01 start/stop sequence</span>' +
      '<p class="tool-intro">Step through AHU-01’s day. Tick a fault before or during the sequence to see how the logic reacts.</p>' +
      '<div class="seq-faults"><label><input type="checkbox" data-f="hand"> HOA switch not in Auto</label>' +
      '<label><input type="checkbox" data-f="nostatus"> Fan fails to prove (no run status)</label>' +
      '<label><input type="checkbox" data-f="fire"> Fire alarm signal</label>' +
      '<label><input type="checkbox" data-f="filter"> Filter dirty</label></div>' +
      '<div class="seq-panel" data-panel></div>' +
      '<div class="seq-btns"><button type="button" class="btn" data-a="next">Next step ▸</button><button type="button" class="btn ghost" data-a="reset">Reset</button></div>' +
      '<ol class="seq-log" data-log></ol>';
    var S, f = function (n) { return $('[data-f="' + n + '"]', root).checked; };
    function reset() {
      S = { step: 0, clock: '07:59', sched: 'Unoccupied', cmd: 'OFF', sts: 'OFF', hz: 0, dmp: 0, vlv: 0, alarm: '—', mode: 'Off', done: false };
      $('[data-log]', root).innerHTML = ''; draw();
    }
    function log(text, cls) { var li = document.createElement('li'); li.innerHTML = '<span class="clk">' + S.clock + '</span> ' + text; if (cls) li.className = cls; $('[data-log]', root).appendChild(li); }
    function draw() {
      var cell = function (a, b, cls) { return '<div><span>' + a + '</span><b class="' + (cls || '') + '">' + b + '</b></div>'; };
      $('[data-panel]', root).innerHTML =
        cell('Mode', S.mode) + cell('Schedule', S.sched) + cell('Start command · DO', S.cmd) + cell('Run status · DI', S.sts, S.sts === 'ON' ? 'ok' : '') +
        cell('VFD speed', S.hz + ' Hz') + cell('Fresh air damper · AO', S.dmp + ' %') + cell('CHW valve · AO', S.vlv + ' %') +
        cell('Alarm', S.alarm, S.alarm === '—' ? '' : (/FIRE|FAIL/.test(S.alarm) ? 'bad' : 'warn'));
      $('[data-a="next"]', root).disabled = S.done;
    }
    function lockout(alarm, text) { S.cmd = 'OFF'; S.hz = 0; S.vlv = 0; S.dmp = 0; S.sts = 'OFF'; S.alarm = alarm; S.mode = 'Locked out'; S.done = true; log(text, 'bad'); }
    function fireCheck() {
      if (f('fire') && S.step > 0 && S.step < 9) {
        lockout('FIRE SHUTDOWN', '<b>Fire signal.</b> The hard-wired trip in the starter circuit stops the fan at once — even if the BMS failed. The BMS sees the fire DI, sets the start command OFF, closes the valve and the fresh air damper, and raises a <b>critical</b> alarm. AHU-01 stays off until the fire system is reset and an operator resets the alarm.');
        return true;
      }
      return false;
    }
    function next() {
      if (S.done) return;
      if (fireCheck()) return draw();
      switch (S.step) {
        case 0: S.clock = '08:00'; S.sched = 'Occupied'; S.mode = 'Starting'; log('Schedule changes to <b>Occupied</b>. Start request.'); break;
        case 1:
          if (f('hand')) { S.alarm = 'NOT IN AUTO'; S.mode = 'Blocked'; S.done = true; log('Permissive check: HOA switch is <b>not in Auto</b>. The BMS cannot control the fan, so it does not start and raises a “not in Auto” alarm.', 'bad'); break; }
          log('Permissives OK: Auto selected, no fire signal, no latched fan fault.'); break;
        case 2: S.dmp = 20; log('Fresh air damper commanded to its <b>minimum position (20 %)</b> so the fan does not start against a closed intake.'); break;
        case 3: S.cmd = 'ON'; S.hz = 42; S.clock = '08:00:30'; log('Start command <b>ON</b> (DO via interposing relay). The VFD ramps to 42 Hz over about 30 s.'); break;
        case 4:
          if (f('nostatus')) { S.clock = '08:01'; lockout('FAN FAIL', 'No run status within <b>30 s</b> of the start command → <b>FAN FAIL</b> alarm (high priority). Command OFF, valve and damper closed, AHU locked out until an operator resets it.'); break; }
          S.sts = 'ON'; S.clock = '08:00:38'; log('Run status ON after 8 s — <b>fan proven</b>.', 'ok'); break;
        case 5: S.clock = '08:01:40'; S.mode = 'Running'; log('After a 60 s stabilising delay the <b>cooling PID</b> and <b>CO₂ control</b> of the fresh air damper are enabled. Temperature alarms are armed after 15 minutes.'); break;
        case 6: S.clock = '10:30'; S.vlv = 62; S.dmp = 35; log('Normal running: the valve sits at 62 % to hold return air at 24.0 °C; CO₂ is 850 ppm, so the fresh air damper is at 35 %.');
          if (f('filter')) { S.alarm = 'FILTER DIRTY'; log('Filter ΔP switch has been closed for 5 minutes while the fan runs → <b>filter dirty</b> alarm (low priority). The AHU keeps running; maintenance is notified.', 'warn'); }
          break;
        case 7: S.clock = '19:00'; S.sched = 'Unoccupied'; S.mode = 'Stopping'; S.vlv = 0; log('Schedule changes to <b>Unoccupied</b>. Cooling PID disabled; valve driven to 0 %.'); break;
        case 8: S.cmd = 'OFF'; S.hz = 0; S.clock = '19:00:10'; log('Start command <b>OFF</b>. The VFD ramps down.'); break;
        case 9: S.sts = 'OFF'; S.dmp = 0; S.clock = '19:01'; S.mode = 'Off'; S.done = true; log('Run status OFF — fan stopped. Fresh air damper closes. AHU-01 is off until tomorrow’s schedule.', 'ok'); break;
      }
      S.step++;
      draw();
    }
    root.addEventListener('click', function (e) {
      var a = e.target.getAttribute && e.target.getAttribute('data-a');
      if (a === 'next') next(); else if (a === 'reset') reset();
    });
    root.addEventListener('change', function (e) {
      if (e.target.getAttribute('data-f') === 'fire' && f('fire') && S.step > 0 && !S.done) { fireCheck(); draw(); }
    });
    reset();
  };

  $$('.tool[data-tool]').forEach(function (el) { var fn = TOOLS[el.getAttribute('data-tool')]; if (fn) fn(el); });
})();
