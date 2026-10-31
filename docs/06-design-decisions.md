---
doc_id: EPR-DEC-001
title: EarthPress design decisions register
project: EarthPress
doc_type: Design decisions register
version: "0.7"
status: Draft
date: '2026-10-30'
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
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Design for construction (EPR-DDR-003, P1 to P15) accepted by Amish on 2026-10-02; the 2026-10-01 row no longer says open for review"
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Value engineering restated: USD 523 with the dust seals (USD 23 over the target)'
- version: "0.6"
  date: '2026-10-25'
  author: Amish Chadha
  change: 'Kit 1.9.1 upgrade: toggle pin fix F1 decided under the standing instruction of 2026-10-23 (EPR-STM-001 S9, S10); corrections C1 to C5 from the detailed model; open decisions D1 (concept selection, three options within 10 %, no pick) and D2 (R7 total mass, 203.8 kg); value engineering at USD 542'
- version: "0.7"
  date: '2026-10-30'
  author: Amish Chadha
  change: "D2 (R7 total of 205 kg) decided by Amish on 2026-10-30 (EPR-DDR-005); D1 stays open (no pick); design load question added as D3 (no recommendation)"
---

# EarthPress design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`, EPR-BLD-001) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Decisions awaiting Amish (D1 had no pick; D3 had no recommendation). D2 was decided on 2026-10-30 and is in Table 3.*

| # | Decision | Options | Recommendation | Status | Record |
| --- | --- | --- | --- | --- | --- |
| D1 | Concept selection (kit 1.8 concept options) | (A) lever and toggle press, the current design: 186 of 245; (B) power screw press: 181; (C) rope-lifted drop rammer: 168 | None: A and B are within 2.7 % and C within 9.7 % of A, so all three go to Amish without a pick (STANDARDS section 21). Notes for the choice: B's self-locking is not assured with a greased screw (EPR-STM-001 B2) and it makes about 225 blocks a day; C's density is unproven (C2) and it makes about 160 a day; A keeps every part of the constructable design | Proposed, awaiting Amish | [EPR-DDR-004](decisions/0004-concept-selection.md), [EPR-OPT-001](02a-concept-options.md) |
| D3 | Design load basis (independent review): the abuse case at the grip | (a) keep 1,000 N at the grip (173 kN) and add a grip stop that limits the load; (b) raise the abuse case to about 1,500 N (about 260 kN) with larger lugs and pins | None: no recommendation was made in the review (EPR-STM-001 S7, S9, S10) | Proposed, awaiting Amish | EPR-STM-001, EPR-DDR-005 |

## Decided under Amish's standing instruction of 2026-10-23

Amish, 2026-10-23: when a STEM check row fails, propose and implement the best fix for the design and its constructability in the same session and record it here as decided under that instruction; Amish can reverse it.

*Table 1a. Fixes decided under the standing instruction.*

| # | Date | STEM row | What failed | Options weighed | Fix made | Cost and mass |
| --- | --- | --- | --- | --- | --- | --- |
| F1 | 2026-10-25 | EPR-STM-001 S9, S10 | The 35 mm C45 toggle pins, loaded as clevis pins, reached 388 MPa in bending against 370 MPa yield at the nominal 81.2 kN (base pin) and 826 MPa at the 173 kN design load; the 20 mm base pin lugs reached 124 MPa in bearing against 100 MPa. EPR-CAL-001 v0.6 checked shear only | (a) 42CrMo4 +QT pins at 35 mm: still 826 MPa against 750 MPa at 173 kN, fails; (b) C45 pins at about 50 mm: bigger links, bushes, lugs and column holes; (c) 40 mm 42CrMo4 +QT pins with 28 mm lugs: passes with the least change to the linkage geometry; (d) clamp the pins so the spacers carry bending: needs bolted collars on every pin and still loads the pin in the gap | (c): toggle pins 40 mm 42CrMo4 +QT in case-hardened 40 x 46 mm bushes; base pin lugs 28 mm (spacers 8 mm); connecting link 24 x 60 mm round the 40.5 mm knee hole; column access holes 46 mm; push rod slot 42 x 205 mm and 12.5 mm of rod below it; dust seals 56 x 40.5 mm; hinge and latch pins 42CrMo4 +QT at 30 mm (their bending factor at 173 kN goes from 1.03 to 2.09). Base pin now 498 MPa against 750 MPa (SF 1.51), lugs 78 MPa (1.29) | About USD 19 more (estimate: line 3 USD 2, line 5 USD 14, line 1 USD 1, line 11 USD 2 for the corrected bolts); about 1.2 kg more. Model, drawings, build plan pictures and text, CAL section 6b, BOM, PRS PR-016 updated |

