# -*- coding: utf-8 -*-
"""Module 3 — Sensors and Field Devices. Vendor-neutral; values are typical — always check the datasheet."""
from bms_common import (table, steps, bullets, callout, cards, fig, svg, defs, t, rect, box,
                        line, path, circle, mcq, tool)

# ==========================================================================
# Diagrams
# ==========================================================================

def d_temp_mounting():
    i = defs("tm")
    # room
    i += rect(20, 30, 130, 150, "d-soft", 8) + t(85, 46, "Room sensor", "d-ts d-tb")
    i += rect(66, 90, 38, 52, "d-box", 6) + t(85, 116, "T", "d-t d-tb")
    i += t(85, 196, "wall, 1.2–1.5 m high", "d-ts")
    # duct probe
    i += rect(180, 70, 150, 70, "d-soft", 4) + t(255, 46, "Duct probe", "d-ts d-tb")
    i += line(200, 105, 310, 105, "d-aline", end="tm-a")
    i += rect(245, 52, 22, 18, "d-box", 3) + line(256, 70, 256, 118, "d-line")
    i += t(255, 196, "probe into the airstream", "d-ts")
    # immersion
    i += rect(360, 92, 150, 34, "d-soft", 17) + t(435, 46, "Immersion + thermowell", "d-ts d-tb")
    i += rect(425, 60, 22, 20, "d-box", 3) + rect(430, 80, 12, 36, "d-acc", 4)
    i += line(370, 109, 500, 109, "d-cold", end="tm-a")
    i += t(435, 196, "tip in the middle of the pipe", "d-ts")
    # strap-on
    i += rect(540, 92, 100, 34, "d-soft", 17) + t(590, 46, "Strap-on", "d-ts d-tb")
    i += rect(578, 74, 24, 18, "d-box", 3) + line(560, 92, 620, 92, "d-line d-thin")
    i += t(590, 196, "clamped to the pipe", "d-ts")
    # outdoor
    i += t(715, 46, "Outdoor", "d-ts d-tb")
    for k in range(4):
        i += rect(690, 74 + k * 18, 50, 10, "d-box", 3)
    i += rect(705, 146, 20, 10, "d-box", 2)
    i += t(715, 196, "in a sun shield", "d-ts")
    return svg(760, 210, i, "Ways of mounting temperature sensors")


def d_rt_curves():
    i = ""
    # left: NTC
    x0, x1, y0, y1 = 50, 350, 190, 30
    X = lambda T: x0 + T / 50 * (x1 - x0)
    import math
    Yn = lambda R: y0 - (R / 35000) * (y0 - y1)
    pts = " ".join(f"{X(T):.1f},{Yn(10000 * math.exp(3950 * (1 / (T + 273.15) - 1 / 298.15))):.1f}" for T in range(0, 51, 2))
    i += line(x0, y0, x1, y0) + line(x0, y0, x0, y1)
    i += f'<polyline points="{pts}" class="d-aline"/>'
    i += t(200, 16, "10k NTC — resistance FALLS as it warms", "d-ts d-tb")
    for T in (0, 25, 50):
        i += t(X(T), y0 + 14, f"{T} °C", "d-ts")
    for R in (0, 10000, 20000, 30000):
        i += t(x0 - 6, Yn(R), f"{R // 1000}k", "d-ts", "end")
    # right: PT1000
    x0, x1 = 430, 730
    X2 = lambda T: x0 + T / 50 * (x1 - x0)
    Yp = lambda R: y0 - ((R - 950) / 300) * (y0 - y1)
    pts = " ".join(f"{X2(T):.1f},{Yp(1000 * (1 + 3.9083e-3 * T - 5.775e-7 * T * T)):.1f}" for T in range(0, 51, 2))
    i += line(x0, y0, x1, y0) + line(x0, y0, x0, y1)
    i += f'<polyline points="{pts}" class="d-warmline" style="stroke-width:2.2"/>'
    i += t(580, 16, "PT1000 — resistance RISES as it warms", "d-ts d-tb")
    for T in (0, 25, 50):
        i += t(X2(T), y0 + 14, f"{T} °C", "d-ts")
    for R in (1000, 1100, 1200):
        i += t(x0 - 6, Yp(R), f"{R}", "d-ts", "end")
    return svg(760, 215, i, "Resistance against temperature for a 10k NTC and a PT1000")


def d_dcv():
    i = defs("dc")
    x0, x1, y0, y1 = 70, 700, 190, 30
    X = lambda c: x0 + (c - 400) / 1000 * (x1 - x0)
    Y = lambda d: y0 - d / 100 * (y0 - y1)
    i += line(x0, y0, x1, y0) + line(x0, y0, x0, y1)
    for c in (400, 600, 800, 1000, 1200, 1400):
        i += t(X(c), y0 + 16, f"{c}", "d-ts")
    i += t((x0 + x1) / 2, y0 + 34, "Return air CO₂ (ppm)", "d-ts d-tb")
    for d in (0, 20, 50, 100):
        i += t(x0 - 8, Y(d), f"{d} %", "d-ts", "end")
    i += path(f"M{X(400)},{Y(20)} L{X(700)},{Y(20)} L{X(1000)},{Y(50)} L{X(1400)},{Y(50)}", "d-aline")
    i += circle(X(700), Y(20), 5, "d-acc") + circle(X(1000), Y(50), 5, "d-acc")
    i += t(X(700), Y(20) + 18, "700 ppm → minimum 20 %", "d-ts d-ta")
    i += t(X(1000), Y(50) - 16, "1,000 ppm → maximum 50 %", "d-ts d-ta")
    i += t(x0 + 6, y1 + 4, "Fresh air damper position", "d-ts d-tb", "start")
    return svg(760, 235, i, "Demand-controlled ventilation: CO2 sets the fresh air damper position")


def d_pressures():
    i = defs("pr")
    i += rect(40, 60, 520, 80, "d-soft", 4) + line(60, 100, 540, 100, "d-aline", end="pr-a") + t(470, 86, "airflow", "d-ts")
    # static tap
    i += line(140, 60, 140, 30, "d-line") + circle(140, 24, 6, "d-box") + t(140, 8, "Static", "d-ts d-tb")
    # pitot
    i += path("M340,100 L300,100 L300,30", "d-line") + circle(300, 24, 6, "d-box") + t(300, 8, "Total", "d-ts d-tb")
    i += box(380, 6, 160, 38, "Velocity pressure", "= total − static", "d-acc")
    i += t(300, 160, "pitot facing the flow → total", "d-ts")
    i += t(50, 160, "wall tap → static", "d-ts", "start")
    i += box(590, 60, 150, 80, "Velocity", "v ≈ 1.29 × √Pv  (m/s)|flow = v × duct area", "d-box")
    return svg(760, 175, i, "Static, total and velocity pressure in a duct")


def d_dp_uses():
    i = defs("du")
    i += rect(20, 70, 300, 70, "d-soft", 4) + t(170, 84, "Filter ΔP", "d-ts d-tb")
    i += path("M170,92 L158,104 L182,116 L158,128 L170,136")
    i += line(30, 105, 140, 105, "d-aline", end="du-a")
    i += box(130, 6, 80, 34, "ΔP", "", "d-acc", "d-t d-tb", 6)
    i += path("M145,40 L145,56 L100,56 L100,70", "d-line d-thin") + t(92, 50, "+", "d-t d-tb")
    i += path("M195,40 L195,56 L240,56 L240,70", "d-line d-thin") + t(250, 50, "−", "d-t d-tb")
    i += t(170, 160, "+ before the filter, − after it", "d-ts")
    i += rect(380, 70, 180, 70, "d-soft", 4) + t(470, 84, "Duct static pressure", "d-ts d-tb")
    i += line(390, 105, 550, 105, "d-aline", end="du-a")
    i += box(580, 6, 80, 34, "ΔP", "", "d-acc", "d-t d-tb", 6)
    i += path("M595,40 L595,56 L470,56 L470,70", "d-line d-thin") + t(480, 50, "+", "d-t d-tb")
    i += path("M645,40 L645,110", "d-line d-thin") + t(655, 116, "− open to the", "d-ts", "start") + t(655, 130, "plant room", "d-ts", "start")
    i += t(470, 160, "+ inside the duct, − to the surroundings", "d-ts")
    return svg(760, 175, i, "Two common uses of a differential pressure sensor")


def d_btu():
    i = defs("bt")
    i += box(290, 60, 180, 90, "AHU coil", "or a building / tenant", "d-soft")
    i += line(20, 80, 288, 80, "d-cold", end="bt-a") + t(30, 66, "CHW supply 7 °C", "d-ts d-ta", "start")
    i += line(472, 130, 740, 130, "d-warmline", end="bt-r") + t(735, 100, "CHW return 12.5 °C", "d-ts", "end")
    i += circle(150, 80, 12, "d-box") + t(150, 80, "T1", "d-ts d-tb")
    i += circle(560, 130, 12, "d-box") + t(560, 130, "T2", "d-ts d-tb")
    i += rect(620, 118, 50, 24, "d-acc", 5) + t(645, 130, "flow", "d-ts d-tb")
    i += box(320, 190, 180, 60, "Energy calculator", "kW = 4.19 × L/s × (T2 − T1)", "d-acc")
    i += path("M150,92 L150,220 L318,220", "d-line d-dash d-thin", end="bt")
    i += path("M560,142 L560,220 L502,220", "d-line d-dash d-thin", end="bt")
    i += path("M645,142 L645,236 L502,236", "d-line d-dash d-thin", end="bt")
    i += line(410, 250, 410, 278, "d-aline d-dash") + t(420, 272, "kW, kWh, flow, temps → BMS (Modbus, M-Bus, BACnet or pulse)", "d-ts d-ta", "start")
    return svg(760, 290, i, "An energy (BTU) meter: flow meter, matched temperature pair and calculator")


def d_damper_types():
    i = ""
    i += t(180, 16, "Opposed blade — for modulating control", "d-ts d-tb") + t(560, 16, "Parallel blade — for open/closed", "d-ts d-tb")
    for x0, opp in ((90, True), (470, False)):
        i += rect(x0, 30, 180, 150, "d-box", 4)
        for k in range(5):
            y = 50 + k * 28
            up = (k % 2 == 0) or not opp
            i += line(x0 + 50, y + (12 if up else -2), x0 + 130, y + (-2 if up else 12), "d-aline")
    return svg(760, 195, i, "Opposed-blade and parallel-blade dampers")


