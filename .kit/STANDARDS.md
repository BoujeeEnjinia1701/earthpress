---
doc_id: OHP-STD-001
title: Documentation and drawing standard
project: Open Hardware Portfolio
doc_type: Standard
version: "1.8.1"
status: Released
date: 2026-10-23
author: Amish Chadha
license: CC-BY-SA-4.0
revisions:
  - version: "1.0"
    date: 2026-09-24
    author: Amish Chadha
    change: First release of the standard
  - version: "1.1"
    date: 2026-09-24
    author: Amish Chadha
    change: Adopt Technology Readiness Levels (section 9) for project maturity
  - version: "1.2"
    date: 2026-09-24
    author: Amish Chadha
    change: Portfolio phase cap (section 10), concept media standard (section 11), CLAUDE.md guardrails
  - version: "1.3"
    date: 2026-09-24
    author: Amish Chadha
    change: Scale figure, interactive 3D viewer and flow diagrams added to concept media; session slash commands
  - version: "1.4"
    date: 2026-09-26
    author: Amish Chadha
    change: Every sheet and render names the project and its GitHub repository; overall dimensions, ISO centre lines and 300 dpi PNG on sheets; titles name the device and view labels state the viewing direction; optional photoreal renders with Blender
  - version: "1.5"
    date: 2026-09-27
    author: Amish Chadha
    change: Product renders (section 12), storefront images and image quality check (section 13), public release and release gate (section 14), authorship, citation and commit signing (section 15)
  - version: "1.6"
    date: 2026-09-29
    author: Amish Chadha
    change: Licensing metadata with REUSE (section 16), Zenodo DOI and Software Heritage archiving (section 17), release gate checks REUSE and a single CITATION.cff license, archive.py
  - version: "1.7"
    date: 2026-09-30
    author: Amish Chadha
    change: Concept and constructable design states; design decisions register (DEC) kept apart from the build plan; prototype build plan (BLD, section 18) with pictures by component is required TRL 3 evidence; every repo targets TRL 3 during the populate phase; build_views.py; /to-trl3 and /build-plan commands
  - version: "1.8"
    date: 2026-10-23
    author: Amish Chadha
    change: "The pipeline: stages P0 to P6 beside TRL (section 19), STEM check (section 20), concept options (section 21), user and product requirements with a generated traceability matrix (section 22), regulatory, feasibility, risk, market and plan documents (section 23); trace.py, stem_check.py, options.py; render.py and the release gate check the pipeline deliverables"
  - version: "1.8.1"
    date: 2026-10-23
    author: Amish Chadha
    change: "STEM check fix rule (section 20): on Amish's standing instruction, a failed detail is fixed in the design in the same session and recorded in the decisions register; working principle, pitch or scope changes still go to Amish"
---

# Documentation and drawing standard

Every project in the portfolio uses this standard, so that each precis, write-up and sketch looks the same and carries its own version history. The standard ships as a kit in each repo's `.kit/` folder. The kit version is in `.kit/KIT_VERSION`.

## 1. Document types and IDs

Every controlled document has a unique ID in the form `PRJ-TYP-NNN`.

- `PRJ` is the three-letter project code listed in section 7.
- `TYP` is the document type code from the table below.
- `NNN` is a sequence number within that project and type, starting at 001.

| Code | Type | Typical file |
| --- | --- | --- |
| PRC | Design precis | `docs/02-concept.md` |
| PRB | Problem statement | `docs/01-problem.md` |
| REQ | Requirements (kit 1.7 and earlier; replaced by URS and PRS) | `docs/03-requirements.md` |
| STM | STEM check (section 20) | `docs/01b-stem-check.md` |
| OPT | Concept options (section 21) | `docs/02a-concept-options.md` |
| URS | User requirements (section 22) | `docs/03a-user-requirements.md` |
| PRS | Product requirements and specifications (section 22) | `docs/03-requirements.md` |
| RTM | Traceability matrix, generated (section 22) | `docs/03b-traceability.md` |
| REG | Regulatory and standards register (section 23) | `docs/07-regulatory.md` |
| FEA | Feasibility assessment (section 23) | `docs/08-feasibility.md` |
| RSK | Risk register, hazard analysis and design FMEA (section 23) | `docs/09-risk.md` |
| MKT | Market and viability (section 23) | `docs/10-market.md` |
| PLN | Project plan, resources and references (section 23) | `docs/11-plan.md` |
| MIN | Meeting minutes, optional (section 19) | `docs/minutes/YYYY-MM-DD.md` |
| CAL | Calculation or sizing note | `docs/04-calcs/*.md` |
| DDR | Design decision record | `docs/decisions/*.md` |
| BOM | Bill of materials | `bom/bom.csv` |
| DWG | Drawing or sketch sheet | `cad/drawings/*.svg` |
| BLD | Prototype build plan (section 18) | `docs/05-build-plan.md` |
| DEC | Design decisions register (section 18) | `docs/06-design-decisions.md` |
| TST | Test plan or test report (front matter adds `environment: lab` or `relevant`) | `docs/05-tests/*.md` |

Example: `TBK-PRC-001` is the ThermaBrick design precis.

## 2. Revision scheme

| Artifact | While in draft | When released | Change after release |
| --- | --- | --- | --- |
| Documents | 0.1, 0.2, 0.3 ... | 1.0 | 1.1 for minor edits, 2.0 for a design change |
| Drawings | Rev P1, P2 ... (preliminary) | Rev A | Rev B, C ... |

