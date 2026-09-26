---
doc_id: EPR-REQ-001
title: EarthPress requirements
project: EarthPress
doc_type: Requirements
version: "0.4"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept estimates
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Status of every requirement from EPR-CAL-001; reference block and 2 MPa target adopted for TRL 3 (EPR-DDR-001); proposed revisions to R5, R7 and R13 listed, awaiting Amish
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: "Recommendations accepted by Amish (DDR-002): R5 reworded, R7 total relaxed to 190 kg, R13 at $500; status from EPR-CAL-001 v0.2"
---

# EarthPress requirements

These requirements are checked by calculation in EPR-CAL-001 (TRL 3). On 2026-09-25 Amish accepted the TRL 3 recommendations (EPR-DDR-002), so R5, R7 and R13 carry the revised targets; the earlier targets are listed under "Revisions accepted" below. Targets still need validation with users in co-design sessions (see EPR-PRB-001).

The **reference block** is 290 x 140 x 90 mm, about 3.65 L and 6.94 kg dry, from a sandy clay loam stabilized with 5 % cement by dry mass (block size, 2 MPa target and stabilizer decided by Amish, 2026-09-25: go with recommendation; EPR-DDR-001 items 3 to 5, EPR-DDR-002).

*Table 1. Requirements and status at TRL 3 (EPR-CAL-001 v0.2).*

| ID | Requirement | Target | Verification (TRL 3 or later) | Status (EPR-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Block dimensions | 290 x 140 mm ± 2 mm on plan; height 90 mm ± 3 mm, checked with the block gauge | Mold tolerance analysis; later gauge checks on a production run | Met on paper: 90.0 mm at the crank stop when the fill is within 0 to +2.7 %; mold bulge 0.08 mm |
| R2 | Compaction pressure | 2.0 MPa or more on the block face at the end of the stroke | Linkage force calculation | **At risk:** 81.2 kN reached with two operators (peak 668 N at the grip) and a weighed fill; one operator at 500 N stalls at 0.53 MPa |
| R3 | Block strength with suitable soil | 28-day dry compressive strength 4 MPa or more and wet strength 2 MPa or more (Auroville class B); in all cases 2.1 MPa (300 psi) or more, as in 14.7.4 NMAC | Literature review at TRL 3; block tests at TRL 4 | Not verifiable at TRL 3 |
| R4 | Output | 300 or more blocks in an 8 h day with a crew of four, including mixing | Cycle time estimate; later timed trials | **At risk:** 296 blocks a day at an assumed 85 s cycle |
| R5 | Operator force | Peak pull of 500 N or less per operator at the lever grip; grip between 0.8 and 1.9 m above ground through the stroke, with the peak force at 1.0 m or higher | Force calculation; ergonomic check of the lever arc | Met on paper with two operators: 334 N each (668 N total) at 1.16 m; grip 0.86 to 1.89 m. Eject 468 N for one |
| R6 | Garage-buildable | Built with a stick welder, angle grinder, drill press and hand tools; no turned or milled parts except purchased pins and bushings | Design review of every part | Met (design review): turned pins, shafts and bushes are bought |
| R7 | Movable | Complete press 190 kg or less; no single piece over 50 kg after removing pins and bolts; fits a 1.5 m pickup bed | Mass estimate from the model | Met on paper: 187 kg in total (3 kg margin); heaviest piece 36.6 kg; plan 1.28 x 0.58 m |
| R8 | Durability | 50,000 blocks before mold liners or bushings need replacing; all pins in replaceable bushings; grease points on every pivot | Wear estimate; later endurance log | Not verifiable at TRL 3: fatigue range 89 MPa against 243 MPa allowed; wear needs soil data |
| R9 | Soil test kit | Field tests (jar sedimentation, shrinkage box, ribbon and drop tests) give a go or no-go and a starting cement content, with a first screen within 1 h and a full result within 24 h | Written procedure; later comparison with lab grading on partner soils | Met (design review); accuracy not verifiable at TRL 3 |
| R10 | Low stabilizer use | Blocks reach R3 with 8 % cement by dry mass or less; 5 % as the design target | Literature at TRL 3; block tests at TRL 4 | Not verifiable at TRL 3 (design at 5 %, 0.33 kg per block) |
| R11 | Embodied carbon | Cradle-to-gate CO2 of the walling material 25 % or less of a fired-brick wall of equal volume | Carbon estimate from published factors | Met on paper: 7.6 % (0.35 t against 4.55 t for a small house) |
| R12 | Safe operation | Lever cannot fall freely when released under load; lid latch holds against at least 1.5 times the peak block force; pinch points between lever and frame guarded or with 100 mm or more clearance | Design review; later proof-load test | Met on paper: rest catch and end pawl; lid and latch checked at 173 kN (1.5 times is 121.8 kN); linkage guard |
| R13 | Affordable | Press and test kit $500 or less in parts, excluding labor and cement | Priced BOM (`bom/bom.csv`) | Met on paper: $488 (indicative, $12 margin) |
| R14 | Open and documented | CERN-OHL-S drawings, BOM and build notes sufficient for a welder to build without contacting the author | Review by an outside fabricator at TRL 3 | Not verifiable at TRL 3: no outside review yet |

## Requirements not met or at risk

No requirement is not met on paper against the targets accepted on 2026-09-25. R7 and R13 are met with small margins (3 kg and $12), so any growth in mass or price reopens them.

- **R2 at risk:** met only with two operators, a weighed fill (0 to +2.7 %) and the assumed soil stiffness; a softer soil (20 mm per decade) raises the peak to 809 N.
- **R4 at risk:** 296 against 300 blocks a day on an assumed cycle. Decided by Amish, 2026-09-25 (EPR-DDR-002): accept the 1 % shortfall and revisit when cycles are timed, which is TRL 4 work and on hold.
- **R3, R8, R10 and R14 cannot be verified at TRL 3.**

## Revisions accepted (EPR-DDR-002)

Decided by Amish, 2026-09-25: go with recommendation. Applied in Table 1.

- R5: was a peak pull of 500 N or less with the grip between 0.9 and 1.6 m (not met: 668 N, and the band allows only 24.5° of arc). Now 500 N or less per operator, grip between 0.8 and 1.9 m, with the peak force at 1.0 m or higher.
- R7: was 140 kg or less in total (not met: 187 kg). Now 190 kg or less; the 50 kg piece limit and pickup bed are unchanged.
- R13: was $450 or less (not met: $488). Now $500 or less, matching `budget_usd` in `project.yaml`.

## Assumptions

- Compaction pressure of 2 to 4 MPa and about 5 % cement follow Auroville Earth Institute practice ([Auroville Earth Institute](https://www.earth-auroville.com/compressed_stabilised_earth_block_en.php)).
- Dry block density about 1,900 kg/m³ (estimate), giving about 6.9 kg per dry block.
- One operator can pull 500 N at the grip for short strokes, using body weight; two can pull 1,000 N on the T-handle. To be checked with users.
- Soil pressure rises tenfold over the last 14 mm of the stroke (range 10 to 20 mm); to be measured with partner soils.
- A crew of four covers soil sieving, mixing, pressing and stacking.
