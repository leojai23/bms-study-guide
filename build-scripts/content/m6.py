# -*- coding: utf-8 -*-
"""Module 6 — BMS Control Logic. Vendor-neutral. Numbers for AHU-01 are example settings for a typical office AHU;
real projects take theirs from the approved sequence of operation."""
from bms_common import (table, steps, bullets, callout, cards, fig, svg, defs, t, rect, box,
                        line, path, circle, mcq, tool)

# ==========================================================================
# Diagrams
# ==========================================================================

def d_start_timeline():
    i = defs("tl")
    x0, x1 = 170, 740
    X = lambda s: x0 + s / 120 * (x1 - x0)
    rows = [("Schedule", [(0, 120, "Occupied")]), ("Fresh air damper", [(0, 120, "20 % min")]),
            ("Fan start (DO)", [(5, 120, "ON")]), ("Run status (DI)", [(13, 120, "proven")]),
            ("Cooling PID", [(73, 120, "enabled")]), ("Temp alarms", [])]
    for k, (name, bars) in enumerate(rows):
        y = 30 + k * 34
        i += t(x0 - 12, y + 10, name, "d-ts d-tb", "end") + line(x0, y + 22, x1, y + 22, "d-line d-thin")
        for a, b, lab in bars:
            i += rect(X(a), y, X(b) - X(a), 20, "d-acc" if k != 3 else "d-ok", 4) + t(X(a) + 6, y + 10, lab, "d-ts", "start")
    i += t(X(120) - 4, 30 + 5 * 34 + 10, "armed after 15 min →", "d-ts", "end")
    for s in (0, 30, 60, 90, 120):
        i += t(X(s), 282, f"{s} s", "d-ts")
    i += path(f"M{X(5)},244 L{X(13)},244", "d-line", end="tl", start="tl") + t(X(5), 258, "proven within 30 s", "d-ts d-ta", "start")
    i += path(f"M{X(13)},236 L{X(73)},236", "d-line", end="tl", start="tl") + t((X(13) + X(73)) / 2 + 40, 248, "60 s stabilise", "d-ts d-ta")
    return svg(760, 292, i, "Timing of AHU-01's start sequence")


def d_safety_chain():
    i = defs("sc")
    i += line(40, 40, 40, 240, "d-warmline") + t(40, 26, "control supply", "d-ts d-tb")
    i += line(720, 40, 720, 240, "d-line") + t(720, 26, "return", "d-ts d-tb")
    y = 100
    parts = [(70, "Fire relay", "closed = healthy"), (190, "High pressure", "cut-out (NC)"), (310, "Overload / VFD", "healthy (NC)")]
    i += line(40, y, 70, y)
    for x, a, b in parts:
        i += line(x, y, x + 15, y) + rect(x + 15, y - 12, 40, 24, "d-box", 4) + t(x + 35, y, "NC", "d-ts d-tb")
        i += line(x + 55, y, x + 120, y)
        i += t(x + 35, y + 22, a, "d-ts d-tb") + t(x + 35, y + 36, b, "d-ts")
    i += line(430, y, 470, y)
    i += box(470, 70, 110, 60, "HOA switch", "Hand · Off · Auto", "d-warn")
    i += path(f"M580,85 L640,85 L640,{y}", "d-line") + t(600, 76, "Hand", "d-ts", "start")
    i += path(f"M525,130 L525,180 L560,180", "d-line") + t(530, 152, "Auto", "d-ts", "start")
    i += box(560, 160, 90, 40, "BMS relay", "start DO", "d-acc", "d-ts d-tb")
    i += path(f"M650,180 L660,180 L660,{y}", "d-line")
    i += line(640, y, 668, y) + box(668, 80, 40, 40, "K", "", "d-box", "d-t d-tb", 4) + line(708, y, 720, y)
    i += t(688, 64, "contactor / VFD run", "d-ts")
    i += t(380, 230, "Safeties sit BEFORE the HOA switch, so they stop the fan in Hand as well as in Auto", "d-ts d-tb d-ta")
    return svg(760, 250, i, "Hard-wired safety chain in a fan starter circuit")


def d_pid_block():
    i = defs("pb")
    i += box(20, 70, 90, 46, "Setpoint", "24 °C", "d-box")
    i += circle(160, 93, 18, "d-acc") + t(160, 93, "Σ", "d-t d-tb") + t(150, 70, "+", "d-t d-tb") + t(176, 124, "−", "d-t d-tb")
    i += line(110, 93, 140, 93, "d-line", end="pb")
    i += line(178, 93, 220, 93, "d-line", end="pb") + t(199, 82, "error", "d-ts")
    for k, (a, b) in enumerate((("P", "× gain"), ("I", "∫ error · dt"), ("D", "d(PV)/dt"))):
        y = 30 + k * 50
        i += path(f"M220,93 L240,93 L240,{y + 20} L262,{y + 20}", "d-line", end="pb")
        i += box(262, y, 100, 40, a, b, "d-acc", "d-t d-tb", 6)
        i += path(f"M362,{y + 20} L390,{y + 20} L390,93 L402,93", "d-line")
    i += circle(420, 93, 18, "d-acc") + t(420, 93, "Σ", "d-t d-tb")
    i += line(438, 93, 480, 93, "d-line", end="pb") + t(459, 82, "output", "d-ts")
    i += box(480, 70, 110, 46, "Valve + coil", "the process", "d-box")
    i += line(590, 93, 640, 93, "d-line", end="pb")
    i += box(640, 70, 100, 46, "Return air", "measured (PV)", "d-box")
    i += path("M690,116 L690,190 L160,190 L160,113", "d-line d-dash", end="pb") + t(420, 204, "feedback", "d-ts")
    return svg(760, 215, i, "Block diagram of a PID control loop")


def d_split_range():
    i = ""
    x0, x1, y0, y1 = 80, 700, 190, 30
    X = lambda v: x0 + v / 100 * (x1 - x0)
    Y = lambda v: y0 - v / 100 * (y0 - y1)
    i += line(x0, y0, x1, y0) + line(x0, y0, x0, y1)
    for v in (0, 25, 50, 75, 100):
        i += t(X(v), y0 + 16, f"{v} %", "d-ts")
    i += t((x0 + x1) / 2, y0 + 34, "PID output", "d-ts d-tb")
    i += t(x0 - 8, Y(100), "100 %", "d-ts", "end") + t(x0 - 8, Y(0), "0 %", "d-ts", "end")
    i += path(f"M{X(0)},{Y(100)} L{X(45)},{Y(0)}", "d-warmline") + t(X(24), Y(82), "heating valve", "d-ts d-tbad")
    i += path(f"M{X(55)},{Y(0)} L{X(100)},{Y(100)}", "d-aline") + t(X(70), Y(72), "cooling valve", "d-ts d-ta")
    i += rect(X(45), y1, X(55) - X(45), y0 - y1, "d-soft", 0) + t(X(50), Y(50), "dead-", "d-ts") + t(X(50), Y(42), "band", "d-ts")
    return svg(760, 235, i, "Split-range control of heating and cooling from one PID output")


def d_ahu01_loops():
    i = defs("lo")
    rows = [("Return air temp (AI)", "PID · SP 24 °C", "CHW valve (AO)", "d-acc"),
            ("Supply air temp (AI)", "low-limit PID · 11 °C", "→ min select with the line above", "d-warn"),
            ("Return CO₂ (AI)", "DCV ramp 700–1,000 ppm", "Fresh air damper (AO) 20–50 %", "d-ok"),
            ("Speed setpoint 42 Hz", "fixed (CAV)", "VFD speed (AO)", "d-soft")]
    for k, (a, b, c, cls) in enumerate(rows):
        y = 20 + k * 56
        i += box(20, y, 190, 40, a, "", "d-box", "d-ts d-tb", 6)
        i += box(280, y, 200, 40, b, "", cls, "d-ts d-tb", 6)
        i += box(550, y, 200, 40, c, "", "d-box", "d-ts d-tb", 6)
        i += line(210, y + 20, 278, y + 20, "d-line", end="lo") + line(480, y + 20, 548, y + 20, "d-line", end="lo")
    return svg(760, 245, i, "AHU-01's control loops")


