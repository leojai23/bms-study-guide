# -*- coding: utf-8 -*-
"""Module 5 — BMS Communication Protocols. Vendor-neutral; based on TIA-485, the Modbus application protocol and
serial-line specifications, and ASHRAE 135 (BACnet). Register maps shown are illustrative examples."""
from bms_common import (table, steps, bullets, callout, cards, fig, svg, defs, t, rect, box,
                        line, path, circle, mcq, tool)

# ==========================================================================
# Diagrams
# ==========================================================================

def d_rs485():
    i = defs("rs")
    i += t(380, 16, "Correct: one daisy chain, terminated at both ends", "d-t d-tb d-tok")
    xs = [60, 210, 360, 510, 660]
    names = ["Controller", "VFD", "Meter", "FCU 3", "FCU 4"]
    for k, x in enumerate(xs):
        i += box(x - 50, 70, 100, 50, names[k], "addr " + str(k if k else "master"), "d-acc" if k == 0 else "d-box")
    for y, cls in ((40, "d-aline"), (52, "d-line")):
        i += line(60, y, 660, y, cls)
    for x in xs:
        i += line(x - 6, 40, x - 6, 70, "d-aline d-thin") + line(x + 6, 52, x + 6, 70, "d-line d-thin")
    for x in (40, 680):
        i += rect(x - 8, 34, 16, 24, "d-warn", 3)
    i += t(32, 64, "120 Ω", "d-ts", "end") + t(690, 64, "120 Ω", "d-ts", "start")
    i += t(60, 134, "+ bias (once)", "d-ts")
    i += t(380, 150, "A/B pair twisted, plus a common (0 V) wire · screen earthed at one point", "d-ts")
    i += line(10, 170, 750, 170, "d-line d-dash d-thin")
    i += t(200, 190, "Wrong: star / spur wiring", "d-t d-tb d-tbad")
    i += box(150, 230, 100, 40, "Controller", "", "d-acc")
    for x, y in ((60, 300), (200, 310), (340, 300)):
        i += line(200, 270, x, y - 10, "d-warmline") + box(x - 40, y - 10, 80, 32, "device", "", "d-box", "d-ts")
    i += t(200, 360, "signal reflections → errors", "d-ts d-tbad")
    i += t(560, 190, "Wrong: terminators everywhere", "d-t d-tb d-tbad")
    i += line(430, 250, 700, 250, "d-line")
    for x in (450, 520, 590, 660):
        i += rect(x - 8, 238, 16, 24, "d-bad", 3)
    i += t(565, 290, "4 × 120 Ω in parallel = 30 Ω", "d-ts") + t(565, 306, "→ bus overloaded", "d-ts d-tbad")
    return svg(760, 375, i, "RS485 topology: daisy chain with end terminations, and two common mistakes")


def d_subnets():
    i = defs("sn")
    i += rect(20, 40, 300, 150, "d-soft", 10) + t(170, 58, "Subnet 10.1.3.0 /24 (Level 3)", "d-ts d-tb")
    i += rect(440, 40, 300, 150, "d-soft", 10) + t(590, 58, "Subnet 10.1.4.0 /24 (Level 4)", "d-ts d-tb")
    i += box(40, 80, 120, 50, "DDC-AHU-01", "10.1.3.21", "d-acc") + box(180, 80, 120, 50, "Supervisory", "10.1.3.10", "d-acc")
    i += box(460, 80, 120, 50, "DDC-AHU-02", "10.1.4.21", "d-acc") + box(600, 80, 120, 50, "Supervisory", "10.1.4.10", "d-acc")
    i += line(30, 160, 310, 160, "d-aline") + line(450, 160, 730, 160, "d-aline")
    for x in (100, 240):
        i += line(x, 130, x, 160, "d-aline")
    for x in (520, 660):
        i += line(x, 130, x, 160, "d-aline")
    i += box(320, 220, 120, 50, "Router", "gateway .1 on each", "d-warn")
    i += path("M170,160 L170,245 L318,245", "d-aline") + path("M590,160 L590,245 L442,245", "d-aline")
    i += t(380, 300, "same subnet → direct · different subnets → through the router (default gateway)", "d-ts")
    return svg(760, 315, i, "Two IP subnets joined by a router")


def d_modbus_frames():
    i = defs("mb")
    i += t(380, 16, "Modbus RTU: client reads 2 holding registers from server address 1", "d-t d-tb")
    req = [("01", "address"), ("03", "function"), ("00 00", "start"), ("00 02", "quantity"), ("C4 0B", "CRC")]
    res = [("01", "address"), ("03", "function"), ("04", "byte count"), ("41 B8", "register 1"), ("00 00", "register 2"), ("xx xx", "CRC")]
    def row(y, cells, cls, label):
        o = t(20, y + 18, label, "d-ts d-tb", "start")
        x = 120
        for a, b in cells:
            w = 40 + 18 * len(a.replace(" ", "")) // 2
            o += box(x, y, w, 36, a, "", cls, "d-t d-tb d-mono", 4) + t(x + w / 2, y + 50, b, "d-ts")
            x += w + 8
        return o
    i += row(40, req, "d-acc", "Request →")
    i += row(130, res, "d-ok", "← Response")
    i += t(380, 214, "0x41B8 0x0000 read as a 32-bit float (big-endian) = 23.0", "d-ts d-ta")
    return svg(760, 230, i, "A Modbus RTU request and response")


def d_bacnet_net():
    i = defs("bn")
    i += rect(20, 40, 330, 130, "d-soft", 10) + t(185, 58, "IP subnet A · BACnet network 1", "d-ts d-tb")
    i += rect(410, 40, 330, 130, "d-soft", 10) + t(575, 58, "IP subnet B · BACnet network 2", "d-ts d-tb")
    i += box(40, 78, 120, 50, "BMS server", "", "d-box") + box(190, 78, 140, 50, "BBMD", "forwards broadcasts", "d-warn")
    i += box(430, 78, 140, 50, "BBMD", "forwards broadcasts", "d-warn") + box(590, 78, 130, 50, "Router", "IP ↔ MS/TP", "d-acc")
    i += line(30, 150, 340, 150, "d-aline") + line(420, 150, 730, 150, "d-aline")
    for x in (100, 260):
        i += line(x, 128, x, 150, "d-aline")
    for x in (500, 655):
        i += line(x, 128, x, 150, "d-aline")
    i += path("M260,150 L260,165 L500,165 L500,150", "d-line d-dash") + t(380, 180, "IP router between subnets · BBMDs exchange broadcasts", "d-ts")
    i += path("M655,150 L655,215", "d-aline")
    i += line(470, 215, 730, 215, "d-line") + t(476, 205, "MS/TP network 3 (RS485)", "d-ts", "start")
    for x, n in ((500, "FCU-301"), (580, "FCU-302"), (660, "VAV-305")):
        i += line(x, 215, x, 232) + box(x - 36, 232, 72, 34, n, "", "d-box", "d-ts d-tb", 5)
    i += t(185, 230, "Every device instance unique across", "d-ts") + t(185, 246, "the whole BACnet internetwork", "d-ts")
    return svg(760, 280, i, "A BACnet internetwork: two IP subnets with BBMDs, and an MS/TP network behind a router")


