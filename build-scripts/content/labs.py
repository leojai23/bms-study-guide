# -*- coding: utf-8 -*-
"""The five Level 1 practical labs. Together they produce AHU-01's control package.
Terminal and cable numbers follow one consistent example design used across all labs."""
import csv
import io

from bms_common import (table, steps, bullets, callout, fig, svg, defs, t, rect, box, line, path, circle,
                        tool, item_url, page_url)
import syllabus as S

# ==========================================================================
# The AHU-01 point list — single source for Labs 1, 2 and the CSV download
# ==========================================================================

P = "B1-L03-AHU01-"
POINTS = [
    # name, description, type, signal/device, range/states, normal, alarm, trend, terminal, cable
    ("SF-CMD", "Supply fan start/stop command", "DO", "Relay → interposing relay KA1 → VFD run input", "Off / On", "Off", "—", "COV", "DO1", "C08"),
    ("SF-STS", "Supply fan run status", "DI", "VFD run relay, volt-free NO", "Stopped / Running", "Open = stopped", "Fan fail: cmd On & sts Off > 30 s (high)", "COV", "UI6", "C09"),
    ("SF-FLT", "Supply fan VFD fault", "DI", "VFD fault relay, closed when healthy", "Normal / Fault", "Closed = normal", "Fault (high)", "COV", "UI7", "C09"),
    ("SF-AM", "Supply fan auto/manual status", "DI", "HOA auxiliary contact, closed in Auto", "Manual / Auto", "Closed = Auto", "Not in Auto while scheduled (medium)", "COV", "UI8", "C10"),
    ("FLT-DP", "Filter dirty", "DI", "Filter ΔP switch, NO, closes on high ΔP", "Clean / Dirty", "Open = clean", "Dirty after fan proven 5 min, 5 min delay (low)", "COV", "UI9", "C11"),
    ("FIRE", "Fire shutdown status", "DI", "FAS interface relay, closed when healthy", "Normal / Fire", "Closed = normal", "Fire (critical)", "COV", "UI10", "C12"),
    ("RAT", "Return air temperature", "AI", "10k NTC duct probe", "0–50 °C", "—", "High > 27 °C 15 min, clears < 26 °C (medium)", "5 min", "UI1", "C01"),
    ("SAT", "Supply air temperature", "AI", "10k NTC duct probe", "0–50 °C", "—", "Low < 10 °C 5 min (medium); high > 18 °C with valve > 90 % (high)", "5 min", "UI2", "C02"),
    ("RAH", "Return air humidity", "AI", "Transmitter 0–10 V, 3-wire", "0–100 % RH", "—", "High > 65 % 30 min, clears < 60 % (medium)", "5 min", "UI3", "C03"),
    ("RACO2", "Return air CO₂", "AI", "Transmitter 0–10 V, 3-wire", "0–2,000 ppm", "—", "High > 1,200 ppm 30 min (low)", "5 min", "UI4", "C04"),
    ("SAP", "Supply duct static pressure", "AI", "Transmitter 4–20 mA, 2-wire", "0–500 Pa", "—", "High > 450 Pa 2 min (high); sensor fault < 3.6 mA", "1 min", "UI5", "C05"),
    ("CHWV", "Chilled water valve command", "AO", "0–10 V to 24 V AC modulating actuator", "0–100 %", "—", "—", "5 min", "AO1", "C06"),
    ("SF-SPD", "Supply fan speed reference", "AO", "0–10 V to VFD analogue input (0–50 Hz)", "0–100 %", "—", "—", "5 min", "AO2", "C13"),
    ("FAD", "Fresh air damper command", "AO", "0–10 V to 24 V AC spring-return actuator", "0–100 %", "—", "—", "5 min", "AO3", "C07"),
]
MODBUS = [
    ("SF-HZ", "Supply fan output frequency", "Modbus", "VFD reg. 40001, UINT16 × 0.1", "0–50 Hz", "5 min"),
    ("SF-AMP", "Supply fan motor current", "Modbus", "VFD reg. 40002, UINT16 × 0.1", "A", "5 min"),
    ("SF-KW", "Supply fan power", "Modbus", "VFD reg. 40003, UINT16 × 0.1", "kW", "15 min"),
    ("SF-KWH", "Supply fan energy", "Modbus", "VFD reg. 40004–5, UINT32", "kWh", "1 h"),
    ("SF-FCODE", "VFD last fault code", "Modbus", "VFD reg. 40006, UINT16", "code", "COV"),
]
SOFT = [
    ("RAT-SP", "Return air temperature setpoint", "AV", "Software", "22–26 °C (24 °C)"),
    ("SAT-LL", "Supply air low-limit setpoint", "AV", "Software", "10–13 °C (11 °C)"),
    ("OCC", "Occupancy mode", "MSV", "From schedule / override", "Unocc / Occ / Override"),
    ("FAD-MIN", "Fresh air damper minimum", "AV", "Software", "20 %"),
    ("SF-RST", "Fan fail reset", "BV", "Operator command", "— / Reset"),
    ("SCHED", "AHU-01 weekly schedule", "Schedule", "Mon–Sat 08:00–19:00", "with holiday calendar"),
]


