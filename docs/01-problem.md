---
doc_id: EPR-PRB-001
title: EarthPress problem statement
project: EarthPress
doc_type: Problem statement
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
  change: Populate to TRL 2 (users, context, constraints, prior work with sources, open questions)
---

# EarthPress problem statement

Walls made of fired brick or cement block carry high embodied carbon and cost, and the cheaper, lower-carbon alternative, compressed stabilized earth blocks (CSEB), depends on a press that most small builders cannot buy or make. Open press designs exist, but the best documented one is hydraulic and costs thousands of dollars, while the manual lever presses that suit a village building site are sold as closed products or survive as old, undimensioned drawings. EarthPress aims to fill that gap with an open, welder-buildable manual press and a field soil test kit.

## Why it matters

- The buildings and construction sector accounts for about 32 % of global energy use and 34 % of global CO2 emissions ([UNEP, *Global Status Report for Buildings and Construction 2024/2025*](https://www.unep.org/resources/report/global-status-report-buildings-and-construction-20242025)).
- Cement production alone accounts for around 8 % of global CO2 emissions ([Chatham House, *Making Concrete Change*, 2018](https://www.chathamhouse.org/2018/06/making-concrete-change-innovation-low-carbon-cement-and-concrete)).
- UN-Habitat estimates that by 2030 about 3 billion people, about 40 % of the world's population, will need access to adequate housing, or about 96,000 new affordable units every day ([UN-Habitat, Housing](https://unhabitat.org/topic/housing)).
- 1.12 billion people lived in slums or informal settlements in 2022, 130 million more than in 2015 ([UN, *Sustainable Development Goals Report 2024*, Goal 11](https://unstats.un.org/sdgs/report/2024/Goal-11/)).
- The Auroville Earth Institute reports that CSEB stabilized with 5 % cement embody about 548 MJ/m³ and about 49 kg CO2/m³, against about 6,120 MJ/m³ and about 643 kg CO2/m³ for locally fired bricks, that is, about 11 times less energy and 13 times less pollution ([Auroville Earth Institute, CSEB](https://www.earth-auroville.com/compressed_stabilised_earth_block_en.php)).

## Users and context

EarthPress serves people who build small load-bearing or infill walls with the soil on or near their site.

| User | Need | Context |
| --- | --- | --- |
| Self-builders and families | Make their own walling for a one- or two-room house, a store or an extension | Peri-urban and rural sites with clay-sand soil; little cash, plenty of labor |
| Small block-making enterprises | Sell blocks locally as a business | A yard with shade, water and a stock of soil; a crew of three to five |
| NGOs and community builders | Train masons and build schools, clinics or reconstruction housing | Programs in sub-Saharan Africa, South Asia and Latin America |
| Local welders and fabricators | Build, repair and sell the press | A stick welder, angle grinder and drill press; steel from a local stockist |
| Architects and owner-builders in high-income countries | Low-carbon garden walls, studios and small buildings | Places with earthen building codes, such as New Mexico |

The press works outdoors on uneven ground, in dust, heat and rain, and is moved between sites on a pickup or by hand. Operators range from trained masons to first-time volunteers.

## Constraints

- Garage-buildable prototype for about $450 USD in parts (`project.yaml`), with no machining beyond drilling and purchased turned pins.
- Human powered: no electricity, hydraulics or engine on site.
- Parts from local steel stockists: flat bar, plate, channel, rectangular tube and pipe in common sizes.
- Wear parts and pins replaceable with hand tools.
- Movable by four people, or by two people once dismantled.
- Blocks must meet a recognized strength reference for the intended use (for example Auroville class B, or the New Mexico code minimum of 300 psi, about 2.1 MPa) when made from suitable, tested soil.

## Out of scope

- Hydraulic or motorized presses, and block-making plant.
- Structural design of buildings, including seismic design; EarthPress supplies blocks, not building approval.
- Rammed earth, adobe and fired brick.
- Certification of blocks against any national standard (a later-stage activity with a test laboratory).

## Prior work

| Work | What it offers | Gap for EarthPress |
| --- | --- | --- |
| CINVA-Ram, a manual lever press developed in Colombia in the 1950s | The original single-lever, bottom-piston press; widely copied | Low compaction by modern standards; drawings vary and are rarely open-licensed |
| Auroville Earth Institute and its Auram presses (India) | Mature CSEB practice: 5 % cement on average, compaction pressure of 2 to 4 MPa, strength classes; the Auram 3000 makes about 1,000 blocks a day ([Auroville Earth Institute](https://www.earth-auroville.com/compressed_stabilised_earth_block_en.php)) | Commercial presses; not open hardware |
| Open Source Ecology CEB Press | Open hardware (CC BY-SA 4.0, GPLv3), about 6 blocks a minute; materials cost $3,000 to $6,500, about $10,000 assembled ([OSE wiki](https://wiki.opensourceecology.org/wiki/CEB_Press)) | Hydraulic and engine powered; too costly for a self-builder |
| 2021 New Mexico Earthen Building Materials Code, 14.7.4 NMAC | Covers CEB; cured units need 300 psi compressive strength and 50 psi modulus of rupture, with five random units tested per project ([NM Commission of Public Records](https://www.srca.nm.gov/parts/title14/14.007.0004.html)) | A strength target, not a press design |
| Interlocking stabilized soil block (ISSB) presses used in East Africa | Mortar-saving interlocking blocks | Specific block geometries; mostly commercial presses |

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design

## Open questions

- Which block size and shape do local masons prefer: flat 290 x 140 x 90 mm, a larger module or an interlocking block?
- Is a single operator's pull enough to reach 2 MPa in practice, or does the crew need two people on the lever?
- Which soils in the first partner region pass the field tests, and what cement or lime content do they need?
- What block strength do local building rules or funders require, and who will test blocks?
- How far do blocks and the press travel, and on what vehicle?