def d_priority():
    i = ""
    i += t(380, 16, "Priority array of AHU-01's CHW valve (Analog Output)", "d-t d-tb")
    slots = {1: ("Manual life safety", None), 2: ("Automatic life safety", None), 5: ("Critical equipment control", None),
             6: ("Minimum on/off", None), 8: ("Manual operator", "0 %"), 16: ("Program (typical)", "62 %")}
    for k in range(16):
        x = 30 + k * 44
        win = k + 1 == 8
        val = slots.get(k + 1, (None, None))[1]
        cls = "d-ok" if win else ("d-acc" if val else "d-soft")
        i += rect(x, 40, 38, 46, cls, 5) + t(x + 19, 54, str(k + 1), "d-ts d-tb") + t(x + 19, 72, val or "null", "d-ts")
    for k, (lab, _v) in slots.items():
        x = 30 + (k - 1) * 44 + 19
        y = 104 if k in (1, 5, 8, 16) else 132
        anchor, tx = ("start", x - 19) if k == 1 else (("end", x + 19) if k == 16 else ("middle", x))
        i += line(x, 86, x, y - 8, "d-line d-thin") + t(tx, y, lab, "d-ts", anchor)
    i += t(380, 168, "Present value = the highest-priority (lowest number) non-null slot → 0 % (operator override at 8)", "d-ts d-tb d-ta")
    i += t(380, 186, "Release (write null at 8) → the program's 62 % at 16 takes effect · all null → relinquish default", "d-ts")
    return svg(760, 200, i, "BACnet priority array")


def d_layers():
    i = defs("ly")
    rows = [("4 · Application", "polling load, timeouts, overrides, priorities, wrong object or register", "d-acc"),
            ("3 · Protocol / data", "function code, register address and offset, data type, byte order, scaling", "d-acc"),
            ("2 · Settings", "address / MAC / device instance, baud, parity, IP, mask, gateway, network numbers", "d-warn"),
            ("1 · Physical", "power, cable, polarity, termination, bias, topology, earthing, noise", "d-bad")]
    for k, (a, b, c) in enumerate(rows):
        y = 20 + k * 58
        i += rect(150, y, 590, 48, c, 8) + t(170, y + 16, a, "d-t d-tb", "start") + t(170, y + 34, b, "d-ts", "start")
    i += path("M80,240 L80,30", "d-aline", end="ly-a") + t(70, 135, "work up", "d-ts d-ta", "end")
    return svg(760, 255, i, "Fix communication faults from the bottom layer up")


# ==========================================================================
# Pages
# ==========================================================================

P1 = dict(
    id="5-1", slug="rs485-basics", title="RS485 communication basics",
    objectives=[
        "Explain what RS485 is — and what it is not.",
        "Wire a correct daisy-chain bus with termination, biasing and a common.",
        "Know the limits: devices, length and speed.",
        "Check a bus with a multimeter before blaming the protocol.",
    ],
    one_line=("RS485 is the <strong>electrical standard</strong> for the twisted-pair cable that BACnet MS/TP and Modbus RTU run on — "
              "a daisy chain of devices, terminated at both ends, sending data as a voltage difference between two wires."),
    why=("<p>Most field-bus problems in buildings are not protocol problems at all — they are wiring problems: a spur, a missing "
         "terminator, swapped wires, a shared earth. RS485 is forgiving when wired properly and miserable when not. Getting the "
         "physical layer right first saves hours of chasing settings.</p>"),
    body=(
        "<h3>What RS485 is</h3>"
        + "<p>RS485 (formally TIA/EIA-485) defines only the <strong>electrical signals</strong>: how ones and zeros are sent as "
          "a voltage difference between two wires. It says nothing about addresses or messages — that is the job of the "
          "protocol running on top, such as <strong>Modbus RTU</strong> or <strong>BACnet MS/TP</strong>. In BMS it is used "
          "<strong>half-duplex on two wires</strong>: all devices share one pair and take turns to talk.</p>"
        + "<p>Because the receiver looks at the <em>difference</em> between the two wires, noise that hits both wires equally "
          "cancels out. That is why the pair must be <strong>twisted</strong>.</p>"
        + fig(d_rs485(), "Top: correct topology. Bottom: the two most common wiring mistakes.")
        + "<h3>The rules</h3>"
        + table(["Rule", "Why"], [
            ("Daisy chain only — in and out of each device", "Stars and long spurs cause signal reflections"),
            ("120 Ω terminator at each <strong>end</strong> of the bus, nowhere else", "Matches the cable and stops reflections; extra terminators overload the drivers"),
            ("Bias (fail-safe) resistors at <strong>one</strong> point, usually the master", "Hold the line in a defined idle state when nobody is talking"),
            ("Use a common (0 V / reference) wire as well as A and B", "Keeps all devices' ground potentials close; prevents damage and errors"),
            ("Twisted-pair cable of about 120 Ω impedance, screened", "Noise rejection and correct termination"),
            ("Earth the screen at one point", "Avoids earth loops"),
            ("Keep away from power and VFD motor cables", "Noise"),
        ])
        + "<h3>Limits</h3>"
        + table(["Limit", "Typical value", "Notes"], [
            ("Devices per segment", "32 unit loads", "Many modern transceivers are ¼ or ⅛ unit load → up to 128 or 256; protocols and performance usually set a lower practical limit (often ~32 per MS/TP segment)"),
            ("Length per segment", "About 1,200 m", "At lower baud rates; less at high speeds"),
            ("Beyond those limits", "Repeater", "Starts a new electrical segment; isolated repeaters also break earth loops"),
        ])
        + callout("warn", "A and B naming",
                  "<p>Manufacturers label the two wires differently — A/B, +/−, D+/D−, Data+/Data− — and some use “A” for the "
                  "opposite wire from others. Follow each device's own manual. If a single device will not talk, trying the "
                  "pair the other way round is a legitimate test: reversed polarity does not damage RS485 transceivers.</p>")
        + "<h3>Checking a bus with a multimeter</h3>"
        + table(["Measurement", "Healthy", "If not"], [
            ("Resistance A–B, power off, all devices connected", "About 60 Ω (two 120 Ω terminators in parallel)", "~120 Ω: one terminator missing · well under 60 Ω: extra terminators"),
            ("DC voltage A–B at idle, powered", "A few hundred mV, steady (biasing working)", "Near 0 V: no biasing"),
            ("Voltage between commons of two devices", "Close to 0 V", "Volts: ground potential difference — connect the common, or isolate"),
            ("Continuity of each conductor end to end", "Continuous", "Broken or swapped conductor"),
        ])
    ),
    ahu01=("<p>DDC-AHU-01 has one RS485 port to the VFD — a short, two-device bus. It still needs a terminator at each end (one in "
           "the controller, one in the VFD, both switchable), bias at the controller, a common wire, and screened twisted pair "
           "kept apart from the VFD's motor cable in the AHU room.</p>"),
    on_site=[
        "Draw the bus as installed — device by device — before fault-finding. Hidden spurs and stars appear immediately.",
        "Look for terminator switches or jumpers on every device; only the two end devices should have them on.",
        "Check biasing: some devices have it built in, some not; usually one point should provide it.",
        "Never connect the screen to device terminals at both ends “to be safe”.",
    ],
    faults=[
        ("Nothing on the bus communicates", "A and B swapped at the master, no termination/bias, broken cable", "Polarity at the master; A–B resistance; continuity"),
        ("Devices beyond a certain point drop out", "Break or bad joint in the chain", "Continuity; halve the bus to find it"),
        ("Intermittent errors under load", "Missing terminator, stars or spurs, noise from motor cables", "Topology; terminators; cable route"),
        ("A–B resistance about 30 Ω", "Four terminators switched on", "Turn off all but the two ends"),
        ("Transceiver damaged on one device", "Large ground potential difference — no common wire", "Common wire; isolated repeater"),
    ],
    terms=[
        ("RS485", "Electrical standard for differential, multi-drop serial communication on a twisted pair."),
        ("Half-duplex", "Devices share one pair and take turns to transmit."),
        ("Daisy chain", "Topology where the cable runs from device to device in a line."),
        ("Termination", "120 Ω resistor at each end of the bus to stop reflections."),
        ("Biasing", "Resistors holding the bus in a defined idle state."),
        ("Unit load", "Measure of how much a device loads the bus; 32 standard unit loads per segment."),
        ("Repeater", "Device that starts a new RS485 segment, extending length and device count."),
        ("Common (reference) wire", "Third conductor linking the devices' signal grounds."),
    ],
    scenarios=[dict(
        prompt="On a new MS/TP bus, the first 12 FCUs communicate but the last 8 never appear. Power is fine at all of them. What do you check first?",
        options=["The BACnet device instance numbers.", "The cable between FCU 12 and FCU 13 — a break, bad joint or swapped pair there cuts off everything after it.",
                 "The BMS server licence."],
        answer=1,
        explain=(" On a daisy chain, everything past a break is lost together. Check continuity and polarity at the joint after the "
                 "last working device. (Settings faults would usually affect devices individually.)"),
    )],
    questions=[
        ("What does RS485 define, and what does it not?", "It defines the electrical signalling only. It does not define addresses or messages — those come from the protocol on top (Modbus RTU, BACnet MS/TP)."),
        ("Where are 120 Ω terminators fitted?", "At the two physical ends of the bus only."),
        ("What should the A–B resistance be with the power off and both terminators in place?", "About 60 Ω."),
        ("Why must the bus be a daisy chain and not a star?", "Stars and spurs create signal reflections that corrupt data."),
        ("Why is a common wire recommended?", "It keeps the devices' signal grounds at nearly the same potential, preventing errors and transceiver damage."),
    ],
)