- Every change to a controlled document adds a row to its revision history before the commit.
- The `version` field in front matter always equals the newest row in `revisions`. The renderer rejects a document where they differ.
- Status is one of `Draft`, `In review`, `Released` or `Superseded`. Draft and In review documents print with a status band on every page.
- Every release is tagged in Git as `<doc_id>/v<version>`, for example `TBK-PRC-001/v1.0`. Drawings are tagged `TBK-DWG-001/revA`.
- Git history is the full audit trail. The in-document revision table is the human-readable summary.

## 3. Document front matter

Every Markdown document under version control starts with this block:

```yaml
---
doc_id: TBK-PRC-001
title: ThermaBrick design precis
project: ThermaBrick
doc_type: Precis
version: "0.1"
status: Draft
date: 2026-09-24
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: 2026-09-24
    author: Amish Chadha
    change: Initial draft
---
```

Quote version numbers so YAML keeps `1.0` as text instead of turning it into a number. List revisions newest last.

## 4. Writing style

- Chicago Manual of Style.
- No em dashes. Restructure the sentence instead.
- Lead each section with its conclusion, then support it.
- SI units throughout, in the form `12 kW`, `450 °C`, `3.2 m`. Imperial values may follow in parentheses.
- Number every figure and table ("Figure 2", "Table 1") and give each a caption.
- State every assumption in the calculation that depends on it.
- Put safety notes in a blockquote starting with **Safety:**.

## 5. Visual identity

| Element | Specification |
| --- | --- |
| Typeface | IBM Plex Sans for text, IBM Plex Mono for code and values (SIL Open Font License, bundled in `.kit/fonts`) |
| Ink | `#111827` |
| Secondary text | `#4B5563` |
| Rules and grid | `#D1D5DB` |
| Accent (one only) | `#0F766E` teal |
| Document page | US Letter, 20 mm margins |
| Drawing sheet | ANSI B landscape (431.8 x 279.4 mm) |
| Footer | Document ID, version, status, license and designmolecule.com on every page |

## 6. Drawing and sketch conventions

- Units are millimeters unless the title block says otherwise.
- Third-angle projection, marked with the symbol in the title block.
- Line weights: visible outlines 0.5 mm, hidden lines 0.25 mm dashed, center lines 0.18 mm chain.
- The title block contains the project, title, drawing number, revision, scale, units, projection, sheet, author, date, material or notes, and license.
- Every sheet and every render names the project and its GitHub repository (from `repo:` in `project.yaml`), at the top of the sheet and in the title block, so a printed or forwarded sheet is never anonymous.
- The drawing title names the device, not only the drawing type (for example "Handheld near-infrared resin scanner: general arrangement").
- Every view label states its scale and viewing direction (for example "Scale 1:1; side elevation looking along +Y"), and every isometric or render states where it is seen from.
- Orthographic views generated with `add_ortho` carry overall dimensions (length and depth on the top view, height on the front view) and ISO 128 centre lines on cylinders; hidden lines are dashed. Tolerances are not shown before TRL 4.
- Sheets are exported as SVG, PDF and a 300 dpi PNG.
- The revision table in the top right of the sheet lists every revision.
- Concept sketches use the same sheet and title block and carry the label "CONCEPT, NOT FOR FABRICATION".
- Geometry comes from `cad/src/*.py` (build123d). Sheets are generated by `.kit/drawing.py` and never edited by hand.

## 7. Project codes

| Code | Project | Code | Project | Code | Project |
| --- | --- | --- | --- | --- | --- |
| TBK | ThermaBrick | PCF | PicoFlow | HLT | HelioLite |
| CCB | CharCube | DRN | DustRunner | TRT | TremorTrace |
| STC | StepCue | FXH | FlexHand | CPD | ColdPod |
| SCL | SunClave | STR | SteamRoot | GGD | GrainGuard |
| SDL | SeedLine | ZBX | ZeerBox | RMS | RootMesh |
| DWD | DewDrive | SSK | StillStack | PPR | PotPress |
| WWT | WaterWatch | LMF | LumaFlow | FCL | FieldCell |
| CNP | ConePro | CVC | CulvertCrawl | EGD | EmberGuard |
| SNF | SnapFrame | CGM | CargoMule | SCM | StepClimber |
| SWC | SwapCell | PLP | PalletPilot | FTK | FlatTrike |
| WWK | WaterWalker | GRR | GrowRider | SSP | SunSpoke |
| SGN | StepGen | PBX | PowerBox | WML | WasteWise-ml |
| WSC | WasteWise Scan | RFE | ReflowEconomy | | |
| OHP | Portfolio-wide | | | | |

## 8. Build and publish

