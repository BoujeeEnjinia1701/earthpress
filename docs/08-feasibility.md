---
doc_id: EPR-FEA-001
title: EarthPress feasibility assessment
project: EarthPress
doc_type: Feasibility assessment
version: "0.2"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First feasibility assessment (kit 1.8 pipeline) for option A after the kit 1.9.1 upgrade
- version: "0.2"
  date: '2026-10-30'
  author: Amish Chadha
  change: "R7 mass against the 205 kg total decided on 2026-10-30"
---

# EarthPress feasibility assessment

Feasible on paper: the lever and toggle press is calculated, drawn at detail level D3, priced and planned for a small welding shop, and its one structural shortfall (the toggle pins) is fixed; what remains uncertain is the soil, not the machine, and the press is 3.8 kg over its mass target and USD 42 over its cost target. Method: STANDARDS section 23.

Table 1. Feasibility by aspect (option A, the current design).

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design | The mechanism and every load-path member are calculated at the 173 kN design load (lowest factor 1.29); kinematics, grip heights and eject checked; the detailed model passes the D3 fidelity check with no interference | High | The soil compaction law is assumed (STM S6), so the peak pull and the fill window could shift; two operators are needed | EPR-STM-001, EPR-CAL-001, `cad/fidelity.json` |
| Materials | Mild steel plate, UPN 80, tube and pipe from a stockist; 42CrMo4 +QT pins and case-hardened bushes bought turned | High | 42CrMo4 bar and 40 x 46 mm bushes to confirm locally (EPR-DEC-001, to confirm item 2) | BOM lines 1 to 7 |
| Manufacturing and assembly | Sawing, cutting, drilling, tapping, stick welding and grinding; 14 components, 13 assembly steps with a picture each; no machining in the shop | High | Squareness of the mold cavity (ground within 0.5 mm) and the 420 mm connecting link centres need care | EPR-BLD-001, DWG-101 to DWG-115 |
| Power and controls | Human powered; no controls | High | Two people on the T-handle at up to 405 N each with the softer design soil | PR-005, PR-015 |
| Supply of parts | Common sections and fasteners; turned pins from a machine shop | Medium | Prices are indicative; the BOM is USD 542 against USD 500 | `bom/bom.csv`, EPR-CAL-001 section 11 |
| Mass and transport | 203.8 kg in pieces of 44.5 kg or less; fits a 1.5 m pickup bed without the lever | Medium | Within the 205 kg R7 total by 1.2 kg (decision D2, 2026-10-30) | EPR-CAL-001 section 8 |
| Blocks | 2 MPa is the low end of CSEB practice; strength depends on soil and curing | Medium | Block strength and wear can only be verified at TRL 4 (on hold) | STM S2, S18; PR-003, PR-008, PR-010 |

Ratings: High, Medium, Low.
