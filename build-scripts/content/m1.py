# -*- coding: utf-8 -*-
"""Module 1 — BMS Architecture. Vendor-neutral; based on general industry practice
and open standards (ISO 16484, ASHRAE 135 / BACnet, Modbus)."""
from bms_common import (table, steps, bullets, callout, cards, fig, svg, defs, t, rect, box,
                        line, path, circle)

# ==========================================================================
# Diagrams
# ==========================================================================

def d_control_loop():
    i = defs("cl")
    i += box(20, 40, 150, 76, "1 · Sense", "Sensor measures|room temp 26 °C", "d-acc")
    i += box(215, 40, 175, 76, "2 · Decide", "Controller compares|with setpoint 24 °C", "d-acc")
    i += box(435, 40, 150, 76, "3 · Act", "Actuator opens the|chilled water valve", "d-acc")
    i += box(625, 40, 125, 76, "Process", "Air is cooled,|room temp falls", "d-box")
    i += line(170, 78, 213, 78, "d-aline", end="cl-a")
    i += line(390, 78, 433, 78, "d-aline", end="cl-a")
    i += line(585, 78, 623, 78, "d-aline", end="cl-a")
    i += path("M687,116 L687,160 L95,160 L95,118", "d-line d-dash", end="cl")
    i += t(390, 178, "Feedback: the sensor measures the result, so the controller keeps correcting", "d-ts")
    return svg(760, 195, i, "Closed control loop: sense, decide, act, process, feedback")


def d_bms_hub():
    i = ""
    sats = [
        (120, 48, "HVAC plant", "control + monitor", True), (380, 48, "Lighting", "schedule + control", True),
        (640, 48, "Energy meters", "monitor", False), (120, 150, "Plumbing, pumps", "monitor + control", True),
        (640, 150, "Electrical: DG, UPS", "monitor", False), (120, 252, "Lifts", "monitor", False),
        (380, 252, "Fire alarm", "monitor only", False), (640, 252, "Access, CCTV", "integrated BMS only", False),
    ]
    for x, y, _a, _b, ctl in sats:
        i += line(x, y, 380, 150, "d-aline" if ctl else "d-line d-dash")
    i += box(295, 112, 170, 76, "BMS", "monitor · control · alarm|schedule · record", "d-acc", "d-tl d-tb")
    for x, y, a, b, _c in sats:
        i += box(x - 80, y - 28, 160, 56, a, b, "d-box")
    i += line(190, 308, 230, 308, "d-aline") + t(238, 308, "controlled by the BMS", "d-ts", "start")
    i += line(420, 308, 460, 308, "d-line d-dash") + t(468, 308, "monitored only", "d-ts", "start")
    return svg(760, 322, i, "Building systems connected to a BMS")


def d_three_levels():
    i = defs("lv")
    i += rect(6, 8, 748, 104, "d-soft", 10) + rect(6, 150, 748, 104, "d-soft", 10) + rect(6, 290, 748, 104, "d-soft", 10)
    for y, a, b in ((50, "MANAGEMENT", "see · store · report"), (192, "AUTOMATION", "decide · control"),
                    (332, "FIELD", "measure · act")):
        i += t(20, y, a, "d-t d-tb d-ta", "start") + t(20, y + 20, b, "d-ts", "start")
    # management
    for x, a, b in ((190, "BMS server", "database · history"), (350, "Workstation", "graphics · alarms"),
                    (510, "Web / mobile", "browser clients")):
        i += line(x + 65, 88, x + 65, 131)
        i += box(x, 30, 130, 58, a, b, "d-box")
    i += line(175, 131, 745, 131, "d-aline")
    i += t(20, 131, "IP backbone · BACnet/IP", "d-ts d-ta", "start")
    # automation
    i += line(255, 131, 255, 168) + line(445, 131, 445, 168) + line(640, 131, 640, 168)
    i += box(180, 168, 150, 60, "Supervisory", "network controller", "d-acc")
    i += box(375, 168, 140, 60, "DDC-AHU-01", "plant controller", "d-acc")
    i += box(565, 168, 150, 60, "DDC-CHILLER", "plant controller", "d-acc")
    # field bus from supervisory
    i += line(255, 228, 255, 272) + line(185, 272, 395, 272, "d-aline")
    i += line(225, 272, 225, 304) + line(345, 272, 345, 304)
    i += box(180, 304, 90, 54, "FCU", "controller", "d-box") + box(300, 304, 90, 54, "VAV", "controller", "d-box")
    # hard-wired + modbus from AHU controller
    i += path("M430,228 L430,284 L470,284 L470,304") + path("M430,284 L570,284 L570,304")
    i += path("M470,228 L470,262 L675,262 L675,304", "d-aline d-dash")
    i += box(425, 304, 90, 54, "Sensors", "AI · DI", "d-box") + box(525, 304, 90, 54, "Actuators", "AO · DO", "d-box")
    i += box(630, 304, 90, 54, "VFD", "Modbus RTU", "d-box")
    i += t(285, 376, "RS485 field bus (MS/TP)", "d-ts d-ta") + t(520, 376, "hard-wired I/O", "d-ts") + t(675, 376, "serial link", "d-ts")
    return svg(760, 400, i, "The three levels of a BMS: management, automation and field")


def d_ddc_inside():
    i = defs("dd")
    i += rect(250, 40, 260, 200, "d-acc", 12) + t(380, 60, "DDC controller", "d-t d-tb d-ta")
    i += box(270, 80, 105, 64, "CPU", "runs the program", "d-box")
    i += box(385, 80, 105, 64, "Memory", "program · settings|trends", "d-box")
    i += box(270, 156, 105, 64, "Real-time clock", "date · time", "d-box")
    i += box(385, 156, 105, 64, "Comms ports", "Ethernet · RS485", "d-box")
    i += box(20, 70, 160, 64, "Sensors, switches", "temperature · pressure|run status", "d-box")
    i += line(180, 102, 248, 102, "d-aline", end="dd-a") + t(214, 88, "inputs", "d-ts")
    i += t(214, 116, "(ADC)", "d-ts")
    i += box(580, 70, 160, 64, "Actuators, relays", "valves · dampers|fan start", "d-box")
    i += line(512, 102, 578, 102, "d-aline", end="dd-a") + t(545, 88, "outputs", "d-ts")
    i += t(545, 116, "(DAC, relay)", "d-ts")
    i += box(20, 172, 160, 56, "24 V AC supply", "from panel transformer", "d-warn")
    i += line(180, 200, 248, 200, "d-line", end="dd")
    i += box(580, 172, 160, 56, "Network", "server · other controllers", "d-box")
    i += line(512, 200, 578, 200, "d-line", end="dd", start="dd")
    return svg(760, 255, i, "Block diagram of a DDC controller")


def d_scan_cycle():
    i = defs("sc")
    labels = [("1 · Read", "sample every|input terminal"), ("2 · Convert", "raw signal →|°C, Pa, %"),
              ("3 · Run program", "compare, PID,|interlocks, alarms"), ("4 · Write", "update relays|and 0–10 V"),
              ("5 · Communicate", "share values,|take commands")]
    for k, (a, b) in enumerate(labels):
        x = 12 + k * 150
        i += box(x, 40, 130, 80, a, b, "d-acc")
        if k < 4:
            i += line(x + 130, 80, x + 148, 80, "d-aline", end="sc-a")
    i += path("M677,120 L677,170 L77,170 L77,122", "d-line d-dash", end="sc")
    i += t(377, 188, "…then repeat — typically every 0.1 to 1 second", "d-ts")
    return svg(760, 205, i, "The DDC scan cycle")


def d_ahu_graphic():
    i = defs("gr")
    i += rect(10, 10, 740, 310, "d-box", 10) + rect(10, 10, 740, 38, "d-soft", 10)
    i += t(28, 29, "AHU-01 · Level 3 offices", "d-t d-tb", "start")
    i += t(732, 29, "Mon 10:42 · Occupied", "d-ts", "end")
    i += rect(575, 60, 160, 30, "d-ok", 15) + t(655, 75, "● RUNNING · AUTO", "d-ts d-tb d-tok")
    i += rect(30, 60, 92, 40, "d-box", 6) + t(76, 72, "Fresh air", "d-ts") + t(76, 88, "30 %", "d-t d-tb")
    i += line(30, 150, 118, 150, "d-aline", end="gr-a")
    i += rect(120, 112, 420, 92, "d-soft", 8)
    i += t(200, 140, "Filter", "d-ts") + t(200, 160, "OK", "d-t d-tb d-tok")
    i += t(300, 140, "CHW valve", "d-ts") + t(300, 160, "62 %", "d-t d-tb")
    i += circle(400, 155, 22, "d-box") + path("M389,165 L413,155 L389,145 Z")
    i += t(475, 140, "Fan speed", "d-ts") + t(475, 160, "42 Hz", "d-t d-tb")
    i += line(542, 150, 730, 150, "d-aline", end="gr-a")
    i += rect(585, 104, 110, 40, "d-box", 6) + t(640, 116, "SAT", "d-ts") + t(640, 132, "14.1 °C", "d-t d-tb")
    i += path("M730,250 L170,250 L170,206", "d-aline", end="gr-a")
    i += rect(385, 262, 130, 42, "d-box", 6) + t(450, 274, "RAT", "d-ts") + t(450, 291, "24.3 °C", "d-t d-tb")
    i += rect(530, 262, 200, 42, "d-acc", 6) + t(630, 274, "Setpoint · click to change", "d-ts")
    i += t(630, 291, "24.0 °C", "d-t d-tb d-ta")
    i += rect(30, 262, 100, 42, "d-soft", 6) + t(80, 283, "Trends ▸", "d-t")
    i += rect(142, 262, 110, 42, "d-soft", 6) + t(197, 283, "Schedule ▸", "d-t")
    return svg(760, 330, i, "Example operator graphic for AHU-01")


