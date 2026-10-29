"""EarthPress STEM check calculations (EPR-STM-001, STANDARDS section 20).

Run from the repo root after the calculation note:
    python docs/04-calcs/sizing.py        (writes docs/04-calcs/results.csv)
    python docs/04-calcs/stem_check.py    (reads it, writes docs/04-calcs/stem_results.csv)

Option A (the current design, a lever and toggle press) takes every number from EPR-CAL-001 through results.csv.
Options B (power screw press) and C (rope-lifted drop rammer) are checked here at first order, with their
masses from cad/fidelity.json. Rows S9 and S10 failed on the 35 mm C45 pins of CAL v0.6 (pin bending, lug
bearing) and were closed by the fix of 2026-10-25 under Amish's standing instruction of 2026-10-23 (EPR-DEC-001,
decision F1); the v0.6 values are printed by sizing.py for the record.
"""
import csv
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit")]
from stem_check import Check, limits, G, WITHIN, PLAUSIBLE  # noqa: E402

R = {r["quantity"]: r["value"] for r in csv.DictReader((ROOT / "docs/04-calcs/results.csv").open())}


def num(key, i=0):
    """The i-th number in a results.csv value."""
    return float(re.findall(r"-?[\d,]*\.?\d+", R[key].replace(",", ""))[i])


fid = json.loads((ROOT / "cad/fidelity.json").read_text())
c = Check(ROOT / "docs/04-calcs/stem_results.csv")
CAL = "EPR-CAL-001"
FIX = "EPR-DEC-001 F1 (2026-10-25, standing instruction)"

# ------------------------------------------------------------------ option A: lever and toggle press
area = 0.290 * 0.140
c.order_of_magnitude("S1", "The press needs 81.2 kN on the 290 x 140 mm block face for 2 MPa", "Mathematics", "Units and dimensional analysis",
                     claimed=num("Force for 2 MPa (nominal)"), estimate=2.0e6 * area / 1e3, unit="kN", law="F = p A", closed_by=CAL)
c.cited("S2", "Compacting a 5 % cement mix to 2 MPa gives blocks that can meet the R3 strength class with suitable soil", "Physics", "Mechanics and statics",
        "Auroville Earth Institute: CSEB pressed at 2 to 4 MPa with about 5 % cement; the Auram press 3000 works at 2.7 to 5.3 MPa",
        "2 MPa is the low end of practice; strength depends on soil, mix and curing and is measured in block tests (TRL 4, on hold)", PLAUSIBLE)
theta = math.radians(6.0)
toggle = 1 / (2 * math.tan(theta))
lever = 1650.0 / num("Connecting link moment arm about the lever pivot at the stop")
c.order_of_magnitude("S3", "The lever and toggle give a force ratio of 173:1 at the crank stop", "Physics", "Mechanics and statics",
                     claimed=num("Overall force ratio at the end of the stroke"), estimate=toggle * lever, unit=":1",
                     law="Toggle 1 / (2 tan 6 deg) times grip radius over the connecting link's arm (virtual work)", closed_by=CAL)
c.balance("S4", "Two people on the 1.71 m grip path supply the compaction work of the softer design soil", "Physics", "Mechanics and statics",
          inputs={"two operators, 500 N each over the grip path": 2 * 500 * num("Grip path length")},
          outputs={"compaction work, soil 20 mm per decade": num("Compaction work, soil 20 mm per decade")}, unit="J", closed_by=CAL)
c.cited("S5", "Each of two operators pulls no more than 500 N at the peak, with the softer design soil", "Biology", "Ergonomics",
        "Peak grip force from the force ratio and the soil law (CAL section 4b); project limit 500 N per operator (R5, PR-005); ISO 11228-2 screening to assess",
        f"{num('Peak grip force at nominal fill, per operator (two on the T-handle)'):.0f} N against 500 N, but it rests on the assumed soil law (S6) and on equal shares between the two operators; "
        "measure on partner soils", PLAUSIBLE)
c.cited("S6", "Soil pressure in the mold rises tenfold over the last 14 mm of the stroke (10 to 20 mm)", "Physics", "Mechanics and statics",
        "Assumed exponential compaction law; no measured curve for the partner's soils",
        "Measure pressure against travel on partner soils (compaction test); S4, S5 and the fill window rest on it", PLAUSIBLE)
c.claim("S7", "Every load-path member stays below yield at the 173 kN design load (1,000 N at the grip at the stop)", "Physics", "Strength of materials",
        "Bending, shear, bearing, net section and buckling against yield of S235/S250 plate, A53 pipe and 42CrMo4 +QT pins (CAL Table 5)",
        1.0, num("Lowest safety factor on yield or capacity (abuse case)"), "of yield", rule="below", closed_by=CAL)
