---
description: Write or refresh the pipeline documents: users and stakeholders, URS, PRS, REG, FEA, RSK, MKT, PLN and the traceability matrix
---
Work only in this repo. Read CLAUDE.md (section 5c), .kit/STANDARDS.md sections 19, 22 and 23, project.yaml and every document in docs/ first. Use the templates in .kit/templates/.

1. PRB: add the users-and-needs and stakeholders tables (templates/problem-tables.md), drawn from the existing users, context and co-design notes.
2. URS (docs/03a-user-requirements.md): user requirements with category, priority and source.
3. PRS (docs/03-requirements.md): migrate each R to a PR with the same target, verification and status, the old number in "Was"; add tolerance, units and the UR it traces to.
4. REG, FEA, RSK (with design FMEA at P3), MKT, PLN. Research regulatory and market facts on the web and cite each with a link and the date checked; reuse the focus-area research where it exists. Mark unknowns "to assess". Health projects: soft, non-clinical wording.
5. Run `python .kit/trace.py` and fix any gap you can; list the rest in docs/REVIEW.md.
6. Set stage in project.yaml (not above stage_cap in .kit/PHASE.yaml).

Record every decision as "Proposed, awaiting Amish". Run `python .kit/render.py --check`, commit, then stop.

Additional instructions from Amish: $ARGUMENTS
