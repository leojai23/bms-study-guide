# -*- coding: utf-8 -*-
"""Module 2 — HVAC Control Fundamentals. Vendor-neutral; typical values are for commercial buildings
in hot climates (such as India) and are always "typical" — the project design governs."""
from bms_common import (table, steps, bullets, callout, cards, fig, svg, defs, t, rect, box,
                        line, path, circle, mcq)

# ==========================================================================
# Diagrams
# ==========================================================================

def d_ahu_sections():
    i = defs("as")
    i += rect(20, 60, 600, 130, "d-soft", 10)
    secs = [(20, 130, "Dampers +", "mixing box"), (130, 190, "Pre-", "filter"), (190, 250, "Fine", "filter"),
            (250, 340, "Cooling", "coil"), (340, 410, "Heating", "coil (opt.)"), (410, 540, "Supply", "fan"),
            (540, 620, "Discharge", "")]
    for k, (a, b, l1, l2) in enumerate(secs):
        if k:
            i += line(a, 62, a, 188, "d-line d-thin d-dash")
        i += t((a + b) / 2, 74, l1, "d-ts d-tb") + (t((a + b) / 2, 88, l2, "d-ts d-tb") if l2 else "")
    i += line(0, 120, 68, 120, "d-aline", end="as-a") + t(4, 106, "Fresh air", "d-ts", "start")
    i += path("M75,240 L75,192", "d-aline", end="as-a") + t(85, 232, "Return air", "d-ts", "start")
    i += rect(70, 104, 26, 30, "d-box", 3) + line(72, 132, 94, 106)
    i += rect(62, 160, 30, 24, "d-box", 3) + line(64, 182, 90, 162)
    for x0 in (148, 208):
        i += path(f"M{x0 + 12},100 L{x0},112 L{x0 + 24},126 L{x0},140 L{x0 + 24},154 L{x0 + 12},168")
    i += rect(275, 100, 40, 70, "d-acc", 3)
    for y in range(108, 170, 9):
        i += line(277, y, 313, y, "d-line d-thin")
    i += rect(268, 172, 54, 7, "d-box", 2)
    i += rect(355, 100, 40, 70, "d-box d-dash", 3)
    i += circle(475, 135, 30, "d-box") + path("M460,151 L494,135 L460,119 Z")
    i += line(622, 125, 770, 125, "d-aline", end="as-a") + t(770, 110, "Supply air", "d-ts", "end")
    pts = [(75, "Damper · AO", "Mixed air T · AI"), (190, "Filter ΔP", "DI or AI"), (295, "CHW valve · AO", "Condensate · DI"),
           (375, "Valve / heater", "AO or DO"), (475, "Start DO · Status DI", "Speed AO"), (690, "SAT · AI", "")]
    for x, a, b in pts:
        i += t(x, 210 if x != 75 else 254, a, "d-ts d-ta") + (t(x, 224 if x != 75 else 268, b, "d-ts d-ta") if b else "")
    return svg(780, 280, i, "Sections of an air handling unit in airflow order, with typical BMS points")


def d_air_streams():
    i = defs("st")
    i += rect(410, 50, 350, 190, "d-soft", 10) + t(585, 72, "Offices — slightly positive pressure", "d-ts d-tb")
    for x in (480, 560, 640, 700):
        i += circle(x, 205, 9, "d-box") + line(x, 214, x, 232)
    i += box(160, 115, 170, 80, "AHU", "fresh + return|= mixed air", "d-acc")
    i += line(10, 140, 158, 140, "d-aline", end="st-a")
    i += t(14, 126, "Fresh (outdoor) air · 35 °C", "d-ts d-ta", "start")
    i += path("M332,140 L470,140 L470,110", "d-aline", end="st-a") + t(395, 128, "Supply air 13 °C", "d-ts d-ta")
    i += path("M410,215 L250,215 L250,197", "d-line", end="st")
    i += t(350, 204, "Return air 24 °C", "d-ts")
    i += path("M300,215 L300,255 L10,255", "d-line d-dash", end="st") + t(14, 242, "Exhaust (relief) air", "d-ts", "start")
    i += rect(286, 214, 28, 26, "d-box", 3) + line(288, 238, 312, 216)
    i += path("M690,50 L690,14", "d-line d-dash", end="st") + t(680, 22, "Toilet exhaust fan", "d-ts", "end")
    return svg(780, 270, i, "The four air streams of an AHU serving offices")


def d_fcu():
    i = defs("fc")
    i += rect(170, 50, 400, 100, "d-soft", 10) + t(370, 64, "Fan coil unit", "d-ts d-tb")
    i += path("M215,76 L203,86 L227,98 L203,110 L227,122 L203,134 L215,142")
    i += rect(262, 74, 46, 70, "d-acc", 3)
    for y in range(82, 144, 9):
        i += line(264, y, 306, y, "d-line d-thin")
    i += circle(420, 100, 28, "d-box") + path("M405,116 L438,100 L405,84 Z")
    i += line(30, 100, 168, 100, "d-aline", end="fc-a") + t(34, 86, "Room (return) air 24 °C", "d-ts", "start")
    i += line(572, 100, 760, 100, "d-aline", end="fc-a") + t(760, 86, "Supply air ≈ 14 °C", "d-ts", "end")
    i += path("M110,22 L190,22 L190,48", "d-line d-dash", end="fc") + t(106, 22, "Fresh air from TFA", "d-ts", "end")
    i += rect(250, 150, 70, 8, "d-box", 2) + t(240, 172, "Drain pan → condensate drain", "d-ts", "end")
    i += line(272, 158, 272, 262, "d-cold") + line(298, 158, 298, 262, "d-warmline")
    i += t(266, 276, "CHWS", "d-ts", "end") + t(304, 276, "CHWR", "d-ts", "start")
    i += path("M290,206 L306,206 L298,218 Z M290,230 L306,230 L298,218 Z", "d-box")
    i += line(298, 218, 322, 218) + box(322, 207, 22, 22, "M", "", "d-box", "d-ts d-tb", 4)
    i += box(560, 190, 200, 76, "Room thermostat", "temperature · setpoint|fan L/M/H · valve", "d-acc")
    i += path("M610,190 L610,172 L430,172 L430,129", "d-line d-dash d-thin", end="fc") + t(520, 182, "fan speed", "d-ts")
    i += path("M560,218 L346,218", "d-line d-dash d-thin", end="fc") + t(450, 208, "valve open/close", "d-ts")
    i += line(660, 266, 660, 290, "d-aline d-dash") + t(652, 284, "to BMS (MS/TP or Modbus)", "d-ts d-ta", "end")
    return svg(780, 300, i, "Fan coil unit with chilled water valve and room thermostat")


def d_cav_vav():
    i = defs("cv")
    i += t(195, 18, "CAV — constant air volume", "d-t d-tb") + t(585, 18, "VAV — variable air volume", "d-t d-tb")
    i += line(390, 30, 390, 250, "d-line d-dash d-thin")
    i += box(20, 60, 110, 60, "AHU", "fixed fan speed", "d-acc")
    i += line(130, 90, 370, 90, "d-aline")
    for x in (190, 260, 330):
        i += line(x, 90, x, 140, "d-aline", end="cv-a")
    i += rect(150, 146, 220, 50, "d-soft", 8) + t(260, 171, "One zone", "d-ts")
    i += circle(330, 171, 12, "d-box") + t(330, 171, "T", "d-ts d-tb")
    i += path("M330,183 L330,215 L75,215 L75,122", "d-line d-dash", end="cv")
    i += t(200, 232, "zone temp → CHW valve · airflow never changes", "d-ts")
    i += box(410, 60, 110, 60, "AHU + VFD", "fan speed varies", "d-acc")
    i += line(520, 90, 770, 90, "d-aline")
    i += circle(745, 90, 12, "d-box") + t(745, 90, "P", "d-ts d-tb")
    i += path("M745,78 L745,40 L465,40 L465,58", "d-line d-dash", end="cv") + t(605, 32, "duct static pressure → fan speed", "d-ts")
    for k, x in enumerate((570, 640, 710)):
        i += line(x, 90, x, 128, "d-aline")
        i += box(x - 28, 128, 56, 34, "VAV", "", "d-box", "d-ts d-tb", 5)
        i += line(x, 162, x, 186, "d-aline", end="cv-a")
        i += circle(x, 205, 12, "d-box") + t(x, 205, "T", "d-ts d-tb")
        i += t(x, 228, f"Zone {k + 1}", "d-ts")
    i += t(640, 248, "each zone varies its own airflow · supply temp ≈ constant", "d-ts")
    return svg(780, 260, i, "CAV and VAV systems compared")


def d_vav_cascade():
    i = defs("vc")
    i += box(10, 50, 120, 60, "Zone temp", "measured 25.1 °C", "d-box")
    i += box(170, 50, 130, 60, "Zone PI loop", "setpoint 24 °C", "d-acc")
    i += box(340, 50, 150, 60, "Airflow setpoint", "between min and max", "d-box")
    i += box(530, 50, 110, 60, "Flow PI loop", "", "d-acc")
    i += box(675, 50, 80, 60, "Damper", "actuator", "d-box")
    for a, b in ((130, 168), (300, 338), (490, 528), (640, 673)):
        i += line(a, 80, b, 80, "d-aline", end="vc-a")
    i += path("M715,110 L715,140 L585,140 L585,112", "d-line d-dash", end="vc")
    i += t(650, 154, "measured airflow (flow sensor)", "d-ts")
    i += t(235, 128, "outer loop: temperature", "d-ts d-ta") + t(585, 34, "inner loop: airflow", "d-ts d-ta")
    return svg(760, 170, i, "Pressure-independent VAV box: temperature loop resets the airflow loop")


