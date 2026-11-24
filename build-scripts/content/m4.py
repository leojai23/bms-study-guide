# -*- coding: utf-8 -*-
"""Module 4 — Digital and Analog I/O. Vendor-neutral. Electrical safety content is general guidance:
local regulations, site rules and the competent person's judgement always take precedence."""
from bms_common import (table, steps, bullets, callout, cards, fig, svg, defs, t, rect, box,
                        line, path, circle, mcq, tool)

# ==========================================================================
# Diagrams
# ==========================================================================

def d_prove_test_prove():
    i = defs("pt")
    items = [("1 · Identify", "drawings, labels|all sources", "d-box"), ("2 · Isolate", "switch off|isolator / MCB", "d-box"),
             ("3 · Lock + tag", "personal padlock|and tag", "d-warn"), ("4 · Prove tester", "on a known|live source", "d-acc"),
             ("5 · Test dead", "every conductor|pair", "d-acc"), ("6 · Re-prove", "tester still|works", "d-acc")]
    for k, (a, b, c) in enumerate(items):
        x = 8 + k * 126
        i += box(x, 40, 112, 70, a, b, c)
        if k < 5:
            i += line(x + 112, 75, x + 124, 75, "d-aline", end="pt-a")
    i += path("M384,110 L384,140 L760,140", "d-line d-dash") + t(574, 154, "steps 4–6: “prove – test – prove”", "d-ts d-ta")
    i += t(380, 22, "Only after step 6 is the circuit treated as dead", "d-ts d-tb")
    return svg(770, 170, i, "Safe isolation steps")


def d_io_quadrants():
    i = defs("io")
    i += rect(260, 70, 240, 150, "d-acc", 12) + t(380, 135, "DDC-AHU-01", "d-tl d-tb") + t(380, 158, "controller", "d-ts")
    quads = [(20, 40, "DI · digital in", "on / off INTO the controller", ["Fan run status", "Fan fault", "Auto/manual", "Filter dirty", "Fire shutdown"]),
             (540, 40, "DO · digital out", "on / off OUT of the controller", ["Fan start/stop"]),
             (20, 210, "AI · analogue in", "a range of values IN", ["Return air temp (NTC)", "Supply air temp (NTC)", "Return RH (0–10 V)", "Return CO₂ (0–10 V)", "Duct pressure (4–20 mA)"]),
             (540, 210, "AO · analogue out", "a range of values OUT", ["CHW valve 0–10 V", "VFD speed 0–10 V", "Fresh air damper 0–10 V"])]
    for x, y, a, b, items in quads:
        i += rect(x, y, 200, 56 + 15 * len(items), "d-box", 8) + t(x + 100, y + 16, a, "d-t d-tb") + t(x + 100, y + 32, b, "d-ts")
        for k, s in enumerate(items):
            i += t(x + 14, y + 52 + 15 * k, "· " + s, "d-ts", "start")
    i += line(220, 90, 258, 110, "d-line", end="io") + line(220, 260, 258, 200, "d-line", end="io")
    i += line(502, 110, 540, 90, "d-line", end="io") + line(502, 200, 540, 240, "d-line", end="io")
    return svg(760, 345, i, "The four I/O types with AHU-01 examples")


def d_loops():
    i = defs("lp")
    # 2-wire
    i += t(130, 16, "2-wire (loop-powered) 4–20 mA", "d-t d-tb")
    i += box(20, 40, 90, 60, "24 V DC", "supply", "d-warn")
    i += box(150, 150, 110, 60, "Transmitter", "e.g. 0–500 Pa", "d-box")
    i += box(150, 40, 110, 60, "Controller AI", "mA input", "d-acc")
    i += path("M65,100 L65,170 L148,170", "d-line", end="lp") + t(60, 135, "+", "d-t d-tb", "end")
    i += path("M262,170 L285,170 L285,70 L262,70", "d-line", end="lp")
    i += path("M148,70 L120,70 L120,55 L110,55", "d-line", end="lp") + t(118, 52, "−", "d-t d-tb", "end")
    i += t(135, 228, "the same current flows all round the loop", "d-ts")
    # 3-wire 0-10 V
    i += t(470, 16, "3-wire 0–10 V transmitter", "d-t d-tb")
    i += box(330, 40, 90, 60, "24 V", "AC or DC", "d-warn")
    i += box(420, 150, 110, 60, "Transmitter", "e.g. RH", "d-box")
    i += box(530, 40, 110, 60, "Controller AI", "0–10 V input", "d-acc")
    i += path("M375,100 L375,165 L418,165", "d-line", end="lp") + t(370, 135, "24 V", "d-ts", "end")
    i += path("M532,180 L585,180 L585,102", "d-aline", end="lp-a") + t(592, 140, "signal", "d-ts d-ta", "start")
    i += path("M420,195 L340,195 L340,100", "d-line d-dash") + t(400, 228, "0 V / common shared by supply and signal", "d-ts")
    i += path("M475,150 L475,120 L640,120 L640,100", "d-line d-dash")
    return svg(760, 240, i, "Two-wire 4–20 mA loop and three-wire 0–10 V transmitter wiring")


def d_contacts():
    i = ""
    labels = [(70, "NO (normally open)", "closes when operated"), (260, "NC (normally closed)", "opens when operated"),
              (470, "Changeover (SPDT)", "COM swaps NC → NO"), (670, "Coil", "relay coil (A1 / A2)")]
    # NO
    i += line(40, 70, 60, 70) + line(60, 70, 92, 52) + line(96, 70, 116, 70) + circle(60, 70, 3, "d-fillink") + circle(96, 70, 3, "d-fillink")
    # NC
    i += line(230, 70, 250, 70) + line(250, 70, 292, 78) + line(286, 70, 306, 70) + line(286, 64, 286, 82)
    i += circle(250, 70, 3, "d-fillink") + circle(286, 70, 3, "d-fillink")
    # changeover
    i += line(430, 70, 450, 70) + line(450, 70, 490, 82) + circle(450, 70, 3, "d-fillink")
    i += line(486, 92, 520, 92) + line(486, 52, 520, 52) + line(486, 86, 486, 98) + circle(486, 92, 3, "d-fillink") + circle(486, 52, 3, "d-fillink")
    i += t(426, 70, "COM", "d-ts", "end") + t(526, 92, "NC", "d-ts", "start") + t(526, 52, "NO", "d-ts", "start")
    # coil
    i += rect(650, 56, 40, 28, "d-box", 3) + line(630, 70, 650, 70) + line(690, 70, 710, 70)
    i += t(626, 70, "A1", "d-ts", "end") + t(714, 70, "A2", "d-ts", "start")
    for x, a, b in labels:
        i += t(x, 120, a, "d-ts d-tb") + t(x, 136, b, "d-ts")
    i += t(380, 20, "Contacts are always drawn in their NORMAL state: relay not energised, device not operated", "d-ts d-ta")
    return svg(760, 150, i, "Contact symbols: normally open, normally closed, changeover, and a relay coil")


def d_di_wiring():
    i = defs("dw")
    i += t(190, 16, "Dry contact into a DI", "d-t d-tb") + t(570, 16, "Fail-safe NC loop (fire shutdown)", "d-t d-tb")
    i += box(20, 40, 130, 130, "Controller", "DI1|COM", "d-acc")
    i += line(150, 85, 240, 85) + line(150, 125, 240, 125)
    i += line(240, 85, 240, 95) + line(240, 95, 260, 110) + line(240, 125, 240, 115)
    i += t(272, 105, "filter ΔP switch", "d-ts", "start") + t(272, 120, "(NO, volt-free)", "d-ts", "start")
    i += t(190, 190, "the controller supplies a small", "d-ts") + t(190, 204, "“wetting” voltage; the contact just closes", "d-ts")
    i += line(380, 30, 380, 220, "d-line d-dash d-thin")
    i += box(400, 40, 110, 50, "FAS relay", "energised = healthy", "d-bad")
    i += box(400, 150, 110, 50, "AHU-01 DI", "+ starter circuit", "d-acc")
    i += path("M510,55 L600,55 L600,90", "d-line") + path("M600,110 L600,175 L512,175", "d-line", end="dw")
    i += line(600, 90, 612, 104) + line(600, 110, 600, 104)
    i += t(618, 96, "contact closed when healthy", "d-ts", "start")
    i += t(570, 225, "fire OR broken wire → contact opens → AHU stops", "d-ts d-tb")
    return svg(760, 235, i, "Wiring a dry contact to a digital input, and a fail-safe normally-closed loop")


