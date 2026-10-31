---
doc_id: EPR-PLN-001
title: EarthPress project plan
project: EarthPress
doc_type: Project plan
version: "0.2"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First project plan (kit 1.8 pipeline) at stage P3, with the reference list for the repo
- version: "0.2"
  date: '2026-10-30'
  author: Amish Chadha
  change: "D2 decided on 2026-10-30; D1 and the design load question remain with Amish"
---

# EarthPress project plan

EarthPress is at stage P3 (design outputs, TRL 3): the lever and toggle press is calculated, modelled at detail level D3 with its two alternative concepts, drawn, priced and planned. The next gate, P4 (verification, TRL 4), is on hold under the portfolio cap. Decided on 2026-10-30: the R7 mass total (D2, set at 205 kg). Still requested from Amish: the concept selection (D1, three options within 10 %, no pick) and the design load question. Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Concept and STEM check | Design lead | EPR-STM-001, EPR-OPT-001, EPR-DDR-004 | Done at P3; STEM check open on soil data (S2, S6, S18); D1 awaiting Amish |
| Requirements and traceability | Design lead | EPR-URS-001, EPR-PRS-001, EPR-RTM-001 | Done at P3; to validate with users |
| Calculation and design | Design lead | EPR-CAL-001, `cad/src/model.py`, drawings EPR-DWG-001 and 101 to 115 | Done at P3 (fix F1 applied); D2 decided 2026-10-30 |
| Build plan and BOM | Design lead | EPR-BLD-001, `bom/bom.csv` | Done at P3 |
| Regulatory, risk, market | Design lead | EPR-REG-001, EPR-RSK-001, EPR-MKT-001 | First pass done; standards marked "to assess" |
| Co-design partner | Amish | Partner agreement, co-design sessions | Not started (candidate decided 2026-10-02) |
| Renders and storefront | Coordinator on Amish's Mac | Options picture, product renders, cards | Waiting for the Mac render |
| Verification (P4) | Fabricator and partner | Prototype build, soil compaction test, block tests, proof load | On hold (portfolio cap P3) |

## Resources needed

Table 2. Resources (P4 onward is on hold; estimates are indicative).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Design lead | P3 upkeep, decision D1 and the design load question carried through once decided | 1 to 2 days | Not costed |
| Local welding shop (P4, on hold) | One prototype press to EPR-BLD-001 | About 5 shop days | 542 parts plus labor (labor not estimated) |
| Co-design partner (P4, on hold) | Soil compaction curves, timed cycles, user feedback | 2 to 4 weeks | To assess |
| Testing laboratory (P4, on hold) | Block compressive and wet strength to PR-003 | 1 batch | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB, STM, OPT, REG, FEA, PLN | Met (2026-10-25) |
| P1 Definition | URS, PRS, RSK with hazard analysis, MKT | Met (2026-10-25) |
| P2 Design inputs | PRS with targets and verification, CAL, RTM, concept DDR, STEM and feasibility closed | Met except the STEM check, open on soil data (repo kept at TRL 3 under STANDARDS section 20) and the concept decision D1 |
| P3 Design outputs | Model, STEP, drawings, priced BOM, BLD, DEC, design FMEA, traceability complete | Met (2026-10-25); CAD fidelity D3 for every option |
| P4 Verification | Prototype, test plans and reports, verification report | On hold |
| P5 Validation | Field trials with a partner | On hold |
| P6 Commercialization | Only with a named deployment partner | On hold |

## Next steps and decision requested

1. Amish: decide D1 (concept: A, B or C; all within 10 %, no pick) and the design load question (1,000 N or 1,500 N abuse case). D2 (R7 total of 205 kg) was decided on 2026-10-30.
2. Coordinator: render the options picture and the product renders on the Mac (`python .kit/options.py`, `.kit/export_views.py`, `.kit/photoreal.py`, `.kit/cards.py`).
3. When the cap allows TRL 4: approach the partner, measure the soil compaction curve (closes STM S6), build the prototype, and test blocks (closes S2, S18).

