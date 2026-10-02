---
doc_id: EPR-DEC-001
title: EarthPress design decisions register
project: EarthPress
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
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
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Amish approved the recommendations for open decisions 1 to 8 (2026-10-02); moved to decisions made (EPR-DDR-003 A1 and A3 accepted)"
---

# EarthPress design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, EPR-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

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

- Steel is the main cost: 200 kg at about USD 1.30/kg is about USD 260. A lighter press (a 16 mm lid plate with deeper ribs, 10 mm mold walls, a lighter base plate, perhaps 10 kg) would save steel as well as mass; it was option (b) of the R7 mass decision, not taken on 2026-10-02, so it stays a saving worth trying.
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
| 2026-10-02 | R7 total mass: option (a). The R7 total is 200 kg, defined to include the guard and bolts, and the 50 kg piece limit is kept (heaviest piece 45 kg) | Amish: "i approve your recommendations for all 555 open decisions." | EPR-DDR-003, A1 |
| 2026-10-02 | Rest catch release: option (a), hand release, for the prototype, with the build plan rule that the catch is in before the latch is opened; a foot pedal is considered only if timed cycles (R4) show the extra step costs output | Amish: "i approve your recommendations for all 555 open decisions." | EPR-DDR-003, A3 |
| 2026-10-02 | First co-design partner: one that already trains builders in stabilized earth blocks and has local soils and cement supply. First candidate to approach: the Auroville Earth Institute in India, whose 290 x 140 x 90 mm block module the press uses | Amish: "i approve your recommendations for all 555 open decisions." | EPR-DDR-001, item 8 |
| 2026-10-02 | Bushes: case-hardened steel with grease nipples, as decided (EPR-DDR-002, item 16f), with simple felt or rubber dust seals added at the bush faces; bronze or UHMW-PE revisited only if TRL 4 wear data show scoring | Amish: "i approve your recommendations for all 555 open decisions." | EPR-PRC-001, open questions |
| 2026-10-02 | Mold wear: build the prototype with plain 12 mm mold walls and measure their wear against R8; bolt-on hardened liners are designed only if the measured rate would not last 50,000 sandy blocks | Amish: "i approve your recommendations for all 555 open decisions." | EPR-PRC-001, open questions |
| 2026-10-02 | Fill: weigh every fill, as decided (EPR-DDR-002, item 15); a calibrated scoop is allowed only for a soil whose scoop-to-mass scatter has been measured within the 0 to 2.7 % fill window | Amish: "i approve your recommendations for all 555 open decisions." | EPR-PRC-001, open questions |
| 2026-10-02 | Stabilizer: cement stays the default; lime is a documented option with its own mix chart and a longer curing period; no change to the press or its dwell | Amish: "i approve your recommendations for all 555 open decisions." | EPR-PRC-001, open questions |
| 2026-10-02 | Design soil: the operating chart is based on the softer soil (809 N peak, 405 N per operator, within R5's 500 N) until partner soils are measured, then each soil gets its own figure | Amish: "i approve your recommendations for all 555 open decisions." | EPR-PRC-001, open questions |