def d_actuator_wiring():
    i = defs("aw")
    cols = [(20, "On/off (2-position)", ["24 V AC supply", "DO switches the supply", "Spring returns it"]),
            (275, "Floating (3-point)", ["24 V AC common", "DO 1 = drive open", "DO 2 = drive close"]),
            (530, "Modulating (0/2–10 V)", ["24 V AC supply (2 wires)", "Y: AO control 0–10 V", "U: feedback 2–10 V → AI"])]
    for x, title, lines_ in cols:
        i += rect(x, 30, 210, 200, "d-soft", 8) + t(x + 105, 48, title, "d-t d-tb")
        i += box(x + 20, 70, 70, 50, "DDC", "", "d-acc")
        i += box(x + 125, 70, 70, 50, "Act.", "", "d-box")
        n = 2 if "On/off" in title else (3 if "Floating" in title else 4)
        for k in range(n):
            y = 80 + k * 10
            i += line(x + 90, y, x + 125, y, "d-line d-thin")
        for k, s in enumerate(lines_):
            i += t(x + 105, 150 + k * 22, s, "d-ts")
    return svg(760, 240, i, "Three ways to control a damper or valve actuator")


def d_two_three_way():
    i = defs("tw")
    i += t(190, 16, "2-way valve — flow varies", "d-t d-tb") + t(570, 16, "3-way valve — flow stays constant", "d-t d-tb")
    for x0 in (40, 420):
        i += rect(x0 + 120, 40, 60, 90, "d-acc", 4) + t(x0 + 150, 85, "coil", "d-ts d-tb")
        i += path(f"M{x0},60 L{x0 + 120},60", "d-cold", end="tw-a") + t(x0 + 6, 50, "supply", "d-ts", "start")
        i += path(f"M{x0 + 180},110 L{x0 + 300},110", "d-warmline", end="tw-r")
    i += path("M260,104 L276,104 L268,116 Z M260,128 L276,128 L268,116 Z", "d-box") + t(268, 142, "closes → less flow", "d-ts")
    i += t(240, 96, "return", "d-ts", "start")
    i += path("M640,60 L700,60 L700,98", "d-line d-dash", end="tw") + t(705, 76, "bypass", "d-ts", "start")
    i += path("M692,104 L708,104 L700,116 Z M692,128 L708,128 L700,116 Z", "d-box") + t(700, 160, "mixes coil flow + bypass", "d-ts")
    i += t(620, 96, "return", "d-ts", "start")
    return svg(760, 175, i, "2-way and 3-way valves at a coil")


def d_valve_curves():
    i = ""
    x0, x1, y0, y1 = 60, 360, 200, 30
    X = lambda v: x0 + v / 100 * (x1 - x0)
    Y = lambda v: y0 - v / 100 * (y0 - y1)
    import math
    eq = " ".join(f"{X(s):.1f},{Y(100 * (30 ** (s / 100 - 1)) if s else 0):.1f}" for s in range(0, 101, 4))
    coil = " ".join(f"{X(f):.1f},{Y(100 * (1 - math.exp(-f / 30)) / (1 - math.exp(-100 / 30))):.1f}" for f in range(0, 101, 4))
    lin = f"{X(0)},{Y(0)} {X(100)},{Y(100)}"
    for x0_, title, xl, yl, pts, cls in ((60, "Valve: equal-percentage", "valve opening %", "flow %", eq, "d-aline"),
                                          (420, "Coil: heat output vs flow", "flow %", "heat output %", coil, "d-warmline")):
        dx = x0_ - 60
        i += line(x0 + dx, y0, x1 + dx, y0) + line(x0 + dx, y0, x0 + dx, y1)
        i += t(210 + dx, 16, title, "d-ts d-tb")
        i += t(210 + dx, y0 + 18, xl, "d-ts")
        i += t(x0 + dx + 6, y1 + 2, yl, "d-ts", "start")
        shifted = " ".join(f"{float(p.split(',')[0]) + dx:.1f},{p.split(',')[1]}" for p in pts.split())
        i += f'<polyline points="{shifted}" class="{cls}" style="stroke-width:2.4"/>'
        i += f'<polyline points="{X(0) + dx},{Y(0)} {X(100) + dx},{Y(100)}" class="d-line d-dash d-thin"/>'
    return svg(760, 225, i, "Equal-percentage valve characteristic and coil heat output curve")


def d_vfd():
    i = defs("vf")
    i += rect(20, 40, 130, 190, "d-acc", 10) + t(85, 60, "DDC-AHU-01", "d-t d-tb")
    i += rect(380, 40, 230, 190, "d-box", 10) + t(495, 60, "VFD", "d-t d-tb")
    i += box(395, 80, 62, 60, "Rectifier", "AC → DC", "d-soft", "d-ts d-tb")
    i += box(464, 80, 62, 60, "DC bus", "capacitors", "d-warn", "d-ts d-tb")
    i += box(533, 80, 62, 60, "Inverter", "DC → AC|0–50 Hz", "d-soft", "d-ts d-tb")
    i += t(495, 170, "control terminals · relays", "d-ts") + t(495, 186, "keypad · fieldbus port", "d-ts")
    rows = [(92, "DO", "start (via interposing relay)", False), (118, "DI", "run status relay", True),
            (144, "DI", "fault relay", True), (170, "AO", "speed 0–10 V or 4–20 mA", False),
            (204, "RS485", "Modbus RTU / BACnet MS/TP", None)]
    for y, io, s_, back in rows:
        i += t(140, y, io, "d-ts d-tb", "end")
        if back is None:
            i += line(150, y, 378, y, "d-aline d-dash", end="vf-a", start="vf-a")
        elif back:
            i += line(378, y, 152, y, "d-line", end="vf")
        else:
            i += line(150, y, 376, y, "d-line", end="vf")
        i += t(264, y - 8, s_, "d-ts")
    i += line(495, 40, 495, 18) + t(503, 18, "415 V supply in", "d-ts", "start")
    i += line(610, 110, 658, 110, "d-warmline", end="vf-r") + t(634, 96, "out", "d-ts")
    i += circle(700, 110, 38, "d-box") + t(700, 110, "Motor", "d-t d-tb")
    return svg(760, 240, i, "VFD power stages and the signals exchanged with the BMS")


def d_proving():
    i = defs("pv")
    i += box(20, 30, 150, 80, "MCC / VFD", "contactor or drive", "d-soft")
    i += circle(420, 150, 40, "d-box") + t(420, 150, "Fan", "d-t d-tb")
    i += path("M170,70 L300,70 L300,150 L378,150", "d-warmline", end="pv-r") + t(240, 60, "motor cable", "d-ts")
    i += circle(300, 110, 13, "d-acc") + t(300, 110, "CT", "d-ts d-tb")
    i += line(462, 150, 740, 150, "d-aline", end="pv-a") + t(740, 136, "air", "d-ts", "end")
    i += box(390, 40, 60, 30, "ΔP", "", "d-acc", "d-t d-tb", 6)
    i += path("M400,70 L380,112", "d-line d-thin") + path("M440,70 L470,145", "d-line d-thin")
    labels = [(95, 140, "① Contactor aux / VFD run relay", "proves the drive is ON"),
              (210, 230, "② Current switch (CT)", "proves the motor draws current"),
              (520, 60, "③ Fan ΔP switch", "proves the fan moves air"),
              (620, 205, "④ Airflow switch / sensor", "proves air reaches the duct")]
    for x, y, a, b in labels:
        i += t(x, y, a, "d-ts d-tb") + t(x, y + 15, b, "d-ts")
    i += circle(620, 150, 10, "d-box")
    return svg(760, 255, i, "Ways to prove that a fan is really running")


# ==========================================================================
# Pages
# ==========================================================================

