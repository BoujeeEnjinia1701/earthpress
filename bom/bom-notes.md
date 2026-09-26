# BOM notes

- Rows 1 to 10 match the numbered callouts in `media/exploded.png`. Rows 11 to 13 (hardware and finish, consumables, linkage guard) have no callout.
- Every line is priced. Unit costs are indicative USD prices for a TRL 3 design, based on mild steel at about $1.30/kg plus cutting, and bought turned pins, shafts and bushes. Steel masses come from the model (`cad/src/model.py`, EPR-CAL-001 section 8). They are to be replaced with local quotes before any build.
- Total of rows 1 to 13: **$488**, which is $38 over the $450 `budget_usd` in `project.yaml` (R13 not met). The TRL 3 review recommends raising the budget to $500; that figure is awaiting Amish and `budget_usd` is unchanged (EPR-DDR-001 item 14). Against $500 the BOM would be $12 under.
- Changes from TRL 2 ($403): heavier frame with a base beam (two bolted pieces), ribbed lid, larger toggle pins and links with case-hardened bushes, 2 in lever pipe with a T-handle, eject seesaw and end pawl, 10 kg scale in the test kit, and the linkage guard.
- Not included: welding labor, cement, water, soil, curing covers and transport.
- The loose soil and the stack of blocks in the renders are context only and are not BOM lines.
