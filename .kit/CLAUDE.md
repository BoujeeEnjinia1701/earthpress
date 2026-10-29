# Instructions for Claude working in this repo

This repo is one design in Amish Chadha's Open Hardware Portfolio. These rules apply to every session and override any broader instruction in a prompt. If a prompt conflicts with them, stop and ask.

## 1. Current portfolio phase: TRL cap 3

- The whole portfolio is capped at **TRL 3** (proof of concept on paper) until every repo is populated. The cap is set in `.kit/PHASE.yaml`.
- Do **not** create TRL 4 or later work: no building or testing of hardware, test articles, purchasing checklists, test plans or reports (TST), PCB layouts or Gerbers, firmware beyond a clearly labeled sketch, or build-log entries or tooling. The prototype build plan (BLD-001, `docs/05-build-plan.md`, STANDARDS section 18) is TRL 3 paper work and is required; it is a plan, never a record of a build.
- `trl` and `trl_target` in `project.yaml` must not exceed the cap. `python .kit/render.py --check` enforces this.
- If the design looks ready for TRL 4, write that up as a recommendation in the review note (section 4) and stop.

## 2. Decision rights

- Amish makes all decisions on scope, budget, naming, visibility, safety trade-offs and anything that changes the pitch.
- Never record a decision as made, accepted or approved unless Amish stated it in this session. Record it as **"Proposed, awaiting Amish"** with the options and a recommendation.
- Never raise a budget past the figure in `project.yaml` without flagging it as proposed.

## 3. Scope of a session

- Do exactly what the prompt asks, in the order asked. Do not add deliverables the prompt did not name.
- Optional ideas go in the review note as suggestions, not into the repo.
- Keep each session to one TRL step for one repo.

## 4. End every session with a review note

Write or update `docs/REVIEW.md` before the final commit:

- What was done, with file paths
- Key results and numbers, including any requirement that is **not** met
- Decisions proposed and awaiting Amish
- Safety concerns
- Recommended next step

Then commit, push and **stop**. Do not continue into the next step without a new instruction.

## 5. Required concept media (all repos, TRL 2 and up)

Every repo needs visuals that explain the idea. Generate them from `cad/src/concept_media.py` with `.kit/concept.py` (`render_all`):

| File | What it shows | When |
| --- | --- | --- |
| `media/hero.png` | Shaded isometric render with a 1.75 m person for scale; the website card | Always |
| `media/concept-blueprint.png` (+ `.pdf`) | Blueprint concept sheet: views, scale, key figures | Always |
| `media/model.glb` + `media/viewer.html` | Interactive 3D viewer for the website | Always |
| `media/cutaway.png` | Section view | When the inside matters |
| `media/exploded.png` | Exploded view with numbered callouts matching the BOM | Recommended |
| `media/flow.png` | System, energy or material flow diagram | When the concept moves energy or material |

For small objects (wearables, handheld tools) use a context part such as a hand or forearm instead of the 1.75 m person (`scale_figure=False, context=[...]`); see `tremortrace` for a worked example. Kit 1.9: the model is detailed at every TRL, never a massing block (STANDARDS section 24): build it in `cad/src/model.py` from `.kit/cad_parts.py`, model every concept option to the repo's detail level (D1 at P0, D2 at P1 and P2, D3 at P3), run `python .kit/cad_check.py --export`, and render every product picture with Blender Cycles. Label concept media "CONCEPT, NOT FOR FABRICATION". Mark estimated flow values as estimates.

## 5a. Session commands

Use the repo's slash commands rather than improvising scope: `/populate` (strong TRL 2 with media), `/advance-trl3` (only after Amish approves), `/rein-in` (stop and review), `/refresh-media`, `/render-product` (appearance model, photoreal renders and storefront images), `/release` (release gate and release preparation; never makes the repo public), and for the pipeline `/stem-check`, `/concept-options`, `/pipeline-docs` and `/upgrade-1.8` (section 5c).

## 5b. Product renders and storefront images (TRL 3)

- Build `cad/src/product_model.py` (`product_parts()`, `TITLE`, `RENDER_VIEWS`) with every main dimension taken from `cad/src/model.py`. Record any appearance deviation in `docs/REVIEW.md` as "Proposed, awaiting Amish".
- Give scale with `.kit/context_parts.py`: a hand or forearm for small objects, `mannequin()` for body-scale products. Never render a floating person.
- Render with `.kit/export_views.py` and `.kit/photoreal.py`, caption with `.kit/photo_caption.py`, and lead the README with `media/render-hero.png`.
- Then run `python .kit/cards.py .` for `media/card.png` and `media/social-preview.png`. See `.kit/STANDARDS.md` sections 12 and 13.
- Run `python .kit/image_qc.py` and look at every image yourself. Text must be inside the image, never overlap other text or the render, and be readable; renders must be sharp. Fix and regenerate anything that fails.