def d_chw_plant():
    i = defs("cw")
    i += line(190, 60, 760, 60, "d-cold") + line(14, 250, 760, 250, "d-warmline")
    i += t(520, 46, "CHW supply header · 7 °C", "d-ts d-ta") + t(470, 266, "CHW return header · 12.5 °C", "d-ts")
    for y, n in ((120, "1"), (190, "2")):
        i += path(f"M14,250 L14,{y} L60,{y}", "d-warmline") if n == "1" else path(f"M14,{y} L60,{y}", "d-warmline")
        i += circle(36, y, 10, "d-box") + t(36, y + 22, f"PP-{n}", "d-ts")
        i += box(60, y - 25, 100, 50, f"CH-{n}", "chiller", "d-acc")
        i += path(f"M160,{y} L190,{y} L190,60" if n == "1" else f"M160,{y} L190,{y} L190,120", "d-cold")
    i += line(250, 60, 250, 250, "d-line d-dash") + t(258, 156, "Decoupler", "d-ts", "start") + t(258, 170, "(bypass)", "d-ts", "start")
    i += circle(340, 60, 15, "d-acc") + t(340, 60, "SP", "d-ts d-tb") + t(340, 90, "secondary pumps", "d-ts") + t(340, 104, "on VFDs", "d-ts")
    for x, n in ((450, "AHU-01"), (550, "AHU-02"), (650, "FCUs")):
        i += line(x, 60, x, 120, "d-cold") + line(x, 170, x, 250, "d-warmline")
        i += rect(x - 22, 120, 44, 50, "d-soft", 3) + t(x, 145, "coil", "d-ts")
        i += path(f"M{x - 8},196 L{x + 8},196 L{x},208 Z M{x - 8},220 L{x + 8},220 L{x},208 Z", "d-box")
        i += t(x + 14, 208, n, "d-ts d-tb", "start")
    i += line(735, 60, 735, 128) + line(735, 182, 735, 250)
    i += box(712, 128, 46, 54, "ΔP", "", "d-acc", "d-t d-tb", 6)
    i += t(770, 30, "index ΔP sensor → secondary pump speed", "d-ts d-ta", "end")
    return svg(780, 285, i, "Primary-secondary chilled water plant")


def d_cooling_tower():
    i = defs("ct")
    i += box(20, 150, 110, 80, "Building", "AHU / FCU|coils", "d-soft")
    i += rect(300, 120, 170, 110, "d-box", 8) + line(300, 175, 470, 175, "d-line d-thin")
    i += t(385, 147, "Condenser", "d-t d-tb") + t(385, 203, "Evaporator", "d-t d-tb")
    i += t(385, 105, "Water-cooled chiller", "d-ts")
    i += line(300, 190, 132, 190, "d-cold", end="ct-a") + t(216, 180, "CHW supply 7 °C", "d-ts d-ta")
    i += line(132, 216, 298, 216, "d-warmline", end="ct-r") + t(216, 230, "CHW return 12.5 °C", "d-ts")
    i += path("M585,150 L605,40 L675,40 L695,150 Z", "d-soft")
    i += path("M600,40 L600,30 L680,30 L680,40", "d-box") + circle(640, 22, 8, "d-box")
    i += t(640, 95, "fill", "d-ts") + t(690, 32, "fan · VFD", "d-ts", "start")
    i += rect(575, 150, 130, 22, "d-box", 3) + t(640, 161, "basin", "d-ts")
    for x in (610, 670):
        i += line(x, 18, x, 2, "d-line", end="ct")
    i += t(700, 10, "warm, moist air out", "d-ts", "start")
    i += line(772, 118, 700, 118, "d-line", end="ct") + t(772, 104, "outdoor air in", "d-ts", "end")
    i += path("M470,135 L520,135 L520,55 L600,55", "d-warmline", end="ct-r") + t(512, 100, "CW return 37 °C", "d-ts", "end")
    i += path("M640,172 L640,205 L555,205", "d-cold") + circle(540, 205, 14, "d-acc") + t(540, 205, "CWP", "d-ts d-tb")
    i += path("M526,205 L490,205 L490,155 L472,155", "d-cold", end="ct-a") + t(560, 230, "CW supply 32 °C", "d-ts d-ta")
    i += path("M770,160 L707,160", "d-line", end="ct") + t(772, 178, "make-up water", "d-ts", "end")
    i += path("M690,172 L690,250", "d-line d-dash", end="ct") + t(700, 252, "blowdown", "d-ts", "start")
    return svg(780, 265, i, "Condenser water loop between a water-cooled chiller and a cooling tower")


def d_range_approach():
    i = defs("ra")
    x = lambda v: 40 + (v - 25) * 46
    i += line(x(25), 70, x(40), 70, "d-line")
    for v in range(25, 41):
        i += line(x(v), 66, x(v), 74, "d-line d-thin") + (t(x(v), 88, f"{v}", "d-ts") if v % 5 == 0 else "")
    for v, lab, cls in ((28, "Wet-bulb 28 °C", "d-ok"), (32, "CW supply 32 °C", "d-acc"), (37, "CW return 37 °C", "d-bad")):
        i += circle(x(v), 70, 7, cls) + t(x(v), 108, lab, "d-ts d-tb")
    i += path(f"M{x(28)},50 L{x(32)},50", "d-line", end="ra", start="ra") + t((x(28) + x(32)) / 2, 38, "approach 4 K", "d-ts d-ta")
    i += path(f"M{x(32)},50 L{x(37)},50", "d-line", end="ra", start="ra") + t((x(32) + x(37)) / 2, 38, "range 5 K", "d-ts d-ta")
    i += t(x(40) + 6, 70, "°C", "d-ts", "start")
    return svg(760, 125, i, "Cooling tower range and approach on a temperature scale")


def d_modes():
    i = defs("md")
    i += box(260, 10, 240, 44, "Fire mode", "from ANY state · overrides everything", "d-bad")
    xs = [(20, "Off", "d-box"), (200, "Starting", "d-acc"), (380, "Running", "d-ok"), (560, "Stopping", "d-acc")]
    for x, n, c in xs:
        i += box(x, 100, 140, 54, n, "", c)
    i += line(160, 127, 198, 127, "d-line", end="md") + line(340, 127, 378, 127, "d-line", end="md") + line(520, 127, 558, 127, "d-line", end="md")
    i += t(179, 112, "start", "d-ts") + t(359, 112, "proven", "d-ts") + t(539, 112, "stop", "d-ts")
    i += path("M630,154 L630,180 L90,180 L90,156", "d-line", end="md") + t(100, 192, "stopped and proven off", "d-ts", "start")
    i += box(290, 210, 180, 44, "Fault / locked out", "alarm · needs reset", "d-warn")
    i += path("M270,154 L320,208", "d-line d-dash", end="md") + path("M450,154 L420,208", "d-line d-dash", end="md")
    i += t(255, 200, "fails to prove", "d-ts", "end") + t(470, 200, "trips", "d-ts", "start")
    i += box(620, 210, 130, 44, "Hand (local)", "BMS not in control", "d-soft")
    return svg(760, 260, i, "Operating modes of a typical plant item")


# ==========================================================================
# Pages
# ==========================================================================

