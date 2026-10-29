---
doc_id: EPR-RSK-001
title: EarthPress risk register and hazard analysis
project: EarthPress
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: First risk register, preliminary hazard analysis and first-pass design FMEA (kit 1.8 pipeline, stage P3) for option A after fix F1
---

# EarthPress risk register and hazard analysis

The top project risks are that partner soils turn out softer or stiffer than assumed, which moves the operating force and the fill window (R1), and that the press stays over its mass and cost targets (R3, R4). The top hazards are the stored energy at the end of the stroke (lever kickback, about 47 J), crushing in the linkage and the mold, and silica dust and wet cement during mixing. The design FMEA's highest risk priority numbers are the fill weighed outside its window and a worn or missing latch pin. Method: STANDARDS section 23 and the ISO 12100 approach. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection 1 (certain to be detected) to 5 (not detected).

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | Partner soils differ from the assumed compaction law | The law (tenfold over the last 14 mm) is assumed (STM S6) | Peak pull above 500 N per operator or a narrower fill window | 3 | 4 | Design lead with the co-design partner | Measure the curve on partner soils first (TRL 4, on hold); the operating chart already uses the softer soil |
| R2 | No co-design partner engaged | Partner not yet approached | Requirements stay unvalidated; no soils or tests | 3 | 4 | Amish | Approach the first candidate (decided 2026-10-02) when TRL 4 opens |
| R3 | Mass over the R7 total | Bushes, fasteners and weld metal counted; fix F1 | 203.8 kg against 200 kg | 5 | 2 | Amish (decision D2) | Decide D2; lighten as a value-engineering item if chosen |
| R4 | Cost over the value-engineering target | Steel mass, turned alloy pins, bushes | USD 542 against USD 500 | 4 | 2 | Design lead | Local quotes; value-engineering items in EPR-DEC-001 |
| R5 | Concept choice reopened | Options A, B and C within 10 % (D1) | Redesign if B or C is chosen | 2 | 4 | Amish (decision D1) | Decide D1; the repo stays on A meanwhile |
| R6 | Local parts not available | 42CrMo4 bar, 40 x 46 mm bushes or UPN 80 not stocked | Substitutions change the checks | 3 | 3 | Fabricator | Confirm when parts are bought (EPR-DEC-001 Table 2); recheck with `sizing.py` |
| R7 | Blocks below the strength reference | Unsuitable soil, low cement, poor curing | Weak walls if blocks are used untested | 3 | 5 | Co-design partner, project engineer | Field tests, mix chart, block tests before structural use (PR-003); stated in every safety note |
| R8 | Output below 300 a day | Cycle longer than the assumed 85 s | Slower house building | 3 | 2 | Co-design partner | Timed cycles at TRL 4 (on hold) |

## Preliminary hazard analysis

