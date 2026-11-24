# -*- coding: utf-8 -*-
"""Course structure for Level 1. Content for each page lives in content/mN.py;
a page listed here without content is shown as "coming soon"."""

LEVEL = dict(
    num=1,
    slug="level-1",
    title="BMS Fundamentals",
    duration="4 weeks · 45–60 minutes a day",
    goal=("Understand BMS architecture, HVAC plant, field devices, I/O wiring, "
          "communication protocols and basic control logic — well enough to read a "
          "BMS drawing, wire and test a point, and explain how an AHU is controlled."),
)

# (page id, file slug, title)
MODULES = [
    dict(num=1, title="BMS Architecture",
         blurb="What a BMS is, how it is layered, and the controllers, servers and panels that make it work.",
         pages=[
             ("1-1", "what-is-a-bms", "What is a BMS?"),
             ("1-2", "bms-architecture-levels", "BMS architecture: field, automation and management levels"),
             ("1-3", "ddc-controller", "The DDC controller and how it works"),
             ("1-4", "server-workstation-operator-interface", "BMS server, workstation and operator interface"),
             ("1-5", "control-panel-architecture", "BMS control panel architecture"),
             ("1-6", "hvac-system-integration", "HVAC system integration"),
         ]),
    dict(num=2, title="HVAC Control Fundamentals",
         blurb="The plant a BMS controls: AHUs, FCUs, VAV/CAV, chilled water, chillers and cooling towers.",
         pages=[
             ("2-1", "air-handling-unit", "Air handling unit (AHU)"),
             ("2-2", "supply-return-fresh-exhaust-air", "Supply, return, fresh and exhaust air"),
             ("2-3", "fan-coil-unit", "Fan coil unit (FCU)"),
             ("2-4", "vav-and-cav-systems", "VAV and CAV systems"),
             ("2-5", "chilled-water-system-chiller-plant", "Chilled water system and chiller plant"),
             ("2-6", "cooling-tower", "Cooling tower and condenser water"),
             ("2-7", "hvac-control-sequences", "HVAC control sequences — an overview"),
         ]),
    dict(num=3, title="Sensors and Field Devices",
         blurb="The devices that measure and move: sensors, meters, actuators, drives and status switches.",
         pages=[
             ("3-1", "temperature-sensors", "Temperature sensors (NTC, PT1000)"),
             ("3-2", "humidity-and-co2-sensors", "Humidity and CO₂ sensors"),
             ("3-3", "differential-pressure-and-airflow", "Differential pressure and airflow sensors"),
             ("3-4", "water-flow-meters", "Water flow meters"),
             ("3-5", "damper-actuators", "Damper actuators"),
             ("3-6", "chilled-water-valve-actuators", "Chilled water valves and actuators"),
             ("3-7", "variable-frequency-drives", "Variable frequency drives (VFD)"),
             ("3-8", "status-devices", "Status devices: current switches and DP switches"),
         ]),
    dict(num=4, title="Digital and Analog I/O",
         blurb="DI, DO, AI and AO; 0–10 V and 4–20 mA; contacts and relays; wiring, testing and drawings.",
         pages=[
             ("4-1", "electrical-safety", "Electrical safety for BMS work"),
             ("4-2", "io-types", "The four I/O types: DI, DO, AI, AO"),
             ("4-3", "analog-signals", "Analog signals: 0–10 V, 4–20 mA, 0–20 mA"),
             ("4-4", "digital-signals-contacts-relays", "Dry contacts, relay outputs, NO and NC"),
             ("4-5", "sensor-wiring-troubleshooting", "Sensor wiring and troubleshooting"),
             ("4-6", "reading-bms-drawings", "Reading BMS drawings and point names"),
         ]),
    dict(num=5, title="BMS Communication Protocols",
         blurb="RS485, addressing, Modbus RTU/TCP, BACnet MS/TP and BACnet/IP, and fixing comms faults.",
         pages=[
             ("5-1", "rs485-basics", "RS485 communication basics"),
             ("5-2", "addressing-ip-device-id-baud", "IP address, subnet mask, device ID and baud rate"),
             ("5-3", "modbus-rtu-and-tcp", "Modbus RTU and Modbus TCP"),
             ("5-4", "bacnet-mstp-and-ip", "BACnet MS/TP and BACnet/IP"),
             ("5-5", "communication-troubleshooting", "Communication troubleshooting"),
         ]),
    dict(num=6, title="BMS Control Logic",
         blurb="Start/stop sequences, interlocks, PID, valve and damper control, alarms and schedules.",
         pages=[
             ("6-1", "ahu-start-stop-sequence", "AHU start/stop sequence"),
             ("6-2", "fan-interlocks-and-safeties", "Fan interlocking and safeties"),
             ("6-3", "pid-control-basics", "PID control basics"),
             ("6-4", "valve-and-damper-control", "Temperature-based valve control and damper control"),
             ("6-5", "alarms", "Alarms: filter dirty, high and low temperature"),
             ("6-6", "scheduling", "Scheduling and time-based logic"),
         ]),
]

LABS = [
    ("L1", "lab-1-ahu-wiring-diagram", "Lab 1 · AHU control wiring diagram"),
    ("L2", "lab-2-ahu-point-list", "Lab 2 · AHU point list (DI, DO, AI, AO)"),
    ("L3", "lab-3-ahu-start-stop-sequence", "Lab 3 · AHU start/stop sequence"),
    ("L4", "lab-4-4-20ma-pressure-sensor", "Lab 4 · 4–20 mA pressure sensor wiring"),
    ("L5", "lab-5-reading-modbus-registers", "Lab 5 · Reading Modbus registers"),
]

REVIEWS = {
    "R1": "Week 1 review + Module 1 quiz",
    "R2": "Week 2 review + Module 2 quiz",
    "R3": "Week 3 review + Modules 3–4 quiz",
    "FT": "Level 1 final test",
}

# Week -> (focus, [day items]); each day is a list of page / lab / review ids.
WEEKS = [
    (1, "BMS architecture + HVAC basics", [
        ["1-1", "1-2"], ["1-3"], ["1-4", "1-5"], ["1-6"], ["2-1"], ["2-2", "2-3"], ["R1"]]),
    (2, "HVAC plant + first sensors", [
        ["2-4"], ["2-5"], ["2-6"], ["2-7"], ["3-1"], ["3-2", "3-3"], ["R2"]]),
    (3, "Field devices, I/O and wiring", [
        ["3-4", "3-5"], ["3-6", "3-7"], ["3-8", "4-1"], ["4-2", "4-3"], ["4-4", "L4"], ["4-5", "4-6"], ["L2", "R3"]]),
    (4, "Protocols + control logic", [
        ["5-1", "5-2"], ["5-3", "L5"], ["5-4", "5-5"], ["6-1", "6-2"], ["6-3", "L3"], ["6-4", "6-5", "6-6"], ["L1", "FT"]]),
]


def schedule_lookup():
    """Return {item id: (week, day)} with day numbered 1..28 across the level."""
    out, day = {}, 0
    for week, _focus, days in WEEKS:
        for items in days:
            day += 1
            for i in items:
                out.setdefault(i, (week, day))
    return out