P2 = dict(
    id="5-2", slug="addressing-ip-device-id-baud", title="IP address, subnet mask, device ID and baud rate",
    objectives=[
        "Explain IP address, subnet mask and default gateway, and decide whether two devices share a subnet.",
        "Know the address ranges for Modbus, MS/TP and BACnet device instances.",
        "Match serial settings — baud rate, data bits, parity, stop bits — across a bus.",
        "Write a simple numbering plan for a building.",
    ],
    one_line=("Every device needs a <strong>unique address</strong> on its network, and everything on one bus must share the same "
              "<strong>communication settings</strong> — get either wrong and devices are invisible or collide."),
    why=("<p>Address and settings mistakes are the second big source of communication faults after wiring. They are also the "
         "easiest to prevent: a written numbering plan, agreed before anyone configures a device, avoids duplicates and makes "
         "every device findable for the life of the building.</p>"),
    body=(
        "<h3>IP addressing in one page</h3>"
        + table(["Setting", "Example", "Meaning"], [
            ("IP address", "10.1.3.21", "This device's address — unique on the network"),
            ("Subnet mask", "255.255.255.0 (/24)", "Which part of the address is the network: here 10.1.3.x"),
            ("Default gateway", "10.1.3.1", "The router to send traffic to for other subnets"),
            ("DNS / NTP servers", "10.1.0.5", "Name lookup and time synchronisation (if used)"),
        ])
        + "<p>Two devices can talk directly only if they are in the <strong>same subnet</strong> — the network part of their "
          "addresses (decided by the mask) is identical. Otherwise traffic must go through the <strong>gateway</strong> "
          "(router). With a /24 mask, 10.1.3.21 and 10.1.3.140 are neighbours; 10.1.3.21 and 10.1.4.21 are not.</p>"
        + fig(d_subnets(), "One subnet per floor, joined by a router.")
        + tool("subnet")
        + bullets([
            "Give BMS controllers <strong>static</strong> addresses (or DHCP reservations) so they never change.",
            "Use <strong>private</strong> ranges: 10.x.x.x, 172.16–31.x.x or 192.168.x.x.",
            "Keep the BMS on its own <strong>VLAN</strong> or physical network, separate from office IT.",
            "In each subnet, the first address (network) and last (broadcast) cannot be used by devices.",
            "Know the ports: <strong>BACnet/IP uses UDP 47808</strong> (0xBAC0); <strong>Modbus TCP uses TCP 502</strong>. Firewalls must allow them.",
        ])
        + "<h3>Device addresses</h3>"
        + table(["Address", "Range", "Must be unique…"], [
            ("Modbus server (slave) address", "1–247 (0 = broadcast)", "on that serial bus"),
            ("BACnet MS/TP MAC address", "0–127 for masters; 128–254 for slaves", "on that MS/TP segment"),
            ("BACnet device instance (device ID)", "0–4,194,302", "across the <strong>whole BACnet internetwork</strong>"),
            ("BACnet network number", "1–65,534", "for each network (IP or MS/TP) in the internetwork"),
        ])
        + callout("tip", "Max_Master", "<p>On MS/TP, each master passes the token only up to the address set in "
                  "<strong>Max_Master</strong> (default 127). If it is set to 31 on some devices, a device at MAC 40 will never "
                  "get the token and stays invisible. Set Max_Master on every device to at least the highest MAC on the segment.</p>")
        + "<h3>Serial settings</h3>"
        + table(["Setting", "Common values", "Notes"], [
            ("Baud rate", "9,600 · 19,200 · 38,400 · 76,800 (MS/TP) · 115,200", "Speed in bits per second; identical on every device of a bus"),
            ("Data bits", "8", "Almost always 8"),
            ("Parity", "None · Even · Odd", "Modbus RTU's default is Even; many devices ship with None. MS/TP uses None"),
            ("Stop bits", "1 (or 2)", "The Modbus specification uses 2 stop bits when parity is None — but many devices use 1. Match the device"),
        ])
        + "<p>Settings are written in short form: <strong>19200 8E1</strong> = 19,200 baud, 8 data bits, Even parity, 1 stop bit. "
          "One device with a different setting does not just fail itself — on some buses it corrupts traffic for everyone.</p>"
        + "<h3>A numbering plan</h3>"
        + table(["Item", "Rule", "AHU-01 example"], [
            ("IP subnet", "One /24 per floor: 10.1.&lt;floor&gt;.0", "10.1.3.0 /24"),
            ("IP address", ".1 router · .10 supervisory · .21–.49 plant controllers", "DDC-AHU-01 = 10.1.3.21"),
            ("BACnet device instance", "Building × 100,000 + floor × 1,000 + device number", "103021"),
            ("MS/TP MAC on the floor bus", "1–32 in order along the cable", "FCU-301 = MAC 1"),
            ("Modbus address on a private bus", "Start at 1", "AHU-01 VFD = 1"),
        ])
    ),
    ahu01=("<p>DDC-AHU-01: IP <strong>10.1.3.21 /24</strong>, gateway 10.1.3.1, BACnet device instance <strong>103021</strong>. Its "
           "private Modbus RTU bus to the VFD: VFD address <strong>1</strong> at <strong>19200 8E1</strong> — the same settings in "
           "the controller's port configuration and in the drive's parameters.</p>"),
    on_site=[
        "Agree the numbering plan with IT and every vendor before configuring anything; keep it in the project documents.",
        "Label each device with its address and device instance.",
        "Use the ping command to test IP reachability before blaming BACnet.",
        "When adding a device to an existing bus, read the current settings first — do not assume the defaults.",
    ],
    faults=[
        ("Device answers ping but not BACnet", "Firewall blocking UDP 47808, or different BACnet/IP port configured", "Port settings; firewall"),
        ("Device reachable only from the same floor", "Wrong or missing default gateway", "Gateway setting"),
        ("Two devices flip in and out of view", "Duplicate IP address or duplicate device instance", "Address list; scan for duplicates"),
        ("MS/TP device at MAC 60 never appears", "Max_Master below 60 on the other devices", "Max_Master on all masters"),
        ("Serial device never responds", "Baud, parity or stop-bit mismatch", "Compare settings on both ends"),
    ],
    terms=[
        ("IP address", "Unique address of a device on an IP network."),
        ("Subnet mask", "Defines which part of an IP address identifies the network."),
        ("Default gateway", "Router address used to reach other subnets."),
        ("VLAN", "Virtual LAN — a logically separate network on shared switches."),
        ("Device instance", "BACnet device identifier, unique across the whole internetwork."),
        ("MAC address (MS/TP)", "Address of a device on an MS/TP segment, 0–127 for masters."),
        ("Max_Master", "Highest MS/TP MAC address to which the token is passed."),
        ("Baud rate", "Serial communication speed in bits per second."),
        ("Parity", "Simple error check bit: none, even or odd."),
        ("8N1 / 8E1", "Short form of serial settings: data bits, parity, stop bits."),
    ],
    scenarios=[dict(
        prompt="A new controller is set to 10.1.3.200 with mask 255.255.255.0 and gateway 10.1.4.1. It can talk to devices on Level 3 but the server on another subnet cannot reach it. Why?",
        options=["The mask is wrong.", "The gateway is not in the controller's own subnet — it should be 10.1.3.1.",
                 "The IP address is above 199."],
        answer=1,
        explain=(" A device can only reach a gateway inside its own subnet. With 10.1.3.x/24, the gateway must be a 10.1.3.x address "
                 "(here the router's 10.1.3.1)."),
    )],
    questions=[
        ("Are 192.168.5.20 and 192.168.6.20 in the same subnet with mask 255.255.255.0?", "No — the network parts are 192.168.5 and 192.168.6."),
        ("What range can a Modbus server address use?", "1–247 (0 is broadcast)."),
        ("Which BACnet identifier must be unique across the whole internetwork?", "The device instance (device ID)."),
        ("What does 9600 8N1 mean?", "9,600 baud, 8 data bits, no parity, 1 stop bit."),
        ("Which UDP port does BACnet/IP use by default?", "47808 (0xBAC0)."),
    ],
)

