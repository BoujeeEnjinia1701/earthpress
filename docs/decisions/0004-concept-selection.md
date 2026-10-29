---
doc_id: EPR-DDR-004
title: EarthPress concept selection
project: EarthPress
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: Concept selection between options A, B and C (EPR-OPT-001); all within 10 %, so no pick; proposed, awaiting Amish
---

# 0004: Concept selection

- **Date:** 2026-10-25
- **Status:** proposed (awaiting Amish; no option recommended)

## Context

Kit 1.8 asks every repo for at least two concept options with different working principles, scored against the user requirements, with the current design as option A in a repo designed before kit 1.8 (STANDARDS section 21). EarthPress was designed around a lever and toggle press and has been constructable at TRL 3 since 2026-10-01 (EPR-DDR-003). Two other ways of compacting a block by hand were developed and modelled at the same detail level (D3): static pressing by a power screw, and dynamic compaction by a dropped weight. The full comparison is EPR-OPT-001; the STEM rows are B1 to B6 and C1 to C6 in EPR-STM-001.

## Options considered

| Option | Working principle | Score (of 245) | Strengths | Weaknesses |
| --- | --- | --- | --- | --- |
| A. Lever and toggle press (current) | Static pressing; a toggle's rising force ratio meets the stiffening soil | 186 | Output (about 296 a day), fixed block height at the crank stop, every part designed, priced and in the build plan | USD 542 against a USD 500 target; 203.8 kg against 200 kg (D2); two operators; narrow fill window; 47 J kickback held by a pawl |
| B. Power screw press | Static pressing by a two-start screw in a bronze nut, turned by a capstan | 181 | Pressure in hand at any fill; little stored energy; lighter (165.5 kg in the model) | Slower (about 225 a day); a greased two-start screw may not self-lock (B2); specialist bought parts; exposed threads in dust |
| C. Rope-lifted drop rammer | Dynamic compaction by about 25 blows of a 20 kg weight | 168 | Simplest parts; light pulls (98 N each); cheapest before pricing the pulley and rope | Density and strength against pressed blocks unproven (C2); about 160 a day; a weight falling about 4,000 times a day |

## Decision

**Proposed, awaiting Amish. No pick:** B scores 2.7 % and C 9.7 % below A, inside the 10 % band in which STANDARDS section 21 sends the options to Amish without a recommendation. Until he decides, the repo stays on option A (`concept_chosen` unset in `project.yaml`), the drawing, BOM and build plan describe A, and B and C stay as concept options in the model.

Points for the decision:

1. A is the only option whose every part is calculated, drawn, priced and planned; B and C are first-order.
2. B's main open point (B2) can be closed by a single-start screw at the cost of twice the turns, or by a brake; either lowers its output further.
3. C's main open point (C2) needs test blocks, which are TRL 4 work and on hold.
4. Choosing B or C changes the pitch ("a manual compressed earth block press with a lever and toggle linkage") and the build plan.

## Consequences

- If A: no design change; B and C stay on record as options; the D2 mass decision and the value-engineering items remain.
- If B or C: a new constructable design, calculation note, drawing, BOM and build plan for that option, and a pitch change; the soil kit, mold box and block stay.
