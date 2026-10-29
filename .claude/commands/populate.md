---
description: Populate this repo to a strong TRL 2 with concept media (current portfolio phase)
---
Work only in this repo. Read CLAUDE.md, .kit/STANDARDS.md and project.yaml first and follow them. Use the three-letter project code from the document IDs in docs/.

Goal: a strong TRL 2, meaning the concept is clearly formulated and visualized. Deliverables, and nothing else:

1. Update the problem statement (PRB-001: problem, users and needs table, stakeholders table, context, constraints; keep any co-design checklist), the user requirements (URS-001) and the product requirements (PRS-001: PR-NNN traced to UR-NNN, with targets, tolerances and units). Run the STEM check and concept options first if they do not exist yet (/stem-check, /concept-options).
2. Update the design precis (PRC-001): how it works, main components, key design choices, first-order numbers with stated assumptions, safety section, open questions.
3. Kit 1.9: build the detailed model in cad/src/model.py (STANDARDS section 24, level D2: every option, real stock, fasteners, welds, edge breaks, materials) and run `python .kit/cad_check.py --export` until it passes. Then call .kit/concept.py render_all from cad/src/concept_media.py with the chosen option's parts (concept.Part with a BOM number) to generate: media/hero.png with the 1.75 m scale figure, media/concept-blueprint.png and .pdf, media/model.glb and media/viewer.html (interactive 3D viewer), media/cutaway.png if the inside matters, media/exploded.png with BOM callouts, and media/flow.png (system, energy or material flow) where the concept moves energy or material. Label any flow values that are estimates.
4. Update bom/bom.csv with main components and indicative costs. Keep project.yaml budget_usd within the concept budget; if it must rise, propose it, never accept it.

Keep trl: 2 and trl_target: 3. Do not start TRL 3 work (detailed calculations, drawing sheets, build plan) or any TRL 4 work. Detailed CAD is not TRL 3 work under kit 1.9: it is required from the start. Record every decision as "Proposed, awaiting Amish". Write docs/REVIEW.md (what was done, results, requirements not met, proposed decisions, safety concerns, recommended next step). Run `python .kit/render.py --check`, commit, push, then stop.

Additional instructions from Amish, if any: $ARGUMENTS
