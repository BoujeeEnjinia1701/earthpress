---
doc_id: EPR-PRC-001
title: EarthPress design precis
project: EarthPress
doc_type: Design precis
version: "0.3"
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update from EPR-CAL-001 and EPR-DDR-001 (linkage geometry, two-person T-handle, separate eject lever, ribbed lid, weighed fill, masses, cost, safety)
---

# EarthPress design precis

## Summary

EarthPress is a manual press, welded from common steel sections, that compacts moist, sieved and cement-stabilized site soil into 290 x 140 x 90 mm blocks with a 1.7 m lever driving a toggle linkage under the mold. The TRL 3 calculation (EPR-CAL-001) shows that the linkage reaches the 81.2 kN needed for 2 MPa with a force ratio of 173:1 at the stop, but that the peak pull is 668 N, so **two people share the lever on a T-handle**. Each fill is **weighed** to within about 200 g, because the pressure reached at the stop is sensitive to fill mass. The block is ejected with the same lever moved to a separate eject socket. A crew of four could make about 296 blocks a day (8.9 m² of 140 mm wall). The press weighs about 187 kg in eight pieces, none over 37 kg, and the press and kit cost about $488 in parts. R5 (operator force and grip height), R7 (total mass) and R13 (cost) are not met on paper; R2 and R4 are at risk. All values are estimates.

![Hero render](../media/hero.png)

*Figure 1. EarthPress at the start of the stroke, with its soil sieve, test kit, a stack of blocks with the block gauge, and a 1.75 m person for scale. Concept model, not for fabrication.*

## How it works

