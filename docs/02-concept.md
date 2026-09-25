---
doc_id: EPR-PRC-001
title: EarthPress design precis
project: EarthPress
doc_type: Design precis
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media, open questions)
---

# EarthPress design precis

## Summary

EarthPress is a manual press, welded from common steel sections, that compacts moist, sieved and cement-stabilized site soil into 290 x 140 x 90 mm blocks with a single lever driving a toggle linkage under the mold. The same lever ejects the block once the lid swings open. A field soil test kit, a 5 mm sieve and a block gauge complete the set. First-order estimates suggest that about 81 kN on the block face gives the 2 MPa compaction pressure used in CSEB practice, that a crew of four could make about 300 blocks a day (about 9 m² of 140 mm wall), and that the press and kit cost about $403 in parts. Two requirements are at risk and one is not met: the work needed per block may exceed one operator's stroke in the modeled layout (R2), the lever ends too low (R5), and the frame is heavier than the 50 kg single-piece limit (R7). All values are estimates to be checked at TRL 3.

![Hero render](../media/hero.png)

*Figure 1. EarthPress with its soil sieve, test kit, a stack of blocks with the block gauge, and a 1.75 m person for scale. Concept massing model, not for fabrication.*

## How it works

1. **Test.** The soil test kit screens site soil with a jar sedimentation test (sand, silt and clay fractions), a shrinkage box (linear shrinkage), and ribbon and drop tests. A printed chart turns the results into go or no-go and a starting cement content, usually 5 % by dry mass, following Auroville Earth Institute practice ([Auroville Earth Institute](https://www.earth-auroville.com/compressed_stabilised_earth_block_en.php)).
2. **Sieve and mix.** The crew throws dry soil through a 5 mm mesh sieve leaning on a prop, measures soil and cement by bucket, mixes them dry, then adds about 10 % water until a squeezed ball holds its shape and breaks cleanly when dropped.
3. **Fill.** With the lever up and the lid open, the piston sits at the bottom of its stroke. The operator fills the 290 x 140 mm mold with a measured scoop of loose mix, about 150 mm deep, strikes it level and closes and latches the lid.
4. **Press.** The operator pulls the 1.5 m lever down. A short crank on the lever pushes the knee of a toggle linkage under the piston toward straight. The piston rises about 60 mm, compacting the soil to about 90 mm. As the toggle straightens its force ratio climbs steeply, so the peak force arrives at the end of the stroke, where the soil is stiffest.
5. **Eject.** The operator returns the lever, unlatches and swings the lid clear, then pulls the lever again past the compaction position to the ejection stop, which lifts the piston flush with the mold rim. The block is lifted off, checked with the block gauge and stacked in shade.
6. **Cure.** Blocks are kept damp under cover for about four weeks to let the cement hydrate, then air dried before use.

![Cutaway](../media/cutaway.png)

*Figure 2. Section through the mold and linkage at the start of the stroke: loose soil (brown) above the piston (yellow), toggle links (orange) under the push rod, lever and crank on the left.*

![Material flow](../media/flow.png)

*Figure 3. Material flow per 100 blocks, in kg. All values are estimates for a soil with 15 % oversize, 5 % cement and 10 % water.*

## Main components

Numbers match the exploded view (Figure 4) and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Frame on skids | Two 100 x 50 mm channel columns, 60 x 60 mm tube skids about 1 m long, 20 mm base plate, round-bar braces | Carries the full block force as tension between the base pivot and the lid |
| 2 | Mold box | 12 mm plate welded around a 290 x 140 x 250 mm cavity, with replaceable 3 mm wear liners (proposed) | Bolted to the columns so it can be removed (proposed, see R7) |
| 3 | Lid with hinge and latch | 22 mm plate on a 28 mm hinge pin, hook latch on the lever side | Reacts the block force; must never open under load |
| 4 | Piston and push rod | 20 mm plate on a 50 x 50 mm bar | Clearance about 1 mm per side in the mold |
| 5 | Toggle linkage and pins | Paired 20 mm flat links, about 190 mm between centers; three 30 mm pins in bronze or steel bushings | Knee moves about 100 mm sideways for about 60 mm of piston travel |
| 6 | Lever and crank | 1.5 m schedule 40 pipe (about 42 mm OD) on a crank about 80 mm long; removable | Lever ratio about 19:1 |
| 7 | Ejection stop and lever catch | Adjustable stop on the column; catch on the skid that holds the lever at rest | Stops the lever from falling when released |
| 8 | Soil sieve | 5 mm welded mesh in a 700 x 900 mm timber frame on a prop | Removes stones and clods |
| 9 | Soil test kit | Two 1 L clear jars, a 600 x 40 x 40 mm shrinkage box, measuring buckets, spring scale, printed chart | Field tests only; no laboratory |
| 10 | Block gauge | Go or no-go bar for length and height | Checks every block |

![Exploded view](../media/exploded.png)

*Figure 4. Exploded view with callouts matching the BOM. Loose soil and the block stack are context only.*

## First-order numbers

All values are estimates with the assumptions stated.

| Quantity | Estimate | Basis |
| --- | --- | --- |
| Block face area | 0.0406 m² | 290 x 140 mm |
| Block force for 2 MPa | about 81 kN (8.3 tonne-force) | 2 MPa x 0.0406 m²; Auroville practice is 2 to 4 MPa |
| Block force for 4 MPa | about 162 kN | Out of reach for a manual toggle press of this size |
| Overall force ratio needed | about 162:1 | 81 kN / 500 N pull at the grip |
| Lever ratio | about 19:1 | 1.5 m lever on an 80 mm crank |
| Toggle ratio needed at end of stroke | about 9:1 | Links within about 3° of straight (ratio about 1 / (2 tan θ)) |
| Compaction work per block | about 0.6 to 1.2 kJ (estimate) | Peak force x 60 mm stroke / 4 to / 8, since pressure rises steeply near the end |
| Work from one operator | about 0.65 kJ | 500 N over about 1.3 m of grip travel (50° arc). **Short of the upper estimate**: a 100° arc or two operators needed |
| Block volume and mass | about 3.65 L, about 6.9 kg dry | Dry density about 1,900 kg/m³ (assumed) |
| Cement per block | about 0.33 kg | 5 % of dry soil mass |
| Output | about 300 blocks per 8 h day, crew of four | About 96 s per block for fill, press, eject and stack (assumed, to be timed) |
| Wall per day | about 9 m² of 140 mm wall | About 33 blocks per m² with 10 mm joints |
| Small house, about 50 m² of wall | about 1,700 blocks, about 6 press days, about 560 kg cement (11 bags of 50 kg) | 22 m perimeter, 2.7 m walls, 15 % openings |
| Embodied CO2 of that wall material | about 0.35 t for CSEB against about 4.6 t for fired brick | 7.1 m³ at 49 and 643 kg CO2/m³ ([Auroville Earth Institute](https://www.earth-auroville.com/compressed_stabilised_earth_block_en.php)); excludes mortar and transport |
| Pin shear, 30 mm pin in double shear | about 57 MPa at 81 kN | Well within mild steel; bearing and link buckling to be checked at TRL 3 |
| Column tension | about 40 MPa at 81 kN | Two channels, about 1,000 mm² each (assumed) |
| Press mass | about 123 kg; frame about 61 kg, mold about 23 kg, lid about 11 kg | Steel at 7,850 kg/m³ over nominal sections |
| Parts cost | about $403 | `bom/bom.csv`, indicative |

## Key design choices

All of these are proposed, awaiting Amish. The review note (`docs/REVIEW.md`) gives options and a recommendation for each.

- **Bottom piston with a toggle, one lever for both pressing and ejection**, following the CINVA-Ram pattern rather than a screw, a bottle jack or a top-down ram. It needs no hydraulic parts and a welder can build and repair it.
- **Flat 290 x 140 x 90 mm block**, the module used by the Auroville Earth Institute, rather than a larger or interlocking block. Interlocking molds could follow as inserts.
- **2 MPa compaction target**, the low end of CSEB practice, because 4 MPa needs about 162 kN, beyond a manual press of this size.
- **Cement stabilization at 5 % by default**, with lime as an option for clay-rich soils.
- **Field soil tests only**, with no lab equipment, so the kit costs little and travels with the press.
- **Bolted mold and removable lever**, so the press splits into pieces two people can lift (R7 is not yet met).

## Safety

> **Safety:** The press applies about 81 kN (over 8 tonne-force) at the piston. Keep hands out of the mold and away from the linkage while anyone is on the lever. Only the operator touches the lever, and only after calling "clear".

> **Safety:** The lever stores energy near the end of the stroke and can kick back if the grip slips or a pin fails. Use the lever catch whenever the lever is released, keep the head out of the lever arc and never stand on the lever.

> **Safety:** Never unlatch the lid while the lever is loaded. A lid or latch failure under load can throw the lid and soil upward. The latch must hold at least 1.5 times the peak block force (R12).

> **Safety:** Portland cement is alkaline and can burn skin and eyes. Wear gloves, long sleeves and eye protection when mixing. Sieving dry soil raises dust that may contain respirable crystalline silica; sieve damp soil where possible, work upwind and wear an FFP2 or N95 respirator.

> **Safety:** A dry block weighs about 7 kg and the press about 123 kg. Lift blocks close to the body, rotate tasks in the crew, and move the press with four people or dismantled.

> **Safety:** Blocks made by EarthPress are not certified. Walls in seismic zones, multi-storey walls and any building that needs a permit require a structural design and block tests by a qualified engineer under the local building code.

> **Safety:** Building the press involves welding, grinding and cutting. Use welding PPE, guard grinders and work away from flammables.

## Open questions

- [ ] Raise the lever pivot to about 800 mm to give a 100° arc and a higher grip at the end of the stroke? This would help both R2 and R5.
- [ ] Bushings: bronze, steel or UHMW-PE for dusty conditions?
- [ ] Does the mold need hardened wear liners, or is plain 12 mm plate enough for 50,000 blocks with sandy soil?
- [ ] How do fill-mass errors change final pressure and block height with a toggle this close to straight? A variable-height stop may be needed.
- [ ] Is lime stabilization practical where cement is scarce, and does the press need a longer dwell for it?
- [ ] Which partner and region should the first co-design sessions use?