def d_troubleshoot():
    i = defs("ts")
    i += box(250, 6, 260, 40, "A reading looks wrong", "", "d-warn")
    i += line(380, 46, 380, 64, "d-line", end="ts")
    i += box(200, 64, 360, 44, "1 · Check the BMS point", "override? out of service? type and range?", "d-box")
    i += line(380, 108, 380, 126, "d-line", end="ts")
    i += box(200, 126, 360, 44, "2 · Measure at the controller terminals", "what does the controller actually receive?", "d-box")
    i += line(380, 170, 380, 188, "d-line", end="ts")
    i += box(270, 188, 220, 44, "Does it match the BMS?", "", "d-acc")
    i += path("M270,210 L150,210 L150,250", "d-line", end="ts") + t(208, 200, "no", "d-ts d-tb")
    i += path("M490,210 L610,210 L610,250", "d-line", end="ts") + t(550, 200, "yes", "d-ts d-tb")
    i += box(30, 250, 240, 54, "Controller side", "configuration, scaling, input card", "d-box")
    i += box(490, 250, 240, 54, "Field side", "disconnect · measure cable · then device", "d-box")
    i += path("M610,304 L610,322 L380,322 L380,340", "d-line", end="ts") + path("M150,304 L150,322 L380,322", "d-line")
    i += box(230, 340, 300, 40, "Fix → verify on BMS → record what you did", "", "d-ok")
    return svg(760, 390, i, "Troubleshooting a wrong reading")


