# Review note: EarthPress

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
