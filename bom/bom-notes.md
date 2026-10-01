# BOM notes

- Rows 1 to 10 match the numbered callouts in `media/exploded.png`. Rows 11 to 13 (hardware and finish, consumables, linkage guard) have no callout.
- Every line is priced. Unit costs are indicative USD prices for a TRL 3 design, based on mild steel at about $1.30/kg plus cutting, and bought turned pins, shafts and bushes. Steel masses come from the model (`cad/src/model.py`, EPR-CAL-001 section 8). They are to be replaced with local quotes before any build.
- Total of rows 1 to 13: **$520**, which is $20 over the $500 `budget_usd` in `project.yaml` (R13 not met on paper). Amish raised the budget from $450 to $500 on 2026-09-25 (EPR-DDR-001 item 14, EPR-DDR-002). Raising it to $520 is open decision 2 in the design decisions register (`docs/06-design-decisions.md`); `budget_usd` is unchanged.
- Changes for the constructable design (2026-10-01, EPR-DDR-003, $488 to $520): tapped mold flanges and hinge and latch lugs, lid pins in rib ears, round-ended links with spacers, piston end skirts, larger base plate, bolted tie tabs, rest catch and end pawl, cranked eject arm, lever locking pin, modelled linkage guard, more fixings.
- Changes from TRL 2 ($403): heavier frame with a base beam (two bolted pieces), ribbed lid, larger toggle pins and links with case-hardened bushes, 2 in lever pipe with a T-handle, eject seesaw and end pawl, 10 kg scale in the test kit, and the linkage guard.
- Not included: welding labor, cement, water, soil, curing covers and transport.
- The loose soil and the stack of blocks in the renders are context only and are not BOM lines.