P1 = dict(
    id="2-1", slug="air-handling-unit", title="Air handling unit (AHU)",
    objectives=[
        "Name the sections of an AHU in airflow order and say what each one does.",
        "List the BMS points that typically belong to each section.",
        "Tell the common AHU types apart, including the treated fresh air unit (TFA).",
        "Choose between return-air, supply-air and space-temperature control.",
    ],
    one_line=("An AHU is a large casing that <strong>filters, cools, dehumidifies and moves air</strong>, delivering it "
              "through ducts to the spaces it serves — the single most common plant item on any BMS."),
    why=("<p>Nearly every BMS engineer's first point list, first wiring diagram and first sequence is for an AHU, and most "
         "comfort complaints in a commercial building lead back to one. If you can read an AHU — what each section does, "
         "which points it needs and how it is controlled — you can handle most of the HVAC side of a BMS.</p>"),
    body=(
        "<h3>The sections, in airflow order</h3>"
        + fig(d_ahu_sections(), "A typical AHU. Blue labels are the BMS points each section usually brings.")
        + table(["Section", "What it does", "Typical BMS points"], [
            ("Fresh air damper", "Lets in outdoor air for ventilation", "Position AO (or open/close DO + end switch DI)"),
            ("Return air damper", "Lets room air back in to be re-used", "Position AO, or manual"),
            ("Mixing box", "Blends fresh and return air", "Mixed air temperature AI (optional)"),
            ("Pre-filter and fine filter", "Remove dust and particles; the pre-filter protects the more expensive fine filter", "ΔP switch DI or ΔP sensor AI per filter"),
            ("Cooling coil", "Cools the air with chilled water and removes moisture", "CHW valve AO"),
            ("Drain pan", "Collects water condensed on the coil", "Condensate overflow DI (optional)"),
            ("Heating coil or electric heater", "Heats or re-heats air — rare in hot climates except for humidity control", "Valve AO or heater stages DO"),
            ("Supply fan", "Moves the air through the ducts", "Start DO, run status DI, fault DI, speed AO"),
            ("Discharge / silencer", "Reduces noise; air leaves for the ducts", "Supply air temperature AI"),
        ])
        + "<p>Bigger systems add a <strong>return fan</strong> and an <strong>exhaust (relief) damper</strong>, a "
          "<strong>humidifier</strong> for dry climates or special areas, or a <strong>heat-recovery wheel</strong> that "
          "pre-cools incoming fresh air with outgoing exhaust air.</p>"
        + "<h3>How the coil removes moisture</h3>"
        + "<p>Air can hold only so much water vapour at a given temperature. When the cooling coil chills the air below "
          "its <strong>dew point</strong>, some of the vapour condenses on the coil fins as water, drips into the drain pan "
          "and leaves through the condensate drain. That is how an AHU dehumidifies — and why the air leaving a "
          "chilled-water coil is usually only about 12–14 °C. In humid climates removing moisture is often as important "
          "as lowering temperature.</p>"
        + "<h3>Common AHU types</h3>"
        + table(["Type", "What it is", "Where you see it"], [
            ("Recirculating AHU", "Mixes a portion of fresh air with return air", "Offices, malls, most comfort cooling"),
            ("Treated fresh air unit (TFA)", "100 % fresh air, cooled and dehumidified, supplied to the floors or to FCUs", "Hotels, offices with FCUs, hospitals"),
            ("Constant volume (CAV) AHU", "Fixed airflow; temperature varied by the valve", "Single large zones — halls, lobbies"),
            ("Variable volume (VAV) AHU", "Fan speed follows duct pressure; airflow varies per zone", "Multi-zone offices (page 2.4)"),
            ("Packaged / DX unit", "Has its own compressor instead of a chilled water coil", "Smaller buildings, retail"),
        ])
        + "<h3>What does the valve control to?</h3>"
        + "<p>The CHW valve is always modulated to hold <em>some</em> temperature. Which one is a design decision:</p>"
        + table(["Control on…", "How it works", "Good for", "Watch out for"], [
            ("Return air temperature", "Return air is taken as the average room temperature", "Simple single-zone AHUs; very common", "Return air is affected by ceiling heat and leaky ducts"),
            ("Supply air temperature", "Holds the air leaving the coil at e.g. 13 °C", "VAV systems; TFAs", "Rooms are not controlled directly; usually reset from zone demand"),
            ("Space temperature", "A room sensor drives the valve", "Single rooms or halls", "One sensor must represent the whole zone"),
            ("Cascade (space → supply)", "Room loop sets the supply air setpoint; supply loop drives the valve", "Best comfort and stability", "Two loops to tune"),
        ])
        + callout("note", "Typical values (always check the design)",
                  bullets(["Supply air leaving a CHW coil: about 12–15 °C.",
                           "Return air / room: about 23–25 °C.",
                           "Chilled water: about 6–7 °C in, 12–13 °C out.",
                           "Filter pressure drop: low when clean, rising as dust builds up; the dirty-filter alarm is set from the filter maker's recommended final pressure drop."]))
    ),
    ahu01=("<p>AHU-01 is a <strong>recirculating CAV-style AHU</strong>: modulating fresh air damper, manual return damper, one "
           "filter stage with a ΔP switch, a CHW coil with a 2-way valve, and a supply fan on a VFD. It controls on "
           "<strong>return air temperature</strong> (24 °C) and monitors supply air temperature for alarms.</p>"),
    on_site=[
        "Check the airflow-direction arrows on filters, coils and dampers — parts are sometimes fitted backwards.",
        "Open the access door and look: is the drain pan clean, and is the condensate trap filled with water? A dry trap lets air suck the condensate back and the pan overflows.",
        "Find out whether the valve is 2-way or 3-way and whether it is a PICV — it changes how the plant behaves (page 3.6).",
        "Note the fan type: belt drive (belts slip and break) or direct drive / EC fan.",
        "Read the AHU's nameplate and the commissioning sheet: design airflow, external static pressure, coil capacity.",
    ],
    faults=[
        ("Rooms hot; valve at 100 %; supply air 18 °C instead of 13 °C", "Chilled water problem: supply temperature too high or flow too low", "CHW supply temperature at the coil; plant status; strainer"),
        ("Supply air cold but rooms still hot", "Not enough airflow: dirty filter, slipping belt, low fan speed, closed damper", "Filter ΔP, fan speed, belt, dampers"),
        ("Water on the floor near the AHU", "Blocked condensate drain or dry trap", "Drain pan, trap, drain line"),
        ("High humidity in the offices", "Coil not cold enough, or too much fresh air", "CHW temperature, supply air temperature, fresh air damper position"),
        ("Filter alarm a week after a filter change", "Wrong filter grade, or switch set too low", "Filter type, ΔP switch setting"),
    ],
    terms=[
        ("AHU", "Air handling unit: filters, cools, dehumidifies and moves air to the spaces it serves."),
        ("Mixing box", "Section where fresh and return air are blended."),
        ("Cooling coil", "Finned tubes carrying chilled water; cools the air passing over them."),
        ("Dew point", "Temperature at which water vapour in the air starts to condense."),
        ("Condensate", "Water removed from the air by the cooling coil."),
        ("TFA", "Treated fresh air unit — an AHU that handles 100 % outdoor air."),
        ("Return air control", "Valve modulated to hold the return air temperature."),
        ("Supply air control", "Valve modulated to hold the supply (off-coil) air temperature."),
        ("Cascade control", "One loop sets the setpoint of another, e.g. room temperature sets supply air temperature."),
    ],
    scenarios=[dict(
        prompt="The 3rd-floor offices are hot. The AHU-01 graphic shows the CHW valve at 100 % and supply air at 18 °C (normally 13 °C). The fan is running at its usual speed. Where do you look first?",
        options=["The AHU-01 PID tuning — it must be too slow.",
                 "The chilled water supply: its temperature at the coil and whether the plant is delivering enough flow.",
                 "The return air sensor — it must be reading high."],
        answer=1,
        explain=(" The controller is already asking for full cooling (valve 100 %), yet the coil cannot cool the air. The "
                 "problem is the water side: high CHW supply temperature, a closed isolation valve, a blocked strainer or "
                 "a plant fault. Tuning cannot help when the output is already at its limit."),
    )],
    questions=[
        ("List the sections of a typical AHU in airflow order.", "Dampers and mixing box → pre-filter → fine filter → cooling coil (with drain pan) → heating coil if fitted → supply fan → discharge/silencer."),
        ("How does an AHU remove moisture from the air?", "The cooling coil chills the air below its dew point, so water vapour condenses on the coil, collects in the drain pan and is drained away."),
        ("What is a TFA and where is it used?", "A treated fresh air unit: an AHU handling 100 % outdoor air, cooling and dehumidifying it before supplying it to floors or FCU zones — common in hotels, offices with FCUs and hospitals."),
        ("Name three BMS points belonging to a supply fan.", "Start/stop command (DO), run status (DI), fault (DI), and speed reference (AO) if it has a VFD."),
        ("Give one advantage and one disadvantage of return air temperature control.", "Advantage: simple — the return air represents the average room temperature. Disadvantage: it can be distorted by ceiling-void heat and duct leakage, and it reacts slowly."),
    ],
)

