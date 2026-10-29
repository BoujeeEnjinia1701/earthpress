---
doc_id: EPR-OPT-001
title: EarthPress concept options
project: EarthPress
doc_type: Concept options
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First concept options (kit 1.8 pipeline, kit 1.9.1 detailed models); the current design is option A; scored against EPR-URS-001; all three within 10 %, sent to Amish without a pick
---

# EarthPress concept options

No recommendation: the current lever and toggle press (option A) scores 186 of 245, the power screw press (option B) 181 and the rope-lifted drop rammer (option C) 168. B is 2.7 % and C 9.7 % below A, so under STANDARDS section 21 all three go to Amish without a pick, recorded as "Proposed, awaiting Amish" (EPR-DEC-001 D1, EPR-DDR-004). The repo stays on option A, the design it was built around, unless Amish decides otherwise. Every option is modelled at detail level D3 in `cad/src/model.py` and `cad/src/epr_options.py` (STANDARDS section 24).

![Concept options side by side at one scale](../media/options.png)

*The options picture is rendered on Amish's Mac with `python .kit/options.py` (Blender Cycles); until then this link has no image.*

## The options

### Option A: lever and toggle press (the current design)

A 1.7 m lever drives a toggle under a bottom piston; the force ratio climbs to 173:1 at a crank stop, so two people press a weighed fill to 2 MPa and a 90 mm block. This is the constructable design of EPR-DDR-003 with fix F1 (40 mm 42CrMo4 +QT toggle pins): a welded base on skids, a bolted press core of UPN 80 columns, a 12 mm plate mold with a ribbed, pinned lid, a slotted push rod, four toggle links in bushes, a lever hub with crank, catch and pawl, an eject seesaw and a linkage guard. It is the CINVA-Ram pattern with every member sized (EPR-CAL-001).

- First-order numbers: 81.2 kN at 2 MPa; peak pull 405 N per operator for the softer design soil; about 296 blocks a day with a crew of four; 203.8 kg in 11 pieces of 44.5 kg or less; USD 542 in parts.
- Key risks: the narrow fill window (0 to +2.7 %, weighed fills), 47 J of kickback held by the end pawl, the soil compaction law not yet measured (EPR-STM-001 S6).
- Needs from a co-design partner: soils to measure the compaction curve, acceptance of a two-person lever, timed cycles.

### Option B: power screw press

Two people turn a capstan on a self-locking two-start Tr 40 x 14 screw in a bronze nut; the screw drives a platen down into the mold to a stop collar. An H frame of UPN 80 columns, a bottom beam and a crosshead carry the nut; a removable stop pin holds a floor piston during pressing, and an eject seesaw lifts it to push the block out.

- First-order numbers: 406 N per operator on 0.53 m capstan grips at 81.2 kN (screw efficiency about 43 %); about 225 blocks a day (111 s cycle, 14 unloaded turns each way); 165.5 kg in the model; about USD 460 plus the screw, bronze nut and thrust bearing (not priced, to assess).
- Key risks: a greased two-start screw may not self-lock (EPR-STM-001 B2), so the platen could run back; thread wear in gritty soil; the bought screw, nut and bearing are specialist parts.
- Needs from a co-design partner: a source for trapezoidal screws and bronze nuts; acceptance of a slower cycle.

### Option C: rope-lifted drop rammer

Two people pull a rope over a head pulley to lift a 20 kg sleeve weight 450 mm up a guide rod and let it fall on an anvil collar; the plunger on the rod compacts the soil with about 25 blows to a height stop. The same base, columns, mold, floor piston and eject seesaw as B, with a light crosshead and guide sleeve instead of the screw.

- First-order numbers: 25 blows of 88 J give standard Proctor energy for the block (2.2 kJ); 98 N per person on the rope (196 N when lifting the plunger for filling); about 160 blocks a day (160 s cycle); 170.5 kg in the model; about USD 470 plus the pulley and rope (not priced, to assess).
- Key risks: impact compaction densifies the top of the block most and its equivalence with 2 MPa static pressing is unproven (C2); a falling weight about 4,000 times a day; the impact force on the mold and floor stop is unknown (C6).
- Needs from a co-design partner: test blocks to compare density and strength with pressed blocks.

## First-order numbers

