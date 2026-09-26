"""EarthPress concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the lever (the compaction lever swings on the -X side), Y across the press, Z up,
ground at Z = 0. Units mm. Geometry comes from cad/src/model.py, so the media match the STEP files
and drawing EPR-DWG-001. The press is shown at the start of the compaction stroke with the lid
closed and loose soil in the mold. Numbers are printed by docs/04-calcs/sizing.py (EPR-CAL-001).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from concept import Part, render_all  # noqa: E402
from model import build_parts  # noqa: E402

parts = [Part(n, shape, colour, bom, ex) for n, shape, colour, bom, ex in build_parts()]

if __name__ == "__main__":
    render_all(
        parts, project="EarthPress", title="Manual CSEB press concept", dwg_no="EPR-DWG-010", date="2026-09-25",
        key_figures=["Block 290 x 140 x 90 mm, 6.9 kg dry (est.)",
                     "81 kN on the block for 2 MPa (est.)",
                     "Toggle and 1.7 m lever: 173:1 at the stop",
                     "Peak pull 668 N: two people on the T-handle",
                     "Fill weighed to 0 to +2.7 % (about 200 g)",
                     "About 296 blocks per day, crew of 4 (est.)",
                     "Press about 187 kg in 8 pieces, none over 37 kg",
                     "About $488 in parts, press and kit (indicative)"],
        cut_exclude=("Soil sieve, 5 mm mesh", "Soil test kit", "Block gauge", "Pressed blocks (context)"),
        flow={"title": "material flow per 100 blocks, kg (estimates, EPR-CAL-001; mixing adds 33 kg cement and 69 kg water)",
              "unit": "kg",
              "stages": [("Dug site soil", 778), ("Sieved soil", 661), ("Moist mix", 787),
                         ("Pressed blocks", 764), ("Cured blocks", 712)],
              "losses": [(0, "Oversize > 5 mm", 117), (2, "Spill and rejects, remixed", 23),
                         (3, "Water lost in curing", 51)]},
    )
