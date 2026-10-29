---
doc_id: EPR-PRS-001
title: EarthPress product requirements and specifications
project: EarthPress
doc_type: Product requirements and specifications
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Kit 1.8 migration of EPR-REQ-001 v0.8 (R1 to R14 become PR-001 to PR-014, old number in "Was"); PR-015 and PR-016 added; traced to EPR-URS-001; status from EPR-CAL-001 v0.7 (PR-007 not met at 203.8 kg; PR-013 USD 542; PR-016 met after fix F1)'
---

# EarthPress product requirements and specifications

What the press must do, each requirement traced to a user need in EPR-URS-001 (links in EPR-RTM-001). This document replaces EPR-REQ-001 (v0.8 of 2026-10-02): every requirement keeps its target, verification and status, with its old number in "Was". Status is from the calculation note EPR-CAL-001 v0.7 for the current design (option A, the lever and toggle press). On paper 8 of the 16 requirements are met, two are at risk, one is **not met** (PR-007, mass), one is over its value-engineering target (PR-013, cost) and four can only be verified at TRL 4. Targets remain proposals for review with a co-design partner (EPR-PRB-001). Method: STANDARDS section 22.

The **reference block** is 290 x 140 x 90 mm, about 3.65 L and 6.94 kg dry, from a sandy clay loam stabilized with 5 % cement by dry mass (decided by Amish, 2026-09-25; EPR-DDR-001 items 3 to 5, EPR-DDR-002).

Table 1. Product requirements and specifications. Status from EPR-CAL-001 v0.7 (2026-10-25).

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Performance | Block dimensions | Blocks shall be 290 x 140 mm on plan and 90 mm high, checked with the block gauge | 290 x 140; 90 | ±2 on plan; ±3 on height | mm | Analysis (CAL-001 sections 5 and 6), TRL 3; gauge checks on a production run, TRL 4 | Met on paper: 90.0 mm at the crank stop with the fill within 0 to +2.7 %; mold bulge 0.08 mm | R1 |
| PR-002 | UR-002 | Performance | Compaction pressure | The press shall reach 2.0 MPa or more on the block face at the end of the stroke | 2.0 | min | MPa | Analysis (CAL-001 sections 3 to 5), TRL 3; load cell, TRL 4 | **At risk**: 2.00 MPa with two operators and a weighed fill; one operator at 500 N stalls at 0.53 MPa; rests on the assumed soil law (STM S6) | R2 |
| PR-003 | UR-002, UR-016 | Performance | Block strength with suitable soil | Blocks from suitable soil shall reach 4 MPa dry and 2 MPa wet at 28 days (Auroville class B), and in all cases 2.1 MPa (300 psi) as in 14.7.4 NMAC | 4; 2; 2.1 | min | MPa | Literature, TRL 3; block tests, TRL 4 | To verify at TRL 4 | R3 |
| PR-004 | UR-003 | Performance | Output | A crew of four shall make 300 or more blocks in an 8 h day, including mixing | 300 | min | blocks a day | Analysis (CAL-001 section 9), TRL 3; timed trials, TRL 4 | **At risk**: 296 a day on an assumed 85 s cycle (shortfall accepted by Amish, 2026-09-25) | R4 |
| PR-005 | UR-004 | Usability | Operator force and grip height | The peak pull per operator at the grip shall be 500 N or less, with the grip between 0.8 and 1.9 m above the ground and the peak at 1.0 m or higher | 500; 0.8 to 1.9; 1.0 | max; band; min | N; m; m | Analysis (CAL-001 sections 3, 4 and 4b), TRL 3; force at the grip, TRL 4 | Met on paper with two operators: 334 N each (base soil), 405 N each (softer design soil); grip 0.86 to 1.89 m; peak at 1.16 m; eject 469 N for one | R5 |
| PR-006 | UR-005 | Physical architecture | Garage-buildable | The press shall be built with a stick welder, angle grinder, drill press and hand tools; turned parts only as bought pins, shafts and bushes | 0 | max | machined parts made in the shop | Inspection of the model, drawings and build plan (BLD-001), TRL 3 | Met by design | R6 |
| PR-007 | UR-006 | Packaging and transport | Movable | The complete press, including the guard, bolts and bushes, shall weigh 200 kg or less; no piece over 50 kg after removing pins and bolts; it shall fit a 1.5 m pickup bed | 200; 50; 1.5 | max | kg; kg; m | Analysis (CAL-001 section 8, kit 1.9.1 model), TRL 3; weighing, TRL 4 | **Not met**: 203.8 kg with every bush, nut, washer and weld bead (3.8 kg over; decision D2, proposed, awaiting Amish); heaviest piece 44.5 kg (met); plan 1.28 x 0.58 m (met) | R7 |
| PR-008 | UR-007, UR-015 | Materials | Durability | The press shall make 50,000 blocks before mold liners or bushes need replacing; all pins in replaceable bushes; a grease point on every pivot | 50,000 | min | blocks | Analysis (CAL-001 section 6, fatigue), TRL 3; endurance log, TRL 4 | To verify at TRL 4: welded range 89 MPa against 243 MPa, pin range 234 MPa against about 350 MPa; wear needs soil data | R8 |
| PR-009 | UR-008 | Usability | Soil test kit | Field tests (jar sedimentation, shrinkage box, ribbon and drop tests) shall give a go or no-go and a starting cement content, a first screen within 1 h and a full result within 24 h | 1; 24 | max | h | Inspection of the written procedure (BLD-001), TRL 3; comparison with laboratory grading, TRL 4 | Met by design; accuracy to verify at TRL 4 | R9 |
| PR-010 | UR-010 | Materials | Low stabilizer use | Blocks shall reach PR-003 with 8 % cement by dry mass or less; 5 % is the design value | 8 | max | % of dry mass | Literature, TRL 3; block tests, TRL 4 | To verify at TRL 4 (design at 5 %, 0.33 kg a block) | R10 |
| PR-011 | UR-011 | Materials | Embodied carbon | Cradle-to-gate CO2 of the walling material shall be 25 % or less of a fired-brick wall of equal volume | 25 | max | % | Analysis (CAL-001 section 10, cited factors), TRL 3 | Met on paper: 7.6 % (0.35 t against 4.55 t for a small house) | R11 |
| PR-012 | UR-012 | Safety | Safe operation | The lever shall not fall freely when released under load; the lid latch shall hold at least 1.5 times the peak block force; pinch points between lever and frame shall be guarded or have 100 mm or more clearance | 1.5; 100 | min | x 81.2 kN; mm | Analysis and design review (CAL-001 section 6), TRL 3; proof-load test, TRL 4 | Met on paper: rest catch and end pawl; lid and latch rated 173 kN; linkage guard | R12 |
| PR-013 | UR-009 | Cost | Affordable | Press and soil kit parts shall cost at or below the value-engineering target, excluding labor and cement | 500 | max | USD | Analysis of the priced BOM (`bom/bom.csv`), TRL 3 | **Over target**: USD 542 (indicative), USD 42 over; savings in EPR-DEC-001 | R13 |
| PR-014 | UR-013 | Usability | Open and documented | CERN-OHL-S drawings, BOM and build plan shall let a welder build the press without contacting the author | 1 | min | outside build review | Review by an outside fabricator, TRL 4 | To verify at TRL 4 | R14 |
| PR-015 | UR-014 | Usability | Human powered | The press shall need no electricity, fuel or hydraulic fluid to press or eject a block | 0 | max | powered parts | Inspection of the model and BOM, TRL 3 | Met by design | |
| PR-016 | UR-012, UR-007 | Safety | Structure at the design load | Every member in the load path shall stay below yield at the 173 kN design load (1,000 N at the grip at the crank stop) | 1.0 | min | safety factor on yield | Analysis (CAL-001 sections 6 and 6b), TRL 3; proof-load test, TRL 4 | Met on paper after fix F1 (EPR-DEC-001): lowest factor 1.29; the 35 mm C45 pins did not meet it | |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Requirements not met or at risk