Table 1. Options compared (mass and parts count from `cad/fidelity.json`; A's mass is the press without the soil kit, from EPR-CAL-001 section 8).

| Quantity | Option A | Option B | Option C |
| --- | --- | --- | --- |
| Estimated parts cost (USD) | 542 (priced BOM) | About 460 plus screw, nut and bearing (to assess) | About 470 plus pulley and rope (to assess) |
| Mass (kg) | 203.8 (press) | 165.5 | 170.5 |
| Output or throughput | About 296 blocks a day | About 225 blocks a day | About 160 blocks a day |
| Energy or effort | 405 N per operator at the peak, for a few seconds | 406 N per operator over 4.3 loaded turns, plus 28 light turns | 98 N per person, 25 pulls per block |
| Parts count (D3 model) | 251 (with the soil kit) | 185 | 165 |
| STEM check | Within, after fix F1; open on S2, S6, S18 | Plausible on self-locking (B2) and nut bearing (B3) | Plausible on density (C2), output (C5) and impact force (C6) |

Costs for B and C are first-order: the soil kit, consumables and fasteners as A (USD 113), plus the rest at A's cost per kilogram of press (USD 2.10/kg, steel, cutting and the bought pins and bushes). They are not priced from quotes.

## Scoring

Table 2. Weighted scoring (weights: High UR 3, Medium 2, Low 1; scores 1 to 5; URs from EPR-URS-001).

| Criterion | Source | Weight | A | B | C | Reason |
| --- | --- | --- | --- | --- | --- | --- |
| Standard block size and height | UR-001 | 3 | 5 | 4 | 3 | A's crank stop fixes 90 mm; B's stop collar fixes it but the frame stretches under load; C's stop sets height but density varies top to bottom |
| Dense, strong blocks (2 MPa) | UR-002 | 3 | 4 | 5 | 2 | A reaches 2 MPa within a weighed fill window; B has pressure in hand at any fill; C's equivalence with pressing is unproven (C2) |
| Output for a house | UR-003 | 3 | 4 | 3 | 2 | 296, about 225 and about 160 blocks a day against 300 |
| Ordinary adults can operate it | UR-004 | 3 | 4 | 4 | 3 | A and B need about 405 N each; C's pulls are light but about 4,000 a day per pair |
| Built and repaired by a local welder | UR-005 | 3 | 4 | 3 | 5 | A needs bought turned pins and bushes; B a trapezoidal screw, bronze nut and thrust bearing; C only plate, tube, bar, a pulley and rope |
| Movable between sites | UR-006 | 2 | 3 | 4 | 4 | 203.8, 165.5 and 170.5 kg |
| Long life, replaceable wear parts | UR-007 | 2 | 3 | 2 | 4 | A has ten bushes and grease points; B's screw and nut wear in grit; C has few moving parts and a consumable rope |
| Mix chosen with field tests | UR-008 | 3 | 4 | 4 | 4 | Same soil kit for all |
| Affordable press and kit | UR-009 | 3 | 3 | 3 | 4 | A USD 542; B and C below A before their bought parts are priced |
| Low stabilizer use | UR-010 | 2 | 4 | 5 | 3 | B's pressure margin could let cement fall; C's uncertain density may need more |
| Lower carbon than fired brick | UR-011 | 2 | 4 | 4 | 3 | Same blocks for A and B; C may need more cement |
| Safe for operators and bystanders | UR-012 | 3 | 3 | 4 | 2 | A stores 47 J at the stop (pawl, guard); B stores little if it self-locks; C drops 20 kg about 4,000 times a day |
| Open documentation | UR-013 | 2 | 4 | 4 | 4 | Same documentation route |
| Human powered | UR-014 | 3 | 5 | 5 | 5 | None uses fuel, electricity or hydraulics |
| Works outdoors in dust and rain | UR-015 | 2 | 4 | 2 | 4 | A's bushes have dust seals; B's threads are exposed; C's rod and collars tolerate grit |
| Blocks testable against a strength reference | UR-016 | 2 | 4 | 4 | 3 | A and B make uniform pressed blocks; C's density gradient widens test scatter |
| Cost against the value-engineering target | STANDARDS s21 | 2 | 3 | 3 | 4 | A is USD 42 over; B and C may come in under |
| Buildable with local skills and tools | STANDARDS s21 | 2 | 4 | 3 | 5 | As UR-005 |
| Safety | STANDARDS s21 | 3 | 3 | 4 | 2 | As UR-012 |
| Maintenance | STANDARDS s21 | 1 | 3 | 2 | 4 | As UR-007 |
| **Weighted total (of 245)** | | | **186** | **181** | **168** | A first; B 2.7 % and C 9.7 % below A |

## Recommendation

None. The three options are within 10 % of each other, so they go to Amish without a pick (STANDARDS section 21), as decision D1 in EPR-DEC-001, argued in EPR-DDR-004. The repo stays on option A, the existing design, unless he chooses otherwise; changing to B or C would change the pitch ("a lever and toggle linkage") and is his decision.

Ideas from the runners-up worth grafting onto A whichever is chosen: from B, a positive stop that does not depend on the operators (A already has one in its crank stop) and a capstan-like long arc for a single operator, which would need a lower force ratio; from C, the simplicity of its parts list, which argues for keeping A's bought parts to the pins, bushes and springs.
