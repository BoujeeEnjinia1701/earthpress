---
doc_id: EPR-CAL-001
title: EarthPress sizing calculations
project: EarthPress
doc_type: Calculation note
version: "0.8"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (force, linkage kinematics, grip force and work, fill tolerance, structure at the design load, ejection, mass, output, material flow, carbon, cost) against every requirement in EPR-REQ-001
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: "Recommendations accepted by Amish (DDR-002). R5, R7 and R13 checked against the accepted targets (500 N per operator, grip 0.8 to 1.9 m with the peak at 1.0 m or higher; 190 kg total; $500 budget); script reads the budget from project.yaml"
- version: "0.3"
  date: '2026-10-01'
  author: Amish Chadha
  change: "Constructable design (EPR-DDR-003): lid span 420 mm between the hinge and latch pins, link net section at the 41 mm bush, column access holes, eject arm, mass with guard and bolts (200 kg, R7 not met), cost $520 (R13 not met)"
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R7 against the 200 kg total set on 2026-10-02 (met on paper); softer design soil for the operating chart noted under R5; sizing.py still to be re-run"
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'sizing.py re-run: R7 met at 200 kg (199.996 kg with the dust seals), BOM USD 523 with dust seals (R13 over by USD 23); operating chart for the softer design soil and the scoop rule added (section 5b)'
- version: "0.7"
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Kit 1.9.1: pin bending and lug bearing checked (section 6b); the 35 mm C45 pins failed and were replaced by 40 mm 42CrMo4 +QT pins in 40 x 46 mm bushes with 28 mm lugs (EPR-DEC-001 F1, standing instruction); masses from the detailed model with bushes, fasteners and weld metal (203.8 kg, R7 not met); BOM USD 542; requirements renumbered PR-001 to PR-016 (EPR-PRS-001)'
- version: "0.8"
  date: '2026-10-30'
  author: Amish Chadha
  change: "R7 against the 205 kg total decided by Amish on 2026-10-30 (EPR-DDR-005 D2): met on paper, margin 1.2 kg; sizing.py re-run"
---

# EarthPress sizing calculations

On paper the press reaches 2 MPa on the 290 x 140 x 90 mm block, but only with **two people on the lever** and a **weighed fill**. The toggle and 1.7 m lever give a force ratio of 173:1 at the stop, and the peak pull under the base soil assumption is **668 N**, which comes about 3 mm before the end of the stroke. One operator pulling 500 N stalls at about 0.5 MPa, so the press is a two-person machine, as Amish decided on 2026-09-25 (EPR-DDR-002). Against the targets he accepted that day, **R5** is met on paper (334 N per operator, grip 0.86 to 1.89 m, peak at 1.16 m). Since the design was made buildable on 2026-10-01 (EPR-DDR-003, v0.3 of this note), R7 was not met (200 kg against 190 kg; no piece over 45 kg, so the 50 kg piece limit is met) until Amish set the total at 200 kg including the guard and bolts on 2026-10-02, so it was met on paper at 199.996 kg in v0.6; counted with every bush, nut, washer and weld bead in the kit 1.9.1 model and with the pin fix, it is **not met at 203.8 kg** (v0.7). **R13 is over its value-engineering target** (estimated $542 against a $500 target, USD 42 over); the cost savings worth trying are in the design decisions register (EPR-DEC-001). R2 and R4 are **at risk**; R3, R8, R10 and R14 cannot be verified at TRL 3.

The calculation corrects four TRL 2 figures and one TRL 2 mechanism. The press mass rises from about 123 kg to 187 kg, the cost from about $403 to $488 and the compaction work falls from 0.6 to 1.2 kJ to about 0.35 to 0.71 kJ (0.49 kJ base). The 22 mm lid would reach yield at 2 MPa and is now a ribbed lid. The TRL 2 concept ejected the block by pulling the lever on past the compaction point, which a toggle ending near straight cannot do; ejection now uses a separate seesaw lever and a lost-motion slot in the push rod.

