---
doc_id: EPR-STM-001
title: EarthPress STEM check
project: EarthPress
doc_type: STEM check
version: "0.2"
status: Draft
date: '2026-10-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First STEM check (kit 1.8 pipeline, run during the kit 1.9.1 upgrade) for the current design (option A) and options B and C; S9 and S10 failed on the 35 mm C45 toggle pins and were closed by fix F1 under the standing instruction of 2026-10-23; independent review recorded
- version: "0.2"
  date: '2026-10-30'
  author: Amish Chadha
  change: "R7 total of 205 kg (decision D2, 2026-10-30)"
---

# EarthPress STEM check

Verdict: compacting moist, cement-stabilized soil into a 290 x 140 x 90 mm block at 2 MPa with a two-person lever and toggle press sits within known physics, chemistry and biology, and no row fails. Two rows failed when first run, both on the toggle pins: the 35 mm C45 base pin yielded in bending at the nominal 81.2 kN (388 MPa against 370 MPa) and the 20 mm base pin lugs exceeded the bush bearing allowable at the 173 kN design load. Both were closed by fix F1 (40 mm 42CrMo4 +QT pins, 28 mm lugs; EPR-DEC-001), decided on 2026-10-25 under Amish's standing instruction of 2026-10-23. Of 35 rows, 23 are within known science and 12 are plausible, to confirm, so `stem_check` is **open**: for option A the soil compaction law (S6), the block strength at 2 MPa (S2), the lime dose (S18), the operator force and eject force (S5, S14), the fill scale (S8) and the team lift (S21) need measurements or assessment on partner soils, which are TRL 4 work and on hold. Method: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py`, which takes option A's numbers from EPR-CAL-001 (`docs/04-calcs/sizing.py`).

## Claims checked

Table 1. Claims, governing science and verdicts (generated from `docs/04-calcs/stem_results.csv`; rows S are option A, the current design; B and C are the other concept options).

