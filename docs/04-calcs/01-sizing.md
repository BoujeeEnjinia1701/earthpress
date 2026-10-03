---
doc_id: EPR-CAL-001
title: EarthPress sizing calculations
project: EarthPress
doc_type: Calculation note
version: "0.6"
status: Draft
date: '2026-10-02'
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
---

# EarthPress sizing calculations

On paper the press reaches 2 MPa on the 290 x 140 x 90 mm block, but only with **two people on the lever** and a **weighed fill**. The toggle and 1.7 m lever give a force ratio of 173:1 at the stop, and the peak pull under the base soil assumption is **668 N**, which comes about 3 mm before the end of the stroke. One operator pulling 500 N stalls at about 0.5 MPa, so the press is a two-person machine, as Amish decided on 2026-09-25 (EPR-DDR-002). Against the targets he accepted that day, **R5** is met on paper (334 N per operator, grip 0.86 to 1.89 m, peak at 1.16 m). Since the design was made buildable on 2026-10-01 (EPR-DDR-003, v0.3 of this note), R7 was not met (200 kg against 190 kg; no piece over 45 kg, so the 50 kg piece limit is met) until Amish set the total at 200 kg including the guard and bolts on 2026-10-02, so it is now met on paper (199.996 kg, a 4 g margin), and **R13 is over its value-engineering target** (estimated $523 against a $500 target, USD 23 over, after the dust seals decided on 2026-10-02 added $3); the cost savings worth trying are in the design decisions register (EPR-DEC-001). R2 and R4 are **at risk**; R3, R8, R10 and R14 cannot be verified at TRL 3.

The calculation corrects four TRL 2 figures and one TRL 2 mechanism. The press mass rises from about 123 kg to 187 kg, the cost from about $403 to $488 and the compaction work falls from 0.6 to 1.2 kJ to about 0.35 to 0.71 kJ (0.49 kJ base). The 22 mm lid would reach yield at 2 MPa and is now a ribbed lid. The TRL 2 concept ejected the block by pulling the lever on past the compaction point, which a toggle ending near straight cannot do; ejection now uses a separate seesaw lever and a lost-motion slot in the push rod.

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
| Steel | Yield 250 MPa (plate and sections), 240 MPa (A53 grade B pipe), 370 MPa (C45 pins); E = 200 GPa | Lower-bound catalog values |
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
| Toggle pins, 35 mm C45, double shear | 42 MPa (5.03) | 90 MPa (2.36) |
| Bush bearing, 2 x 28 mm links | 42 MPa (2.40) | 89 MPa (1.13) |
| Link net section at the 41 mm bush hole, 28 x 70 mm | 50 MPa (4.97) | 107 MPa (2.33) |
| Link buckling out of plane | SF 103 | SF 48 |
| Push rod net section at the slot, 60 mm square | 59 MPa (4.25) | 125 MPa (1.99) |
| Lid, 20 mm plate with two 20 x 70 mm ribs, 420 mm between hinge and latch pins | 73 MPa (3.43) | 155 MPa (1.61) |
| Lid deflection at mid-span | 0.08 mm | 0.17 mm |
| Hinge and latch pins, 30 mm, double shear | 29 MPa (7.43) | 61 MPa (3.49) |
| Mold long wall with the 16 x 50 mm belt | 89 MPa (2.80) | 190 MPa (1.31) |
| Columns, UPN 80 in tension | 37 MPa (6.77) | 79 MPa (3.18) |
| Columns at the 40 mm pin access hole | 47 MPa (5.30) | 101 MPa (2.49) |
| Mold to column bolts, 8 x M16 8.8 | SF 5.9 | SF 2.8 |
| Base beam, two 20 x 100 mm plates | 73 MPa (3.41) | 156 MPa (1.60) |
| Connecting link, 50 x 24 mm, 42.2 kN at the abuse case | | buckling SF 15.3 |
| Lever, 2 in schedule 40 at the socket mouth | 102 MPa at the 668 N peak (2.35) | 153 MPa at 1,000 N (1.57) |

The lowest factor is 1.13 (bush bearing at the abuse load). The connecting link acts 39.1 mm from the lever pivot at the stop and carries 42.2 kN at the abuse case; the two tie tubes from the lever bracket to the base beam carry a horizontal 34.1 kN. The mold wall bulges 0.08 mm at 2 MPa and the columns stretch 0.16 mm, so neither affects block size.

**The TRL 2 lid does not work.** A plain 22 mm plate, 220 mm wide, spanning the 420 mm between hinge and latch pins reaches 315 MPa at the nominal 81 kN, above yield. The ribbed lid in the model is the fix; it weighs 27 kg with its pins, which the operator lifts at the latch end every cycle (about 133 N).

**Fatigue (R8).** The highest nominal stress range per block is 89 MPa (mold wall), below the 243 MPa allowed for a FAT 71 welded detail at 50,000 cycles. Wear of bushes and mold faces cannot be estimated without soil data, so **R8 is not verifiable at TRL 3**.

**Safety features (R12).** If the lever is released at the end of the stroke, the soil rebound and column stretch return about **47 J** to it (roughly a 5 kg mass dropped 1 m), so it kicks back upward. The end pawl and the rest catch, spring pawls on the lever bracket, hold the crank pin at the end and at the start of the stroke; the end pawl takes the kickback end on. The T-handle stays 846 mm above the ground at the stop, and the grip is more than 1.5 m from the frame. The crank, connecting link and knee form a scissor point, covered by the linkage guard (BOM item 13). **R12 is met on paper.**

## 7. Ejection (R2, R5)