def d_alarm_states():
    i = defs("al")
    i += box(20, 110, 140, 60, "Normal", "", "d-ok")
    i += box(250, 40, 180, 60, "Active", "unacknowledged", "d-bad")
    i += box(540, 40, 190, 60, "Active", "acknowledged", "d-warn")
    i += box(250, 180, 180, 60, "Returned to normal", "unacknowledged", "d-warn")
    i += path("M90,110 L90,70 L248,70", "d-line", end="al") + t(168, 58, "limit crossed", "d-ts")
    i += line(430, 70, 538, 70, "d-line", end="al") + t(484, 58, "operator acks", "d-ts")
    i += path("M635,40 L635,16 L60,16 L60,108", "d-line", end="al") + t(350, 28, "value returns to normal", "d-ts")
    i += line(340, 100, 340, 178, "d-line", end="al") + t(350, 139, "value returns first", "d-ts", "start")
    i += path("M250,210 L90,210 L90,172", "d-line", end="al") + t(170, 224, "operator acks", "d-ts")
    return svg(760, 250, i, "Alarm life cycle")


def d_panel_layout():
    i = rect(20, 10, 720, 400, "d-box", 8)
    i += box(40, 30, 95, 60, "Isolator", "230 V in", "d-warn")
    i += box(145, 30, 95, 60, "MCBs / fuses", "per circuit", "d-warn")
    i += box(250, 30, 125, 60, "Transformer", "230 / 24 V AC", "d-warn")
    i += box(385, 30, 125, 60, "24 V DC PSU", "for 4–20 mA loops", "d-warn")
    i += box(520, 30, 95, 60, "Surge prot.", "RS485 / IP", "d-box")
    i += box(625, 30, 95, 60, "Switch", "Ethernet", "d-box")
    i += rect(40, 100, 680, 18, "d-soft", 3) + t(380, 109, "cable trunking", "d-ts")
    i += box(40, 128, 200, 90, "DDC controller", "CPU · comms · I/O", "d-acc")
    i += box(250, 128, 125, 90, "I/O module", "expansion", "d-acc")
    i += box(385, 128, 105, 90, "Spare space", "≈ 20 %", "d-soft")
    i += rect(500, 128, 220, 90, "d-box", 8) + t(610, 145, "Interposing relays", "d-t d-tb")
    for k in range(6):
        i += rect(512 + k * 34, 160, 26, 46, "d-soft", 3)
    i += rect(40, 228, 680, 18, "d-soft", 3) + t(380, 237, "cable trunking", "d-ts")
    for k in range(10):
        i += rect(48 + k * 20, 262, 15, 46, "d-warn", 2)
    i += t(145, 322, "230 V terminals", "d-ts") + t(145, 337, "MCC, power", "d-ts")
    i += line(268, 252, 268, 344, "d-line d-dash")
    for k in range(18):
        i += rect(282 + k * 20, 262, 15, 46, "d-acc", 2)
    i += t(460, 322, "24 V signal terminals", "d-ts") + t(460, 337, "AI · AO · DI · DO · RS485", "d-ts")
    i += rect(655, 278, 60, 14, "d-box", 2) + t(685, 322, "Earth bar", "d-ts")
    for k in range(9):
        i += circle(80 + k * 75, 388, 9, "d-soft")
    i += t(380, 365, "Cable entry from below — power on the left, signals on the right", "d-ts")
    return svg(760, 420, i, "Front view of a typical DDC control panel")


def d_interposing():
    i = defs("ir")
    i += box(20, 60, 170, 110, "DDC controller", "DO1|24 V, low current", "d-acc")
    i += rect(290, 40, 190, 140, "d-box", 8) + t(385, 58, "Interposing relay", "d-t d-tb")
    i += rect(305, 92, 50, 56, "d-soft", 4) + t(330, 120, "coil", "d-ts")
    i += line(190, 104, 305, 104) + line(190, 136, 305, 136)
    i += t(248, 92, "24 V control", "d-ts")
    i += line(380, 70, 380, 170, "d-line d-dash d-thin")
    i += line(420, 86, 420, 108) + line(420, 108, 440, 126) + line(420, 132, 420, 156)
    i += t(452, 120, "NO", "d-ts", "start")
    i += path("M420,86 L420,76 L580,76") + path("M420,156 L420,166 L580,166")
    i += box(580, 50, 160, 130, "MCC starter", "230 V start circuit|contactor coil", "d-warn")
    i += t(105, 198, "Controller output", "d-ts") + t(385, 198, "Isolation + higher rating", "d-ts")
    i += t(660, 198, "Motor control circuit", "d-ts")
    return svg(760, 212, i, "An interposing relay between a controller output and a motor starter")


def d_hardwired_vs_hli():
    i = defs("hw")
    i += t(190, 18, "Hard-wired", "d-t d-tb") + t(570, 18, "High-level interface (HLI)", "d-t d-tb")
    i += line(380, 34, 380, 232, "d-line d-dash d-thin")
    i += box(20, 44, 115, 160, "Chiller", "control panel", "d-box")
    i += box(245, 44, 115, 160, "DDC", "controller", "d-acc")
    rows = [(72, "Enable · DO", True), (106, "Run · DI", False), (140, "Fault · DI", False), (174, "Setpoint · AO", True)]
    for y, lab, to_chiller in rows:
        if to_chiller:
            i += line(243, y, 137, y, "d-line", end="hw")
        else:
            i += line(137, y, 243, y, "d-line", end="hw")
        i += t(190, y - 10, lab, "d-ts")
    i += t(190, 224, "4 values = 4 pairs of wires", "d-ts")
    i += box(400, 44, 115, 160, "Chiller", "controller", "d-box")
    i += box(625, 44, 115, 160, "BMS", "controller / server", "d-acc")
    i += line(517, 124, 623, 124, "d-aline", end="hw-a", start="hw-a")
    i += t(570, 106, "BACnet / Modbus", "d-ts d-ta") + t(570, 142, "one cable", "d-ts")
    i += t(570, 224, "100+ values over one cable", "d-ts")
    return svg(760, 240, i, "Hard-wired interface compared with a high-level interface")


# ==========================================================================
# Pages
# ==========================================================================