X1 = [("UI1", "1–2"), ("UI2", "3–4"), ("UI3", "5–7"), ("UI4", "8–10"), ("UI5", "11–12"), ("UI6", "13–14"),
      ("UI7", "15–16"), ("UI8", "17–18"), ("UI9", "19–20"), ("UI10", "21–22"), ("DO1", "23–24"), ("AO1", "25–27"),
      ("AO2", "28–29"), ("AO3", "30–32")]


def point_list_table():
    rows = [(f"<code>{P}{n}</code>", d, ty, sig, rng, norm, alm, tr, term, cab)
            for n, d, ty, sig, rng, norm, alm, tr, term, cab in POINTS]
    return table(["Point name", "Description", "Type", "Signal / device", "Range / states", "Normal",
                  "Alarm", "Trend", "Terminal", "Cable"], rows)


def downloads():
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["Point name", "Description", "Type", "Signal / device", "Range / states", "Normal state",
                "Alarm", "Trend", "Controller", "Terminal", "Cable"])
    for n, d, ty, sig, rng, norm, alm, tr, term, cab in POINTS:
        w.writerow([P + n, d, ty, sig, rng, norm, alm, tr, "DDC-AHU-01", term, cab])
    for n, d, ty, sig, rng, tr in MODBUS:
        w.writerow([P + n, d, ty, sig, rng, "", "", tr, "DDC-AHU-01", "RS485-1", "C14"])
    for n, d, ty, sig, rng in SOFT:
        w.writerow([P + n, d, ty, sig, rng, "", "", "", "DDC-AHU-01", "", ""])
    template = io.StringIO()
    csv.writer(template, lineterminator="\n").writerow(
        ["Point name", "Description", "Type", "Signal / device", "Range / states", "Normal state", "Alarm", "Trend",
         "Controller", "Terminal", "Cable"])
    return {"level-1/labs/ahu-01-point-list.csv": buf.getvalue(),
            "level-1/labs/point-list-template.csv": template.getvalue()}


# ==========================================================================
# Lab diagrams
# ==========================================================================

def d_wiring_schedule():
    i = defs("ws")
    i += t(110, 18, "Panel DDC-AHU-01", "d-t d-tb") + t(400, 18, "Terminals X1", "d-t d-tb") + t(660, 18, "Field device", "d-t d-tb")
    # power block
    i += box(20, 34, 180, 70, "Power", "230 V L/N → Q1 6 A MCB|T1 230/24 V AC 100 VA → F1 2 A|G1 24 V DC 1 A PSU → F2 1 A", "d-warn", "d-ts d-tb")
    i += rect(210, 34, 100, 70, "d-acc", 8) + t(260, 52, "Controller", "d-ts d-tb") + t(260, 68, "G / G0 ← T1", "d-ts") + t(260, 84, "24 V AC", "d-ts")
    short = {"UI1": "10k NTC duct probe", "UI2": "10k NTC duct probe", "UI3": "RH transmitter 0–10 V",
             "UI4": "CO₂ transmitter 0–10 V", "UI5": "pressure transmitter 4–20 mA", "UI6": "VFD run relay",
             "UI7": "VFD fault relay", "UI8": "HOA auxiliary contact", "UI9": "filter ΔP switch",
             "UI10": "FAS interface relay", "DO1": "KA1 → VFD run input", "AO1": "CHW valve actuator 0–10 V",
             "AO2": "VFD speed input 0–10 V", "AO3": "fresh air damper actuator 0–10 V"}
    by_term = {r[8]: r for r in POINTS}
    rows = [(term, by_term[term][0], short[term], by_term[term][9], x1) for term, x1 in X1]
    rows.append(("RS485", "Modbus", "to VFD · 19200 8E1 · A/B/COM", "C14", "33–35"))
    y0 = 124
    for k, (term, name, sig, cab, x1) in enumerate(rows):
        y = y0 + k * 30
        cls = {"UI": "d-acc", "DO": "d-warn", "AO": "d-ok"}.get(term[:2], "d-soft")
        i += rect(210, y, 100, 24, cls, 4) + t(260, y + 12, term, "d-ts d-tb")
        i += line(310, y + 12, 370, y + 12, "d-line")
        i += rect(370, y, 60, 24, "d-box", 4) + t(400, y + 12, x1, "d-ts")
        i += line(430, y + 12, 500, y + 12, "d-aline") + t(465, y + 4, cab, "d-ts d-ta")
        i += rect(500, y, 260, 24, "d-soft", 4) + t(508, y + 12, f"{name} · {sig}", "d-ts", "start")
    y = y0 + len(rows) * 30 + 6
    i += t(20, y + 10, "Colours: blue = universal inputs · amber = digital output (via KA1) · green = analogue outputs · grey = RS485. Spare: UI11, UI12, DO2, AO4 on X1:36–39.", "d-ts", "start")
    return svg(780, y + 26, i, "Wiring schedule for panel DDC-AHU-01")