P2 = dict(
    id="2-2", slug="supply-return-fresh-exhaust-air", title="Supply, return, fresh and exhaust air",
    objectives=[
        "Define supply, return, fresh, mixed and exhaust air.",
        "Explain why buildings need fresh air and why it is expensive.",
        "Calculate mixed air temperature and the fresh air fraction.",
        "Explain building pressurisation and where sensors should be placed.",
    ],
    one_line=("Every AHU handles the same air streams: <strong>fresh air</strong> in from outside, <strong>supply air</strong> "
              "out to the rooms, <strong>return air</strong> back from the rooms and <strong>exhaust air</strong> thrown away — "
              "and the balance between them decides air quality, energy use and building pressure."),
    why=("<p>Fresh air is essential for the people in the building, but in a hot, humid climate it is also the biggest "
         "single cooling load. Get the balance wrong and you either waste energy or leave people in stuffy rooms. Many "
         "BMS points — damper positions, CO₂ readings, mixed air temperature — exist only to manage this balance.</p>"),
    body=(
        fig(d_air_streams(), "Air streams of an AHU serving offices. Temperatures are typical for a hot afternoon.")
        + table(["Air stream", "Also called", "Meaning"], [
            ("Fresh air", "Outdoor air, outside air", "Air drawn in from outside for ventilation."),
            ("Return air", "Recirculated air", "Air drawn back from the rooms to the AHU."),
            ("Mixed air", "—", "The blend of fresh and return air entering the filters and coil."),
            ("Supply air", "Off-coil air, discharge air", "Conditioned air delivered to the rooms."),
            ("Exhaust air", "Relief air, spill air", "Return air pushed out of the building instead of being re-used."),
            ("Transfer air", "—", "Air passing from one room to another, e.g. offices to toilets."),
        ])
        + "<h3>Why fresh air — and why it costs</h3>"
        + "<p>People breathe out CO₂ and moisture; materials give off odours and chemicals. Fresh air dilutes them. "
          "Ventilation standards — ASHRAE 62.1 internationally and the National Building Code in India — set minimum "
          "fresh air rates per person and per floor area. For a typical office this works out at very roughly "
          "8–10 litres per second per person.</p>"
          "<p>On a 35 °C humid afternoon every litre of that air must be cooled and dried to about 13 °C. That is why "
          "buildings do not simply use 100 % fresh air everywhere, and why controlling fresh air to the actual occupancy "
          "(CO₂ control, page 3.2 and Module 6) saves so much energy.</p>"
        + "<h3>Mixed air temperature — a calculation worth knowing</h3>"
        + "<p>Mixed air temperature is the weighted average of the two streams:</p>"
        + callout("note", "Formula", "<p><strong>MAT = (fresh fraction × fresh air temp) + (return fraction × return air temp)</strong></p>"
                  "<p>Example: 20 % fresh air at 35 °C with 80 % return air at 24 °C → MAT = 0.2 × 35 + 0.8 × 24 = 7 + 19.2 = <strong>26.2 °C</strong>.</p>")
        + "<p>Turn it round and you can <em>measure</em> the fresh air fraction from three temperature sensors — a quick "
          "site check that the fresh air damper is really doing what the BMS says:</p>"
        + callout("note", "Fresh air fraction", "<p><strong>Fresh fraction = (MAT − RAT) ÷ (OAT − RAT)</strong></p>"
                  "<p>Example: MAT 26.2 °C, RAT 24 °C, OAT 35 °C → (2.2) ÷ (11) = <strong>0.20, i.e. 20 %</strong>.</p>"
                  "<p>It only works when outdoor and return temperatures are several degrees apart.</p>")
        + "<h3>How much cooling does the air carry?</h3>"
        + "<p>For air, a useful approximation of the sensible cooling delivered is:</p>"
        + callout("note", "Sensible heat", "<p><strong>Cooling (W) ≈ 1.2 × airflow (L/s) × ΔT (K)</strong></p>"
                  "<p>Example: 1,000 L/s supplied at 13 °C into a room at 24 °C → 1.2 × 1,000 × 11 ≈ <strong>13 kW</strong>.</p>")
        + "<h3>Building pressure</h3>"
        + "<p>A building is usually kept <strong>slightly positive</strong> — a little more air supplied than exhausted — so "
          "that dust, heat and humid air do not leak in through doors and gaps. Toilets, kitchens and car parks are kept "
          "<strong>negative</strong> so their smells stay put. Symptoms of the wrong balance: doors that whistle, slam or "
          "are hard to open, and humid air drifting in at entrances.</p>"
        + "<h3>Free cooling (economiser)</h3>"
        + "<p>In mild climates, when outdoor air is cooler and drier than return air, an AHU can open its fresh air damper "
          "fully and cool with outside air for free. In hot, humid climates the opportunity is small — outdoor air is "
          "rarely both cooler <em>and</em> drier — so economiser logic must compare enthalpy (heat <em>and</em> moisture), "
          "not just temperature.</p>"
        + "<h3>Sensor placement matters</h3>"
        + table(["Sensor", "Put it…", "Avoid…"], [
            ("Outdoor air temperature", "In the shade, north-facing, in a ventilated shield", "Direct sun, exhaust outlets, condensing units, roof heat"),
            ("Return air temperature", "In the return duct, away from the mixing box", "Where fresh air can blow back onto it"),
            ("Mixed air temperature", "An averaging sensor across the duct", "A single-point probe — mixed air layers badly"),
            ("Supply air temperature", "Several duct widths downstream of coil and fan, where air is mixed", "Right at the coil face"),
        ])
    ),
    ahu01=("<p>AHU-01's fresh air damper has a <strong>minimum position of 20 %</strong> for the design occupancy. The return "
           "air CO₂ sensor lets the BMS open it further when the floor is busy (Module 6). The return damper is set "
           "manually during balancing. Toilet exhaust fans keep the toilets negative; the offices stay slightly positive.</p>"),
    on_site=[
        "Watch the damper linkages actually move when you command them — a slipped shaft clamp can leave a damper stuck while the actuator turns.",
        "Use the fresh air fraction formula with a hand thermometer to check what the dampers are really doing.",
        "Feel for air movement at entrance doors: strong inward draught means the building is negative.",
        "If an outdoor air sensor reads high every afternoon, look at where the sun reaches it.",
    ],
    faults=[
        ("Outdoor temperature reads 46 °C at 3 pm when the weather service says 36 °C", "Sensor in direct sun or near a hot exhaust", "Sensor location and shield"),
        ("High CO₂ in offices", "Fresh air damper stuck or minimum position too low", "Damper position on site vs BMS; actuator and linkage"),
        ("Entrance doors whistle; humid air at the lobby", "Building negative: exhaust exceeds supply", "Exhaust fan operation, fresh air dampers, AHU airflow"),
        ("Mixed air temperature jumps around", "Single-point sensor in stratified air", "Fit an averaging sensor"),
    ],
    terms=[
        ("Fresh air", "Outdoor air brought in for ventilation."),
        ("Return air", "Air drawn back from the rooms to the AHU."),
        ("Mixed air", "Blend of fresh and return air entering the coil."),
        ("Supply air", "Conditioned air delivered to the rooms."),
        ("Exhaust (relief) air", "Air discharged to outside."),
        ("Fresh air fraction", "Share of fresh air in the mixed air, e.g. 20 %."),
        ("Building pressurisation", "Keeping a building slightly above outdoor pressure."),
        ("Economiser", "Using cool outdoor air instead of mechanical cooling when conditions allow."),
        ("Enthalpy", "Total heat content of air, including the heat held in its moisture."),
    ],
    scenarios=[dict(
        prompt="On a hot afternoon AHU-02 shows OAT 34 °C, RAT 24 °C and MAT 24.3 °C. The BMS says the fresh air damper is at 30 %. What does this tell you?",
        options=["Everything is normal.",
                 "Very little fresh air is actually entering — about 3 % — so the damper or its linkage is probably not where the BMS thinks it is.",
                 "The building has too much fresh air."],
        answer=1,
        explain=(" Fresh fraction = (24.3 − 24) ÷ (34 − 24) = 0.03. If the damper were really at 30 %, MAT would be about 27 °C. "
                 "Check the damper on site: actuator, shaft clamp, linkage — or a blocked intake."),
    )],
    questions=[
        ("Define mixed air.", "The blend of fresh (outdoor) air and return air that enters the filters and coil."),
        ("Calculate MAT for 25 % fresh air at 36 °C and 75 % return air at 24 °C.", "0.25 × 36 + 0.75 × 24 = 9 + 18 = 27 °C."),
        ("Why is fresh air the largest cooling load in a hot, humid climate?", "Every litre must be cooled from outdoor temperature (e.g. 35 °C) and dried — removing moisture takes a lot of energy — whereas return air is already near room conditions."),
        ("Why are buildings kept slightly positive?", "So that unconditioned, dusty or humid outdoor air does not leak in through doors and gaps."),
        ("Where should an outdoor air temperature sensor be mounted?", "In the shade (north-facing), in a ventilated radiation shield, away from exhausts, condensing units and hot roof surfaces."),
    ],
)

P3 = dict(
    id="2-3", slug="fan-coil-unit", title="Fan coil unit (FCU)",
    objectives=[
        "Describe the parts of an FCU and how it cools a room.",
        "Explain 2-pipe and 4-pipe systems and the valve and fan options.",
        "Describe how a room thermostat controls an FCU.",
        "List the points a BMS reads and writes on a networked FCU.",
    ],
    one_line=("An FCU is a small, local air-conditioning unit — <strong>a fan blowing room air over a chilled water coil</strong> — "
              "serving one room or zone, usually controlled by its own room thermostat or small controller."),
    why=("<p>A large building can have hundreds of FCUs — in hotel rooms, cabins, meeting rooms. Individually they are simple, "
         "but together they are a big share of the BMS points, the network traffic and the comfort complaints. Knowing how "
         "an FCU and its thermostat work lets you fix most room-level problems quickly.</p>"),
    body=(
        fig(d_fcu(), "A ceiling-concealed FCU with an on/off chilled water valve and a networked room thermostat.")
        + table(["Part", "Job", "Typical control or point"], [
            ("Return grille and filter", "Draws room air in and catches dust", "—"),
            ("Chilled water coil", "Cools and dehumidifies the air", "—"),
            ("Valve and actuator", "Lets chilled water through the coil", "On/off (thermal or motorised) or modulating 0–10 V"),
            ("Fan and motor", "Moves the air", "3-speed (low/medium/high relays) or EC motor with 0–10 V speed"),
            ("Drain pan", "Collects condensate", "Float switch to stop the unit or alarm (optional)"),
            ("Room thermostat / controller", "Measures temperature, holds the setpoint, drives fan and valve", "Often networked to the BMS"),
        ])
        + "<h3>Types and piping</h3>"
        + cards([
            ("Ceiling concealed (ducted)", "Hidden above the ceiling with short ducts to diffusers. Offices, hotels."),
            ("Cassette", "Ceiling-mounted with a 4-way outlet. Shops, meeting rooms."),
            ("Wall or floor mounted", "Exposed units; older buildings and retrofits."),
            ("2-pipe vs 4-pipe", "2-pipe: one coil, chilled water only (or changeover). 4-pipe: separate cooling and heating coils, each with a valve."),
        ])
        + "<h3>How the thermostat controls it</h3>"
        + steps([
            "The thermostat measures room temperature and compares it with the setpoint (e.g. 24 °C).",
            "If the room is warmer than the setpoint plus half the <strong>deadband</strong> (a small band, e.g. ±0.5 K, in which nothing changes), it opens the valve.",
            "The further the room is above setpoint, the higher the fan speed: low, then medium, then high (or a higher 0–10 V signal on an EC fan).",
            "When the room is satisfied the valve closes. The fan either keeps running at low speed (for air movement and fresh air) or stops, depending on the setting.",
        ])
        + callout("tip", "Why a deadband?",
                  "<p>Without one, an on/off valve would open and close every few seconds as the temperature crossed the "
                  "setpoint, wearing out the actuator and annoying occupants. The deadband gives the room some room to "
                  "drift before the controller acts.</p>")
        + "<h3>Fresh air for FCU zones</h3>"
        + "<p>An FCU only recirculates room air. Fresh air usually comes from a separate <strong>TFA</strong> unit through "
          "ducts into each room or into the FCU's return plenum. If the TFA stops, the FCUs still cool — but the rooms go "
          "stuffy.</p>"
        + "<h3>Connecting FCUs to the BMS</h3>"
        + "<p>Most FCU controllers are application-specific controllers or networked thermostats on an RS485 field bus "
          "(BACnet MS/TP or Modbus RTU). Typical points:</p>"
        + table(["Point", "Read / write", "Use"], [
            ("On/off command", "Write", "Switch the FCU from the BMS schedule"),
            ("Occupancy (occupied / unoccupied / standby)", "Write", "Schedule, key-card or occupancy sensor"),
            ("Setpoint and setpoint limits", "Read / write", "Central setpoint; limit how far occupants can change it"),
            ("Room temperature", "Read", "Monitoring, trends, alarms"),
            ("Fan speed and mode", "Read / write", "Monitoring and override"),
            ("Valve status or position", "Read", "Shows cooling demand"),
            ("Alarms — filter, condensate, sensor", "Read", "Maintenance"),
        ])
        + table(["", "FCU", "AHU"], [
            ("Serves", "One room or small zone", "A floor or a large zone"),
            ("Fresh air", "None of its own — needs a TFA", "Built in (fresh air damper)"),
            ("Control", "Room thermostat or small ASC", "Programmable plant controller"),
            ("BMS points per unit", "About 5–15, usually over a field bus", "About 15–40, mostly hard-wired"),
        ], "plain")
    ),
    ahu01=("<p>The meeting rooms and cabins on AHU-01's floor use <strong>FCUs with networked thermostats</strong> on a "
           "BACnet MS/TP field bus to the floor's supervisory controller (the “FCU controller” box in the page 1.2 diagram). "
           "Their schedules follow AHU-01's, so the whole floor switches together.</p>"),
    on_site=[
        "Check where the thermostat is mounted: not in sun, not near a door, not above a printer or kettle.",
        "Many valve actuators have a manual-open lever or button for flushing — find out if one was left open.",
        "Lift a ceiling tile and look at the drain pan when investigating a leak or smell.",
        "On a new network of FCUs, check every address is unique before connecting the bus (Module 5).",
        "Compare the thermostat reading with a hand-held thermometer at the same spot.",
    ],
    faults=[
        ("Room too cold even at a high setpoint", "Valve stuck open, manual override lever set, or actuator failed open", "Valve status, actuator, manual lever"),
        ("Room too warm; fan runs; valve shows open", "No chilled water flow: isolation valve shut, air lock, blocked strainer", "Feel the pipes — is the CHW pipe cold on both sides of the valve?"),
        ("Water dripping from the ceiling", "Blocked drain, failed condensate pump, or pan overflowing", "Drain pan, drain line, pump"),
        ("FCU offline on the BMS; others on the same bus OK", "Address or power problem at that unit", "Power to the controller, address, bus wiring at that unit"),
        ("All FCUs on one bus offline", "Bus wiring, termination or supervisory controller fault", "Module 5 troubleshooting"),
    ],
    terms=[
        ("FCU", "Fan coil unit: fan plus chilled water coil serving one room or zone."),
        ("2-pipe / 4-pipe", "One coil with one supply and return, or separate cooling and heating coils."),
        ("Deadband", "A band around the setpoint in which the controller takes no action."),
        ("EC motor", "Electronically commutated fan motor with stepless speed control, usually 0–10 V."),
        ("Thermal actuator", "Slow on/off valve actuator driven by a small heater element."),
        ("Occupancy mode", "Occupied, unoccupied or standby — changes setpoints and fan behaviour."),
        ("Condensate pump", "Small pump lifting condensate to a drain when gravity drainage is not possible."),
    ],
    scenarios=[dict(
        prompt="A meeting room is too cold. Its thermostat shows setpoint 24 °C, room 20 °C, fan on low, valve status closed. The CHW pipe after the valve is cold to the touch. What is the likely cause?",
        options=["The thermostat is reading wrong.",
                 "Water is passing through a valve that should be closed — the valve is stuck or its manual lever is set open.",
                 "The TFA is supplying too much fresh air."],
        answer=1,
        explain=(" The controller has closed the valve, yet chilled water still flows — the pipe after the valve is cold. The valve "
                 "is passing: stuck, damaged, or left on manual override. Check the actuator and the manual lever."),
    )],
    questions=[
        ("What does an FCU not provide that an AHU does?", "Fresh air — an FCU only recirculates room air. Fresh air comes from a separate TFA."),
        ("Why does an FCU thermostat use a deadband?", "To stop the valve and fan switching on and off rapidly around the setpoint."),
        ("Explain the difference between 2-pipe and 4-pipe FCUs.", "2-pipe has one coil with one supply and return pipe (cooling only, or changeover). 4-pipe has separate cooling and heating coils, each with its own pipes and valve."),
        ("Name four points a BMS typically reads or writes on a networked FCU.", "Any four of: on/off, occupancy mode, setpoint, room temperature, fan speed, valve status, alarms."),
        ("A whole floor of FCUs goes offline at once. What kind of fault does that suggest?", "A shared fault: the field-bus wiring, termination, power, or the supervisory controller — not the individual units."),
    ],
)