P1 = dict(
    id="3-1", slug="temperature-sensors", title="Temperature sensors (NTC, PT1000)",
    objectives=[
        "Explain how NTC thermistors and PT1000 RTDs measure temperature.",
        "Choose the right sensor type and mounting for a job.",
        "Calculate the error caused by wiring resistance.",
        "Diagnose open-circuit and short-circuit faults from the reading.",
    ],
    one_line=("Most BMS temperature sensors are simply <strong>resistors whose value changes with temperature</strong> — an "
              "NTC's resistance falls as it warms, a PT1000's rises — and the controller converts that resistance into °C."),
    why=("<p>Temperature is the most measured value in any BMS. Every control loop that holds a room, a duct or a pipe at a "
         "setpoint relies on a sensor being the right type, in the right place, wired correctly and configured to match. "
         "Getting any one of those wrong gives a reading that looks plausible but is wrong — the worst kind of fault.</p>"),
    body=(
        "<h3>The two common sensor families</h3>"
        + fig(d_rt_curves(), "NTC: large, non-linear change. PT1000: small, almost straight-line change.")
        + table(["", "NTC thermistor (e.g. 10k)", "PT1000 (platinum RTD)"], [
            ("Principle", "Semiconductor; resistance falls as temperature rises", "Platinum wire; resistance rises as temperature rises"),
            ("Value at reference", "10,000 Ω at 25 °C", "1,000 Ω at 0 °C"),
            ("Sensitivity", "Large — about 440 Ω per °C near 25 °C", "Small — about 3.85 Ω per °C"),
            ("Curve", "Strongly non-linear; many different curves exist", "Nearly linear; one international standard (IEC 60751)"),
            ("Interchangeability", "Must match the controller's configured curve exactly", "Any PT1000 to the standard works"),
            ("Typical use", "Rooms, ducts, general HVAC", "Pipes, energy meters, wider ranges, higher accuracy"),
        ])
        + callout("warn", "Match the curve",
                  "<p>“10k NTC” is not one sensor. There are several 10k curves (often described by a β value such as 3435 "
                  "or 3950, or by maker-specific “types”). If the controller input is set to a different curve from the sensor "
                  "fitted, the reading is right at 25 °C and increasingly wrong away from it. Always check the sensor datasheet "
                  "against the input configuration.</p>")
        + "<h3>Reference values</h3>"
        + table(["°C", "0", "10", "20", "25", "30", "40", "50"], [
            ("PT1000 (Ω)", "1000.0", "1039.0", "1077.9", "1097.3", "1116.7", "1155.4", "1194.0"),
            ("10k NTC β3950 (Ω, approx.)", "33,600", "20,200", "12,500", "10,000", "8,040", "5,300", "3,590"),
        ], "plain")
        + tool("rtd")
        + "<h3>Accuracy</h3>"
        + "<p>PT1000 accuracy is set by class in IEC 60751: <strong>Class B</strong> is ±(0.3 + 0.005 × |t|) °C — about ±0.3 °C "
          "at 0 °C — and <strong>Class A</strong> is ±(0.15 + 0.002 × |t|) °C. NTC sensors for HVAC are typically ±0.2 to "
          "±0.5 °C around room temperature. In practice, <strong>location</strong> errors (sun, draughts, a sensor touching the "
          "duct wall) are usually bigger than the sensor's own error.</p>"
        + "<h3>Wiring resistance</h3>"
        + "<p>Most BMS resistive sensors use two wires. The controller measures the sensor <em>plus</em> both wires, so cable "
          "resistance adds to the reading:</p>"
        + table(["50 m of 0.75 mm² cable (≈ 2.5 Ω loop)", "Error"], [
            ("10k NTC (≈ 440 Ω/°C)", "≈ 0.006 °C — negligible"),
            ("PT1000 (3.85 Ω/°C)", "≈ 0.6 °C — usually acceptable, or compensate with an offset"),
            ("PT100 (0.385 Ω/°C)", "≈ 6.5 °C — unacceptable with 2 wires; needs 3- or 4-wire connection"),
        ], "plain")
        + "<p>This is why BMS uses PT1000 rather than PT100, and why many controllers let you enter an offset or the cable "
          "resistance.</p>"
        + "<h3>Mounting types</h3>"
        + fig(d_temp_mounting(), "Choose the mounting that puts the sensing tip where the temperature you want really is.")
        + table(["Type", "Use", "Tips"], [
            ("Room / wall", "Space temperature", "1.2–1.5 m high; away from sun, doors, equipment and outside walls"),
            ("Duct probe", "Supply, return, mixed air", "Tip in the middle of the airstream, several duct widths after coil or fan"),
            ("Averaging (capillary)", "Mixed air, coil leaving air across large ducts", "Snaked across the whole duct face"),
            ("Immersion + thermowell", "Water pipes: CHW, CW, energy meters", "Tip in the middle third of the pipe; thermal paste in the well"),
            ("Strap-on / clamp", "Quick or retrofit pipe measurement", "Insulate over it; less accurate than immersion"),
            ("Outdoor", "Outside air", "In a ventilated sun shield, north-facing"),
        ])
        + "<h3>What the reading tells you when it fails</h3>"
        + table(["Fault", "NTC reads…", "PT1000 reads…"], [
            ("Open circuit (broken wire, loose terminal)", "Very <strong>low</strong> (resistance → ∞)", "Very <strong>high</strong>"),
            ("Short circuit (wires touching)", "Very <strong>high</strong> (resistance → 0)", "Very <strong>low</strong>"),
        ], "plain")
        + "<p>Most controllers show these as “out of range” or a fault flag. A good program also alarms on an impossible "
          "value and uses a fallback.</p>"
        + callout("note", "Transmitter versions",
                  "<p>Where the cable is long or noisy, use a <strong>temperature transmitter</strong> that converts the reading "
                  "into 4–20 mA or 0–10 V (Module 4). The controller then reads a scaled signal instead of a resistance.</p>")
    ),
    ahu01=("<p>AHU-01 has two temperature sensors: a <strong>return air duct probe (RAT)</strong> and a <strong>supply air duct "
           "probe (SAT)</strong>, both 10k NTC on universal inputs configured to the same curve as the sensors. RAT drives the "
           "valve loop; SAT is used for monitoring and the low-supply-temperature alarm.</p>"),
    on_site=[
        "Check the sensor's datasheet curve against the input configuration before blaming the sensor.",
        "To test a sensor, disconnect it and measure its resistance with a multimeter; compare with the table at a known temperature.",
        "Compare with a calibrated hand-held thermometer placed right next to the sensing tip.",
        "Fill thermowells with thermal paste — an empty well adds lag and error.",
        "Label sensor cables at both ends; swapped RAT and SAT sensors are a classic commissioning mistake.",
    ],
    faults=[
        ("Supply air reads −40 °C (or the input's minimum)", "NTC open circuit: broken wire, loose terminal, sensor unplugged", "Resistance at the terminals with the sensor disconnected"),
        ("Reading correct at 25 °C, wrong at 15 °C", "Wrong NTC curve configured", "Sensor datasheet vs input type"),
        ("Pipe temperature reads ~1 °C high on a long run", "PT1000 cable resistance", "Cable length and size; apply an offset"),
        ("Room reads 3 °C high every afternoon", "Sun on the sensor, or heat from equipment nearby", "Sensor location"),
        ("RAT and SAT look swapped", "Cables crossed during installation", "Warm one sensor in your hand and watch which value moves"),
    ],
    terms=[
        ("NTC thermistor", "Sensor whose resistance falls as temperature rises; 10k at 25 °C is common in HVAC."),
        ("RTD", "Resistance temperature detector — a metal (usually platinum) sensor whose resistance rises with temperature."),
        ("PT1000", "Platinum RTD with 1,000 Ω at 0 °C, about 3.85 Ω per °C (IEC 60751)."),
        ("β (beta) value", "Number describing the shape of an NTC's curve, e.g. 3435 or 3950."),
        ("Thermowell", "Closed tube in a pipe into which an immersion sensor is inserted."),
        ("Averaging sensor", "Long capillary sensor giving the average temperature across a duct."),
        ("Lead resistance", "Resistance of the sensor cable, which adds to the measured resistance."),
        ("Accuracy class", "IEC 60751 tolerance band for PT sensors, e.g. Class A or B."),
    ],
    scenarios=[dict(
        prompt="After ceiling works, AHU-01's supply air temperature suddenly reads −40 °C. The AHU is running and the offices are comfortable. What is the most likely cause?",
        options=["The coil is freezing.", "The NTC sensor circuit is open — a wire was cut or a terminal pulled loose.",
                 "The sensor is shorted."],
        answer=1,
        explain=(" An NTC reads very low when its circuit is open (infinite resistance). Comfortable offices confirm the real air "
                 "is fine. Measure resistance at the controller terminals with the sensor disconnected."),
    )],
    questions=[
        ("How does a PT1000's resistance change with temperature?", "It rises — about 3.85 Ω per °C, from 1,000 Ω at 0 °C."),
        ("Why can't you swap any 10k NTC for another?", "Different 10k NTCs follow different curves (β values or maker types). The controller input must be set to the same curve as the sensor, otherwise readings drift away from 25 °C."),
        ("An NTC input reads a very high temperature. Open or short circuit?", "Short circuit — the resistance has dropped to near zero, which an NTC reports as very hot."),
        ("Why is PT1000 preferred over PT100 for 2-wire BMS inputs?", "Its sensitivity is ten times higher (3.85 vs 0.385 Ω/°C), so cable resistance causes a ten times smaller error."),
        ("Where should the tip of an immersion sensor sit?", "In the middle third of the pipe, in a thermowell filled with thermal paste."),
    ],
)

P2 = dict(
    id="3-2", slug="humidity-and-co2-sensors", title="Humidity and CO₂ sensors",
    objectives=[
        "Explain relative humidity and dew point in practical terms.",
        "Describe how capacitive humidity sensors and NDIR CO₂ sensors work.",
        "Scale and check their 0–10 V or 4–20 mA outputs.",
        "Explain demand-controlled ventilation and the limits of automatic calibration.",
    ],
    one_line=("Humidity sensors tell the BMS <strong>how much moisture</strong> the air holds; CO₂ sensors tell it <strong>how many "
              "people</strong> are breathing in a space — and therefore how much fresh air is needed."),
    why=("<p>In humid climates, moisture control matters as much as temperature: too humid and rooms feel clammy and mould "
         "grows. CO₂ is the cheapest reliable way to measure occupancy, and using it to control fresh air is one of the "
         "biggest energy savings a BMS can deliver. Both sensors drift over time, so you need to know how to check them.</p>"),
    body=(
        "<h3>Humidity in one minute</h3>"
        + table(["Term", "Meaning", "Example"], [
            ("Relative humidity (RH)", "How full of moisture the air is, compared with the most it could hold at that temperature (%)", "50 % RH at 24 °C"),
            ("Dew point", "The temperature at which that air would start to condense", "24 °C, 50 % RH → dew point ≈ 13 °C"),
            ("Absolute humidity", "Actual mass of water per kg of dry air (g/kg)", "≈ 9.3 g/kg for 24 °C, 50 % RH"),
        ])
        + "<p>RH depends on temperature: cool the same air and its RH rises, even though the moisture is unchanged. That is why "
          "RH is always read together with temperature — most humidity sensors are combined temperature + RH units. Most "
          "offices aim for roughly <strong>40–60 % RH</strong>; above about 60 % comfort falls and mould risk rises.</p>"
        + "<h3>How humidity sensors work</h3>"
        + "<p>Most BMS humidity sensors are <strong>capacitive</strong>: a thin polymer layer absorbs moisture, changing the "
          "capacitance of a tiny capacitor. Electronics convert this into a <strong>0–10 V</strong> or <strong>4–20 mA</strong> "
          "signal for 0–100 % RH (some sensors communicate over Modbus or BACnet instead).</p>"
        + bullets([
            "Typical accuracy: about ±2–3 % RH in the middle of the range.",
            "Sensors <strong>drift</strong> slowly and can be damaged by condensation, dust and chemicals. Check them against a calibrated hand-held instrument every year or two.",
            "Never mount them where they can get wet — e.g. right after a cooling coil, where air is close to saturation.",
        ])
        + "<h3>CO₂ — the occupancy sensor</h3>"
        + "<p>People breathe out CO₂. Outdoor air is around <strong>420 ppm</strong> (parts per million). In an occupied room, CO₂ "
          "rises until the fresh air supplied balances what people breathe out. Many designs aim to keep indoor CO₂ below "
          "about <strong>1,000 ppm</strong> — roughly 600 ppm above outdoor air.</p>"
          "<p>BMS CO₂ sensors use <strong>NDIR</strong> (non-dispersive infrared): CO₂ absorbs infrared light at a particular "
          "wavelength, so the sensor measures how much light is absorbed across a small chamber. Output is commonly "
          "0–10 V for <strong>0–2,000 ppm</strong> — so 1 V = 200 ppm.</p>"
        + callout("warn", "Automatic calibration has a catch",
                  "<p>Many single-channel CO₂ sensors use <strong>automatic baseline calibration</strong> (ABC): they assume the "
                  "lowest reading over the last week or so is outdoor air (≈ 400 ppm) and correct themselves to it. That only "
                  "works if the space really empties overnight or at weekends. In 24/7 spaces — hospitals, control rooms, "
                  "some hotels — ABC drags the readings too low. Use dual-channel sensors there, or turn ABC off and calibrate "
                  "manually.</p>")
        + "<h3>Demand-controlled ventilation (DCV)</h3>"
        + fig(d_dcv(), "Below 700 ppm the damper stays at its minimum; above 1,000 ppm it is at its maximum; in between it moves in proportion.")
        + "<p>Instead of supplying fresh air for the design number of people all day, DCV opens the fresh air damper only as "
          "far as the measured CO₂ requires. Empty meeting rooms and half-full offices then cost far less to cool. The "
          "minimum position still covers the building's own emissions (materials, furniture).</p>"
        + table(["Other air-quality sensors", "Measures", "Typical use"], [
            ("Carbon monoxide (CO)", "Exhaust fumes (electrochemical cell)", "Car parks — ventilation fans staged on CO levels set by local codes"),
            ("VOC", "Volatile organic compounds (odours, chemicals)", "Indicative air quality in offices"),
            ("PM2.5 / PM10", "Fine particles", "Filter performance, outdoor pollution"),
        ], "plain")
        + callout("note", "Do not mix up CO and CO₂", "<p>CO₂ (carbon dioxide) measures people. CO (carbon monoxide) is a toxic "
                  "gas from engines and burners. They use different sensors and different limits.</p>")
    ),
    ahu01=("<p>AHU-01 has a <strong>combined return air humidity sensor (0–10 V = 0–100 % RH)</strong> and a <strong>return air "
           "CO₂ sensor (0–10 V = 0–2,000 ppm)</strong>. The CO₂ value drives the fresh air damper between 20 % at 700 ppm and "
           "50 % at 1,000 ppm, exactly as in the graph. The humidity value is trended and alarmed above 65 % RH.</p>"),
    on_site=[
        "Check scaling: a CO₂ sensor reading exactly half or double the expected value usually has the wrong range configured (e.g. 0–2,000 vs 0–1,000 ppm).",
        "Compare an RH sensor with a calibrated hand-held hygrometer at the same spot and temperature.",
        "Room CO₂ sensors belong at breathing height, away from doors, windows and supply diffusers.",
        "Ask whether a space is ever empty before relying on a CO₂ sensor's automatic calibration.",
    ],
    faults=[
        ("RH stuck at 100 %", "Sensor wet or failed; mounted in saturated air after the coil", "Location; dry and recheck; replace"),
        ("CO₂ always ≈ 400 ppm, even in a packed room", "Sensor in the fresh air intake, or range misconfigured", "Location and input scaling"),
        ("CO₂ reads lower month after month in a 24/7 space", "Automatic baseline calibration drift", "Disable ABC or use a dual-channel sensor"),
        ("CO₂ reads exactly double the hand-held meter", "Range set to 0–2,000 when the sensor is 0–1,000 ppm (or vice versa)", "Sensor jumper/DIP setting vs controller scaling"),
        ("Humidity jumps when the sun hits the façade", "Sensor temperature affected, so RH calculation shifts", "Sensor location"),
    ],
    terms=[
        ("Relative humidity (RH)", "Moisture in the air as a percentage of the maximum it could hold at that temperature."),
        ("Dew point", "Temperature at which water vapour in the air starts to condense."),
        ("Capacitive humidity sensor", "Sensor using a moisture-absorbing polymer whose capacitance changes with humidity."),
        ("ppm", "Parts per million — unit for gas concentration such as CO₂."),
        ("NDIR", "Non-dispersive infrared — the measuring principle of most CO₂ sensors."),
        ("ABC", "Automatic baseline calibration — self-correction assuming the lowest reading is outdoor air."),
        ("DCV", "Demand-controlled ventilation — fresh air varied with measured occupancy (CO₂)."),
    ],
    scenarios=[dict(
        prompt="A 0–10 V CO₂ sensor shows 6 V. The BMS is set for 0–2,000 ppm. What does the BMS display, and what does that mean for AHU-01's fresh air damper?",
        options=["600 ppm — damper at minimum (20 %).", "1,200 ppm — damper at maximum (50 %).", "6,000 ppm — sensor fault."],
        answer=1,
        explain=(" 6 V × 200 ppm/V = 1,200 ppm. That is above the 1,000 ppm point, so DCV drives the fresh air damper to its 50 % "
                 "maximum."),
    )],
    questions=[
        ("Why is RH always measured together with temperature?", "RH depends on temperature: the same air shows a higher RH when cooler. Without temperature you cannot interpret it or calculate dew point."),
        ("What does a CO₂ sensor tell a BMS?", "How much fresh air is needed for the people present — CO₂ rises with occupancy."),
        ("A 0–10 V, 0–2,000 ppm CO₂ sensor reads 4.5 V. What is the CO₂?", "4.5 × 200 = 900 ppm."),
        ("When does automatic baseline calibration give wrong readings?", "When the space never empties (24/7 occupancy), so the lowest reading over the period is not really outdoor air."),
        ("What is the difference between CO and CO₂ sensors?", "CO₂ (carbon dioxide) indicates occupancy; CO (carbon monoxide) is a toxic exhaust gas, monitored in car parks. They use different sensors and limits."),
    ],
)

