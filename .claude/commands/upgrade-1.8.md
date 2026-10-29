---
description: Upgrade a kit 1.7 repo to the kit 1.8 pipeline (STEM check, concept options, pipeline documents)
---
Work only in this repo. Read CLAUDE.md, .kit/STANDARDS.md (sections 19 to 23) and project.yaml first. The design does not change in this command; only the record around it grows.

1. Do everything /stem-check asks.
2. Do everything /concept-options asks, with the current design as option A.
3. Do everything /pipeline-docs asks.
4. Update the README: links line gains the STEM check, concept options, requirements and traceability; add short "Concept options" and "STEM check" sections after "Concept".
5. Set stage: P3 (for a TRL 3 repo), stem_check, concept_options; add the new files to trl_evidence.
6. Write a "Session: kit 1.8 upgrade" section in docs/REVIEW.md: what was added, STEM verdicts and the fixes made under the fix rule, the option scores, regulatory unknowns, top risks, and every decision awaiting Amish.

Run `python .kit/render.py --check` and `python .kit/release_gate.py`, commit, then stop.

Additional instructions from Amish: $ARGUMENTS