1. **Test.** The soil test kit screens site soil with a jar sedimentation test (sand, silt and clay fractions), a shrinkage box (linear shrinkage), and ribbon and drop tests. A printed chart turns the results into go or no-go and a starting cement content, usually 5 % by dry mass, following Auroville Earth Institute practice ([Auroville Earth Institute](https://www.earth-auroville.com/compressed_stabilised_earth_block_en.php)).
2. **Sieve and mix.** The crew throws dry soil through a 5 mm mesh sieve leaning on a prop, measures soil and cement by bucket, mixes them dry, then adds about 10 % water until a squeezed ball holds its shape and breaks cleanly when dropped.
3. **Weigh and fill.** With the lever on its rest stop and the lid open, the piston sits at the bottom of its stroke. The operator weighs a scoop of mix on the 10 kg scale to the target on the chart (about 7.74 kg for the reference soil, +1.3 % ± 100 g), tips it into the 290 x 140 mm mold, levels it about 150 mm deep, and closes and latches the lid.
4. **Press.** Two people pull the T-handle down from about 1.9 m to about 0.86 m. A 107 mm crank on the lever hub pushes a 420 mm connecting link against the knee of the toggle, which straightens from 29° to 6° from vertical and lifts the piston 60 mm. The force ratio climbs from about 15:1 to 173:1, so the force arrives where the soil is stiffest; the peak pull, 668 N in total, comes about 3 mm before the crank stop, at waist height. The end pawl catches the lever at the stop.
5. **Eject.** The operators hold the lever, lift the pawl and return the lever to its rest stop, which unloads the block. The lid is unlatched and swung open. The operator moves the lever to the eject socket on the +X side and pulls down: the seesaw fork lifts the push rod 160 mm, the rod rising past the toggle pin in its 200 mm slot, which pushes the block flush with the rim at about 470 N on the grip. The block is lifted off, checked with the block gauge and stacked in shade.
6. **Cure.** Blocks are kept damp under cover for about four weeks to let the cement hydrate, then air dried before use.

![Cutaway](../media/cutaway.png)

*Figure 2. Section through the mold and linkage at the start of the stroke: loose soil (brown) above the piston and slotted push rod (yellow), toggle links (orange), lever hub, crank and connecting link on the left, eject seesaw (purple) on the right.*

![Material flow](../media/flow.png)

*Figure 3. Material flow per 100 blocks, in kg (EPR-CAL-001 section 10). All values are estimates for a soil with 15 % oversize, 5 % cement and 10 % water.*

## Main components

Numbers match the exploded view (Figure 4) and `bom/bom.csv`. The general arrangement is drawing EPR-DWG-001 (`cad/drawings/EPR-DWG-001.pdf`).

*Table 1. Components.*

| # | Component | Choice | Notes |
| --- | --- | --- | --- |
| 1 | Frame, in two bolted pieces | Base: 60 x 60 x 3 mm tube skids 1.0 m long, 50 x 50 mm cross tubes, 12 mm base plate, lever bracket with rest stop, tie tubes. Core: two UPN 80 columns and a base beam of two 20 x 100 mm plates carrying the toggle base pin | The press force closes through the core and mold; the base only carries weight and the lever reaction. 36.6 and 27.7 kg |
| 2 | Mold box | 12 mm plate round a 290 x 140 x 200 mm cavity, 16 x 50 mm belt round the top, bolted to the columns with eight M16 8.8 bolts | 32.0 kg; wear liners remain an open question |
| 3 | Lid with hinge and latch | 20 mm plate with two 20 x 70 mm ribs; 30 mm hinge and latch pins | Rated for 173 kN; 25.9 kg |
| 4 | Piston and push rod | 25 mm plate on a 60 mm square rod with a 200 mm lost-motion slot and a foot pin | Clearance about 1 mm per side in the mold |
| 5 | Toggle linkage | Four 28 x 70 mm links, 245 mm between centers; 24 x 50 mm connecting link, 420 mm; three 35 mm C45 pins in case-hardened steel bushes, greased | Crank stop at 6° limits the force to 173 kN |
| 6 | Lever, crank hub and T-handle | 1.7 m of 2 in schedule 40 pipe in a socket on a hub with a 107 mm crank; pivot at 266 mm height, 468 mm from the piston axis; 0.5 m T-handle | Removable; the same pipe fits the eject socket |
| 7 | Eject lever, catch and end pawl | Seesaw with a 160 mm fork and a socket, pivoted on the +X side; rest stop and catch; spring pawl at the end of the stroke | Eject ratio 10.3:1 |
| 8 | Soil sieve | 5 mm welded mesh in a 700 x 900 mm timber frame on a prop | Removes stones and clods |
| 9 | Soil test kit | Two 1 L clear jars, a 600 x 40 x 40 mm shrinkage box, measuring buckets, 10 kg scale with 50 g divisions, printed chart | Field tests only (EPR-DDR-001 item 7) |
| 10 | Block gauge | Go or no-go bar for length and height | Checks every block |

BOM lines 11 to 13 (hardware and paint, consumables, and an expanded-metal guard over the crank, connecting link and knee) have no callout.

![Exploded view](../media/exploded.png)

*Figure 4. Exploded view with callouts matching the BOM. Loose soil and the block stack are context only.*

## Key numbers

All values are estimates from EPR-CAL-001, where the assumptions are stated.

*Table 2. Key numbers.*

| Quantity | Value | Basis |
| --- | --- | --- |
| Block force for 2 MPa | 81.2 kN (8.3 tonne-force) | 2 MPa x 0.0406 m² |
| Block volume and mass | 3.65 L; 6.94 kg dry, 7.64 kg moist | Dry density 1,900 kg/m³ (assumed) |
| Force ratio | 14.8:1 at the start, 20.0:1 at 30 mm, 173:1 at the stop | Toggle 29.3° to 6.0°, lever arc 59.2° |
| Peak pull at the grip | 668 N (334 N each for two); 571 to 809 N for stiffer or softer soil | Soil pressure rising tenfold over the last 14 mm (assumed) |
| One operator at 500 N | Stalls at 0.53 MPa | The peak comes before the stop |
| Compaction work | 494 J (353 to 705 J) | Same soil law |
| Fill window for 2 MPa at the stop | 0 to +2.7 % of nominal (0 to 206 g) | Two operators |
| Design load for the structure | 173 kN (4.26 MPa on the block) | 1,000 N at the grip at the stop |
| Lowest safety factor at 173 kN | 1.13 (bush bearing); lid 1.84, base beam 1.60, lever 1.57 | EPR-CAL-001 Table 5 |
| Kickback energy if released at the stop | 47 J | 1 mm soil rebound plus column stretch |
| Eject force and grip force | 4.83 kN; 468 N | 0.1 MPa residual wall pressure, friction 0.6 (assumed) |
| Output | 296 blocks per day, crew of four; 8.9 m² of wall | 85 s cycle (assumed) |
| Small house, 50.5 m² of wall | 1,683 blocks, 5.7 press days, 556 kg cement (11.1 bags) | 22 m perimeter, 2.7 m walls, 15 % openings |
| Embodied CO2 of that wall | 0.35 t as CSEB against 4.55 t as fired brick (7.6 %) | 49 and 643 kg CO2/m³ ([Auroville Earth Institute](https://www.earth-auroville.com/compressed_stabilised_earth_block_en.php)); excludes mortar and transport |
| Press mass | 187 kg in eight pieces; heaviest 36.6 kg | Model volumes at 7,850 kg/m³ |
| Parts cost | $488 (indicative) | `bom/bom.csv` |

## Key design choices

The first six choices are adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction and remain open for his review (EPR-DDR-001 Table 1). The rest are TRL 3 engineering proposals, awaiting Amish (EPR-DDR-001 Table 2).

- **Bottom piston with a toggle and one lever**, following the CINVA-Ram pattern rather than a screw, a bottle jack or a top-down ram. It needs no hydraulic parts and a welder can build and repair it.
- **Flat 290 x 140 x 90 mm block**, the module used by the Auroville Earth Institute. Interlocking molds could follow as inserts.
- **2 MPa compaction target**, the low end of CSEB practice.
- **Cement stabilization at 5 % by default**, with lime as an option for clay-rich soils.
- **Field soil tests only**, with no lab equipment.
- **Bolted frame and mold with a 12 mm base plate**, so the press splits into pieces of 37 kg or less.
- **Longer arc from a low pivot** (proposal): the lever starts nearly upright, which gives 59° of arc with the grip between 0.86 and 1.89 m. Raising the pivot to 800 mm for a 100° arc, as proposed at TRL 2, would take the grip below the ground.
- **Two operators on a T-handle** (proposal), since one person at 500 N stalls at 0.53 MPa.
- **Separate eject seesaw with a lost-motion slot** (proposal), because a toggle ending near straight cannot lift the piston another 90 mm.
- **Crank stop at the design end angle and a weighed fill** (proposal), which caps the force at 173 kN and fixes the block height at 90 mm.

## Safety

> **Safety:** The press applies 81 kN (over 8 tonne-force) at the piston, and up to 173 kN if two people pull hard at the stop. Keep hands out of the mold, the linkage and the eject fork while anyone is on a lever. Only the people on the lever touch it, and only after calling "clear". Keep the linkage guard in place.

> **Safety:** Released at the end of the stroke, the lever kicks back with about 47 J. Engage the end pawl before letting go, return the lever to its rest stop under control, keep heads out of the lever arc and never stand on the lever.

> **Safety:** Never unlatch the lid while the lever is loaded. Return the lever to the rest stop first. The lid and latch are sized for 173 kN, but a worn latch or a missing pin can throw the lid and soil upward.

> **Safety:** Portland cement is alkaline and can burn skin and eyes. Wear gloves, long sleeves and eye protection when mixing. Sieving dry soil raises dust that may contain respirable crystalline silica; sieve damp soil where possible, work upwind and wear an FFP2 or N95 respirator.

> **Safety:** A moist block weighs about 7.6 kg, the lid 26 kg on its hinge and the press 187 kg. Lift blocks close to the body, rotate tasks in the crew, and move the press dismantled, two people to each piece.

> **Safety:** Blocks made by EarthPress are not certified. Walls in seismic zones, multi-storey walls and any building that needs a permit require a structural design and block tests by a qualified engineer under the local building code.

> **Safety:** Building the press involves welding, grinding and cutting. Use welding PPE, guard grinders and work away from flammables.

## Open questions

- [ ] Bushes: case-hardened steel is assumed; would bronze or UHMW-PE last longer in dust?
- [ ] Does the mold need hardened wear liners, or is plain 12 mm plate enough for 50,000 blocks with sandy soil?
- [ ] How stiff are real partner soils? The peak pull ranges from 571 to 809 N over the assumed range.
- [ ] Can a fill-by-volume scoop replace weighing once a soil is characterized?
- [ ] Is lime stabilization practical where cement is scarce, and does the press need a longer dwell for it?
- [ ] Which partner and region should the first co-design sessions use (EPR-DDR-001 item 8)?