def d_alarm_timing():
    i = defs("at")
    x0, x1, y0, y1 = 70, 720, 170, 30
    X = lambda m: x0 + m / 80 * (x1 - x0)
    Y = lambda v: y0 - (v - 23) / 6 * (y0 - y1)
    pts = [(0, 25.5), (10, 27.0), (14, 27.6), (30, 28.0), (45, 27.4), (55, 26.6), (60, 25.9), (70, 25.4), (80, 25.2)]
    i += line(x0, y0, x1, y0) + line(x0, y0, x0, y1)
    i += line(x0, Y(27), x1, Y(27), "d-warmline d-dash") + t(x1, Y(27) - 8, "limit 27 °C", "d-ts d-tbad", "end")
    i += line(x0, Y(26), x1, Y(26), "d-line d-dash d-thin") + t(X(40), Y(24.4), "grey dashed line: the alarm clears below 26 °C (1 K deadband)", "d-ts")
    i += f'<polyline points="{" ".join(f"{X(m):.1f},{Y(v):.1f}" for m, v in pts)}" class="d-aline"/>'
    i += rect(X(25), 186, X(59) - X(25), 18, "d-bad", 4) + t((X(25) + X(59)) / 2, 195, "ALARM", "d-ts d-tb d-tbad")
    i += path(f"M{X(10)},214 L{X(25)},214", "d-line", end="at", start="at") + t((X(10) + X(25)) / 2, 226, "15 min delay", "d-ts")
    for m in (0, 20, 40, 60, 80):
        i += t(X(m), 244, f"{m} min", "d-ts")
    for v in (24, 26, 28):
        i += t(x0 - 8, Y(v), f"{v} °C", "d-ts", "end")
    return svg(760, 255, i, "High return air temperature alarm with delay and deadband")


def d_schedule():
    i = ""
    x0, x1 = 90, 740
    X = lambda h: x0 + h / 24 * (x1 - x0)
    days = [("Mon", (8, 19)), ("Tue", (8, 19)), ("Wed", (8, 19)), ("Thu", (8, 19)), ("Fri", (8, 19)), ("Sat", (8, 19)), ("Sun", None)]
    for k, (d, occ) in enumerate(days):
        y = 30 + k * 26
        i += t(x0 - 10, y + 9, d, "d-ts d-tb", "end") + rect(x0, y, x1 - x0, 18, "d-soft", 3)
        if occ:
            i += rect(X(occ[0]), y, X(occ[1]) - X(occ[0]), 18, "d-acc", 3)
            if k == 0:
                i += rect(X(6.5), y, X(8) - X(6.5), 18, "d-warn", 3) + t(X(6.5) - 4, y + 9, "optimum start", "d-ts", "end")
    y = 30 + 3 * 26
    i += rect(X(19), y, X(21) - X(19), 18, "d-ok", 3) + t(X(21) + 6, y + 9, "override 2 h", "d-ts", "start")
    for h in (0, 6, 8, 12, 19, 24):
        i += t(X(h), 228, f"{h:02d}:00", "d-ts")
    i += t(X(13.5), 30 + 6 * 26 + 9, "unoccupied (holiday calendar can make any day like this)", "d-ts")
    return svg(760, 240, i, "AHU-01 weekly schedule with optimum start and an after-hours override")


def d_timers():
    i = ""
    x0, x1 = 150, 740
    X = lambda s: x0 + s / 100 * (x1 - x0)
    rows = [("Input", [(10, 60)]), ("On-delay (10 s)", [(20, 60)]), ("Off-delay (15 s)", [(10, 75)]), ("Min on 30 s", [(10, 60)])]
    for k, (name, bars) in enumerate(rows):
        y = 26 + k * 38
        i += t(x0 - 10, y + 10, name, "d-ts d-tb", "end") + line(x0, y + 20, x1, y + 20, "d-line d-thin")
        for a, b in bars:
            i += rect(X(a), y, X(b) - X(a), 20, "d-acc" if k else "d-box", 3)
    i += t(X(85), 26 + 3 * 38 + 10, "(input held ≥ 30 s here)", "d-ts")
    for s in range(0, 101, 20):
        i += t(X(s), 186, f"{s} s", "d-ts")
    return svg(760, 200, i, "Timer behaviour: on-delay, off-delay and minimum on time")


# ==========================================================================
# Pages
# ==========================================================================