## Corrections from the detailed kit 1.9.1 model

Found while modelling every fastener and part to detail level D3 (Amish, 2026-10-24: "I want detailed TRL3 CAD"). Each changes a dimension or a fastener, not the working principle; recorded here so Amish can reverse any of them.

*Table 1b. Model corrections, 2026-10-25.*

| # | What the model showed | Correction |
| --- | --- | --- |
| C1 | Two lines of M16 bolts at 18 mm either side of the column web centre put the 30 mm washers on the UPN 80 flanges (the flat of the web between the root radii is about 48 mm) | Four M16 bolts per side in one line on the web centre, 20, 57, 93 and 130 mm up from the mold's bottom edge; same eight bolts, same shear check |
| C2 | M16 x 20 bolts engaged 11 mm of the 16 mm tapped flange | M16 x 25, full engagement |
| C3 | M12 x 40 column foot bolts and M12 x 50 tie tab bolts were too short for two washers and a nut over 28 and 38 mm grips | M12 x 50 (feet) and M12 x 60 (ties) |
| C4 | The guard foot bolts sat under the guard's vertical frame member (no room for the head) and their nuts would have landed inside the cross tube under the base plate | Guard feet extended 15 mm inward; M10 x 16 bolts into holes tapped M10 in the base plate, 94 mm from the press axis and 103 mm off centre |
| C5 | The guard bracket bolts pass the bracket plate, a 45 mm spacer bracket and the guard's side frame (77 mm), not a 35 mm spacer | M10 x 95 with two washers and a nut |

## To confirm when parts are bought

*Table 2. Items to confirm when parts are bought.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The UPN 80 channel's web (6 mm), flange (8 mm) and depth (45 mm) | The mold bolt holes, the pin access holes and the tie bolt holes are set from them; the column webs must be 196 apart | EPR-DDR-003, P2 |
| 2 | Bushes of 40 bore and 46 outside diameter are available locally, and 40 mm 42CrMo4 +QT bar for the pins | The link and lug bores are 46; another bush size changes the bore, the net section and the bearing checks (F1) | EPR-DDR-003, P5; F1 |
| 3 | A tube with about 61.3 inside diameter for the two sockets | The 2 in schedule 40 lever (60.3) must slide in without much play | EPR-BLD-001, sections 3.7 and 3.9 |
| 4 | Two small torsion springs strong enough to snap the catch and the pawl in | They make the catch and the pawl self-acting | EPR-BLD-001, section 3.8 |
| 5 | Expanded metal openings of 12 mm or less | Keeps fingers out of the guard | EPR-BLD-001, section 3.10 |
| 6 | Local prices for steel, turned pins and bushes | The BOM prices are indicative; they set the estimated cost against the value-engineering target | EPR-CAL-001, section 11 |

## Value engineering

Value-engineering target: USD 500 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 542 (USD 42 over the target) after fix F1 and corrections C2 to C5 (USD 19). Main cost drivers and savings worth trying:

- Steel is the main cost: about 204 kg at about USD 1.30/kg is about USD 265. A lighter press (a 16 mm lid plate with deeper ribs, 10 mm mold walls, a lighter base plate, perhaps 10 kg) would save steel as well as mass; it was option (b) of the R7 mass decision, not taken on 2026-10-02 or 2026-10-30 (EPR-DDR-005), so it stays a saving worth trying.
- The parts added to make the press buildable (EPR-DDR-003) account for the rise from USD 488 to USD 520; the felt or rubber dust seals at the bush faces (decided 2026-10-02, about USD 3) take it to USD 523.
- Plain pins without bushes would save about USD 30, but R8 (wear) would fail, so this is a saving to weigh, not to take.
- Local prices for steel, turned pins and bushes are to be confirmed when parts are bought; every price is indicative.

## Decisions made

