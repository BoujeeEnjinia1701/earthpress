"""EarthPress general arrangement drawing EPR-DWG-001 (Rev P3).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/EPR-DWG-001.svg, .pdf and .png from the parametric model.
The concept blueprint keeps EPR-DWG-010 (media/concept-blueprint); the making sketches for the
build plan are EPR-DWG-101 onward (cad/src/build_plan_media.py).
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, assemblies, geometry  # noqa: E402

asm = assemblies()["earthpress-assembly"]
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)
g = geometry()

s = Sheet(project="EarthPress", title="Manual CSEB press: general arrangement", dwg_no="EPR-DWG-001",
          rev="P3", author="Amish Chadha", date="2026-10-02", concept=True,
          material="Mild steel plate, UPN 80, tube and 2 in pipe; C45 pins. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from the TRL 3 model (EPR-CAL-001)", "2026-09-25", "AC"),
                     ("P2", "Constructable design (EPR-DDR-003): fixings, guard, catch, eject arm", "2026-10-01", "AC"),
                     ("P3", "Dust seals at the bush faces (EPR-DEC-001, 2026-10-02)", "2026-10-02", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 80, label="Isometric view", sublabel="Not to scale; seen from the front right and above")
s.add_notes("Key dimensions and interfaces (mm)", [
    "Shown at start of stroke, lid closed, lever on its catch",
    f"Cavity {P['blk_l']:.0f} x {P['blk_w']:.0f}, rim at {P['mold_top']:.0f}; fill {P['fill_h']:.0f}, block {P['blk_h']:.0f}",
    f"Mold wall {P['wall']:.0f}, belt {P['belt_t']:.0f} x {P['belt_h']:.0f}; 8 x M16 into tapped flanges",
    "UPN 80 columns, webs toward the mold; pin access holes",
    f"Lid {P['lid_t']:.0f} plate + 2 ribs {P['rib_t']:.0f} x {P['rib_h']:.0f}; pins {P['hinge_pin_d']:.0f} in rib ears",
    f"Toggle links {P['link_l']:.0f} c/c, {P['link_t']:.0f} x {P['link_w']:.0f}, round ends; pins {P['pin_d']:.0f}; {P['seal_t']:.0f} mm dust seals",
    f"Base pin at {g['z_b']:.0f}; stop at {P['theta_end']:.0f} deg from vertical",
    f"Lever pivot ({P['lever_x']:.0f}, {P['lever_z']:.0f}); crank {P['crank']:.0f}; link {P['conlink']:.0f}",
    f"Lever 2 in sch 40, grip radius {P['grip_r']:.0f}; arc 59 deg",
    f"Eject seesaw at ({P['eject_x']:.0f}, {P['eject_z']:.0f}), arm {P['eject_arm']:.0f}, lift {P['eject_lift']:.0f}",
    "Rest catch and end pawl on the crank pin; guard",
    "Ratio 173:1 at the stop; 81 kN at 2 MPa",
    "Mass about 200 kg; heaviest piece 45 kg",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=122, width=140)
s.save(ROOT / "cad/drawings/EPR-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/EPR-DWG-001.svg, .pdf, .png")