P1 = dict(
    id="1-1", slug="what-is-a-bms", title="What is a BMS?",
    objectives=[
        "Explain in plain words what a BMS is — and what it is not.",
        "List the five jobs every BMS does.",
        "Name the building systems a BMS controls, and those it only monitors.",
        "Describe the basic control loop: sense → decide → act.",
    ],
    one_line=("A Building Management System (BMS) is a network of controllers and software that "
              "<strong>monitors and automatically controls</strong> a building's services — mainly air-conditioning "
              "and ventilation — from one central place."),
    why=("<p>HVAC is usually the largest energy user in a commercial building, and it runs every day. Without "
         "automation, someone would have to walk the plant rooms switching equipment on and off, adjusting valves "
         "and checking for faults. A BMS does that work continuously: it keeps people comfortable, cuts wasted "
         "energy, and tells the maintenance team about a problem before the occupants notice it.</p>"
         "<p>Every BMS task you will do — wiring a sensor, programming a controller, integrating a chiller — "
         "serves those three goals: <strong>comfort, energy and reliability</strong>.</p>"),
    body=(
        "<h3>Other names you will hear</h3>"
        + table(["Term", "Meaning"], [
            ("BMS", "Building Management System — the usual term in India, the UK, the Middle East and most of Asia."),
            ("BAS", "Building Automation System — the usual term in the USA. Same thing."),
            ("BACS", "Building Automation and Control System — the term used in the ISO 16484 and EN standards."),
            ("BEMS", "Building Energy Management System — a BMS with the emphasis on energy metering and reporting."),
            ("IBMS", "Integrated BMS — one platform that also brings in fire alarm, CCTV, access control and more."),
        ])
        + "<p>This guide uses <strong>BMS</strong> throughout.</p>"
        + "<h3>The five jobs of a BMS</h3>"
        + steps([
            "<strong>Monitor</strong> — read values from sensors and equipment: temperatures, pressures, run status, faults.",
            "<strong>Control</strong> — decide what equipment should do and send commands: start a fan, open a valve to 40 %, change a fan's speed.",
            "<strong>Alarm</strong> — compare values with limits and alert people when something is wrong: a fan has tripped, a room is too hot, a filter is blocked.",
            "<strong>Schedule</strong> — run equipment only when it is needed, for example office AHUs from 08:00 to 19:00 on working days.",
            "<strong>Record and report</strong> — store values over time (<em>trends</em>) and produce energy and performance reports.",
        ])
        + "<h3>The basic idea: sense → decide → act</h3>"
        + "<p>Every automatic control in a building — from one fan coil unit to a whole chiller plant — follows the same three-step loop.</p>"
        + fig(d_control_loop(), "The control loop. Module 6 explains the maths (PID); for now, remember the loop.")
        + "<p>The value the controller is trying to reach is the <strong>setpoint</strong> (24 °C). The value it measures "
          "is the <strong>process variable</strong> (26 °C). Because the sensor measures the <em>result</em> of the action, "
          "the controller keeps correcting until the two match. This is called <strong>closed-loop</strong> or "
          "<strong>feedback</strong> control.</p>"
        + "<h3>What a BMS controls — and what it only watches</h3>"
        + fig(d_bms_hub(), "A BMS sits at the centre of the building's services. Solid lines: controlled. Dashed lines: monitored only.")
        + table(["System", "Typical BMS role"], [
            ("HVAC — AHUs, FCUs, chillers, pumps, cooling towers, ventilation fans", "Full monitoring and control. This is the core of every BMS."),
            ("Lighting — common areas, car parks, façade", "Schedules and on/off control, often through a separate lighting control system."),
            ("Energy meters — electrical, BTU, water", "Monitoring, logging and reports."),
            ("Plumbing — water tanks, transfer pumps, sump pits", "Level monitoring, pump status, high-level alarms; sometimes pump control."),
            ("Electrical — generators (DG), UPS, transformers, panels", "Monitoring only: status, alarms, kW."),
            ("Lifts", "Monitoring only: status and fault."),
            ("Fire alarm system", "Monitoring only. The fire system is independent and sends signals to the BMS."),
            ("Access control, CCTV", "Usually separate systems; linked only in an integrated BMS."),
        ])
        + callout("warn", "Life-safety systems stay independent",
                  "<p>A BMS never replaces the fire alarm panel or fire-fighting controls. Safety actions — such as "
                  "stopping an AHU when the fire alarm operates — are <strong>hard-wired</strong> so they work even if the "
                  "BMS fails. You will meet this again in Module 6.</p>")
        + "<h3>What a BMS is made of</h3>"
        + "<p>Every BMS, from any manufacturer, is built from four kinds of parts:</p>"
        + table(["Part", "Example", "Where you study it"], [
            ("Field devices", "Temperature sensor, valve actuator, damper actuator", "Module 3"),
            ("Controllers", "DDC controller in the AHU panel", "Page 1.3"),
            ("Network", "BACnet and Modbus cables, network switches", "Module 5"),
            ("Software", "BMS server, operator workstation", "Page 1.4"),
        ])
    ),
    ahu01=("<p>Throughout Level 1 we follow one example: <strong>AHU-01</strong>, an air handling unit that cools the "
           "3rd-floor offices of a commercial building. It has a supply fan on a VFD, a chilled-water cooling coil with "
           "a 2-way valve, a filter, a modulating fresh air damper and a manual return air damper.</p>"
           "<p>Its BMS job: <strong>hold the offices at 24 °C from 08:00 to 19:00, Monday to Saturday, and raise an alarm "
           "if anything fails.</strong> Each page adds one piece of the picture. See the full schematic on the "
           "<a href=\"../index.html#ahu-01\">Level 1 overview</a>.</p>"),
    on_site=[
        "On a new site, ask first for the <strong>BMS architecture drawing</strong> and the <strong>points list</strong>. Together they tell you what the system does.",
        "On project drawings, “BMS” usually means the whole package: controllers, panels, sensors, cables, software and integration.",
        "Before writing any logic that touches a life-safety system, check the interface schedule — the BMS usually only monitors it.",
        "Operators often see only the graphics. Learn to trace a value on screen back to the physical sensor; it is the core troubleshooting skill.",
    ],
    terms=[
        ("BMS / BAS", "A computer-based system that monitors and controls a building's services."),
        ("Point", "One value in the BMS: an input (e.g. a temperature) or an output (e.g. a start command)."),
        ("Setpoint", "The target value the controller is trying to reach, e.g. 24 °C."),
        ("Process variable", "The measured value being controlled, e.g. the actual room temperature."),
        ("Closed-loop control", "Control where the result is measured and fed back, so the controller keeps correcting."),
        ("Trend", "A record of a point's value over time, shown as a graph."),
        ("Alarm", "A notification that a value is outside its limits or equipment has failed."),
        ("Schedule", "A time program that decides when equipment should run."),
    ],
    scenarios=[dict(
        prompt="A facility manager asks you to “make the BMS start the fire pumps when a fire is detected”. What is the right response?",
        options=["Add the logic to the AHU controller, since it already receives the fire signal.",
                 "Explain that fire pumps are started by the fire-fighting system itself; the BMS should only monitor their status.",
                 "Use a BMS schedule to test-run the fire pumps every night instead."],
        answer=1,
        explain=(" Life-safety systems must work even if the BMS fails, so they control themselves and are tested under "
                 "fire regulations. The BMS monitors fire pump run, fault and power status and raises alarms."),
    )],
    questions=[
        ("What are the five jobs of a BMS?", "Monitor, control, alarm, schedule, and record/report."),
        ("Explain sense → decide → act using a room that is too warm.",
         "The sensor measures 26 °C (sense). The controller compares it with the 24 °C setpoint, sees the room is too warm, and works out a bigger valve opening (decide). The actuator opens the chilled-water valve (act). The room cools, the sensor measures the new temperature, and the loop repeats."),
        ("Why is the fire alarm system kept independent of the BMS?",
         "Life-safety functions must work even if the BMS, its network or its software fails. Fire systems have their own approved controls; the BMS only receives signals for monitoring, and safety actions such as AHU shutdown are hard-wired."),
        ("What is the difference between a setpoint and a process variable?",
         "The setpoint is the target (24 °C). The process variable is the measured actual value (e.g. 25.2 °C). The controller acts on the difference between them, called the error."),
        ("Name three systems a BMS typically only monitors.",
         "Any three of: generators (DG), UPS, transformers and electrical panels, lifts, the fire alarm system, energy meters."),
    ],
)

