---
doc_id: EPR-MKT-001
title: EarthPress market and viability
project: EarthPress
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First market and viability note (kit 1.8 pipeline); prices checked 2026-10-25
---

# EarthPress market and viability

EarthPress is for self-builders, small block yards and NGO building programs who need walling from site soil without power, competing with closed manual presses sold at roughly USD 800 to 1,000 and with open hydraulic designs costing several thousand dollars in materials. Its case is not the lowest price, which it is near, but that it is open and dimensioned, so a local welder can build and repair it and the soil kit and mix guidance travel with it. Prices and benchmarks are cited with the date they were checked; EarthPress's own cost is the indicative BOM (USD 542, parts only). Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Self-build and community housing | Families and cooperatives in sub-Saharan Africa, South Asia and Latin America | Makiga manual soil block press, 290 x 140 mm blocks, about 500 a day with four workers, 130 kg: USD 996.52 suggested retail ([Engineering for Change](https://www.engineeringforchange.org/solutions/product/makiga-stabilized-soil-block-press/), updated 2024-03-04, checked 2026-10-25) | 542 in parts plus local welding labor (not estimated) | Built locally from drawings; repairable; soil kit and mix chart included |
| Small block yards | Enterprises selling blocks to local builders | Star Top manual presses, USD 800 to 900 ([Natural Building Blog](https://naturalbuildingblog.com/?p=2586), undated post, checked 2026-10-25); Auram press 3000, 2.7 to 5.3 MPa, about 850 blocks a day with seven people, price not published ([Auroville Earth Institute](https://www.earth-auroville.com/specifications_of_the_press_3000_en.php), checked 2026-10-25) | 542 | Lower output than the Auram (about 296 a day with four) but buildable and repairable without a supplier |
| NGO and humanitarian programs | Reconstruction and training programs | Kenya soil block press about KSh 100,000 ([Construction Kenya](https://www.constructionkenya.com/?p=4970), dated 2024-01-23, checked 2026-10-25); Open Source Ecology CEB Press, hydraulic, USD 3,000 to 6,500 in materials ([OSE wiki](https://wiki.opensourceecology.org/wiki/CEB_Press), cited in the README) | 542 | Open documentation for many sites; no hydraulics or engine to maintain |
| Vocational education | Technical colleges teaching earth building and fabrication | Same benchmarks | 542 | A complete, calculated design to build as a class project, with a build plan |
| Low-carbon building in high-income countries | Architects and owner-builders where earthen codes allow CEB (for example New Mexico) | Same benchmarks plus shipping | 542 | Open design; blocks tested against the local code (EPR-REG-001) |

The BOM covers parts only; welding labor, cement and transport are excluded. Converting the Kenyan shilling price needs a dated exchange rate and is not done here.

## Open route

The press spreads as drawings, not as a product: a local welding shop builds it from the CERN-OHL-S drawings, BOM and build plan (EPR-BLD-001), and a training partner (first candidate: the Auroville Earth Institute, decided 2026-10-02) teaches soil testing and pressing. Vocational colleges and NGO programs are the likely first builders, since they can build several presses and train crews. What keeps it open: the CERN-OHL-S-2.0 license (changes to the hardware stay open), the MIT license on the scripts, the parametric model (`cad/src/model.py`) so a builder can change sizes and rerun the checks, and the REUSE and archive records (Zenodo, Software Heritage). No commercial route is planned at TRL 3; any sale or partnership is Amish's decision.

## Sources

- Engineering for Change, "Makiga Stabilized Soil Block Press," https://www.engineeringforchange.org/solutions/product/makiga-stabilized-soil-block-press/, accessed 2026-10-25.
- Natural Building Blog, post 2586 on compressed earth block presses, https://naturalbuildingblog.com/?p=2586, accessed 2026-10-25.
- Auroville Earth Institute, "Specifications of the Press 3000," https://www.earth-auroville.com/specifications_of_the_press_3000_en.php, accessed 2026-10-25.
- Construction Kenya, soil block press article, https://www.constructionkenya.com/?p=4970, accessed 2026-10-25.
- Open Source Ecology, "CEB Press," https://wiki.opensourceecology.org/wiki/CEB_Press (as cited in the README and EPR-PRB-001).
