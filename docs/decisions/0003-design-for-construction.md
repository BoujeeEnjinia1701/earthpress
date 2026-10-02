---
doc_id: EPR-DDR-003
title: EarthPress design for construction
project: EarthPress
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "A1 and A3 accepted by Amish (2026-10-02); Table 1 still open for his review; status kept Draft"
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. The changes in Table 1 were made under Amish's 2026-09-30 instruction to make the design physically buildable; they are open for his review. Of the items in Table 3, A1 and A3 were accepted by Amish on 2026-10-02 as recommended in the design decisions register (EPR-DEC-001): "i approve your recommendations for all 555 open decisions." A2 needed no decision and is carried in the register's Value engineering section.

## Context

On 2026-09-30 Amish asked for a build plan for every repo that shows how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of EPR-DDR-002 showed what EarthPress does and that it works on paper, but several of its parts floated, overlapped a moving part or had no fixing. Checking the model with build123d (part-to-part overlaps at seven poses through the stroke and the eject, contacts, clearances of every moving part, and assembly order) found the fifteen problems below.

The changes keep what the press does: the same block, mold rim height, toggle, lever pivot, lever arc, grip heights, force ratio, crank stop, eject lift and two-person operation. No requirement target, pitch, problem or safety case is changed. Every change is in `cad/src/model.py`, which now builds each part on its own (`build_components`) and runs 47 constructability checks (`python cad/src/model.py --check`); all 47 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The base plate floated: the cross tubes sat 5 mm below the skid tops and none of them was under the plate. | Cross tubes raised flush with the skid tops; the two inner tubes moved under the base plate's edges; base plate 315 x 340 mm (was 240 x 380 mm) so it also carries the eject posts. | The plate now sits and is welded on two tubes; the posts stand on it. |
| P2 | The UPN 80 columns faced the mold with their open side, so the eight M16 bolts had no place for a nut (the flange is welded to the mold wall). The base beam plates overlapped the column flanges, and the base pin lugs floated above the beam's bottom plate. | Columns turned so the webs face the mold; the mold flanges are drilled and tapped M16 and the bolts go in from inside the open channel. Beam plates moved to the outside faces of the column flanges and welded there; lugs welded between the beam plates; bottom plate removed. Column feet get four M12 bolts each. | Every bolt can be reached with a socket from the open side of the channel; the beam and lugs form one welded clevis. |
| P3 | The push rod guide strap under the mold sat in the path of the upper links and upper pin, which rise into the mold (to 820 mm) at the end of the stroke; the upper pin's ends also passed through the mold walls. | Guide strap removed. The piston gets two 12 mm end skirts, 60 mm deep, that keep it square in the cavity. Upper pin shortened to 128 mm so it stays inside the cavity's width. | A plate 288 mm long and 25 mm thick could tip in a 290 mm cavity; with the skirts it cannot. |
| P4 | The base pin and upper pin could not be fitted: a 192 mm pin along the press's width is blocked by the column webs. Links had up to 20 mm of free play along the pins. | 40 mm access holes in the +Y column web at the base pin and at the upper pin (fitted with the toggle folded to 35°, upper pin at 699 mm). The knee pin goes in from the side, outside the columns, and the crank pin through a 31 mm access hole in the +Y lever bracket plate with the lever at rest. Spacer tubes on the base pin (two of 16 mm) and knee pin (two of 20 mm). Pins end 2 mm inside the column webs. | Each hole takes about 22 % of the column's section; the column's net section is still 2.5 times stronger than needed at the 173 kN design load [EPR-CAL-001 section 6]. |
| P5 | The links stopped at the pin centres, with no metal round the holes. | Round ends of half the link width on all four toggle links, the connecting link, the crank plates and the eject arm. Bushes 41 mm outside diameter pressed into the links. | A link needs metal round its hole; the net section at the bush is checked [EPR-CAL-001]. |
| P6 | The lid's hinge knuckle cut into the mold belt, and the hinge base had no pin through it. | The lid's two ribs are cut long as ears; the 30 mm hinge pin passes the two ears and two 20 mm lugs on the mold belt, 210 mm from the centre line. Knuckle tube removed. | Four plates on one pin, each ear inside a lug: the pin works in double shear as the calculation assumed. |
| P7 | The latch hook sat above its keeper and could not hold the lid down. | Latch: a 30 mm pin with a T-handle, pushed through ears on the lid ribs and two lugs on the mold, 210 mm from the centre line. | A pin through lugs is the simplest latch that holds the full 173 kN. |
| P8 | The rest stop bar sat in the path of the lever socket and would stop the stroke; the end pawl floated 5 mm off the bracket and could not reach the lever. | Rest stop: a 30 mm bar between the bracket plates, under the crank arms. Rest catch (on the -Y plate) and end pawl (on the +Y plate): each a 12 mm spring pawl on a 16 mm shaft that turns in the bracket plate, with a release handle outside the plate, catching the crank pin at the start and at the end of the stroke. Crank pin 112 mm long. | The pawl lies on the line the crank pin moves when the lever kicks back, so the 47 J kickback pushes it end on; the catch does the same at the start, where the lever's weight would otherwise let it fall into the stroke. |
| P9 | The eject fork's tines and the 110 mm foot pin crossed the upper links at the end of the stroke. | One central eject arm, cut from 20 mm plate with a crank in it, whose round nose pushes on the push rod's foot; foot pin removed. Eject pivot at 160 mm from the axis and 607.5 mm up (was 620 mm), so the nose stays under the rod for the whole 160 mm lift. | The arm stays inside the rod's width, where no link passes. The lever ratio is unchanged (160 mm arm). |
| P10 | The two ties ran 45 to 85 mm off the centre line, through the crank pin's path. | Ties moved out to 90 mm off the centre line, welded along the bracket plates' outer faces, with 10 mm end tabs bolted by two M12 through the beam plate and the column flange. | The crank pin now clears them; the core can be unbolted from the base. |
| P11 | The linkage guard (BOM 13) was in the BOM but not drawn. | Guard modelled: expanded metal on a 20 x 20 x 3 mm angle frame, top and both sides over the crank, connecting link and ties; two M10 feet on the base plate, two M10 brackets with 35 mm spacers on each bracket plate. | It clears every moving part over the full stroke. |
| P12 | The lever pipe began inside the hub, and nothing kept it in its socket. | Pipe starts 46 mm from the hub centre; a 12 mm locking pin with an R-clip through socket and pipe. | The lever cannot slide out under load. |
| P13 | The 100 mm hub sat between bracket plates 120 mm apart with nothing to locate it. | 10 mm washers each side; shaft held by circlips. | Locates the crank and connecting link on the centre line. |
| P14 | The block gauge was a placeholder (legs 316 mm apart). | Legs 292 mm apart inside and a 93 mm notch in the top edge. | It now checks the longest and the tallest good block (R1). |
| P15 | The lever bracket plates had no room for the parts above. | Bracket plates reshaped (about 230 x 272 mm) to carry the shaft, rest stop, catch and pawl shafts and the ties. | One outline, cut twice as a mirror pair. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Press 200.0 kg, heaviest piece 45.0 kg (was 187.0 kg and 36.6 kg) [EPR-CAL-001 section 8]. The total now counts the guard (5.5 kg) and the bolts (1.2 kg), which the concept left out. **R7's 190 kg total is not met** (10 kg over); its 50 kg piece limit is met. | Round link ends, lugs, base plate, guard, fixings. |
| Cost | BOM lines 1 to 7, 11 and 13 repriced: $520 against the $500 value-engineering target (`budget_usd`) [EPR-CAL-001 section 11]. **R13 is over the target by USD 20.** | Parts added for construction. `budget_usd` is not changed: see Table 3. |
| Calculations | EPR-CAL-001 v0.3: lid span 420 mm (lid SF 1.61 at the design load, was 1.84); link net section at the 41 mm bush hole (SF 2.33); new checks for the column at its access hole (SF 2.49) and the eject arm (SF 1.72). Lowest safety factor unchanged at 1.13 (bush bearing). | Follows the model. |
| Drawings | EPR-DWG-001 Rev P2; concept blueprint EPR-DWG-010 Rev P2; making sketches EPR-DWG-101 to 115 added. | Follows the model. |
| Documents | EPR-PRC-001 v0.5, EPR-REQ-001 v0.5, `bom/bom.csv`, `README.md`: mass, cost, latch, catch and eject descriptions. | Follows the model. |

