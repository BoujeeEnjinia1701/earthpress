---
doc_id: EPR-REQ-001
title: EarthPress requirements
project: EarthPress
doc_type: Requirements
version: "0.2"
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
---

# EarthPress requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be checked by calculation at TRL 3 and revised after co-design sessions (see EPR-PRB-001). The status column gives the concept estimate from EPR-PRC-001; every value there is an estimate.

The **reference block** is 290 x 140 x 90 mm (proposed, awaiting Amish), about 3.65 L, from a sandy clay loam stabilized with 5 % cement by dry mass.

| ID | Requirement | Target | Verification (TRL 3 or later) | Concept status |
| --- | --- | --- | --- | --- |
| R1 | Block dimensions | 290 x 140 mm ± 2 mm on plan; height 90 mm ± 3 mm, checked with the block gauge | Mold tolerance analysis; later gauge checks on a production run | Met by design, unverified |
| R2 | Compaction pressure | 2.0 MPa or more on the block face at the end of the stroke | Linkage force calculation | At risk: about 81 kN needed. Force ratio is reachable (lever about 19:1 times toggle about 9:1 within about 3° of straight), but the compaction work, about 0.6 to 1.2 kJ, exceeds the about 0.65 kJ one operator delivers over the modeled 50° lever arc |
| R3 | Block strength with suitable soil | 28-day dry compressive strength 4 MPa or more and wet strength 2 MPa or more (Auroville class B); in all cases 2.1 MPa (300 psi) or more, as in 14.7.4 NMAC | Literature review at TRL 3; block tests at TRL 4 | **Not verifiable at TRL 2.** Depends on soil, mix and curing as much as on the press |
| R4 | Output | 300 or more blocks in an 8 h day with a crew of four, including mixing | Cycle time estimate; later timed trials | Met on paper (about 96 s per block allowed), unverified |
| R5 | Operator force | Peak pull of 500 N or less at the lever grip; grip between 0.9 and 1.6 m above ground through the stroke | Force calculation; ergonomic check of the lever arc | At risk: in the modeled layout the grip starts about 1.36 m high and ends about 0.3 m above ground, below the 0.9 m target |
| R6 | Garage-buildable | Built with a stick welder, angle grinder, drill press and hand tools; no turned or milled parts except purchased pins and bushings | Design review of every part | Met by design |
| R7 | Movable | Complete press 140 kg or less; no single piece over 50 kg after removing pins and bolts; fits a 1.5 m pickup bed | Mass estimate from the model | **Not met:** press about 123 kg, but the frame alone is about 61 kg |
| R8 | Durability | 50,000 blocks before mold liners or bushings need replacing; all pins in replaceable bushings; grease points on every pivot | Wear estimate; later endurance log | Not assessed at TRL 2 |
| R9 | Soil test kit | Field tests (jar sedimentation, shrinkage box, ribbon and drop tests) give a go or no-go and a starting cement content, with a first screen within 1 h and a full result within 24 h | Written procedure; later comparison with lab grading on partner soils | Met by design, unverified |
| R10 | Low stabilizer use | Blocks reach R3 with 8 % cement by dry mass or less; 5 % as the design target | Literature at TRL 3; block tests at TRL 4 | Plausible from Auroville practice, unverified |
| R11 | Embodied carbon | Cradle-to-gate CO2 of the walling material 25 % or less of a fired-brick wall of equal volume | Carbon estimate from published factors | Met on paper: about 8 % using Auroville figures |
| R12 | Safe operation | Lever cannot fall freely when released under load; lid latch holds against at least 1.5 times the peak block force; pinch points between lever and frame guarded or with 100 mm or more clearance | Design review; later proof-load test | Addressed in concept; not yet dimensioned |
| R13 | Affordable | Press and test kit $450 or less in parts, excluding labor and cement | Priced BOM (`bom/bom.csv`) | Met: about $403 (indicative) |
| R14 | Open and documented | CERN-OHL-S drawings, BOM and build notes sufficient for a welder to build without contacting the author | Review by an outside fabricator at TRL 3 | Not yet assessed |

## Requirements not met or at risk

- **R7 not met:** the frame with its 20 mm base plate is about 61 kg against the 50 kg single-piece limit. Options are a thinner base plate or a bolted two-part frame.
- **R2 at risk:** the force ratio can reach 2 MPa, but the work needed may exceed what one person delivers over a 50° lever arc. Raising the lever pivot to allow about a 100° arc, or two people on the lever, would cover it. Reaching 2 MPa also depends on the toggle ending within about 3° of straight, which makes the final pressure sensitive to fill mass.
- **R5 at risk:** the lever grip ends about 0.3 m above ground, which forces a deep stoop at the end of the stroke, where force is highest. The same raised pivot would help.
- **R3, R8 and R10 cannot be shown at TRL 2.**

## Assumptions

- Compaction pressure of 2 to 4 MPa and about 5 % cement follow Auroville Earth Institute practice ([Auroville Earth Institute](https://www.earth-auroville.com/compressed_stabilised_earth_block_en.php)).
- Dry block density about 1,900 kg/m³ (estimate), giving about 6.9 kg per dry block.
- One operator can pull 500 N at the grip for short strokes, using body weight; this is an assumption to be checked with users.
- A crew of four covers soil sieving, mixing, pressing and stacking.