P4 = dict(
    id="2-4", slug="vav-and-cav-systems", title="VAV and CAV systems",
    objectives=[
        "Explain the difference between CAV and VAV.",
        "Describe how a pressure-independent VAV box controls a zone.",
        "Explain how the AHU fan is controlled in a VAV system.",
        "Use the fan affinity laws to explain why VAV saves energy.",
    ],
    one_line=("A <strong>CAV</strong> system always delivers the same airflow and varies the supply temperature; a "
              "<strong>VAV</strong> system keeps the supply temperature roughly constant and varies the airflow to each zone."),
    why=("<p>Most modern multi-zone office AHUs are VAV. They save a lot of fan energy, but they add a second layer of control "
         "— a box and controller in every zone, and a fan speed loop on the AHU — that must be set up correctly. Many "
         "comfort and noise complaints in VAV buildings are really control problems.</p>"),
    body=(
        fig(d_cav_vav(), "Left: one zone, fixed airflow. Right: several zones, each with its own VAV box, and the AHU fan following duct pressure.")
        + table(["", "CAV — constant air volume", "VAV — variable air volume"], [
            ("Airflow", "Fixed", "Varies with each zone's demand"),
            ("What varies", "Supply air temperature (coil valve)", "Airflow to each zone (box dampers); fan speed follows"),
            ("Zones", "Usually one per AHU", "Many per AHU, each with its own thermostat"),
            ("Fan energy", "Constant", "Much lower at part load"),
            ("Complexity", "Simple", "More controllers, more tuning"),
            ("Good for", "Halls, lobbies, auditoriums, process areas", "Multi-zone offices"),
        ], "plain")
        + "<h3>Inside a VAV box</h3>"
        + "<p>A VAV box (terminal unit) sits in the duct above the ceiling. It has an <strong>inlet flow sensor</strong> "
          "(usually a cross-shaped tube measuring velocity pressure), a <strong>damper</strong> with an actuator, a small "
          "<strong>controller</strong>, and sometimes a <strong>reheat coil</strong>. Most modern boxes are "
          "<strong>pressure-independent</strong>: they control <em>airflow</em>, not damper position, so a pressure change "
          "in the duct does not upset the room.</p>"
        + fig(d_vav_cascade(), "Two loops in cascade: room temperature decides how much air is needed; the flow loop delivers exactly that.")
        + steps([
            "The zone sensor reads 25.1 °C against a 24 °C setpoint.",
            "The <strong>temperature loop</strong> calculates the airflow needed — somewhere between the box's <strong>minimum</strong> (for ventilation) and <strong>maximum</strong> (design) airflow.",
            "The <strong>flow loop</strong> moves the damper until the measured airflow matches that setpoint.",
            "If duct pressure changes, the flow loop corrects the damper straight away — the room never notices.",
        ])
        + "<h3>Controlling the AHU fan</h3>"
        + "<p>As boxes close, pressure in the supply duct rises. A <strong>duct static pressure sensor</strong>, usually about "
          "two-thirds of the way along the longest duct run, measures it. A PID loop varies the fan's VFD to hold a "
          "setpoint chosen during commissioning (often a few hundred pascals). The supply air temperature is held at about "
          "13 °C by the coil valve, as in any AHU.</p>"
        + callout("tip", "Static pressure reset",
                  "<p>A fixed pressure setpoint is usually higher than needed most of the time. With <strong>trim and respond</strong> "
                  "reset, the BMS lowers the setpoint a little at a time until one box damper is nearly fully open, and raises it "
                  "when boxes report they are starved. Same comfort, less fan energy and less noise. ASHRAE Guideline 36 "
                  "describes standard sequences for this.</p>")
        + "<h3>Why VAV saves so much energy: the fan laws</h3>"
        + table(["When fan speed changes by…", "Airflow changes by…", "Pressure changes by…", "Power changes by…"], [
            ("100 % → 80 %", "80 %", "64 % (0.8²)", "≈ 51 % (0.8³)"),
            ("100 % → 60 %", "60 %", "36 %", "≈ 22 %"),
            ("100 % → 50 %", "50 %", "25 %", "≈ 13 %"),
        ], "plain")
        + "<p>Power falls with the <strong>cube</strong> of speed: running at 80 % speed needs only about half the power. "
          "Real systems save a little less than the ideal law suggests, but the savings are still large.</p>"
    ),
    ahu01=("<p>AHU-01 is run as a <strong>constant-volume</strong> AHU: its VFD is set to a fixed commissioned speed (42 Hz) and "
           "its valve controls return air temperature. Its <strong>duct static pressure sensor</strong> is used for monitoring "
           "and a high-pressure alarm. If VAV boxes were added to the floor, the VFD would be switched to control that "
           "pressure — the sensor is already in place.</p>"),
    on_site=[
        "Check every VAV box's minimum and maximum airflow against the design schedule.",
        "The flow sensor's two tubes (high and low) must not be swapped, kinked or blocked — the controller will read nonsense.",
        "Look at the duct static pressure sensor's tubing as well as its reading: a loose tube is a common cause of runaway fans.",
        "Check damper rotation: does “open” on the BMS really open the damper?",
        "Trend fan speed and the most-open box damper together — they show whether the pressure setpoint is right.",
    ],
    faults=[
        ("Zone hot; its box damper is 100 % open but airflow is low", "Duct pressure too low, or AHU not delivering enough air", "Duct static pressure, AHU fan speed, other boxes"),
        ("Diffusers whistle; fan runs fast", "Static pressure setpoint too high", "Setpoint; consider trim-and-respond reset"),
        ("After maintenance the fan runs at 50 Hz and pressure reads 0 Pa", "Static pressure sensor tube disconnected", "Sensor tubes and connections"),
        ("Box airflow reads 0 with the damper open", "Flow sensor tubes blocked or swapped", "Tubes at the flow cross and controller"),
        ("Zone always cold at low load", "Minimum airflow too high for the load, no reheat", "Box minimum airflow setting"),
    ],
    terms=[
        ("CAV", "Constant air volume — fixed airflow, varying supply temperature."),
        ("VAV", "Variable air volume — varying airflow to each zone at roughly constant supply temperature."),
        ("VAV box", "Terminal unit with a damper, flow sensor and controller serving one zone."),
        ("Pressure-independent", "A box that controls airflow, so duct pressure changes do not affect the room."),
        ("Duct static pressure", "Pressure inside the supply duct relative to the surroundings; used to control the fan."),
        ("Trim and respond", "Reset method that lowers a setpoint until a zone asks for more."),
        ("Fan affinity laws", "Flow ∝ speed, pressure ∝ speed², power ∝ speed³."),
        ("Minimum airflow", "The lowest airflow a box may supply, for ventilation and air distribution."),
    ],
    scenarios=[dict(
        prompt="After a filter change on AHU-02 (a VAV AHU), its VFD runs at 50 Hz, diffusers whistle and duct static pressure on the BMS reads 0 Pa. What has most likely happened?",
        options=["The VAV boxes have all failed closed.",
                 "The static pressure sensor's tube was knocked off, so the sensor sees no pressure and the loop drives the fan to maximum.",
                 "The filter was fitted backwards."],
        answer=1,
        explain=(" The loop sees 0 Pa, far below setpoint, so it ramps the fan to full speed — while real duct pressure is very high. "
                 "Reconnect the tube. A good program also alarms on “fan at maximum with pressure near zero”."),
    )],
    questions=[
        ("What varies in a CAV system and what varies in a VAV system?", "CAV: airflow is fixed; supply temperature varies. VAV: supply temperature is roughly constant; airflow to each zone varies."),
        ("What does “pressure-independent” mean for a VAV box?", "The box controls measured airflow, not just damper position, so it compensates automatically for changes in duct pressure."),
        ("How is the AHU fan controlled in a VAV system?", "A PID loop varies the VFD to hold duct static pressure, measured about two-thirds of the way down the duct, at its setpoint."),
        ("A fan slows from 100 % to 70 % speed. Roughly what power does it need?", "0.7³ ≈ 0.34, so about a third of full-speed power."),
        ("Why does a VAV box have a minimum airflow?", "To keep supplying enough fresh air for ventilation and enough air movement for good distribution, even when the zone needs little cooling."),
    ],
)