<!-- STM_TABLE -->
| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | The press needs 81.2 kN on the 290 x 140 mm block face for 2 MPa | Mathematics | Units and dimensional analysis | F = p A | claimed 81.2 kN, estimate 81.2 kN (ratio 1.00) | Within known science | EPR-CAL-001 |
| S2 | Compacting a 5 % cement mix to 2 MPa gives blocks that can meet the R3 strength class with suitable soil | Physics | Mechanics and statics | Auroville Earth Institute: CSEB pressed at 2 to 4 MPa with about 5 % cement; the Auram press 3000 works at 2.7 to 5.3 MPa | 2 MPa is the low end of practice; strength depends on soil, mix and curing and is measured in block tests (TRL 4, on hold) | Plausible, to confirm at TRL 3 | Open |
| S3 | The lever and toggle give a force ratio of 173:1 at the crank stop | Physics | Mechanics and statics | Toggle 1 / (2 tan 6 deg) times grip radius over the connecting link's arm (virtual work) | claimed 173 :1, estimate 201 :1 (ratio 0.86) | Within known science | EPR-CAL-001 |
| S4 | Two people on the 1.71 m grip path supply the compaction work of the softer design soil | Physics | Mechanics and statics | Conservation of energy or mass | in 1710 J, out 705 J | Within known science | EPR-CAL-001 |
| S5 | Each of two operators pulls no more than 500 N at the peak, with the softer design soil | Biology | Ergonomics | Peak grip force from the force ratio and the soil law (CAL section 4b); project limit 500 N per operator (R5, PR-005); ISO 11228-2 screening to assess | 405 N against 500 N, but it rests on the assumed soil law (S6) and on equal shares between the two operators; measure on partner soils | Plausible, to confirm at TRL 3 | Open |
| S6 | Soil pressure in the mold rises tenfold over the last 14 mm of the stroke (10 to 20 mm) | Physics | Mechanics and statics | Assumed exponential compaction law; no measured curve for the partner's soils | Measure pressure against travel on partner soils (compaction test); S4, S5 and the fill window rest on it | Plausible, to confirm at TRL 3 | Open |
| S7 | Every load-path member stays below yield at the 173 kN design load (1,000 N at the grip at the stop) | Physics | Strength of materials | Bending, shear, bearing, net section and buckling against yield of S235/S250 plate, A53 pipe and 42CrMo4 +QT pins (CAL Table 5) | 1 of yield <= 1.29 of yield | Within known science | EPR-CAL-001 |
| S8 | A 10 kg scale with 50 g divisions can hold the fill to its window of 0 to +206 g | Engineering and technology | Sensing resolution | Scale division against half the fill window (CAL section 5) | 50 g division against a half-width of 103 g for the base soil, but the softer design soil has a window of about 0 to +153 g (half-width 76 g), a division is not the scale's accuracy (a low-cost 10 kg scale is about 50 to 100 g) and a 1 % moisture swing moves the dry mass by about 70 g: confirm scale accuracy and moisture control | Plausible, to confirm at TRL 3 | Open |
| S9 | The 40 mm 42CrMo4 +QT toggle pins stay below yield in bending at the 173 kN design load | Physics | Strength of materials | Pin in a clevis: link force per side times the distance between bearing centres (base pin 36 mm arm), M / (pi d^3 / 32) against Rp0.2 750 MPa for 16 < d <= 40 mm; the 35 mm C45 pins of CAL v0.6 failed (388 MPa against 370 MPa at the nominal load, 826 MPa at 173 kN) | 498 MPa <= 750 MPa | Within known science | EPR-DEC-001 F1 (2026-10-25, standing instruction) |
| S10 | The base pin lugs carry the design load within the bush bearing allowable | Physics | Strength of materials | Bearing p = F / (2 t d) on 2 x 28 mm lugs at 40 mm, allowable 100 MPa for hardened greased bushes (assumed); the 20 mm lugs on 35 mm reached 124 MPa | 78 MPa <= 100 MPa | Within known science | EPR-DEC-001 F1 (2026-10-25, standing instruction) |
| S11 | Welded members last 50,000 blocks in fatigue | Physics | Strength of materials | Nominal stress range per block against a FAT 71 detail at 50,000 cycles (EN 1993-1-9 method) | 89 MPa <= 243 MPa | Within known science | EPR-CAL-001 |
| S12 | The turned toggle pins last 50,000 blocks in bending fatigue | Physics | Strength of materials | Pulsating range against 0.5 Rm x 0.7 for surface and size (Rm 1,000 MPa minimum, 42CrMo4 +QT; first-order) | 234 MPa <= 350 MPa | Within known science | EPR-CAL-001 |
| S13 | Released at the stop, the lever kicks back with about 47 J | Physics | Mechanics and statics | Strain energy 0.5 F d with 1.0 mm soil rebound (assumed) and the column stretch | claimed 47 J, estimate 47.1 J (ratio 1.00) | Within known science | EPR-CAL-001 |
| S14 | One person ejects the block with 470 N or less on the eject lever | Physics | Mechanics and statics | Wall friction 0.1 MPa residual lateral pressure x 0.6 x wall area, plus piston and block weight, over the 10.3:1 eject ratio (assumed residual pressure) | 469 N against 500 N, a margin of about 6 % that rests on the assumed 0.1 MPa residual pressure (at 0.2 MPa the force would be about 930 N): measure on partner soils | Plausible, to confirm at TRL 3 | Open |
| S15 | A crew of four makes about 296 blocks in an 8 h day | Mathematics | Orders of magnitude | Makiga manual press, 290 x 140 mm blocks, about 500 a day with a crew of four (Engineering for Change); EarthPress cycle 85 s assumed (CAL section 9) | claimed 296 blocks, estimate 500 blocks (ratio 0.59) | Within known science | Open |
| S16 | Curing blocks bind about 0.23 kg of water per kg of cement | Chemistry | Physical chemistry | Non-evaporable water of fully hydrated Portland cement about 0.23 g/g (Powers and Brownyard; Neville, Properties of Concrete) | Used only for the cured mass in the flow figure; 712 kg per 100 blocks | Within known science | EPR-CAL-001 |
| S17 | CSEB walling embodies 25 % or less of the CO2 of fired brick of equal volume | Chemistry | Environmental and atmospheric chemistry | Auroville Earth Institute factors: 49 kg CO2/m3 for 5 % CSEB, 643 kg CO2/m3 for locally fired brick | 7.6 % <= 25 % | Within known science | EPR-CAL-001 |
| S18 | Lime at about 8 % stabilizes clay-rich soils, with a longer curing period than cement | Chemistry | Inorganic chemistry | Lime and clay react slowly (cation exchange, then pozzolanic calcium silicate and aluminate hydrates); needs enough clay and moisture | Starting value only; wet-strength tests on partner soils decide the dose and the curing time (TRL 4, on hold) | Plausible, to confirm at TRL 3 | Open |
| S19 | Sieving dry soil raises respirable crystalline silica, so damp sieving and an FFP2 or N95 respirator are specified | Biology | Toxicology | Crystalline silica is carcinogenic to humans (IARC Group 1, Monograph 100C); OSHA PEL 50 ug/m3 over 8 h (29 CFR 1926.1153) | Hazard and controls stated in PRC, BLD and RSK; no exposure claim is made | Within known science | EPR-RSK-001 |
| S20 | Wet cement can burn skin and eyes, so gloves and eye protection are specified | Biology | Toxicology | Portland cement safety data sheets: causes skin irritation and serious eye damage (hazard statements H315, H318); wet mix is strongly alkaline | Hazard and controls stated in PRC, BLD and RSK | Within known science | EPR-RSK-001 |
| S21 | Two people can lift the heaviest piece of the press | Biology | Ergonomics | ISO 11228-1 reference mass 25 kg per person for occasional lifts; two people share the piece | 22.2 kg per person if the load halves exactly, but team lifting usually reduces each person's share of the capacity and the 25 kg figure is for ideal conditions: to assess; lift with a trolley, a hoist or four people | Plausible, to confirm at TRL 3 | Open |
| S22 | The grip stays at 0.8 m or higher through the stroke, with the peak force at 1.0 m or higher | Biology | Ergonomics | Lever kinematics (CAL section 3); R5 band | 800 mm <= 863 mm | Within known science | EPR-CAL-001 |
| S23 | The mold walls bulge far less than the 2 mm block tolerance at 2 MPa | Physics | Strength of materials | Fixed-fixed wall strip with the belt, lateral pressure 0.5 x vertical (assumed K0) | 0.078 mm <= 2 mm | Within known science | EPR-CAL-001 |
| B1 | Option B: two people on a 1.2 m capstan turn the screw at the 81 kN pressing force within 500 N each | Physics | Mechanics and statics | Power screw torque T = F d2 / 2 tan(lambda + phi'), lambda 7.0 deg, phi' 8.8 deg (mu 0.15), T 430 N m; grips 0.53 m from the axis | 406 N <= 500 N | Within known science | Open |
| B2 | Option B: the two-start screw is self-locking, so it holds the load without a pawl | Physics | Mechanics and statics | Self-locking when the lead angle is below the friction angle | lambda 7.0 deg against phi' 8.8 deg at mu 0.15 but 5.9 deg at mu 0.10 (well greased): not self-locking when greased; a brake or a single-start screw would be needed | Plausible, to confirm at TRL 3 | Open |
| B3 | Option B: a 90 mm bronze nut carries the pressing force within its bearing allowable | Physics | Strength of materials | Thread bearing p = F / (pi d2 H1 n); hand press, steel screw on bronze nut, 17 to 24 MPa (Shigley, Table 8-4) | 15.7 MPa <= 17 MPa | Plausible, to confirm at TRL 3 | Open |
| B4 | Option B: the screw's root section stays below yield at the largest force two people can make | Physics | Strength of materials | Root diameter 32 mm; two people at 500 N on 0.53 m give the largest force; C45 yield 340 MPa (first-order) | 128 MPa <= 340 MPa | Within known science | Open |
| B5 | Option B: a crew of four makes about 225 blocks a day | Mathematics | Orders of magnitude | Makiga manual press about 500 a day (Engineering for Change); option B cycle 111 s with 14 unloaded turns each way (227 a day) | claimed 225 blocks, estimate 500 blocks (ratio 0.45) | Within known science | Open |
| B6 | Option B: the operators supply the pressing work through a screw of about 43 % efficiency | Physics | Mechanics and statics | Conservation of energy or mass | in 1.432e+04 J, out 1633 J | Within known science | Open |
| C1 | Option C: about 25 blows of a 20 kg weight falling 450 mm give standard Proctor compaction energy | Physics | Mechanics and statics | ASTM D698 standard effort 592.7 kJ/m3 over the 3.65 L block; blow energy m g h | claimed 25 blows, estimate 24.5 blows (ratio 1.02) | Within known science | Open |
| C2 | Option C: impact compaction at standard Proctor effort reaches the density of 2 MPa static pressing | Physics | Mechanics and statics | Impact and static compaction give different density profiles; impact from the top densifies the top layer most | No source equates the two for CSEB; test blocks needed | Plausible, to confirm at TRL 3 | Open |
| C3 | Option C: each of two people pulls under 500 N on the rope, even when lifting the plunger for filling | Biology | Ergonomics | Weight, rod and plunger about 40 kg, shared by two over the head pulley | 196 N <= 500 N | Within known science | Open |
| C4 | Option C: the operators' sustained power stays within human capacity | Biology | Human physiology and biomechanics | 25 blows of 88 J in 100 s, shared by two; sustained adult output about 75 W | 11 W <= 75 W | Within known science | Open |
| C5 | Option C: a crew of four makes about 160 blocks a day | Mathematics | Orders of magnitude | Makiga manual press about 500 a day (Engineering for Change); option C cycle 160 s (25 blows at 15 a minute plus 60 s) | claimed 160 blocks, estimate 500 blocks (ratio 0.32) | Plausible, to confirm at TRL 3 | Open |
| C6 | Option C: the mold, plunger and floor stop survive the impact peak force | Physics | Strength of materials | Impact force depends on the soil's stiffness at the end of compaction, not yet known | To be estimated from a measured soil stiffness (S6) | Plausible, to confirm at TRL 3 | Open |
<!-- /STM_TABLE -->

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails, fix proposed**, **Fails**.

### Rows closed by a fix

| Row | First run (CAL v0.6 design) | Fix | Rerun |
| --- | --- | --- | --- |
| S9 | Fails, fix proposed: 35 mm C45 base pin in bending, 388 MPa against 370 MPa at 81.2 kN and 826 MPa at 173 kN (arm 40 mm from the link to the lug); knee and upper pins 661 and 641 MPa at 173 kN | F1: 40 mm 42CrMo4 +QT pins (Rp0.2 750 MPa), lugs grown to 28 mm so the arm falls to 36 mm (EPR-DEC-001, 2026-10-25, standing instruction) | Within known science: 498 MPa (base), 463 MPa (knee, with the connecting link), 429 MPa (upper) against 750 MPa at 173 kN |
| S10 | Fails, fix proposed: 2 x 20 mm lugs on a 35 mm pin, 124 MPa against 100 MPa at 173 kN | F1: 2 x 28 mm lugs on the 40 mm bush bore | Within known science: 78 MPa |

The fix keeps the working principle, the linkage geometry and the pitch; it is not a decision for Amish under the fix rule, but he can reverse it. It adds about 1.2 kg and about USD 19 (estimate), which takes the press to 203.8 kg against the 205 kg R7 total decided on 2026-10-30 (decision D2) and the BOM to USD 542.

## Fields not relevant

- Physics, electromagnetism and circuits, optics and radiation, nuclear and ionising radiation: no electrical parts, light or radiation sources; the press is hand powered (PR-015).
- Physics, thermodynamics and heat transfer: no heat process; cement hydration heat in a 90 mm block cured in shade is negligible for the press.
- Biology, microbiology, ecology and agronomy, epidemiology: no living material is used; soil with organic matter is screened out by the field tests (PR-009). Toxicology (S19, S20) and ergonomics (S5, S21, S22) are covered.
- Engineering and technology, power and link budgets, control: no powered or controlled parts.

## Concept options

- Option A, lever and toggle press (the current design): rows S1 to S23; within known science after fix F1; open on S2, S6 and S18 (partner soil data).
- Option B, power screw press: within known science on force, thread bearing, screw strength, energy and output (B1, B3 to B6); plausible on self-locking (B2: the lead angle of a two-start Tr 40 x 14 screw is 7.0 deg against a friction angle of 8.8 deg at a friction coefficient of 0.15 but 5.9 deg at 0.10, so a greased screw may run back and would need a brake or a single-start screw) and on the nut, which is within 8 % of its bearing allowable (B3).
- Option C, rope-lifted drop rammer: within known science on blow count, rope pull and sustained power (C1, C3, C4); plausible on whether impact compaction reaches the density of 2 MPa static pressing (C2), on output, about 160 blocks a day, just under a third of the benchmark (C5), and on the impact force in the mold (C6).

No option has a Fails row, so none is dropped.

## Independent review

The reviewer (claude-opus-5-5, run headless, shown only the STEM check, CAL, PRS and the two scripts) found nothing blocking and recomputed S1, S9, S10 (arithmetic), S15 to S16, S19, S20, S22, S23, B1 to B6 and C1, C3, C4 as holding. Findings and what was done under the fix rule:

- **S5 (operator force), S8 (scale), S14 (eject force), S21 (team lift): downgraded to Plausible, to confirm.** S5 rests on the assumed soil law (S6) and equal shares; S8 used the base soil's half-width (103 g) while the design soil's window is about 76 g and a 50 g division is not scale accuracy; S14 has a 6 % margin on an assumed 0.1 MPa residual pressure (930 N at 0.2 MPa); S21 assumed that two people halve the load exactly. The script and Table 1 now show these as plausible.
- **S3 (force ratio):** the closed-form estimate (201:1, symmetric knee) is 14 % above the 173:1 of CAL, which is the numerical derivative of the modelled linkage kinematics (the lever pivot, link and piston at their real positions, not a symmetric knee). The model is taken as authoritative and the closed form as an upper bound. Not changed; the design load stays at 173 kN. If the real ratio were 201:1 the lugs would reach about 91 MPa and the lowest factor about 1.11, so the linkage geometry should be re-checked in the TRL 4 prototype.
- **Design load basis (S7, S9, S10):** 1,000 N at the grip is two operators at their normal pull; two people hanging body weight (about 1,500 N) would give about 260 kN and exceed the lug allowable. The crank stop and end pawl are not separately checked. Proposed to Amish: either state the abuse case as 1,000 N and add a grip stop that limits the load, or raise the lug and pin sizes again. Not changed because it changes the stated design load and scope (the design load question).
- **S7 yield:** S235 plate is 235 MPa (225 MPa for 16 to 40 mm), not the 250 MPa used. The lowest factor of 1.29 is the base pin lug bearing, not a plate, so the headline holds; the mold wall factor falls from 1.31 to about 1.18. Noted, to correct in CAL v0.8.
- **S11, S12 (fatigue):** no partial factor, nominal load rather than the top of the fill window, no stress concentration at the grease hole, and the lug fillet welds are not checked (FAT 36 to 45). Margins are thin; noted, still "within known science" at first order, to be re-checked with the prototype.
- **S13 (kickback):** not independent of CAL; at the top of the fill window it would be about 80 J. The end pawl takes it either way.
- **S17 (carbon):** the cement count gives about 11 % rather than 7.6 %; the text now says so and R11 is still met.
- **Documents:** CAL has two tables numbered "5b" (to renumber in the next CAL revision).

## Sources

- Auroville Earth Institute, "Compressed Stabilised Earth Block," https://www.earth-auroville.com/compressed_stabilised_earth_block_en.php, accessed 2026-10-25 (compaction 2 to 4 MPa, about 5 % cement; 49 and 643 kg CO2/m3; S2, S17).
- Auroville Earth Institute, "Specifications of the Press 3000," https://www.earth-auroville.com/specifications_of_the_press_3000_en.php, accessed 2026-10-25 (2.7 to 5.3 MPa, 150 kN; S2).
- Engineering for Change, "Makiga Stabilized Soil Block Press," updated 2024-03-04, https://www.engineeringforchange.org/solutions/product/makiga-stabilized-soil-block-press/, accessed 2026-10-25 (about 500 blocks a day with four workers; S15, B5, C5).
- Swiss Steel Group, "42CrMoS4" data sheet (Rp0.2 750 MPa for 16 < d <= 40 mm, +QT), https://swisssteel-group.com/content-media/documents/Data-Sheets/Engineering-Steel/42CrMoS4_en.pdf, accessed 2026-10-25 (S9, S12).
- OSHA, "Silica, Crystalline: Construction," https://osha.gov/silica-crystalline/construction-info, accessed 2026-10-25 (PEL 50 ug/m3, 29 CFR 1926.1153; S19).
- IARC, *Arsenic, Metals, Fibres, and Dusts*, IARC Monographs 100C (Lyon: IARC, 2012) (crystalline silica, Group 1; S19).
- ASTM D698, Standard Test Methods for Laboratory Compaction Characteristics of Soil Using Standard Effort (592.7 kN m/m3; C1).
- R. G. Budynas and J. K. Nisbett, *Shigley's Mechanical Engineering Design*, power screws and thread bearing pressure (Table 8-4) (B1 to B4).
- A. M. Neville, *Properties of Concrete*, non-evaporable water of hydrated cement (S16).
- ISO 11228-1 (lifting, reference mass 25 kg; S21) and ISO 11228-2 (pushing and pulling; S5, to assess).
- EN 1993-1-9, fatigue detail categories (FAT 71; S11).
- EPR-CAL-001 (`docs/04-calcs/01-sizing.md`, `sizing.py`) for every option A number.