P2 = dict(
    id="1-2", slug="bms-architecture-levels", title="BMS architecture: field, automation and management levels",
    objectives=[
        "Name the three levels of a BMS and the devices at each level.",
        "Say which network is typically used at each level.",
        "Explain why the plant must keep running when the server fails.",
        "Place every AHU-01 component at the right level.",
    ],
    one_line=("A BMS is built in three layers: <strong>field</strong> devices measure and act, <strong>automation</strong> "
              "controllers run the control logic, and the <strong>management</strong> level gives people a window into the "
              "whole building."),
    why=("<p>When something goes wrong, the first useful question is <em>which level is the problem at?</em> A wrong "
         "temperature on screen could be a faulty sensor (field), a configuration mistake (automation) or a stale "
         "screen (management). Thinking in levels turns a vague complaint into a short list of checks.</p>"
         "<p>The three levels are described in the international standard for building automation, ISO 16484, so "
         "every manufacturer's system follows the same basic pattern — even when the product names differ.</p>"),
    body=(
        fig(d_three_levels(), "The three levels. Solid lines: hard-wired or main network. Dashed: serial link (Modbus RTU) to the VFD.")
        + "<h3>Field level — the senses and muscles</h3>"
        + "<p>Everything that physically touches the building: sensors (temperature, humidity, pressure, CO₂), actuators "
          "(valves, dampers), switches, relays and drives. Most field devices are wired straight to a controller's "
          "inputs and outputs — this is <strong>hard-wired I/O</strong>.</p>"
          "<p>Smarter field devices — VFDs, energy meters, small room controllers — talk to the controller over a "
          "<strong>field bus</strong>, usually an RS485 cable running BACnet MS/TP or Modbus RTU.</p>"
        + "<h3>Automation level — the brains</h3>"
        + "<p>DDC controllers read the field devices, run the control program and drive the outputs. Each controller "
          "looks after one plant item or one area — one AHU, a group of FCUs, the chiller plant.</p>"
          "<p>Larger systems add a <strong>supervisory controller</strong> (also called a network controller or "
          "building controller). It usually controls no equipment itself. Instead it:</p>"
        + bullets([
            "collects data from the field controllers below it,",
            "routes messages between the RS485 field bus and the IP network,",
            "runs building-wide schedules and shares values such as outdoor temperature,",
            "stores trends and alarms locally while the server is unavailable.",
        ])
        + "<h3>Management level — the window</h3>"
        + "<p>The BMS server and the operator workstations. This is where people view graphics, acknowledge alarms, "
          "change setpoints and schedules, look at trends and print reports. The server also keeps long-term history "
          "and connects to other systems such as energy dashboards and maintenance software.</p>"
        + table(["Level", "Typical devices", "Main job", "Typical network"], [
            ("Management", "BMS server, workstation, web and mobile clients", "Show, store, alarm handling, reports", "Ethernet / IP (BACnet/IP, web)"),
            ("Automation", "Supervisory controllers, DDC plant controllers", "Run control logic, schedules, local alarms", "BACnet/IP or BACnet MS/TP"),
            ("Field", "Sensors, actuators, VFDs, meters, room controllers", "Measure and act", "Hard-wired I/O; RS485 (MS/TP, Modbus RTU)"),
        ])
        + "<h3>The golden rule: control lives in the controller</h3>"
        + callout("tip", "Remember",
                  "<p>The server is a <strong>window</strong>, not the brain. If the server or the network goes down, every "
                  "DDC controller must keep running its plant with its own program, setpoints and schedule. Operators lose "
                  "visibility, but the building keeps working. This is called <strong>standalone operation</strong>, and it is "
                  "the main reason for the layered design.</p>")
        + table(["If this fails…", "…this still works", "…and this is lost"], [
            ("BMS server", "All controllers run normally", "Graphics, central alarms, long-term trends (controllers may buffer some)"),
            ("IP network between floors", "Controllers on each side run normally", "Values shared across the break, e.g. outdoor temperature"),
            ("One DDC controller", "All other plant", "Control of that plant item — its outputs go to their fail-safe state"),
            ("One sensor", "The controller", "Good control of that loop — a well-written program alarms and uses a fallback"),
        ])
        + "<h3>Modern systems: the levels are flattening</h3>"
        + "<p>Older systems had strict layers joined by proprietary networks. Today many controllers sit directly on the "
          "IP network, and some field devices (smart actuators, wireless sensors) talk IP too. The three-level model is "
          "still the right way to <em>think</em>: even when everything shares one network, each device still does a "
          "field, automation or management job.</p>"
    ),
    ahu01=table(["Level", "AHU-01 parts"], [
        ("Field", "Return and supply air sensors, duct pressure sensor, filter ΔP switch, CHW valve actuator, fresh air damper actuator, VFD"),
        ("Automation", "DDC-AHU-01, a plant controller in the panel in the 3rd-floor AHU room, connected to the floor's IP network"),
        ("Management", "The AHU-01 graphic, alarms and trends on the BMS server"),
    ], "plain"),
    on_site=[
        "For any complaint, decide the level first: is the field device wrong, the controller logic wrong, or only the screen?",
        "Compare the value on the BMS screen with the value at the controller (local display or service tool). If they match, look at the field device or the logic; if not, look at communication or the server.",
        "Keep a copy of the <strong>network riser diagram</strong>. It shows which controller sits on which network and is the map for every communication fault.",
        "Ask which plant must keep running without the server. Its schedules and setpoints must live in the controller.",
    ],
    faults=[
        ("A whole floor shows “offline” on the graphics, but the AHUs are running", "Network switch or supervisory controller for that floor is down", "Switch power and port lights, supervisory controller status LEDs, IP cable"),
        ("One value is clearly wrong; others are fine", "Sensor, its wiring, or its scaling", "Measure at the sensor and compare with the controller's reading"),
        ("Plant stopped when the server was restarted", "Schedule or logic was running in the server, not the controller", "Move the schedule and logic into the controller"),
        ("All values stop updating at the same time", "Server communication driver or service stopped", "Server services, licence, driver status"),
    ],
    terms=[
        ("Field level", "Sensors, actuators and other devices that measure and act on the building."),
        ("Automation level", "DDC and supervisory controllers that run the control logic."),
        ("Management level", "Servers, workstations and clients used by people to view and manage the system."),
        ("Supervisory controller", "A controller that manages a group of field controllers, routes between networks and stores data locally."),
        ("Field bus", "A communication cable (usually RS485) linking controllers and smart field devices."),
        ("Hard-wired I/O", "Field devices wired directly to controller input and output terminals."),
        ("Standalone operation", "A controller running its plant on its own when the server or network is unavailable."),
        ("Network riser diagram", "Drawing showing every controller and how they connect, floor by floor."),
    ],
    scenarios=[dict(
        prompt="The 5th-floor graphics show “---” for every value. Staff on the 5th floor say it is comfortable, and you can hear the AHU running. Where is the fault most likely?",
        options=["Field level — all the 5th-floor sensors have failed.",
                 "Automation level — every 5th-floor controller has stopped.",
                 "Communication between the 5th floor and the management level (switch, cable or supervisory controller)."],
        answer=2,
        explain=(" The floor is comfortable and the AHU runs, so the sensors and controllers are working. Only visibility is lost, "
                 "which points to the link between the floor and the server."),
    )],
    questions=[
        ("Name the three levels of a BMS and give one device at each.",
         "Management — BMS server or workstation. Automation — DDC plant controller or supervisory controller. Field — temperature sensor, valve actuator, VFD."),
        ("What does a supervisory controller do?",
         "It manages a group of field controllers: collects their data, routes messages between the field bus and the IP network, runs shared schedules and values, and buffers trends and alarms if the server is down. It usually has little or no plant I/O."),
        ("The BMS server is switched off for maintenance. What happens to AHU-01?",
         "Nothing changes in its operation. DDC-AHU-01 keeps running its program, setpoints and schedule. Operators cannot see the graphic or receive central alarms until the server is back."),
        ("Why might a VFD be connected over a field bus as well as hard-wired?",
         "The field bus gives many extra values — frequency, current, kW, energy, fault codes — for the cost of one cable. The critical start/stop and status are still hard-wired so the fan works if communication fails."),
        ("Which standard describes the three-level model for building automation?", "ISO 16484."),
    ],
)