P3 = dict(
    id="5-3", slug="modbus-rtu-and-tcp", title="Modbus RTU and Modbus TCP",
    objectives=[
        "Explain Modbus's client/server model and its four data tables.",
        "Use the common function codes and avoid the off-by-one address trap.",
        "Decode 16-bit and 32-bit values, including byte order and scaling.",
        "Recognise Modbus exception codes and timeouts.",
    ],
    one_line=("Modbus is a simple <strong>ask-and-answer</strong> protocol: a client asks a device for numbered registers, the device "
              "replies with raw 16-bit numbers — and it is up to you to know what each number means."),
    why=("<p>Modbus is everywhere: VFDs, energy meters, generators, UPSs, many chillers. It is easy to start with and easy to get "
         "subtly wrong — the device answers, but the values are nonsense because of an address offset, a data type or a byte "
         "order. Reading registers correctly is a core skill, practised in Lab 5.</p>"),
    body=(
        "<h3>How Modbus works</h3>"
        + bullets([
            "One <strong>client</strong> (traditionally “master”) — the BMS controller or gateway — sends requests.",
            "Each <strong>server</strong> (“slave”) — the VFD, meter — answers only when asked. Servers never talk on their own.",
            "<strong>Modbus RTU</strong> runs on RS485 serial lines; each server has an address 1–247.",
            "<strong>Modbus TCP</strong> carries the same requests over Ethernet (TCP port 502); a <strong>unit ID</strong> selects a device behind a gateway.",
        ])
        + "<h3>The four data tables</h3>"
        + table(["Table", "Size", "Access", "Traditional numbering", "Read / write function codes"], [
            ("Coils", "1 bit", "Read / write", "0xxxx (00001…)", "01 read · 05 write one · 15 write many"),
            ("Discrete inputs", "1 bit", "Read only", "1xxxx (10001…)", "02 read"),
            ("Input registers", "16 bit", "Read only", "3xxxx (30001…)", "04 read"),
            ("Holding registers", "16 bit", "Read / write", "4xxxx (40001…)", "03 read · 06 write one · 16 write many"),
        ])
        + callout("warn", "The off-by-one trap",
                  "<p>Documentation often numbers registers from 1 with a table prefix — <strong>40001</strong> — but on the wire the "
                  "first holding register is address <strong>0</strong>. So “40001” = function 03, address 0; “40010” = address 9. "
                  "Some tools and BMS drivers expect the documentation number, others the wire address. If every value looks "
                  "like its neighbour's, you are off by one.</p>")
        + "<h3>What a request looks like</h3>"
        + fig(d_modbus_frames(), "RTU frame: address, function, data, CRC. Modbus TCP drops the CRC and adds a 7-byte header with the unit ID.")
        + "<h3>Data types and byte order</h3>"
        + table(["Data type", "Registers", "Example"], [
            ("Unsigned 16-bit integer", "1", "0 to 65,535 — e.g. frequency in 0.1 Hz: 425 = 42.5 Hz"),
            ("Signed 16-bit integer", "1", "−32,768 to 32,767 — e.g. temperature in 0.1 °C: 65,486 read unsigned = −50 → −5.0 °C"),
            ("32-bit integer", "2", "Energy totals — kWh"),
            ("32-bit float (IEEE 754)", "2", "Many meters: 0x41B8 0x0000 = 23.0"),
        ])
        + "<p>32-bit values use two registers, and devices disagree on which comes first. The usual orders are "
          "<strong>ABCD</strong> (big-endian, high word first — the Modbus convention) and <strong>CDAB</strong> (word swapped). "
          "If a float reads as a huge or tiny nonsense number, try swapping the words.</p>"
        + tool("modbus", r1="16824", r2="0")
        + "<h3>An example register map</h3>"
        + "<p>Every device has its own map; this one is illustrative only — always use the map for the exact model and firmware.</p>"
        + table(["Register (doc)", "Wire address", "Description", "Type", "Scale"], [
            ("40001", "0", "Output frequency", "UINT16", "× 0.1 Hz"),
            ("40002", "1", "Motor current", "UINT16", "× 0.1 A"),
            ("40003", "2", "Output power", "UINT16", "× 0.1 kW"),
            ("40004–40005", "3–4", "Energy total", "UINT32 (ABCD)", "× 1 kWh"),
            ("40006", "5", "Last fault code", "UINT16", "code table"),
        ], "plain")
        + "<h3>When it goes wrong: exceptions and timeouts</h3>"
        + table(["Response", "Meaning", "Usual cause"], [
            ("No response (timeout)", "Nobody answered", "Wrong address, baud or parity; wiring; device off"),
            ("Exception 01 — illegal function", "Device does not support that function", "Using 03 where the device needs 04 (or the reverse)"),
            ("Exception 02 — illegal data address", "Register does not exist", "Off-by-one, wrong map, reading past the end"),
            ("Exception 03 — illegal data value", "Value or quantity not allowed", "Too many registers in one request; out-of-range write"),
            ("Exception 04 — device failure", "Device could not do it", "Device fault"),
            ("CRC errors", "Frame corrupted", "Noise, termination, baud mismatch"),
        ])
        + "<p>Polling settings matter too: <strong>timeout</strong> (how long to wait), <strong>retries</strong>, and <strong>poll "
          "rate</strong>. A slow bus with many registers and a short poll interval never catches up.</p>"
    ),
    ahu01=("<p>DDC-AHU-01 polls the VFD at <strong>address 1, 19200 8E1</strong> every 5 seconds with function 03 for the first six "
           "holding registers. It scales frequency and current by 0.1, combines two registers for kWh, and alarms if the VFD stops "
           "answering for 60 seconds. If the link fails, AHU-01 keeps running on its hard-wired points.</p>"),
    on_site=[
        "Get the register map for the exact model and firmware, and note whether it numbers from 0 or 1.",
        "Read a value you can verify on the device display first (e.g. frequency) to prove address, offset and scale.",
        "Read the fewest registers you need, in blocks; avoid hundreds of single-register requests.",
        "Only one client on an RTU bus. Two masters on one bus collide.",
    ],
    faults=[
        ("Every value is the one from the next register", "Off-by-one address", "Address base (0 or 1) in tool and BMS"),
        ("Float values like 1.7e−38 or 4.2e+9", "Wrong word order", "Try CDAB vs ABCD"),
        ("Value 65,486 for a temperature", "Signed value read as unsigned", "Data type signed 16-bit"),
        ("Exception 02 for every read", "Wrong register range for the device", "Register map; start address"),
        ("Timeouts on every device", "Settings or wiring", "Baud, parity, polarity, termination"),
    ],
    terms=[
        ("Client / server", "Modbus roles: the client asks, the server answers (formerly master/slave)."),
        ("Holding register", "16-bit read/write value (4xxxx); read with function 03."),
        ("Input register", "16-bit read-only value (3xxxx); read with function 04."),
        ("Coil / discrete input", "1-bit read/write and read-only values."),
        ("Function code", "Number identifying the request type, e.g. 03 read holding registers."),
        ("Exception code", "Error reply from a server, e.g. 02 illegal data address."),
        ("Byte / word order", "Order in which the bytes of a 32-bit value are sent (ABCD, CDAB…)."),
        ("Unit ID", "Field in Modbus TCP addressing a device behind a gateway."),
        ("CRC", "Error-check field at the end of every RTU frame."),
    ],
    scenarios=[dict(
        prompt="An energy meter's map lists “voltage L1 = 30001, float32”. Reading function 04, address 1, 2 registers gives nonsense; the device display shows 231.4 V. What do you try first?",
        options=["Change to function 03.", "Read from address 0 — the documentation number 30001 is wire address 0.",
                 "Change the baud rate."],
        answer=1,
        explain=(" 30001 is the first input register, which is address 0 on the wire. Reading from address 1 straddles two different "
                 "values. If address 0 still gives nonsense, then try the other word order."),
    )],
    questions=[
        ("Which function code reads holding registers?", "03."),
        ("What wire address is documentation register 40010?", "9 (function 03)."),
        ("A float reads as 4.2e+9 but should be about 230. What is the likely problem?", "Wrong word (or byte) order — try swapping the two registers (CDAB vs ABCD)."),
        ("What does exception 02 mean?", "Illegal data address — the register does not exist on that device."),
        ("How does Modbus TCP address a device behind a gateway?", "With the unit ID field in the MBAP header."),
    ],
)