c.cited("S8", "A 10 kg scale with 50 g divisions can hold the fill to its window of 0 to +206 g", "Engineering and technology", "Sensing resolution",
        "Scale division against half the fill window (CAL section 5)",
        f"50 g division against a half-width of {num('Half-width of the fill window'):.0f} g for the base soil, but the softer design soil has a window of about 0 to +153 g (half-width 76 g), "
        "a division is not the scale's accuracy (a low-cost 10 kg scale is about 50 to 100 g) and a 1 % moisture swing moves the dry mass by about 70 g: confirm scale accuracy and moisture control", PLAUSIBLE)
c.claim("S9", "The 40 mm 42CrMo4 +QT toggle pins stay below yield in bending at the 173 kN design load", "Physics", "Strength of materials",
        "Pin in a clevis: link force per side times the distance between bearing centres (base pin 36 mm arm), M / (pi d^3 / 32) against "
        "Rp0.2 750 MPa for 16 < d <= 40 mm; the 35 mm C45 pins of CAL v0.6 failed (388 MPa against 370 MPa at the nominal load, 826 MPa at 173 kN)",
        num("Base pin 40 mm in bending, arm 36 mm, abuse"), 750.0, "MPa", closed_by=FIX)
c.claim("S10", "The base pin lugs carry the design load within the bush bearing allowable", "Physics", "Strength of materials",
        "Bearing p = F / (2 t d) on 2 x 28 mm lugs at 40 mm, allowable 100 MPa for hardened greased bushes (assumed); the 20 mm lugs on 35 mm reached 124 MPa",
        num("Base pin lug bearing, 2 x 28 mm on the 40 mm bush bore, abuse"), 100.0, "MPa", closed_by=FIX)
c.claim("S11", "Welded members last 50,000 blocks in fatigue", "Physics", "Strength of materials",
        "Nominal stress range per block against a FAT 71 detail at 50,000 cycles (EN 1993-1-9 method)",
        num("Highest nominal stress range per block in a welded member"), num("Allowed range, FAT 71 welded detail at 50,000 cycles"), "MPa", closed_by=CAL)
c.claim("S12", "The turned toggle pins last 50,000 blocks in bending fatigue", "Physics", "Strength of materials",
        "Pulsating range against 0.5 Rm x 0.7 for surface and size (Rm 1,000 MPa minimum, 42CrMo4 +QT; first-order)",
        num("Highest nominal bending stress range in a toggle pin per block"), num("Allowed range for the turned 42CrMo4 +QT pins (0.5 Rm x 0.7, assumed)"), "MPa", margin=0.2, closed_by=CAL)
c.order_of_magnitude("S13", "Released at the stop, the lever kicks back with about 47 J", "Physics", "Mechanics and statics",
                     claimed=num("Energy returned to the lever if released at the end"), estimate=0.5 * 81.2e3 * (1.0 + num("Column stretch at 2 MPa")) / 1000, unit="J",
                     law="Strain energy 0.5 F d with 1.0 mm soil rebound (assumed) and the column stretch", closed_by=CAL)
c.cited("S14", "One person ejects the block with 470 N or less on the eject lever", "Physics", "Mechanics and statics",
        "Wall friction 0.1 MPa residual lateral pressure x 0.6 x wall area, plus piston and block weight, over the 10.3:1 eject ratio (assumed residual pressure)",
        f"{num('Grip force to eject'):.0f} N against 500 N, a margin of about 6 % that rests on the assumed 0.1 MPa residual pressure (at 0.2 MPa the force would be about 930 N): measure on partner soils", PLAUSIBLE)
c.order_of_magnitude("S15", "A crew of four makes about 296 blocks in an 8 h day", "Mathematics", "Orders of magnitude",
                     claimed=num("Blocks per 8 h day (7 h working)"), estimate=500.0, unit="blocks",
                     law="Makiga manual press, 290 x 140 mm blocks, about 500 a day with a crew of four (Engineering for Change); EarthPress cycle 85 s assumed (CAL section 9)")
c.cited("S16", "Curing blocks bind about 0.23 kg of water per kg of cement", "Chemistry", "Physical chemistry",
        "Non-evaporable water of fully hydrated Portland cement about 0.23 g/g (Powers and Brownyard; Neville, Properties of Concrete)",
        "Used only for the cured mass in the flow figure; 712 kg per 100 blocks", WITHIN, closed_by=CAL)