P3 = dict(
    id="1-3", slug="ddc-controller", title="The DDC controller and how it works",
    objectives=[
        "Explain what “direct digital control” means and why it replaced older controls.",
        "Name the main parts inside a DDC controller.",
        "Describe the scan cycle step by step.",
        "Tell a programmable plant controller from an application-specific controller.",
    ],
    one_line=("A DDC (Direct Digital Control) controller is a small industrial computer that <strong>reads its inputs, "
              "runs a control program and writes its outputs</strong> — in a continuous loop, typically once a second or faster."),
    why=("<p>Every point on a BMS starts or ends at a controller terminal. When you understand how the controller sees the "
         "world — as numbers read and written on every cycle — most things you see on site make sense: why readings are "
         "smoothed, why an output “won't move”, and what happens when the power or the network drops.</p>"),
    body=(
        "<h3>Why “direct digital”?</h3>"
        "<p>Before DDC, buildings used pneumatic (compressed-air) or electronic analogue controllers. Each control loop "
        "needed its own device, and the logic was fixed by the hardware. With DDC, a digital processor makes the control "
        "decisions <em>directly</em> in software. One controller can run many loops, the logic is changed by editing the "
        "program, and every value can be shared over the network and shown on the BMS.</p>"
        "<h3>What is inside</h3>"
        + fig(d_ddc_inside(), "Inside a DDC controller. Inputs come in on the left, outputs leave on the right.")
        + table(["Part", "What it does"], [
            ("Power supply", "Usually 24 V AC from a transformer in the panel; some models use 24 V DC or 230 V AC."),
            ("Processor (CPU)", "Runs the control program."),
            ("Memory", "Holds the program, settings (setpoints, schedules) and recent trends. Flash or battery-backed, so settings survive a power cut."),
            ("Real-time clock", "Keeps date and time for schedules. Usually battery-backed or synchronised over the network."),
            ("Input circuits", "Turn sensor signals into numbers. An analogue-to-digital converter (ADC) converts a resistance, voltage or current into a value."),
            ("Output circuits", "Relays or triacs for on/off outputs; a digital-to-analogue converter (DAC) makes 0–10 V or 4–20 mA signals."),
            ("Communication ports", "Ethernet for IP networks, RS485 for field buses, a USB or service port for the engineer's laptop."),
            ("Status LEDs / display", "Show power, program running, communication activity and faults."),
        ])
        + "<h3>Inputs and outputs in one minute</h3>"
        + "<p>Module 4 covers I/O in detail. For now, learn the four letters:</p>"
        + table(["Type", "Direction and kind", "Example on AHU-01"], [
            ("DI — digital input", "Into the controller; on or off", "Fan run status, filter dirty switch"),
            ("DO — digital output", "Out of the controller; on or off", "Fan start/stop command"),
            ("AI — analogue input", "Into the controller; a range of values", "Return air temperature"),
            ("AO — analogue output", "Out of the controller; a range of values", "CHW valve position 0–100 %"),
            ("UI — universal input", "Configured in software as AI or DI", "Most modern controllers have UIs"),
        ])
        + "<h3>The scan cycle</h3>"
        + fig(d_scan_cycle(), "The controller repeats the same five steps for as long as it has power.")
        + steps([
            "<strong>Read inputs.</strong> The controller samples every input terminal: the resistance of a temperature sensor, a voltage, a current, an open or closed contact.",
            "<strong>Convert.</strong> Raw readings become engineering units using each input's configuration — for example 10.5 kΩ from an NTC sensor becomes 23.8 °C, and 12 mA becomes 250 Pa. Filtering smooths out electrical noise.",
            "<strong>Run the program.</strong> The logic runs: compare values with setpoints, calculate PID loops, check interlocks and alarms, follow the schedule.",
            "<strong>Write outputs.</strong> The results go to the output terminals: a relay closes, a valve gets a new 0–10 V signal.",
            "<strong>Communicate.</strong> Share values with other controllers and the server, and accept operator commands such as a setpoint change.",
        ])
        + "<p>Then it starts again. A cycle typically takes between a tenth of a second and about one second. That is fast "
          "enough for HVAC, where temperatures change over minutes, not milliseconds.</p>"
        + "<h3>Types of controller</h3>"
        + table(["Type", "Used for", "How it is set up"], [
            ("Plant controller (freely programmable)", "AHUs, chiller plants, pump sets — anything with custom logic and many points", "The engineer writes the program, usually with graphical function blocks"),
            ("Application-specific controller (ASC)", "FCUs, VAV boxes, simple exhaust fans — many identical units", "Pre-loaded application; the engineer selects options and sets parameters"),
            ("Supervisory / network controller", "Managing a group of controllers, routing, building-wide schedules", "Configured; little or no plant I/O"),
            ("I/O expansion module", "Adding more points to a plant controller", "No logic of its own — extends the controller's I/O"),
        ])
        + "<h3>Standalone operation and fail-safe positions</h3>"
        + "<p>A DDC controller must not depend on the server to do its job. Its program, setpoints and schedule are stored "
          "locally. If a value it receives over the network — such as the outdoor temperature from another controller — "
          "stops updating, a good program detects this and switches to a sensible fallback value.</p>"
          "<p>If the controller itself loses power, outputs go to their <strong>fail-safe</strong> state: relays drop out "
          "(so fans stop) and spring-return actuators drive valves and dampers to a chosen safe position — for example the "
          "fresh air damper closes. Choosing these positions is part of the design.</p>"
    ),
    ahu01=("<p>DDC-AHU-01 runs AHU-01. On every scan it reads the return air temperature (AI), compares it with the 24 °C "
           "setpoint, runs a PID loop and writes a new CHW valve position (AO). It also checks that the fan's run status (DI) "
           "follows the start command (DO) — if the fan does not prove running within about 30 seconds, it raises a "
           "<em>fan fail</em> alarm and stops the fan.</p>"),
    on_site=[
        "A healthy controller usually shows: power LED on, a “run” or heartbeat LED blinking, and communication LEDs flickering. Learn what the LEDs mean on the brand you work with.",
        "Check the controller's own reading (local display or service tool) before blaming the BMS server.",
        "Back up the controller program and database before any change, and again after commissioning.",
        "Leave spare capacity: a good panel design keeps around 10–20 % spare I/O for future changes.",
        "Never connect 230 V to an input or output rated for 24 V — it destroys the I/O circuit instantly.",
        "When an output “won't respond”, look for an override first: on the BMS, on the controller, or a hand/auto switch in the panel.",
    ],
    faults=[
        ("Controller offline, no LEDs lit", "No power: blown fuse, tripped MCB or failed transformer", "24 V AC at the controller terminals"),
        ("Controller keeps restarting", "Transformer overloaded or supply voltage dipping", "Supply voltage while actuators are moving; total VA of connected devices"),
        ("Output command changes but the equipment does not", "Override active, or a wiring/relay fault", "Override status on BMS and controller, HOA switch, output LED, voltage at the terminal"),
        ("A value is frozen at its last reading", "Program stopped, or input misconfigured", "Program run status, input type and configuration"),
        ("Settings or time lost after a power cut", "Memory backup battery flat, or changes not saved to flash", "Battery status; the vendor's save or commit procedure"),
    ],
    terms=[
        ("DDC", "Direct Digital Control: a digital processor makes the control decisions in software."),
        ("Scan cycle", "The repeating loop of read inputs → convert → run program → write outputs → communicate."),
        ("ADC / DAC", "Converters between electrical signals and numbers: analogue-to-digital (inputs) and digital-to-analogue (outputs)."),
        ("Universal input (UI)", "An input that can be configured in software as analogue or digital."),
        ("Plant controller", "A freely programmable controller for complex plant such as AHUs."),
        ("ASC", "Application-specific controller with a pre-loaded program, used for FCUs, VAV boxes and similar."),
        ("Fail-safe position", "The state an output goes to when power or control is lost."),
        ("Override", "A manual command that replaces the program's output until it is released."),
        ("Firmware", "The controller's built-in operating software, separate from the application program."),
    ],
    scenarios=[dict(
        prompt="After a weekend power cut, DDC-AHU-01 is running again, but AHU-01 now starts at 03:00 instead of 08:00 every day. The schedule settings look correct. What is the most likely cause?",
        options=["The return air sensor has drifted.",
                 "The controller's real-time clock lost its time and is not synchronised.",
                 "The VFD has been set to the wrong speed."],
        answer=1,
        explain=(" The schedule is right but runs at the wrong time, so the controller's clock is wrong. Check the clock's backup "
                 "battery and set up network time synchronisation from the server."),
    )],
    questions=[
        ("Put the five steps of the scan cycle in order.", "Read inputs → convert to engineering units → run the program → write outputs → communicate. Then repeat."),
        ("What does the ADC do in a controller?", "The analogue-to-digital converter turns an electrical input — resistance, voltage or current — into a number the processor can use."),
        ("What is the difference between a plant controller and an ASC?",
         "A plant controller is freely programmable and used for complex plant such as AHUs. An ASC runs a pre-loaded application for a standard unit such as an FCU or VAV box; you only set options and parameters."),
        ("What happens to AHU-01's outputs if DDC-AHU-01 loses power?",
         "They go to their fail-safe state: the fan start relay drops out so the fan stops, and spring-return actuators drive the valve and damper to their designed safe positions — for example the fresh air damper closes."),
        ("Name three things a controller stores in its memory.", "The program, settings such as setpoints and schedules, and recent trend and alarm data."),
    ],
)