def d_symbols():
    i = ""
    cells = [("T", "Temperature sensor"), ("H", "Humidity sensor"), ("P", "Pressure sensor"), ("ΔP", "ΔP sensor / switch"),
             ("CO₂", "CO₂ sensor"), ("F", "Flow meter / switch"), ("CT", "Current switch"), ("M", "Actuator (motor)")]
    for k, (s, lab) in enumerate(cells):
        x = 50 + (k % 4) * 190
        y = 40 + (k // 4) * 70
        i += circle(x, y, 16, "d-box") + t(x, y, s, "d-ts d-tb") + t(x + 26, y, lab, "d-ts", "start")
    y = 200
    i += path(f"M40,{y - 8} L56,{y - 8} L48,{y} Z M40,{y + 8} L56,{y + 8} L48,{y} Z", "d-box") + line(48, y, 48, y - 22) + rect(40, y - 36, 16, 14, "d-box", 2)
    i += t(70, y, "Control valve + actuator", "d-ts", "start")
    i += rect(240, y - 16, 30, 32, "d-box", 3) + line(242, y + 14, 268, y - 14) + t(282, y, "Damper", "d-ts", "start")
    i += circle(450, y, 16, "d-box") + path(f"M441,{y + 9} L462,{y} L441,{y - 9} Z") + t(474, y, "Fan / pump", "d-ts", "start")
    i += path(f"M610,{y - 16} L600,{y - 8} L620,{y} L600,{y + 8} L610,{y + 16}") + t(632, y, "Filter", "d-ts", "start")
    i += t(380, 250, "Symbols vary between companies — every drawing set has its own legend sheet. Read it first.", "d-ts d-ta")
    return svg(760, 265, i, "Common symbols on BMS control schematics")


def d_naming():
    i = ""
    parts = [("B1", "building"), ("L03", "floor / level"), ("AHU01", "equipment"), ("RAT", "point")]
    x = 110
    for k, (a, b) in enumerate(parts):
        w = 40 + len(a) * 14
        i += box(x, 30, w, 50, a, "", "d-acc", "d-tl d-tb", 8)
        i += t(x + w / 2, 100, b, "d-ts")
        if k < 3:
            i += t(x + w + 10, 55, "–", "d-tl d-tb")
        x += w + 20
    i += t(380, 130, "B1-L03-AHU01-RAT  =  Building 1, Level 3, AHU-01, return air temperature", "d-t d-mono")
    return svg(760, 145, i, "Anatomy of a point name")


# ==========================================================================
# Pages
# ==========================================================================

P1 = dict(
    id="4-1", slug="electrical-safety", title="Electrical safety for BMS work",
    objectives=[
        "Name the voltages found in BMS panels and why “24 V” areas are not automatically safe.",
        "Follow the safe-isolation steps, including prove–test–prove.",
        "Recognise BMS-specific hazards: remote starts, foreign voltages, stored energy, spring returns.",
        "Use a multimeter safely for BMS measurements.",
    ],
    one_line=("BMS work mixes 415 V motor circuits, 230 V panel supplies and 24 V controls in the same rooms and sometimes the "
              "same panel — so you <strong>isolate, lock, and prove dead</strong> before you touch, and you never trust a "
              "screen that says equipment is “off”."),
    why=("<p>Most BMS signals are low voltage, which makes it easy to forget that the panel next to them — or a terminal in the "
         "same row — can be at 230 V, and that the fan you are working on can be started by a schedule on a server in "
         "another building. This page comes before wiring on purpose. Read it, and follow your site's rules and permits: "
         "they always take precedence over this guide.</p>"),
    body=(
        "<h3>Voltages you will meet</h3>"
        + table(["Voltage", "Where", "Notes"], [
            ("415 V AC, 3-phase", "MCCs, VFDs, motors, chillers", "Lethal; arc-flash risk in large panels — authorised people only"),
            ("230 V AC, single-phase", "Panel supplies, transformer primaries, some actuators and contactor coils, lighting", "Lethal"),
            ("24 V AC / DC", "Controllers, actuators, sensors", "Extra-low voltage (ELV) — but shares panels with 230 V"),
            ("0–10 V, 4–20 mA, RS485", "Signals", "Low energy — but can carry dangerous voltage under fault conditions"),
        ])
        + callout("warn", "“Volt-free” is not always volt-free",
                  "<p>Contacts that should be volt-free sometimes carry a <strong>foreign voltage</strong> — for example a 230 V "
                  "control circuit from the MCC looped through BMS terminals. A DI terminal that reads 230 V will destroy "
                  "the input card and can kill. Measure before you touch, and label any foreign voltage in a panel clearly.</p>")
        + "<h3>Safe isolation</h3>"
        + fig(d_prove_test_prove(), "The safe-isolation sequence. Testing a circuit dead with an unproven tester proves nothing.")
        + steps([
            "<strong>Identify</strong> every source feeding what you will work on — drawings, labels, and back-feeds such as UPS supplies or MCC control circuits.",
            "<strong>Isolate</strong> at the correct isolator or MCB.",
            "<strong>Lock off and tag</strong> with your own padlock and a tag giving your name and the date. You keep the key.",
            "<strong>Prove</strong> your voltage tester on a known live source or proving unit.",
            "<strong>Test dead</strong> between every pair of conductors: L–N, L–E, N–E (and between phases on 3-phase).",
            "<strong>Re-prove</strong> the tester to show it did not fail during the test.",
        ])
        + "<h3>Hazards specific to BMS</h3>"
        + table(["Hazard", "Why it happens", "Control"], [
            ("Remote start", "Schedules, overrides, other operators, fire or smoke control can start fans and pumps at any time", "Isolate and lock the local isolator before touching fans, belts, pumps or dampers"),
            ("Foreign voltage", "Control circuits from other panels looped into BMS terminals", "Measure first; label; isolate at the source too"),
            ("Stored energy in VFDs", "DC bus capacitors stay charged for minutes", "Wait the time on the label; measure the DC bus"),
            ("Spring-return actuators", "Dampers and valves snap to their safe position when power is removed", "Keep fingers out of damper blades and linkages"),
            ("Back-feed", "UPS or generator supplies; neutral shared between circuits", "Identify all sources; test every conductor"),
            ("Working at height, confined spaces", "Ceiling voids, AHU rooms, shafts", "Correct access equipment and permits"),
        ])
        + "<h3>Using a multimeter safely</h3>"
        + bullets([
            "Use a meter and leads rated for the panel: at least <strong>CAT III 600 V</strong> for building distribution work.",
            "Select the function <strong>before</strong> connecting. Never put a meter in current (A or mA) mode across a voltage — it is a short circuit through the meter.",
            "To measure a 4–20 mA loop, put the meter <strong>in series</strong> at a test point or terminal designed to be opened, or use a mA clamp meter — never across the loop supply.",
            "Measure resistance only on <strong>de-energised</strong> circuits, with the device disconnected.",
            "Keep one hand away from the panel when probing live terminals, and use insulated probe tips.",
        ])
        + callout("note", "Live work", "<p>Some diagnosis needs measurements on live circuits. That is done only when it is "
                  "necessary, by a competent person, with a risk assessment and the right PPE — never as a short-cut. Your "
                  "site's permit-to-work system and local electrical regulations decide who may do what.</p>")
    ),
    ahu01=("<p>Before changing AHU-01's fan belt: the BMS shows the fan off by schedule — that is <strong>not</strong> isolation. Turn "
           "off and lock the AHU's local isolator (and the VFD supply), prove dead at the motor terminals, wait for the VFD's DC bus to "
           "discharge, and only then open the fan section. In panel DDC-AHU-01, remember that the incoming 230 V terminals stay "
           "live even with the controller's MCB off.</p>"),
    on_site=[
        "Carry your own padlock, tags and a proving unit; a tester you cannot prove is not a tester.",
        "Treat every unidentified terminal as live until measured.",
        "Tell the operators before isolating plant — and put the BMS point in a maintenance state so alarms do not flood.",
        "After work: remove your own lock only, restore, and test the plant in Hand and Auto.",
    ],
    faults=[
        ("A DI terminal in the BMS panel measures 230 V", "Foreign voltage from an MCC control circuit", "Stop; identify source; isolate; fit interposing relay or proper interface"),
        ("Fan is “off” on the BMS and you need to change the belt", "Remote start possible at any time", "Isolate and lock locally before touching"),
        ("Meter fuse blows when probing a terminal", "Meter left in current mode", "Always set the function first"),
        ("VFD display is dark after isolation", "DC bus may still be charged", "Wait the labelled time and measure"),
        ("Damper snaps shut when you remove the actuator supply", "Spring return", "Keep hands clear of blades and linkage"),
    ],
    terms=[
        ("ELV", "Extra-low voltage — not exceeding 50 V AC or 120 V DC."),
        ("Isolation", "Disconnecting a circuit from all sources of supply."),
        ("Lock-out / tag-out (LOTO)", "Securing an isolator with a personal lock and tag so nobody can re-energise it."),
        ("Prove – test – prove", "Check the tester, test the circuit dead, check the tester again."),
        ("Foreign voltage", "A voltage from another system present on terminals expected to be volt-free."),
        ("CAT rating", "Measurement category of a meter, e.g. CAT III 600 V, showing where it may safely be used."),
        ("Permit to work", "Formal written authorisation for a specific job under controlled conditions."),
    ],
    scenarios=[dict(
        prompt="You need to replace AHU-01's fan belt. The BMS shows the fan OFF and the schedule says it will not start until tomorrow. What must you do before opening the fan section?",
        options=["Nothing — the BMS shows it is off.", "Put the fan in manual OFF on the BMS.",
                 "Isolate and lock off the local isolator (and VFD supply), prove dead, and wait for the VFD to discharge."],
        answer=2,
        explain=(" Software states are not isolation: an operator override, fire mode or a schedule change can start the fan. Only "
                 "a locked-off isolator, proven dead, makes it safe."),
    )],
    questions=[
        ("Why is a “24 V panel” not automatically safe?", "It often contains 230 V supplies (transformer primary, incoming terminals) and can carry foreign voltages from other panels."),
        ("List the six safe-isolation steps.", "Identify sources → isolate → lock and tag → prove tester → test dead on all conductors → re-prove tester."),
        ("Why must you isolate locally even though the BMS shows a fan as off?", "The fan can be started at any moment by a schedule, override, another operator or another system."),
        ("How do you measure a 4–20 mA loop current safely?", "Put the meter in series at a designed test point or openable terminal, or use a mA clamp — never connect a meter in current mode across a supply."),
        ("What is a foreign voltage?", "A voltage from another system present on terminals that should be volt-free, e.g. a 230 V control circuit looped through BMS terminals."),
    ],
)

P2 = dict(
    id="4-2", slug="io-types", title="The four I/O types: DI, DO, AI, AO",
    objectives=[
        "Classify any field signal as DI, DO, AI or AO.",
        "Explain how each I/O type appears on the BMS and in BACnet.",
        "Choose the right I/O for fans, dampers, valves and sensors.",
        "Count the I/O for a plant item and size a controller with spare capacity.",
    ],
    one_line=("Every hard-wired point is one of four types: <strong>DI</strong> and <strong>DO</strong> carry on/off states in and "
              "out of the controller; <strong>AI</strong> and <strong>AO</strong> carry a range of values in and out."),
    why=("<p>The I/O type decides everything downstream: which controller terminal is used, what signal and cable are needed, "
         "how the point is configured and how it is shown on the screen. Classifying signals correctly is the first step of "
         "every point list, wiring diagram and controller selection — the basis of Labs 1 and 2.</p>"),
    body=(
        fig(d_io_quadrants(), "AHU-01's 14 hard-wired points sorted into the four I/O types.")
        + table(["Type", "Direction", "Signal", "Typical examples"], [
            ("DI — digital input", "Into the controller", "Contact open/closed (dry contact), sometimes a voltage", "Run status, fault, auto/manual, filter switch, fire signal, flow switch, pulses from meters"),
            ("DO — digital output", "Out of the controller", "Relay or triac contact", "Start/stop, enable chiller, open/close damper, floating actuator open and close"),
            ("AI — analogue input", "Into the controller", "Resistance (NTC, PT1000), 0–10 V, 4–20 mA", "Temperature, humidity, pressure, CO₂, flow, actuator feedback"),
            ("AO — analogue output", "Out of the controller", "0–10 V, 2–10 V, 4–20 mA", "Valve position, damper position, VFD speed"),
        ])
        + "<h3>Universal I/O</h3>"
        + "<p>Many controllers have <strong>universal inputs (UI)</strong> — and some <strong>universal I/O (UIO)</strong> — that "
          "are set in software to the type and signal you need. They make design flexible, but every point must then be "
          "<em>configured</em> correctly: an NTC sensor on a UI set for 0–10 V will read nonsense.</p>"
        + "<h3>How points look on the BMS</h3>"
        + table(["I/O", "BACnet object", "Shows as", "Configured with"], [
            ("DI", "Binary Input (BI)", "Two state texts — Running/Stopped, Normal/Alarm", "Normal state (NO/NC), state texts, alarm state, delay"),
            ("DO", "Binary Output (BO)", "Command On/Off with priority", "Minimum on/off time, state texts, relinquish default"),
            ("AI", "Analog Input (AI)", "Value with units — 23.8 °C", "Sensor type or range, scaling, units, offset, filter, limits"),
            ("AO", "Analog Output (AO)", "Value in % or units", "Signal range (0–10 / 2–10 V), min/max, relinquish default"),
            ("Software (virtual)", "Analog Value (AV), Binary Value (BV), Multi-state Value (MSV)", "Setpoints, modes, calculated values", "Limits, units, who may write"),
        ])
        + "<p>Not every point is physical. <strong>Software points</strong> — setpoints, occupancy mode, calculated values such "
          "as mixed air fraction, alarm flags — live only in the controller program but appear on the BMS like any other point.</p>"
        + "<h3>Choosing I/O for common equipment</h3>"
        + table(["Equipment", "Points", "Why"], [
            ("Fan or pump, direct-on-line", "DO start · DI status · DI fault · DI auto", "Command, proof, trip, and whether the BMS is in control"),
            ("Fan or pump on a VFD", "As above + AO speed (+ network)", "Speed control"),
            ("On/off damper", "DO (+ DI end switch)", "Two positions; end switch proves it"),
            ("Modulating damper or valve", "AO (+ AI feedback)", "Position control; feedback shows actual position"),
            ("Floating actuator", "2 × DO", "Drive open / drive close"),
            ("Temperature sensor", "AI (resistive)", "NTC or PT1000 direct to the input"),
            ("Transmitter (RH, CO₂, pressure)", "AI (0–10 V or 4–20 mA)", "Scaled signal"),
        ])
        + "<h3>Counting I/O and sizing a controller</h3>"
        + steps([
            "List every device and its points (the point list — Lab 2).",
            "Count by type: DI, DO, AI, AO (and which inputs can share universal terminals).",
            "Add <strong>spare capacity</strong> — typically 10–20 % of each type — for changes during the project and later.",
            "Choose a controller (plus I/O modules if needed) that covers the totals, and check other limits: number of PID loops, trend memory, communication ports.",
        ])
    ),
    ahu01=("<p>AHU-01 has <strong>1 DO, 5 DI, 5 AI and 3 AO = 14 hard-wired points</strong>, plus the Modbus link to the VFD and "
           "software points such as the 24 °C setpoint and the occupancy mode. Its 10 inputs can share universal inputs. With "
           "about 20 % spare, a controller with around 12 UI, 2 DO and 4 AO would do — sized properly in Lab 2.</p>"),
    on_site=[
        "When a reading is wrong, check the point configuration (type, range, units) before blaming the sensor.",
        "Check the DI “normal” state: a filter switch configured the wrong way round shows an alarm when the filter is clean.",
        "Look at the point's priority array or override flag before assuming an output is broken (Module 5).",
        "Keep the I/O summary up to date — it is how the next engineer finds spare terminals.",
    ],
    faults=[
        ("Filter DI shows ALARM with a new filter and the contact open", "DI normal state configured backwards", "Point configuration: normal open/closed"),
        ("AI reads full scale all the time", "Input type wrong, e.g. 4–20 mA sensor on an input set for 0–10 V", "Input type vs sensor"),
        ("AO commanded 60 % but terminal measures 0 V", "Output overridden, out of service, or set as a different type", "Point status and priority; configuration"),
        ("Setpoint changes are lost after a restart", "Software point not saved to non-volatile memory", "Controller save/commit procedure"),
    ],
    terms=[
        ("DI", "Digital input: an on/off state into the controller."),
        ("DO", "Digital output: an on/off command from the controller."),
        ("AI", "Analogue input: a range of values into the controller."),
        ("AO", "Analogue output: a range of values from the controller."),
        ("Universal input (UI)", "Input configurable as AI or DI and for different signal types."),
        ("Software (virtual) point", "A point that exists only in the program — setpoints, modes, calculated values."),
        ("Normal state", "The state of a DI that the BMS treats as normal (contact open or closed)."),
        ("I/O summary", "Count of all points by type, used to choose controllers."),
        ("Spare capacity", "Unused I/O kept for future changes, typically 10–20 %."),
    ],
    scenarios=[dict(
        prompt="A new filter is fitted on AHU-02. The filter ΔP switch contact is open (clean filter), but the BMS shows “Filter dirty — ALARM”. What is wrong?",
        options=["The switch is faulty.", "The DI's normal state is configured as “closed” instead of “open”.",
                 "The filter is the wrong grade."],
        answer=1,
        explain=(" An open contact on a clean filter is correct. The BMS interprets the open contact as abnormal because the point "
                 "is configured the wrong way round. Fix the configuration and test by closing the contact."),
    )],
    questions=[
        ("Classify: valve position command, CO₂ reading, fan trip, chiller enable.", "Valve command = AO; CO₂ = AI; fan trip = DI; chiller enable = DO."),
        ("What is a universal input?", "An input that can be configured in software as an AI or DI and for different signal types."),
        ("Which BACnet object type represents a DI?", "Binary Input (BI)."),
        ("Give two examples of software points.", "Any two of: setpoints, occupancy mode, calculated values (e.g. fresh air fraction), alarm flags, schedules' outputs."),
        ("Why add 10–20 % spare I/O?", "To allow for design changes during the project and future additions without new controllers."),
    ],
)

P3 = dict(
    id="4-3", slug="analog-signals", title="Analog signals: 0–10 V, 4–20 mA, 0–20 mA",
    objectives=[
        "Explain how voltage and current signals carry a value.",
        "Scale any analogue signal to engineering units — and back.",
        "Wire 2-, 3- and 4-wire transmitters and check a loop's voltage budget.",
        "Use the live zero of 4–20 mA to detect faults.",
    ],
    one_line=("An analogue signal carries a value as a <strong>voltage (0–10 V)</strong> or a <strong>current (4–20 mA)</strong> that "
              "is scaled across a range — 12 mA on a 0–500 Pa sensor means 250 Pa."),
    why=("<p>Most transmitters and almost every modulating actuator use these signals. Scaling mistakes, wrong signal types and "
         "voltage drops cause a large share of commissioning faults — and they are easy to find once you can calculate what "
         "the signal <em>should</em> be and measure what it is.</p>"),
    body=(
        "<h3>The three common signals</h3>"
        + table(["", "0–10 V (and 2–10 V)", "4–20 mA", "0–20 mA"], [
            ("Carries the value as", "Voltage", "Current", "Current"),
            ("Live zero", "No (2–10 V: yes)", "Yes — 4 mA = bottom of range", "No"),
            ("Wire-break detection", "No — 0 V looks like a real minimum", "Yes — 0 mA is clearly a fault", "No"),
            ("Effect of long cables", "Voltage drop and noise cause errors", "Immune to voltage drop (same current everywhere in the loop)", "Same as 4–20 mA"),
            ("Typical use", "Actuators, short sensor runs inside buildings", "Pressure and flow transmitters, long or noisy runs, industrial devices", "Rare in HVAC"),
        ], "plain")
        + "<h3>Scaling</h3>"
        + callout("note", "Signal → value",
                  "<p><strong>Value = Min + (Signal − Signal<sub>min</sub>) ÷ (Signal span) × (Max − Min)</strong></p>"
                  "<p>4–20 mA, 0–500 Pa, 12 mA → 0 + (12 − 4) ÷ 16 × 500 = <strong>250 Pa</strong><br>"
                  "0–10 V, 0–100 % RH, 6.2 V → 6.2 ÷ 10 × 100 = <strong>62 % RH</strong></p>")
        + callout("note", "Value → signal (outputs)",
                  "<p><strong>Signal = Signal<sub>min</sub> + (Value ÷ 100 %) × Signal span</strong></p>"
                  "<p>Valve 35 % on 0–10 V → <strong>3.5 V</strong>. On 2–10 V → 2 + 0.35 × 8 = <strong>4.8 V</strong>.</p>")
        + tool("scale", type="4-20", lo="0", hi="500", u="Pa", sig="12")
        + "<h3>Wiring transmitters</h3>"
        + fig(d_loops(), "Left: a 2-wire transmitter powered by its own loop. Right: a 3-wire transmitter sharing 0 V between supply and signal.")
        + table(["Type", "Wires", "How it is powered"], [
            ("2-wire (loop-powered)", "2", "The 4–20 mA loop itself powers the transmitter — supply +, through the transmitter, through the controller input, back to supply −."),
            ("3-wire", "3", "Separate supply; supply and signal share one common (0 V) wire. Common for 0–10 V sensors."),
            ("4-wire", "4", "Separate supply pair and separate signal pair — the signal is isolated from the supply."),
        ])
        + "<h3>The 4–20 mA loop's voltage budget</h3>"
        + "<p>A controller usually measures loop current as the voltage across an internal resistor (250 Ω turns 4–20 mA into "
          "1–5 V). The transmitter also needs a minimum voltage across it to work. Everything must fit inside the supply voltage:</p>"
        + callout("note", "Maximum loop resistance",
                  "<p><strong>R<sub>max</sub> = (Supply − Transmitter minimum) ÷ 0.020 A</strong></p>"
                  "<p>24 V supply, transmitter needs 12 V → (24 − 12) ÷ 0.020 = <strong>600 Ω</strong>. Minus a 250 Ω input "
                  "leaves 350 Ω for the cable — plenty for most buildings.</p>")
        + "<h3>Why 0–10 V can be wrong on long cables</h3>"
        + "<p>If a 0–10 V sensor's signal is measured against a 0 V wire that also carries actuator supply current, the voltage "
          "drop on that shared wire adds straight onto the reading. For example 0.3 A of actuator current on 50 m of 0.75 mm² "
          "cable (about 1.2 Ω) shifts the reference by about 0.37 V — 3.7 % of full scale. Use a separate signal common, keep 0–10 V "
          "runs short, or use 4–20 mA for long runs.</p>"
        + "<h3>Using the live zero</h3>"
        + table(["Loop current", "Meaning"], [
            ("Below about 3.6 mA", "Fault: open circuit, no loop power, failed transmitter"),
            ("4 mA", "Bottom of the range"),
            ("20 mA", "Top of the range"),
            ("Above about 21 mA", "Fault or over-range: short circuit, failed transmitter"),
        ], "plain")
        + "<p>These limits follow the widely used NAMUR NE 43 recommendation. Configure the AI to flag readings outside them as "
          "a sensor fault, so the program can alarm and use a fallback.</p>"
    ),
    ahu01=("<p>AHU-01 uses both kinds. Its <strong>duct pressure sensor</strong> is a 2-wire 4–20 mA transmitter for 0–500 Pa, "
           "powered from the panel's 24 V DC supply (Lab 4). Its <strong>RH and CO₂ sensors</strong> are 3-wire 0–10 V units, and "
           "all three <strong>AOs</strong> (valve, damper, VFD speed) are 0–10 V.</p>"),
    on_site=[
        "Calculate the expected signal before you measure; then the measurement tells you something.",
        "Check transmitter range settings (jumpers, DIP switches or menus) against the controller's scaling.",
        "Measure 0–10 V between signal and the controller's own common terminal, not a nearby earth.",
        "Some controller inputs need a jumper or configuration change to switch between V and mA.",
    ],
    faults=[
        ("4–20 mA input reads below range / fault", "Open loop, no 24 V DC, transmitter wired backwards", "Loop supply; continuity; polarity"),
        ("Reading exactly double or half the true value", "Range mismatch between transmitter and controller", "Transmitter setting vs scaling"),
        ("0–10 V reading drifts when actuators move", "Shared common carrying actuator current", "Separate signal common; shorter run"),
        ("Value flickers", "Electrical noise from VFD or power cables", "Screened twisted pair, cable route, screen earth"),
        ("AO valve only opens half way", "2–10 V device driven with 0–10 V (or the reverse)", "Signal range on both sides"),
    ],
    terms=[
        ("0–10 V signal", "Analogue signal carried as voltage."),
        ("4–20 mA signal", "Analogue signal carried as current, with 4 mA as the live zero."),
        ("Live zero", "A non-zero bottom of range, so a dead signal can be told apart from a real minimum."),
        ("Loop-powered (2-wire)", "Transmitter powered by its own 4–20 mA loop."),
        ("Scaling", "Converting a signal to engineering units using the range minimum and maximum."),
        ("Burden / load resistance", "Resistance of the input (e.g. 250 Ω) through which loop current flows."),
        ("NAMUR NE 43", "Recommendation defining fault levels outside 3.8–20.5 mA, commonly applied as < 3.6 / > 21 mA."),
    ],
    scenarios=[dict(
        prompt="AHU-01's duct pressure (4–20 mA, 0–500 Pa) reads −31 Pa on the BMS. You measure 3.0 mA in the loop. What is the most likely cause?",
        options=["The duct is under negative pressure.", "A fault in the loop or transmitter — below 3.6 mA should be treated as a failure.",
                 "The scaling is wrong."],
        answer=1,
        explain=(" 3.0 mA is below the live zero, so the reading is not a real pressure. The transmitter is failing, under-powered or "
                 "the loop has a high resistance. Configure the AI to flag this as a fault instead of showing −31 Pa."),
    )],
    questions=[
        ("A 4–20 mA, 0–1,000 Pa sensor gives 8 mA. What is the pressure?", "(8 − 4) ÷ 16 × 1,000 = 250 Pa."),
        ("What voltage drives a valve to 70 % on a 2–10 V actuator?", "2 + 0.7 × 8 = 7.6 V."),
        ("Why is 4–20 mA better than 0–10 V for long cable runs?", "Current is the same everywhere in a series loop, so cable resistance does not change the reading, and the live zero shows wire breaks."),
        ("A transmitter needs 10 V; the supply is 24 V. What is the maximum loop resistance?", "(24 − 10) ÷ 0.02 = 700 Ω."),
        ("Describe how a 2-wire transmitter is connected.", "Supply + → transmitter + ; transmitter − → controller mA input; controller input common → supply −. The loop current powers the transmitter."),
    ],
)

P4 = dict(
    id="4-4", slug="digital-signals-contacts-relays", title="Dry contacts, relay outputs, NO and NC",
    objectives=[
        "Read contact symbols and explain what “normally” means.",
        "Distinguish dry (volt-free) and wet contacts and wire each to a DI safely.",
        "Compare relay, triac and transistor outputs.",
        "Use normally-closed wiring to make safety signals fail-safe.",
    ],
    one_line=("A contact is just a switch: <strong>NO</strong> is open and <strong>NC</strong> is closed in its normal, unoperated "
              "state; a <strong>dry</strong> contact carries no voltage of its own — the receiving side supplies it."),
    why=("<p>Most status, alarm and command signals in a BMS are contacts. Choosing NO or NC, dry or wet, and the right output "
         "type decides whether a broken wire is noticed or silently ignored — and whether a field fault destroys a controller "
         "output. These details separate a system that fails safely from one that does not.</p>"),
    body=(
        fig(d_contacts(), "Contacts are drawn de-energised. “Normally” means at rest, not “when the plant is running normally”.")
        + table(["Contact form", "Also called", "Terminals", "Use"], [
            ("SPST-NO", "Form A, make", "2", "Status, start command"),
            ("SPST-NC", "Form B, break", "2", "Fail-safe alarms and trips"),
            ("SPDT (changeover)", "Form C", "3 — COM, NO, NC", "Either function from one relay"),
            ("DPDT", "Two changeover sets", "6", "Two independent circuits switched together"),
        ])
        + callout("warn", "“Normal” means de-energised",
                  "<p>A relay's NO contact is open when its coil is <em>off</em>. A fire alarm relay that is held energised while "
                  "the system is healthy has its “NO” contact <em>closed</em> in normal service. Always ask: what is the coil "
                  "state when the plant is healthy?</p>")
        + "<h3>Dry and wet contacts</h3>"
        + table(["", "Dry (volt-free, potential-free)", "Wet"], [
            ("What it is", "Just a switch; no voltage of its own", "The contact switches a voltage supplied by its own panel"),
            ("Into a BMS DI", "Directly — the controller supplies a small wetting voltage", "Only via an interposing relay or an input rated for that voltage"),
            ("Example", "VFD fault relay, ΔP switch, auxiliary contact", "230 V lamp circuit, 24 V signal from another system"),
        ])
        + fig(d_di_wiring(), "Left: a dry contact straight into a DI. Right: a normally-closed loop that stops the AHU on fire or on a broken wire.")
        + "<h3>Fail-safe: why safety signals use closed-when-healthy contacts</h3>"
        + "<p>If a fire shutdown signal were a contact that <em>closes</em> on fire, a cut cable would look exactly like “no fire” — "
          "and the AHU would keep running in a real fire. Wiring it so the contact is <strong>closed when healthy</strong> and "
          "<strong>opens</strong> on fire means a broken wire also stops the AHU and raises an alarm. The same principle is used "
          "for high-pressure cut-outs, freeze protection and emergency stops.</p>"
        + "<p>The BMS point is configured to match: “normal = closed”. The display shows <em>Normal</em> when the contact is "
          "closed and <em>Fire</em> (or <em>Alarm</em>) when it opens.</p>"
        + "<h3>Output types</h3>"
        + table(["Output", "Switches", "Notes"], [
            ("Relay", "AC or DC, within its rating", "Isolated contact; most versatile. Check the current rating and use an interposing relay for motor circuits"),
            ("Triac", "AC only (usually 24 V AC)", "Small leakage current when off can keep sensitive loads (e.g. small relays) energised; cannot switch DC"),
            ("Transistor / open collector", "Low-voltage DC, small currents", "Fast — for pulse outputs and small DC relays; observe polarity"),
        ])
        + bullets([
            "<strong>Suppress coils:</strong> fit an RC snubber across AC relay or contactor coils and a diode across DC coils, so switching spikes do not damage outputs or create noise.",
            "<strong>Dry-circuit contacts:</strong> heavy power contacts can fail to make reliable contact at the tiny currents of a DI. Signal relays often have gold-plated contacts for this reason.",
        ])
    ),
    ahu01=("<p>AHU-01's fire signal comes from a relay in the fire alarm panel that is <strong>energised when healthy</strong>. Its "
           "closed contact is wired in series into the fan's starter circuit (hard-wired trip) and, through a second contact, to "
           "a BMS DI configured “normal = closed”. Fire, power loss at the fire panel interface, or a broken wire all stop the "
           "fan and show <em>Fire shutdown</em>. The VFD's fault relay is also wired fail-safe (closed when healthy).</p>"),
    on_site=[
        "Before connecting any contact to a DI, measure across it in both states — it must show 0 V (dry).",
        "Use the changeover's COM/NO/NC labels on the device, not your assumption.",
        "After replacing a panel or device, check every NC safety loop is reconnected — a missing link stops the plant (safely).",
        "Test fail-safe loops by opening them, not just by simulating in software.",
    ],
    faults=[
        ("DI always ON, even with the device off", "Contact welded, wrong NO/NC terminal, or foreign voltage", "Measure across the contact; check terminals"),
        ("DI flickers on and off", "Contact bounce, loose terminal, vibration", "Terminal tightness; add debounce delay"),
        ("A small relay stays energised although the triac output is off", "Triac leakage current", "Use a relay output or a load resistor"),
        ("AHU will not start after panel work; BMS shows Fire with no fire", "NC fire loop not reconnected (open = fire, by design)", "Fire interface terminals and links"),
        ("DI card destroyed", "Wet (powered) contact connected to a dry DI", "Use an interposing relay"),
    ],
    terms=[
        ("NO (normally open)", "Contact that is open when its device is at rest / de-energised."),
        ("NC (normally closed)", "Contact that is closed when its device is at rest / de-energised."),
        ("Changeover (SPDT)", "Contact set with common, NO and NC terminals."),
        ("Dry contact", "Volt-free contact; the receiving side supplies the voltage."),
        ("Wet contact", "Contact that switches a voltage from its own panel."),
        ("Fail-safe", "Designed so that a failure (e.g. broken wire) produces the safe outcome."),
        ("Triac output", "Solid-state AC switch used for small 24 V AC loads."),
        ("Snubber", "RC network that suppresses switching spikes from coils."),
        ("Wetting voltage", "Small voltage supplied by a DI to sense whether a dry contact is closed."),
    ],
    scenarios=[dict(
        prompt="After replacing the fire alarm interface module, AHU-01 refuses to start and the BMS shows “Fire shutdown” — but there is no fire and the fire panel shows normal. What is the most likely cause?",
        options=["The BMS program is corrupt.", "The normally-closed fire loop has not been reconnected (or a link is missing), so the open circuit reads as Fire.",
                 "The fan motor has failed."],
        answer=1,
        explain=(" This is the fail-safe design doing its job: an open loop means Fire. Check the interface wiring and links — and be glad "
                 "a broken wire stops the plant instead of hiding a real fire."),
    )],
    questions=[
        ("What does “normally” mean in NO and NC?", "The contact's state when the device is at rest or its relay coil is de-energised — not the state during normal plant operation."),
        ("Why should a fire shutdown signal be closed when healthy?", "So that a broken wire or loss of the signal opens the contact and stops the plant (fail-safe), instead of hiding a real fire."),
        ("Can you connect a wet contact directly to a dry DI?", "No — use an interposing relay or an input rated for that voltage, or the input may be destroyed."),
        ("Name the three terminals of a changeover contact.", "COM (common), NO and NC."),
        ("Why might a triac output fail to switch a small relay off?", "Triacs leak a small current when off, which can be enough to keep a sensitive relay coil energised."),
    ],
)

P5 = dict(
    id="4-5", slug="sensor-wiring-troubleshooting", title="Sensor wiring and troubleshooting",
    objectives=[
        "Choose cable types and apply segregation, screening and termination good practice.",
        "Calculate voltage drop on 24 V supplies and signal commons.",
        "Follow a systematic method to find the cause of a wrong reading.",
        "Know what to measure for every signal type.",
    ],
    one_line=("Good wiring — the right cable, kept away from power, screened and terminated neatly — prevents most faults; a "
              "<strong>systematic method</strong> finds the rest quickly: check the point, measure at the controller, then split "
              "the problem in half until it is found."),
    why=("<p>Field wiring faults are the most common BMS faults on site, and the most time-wasting if you hunt randomly. A "
         "standard method means you can walk up to any system, from any manufacturer, and find the fault with a multimeter and "
         "the drawings.</p>"),
    body=(
        "<h3>Cables</h3>"
        + table(["Signal", "Typical cable", "Notes"], [
            ("AI (resistive, 0–10 V, 4–20 mA), AO", "Twisted pair, overall screen, about 0.5–1.0 mm²", "Twisting and screening reject noise"),
            ("DI, DO (24 V)", "Multicore, about 0.75–1.5 mm²", "Screen needed near VFDs or long runs"),
            ("RS485 field bus", "Dedicated twisted pair, ~120 Ω characteristic impedance, screened", "Module 5"),
            ("24 V AC actuator supply", "Sized for voltage drop (see below)", "Often the limiting factor"),
            ("230 V / motor", "Power cable; screened for VFD outputs", "Never in the same containment as signals"),
        ])
        + "<h3>Segregation, screens and terminations</h3>"
        + bullets([
            "Run signal cables in <strong>separate containment</strong> from power cables, or keep a clear gap — specifications often ask for around 300 mm. Cross power cables at right angles.",
            "Earth cable screens at <strong>one end only</strong>, normally the panel. Earthing both ends lets current flow in the screen (an earth loop) and adds noise.",
            "Keep the screen continuous through junction boxes and cut back neatly at the device.",
            "Use <strong>ferrules</strong> on stranded wires, tighten to the terminal's torque, and leave no stray strands.",
            "Label both ends of every cable with the number on the drawings.",
        ])
        + "<h3>Voltage drop</h3>"
        + callout("note", "Two-wire supply voltage drop",
                  "<p><strong>V<sub>drop</sub> = 2 × length (m) × current (A) × resistance (Ω/m)</strong></p>"
                  "<p>Copper is roughly 0.0245 Ω/m for 0.75 mm², 0.018 Ω/m for 1.0 mm² and 0.012 Ω/m for 1.5 mm².</p>"
                  "<p>Example: three actuators drawing 0.8 A in total, 40 m away on 0.75 mm²: 2 × 40 × 0.8 × 0.0245 ≈ <strong>1.6 V</strong>. "
                  "A 24 V AC supply arrives at about 22.4 V — usually fine, but check the actuators' minimum (often around −20 %). "
                  "Long runs or many actuators need a bigger cable or a local transformer.</p>")
        + "<h3>A method that always works</h3>"
        + fig(d_troubleshoot(), "Start at the BMS, find which side of the controller terminals the fault is on, then split again.")
        + steps([
            "<strong>Confirm the symptom</strong> against something independent — a hand-held thermometer, the device's own display, your own eyes.",
            "<strong>Check the point</strong> on the BMS: is it overridden, out of service, or configured with the wrong type, range or units?",
            "<strong>Measure at the controller terminals.</strong> If the signal there is correct but the BMS is wrong, the fault is in configuration or the controller.",
            "If the signal at the terminals is wrong, <strong>disconnect the field cable</strong> and measure the field side — cable plus device.",
            "<strong>Measure at the device.</strong> Correct at the device but wrong at the panel → cable or junction box. Wrong at the device → the device or its supply.",
            "<strong>Fix, then verify</strong> on the BMS — and write down what you found and did.",
        ])
        + "<h3>What to measure</h3>"
        + table(["Signal", "Measure", "Expect"], [
            ("NTC / PT1000", "Resistance, sensor disconnected, power off", "Value matching the temperature (page 3.1 table)"),
            ("0–10 V input", "DC volts, signal to the input's own common", "Value ÷ range × 10 V"),
            ("4–20 mA input", "mA in series, or volts across the input resistor (250 Ω: 1–5 V)", "4 + value ÷ range × 16 mA"),
            ("Loop supply", "DC volts at the transmitter terminals", "Above the transmitter's minimum"),
            ("DI", "Volts across the open contact (wetting voltage); continuity with power off", "Wetting voltage when open; ~0 V when closed"),
            ("DO", "Contact continuity, or voltage switched downstream", "Changes with the command"),
            ("AO", "DC volts, output to its common", "Command % × span (+ live zero)"),
            ("24 V AC actuator supply", "AC volts at the actuator while it moves", "Within the actuator's tolerance"),
        ])
    ),
    ahu01=("<p>Worked example: AHU-01's CO₂ reads 0 ppm. (1) The point is not overridden and is set for 0–10 V, 0–2,000 ppm. (2) At "
           "the controller terminals: 0.0 V. (3) Disconnected, the field cable shows 0 V from the sensor. (4) At the sensor: no "
           "24 V supply. (5) The 24 V supply's fuse in the panel has blown — a shorted cable to a second sensor. Fix the short, "
           "replace the fuse, check the BMS shows a sensible value, and note it in the log.</p>"),
    on_site=[
        "Carry the drawings — the terminal numbers and cable numbers save you from guessing.",
        "Change one thing at a time, and put back anything you change that does not fix the problem.",
        "Photograph terminations before you disconnect anything.",
        "Intermittent faults: trend the point at a short interval and wiggle-test terminations while watching.",
    ],
    faults=[
        ("Analogue value noisy near VFDs", "Unscreened cable, screen not earthed, or cable alongside motor cables", "Cable type, route, screen earth"),
        ("Value correct at the device, wrong at the panel", "Cable fault, junction box, or wrong terminal", "Continuity and insulation of the cable; terminal numbers"),
        ("Several sensors fail together", "Shared 24 V supply or fuse", "Supply voltage and fuses"),
        ("Actuators slow or stop when many move", "Voltage drop on the 24 V AC supply", "Voltage at the actuator while moving"),
        ("Fault comes and goes", "Loose terminal or damaged cable", "Trend + wiggle test; re-terminate"),
    ],
    terms=[
        ("Segregation", "Physical separation of signal and power cables."),
        ("Screen (shield)", "Conductive layer around signal pairs that intercepts electrical noise."),
        ("Earth loop", "Unwanted current flowing in a screen earthed at both ends."),
        ("Ferrule", "Crimped sleeve on a stranded wire end for a reliable termination."),
        ("Voltage drop", "Loss of voltage along a cable due to its resistance and the current."),
        ("Half-split", "Troubleshooting by testing in the middle of the chain to halve the search each time."),
        ("Wiggle test", "Gently moving cables and terminals while watching a value to find intermittent faults."),
    ],
    scenarios=[dict(
        prompt="AHU-01's supply air temperature reads 3 °C higher on the BMS than a hand-held thermometer at the sensor. You disconnect the sensor and measure its resistance: it matches the hand-held temperature. What next?",
        options=["Replace the sensor.", "Check the point configuration (curve type, offset) and the cable — the sensor itself is correct.",
                 "Retune the valve PID loop."],
        answer=1,
        explain=(" The device is proven correct, so the error is between the sensor and the BMS value: a wrong NTC curve or offset in "
                 "the configuration, or extra resistance in the cable or a terminal. Measure resistance at the controller end next."),
    )],
    questions=[
        ("Why earth a cable screen at one end only?", "Earthing both ends lets current circulate in the screen (an earth loop), which adds noise instead of removing it."),
        ("Calculate the voltage drop for 1 A over 30 m of 1.0 mm² (0.018 Ω/m).", "2 × 30 × 1 × 0.018 = 1.08 V."),
        ("You measure the correct signal at the controller terminals but the BMS value is wrong. Where is the fault?", "On the controller side: point configuration (type, range, scaling, offset), an override, or the controller/input itself."),
        ("How do you measure a PT1000 sensor?", "Power off or disconnect it, and measure its resistance; compare with the PT1000 table at the actual temperature."),
        ("What is the first thing to check on the BMS when a reading is wrong?", "Whether the point is overridden or out of service, and that its type, range and units are configured correctly."),
    ],
)

P6 = dict(
    id="4-6", slug="reading-bms-drawings", title="Reading BMS drawings and point names",
    objectives=[
        "Name the drawings and documents in a BMS package and what each is for.",
        "Read a control schematic using its legend.",
        "Build and decode point names with a consistent convention.",
        "List the columns of a complete point list.",
    ],
    one_line=("BMS drawings and point names are the <strong>shared language</strong> between designer, installer, programmer and "
              "operator — read them first, keep them consistent, and update them when anything changes."),
    why=("<p>Every task — wiring, programming, commissioning, fault-finding — starts with a drawing or a point list. A consistent "
         "point name lets anyone find “Level 3 AHU-01 return air temperature” on the graphic, the controller, the panel label "
         "and the trend log without guessing. Lab 2 asks you to produce exactly this for AHU-01.</p>"),
    body=(
        "<h3>The document set</h3>"
        + table(["Document", "Shows", "You use it to…"], [
            ("System architecture / network riser", "All controllers, networks and servers, floor by floor", "Find which controller and network a point is on"),
            ("Control schematic", "Plant diagram with every sensor, actuator and point", "Understand what is controlled and measured"),
            ("Point list / I/O schedule", "Every point with type, signal, range, alarm and terminal", "Configure, wire and test"),
            ("Panel drawings", "Layout, power, I/O wiring, terminal schedule", "Build, wire and fault-find the panel"),
            ("Cable schedule", "Every cable: number, type, from, to", "Pull and terminate cables"),
            ("Sequence of operation", "How the plant should behave", "Program and test"),
            ("Device schedule and datasheets", "Make, model and settings of every device", "Configure sensors and actuators"),
            ("As-built drawings", "Final, corrected versions after commissioning", "Maintain the system for years"),
        ])
        + "<h3>Symbols</h3>"
        + fig(d_symbols(), "Common symbols. Always check the legend sheet of the drawing set you are using.")
        + "<h3>Reading a control schematic</h3>"
        + steps([
            "Read the title block: system, drawing number, <strong>revision</strong>, and whether it is “for construction” or “as-built”.",
            "Follow the <strong>air path</strong> (or water path) from inlet to outlet, naming each component.",
            "Find every <strong>point bubble</strong> and note its tag and I/O type.",
            "Look for <strong>interlock lines</strong> and notes — fire shutdown, hard-wired safeties.",
            "Cross-check against the point list: every bubble should appear there, and every list entry on the schematic.",
        ])
        + "<h3>Point naming</h3>"
        + fig(d_naming(), "A name built from fixed parts, always in the same order.")
        + "<p>Conventions differ between companies and projects, but good ones share these rules:</p>"
        + bullets([
            "Fixed order — from big to small: site, building, floor, system/equipment, point.",
            "Short, defined abbreviations from an agreed list (RAT, SAT, CHWV, SF-CMD…).",
            "No spaces or special characters that some systems cannot handle.",
            "The same name on the drawing, the controller, the graphic, the panel label and the trend log.",
        ])
        + table(["Example", "Meaning"], [
            ("B1-L03-AHU01-SF-CMD", "Supply fan start/stop command"),
            ("B1-L03-AHU01-SF-STS", "Supply fan run status"),
            ("B1-L03-AHU01-RAT", "Return air temperature"),
            ("B1-L03-AHU01-CHWV", "Chilled water valve command"),
            ("B1-L03-AHU01-RAT-SP", "Return air temperature setpoint (software point)"),
        ], "plain")
        + callout("note", "Tagging",
                  "<p>Large and analytics-heavy projects add <strong>semantic tags</strong> (open schemes such as Project "
                  "Haystack or Brick) describing what each point is — “air, temp, sensor, return” — so software can find points "
                  "without parsing names. The naming discipline above is still the foundation.</p>")
        + "<h3>Columns of a good point list</h3>"
        + table(["Column", "Example"], [
            ("Point name / tag", "B1-L03-AHU01-RAT"),
            ("Description", "Return air temperature"),
            ("I/O type", "AI"),
            ("Signal / device", "10k NTC duct probe"),
            ("Range and units", "−10 to 50 °C"),
            ("Normal state (digital)", "e.g. Open = clean (filter switch)"),
            ("Alarm limits, delay and priority", "High > 27 °C for 15 min, medium"),
            ("Trend", "5 min"),
            ("Controller and terminal", "DDC-AHU-01, UI3"),
            ("Cable number", "C-AHU01-07"),
            ("Remarks", "Mounted 2 m after the mixing box"),
        ], "plain")
    ),
    ahu01=("<p>AHU-01's points all start <strong>B1-L03-AHU01-</strong>. In Lab 2 you build its full point list with every column "
           "above, and in Lab 1 its wiring diagram uses the same names and terminal numbers.</p>"),
    on_site=[
        "Check the drawing revision before you start — wiring to an old revision is a common and expensive mistake.",
        "Mark up changes in red on a site copy and hand them in for the as-builts.",
        "If the name on the panel label, drawing and graphic differ, report it — it will confuse someone during a fault.",
        "Keep a copy of the abbreviation list with the point list.",
    ],
    faults=[
        ("Point on the graphic does not exist in the controller", "Graphic built from an old point list", "Point list revision; controller database"),
        ("Two points with the same name on different floors", "Building/floor part missing from the convention", "Naming convention"),
        ("Field wiring doesn't match the drawing", "Drawing not as-built, or wiring changed on site", "As-built mark-ups"),
        ("Operators cannot find points in trends", "Inconsistent or cryptic names", "Rename to the convention; add descriptions"),
    ],
    terms=[
        ("Control schematic", "Drawing of the plant with all sensors, actuators and points."),
        ("Point list / I/O schedule", "Table of every point with its type, signal, range, alarms and terminal."),
        ("Network riser", "Drawing of controllers and networks by floor."),
        ("As-built", "Drawings corrected to match what was actually installed."),
        ("Revision", "Version letter or number of a drawing."),
        ("Point naming convention", "Agreed rules for building point names from fixed parts."),
        ("Semantic tagging", "Describing points with standard tags (e.g. Project Haystack, Brick) so software can interpret them."),
    ],
    scenarios=[dict(
        prompt="You are sent to wire AHU-04's panel from drawing revision B. The site office has revision D on the wall. What do you do?",
        options=["Wire from revision B — that is what you were given.", "Stop and get the current revision (D) confirmed before wiring.",
                 "Wire from whichever looks more complete."],
        answer=1,
        explain=(" Always work from the current approved revision. Points, terminals or devices may have changed between B and D; "
                 "re-wiring later costs far more than a phone call now."),
    )],
    questions=[
        ("Which drawing tells you which network a controller is on?", "The system architecture / network riser diagram."),
        ("Decode B1-L03-AHU01-SF-STS.", "Building 1, Level 3, AHU-01, supply fan run status."),
        ("Name six columns of a good point list.", "Any six of: name/tag, description, I/O type, signal/device, range and units, normal state, alarm limits/priority, trend interval, controller and terminal, cable number, remarks."),
        ("What are as-built drawings and why do they matter?", "Drawings corrected to show what was actually installed; they are what maintenance engineers rely on for the life of the building."),
        ("Why should a point have the same name everywhere?", "So anyone can find and match it across drawings, controller, graphics, labels and trends without confusion."),
    ],
)

MODULE_INTRO = (
    "<p>This is the hands-on module. It starts with electrical safety — before you touch a terminal — then covers the four "
    "I/O types, analogue and digital signals, wiring and troubleshooting, and the drawings that tie it all together. The "
    "scaling calculator on page 4.3 and Labs 2 and 4 put it into practice.</p>"
)

PAGES = [P1, P2, P3, P4, P5, P6]

QUIZ = [
    mcq("Which step comes immediately before testing a circuit dead?", ["Lock and tag", "Prove the tester on a known live source", "Re-prove the tester", "Remove the fuse"], 1,
        "Prove – test – prove: a tester must be shown to work before you trust a “dead” reading.", "4.1"),
    mcq("The BMS shows a fan OFF. Is it safe to change the belt?", ["Yes", "Only at night", "No — isolate and lock off locally first", "Yes, if in manual"], 2,
        "Fans can be started remotely at any time.", "4.1"),
    mcq("A fan trip signal into the controller is a…", ["DO", "AO", "DI", "AI"], 2, "On/off state into the controller = digital input.", "4.2"),
    mcq("4–20 mA, 0–500 Pa: what current means 375 Pa?", ["12 mA", "15 mA", "16 mA", "18 mA"], 2, "4 + 375/500 × 16 = 4 + 12 = 16 mA.", "4.3"),
    mcq("A 4–20 mA input reads 1.5 mA. This indicates…", ["the bottom of the range", "a fault — open loop or failed transmitter", "over-range", "normal operation"], 1,
        "Below about 3.6 mA is treated as a fault.", "4.3"),
    mcq("A valve at 40 % on a 2–10 V actuator needs…", ["4.0 V", "5.2 V", "6.0 V", "2.4 V"], 1, "2 + 0.4 × 8 = 5.2 V.", "4.3"),
    mcq("“NC” on a relay contact means it is closed when…", ["the plant is running", "the relay coil is de-energised", "the BMS is online", "the contact is wet"], 1,
        "Normal = at rest / de-energised.", "4.4"),
    mcq("Why is a fire shutdown loop wired closed-when-healthy?", ["It uses less power", "A broken wire then stops the plant (fail-safe)", "BACnet requires it", "To save cable"], 1,
        "Open circuit = fire, so faults are never hidden.", "4.4"),
    mcq("You measure the correct signal at the controller terminals but the BMS value is wrong. The fault is…", ["in the field device", "in the cable", "on the controller side — configuration, override or input", "in the drawings"], 2,
        "The field side is proven good.", "4.5"),
    mcq("Which document shows the final installed state?", ["Tender drawing", "For-construction drawing", "As-built drawing", "Datasheet"], 2,
        "As-builts are corrected to match what was installed.", "4.6"),
]

FINAL = [
    mcq("A DI terminal measures 230 V AC. What is this?", ["Normal wetting voltage", "A foreign voltage — stop and investigate", "A 4–20 mA signal", "Induced noise only"], 1,
        "DI wetting voltages are low; 230 V means a foreign voltage.", "4.1"),
    mcq("Which BACnet object type is a setpoint stored only in the program?", ["Analog Input", "Analog Output", "Analog Value", "Binary Input"], 2,
        "Software points are Value objects.", "4.2"),
    mcq("A transmitter needs 12 V on a 24 V loop. Maximum loop resistance?", ["300 Ω", "600 Ω", "1,200 Ω", "250 Ω"], 1, "(24 − 12) ÷ 0.02 = 600 Ω.", "4.3"),
    mcq("A triac output can switch…", ["DC loads", "AC loads only", "4–20 mA", "RS485"], 1, "Triacs are AC-only switches.", "4.4"),
    mcq("Earthing a cable screen at both ends can cause…", ["better shielding", "an earth loop and more noise", "higher voltage drop", "nothing"], 1,
        "Current flows in the screen between earth points.", "4.5"),
]