def d_wiring_details():
    i = defs("wd")
    # (a) DO via interposing relay to VFD
    i += t(130, 16, "(a) Fan start: DO1 → KA1 → VFD", "d-ts d-tb")
    i += box(10, 30, 70, 60, "DO1", "C · NO", "d-acc", "d-ts d-tb")
    i += line(80, 48, 110, 48) + line(80, 72, 110, 72)
    i += rect(110, 36, 60, 48, "d-box", 4) + t(140, 52, "KA1", "d-ts d-tb") + t(140, 68, "coil 24 V AC", "d-ts")
    i += t(95, 102, "24 V AC via DO1", "d-ts")
    i += line(170, 50, 205, 50) + line(205, 50, 222, 38) + line(222, 50, 250, 50)
    i += line(170, 72, 250, 72)
    i += t(215, 30, "NO", "d-ts")
    i += box(178, 108, 90, 34, "VFD DI1 / DCOM", "", "d-soft", "d-ts", 4)
    i += path("M250,50 L262,50 L262,108", "d-line") + path("M250,72 L256,72 L256,108", "d-line")
    # (b) 2-wire 4-20 mA
    i += t(400, 16, "(b) Duct pressure: 4–20 mA loop", "d-ts d-tb")
    i += box(300, 30, 76, 46, "G1 24 V DC", "+ via F2", "d-warn", "d-ts d-tb")
    i += box(420, 100, 90, 42, "Transmitter", "0–500 Pa", "d-box", "d-ts d-tb")
    i += box(420, 30, 90, 46, "UI5 (mA)", "+ / COM", "d-acc", "d-ts d-tb")
    i += path("M338,76 L338,121 L418,121", "d-line", end="wd") + t(332, 104, "+", "d-t d-tb", "end")
    i += path("M512,121 L530,121 L530,53 L512,53", "d-line", end="wd")
    i += path("M420,64 L392,64 L392,76", "d-line") + t(400, 92, "COM → 0 V", "d-ts")
    # (c) modulating actuator
    i += t(660, 16, "(c) CHW valve: AO1 + 24 V AC", "d-ts d-tb")
    i += box(570, 30, 76, 66, "Controller", "G (24 V AC)|G0 (common)|AO1 (Y)", "d-acc", "d-ts d-tb")
    i += box(690, 30, 80, 66, "Actuator", "24 V AC|common|Y 0–10 V", "d-box", "d-ts d-tb")
    for k, y in enumerate((48, 63, 78)):
        i += line(646, y, 690, y, "d-line" if k < 2 else "d-aline")
    i += t(668, 112, "3 cores + screen (C06)", "d-ts")
    i += t(668, 128, "common shared by supply and signal", "d-ts")
    return svg(780, 150, i, "Wiring details for three typical circuits")


def d_lab4_loop():
    i = defs("l4")
    i += box(30, 40, 130, 70, "G1  24 V DC PSU", "+ / −", "d-warn")
    i += box(260, 150, 160, 70, "Pressure transmitter", "0–500 Pa · 2-wire|+ and − terminals", "d-box")
    i += box(520, 40, 200, 70, "DDC-AHU-01  UI5", "set to 4–20 mA|internal 250 Ω burden", "d-acc")
    i += path("M95,110 L95,185 L258,185", "d-line", end="l4") + t(100, 150, "X1:11 → C05 core 1 (+24 V)", "d-ts", "start")
    i += rect(150, 172, 40, 26, "d-warn", 4) + t(170, 185, "F2", "d-ts d-tb")
    i += path("M422,185 L620,185 L620,112", "d-line", end="l4") + t(430, 170, "C05 core 2 → X1:12 → UI5", "d-ts", "start")
    i += path("M520,62 L200,62 L200,75 L162,75", "d-line", end="l4") + t(340, 52, "UI5 COM → PSU 0 V", "d-ts")
    i += circle(600, 185, 14, "d-ok") + t(600, 185, "mA", "d-ts d-tb") + t(600, 214, "meter in series", "d-ts") + t(600, 228, "(test terminal)", "d-ts")
    i += t(390, 252, "One current flows round the whole loop: + 24 V → transmitter → UI5 → 0 V", "d-ts d-ta")
    return svg(760, 265, i, "AHU-01 duct pressure 4–20 mA loop with terminal and cable numbers")


# ==========================================================================
# Lab content
# ==========================================================================

def _read_first(root, ids):
    out = []
    for pid in ids:
        for m in S.MODULES:
            for p_, slug, title in m["pages"]:
                if p_ == pid:
                    out.append(f'<a href="{root}{page_url(p_, slug)}">{p_.replace("-", ".")} {title}</a>')
    return "<br>".join(out)