P4 = dict(
    id="1-4", slug="server-workstation-operator-interface", title="BMS server, workstation and operator interface",
    objectives=[
        "Explain what the BMS server does and what it stores.",
        "Describe the four screens an operator uses most: graphics, alarms, trends and schedules.",
        "Follow the life cycle of an alarm.",
        "Explain why manual overrides must be managed carefully.",
    ],
    one_line=("The BMS <strong>server</strong> collects data from every controller and stores the building's history; the "
              "<strong>workstation and operator interface</strong> are how people see that data and give commands."),
    why=("<p>Most people judge a BMS by what they see on screen. As a BMS engineer you will build these screens, set up the "
         "alarms and trends, and train the operators. Good front-end work turns thousands of points into a few clear "
         "pictures; poor work hides the one alarm that matters among a hundred that don't.</p>"),
    body=(
        "<h3>The BMS server</h3>"
        "<p>The server is a computer — physical or virtual — running the BMS supervisory software. Its jobs:</p>"
        + table(["Function", "What it means"], [
            ("Data collection", "Polls or receives values from all controllers."),
            ("Database", "Holds the list of every device, point and graphic."),
            ("History (trend logs)", "Stores values over time — e.g. AHU-01 return air temperature every 5 minutes for a year."),
            ("Alarm management", "Receives, stores and routes alarms; sends e-mail or SMS notifications."),
            ("Schedules and calendars", "A central place to view and edit schedules and holidays. The schedules themselves still run in the controllers."),
            ("Users and security", "User accounts, access levels, and an audit trail of who changed what."),
            ("Integration", "Drivers for third-party systems; exports to energy or maintenance software."),
            ("Reports", "Energy use, run-hours, alarm statistics, performance."),
        ])
        + "<h3>Workstations and clients</h3>"
        + "<p>A <strong>workstation</strong> is a PC that operators use to work with the BMS. Most modern systems are "
          "web-based, so any authorised browser, tablet or phone can act as a <strong>client</strong>. Plant rooms may "
          "also have a <strong>local display</strong> (HMI) on the panel door, which shows the controller's points even "
          "when the server is unavailable.</p>"
        + "<h3>The four screens every operator uses</h3>"
        + cards([
            ("Graphics", "Pictures of the plant and floor plans with live values. Click a point to command it."),
            ("Alarm console", "A list of active alarms with priority, time and state. This is where alarms are acknowledged."),
            ("Trends", "Graphs of values over time — the best tool for finding when and why a problem started."),
            ("Schedules", "Weekly time programs and holiday calendars that decide when plant runs."),
        ])
        + fig(d_ahu_graphic(), "A typical AHU graphic: the plant drawn simply, live values beside each device, the setpoint next to the value it controls.")
        + "<h3>The life of an alarm</h3>"
        + fig(d_alarm_states(), "Alarm states. An alarm leaves the list only when it is both back to normal and acknowledged.")
        + "<p>Alarms carry a <strong>priority</strong> so the important ones stand out and can be routed differently:</p>"
        + table(["Priority", "Example", "Typical routing"], [
            ("Critical", "Fire shutdown active, chiller plant tripped", "Alarm console + SMS to the on-call engineer"),
            ("High", "AHU fan failed, pump tripped", "Alarm console + e-mail"),
            ("Medium", "Room temperature out of range for 15 minutes", "Alarm console"),
            ("Low / maintenance", "Filter dirty, run-hours due for service", "Alarm console or maintenance report"),
        ])
        + callout("tip", "Avoid alarm flooding",
                  "<p>A good alarm is one somebody needs to act on. If operators see hundreds a day, they stop reading them. "
                  "Use time delays (e.g. 15 minutes before a high-temperature alarm), suppress alarms that cannot matter "
                  "(no temperature alarms while the AHU is off by schedule), and review alarm counts every month.</p>")
        + "<h3>Commands and overrides</h3>"
        + "<p>Operators can command points: start a fan, change a setpoint, force a valve to 100 %. A <strong>manual "
          "override</strong> replaces the program's value until someone releases it.</p>"
        + callout("warn", "Forgotten overrides",
                  "<p>Overrides left in place are one of the most common causes of wasted energy and “mystery” faults. A fan "
                  "forced ON during a test runs all night; a valve forced to 0 % leaves a floor hot for weeks. Use timed "
                  "overrides where the system allows it, and check the override list regularly.</p>")
        + "<h3>Users and access levels</h3>"
        + table(["Level", "Typical rights"], [
            ("View only", "See graphics, alarms and trends."),
            ("Operator", "Acknowledge alarms; change setpoints and schedules within limits."),
            ("Engineer", "Change configuration, logic, graphics and alarm limits."),
            ("Administrator", "Manage users, backups and system settings."),
        ])
        + "<p>Basic cyber-security: change every default password, give each person their own login (so the audit trail "
          "means something), keep the BMS network separate from the office network, and keep backups off the server.</p>"
    ),
    ahu01=("<p>On the server, AHU-01 has:</p>"
           + bullets([
               "<strong>a graphic</strong> like the one above;",
               "<strong>alarms</strong> — fan fail (high), fire shutdown (critical), return air above 27 °C for 15 minutes (medium), filter dirty (low);",
               "<strong>trends</strong> — return and supply air temperature, valve position, fan speed and CO₂, every 5 minutes;",
               "<strong>a schedule</strong> — Monday to Saturday, 08:00–19:00, with the public-holiday calendar.",
           ])),
    on_site=[
        "Make sure the server and all controllers use one time source (NTP); otherwise trends and alarm times will not line up.",
        "When investigating a problem, open a trend before touching anything. It usually shows when the problem started and what changed.",
        "Keep graphics honest: show units, put each setpoint next to the value it controls, and make points in override stand out.",
        "Back up the server before any upgrade or major change, and store a copy somewhere other than the server.",
    ],
    faults=[
        ("Graphic shows “?”, “---” or greyed-out values", "Controller offline or the point is not communicating", "Controller status and network"),
        ("Gaps in trend graphs", "Server was down, or the controller's trend buffer overflowed", "Server uptime; trend interval and buffer size"),
        ("Alarms arrive late or with wrong times", "Clocks not synchronised", "NTP / time-sync settings on server and controllers"),
        ("Operators ignore alarms", "Too many nuisance alarms", "Alarm count report; add delays and suppression"),
        ("Plant runs at night or at weekends", "Override left on, or a wrong schedule or holiday", "Override list, schedule, holiday calendar"),
    ],
    terms=[
        ("Server", "Computer running the BMS supervisory software and database."),
        ("Workstation / client", "A PC, browser or mobile device used to operate the BMS."),
        ("HMI / local display", "A screen on or near the panel showing the controller's points."),
        ("Graphic", "A live picture of plant or a floor plan with values and commands."),
        ("Trend log", "Stored history of a point's values over time."),
        ("Alarm priority", "The importance of an alarm, used for display and routing."),
        ("Acknowledge", "An operator's confirmation that an alarm has been seen."),
        ("Override", "A manual command that replaces the program's value until released."),
        ("Audit trail", "Record of who changed what, and when."),
        ("NTP", "Network Time Protocol — keeps all clocks on the network in step."),
    ],
    scenarios=[dict(
        prompt="AHU-01 ran all weekend, although its schedule is Monday to Saturday 08:00–19:00 and the schedule is set correctly. What do you check first?",
        options=["The return air temperature sensor.", "The override list — someone may have commanded the fan ON manually.",
                 "The chilled water plant."],
        answer=1,
        explain=(" A correct schedule that is not being followed usually means the program's output is being overridden. "
                 "Check the override list (and the HOA switch in Hand). Then release the override and find out why it was set."),
    )],
    questions=[
        ("Name four functions of a BMS server.", "Any four of: data collection, database, history/trends, alarm management, schedules and calendars, users and security, integration, reports."),
        ("An alarm returns to normal before anyone acknowledges it. Does it leave the alarm list?",
         "No. It moves to “returned to normal, unacknowledged” and stays on the list until an operator acknowledges it, so short events are not missed."),
        ("Give two ways to reduce nuisance alarms.", "Add time delays; suppress dependent alarms when plant is off by schedule; set sensible limits; review alarm counts regularly."),
        ("Why should every operator have their own login?", "So the audit trail shows who made each change, and access rights can be set per person."),
        ("Why are forgotten overrides a problem?", "They keep equipment in a fixed state regardless of the program — wasting energy or causing comfort complaints — often without anyone noticing."),
    ],
)

