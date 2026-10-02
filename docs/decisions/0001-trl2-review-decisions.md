---
doc_id: EPR-DDR-001
title: EarthPress TRL 2 review decisions
project: EarthPress
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, the items that remain open, and new items from EPR-CAL-001
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Item 8 decided by Amish on 2026-10-02 (EPR-DEC-001)"
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted; item 8 decided on 2026-10-02. Items 1 to 7 and 9 to 16: Decided by Amish, 2026-09-25: go with recommendation (see EPR-DDR-002). Item 8 had no recommendation on 2026-09-25; a recommendation was written later and Amish approved it on 2026-10-02 ("i approve your recommendations for all 555 open decisions."; EPR-DEC-001).

## Context

The TRL 2 review note (`docs/REVIEW.md`, session of 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", eight of them with a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the EarthPress items one by one. Under that instruction, each item that has a recommendation is adopted as recommended so that the TRL 3 work can proceed, and stays open for his review. Items without a recommendation stay open. TRL 4 is on hold by Amish's instruction. Later on 2026-09-25 Amish wrote "i accept all your recommendations, go with them across all repos", so every item with a recommendation is now decided (EPR-DDR-002).

EarthPress uses none of the shared components in this batch (FieldNode, CellGuard, MotionCore, ThermaCart, TwinKit, CalRig) or SwapCell, so there are no cross-repo interfaces to keep consistent.

## Options considered

The options for items 1 to 9 are in `docs/REVIEW.md` (TRL 2 section). Items 10 to 16 are new at TRL 3 and come from EPR-CAL-001; their options are in Table 2.

## Decision

*Table 1. TRL 2 items, decided.*

| # | Item | Status | Where it now lives |
| --- | --- | --- | --- |
| 1 | Mechanism: bottom piston with a toggle and one lever (CINVA-Ram pattern); the bottle-jack variant documented later | Decided by Amish, 2026-09-25: go with recommendation | EPR-PRC-001 v0.3, `cad/src/model.py` |
| 2 | Lever layout: raise the pivot for a longer arc and a higher grip at the end of the stroke | Decided by Amish, 2026-09-25: go with recommendation. EPR-CAL-001 section 3 shows the specific figures (800 mm pivot, 100° arc) do not work with a 1.65 m grip radius, because the grip would pass below the ground; the intent is met with a low pivot and a 59° arc from a nearly upright start (grip 1.89 to 0.86 m). The geometry change is item 16a | EPR-CAL-001 section 3, `cad/src/model.py` |
| 3 | Block: flat 290 x 140 x 90 mm (Auroville module); interlocking inserts a later option | Decided by Amish, 2026-09-25: go with recommendation | EPR-REQ-001 v0.3, EPR-PRC-001 v0.3 |
| 4 | Compaction target: 2 MPa | Decided by Amish, 2026-09-25: go with recommendation | EPR-REQ-001 R2 |
| 5 | Stabilizer: 5 % cement by dry mass, lime for clay-rich soils, confirmed with partner soils | Decided by Amish, 2026-09-25: go with recommendation | EPR-PRC-001 v0.3, EPR-REQ-001 R10 |
| 6 | Meeting R7: 12 mm base plate and a bolted mold (rather than relaxing R7) | Decided by Amish, 2026-09-25: go with recommendation. The frame is now two bolted pieces (36.6 and 27.7 kg) and no piece exceeds 37 kg, but the total is 187 kg against 140 kg (item 13) | `cad/src/model.py`, EPR-CAL-001 section 8 |
| 7 | Soil test kit: field tests only at TRL 3 | Decided by Amish, 2026-09-25: go with recommendation | EPR-PRC-001 v0.3, BOM item 9 |
| 9 | Budget and wording: no change to `budget_usd` ($450); pitch and problem unchanged | Decided by Amish, 2026-09-25: go with recommendation. `budget_usd` was then raised to $500 under item 14, which supersedes the budget part of this item | `project.yaml` (unchanged) |

No pitch or problem rewording was recommended at TRL 2, so `project.yaml` and `README.md` keep the TRL 2 wording.

### TRL 3 items

*Table 2. TRL 3 items. Item 8 remains open; items 10 to 16 are decided.*

| # | Item | Options and recommendation | Status |
| --- | --- | --- | --- |
| 8 | First co-design partner and region | Examples at TRL 2: an earth-building NGO in East Africa or India. No recommendation was made | Decided by Amish, 2026-10-02: a partner that already trains builders in stabilized earth blocks and has local soils and cement supply; first candidate to approach, the Auroville Earth Institute (EPR-DEC-001) |
| 10 | Ejection | The TRL 2 concept ejected by pulling the lever past the compaction point; a toggle ending near straight cannot lift the piston another 90 mm. Options: (a) a seesaw eject lever on the +X side, driven by the same removable lever in a second socket, with a 200 mm lost-motion slot in the push rod (in the model); (b) a bell crank that ejects on an upward lever stroke (awkward to push up at 1.9 m and above); (c) a permanently fitted second lever. Recommendation: (a) | Decided by Amish, 2026-09-25: go with recommendation; (a) is in the model |
| 11 | Two operators for R2 | Peak pull is 668 N; one operator at 500 N stalls at 0.53 MPa. Options: (a) two people on a T-handle (334 N each; in the model); (b) accept one operator pulling about 670 N with body weight; (c) lower the target pressure. Recommendation: (a) | Decided by Amish, 2026-09-25: go with recommendation |
| 12 | R5 wording | The 0.9 to 1.6 m band allows only 24.5° of arc. Recommendation: reword R5 as 500 N or less per operator, grip between 0.8 and 1.9 m, with the peak force at 1.0 m or higher (the design gives 1.16 m) | Decided by Amish, 2026-09-25: go with recommendation; R5 reworded in EPR-REQ-001 v0.4 |
| 13 | R7 total mass | 187 kg against 140 kg. Options: (a) relax the total to 190 kg and keep the 50 kg piece limit; (b) lighten (flat-bar columns, 16 mm lid plate, 10 mm mold walls), perhaps 15 kg, then re-check; (c) both. Recommendation: (a), since the piece limit is what governs moving it | Decided by Amish, 2026-09-25: go with recommendation (a); R7 is 190 kg in EPR-REQ-001 v0.4 |
| 14 | Budget | BOM $488 against $450. Options: (a) raise `budget_usd` to $500; (b) cost down: plain pins without bushes (about $30 less, but fails R8), local offcut steel, lighter frame; (c) hold $450 until real quotes. Recommendation: (a). | Decided by Amish, 2026-09-25: go with recommendation (a); `budget_usd` raised from $450 to $500 |
| 15 | Fill control | The fill must be 0 to +2.7 % of nominal (0 to 206 g) for 2 MPa at the stop. Proposal: weigh every fill on a 10 kg scale with 50 g divisions (in the BOM) to about +1.3 % ± 100 g, and put the target mass on the test chart | Decided by Amish, 2026-09-25: go with recommendation; in the BOM and the precis |
| 16 | Other TRL 3 engineering proposals | (a) Lever pivot at x = -468, z = 266 mm, 1.7 m lever of 2 in schedule 40 pipe, mold rim at 940 mm; (b) crank stop at the 6° end angle, which limits the linkage to 173 kN (the structural design case); (c) ribbed lid (the TRL 2 22 mm plate reaches 275 MPa at 2 MPa); (d) end pawl against 47 J of kickback; (e) guard over the crank, connecting link and knee; (f) case-hardened steel bushes; (g) R4 at 296 blocks a day, 1 % short, to be revisited when cycles are timed | Decided by Amish, 2026-09-25: go with recommendation; all in the model and EPR-CAL-001 |

## Consequences

- EPR-PRB-001, EPR-PRC-001 and EPR-REQ-001 moved to v0.3 at TRL 3 and to v0.4 when Amish accepted the recommendations (EPR-DDR-002).
- `budget_usd` is $500 (was $450); R13 is met on paper ($488).
- R5 and R7 are met on paper against the accepted targets; R2 and R4 are at risk; R3, R8, R10 and R14 cannot be verified before block and wear tests, which are TRL 4 work and on hold.