*Table 3. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 items 1 to 7 and 9: toggle and one lever (CINVA-Ram pattern), longer arc from a low pivot, 290 x 140 x 90 mm block, 2 MPa, 5 % cement, 12 mm base plate and bolted mold, field soil tests only, no pitch change | Amish: "i accept all your recommendations, go with them across all repos." | EPR-DDR-001, EPR-DDR-002 |
| 2026-09-25 | TRL 3 items 10 to 16: separate eject seesaw with a lost-motion slot, two operators on a T-handle, R5 reworded, R7 total 190 kg, budget $500, weighed fill, linkage geometry, crank stop, ribbed lid, end pawl, linkage guard, hardened bushes, R4 at 296 blocks a day | Amish, same instruction | EPR-DDR-001, EPR-DDR-002 |
| 2026-10-01 | Design for construction: columns turned, tapped mold flanges, pin access holes and spacers, round link ends, end skirts on the piston, lid pins in rib ears, rest catch and end pawl on the crank pin, central eject arm, ties moved, guard modelled, gauge made real (P1 to P15) | Made under Amish's 2026-09-30 instruction to make the design physically buildable ("fix the design assumptions to match and be physically feasible"); the changes themselves were accepted on 2026-10-02 (below) | EPR-DDR-003 |
| 2026-10-02 | R7 total mass: option (a). The R7 total is 200 kg, defined to include the guard and bolts, and the 50 kg piece limit is kept (heaviest piece 45 kg) | Amish: "i approve your recommendations for all 555 open decisions." | EPR-DDR-003, A1 |
| 2026-10-30 | R7 total mass (D2): option (a). The R7 total is 205 kg, counting bushes, nuts, washers and weld metal; the 50 kg piece limit is kept (heaviest piece 44.5 kg). The press is 203.8 kg in the model, 1.2 kg under; lightening by about 10 kg stays a value-engineering item | Amish, 2026-10-30: "on the calls - i go with your recommendations" | [EPR-DDR-005](decisions/0005-decisions-2026-10-30.md), EPR-CAL-001 section 8 |
| 2026-10-02 | Rest catch release: option (a), hand release, for the prototype, with the build plan rule that the catch is in before the latch is opened; a foot pedal is considered only if timed cycles (R4) show the extra step costs output | Amish: "i approve your recommendations for all 555 open decisions." | EPR-DDR-003, A3 |
| 2026-10-02 | First co-design partner: one that already trains builders in stabilized earth blocks and has local soils and cement supply. First candidate to approach: the Auroville Earth Institute in India, whose 290 x 140 x 90 mm block module the press uses | Amish: "i approve your recommendations for all 555 open decisions." | EPR-DDR-001, item 8 |
| 2026-10-02 | Bushes: case-hardened steel with grease nipples, as decided (EPR-DDR-002, item 16f), with simple felt or rubber dust seals added at the bush faces; bronze or UHMW-PE revisited only if TRL 4 wear data show scoring | Amish: "i approve your recommendations for all 555 open decisions." | EPR-PRC-001, open questions |
| 2026-10-02 | Mold wear: build the prototype with plain 12 mm mold walls and measure their wear against R8; bolt-on hardened liners are designed only if the measured rate would not last 50,000 sandy blocks | Amish: "i approve your recommendations for all 555 open decisions." | EPR-PRC-001, open questions |
| 2026-10-02 | Fill: weigh every fill, as decided (EPR-DDR-002, item 15); a calibrated scoop is allowed only for a soil whose scoop-to-mass scatter has been measured within the 0 to 2.7 % fill window | Amish: "i approve your recommendations for all 555 open decisions." | EPR-PRC-001, open questions |
| 2026-10-02 | Stabilizer: cement stays the default; lime is a documented option with its own mix chart and a longer curing period; no change to the press or its dwell | Amish: "i approve your recommendations for all 555 open decisions." | EPR-PRC-001, open questions |
| 2026-10-02 | Design soil: the operating chart is based on the softer soil (809 N peak, 405 N per operator, within R5's 500 N) until partner soils are measured, then each soil gets its own figure | Amish: "i approve your recommendations for all 555 open decisions." | EPR-PRC-001, open questions |
| 2026-10-25 | Toggle pin fix F1 (Table 1a) | Decided under Amish's standing instruction of 2026-10-23 ("propose and implement the best fix ... and record it in DEC as decided under that instruction"); Amish can reverse it | EPR-STM-001 S9, S10; EPR-CAL-001 section 6b |
| 2026-10-02 | Design for construction accepted: the changes P1 to P15, as made | Amish: "APPROVED: Design-for-construction changes in 10 repos (CityTwin, CoolShade, PalletPilot, Heliolite, PotholeLog, EarthPress, ReadyKit, CellCheck, CargoMule and ThermaCart)" | [EPR-DDR-003](decisions/0003-design-for-construction.md), Table 1 |