- `python .kit/render.py` checks every controlled document and renders it to `docs/pdf/<doc_id>_v<version>.pdf`.
- `python .kit/drawing.py` (called from each project's `cad/src/sheets.py`) builds drawing sheets as SVG and PDF in `cad/drawings/`.
- The GitHub Action in `.github/workflows/docs.yml` runs the checks on every push and attaches PDFs to a GitHub Release whenever a release tag is pushed.
- Public releases follow section 14: `python .kit/release_gate.py` must pass, and the release tag is `v0.<TRL>.0` (for example `v0.3.0` at TRL 3).

## 9. Technology Readiness Level (TRL)

Each project states its maturity as a Technology Readiness Level on the NASA and US DOE 1 to 9 scale. The TRL rates this specific design, not the underlying technology. A sand battery is commercial elsewhere, but a new sand battery design starts at TRL 2 until evidence shows otherwise.

| TRL | Definition | Evidence the repo must contain |
| --- | --- | --- |
| 1 | Basic principles observed | Problem statement (PRB) |
| 2 | Technology concept formulated | Draft precis (PRC), user and product requirements (URS, PRS; REQ before kit 1.8), STEM check (STM) with no failed claim, at least two concept options (OPT); pipeline stage P1 or later |
| 3 | Analytical or experimental proof of concept | Calculation note (CAL), working build123d model with STEP export, drawing sheet (DWG), priced BOM with every unit cost filled in, prototype build plan (BLD) with pictures, `design_state: constructable`, STEM check passed, generated traceability matrix (RTM), and the regulatory, feasibility, risk (with design FMEA), market and plan documents; pipeline stage P3 |
| 4 | Components validated in the lab | Test report (TST) with `environment: lab`, build log entries |
| 5 | Validated in a relevant environment | Test report (TST) with `environment: relevant` |
| 6 | System prototype demonstrated in a relevant environment | Precis at version 1.0 or later with status Released, a drawing at a lettered revision (Rev A or later), and a system-level TST with `environment: relevant` |
| 7 to 9 | Operational demonstration through proven in service | Beyond portfolio scope; claim only with a named deployment partner and evidence |

Rules:

- `project.yaml` records `trl` (current level), `trl_target` (the level the current effort aims for) and `trl_evidence` (the files that support the claim).
- `python .kit/render.py --check` fails if the evidence for the claimed TRL is missing. CI runs this check on every push.
- Documentation alone cannot go past TRL 3. TRL 4 and above require hardware and a test report.
- TRL and visibility are independent. A repo can be public at TRL 3 as a documented design ready to build.
- A change of TRL is recorded in the build log with the date and the evidence that justified it.

## 10. Portfolio phase and TRL cap

`.kit/PHASE.yaml` sets the current phase. During the **populate** phase every repo is capped at **TRL 3**: `trl` and `trl_target` may not exceed 3, and the check fails if they do. Every repo targets the cap: `trl_target` must equal 3, so a new repo is taken all the way to TRL 3 (scaffold, populate and advance, see `/to-trl3`). Work that belongs to TRL 4 or later (building or testing hardware, test articles, test plans and reports, build-log entries, purchasing lists, PCB layouts) must not be started. The prototype build plan (BLD, section 18) is TRL 3 paper work and is required. Where it already exists it is kept, flagged in the check output, and not extended. Only Amish changes `PHASE.yaml`.

Every repo carries a `CLAUDE.md` with the working rules for AI sessions: the TRL cap, decision rights (nothing is recorded as decided unless Amish decided it), one step per session, and a mandatory `docs/REVIEW.md` before stopping.

## 11. Concept media

Every repo at TRL 2 or above explains its idea visually. Media are generated from a build123d massing model with `.kit/concept.py`, never drawn by hand, so they stay in step with the design.

| File | Required | Purpose |
| --- | --- | --- |
| `media/hero.png` | TRL 2+ | Shaded isometric render with a 1.75 m person for scale; the website card image |
| `media/concept-blueprint.png` and `.pdf` | TRL 2+ | Blueprint concept sheet: orthographic and isometric views, scale, key figures, title block |
| `media/model.glb` and `media/viewer.html` | TRL 2+ | Interactive 3D viewer (glTF plus model-viewer) for the website |
| `media/cutaway.png` | When the inside matters | Section view showing internal parts |
| `media/exploded.png` | Recommended | Exploded view with numbered callouts matching the BOM |
| `media/flow.png` | When energy or material moves | System, energy or material flow diagram with losses |

Session commands in `.claude/commands/` (`/populate`, `/advance-trl3`, `/rein-in`, `/refresh-media`) carry the standard prompts, so every Claude Code session starts from the same instructions.

At TRL 2 a massing model is enough: correct overall proportions and main components. All concept media carry "CONCEPT, NOT FOR FABRICATION". The check warns when required media are missing at TRL 2 and fails at TRL 3.

## 12. Product renders

Every repo at TRL 3 shows the product as it would look, not only as a massing model.

- `cad/src/product_model.py` is the appearance model. It defines `product_parts()` (named parts with a shape and a material), `TITLE` ("Name: what it is") and `RENDER_VIEWS`. It is for renders only: every main dimension comes from `cad/src/model.py`, never typed in again.
- Where the appearance model departs from `model.py` (a chamfer, a label, a fastener drawn for realism), record the deviation in `docs/REVIEW.md` as "Proposed, awaiting Amish".
- Scale comes from context, not from a floating figure: a hand or forearm for handheld objects, and the posed mannequin (`mannequin()` in `.kit/context_parts.py`: stand, walk, push, ride, sit, reach) for anything a person uses at body scale.
- Renders are made with `.kit/export_views.py` (one scene per view) and `.kit/photoreal.py` (Blender Cycles), then captioned with `.kit/photo_caption.py`. Files are `media/render-<view>.png`; `media/render-hero.png` is required.
- Every caption names the project, the repository and the viewing direction, and carries "CONCEPT, NOT FOR FABRICATION".
- Captions never sit on the render. `.kit/photo_caption.py` adds a header band (title, concept label, repository) above the render and a footer band (view note) below it, wraps every line to the image width, and steps the font down to a floor before adding a line.
- The README opens with `media/render-hero.png`.
- Software-only and scene repositories (no single product) may use a scene render as the hero instead of a product model.

## 13. Storefront images

Two images, both made from `media/render-hero.png` by `python .kit/cards.py .`:

| File | Size | Purpose |
| --- | --- | --- |
| `media/card.png` | 800 x 800 | Square thumbnail for the organization profile page |
| `media/social-preview.png` | 1280 x 640, under 1 MB | GitHub social preview, shown when a repository link is shared |

- The social preview shows the area, name, one-line description, the first sentence of the pitch, the brand line and the repository address. Design Molecule repos read "Design Molecule · open hardware concept, TRL n"; OpenRatio repos read "OpenRatio · research and educational prototype, TRL n".
- GitHub has no API for the social preview. Upload it under the repository's Settings, Social preview, on release day.
- Regenerate both images whenever `render-hero.png` changes.

### Image quality

Every render, card and social preview must be clear and readable. `python .kit/image_qc.py` checks each one, and the release gate blocks on any failure:

| Check | Rule |
| --- | --- |
| Layout | Made by the current `photo_caption.py` or `cards.py`, which store the text layout in the PNG |
| Text inside the image | Every line at least 1.2 % of the image width from each edge; nothing runs off the side |
| No overlap | No line of text touches another line, and no caption text sits on the render |
| Text size | Render captions at least 1.05 % of the image width in pixel height (17 px at 1600 px); social preview text at least 16 px |
| Resolution | Renders at least 1200 px wide; card 800 x 800; social preview 1280 x 640 and under 1 MB |
| Sharpness | The render is not blurred or upscaled (edge sharpness at least 15 on the `image_qc.py` scale) |

Long titles and notes wrap to more lines rather than shrinking below the floor. The social preview shortens the pitch sentence with an ellipsis only if it cannot fit at the smallest size.

## 14. Public release

A repository goes public only when Amish approves it, and only after `python .kit/release_gate.py` passes. The gate checks:

1. `render.py --check` passes (document control, TRL cap, concept media).
2. Storefront: hero render, card, social preview under 1 MB, README leading with the hero, and every image passing the image quality check (section 13).
3. Issue templates in `.github/ISSUE_TEMPLATE/`: question, build report, design suggestion. The build report template restates that the design is a TRL 3 concept, not released for fabrication (OpenRatio: a research and educational prototype, not a medical device).
4. `CITATION.cff` valid, with an author ORCID.
5. License files match `project.yaml`.
6. No em dashes in the repository's own text.
7. BioMedical and OpenRatio repos use soft, non-clinical wording: "research and educational prototype, not a medical device".
8. No secrets anywhere in the history (gitleaks).
9. No links to sibling repositories that are still private.
10. REUSE files present (`REUSE.toml`, `LICENSES/`, `.github/workflows/reuse.yml`) and `reuse lint` passes (section 16).
11. `CITATION.cff` names exactly one license, because Zenodo rejects a list (section 17).

It warns, without blocking, when the README lacks a Safety heading or a "not for fabrication" statement, when `CITATION.cff` has no DOI yet, and when the README lacks the Zenodo DOI, REUSE or Software Heritage badge, so a person can confirm.

On release day, per repository:

- A signed, annotated tag `v0.<TRL>.0` on `main`.
- A GitHub release with short notes (what it is, TRL, status, licenses, how to cite) and a design pack, `<repo>-v0.<TRL>.0-design-pack.zip`, holding `cad/step`, `cad/drawings`, `docs/pdf`, `bom`, README, licenses and `CITATION.cff`.
- Description from the first sentences of `pitch` (350 characters at most), website `https://designmolecule.com` (OpenRatio: `https://openratio.ai`), topics from `project.yaml`.
- Before the first release, the repository is switched on in Zenodo (section 17), so the release is archived and gets a DOI.
- Visibility switched to public last, after the release exists.
- The social preview uploaded and the organization profile updated with the new cards.
- After the release: the concept DOI written to `CITATION.cff` and a Software Heritage save requested (section 17).

The internal working files (`CLAUDE.md`, `.kit/CLAUDE.md`, `.claude/commands/`, `docs/REVIEW.md`) stay public, and open "Proposed, awaiting Amish" items stay visible as open questions (Amish, 2026-09-27).

## 15. Authorship, citation and signing

- Amish Chadha is the author of every design, ORCID 0009-0000-8079-7141. Commits are authored as Amish Chadha <amish@designmolecule.com>.
- `CITATION.cff` lists Amish (with ORCID) first, then any credited contributors; `CONTRIBUTORS.md` and the README Credits section agree with it.
- `CITATION.cff` names one license: the hardware license (CERN-OHL-S-2.0), or the software license in a software-only repository. The full split between hardware and software licenses lives in `REUSE.toml` and the README. Once the repository is archived, `CITATION.cff` carries the concept DOI in `doi:`.
- Work done with Claude carries the trailer `Co-Authored-By: Claude <noreply@anthropic.com>` (with the model name), and the README Credits section says designs are developed with AI assistance.
- Every commit and tag pushed to GitHub is signed with Amish's SSH signing key, so GitHub shows it as Verified. Commits prepared elsewhere are re-signed on Amish's Mac before they are pushed.
- Once a repository is public, its history is never rewritten.

## 16. Licensing metadata (REUSE)

Every file states its copyright and license in a machine-readable way, following the REUSE Specification 3.3 (https://reuse.software). A repository is set up with:

```
python .kit/archive.py reuse
```

This writes three things and adds the REUSE and Software Heritage badges to the README badge line:

- `REUSE.toml`, built from the licenses in `project.yaml`. Everything is under the hardware license by default. Scripts, firmware, notebooks, web viewers, workflows and agent commands are under the software license. `cad/` and `electronics/` stay under the hardware license even where they are written as Python. The bundled IBM Plex fonts are OFL-1.1 (IBM Corp.). Copyright is "<first commit year> Amish Chadha".
- `LICENSES/`, with the full text of each license used (`reuse download`). The root `LICENSE` and `LICENSE-SOFTWARE` files stay for GitHub's license detection.
- `.github/workflows/reuse.yml`, which runs the REUSE check (fsfe/reuse-action) on every push and drives the README badge.

A new kind of file that falls outside these rules gets a new annotation in `REUSE.toml` rather than a header comment. `reuse lint` must pass before every commit that adds files, and the release gate enforces it.

## 17. Archiving and DOI (Zenodo and Software Heritage)

Every public repository is archived twice, so the design stays citable and retrievable if GitHub changes.

Zenodo (a citable DOI for each release):

1. Amish's Zenodo account is linked to GitHub. Before the first release, Amish switches the repository on in Zenodo (Account, GitHub). Only Amish changes Zenodo or GitHub settings.
2. Run `python .kit/archive.py zenodo`: it makes sure `CITATION.cff` names one license and adds the Zenodo DOI badge, which uses the GitHub repository ID and always points at the latest version. Zenodo reads its metadata (title, authors with ORCID, license, keywords) from `CITATION.cff`, and rejects the whole archive when that file lists several licenses.
3. Publish the GitHub release (section 14). Zenodo archives it within minutes and mints two DOIs: a version DOI for that release and a concept DOI that stands for all versions.
4. Check the Zenodo record: title, author and ORCID, license, keywords. If Zenodo shows "Citation metadata load failed", fix `CITATION.cff`, validate it with cffconvert and publish a new patch release (for example `v0.3.2`); a failed release is never re-used.
5. Run `python .kit/archive.py zenodo --doi <concept DOI>` and commit, so GitHub's "Cite this repository" and every future archive carry the concept DOI. Every later release gets its own version DOI automatically; the concept DOI never changes.

Software Heritage (permanent source archive):

1. After the repository is public, request a save at https://archive.softwareheritage.org/save/ (origin type git, the repository URL). Anonymous requests are limited to about ten an hour, so batches are spread out.
2. The Software Heritage badge on the README resolves once the save is accepted and ingested. Later pushes are picked up by its regular crawl.

OpenRatio repositories follow the same steps when Amish approves their release.

## 18. Prototype build plan (BLD) and the constructable design

### Two design states

A design moves through two states, recorded as `design_state` in `project.yaml`:

- **Concept**: the design shows what the product does and that it works on paper (TRL 2 and the calculations of TRL 3). Parts may be simplified shapes that have never been checked for how they are made or how they join.
- **Constructable**: every part can be made with the stated process and material, and every part fits and fastens to the parts next to it. Nothing is left as a shape that cannot be cut, cast, bent, printed, machined or bought.

A repo reaches TRL 3 only when its design is constructable and its build plan shows how. Writing the build plan is how the design is made constructable: when a part cannot be made or cannot fit as modelled, change the model so it can (Amish, 2026-09-30: "fix the design assumptions to match and be physically feasible"), keep what the concept does, and record every change in a decision record "Design for construction" (DDR) and in the plan. Changes that alter what the product does, its pitch or its safety case are proposed, not made.

### What the build plan is

`docs/05-build-plan.md` (`PRJ-BLD-001`) tells a capable maker how to build the first proof-of-concept prototype, in order, component by component, and shows it in pictures. It is written before anything is built, states "Plan, not yet built" under the title and never claims results. Building and testing to it is TRL 4 work.

### Writing rules

- **Plain English.** Say "the steel plate the jack stands on", not a model parameter or variable name. No code identifiers, function names, parameter names or file paths in the body of the plan. Give sizes as numbers with units ("a 62 mm hole, centred 100 mm up from the bottom edge"). The only place file names appear is the closing "Where the numbers come from" list.
- **Pictures first.** Every component and every assembly step has a picture. A reader should be able to build from the pictures, with the words explaining what the pictures cannot show (order, force, tolerance, checks).
- **By component, in build order.** Each component is made and checked before the step that needs it.
- **Cost is not the focus.** One line in the overview may state the parts cost from the BOM; there is no cost or time section.

### Sections, in order

1. **What you are building**: the overview picture (every component pulled apart and numbered in build order) and one short paragraph.
2. **What changed to make it buildable**: a table of each change from the concept (what the concept had, what the constructable design has, why), with a picture where the change is visible. "None" if nothing changed.
3. **Making the components**: one subsection per made component, in build order, each with:
   - its making sketch (three views with overall sizes, a 3D view, where it goes, making notes), `cad/drawings/PRJ-DWG-1NN`;
   - what it is and what it is made from (material, stock size);
   - how to make it, as numbered steps (mark out, cut, drill, bend, weld, cast, print, machine, finish), with the sizes that matter;
   - how it fits the parts next to it: a close-up picture of the joint, which faces touch, what holds them (bolt, weld, pin, clip, glue), the gap or fit needed, and which side goes where;
   - the check before moving on.
   Bought components get a short subsection: what to buy (specification, not brand), and what to do to it (drill, trim, fit).
4. **Putting it together**: numbered assembly steps, each with a step picture (parts already fitted in grey, the part being fitted in colour with an arrow showing the way it goes in), the fasteners, and any hold point.
5. **First checks**: fit, movement, first power or first load, each tied to a requirement ID with a pass criterion. The plan lists them; a TRL 4 test report records them.
6. **Safety stops**: points where work stops (before energising, pressurising, loading, lifting or operating) and what must be true to carry on.
7. **Tools, skills and workspace.**
8. **Where the numbers come from**: the model, drawings, calculation note and BOM, by file name.

### Budgets are value-engineering targets

`budget_usd` in `project.yaml` is a hypothetical control target that keeps the design thinking along a value-engineering lens; it is not a spending limit (Amish, 2026-10-01: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y"). Write it that way everywhere: "Value-engineering target: USD X. Estimated cost of the constructable design: USD Y (USD Z over or under the target)." A cost requirement is reported against the target ("over the value-engineering target by USD Z"), never as a failure that needs a budget decision, and the design decisions register does not carry "raise the budget" decisions. Instead the register has a short **Value engineering** section: target, estimated cost, the main cost drivers and the savings worth trying.

### Decisions live in their own document

The build plan describes the design as it stands; it never lists outstanding decisions, open questions or items awaiting Amish (Amish, 2026-09-30: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such"). Those go in the **design decisions register**, `docs/06-design-decisions.md` (`PRJ-DEC-001`), which has two tables: open decisions (what is to be decided, options, recommendation, what it affects in the build, source record) and decisions made (date, decision, Amish's words where recorded, link to the decision record). Things to confirm when parts are bought (for example a panel's frame lip) are open items in the register too. The build plan may say "see the design decisions register" once, in its introduction.

### Pictures

Pictures are generated from the model by `cad/src/build_plan_media.py` using `.kit/build_views.py` (overview, component making sketches, joint close-ups, assembly steps), so they always match the model. They are written to `docs/05-build-plan/` and `cad/drawings/`. Look at every picture before committing: labels readable, nothing overlapping, the part in question clearly visible.

`render.py --check` at TRL 3 requires a BLD document, `design_state: constructable` in `project.yaml`, and `docs/05-build-plan/overview.png`.

## 19. The pipeline: stages and deliverables

Every project moves through the pipeline, seven stages that sit beside the TRL scale. `project.yaml` records `stage` (P0 to P6); `.kit/PHASE.yaml` caps it with `stage_cap`, set by Amish (P3 while the TRL cap is 3). A stage is reached when its deliverables exist and are not placeholders; each stage also updates the documents of the stages before it.

| Stage | Name | TRL | Deliverables added |
| --- | --- | --- | --- |
| P0 | Proposal | 1 to 2 | Problem statement with user-needs and stakeholder tables (PRB), STEM check (STM), concept options (OPT), first pass of the regulatory register (REG), feasibility (FEA) and project plan (PLN) |
| P1 | Definition | 2 | User requirements (URS), product requirements draft (PRS), risk register with preliminary hazard analysis (RSK), market and viability (MKT), regulatory register complete |
| P2 | Design inputs | 2 to 3 | Product requirements with targets, tolerances and verification (PRS), calculation note (CAL), traceability matrix (RTM), concept selection decision record (DDR), STEM check closed, feasibility closed |
| P3 | Design outputs | 3 | Model, STEP, drawings (DWG), priced BOM, build plan (BLD), decisions register (DEC), first-pass design FMEA in RSK, traceability complete |
| P4 | Verification | 4 to 5 | Test plans and lab test reports (TST), verification report, reliability plan, RSK updated from results |
| P5 | Validation | 5 to 6 | Validation and human factors reports (TST, `environment: relevant`), field trials with a partner, certification status in REG |
| P6 | Commercialization | 7 to 9 | Launch plan, instructions for use, operator training, standard cost estimate; only with a named deployment partner |

Rules:

- `stage` may not exceed `stage_cap`; `render.py --check` fails if it does.
- A repo at TRL 2 is at least P1; a repo at TRL 3 is P3. The check fails if `stage` and `trl` disagree.
- Deliverables of P4 to P6 are not started while the cap is P3. They may appear in PLN as planned work, marked on hold.
- Meeting minutes (MIN, `docs/minutes/YYYY-MM-DD.md`) are optional: used when people beyond Amish join a project (date, attendees, agenda, notes, decisions, actions with owners).

## 20. STEM check (STM)

Every idea and every concept option passes a written STEM check before it can be called TRL 2: a test that what is envisaged sits within known physics, chemistry and biology, across all their branches, with the mathematics and engineering done correctly. The check exists to stop wonky science reaching a drawing.

**File:** `docs/01b-stem-check.md` (`PRJ-STM-001`), calculations in `docs/04-calcs/stem_check.py` using `.kit/stem_check.py`.

**Fields and branches.** One row per claim the design makes, tagged with its field and branch:

| Field | Branches |
| --- | --- |
| Physics | Mechanics and statics, strength of materials, thermodynamics, heat transfer, fluid mechanics, electromagnetism and circuits, optics and radiation, acoustics and vibration, nuclear and ionising radiation |
| Chemistry | Inorganic, organic, physical (kinetics, equilibria, thermochemistry), electrochemistry and batteries, materials and polymer chemistry, analytical, environmental and atmospheric chemistry |
| Biology | Microbiology, human physiology and biomechanics, ergonomics, ecology and agronomy, plant and animal biology, toxicology, epidemiology, biochemistry |
| Mathematics | Units and dimensional analysis, orders of magnitude, statistics and uncertainty, numerical method |
| Engineering and technology | Power and link budgets, control, sensing resolution, manufacturing tolerances, standards practice |

**Method.**

1. List every physical, chemical or biological claim, with its number and unit, field and branch.
2. Tie each claim to its governing law or a cited source (textbook, standard, datasheet or peer-reviewed paper).
3. Do the first-order calculation in `docs/04-calcs/stem_check.py`, so the check reruns when the design changes. Typical checks: energy and mass balance, efficiency against its theoretical limit (Carnot, Betz, Shockley-Queisser, pump curves), stress against yield with a safety factor, suction lift, heat flow, reaction stoichiometry and dose, battery life from a power budget, an order-of-magnitude estimate within a factor of about 3.
4. Give each row a verdict: **Within known science**; **Plausible, to confirm at TRL 3** (naming the CAL item that will confirm it); **Fails, fix proposed** (a detail fails, and a fix that keeps the working principle exists; see the fix rule below); or **Fails** (the working principle itself does not hold).
5. An independent reviewer pass (a second agent that does not see the author's reasoning) tries to refute every "Within known science" verdict; its findings are recorded in the document.

**Fix rule (Amish, 2026-10-23).** When a row fails, Claude proposes the best fix for the design and its constructability and implements it in the same session: model, drawings, calculations, BOM, build plan and requirements. The fix is recorded in the design decisions register as decided under Amish's standing instruction of 2026-10-23, with the options weighed and the cost, and Amish can reverse it. The STEM check is then rerun and the row is closed by the fix (verdict **Within known science**, "Closed by" naming the decision). Two exceptions go to Amish as decisions instead: a fix that changes the working principle, the pitch or the user-facing scope, and a row that is **Fails** outright (the concept goes back to concept options, section 21).

**Pass rule.** No row may be **Fails**: a concept whose working principle fails is dropped. A **Fails, fix proposed** row keeps the check open until its fix is implemented under the fix rule, or decided by Amish where the fix rule sends it to him. Every field the concept touches has at least one row; a field marked not relevant says why in one line. Every **Plausible** row is closed by a CAL result before TRL 3. `project.yaml` records `stem_check: pass`, `open` or `fail`. `render.py --check` fails at TRL 2 or above if STM is missing or `stem_check` is `fail`. The release gate fails unless `stem_check` is `pass`, so an open item (a Plausible row not yet closed, or a Fails, fix proposed row not yet fixed) blocks any release until it is closed. A repo already at TRL 3 when its first STEM check finds an open item (the kit 1.8 upgrade) keeps its TRL and applies the fix rule to the items. Health and biology claims use soft, non-clinical wording.

## 21. Concept options (OPT)

Every idea gets at least two genuinely different design concepts, three where a clearly different working principle exists, scored against the same user requirements before one is carried forward. A variant that only changes size or material does not count.

**File:** `docs/02a-concept-options.md` (`PRJ-OPT-001`); option models in `cad/src/options.py`, drawn side by side at one scale by `.kit/options.py` into `media/options.png`.

Each option records: name and one-line working principle; a massing render at the shared scale; first-order numbers (cost, mass, output or throughput, energy, parts count); its own STEM check rows (an option that fails is shown, marked and dropped); key risks; what it needs from a co-design partner.

**Scoring.** A weighted table: criteria are the user requirements (High weighs 3, Medium 2, Low 1) plus cost against the value-engineering target, buildability with local skills, safety and maintenance. Each option scores 1 to 5 per criterion with a one-line reason. The table shows weighted totals, the recommended option, and the runner-up's best idea to graft onto it.

**Choice.** The selection is a decision for Amish: recorded as "Proposed, awaiting Amish" in the decisions register (DEC) and argued in a concept selection decision record (DDR). If two options score within 10 %, both go to Amish without a pick. The chosen option is what PRC describes.

**Existing designs.** In a repo designed before kit 1.8, the current design is option A. If another option outscores it, that goes to Amish as a decision; the repo is not redesigned without his go.

`project.yaml` records `concept_options` (each option's name) and `concept_chosen`. `render.py --check` fails at TRL 2 or above if OPT is missing or lists fewer than two options.

## 22. Requirements and traceability (URS, PRS, RTM)

Requirements are split into what users need and what the design must do, and every product requirement traces to a user need and to its evidence.

**User requirements** (`docs/03a-user-requirements.md`, `PRJ-URS-001`): one table with ID (UR-001 and on), category (deployment and assembly, performance, usability, safety, environment and durability, logistics, maintenance, cost, regulatory), title, need written from the user's side, priority (High, Medium, Low) and source (the user type or stakeholder in PRB).

**Product requirements and specifications** (`docs/03-requirements.md`, `PRJ-PRS-001`, which replaces REQ): one table with ID (PR-001 and on), traces to (UR IDs), category, title, requirement (a "shall" statement), target, tolerance, units, verification (analysis, inspection, demonstration or test, and the TRL at which it happens), status (met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4) and, for repos migrated from REQ, the old R number in a "Was" column. Targets remain proposals for review with a co-design partner.

**Traceability matrix** (`docs/03b-traceability.md`, `PRJ-RTM-001`): generated by `python .kit/trace.py`, never typed by hand. It reads URS, PRS, the CAL results, the BOM and the build plan and lists UR to PR to evidence (CAL, DWG, BOM line or BLD step) to verification. It flags a High UR with no PR, a PR with no UR, a PR with no evidence and a PR with no verification. `render.py --check` fails at TRL 3 if the matrix is missing or out of date, or if a High UR has no PR.

## 23. Regulatory, feasibility, risk, market and plan documents

| Code | File | Content |
| --- | --- | --- |
| REG | `docs/07-regulatory.md` | Regulatory and standards register: standard or regulation, jurisdiction, applicability, owner (role), status (to assess, applies, does not apply, met by design, certification needed later). Standards shared across a focus area are researched once and cited in each repo. Health projects: soft, non-clinical wording, and any device classification is "to assess" with a regulatory consultant. |
| FEA | `docs/08-feasibility.md` | Feasibility assessment: aspect (design, materials, manufacturing and assembly, power, controls, supply), assessment, rating (High, Medium, Low), risks and notes, with links to STM and CAL. |
| RSK | `docs/09-risk.md` | Project risk register (risk, cause, effect, likelihood and impact 1 to 5, owner role, response); preliminary hazard analysis (hazard, cause, harm, severity, likelihood, control, residual); from P3 a first-pass design FMEA (item, function, failure mode, effect, cause, severity, occurrence, detection, RPN, action). |
| MKT | `docs/10-market.md` | Market and viability: segment, target users and region, competitive benchmark with cited price, estimated cost per unit (from the BOM), value proposition, and the open, non-commercial route (who would build it and how it spreads). Prices and benchmarks are cited with a date. |
| PLN | `docs/11-plan.md` | Project plan: workstreams with owner role, resources needed (role, deliverable, effort, cost), stage gates and dates, next steps and decision request, and the reference list of every source cited in the repo's documents. |

`render.py --check` requires REG, FEA and PLN from P0, RSK and MKT from P1, and the design FMEA in RSK at P3.

## 24. CAD fidelity at every TRL (kit 1.9)

Amish, 2026-10-24: "I want detailed TRL3 CAD - and in fact want to ensure the CAD is detailed across all TRLs." The model is detailed from the first concept, not a massing block that is detailed later, and every concept option is modelled to the repo's level (Amish, 2026-10-24: "Detail every option").

**Model interface.** `cad/src/model.py` defines `PARAMS` (every main dimension; the calculations read it), `OPTIONS` (key to name), `PRINCIPLES` (key to one-line working principle), `CHOSEN` (the option carried to the drawing, BOM and build plan), optional `OPTION_VIEWS` (key to render elevation, azimuth and scale) and `ALLOWED_CONTACTS`, and `components(option)`, which returns a list of `cad_parts.part()` dicts. Every part has a name, a solid, a material from `cad_parts.MATERIALS` and a kind: made, bought, fastener, weld or context.

**Parts library.** `.kit/cad_parts.py` supplies real stock (rectangular, square and round hollow sections, angle, channel, flat and round bar, sheet with holes, folded sheet, mesh), ISO fasteners (ISO 4017 bolts, ISO 4032 nuts, ISO 7089 washers, `hex_bolt_set` for a bolted joint, coach screws, anchors, ISO 2341 clevis pins and split pins), fillet weld beads, hinges, bushes, pulleys, a 200 L drum, rope, hand wheels and levers, and `break_edges()` for the radius or chamfer a real part has. Use it rather than bare boxes and cylinders.

**Detail levels.**

| Level | Stage | What the model must have | Checked by `cad_check.py` |
| --- | --- | --- | --- |
| D1 Recognisable | P0 (TRL 1) | Every visible part its own solid; real stock sections; moving parts at their real pivots; bought parts at catalogue envelope; broken edges; a material per part | At least 8 parts per option; no more than 50 % of made or bought parts are bare boxes or cylinders; every part has a material |
| D2 Engineered | P1 and P2 (TRL 2) | D1 plus dimensions from `PARAMS`; hole patterns; every bolt, nut, washer, pin and screw; welds as beads; hinges, pins and bushes; mass per part; no interference | At least 15 parts; bare share at most 25 %; fasteners present; no two parts overlap by more than 5 mm3 unless listed in `ALLOWED_CONTACTS` |
| D3 Constructable | P3 (TRL 3) | D2 plus every made part drawable on its own; fits and clearances checked; the assembly sequence the build plan follows; STEP per made or bought part of the chosen option, and an assembly STEP per option | At least 20 parts; bare share at most 15 %; per-part STEP files in `cad/step/<chosen>/` and `cad/step/<option>-assembly.step` for every option (fasteners and welds appear in the assemblies only); every made or bought part of the chosen option has a BOM line that exists in `bom/bom.csv` |

`project.yaml` may set `cad_level` to raise the level above the stage's; it can never lower it. At TRL 3 every option's geometry reaches D3; the drawing, priced BOM and build plan describe the chosen option only.

**Running the check.** `python .kit/cad_check.py --export` checks every option, writes the STEP files and stores the result (export tessellations for the web viewer and STL use a 0.1 to 0.2 mm chord error, so no file nears GitHub's 50 MB warning) with a hash of the CAD sources in `cad/fidelity.json`. `render.py --check` fails at kit 1.9 when that file is missing, stale, checked at too low a level, or failed.

**Renders.** From D1 every picture of the product is a Blender Cycles render (`.kit/photoreal.py`), not a shaded matplotlib view: the options picture (`python .kit/options.py` renders `components()` of every option), the product renders and the hero. Materials come from `cad_parts.MATERIALS` and render as physically based materials (painted steel with edge wear, galvanised and stainless steel, aluminium, HDPE, EPDM, timber, plywood, bamboo, coir, rope, concrete, mirror, water). Site renders use `--scene=outdoor` with a physical sky and sun and a procedural ground (`--ground=mud`, `concrete`, `roof`, `sand`, `soil`, `grass`, `workshop`) and optional still water (`--water=<mm>`); the product model supplies any site structure (a headwall, a roof parapet) as context parts. The blueprint sheet and the 3D viewer stay as they are.