P5 = dict(
    id="2-5", slug="chilled-water-system-chiller-plant", title="Chilled water system and chiller plant",
    objectives=[
        "Trace the chilled water loop from the chillers to the coils and back.",
        "Explain the main pumping arrangements: primary-secondary and variable primary.",
        "Describe how chillers are started, staged and stopped.",
        "Use the water-side cooling formula and explain low ΔT syndrome.",
    ],
    one_line=("A chiller plant <strong>makes chilled water</strong> (typically about 6–7 °C) and pumps it to the AHU and FCU coils; "
              "the water returns warmer (about 12–13 °C) and goes back to the chillers to be cooled again."),
    why=("<p>The chiller plant is usually the biggest energy user in the building and the most complex sequence on the BMS. "
         "Even if you never program one yourself, you need to understand it: when AHUs cannot cool, the cause is often "
         "in the plant room.</p>"),
    body=(
        fig(d_chw_plant(), "A primary-secondary plant: constant flow through the chillers, variable flow to the buildings, joined by a decoupler.")
        + "<h3>What a chiller does</h3>"
        + "<p>A chiller is a refrigeration machine. Refrigerant evaporates in the <strong>evaporator</strong>, taking heat out of "
          "the chilled water. The <strong>compressor</strong> raises the refrigerant's pressure and temperature. In the "
          "<strong>condenser</strong> the refrigerant gives that heat away — to outdoor air (air-cooled chillers) or to "
          "condenser water and a cooling tower (water-cooled chillers, page 2.6). An <strong>expansion valve</strong> drops "
          "the pressure again and the cycle repeats. The chiller's own controller runs all of this; the BMS enables it, "
          "watches it and may reset its setpoint.</p>"
        + callout("note", "Cooling capacity",
                  "<p><strong>Cooling (kW) = 4.19 × flow (L/s) × ΔT (K)</strong> &nbsp;·&nbsp; <strong>1 TR (ton of refrigeration) = 3.517 kW</strong></p>"
                  "<p>Example: 20 L/s through a coil, 7 °C in and 12.5 °C out → 4.19 × 20 × 5.5 ≈ <strong>461 kW ≈ 131 TR</strong>.</p>")
        + "<h3>Pumping arrangements</h3>"
        + table(["Arrangement", "How it works", "Notes"], [
            ("Constant primary", "Fixed-speed pumps push constant flow through chillers and 3-way valves at the coils", "Older, simple; wastes pump energy"),
            ("Primary-secondary", "Constant-flow primary pumps serve the chillers; variable-speed secondary pumps serve the building; a decoupler pipe joins the two", "Very common; robust"),
            ("Variable primary flow (VPF)", "One set of variable-speed pumps through chillers and building; a bypass valve keeps minimum chiller flow", "Saves pump energy; needs careful control"),
        ])
        + "<p>With 2-way valves at the coils, building flow falls as valves close. The secondary (or VPF) pumps are slowed "
          "to hold a <strong>differential pressure</strong> measured across the far end of the system (the <em>index circuit</em>), "
          "so even the most remote coil always has enough pressure.</p>"
        + "<h3>The chiller start sequence</h3>"
        + steps([
            "Cooling is needed (schedule, outdoor temperature or demand from AHUs).",
            "Open the chiller's isolation valves (if motorised) and start its <strong>chilled water pump</strong>.",
            "<strong>Prove chilled water flow</strong> (flow switch or the chiller's own flow sensing).",
            "For a water-cooled chiller: start the <strong>condenser water pump</strong> and the cooling tower; prove condenser flow.",
            "<strong>Enable the chiller.</strong> Its own controller starts the compressor and loads up to hold its leaving water setpoint.",
            "Stopping is the reverse: disable the chiller, then keep the pumps running for a few minutes (<strong>run-on</strong>) before stopping them.",
        ])
        + callout("warn", "Never without flow",
                  "<p>A chiller must never run without proven water flow through its evaporator and condenser — the water can "
                  "freeze in the evaporator or the pressure can trip the machine. Flow proving is an interlock, not an option.</p>")
        + "<h3>Staging: how many chillers?</h3>"
        + bullets([
            "<strong>Stage up</strong> (start another chiller) when the running chillers are near full load for a sustained time, or supply water stays above setpoint — e.g. above 90 % load for 15 minutes, or CHW supply more than 1 K above setpoint.",
            "<strong>Stage down</strong> when the remaining chillers could carry the load with margin — e.g. total load would be under about 70–80 % of the remaining capacity for 15 minutes.",
            "Use <strong>time delays</strong> and minimum run and off times so chillers do not short-cycle.",
            "<strong>Rotate the lead chiller</strong> by run-hours so wear is shared.",
        ])
        + table(["Typical plant points", "Type"], [
            ("Chiller enable, run status, common fault", "DO, DI, DI (hard-wired)"),
            ("Chiller details: leaving temp, load %, kW, alarms", "BACnet or Modbus"),
            ("CHW supply and return header temperatures", "AI"),
            ("Pump start/stop, status, fault, speed", "DO, DI, DI, AO"),
            ("Flow switches / flow meters", "DI / AI or pulse"),
            ("Index differential pressure", "AI"),
            ("Bypass valve (VPF)", "AO"),
        ], "plain")
        + "<h3>Low ΔT syndrome</h3>"
        + "<p>Chillers are designed for a certain temperature difference — say 5.5 K. If water comes back from the building "
          "<em>too cold</em> (a small ΔT), each chiller can only deliver part of its capacity, so more chillers and pumps run "
          "for the same load. Causes include 3-way valves, valves stuck open or passing, coils fouled, setpoints set too "
          "low, and too much flow forced through coils. Trending CHW return temperature is one of the best checks of plant "
          "health.</p>"
    ),
    ahu01=("<p>AHU-01's coil is one of the loads on the secondary loop. Its 2-way valve takes as much 7 °C water as it needs. "
           "As the floor cools and the valve closes, the index ΔP rises and the secondary pumps slow down. Its design is "
           "7 °C in and about 12.5 °C out — if it returns colder than that, AHU-01 is contributing to low ΔT.</p>"),
    on_site=[
        "Treat the chiller's own controller as the authority for the machine. The BMS enables it and may reset its setpoint — it does not run the compressor.",
        "Check strainers and isolation valves whenever flow is low or a chiller trips on flow.",
        "Record the CHW supply and return temperatures every visit; a shrinking ΔT is an early warning.",
        "Know where the index ΔP sensor is and what its setpoint is — it decides every pump's speed.",
    ],
    faults=[
        ("CHW supply temperature creeping up; chiller running", "Chiller at full load (stage up needed), or limited by a fault or condenser problem", "Chiller load %, alarms, condenser water temperature"),
        ("Three chillers running, each lightly loaded; ΔT only 2.5 K", "Low ΔT syndrome", "Coil valves, 3-way valves, setpoints"),
        ("Chiller trips on low flow", "Blocked strainer, pump fault, closed valve", "Strainer ΔP, pump status, valve positions"),
        ("BMS enables chiller but it does not start", "Interlocks not made (flow not proven), chiller in local mode or in alarm", "Flow proving, chiller panel local/remote switch, alarms"),
        ("Secondary pumps hunting", "ΔP loop tuned too aggressively, or sensor noisy", "Trend ΔP and pump speed; PID settings"),
    ],
    terms=[
        ("Chiller", "Refrigeration machine that produces chilled water."),
        ("Evaporator / condenser", "Heat exchangers where the refrigerant takes heat from chilled water and gives it to air or condenser water."),
        ("Primary-secondary", "Pumping arrangement with constant chiller flow and variable building flow, joined by a decoupler."),
        ("Variable primary flow", "Single set of variable-speed pumps serving chillers and building."),
        ("Decoupler", "Short pipe joining the primary and secondary loops so their flows can differ."),
        ("Index circuit", "The hydraulically furthest circuit, where the ΔP sensor is placed."),
        ("Staging", "Starting or stopping chillers to match the load."),
        ("TR", "Ton of refrigeration = 3.517 kW of cooling."),
        ("Low ΔT syndrome", "Chilled water returning too cold, so chillers cannot load fully."),
    ],
    scenarios=[dict(
        prompt="Three chillers are running, each at about 40 % load. CHW supply is 7 °C but the return is only 9.5 °C (design 12.5 °C). What is the plant suffering from?",
        options=["Too few chillers running.", "Low ΔT syndrome — too much flow through the coils for the load.",
                 "A failed CHW supply sensor."],
        answer=1,
        explain=(" With a ΔT of 2.5 K instead of 5.5 K, each chiller can deliver less than half its capacity, so extra chillers and pumps "
                 "run. Look for passing or stuck-open coil valves, 3-way valves and low supply air setpoints."),
    )],
    questions=[
        ("Name the four main parts of the refrigeration cycle in a chiller.", "Evaporator, compressor, condenser, expansion valve."),
        ("Calculate the cooling for 15 L/s with a 5 K temperature difference.", "4.19 × 15 × 5 ≈ 314 kW ≈ 89 TR."),
        ("What does the decoupler do in a primary-secondary plant?", "Joins the primary and secondary loops so the chiller flow (constant) and building flow (variable) can differ; the difference flows through the decoupler."),
        ("List the start sequence for a water-cooled chiller.", "Start CHW pump → prove CHW flow → start CW pump and tower → prove CW flow → enable chiller."),
        ("What is low ΔT syndrome and why is it costly?", "Chilled water returning too cold. Each chiller can only deliver part of its capacity, so more chillers and pumps run than the load needs."),
    ],
)