P4 = dict(
    id="5-4", slug="bacnet-mstp-and-ip", title="BACnet MS/TP and BACnet/IP",
    objectives=[
        "Describe BACnet's object model: devices, objects and properties.",
        "Explain how devices are discovered and values read, written and reported.",
        "Use the priority array correctly when commanding outputs.",
        "Explain MS/TP token passing, BACnet/IP, routers and BBMDs.",
    ],
    one_line=("BACnet is the open protocol designed for building automation: every device describes itself as a set of "
              "<strong>objects</strong> (inputs, outputs, schedules…) with <strong>properties</strong>, that any BACnet client can "
              "discover, read and command."),
    why=("<p>BACnet (ASHRAE 135, also ISO 16484-5) is the main open protocol in BMS. Unlike Modbus, a BACnet device tells you what "
         "it has — names, units, alarm states — so integration is faster and more reliable. But it has more concepts to "
         "understand, and its priority array is one of the most misunderstood features in the industry.</p>"),
    body=(
        "<h3>Devices, objects, properties</h3>"
        + table(["Object type", "Represents", "Example"], [
            ("Device", "The controller itself — one per device, with its instance number", "DDC-AHU-01, instance 103021"),
            ("Analog Input / Output / Value (AI, AO, AV)", "Measured values, analogue outputs, software values", "RAT, CHW valve, RAT setpoint"),
            ("Binary Input / Output / Value (BI, BO, BV)", "On/off states and commands", "Fan status, fan command, occupancy flag"),
            ("Multi-state Input / Output / Value", "Several named states", "Mode: Off / Occupied / Unoccupied / Fire"),
            ("Schedule, Calendar", "Time programs and holiday lists", "AHU-01 occupancy schedule"),
            ("Trend Log", "Stored history of a value", "RAT every 5 minutes"),
            ("Notification Class", "Who receives which alarms, at what priority", "Critical alarms → on-call"),
            ("Loop", "A PID loop (on some devices)", "RAT → CHW valve"),
        ])
        + "<p>Each object has <strong>properties</strong>. The important ones: <strong>Present_Value</strong> (the value), "
          "<strong>Object_Name</strong>, <strong>Units</strong>, <strong>Status_Flags</strong> (in alarm, fault, overridden, "
          "out of service), <strong>Out_Of_Service</strong> (lets you test logic with a simulated value), <strong>Reliability</strong>, "
          "and for commandable objects the <strong>Priority_Array</strong> and <strong>Relinquish_Default</strong>.</p>"
        + "<h3>Services: how devices talk</h3>"
        + table(["Service", "Use"], [
            ("Who-Is / I-Am", "Discovery: “who is out there?” — each device answers with its instance and address"),
            ("ReadProperty / ReadPropertyMultiple", "Read values (many at once is far more efficient)"),
            ("WriteProperty", "Change a value or command an output, at a priority"),
            ("SubscribeCOV", "Ask a device to report a value only when it changes — less traffic than polling"),
            ("Event / alarm notifications", "Devices report alarms themselves (intrinsic reporting) to the recipients in a Notification Class"),
        ])
        + "<h3>The priority array</h3>"
        + fig(d_priority(), "Sixteen slots. The highest-priority non-empty slot wins.")
        + "<p>Commandable objects (outputs and some values) do not just have one value — they have <strong>16 priority slots</strong>. "
          "Each writer writes into its own slot; the <strong>lowest-numbered slot that is not empty</strong> decides the output. "
          "When every slot is empty (null), the output takes its <strong>Relinquish_Default</strong>.</p>"
        + table(["Priority", "Standard use"], [
            ("1", "Manual life safety"),
            ("2", "Automatic life safety"),
            ("5", "Critical equipment control"),
            ("6", "Minimum on/off time"),
            ("8", "Manual operator"),
            ("9–16", "Available for applications — the program and schedules typically use a low priority such as 16 (conventions vary by project)"),
        ], "plain")
        + callout("warn", "Release, don't overwrite",
                  "<p>To remove an operator override you <strong>relinquish</strong> it — write null at priority 8. Writing a new "
                  "value at 8 leaves the override in place, just with a different number, and the program stays locked out. "
                  "Forgotten writes at high priorities are a classic cause of “the program doesn't work”.</p>")
        + "<h3>BACnet MS/TP</h3>"
        + bullets([
            "Runs on RS485 (page 5.1). <strong>Master-Slave/Token-Passing</strong>: masters pass a token around in MAC-address order; only the holder may send.",
            "Masters use MAC 0–127; set <strong>Max_Master</strong> to at least the highest MAC used.",
            "Baud rates 9,600–115,200; 38,400 and 76,800 are common. All devices on the segment must match.",
            "Cheap and robust for FCU, VAV and other room-level devices; slower than IP.",
        ])
        + "<h3>BACnet/IP, routers and BBMDs</h3>"
        + fig(d_bacnet_net(), "Routers join different network types; BBMDs carry broadcasts between IP subnets.")
        + bullets([
            "<strong>BACnet/IP</strong> sends BACnet messages in UDP packets, default port <strong>47808</strong>.",
            "Discovery (Who-Is) uses <strong>broadcasts</strong>, which IP routers do not forward. A <strong>BBMD</strong> (BACnet Broadcast Management Device) in each subnet forwards them to the others listed in its broadcast distribution table.",
            "A single device outside any BBMD subnet can join as a <strong>foreign device</strong> by registering with a BBMD.",
            "A <strong>BACnet router</strong> joins different networks — for example BACnet/IP to MS/TP. Every network gets a unique <strong>network number</strong>.",
            "<strong>BACnet/SC</strong> (Secure Connect) is the newer, encrypted transport using TLS — increasingly specified for cyber-security.",
        ])
        + callout("note", "PICS and BTL",
                  "<p>A device's <strong>PICS</strong> (Protocol Implementation Conformance Statement) lists exactly which objects "
                  "and services it supports. <strong>BTL</strong> listing shows it was tested by the BACnet Testing Laboratories. "
                  "Check both when selecting devices for integration.</p>")
    ),
    ahu01=("<p>DDC-AHU-01 is a BACnet/IP device, instance <strong>103021</strong>. Its points are BACnet objects: RAT is AI-1, the CHW "
           "valve is AO-1, the fan command is BO-1, the RAT setpoint is AV-1, the occupancy schedule is Schedule-1. The program "
           "writes the valve at priority 16; an operator override from the graphic writes at priority 8 and must be relinquished "
           "afterwards. The FCUs on the floor are on MS/TP behind the supervisory controller, which acts as the router.</p>"),
    on_site=[
        "Discover with a BACnet explorer tool (the free YABE is widely used) to see devices, objects and priority arrays directly.",
        "When an output ignores the program, look at its priority array before anything else.",
        "Plan network numbers and device instances for the whole site before commissioning.",
        "Use ReadPropertyMultiple and COV where available — they cut network load dramatically.",
    ],
    faults=[
        ("Program writes have no effect", "A higher-priority slot (e.g. 8) holds an old override", "Priority array; relinquish it"),
        ("Devices on another subnet not discovered", "No BBMD or BBMD tables incomplete", "BBMD configuration on both subnets"),
        ("Two devices appear and disappear alternately", "Duplicate device instance", "Instance plan; scan"),
        ("MS/TP devices missing above a certain MAC", "Max_Master too low", "Max_Master on every master"),
        ("Router shows networks but no devices on one", "Duplicate or wrong network number", "Network numbers on each router port"),
    ],
    terms=[
        ("BACnet", "Open data communication protocol for building automation (ASHRAE 135 / ISO 16484-5)."),
        ("Object", "A BACnet representation of a point or function, e.g. Analog Input."),
        ("Property", "An attribute of an object, e.g. Present_Value, Units."),
        ("Who-Is / I-Am", "Discovery services."),
        ("COV", "Change of value — reporting only when a value changes."),
        ("Priority array", "Sixteen command slots; the highest-priority non-null slot sets the output."),
        ("Relinquish", "Write null to a priority slot, removing that command."),
        ("Relinquish_Default", "Value used when every priority slot is null."),
        ("BBMD", "BACnet Broadcast Management Device — forwards broadcasts between IP subnets."),
        ("PICS", "Protocol Implementation Conformance Statement — what a device supports."),
        ("BACnet/SC", "Secure Connect — encrypted BACnet transport over TLS."),
    ],
    scenarios=[dict(
        prompt="After commissioning, AHU-01's CHW valve stays at 0 % whatever the PID loop does. The priority array shows 0 % at priority 8 and 62 % at priority 16. What do you do?",
        options=["Write 62 % at priority 8.", "Relinquish (write null to) priority 8, so the program's value at 16 takes control.",
                 "Restart the controller."],
        answer=1,
        explain=(" A leftover operator override at priority 8 outranks the program at 16. Writing a new value at 8 keeps the program "
                 "locked out; relinquishing removes the override. Then find out who left it."),
    )],
    questions=[
        ("Which property holds a BACnet object's current value?", "Present_Value."),
        ("What is the difference between polling and COV?", "Polling asks repeatedly; COV subscriptions make the device report only when the value changes, reducing traffic."),
        ("Priorities 8 and 16 both hold values. Which wins?", "Priority 8 — the lowest number that is not null."),
        ("Why are BBMDs needed?", "Discovery and some services use broadcasts, which IP routers do not pass between subnets; BBMDs forward them."),
        ("What does a PICS tell you?", "Which BACnet objects, properties and services a device supports."),
    ],
)