P1 = dict(
    id="6-1", slug="ahu-start-stop-sequence", title="AHU start/stop sequence",
    objectives=[
        "Explain each step of AHU-01's start and stop sequence and why it is there.",
        "Define enable conditions, proving, stabilising delays and lockout.",
        "Handle power return, minimum off times and after-hours requests.",
        "Test a start/stop sequence step by step, including its failure paths.",
    ],
    one_line=("A start/stop sequence starts plant <strong>in a safe order, proves each step, and stops it cleanly</strong> — with a "
              "defined response when anything fails along the way."),
    why=("<p>Starting a fan against a closed damper, opening a valve with no airflow, or restarting forty AHUs at once after a "
         "power cut all cause real damage or trips. A good sequence prevents them, and the failure paths in it are what turn a "
         "silent fault into a clear alarm. This is the logic you will write and test in Lab 3.</p>"),
    body=(
        "<h3>Enable conditions (permissives)</h3>"
        + "<p>AHU-01 may start only when <strong>all</strong> of these are true:</p>"
        + table(["Condition", "Point", "If false"], [
            ("Schedule says Occupied, or a timed override is active", "Schedule / override (software)", "Stay off"),
            ("HOA switch in Auto", "Auto status DI", "Stay off; “not in Auto” alarm if the schedule wants it running"),
            ("No fire signal", "Fire DI (fail-safe)", "Stay off; critical alarm"),
            ("No latched fan failure", "Software flag", "Stay off until an operator resets it"),
            ("Minimum off time has passed (3 min)", "Timer", "Wait, to avoid short-cycling"),
        ])
        + "<h3>The start sequence</h3>"
        + fig(d_start_timeline(), "AHU-01 start: each step waits for the one before it.")
        + steps([
            "<strong>Open the fresh air damper to minimum (20 %).</strong> A fan should not start against a closed intake.",
            "<strong>Start the fan.</strong> DO on (via the interposing relay); the VFD ramps to its 42 Hz speed setpoint over about 30 s.",
            "<strong>Prove it.</strong> Run status must arrive within <strong>30 s</strong>. If not: “fan fail” alarm, command off, damper closed, lock out until reset.",
            "<strong>Stabilise (60 s).</strong> The valve stays at 0 % while airflow settles — PID loops started too early react to start-up transients.",
            "<strong>Enable control.</strong> Start the RAT PID loop (bumpless, from 0 %), and CO₂ control of the damper.",
            "<strong>Arm the temperature alarms after 15 min</strong>, so the morning pull-down does not raise high-temperature alarms.",
        ])
        + "<h3>The stop sequence</h3>"
        + steps([
            "Disable the PID loop and drive the CHW valve to 0 % — a cold coil without airflow sweats and drips.",
            "Command the fan off. Run status must clear within 60 s, or raise “fan failed to stop” (welded contactor, drive in Hand).",
            "Close the fresh air damper (spring-return closes it anyway on power loss).",
            "Start the minimum off timer.",
        ])
        + tool("ahuseq")
        + "<h3>The less obvious parts</h3>"
        + table(["Situation", "What the sequence does"], [
            ("Power returns after an outage", "Wait a staggered delay (AHU-01: 60 s; each later AHU 20 s more) before re-evaluating the enable conditions, so the generator or supply is not overloaded"),
            ("After-hours request", "Timed override for 2 h from a BMS command or a local button; logged for tenant billing"),
            ("Fan fails while running", "Status lost for > 10 s → fan fail alarm, stop, lock out — the same path as failing to start"),
            ("Return air sensor fails", "Sensor-fault alarm; valve to a fixed safe position (e.g. 50 %) instead of following a bad value"),
            ("Controller loses the server", "Nothing changes — the sequence runs in the controller"),
        ])
    ),
    ahu01=("<p>This page <em>is</em> AHU-01's sequence. Use the stepper above: tick “fan fails to prove” and step through, then reset "
           "and try “fire” halfway through the day. Notice that in both cases the plant ends in a safe, alarmed, locked-out state — "
           "the goal of every failure path.</p>"),
    on_site=[
        "Test the sequence with real failures, not only simulated points: open the status contact, put the HOA in Hand, operate the fire relay.",
        "Time the proving and stabilising delays with a stopwatch against the specification.",
        "After a power-return test, check every AHU restarted — and in the planned order.",
        "Write the as-left delays and setpoints into the commissioning record.",
    ],
    faults=[
        ("Nuisance “fan fail” on every start", "Proving delay shorter than the VFD's ramp-up time", "Proving delay vs ramp time"),
        ("Valve opens before airflow is established", "No stabilising delay or PID enabled with the start command", "Enable condition of the PID loop"),
        ("AHU starts and stops every few minutes", "No minimum off/on time; schedule and override fighting", "Timers; override list"),
        ("All AHUs restart together after a power cut", "No staggered restart", "Power-return logic"),
        ("High-temperature alarms every morning", "Alarm armed immediately at start", "Alarm enable delay"),
    ],
    terms=[
        ("Permissive", "Condition that must be true before plant may start."),
        ("Proving delay", "Maximum time allowed for status to confirm a command."),
        ("Stabilising delay", "Wait after start before enabling control loops."),
        ("Lockout", "State after a failure where plant stays off until reset."),
        ("Bumpless transfer", "Starting or switching a loop without a sudden jump in output."),
        ("Minimum off time", "Shortest time plant must stay off before restarting (anti-short-cycle)."),
        ("Staggered restart", "Restarting plant items one after another after a power return."),
        ("Timed override", "Temporary occupied mode, e.g. 2 h after hours."),
    ],
    scenarios=[dict(
        prompt="Every morning AHU-01 raises “fan fail” and locks out, but restarts fine when reset. The VFD ramp-up time was recently changed to 45 s. What is wrong?",
        options=["The fan motor is failing.", "The 30 s proving delay is shorter than the new 45 s ramp, so status arrives too late.",
                 "The schedule is wrong."],
        answer=1,
        explain=(" Depending on how the drive's run relay is set, status may only appear near full speed. Set the proving delay longer "
                 "than the ramp (e.g. 60 s), or use a relay function that closes as soon as the drive runs."),
    )],
    questions=[
        ("Why is the fresh air damper opened before the fan starts?", "So the fan does not start against a closed intake, which can over-pressurise or collapse ductwork and stress the fan."),
        ("What happens if run status is not received within the proving delay?", "“Fan fail” alarm, start command off, damper closed, and the AHU locks out until an operator resets it."),
        ("Why wait 60 s before enabling the PID loop?", "To let airflow and readings settle; a loop enabled during start-up transients overreacts."),
        ("Why close the CHW valve when the fan stops?", "A cold coil without airflow cools the casing and condenses water — sweating, dripping and wasted chilled water."),
        ("What is a staggered restart?", "Restarting plant items one after another after power returns, so their starting currents do not overload the supply or generator."),
    ],
)

P2 = dict(
    id="6-2", slug="fan-interlocks-and-safeties", title="Fan interlocking and safeties",
    objectives=[
        "Distinguish safety interlocks from control (software) interlocks.",
        "Explain why safeties are hard-wired and where they sit in the starter circuit.",
        "List the common interlocks around AHUs and fans, including the fire alarm interface.",
        "Test interlocks properly and handle resets.",
    ],
    one_line=("Interlocks make one thing depend on another; <strong>safety interlocks</strong> are hard-wired so they stop plant even "
              "if the BMS, its program or its network fails — and even when the plant is in Hand."),
    why=("<p>Interlocks protect people, ductwork and equipment. A fire signal that only reaches the BMS program is not a safety "
         "function — software can crash, be overridden, or be bypassed by a switch in Hand. Knowing which interlocks must be "
         "hard-wired, and where they go, is a basic responsibility of a BMS engineer.</p>"),
    body=(
        "<h3>Two kinds of interlock</h3>"
        + table(["", "Safety interlock", "Control interlock"], [
            ("Purpose", "Protect people and equipment", "Make the plant run in the right order"),
            ("Implemented", "Hard-wired in the starter or control circuit (plus monitored by the BMS)", "In the controller program"),
            ("Works when the BMS fails?", "Yes", "No"),
            ("Works in Hand?", "Yes — wired before the HOA switch", "No"),
            ("Examples", "Fire shutdown, high static pressure cut-out, overloads, heater airflow and overheat protection", "Valve closed when fan off; return fan follows supply fan; damper open before fan start"),
        ], "plain")
        + fig(d_safety_chain(), "Every safety contact is closed when healthy and in series. Any one opening stops the fan — in Auto or in Hand.")
        + "<h3>Common interlocks around an AHU</h3>"
        + table(["Interlock", "Type", "What it does"], [
            ("Fire alarm shutdown", "Safety, hard-wired", "Fire signal opens the starter circuit; BMS DI monitors it"),
            ("Duct smoke detector", "Safety, via the fire system", "Detects smoke in the duct; fire system shuts the AHU"),
            ("High static pressure cut-out", "Safety, hard-wired, manual reset", "Stops the fan if dampers close and duct pressure becomes dangerous"),
            ("Motor overload / VFD fault", "Safety, hard-wired", "Protects the motor; BMS reads the fault DI"),
            ("Access door switch", "Safety (optional)", "Stops the fan when a fan-section door opens"),
            ("Electric heater: airflow proven + overheat cut-out", "Safety, hard-wired", "Heater only with proven airflow; thermal cut-out with manual reset"),
            ("Isolation damper end switch before fan start", "Control (sometimes also hard-wired)", "Fan waits until the damper is proven open"),
            ("Return fan follows supply fan", "Control", "Return fan only runs with the supply fan proven"),
            ("Kitchen exhaust and make-up air", "Control", "Make-up air fan runs whenever the exhaust runs"),
            ("CHW valve closed when fan off", "Control", "Prevents a sweating coil"),
        ])
        + "<h3>The fire alarm interface</h3>"
        + bullets([
            "The <strong>fire strategy</strong> (a fire engineer's document) says what each fan does in a fire: stop, or — for smoke-extract and stair-pressurisation fans — run. The BMS follows it; it does not decide it.",
            "The fire system's relay contact is wired <strong>fail-safe</strong> (closed when healthy) into the starter circuit <strong>upstream of the HOA switch</strong>.",
            "A second contact goes to a BMS DI so the BMS shows <em>Fire shutdown</em>, closes valves and dampers, and raises a critical alarm.",
            "Fans that must <em>run</em> in fire mode are controlled by the fire system with priority over the BMS — never the other way round.",
        ])
        + "<h3>Resets</h3>"
        + "<p>Safety trips usually <strong>latch</strong>: plant stays off until a person resets it after finding the cause — a manual "
          "reset button on a pressure cut-out, an operator reset on the BMS after a fan failure. Automatic restart is reserved for "
          "conditions where restarting is clearly safe, such as power returning.</p>"
        + callout("warn", "Never bypass a safety to “get it running”",
                  "<p>Links across fire contacts or pressure cut-outs, left in “temporarily”, remove protection permanently and "
                  "invisibly. If a safety stops the plant, find out why.</p>")
        + "<h3>Testing interlocks</h3>"
        + steps([
            "Test each interlock by <strong>operating the real device</strong> — the fire relay, the pressure switch, the overload trip — not just by forcing a BMS point.",
            "Test in <strong>Auto and in Hand</strong>: safeties must stop the fan in both.",
            "Check the <strong>BMS indication</strong> and alarm for each trip.",
            "Check the <strong>reset</strong>: the plant must not restart until reset, and must restart correctly after it.",
            "Record each test — fire interface tests are usually witnessed.",
        ])
    ),
    ahu01=("<p>AHU-01's starter circuit has, in series and before the HOA switch: the <strong>fire interface relay</strong> (closed when "
           "healthy), a <strong>high static pressure cut-out</strong> on the supply duct (manual reset), and the <strong>VFD's healthy "
           "contact</strong>. The BMS monitors the fire signal, the VFD fault and the auto/manual status on DIs. Software interlocks: "
           "valve closed and damper closed whenever the fan is not proven.</p>"),
    on_site=[
        "Trace the fire interface wiring yourself — check it sits upstream of the HOA switch.",
        "Look for links or jumpers across safety terminals; report any you find.",
        "Find out the fire strategy for every fan before writing fire-mode logic.",
        "After a fire alarm test, check every AHU stopped — and restarted afterwards as specified.",
    ],
    faults=[
        ("Fan keeps running in Hand during a fire test", "Fire contact wired after the HOA switch (or only into the BMS)", "Starter wiring; rewire upstream of HOA"),
        ("AHU won't start, no BMS alarm", "Pressure cut-out tripped (manual reset) and not monitored", "Cut-out; add a monitoring DI"),
        ("Return fan runs alone after the supply fan trips", "Missing software interlock", "Program logic"),
        ("Fire shutdown shows during normal operation", "NC fire loop open: wiring, link or interface module", "Interface terminals"),
    ],
    terms=[
        ("Interlock", "A condition that permits or prevents operation of plant."),
        ("Safety interlock", "Hard-wired interlock protecting people or equipment, independent of the BMS."),
        ("Control interlock", "Program logic that sequences plant correctly."),
        ("Fire strategy", "Fire engineer's document defining what each system does in a fire."),
        ("High static pressure cut-out", "Pressure switch that stops a fan before ducts are damaged; usually manual reset."),
        ("Latching", "Staying in the tripped state until reset."),
        ("Upstream of the HOA", "Wired so the device acts in Hand as well as Auto."),
    ],
    scenarios=[dict(
        prompt="During a witnessed fire alarm test, AHU-03 stops in Auto, but when the technician switches its HOA to Hand, the fan restarts while the fire alarm is still active. What is wrong?",
        options=["Nothing — Hand is meant to override everything.", "The fire contact is wired after the HOA switch (or only to the BMS), so Hand bypasses it.",
                 "The BMS program has a bug."],
        answer=1,
        explain=(" Safety contacts must be in series upstream of the HOA switch so they act in every mode. Rewire it and repeat the test."),
    )],
    questions=[
        ("Why must a fire shutdown be hard-wired?", "So it works even if the BMS, its program or network fails, and cannot be overridden by software or bypassed by Hand mode."),
        ("Where in the starter circuit do safety contacts go?", "In series, upstream of the HOA switch, so they stop the fan in Hand and Auto."),
        ("Give two control (software) interlocks for an AHU.", "Any two of: valve closed when fan off; return fan follows supply fan; damper proven open before fan start; make-up air with exhaust."),
        ("Who decides what each fan does in a fire?", "The fire strategy, written by the fire engineer; the BMS follows it."),
        ("Why are most safety trips latching?", "So plant stays off until a person has found and fixed the cause, rather than cycling on and off into a fault."),
    ],
)