P5 = dict(
    id="1-5", slug="control-panel-architecture", title="BMS control panel architecture",
    objectives=[
        "Name the main components inside a DDC control panel and what each does.",
        "Explain why interposing relays are used.",
        "Describe the signals exchanged between the BMS panel and the motor control centre (MCC).",
        "Recognise good panel practice: segregation, labelling, spare capacity.",
    ],
    one_line=("A BMS control panel (DDC panel) is the enclosure that houses the controller with its <strong>power supplies, "
              "protection, relays and terminals</strong>, so field wiring can be connected safely and neatly."),
    why=("<p>Most hands-on BMS work happens at the panel: terminating cables, measuring signals, replacing relays, "
         "connecting a laptop. A well-built panel makes this quick and safe; a poor one hides faults behind loose "
         "terminals and missing labels. You also need to read panel drawings to wire, test and fault-find.</p>"),
    body=(
        fig(d_panel_layout(), "A typical DDC panel. Orange: 230 V side. Blue: controller and 24 V signal side, kept apart.")
        + table(["Component", "What it does"], [
            ("Incoming isolator / MCB", "Switches and protects the panel's 230 V supply."),
            ("Circuit MCBs or fuses", "Protect each circuit separately — controller, transformer, 24 V DC supply, field devices."),
            ("Control transformer (230 / 24 V AC)", "Supplies 24 V AC to the controller and actuators. Sized in VA for all loads, plus a margin."),
            ("24 V DC power supply (SMPS)", "Powers 4–20 mA sensors and other DC devices."),
            ("DDC controller and I/O modules", "Mounted on DIN rail, with spare space for future modules."),
            ("Interposing relays", "Stand between controller outputs and field circuits (see below)."),
            ("Terminal blocks", "Every field cable lands here — never directly on the controller. Numbered to match the drawings."),
            ("Cable trunking", "Keeps wiring tidy and separates power from signal cables."),
            ("Earth bar", "Protective earth and cable-screen connections."),
            ("Network devices", "Ethernet switch, surge protection for RS485 and IP cables, repeaters where needed."),
            ("Accessories", "Panel light, cooling fan and filter, door-mounted display, drawing pocket."),
        ])
        + "<h3>Why interposing relays?</h3>"
        + "<p>A controller's digital output is a small relay or triac meant for low currents. A motor starter in the MCC "
          "may work at 230 V and draw more current, and a fault in that circuit could destroy the controller. An "
          "<strong>interposing relay</strong> sits between them: the controller's output energises the relay coil at 24 V, "
          "and the relay's own, stronger contact switches the field circuit.</p>"
        + fig(d_interposing(), "The controller only ever switches the 24 V relay coil. The relay's contact switches the MCC circuit.")
        + steps([
            "<strong>Isolation</strong> — the 230 V field circuit never reaches the controller.",
            "<strong>Higher rating</strong> — the relay contact can carry more current and voltage than the controller output.",
            "<strong>Easy replacement</strong> — plug-in relays are cheap and swapped in seconds; a damaged controller output is not.",
            "<strong>Visible state</strong> — most relays have an LED, so you can see the command without a meter.",
        ])
        + "<h3>The BMS–MCC interface</h3>"
        + "<p>Fans and pumps are powered and protected in the <strong>motor control centre (MCC)</strong> or a starter "
          "panel — not in the BMS panel. The two panels exchange a few simple signals:</p>"
        + table(["Signal", "Direction", "Point type", "Meaning"], [
            ("Start / stop command", "BMS → MCC", "DO (relay contact)", "Contact closed = run"),
            ("Run status", "MCC → BMS", "DI", "Contactor auxiliary or VFD relay closed = running"),
            ("Trip / fault", "MCC → BMS", "DI", "Overload tripped or VFD fault"),
            ("Auto / manual status", "MCC → BMS", "DI", "Selector in Auto = the BMS is in control"),
            ("Speed reference", "BMS → VFD", "AO (0–10 V or 4–20 mA)", "Required fan or pump speed"),
        ])
        + "<p>These contacts are <strong>potential-free</strong> (also called volt-free or dry): each one is just a switch, "
          "and the receiving side supplies its own voltage. That keeps the two panels electrically independent. "
          "Module 4 explains this fully.</p>"
        + callout("note", "The HOA switch",
                  "<p><strong>Hand–Off–Auto.</strong> In <em>Hand</em> the motor runs locally whatever the BMS says; in <em>Off</em> it "
                  "is stopped; only in <em>Auto</em> does the BMS command it. Many “the BMS won't start the fan” calls end at a "
                  "switch left in Hand or Off — which is exactly why the auto/manual status is wired back to the BMS.</p>")
        + "<h3>Good panel practice</h3>"
        + bullets([
            "<strong>Segregate</strong> 230 V wiring from 24 V signal wiring — separate trunking and terminal groups. Mixing them causes electrical noise and is a safety risk.",
            "<strong>Ferrule</strong> every wire end with a number that matches the drawing, and label every device.",
            "Keep <strong>10–20 % spare</strong> terminals, I/O and DIN-rail space.",
            "Earth cable <strong>screens at one end only</strong>, normally at the panel (more in Module 4).",
            "Choose an enclosure <strong>IP rating</strong> for the location — e.g. IP54 in a plant room, higher outdoors.",
            "Keep a copy of the drawings in the <strong>door pocket</strong> and update them after every change.",
        ])
        + "<h3>Panel drawings</h3>"
        + table(["Drawing", "Shows"], [
            ("General arrangement (GA)", "Physical layout of components on the back-plate and door."),
            ("Power distribution", "Incoming supply, MCBs, fuses, transformer and power supplies."),
            ("I/O wiring schematic", "Each controller terminal, its terminal block and the field device it connects to."),
            ("Terminal schedule", "Every terminal with its cable number and destination."),
            ("Bill of materials", "Every component with make and part number."),
        ])
        + "<p>Panels are tested twice: a <strong>factory acceptance test</strong> (FAT) at the panel builder, and a site "
          "acceptance test after installation, when every point is checked end to end.</p>"
    ),
    ahu01=("<p>Panel <strong>DDC-AHU-01</strong> sits in the 3rd-floor AHU room. It takes 230 V from the floor's distribution "
           "board through a 6 A MCB and contains: a 230/24 V AC transformer for the controller and the two actuators; a "
           "24 V DC supply for the 4–20 mA duct pressure sensor; one interposing relay for the fan start; terminals for all "
           "hard-wired points plus spares; and RS485 terminals for the Modbus link to the VFD.</p>"),
    on_site=[
        "Before working inside a panel, isolate it and <strong>prove it dead</strong> with a tester. The incoming terminals stay live even when the controller is off.",
        "Measure the 24 V AC at the transformer and at the controller while the actuators are moving — that is when a weak supply shows.",
        "Tug each wire gently to find loose terminals; they cause intermittent faults that are hard to trace.",
        "Relay LED on but the motor does not run? The problem is on the MCC side: HOA position, contactor, overload, wiring.",
        "Mark up the drawings when you change wiring. Up-to-date “as-built” drawings save the next engineer hours.",
    ],
    faults=[
        ("Controller and actuators all dead", "Blown fuse, tripped MCB or failed transformer", "230 V in, 24 V out, each fuse"),
        ("Random restarts, or actuators stall when several move", "Transformer too small; voltage dips", "Total VA against transformer rating; voltage under load"),
        ("Fan won't start; relay LED is ON", "MCC side: HOA not in Auto, overload tripped, wiring", "Auto/manual DI, MCC panel, overload"),
        ("Fan won't start; relay LED is OFF", "No command: schedule, interlock, override, or DO fault", "Command on the BMS, controller output LED"),
        ("Unstable analogue readings", "Signal cable next to power cable, or screen not earthed", "Cable routes, segregation, screen earth"),
        ("All 4–20 mA sensors read zero or fault", "24 V DC supply off or its fuse blown", "24 V DC at the supply and at the terminals"),
    ],
    terms=[
        ("DDC panel", "Enclosure holding the controller, power supplies, protection, relays and terminals."),
        ("Control transformer", "Steps 230 V AC down to 24 V AC for controllers and actuators; rated in VA."),
        ("SMPS", "Switched-mode power supply — here, the 24 V DC supply for sensors."),
        ("Interposing relay", "A relay between a controller output and a field circuit, for isolation and higher rating."),
        ("Potential-free contact", "A contact that is only a switch, carrying no voltage of its own. Also “volt-free” or “dry”."),
        ("MCC", "Motor control centre — where motors are powered, started and protected."),
        ("HOA switch", "Hand–Off–Auto selector; the BMS has control only in Auto."),
        ("Ferrule", "A numbered marker on a wire end matching the drawing."),
        ("Segregation", "Keeping power and signal wiring physically separate."),
        ("FAT", "Factory acceptance test of the panel before delivery."),
        ("IP rating", "Ingress Protection — how well an enclosure keeps out dust and water (e.g. IP54)."),
    ],
    scenarios=[dict(
        prompt="The BMS commands AHU-01's fan ON. The interposing relay's LED is lit, but the fan is not running. The auto/manual status on the graphic shows “Manual”. What is the likely cause?",
        options=["The controller's digital output has failed.",
                 "The HOA switch in the MCC or VFD is not in Auto, so the BMS command is ignored.",
                 "The return air sensor is reading too low."],
        answer=1,
        explain=(" The relay LED proves the BMS is commanding the fan, and the auto/manual status says the MCC is not in Auto. "
                 "Put the switch back to Auto — and find out who left it in Hand or Off, and why."),
    )],
    questions=[
        ("Why are field cables landed on terminal blocks rather than directly on the controller?",
         "Terminal blocks give a clear, numbered connection point for testing and disconnection, protect the controller's terminals from repeated work, and let the controller be replaced without disturbing field wiring."),
        ("Give three reasons for using interposing relays.", "Isolation of the controller from 230 V circuits, higher contact rating, cheap and quick replacement, and a visible LED showing the command."),
        ("What does “potential-free contact” mean?", "The contact is only a switch and carries no voltage from its own panel; the receiving panel supplies the voltage. It keeps the two panels electrically independent."),
        ("List the signals usually exchanged between the BMS and a fan's MCC starter.", "Start/stop command (DO), run status (DI), trip/fault (DI), auto/manual status (DI), and a speed reference (AO) if a VFD is fitted."),
        ("Why should 230 V and 24 V signal wiring be kept apart?", "For safety, and because power cables induce electrical noise into signal cables, which makes analogue readings unstable."),
    ],
)