P3 = dict(
    id="3-3", slug="differential-pressure-and-airflow", title="Differential pressure and airflow sensors",
    objectives=[
        "Explain what a differential pressure sensor measures and how its ports are connected.",
        "List the main uses of ΔP sensors and switches in HVAC.",
        "Explain static, total and velocity pressure, and calculate air velocity.",
        "Diagnose common ΔP faults from the readings.",
    ],
    one_line=("A differential pressure (ΔP) sensor measures the <strong>difference in pressure between its two ports</strong> — "
              "across a filter, between a duct and a room, or between two points in an airflow probe to work out velocity."),
    why=("<p>ΔP sensors are everywhere in HVAC: they tell you when filters are dirty, they control VAV fans, they prove fans are "
         "moving air, they keep clean rooms at the right pressure and they measure airflow. They are simple devices — but a "
         "swapped or loose tube gives readings that send whole systems the wrong way.</p>"),
    body=(
        "<h3>Two ports, one difference</h3>"
        + "<p>A ΔP sensor has a <strong>high (+)</strong> and a <strong>low (−)</strong> port, each connected by plastic tube to a "
          "measuring point. It outputs the difference in pascals (Pa), as 0–10 V, 4–20 mA, or over a bus. A <strong>ΔP "
          "switch</strong> does the same job but only closes a contact above a set pressure.</p>"
        + fig(d_dp_uses(), "Filter monitoring and duct static pressure — the two uses you will meet first.")
        + table(["Use", "Measures", "Typical range", "Sensor or switch"], [
            ("Filter monitoring", "Across a filter", "0–500 Pa or more", "Either"),
            ("Duct static pressure (VAV)", "Duct relative to surroundings", "0–500 Pa / 0–1,000 Pa", "Sensor (control)"),
            ("Fan proving", "Across the fan", "0–1,000 Pa or more", "Usually a switch"),
            ("Room pressure", "Room relative to corridor", "± 50 Pa (often only a few pascals)", "Sensor"),
            ("Airflow measurement", "Velocity pressure from a probe", "0–250 Pa or so", "Sensor"),
            ("Water ΔP (pumps, index circuit)", "Between supply and return pipes", "In kPa or bar", "Water-rated sensor"),
        ])
        + "<p>Units: <strong>1 Pa</strong> is tiny — 100 Pa = 1 mbar; 1 kPa = 1,000 Pa; 1 bar = 100 kPa. Many ΔP sensors have a "
          "selectable range (DIP switch or menu) — the controller's scaling must match the range selected.</p>"
        + "<h3>Static, total and velocity pressure</h3>"
        + fig(d_pressures(), "A pitot tube facing the flow sees total pressure; a wall tap sees static pressure; the difference is velocity pressure.")
        + callout("note", "Air velocity from velocity pressure (air at about 1.2 kg/m³)",
                  "<p><strong>v ≈ 1.29 × √Pv</strong> (m/s, with Pv in Pa) &nbsp;·&nbsp; <strong>Airflow = v × duct area</strong></p>"
                  "<p>Example: Pv = 100 Pa → v ≈ 1.29 × 10 = 12.9 m/s. In a 0.5 × 0.4 m duct (0.2 m²): 12.9 × 0.2 ≈ "
                  "<strong>2.6 m³/s (2,600 L/s)</strong>.</p>")
        + "<h3>Measuring airflow in practice</h3>"
        + table(["Device", "How it works", "Notes"], [
            ("Averaging pitot array / flow station", "Many total and static holes across the duct, averaged", "Needs a straight duct run upstream; low pressures at low velocity"),
            ("VAV flow cross", "Cross-shaped probe in the box inlet; flow = K × √ΔP", "The box's K-factor comes from the manufacturer"),
            ("Fan inlet ring (piezometer)", "Pressure taps in the fan inlet cone", "Fan maker supplies the K-factor"),
            ("Thermal dispersion", "Heated element cooled by the airflow", "Good at low velocities; no pressure drop"),
            ("Airflow (paddle) switch", "Paddle pushed by the airflow closes a contact", "On/off proving only"),
        ])
        + callout("tip", "Straight runs", "<p>Bends, dampers and fans make the airflow uneven. Airflow probes and duct static sensors "
                  "need a stretch of straight duct before them — the maker states how much. Poor placement gives jumpy or biased readings.</p>")
    ),
    ahu01=("<p>AHU-01 has two pressure devices: a <strong>filter ΔP switch</strong> (contact closes when the filter is dirty → DI) "
           "and a <strong>supply duct static pressure sensor, 0–500 Pa, 4–20 mA</strong> (→ AI), with its + port in the duct "
           "and its − port open to the plant room. Lab 4 wires and scales this sensor.</p>"),
    on_site=[
        "Check the tubes: + to the higher pressure, − to the lower. Swapped tubes give negative readings, or zero on sensors that cannot read negative.",
        "Run tubes without kinks or sags where condensate can collect; use rigid connectors through the duct wall.",
        "Most ΔP sensors have a zero (auto-zero) function — use it with both ports open to the same pressure during commissioning.",
        "Check the range jumper or menu against the controller's scaling.",
    ],
    faults=[
        ("Reading negative or stuck at zero", "Tubes swapped (+ and −)", "Tube connections at the sensor"),
        ("Duct static reads 0 Pa; fan runs at maximum", "Tube disconnected or blocked", "Tubes and duct connection"),
        ("Reading jumps around", "Probe in turbulent air (too close to a bend or fan)", "Location; straight run; output damping"),
        ("Small, constant error even with no flow", "Zero drift", "Auto-zero / recalibrate"),
        ("Filter alarm never comes, even with filters black", "Switch set too high, or tubes not connected", "Switch setpoint and tubes"),
    ],
    terms=[
        ("Differential pressure (ΔP)", "Difference in pressure between two points."),
        ("Static pressure", "Pressure the air exerts on the duct walls."),
        ("Total pressure", "Static pressure plus velocity pressure, seen by a probe facing the flow."),
        ("Velocity pressure", "Pressure due to air movement: total minus static."),
        ("Pitot tube", "Probe facing the airflow that measures total (and often static) pressure."),
        ("K-factor", "Constant relating ΔP to flow for a specific probe or box: flow = K × √ΔP."),
        ("ΔP switch", "Device that closes a contact when the pressure difference exceeds a setpoint."),
        ("Pa (pascal)", "Unit of pressure; 100 Pa = 1 mbar."),
    ],
    scenarios=[dict(
        prompt="A new filter ΔP sensor on AHU-03 reads −120 Pa while the fan runs. What has happened?",
        options=["The filter is torn.", "The + and − tubes have been connected the wrong way round.", "The fan is running backwards."],
        answer=1,
        explain=(" Air pressure is higher before the filter than after it, so + must go before the filter. A negative reading of a "
                 "sensible size means the tubes are swapped."),
    )],
    questions=[
        ("What do the + and − ports of a ΔP sensor mean?", "+ is the high-pressure port and − the low-pressure port; the output is the + pressure minus the − pressure."),
        ("Calculate air velocity for a velocity pressure of 64 Pa.", "v ≈ 1.29 × √64 = 1.29 × 8 ≈ 10.3 m/s."),
        ("Where are the ports of a duct static pressure sensor connected?", "+ to a tap inside the duct, − open to the surroundings (plant room or ceiling space)."),
        ("Name four uses of ΔP sensors or switches in HVAC.", "Any four of: filter monitoring, duct static pressure control, fan proving, room pressure, airflow measurement, water ΔP for pumps."),
        ("Why do airflow probes need a straight duct run?", "Bends, fans and dampers make the airflow uneven and turbulent, which gives jumpy or biased readings."),
    ],
)