After pressing, the lever is returned to its rest stop, which lets the toggle fold under the weight of the piston while the block stays in the mold. The lid is opened and the lever is moved to the eject socket, a seesaw pivoted at x = 160 mm, z = 607.5 mm on the +X side. Its central arm, with a round nose 160 mm from the pivot, lifts the push rod by its foot, while the 200 mm slot in the rod lets it rise past the toggle pin.

Breaking the block free takes 4.64 kN of wall friction, 4.84 kN with the piston and block weight. The eject lever ratio is 10.3:1 or better (the nose is 139 to 160 mm from the pivot, measured across), so the **grip force is 470 N** or less, within R5 for one operator, over a 60° arc for the 160 mm lift (60 mm up to the block, 90 mm out, 10 mm clear). The 20 x 40 mm arm reaches 145 MPa in bending at the hub (SF 1.72).

## 8. Mass (R7)

*Table 6. Piece masses from the model at 7,850 kg/m³.*

| Piece | Mass |
| --- | --- |
| Base frame with lever bracket, ties and eject posts | 45.0 kg |
| Press core, columns and base beam | 28.2 kg |
| Mold box with hinge and latch lugs | 30.4 kg |
| Lid with ribs, hinge and latch pins | 27.0 kg |
| Piston and slotted push rod | 12.6 kg |
| Toggle links, pins and spacers | 24.6 kg |
| Lever hub, crank, shaft and crank pin | 8.2 kg |
| Lever pipe and T-handle (pipe alone 9.2 kg) | 10.4 kg |
| Eject seesaw, pivot pin, end pawl and rest catch | 7.0 kg |
| Linkage guard (expanded metal at 35 % of solid sheet) | 5.5 kg |
| Bolts | 1.2 kg |
| **Total** | **200.0 kg** |

**R7 was not met on paper** against the earlier 190 kg: the total is 200.0 kg against the 190 kg accepted by Amish on 2026-09-25 (EPR-DDR-002), 10 kg over. Of the 13 kg added since v0.2, 6.7 kg is the guard and bolts, which v0.2 did not count, and the rest is the round link ends, lugs, larger base plate and other parts added to make the press buildable (EPR-DDR-003). The heaviest piece is 45.0 kg, so the 50 kg piece limit is met. The press is 1,280 x 580 mm in plan, so it fits a 1.5 m pickup bed with the lever removed. On 2026-10-02 Amish set the R7 total at 200 kg, including the guard and bolts, and kept the 50 kg piece limit (EPR-DDR-003, A1), so R7 is now met on paper: 200.0 kg of steel plus about 5 g of felt dust seals is 199.996 kg, a margin of 4 g, which is no real margin; the weighed prototype at TRL 4 decides it (`sizing.py`, section 7).

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

A small house with a 22 m perimeter, 2.7 m walls and 15 % openings has 50.5 m² of wall. At 33.3 blocks per m² with 10 mm joints it needs **1,683 blocks**, about 5.7 press days (8.9 m² of wall a day), and 556 kg of cement (11.1 bags of 50 kg). Its 7.07 m³ of walling embodies about **0.35 t CO2 as CSEB against 4.55 t as fired brick**, 7.6 % of the brick figure (**R11 met on paper**; mortar and transport excluded). R10 (strength with 8 % cement or less) is set by design at 5 % but cannot be verified without block tests.

## 11. Cost (R13)

Value-engineering target: USD 500. Estimated cost of the constructable design: USD 523 (USD 23 over the target) on indicative prices. The priced BOM totals **$523**: the $520 of 2026-10-01 plus $3 for eight felt or rubber dust seal washers at the bush faces (BOM line 5, decided on 2026-10-02; about $0.35 each from 2 mm felt or rubber sheet). `budget_usd` in `project.yaml` (a hypothetical control target) is unchanged, so **R13 is over the target by USD 23**. The steel alone (200 kg at about $1.30/kg) is about $260. The parts added to make the press buildable (EPR-DDR-003) account for the rise from $488. `budget_usd` is unchanged; the savings worth trying are in the Value engineering section of EPR-DEC-001.

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
| R7 | Movable | 200 kg total (199.996 kg with the dust seals); heaviest piece 45.0 kg; plan 1.28 x 0.58 m | 200 kg total including guard and bolts (190 kg until 2026-10-02); 50 kg per piece; 1.5 m bed | Met on paper (piece limit met) |
| R8 | Durability | Stress range 89 MPa against 243 MPa; bushes, grease nipples | 50,000 blocks; replaceable bushes | Not verifiable at TRL 3 (wear) |
| R9 | Soil test kit | Field tests, chart and a 10 kg scale for fill weighing | Go or no-go in 1 h, full result in 24 h | Met (design review); accuracy not verifiable at TRL 3 |
| R10 | Low stabilizer use | 5 % cement, 0.33 kg per block | 8 % or less reaching R3 | Not verifiable at TRL 3 |
| R11 | Embodied carbon | 7.6 % of fired brick | 25 % or less | Met on paper |
| R12 | Safe operation | Rest catch and end pawl on the crank pin; latch and lid rated 173 kN; guard over the linkage; grip over 1.5 m from the frame | No free fall; latch 1.5 x (121.8 kN); guards or 100 mm | Met on paper |
| R13 | Affordable | $523 | At or below the $500 value-engineering target | **Over the value-engineering target by USD 23** |
| R14 | Open and documented | Model, drawing, BOM and this note | Build by an outside welder without the author | Not verifiable at TRL 3 |

> **Safety:** The press delivers 81 kN at 2 MPa and up to 173 kN if two people pull hard at the stop. Keep hands out of the mold, the linkage and the eject arm while anyone is on the lever. The lever kicks back with about 47 J if released at the end of the stroke; engage the end pawl before letting go. Never open the lid until the lever is back on its rest stop.