## 5c. The pipeline (kit 1.8 and 1.9, STANDARDS sections 19 to 24)

- Every repo carries the pipeline documents for its stage: STEM check (STM), concept options (OPT), user and product requirements (URS, PRS), the generated traceability matrix (RTM), regulatory register (REG), feasibility (FEA), risk register with hazard analysis and design FMEA (RSK), market and viability (MKT) and project plan (PLN). Templates are in `.kit/templates/`.
- **STEM check first.** Before designing anything, list every physical, chemical and biological claim and check it against known science (`docs/04-calcs/stem_check.py`, `.kit/stem_check.py`). A claim that fails stops the concept unless a fix keeps the working principle: then propose the best fix for the design and its constructability and implement it in the same session (Amish's standing instruction, 2026-10-23; STANDARDS section 20, fix rule), record it in the decisions register as decided under that instruction, and rerun the check. A fix that changes the working principle, pitch or scope goes to Amish instead. Then have an independent reviewer (a second agent that does not see your reasoning) try to refute every "Within known science" verdict, and record what it found.
- **At least two concept options.** Different working principles, not size or material variants. Score them against the user requirements, draw them with `python .kit/options.py`, and record the choice as "Proposed, awaiting Amish". If two options are within 10 %, both go to Amish. In a repo designed before kit 1.8 the current design is option A; never redesign it without Amish's go.
- **Requirements.** User requirements (UR) come from the users and stakeholders in PRB; every product requirement (PR) traces to one. Run `python .kit/trace.py` after any requirement, calculation, BOM or build plan change. Never type the matrix by hand.
- **Research.** Regulatory and market facts are cited with a link and the date checked. Standards shared across a focus area are researched once and cited in each repo. Never invent a price, standard number or classification; mark unknowns "to assess".
- `stage` in `project.yaml` may not exceed `stage_cap` in `.kit/PHASE.yaml` (P3 now). P4 to P6 deliverables appear only as planned work in PLN.
- **CAD fidelity (kit 1.9).** Every option in `cad/src/model.py` (`OPTIONS`, `components(option)`) is modelled with real stock, fasteners, welds and edge breaks to the stage's detail level, and `cad/fidelity.json` must pass (`python .kit/cad_check.py --export`). The options picture is rendered from those models with `python .kit/options.py`.
- Commands: `/stem-check`, `/concept-options`, `/pipeline-docs`, `/upgrade-1.8`, `/upgrade-1.9`.

## 6. Standards

- Follow `.kit/STANDARDS.md` (document IDs, versions, revision history, TRL evidence).
- Chicago Manual of Style. **Never use em dashes.** Restructure the sentence instead.
- SI units, with imperial in parentheses where useful.
- Safety notes stay in every document that describes something hazardous. Mains voltage, high temperature, pressure, lithium cells and moving machinery always get a safety section.
- Run `python .kit/render.py --check` before committing. Do not commit if it fails.

## 7. Release and authorship

- Making a repository public, tagging a release or changing repository settings is Amish's decision. Prepare, then ask.
- Before any release, `python .kit/release_gate.py` must pass (`.kit/STANDARDS.md` section 14). Fix what fails; report warnings.
- Author commits as Amish Chadha <amish@designmolecule.com> with a `Co-Authored-By: Claude` trailer. Commits must reach GitHub signed with Amish's key (Verified). Never rewrite history once a repository is public.
- Keep `CITATION.cff` (Amish first, ORCID 0009-0000-8079-7141), `CONTRIBUTORS.md` and the README Credits section in agreement. `CITATION.cff` names one license only (Zenodo rejects a list); the full license split lives in `REUSE.toml`.
- Keep the repo REUSE compliant: when you add a kind of file that `REUSE.toml` does not cover, add an annotation there and run `reuse lint` before committing (`.kit/STANDARDS.md` section 16).
- Zenodo and Software Heritage (`.kit/STANDARDS.md` section 17): prepare with `python .kit/archive.py reuse` and `python .kit/archive.py zenodo`. Switching a repo on in Zenodo, publishing releases and requesting archive saves are Amish's decisions. After Zenodo mints the DOIs, record the concept DOI with `python .kit/archive.py zenodo --doi <concept DOI>`.
- OpenRatio and BioMedical repos: soft, non-clinical wording only ("research and educational prototype, not a medical device").

