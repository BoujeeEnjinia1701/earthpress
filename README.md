# EarthPress

**Area:** Sustainable Housing · **Status:** Concept · **Prototype budget:** about $450 USD · **Difficulty:** 3 of 5

A manual compressed earth block press with a lever and toggle linkage, producing stabilized soil blocks for low-carbon walls, with a simple soil test kit to choose mixes.

## Concept rationale

A press a local welder can build lets communities make their own walling from site soil.

## Burning platform

Housing demand in fast-growing cities is met with carbon-intensive materials many families cannot afford.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. It extends the sustainable housing work of SnapFrame and ThermaBrick.

## Problem

Fired bricks and cement blocks carry high embodied carbon and cost; compressed earth blocks are proven but good presses are expensive or hard to source.

## Concept

A manual compressed earth block press with a lever and toggle linkage, producing stabilized soil blocks for low-carbon walls, with a simple soil test kit to choose mixes.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Steel mold box and lid
- Lever and toggle linkage
- Ejection mechanism
- Frame on skids
- Soil sieve and test kit
- Block gauge

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> High lever forces: keep hands clear of the mold and linkage, and use two-person lifting for blocks and the press.

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Extending strong areas set.
