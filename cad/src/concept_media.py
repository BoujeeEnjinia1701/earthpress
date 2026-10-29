"""EarthPress concept media from the detailed TRL 3 model (option A, kit 1.9.1).

Run from the repo root:  python cad/src/concept_media.py [hero|cutaway|exploded|flow|web|blueprint|all ...]
With no argument it draws everything with .kit/concept.py render_all. On a small machine run one picture per
process. Geometry comes from components("A") in cad/src/model.py, so the media match the STEP files, the
drawings and the fidelity check; the flow values come from EPR-CAL-001 (docs/04-calcs/sizing.py).

Axes as model.py: X along the lever (the compaction lever on the -X side), Y across the press, Z up from the
ground. The press is shown at the start of the stroke with the lid closed and loose soil in the mold. The
linkage guard is left out of the media so the linkage shows (it is in the model, the STEP files and the
drawing); fasteners and weld beads are shown without callouts (BOM lines 11 and 12 have none).
CONCEPT, NOT FOR FABRICATION.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
import concept as K  # noqa: E402
from concept import Part  # noqa: E402
import model as M  # noqa: E402

PROJECT, TITLE, DWG, DATE = "EarthPress", "Manual CSEB press concept", "EPR-DWG-010", "2026-10-25"
MD = ROOT / "media"
CONTEXT_COL = "#B7794A"


def _bom_names():
    out = {}
    for r in csv.DictReader((ROOT / "bom/bom.csv").open()):
        n, _, name = r["item"].partition(" ")
        out[int(n)] = name
    return out


def parts(context=True):
    names = _bom_names()
    out = []
    for p in M.components(M.CHOSEN):
        if p["bom"] == 13:
            continue
        if p["kind"] == "context":
            if context:
                out.append(Part(p["name"], p["shape"], CONTEXT_COL, None, (0, 0, 0)))
            continue
        bom = p["bom"] if p["kind"] in ("made", "bought") else None
        out.append(Part(names.get(p["bom"], p["name"]) if bom else p["name"], p["shape"], p["color"], bom, tuple(p["explode"])))
    return out


def key_figures():
    return ["Block 290 x 140 x 90 mm, 6.9 kg dry (est.)",
            "81 kN on the block for 2 MPa (est.)",
            "Toggle and 1.7 m lever: 173:1 at the stop",
            "Peak pull 405 N each for two (softer soil)",
            "Toggle pins 40 mm 42CrMo4 in 40 x 46 bushes",
            "About 296 blocks per day, crew of 4 (est.)",
            "Press about 204 kg; heaviest piece 45 kg (est.)",
            "About $542 in parts, press and kit (indicative)"]


def flow_spec():
    return {"title": "material flow per 100 blocks, kg (estimates, EPR-CAL-001; mixing adds 33 kg cement and 69 kg water)",
            "unit": "kg",
            "stages": [("Dug site soil", 778), ("Sieved soil", 661), ("Moist mix", 787), ("Pressed blocks", 764), ("Cured blocks", 712)],
            "losses": [(0, "Oversize > 5 mm", 117), (2, "Spill and rejects, remixed", 23), (3, "Water lost in curing", 51)]}


CUT_EXCLUDE = ("Soil sieve", "Soil test kit", "Block gauge", "Pressed blocks (context)")


def blueprint():
    """Concept blueprint sheet, projected from the constructable model (M.ga_assembly) so hidden-line removal
    finishes; same sheet layout as .kit/concept.render_all."""
    from drawing import Sheet, project_views
    from build123d import Compound
    asm = M.ga_assembly()
    views = project_views(asm, MD / "_views")
    fig = [q for q in K.with_scale_figure([Part("Press", asm, "#4B5563")]) if q.name != "Press"]
    views["iso"] = project_views(Compound(children=[asm] + [q.shape for q in fig]), MD / "_views_fig")["iso"]
    s = Sheet(project=PROJECT, title=TITLE, dwg_no=DWG, rev="P4", author="Amish Chadha", date=DATE, theme="blueprint",
              material="Concept model for communication", revisions=[("P4", "Concept sheet, kit 1.9.1 model", DATE, "AC")])
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 32, 140, 118, label="Isometric view", sublabel="Not to scale; figure is a 1.75 m person")
    s.add_notes("Key figures", key_figures(), x=276, y=168, width=140)
    s.save(MD / "concept-blueprint")
    import shutil
    shutil.rmtree(MD / "_views", ignore_errors=True); shutil.rmtree(MD / "_views_fig", ignore_errors=True)
    return MD / "concept-blueprint.png"


def everything():
    ps = parts(context=False)
    return K.render_all(ps, PROJECT, TITLE, DWG, key_figures(), date=DATE, rev="P4", flow=flow_spec(),
                        context=[q for q in parts(context=True) if q.bom is None and "(context)" in q.name],
                        cut_exclude=CUT_EXCLUDE)


if __name__ == "__main__":
    fns = {"hero": lambda: K._render(K.with_scale_figure(parts()), MD / "hero.png", title=PROJECT,
                                     note="Seen from the front right and above, 24 deg elevation. Grey figure: 1.75 m person for scale"),
           "cutaway": lambda: K._render(K.cutaway_parts([q for q in parts() if q.name not in CUT_EXCLUDE]), MD / "cutaway.png", azim=-90, elev=18,
                                        title=f"{PROJECT}: cutaway", note="Front half removed; seen from the front and above, 18 deg elevation"),
           "exploded": lambda: K._render(parts(context=False), MD / "exploded.png", offsets=True, labels=True, title=f"{PROJECT}: exploded view",
                                         note="Seen from the front right and above, 24 deg elevation; numbers match bom/bom.csv"),
           "flow": lambda: K.flow_diagram(flow_spec()["stages"], MD / "flow.png", f"{PROJECT}: {flow_spec()['title']}", "kg", flow_spec()["losses"]),
           "blueprint": blueprint,
           "web": lambda: K.export_web_model(parts(context=False), "media", title=f"{PROJECT}: {TITLE}"),
           "all": everything}
    for w in sys.argv[1:] or ["all"]:
        print(w, "->", fns[w]())