*Table 3. Items proposed to Amish; A1 and A3 accepted on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | R7 total mass: 200 kg against 190 kg. | (a) Relax the total to 200 kg and keep the 50 kg piece limit (heaviest piece 45 kg). (b) Lighten: a 16 mm lid plate with deeper ribs, 10 mm mold walls, a lighter base plate, perhaps 10 kg, then re-check. (c) Both. | (a), as for EPR-DDR-002 item 13: the piece limit is what governs moving the press. Accepted 2026-10-02: the R7 total is 200 kg, defined to include the guard and bolts; the 50 kg piece limit is kept. |
| A2 | R13 cost: $520 estimated against the $500 value-engineering target (a hypothetical control target), USD 20 over. | No decision needed. The target stays $500. Savings worth trying: a lighter press, and local quotes at TRL 4; plain pins without bushes would save about $30 but R8 fails. | Carry in the value engineering section of EPR-DEC-001. |
| A3 | The rest catch adds a step: the operator lifts it before each stroke. | (a) Hand release, as modelled. (b) A foot pedal linked to the catch. | (a) for the prototype; reconsider after timing cycles (R4). Accepted 2026-10-02: hand release, with the rule that the catch is in before the latch is opened; a foot pedal only if timed cycles show the extra step costs output. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan EPR-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status: R7 moved from met on paper to **not met** (A1); with A1 accepted on 2026-10-02 the total limit is 200 kg including the guard and bolts, so R7 is met on paper again (EPR-REQ-001) and R13 to **over the value-engineering target by USD 20** (A2); R2 and R4 stay at risk; R5, R1, R11 and R12 stay met on paper; R6 and R9 met by design review; R3, R8, R10 and R14 not verifiable at TRL 3.
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept's hinge knuckle, latch hook, eject fork and guide strap; they need updating on Amish's Mac, where Blender is.
- The UPN 80 section, bush sizes, socket tube and springs are confirmed when bought (register, "To confirm when parts are bought").