P4 = dict(
    id="3-4", slug="water-flow-meters", title="Water flow meters",
    objectives=[
        "Compare electromagnetic, ultrasonic and mechanical flow meters.",
        "Explain how an energy (BTU) meter calculates cooling energy.",
        "Configure a pulse output and convert between flow units.",
        "Recognise installation errors that spoil flow readings.",
    ],
    one_line=("Flow meters measure <strong>how much water passes</strong> through a pipe; add a pair of temperature sensors and a "
              "calculator and you have an <strong>energy (BTU) meter</strong> that tells you how much cooling was delivered."),
    why=("<p>Flow and energy data turn a BMS from a control system into an energy-management system: you can see what each "
         "plant item or tenant really uses, bill for it, and spot waste such as low ΔT. Meters are also used to prove flow "
         "before starting chillers. They are expensive, and a badly installed one is worse than none — it gives confident, "
         "wrong numbers.</p>"),
    body=(
        table(["Meter type", "How it works", "Strengths", "Watch out for"], [
            ("Electromagnetic (magmeter)", "Conductive water moving through a magnetic field generates a voltage proportional to velocity", "Accurate, no moving parts, no pressure drop", "Pipe must be full; needs conductive liquid; straight pipe before and after"),
            ("Ultrasonic, clamp-on", "Measures the difference in transit time of sound with and against the flow", "Fits outside the pipe — no cutting", "Needs good pipe data and more straight pipe; less accurate"),
            ("Ultrasonic, in-line", "Same principle, built into a pipe section", "Accurate; common in energy meters", "Straight runs; air bubbles"),
            ("Mechanical (turbine, multi-jet)", "Water turns a rotor", "Cheap; good for domestic water", "Wear, debris, pressure drop"),
            ("Vortex", "Counts vortices shed by a bluff body", "Robust", "Not good at low velocities"),
        ])
        + callout("tip", "Straight pipe", "<p>Bends, valves and pumps disturb the flow profile. Meters need straight pipe "
                  "upstream and downstream — for magmeters typically about 5 pipe diameters before and 2–3 after; clamp-on "
                  "ultrasonic meters usually need more. Use the maker's figures.</p>")
        + "<h3>Energy (BTU) meters</h3>"
        + fig(d_btu(), "The calculator multiplies flow by the temperature difference to give cooling power and energy.")
        + callout("note", "Cooling power", "<p><strong>kW = 4.19 × flow (L/s) × ΔT (K)</strong></p>"
                  "<p>Example: 5 L/s with 7 °C in and 12.5 °C out → 4.19 × 5 × 5.5 ≈ <strong>115 kW</strong>. Over 10 hours that is "
                  "1,150 kWh of cooling.</p>")
        + "<p>The two temperature sensors are a <strong>matched pair</strong> (often PT500 or PT1000), calibrated together, because a "
          "small error in ΔT gives a big error in energy: on a 5.5 K ΔT, a 0.1 K error is about 2 %.</p>"
        + "<h3>Getting data out of the meter</h3>"
        + table(["Output", "How the BMS uses it"], [
            ("4–20 mA / 0–10 V", "Instantaneous flow (or power) on an AI — fine for control, no totals."),
            ("Pulse output", "Each pulse = a fixed volume or energy (e.g. 1 pulse = 10 L). The BMS counts pulses on a DI to build totals."),
            ("Modbus, BACnet, M-Bus", "Everything: flow, temperatures, power, totals, alarms. Best for energy monitoring."),
        ])
        + "<p>When counting pulses, set the <strong>pulse weight</strong> (litres or kWh per pulse) in the BMS to match the meter, "
          "and check the input can count fast enough at maximum flow.</p>"
        + table(["Convert", "Multiply by"], [
            ("L/s → m³/h", "3.6"),
            ("m³/h → L/s", "0.2778 (÷ 3.6)"),
            ("L/s → US gpm", "15.85"),
            ("kW → TR", "÷ 3.517"),
        ], "plain")
        + "<h3>Flow switches</h3>"
        + "<p>Where you only need to know that water <em>is</em> flowing — chiller and pump proving — a <strong>flow switch</strong> "
          "(paddle or thermal) closes a contact above a set flow. It is a DI, and part of the chiller's safety interlocks.</p>"
    ),
    ahu01=("<p>AHU-01 has no meter of its own, but the 3rd floor has an <strong>energy meter on its chilled water branch</strong>, "
           "read over Modbus, so the floor's cooling energy can be compared with AHU-01's valve position and run-hours. A floor "
           "using more energy for the same weather and occupancy is a sign of a fault.</p>"),
    on_site=[
        "Check the flow-direction arrow on the meter body — reversed meters read zero or negative.",
        "Magmeters must be in a pipe that is always full: not at a high point where air collects.",
        "Check which pipe each temperature sensor is in. Swapped sensors give negative energy.",
        "Compare pulse totals with the meter's own display over a few days to prove the pulse weight.",
    ],
    faults=[
        ("Flow reads zero although the pump runs", "Empty or part-full pipe, reversed meter, or air", "Meter position, direction arrow, air vents"),
        ("Energy reads negative", "Supply and return temperature sensors swapped", "Sensor positions vs meter configuration"),
        ("Flow reading unsteady", "Not enough straight pipe; air bubbles", "Installation against maker's requirements"),
        ("BMS total is 10× the meter display", "Pulse weight set wrong", "Pulse weight in meter and BMS"),
        ("Energy too low at high load", "Temperature sensors not fully immersed / no paste", "Sensor pockets"),
    ],
    terms=[
        ("Magmeter", "Electromagnetic flow meter for conductive liquids; no moving parts."),
        ("Ultrasonic meter", "Flow meter using the transit time of sound waves with and against the flow."),
        ("Energy (BTU) meter", "Flow meter + matched temperature pair + calculator that totals thermal energy."),
        ("Matched pair", "Two temperature sensors calibrated together for an accurate ΔT."),
        ("Pulse weight", "Quantity represented by one output pulse, e.g. 10 L or 1 kWh."),
        ("M-Bus", "Meter-Bus: a standard for reading utility meters."),
        ("Flow switch", "Device that closes a contact when flow exceeds a set value."),
    ],
    scenarios=[dict(
        prompt="A new BTU meter on the 3rd-floor branch shows −110 kW during the working day. Flow looks right. What is wrong?",
        options=["The chilled water is flowing backwards.", "The supply and return temperature sensors are in each other's pipes.",
                 "The meter is reading heating energy."],
        answer=1,
        explain=(" With a correct flow, a negative power of a believable size means the meter sees the return as colder than the "
                 "supply: the sensors are swapped (or the configuration says the wrong pipe)."),
    )],
    questions=[
        ("Why does a magmeter need a full pipe?", "It measures the voltage across the flowing water; with air in the pipe the measurement is wrong or lost."),
        ("Calculate the cooling for 8 L/s with a 5 K ΔT.", "4.19 × 8 × 5 ≈ 168 kW."),
        ("What is a pulse weight, and why must it match?", "The quantity one pulse represents (e.g. 10 L). If the BMS uses a different value, all totals are wrong by that factor."),
        ("Convert 36 m³/h to L/s.", "36 ÷ 3.6 = 10 L/s."),
        ("Why do energy meters use a matched temperature pair?", "Because energy depends on a small ΔT; matched sensors keep the ΔT error tiny."),
    ],
)