P3 = dict(
    id="6-3", slug="pid-control-basics", title="PID control basics",
    objectives=[
        "Explain error, action and output of a control loop.",
        "Describe what P, I and D each do, including offset and integral windup.",
        "Recognise hunting, sluggish response, offset and overshoot on a trend.",
        "Tune a simple HVAC loop by a safe, step-by-step method.",
    ],
    one_line=("A PID loop sets its output from the <strong>error</strong> (setpoint − measured value): <strong>P</strong> reacts to how "
              "big the error is, <strong>I</strong> to how long it has lasted, <strong>D</strong> to how fast it is changing."),
    why=("<p>Nearly every modulating output in a BMS — valves, dampers, fan speeds — is driven by a PID loop. A badly tuned loop "
         "wears out actuators, wastes energy and causes comfort complaints that look like equipment faults. You do not need "
         "the maths to tune well; you need to know what each term does and what a good response looks like.</p>"),
    body=(
        fig(d_pid_block(), "The controller compares the setpoint with the measured value and adds three responses to the error.")
        + "<h3>Error and action</h3>"
        + "<p><strong>Error</strong> is the difference between setpoint and process variable. The <strong>action</strong> decides "
          "which way the output moves: a cooling valve must open <em>more</em> as the temperature rises above setpoint; a heating "
          "valve must open more as it falls below. Many products call these <em>direct</em> and <em>reverse</em> acting — but "
          "the naming is not consistent between manufacturers, so check the help and test it: if the loop drives the wrong "
          "way, the output runs straight to one end.</p>"
        + "<h3>P — proportional</h3>"
        + "<p>The output is proportional to the error. It is often set as a <strong>proportional band</strong> (PB): the error "
          "that moves the output across its whole range. A PB of 4 K means each 1 K of error moves the valve 25 %. "
          "(Gain = 100 % ÷ PB.)</p>"
        + callout("note", "Why P alone leaves an offset",
                  "<p>To hold the valve at, say, 60 %, a P-only controller needs an error — 2.4 K with a 4 K band. So the "
                  "temperature settles <em>away</em> from setpoint. That steady error is the <strong>offset</strong>. A narrower "
                  "band shrinks it, but too narrow and the loop oscillates.</p>")
        + "<h3>I — integral</h3>"
        + "<p>Integral action keeps adding to the output for as long as any error remains, so it slowly pushes the error to "
          "zero and removes the offset. It is set as an <strong>integral time</strong> (Ti): shorter means faster — and more "
          "likely to overshoot.</p>"
        + callout("warn", "Integral windup",
                  "<p>If the output is stuck at a limit — valve at 100 % because the chilled water is too warm — the integral keeps "
                  "growing. When conditions recover, the oversized integral holds the valve fully open long after it should close, "
                  "causing a big overshoot. Controllers use <strong>anti-windup</strong> to stop integrating at the limits; loops "
                  "should also be held at a sensible value while disabled (e.g. fan off) so they start smoothly.</p>")
        + "<h3>D — derivative</h3>"
        + "<p>Derivative reacts to how fast the measured value is changing, braking the output before the error gets large. It "
          "also amplifies noise. HVAC processes are slow and sensor signals noisy, so <strong>most HVAC loops use PI only "
          "(D = 0)</strong>.</p>"
        + tool("pid")
        + "<h3>Reading the response</h3>"
        + table(["What the trend shows", "Diagnosis", "Change"], [
            ("Value swings above and below setpoint continuously; output saw-tooths", "Hunting — too aggressive", "Wider PB (less gain) and/or longer Ti"),
            ("Value settles but never reaches setpoint", "Offset — no or too little integral", "Add integral / shorten Ti"),
            ("Value takes a very long time to reach setpoint", "Sluggish", "Narrower PB and/or shorter Ti"),
            ("Big overshoot after the output was at a limit", "Integral windup", "Enable anti-windup; check the limit cause"),
            ("Output jumps around with a noisy sensor", "Noise amplified — D too high or PB too narrow", "Remove D; filter the input"),
        ])
        + "<h3>A safe way to tune an HVAC loop</h3>"
        + steps([
            "Make sure the loop is otherwise healthy: correct action, sensor reading correctly, actuator moving its full stroke, valve correctly sized.",
            "Start with <strong>P only</strong>, a wide band and no integral.",
            "Make a setpoint change and watch the trend. Narrow the band step by step until the response starts to oscillate, then widen it to about double that value.",
            "Add <strong>integral</strong> with a long Ti, then shorten it until the offset disappears in reasonable time without a large overshoot.",
            "Test at low and high load if you can — a loop tuned at full load can hunt at light load.",
            "Record the as-left settings.",
        ])
        + table(["Loop", "Typical speed"], [
            ("Duct static pressure → fan speed", "Fast — seconds"),
            ("Supply air temperature → valve", "Medium — about a minute"),
            ("Return air or room temperature → valve", "Slow — several minutes"),
            ("Chilled water ΔP → pump speed", "Fast — seconds"),
        ], "plain")
    ),
    ahu01=("<p>AHU-01's return air loop is PI: proportional band <strong>4 K</strong>, integral time <strong>240 s</strong>, no "
           "derivative, output limited to 0–100 % with anti-windup, held at 0 % while the fan is off. Try those values in the "
           "playground above — they are the “P + I (good)” preset — then try the aggressive and sluggish presets to see what "
           "badly tuned loops look like.</p>"),
    on_site=[
        "Always tune from a trend, not from a single reading.",
        "Before touching PID settings, check the valve really moves: many “tuning problems” are mechanical.",
        "Change one setting at a time and give the loop time to respond.",
        "Note the original settings before changing them.",
    ],
    faults=[
        ("Valve swings 0–100 % every few minutes", "Gain too high or Ti too short; oversized valve", "PB and Ti; valve sizing"),
        ("Temperature always 1–2 K above setpoint", "P-only loop (offset)", "Add integral action"),
        ("Output runs straight to 0 % or 100 % and stays", "Wrong action, or sensor fault", "Action setting; sensor reading"),
        ("Huge overshoot after chilled water recovers", "Integral windup", "Anti-windup; loop hold"),
        ("Loop fine at full load, hunts at light load", "Non-linear valve/coil or oversized valve", "Equal-% valve, PICV, gain scheduling"),
    ],
    terms=[
        ("Error", "Difference between setpoint and measured value."),
        ("Action", "Direction in which the output moves for a given error (direct / reverse)."),
        ("Proportional band", "Error needed to move the output across its full range; gain = 100 % ÷ PB."),
        ("Offset", "Steady error left by P-only control."),
        ("Integral time (Ti)", "Setting of integral action; shorter is faster."),
        ("Windup", "Integral building up while the output is at a limit, causing overshoot."),
        ("Derivative", "Action based on the rate of change; rarely used in HVAC."),
        ("Hunting", "Continuous oscillation around setpoint."),
        ("Overshoot", "Going past the setpoint before settling."),
    ],
    scenarios=[dict(
        prompt="A new supply air temperature loop drives the CHW valve straight to 0 % at start-up and leaves it there, while the supply air is 20 °C against a 13 °C setpoint. What is the most likely cause?",
        options=["The proportional band is too wide.", "The loop's action is the wrong way round — it closes the valve when it is too warm.",
                 "The integral time is too long."],
        answer=1,
        explain=(" Tuning makes a loop fast or slow; it does not make it go the wrong way. An output that runs to the wrong end and stays "
                 "there is almost always the action setting (or the actuator's direction)."),
    )],
    questions=[
        ("A loop has a 5 K proportional band. How far does the output move for a 1 K error?", "20 % (100 % ÷ 5 K)."),
        ("Why does P-only control leave an offset?", "It needs an error to produce any output; to hold a non-zero output it must settle with a steady error."),
        ("What does integral action do?", "Keeps adding to the output while any error remains, so it removes the offset over time."),
        ("What is integral windup?", "The integral growing while the output is stuck at a limit, so the loop overshoots badly when conditions recover."),
        ("Why is derivative rarely used in HVAC loops?", "HVAC processes are slow and sensors noisy; derivative amplifies noise and adds little benefit."),
    ],
)