## References

Every source cited in this repo's documents.

- Auroville Earth Institute. "Compressed Stabilised Earth Block." Accessed 2026-10-25. https://www.earth-auroville.com/compressed_stabilised_earth_block_en.php.
- Auroville Earth Institute. "Specifications of the Press 3000." Accessed 2026-10-25. https://www.earth-auroville.com/specifications_of_the_press_3000_en.php.
- Botti. Article on the CINVA-Ram and self-help housing. *Frontiers of Architectural Research*, 2023. https://www.sciencedirect.com/science/article/pii/S2095263523000584 (as cited in the README; title not rechecked).
- Budynas, Richard G., and J. Keith Nisbett. *Shigley's Mechanical Engineering Design*. New York: McGraw-Hill.
- Bureau of Indian Standards. IS 1725:2013 and IS 1725:2023, *Stabilized Soil Blocks Used in General Building Construction: Specification*. Accessed 2026-10-25. https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/Indian_standards/isdetails/NDQ4.
- Chatham House. *Making Concrete Change: Innovation in Low-Carbon Cement and Concrete*. 2018. https://www.chathamhouse.org/2018/06/making-concrete-change-innovation-low-carbon-cement-and-concrete.
- Construction Kenya. Soil block press article. 2024-01-23. Accessed 2026-10-25. https://www.constructionkenya.com/?p=4970.
- Engineering for Change. "Makiga Stabilized Soil Block Press." Updated 2024-03-04. Accessed 2026-10-25. https://www.engineeringforchange.org/solutions/product/makiga-stabilized-soil-block-press/.
- Global ABC Sustainable Materials Hub. "African Standard WD-ARS 1333:2018 Compressed Stabilized Earth Blocks." Accessed 2026-10-25. https://globalabc.org/sustainable-materials-hub/resources/african-standard-wd-ars-13332018-compressed-stabilized-earth.
- IARC. *Arsenic, Metals, Fibres, and Dusts*. IARC Monographs 100C. Lyon: IARC, 2012.
- Natural Building Blog. Post on compressed earth block presses. Accessed 2026-10-25. https://naturalbuildingblog.com/?p=2586.
- Neville, A. M. *Properties of Concrete*. Harlow: Pearson.
- New Mexico Commission of Public Records. 14.7.4 NMAC, *Earthen Building Materials Code*. Accessed 2026-10-25. https://www.srca.nm.gov/parts/title14/14.007.0004.html.
- Open Source Ecology. "CEB Press." https://wiki.opensourceecology.org/wiki/CEB_Press.
- OSHA. "Silica, Crystalline: Construction." Accessed 2026-10-25. https://osha.gov/silica-crystalline/construction-info.
- Rwanda Standards Board. DRS 514-1:2022, *Compressed Earth Blocks, Part 1*. Accessed 2026-10-25. https://www.rsb.gov.rw/fileadmin/user_upload/files/pictures/DRS_514-1_2022.pdf.
- Swiss Steel Group. "42CrMoS4" data sheet. Accessed 2026-10-25. https://swisssteel-group.com/content-media/documents/Data-Sheets/Engineering-Steel/42CrMoS4_en.pdf.
- UNEP. *Global Status Report for Buildings and Construction 2024/2025*. https://www.unep.org/resources/report/global-status-report-buildings-and-construction-20242025.
- UN-Habitat. "Housing." https://unhabitat.org/topic/housing.
- United Nations. *The Sustainable Development Goals Report 2024*, Goal 11. https://unstats.un.org/sdgs/report/2024/Goal-11/.
- Standards cited by number and title: ASTM D698; ASTM E2392/E2392M-24; EN 1993-1-9; ISO 11228-1; ISO 11228-2; ISO 12100; ISO 13857; Regulation (EU) 2023/1230; 29 CFR 1926.1153.
