# Review note: EarthPress

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

### Proposed, awaiting Amish

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
