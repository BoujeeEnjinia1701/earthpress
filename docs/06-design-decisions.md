---
doc_id: EPR-DEC-001
title: EarthPress design decisions register
project: EarthPress
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Register opened with the open decisions from EPR-DDR-001 to EPR-DDR-003, the precis and the build work
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
---

# EarthPress design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, EPR-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Open decisions, Proposed, awaiting Amish.*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | R7 total mass: the buildable press is 200 kg against the 190 kg target (heaviest piece 45 kg against the 50 kg limit) | (a) Relax the total to 200 kg, keep the 50 kg piece limit; (b) lighten (16 mm lid plate with deeper ribs, 10 mm mold walls, lighter base plate), perhaps 10 kg, then re-check; (c) both | (a): the piece limit is what governs moving the press | None for (a); for (b), the lid, mold and base frame sketches | EPR-DDR-003, A1 |
| 2 | Rest catch release: the operator lifts the catch before each stroke | (a) Hand release, as modelled; (b) a foot pedal linked to the catch | (a) for the prototype; reconsider after timing cycles (R4) | The rest catch and its handle (build plan section 3.8) | EPR-DDR-003, A3 |
| 3 | First co-design partner and region | An earth-building NGO in East Africa or India were the TRL 2 examples | None yet | Soil for the first blocks; local steel sizes | EPR-DDR-001, item 8 |
| 4 | Bush material in dusty use | Case-hardened steel (as modelled), bronze or UHMW-PE | None yet; case-hardened steel until wear data exist | The bushes in the links and lugs | EPR-PRC-001, open questions |
| 5 | Mold wear liners | Plain 12 mm plate (as modelled) or hardened liners for 50,000 blocks of sandy soil | None yet; decide on wear data (R8) | The mold walls | EPR-PRC-001, open questions |
| 6 | Fill by volume once a soil is characterized | Weigh every fill (as now) or a calibrated scoop | None yet; keep weighing until partner soils are measured | The test kit and the operating procedure, not the press | EPR-PRC-001, open questions |
| 7 | Lime stabilization where cement is scarce, and whether the press needs a longer dwell for it | Cement only (as now), or lime as an option with its own chart | None yet | The test chart | EPR-PRC-001, open questions |
| 8 | Design soil for the force calculations: the peak pull ranges from 571 to 809 N over the assumed soil range | Keep the base soil (668 N); or design for the softer soil (809 N, 405 N each for two) | None yet; measure partner soils at TRL 4 | None in the press; the operating chart | EPR-PRC-001, open questions |

## To confirm when parts are bought

*Table 2. Items to confirm when parts are bought.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The UPN 80 channel's web (6 mm), flange (8 mm) and depth (45 mm) | The mold bolt holes, the pin access holes and the tie bolt holes are set from them; the column webs must be 196 apart | EPR-DDR-003, P2 |
| 2 | Bushes of 35 bore and 41 outside diameter are available locally | The link and lug bores are 41; another bush size changes the bore and the net section check | EPR-DDR-003, P5 |
| 3 | A tube with about 61.3 inside diameter for the two sockets | The 2 in schedule 40 lever (60.3) must slide in without much play | EPR-BLD-001, sections 3.7 and 3.9 |
| 4 | Two small torsion springs strong enough to snap the catch and the pawl in | They make the catch and the pawl self-acting | EPR-BLD-001, section 3.8 |
| 5 | Expanded metal openings of 12 mm or less | Keeps fingers out of the guard | EPR-BLD-001, section 3.10 |
| 6 | Local prices for steel, turned pins and bushes | The BOM prices are indicative; they set the estimated cost against the value-engineering target | EPR-CAL-001, section 11 |

## Value engineering

Value-engineering target: USD 500 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 520 (USD 20 over the target). Main cost drivers and savings worth trying:

- Steel is the main cost: 200 kg at about USD 1.30/kg is about USD 260. A lighter press (decision 1, option b: a 16 mm lid plate with deeper ribs, 10 mm mold walls, a lighter base plate, perhaps 10 kg) saves steel as well as mass.
- The parts added to make the press buildable (EPR-DDR-003) account for the rise from USD 488.
- Plain pins without bushes would save about USD 30, but R8 (wear) would fail, so this is a saving to weigh, not to take.
- Local prices for steel, turned pins and bushes are to be confirmed when parts are bought; every price is indicative.

## Decisions made

*Table 3. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 items 1 to 7 and 9: toggle and one lever (CINVA-Ram pattern), longer arc from a low pivot, 290 x 140 x 90 mm block, 2 MPa, 5 % cement, 12 mm base plate and bolted mold, field soil tests only, no pitch change | Amish: "i accept all your recommendations, go with them across all repos." | EPR-DDR-001, EPR-DDR-002 |
| 2026-09-25 | TRL 3 items 10 to 16: separate eject seesaw with a lost-motion slot, two operators on a T-handle, R5 reworded, R7 total 190 kg, budget $500, weighed fill, linkage geometry, crank stop, ribbed lid, end pawl, linkage guard, hardened bushes, R4 at 296 blocks a day | Amish, same instruction | EPR-DDR-001, EPR-DDR-002 |
| 2026-10-01 | Design for construction: columns turned, tapped mold flanges, pin access holes and spacers, round link ends, end skirts on the piston, lid pins in rib ears, rest catch and end pawl on the crank pin, central eject arm, ties moved, guard modelled, gauge made real (P1 to P15) | Made under Amish's 2026-09-30 instruction to make the design physically buildable ("fix the design assumptions to match and be physically feasible"); open for his review | EPR-DDR-003 |
