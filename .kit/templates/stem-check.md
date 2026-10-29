---
doc_id: PRJ-STM-001
title: Project STEM check
project: Project name
doc_type: STEM check
version: "0.1"
status: Draft
date: YYYY-MM-DD
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: YYYY-MM-DD
    author: Amish Chadha
    change: Initial draft
---

# Project STEM check

Verdict: lead with the result in one sentence (for example "All 14 claims sit within known science; 3 are plausible and confirmed by CAL-001 at TRL 3"). Method and rules: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py`.

## Claims checked

Table 1. Claims, governing science and verdicts.

| # | Claim (number and unit) | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | Example: frame stays below yield at 1.5 x the 20 t jack rating | Physics | Strength of materials | Beam bending, yield of S275 steel (EN 10025) | 212 MPa against 275 MPa | Within known science | CAL-001 Table 2 |

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails**.

## Fields not relevant

One line per field the concept does not touch, with the reason (for example "Biology: no living material, no exposure beyond the safety notes in PRC").

## Concept options

STEM verdict for each option in OPT, one line each; an option with a Fails row is marked and dropped.

## Independent review

What the second reviewer tried to refute, what it found and what changed.

## Sources

Every law, standard, datasheet or paper cited above.