P4 = dict(
    id="6-4", slug="valve-and-damper-control", title="Temperature-based valve control and damper control",
    objectives=[
        "Describe AHU-01's control loops and how they combine.",
        "Explain cascade control and supply air temperature reset.",
        "Use split-range control with a deadband to avoid simultaneous heating and cooling.",
        "Control dampers: minimum position, DCV, economiser and complementary dampers — and combine outputs with min/max select.",
    ],
    one_line=("Temperature loops drive the <strong>valves</strong>, air-quality and economy logic drive the <strong>dampers</strong> — "
              "and simple <strong>min/max selects</strong> let limits and overrides take over safely when needed."),
    why=("<p>Real AHUs run several loops at once, and those loops interact. Knowing the standard patterns — cascade, reset, split "
         "range, minimum position, select logic — lets you read any vendor's program, write clear sequences and spot why two "
         "loops are fighting each other.</p>"),
    body=(
        "<h3>AHU-01's loops</h3>"
        + fig(d_ahu01_loops(), "Each loop has one job; a min select lets the supply-air low limit override the main loop.")
        + table(["Loop", "Input → output", "Notes"], [
            ("Temperature", "Return air (24 °C) → CHW valve", "PI; enabled only with the fan proven"),
            ("Supply air low limit", "Supply air (11 °C) → limits the valve", "Stops very cold supply air (condensation on diffusers, cold draughts) if the return loop asks for too much"),
            ("Ventilation", "Return CO₂ → fresh air damper 20–50 %", "Demand-controlled ventilation (page 3.2)"),
            ("Fan speed", "Fixed 42 Hz", "Would become a static-pressure loop with VAV (page 2.4)"),
        ])
        + "<h3>Combining loops: min and max select</h3>"
        + "<p>When two loops want to drive the same output, a <strong>select</strong> decides. A <strong>min select</strong> takes "
          "the lower of the two outputs: AHU-01's valve = min(return-air loop, supply-air low-limit loop), so the limit can "
          "only <em>reduce</em> cooling. A <strong>max select</strong> takes the higher: fresh air damper = max(minimum position, "
          "CO₂ demand, economiser), so ventilation can never fall below the minimum.</p>"
        + "<h3>Cascade control and supply air reset</h3>"
        + bullets([
            "<strong>Cascade:</strong> an outer room (or return) loop calculates a supply air setpoint; an inner supply air loop drives the valve to it. The inner loop catches disturbances — such as a change in chilled water temperature — before the room notices.",
            "<strong>Supply air temperature reset:</strong> in VAV systems, the supply air setpoint is raised (e.g. from 13 °C towards 16 °C) when zones need little cooling, saving chiller energy — but limited by humidity, because warmer coil air removes less moisture.",
        ])
        + "<h3>Split range with a deadband</h3>"
        + fig(d_split_range(), "One loop output drives two valves in sequence, with a band in the middle where both are closed.")
        + "<p>Where an AHU has both heating and cooling, one PID output can drive both: the bottom of the range opens the heating "
          "valve, the top opens the cooling valve, and a <strong>deadband</strong> in the middle keeps both closed. This makes "
          "simultaneous heating and cooling impossible — a common, expensive fault when two separate loops are used.</p>"
        + "<h3>Damper control</h3>"
        + table(["Strategy", "How", "Notes"], [
            ("Minimum position", "Fresh air damper never below the design minimum while occupied", "Covers the building's own pollutants"),
            ("Demand-controlled ventilation", "CO₂ ramps the damper between minimum and maximum", "Big energy saving in variable occupancy"),
            ("Economiser (free cooling)", "Open fully when outdoor air enthalpy is below return air enthalpy", "Limited value in hot, humid climates; compare enthalpy, not just temperature"),
            ("Complementary fresh and return dampers", "One signal: fresh opens as return closes (actuators set in opposite directions)", "Keeps the total airflow steady"),
            ("Exhaust tracking", "Exhaust/relief damper follows the fresh air damper", "Keeps building pressure stable"),
            ("Closed when off", "All outside-air dampers closed when the AHU stops", "Spring return gives the same on power loss"),
        ])
        + "<h3>Valves on FCUs and other small units</h3>"
        + "<p>On/off (two-position) valves use a thermostat with a <strong>deadband</strong> and often a minimum on/off time rather "
          "than PID (page 2.3). Modulating FCU valves use the same PI principles as AHUs, usually inside an application-specific "
          "controller with pre-set tuning.</p>"
    ),
    ahu01=("<p>In code-like terms: <strong>CHWV = min(PID_RAT, PID_SAT_lowlimit)</strong> when the fan is proven, else 0 %; "
           "<strong>FAD = max(20 %, DCV(CO₂))</strong> limited to 50 % when the fan is proven, else 0 %. Two lines, four loops, "
           "every case covered — that is what good control logic looks like.</p>"),
    on_site=[
        "Trend every loop that drives the same output together — fighting loops show up immediately.",
        "Check select logic by forcing one input: e.g. warm the supply air sensor's limit and watch the valve.",
        "For complementary dampers, check both move — and in opposite directions — across the full range.",
        "Look for heating and cooling valves open at the same time; it is never intentional.",
    ],
    faults=[
        ("Heating and cooling valves both open", "Two separate loops without a deadband or interlock", "Use split range or interlock"),
        ("Supply air too cold, diffusers dripping", "No supply air low limit; return loop asking for full cooling", "Add low-limit select"),
        ("CO₂ high but damper stays at minimum", "Select uses min instead of max, or DCV disabled", "Select logic; DCV enable"),
        ("Room cycles slowly despite good tuning", "Single slow loop; disturbances on the water side", "Consider cascade (room → supply air)"),
    ],
    terms=[
        ("Min / max select", "Logic choosing the lower / higher of several outputs."),
        ("Low-limit loop", "Loop that only reduces an output to keep a value above a limit."),
        ("Cascade control", "Outer loop sets the setpoint of an inner loop."),
        ("Supply air temperature reset", "Raising or lowering the supply air setpoint with demand."),
        ("Split range", "One loop output driving two devices in sequence."),
        ("Deadband (split range)", "Middle band where neither device is active."),
        ("Complementary dampers", "Dampers driven so one opens as the other closes."),
        ("Economiser", "Using outdoor air for free cooling when it has less enthalpy than return air."),
    ],
    scenarios=[dict(
        prompt="In a meeting room AHU with both heating and cooling, trends show the heating valve at 30 % and the cooling valve at 45 % for hours. Each valve has its own PID loop with the same setpoint. What is the fix?",
        options=["Raise both setpoints.", "Replace the two loops with split-range control and a deadband (or interlock them).",
                 "Slow both loops down."],
        answer=1,
        explain=(" Two loops chasing the same setpoint end up fighting, heating and cooling at once. Split range with a deadband makes "
                 "simultaneous operation impossible."),
    )],
    questions=[
        ("Why is AHU-01's valve a min select of two loops?", "So the supply air low-limit loop can reduce cooling when supply air gets too cold, while the return air loop controls normally otherwise."),
        ("Why is the fresh air damper a max select?", "So ventilation never falls below the minimum, whatever the CO₂ or economiser logic asks for."),
        ("What is cascade control?", "An outer loop (room or return temperature) sets the setpoint of an inner loop (supply air), which drives the valve."),
        ("What does the deadband in split-range control prevent?", "Heating and cooling being active at the same time."),
        ("Why is an economiser less useful in hot, humid climates?", "Outdoor air is rarely both cooler and drier than return air, so its enthalpy is usually higher."),
    ],
)

