---
description: Develop at least two concept options for this repo, score them and recommend one
---
Work only in this repo. Read CLAUDE.md (section 5c), .kit/STANDARDS.md section 21, project.yaml, PRB, URS and the STEM check first.

1. Define at least two concept options with different working principles (three where a clearly different principle exists). In a repo designed before kit 1.8, the current design is option A.
2. Kit 1.9: model each option in detail in cad/src/model.py (OPTIONS, PRINCIPLES, components(option); STANDARDS section 24) and run `python .kit/options.py`, which renders every option in Blender Cycles at one scale into media/options.png. Look at the picture.
3. Add each option's claims to the STEM check and rerun it.
4. Write docs/02a-concept-options.md (PRJ-OPT-001) from .kit/templates/concept-options.md: options, first-order numbers, weighted scoring against the user requirements, recommendation and the runner-up's best idea.
5. Record the recommendation as "Proposed, awaiting Amish" in docs/06-design-decisions.md and a concept selection DDR. Set concept_options in project.yaml; leave concept_chosen empty until Amish decides (for an existing repo it stays the current design unless he says otherwise).

Run `python .kit/render.py --check`, commit, then stop.

Additional instructions from Amish: $ARGUMENTS