c.claim("S17", "CSEB walling embodies 25 % or less of the CO2 of fired brick of equal volume", "Chemistry", "Environmental and atmospheric chemistry",
        "Auroville Earth Institute factors: 49 kg CO2/m3 for 5 % CSEB, 643 kg CO2/m3 for locally fired brick (a bottom-up count of this design's 556 kg of cement at about 0.9 kg CO2/kg gives about 0.5 t, 11 % of the brick figure)", num("CSEB as a share of fired brick"), 25.0, "%", closed_by=CAL)
c.cited("S18", "Lime at about 8 % stabilizes clay-rich soils, with a longer curing period than cement", "Chemistry", "Inorganic chemistry",
        "Lime and clay react slowly (cation exchange, then pozzolanic calcium silicate and aluminate hydrates); needs enough clay and moisture",
        "Starting value only; wet-strength tests on partner soils decide the dose and the curing time (TRL 4, on hold)", PLAUSIBLE)
c.cited("S19", "Sieving dry soil raises respirable crystalline silica, so damp sieving and an FFP2 or N95 respirator are specified", "Biology", "Toxicology",
        "Crystalline silica is carcinogenic to humans (IARC Group 1, Monograph 100C); OSHA PEL 50 ug/m3 over 8 h (29 CFR 1926.1153)",
        "Hazard and controls stated in PRC, BLD and RSK; no exposure claim is made", WITHIN, closed_by="EPR-RSK-001")
c.cited("S20", "Wet cement can burn skin and eyes, so gloves and eye protection are specified", "Biology", "Toxicology",
        "Portland cement safety data sheets: causes skin irritation and serious eye damage (hazard statements H315, H318); wet mix is strongly alkaline",
        "Hazard and controls stated in PRC, BLD and RSK", WITHIN, closed_by="EPR-RSK-001")
c.cited("S21", "Two people can lift the heaviest piece of the press", "Biology", "Ergonomics",
        "ISO 11228-1 reference mass 25 kg per person for occasional lifts; two people share the piece",
        f"{num('Heaviest single piece') / 2:.1f} kg per person if the load halves exactly, but team lifting usually reduces each person's share of the capacity and the 25 kg figure is for ideal conditions: "
        "to assess; lift with a trolley, a hoist or four people", PLAUSIBLE)
c.claim("S22", "The grip stays at 0.8 m or higher through the stroke, with the peak force at 1.0 m or higher", "Biology", "Ergonomics",
        "Lever kinematics (CAL section 3); R5 band", 800.0, num("Grip height at start / end", 1), "mm", rule="below", closed_by=CAL)
c.claim("S23", "The mold walls bulge far less than the 2 mm block tolerance at 2 MPa", "Physics", "Strength of materials",
        "Fixed-fixed wall strip with the belt, lateral pressure 0.5 x vertical (assumed K0)", num("Mold wall bulge at 2 MPa"), 2.0, "mm", closed_by=CAL)

# ------------------------------------------------------------------ option B: power screw press (first order)
F = 81.2e3
d2, lead, P_ = 36.5, 14.0, 7.0                      # Tr 40 x 14 (P7) two-start: pitch diameter, lead, pitch (mm)
lam = math.atan(lead / (math.pi * d2))
phi = math.atan(0.15 / math.cos(math.radians(15)))   # trapezoidal thread, 30 deg included, mu 0.15 dry to greased steel on bronze
T = F * d2 / 2e3 * math.tan(lam + phi) + 0.005 * F * 0.027     # N m, plus the thrust bearing
r_grip = 0.53
Fop = T / (2 * r_grip)
c.claim("B1", "Option B: two people on a 1.2 m capstan turn the screw at the 81 kN pressing force within 500 N each", "Physics", "Mechanics and statics",
        f"Power screw torque T = F d2 / 2 tan(lambda + phi'), lambda {math.degrees(lam):.1f} deg, phi' {math.degrees(phi):.1f} deg (mu 0.15), T {T:.0f} N m; grips 0.53 m from the axis",
        round(Fop), 500.0, "N")
phi_lo = math.atan(0.10 / math.cos(math.radians(15)))
c.cited("B2", "Option B: the two-start screw is self-locking, so it holds the load without a pawl", "Physics", "Mechanics and statics",
        "Self-locking when the lead angle is below the friction angle",
        f"lambda {math.degrees(lam):.1f} deg against phi' {math.degrees(phi):.1f} deg at mu 0.15 but {math.degrees(phi_lo):.1f} deg at mu 0.10 (well greased): "
        "not self-locking when greased; a brake or a single-start screw would be needed", PLAUSIBLE)
H1 = 0.5 * P_
n_th = 90.0 / P_
p_nut = F / (math.pi * d2 * H1 * n_th)
c.claim("B3", "Option B: a 90 mm bronze nut carries the pressing force within its bearing allowable", "Physics", "Strength of materials",
        "Thread bearing p = F / (pi d2 H1 n); hand press, steel screw on bronze nut, 17 to 24 MPa (Shigley, Table 8-4)", round(p_nut, 1), 17.0, "MPa", margin=0.1)
