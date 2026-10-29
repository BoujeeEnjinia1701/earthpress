---
description: Upgrade this repo to kit 1.9 (CAD fidelity at every TRL, Cycles renders); only on Amish's go
---
Work only in this repo. Read CLAUDE.md and .kit/STANDARDS.md section 24 first.

1. Rebuild `cad/src/model.py` to the kit 1.9 interface: `PARAMS`, `OPTIONS`, `PRINCIPLES`, `CHOSEN`, `components(option)` returning `cad_parts.part()` dicts, using `.kit/cad_parts.py` for stock, fasteners, welds and edge breaks. Model every concept option to the detail level of the repo's stage (D1 at P0, D2 at P1 and P2, D3 at P3). In a repo already at TRL 3, keep the existing design and its numbers; only the modelling gets richer. Never change a design dimension without recording it in the decisions register.
2. Run `python .kit/cad_check.py --export` until it passes; fix the model, not the thresholds.
3. Re-render the options picture (`python .kit/options.py`) and, at TRL 3, the product renders (STANDARDS sections 12 and 24), then the cards.
4. Write docs/REVIEW.md (what changed, part counts per option, mass, any decision proposed), run `python .kit/render.py --check`, commit, then stop.

Additional instructions from Amish: $ARGUMENTS