- **PR-007 not met:** 203.8 kg against 200 kg. The earlier 199.996 kg left out the bushes, nuts, washers and weld metal, which the kit 1.9.1 model counts, and fix F1 adds about 1.2 kg. Options in EPR-DEC-001 D2 (proposed, awaiting Amish).
- **PR-013 over target:** USD 542 against the USD 500 value-engineering target (a hypothetical control target, `budget_usd` unchanged).
- **PR-002 at risk:** met only with two operators, a weighed fill and the assumed soil stiffness.
- **PR-004 at risk:** 296 against 300 blocks a day on an assumed cycle; the shortfall was accepted by Amish on 2026-09-25 (EPR-DDR-002).
- PR-003, PR-008, PR-010 and PR-014 can only be verified at TRL 4, which is on hold.

## Revisions accepted (EPR-DDR-002)

Decided by Amish, 2026-09-25: go with recommendation. R5 (now PR-005) was a peak pull of 500 N or less with the grip between 0.9 and 1.6 m; R7 (PR-007) was 140 kg, then 190 kg, and has been 200 kg including the guard and bolts since 2026-10-02 (EPR-DDR-003 A1); R13 (PR-013) was USD 450 and has been USD 500 since 2026-09-25.

## Assumptions

- Compaction pressure of 2 to 4 MPa and about 5 % cement follow Auroville Earth Institute practice ([Auroville Earth Institute](https://www.earth-auroville.com/compressed_stabilised_earth_block_en.php)).
- Dry block density about 1,900 kg/m³ (estimate), giving about 6.9 kg per dry block.
- One operator can pull 500 N at the grip for short strokes, using body weight; two can pull 1,000 N on the T-handle. To be checked with users.
- Soil pressure rises tenfold over the last 14 mm of the stroke (range 10 to 20 mm); to be measured with partner soils (EPR-STM-001 S6).
- A crew of four covers soil sieving, mixing, pressing and stacking.
