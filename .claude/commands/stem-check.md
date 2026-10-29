---
description: Run the STEM check (physics, chemistry, biology, mathematics, engineering) on this repo's idea and concept options
---
Work only in this repo. Read CLAUDE.md (section 5c), .kit/STANDARDS.md section 20, project.yaml, PRB, PRC and any CAL first.

1. List every physical, chemical and biological claim the idea and each concept option makes, each with its number and unit, field and branch.
2. Write docs/04-calcs/stem_check.py with .kit/stem_check.py: a limit, balance, order-of-magnitude or cited check for every claim. Run it.
3. Write docs/01b-stem-check.md (PRJ-STM-001) from .kit/templates/stem-check.md: the claims table with verdicts, fields not relevant with reasons, a verdict line per concept option, and sources.
4. Independent review: start a separate agent that sees only the claims table and the sources, not your reasoning, and ask it to refute every "Within known science" verdict. Record what it found and what changed.
5. For every "Fails, fix proposed" row, apply the fix rule (STANDARDS section 20): weigh the options, implement the best fix for the design and its constructability (model, drawings, CAL, BOM, build plan, PRS), record it in the decisions register as decided under Amish's standing instruction of 2026-10-23, and rerun the check so the row closes. A fix that changes the working principle, pitch or scope, and any outright Fails row, goes to docs/REVIEW.md and the decisions register as "Proposed, awaiting Amish".
6. Set stem_check in project.yaml to pass, open or fail.

Run `python .kit/render.py --check`, commit, then stop.

Additional instructions from Amish: $ARGUMENTS
