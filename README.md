# EarthPress

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Sustainable Housing · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $450 USD · **Difficulty:** 3 of 5

A manual compressed earth block press with a lever and toggle linkage, producing stabilized soil blocks for low-carbon walls, with a simple soil test kit to choose mixes.

![EarthPress concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Concept rationale

Compressed stabilized earth blocks turn the soil on a building site into walling with a fraction of the energy of fired brick, but only if someone has a press. A manual lever and toggle press needs no fuel, power or hydraulics, can be welded from stock steel sections, and puts block making in the hands of the builder instead of a factory. The toggle suits the job because soil gets stiffer as it compacts, and a toggle's force ratio rises sharply at the end of its stroke, exactly where the force is needed.

EarthPress is open hardware so that a local welder can build, repair and adapt it without license fees or a distant supplier, and so that the soil test kit and mix guidance travel with it. The press is about $400 in parts, well below the thousands of dollars of hydraulic designs, and garage-buildable with a stick welder, grinder and drill press.

## Burning platform

Buildings and construction account for about 32 % of global energy use and 34 % of global CO2 emissions ([UNEP, 2025](https://www.unep.org/resources/report/global-status-report-buildings-and-construction-20242025)), and cement alone for around 8 % of global CO2 ([Chatham House, 2018](https://www.chathamhouse.org/2018/06/making-concrete-change-innovation-low-carbon-cement-and-concrete)). At the same time UN-Habitat estimates that about 3 billion people will need adequate housing by 2030, about 96,000 new affordable homes every day ([UN-Habitat](https://unhabitat.org/topic/housing)).

Meeting that demand with fired brick and cement block would lock in large emissions. Cement-stabilized earth blocks embody about 49 kg CO2/m³ against about 643 kg CO2/m³ for locally fired bricks ([Auroville Earth Institute](https://www.earth-auroville.com/compressed_stabilised_earth_block_en.php)), so the walls of a small house (about 7 m³ of blockwork) would avoid roughly 4 t of CO2 (estimate, excluding mortar and transport).

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Self-build and affordable housing | Families and cooperatives make walling for one- and two-room houses from site soil |
| Small construction enterprises | A block yard sells stabilized blocks to local builders as a business |
| Humanitarian and reconstruction programs | NGOs train masons and build schools, clinics and transitional-to-permanent housing |
| Agriculture | Farm stores, grain stores, animal shelters and boundary walls |
| Vocational education | Technical colleges teach earth building, soil testing and press fabrication |
| Low-carbon architecture in high-income countries | Garden walls, studios and small buildings where earthen codes allow CEB |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| Sub-Saharan Africa | 265 million people lived in slums in 2022, with an estimated 360 million more by 2030 if trends persist ([UN SDG Report 2024](https://unstats.un.org/sdgs/report/2024/Goal-11/)); soil is abundant and cement is costly |
| India and South Asia | Central and Southern Asia had 334 million slum dwellers in 2022 ([UN SDG Report 2024](https://unstats.un.org/sdgs/report/2024/Goal-11/)); India is home to the Auroville Earth Institute, a long-running center of CSEB practice, and fired-brick kilns are widespread |
| Eastern and South-Eastern Asia | The largest slum population, 362 million people in 2022 ([UN SDG Report 2024](https://unstats.un.org/sdgs/report/2024/Goal-11/)) |
| Colombia and Latin America | Birthplace of the CINVA-Ram manual press in the 1950s, with a living tradition of earth building |
| United States (New Mexico) | The 2021 New Mexico Earthen Building Materials Code covers CEB and requires 300 psi (about 2.1 MPa) compressive strength ([14.7.4 NMAC](https://www.srca.nm.gov/parts/title14/14.007.0004.html)) |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. It extends the sustainable housing work of SnapFrame and ThermaBrick. The practical trigger was a gap in open presses: the best-documented open design, the Open Source Ecology CEB Press, is hydraulic and costs $3,000 to $6,500 in materials ([OSE wiki](https://wiki.opensourceecology.org/wiki/CEB_Press)), while the manual lever presses that suit a self-builder are mostly closed products or old drawings.

## Problem

Fired bricks and cement blocks carry high embodied carbon and cost; compressed earth blocks are proven but good presses are expensive or hard to source. Design with, not for: requirements must come from co-design sessions with builders and masons through a local partner (see [docs/01-problem.md](docs/01-problem.md)).

## Concept

A manual compressed earth block press with a lever and toggle linkage, producing stabilized soil blocks for low-carbon walls, with a simple soil test kit to choose mixes. One 1.5 m lever drives a toggle under the piston to compact moist, sieved soil into a 290 x 140 x 90 mm block at about 2 MPa (about 81 kN), then ejects the block. First estimates: about 300 blocks a day with a crew of four and about $403 in parts. All figures are estimates to be checked at TRL 3.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

1. Frame on skids
2. Steel mold box
3. Lid with hinge and latch
4. Piston and push rod
5. Toggle linkage and pins
6. Lever and crank (removable)
7. Ejection stop and lever catch
8. Soil sieve, 5 mm mesh
9. Soil test kit
10. Block gauge

The working bill of materials is in [bom/bom.csv](bom/bom.csv). Numbers match the [exploded view](media/exploded.png).

## Safety

> High lever forces: the piston applies about 81 kN. Keep hands clear of the mold and linkage, use the lever catch whenever the lever is released, and never unlatch the lid under load. Cement burns skin and eyes, and sieving dry soil raises silica dust: wear gloves, eye protection and a respirator. Use two-person lifting for the press parts. Blocks are not certified; structural use needs an engineer and block tests under the local code. See the safety section of [docs/02-concept.md](docs/02-concept.md).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (EPR-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `EPR-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Extending strong areas set.