Table 2. Hazards (option A).

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Lever kickback | Lever released at the end of the stroke; 47 J returned from soil rebound and column stretch | Struck head or arm | 4 | 3 | End pawl drops under the crank pin at the stop; rest catch at the start; rule: engage the pawl before letting go; heads out of the lever arc | 4 x 1 |
| H2 | Crushing in the linkage | Hands in the crank, connecting link and knee scissor while the lever moves | Crushed fingers or hand | 4 | 3 | Linkage guard with openings of 12 mm or less; only the people on the lever touch it, after calling "clear" | 4 x 1 |
| H3 | Lid thrown open under load | Latch unpinned while the toggle is loaded; worn or missing latch pin | Struck by the 27 kg lid or ejected soil | 5 | 2 | Lid and latch rated 173 kN; rule: rest catch in before the latch is opened; latch pin on a T-handle, inspected | 5 x 1 |
| H4 | Crushing in the mold | Hands in the mold during pressing or ejection | Crushed fingers | 4 | 2 | Fill with a scoop; lid closed before pressing; eject only with the lever in the eject socket | 4 x 1 |
| H5 | Eject arm and push rod | Hands near the push rod foot during ejection | Pinched fingers | 3 | 2 | Eject seesaw under the base; hands on the lever only | 3 x 1 |
| H6 | Silica dust | Sieving dry soil | Lung disease over time | 4 | 3 | Sieve damp soil; work upwind; FFP2 or N95 respirator (STM S19) | 4 x 2 |
| H7 | Wet cement | Mixing cement-stabilized soil by hand | Skin burns, eye damage | 3 | 3 | Gloves, long sleeves, eye protection (STM S20) | 3 x 1 |
| H8 | Manual handling | Moving press pieces of up to 44.5 kg; carrying 7.6 kg blocks all day | Back injury | 3 | 3 | Two people to each piece (STM S21); rotate tasks; lift blocks close to the body | 3 x 2 |
| H9 | Structural overload | Extra people or a cheater bar on the lever beyond 1,000 N | Pin, link or lid failure | 5 | 1 | Crank stop caps the force at the design load; members sized at 173 kN with factors of 1.29 or more (PR-016, fix F1) | 5 x 1 |
| H10 | Fabrication | Welding, cutting, grinding | Burns, eye injury, fire | 4 | 2 | Welding PPE, guarded grinders, no flammables (BLD-001) | 4 x 1 |
| H11 | Unsafe walls | Blocks used structurally without tests or design | Wall collapse | 5 | 2 | Every document states that blocks are not certified and need tests and an engineer for structural use | 5 x 1 |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Toggle pins | Carry the link forces | Bend or yield | Linkage jams; block height lost | Pins too small in bending (found in the STEM check) | 5 | 1 | 3 | 15 | Done: 40 mm 42CrMo4 +QT pins (fix F1); check straightness at each service |
| F2 | Bushes | Pin bearing | Wear or scoring | Play in the linkage; low pressure at the stop | Grit, lack of grease | 3 | 3 | 3 | 27 | Dust seals, grease nipples, weekly greasing; measure play at TRL 4 |
| F3 | Fill | Set block density and height | Fill outside 0 to +2.7 % | Weak block (under) or operators stall short of the stop (over) | Not weighed; scale misread | 4 | 4 | 3 | 48 | Weigh every fill; scoop only after the scatter test; block gauge on every block |
| F4 | Latch pin | Hold the lid | Worn, bent or missing | Lid thrown open (H3) | Wear, loss | 5 | 2 | 4 | 40 | Inspect at each shift; spare pin on a chain; replace when worn by 0.5 mm |
| F5 | End pawl and spring | Hold the crank pin at the stop | Spring broken; pawl does not drop | Kickback (H1) | Fatigue, grit | 4 | 2 | 3 | 24 | Check pawl action at the start of each shift; spare spring |
| F6 | Mold walls | Shape the block | Wear of the cavity faces | Oversize blocks | Sandy soils | 3 | 3 | 2 | 18 | Gauge blocks; measure wear against PR-008 (decided 2026-10-02) |
| F7 | Welds of the base beam and lugs | Carry the toggle reaction | Fatigue crack | Loss of the base pin support | Poor weld; overload | 5 | 1 | 4 | 20 | FAT 71 detail at 89 MPa range (S11); visual check of the lug welds each month |
| F8 | Mold bolts | Hold the mold to the columns | Loosen | Mold shifts; flange wear | Vibration, no locking | 3 | 2 | 3 | 18 | Torque to grade 8.8 value; check monthly |
| F9 | Lever socket and locking pin | Hold the lever | Pin missing | Lever slides out under load | Pin lost | 4 | 2 | 2 | 16 | Clevis pin with split pin; spare on a chain |
| F10 | Guard | Keep hands out of the linkage | Removed or damaged | Crushing (H2) | Removed for cleaning and not refitted | 4 | 2 | 2 | 16 | Rule: no pressing without the guard |
