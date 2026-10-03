# Review note: EarthPress

## Session 2026-10-01: constructable design and prototype build plan (kit 1.7.0)

Kit 1.7.0 installed (`.kit/`, `.claude/commands/`, `CLAUDE.md`). The design was checked for construction with build123d and made buildable under Amish's 2026-09-30 instruction ("fix the design assumptions to match and be physically feasible"); every change is in `docs/decisions/0003-design-for-construction.md` (EPR-DDR-003, Draft, open for his review).

### Design changes made for construction

- P1 Base frame: cross tubes flush with the skid tops and two of them under the base plate (the plate floated); base plate 315 x 340 mm, carrying the eject posts.
- P2 Columns turned so the webs face the mold; mold flanges tapped M16 and bolted from inside the channel (no room for a nut before); beam plates moved to the outside of the column flanges; base pin lugs welded between them (they floated); column feet bolted with 4 x M12 each.
- P3 Push rod guide strap removed (it sat in the path of the upper links and pin); two 12 mm end skirts under the piston keep it square; upper pin shortened to 128 mm (its ends passed through the mold walls).
- P4 40 mm access holes in the +Y column web for the base pin and the upper pin, and a 31 mm access hole in the +Y lever bracket plate for the crank pin (none could be fitted before); spacer tubes on the base and knee pins.
- P5 Round ends on every link and pressed-in 41 mm bushes (the links stopped at the pin centres).
- P6 Lid hinge: the lid ribs are cut long as ears on a 30 mm pin between two lugs on the mold (the knuckle cut into the belt and had no pin).
- P7 Latch: a 30 mm pin with a T-handle through the rib ears and two mold lugs (the hook sat above its keeper).
- P8 Rest stop bar under the crank; spring rest catch (-Y) and end pawl (+Y) on the crank pin (the old rest bar blocked the stroke and the pawl could not reach the lever).
- P9 Eject: one central cranked arm with a round nose under the push rod's foot, pivot at 607.5 mm (the fork and foot pin crossed the upper links at the end of the stroke).
- P10 Ties moved out to 90 mm off the centre line and bolted to the beam with tabs (they ran through the crank pin's path).
- P11 Linkage guard modelled and fixed (it was only in the BOM).
- P12 Lever pipe starts clear of the hub; 12 mm locking pin. P13 Hub washers and circlips. P14 Block gauge made real (legs 292 mm apart, 93 mm notch). P15 Bracket plates reshaped.

`cad/src/model.py` now builds each part on its own and runs 47 constructability checks at seven poses (`python cad/src/model.py --check`); all pass.

### What was done

- `docs/05-build-plan.md` (EPR-BLD-001 v0.1) with `cad/src/build_plan_media.py`: overview, 15 making sketches (`cad/drawings/EPR-DWG-101` to `115`), 11 joint pictures and 13 step pictures in `docs/05-build-plan/`.
- `docs/06-design-decisions.md` (EPR-DEC-001 v0.1): 9 open decisions (8 after the 2026-10-01 budget wording pass), 6 items to confirm when parts are bought, decisions made. The precis's open questions moved there.
- Regenerated: STEP and STL (`cad/step`, `cad/stl`), EPR-DWG-001 Rev P2, concept media (hero, blueprint EPR-DWG-010 Rev P2, cutaway, exploded, flow, model.glb).
- Calculations re-run: EPR-CAL-001 v0.3 (`docs/04-calcs/sizing.py`, `results.csv`). Updated: EPR-PRC-001 v0.5, EPR-REQ-001 v0.5, `bom/bom.csv`, `bom/bom-notes.md`, `README.md` (links line, "Building the prototype" section, numbers), `project.yaml` (`design_state: constructable`, new evidence).

### Key results and requirements

- Force ratio, grip heights (1.89 to 0.86 m), peak pull (668 N, 334 N each), crank stop and eject force (470 N) are unchanged.
- Lowest safety factor still 1.13 (bush bearing); lid 1.61 (was 1.84, longer pin span); column at its access hole 2.49; eject arm 1.72.
- **R7 not met:** 200.0 kg against 190 kg (heaviest piece 45.0 kg, within 50 kg). The total now counts the guard and bolts (6.7 kg) that the concept left out.
- **R13 over the value-engineering target:** $520 estimated against the $500 target, USD 20 over.
- R2 and R4 at risk; R5, R1, R11 and R12 met on paper; R6 and R9 met by design review; R3, R8, R10 and R14 not verifiable at TRL 3.

### Proposed, awaiting Amish (register EPR-DEC-001)

The budget is not a decision: `budget_usd` stays $500 as a value-engineering target, with the savings worth trying in the register's Value engineering section (2026-10-01 wording pass).

1. R7: relax the total to 200 kg (recommended) or lighten.
2. Rest catch: hand release (recommended) or a foot pedal.
3. First co-design partner and region (no recommendation), plus the open questions carried over from the precis (bushes, wear liners, fill by volume, lime, design soil).

### Stale until regenerated on Amish's Mac

The photoreal renders (`media/render-*.png`, referenced by the README), `media/card.png`, `media/social-preview.png` and `cad/src/product_model.py` still show the concept's hinge knuckle, latch hook, eject fork, guide strap and plain link ends. `product_model.py` still imports from `model.py` (same names) but was not re-run.

### Safety concerns

Unchanged in kind: up to 173 kN in the linkage, 47 J kickback (now taken end on by the pawl), crushing at the mold, linkage and eject arm, a 27 kg lid, cement burns and silica dust. The rest catch must be in before the latch is opened; the build plan's safety stops cover this.

### Recommended next step

Amish reviews EPR-DDR-003 and decides open decisions 1 and 2. TRL 4 (building to the plan) stays on hold.

## Session 2026-09-26: sources strengthened

- "By country or region" in `README.md`: the Colombia and Latin America row had no citation. It now cites [Botti, *Frontiers of Architectural Research*, 2023](https://www.sciencedirect.com/science/article/pii/S2095263523000584), and the row was rewritten to what the paper supports (soil-cement blocks in Colombian projects by the 1940s; the CINVA-Ram designed at CINVA in Bogotá in 1956 and spread to Bolivia, Brazil, Peru and beyond). The unsupported phrase "living tradition of earth building" was removed.
- Kept and verified by fetching: UNEP *Global Status Report 2024/2025* (32 % energy, 34 % CO2), Chatham House 2018 (cement about 8 % of CO2), UN-Habitat housing page (3 billion people, 96,000 units a day), Auroville Earth Institute (49 against 643 kg CO2/m³), UN SDG Report 2024 Goal 11 (regional slum figures), 14.7.4 NMAC (300 psi for CEB), Botti 2023 (CINVA-Ram, What sparked the idea) and the OSE wiki (kept alongside Botti; hydraulic, $3,000 to $6,500 in materials).
- Inspiration unchanged; it already rests on a peer-reviewed paper.
- No controlled document changed. No budget change.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (EPR-DDR-002 v0.1). EPR-DDR-001 moves to v0.2 with the new statuses.

### Decisions applied and what changed

- 15 items decided: TRL 2 items 1 to 7 and 9, and TRL 3 items 10 to 16. Most were already in the model, so the geometry, STEP, STL and EPR-DWG-001 (Rev P1) are unchanged in substance; all were regenerated.
- Budget (item 14): `budget_usd` $450 to **$500**; R13 target $450 to $500. BOM unchanged at $488, so R13 goes from not met to met on paper ($12 margin).
- R5 wording (item 12): 500 N with the grip between 0.9 and 1.6 m, to 500 N or less per operator, grip 0.8 to 1.9 m, peak at 1.0 m or higher. With two operators (item 11) at 334 N each and the peak at 1,157 mm, R5 goes from not met to met on paper.
- R7 total (item 13): 140 kg to **190 kg**, piece limit 50 kg kept. At 187 kg, R7 goes from not met to met on paper (3.0 kg margin).
- Items 10, 15 and 16 (eject seesaw, weighed fill, linkage proposals): already in the model, BOM and precis; the word "proposal" was removed.
- Item 9: pitch and problem unchanged; its budget part is superseded by item 14.
- `docs/04-calcs/sizing.py` and EPR-CAL-001 to v0.2: the script checks the accepted R5 band and peak height and the 190 kg total, and reads the budget from `project.yaml`; results table updated.
- Controlled docs bumped with revision "Recommendations accepted by Amish (DDR-002)": EPR-PRB-001 0.3 to 0.4, EPR-PRC-001 0.3 to 0.4, EPR-REQ-001 0.3 to 0.4, EPR-CAL-001 0.1 to 0.2, EPR-DDR-001 0.1 to 0.2. `bom/bom-notes.md` and `README.md` updated for the $500 budget and the new status.
- Kit links switched to designmolecule.com: all docs PDFs, EPR-DWG-001 and all media regenerated; superseded PDFs removed from `docs/pdf/` where they still showed the old domain; `media/_views*` deleted. Hero, blueprint and exploded images checked by eye.
- README "What sparked the idea" rewritten around the CINVA-Ram (Raúl Ramírez, CINVA, Bogotá, 1956; patented 1958), cited to Botti, *Frontiers of Architectural Research*, 2023. The same source now closes the TRL 2 citation flag on the CINVA-Ram origin in EPR-PRB-001.

### Requirement status (EPR-CAL-001 v0.2)

| Status | Requirements |
| --- | --- |
| Not met | None |
| At risk | R2 (2.00 MPa only with two operators, a weighed fill and the assumed soil); R4 (296 against 300 blocks a day; item 16g, revisit when timed) |
| Not verifiable at TRL 3 | R3, R8, R10, R14 |
| Met on paper | R1, R5, R7 (3 kg margin), R11, R12, R13 ($12 margin) |
| Met (design review) | R6, R9 |

### Still awaiting Amish

1. **First co-design partner and region (item 8).** No recommendation; stays "Proposed, awaiting Amish".

### Cross-repo actions

None. EarthPress uses no shared component and no recommendation required another repo to change.

### TRL 4

TRL 4 remains on hold by Amish's instruction. Decided but on hold: confirming the stabilizer with partner soils (item 5), timing cycles for R4 (item 16g), and any build, block test, proof-load test or soil compaction measurement. `trl: 3`, `trl_target: 3`.

## Session 2026-09-25: TRL 3

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (EPR-DDR-001 v0.1): TRL 2 items 1 to 7 and 9 adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review; item 8 (partner) and seven new TRL 3 items (10 to 16) listed as open.
- `docs/04-calcs/01-sizing.md` (EPR-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `results.csv`: force, linkage kinematics, grip force and work against a soil compaction law, fill tolerance, structure at the design load, ejection, mass, output, material flow, carbon and cost, with a results table for R1 to R14. The script reads `cad/src/model.py` and `bom/bom.csv` and prints every quoted number.
- `cad/src/model.py`: parametric build123d model with the toggle kinematics (`toggle_state`, `knee_and_crank`, `lever_angle`) shared with the calculation. Parts: base on skids with lever bracket, press core (columns and base beam), mold box with belt, ribbed lid with hinge and latch, piston with slotted push rod, toggle links and pins, connecting link, lever hub, crank and T-handle, eject seesaw and end pawl, plus the sieve, test kit, gauge and context. Exports `cad/step/` and `cad/stl/` `earthpress-assembly`, `earthpress-set`, `earthpress-mold`, `earthpress-lid` and `earthpress-toggle`.
- `cad/src/sheets.py` and `cad/drawings/EPR-DWG-001.svg`, `.pdf`, `.png`: general arrangement, Rev P1, "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept blueprint keeps EPR-DWG-010.
- `bom/bom.csv`: 13 lines, all priced with supplier types; new line 13 (linkage guard); `bom/bom-notes.md` totals against $450 and the recommended $500.
- `cad/src/concept_media.py` now builds from the model; every image in `media/` regenerated and checked by eye; the exploded-view lever offset was moved so it no longer crosses the legend; temporary `media/_views*` folders deleted.
- Docs updated to v0.3 with revision entries dated 2026-09-25: EPR-PRB-001, EPR-PRC-001, EPR-REQ-001. `project.yaml`: `trl: 3`, `trl_target: 3`, evidence listed; pitch, problem and `budget_usd` unchanged. `README.md`: TRL 3, numbers from EPR-CAL-001, links to the drawing, sizing note and DDR; the five required sections kept in order.

### Requirements (EPR-CAL-001)

Three met on paper, two met by design review, three not met, two at risk, four not verifiable at TRL 3.

| ID | Status | Value |
| --- | --- | --- |
| R5 | **Not met** | Peak pull 668 N (334 N each with two); grip 0.86 to 1.89 m. The 0.9 to 1.6 m band allows only 24.5° of arc with a 1.65 m grip radius |
| R7 | **Not met** | 187 kg against 140 kg; heaviest piece 36.6 kg (limit 50 kg); fits a 1.5 m bed |
| R13 | **Not met** | $488 against $450 (recommended $500, awaiting Amish) |
| R2 | At risk | 2.00 MPa with two operators and a fill of 0 to +2.7 %; one operator at 500 N stalls at 0.53 MPa; peak 571 to 809 N over the soil range |
| R4 | At risk | 296 blocks a day on an assumed 85 s cycle |
| R3, R8, R10, R14 | Not verifiable at TRL 3 | Need block tests, wear data or an outside review; fatigue range 89 MPa against 243 MPa allowed |
| R1, R11, R12 | Met on paper | Height 90.0 mm at the stop; CO2 7.6 % of fired brick; lid and latch checked at 173 kN, end pawl, guard |
| R6, R9 | Met (design review) | Bought turned parts only; kit defined |

Other key numbers: 81.2 kN for 2 MPa; force ratio 173:1 at the stop; lever arc 59.2°; compaction work 494 J (353 to 705 J); design load 173 kN (1,000 N at the grip); lowest safety factor 1.13 (bush bearing); kickback 47 J; eject 4.83 kN at 468 N on the grip; 1,683 blocks and 556 kg of cement for a small house.

TRL 2 figures corrected: press mass 123 to 187 kg; cost $403 to $488; compaction work 0.6 to 1.2 kJ to 0.35 to 0.71 kJ; output about 300 to 296 blocks a day; lever 1.5 to 1.7 m; the 22 mm lid (275 MPa at 2 MPa, above yield) replaced by a ribbed lid; ejection by continuing the stroke replaced, because a toggle ending near straight cannot lift the piston another 90 mm.

### Decisions recorded (EPR-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, now decided by Amish, 2026-09-25: go with recommendation (EPR-DDR-002): toggle mechanism (item 1); longer lever arc with a higher end grip (item 2, met in intent with a low pivot, since the 800 mm pivot and 100° arc would put the grip below the ground); 290 x 140 x 90 mm block (3); 2 MPa (4); 5 % cement with lime for clay soils (5); 12 mm base plate and bolted mold (6); field tests only (7); no change to budget, pitch or problem (9).

### Items then awaiting Amish (all but item 8 now decided, EPR-DDR-002)

1. **First co-design partner and region (item 8).** No recommendation.
2. **Ejection (item 10).** Recommendation: separate eject seesaw with the lever in a second socket and a lost-motion slot (in the model). **Decided by Amish, 2026-09-25: go with recommendation.**
3. **Two operators (item 11).** Recommendation: two people on a T-handle (in the model). **Decided by Amish, 2026-09-25: go with recommendation.**
4. **R5 wording (item 12).** Recommendation: 500 N or less per operator; grip 0.8 to 1.9 m with the peak force at 1.0 m or higher. **Decided by Amish, 2026-09-25: go with recommendation.**
5. **R7 total (item 13).** Recommendation: relax the total to 190 kg, keep the 50 kg piece limit. **Decided by Amish, 2026-09-25: go with recommendation.**
6. **Budget (item 14).** Recommendation: raise `budget_usd` to $500 ($488 now). Not applied. **Decided by Amish, 2026-09-25: go with recommendation.**
7. **Fill control (item 15).** Weigh every fill on a 10 kg scale to about +1.3 % ± 100 g. **Decided by Amish, 2026-09-25: go with recommendation.**
8. **Engineering proposals (item 16).** Linkage geometry and 940 mm rim, crank stop at 6° (173 kN design load), ribbed lid, end pawl, linkage guard, hardened steel bushes, and R4 at 296 blocks a day. **Decided by Amish, 2026-09-25: go with recommendation.**

### Cross-repo notes

EarthPress depends on none of the shared components in this batch (FieldNode, CellGuard, MotionCore, ThermaCart, TwinKit, CalRig) or SwapCell. No other repo was read or changed.

### Safety concerns

- Up to 173 kN in the linkage if two people pull hard at the stop; crushing in the mold, linkage, crank scissor and eject fork. The guard is not modeled.
- Lever kickback of about 47 J if released at the end of the stroke; the end pawl is a paper design.
- The lid weighs 26 kg and is lifted every cycle (about 127 N at the latch end); it must never be opened with the lever off its rest stop.
- The soil law is an assumption: a softer soil raises the peak pull to 809 N, and operators may then hang on the lever.
- Cement burns, silica dust from dry sieving, 7.6 kg blocks handled about 300 times a day, and uncertified blocks for structural use are unchanged from TRL 2.

### Other notes

- No TRL 4 material exists in the repo: no test plans or reports, build procedures, cut lists or purchasing lists. `build-log/README.md` is the scaffold stub and was not touched.
- Citations: the TRL 2 note flags the CINVA-Ram origin (Colombia, 1950s) as stated without a link. WebFetch could not reach the Wikipedia CINVA Ram page (the domain is cache-only for this tool), and the Wikipedia compressed earth block page does not mention it, so the flag stays. WebSearch was not used (quota exhausted).
- The linkage geometry came from a numerical design search (minimum peak grip force with the grip between 0.8 and 1.9 m); the search script is not in the repo, and `sizing.py` checks the chosen geometry.
- The kit's cutaway cuts at the mean Y of the parts; the press is centered on Y = 0 and the sieve, kit, gauge and blocks are excluded, so the cut passes through the piston axis without shifting the model.
- The soil compaction law (tenfold over the last 14 mm) is the largest single uncertainty in R2 and R5.
- `render.py --check` and `render.py` pass; PDFs are in `docs/pdf/`.

### Recommended next step

Review EPR-DDR-001, in particular the two-person lever (item 11), the R5 and R7 rewording (items 12 and 13) and the budget (item 14), and choose the first partner (item 8). TRL 4 is on hold by Amish's instruction. For reference only, TRL 4 would need: a bench build of the press; a lab test report (TST, `environment: lab`) covering the soil compaction curve with partner soil, grip force through the stroke with one and two operators, fill-mass sensitivity, lid and latch proof load at 1.5 times the block force, ejection force, cycle time and block strength after curing; and build-log entries. None of this has been started.

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (EPR-PRB-001 v0.2): why it matters (cited), users and context, constraints, out of scope, prior work with sources (CINVA-Ram, Auroville Earth Institute, Open Source Ecology CEB Press, 14.7.4 NMAC, ISSB presses), open questions; co-design checklist kept.
- `docs/03-requirements.md` (EPR-REQ-001 v0.2): 14 measurable requirements (R1 to R14) with targets, verification and a concept status column, plus a list of requirements not met or at risk.
- `docs/02-concept.md` (EPR-PRC-001 v0.2): how it works in six steps, numbered components, first-order numbers with assumptions, key design choices, safety section, open questions.
- `cad/src/concept_media.py`: massing model of the press (frame on skids, mold box, lid, piston, toggle, lever and crank, ejection stop and catch) with the soil sieve, test kit, block gauge, a block stack and loose soil fill as context; 1.75 m scale figure.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `cutaway.png` (mold, fill, piston and toggle), `exploded.png` (callouts 1 to 10 match the BOM), `flow.png` (material flow per 100 blocks, estimates), `model.glb` and `viewer.html`. Temporary `media/_views*` folders removed.
- `bom/bom.csv`: 12 lines with indicative USD costs, rows 1 to 10 numbered to match the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line after the intro; Concept rationale, Burning platform, Where it could be used (by industry, by country or region), What sparked the idea, Problem, Concept, Key components and Safety expanded with cited figures.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Block | 290 x 140 x 90 mm, about 6.9 kg dry | R1 |
| Force for 2 MPa | about 81 kN | R2 |
| Force ratio | lever about 19:1 times toggle about 9:1 (within about 3° of straight) | R2 force met on paper |
| Compaction work versus one operator | about 0.6 to 1.2 kJ needed, about 0.65 kJ available over a 50° arc | **R2 at risk** |
| Lever grip height | about 1.36 m at start, about 0.3 m at end | **R5 at risk** |
| Output | about 300 blocks per day, crew of four (about 9 m² of wall) | R4 met on paper |
| Press mass | about 123 kg total; frame about 61 kg | **R7 not met** (50 kg per piece) |
| Cement | about 0.33 kg per block; about 560 kg for a 50 m² wall | R10 target 5 % |
| Embodied CO2, 7.1 m³ of walling | about 0.35 t CSEB against about 4.6 t fired brick (about 8 %) | R11 met on paper |
| Parts cost | about $403 | R13 met ($450 budget) |

Requirements not met or at risk:

- **R7 not met:** the frame is about 61 kg against a 50 kg single-piece limit.
- **R2 at risk:** the force ratio can reach 2 MPa, but one operator may not deliver enough work over the modeled 50° lever arc.
- **R5 at risk:** the grip ends about 0.3 m above ground at the point of highest force.
- **R3, R8 and R10 cannot be shown at TRL 2**; block strength depends on soil, mix and curing and needs block tests (TRL 4).
- R12 and R14 are addressed in concept only.

### Proposed, awaiting Amish (items 1 to 7 and 9 now decided by Amish, 2026-09-25: go with recommendation, EPR-DDR-002; item 8 still awaiting Amish)

1. **Mechanism.** Option A: bottom piston with a toggle and one lever for press and eject (CINVA-Ram pattern). Option B: the same frame with a 20 t hydraulic bottle jack (reaches 4 MPa easily, adds a bought hydraulic part). Option C: screw press (slow). Recommendation: A, with B documented later as a variant.
2. **Lever layout.** Raise the lever pivot to about 800 mm for a 100° arc, to fix R2 and R5, rather than keeping the low pivot in the model. Recommendation: raise it at TRL 3.
3. **Block size.** Flat 290 x 140 x 90 mm (Auroville module), 300 x 150 x 100 mm, or an interlocking block. Recommendation: 290 x 140 x 90 mm, with interlocking inserts as a later option.
4. **Compaction target.** 2 MPa (manual, one or two operators) or 4 MPa (needs about 162 kN). Recommendation: 2 MPa.
5. **Stabilizer default.** 5 % cement by dry mass, with lime for clay-rich soils. Recommendation: as stated, confirmed with partner soils.
6. **Meeting R7.** Thinner 12 mm base plate and a bolted mold, or a two-part bolted frame, or relaxing R7 to 65 kg. Recommendation: thinner base plate plus bolted mold.
7. **Soil test kit scope.** Field tests only, or add a small hand-operated block crusher for strength checks. Recommendation: field tests only at TRL 3.
8. **First partner and region** for co-design (for example an earth-building NGO in East Africa or India).
9. **Budget.** No change proposed; about $403 is within $450. `project.yaml` pitch and problem are unchanged because the figures found support them.

### Safety concerns

- About 81 kN at the piston: crushing of hands in the mold or linkage; lever kickback if the grip slips or a pin fails; lid or latch failure under load.
- Portland cement burns to skin and eyes; respirable crystalline silica from sieving dry soil.
- Manual handling: 7 kg blocks repeated hundreds of times a day, and a 123 kg press.
- Blocks are uncertified; structural and seismic use needs an engineer and tests under local code.
- Welding and grinding hazards while building the press.

### Problems and notes

- The massing model is proportional, not kinematic: the modeled crank is about 60 mm and the toggle links about 185 to 200 mm, while the precis uses about 80 mm and about 190 mm. The TRL 3 model should set these from the linkage calculation.
- WebSearch was unavailable in this session (session search budget used up), so sources were verified by fetching the primary pages directly. No figure was used that could not be confirmed on its source page. The CINVA-Ram origin (Colombia, 1950s) is stated without a link.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 to 4 and 6. If approved, run `/advance-trl3` to size the linkage and lever layout by calculation (force ratio and work over the stroke), check the lid, latch, pins and links, and build the parametric model and drawing sheet.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26.

### What was added

`cad/src/product_model.py` exposes `product_parts()` (54 parts: 24 shell, 9 internal, 17 accessory, 4 context), `TITLE` and `RENDER_VIEWS` (hero with the operator, exploded, and a detail view of the toggle linkage, connecting link and lever hub under the mold box, without the lever pipe, operator or ground). It imports PARAMS and the kinematics (`geometry()`, `theta_start()`, `toggle_state()`, `knee_and_crank()`) and the geometry helpers from `cad/src/model.py`; every main dimension and interface is as model.py. It adds:

- Base skids and cross tubes as rounded 60 and 50 mm hollow sections with rubber end caps; filleted base plate, lever bracket plates and rest stop with a rubber pad.
- UPN 80 columns, base beam, rounded toggle base lugs and column feet with eight M12 bolt heads; a yellow pinch-point label on the front column.
- Teal mold box with a rounded belt, flanges, guide strap, hinge base and latch keeper; a bright ground rim; eight M16 bolt heads on the column webs; a raised EARTHPRESS nameplate on the belt.
- Lid with filleted plate and ribs, hinge knuckle, latch hook with a rubber grip, bright hinge and latch pins with circlips.
- Piston and slotted push rod in bright steel, with the foot pin.
- Round-ended toggle links and connecting link in safety orange; 35 mm pins with circlips, bush flanges and brass grease nipples.
- Lever hub, round-ended crank plates and socket; crank pin and circlips. The 2 in lever pipe and T-handle as a removable accessory, with ringed rubber grips and end caps.
- Eject seesaw with round-ended fork plates, posts, pivot pin and socket; the end-of-stroke pawl.
- Soil sieve with a timber frame, wire mesh and prop; soil test kit crate with hand holes and vents, a shrinkage box, two clear 1 L jars showing settled sand, silt and clay layers, and a laminated chart; block gauge with a grip.
- Context: a compact patch of compacted earth, the stack of 32 finished blocks, the loose soil in the mold, and the shared clay mannequin (1.75 m, push pose) with both hands on the T-handle grips and feet on the ground.

`README.md` now shows `media/render-hero.png` and links `media/render-exploded.png`; the orchestrator produces both files. Matplotlib self-check previews (clear parts left out) are in `/tmp/earthpress-prod/`.

### Differences from model.py (Proposed, awaiting Amish)

1. **Pose.** The press is shown at 85 % of the compaction stroke (toggle about 9.5° from vertical, T-handle at about 1.21 m) instead of at the start of the stroke, so the operator's push reads. The pose uses model.py's own kinematics; no dimension changes. Recommendation: keep this pose for renders only.
2. **Link ends.** Toggle links, the connecting link, crank plates and eject fork plates extend half their width past the pin centres with round ends; model.py stops each bar at the pin centres, which leaves no metal round the pins. Recommendation: adopt round ends in model.py at the next model revision.
3. **Added visible details not in the BOM:** the nameplate, the pinch-point label, rubber tube end caps, the rest stop pad and the latch hook grip. Recommendation: add labels and caps to BOM line 11 (hardware and finish) if Amish accepts them.
4. **One operator.** The mannequin is a single person, while EPR-CAL-001 needs two people on the T-handle (668 N peak pull). Recommendation: keep one figure for a clean hero, and state two operators in the caption; or add a second mannequin on the other half of the T-handle.
5. **Placement of the kit.** The soil sieve moves from about (1150, 750) to (250, 690) mm, behind the press, and the test kit 50 mm toward the press, to keep the ground patch compact. The sieve mesh is drawn at a 30 mm pitch, not 5 mm. Recommendation: accept for renders.
6. **Colours** differ from the concept media: graphite frame, teal mold and lid, orange linkage, black lever, grey eject lever. Recommendation: accept as the product palette.
7. **Linkage guard (BOM 13)** is not shown, as in model.py, so the toggle can be seen. Recommendation: show it as expanded metal in a later render once its shape is drawn.

### TRL

This is an appearance model only. No tolerances, fabrication detail, build or test work were added. `trl: 3`, `trl_target: 3`; TRL 4 remains on hold.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-02: open decisions decided

Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This approves the recommendation written for every open decision in the design decisions register (EPR-DEC-001). trl stays 3; nothing was built, bought or tested, and TRL 4 remains on hold.

### Decisions recorded (8)

| Register item | Decision |
| --- | --- |
| 1 | R7 total 200 kg including the guard and bolts; 50 kg piece limit kept (EPR-DDR-003 A1 accepted) |
| 2 | Hand release of the rest catch for the prototype; the catch is in before the latch is opened; foot pedal only if timed cycles show a cost (EPR-DDR-003 A3 accepted) |
| 3 | Partner that already trains builders in stabilized earth blocks; first candidate to approach, the Auroville Earth Institute |
| 4 | Case-hardened steel bushes with grease nipples kept; felt or rubber dust seals added at the bush faces |
| 5 | Plain 12 mm mold walls for the prototype, wear measured against R8; liners only if needed |
| 6 | Weigh every fill; calibrated scoop only for a soil with measured scatter inside the 0 to 2.7 % window |
| 7 | Cement default; lime a documented option with its own chart and longer curing; no press change |
| 8 | Operating chart on the softer soil (809 N, 405 N per operator) until partner soils are measured |

All 8 moved to Decisions made in EPR-DEC-001, dated 2026-10-02; the Open decisions section now reads "None."

### Documents changed

- `docs/06-design-decisions.md` (EPR-DEC-001 v0.3): items 1 to 8 moved to Decisions made; Open decisions reads "None"; the lighter-press saving in Value engineering reworded now that decision 1 is made
- `docs/decisions/0003-design-for-construction.md` (EPR-DDR-003 v0.3): A1 and A3 recorded as accepted (status kept Draft; Table 1 still open for review at that point, see below); R7 consequence updated
- `docs/03-requirements.md` (EPR-REQ-001 v0.7): R7 relaxed to 200 kg including guard and bolts, now met on paper; R5 status gives the softer design soil; summary updated
- `docs/04-calcs/01-sizing.md` (EPR-CAL-001 v0.5): R7 text and results row against 200 kg; softer design soil noted under R5
- `docs/02-concept.md` (EPR-PRC-001 v0.7): R7 status; weighed fill and scoop rule; design soil; bush dust seals; lime option; plain mold walls
- `docs/01-problem.md` (EPR-PRB-001 v0.5): partner rule and first candidate; design soil and lime; press mass
- `bom/bom-notes.md`: dust seals at the bush faces and plain mold walls noted
- `README.md`: R7 status
- `docs/decisions/0001-trl2-review-decisions.md` (EPR-DDR-001 v0.3): item 8 ("Proposed, awaiting Amish") recorded as decided
- `docs/decisions/0002-recommendations-accepted.md` (EPR-DDR-002 v0.2): item 8 recorded as decided
- PDFs regenerated with `python3 .kit/render.py`; superseded versions removed.

Note: the register had no open item for accepting the design-for-construction changes P1 to P15 as a whole (EPR-DDR-003, Table 1), so this approval did not cover them. Amish accepted them later on 2026-10-02 (see the next session).

### Follow-up actions to carry approved decisions into the design

The model, BOM quantities and prices, calculations and pictures were not changed in this session. These actions carry the approved decisions into them:

1. Decision 1 (calculations): Re-run `docs/04-calcs/sizing.py` with the R7 total at 200 kg including the guard and bolts so its R7 line and `results.csv` show met on paper.
2. Decision 4 (model, BOM): Add felt or rubber dust seals at the bush faces: a BOM line or an addition to line 5 with a price, and the seal faces in the model and the link making sketches if they change the stack-up.
3. Decision 4 (drawings, build plan pictures): Show the dust seals in the toggle linkage joint pictures and making sketches once modelled.
4. Decision 6 and 8 (calculations, documents): Write the operating chart for the softer design soil (809 N, 405 N per operator) and the scoop calibration rule into the test kit procedure; recompute per soil once partner soils are measured.
5. Decision 7 (documents): Add a lime mix chart and its curing period to the soil test kit procedure.
6. Decision 5 (test plan): Measure mold wall wear at TRL 4 against R8; design bolt-on liners only if the rate would not last 50,000 sandy blocks.
7. Decision 3 (documents): Approach the first candidate partner (the Auroville Earth Institute); nothing is agreed yet.

### Points found in the review

Raised when the recommendations were written (2026-10-01) and kept here so they are not lost:

- Item 1 does not compare like with like: the 190 kg limit was set against a 187 kg figure that left out the guard and bolts (6.7 kg), so the 200 kg total is about 6 kg of real growth plus 6.7 kg newly counted.
- Item 4 overlaps a decision already made: case-hardened steel bushes were accepted on 2026-09-25 (EPR-DDR-002, item 16f).
- Item 7 overlaps a decision already made: 'lime for clay-rich soils' was accepted with the stabilizer choice on 2026-09-25 (EPR-DDR-001, item 5); only the chart and curing details are open.
- The seven appearance items from REVIEW.md 2026-09-26 are not in the register. Two touch what the renders claim: item 4 shows one operator although the press needs two (668 N peak), and item 7 leaves the linkage guard out of the renders; both should be resolved before the renders are public.
- Item 6 is already decided for now (weighed fill, EPR-DDR-002 item 15); the open part is only the future scoop rule.

## Session 2026-10-02: design-for-construction changes accepted

Amish, 2026-10-02: "APPROVED: Design-for-construction changes in 10 repos (CityTwin, CoolShade, PalletPilot, Heliolite, PotholeLog, EarthPress, ReadyKit, CellCheck, CargoMule and ThermaCart)". This accepts the design-for-construction changes P1 to P15 in Table 1 of EPR-DDR-003, which were left open for his review when the open decisions were decided earlier the same day. No other item is decided by it. trl stays 3; no build or test work was done, and the model, BOM, calculations and pictures are unchanged.

### Documents changed

- `docs/decisions/0003-design-for-construction.md` (EPR-DDR-003 v0.4, status Draft): status line now "accepted" with Amish's words.
- `docs/06-design-decisions.md` (EPR-DEC-001 v0.4): Decisions made row added, dated 2026-10-02; the 2026-10-01 row no longer calls the changes open for review.
- `docs/05-build-plan.md` (EPR-BLD-001 v0.3): section 2 says EPR-DDR-003 is accepted.
- PDFs regenerated.

### Recommended next step

No change: the follow-up actions of the previous session stand. TRL 4 remains on hold by Amish's instruction.

## Session 2026-10-02: approved follow-ups carried out

Authority: Amish, 2026-10-02, approved every follow-up action from the open-decision sign-off. `trl` and `trl_target` stay at 3; `budget_usd` is unchanged at 500. No commit or push.

### Follow-ups

1. Decision 1, R7 at 200 kg: done. `docs/04-calcs/sizing.py` re-run: steel 200.0 kg (199.991 kg) plus about 5 g of felt dust seals is 199.996 kg, so R7 is met on paper with a 4 g margin; `results.csv` updated. The margin is too small to mean anything; the weighed prototype decides.
2. Decision 4, dust seals in the model and BOM: done. `cad/src/model.py` now has eight 2 mm felt or rubber washers (50 mm outside, 35.5 mm bore) on the outer link faces at the base, knee and upper pins; pins already ended 4 mm past the links, which leaves room for the seal and a 1.5 mm circlip, so no part of the stack-up changed. Model checks: 52 of 52 pass (new: seal contacts, circlip room, seal clearance from the column webs). BOM line 5 goes from USD 91 to USD 94 (eight washers at about USD 0.35, rounded to USD 3); STEP and STL regenerated.
3. Decision 4, drawings and pictures: done. EPR-DWG-001 now Rev P3; the toggle link making sketch (EPR-DWG-107) notes the seals; joint pictures for the base pin, knee and upper pin, the overview and assembly steps 5 to 7 show them; concept media regenerated.
4. Decisions 6 and 8, operating chart and scoop rule: done. New build plan section 3.15 (soil test kit procedure) carries the operating chart for the softer design soil and the scoop rule; `sizing.py` section 4b computes them. Finding: on the softer soil the good fill window narrows to 0 to +2.0 % (from 0 to +2.7 %), so the weighing target for it is +1.0 % (7.72 kg) give or take 75 g, not +1.3 %. Peak pull 809 N (405 N each) at nominal fill and 498 N each at +2.0 %.
5. Decision 7, lime chart: done, as starting values to be confirmed by strength tests: 8 % hydrated lime (51 kg per 100 blocks against 33 kg of cement), about 8 weeks damp curing against about 4 (`sizing.py` section 4c; build plan Table 3). The 8 % and 8 weeks are my assumptions, not sourced figures.
6. Decision 5, mold wall wear measurement: not done, TRL 4 test plan work.
7. Decision 3, approach the Auroville Earth Institute: not done, outreach by Amish.

### Requirement status changes

- R7: met on paper (was not met against 190 kg until 2026-10-02; the calculation now confirms it): 199.996 kg.
- R13: stays over the target, now by USD 23 (USD 523 against USD 500). Value-engineering target: USD 500. Estimated cost of the constructable design: USD 523 (USD 23 over the target).
- No other status changed.

### Documents changed and new versions

EPR-CAL-001 v0.6; EPR-REQ-001 v0.8; EPR-PRC-001 v0.8; EPR-BLD-001 v0.4; EPR-DEC-001 v0.5. Also `README.md`, `bom/bom.csv`, `bom/bom-notes.md`, `docs/04-calcs/sizing.py` and `results.csv`, `cad/src/model.py`, `sheets.py`, `build_plan_media.py`, `concept_media.py`, `product_model.py`.

### Render scenes

`cad/src/product_model.py` was out of date (it still used parameters from before the constructable design and failed to run). It now takes every steel part from `cad/src/model.py` itself (round link ends, tapped flanges, access holes, catch, guard, bolts, seals) and adds only paint, rubber, felt, circlips, grease nipples, grips, the sieve, test kit, blocks and the mannequin. The decorative extras of 2026-09-26 that no longer match (nameplate, pinch-point label, rest stop pad, latch hook grip, mold rim band, bush flanges) are dropped; the guard is now shown. Scenes exported to `/home/claude/renders/earthpress` for the views hero, exploded and detail, with `earthpress__jobs.json`. Photoreal images, `card.png` and `social-preview.png` are to be made on Amish's Mac.

### Cross-repo actions

None for other repos.

### Decisions proposed and awaiting Amish

None new. The lime values (8 %, 8 weeks) in Table 3 of the build plan are starting figures to confirm at TRL 4.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.