P6 = dict(
    id="1-6", slug="hvac-system-integration", title="HVAC system integration",
    objectives=[
        "Explain what integration means in a BMS.",
        "Compare hard-wired interfaces with high-level (protocol) interfaces.",
        "List the steps to integrate third-party equipment such as a chiller or VFD.",
        "Decide which signals should be hard-wired and which integrated over a protocol.",
    ],
    one_line=("Integration means connecting equipment that has <strong>its own controller</strong> — chillers, VFDs, energy "
              "meters, VRF systems — to the BMS, so it can be monitored and commanded alongside everything else."),
    why=("<p>Modern buildings are full of packaged equipment with built-in controls. One chiller can offer hundreds of "
         "values. Integration is how the BMS gets that information without hundreds of wires — and it is one of the "
         "most common, and most error-prone, jobs a BMS engineer does.</p>"),
    body=(
        "<h3>Two ways to connect</h3>"
        + fig(d_hardwired_vs_hli(), "Left: one pair of wires per signal. Right: one communication cable carrying many values.")
        + table(["", "Hard-wired", "High-level interface (HLI)"], [
            ("How", "One pair of wires per signal", "One communication cable carries many values"),
            ("Values available", "Few — limited by I/O count and cost", "Many — whatever the equipment publishes"),
            ("Reliability", "Very high; easy to test with a multimeter", "Depends on settings, addressing and the device's software"),
            ("Speed", "Immediate", "Values are polled — a few seconds' delay is normal"),
            ("Cost per value", "High", "Low"),
            ("Typical use", "Critical commands and status: enable, run, trip", "Detail: temperatures, kW, alarms, fault codes"),
        ])
        + "<h3>Common protocols</h3>"
        + table(["Protocol", "Where you will find it"], [
            ("BACnet (IP and MS/TP)", "The main open BMS protocol: controllers, chillers, VRF gateways. Module 5."),
            ("Modbus (RTU and TCP)", "VFDs, energy meters, generators, UPS, many chillers. Module 5."),
            ("M-Bus", "Heat (BTU) and water meters, especially in Europe."),
            ("KNX, DALI", "Lighting and room control."),
            ("LonWorks", "Older installations."),
            ("OPC UA, MQTT, web APIs", "Links to IT systems, analytics and cloud platforms."),
        ])
        + "<p>When two systems speak different protocols, a <strong>gateway</strong> (protocol converter) translates — for "
          "example from a VRF manufacturer's own protocol to BACnet/IP.</p>"
        + "<h3>The rule of thumb</h3>"
        + callout("tip", "Hard-wire what must work, integrate what you want to know",
                  "<p>Commands and status that the plant depends on — enable, start/stop, run status, common fault, fire "
                  "shutdown — are hard-wired. Detail — internal temperatures, kW, alarm codes, run-hours — comes over the "
                  "high-level interface. If communication fails, the plant still works and the BMS still knows whether it "
                  "is running.</p>")
        + "<h3>Integration step by step</h3>"
        + steps([
            "<strong>Get the documents</strong> — the device's register map (Modbus) or PICS and object list (BACnet), and the communication settings it supports.",
            "<strong>Agree the interface</strong> — an interface (responsibility) matrix lists which points are needed, read or write, and who supplies the cable, gateway and configuration.",
            "<strong>Set the communication parameters</strong> on both sides — protocol, address or device ID, baud rate, IP settings (Module 5).",
            "<strong>Connect and discover</strong> — wire the bus or network and check the BMS can see the device.",
            "<strong>Map the points</strong> — create a BMS point for each register or object, with the correct scaling and units.",
            "<strong>Test point to point</strong> — compare every value on the BMS with the device's own display, and test every write (change the setpoint, see it change on the chiller).",
            "<strong>Finish the front end</strong> — add the integrated points to graphics, alarms and trends.",
        ])
        + "<h3>Typical integrated equipment</h3>"
        + table(["Equipment", "Usually hard-wired", "Usually over the HLI"], [
            ("Chiller", "Enable, run status, common fault", "CHW supply/return temperatures, setpoint, load %, kW, alarms"),
            ("VFD", "Start/stop, run, fault, speed reference", "Frequency, current, kW, kWh, fault code"),
            ("Energy meter", "—", "kW, kWh, voltage, current, power factor"),
            ("Generator (DG)", "Running, fault", "Fuel level, voltage, load, run-hours"),
            ("VRF system", "—", "On/off, mode, setpoint and room temperature for each indoor unit (via gateway)"),
            ("Fire alarm panel", "Fire signal to AHU shutdown; fire status to BMS", "Zone status (in an integrated BMS)"),
        ])
    ),
    ahu01=("<p>AHU-01's VFD uses both methods. <strong>Hard-wired:</strong> start/stop (DO), run status and fault (DI), speed "
           "reference (AO). <strong>Modbus RTU:</strong> output frequency, motor current, kW, kWh and the last fault code. If "
           "the Modbus link fails, AHU-01 keeps running and the BMS still knows whether the fan is on.</p>"),
    on_site=[
        "Get the register map or object list for the <strong>exact model and firmware</strong> — tables change between versions.",
        "Check the scaling of every value: a Modbus register reading 2415 might mean 241.5 V or 24.15 Hz.",
        "Test writes carefully on live plant. Changing a chiller setpoint or a VFD parameter has real effects.",
        "Keep a table of every integrated device: address or device ID, baud rate, parity, IP address.",
        "Agree in writing who configures the third-party side. Many integration delays are spent waiting for another vendor's engineer.",
    ],
    faults=[
        ("Device not found on the network", "Wrong address, baud rate or parity, or wiring fault", "Settings on both sides, A/B polarity, termination"),
        ("All values read 0 or nonsense", "Wrong register addresses (often off by one) or wrong data type", "Register map, address base (0 or 1), data type"),
        ("Values 10× or 100× too big or small", "Scaling factor missing", "Units and scale in the register map"),
        ("Values update slowly", "Too many points on a slow bus", "Poll rate, number of points, baud rate"),
        ("Writes have no effect", "Point is read-only, device is in local mode, or needs a remote-enable", "Register map; device's local/remote setting"),
    ],
    terms=[
        ("Integration", "Connecting equipment that has its own controller to the BMS."),
        ("HLI", "High-level interface: a data link that carries many values over one protocol connection."),
        ("Gateway", "A device that translates between two protocols."),
        ("Register map", "A Modbus device's list of registers, their meaning, data type and scaling."),
        ("PICS", "A BACnet device's statement of which BACnet features it supports."),
        ("Interface matrix", "A table agreeing which points are exchanged and who is responsible for each part."),
        ("Point-to-point test", "Checking every value and command end to end, from device to BMS screen."),
        ("Polling", "The BMS asking each device for its values in turn."),
        ("Scaling", "Converting a raw value into engineering units, e.g. 70 → 7.0 °C."),
    ],
    scenarios=[dict(
        prompt="A chiller is integrated over Modbus. The BMS shows the chilled water supply temperature as 70 °C, while the chiller's own display shows 7.0 °C. What is wrong?",
        options=["The chiller's sensor is faulty.", "The scaling factor (× 0.1) is missing in the BMS point.",
                 "The baud rate is set incorrectly."],
        answer=1,
        explain=(" The value is exactly ten times too large and otherwise correct, so communication is fine. The register holds "
                 "tenths of a degree; apply a scale of 0.1 to the BMS point. A baud-rate error would stop communication completely."),
    )],
    questions=[
        ("What is the difference between a hard-wired interface and a high-level interface?",
         "Hard-wired uses one pair of wires per signal — few values, very reliable. A high-level interface uses one communication cable and a protocol to carry many values — cheap per value, but it depends on communication settings and software."),
        ("Which AHU-01 VFD signals are hard-wired, and why?", "Start/stop, run status, fault and speed reference — so the fan can be controlled and monitored even if the Modbus link fails."),
        ("What is a gateway used for?", "To translate between two different protocols, e.g. a manufacturer's own protocol to BACnet/IP."),
        ("List the seven steps of integrating a device.", "Get documents → agree the interface → set communication parameters → connect and discover → map points → point-to-point test → graphics, alarms and trends."),
        ("Why must you be careful when testing writes on live plant?", "Writing a setpoint or parameter changes how real equipment runs; a mistake can trip plant or affect occupants."),
    ],
)

MODULE_INTRO = (
    "<p>This module gives you the big picture before the detail. By the end you will be able to sketch a BMS from "
    "the sensors up to the operator's screen, explain what a DDC controller does on every scan, and describe what is "
    "inside a control panel.</p>"
)

PAGES = [P1, P2, P3, P4, P5, P6]
