# -*- coding: utf-8 -*-
"""AHU-01: the example unit followed through the whole of Level 1."""
from bms_common import svg, defs, t, rect, box, line, path, circle, table, fig


def schematic():
    i = defs("ah")
    # casing and sections
    i += rect(170, 70, 440, 120, "d-soft", 10)
    for x in (255, 305, 375, 480):
        i += line(x, 72, x, 188, "d-line d-thin d-dash")
    for x, s in ((212, "Mixing"), (280, "Filter"), (340, "Coil"), (427, "Fan"), (545, "Discharge")):
        i += t(x, 82, s, "d-ts")
    # fresh air + damper
    i += line(20, 120, 168, 120, "d-aline", end="ah-a")
    i += t(60, 104, "Fresh air", "d-ts")
    i += rect(108, 104, 28, 32, "d-box", 3) + line(110, 134, 134, 106)
    i += t(122, 150, "Fresh air damper · AO", "d-ts")
    # filter + DP switch
    i += path("M280,94 L268,104 L292,116 L268,128 L292,140 L268,152 L292,164 L280,176")
    i += box(250, 18, 60, 26, "ΔP", "", "d-acc", "d-t d-tb", 6)
    i += line(262, 44, 252, 70, "d-line d-thin") + line(298, 44, 308, 70, "d-line d-thin")
    i += t(242, 31, "Filter dirty switch · DI", "d-ts", "end")
    # coil + pipes + valve
    i += rect(318, 94, 44, 84, "d-acc", 3)
    for y in range(104, 176, 10):
        i += line(320, y, 360, y, "d-line d-thin")
    i += line(328, 178, 328, 250, "d-cold") + line(352, 178, 352, 250, "d-warmline")
    i += t(322, 262, "CHWS", "d-ts", "end") + t(358, 262, "CHWR", "d-ts", "start")
    i += path("M344,206 L360,206 L352,218 Z M344,230 L360,230 L352,218 Z", "d-box")
    i += line(352, 218, 374, 218) + box(374, 207, 22, 22, "M", "", "d-box", "d-ts d-tb", 4)
    i += t(402, 218, "CHW valve · AO", "d-ts", "start")
    # fan + VFD
    i += circle(427, 135, 28, "d-box")
    i += path("M413,150 L445,135 L413,120 Z", "d-line")
    i += box(397, 18, 60, 28, "VFD", "", "d-acc", "d-t d-tb", 6)
    i += line(427, 46, 427, 105, "d-line d-thin d-dash")
    i += t(465, 32, "Start DO · Run, fault DI · Speed AO · Modbus", "d-ts", "start")
    # supply air + sensors
    i += line(612, 120, 768, 120, "d-aline", end="ah-a")
    i += t(700, 98, "Supply air to offices", "d-ts", "end")
    i += circle(650, 120, 13, "d-box") + t(650, 120, "T", "d-ts d-tb")
    i += t(650, 146, "SAT · AI", "d-ts")
    i += circle(722, 120, 13, "d-box") + t(722, 120, "P", "d-ts d-tb")
    i += t(722, 146, "Duct pressure · AI", "d-ts")
    # return air + sensors + manual damper
    i += path("M770,290 L210,290 L210,192", "d-aline", end="ah-a")
    i += t(770, 274, "Return air from offices", "d-ts", "end")
    for x, s, lab in ((470, "T", "RAT · AI"), (525, "H", "RH · AI"), (580, "CO₂", "CO₂ · AI")):
        i += circle(x, 290, 15, "d-box") + t(x, 290, s, "d-ts d-tb") + t(x, 318, lab, "d-ts")
    i += rect(196, 226, 28, 28, "d-box", 3) + line(198, 252, 222, 228)
    i += t(186, 240, "Return damper (manual)", "d-ts", "end")
    return svg(780, 335, i, "Schematic of AHU-01 with dampers, filter, cooling coil, fan, VFD and sensors")


def figure():
    return fig(schematic(),
               "AHU-01. Air enters from the left (fresh air) and the bottom (return air), is filtered and cooled, "
               "and the fan pushes it to the offices. Every symbol is a BMS point.")


DEVICES = [
    ("Supply fan (via VFD)", "Start/stop command", "DO"),
    ("Supply fan (via VFD)", "Run status, fault, auto/manual", "DI"),
    ("Supply fan (via VFD)", "Speed reference", "AO"),
    ("Supply fan (via VFD)", "Frequency, current, kW, fault code", "Modbus RTU"),
    ("Filter ΔP switch", "Filter dirty", "DI"),
    ("Fire alarm interface", "Fire shutdown signal", "DI (+ hard-wired trip)"),
    ("Return air sensors", "Temperature (RAT), humidity (RH), CO₂", "AI"),
    ("Supply air sensors", "Temperature (SAT), duct static pressure", "AI"),
    ("CHW valve actuator", "Valve position command", "AO"),
    ("Fresh air damper actuator", "Damper position command", "AO"),
]


def device_table():
    return table(["Device", "What the BMS sees or sends", "Point type"], DEVICES, "plain")