P5 = dict(
    id="5-5", slug="communication-troubleshooting", title="Communication troubleshooting",
    objectives=[
        "Troubleshoot communication faults layer by layer, from the cable up.",
        "Choose the right tool for each layer.",
        "Recognise the symptoms of the most common Modbus, MS/TP and BACnet/IP faults.",
        "Isolate a faulty device or segment on a bus quickly.",
    ],
    one_line=("Fix communication faults <strong>from the bottom up</strong>: prove the wiring, then the settings, then the protocol "
              "details, then the application — and split the network in half until the fault has nowhere left to hide."),
    why=("<p>Communication faults look the same on the screen — “offline”, “?”, frozen values — whatever the cause. Guessing at "
         "settings wastes hours. A fixed order of checks, and the right tool at each step, turns them into routine jobs.</p>"),
    body=(
        fig(d_layers(), "Most faults are in the bottom two layers. Do not skip them.")
        + "<h3>The tools</h3>"
        + table(["Tool", "Layer", "Use"], [
            ("Multimeter", "Physical", "A–B resistance, bias voltage, power, continuity (page 5.1)"),
            ("Device LEDs (TX/RX, link)", "Physical / settings", "Is anything being sent and received?"),
            ("USB–RS485 adapter + Modbus master tool (e.g. Modbus Poll, QModMaster)", "Settings / protocol", "Talk to one device directly, bypassing the BMS"),
            ("BACnet explorer (e.g. YABE)", "Settings / protocol / application", "Discover devices, read objects and priority arrays"),
            ("ping / arp", "Physical / settings (IP)", "Is the IP address reachable? Is it duplicated?"),
            ("Wireshark", "Protocol", "Capture and decode BACnet/IP and Modbus TCP packets"),
            ("The controller's own diagnostics", "All", "Error counters, token statistics, last-error messages"),
        ])
        + "<h3>Step by step</h3>"
        + steps([
            "<strong>Define the scope.</strong> One point, one device, one segment, or everything? Shared symptoms point to shared causes.",
            "<strong>Physical.</strong> Power on? Cable continuous, right polarity, right topology? Termination and bias correct? IP link lights on?",
            "<strong>Settings.</strong> Address, baud, parity, stop bits; IP, mask, gateway; device instance, MAC, Max_Master, network numbers. Compare with the numbering plan.",
            "<strong>Talk to it directly.</strong> Connect a laptop tool straight to the device. If the tool works and the BMS does not, the problem is in the BMS configuration.",
            "<strong>Protocol details.</strong> Function code, register address and offset, data type, word order, scaling; BACnet object type and instance.",
            "<strong>Application.</strong> Poll rate and timeouts, too many points, overrides in the priority array.",
            "<strong>Divide and conquer</strong> a bus: disconnect half; whichever half still fails holds the fault. Repeat.",
        ])
        + "<h3>Symptoms and causes</h3>"
        + table(["Protocol", "Symptom", "Most likely causes"], [
            ("Modbus RTU", "Timeout from one device", "Address, baud/parity mismatch on that device; its wiring or power"),
            ("Modbus RTU", "Timeouts from all devices", "Master port settings; polarity at the master; termination/bias; broken trunk"),
            ("Modbus", "Values wrong but answers arrive", "Offset, data type, word order, scale"),
            ("Modbus", "Exception 02", "Register not on this device — offset or wrong map"),
            ("Modbus RTU", "Many CRC errors", "Noise, missing terminators, two masters, baud mismatch on one device"),
            ("MS/TP", "Whole segment offline", "Baud mismatch on one device, short circuit, polarity, termination"),
            ("MS/TP", "Devices above a MAC missing", "Max_Master too low"),
            ("MS/TP", "Devices drop out under load", "Too many devices or too much traffic; token timing; poor wiring"),
            ("MS/TP", "Duplicate MAC", "Two devices fight; both flap on and off"),
            ("BACnet/IP", "Found on own subnet only", "BBMD missing or tables wrong; gateway"),
            ("BACnet/IP", "Ping works, BACnet doesn't", "UDP 47808 blocked; different BACnet port"),
            ("BACnet/IP", "Device appears with wrong name or flaps", "Duplicate device instance"),
            ("Any", "Values update slowly", "Poll interval, too many points, slow baud, no COV"),
        ])
        + callout("tip", "Write it down", "<p>Record what you checked and the readings — A–B resistance, settings, error counts. "
                  "Communication faults often return, and a log turns the next visit into a five-minute job.</p>")
    ),
    ahu01=("<p>Worked example: the AHU-01 graphic shows the VFD's kW as “?”. Hard-wired points are fine, so only the Modbus link is "
           "affected. (1) Physical: A–B resistance with power off = 60 Ω; the drive's RS485 LED never flashes. (2) Settings: the "
           "drive was replaced last week and its parameters are at factory default — 9600 8N1, address 1 — while the controller "
           "uses 19200 8E1. Set the drive to 19200 8E1, and the values return. Add the drive's parameters to the as-built "
           "records so the next replacement goes faster.</p>"),
    on_site=[
        "Ask what changed recently — a replaced device, a firmware update, new IT equipment. Most faults follow a change.",
        "Check the device's diagnostics page or error counters before swapping hardware.",
        "Keep a known-good USB–RS485 adapter and a laptop with Modbus and BACnet tools in your kit.",
        "Never reconfigure a working device's address “to see if it helps” without writing down the original.",
    ],
    faults=[
        ("Everything offline after an IT switch replacement", "BMS VLAN not configured on the new switch", "Switch port VLAN; link lights"),
        ("Replaced VFD not communicating", "New drive at factory default settings", "Address, baud, parity on the drive"),
        ("BACnet devices vanish every few minutes", "Duplicate device instance or IP", "Scan with an explorer; check the plan"),
        ("Bus works until the plant starts", "Noise from VFD motor cables", "Cable route, screen earthing, isolated repeater"),
        ("Values frozen but device shows online", "Polling stopped or COV subscription lapsed", "Driver status; resubscribe"),
    ],
    terms=[
        ("Bottom-up troubleshooting", "Checking physical layer first, then settings, protocol and application."),
        ("Divide and conquer", "Splitting a network in halves to locate a fault."),
        ("Modbus master tool", "Software that sends Modbus requests directly to a device (e.g. Modbus Poll, QModMaster)."),
        ("BACnet explorer", "Software that discovers and reads BACnet devices (e.g. YABE)."),
        ("Wireshark", "Network packet capture tool that decodes BACnet/IP and Modbus TCP."),
        ("Error counters", "Device statistics of CRC errors, timeouts and token faults."),
    ],
    scenarios=[dict(
        prompt="On an MS/TP floor bus, all 20 FCUs went offline at 10:00. An electrician installed one new FCU controller at 09:55. Power is fine everywhere. What is the most likely cause?",
        options=["The BMS server crashed.", "The new controller has a different baud rate (or a duplicate MAC), disrupting the whole segment.",
                 "All 20 FCU controllers failed together."],
        answer=1,
        explain=(" A single device with a mismatched baud rate or duplicate MAC can upset token passing for the whole MS/TP segment. "
                 "Disconnect the new device: if the others return, configure it correctly before reconnecting."),
    )],
    questions=[
        ("List the four layers in bottom-up order.", "Physical → settings → protocol/data → application."),
        ("Your laptop Modbus tool reads the device perfectly, but the BMS shows timeouts. Where is the fault?", "In the BMS side: its port settings, driver configuration, addresses or polling."),
        ("Ping works but BACnet/IP discovery fails. Name two causes.", "UDP 47808 blocked by a firewall; device on another subnet without a BBMD; non-standard BACnet port."),
        ("How does divide and conquer work on a bus?", "Disconnect half of the bus; the half that still shows the fault contains it. Repeat until one device or cable section is left."),
        ("What should you ask first when a working system stops communicating?", "What changed — replaced devices, firmware, IT equipment, new devices on the bus."),
    ],
)