P5 = dict(
    id="6-5", slug="alarms", title="Alarms: filter dirty, high and low temperature",
    objectives=[
        "Name the main types of BMS alarm.",
        "Set limits, deadbands, delays, enable conditions and priorities correctly.",
        "Configure filter-dirty and high/low temperature alarms for an AHU.",
        "Write alarm messages that tell the reader what to do.",
    ],
    one_line=("A good alarm fires <strong>only when someone needs to act</strong>, clears cleanly, and tells the reader "
              "<strong>what is wrong, where, and what to check first</strong>."),
    why=("<p>Alarms are how the BMS asks for help. Too few and failures go unnoticed; too many and operators stop reading them. "
         "The difference lies in a handful of settings — deadband, delay, enable condition, priority — and in how the message "
         "is written.</p>"),
    body=(
        "<h3>Types of alarm</h3>"
        + table(["Type", "Example"], [
            ("Status / proving", "Fan commanded on but not running; failed to stop"),
            ("Analogue limit", "Return air above 27 °C"),
            ("Deviation", "Supply air more than 3 K from its setpoint for 20 min"),
            ("Equipment fault", "VFD fault, chiller common alarm"),
            ("Maintenance", "Filter dirty; run-hours due for service"),
            ("Sensor fault", "Reading out of range, open or short circuit"),
            ("Communication", "Device offline, Modbus timeouts"),
            ("Safety", "Fire shutdown, high-pressure cut-out"),
        ])
        + "<h3>The settings that matter</h3>"
        + table(["Setting", "What it does", "Without it…"], [
            ("Limit", "The value that triggers the alarm", "—"),
            ("Deadband (hysteresis)", "The value must come back past limit − deadband to clear", "Alarm chatters on and off around the limit"),
            ("Delay", "Condition must last this long before the alarm fires", "Every short spike is an alarm"),
            ("Enable condition", "Alarm only active when it makes sense (e.g. fan running, occupied)", "Alarms all night when the plant is off by schedule"),
            ("Priority", "Critical / high / medium / low — drives display and routing", "Everything looks equally urgent"),
            ("Message", "Text shown to the operator", "Operators guess"),
            ("Acknowledge required", "Operator must confirm", "Short events vanish unnoticed"),
        ])
        + fig(d_alarm_timing(), "The alarm fires after 15 minutes above 27 °C and clears only below 26 °C.")
        + "<h3>Filter dirty alarm</h3>"
        + steps([
            "Source: the filter ΔP switch (DI), or a ΔP sensor (AI) compared with the filter's recommended final pressure drop.",
            "Enable only while the fan has been <strong>proven running for 5 minutes</strong> — ΔP is meaningless with the fan off or starting.",
            "Delay <strong>5 minutes</strong> so gusts and start-up transients do not trigger it.",
            "Priority <strong>low (maintenance)</strong> — the AHU keeps running.",
            "With a ΔP sensor, also trend it: the slow rise shows when filters will need changing.",
        ])
        + "<h3>High and low temperature alarms</h3>"
        + table(["Alarm", "Condition", "Enable", "Priority", "Why"], [
            ("Return air high", "> 27 °C for 15 min, clears < 26 °C", "Fan proven 30 min and occupied", "Medium", "Comfort failure"),
            ("Supply air low", "< 10 °C for 5 min, clears > 11 °C", "Fan proven", "Medium", "Condensation on diffusers; control fault"),
            ("Insufficient cooling", "Supply air > 18 °C for 15 min while valve > 90 %", "Fan proven", "High", "Points to the chilled water side, not the AHU"),
            ("Return air humidity high", "> 65 % RH for 30 min, clears < 60 %", "Fan proven", "Medium", "Comfort and mould risk"),
        ])
        + callout("tip", "Combine conditions for diagnosis",
                  "<p>“Supply air high <em>and</em> valve fully open” tells the operator the AHU is doing its best and the problem is "
                  "upstream. One well-designed combined alarm is worth several simple ones.</p>")
        + "<h3>Writing alarm messages</h3>"
        + table(["Weak message", "Better message"], [
            ("AHU01_SF_ALM", "AHU-01 (L3 offices) supply fan failed to start — check VFD display and MCC isolator"),
            ("RAT HIGH", "AHU-01 return air 27.8 °C, above 27 °C for 15 min — check CHW valve and chilled water supply"),
            ("FILTER", "AHU-01 filter dirty — schedule filter replacement (AHU keeps running)"),
        ], "plain")
    ),
    ahu01=table(["AHU-01 alarm", "Source", "Priority"], [
        ("Fire shutdown", "Fire DI", "Critical"),
        ("Supply fan failed to start / stopped", "Command vs status", "High"),
        ("Supply fan failed to stop", "Command off, status on > 60 s", "High"),
        ("VFD fault", "Fault DI (+ Modbus fault code)", "High"),
        ("Insufficient cooling", "SAT + valve position", "High"),
        ("Not in Auto", "Auto DI while the schedule wants it running", "Medium"),
        ("Return air high / supply air low / humidity high", "AIs as above", "Medium"),
        ("Filter dirty", "ΔP switch DI", "Low"),
        ("Sensor fault (any AI)", "Out of range", "Medium"),
        ("VFD communication lost", "Modbus timeout 60 s", "Low"),
    ], "plain"),
    on_site=[
        "Review the alarm log weekly during the first months: anything frequent is either a real problem or a badly set alarm.",
        "Test each alarm by creating the condition, and check it reaches the right person.",
        "Agree priorities and routing with the facility team — they live with them.",
        "Check “return to normal” works as well as the alarm itself.",
    ],
    faults=[
        ("Same alarm dozens of times a day", "No deadband or delay", "Add hysteresis and a delay"),
        ("Temperature alarms every night", "No enable condition (plant off by schedule)", "Enable only when running and occupied"),
        ("Filter alarm whenever the fan starts", "No running-time enable", "Enable after fan proven 5 min"),
        ("Critical alarms missed", "Everything at the same priority / no routing", "Priorities and notification routing"),
    ],
    terms=[
        ("Alarm limit", "Value at which the alarm condition starts."),
        ("Hysteresis (deadband)", "Amount the value must return past the limit before the alarm clears."),
        ("Alarm delay", "Time the condition must persist before the alarm is raised."),
        ("Enable condition", "Condition under which an alarm is active."),
        ("Priority", "Importance of an alarm for display and routing."),
        ("Return to normal", "Event when the alarm condition clears."),
        ("Combined alarm", "Alarm based on several conditions, e.g. supply air high and valve fully open."),
    ],
    scenarios=[dict(
        prompt="Operators complain that AHU-05's “return air high” alarm appears and clears 30 times an afternoon, with the value hovering around 27.0 °C. What should you change?",
        options=["Delete the alarm.", "Add a deadband (e.g. clear below 26 °C) and a time delay (e.g. 15 min).",
                 "Raise the limit to 35 °C."],
        answer=1,
        explain=(" Without hysteresis and delay, a value hovering at the limit makes the alarm chatter. Fix the settings — and also look at "
                 "why the AHU cannot hold 24 °C."),
    )],
    questions=[
        ("What does an alarm deadband do?", "The value must return past the limit by the deadband before the alarm clears, so it does not chatter around the limit."),
        ("Why is the filter-dirty alarm enabled only after the fan has run for 5 minutes?", "ΔP across the filter is meaningless when the fan is off or starting; checking too early gives false results."),
        ("Why is “supply air high while valve > 90 %” a useful alarm?", "It shows the AHU is asking for full cooling and still failing, pointing to the chilled water supply rather than the AHU."),
        ("Name three things a good alarm message contains.", "What is wrong, where (which plant/area), and what to check first or the impact."),
        ("Why should temperature alarms have an enable condition?", "So they do not fire when the plant is off by schedule or starting up — when the values are expected to be out of range."),
    ],
)