P5 = dict(
    id="3-5", slug="damper-actuators", title="Damper actuators",
    objectives=[
        "Tell opposed-blade and parallel-blade dampers apart and know where each is used.",
        "Compare on/off, floating and modulating actuators.",
        "Explain spring return, fail-safe positions, running time and torque.",
        "Set up and troubleshoot a modulating damper actuator.",
    ],
    one_line=("A damper actuator is a small motor that <strong>turns a damper's shaft</strong> to open, close or position it, "
              "in response to a control signal from the BMS."),
    why=("<p>Dampers decide how much fresh air comes in, where air goes and whether a duct is open at all. A stuck or "
         "wrongly-set damper can starve a building of fresh air, waste energy, or let a fan run against a closed duct. "
         "Actuators are among the most frequently replaced field devices — and among the most often wired or set wrongly.</p>"),
    body=(
        "<h3>Dampers first</h3>"
        + fig(d_damper_types(), "Opposed blades give smoother modulating control; parallel blades suit open/closed duty.")
        + table(["Damper", "Use", "BMS role"], [
            ("Opposed blade", "Modulating: fresh air, return air, mixing", "Controlled"),
            ("Parallel blade", "Two-position isolation", "Controlled (open/closed)"),
            ("Volume control damper (VCD)", "Manual balancing", "None — set by the balancing engineer"),
            ("Fire damper", "Closes on heat (fusible link) to stop fire spreading", "None, or monitored end switch"),
            ("Smoke / fire-smoke damper", "Motorised, controlled by the fire system", "Monitoring only — the fire system is in control"),
        ])
        + "<h3>Three ways to control an actuator</h3>"
        + fig(d_actuator_wiring(), "The control signal decides what the BMS output must be: one DO, two DOs, or an AO.")
        + table(["Control type", "BMS outputs", "Position known by", "Use"], [
            ("On/off (2-position)", "1 DO (often switching the supply)", "End switch DI, if fitted", "Isolation dampers"),
            ("Floating (3-point)", "2 DOs: drive open / drive close", "Calculated from running time, re-synced at the ends", "Older systems; some VAV boxes"),
            ("Modulating", "1 AO (0–10 V or 2–10 V)", "Feedback signal (2–10 V) to an AI, if wired", "Fresh air, mixing and most control dampers"),
        ])
        + "<h3>Key actuator specifications</h3>"
        + table(["Specification", "Meaning", "Typical"], [
            ("Torque (Nm)", "Turning force; must exceed what the damper needs, with margin", "Sized from the damper maker's figure (often in Nm per m² of damper)"),
            ("Running time", "Time to travel full stroke under motor power", "About 90–150 s for modulating actuators"),
            ("Spring return", "A spring drives the damper to its safe position when power is lost", "Spring time about 15–25 s"),
            ("Supply", "Usually 24 V AC/DC; some 230 V", "Power stated in VA for transformer sizing"),
            ("Control signal", "0–10 V, 2–10 V, floating, or on/off", "Selectable on many models"),
            ("Feedback", "Position signal back to the BMS", "2–10 V"),
            ("Auxiliary switches", "Contacts at set positions (e.g. fully open)", "Used for proving to a DI"),
        ])
        + callout("warn", "Fail-safe position",
                  "<p>Choose what happens on power loss. A fresh air damper is usually <strong>spring-return closed</strong> so "
                  "unfiltered, humid air cannot pour in when the AHU is off. Smoke-control dampers follow the fire strategy, "
                  "not the BMS.</p>")
        + "<h3>Setting up a modulating actuator</h3>"
        + steps([
            "Mount it on the damper shaft with the damper <strong>fully closed</strong> and the actuator at its 0 % end; tighten the shaft clamp.",
            "Set the <strong>rotation direction</strong> switch so that increasing signal opens the damper.",
            "Select the <strong>signal type</strong> (0–10 V or 2–10 V) to match the controller output.",
            "Wire supply, common, control signal (Y) and feedback (U). Many makers number these 1, 2, 3 and 5 — always check the label.",
            "Run the <strong>adaptation / stroke</strong> function if the actuator has one, so it learns the real end stops.",
            "Command 0, 50 and 100 % from the BMS and check the damper on site and the feedback each time.",
        ])
        + callout("note", "Powering many actuators", "<p>Add up the VA of every actuator on a 24 V AC transformer (using the "
                  "running figure) and add margin. Undersized transformers cause actuators to stall or behave erratically when "
                  "several move at once. Keep 24 V polarity consistent: the controller's signal common and the actuator's "
                  "supply common must be the same conductor.</p>")
    ),
    ahu01=("<p>AHU-01's <strong>fresh air damper</strong> uses a modulating, spring-return-closed actuator: 24 V AC, 0–10 V control "
           "from an AO. It sits at 20 % minimum when the AHU runs and closes on power loss or when the AHU stops. The return "
           "damper is a manual balancing damper, so it has no actuator.</p>"),
    on_site=[
        "Check the damper itself moves — actuators often turn while a loose shaft clamp lets the damper stay put.",
        "Use the actuator's manual override (button or crank) to check the damper moves freely end to end.",
        "Feedback different from command? The damper is binding, or the actuator has not been adapted.",
        "Look for the position indicator on the actuator — it shows the actuator's position, not necessarily the damper's.",
    ],
    faults=[
        ("Actuator turns, damper doesn't", "Loose shaft clamp or broken linkage", "Clamp and linkage"),
        ("Damper opens when it should close", "Rotation direction set wrong", "Direction switch; signal type"),
        ("Feedback stops at 70 % while command is 100 %", "Damper binding or end-stop wrong", "Free movement by hand; adaptation"),
        ("Floating actuator slowly drifts out of step", "Calculated position error builds up", "Periodic re-sync to fully closed"),
        ("Several actuators stall at the same time", "24 V transformer undersized or voltage drop", "VA total; voltage while they move"),
    ],
    terms=[
        ("Opposed-blade damper", "Adjacent blades rotate in opposite directions; good for modulating control."),
        ("Parallel-blade damper", "All blades rotate the same way; used for open/closed duty."),
        ("Floating (3-point) control", "Two outputs drive the actuator open or closed; position inferred from time."),
        ("Modulating control", "Continuous position control from an analogue signal such as 0–10 V."),
        ("Spring return", "Actuator spring drives to a safe position on power loss."),
        ("Running time", "Time for the actuator to travel its full stroke."),
        ("Torque", "Turning force of an actuator, in Nm."),
        ("Adaptation", "Actuator function that learns the real end positions of the damper or valve."),
    ],
    scenarios=[dict(
        prompt="The BMS shows AHU-01's fresh air damper at 50 % and the actuator's position indicator agrees, but there is almost no fresh air coming in. What do you check first?",
        options=["The CO₂ sensor scaling.", "The actuator's shaft clamp and the damper linkage — the damper may not be turning with the actuator.",
                 "The supply fan speed."],
        answer=1,
        explain=(" The actuator says 50 %, but the damper blades may not have moved. A loose clamp on the shaft is the classic cause. "
                 "Look at the blades themselves."),
    )],
    questions=[
        ("Which damper type is best for modulating control, and why?", "Opposed-blade, because its flow changes more evenly with position, giving smoother control."),
        ("How many BMS outputs does a floating actuator need?", "Two digital outputs: one to drive open, one to drive close."),
        ("What is the usual fail-safe position for a fresh air damper, and why?", "Closed (spring return), so unconditioned outdoor air does not enter when the AHU is off or loses power."),
        ("What is actuator adaptation?", "A function where the actuator runs end to end to learn the real stroke of the damper or valve, so 0–100 % maps to the full real movement."),
        ("Why must you add up actuator VA before choosing a transformer?", "So the transformer can supply all actuators moving at once without the voltage dropping and actuators stalling."),
    ],
)

P6 = dict(
    id="3-6", slug="chilled-water-valve-actuators", title="Chilled water valves and actuators",
    objectives=[
        "Compare 2-way and 3-way valves and their effect on system flow.",
        "Recognise globe, characterised ball, butterfly and pressure-independent valves.",
        "Explain why equal-percentage valves are used on coils and calculate Kv.",
        "Choose and set up an actuator, including fail-safe and close-off.",
    ],
    one_line=("A control valve and its actuator decide <strong>how much chilled water flows through a coil</strong> — and so how "
              "much cooling it gives. Choosing, sizing and setting them up correctly is what makes a temperature loop stable."),
    why=("<p>The valve is the final control element of nearly every cooling loop. An oversized valve makes the loop hunt; a "
         "leaking one wastes energy and causes low ΔT; the wrong fail-safe can freeze a coil or flood a room with cold air. "
         "Many “PID tuning problems” are really valve problems.</p>"),
    body=(
        "<h3>2-way or 3-way?</h3>"
        + fig(d_two_three_way(), "A 2-way valve reduces flow; a 3-way valve diverts the unused water round the coil.")
        + table(["", "2-way valve", "3-way valve"], [
            ("Flow in the system", "Variable — falls as valves close", "Constant — unused water bypasses the coil"),
            ("Pumps", "Can slow down (VFD) — saves energy", "Run at constant flow"),
            ("Return water", "Warm — good ΔT", "Mixed with bypass water — low ΔT"),
            ("Use today", "Most modern systems", "Older systems; end-of-line units to keep minimum flow"),
        ], "plain")
        + "<h3>Valve types</h3>"
        + table(["Type", "Movement", "Typical use"], [
            ("Globe valve", "Linear — a plug moves up and down", "Classic coil control valve"),
            ("Characterised ball valve", "Rotary (quarter-turn); a shaped disc gives the right characteristic", "Coil control in smaller sizes"),
            ("Butterfly valve", "Rotary", "Large pipes; isolation and chiller/tower changeover"),
            ("Pressure-independent control valve (PICV)", "Control valve + built-in pressure regulator", "Modern coil control; flow does not change with system pressure"),
        ])
        + "<h3>Sizing: Kv</h3>"
        + callout("note", "Valve flow coefficient",
                  "<p><strong>Kv</strong> = flow in m³/h through the fully open valve with a 1 bar pressure drop.</p>"
                  "<p><strong>Flow (m³/h) = Kv × √ΔP (bar)</strong> &nbsp;→&nbsp; <strong>Kv = Flow ÷ √ΔP</strong></p>"
                  "<p>Example: a coil needs 9 m³/h and the valve should take 0.25 bar → Kv = 9 ÷ 0.5 = <strong>18</strong>. Choose the "
                  "nearest standard Kvs at or just below.</p>")
        + "<p>A valve must take a decent share of the circuit's pressure drop to control well. This share is its "
          "<strong>authority</strong>: ΔP(valve) ÷ [ΔP(valve) + ΔP(rest of the circuit)]. Aim for about 0.5. A valve with low "
          "authority does nothing for most of its stroke, then everything at once.</p>"
        + "<h3>Why equal-percentage?</h3>"
        + fig(d_valve_curves(), "Left: an equal-percentage valve passes little flow until well open. Right: a coil gives most of its output at low flow. Together they give a near-linear response.")
        + "<p>A cooling coil gives a large part of its capacity at a small part of its flow. If the valve were linear, the first "
          "20 % of opening would deliver most of the cooling and the loop would be twitchy at low load. An "
          "<strong>equal-percentage</strong> valve does the opposite, so the combined valve-plus-coil response is roughly "
          "linear — and the PID loop behaves the same at every load.</p>"
        + "<h3>Actuators for valves</h3>"
        + table(["Specification", "What to check"], [
            ("Linear or rotary", "Linear (force in N) for globe valves; rotary (torque in Nm) for ball and butterfly"),
            ("Signal", "0–10 V, 2–10 V or floating, matching the controller output"),
            ("Fail-safe", "Spring return or capacitor return to open or closed — a design decision"),
            ("Close-off pressure", "The highest ΔP against which it can close tightly. Exceed it and the valve leaks"),
            ("Direct / reverse action", "Whether increasing signal opens or closes"),
            ("Feedback and manual override", "Position feedback to an AI; hand wheel or lever for manual operation"),
        ])
        + callout("tip", "Pressure-independent valves",
                  "<p>A <strong>PICV</strong> holds the flow for a given opening constant even when pump pressure changes — so "
                  "when other valves close, this coil is not suddenly over-supplied. Its maximum flow is set with a dial, "
                  "replacing a separate balancing valve. It needs a minimum ΔP across it (from the datasheet) to work.</p>")
    ),
    ahu01=("<p>AHU-01's CHW valve is a <strong>2-way, equal-percentage valve with a modulating actuator</strong> (24 V AC, 0–10 V "
           "control from an AO). On power loss it stays where it is (non-spring-return). The program closes it whenever the "
           "fan is off, so the coil does not get cold and sweat when there is no airflow.</p>"),
    on_site=[
        "Look at the flow arrow on the valve body — globe valves fitted backwards chatter and leak.",
        "Check the actuator is fully coupled: command 0 % and 100 % and watch the stem or indicator move the full stroke.",
        "To test for passing (leaking), command 0 % with the AHU running: supply air and the pipe after the valve should warm up.",
        "Note the PICV's maximum-flow dial setting and check it against the balancing schedule.",
    ],
    faults=[
        ("Valve at 100 % but little cooling", "Isolation valve shut, blocked strainer, air in coil, actuator decoupled", "Feel the pipes; isolation valves; strainer"),
        ("Loop hunts at low load", "Oversized valve or low authority", "Valve Kvs vs required; consider a PICV or smaller valve"),
        ("Room cold with valve commanded closed", "Valve passing: worn seat, or close-off pressure exceeded", "Pipe temperature after the valve; close-off rating vs pump head"),
        ("Valve opens when the BMS closes it", "Direct/reverse action wrong", "Actuator setting; signal type"),
        ("Valve moves only part of its stroke", "Actuator not adapted, or wrong 0–10 / 2–10 V setting", "Adaptation; signal range"),
    ],
    terms=[
        ("2-way valve", "Valve that varies flow through the coil; system flow varies."),
        ("3-way valve", "Valve that diverts unused flow through a bypass; system flow stays constant."),
        ("Kv / Kvs", "Flow (m³/h) at 1 bar drop; Kvs is the value when fully open."),
        ("Valve authority", "Share of circuit pressure drop taken by the valve; about 0.5 is good."),
        ("Equal-percentage", "Valve characteristic where each step of opening increases flow by the same percentage."),
        ("PICV", "Pressure-independent control valve — flow set by opening, unaffected by system pressure."),
        ("Close-off pressure", "Maximum ΔP against which a valve and actuator can shut tight."),
        ("Passing valve", "A valve that leaks flow when commanded closed."),
    ],
    scenarios=[dict(
        prompt="AHU-01's return air temperature swings ±1.5 °C every few minutes at light load, but is steady at full load. The valve was replaced last month with a much larger one “to be safe”. What is the likely cause?",
        options=["The return air sensor is faulty.", "The new valve is oversized, so a tiny movement gives a big change in cooling at low load.",
                 "The chiller is short-cycling."],
        answer=1,
        explain=(" An oversized valve works in the bottom few percent of its stroke at low load, where small movements make large "
                 "changes — the loop hunts. Size the valve to the coil (Kv), or use a PICV."),
    )],
    questions=[
        ("Why do most modern systems use 2-way valves?", "System flow then varies with load, so pumps can slow down (saving energy) and return water stays warm (good ΔT)."),
        ("A coil needs 4 m³/h with a 0.16 bar valve drop. What Kv is needed?", "Kv = 4 ÷ √0.16 = 4 ÷ 0.4 = 10."),
        ("Why are equal-percentage valves used on coils?", "Coils give most of their output at low flow; an equal-percentage valve compensates, so the combined response is close to linear and the loop is stable at every load."),
        ("What does close-off pressure mean?", "The maximum pressure difference against which the valve and actuator can close tightly; above it the valve passes."),
        ("What is the advantage of a PICV?", "Its flow depends only on its opening, not on changes in system pressure, so coils are not over- or under-supplied as other valves move; it also replaces the balancing valve."),
    ],
)