P6 = dict(
    id="2-6", slug="cooling-tower", title="Cooling tower and condenser water",
    objectives=[
        "Explain what a cooling tower does and how evaporative cooling works.",
        "Define range, approach and wet-bulb temperature.",
        "Describe how tower fans are controlled and sequenced with chillers.",
        "List the main cooling tower points, including water treatment.",
    ],
    one_line=("A cooling tower <strong>rejects the heat</strong> that water-cooled chillers take out of the building, by evaporating "
              "a small part of the condenser water into the outside air."),
    why=("<p>Heat removed from every room has to go somewhere. In water-cooled plants it leaves through the cooling tower. If the "
         "tower cannot reject heat — fans off, fill clogged, a very humid day — the chillers lose capacity and eventually trip. "
         "Tower control also has a direct effect on chiller efficiency.</p>"),
    body=(
        fig(d_cooling_tower(), "Heat travels: room → air → chilled water → refrigerant → condenser water → outdoor air.")
        + "<h3>How it works</h3>"
        + steps([
            "Warm condenser water (about 37 °C) from the chiller is sprayed over the <strong>fill</strong> — a large surface of thin plastic sheets.",
            "The <strong>fan</strong> draws outdoor air up through the fill.",
            "A small part of the water <strong>evaporates</strong>. Evaporation takes a lot of heat, so the rest of the water cools.",
            "Cooled water (about 32 °C) collects in the <strong>basin</strong> and the condenser water pump sends it back to the chiller.",
        ])
        + "<h3>Range, approach and wet-bulb</h3>"
        + fig(d_range_approach(), "Typical design values for a hot, humid climate.", small=True)
        + table(["Term", "Meaning", "Typical"], [
            ("Wet-bulb temperature", "The lowest temperature water can be cooled to by evaporation; depends on humidity. It is the tower's limit — not the ordinary (dry-bulb) temperature.", "26–29 °C on humid Indian summer days"),
            ("Range", "Water in minus water out (CW return − CW supply)", "About 5 K"),
            ("Approach", "Water out minus wet-bulb (CW supply − wet-bulb)", "About 3–5 K"),
        ])
        + callout("warn", "You cannot beat the wet-bulb",
                  "<p>Condenser water leaving the tower can never be colder than the wet-bulb temperature, and in practice not "
                  "closer than the approach. A setpoint of 26 °C on a day with a 28 °C wet-bulb will simply run every fan at "
                  "full speed for nothing.</p>")
        + "<h3>Controlling the fans</h3>"
        + "<p>The BMS holds the <strong>condenser water supply temperature</strong> (water leaving the tower) at a setpoint by "
          "varying fan speed (VFDs) or by switching fans or cells on and off. Colder condenser water makes the chiller more "
          "efficient but costs fan energy; and each chiller has a <strong>minimum</strong> condenser water temperature it "
          "needs to run properly. The best setpoint often <em>floats</em> with the wet-bulb (e.g. wet-bulb + approach).</p>"
        + "<p>The heat rejected is more than the cooling load — the tower also gets rid of the compressor's energy — "
          "typically about 1.2–1.3 times the cooling delivered.</p>"
        + "<h3>Water and water treatment</h3>"
        + "<p>Evaporation leaves minerals behind, so the water gets steadily more concentrated. A <strong>conductivity</strong> "
          "sensor opens a <strong>blowdown</strong> valve to drain some concentrated water, and a float or level control adds "
          "<strong>make-up water</strong>. Chemical dosing controls scale, corrosion and bacteria — including "
          "<em>Legionella</em>, which is why towers need regular cleaning and treatment records.</p>"
        + table(["Typical tower points", "Type"], [
            ("Fan start/stop, run status, fault, speed", "DO, DI, DI, AO"),
            ("Vibration switch", "DI (stops the fan on high vibration)"),
            ("CW supply and return temperature", "AI"),
            ("Basin level high / low", "DI"),
            ("Make-up water meter", "Pulse input"),
            ("Conductivity / blowdown valve", "AI / DO"),
            ("Cell isolation valves (multi-cell)", "DO + end-switch DI"),
            ("Outdoor wet-bulb (or temperature + humidity)", "AI / calculated"),
        ], "plain")
    ),
    ahu01=("<p>AHU-01 has no direct link to the tower, but the heat it removes from the 3rd floor ends up there. On a very humid "
           "afternoon, if the towers struggle, the chillers lose capacity, CHW supply temperature rises — and AHU-01's valve "
           "goes to 100 % without bringing the floor down. Plant-room problems show up as office complaints.</p>"),
    on_site=[
        "Check fan rotation and the vibration switch after any motor or belt work.",
        "Look at the basin level and the make-up valve; an overflowing basin wastes water and chemicals.",
        "Compare CW supply temperature with the current wet-bulb before calling the tower faulty.",
        "Make sure isolation valves on unused cells are closed, or water bypasses the working fill.",
    ],
    faults=[
        ("CW supply high; chiller trips on high condenser pressure", "Tower fans off or tripped, fouled fill, very high wet-bulb, low CW flow", "Fan status, fill condition, wet-bulb, CW pump"),
        ("Basin overflowing", "Make-up float or valve stuck open", "Make-up valve and level control"),
        ("Tower fan trips repeatedly", "Vibration switch: unbalanced fan, loose mounting", "Fan blades, bearings, mountings"),
        ("Fans cycle on and off every few minutes", "No deadband or minimum run time in the staging logic", "Staging parameters"),
        ("Water use much higher than normal", "Blowdown stuck open, or drift losses", "Blowdown valve, conductivity setpoint, drift eliminators"),
    ],
    terms=[
        ("Cooling tower", "Device that cools condenser water by evaporating part of it into outdoor air."),
        ("Condenser water (CW)", "Water loop carrying heat from the chiller's condenser to the tower."),
        ("Fill", "Large-surface packing that spreads water so it evaporates efficiently."),
        ("Wet-bulb temperature", "Lowest temperature reachable by evaporative cooling; set by air humidity."),
        ("Range", "CW return temperature minus CW supply temperature."),
        ("Approach", "CW supply temperature minus wet-bulb temperature."),
        ("Blowdown", "Draining some tower water to limit mineral concentration."),
        ("Make-up water", "Fresh water added to replace evaporation, drift and blowdown."),
    ],
    scenarios=[dict(
        prompt="The outdoor wet-bulb is 28 °C. An operator has set the condenser water supply setpoint to 26 °C “to save chiller energy”. What happens?",
        options=["The chillers become far more efficient.", "The tower fans run flat out all day and still never reach 26 °C — wasted fan energy.",
                 "The chiller trips on low condenser temperature."],
        answer=1,
        explain=(" Water leaving the tower cannot be colder than the wet-bulb (28 °C) and realistically stays a few degrees above it. "
                 "Set the setpoint at wet-bulb + approach, or let it float, respecting the chiller's minimum."),
    )],
    questions=[
        ("How does a cooling tower cool water?", "By evaporation: a small part of the water evaporates into air drawn through the fill, taking heat with it and cooling the rest."),
        ("Define range and approach.", "Range = CW return − CW supply. Approach = CW supply − wet-bulb temperature."),
        ("Why is the wet-bulb temperature, not the dry-bulb, the tower's limit?", "Evaporation can only cool water down to the wet-bulb temperature, which depends on the air's humidity."),
        ("What is blowdown and why is it needed?", "Draining part of the tower water so that minerals concentrated by evaporation do not build up into scale and corrosion."),
        ("Name four cooling tower points.", "Any four of: fan start/stop, run status, fault, speed, vibration switch, CW supply and return temperature, basin level, make-up water meter, conductivity, blowdown valve."),
    ],
)