**Kit 1.9.1 update (v0.7, 2026-10-25).** The STEM check (EPR-STM-001) found that this note checked the toggle pins in shear only. In bending, as pins loaded through a clevis, the 35 mm C45 base pin reached 388 MPa against 370 MPa at the nominal 81.2 kN and 826 MPa at the 173 kN design load, and the 20 mm base pin lugs reached 124 MPa in bearing against 100 MPa. Under Amish's standing instruction of 2026-10-23 the pins are now 40 mm 42CrMo4 +QT in 40 x 46 mm bushes, the lugs 28 mm, the connecting link 24 x 60 mm and the slot 205 mm (EPR-DEC-001 F1). The pins now reach 498 MPa against 750 MPa at the design load (section 6b), and the lowest safety factor in the press is 1.29. The masses now come from the detailed kit 1.9.1 model with every bush, nut, washer, circlip and weld bead: **203.8 kg, so R7 (PR-007) is not met by 3.8 kg**; the 4 g margin of v0.6 left out the bushes and nut hardware. The priced BOM is **USD 542**. Requirement numbers R1 to R14 are now PR-001 to PR-014 in EPR-PRS-001, with PR-015 (human powered, met by design: no electricity, hydraulics or engine) and PR-016 (every load-path member below yield at the 173 kN design load, sections 6 and 6b).

Every number here is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the geometry from `cad/src/model.py` and the costs from `bom/bom.csv`. All values are first-principles estimates; nothing is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design.*