P7 = dict(
    id="3-7", slug="variable-frequency-drives", title="Variable frequency drives (VFD)",
    objectives=[
        "Explain how a VFD changes motor speed.",
        "List the hard-wired and network signals between a BMS and a VFD.",
        "Name the VFD parameters that matter for BMS control.",
        "Diagnose common VFD control and communication faults.",
    ],
    one_line=("A VFD (variable frequency drive, also called an inverter or variable speed drive) <strong>changes a motor's speed "
              "by changing the frequency of its supply</strong> — so fans and pumps deliver only what is needed, using far less energy."),
    why=("<p>Almost every new fan and pump in a commercial building has a VFD, and the fan laws (page 2.4) mean they save a lot "
         "of energy. For the BMS engineer a VFD is a busy interface: hard-wired start, status and speed signals plus a "
         "communication link — and several parameters that decide whether the BMS is actually in control.</p>"),
    body=(
        fig(d_vfd(), "Inside a VFD and the signals between it and the controller.")
        + "<h3>How it works</h3>"
        + steps([
            "The <strong>rectifier</strong> turns the incoming AC supply (e.g. 415 V, 50 Hz) into DC.",
            "The <strong>DC bus</strong> capacitors smooth and store that DC.",
            "The <strong>inverter</strong> switches the DC very fast to build a new AC supply at whatever frequency is required.",
            "Motor speed is proportional to frequency: 50 Hz = full speed, 25 Hz ≈ half speed.",
        ])
        + "<h3>The BMS interface</h3>"
        + table(["Signal", "Direction", "Type", "Notes"], [
            ("Run / start", "BMS → VFD", "DO via interposing relay to a VFD digital input", "Contact closed = run"),
            ("Speed reference", "BMS → VFD", "AO, 0–10 V or 4–20 mA", "VFD input type and scaling must match"),
            ("Run status", "VFD → BMS", "Relay output → DI", "Means the drive output is on"),
            ("Fault", "VFD → BMS", "Relay output → DI", "Often normally-closed for fail-safe"),
            ("Speed / current feedback", "VFD → BMS", "Analogue output → AI (optional)", ""),
            ("Network", "Both ways", "Modbus RTU, BACnet MS/TP or IP", "Frequency, current, kW, kWh, fault codes, run-hours"),
        ])
        + "<h3>Parameters that matter to the BMS</h3>"
        + table(["Parameter", "Why it matters"], [
            ("Control (command) source", "Keypad/local, terminals, or fieldbus. If it is set to keypad, the BMS start command is ignored."),
            ("Reference (speed) source", "Which input sets the speed: AI, keypad, fieldbus."),
            ("Analogue input type and scaling", "0–10 V or 4–20 mA, and what 0 % and 100 % mean in Hz."),
            ("Minimum / maximum frequency", "Minimum keeps airflow and motor cooling (often around 20–25 Hz for fans); maximum usually 50 Hz."),
            ("Acceleration / deceleration ramps", "Too short and the drive trips on over-current or over-voltage."),
            ("Loss-of-reference action", "What the drive does if the 4–20 mA signal disappears: stop, hold, or go to a preset speed."),
            ("Auto-restart", "Whether it restarts by itself after a power dip or a fault reset."),
            ("Skip frequencies", "Speeds to avoid because they make the fan or ductwork resonate."),
            ("Motor nameplate data", "Voltage, current, power, speed — needed for protection and good control."),
        ])
        + callout("warn", "Stored energy",
                  "<p>The DC bus capacitors stay charged for minutes after isolation. Wait for the time printed on the drive "
                  "(often 5–15 minutes) and check the DC bus has discharged before touching power terminals. Motor cables are "
                  "screened; keep BMS signal cables away from them and land screens as the maker says, or the drive's switching "
                  "noise will appear on your analogue signals.</p>")
        + "<h3>Hand–Off–Auto on the keypad</h3>"
        + "<p>Most drives have their own Hand/Off/Auto keys. In <strong>Hand</strong> the speed comes from the keypad; in "
          "<strong>Auto</strong> the BMS controls start and speed. A drive left in Hand after maintenance is a very common "
          "reason for “the BMS has lost control”. The drive's relay or a network value can report which mode it is in.</p>"
        + "<h3>Bypass</h3>"
        + "<p>Some critical fans and pumps have a <strong>bypass</strong> starter so the motor can run direct-on-line at full "
          "speed if the drive fails. The BMS should know which path is running (a DI from the bypass contactor).</p>"
    ),
    ahu01=("<p>AHU-01's supply fan VFD gets: <strong>start</strong> from a DO via an interposing relay, <strong>speed</strong> from an "
           "AO (0–10 V = 0–50 Hz), and returns <strong>run</strong> and <strong>fault</strong> relays to DIs. Over <strong>Modbus "
           "RTU</strong> the BMS reads frequency, current, kW, kWh and the last fault code. Control source: terminals; minimum "
           "frequency 20 Hz; it normally runs at 42 Hz.</p>"),
    on_site=[
        "When the BMS “has no control”, look at the keypad first: Hand or Auto? Local or remote?",
        "Check that the AI type on the drive (voltage or current, often a switch as well as a parameter) matches the BMS output.",
        "Record the key parameters after commissioning; a drive replacement then takes minutes, not hours.",
        "Compare the frequency on the drive display with what the BMS commands — a mismatch points at scaling.",
    ],
    faults=[
        ("Drive runs from its keypad but ignores the BMS", "Control source set to local/keypad, or drive in Hand", "Keypad mode; control source parameter"),
        ("BMS commands 100 %, drive sits at 20 Hz", "Speed input misconfigured (V vs mA), broken wire, or reference source wrong", "AI type switch/parameter; voltage at the terminal"),
        ("Trips on over-current when starting", "Acceleration ramp too short, or mechanical problem", "Ramp time; fan/belt/bearing"),
        ("Trips on over-voltage when stopping", "Deceleration ramp too short", "Decel time or braking setting"),
        ("Unstable analogue readings across the plant room", "Drive noise coupled into signal cables", "Cable routes, screened motor cable, earthing"),
        ("Modbus values all zero", "Wrong address, baud rate or register map", "Module 5"),
    ],
    terms=[
        ("VFD", "Variable frequency drive: varies motor speed by varying supply frequency."),
        ("DC bus", "Internal DC stage of the drive; stays charged after power is removed."),
        ("Speed reference", "Analogue or network signal telling the drive what speed to run."),
        ("Control source", "Parameter deciding whether start/stop comes from keypad, terminals or fieldbus."),
        ("Ramp time", "Time the drive takes to accelerate or decelerate."),
        ("Minimum frequency", "Lowest speed the drive will run at."),
        ("Skip frequency", "A speed band the drive avoids because of resonance."),
        ("Bypass", "Contactor arrangement to run the motor directly if the drive fails."),
    ],
    scenarios=[dict(
        prompt="The BMS shows AHU-01's speed command at 100 %, but the VFD display shows 20 Hz and the fan is slow. Run status is ON. What is the most likely cause?",
        options=["The VFD is in Hand.", "The drive's speed input does not match the signal — e.g. set for 4–20 mA while the BMS sends 0–10 V — so it sits at minimum speed.",
                 "The fan belt is broken."],
        answer=1,
        explain=(" The drive is running (status ON) and obeying the start, but reads no useful speed reference, so it holds minimum "
                 "frequency. Check the AI type (switch and parameter), the reference source and the voltage at the terminals."),
    )],
    questions=[
        ("Explain in three steps how a VFD makes a variable-frequency supply.", "Rectifier converts AC to DC → DC bus stores and smooths it → inverter switches the DC to make AC at the required frequency."),
        ("List four hard-wired signals between the BMS and a VFD.", "Start (DO), speed reference (AO), run status (DI), fault (DI)."),
        ("Why does a fan VFD have a minimum frequency?", "To keep enough airflow and motor cooling, and avoid running the fan too slowly to be useful."),
        ("What is the danger of the DC bus after isolation?", "The capacitors remain charged for several minutes; touching power terminals before they discharge can be lethal."),
        ("The drive ignores the BMS start command. Name two settings to check.", "Whether the keypad is in Hand/local, and the control (command) source parameter."),
    ],
)