LABS = {
    "L2": dict(
        time="About 90 min", lede="Build the complete point list for AHU-01 — the document every other part of the project is built from.",
        keywords="point list I/O schedule tag naming CSV template",
        read=["4-2", "4-6", "3-8", "6-5"],
        needs=["A spreadsheet (Excel, LibreOffice or Google Sheets)", "The AHU-01 schematic on the Level 1 overview",
               "The blank template: <a href=\"point-list-template.csv\" download>point-list-template.csv</a>"],
        produce="A point list with every hard-wired, network and software point of AHU-01, plus an I/O summary and a controller choice.",
        tasks=[
            ("1 · List the devices", "<p>From the AHU-01 schematic and device list, write down every device: sensors, actuators, the VFD, "
             "the filter switch, the fire interface. Next to each, note what the BMS needs from it (status, command, value).</p>"),
            ("2 · Name every point", "<p>Use the convention from page 4.6: <code>B1-L03-AHU01-</code> followed by a short point code "
             "(SF-CMD, RAT…). Keep the codes consistent — the same code means the same thing on every AHU.</p>"),
            ("3 · Fill in the columns", "<p>For each point: description, I/O type, signal and device, range or states, the normal "
             "state of digital inputs, alarm limits with delay and priority, trend interval. Use pages 3.x and 6.5 for the values.</p>"),
            ("4 · Add network and software points", "<p>Add the VFD's Modbus points (page 5.3) and the software points: setpoints, "
             "occupancy mode, schedule, reset command.</p>"),
            ("5 · Assign terminals", "<p>Group the inputs on universal inputs, outputs on DO and AO terminals, and leave spares. "
             "Give every field cable a number. Lab 1 uses this assignment.</p>"),
            ("6 · Summarise and size", "<p>Count points by type, add about 20 % spare, and state the minimum controller I/O you need.</p>"),
        ],
        checklist=["Every device on the schematic has at least one point", "Every point name follows the convention exactly",
                   "Every DI has a normal state", "Every analogue point has a range and units",
                   "Alarms have a limit, delay, enable condition and priority", "Network points include data type and scale",
                   "Software setpoints have limits", "Terminals are unique and spares are listed", "I/O summary includes spare capacity"],
        model=lambda root: (
            "<p>Download the model as a spreadsheet: <a href=\"ahu-01-point-list.csv\" download>ahu-01-point-list.csv</a></p>"
            "<h3>Hard-wired points</h3>" + point_list_table()
            + "<h3>Network points (Modbus RTU from the VFD, address 1, 19200 8E1)</h3>"
            + table(["Point name", "Description", "Source", "Units", "Trend"],
                    [(f"<code>{P}{n}</code>", d, sig, rng, tr) for n, d, _t, sig, rng, tr in MODBUS])
            + "<h3>Software points</h3>"
            + table(["Point name", "Description", "Object", "Source", "Range / default"],
                    [(f"<code>{P}{n}</code>", d, ty, sig, rng) for n, d, ty, sig, rng in SOFT])
            + "<h3>I/O summary and controller choice</h3>"
            + table(["Type", "Used", "+ ~20 % spare", "Provide"], [
                ("Universal inputs (5 AI + 5 DI)", "10", "2", "12 UI"),
                ("Digital outputs", "1", "1", "2 DO"),
                ("Analogue outputs", "3", "1", "4 AO"),
                ("RS485 port", "1", "—", "1"),
            ], "plain")
            + "<p>A plant controller with at least <strong>12 UI, 2 DO, 4 AO and one RS485 port</strong> (or a smaller controller plus "
              "an I/O module) covers AHU-01 with spare capacity.</p>"),
    ),
    "L4": dict(
        time="About 60 min (+ 30 min with hardware)", lede="Wire, scale, configure and fault-find AHU-01's 4–20 mA duct pressure sensor.",
        keywords="4-20 mA loop pressure transmitter wiring scaling troubleshooting",
        read=["4-3", "3-3", "4-5", "4-1"],
        needs=["Pen and paper or a drawing tool", "The scaling calculator below",
               "Optional hardware: 24 V DC supply, a 2-wire 4–20 mA transmitter or loop calibrator, a 250 Ω resistor, a multimeter"],
        produce="A loop drawing, a scaling table, the AI configuration, a test record and answers to six fault cases.",
        tasks=[
            ("1 · Draw the loop", "<p>Draw the 2-wire loop for the duct pressure sensor: 24 V DC supply (G1) with its fuse (F2), "
             "transmitter + and −, controller input UI5 set to mA, and the return to 0 V. Add terminal numbers (X1:11, X1:12) and "
             "cable C05. Mark where you would connect a meter in series.</p>"),
            ("2 · Make the scaling table", "<p>For a 0–500 Pa transmitter, calculate the current at 0, 100, 250, 400 and 500 Pa, and "
             "the pressure for 6, 10 and 18 mA. Check your answers with the calculator.</p>" + tool("scale", type="4-20", lo="0", hi="500", u="Pa", sig="10")),
            ("3 · Check the voltage budget", "<p>The transmitter needs at least 12 V. The controller input has a 250 Ω burden, and "
             "the 60 m of 0.75 mm² cable has about 3 Ω. Is 24 V enough? What is the largest burden the loop could take?</p>"),
            ("4 · Configure the input", "<p>Write down the AI settings: signal type, range, units, filtering, and what the "
             "controller should do below 3.6 mA and above 21 mA.</p>"),
            ("5 · Test it", "<p>Write a short test procedure: what you measure, where, and the expected values. With hardware: "
             "build the loop on the bench with a 250 Ω resistor in place of the controller and measure the voltage across it "
             "(1–5 V) as you change the pressure or the calibrator output.</p>"),
            ("6 · Fault cases", "<p>Diagnose each: (a) BMS shows sensor fault, loop current 0 mA; (b) 3.0 mA; (c) 22.5 mA; "
             "(d) BMS shows 500 Pa while a hand-held manometer reads 250 Pa; (e) the value drops to zero whenever the panel door "
             "is opened; (f) reading correct, but swings ±40 Pa when the VFD speeds up.</p>"),
        ],
        checklist=["Loop drawn with polarity, fuse, terminals and cable number", "Scaling table complete and checked",
                   "Voltage budget calculated", "AI configuration written, including fault limits",
                   "Test procedure lists measurement points and expected values", "All six fault cases answered"],
        model=lambda root: (
            fig(d_lab4_loop(), "Model loop drawing.")
            + "<h3>Scaling</h3>"
            + table(["Pressure (Pa)", "0", "100", "250", "400", "500"], [("Current (mA)", "4.0", "7.2", "12.0", "16.8", "20.0")], "plain")
            + "<p>6 mA → 62.5 Pa · 10 mA → 187.5 Pa · 18 mA → 437.5 Pa. (Pa = (mA − 4) ÷ 16 × 500.)</p>"
            + "<h3>Voltage budget</h3>"
            + "<p>At 20 mA: burden 250 Ω × 0.02 A = 5 V; cable 3 Ω × 0.02 A = 0.06 V. 24 − 5 − 0.06 = 18.9 V across the transmitter, "
              "above its 12 V minimum — fine. Largest total loop resistance: (24 − 12) ÷ 0.02 = 600 Ω.</p>"
            + "<h3>AI configuration</h3>"
            + table(["Setting", "Value"], [("Type", "Current, 4–20 mA"), ("Range", "4 mA = 0 Pa, 20 mA = 500 Pa"), ("Units", "Pa"),
                                          ("Filter", "Light (a few seconds) to smooth turbulence"),
                                          ("Fault", "Below 3.6 mA or above 21 mA → sensor fault flag, alarm, program uses a fallback")], "plain")
            + "<h3>Test procedure</h3>"
            + steps(["Isolate nothing — this is a 24 V DC loop — but check the panel for other voltages first (page 4.1).",
                     "Measure 24 V DC at G1 and after F2.",
                     "With the fan off, measure the loop current in series at the test terminal: expect about 4 mA (0 Pa).",
                     "Start the fan; compare the BMS value with a hand-held manometer at the same tapping; compare the current with the scaling table.",
                     "Open the loop at the test terminal: the BMS must show a sensor fault and raise the alarm.",
                     "Record supply voltage, current at rest and running, and the BMS values."])
            + "<h3>Fault cases</h3>"
            + table(["Case", "Diagnosis"], [
                ("(a) 0 mA", "Open loop or no supply: check F2, 24 V at G1, terminations and cable continuity"),
                ("(b) 3.0 mA", "Below the live zero: transmitter failing or under-powered — check voltage across it"),
                ("(c) 22.5 mA", "Over-range or failed transmitter; short between cores"),
                ("(d) 500 Pa vs 250 Pa", "Range mismatch: transmitter set to 0–250 Pa while the BMS scales 0–500 Pa (or the reverse)"),
                ("(e) zero when the door opens", "Loose termination or a cable strained by the door hinge"),
                ("(f) swings with VFD speed", "Noise pick-up — cable near the motor cable or screen not earthed; or real turbulence at the tapping"),
            ], "plain")),
    ),
    "L5": dict(
        time="About 90 min", lede="Talk Modbus to a simulated device on your own laptop, read registers, decode them, and make the classic mistakes on purpose.",
        keywords="Modbus Poll ModScan QModMaster simulator registers decode function 03",
        read=["5-3", "5-2", "5-5", "5-1"],
        needs=["A Windows laptop", "A Modbus server simulator — e.g. ModRSsim2 (free)",
               "A Modbus client — Modbus Poll (commercial, free trial), ModScan (commercial) or QModMaster (free)",
               "Optional: a USB–RS485 adapter and a real Modbus device (or two adapters) for Part D"],
        produce="A table of decoded values, notes on the off-by-one and byte-order effects, and a short written explanation of each error you provoked.",
        tasks=[
            ("Before you start", callout("warn", "Practise on simulators, not live plant",
                                         "<p>Reading is harmless; <strong>writing</strong> to a real VFD or chiller changes how it runs. "
                                         "Only write to live equipment with permission and a plan.</p>")
             + "<p>Download tools only from their publishers' official websites. Screens and menu names differ between versions; "
               "the steps below describe what to set, which every tool offers in some form.</p>"),
            ("A · Set up a simulated device", "<p>Start the simulator in <strong>Modbus TCP</strong> mode on port <strong>502</strong> "
             "(your laptop's own address, 127.0.0.1). In its holding-register table, enter these values (documentation numbering):</p>"
             + table(["Register", "Value", "Meaning (from the example VFD map, page 5.3)"], [
                 ("40001", "425", "Output frequency × 0.1 Hz"), ("40002", "183", "Motor current × 0.1 A"),
                 ("40003", "75", "Output power × 0.1 kW"), ("40004", "1", "Energy, high word"), ("40005", "34464", "Energy, low word"),
                 ("40006", "0", "Last fault code"), ("40011", "16828", "A float32, high word"), ("40012", "0", "A float32, low word"),
                 ("40013", "65486", "A signed temperature × 0.1 °C")], "plain")),
            ("B · Connect a client and read", "<p>In the client, create a <strong>Modbus TCP</strong> connection to 127.0.0.1 port 502. "
             "Set up a read of <strong>function 03 (read holding registers)</strong>, slave/unit ID <strong>1</strong>, starting at the "
             "<strong>first holding register</strong>, quantity <strong>13</strong>, every 1 s.</p>"
             + table(["Tool", "Where", "Notes"], [
                 ("Modbus Poll", "Connection → Connect (TCP/IP, 127.0.0.1, 502); Setup → Read/Write Definition: Slave ID 1, Function 03, Address 0, Quantity 13", "Addresses are zero-based by default; the Display menu changes data formats"),
                 ("ModScan", "Connection → Connect; Address 0001, Length 13, Device Id 1, point type 03: HOLDING REGISTER", "Addresses are one-based"),
                 ("QModMaster", "Modbus TCP settings: 127.0.0.1:502; Read Holding Registers, slave 1, start address, 13 registers", "Check whether the start address is entered from 0 or 1"),
             ], "plain")),
            ("C · Decode", "<p>Using the map, convert each value to engineering units: frequency, current, power, energy (combine "
             "40004 and 40005 as one 32-bit value), the float at 40011–40012, and the signed temperature at 40013. Check them "
             "with the decoder:</p>" + tool("modbus", r1="16828", r2="0")),
            ("D · Make the mistakes on purpose", "<p>(1) Start the read one register later — what happens to every value? (2) Display "
             "40011–40012 as a float with the words swapped. (3) Show 40013 as unsigned. (4) Read 3 registers starting beyond the "
             "simulator's configured table, and note the reply. (5) Change the slave ID to 2. (6) Write 400 to 40001 with function 06 "
             "and watch the simulator. Write down what each one looks like — on site you will recognise them instantly.</p>"),
            ("E · Optional: Modbus RTU over RS485", "<p>Connect a USB–RS485 adapter to a real device (or a second adapter running the "
             "simulator on a COM port). Match baud, parity and stop bits (e.g. 19200 8E1), wire A/B/common, terminate both ends, and "
             "repeat Part B with an RTU connection. If nothing answers, apply page 5.5 from the bottom up.</p>"),
        ],
        checklist=["Simulator running with the nine values entered", "Client reads 13 registers without errors",
                   "All values decoded to engineering units", "Off-by-one effect observed and explained",
                   "Word-swap and signed/unsigned effects observed", "Exception or error from an invalid address noted",
                   "Wrong slave ID / timeout observed", "Write with function 06 seen in the simulator"],
        model=lambda root: (
            table(["Register(s)", "Raw", "Decoded"], [
                ("40001", "425", "42.5 Hz"), ("40002", "183", "18.3 A"), ("40003", "75", "7.5 kW"),
                ("40004–40005", "1, 34464", "1 × 65,536 + 34,464 = 100,000 kWh"), ("40006", "0", "no fault"),
                ("40011–40012", "16828, 0 (0x41BC 0x0000)", "23.5 (float32, ABCD)"),
                ("40013", "65486", "signed −50 → −5.0 °C"),
            ], "plain")
            + "<h3>The mistakes</h3>"
            + table(["Mistake", "What you see", "Lesson"], [
                ("Read one register late", "Every value is its neighbour's (frequency shows 18.3…)", "Off-by-one: check the address base"),
                ("Float words swapped", "0x0000 0x41BC → a tiny number, about 2.4e−41", "Try CDAB vs ABCD"),
                ("Signed shown unsigned", "65486 instead of −50", "Set the data type to signed 16-bit"),
                ("Address beyond the table", "Exception 02 (illegal data address), or an error in the tool", "Register does not exist on this device"),
                ("Wrong slave ID", "Timeout / no response (on TCP some simulators answer any ID)", "Address must match"),
                ("Write 400 to 40001 (fn 06)", "Simulator now shows 400; client reads 40.0 Hz", "Writes change the device — be careful on live plant"),
            ], "plain")),
    ),
    "L3": dict(
        time="About 90 min", lede="Write AHU-01's complete start/stop sequence of operation and the test script that proves it.",
        keywords="sequence of operation start stop test script functional test",
        read=["6-1", "6-2", "2-7", "6-5", "6-6"],
        needs=["A word processor", "Your Lab 2 point list", "The AHU-01 sequence stepper below, to check your logic"],
        produce="A sequence of operation in numbered sections, an adjustable-parameter table and a functional test script.",
        tasks=[
            ("1 · Structure", "<p>Use the sections from page 2.7: general, points, modes, enable conditions, start, normal control, stop, "
             "safeties and interlocks, alarms, failure responses, adjustable parameters.</p>"),
            ("2 · Write the steps", "<p>One action per step, in order; give every number and mark it adjustable; say how each step is "
             "proven and what happens if it is not. Use the point names from Lab 2.</p>"),
            ("3 · Cover the failures", "<p>Failure to prove, fan trip while running, fire, HOA not in Auto, sensor failure, loss of the "
             "Modbus link, power return.</p>"),
            ("4 · Write the test script", "<p>For each step and each failure: what the tester does, and the expected result. Use the "
             "stepper to check your expectations:</p>" + tool("ahuseq")),
        ],
        checklist=["Every section present", "Every number given and marked adjustable", "Every start step has its proof",
                   "Every failure path ends in a safe, alarmed state", "Fire behaviour matches page 6.2 (hard-wired + BMS)",
                   "Point names match Lab 2", "Test script covers normal and failure cases"],
        model=lambda root: (
            "<h3>AHU-01 — sequence of operation</h3>"
            + "<p><strong>1 General.</strong> AHU-01 serves the Level 3 offices. It is a constant-volume recirculating AHU with a CHW coil "
              "(2-way valve), a VFD-driven supply fan, a modulating spring-return-closed fresh air damper and a manual return damper. "
              "It is controlled by DDC-AHU-01. Point names refer to the AHU-01 point list.</p>"
            + "<p><strong>2 Modes.</strong> Off · Starting · Running · Stopping · Fire shutdown · Fan-fail lockout · Hand (local).</p>"
            + "<p><strong>3 Enable.</strong> AHU-01 shall run when OCC is Occupied or Override AND SF-AM = Auto AND FIRE = Normal AND no "
              "fan-fail lockout AND the minimum off time (3 min, adj.) has elapsed.</p>"
            + "<p><strong>4 Start.</strong></p>"
            + steps(["Command FAD to FAD-MIN (20 %, adj.).",
                     "Command SF-CMD On and SF-SPD to the speed setpoint (84 % = 42 Hz, adj.).",
                     "If SF-STS is not Running within 30 s (adj.): raise “AHU-01 supply fan failed to start” (high), command SF-CMD Off, FAD 0 %, enter fan-fail lockout.",
                     "After SF-STS Running for 60 s (adj.), enable the RAT and SAT low-limit loops and CO₂ control.",
                     "Arm the temperature and humidity alarms 15 min (adj.) after the fan is proven."])
            + "<p><strong>5 Normal control.</strong> CHWV = min(PI on RAT to RAT-SP 24 °C, PI on SAT to SAT-LL 11 °C), 0–100 %. "
              "FAD = max(FAD-MIN, DCV), where DCV ramps from FAD-MIN at 700 ppm to 50 % at 1,000 ppm RACO2 (adj.). SF-SPD fixed.</p>"
            + "<p><strong>6 Stop.</strong> On OCC Unoccupied: disable loops and drive CHWV to 0 %; command SF-CMD Off; if SF-STS remains "
              "Running 60 s after, raise “failed to stop” (high); command FAD 0 %; start the minimum off timer.</p>"
            + "<p><strong>7 Safeties and interlocks.</strong> The FAS contact, the high static pressure cut-out (manual reset) and the VFD "
              "healthy contact are hard-wired in series upstream of the HOA switch. On FIRE: the fan stops by the hard-wired trip; the "
              "BMS sets SF-CMD Off, CHWV and FAD 0 %, and raises a critical alarm; restart requires FAS reset and operator reset "
              "(SF-RST). CHWV and FAD are 0 % whenever SF-STS is not Running.</p>"
            + "<p><strong>8 Alarms.</strong> As in the point list (page 6.5 settings).</p>"
            + "<p><strong>9 Failure responses.</strong> Fan trips while running (SF-STS lost > 10 s): as failure to start. SF-AM = Manual while "
              "the schedule requires running: “not in Auto” (medium). RAT sensor fault: alarm; CHWV fixed at 50 % (adj.). SAT sensor "
              "fault: alarm; low-limit loop disabled. RACO2 fault: FAD to 35 % (adj.). Modbus loss 60 s: alarm (low); hard-wired control "
              "continues. Power return: wait 60 s (AHU-01 stagger, adj.), then re-evaluate enable.</p>"
            + "<p><strong>10 Adjustable parameters.</strong></p>"
            + table(["Parameter", "Default", "Range"], [
                ("RAT-SP", "24 °C", "22–26 °C"), ("SAT-LL", "11 °C", "10–13 °C"), ("FAD-MIN", "20 %", "10–40 %"),
                ("DCV start / full", "700 / 1,000 ppm", "500–1,200 ppm"), ("Fan proving delay", "30 s", "10–120 s"),
                ("Stabilising delay", "60 s", "0–300 s"), ("Minimum off time", "3 min", "0–15 min"),
                ("Power-return delay", "60 s", "0–600 s"), ("Timed override", "2 h", "0.5–4 h")], "plain")
            + "<h3>Functional test script (extract)</h3>"
            + table(["#", "Action", "Expected result"], [
                ("1", "Set OCC to Occupied", "FAD → 20 %; SF-CMD On; SF-STS Running within 30 s"),
                ("2", "Wait 60 s", "CHWV starts modulating; trend shows RAT moving to 24 °C"),
                ("3", "Open the SF-STS contact at the terminal while running", "After 10 s: fan-fail alarm, fan off, FAD and CHWV 0 %, lockout"),
                ("4", "Operator reset (SF-RST)", "AHU restarts through the full start sequence"),
                ("5", "Switch HOA to Hand", "Fan runs locally; SF-AM Manual; “not in Auto” alarm"),
                ("6", "Operate the FAS interface relay (in Auto and again in Hand)", "Fan stops in both; FIRE alarm critical; CHWV, FAD 0 %"),
                ("7", "Disconnect RAT", "Sensor-fault alarm; CHWV goes to 50 %"),
                ("8", "Set OCC to Unoccupied", "CHWV 0 %, fan stops, SF-STS Stopped within 60 s, FAD 0 %"),
            ], "plain")),
    ),
    "L1": dict(
        time="About 2 hours", lede="Draw AHU-01's control wiring: power, every point from controller terminal to field device, and the terminal schedule.",
        keywords="wiring diagram panel terminal schedule interposing relay transformer",
        read=["1-5", "4-3", "4-4", "4-5", "3-5", "3-7"],
        needs=["Pen and paper, or a free drawing tool such as draw.io", "Your Lab 2 point list (terminals and cable numbers)",
               "Datasheet figures for VA and current (the example figures below are fine)"],
        produce="A wiring diagram for panel DDC-AHU-01 and a terminal schedule.",
        tasks=[
            ("1 · Power section", "<p>Draw the 230 V supply through the MCB (Q1) to the control transformer (T1, 230/24 V AC) and the "
             "24 V DC supply (G1), each with its own fuse. Size T1: controller 20 VA + valve actuator 8 VA + damper actuator 6 VA + "
             "relay coil 1 VA ≈ 35 VA — choose a standard size with plenty of margin. Size G1 for the 4–20 mA loop and the two "
             "transmitters.</p>"),
            ("2 · Inputs", "<p>Draw each input from its UI terminal to the X1 terminal strip, its cable number, and the field device. "
             "Show the NTC sensors as 2-wire, the RH and CO₂ transmitters as 3-wire (24 V, 0 V, signal), the pressure transmitter as a "
             "2-wire loop, and the DI contacts as volt-free pairs.</p>"),
            ("3 · Outputs", "<p>DO1 to the coil of interposing relay KA1; KA1's NO contact to the VFD run input. AO1 and AO3 with the "
             "24 V AC supply to their actuators (3 cores each). AO2 to the VFD's speed input.</p>"),
            ("4 · Communication and fire", "<p>Add RS485 (A, B, common) to the VFD with terminators at both ends. Show the FAS contact "
             "to UI10 and note that a second FAS contact is wired into the starter circuit upstream of the HOA (page 6.2).</p>"),
            ("5 · Terminal schedule", "<p>List every terminal: number, wire/core, cable, destination, signal. Mark spares.</p>"),
            ("6 · Check", "<p>Trace every point in your Lab 2 list through the drawing. Then check segregation: 230 V terminals apart from "
             "24 V signals.</p>"),
        ],
        checklist=["Power section with MCB, transformer, DC supply and fuses", "Transformer sized from a VA total with margin",
                   "Every Lab 2 point appears with terminal and cable number", "DO drives an interposing relay, not the VFD directly",
                   "Transmitters drawn with the right number of wires", "Actuators show supply, common and signal",
                   "RS485 with polarity, common and both terminators", "Fire interface shown (BMS DI + hard-wired trip)",
                   "Terminal schedule complete, with spares", "230 V and 24 V segregated"],
        model=lambda root: (
            fig(d_wiring_schedule(), "Model: wiring schedule for DDC-AHU-01 — controller terminal → X1 terminals → cable → device.")
            + fig(d_wiring_details(), "Model details: interposing relay, 2-wire 4–20 mA loop, and a 24 V AC modulating actuator.")
            + "<h3>Power sizing</h3>"
            + "<p>T1: 35 VA load → choose <strong>100 VA</strong> (margin for actuators moving together and future additions). "
              "G1: loop 20 mA + two transmitters ~ 2 × 30 mA ≈ 0.1 A → a <strong>1 A</strong> 24 V DC supply is ample. Fuses: F1 2 A on "
              "24 V AC, F2 1 A on 24 V DC; Q1 6 A MCB on the 230 V supply.</p>"
            + "<h3>Terminal schedule (extract)</h3>"
            + table(["X1", "Cable / core", "Controller", "Device terminal", "Signal"], [
                ("1–2", "C01 / 1–2", "UI1 / COM", "RAT sensor", "10k NTC"),
                ("3–4", "C02 / 1–2", "UI2 / COM", "SAT sensor", "10k NTC"),
                ("5–7", "C03 / 1–3", "24 V / 0 V / UI3", "RH transmitter: 24 V, 0 V, out", "0–10 V"),
                ("11–12", "C05 / 1–2", "G1 +24 V / UI5", "Pressure transmitter + / −", "4–20 mA"),
                ("13–14", "C09 / 1–2", "UI6 / COM", "VFD run relay", "volt-free"),
                ("15–16", "C09 / 3–4", "UI7 / COM", "VFD fault relay (closed when healthy)", "volt-free"),
                ("21–22", "C12 / 1–2", "UI10 / COM", "FAS interface relay (closed when healthy)", "volt-free"),
                ("23–24", "C08 / 1–2", "KA1 NO contact", "VFD DI1 / DCOM", "volt-free"),
                ("25–27", "C06 / 1–3", "G / G0 / AO1", "CHW valve actuator", "24 V AC + 0–10 V"),
                ("33–35", "C14 / 1–3", "RS485 A / B / COM", "VFD RS485", "Modbus RTU"),
                ("36–39", "—", "UI11, UI12, DO2, AO4", "spare", "—"),
            ], "plain")),
    ),
}


def render(lid, lab, root):
    meta = (f'<div class="lab-meta"><div class="card"><h4>Time</h4><p>{lab["time"]}</p></div>'
            f'<div class="card"><h4>You will produce</h4><p>{lab["produce"]}</p></div>'
            f'<div class="card"><h4>Read first</h4><p>{_read_first(root, lab["read"])}</p></div></div>')
    needs = "<h2>What you need</h2>" + bullets(lab["needs"])
    tasks = "<h2>Tasks</h2>" + "".join(f"<h3>{h}</h3>{body}" for h, body in lab["tasks"])
    check = ("<h2>Self-check</h2><p>Tick each item when your work meets it. Ticks are saved in this browser.</p>"
             f'<ul class="checklist" data-key="{lid}">'
             + "".join(f"<li><input type=\"checkbox\" id=\"{lid}-c{k}\"><label for=\"{lid}-c{k}\">{c}</label></li>"
                       for k, c in enumerate(lab["checklist"])) + "</ul>")
    model = ("<h2>Model answer</h2><p>Finish your own version first — comparing afterwards is where the learning happens.</p>"
             f'<details class="model"><summary>Show the model answer</summary><div>{lab["model"](root)}</div></details>')
    return meta + needs + tasks + check + model