MODULE_INTRO = (
    "<p>Communication is what turns separate controllers and devices into one system. This module starts with the RS485 cable "
    "and addressing, then covers the two protocols you will use most — Modbus and BACnet — and finishes with a method for "
    "finding communication faults. The subnet checker (5.2) and Modbus decoder (5.3) are there to practise with; Lab 5 puts "
    "Modbus into your hands with free tools.</p>"
)

PAGES = [P1, P2, P3, P4, P5]

QUIZ = [
    mcq("RS485 defines…", ["the message format", "the electrical signalling only", "IP addressing", "BACnet objects"], 1,
        "Protocols such as Modbus RTU and MS/TP run on top of it.", "5.1"),
    mcq("A–B resistance with power off reads about 120 Ω on a long bus. This suggests…", ["correct termination", "one terminator missing", "too many terminators", "a short circuit"], 1,
        "Two terminators in parallel give about 60 Ω.", "5.1"),
    mcq("10.1.3.21/24 and 10.1.4.21/24 are…", ["in the same subnet", "in different subnets", "duplicate addresses", "invalid"], 1,
        "The network parts are 10.1.3 and 10.1.4.", "5.2"),
    mcq("Which identifier must be unique across the whole BACnet internetwork?", ["MS/TP MAC", "Modbus address", "Device instance", "Baud rate"], 2,
        "MS/TP MACs only need to be unique per segment.", "5.2"),
    mcq("Modbus function 03 reads…", ["coils", "discrete inputs", "input registers", "holding registers"], 3, "03 = read holding registers.", "5.3"),
    mcq("Documentation register 40001 is wire address…", ["0", "1", "40000", "40001"], 0, "The first holding register is address 0 on the wire.", "5.3"),
    mcq("A float value reads 4.2e+9 instead of ~230. Try…", ["a different baud", "swapping the word order", "function 05", "a new cable"], 1,
        "Devices differ in ABCD vs CDAB order.", "5.3"),
    mcq("A BACnet output has values at priorities 8 and 16. Which applies?", ["16", "8", "The average", "Relinquish_Default"], 1,
        "The lowest-numbered non-null slot wins.", "5.4"),
    mcq("BACnet discovery fails across IP subnets. What is usually missing?", ["A terminator", "A BBMD", "Max_Master", "A CRC"], 1,
        "Routers do not forward broadcasts; BBMDs do.", "5.4"),
    mcq("A Modbus tool on a laptop reads the device fine, but the BMS cannot. The fault is in…", ["the cable", "the device", "the BMS configuration", "the device's power"], 2,
        "The device and its settings are proven by the direct test.", "5.5"),
]

FINAL = [
    mcq("Where are RS485 terminators fitted?", ["At every device", "At the two ends of the bus", "At the master only", "Nowhere"], 1,
        "120 Ω at each physical end.", "5.1"),
    mcq("BACnet/IP's default UDP port is…", ["502", "47808", "80", "1883"], 1, "47808 = 0xBAC0.", "5.2"),
    mcq("Modbus exception 02 means…", ["illegal function", "illegal data address", "device busy", "CRC error"], 1, "The register does not exist.", "5.3"),
    mcq("To remove an operator override at BACnet priority 8 you…", ["write 0 at priority 8", "relinquish (write null) at priority 8", "write at priority 16", "restart the device"], 1,
        "Writing a new value leaves the override in place.", "5.4"),
    mcq("All 20 MS/TP devices went offline just after one new device was added. First action?", ["Replace the server", "Disconnect the new device and check its baud and MAC",
        "Re-address all devices", "Change the cable"], 1, "One mismatched device can upset the whole segment.", "5.5"),
]