P6 = dict(
    id="6-6", slug="scheduling", title="Scheduling and time-based logic",
    objectives=[
        "Set up weekly schedules, exceptions and holiday calendars.",
        "Explain occupancy modes, optimum start and timed overrides.",
        "Use on-delay, off-delay and minimum on/off timers correctly.",
        "Apply staggered starts, run-hour rotation and unoccupied humidity control.",
    ],
    one_line=("Schedules decide <strong>when</strong> plant should run; timers and time-based logic decide <strong>how</strong> it "
              "changes state — and together they are the biggest single energy saving a BMS delivers."),
    why=("<p>Plant that runs when nobody is there wastes energy every night and weekend. Plant that starts too late leaves the first "
         "people of the day uncomfortable. Getting schedules, holidays and overrides right — and making sure they live in the "
         "controller — is basic, valuable BMS work.</p>"),
    body=(
        fig(d_schedule(), "Blue: occupied. Amber: optimum start. Green: a 2-hour after-hours override.")
        + "<h3>Schedules and calendars</h3>"
        + table(["Element", "What it does", "BACnet object"], [
            ("Weekly schedule", "On/off (or mode) times for each day of the week", "Schedule — weekly part"),
            ("Exception schedule", "Different times for specific dates", "Schedule — exception part"),
            ("Holiday calendar", "List of dates treated as holidays by many schedules", "Calendar"),
            ("Schedule output", "Writes occupied/unoccupied to the plant's occupancy point", "Writes to a BV / MSV at a set priority"),
        ])
        + "<p>Schedules must run <strong>in the controller</strong> (or a supervisory controller on the same network), so plant still "
          "starts and stops when the server is down. The server is where people view and edit them.</p>"
        + "<h3>Occupancy modes</h3>"
        + table(["Mode", "Typical behaviour"], [
            ("Occupied", "Normal setpoints, full ventilation"),
            ("Unoccupied", "Plant off; may restart for humidity or temperature limits"),
            ("Standby", "Plant on with wider setpoints (e.g. empty meeting room)"),
            ("Optimum start", "Plant starts early enough to reach setpoint at occupancy"),
        ])
        + "<h3>Optimum start</h3>"
        + "<p>Instead of a fixed early start, the controller works out <em>when</em> to start: it compares the room temperature with "
          "the setpoint and uses the pull-down rate it has learned on previous days. Example: return air 29 °C at 06:00, "
          "setpoint 24 °C, learned rate 2.5 K per hour → needs 2 hours → start at 06:00 for 08:00. An <strong>earliest start</strong> "
          "limit stops it starting absurdly early after a long weekend. <strong>Optimum stop</strong> does the opposite — stopping a "
          "little early when the building can coast to the end of occupancy.</p>"
        + "<h3>Overrides</h3>"
        + bullets([
            "<strong>Timed override</strong> for after-hours work: a BMS command or local button gives occupied mode for a fixed time (e.g. 2 hours), then reverts automatically. Log it — tenants are often billed for it.",
            "Avoid <strong>permanent</strong> overrides; they are how plant ends up running all weekend (page 1.4).",
        ])
        + "<h3>Timers</h3>"
        + fig(d_timers(), "On-delay waits before switching on; off-delay keeps the output on after the input drops.")
        + table(["Timer", "Use"], [
            ("On-delay (TON)", "Proving delays; alarm delays; stabilising before enabling a loop"),
            ("Off-delay (TOF)", "Pump run-on after a chiller stops; fan run-on to clear an electric heater's heat"),
            ("Minimum on / off time", "Stop compressors, fans and pumps short-cycling"),
            ("Run-hour counter", "Maintenance scheduling; lead/lag rotation"),
        ])
        + "<h3>More time-based logic</h3>"
        + bullets([
            "<strong>Staggered start:</strong> offset each AHU's start by a minute or two so the morning peak and the plant's starting currents are spread.",
            "<strong>Lead/lag rotation:</strong> swap duty and standby pumps or fans by run-hours or weekly, so they wear evenly and the standby is known to work.",
            "<strong>Unoccupied humidity control:</strong> in humid climates, an empty, closed building can reach mould-friendly humidity. Starting the AHU briefly when return humidity exceeds a limit (e.g. 70 %) protects the building.",
            "<strong>Time synchronisation:</strong> all controllers take time from one NTP source; daylight-saving changes (where used) must be handled consistently.",
        ])
    ),
    ahu01=("<p>AHU-01: weekly schedule <strong>Monday–Saturday 08:00–19:00</strong>, Sunday off, the site's <strong>holiday calendar</strong> "
           "applied; <strong>optimum start</strong> with an earliest start of 06:30; <strong>timed override 2 h</strong> from the BMS or "
           "the floor's after-hours button; staggered start <strong>+0 min</strong> (AHU-02 +2 min, AHU-03 +4 min…); unoccupied "
           "humidity run when return RH exceeds 70 % for 30 minutes. The schedule lives in DDC-AHU-01.</p>"),
    on_site=[
        "Load the year's public holidays into the calendar before January — and check it every year.",
        "Check where each schedule actually runs; schedules held only in the server stop working when it is down.",
        "Review the override log monthly: frequent overrides mean the schedule does not match how the building is used.",
        "After any time change (power loss, firmware update), check controller clocks against the NTP source.",
    ],
    faults=[
        ("Plant ran on a public holiday", "Holiday missing from the calendar, or calendar not linked to the schedule", "Calendar entries and links"),
        ("Plant starts at the wrong time", "Controller clock wrong; time zone or DST setting", "Time sync"),
        ("Everything starts at 08:00 sharp, tripping supply", "No staggered start", "Start offsets"),
        ("Pump B never runs; fails when finally needed", "No lead/lag rotation", "Rotation logic"),
        ("Musty smell on Monday mornings", "No unoccupied humidity control in a humid climate", "Add humidity-based run"),
    ],
    terms=[
        ("Weekly schedule", "Repeating on/off or mode times for each day."),
        ("Exception schedule", "Schedule entry for a specific date or date range."),
        ("Holiday calendar", "List of dates treated as holidays by schedules."),
        ("Optimum start", "Starting plant at the time needed to reach setpoint by occupancy."),
        ("Timed override", "Temporary occupied mode that reverts automatically."),
        ("On-delay / off-delay", "Timers delaying switching on, or delaying switching off."),
        ("Minimum on/off time", "Shortest run or rest time to prevent short-cycling."),
        ("Lead/lag rotation", "Swapping duty and standby equipment to share wear."),
        ("Staggered start", "Starting plant items at different times to limit peaks."),
    ],
    scenarios=[dict(
        prompt="On Republic Day the office was closed, but all AHUs ran from 08:00 to 19:00. The weekly schedules are correct. What was missing?",
        options=["An NTP server.", "The holiday in the holiday calendar (or the calendar was not linked to the AHU schedules).",
                 "Optimum start."],
        answer=1,
        explain=(" Weekly schedules do not know about holidays. The date must be in the calendar, and each schedule must reference that "
                 "calendar as an exception."),
    )],
    questions=[
        ("Why must schedules run in the controller rather than only on the server?", "So plant still starts and stops on time when the server or network is down."),
        ("How does optimum start decide when to start?", "From the difference between room temperature and setpoint and the learned pull-down rate, within an earliest-start limit."),
        ("Give one use each for an on-delay and an off-delay.", "On-delay: proving or alarm delays. Off-delay: pump run-on after a chiller stops."),
        ("What is lead/lag rotation and why do it?", "Swapping duty and standby equipment (e.g. by run-hours) so wear is shared and the standby is known to work."),
        ("Why might an AHU run in unoccupied hours in a humid climate?", "To bring down high humidity in the closed building and prevent mould and musty smells."),
    ],
)

