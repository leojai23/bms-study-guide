# -*- coding: utf-8 -*-
"""Level 1 cheat sheet — one printable page of the numbers and rules used most."""
from bms_common import table, page_url
import syllabus as S

KEYWORDS = ("cheat sheet reference formulas PT1000 NTC table 4-20 mA scaling Modbus function codes BACnet priority "
            "RS485 rules baud ports TR kW fan laws")


def _link(root, pid):
    for m in S.MODULES:
        for p, slug, title in m["pages"]:
            if p == pid:
                return f'<a href="{root}{page_url(p, slug)}">{p.replace("-", ".")}</a>'
    return pid


def body(root):
    def sec(title, html, ref):
        return f'<section class="cs"><h3>{title} <small>{_link(root, ref)}</small></h3>{html}</section>'

    s = []
    s.append(sec("Analogue signals", table(["Signal", "Value from signal"], [
        ("4–20 mA", "min + (mA − 4) ÷ 16 × span"), ("0–10 V", "min + V ÷ 10 × span"), ("2–10 V", "min + (V − 2) ÷ 8 × span"),
        ("Output 0–10 V", "V = % ÷ 10"), ("Output 2–10 V", "V = 2 + % × 0.08"),
    ], "plain") + "<p>4–20 mA faults: &lt; 3.6 mA or &gt; 21 mA · 250 Ω burden → 1–5 V · max loop R = (V<sub>supply</sub> − V<sub>tx min</sub>) ÷ 0.02</p>", "4-3"))
    s.append(sec("Temperature sensors", table(["°C", "0", "10", "20", "25", "30", "40"], [
        ("PT1000 Ω", "1000", "1039", "1078", "1097", "1117", "1155"),
        ("NTC 10k β3950 Ω", "33.6k", "20.2k", "12.5k", "10.0k", "8.0k", "5.3k"),
    ], "plain") + "<p>PT1000 ≈ 3.85 Ω/°C · open → NTC reads LOW, PT reads HIGH · short → NTC HIGH, PT LOW · match the NTC curve!</p>", "3-1"))
    s.append(sec("I/O types", table(["", "Direction", "Examples"], [
        ("DI", "in, on/off", "status, fault, auto, filter, fire"), ("DO", "out, on/off", "start/stop, enable"),
        ("AI", "in, range", "temp, RH, pressure, CO₂"), ("AO", "out, range", "valve, damper, VFD speed"),
    ], "plain") + "<p>NO/NC = state when de-energised · safety signals closed-when-healthy (fail-safe) · motor circuits via interposing relay</p>", "4-2"))
    s.append(sec("RS485 rules", "<ul><li>Daisy chain only — no stars or spurs</li><li>120 Ω at both ends only → A–B ≈ 60 Ω (power off)</li>"
                 "<li>Bias at one point · use the common wire · screen earthed once</li><li>32 unit loads · ~1,200 m per segment · repeaters beyond</li>"
                 "<li>A/B labels vary — swapping is a safe test</li></ul>", "5-1"))
    s.append(sec("Addresses, speeds and ports", table(["Item", "Value"], [
        ("Modbus address", "1–247"), ("MS/TP MAC", "0–127 masters (Max_Master ≥ highest)"), ("BACnet device instance", "0–4,194,302, unique site-wide"),
        ("Common baud", "9600 · 19200 · 38400 · 76800 · 115200"), ("Modbus RTU default", "19200 8E1"),
        ("Modbus TCP port", "502"), ("BACnet/IP port", "UDP 47808 (0xBAC0)"),
    ], "plain"), "5-2"))
    s.append(sec("Modbus", table(["Code", "Function"], [
        ("01 / 05 / 15", "read / write one / write many coils"), ("02", "read discrete inputs"), ("03", "read holding registers (4xxxx)"),
        ("04", "read input registers (3xxxx)"), ("06 / 16", "write one / many holding registers"),
    ], "plain") + "<p>40001 = address 0 · exceptions: 01 function · 02 address · 03 value · 04 device · 32-bit order ABCD or CDAB</p>", "5-3"))
    s.append(sec("BACnet", table(["Priority", "Use"], [
        ("1 / 2", "manual / automatic life safety"), ("5", "critical equipment"), ("6", "minimum on/off"), ("8", "manual operator"), ("16", "typical program level"),
    ], "plain") + "<p>Lowest non-null slot wins · release = write null · BBMD for broadcasts across subnets · PICS = what a device supports</p>", "5-4"))
    s.append(sec("HVAC numbers", table(["Quantity", "Typical / formula"], [
        ("Supply / return air", "12–15 °C / 23–25 °C"), ("CHW / CW", "7 → 12.5 °C / 32 → 37 °C"),
        ("Air cooling", "W ≈ 1.2 × L/s × ΔT"), ("Water cooling", "kW = 4.19 × L/s × ΔT"), ("1 TR", "3.517 kW"),
        ("Fan laws", "flow ∝ n · pressure ∝ n² · power ∝ n³"), ("Air velocity", "v ≈ 1.29 × √Pv"), ("Valve", "Kv = Q ÷ √ΔP(bar)"),
        ("Mixed air", "MAT = f × OAT + (1 − f) × RAT"),
    ], "plain"), "2-5"))
    s.append(sec("PID and alarms", "<ul><li>Gain = 100 % ÷ proportional band</li><li>P only → offset · I removes it · D rarely in HVAC</li>"
                 "<li>Hunting → wider PB / longer Ti · sluggish → narrower PB / shorter Ti</li>"
                 "<li>Alarms: limit + deadband + delay + enable condition + priority + clear message</li></ul>", "6-3"))
    s.append(sec("Safety and fault-finding", "<ul><li>Isolate · lock · tag · <strong>prove – test – prove</strong></li>"
                 "<li>BMS “off” is not isolation — fans start remotely</li><li>VFD DC bus: wait the labelled time</li>"
                 "<li>Fault-finding: check the point → measure at the controller → split field / controller side</li>"
                 "<li>Comms: physical → settings → protocol → application</li></ul>", "4-1"))
    return '<div class="cheat">' + "".join(s) + "</div>"