P8 = dict(
    id="3-8", slug="status-devices", title="Status devices: current switches and DP switches",
    objectives=[
        "Explain why a start command is not proof that equipment is running.",
        "Compare the ways of proving a fan or pump is running and what each really proves.",
        "Set up a current switch and a fan ΔP switch correctly.",
        "Write the logic for fan-fail and unexpected-running alarms.",
    ],
    one_line=("A status device gives the BMS <strong>independent proof</strong> that equipment is really running — because a start "
              "command only shows what the BMS asked for, not what happened."),
    why=("<p>Contactors stick, belts break, drives trip and fans spin backwards. If the BMS only knows what it commanded, it will "
         "show a fan as “running” while the floor overheats. Good status devices — and alarms comparing command with status — "
         "catch these failures in seconds.</p>"),
    body=(
        fig(d_proving(), "Each device proves a different link in the chain. The further down the chain, the stronger the proof.")
        + table(["Device", "Proves…", "Does NOT prove…"], [
            ("Contactor auxiliary contact", "The contactor pulled in", "Motor turning; belt intact; air moving"),
            ("VFD run relay", "The drive's output is on", "Belt intact; fan moving air"),
            ("Current switch / sensor", "The motor draws current", "Air moving (unless set above no-load current)"),
            ("Fan ΔP switch", "The fan is building pressure — moving air", "Exact airflow"),
            ("Airflow switch or sensor", "Air is flowing in the duct", "—"),
            ("Water flow switch", "Water flowing in a pipe", "Exact flow rate"),
            ("Damper end switch", "Damper reached its end position", "Blades sealed"),
        ])
        + "<h3>Current switches</h3>"
        + "<p>A current switch is a small current transformer (CT) clipped round <strong>one</strong> phase conductor of the motor "
          "cable, with a contact that closes when the current rises above an adjustable threshold. Split-core versions clip on "
          "without disconnecting the cable.</p>"
        + steps([
            "Run the motor normally and note the current (from the drive display or a clamp meter).",
            "Break the load if you can do so safely — e.g. with the belt removed the motor draws only its <strong>no-load</strong> current.",
            "Set the threshold <strong>between</strong> the no-load current and the lowest normal running current. Now a broken belt shows as “not running”.",
            "On VFD motors, use a current switch rated for variable frequency and check it still trips at minimum speed — or read the current from the drive over the network.",
        ])
        + "<h3>Fan ΔP switches</h3>"
        + "<p>A ΔP switch across the fan — + to the outlet side, − to the inlet — closes when the fan builds pressure. Set it "
          "well below the lowest normal running ΔP (at minimum speed) but clearly above zero, so it proves airflow without "
          "chattering. Filter ΔP switches use the same device to a different purpose (page 3.3).</p>"
        + "<h3>Using status in logic</h3>"
        + table(["Condition", "Meaning", "Action"], [
            ("Command ON, status OFF for > 30 s", "Failed to start or stopped unexpectedly", "“Fan fail” alarm; stop command; lock out until reset"),
            ("Command OFF, status ON for > 60 s", "Running when it should not — Hand mode, welded contactor", "“Running unexpectedly” alarm"),
            ("Status flickers on and off", "Threshold too close to running value, loose wiring", "Maintenance alarm; check set point"),
        ])
        + callout("tip", "Delays matter", "<p>Every status check needs a delay: a fan takes a few seconds to prove after a start "
                  "command, and some seconds to stop. Too short and you get nuisance alarms; too long and failures go unnoticed.</p>")
    ),
    ahu01=("<p>AHU-01 proves its fan with the <strong>VFD run relay</strong> (DI) — which shows the drive is on — and checks the "
           "<strong>VFD motor current over Modbus</strong>: if the drive runs but the current is close to no-load, the BMS raises a "
           "“possible belt failure” alarm. The supply duct pressure sensor gives a third, independent check that air is moving.</p>"),
    on_site=[
        "Find out what the status point is really wired to — an auxiliary contact proves much less than a ΔP switch.",
        "Test the proving: stop the fan locally with the BMS command still on — the fan-fail alarm must appear after its delay.",
        "Re-check current-switch thresholds after motor or belt changes.",
        "For DP switches, check the tubes are on the right sides and not blocked.",
    ],
    faults=[
        ("BMS shows “running” but the floor is hot and air is still", "Status from a contactor or drive relay; belt broken", "Look at the fan; motor current"),
        ("Fan-fail alarm on every start", "Proving delay too short, or ΔP switch set too high", "Delay and switch setting"),
        ("Status flickers at low speed", "Current or ΔP threshold too close to the low-speed value", "Threshold vs value at minimum speed"),
        ("“Running unexpectedly” alarm", "Fan in Hand, contactor welded, or another system started it", "HOA, contactor, fire/smoke control"),
    ],
    terms=[
        ("Status / proving", "Independent feedback that equipment is really running."),
        ("Auxiliary contact", "Extra contact on a contactor that changes state when it pulls in."),
        ("Current switch", "CT with a contact that closes above an adjustable current."),
        ("No-load current", "Current a motor draws with no mechanical load, e.g. with the belt off."),
        ("Fan ΔP switch", "Pressure switch across a fan that proves it is building pressure."),
        ("Fan fail", "Alarm when a fan is commanded on but status is not proven."),
        ("Proving delay", "Time allowed between a command and the expected status."),
    ],
    scenarios=[dict(
        prompt="An AHU's status comes from the contactor's auxiliary contact. The fan belt snaps at 11:00. What does the BMS show, and how would you prevent this blind spot?",
        options=["It shows fan fail immediately — no change needed.",
                 "It still shows “running”, because the contactor is still pulled in. Use a correctly-set current switch or a fan ΔP switch for status.",
                 "It shows the fan off, because the motor stops."],
        answer=1,
        explain=(" The contactor stays energised and the motor keeps spinning, so the auxiliary contact stays closed. Only a device "
                 "further down the chain — current above no-load, or fan ΔP — detects the broken belt."),
    )],
    questions=[
        ("Why is a DO start command not proof that a fan is running?", "It only shows what the BMS asked for. Tripped overloads, Hand switches, broken belts and failed drives all leave the command ON while the fan is not moving air."),
        ("Where should a current switch threshold be set?", "Between the motor's no-load current and its lowest normal running current, so a broken belt reads as “not running”."),
        ("What does a fan ΔP switch prove that a VFD run relay does not?", "That the fan is actually building pressure — moving air — not just that the drive output is on."),
        ("Write the logic for a fan-fail alarm.", "If the start command is ON and run status is OFF for more than the proving delay (e.g. 30 s), raise “fan fail”, stop the fan and lock out until reset."),
        ("What does a “running unexpectedly” alarm usually mean?", "The equipment runs while the BMS commands it off — often a Hand switch, a welded contactor, or another system (e.g. fire control) starting it."),
    ],
)

MODULE_INTRO = (
    "<p>Field devices are where the BMS meets the physical building. This module covers what each common sensor and actuator "
    "measures or moves, how to choose and mount it, the signals it uses, and how it fails. Two interactive tools help: the "
    "NTC/PT1000 calculator on page 3.1, and the scaling calculator you will meet in Module 4.</p>"
)

PAGES = [P1, P2, P3, P4, P5, P6, P7, P8]

QUIZ = [
    mcq("What happens to a PT1000's resistance as temperature rises?", ["It falls sharply", "It rises about 3.85 Ω per °C",
        "It stays the same", "It rises 440 Ω per °C"], 1, "PT1000: 1,000 Ω at 0 °C, rising about 3.85 Ω/°C.", "3.1"),
    mcq("An NTC sensor input suddenly reads −40 °C. Most likely cause?", ["Short circuit", "Open circuit", "Wrong setpoint", "Sun on the sensor"], 1,
        "Open circuit → infinite resistance → an NTC reads very cold.", "3.1"),
    mcq("A 0–10 V CO₂ sensor scaled 0–2,000 ppm reads 5 V. CO₂ is…", ["500 ppm", "1,000 ppm", "2,000 ppm", "5,000 ppm"], 1,
        "5 V × 200 ppm/V = 1,000 ppm.", "3.2"),
    mcq("Why can automatic baseline calibration fail in a hospital ward?", ["The sensor is too old", "The space is never empty, so it never sees outdoor-level CO₂",
        "Hospitals use CO instead", "NDIR does not work indoors"], 1, "ABC assumes the lowest recent reading is outdoor air.", "3.2"),
    mcq("A filter ΔP sensor reads −90 Pa with the fan running. What is wrong?", ["Filter torn", "Tubes swapped", "Sensor range too high", "Nothing"], 1,
        "Pressure is higher before the filter; + belongs there.", "3.3"),
    mcq("Velocity pressure is 100 Pa. Air velocity is about…", ["1.3 m/s", "10 m/s", "12.9 m/s", "129 m/s"], 2, "v ≈ 1.29 × √100 = 12.9 m/s.", "3.3"),
    mcq("An energy meter reads negative power with correct flow. Most likely?", ["Meter reversed", "Temperature sensors swapped", "Pipe empty", "Pulse weight wrong"], 1,
        "Return reading colder than supply gives negative energy.", "3.4"),
    mcq("A floating (3-point) actuator needs…", ["one AO", "two DOs", "one DI", "a 4–20 mA loop"], 1, "One output drives open, the other drives close.", "3.5"),
    mcq("Why are equal-percentage valves used on cooling coils?", ["They are cheaper", "They compensate for the coil's non-linear output",
        "They never leak", "They need no actuator"], 1, "Valve + coil together give a near-linear response.", "3.6"),
    mcq("A belt breaks. Which status device will still say the fan is running?", ["Fan ΔP switch", "Correctly set current switch",
        "Contactor auxiliary contact", "Airflow switch"], 2, "The contactor stays pulled in even though no air moves.", "3.8"),
]

FINAL = [
    mcq("Why is PT1000 preferred to PT100 for 2-wire BMS inputs?", ["It is cheaper", "Cable resistance causes a ten times smaller error",
        "It is an NTC", "It needs no configuration"], 1, "3.85 Ω/°C vs 0.385 Ω/°C.", "3.1"),
    mcq("What does DCV adjust?", ["Chilled water temperature", "Fresh air according to CO₂", "Fan belt tension", "Filter grade"], 1,
        "Demand-controlled ventilation varies fresh air with occupancy.", "3.2"),
    mcq("Kv for 6 m³/h at 0.36 bar valve drop is…", ["6", "10", "16.7", "2.2"], 1, "6 ÷ √0.36 = 6 ÷ 0.6 = 10.", "3.6"),
    mcq("A VFD ignores the BMS start command but runs from its keypad. Check first…", ["Motor insulation", "Control source / Hand–Auto mode",
        "Duct pressure", "Filter"], 1, "The drive must be in Auto with the control source set to terminals or fieldbus.", "3.7"),
    mcq("A fresh air damper actuator is usually…", ["spring-return open", "spring-return closed", "never spring-return", "floating only"], 1,
        "Closed on power loss keeps unconditioned air out.", "3.5"),
]