A3 = math.pi * 32.0 ** 2 / 4
F_max_b = 2 * 500.0 * r_grip / (d2 / 2e3 * math.tan(lam + phi))     # N, ignoring the small bearing friction
c.claim("B4", "Option B: the screw's root section stays below yield at the largest force two people can make", "Physics", "Strength of materials",
        "Root diameter 32 mm; two people at 500 N on 0.53 m give the largest force; C45 yield 340 MPa (first-order)",
        round(F_max_b / A3), 340.0, "MPa")
cyc_b = 25 + 5 + 14 + 20 + 14 + 10 + 15 + 8
c.order_of_magnitude("B5", "Option B: a crew of four makes about 225 blocks a day", "Mathematics", "Orders of magnitude",
                     claimed=225, estimate=500.0, unit="blocks",
                     law=f"Makiga manual press about 500 a day (Engineering for Change); option B cycle {cyc_b} s with 14 unloaded turns each way ({7 * 3600 / cyc_b:.0f} a day)")
eta = math.tan(lam) / math.tan(lam + phi)
c.balance("B6", "Option B: the operators supply the pressing work through a screw of about 43 % efficiency", "Physics", "Mechanics and statics",
          inputs={"two operators, 4.3 loaded turns": 2 * 500 * 2 * math.pi * r_grip * 4.3}, outputs={"compaction work / efficiency": 705.0 / eta}, unit="J")

# ------------------------------------------------------------------ option C: rope-lifted drop rammer (first order)
E_std = 592.7e3 * 0.290 * 0.140 * 0.090            # J, ASTM D698 standard effort over the pressed block volume
blow = 20.0 * G * 0.450
c.order_of_magnitude("C1", "Option C: about 25 blows of a 20 kg weight falling 450 mm give standard Proctor compaction energy", "Physics", "Mechanics and statics",
                     claimed=25, estimate=E_std / blow, unit="blows", law="ASTM D698 standard effort 592.7 kJ/m3 over the 3.65 L block; blow energy m g h")
c.cited("C2", "Option C: impact compaction at standard Proctor effort reaches the density of 2 MPa static pressing", "Physics", "Mechanics and statics",
        "Impact and static compaction give different density profiles; impact from the top densifies the top layer most",
        "No source equates the two for CSEB; test blocks needed", PLAUSIBLE)
c.claim("C3", "Option C: each of two people pulls under 500 N on the rope, even when lifting the plunger for filling", "Biology", "Ergonomics",
        "Weight, rod and plunger about 40 kg, shared by two over the head pulley", round(40 * G / 2), 500.0, "N")
c.claim("C4", "Option C: the operators' sustained power stays within human capacity", "Biology", "Human physiology and biomechanics",
        "25 blows of 88 J in 100 s, shared by two; sustained adult output about 75 W", round(25 * blow / 100 / 2, 1), limits.HUMAN_SUSTAINED_W, "W")
c.order_of_magnitude("C5", "Option C: a crew of four makes about 160 blocks a day", "Mathematics", "Orders of magnitude",
                     claimed=160, estimate=500.0, unit="blocks",
                     law="Makiga manual press about 500 a day (Engineering for Change); option C cycle 160 s (25 blows at 15 a minute plus 60 s)")
c.cited("C6", "Option C: the mold, plunger and floor stop survive the impact peak force", "Physics", "Strength of materials",
        "Impact force depends on the soil's stiffness at the end of compaction, not yet known", "To be estimated from a measured soil stiffness (S6)", PLAUSIBLE)

state = c.write()
for k in ("A", "B", "C"):
    o = fid["options"][k]
    print(f"option {k} ({o['title']}): {o['parts']} parts, {o.get('mass_kg')} kg in the model")

# ------------------------------------------------------------------ write Table 1 into docs/01b-stem-check.md
doc = ROOT / "docs/01b-stem-check.md"
if doc.exists():
    head = "| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n"
    body = "".join(f"| {r['id']} | {r['claim']} | {r['field']} | {r['branch']} | {r['law']} | {r['check']} | {r['verdict']} | {r['closed_by'] or 'Open'} |\n" for r in c.rows)
    t = doc.read_text()
    a, b = t.index("<!-- STM_TABLE -->") + len("<!-- STM_TABLE -->\n"), t.index("<!-- /STM_TABLE -->")
    doc.write_text(t[:a] + head + body + t[b:])
    print(f"wrote Table 1 into {doc.relative_to(ROOT)}")