| Input | Value | Basis |
| --- | --- | --- |
| Block | 290 x 140 x 90 mm; loose fill 150 mm deep | EPR-DDR-001 item 3 |
| Target pressure | 2.0 MPa at the end of the stroke | EPR-DDR-001 item 4, R2 |
| Dry block density | 1,900 kg/m³ | TRL 2 assumption |
| Stabilizer and water | 5 % cement on dry soil, 10 % water on dry mix | EPR-DDR-001 item 5 |
| Soil compaction law | Pressure rises tenfold over the last 14 mm of the stroke (exponential); range 10 to 20 mm | Assumed; to be measured with partner soil |
| Operators | 500 N for one person (R5 limit); 1,000 N for two on the T-handle, also the abuse case | Assumed |
| Working grip band | 0.8 to 1.9 m above ground, peak force at 1.0 m or higher | R5 as accepted by Amish, EPR-DDR-002 |
| Steel | Yield 250 MPa (plate and sections), 240 MPa (A53 grade B pipe), 750 MPa (42CrMo4 +QT pins, 16 < d <= 40 mm; were 370 MPa C45); E = 200 GPa | Lower-bound catalog values; 42CrMo4 from the [Swiss Steel 42CrMoS4 data sheet](https://swisssteel-group.com/content-media/documents/Data-Sheets/Engineering-Steel/42CrMoS4_en.pdf), accessed 2026-10-25 |
| Bush bearing pressure | 100 MPa allowable, hardened steel, greased, slow oscillation | Assumed |
| Lateral pressure in the mold | 0.5 x vertical during pressing; 0.1 MPa residual after unloading, friction 0.6 | Assumed |
| Soil rebound at 2 MPa | 1.0 mm | Assumed |
| Bolts | M16 8.8, 60.3 kN each in single shear through the thread | 0.6 x 800 x 157 / 1.25 |
| Fatigue | FAT 71 welded detail, 243 MPa range at 50,000 cycles | 71 x (2 x 10⁶ / 5 x 10⁴)^(1/3) |
| Cycle | 85 s per block (Table 6); 7 working hours per 8 h day | Assumed, to be timed |
| Soil preparation | 15 % oversize; sieving 400 kg/h and mixing 600 kg/h per person; 3 % rejects remixed | Assumed |
| Carbon | 49 kg CO2/m³ for 5 % CSEB, 643 kg CO2/m³ for fired brick | [Auroville Earth Institute](https://www.earth-auroville.com/compressed_stabilised_earth_block_en.php) |
| Steel price | About $1.30/kg | Indicative, TRL 2 basis |

## 2. Block and force (R1, R2)

The block face is 0.0406 m², so **2 MPa needs 81.2 kN** (4 MPa would need 162.4 kN). The block holds 3.65 L and weighs 6.94 kg dry and 7.64 kg moist at the press, with 0.33 kg of cement. A 150 mm loose fill compacts to 90 mm, a ratio of 1.67, which implies a loose dry density of about 1,140 kg/m³ in the mold.

## 3. Linkage and lever (R2, R5)

The mechanism is a bottom piston driven by a symmetric toggle (two 245 mm links), whose knee is pushed by a 420 mm connecting link from a 107 mm crank on the lever hub. The geometry in `cad/src/model.py` came from a design search that minimized the peak grip force while keeping the grip between 0.8 and 1.9 m; the script checks it.

*Table 2. Kinematics.*

| Quantity | Value |
| --- | --- |
| Toggle angle from vertical, start to stop | 29.3° to 6.0° |
| Piston stroke | 60.0 mm |
| Base pin and upper pin heights at the stop | 298 mm and 785 mm (mold rim at 940 mm) |
| Lever pivot | x = -468 mm, z = 266 mm; grip radius 1,650 mm |
| Lever angle, start to stop | 99.6° to 158.8° from horizontal (+X), an arc of **59.2°** |
| Grip path | 1.71 m |
| Grip height, start to stop | 1,893 mm to 863 mm |
| Force ratio at 30 mm and at the stop | 20.0:1 and **173:1**; it rises monotonically to the stop |

**The original R5 band could not hold a useful arc.** A grip 1.65 m from the pivot can stay between 0.9 and 1.6 m for only 24.5° of arc. The TRL 2 recommendation to raise the pivot to about 800 mm for a 100° arc does not work with a lever of this length: a symmetric 100° arc would take the grip to -464 mm, below the ground. The design therefore keeps a low pivot and starts the lever nearly upright, which gives 59° of arc with the grip between 0.86 and 1.89 m. This meets the intent of EPR-DDR-001 item 2 (a longer arc and a higher grip at the end) but not its wording, and it did not meet the original 0.9 to 1.6 m R5 band. Amish accepted the reworded R5 on 2026-09-25 (grip 0.8 to 1.9 m with the peak force at 1.0 m or higher; EPR-DDR-002), and the design meets it: the grip stays inside the band and the peak comes at 1,157 mm.

## 4. Grip force and work (R2, R5)

*Table 3. Grip force through the stroke, base soil (14 mm per decade).*

| Travel (mm) | Piston force (kN) | Force ratio | Grip force (N) | Grip height (mm) |
| --- | --- | --- | --- | --- |
| 0 | 0.00 | 14.8 | 0 | 1,893 |
| 30 | 0.59 | 20.0 | 29 | 1,735 |
| 40 | 3.04 | 25.0 | 122 | 1,621 |
| 50 | 15.7 | 37.5 | 417 | 1,429 |
| 55 | 35.7 | 56.5 | 632 | 1,257 |
| 57 | 49.8 | 74.5 | **668** | 1,150 |
| 59 | 68.7 | 115.8 | 593 | 994 |
| 60 | 81.2 | 173.0 | 469 | 863 |

- **Peak grip force: 668 N** at 56.9 mm of travel, with the grip at 1.16 m (waist to chest height). With a stiffer soil (10 mm per decade) the peak is 571 N; with a softer one (20 mm) it is 809 N.
- **One operator at 500 N stalls at 51.9 mm, at 0.53 MPa**, and no overfill helps (best 0.53 MPa). The peak comes before the stop, so the operator cannot "push through" it.
- **Two operators on the T-handle** (334 N each at the peak) reach the stop at 2.00 MPa.
- Compaction work is **494 J** for the base soil (353 J and 705 J for the range). One operator at 500 N could give 853 J over the arc, so energy is not the limit; the mismatch between the force ratio and the soil curve is. A perfect match would need 58 % of the operator's capacity.

**R2 is at risk** (met with two operators, within the fill window of section 5, for the base soil). With the accepted R5 (500 N or less per operator, EPR-DDR-002), **R5 is met on paper** with two operators at 334 N each and the peak at 1,157 mm; one operator alone cannot make a 2 MPa block. On 2026-10-02 Amish decided that the operating chart is based on the softer soil until partner soils are measured: 809 N in all, 405 N per operator, still within R5's 500 N.

## 5. Fill tolerance (R1, R2)

The crank stop sits at the design end angle (6°), so the stop limits the force the linkage can deliver (section 6) and every block that reaches the stop is 90.0 mm high. The price is a narrow fill window. If the fill mass is e above nominal, the soil reaches 2 MPa at a height of 90(1 + e) mm.

*Table 4. Pressure and block height against fill error, two operators (1,000 N).*

| Fill error | Pressure | Block height |
| --- | --- | --- |
| -2 % | 1.49 MPa | 90.0 mm |
| -1 % | 1.72 MPa | 90.0 mm |
| 0 % | 2.00 MPa | 90.0 mm |
| +2 % | 2.69 MPa | 90.0 mm |
| +4 % | 1.15 MPa (operators stall) | 97.0 mm |

The fill must be between **0 and +2.7 %** of nominal, that is, 0 to 206 g over 7.64 kg of moist mix. Filling by struck volume alone cannot hold this, since loose density varies with moisture and handling. The proposal is to weigh each fill to about +1.3 % ± 100 g on a 10 kg hanging scale with 50 g divisions (now in the soil test kit, BOM item 9). R1 (height 90 ± 3 mm) is met on paper within this window.

### 5b. Operating chart for the softer design soil

Until partner soils are measured, the operating chart is written for the softer soil (pressure rising tenfold over the last 20 mm of the stroke), which Amish decided on 2026-10-02 (EPR-DEC-001). The peak pull is 809 N in total, 405 N for each of two operators, inside R5's 500 N [`sizing.py` section 4b]. The softer soil narrows the fill window to 0 to +2.0 % (0 to +153 g) from 0 to +2.7 %, because the operators stall sooner on an overfill.

*Table 5b. Operating chart, softer design soil, two operators.*

| Fill over nominal | Pressure at the stop | Block height | Peak pull per operator | Result |
| --- | --- | --- | --- | --- |
| -2 % (-153 g) | 1.63 MPa | 90.0 mm | 329 N | Too light: under 2 MPa |
| -1 % (-76 g) | 1.80 MPa | 90.0 mm | 365 N | Too light: under 2 MPa |
| 0 % (nominal) | 2.00 MPa | 90.0 mm | 405 N | Good, at the edge |
| +1.0 % (+76 g) | 2.22 MPa | 90.0 mm | 449 N | Good: the weighing target for this soil |
| +2.0 % (+153 g) | 2.46 MPa | 90.0 mm | 498 N | Good, at the edge: the operators are at their 500 N limit |
| +2.7 % (+206 g) | 1.07 MPa | 97.9 mm | 501 N | Operators stall: too heavy |
| +4 % (+305 g) | 0.90 MPa | 100.5 mm | 502 N | Operators stall: too heavy |

The weighing target for the softer soil is therefore +1.0 % (+76 g over nominal) with a tolerance of 75 g either way, against +1.3 % for the base soil. Each soil measured at a partner site gets its own row set, recomputed with `sizing.py`.

**Scoop rule.** A calibrated scoop may replace weighing only for a soil whose scoop-to-mass scatter has been measured inside the fill window (decided on 2026-10-02). Half the window is 103 g for the base soil (0.45 % of the moist fill, 34 g, is the largest standard deviation allowed, so that three standard deviations fit in the half window). The test: weigh 20 scoops of the prepared mix; accept the scoop only if the standard deviation is 34 g or less and the mean is on the weighing target. A new soil, a new moisture or a new scoop needs the test again.

## 6. Design load and structure (R8, R12)

**Design load.** The largest force the linkage can deliver is the operators' pull times the force ratio at the stop: 1,000 N x 173 = **173 kN** (4.26 MPa on the block). All members are checked at this abuse load and at the nominal 81.2 kN. It exceeds the R12 latch requirement of 1.5 x 81.2 = 121.8 kN.

*Table 5. Structural checks (safety factor on yield or capacity).*

| Member | Nominal 81.2 kN | Abuse 173 kN |
| --- | --- | --- |
| Toggle pins, 40 mm 42CrMo4 +QT, double shear | 32 MPa (13.3) | 69 MPa (6.25) |
| Bush bearing, 2 x 28 mm links on 40 mm | 36 MPa (2.74) | 78 MPa (1.29) |
| Link net section at the 46 mm bush hole, 28 x 70 mm | 61 MPa (4.12) | 129 MPa (1.93) |
| Link buckling out of plane | SF 103 | SF 48 |
| Push rod net section at the 42 mm slot, 60 mm square | 75 MPa (3.33) | 160 MPa (1.56) |
| Lid, 20 mm plate with two 20 x 70 mm ribs, 420 mm between hinge and latch pins | 73 MPa (3.43) | 155 MPa (1.61) |
| Lid deflection at mid-span | 0.08 mm | 0.17 mm |
| Hinge and latch pins, 30 mm 42CrMo4 +QT, double shear | 29 MPa (15.1) | 61 MPa (7.07) |
| Mold long wall with the 16 x 50 mm belt | 89 MPa (2.80) | 190 MPa (1.31) |
| Columns, UPN 80 in tension | 37 MPa (6.77) | 79 MPa (3.18) |
| Columns at the 46 mm pin access hole | 49 MPa (5.07) | 105 MPa (2.38) |
| Mold to column bolts, 8 x M16 8.8 | SF 5.9 | SF 2.8 |
| Base beam, two 20 x 100 mm plates | 73 MPa (3.41) | 156 MPa (1.60) |
| Connecting link, 60 x 24 mm, 42.2 kN at the abuse case | | buckling SF 18.3 |
| Lever, 2 in schedule 40 at the socket mouth | 102 MPa at the 668 N peak (2.35) | 153 MPa at 1,000 N (1.57) |

The lowest factor is 1.29 (bush and lug bearing at the abuse load; it was 1.13 with the 35 mm pins). The connecting link acts 39.1 mm from the lever pivot at the stop and carries 42.2 kN at the abuse case; the two tie tubes from the lever bracket to the base beam carry a horizontal 34.1 kN. The mold wall bulges 0.08 mm at 2 MPa and the columns stretch 0.16 mm, so neither affects block size.

**The TRL 2 lid does not work.** A plain 22 mm plate, 220 mm wide, spanning the 420 mm between hinge and latch pins reaches 315 MPa at the nominal 81 kN, above yield. The ribbed lid in the model is the fix; it weighs 27 kg with its pins, which the operator lifts at the latch end every cycle (about 133 N).

### 6b. Pin bending and lug bearing (PR-016; EPR-STM-001 S9 and S10)

A toggle pin is loaded like a clevis pin: on each side the outer member pushes one way and the inner member the other, so the pin carries a bending moment of the link force per side times the distance between the centres of the two bearing faces. Versions 0.1 to 0.6 checked shear only.

*Table 5b. Pin bending and lug bearing, 40 mm 42CrMo4 +QT pins (yield 750 MPa) and 28 mm lugs.*

| Check | Nominal 81.2 kN | Abuse 173 kN |
| --- | --- | --- |
| Base pin, arm 36 mm (link to lug) | 234 MPa (3.21) | 498 MPa (1.51) |
| Knee pin, arm 32 mm, with the connecting link force | 217 MPa (3.45) | 463 MPa (1.62) |
| Upper pin, arm 31 mm (link to rod) | 201 MPa (3.72) | 429 MPa (1.75) |
| Base pin lugs, 2 x 28 mm bearing on 40 mm | 36 MPa (2.74) | 78 MPa (1.29) |
| Hinge and latch pins, 30 mm, arm 22 mm | 168 MPa (4.45) | 359 MPa (2.09) |
| **v0.6 base pin, 35 mm C45, arm 40 mm** | **388 MPa against 370 (0.95)** | **826 MPa (0.45)** |
| **v0.6 lugs, 2 x 20 mm on 35 mm** | | **124 MPa against 100** |
| v0.6 hinge and latch pins, 30 mm C45 | | 359 MPa (1.03) |

The 35 mm C45 base pin would have yielded at the nominal load, so the design did not meet PR-016. The fix (EPR-DEC-001 F1, decided on 2026-10-25 under Amish's standing instruction of 2026-10-23) keeps the working principle and the linkage geometry: 40 mm 42CrMo4 +QT pins in 40 x 46 mm case-hardened bushes, the base pin lugs 28 mm thick (grown toward the links, so the base spacers shrink from 16 to 8 mm and the bending arm from 40 to 36 mm), the connecting link widened from 50 to 60 mm round its 40.5 mm knee hole, the column access holes 46 mm, the push rod slot 42 x 205 mm, and the hinge and latch pins also in 42CrMo4 +QT. It adds about 1.2 kg and about USD 19 (estimate).

**Fatigue (R8).** The highest nominal stress range per block in a welded member is 89 MPa (mold wall), below the 243 MPa allowed for a FAT 71 welded detail at 50,000 cycles. The turned pins are not welded; their highest bending range is 234 MPa against about 350 MPa (half of an endurance limit taken as 0.5 Rm with a 0.7 surface and size factor, Rm 1,000 MPa; first-order). Wear of bushes and mold faces cannot be estimated without soil data, so **R8 is not verifiable at TRL 3**.

**Safety features (R12).** If the lever is released at the end of the stroke, the soil rebound and column stretch return about **47 J** to it (roughly a 5 kg mass dropped 1 m), so it kicks back upward. The end pawl and the rest catch, spring pawls on the lever bracket, hold the crank pin at the end and at the start of the stroke; the end pawl takes the kickback end on. The T-handle stays 846 mm above the ground at the stop, and the grip is more than 1.5 m from the frame. The crank, connecting link and knee form a scissor point, covered by the linkage guard (BOM item 13). **R12 is met on paper.**

## 7. Ejection (R2, R5)

After pressing, the lever is returned to its rest stop, which lets the toggle fold under the weight of the piston while the block stays in the mold. The lid is opened and the lever is moved to the eject socket, a seesaw pivoted at x = 160 mm, z = 607.5 mm on the +X side. Its central arm, with a round nose 160 mm from the pivot, lifts the push rod by its foot, while the 200 mm slot in the rod lets it rise past the toggle pin.

Breaking the block free takes 4.64 kN of wall friction, 4.84 kN with the piston and block weight. The eject lever ratio is 10.3:1 or better (the nose is 139 to 160 mm from the pivot, measured across), so the **grip force is 470 N** or less, within R5 for one operator, over a 60° arc for the 160 mm lift (60 mm up to the block, 90 mm out, 10 mm clear). The 20 x 40 mm arm reaches 145 MPa in bending at the hub (SF 1.72).

## 8. Mass (R7)

*Table 6. Piece masses from the detailed kit 1.9.1 model (every part at its material's density; bushes, seals, fasteners and weld beads included; the guard's expanded metal at 35 % of solid sheet).*

| Piece | Mass |
| --- | --- |
| Base frame with lever bracket, ties and eject posts | 44.5 kg |
| Press core, columns and base beam | 28.9 kg |
| Mold box with hinge and latch lugs | 30.6 kg |
| Lid with ribs, hinge and latch pins | 27.5 kg |
| Piston and slotted push rod | 12.1 kg |
| Toggle links, pins, bushes, spacers and seals | 26.8 kg |
| Lever hub, crank, shaft and crank pin | 8.2 kg |
| Lever pipe and T-handle | 10.5 kg |
| Eject seesaw, pivot pin, end pawl and rest catch | 7.0 kg |
| Linkage guard | 5.4 kg |
| Bolts, nuts and washers | 2.2 kg |
| **Total** | **203.8 kg** |

**R7 (PR-007) is met on paper:** 203.8 kg against the 205 kg total Amish set on 2026-10-30 (decision D2 option (a), EPR-DDR-005), a margin of 1.2 kg. The 200 kg of 2026-10-02 (EPR-DDR-003, A1) was exceeded by 3.8 kg once the v0.6 figure (199.996 kg) counted only the steel parts and the seals, not the ten bushes (0.9 kg), the nuts and washers, or the weld metal (1.2 kg); the pin fix of 2026-10-25 adds about 1.2 kg. The heaviest piece is 44.5 kg, so the 50 kg piece limit is met, and the press is 1,280 x 580 mm in plan, so it fits a 1.5 m pickup bed with the lever removed. The margin is thin: the weighed prototype decides. Lightening by about 10 kg stays a value-engineering item (EPR-DEC-001). `sizing.py`, section 7.

## 9. Output and crew (R4)

*Table 7. Cycle time (assumed).*

| Step | Time |
| --- | --- |
| Weigh and fill | 25 s |
| Strike, close and latch | 8 s |
| Press, two on the lever | 10 s |
| Return lever, unlatch, open lid | 7 s |
| Move lever to the eject socket | 6 s |
| Eject | 6 s |
| Lift off, gauge, carry to the stack | 15 s |
| Return lever, brush the mold | 8 s |
| **Total** | **85 s** |

In 7 working hours the press makes **296 blocks per day**, 1 % short of the 300 in R4, so **R4 is at risk**. Two people at the press share the lever and block handling; two others dig, sieve and mix 2,375 kg of soil a day, which takes 9.8 of their 16 person-hours.

## 10. Material flow, house and carbon (R10, R11)

Per 100 blocks the crew digs 778 kg of soil, sieves out 117 kg of oversize, adds 33 kg of cement and 69 kg of water, and mixes 787 kg including 23 kg of remixed spill and rejects. The press turns out 764 kg of moist blocks, which cure to 712 kg after losing 51 kg of water (Figure 3 in EPR-PRC-001).

A small house with a 22 m perimeter, 2.7 m walls and 15 % openings has 50.5 m² of wall. At 33.3 blocks per m² with 10 mm joints it needs **1,683 blocks**, about 5.7 press days (8.9 m² of wall a day), and 556 kg of cement (11.1 bags of 50 kg). Its 7.07 m³ of walling embodies about **0.35 t CO2 as CSEB against 4.55 t as fired brick**, 7.6 % of the brick figure (**R11 met on paper**; mortar and transport excluded; counting the 556 kg of cement at about 0.9 kg CO2 per kg, an assumed factor, gives about 0.5 t or 11 %, still inside the 25 % limit). R10 (strength with 8 % cement or less) is set by design at 5 % but cannot be verified without block tests.

## 11. Cost (R13)

Value-engineering target: USD 500. Estimated cost of the constructable design: **USD 542** (USD 42 over the target) on indicative prices. The rise from USD 523 is the pin fix (USD 14 on line 5 and USD 2 on line 3: 42CrMo4 +QT pins and 40 x 46 bushes, estimates of 2026-10-25), about USD 1 of steel for the thicker lugs and about USD 2 for the corrected bolt lengths (line 11). `budget_usd` in `project.yaml` (a hypothetical control target) is unchanged, so **R13 is over the target by USD 42**. The steel in the press (about 204 kg at about USD 1.30/kg) is about USD 265. The savings worth trying are in the Value engineering section of EPR-DEC-001.

## 12. Results against requirements

*Table 8. Every requirement in EPR-REQ-001 against this note.*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R1 | Block dimensions | Cavity 290 x 140 mm; height 90.0 mm at the stop; wall bulge 0.08 mm | ± 2 mm plan, 90 ± 3 mm height | Met on paper, within the fill window |
| R2 | Compaction pressure | 2.00 MPa with two operators and fill 0 to +2.7 %; 0.53 MPa with one at 500 N | 2.0 MPa or more | At risk |
| R3 | Block strength | Depends on soil, mix and curing | 4 MPa dry, 2 MPa wet; 2.1 MPa minimum | Not verifiable at TRL 3 |
| R4 | Output | 296 blocks per day, crew of four | 300 or more | At risk |
| R5 | Operator force and grip height | Peak 668 N total (334 N each for two) at 1.16 m; 809 N (405 N each) for the softer design soil of the operating chart; grip 0.86 to 1.89 m; eject 470 N | 500 N or less per operator; grip 0.8 to 1.9 m; peak at 1.0 m or higher | Met on paper (two operators) |
| R6 | Garage-buildable | Plate, sections, pipe and tube; turned pins, shafts and bushes bought | Stick welder, grinder, drill press | Met (design review) |
| R7 | Movable | 203.8 kg total with bushes, fasteners and weld metal; heaviest piece 44.5 kg; plan 1.28 x 0.58 m | 205 kg total including guard, bolts, bushes and weld metal (200 kg from 2026-10-02, 190 kg before); 50 kg per piece; 1.5 m bed | **Met on paper**, margin 1.2 kg (piece limit met) |
| R8 | Durability | Welded range 89 MPa against 243 MPa; pin range 234 MPa against about 350 MPa; bushes, grease nipples | 50,000 blocks; replaceable bushes | Not verifiable at TRL 3 (wear) |
| R9 | Soil test kit | Field tests, chart and a 10 kg scale for fill weighing | Go or no-go in 1 h, full result in 24 h | Met (design review); accuracy not verifiable at TRL 3 |
| R10 | Low stabilizer use | 5 % cement, 0.33 kg per block | 8 % or less reaching R3 | Not verifiable at TRL 3 |
| R11 | Embodied carbon | 7.6 % of fired brick | 25 % or less | Met on paper |
| R12 | Safe operation | Rest catch and end pawl on the crank pin; latch and lid rated 173 kN; guard over the linkage; grip over 1.5 m from the frame | No free fall; latch 1.5 x (121.8 kN); guards or 100 mm | Met on paper |
| PR-016 | Structure at the design load | Lowest safety factor 1.29 at 173 kN; pins 498 MPa against 750 MPa (section 6b) | Every load-path member below yield at 173 kN | Met on paper after EPR-DEC-001 F1 (the 35 mm C45 pins did not meet it) |
| R13 | Affordable | $542 | At or below the $500 value-engineering target | **Over the value-engineering target by USD 42** |
| R14 | Open and documented | Model, drawing, BOM and this note | Build by an outside welder without the author | Not verifiable at TRL 3 |
| PR-015 | Human powered | Lever, toggle and eject seesaw only | No electricity, hydraulics or engine | Met by design |

> **Safety:** The press delivers 81 kN at 2 MPa and up to 173 kN if two people pull hard at the stop. Keep hands out of the mold, the linkage and the eject arm while anyone is on the lever. The lever kicks back with about 47 J if released at the end of the stroke; engage the end pawl before letting go. Never open the lid until the lever is back on its rest stop.
