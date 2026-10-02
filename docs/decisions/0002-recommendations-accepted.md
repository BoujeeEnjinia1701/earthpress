---
doc_id: EPR-DDR-002
title: EarthPress recommendations accepted
project: EarthPress
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of every recommendation in EPR-DDR-001 and docs/REVIEW.md, what changed in the repo, and the items still open
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Item 8 decided by Amish on 2026-10-02 (EPR-DEC-001)"
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item with a recommendation is decided; item 8 (first co-design partner and region) had no recommendation and was decided by Amish on 2026-10-02 (EPR-DEC-001).

## Context

EPR-DDR-001 adopted the TRL 2 recommendations for TRL 3 work, open for Amish's review, and listed seven new TRL 3 items (10 to 16) as proposed, awaiting Amish. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Each item with a recommendation is therefore **decided by Amish, 2026-09-25: go with recommendation**. Where an item offered several options, the recommended option is the decision. Items with no recommendation stay open. The project stays at TRL 3 (`trl: 3`, `trl_target: 3`); TRL 4 work is on hold by Amish's instruction.

## Decision

*Table 1. Items decided on 2026-09-25 and what changed in the repo.*

| # | Item | Decision | What changed |
| --- | --- | --- | --- |
| 1 | Mechanism | Bottom piston, toggle and one lever (CINVA-Ram pattern); bottle-jack variant documented later | None; already in the precis and model |
| 2 | Lever layout | Longer arc and higher end grip, met in intent with a low pivot (59.2° arc, grip 1.89 to 0.86 m) | None; already in the model |
| 3 | Block | 290 x 140 x 90 mm; interlocking inserts later | None |
| 4 | Compaction target | 2 MPa | None |
| 5 | Stabilizer | 5 % cement, lime for clay-rich soils, confirmed with partner soils | None; partner soil confirmation is TRL 4 work, on hold |
| 6 | Meeting R7 | 12 mm base plate and bolted mold | None; already in the model (heaviest piece 36.6 kg) |
| 7 | Soil test kit | Field tests only | None |
| 9 | Pitch and problem | No rewording | `project.yaml` pitch and problem unchanged; the budget part is superseded by item 14 |
| 10 | Ejection | (a) Separate eject seesaw, same lever in a second socket, 200 mm lost-motion slot | None; already in the model |
| 11 | Two operators | (a) Two people on a T-handle, 334 N each | Precis and requirements now describe the press as a two-person machine |
| 12 | R5 wording | 500 N or less per operator; grip 0.8 to 1.9 m; peak force at 1.0 m or higher | EPR-REQ-001 R5 reworded (was 500 N, grip 0.9 to 1.6 m); status **not met to met on paper** (334 N per operator, peak at 1.16 m) |
| 13 | R7 total | (a) Relax total to 190 kg, keep the 50 kg piece limit | EPR-REQ-001 R7 total 140 kg to 190 kg; status **not met to met on paper** (187 kg, 3 kg margin) |
| 14 | Budget | (a) Raise `budget_usd` to $500 | `budget_usd` $450 to $500; R13 target $450 to $500; status **not met to met on paper** ($488, $12 margin) |
| 15 | Fill control | Weigh every fill on a 10 kg scale to about +1.3 % ± 100 g; target mass on the test chart | None; the scale is already in the BOM and the rule in the precis |
| 16 | Engineering proposals | (a) Pivot at x = -468, z = 266 mm, 1.7 m lever, rim at 940 mm; (b) crank stop at 6° (173 kN design load); (c) ribbed lid; (d) end pawl; (e) linkage guard; (f) case-hardened bushes; (g) R4 at 296 blocks a day, revisit when cycles are timed | None to geometry; all were already in the model. R4 stays at risk; timing cycles is TRL 4 work, on hold |

No decision changed the geometry, so `cad/src/model.py`, the STEP and STL exports and EPR-DWG-001 keep their geometry and notes; the drawing stays at Rev P1 and was regenerated only for the title block. EPR-CAL-001 moves to v0.2: the script now checks the accepted R5 band and peak height, the 190 kg R7 total and reads the budget from `project.yaml`.

### Items still open

| # | Item | Status |
| --- | --- | --- |
| 8 | First co-design partner and region (examples: an earth-building NGO in East Africa or India) | No recommendation was made on 2026-09-25. Decided by Amish, 2026-10-02: a partner that already trains builders in stabilized earth blocks and has local soils and cement supply; first candidate to approach, the Auroville Earth Institute (EPR-DEC-001) |

### On hold (TRL 4)

Decided in principle but not started, because TRL 4 is on hold: confirming the stabilizer with partner soils (item 5), timing the press cycle for R4 (item 16g), and every build, block test, proof-load test and measurement of the soil compaction curve.

## Consequences

- EPR-PRB-001, EPR-PRC-001 and EPR-REQ-001 move to v0.4; EPR-CAL-001 to v0.2; EPR-DDR-001 to v0.2.
- Requirements on paper: none not met; R2 and R4 at risk; R3, R8, R10 and R14 not verifiable at TRL 3; R1, R5, R7, R11, R12 and R13 met on paper; R6 and R9 met by design review.
- R7 and R13 are met with small margins (3 kg and $12). Any growth in mass or price reopens them.
- No cross-repo actions: EarthPress uses no shared component.