P7 = dict(
    id="2-7", slug="hvac-control-sequences", title="HVAC control sequences — an overview",
    objectives=[
        "Explain what a sequence of operation is and why it matters.",
        "List the sections a good sequence contains.",
        "Recognise the operating modes of a plant item.",
        "Write sequence steps that are clear, testable and include failure behaviour.",
    ],
    one_line=("A <strong>sequence of operation</strong> is the written, step-by-step description of exactly how a piece of plant "
              "must start, run, stop and react to faults — the specification the BMS program is built from and tested against."),
    why=("<p>The program in a controller is only as good as the sequence behind it. A clear sequence lets the designer, the "
         "programmer, the commissioning engineer and the operator all agree on what the plant should do. A vague one "
         "(“the AHU shall be controlled as required”) leads to arguments, rework and buildings that never quite work.</p>"),
    body=(
        "<h3>What a complete sequence covers</h3>"
        + table(["Section", "Answers the question"], [
            ("Equipment and points", "What plant and which points are involved?"),
            ("Operating modes", "Occupied, unoccupied, fire, maintenance, hand — what changes in each?"),
            ("Enable conditions (permissives)", "What must be true before it may start?"),
            ("Start sequence", "In what order do things happen, with what delays and proofs?"),
            ("Normal control", "Which loops run, to which setpoints, with what limits?"),
            ("Stop sequence", "In what order does it shut down?"),
            ("Interlocks and safeties", "What must stop it, regardless of the program?"),
            ("Alarms", "What is alarmed, with what limits, delays and priorities?"),
            ("Failure responses", "What happens if a sensor fails, communication is lost or power returns?"),
            ("Adjustable parameters", "Which setpoints and timers can an operator change, and within what limits?"),
        ])
        + "<h3>Operating modes</h3>"
        + fig(d_modes(), "Modes of a plant item. Fire mode overrides everything; Hand means the BMS is not in control.")
        + "<h3>A short example: AHU-01</h3>"
        + steps([
            "<strong>Enable:</strong> when the schedule is Occupied (or an operator override is active), and the HOA is in Auto, and there is no fire signal or latched fan fault.",
            "<strong>Start:</strong> command the fresh air damper to minimum (20 %), then start the supply fan.",
            "<strong>Prove:</strong> if run status is not received within 30 s, raise “fan fail”, stop the fan and lock out until reset.",
            "<strong>Control:</strong> after 60 s, enable the PID loop holding return air at 24 °C (adjustable 22–26 °C) by modulating the CHW valve; modulate the fresh air damper on return CO₂.",
            "<strong>Stop:</strong> at the end of occupancy, close the valve, stop the fan, then close the fresh air damper.",
            "<strong>Fire:</strong> on a fire signal the fan stops immediately via the hard-wired trip; the BMS closes the valve and damper and raises a critical alarm.",
        ])
        + "<p>Lab 3 turns this summary into a complete, testable sequence; page 6.1 explains every step.</p>"
        + "<h3>How to write a good sequence</h3>"
        + bullets([
            "<strong>One action per step</strong>, in the order it happens.",
            "<strong>Give numbers</strong> — setpoints, delays, limits — and mark them “adjustable”.",
            "<strong>Say how each step is proven</strong> (“when run status is received”), not just what is commanded.",
            "<strong>Say what happens when it goes wrong</strong>: failure to prove, sensor failure, communication loss, power return.",
            "<strong>Use the point names</strong> from the points list, so programmer and tester mean the same thing.",
            "<strong>Avoid</strong> “as required”, “as necessary”, “suitable” — they cannot be tested.",
        ])
        + "<h3>Common HVAC sequences on a BMS</h3>"
        + table(["Plant", "Core of the sequence"], [
            ("AHU (CAV)", "Schedule, start/prove, valve on return or supply temperature, fresh air control, alarms"),
            ("AHU (VAV)", "As above plus fan speed on duct static pressure, often with pressure and temperature reset"),
            ("FCU", "Occupancy, setpoint with deadband, fan speed staging, valve on/off or modulating"),
            ("VAV box", "Zone temperature → airflow setpoint between min and max (page 2.4)"),
            ("Chiller plant", "Start/stop and staging, pump control, lead/lag rotation (page 2.5)"),
            ("Cooling towers", "Fan speed or staging on CW supply temperature (page 2.6)"),
            ("Exhaust and car-park fans", "Schedules; car parks often on carbon monoxide (CO) sensors"),
            ("Water tanks and pumps", "Level control with duty/standby pumps and high/low level alarms"),
        ])
        + callout("note", "Standard sequences",
                  "<p>ASHRAE Guideline 36 publishes standardised, high-performance sequences for AHUs and VAV terminal units. "
                  "Even when a project does not adopt it, it is an excellent reference for how good sequences are written.</p>")
    ),
    ahu01=("<p>The six steps above <em>are</em> AHU-01's sequence in summary. Over the next modules you will learn what is "
           "behind each one: the devices (Module 3), the wiring (Module 4), the communication (Module 5) and the logic "
           "(Module 6). In Lab 3 you write it out in full.</p>"),
    on_site=[
        "Get the approved sequence <strong>before</strong> programming; mark up any deviations and get them agreed.",
        "During commissioning, test the sequence step by step and tick each one — including the failure steps.",
        "Put the adjustable parameters (setpoints, delays) on the graphic so operators can see them.",
        "Keep the final, as-built sequence with the O&amp;M documents; the next engineer will need it.",
    ],
    faults=[
        ("Plant short-cycles on and off", "No deadband, minimum run time or minimum off time", "Sequence timers and deadbands"),
        ("Heating and cooling valves both open", "No interlock or deadband between them", "Sequence logic for both loops"),
        ("Plant stays off after a power cut", "No automatic restart in the sequence", "Power-return logic"),
        ("All plant starts at once after a power cut, overloading the generator", "No staggered restart", "Add restart delays per item"),
        ("Operators and contractor disagree on how plant should run", "Sequence vague or never approved", "Write and agree a testable sequence"),
    ],
    terms=[
        ("Sequence of operation", "Written step-by-step description of how plant must operate."),
        ("Permissive", "A condition that must be true before plant may start."),
        ("Proving", "Confirming that a commanded action actually happened, e.g. run status after a start command."),
        ("Operating mode", "A defined state such as occupied, unoccupied, fire or hand."),
        ("Lockout", "A state after a fault in which plant will not restart until reset."),
        ("Adjustable parameter", "A setpoint or timer an operator can change within limits."),
        ("Staggered restart", "Restarting plant items one after another after a power cut."),
        ("ASHRAE Guideline 36", "Published standard sequences for high-performance AHU and VAV control."),
    ],
    scenarios=[dict(
        prompt="Power returns after a grid failure. Within two seconds all 40 AHUs, 12 pumps and 4 chillers try to start. The generator trips on overload. What should the sequence have included?",
        options=["Bigger generator fuses.", "A staggered restart — each plant item waits a different delay after power returns.",
                 "Manual restart only, for every item."],
        answer=1,
        explain=(" Starting large motors one after another limits the inrush current. Sequences should define power-return behaviour: "
                 "restart delays per item, and which plant restarts automatically."),
    )],
    questions=[
        ("Why should every sequence step say how it is proven?", "Because a command does not guarantee the action happened. The sequence must say what feedback confirms each step (e.g. run status) and what happens if it does not arrive."),
        ("Name five sections of a complete sequence of operation.", "Any five of: equipment and points, modes, enable conditions, start sequence, normal control, stop sequence, interlocks and safeties, alarms, failure responses, adjustable parameters."),
        ("Which mode overrides every other mode?", "Fire mode."),
        ("Rewrite “the valve shall be controlled as required”.", "For example: “When the supply fan is proven running, a PID loop shall modulate the CHW valve (0–100 %) to hold return air temperature at 24 °C (adjustable 22–26 °C). When the fan is off, the valve shall be closed.”"),
        ("What is ASHRAE Guideline 36?", "A published set of standardised high-performance control sequences for AHUs and VAV terminal units."),
    ],
)

MODULE_INTRO = (
    "<p>Before you can control plant, you need to know how it works. This module covers the equipment a BMS spends most of "
    "its time on — AHUs, FCUs, VAV systems, chillers and cooling towers — and ends with the language used to describe how "
    "they should run: the sequence of operation.</p>"
)

PAGES = [P1, P2, P3, P4, P5, P6, P7]

QUIZ = [
    mcq("In airflow order, which comes first in a typical AHU?", ["Supply fan", "Cooling coil", "Filters", "Discharge silencer"], 2,
        "Air passes dampers and mixing box, then filters, then the coil, then the fan.", "2.1"),
    mcq("How does a chilled water coil remove moisture from air?",
        ["By heating it", "By cooling it below its dew point so vapour condenses", "With a chemical filter", "By adding fresh air"], 1,
        "Condensed water collects in the drain pan and is drained away.", "2.1"),
    mcq("20 % fresh air at 35 °C mixes with 80 % return air at 24 °C. What is the mixed air temperature?",
        ["24.0 °C", "26.2 °C", "29.5 °C", "31.0 °C"], 1, "0.2 × 35 + 0.8 × 24 = 26.2 °C.", "2.2"),
    mcq("A building should normally be kept…",
        ["strongly negative", "slightly positive", "exactly neutral at all times", "positive in toilets"], 1,
        "Slightly positive keeps dust and humid air out; toilets and kitchens are kept negative.", "2.2"),
    mcq("Where does an FCU zone usually get its fresh air?",
        ["From the FCU's own fresh air damper", "From a separate TFA unit", "It never needs any", "From the chilled water"], 1,
        "FCUs recirculate room air; fresh air comes from a treated fresh air unit.", "2.3"),
    mcq("In a VAV system, what does the AHU's VFD usually control?",
        ["Return air temperature", "Duct static pressure", "Chilled water flow", "Room CO₂"], 1,
        "As boxes close, duct pressure rises and the fan slows to hold the pressure setpoint.", "2.4"),
    mcq("A fan slows to 80 % speed. Roughly how much power does it now need?",
        ["80 %", "64 %", "51 %", "20 %"], 2, "Power ∝ speed³: 0.8³ ≈ 0.51.", "2.4"),
    mcq("What must be proven before a chiller is enabled?",
        ["Chilled (and condenser) water flow", "Room temperature", "Outdoor humidity", "BMS server online"], 0,
        "A chiller must never run without proven water flow.", "2.5"),
    mcq("Condenser water leaving a cooling tower can never be colder than…",
        ["the dry-bulb temperature", "the wet-bulb temperature", "the chilled water supply", "15 °C"], 1,
        "Evaporative cooling is limited by the wet-bulb temperature.", "2.6"),
    mcq("Which sequence statement is testable?",
        ["Control the valve as required", "Start the fan when suitable",
         "If run status is not received within 30 s of the start command, raise “fan fail” and stop the fan",
         "Keep the building comfortable"], 2, "It has a condition, a time limit, a proof and an action.", "2.7"),
]

FINAL = [
    mcq("What is a TFA?", ["A fan coil with a thermostat", "An AHU that handles 100 % treated fresh air",
                           "A type of chiller", "A filter grade"], 1, "Treated fresh air unit.", "2.1"),
    mcq("Fresh fraction from MAT 26 °C, RAT 24 °C, OAT 34 °C is…", ["10 %", "20 %", "26 %", "50 %"], 1,
        "(26 − 24) ÷ (34 − 24) = 0.2.", "2.2"),
    mcq("A pressure-independent VAV box controls…", ["damper position only", "measured airflow", "duct pressure", "chilled water"], 1,
        "Its flow loop holds the airflow set by the zone temperature loop.", "2.4"),
    mcq("Cooling delivered by 10 L/s of chilled water with a 5.5 K temperature difference is about…",
        ["23 kW", "230 kW", "55 kW", "2.3 kW"], 1, "4.19 × 10 × 5.5 ≈ 230 kW, about 66 TR.", "2.5"),
    mcq("Which mode overrides every other operating mode?", ["Hand", "Unoccupied", "Fire", "Maintenance"], 2,
        "Fire mode overrides everything.", "2.7"),
]
