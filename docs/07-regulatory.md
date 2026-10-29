---
doc_id: EPR-REG-001
title: EarthPress regulatory and standards register
project: EarthPress
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First regulatory and standards register (kit 1.8 pipeline); sources checked 2026-10-25
---

# EarthPress regulatory and standards register

Which standards and regulations apply, where, and what is needed. Not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. Two families matter: the rules for the **blocks** (earthen building codes and block standards, which set strength and testing and differ by country) and the rules for the **press** as hand-operated machinery (guarding, ergonomics and, if it is ever sold in a regulated market, machinery law). EarthPress makes no claim that its blocks comply with any code; structural use needs local block tests and an engineer (PRC safety notes). Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | 14.7.4 NMAC, New Mexico Earthen Building Materials Code (2021) | New Mexico, United States | Adobe, rammed earth and compressed earth blocks: 300 psi (about 2.1 MPa) compressive strength, 50 psi modulus of rupture, five random units tested per project | Strength reference for PR-003; applies to blocks used in New Mexico, not to the press | Co-design partner and project engineer | Applies to blocks where used; tests at TRL 4 |
| G2 | IS 1725:2023, Stabilized soil blocks used in general building construction, specification (replaces IS 1725:2013) | India | Requirements and tests for stabilized soil blocks | The first candidate partner is in India (EPR-DEC-001, 2026-10-02); strength classes and tests for PR-003 | Co-design partner | To assess (standard not yet read) |
| G3 | ARSO WD-ARS 1333:2018, Compressed stabilized earth blocks: requirements, production and construction | African Organisation for Standardisation member states | Block requirements, production and construction | Reference for programs in sub-Saharan Africa; status of adoption per country to check | Co-design partner | To assess (working draft; adoption to check) |
| G4 | ASTM E2392/E2392M-24, Standard guide for design of earthen wall building systems | International (ASTM) | Design guidance for earthen walls, including compressed earth blocks | Guidance for structural use of the blocks, not the press | Project engineer | To assess |
| G5 | DRS 514-1:2022, Compressed earth blocks, part 1: definitions, classification and specifications (draft Rwanda standard; parts 2 to 4 also published as drafts) | Rwanda | CEB types, requirements, test methods and conformity criteria; excludes earthquake, flood and cyclone-prone areas | Example of a national CEB standard in East Africa | Co-design partner | To assess |
| G6 | ISO 12100, Safety of machinery: general principles for design, risk assessment and risk reduction | International | Hazard identification and risk reduction method | Method used for the hazard analysis in EPR-RSK-001 | Design lead | Applies as method; met by design at TRL 3 (RSK) |
| G7 | ISO 13857, Safety of machinery: safety distances to prevent hazard zones being reached by upper and lower limbs | International | Guard opening sizes and reach distances | Linkage guard openings (12 mm or less, BLD-001) and the 100 mm pinch clearance in PR-012 | Design lead | To assess (openings to check against the standard's tables) |
| G8 | Regulation (EU) 2023/1230 on machinery | European Union | Essential health and safety requirements and conformity assessment for machinery placed on the EU market | Only if a press is placed on the EU market; an open design built by its user is outside the plan at TRL 3 | Amish (decision) | To assess, only if sold in the EU |
| G9 | ISO 11228-1 and ISO 11228-2, Ergonomics: manual handling (lifting and carrying; pushing and pulling) | International | Recommended limits for lifting (reference mass 25 kg) and for push and pull forces | Lifting the press pieces (44.5 kg by two) and the lever force (PR-005); STM S5, S21 | Design lead | Lifting met on paper (S21); pull force to assess against ISO 11228-2 |
| G10 | 29 CFR 1926.1153, Respirable crystalline silica in construction (OSHA) | United States | Permissible exposure limit 50 ug/m3 over 8 h and control measures | Sieving dry soil; damp sieving and FFP2 or N95 respirators specified (PRC, BLD); other countries have their own limits | Site lead | Applies where used in the United States; controls stated; no exposure claim |
| G11 | National cement handling and PPE rules; cement safety data sheets | Every jurisdiction | Skin and eye hazards of wet cement | Gloves and eye protection specified (PRC, BLD) | Site lead | Applies; controls stated |
| G12 | CERN-OHL-S-2.0 and MIT licenses; REUSE | International | Open hardware and software licensing | The repo's licenses (`REUSE.toml`) | Amish | Met by design |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- New Mexico Commission of Public Records, 14.7.4 NMAC, https://www.srca.nm.gov/parts/title14/14.007.0004.html, accessed 2026-10-25.
- Bureau of Indian Standards, IS 1725:2013 details (withdrawn, replaced by IS 1725:2023), https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/Indian_standards/isdetails/NDQ4, accessed 2026-10-25; IS 1725:2023 listing, https://shop.standards.ie/en-ie/standards/is-1725-2023-191237_saig_bis_bis_3262347, accessed 2026-10-25.
- Global ABC Sustainable Materials Hub, "African Standard WD-ARS 1333:2018 Compressed stabilized earth blocks," https://globalabc.org/sustainable-materials-hub/resources/african-standard-wd-ars-13332018-compressed-stabilized-earth, accessed 2026-10-25.
- ANSI Webstore, ASTM E2392/E2392M-24, https://webstore.ansi.org/standards/astm/astme2392e2392m24, accessed 2026-10-25.
- Rwanda Standards Board, DRS 514-1:2022, https://www.rsb.gov.rw/fileadmin/user_upload/files/pictures/DRS_514-1_2022.pdf, accessed 2026-10-25 (parts 2 to 4 listed at the same address, not read).
- OSHA, "Silica, Crystalline: Construction," https://osha.gov/silica-crystalline/construction-info, accessed 2026-10-25.
- ISO 12100, ISO 13857, ISO 11228-1, ISO 11228-2 and Regulation (EU) 2023/1230 are cited by number and title; their texts were not read for this register.