MODULE_INTRO = (
    "<p>This module brings everything together: the AHU-01 start/stop sequence, the interlocks and safeties around it, PID "
    "loops and how to tune them, the patterns used to control valves and dampers, alarms worth receiving, and schedules. "
    "Two interactive tools help — the AHU-01 sequence stepper (6.1) and the PID playground (6.3).</p>"
)

PAGES = [P1, P2, P3, P4, P5, P6]

QUIZ = [
    mcq("AHU-01's fan is commanded on but status does not arrive in 30 s. The sequence…", ["keeps trying forever", "raises fan fail, stops the fan and locks out",
        "opens the valve fully", "switches to Hand"], 1, "Failure to prove → alarm, stop, lockout until reset.", "6.1"),
    mcq("Why is the CHW valve closed when the fan stops?", ["To save the actuator", "A cold coil without airflow sweats and drips", "BACnet requires it", "To reset the PID"], 1,
        "No airflow + cold coil = condensation.", "6.1"),
    mcq("Where must a fire shutdown contact be wired?", ["Only to a BMS DI", "In series, upstream of the HOA switch", "After the HOA switch", "In the server"], 1,
        "So it stops the fan in Hand as well as Auto.", "6.2"),
    mcq("A 4 K proportional band means a 1 K error moves the output by…", ["4 %", "25 %", "40 %", "100 %"], 1, "100 % ÷ 4 K = 25 % per K.", "6.3"),
    mcq("A loop settles 1.5 K away from setpoint and stays there. It most likely lacks…", ["derivative", "integral", "a sensor", "a deadband"], 1,
        "P-only control leaves an offset; integral removes it.", "6.3"),
    mcq("AHU-01's fresh air damper uses a max select because…", ["it saves energy", "ventilation must never fall below the minimum", "it is faster", "BACnet needs it"], 1,
        "Max(20 %, DCV, economiser).", "6.4"),
    mcq("Heating and cooling valves both open for hours. Best fix?", ["Slower loops", "Split range with a deadband", "Higher setpoint", "Bigger valves"], 1,
        "Split range makes simultaneous operation impossible.", "6.4"),
    mcq("An alarm chatters on and off around its limit. Add…", ["a higher priority", "deadband and delay", "more trend logs", "a second sensor"], 1,
        "Hysteresis and delay stop chattering.", "6.5"),
    mcq("Plant ran on a public holiday although weekly schedules are right. Check…", ["the PID tuning", "the holiday calendar and its link to the schedules", "the VFD", "the sensor"], 1,
        "Weekly schedules need the calendar for holidays.", "6.6"),
    mcq("Which timer keeps a pump running after a chiller stops?", ["On-delay", "Off-delay", "Minimum off time", "Run-hour counter"], 1,
        "Off-delay = run-on.", "6.6"),
]

FINAL = [
    mcq("Why wait 60 s after the fan is proven before enabling the PID loop?", ["To save energy", "To let airflow and readings settle", "BACnet timing", "To test the alarm"], 1,
        "Loops enabled during start-up transients overreact.", "6.1"),
    mcq("Safety interlocks are…", ["in the program only", "hard-wired and independent of the BMS", "only on the server", "optional in Hand"], 1,
        "They must work if the BMS fails and in every mode.", "6.2"),
    mcq("Most HVAC loops use…", ["P only", "PI", "PID with large D", "D only"], 1, "Derivative amplifies noise; HVAC is slow.", "6.3"),
    mcq("The filter-dirty alarm should be enabled…", ["always", "only after the fan has been proven for a few minutes", "only at night", "only in Hand"], 1,
        "ΔP is meaningless when the fan is off or starting.", "6.5"),
    mcq("Optimum start calculates…", ["the end of occupancy", "how early to start so setpoint is reached at occupancy", "the PID gain", "the holiday list"], 1,
        "Using the temperature difference and learned pull-down rate.", "6.6"),
]
