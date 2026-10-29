#!/usr/bin/env python3
"""CAD fidelity check and per-part STEP export (kit 1.9, STANDARDS section 24).

Reads cad/src/model.py, which (kit 1.9) defines

    PARAMS = {...}                      # every main dimension; the calculations read these
    OPTIONS = {"A": "Ribbed flap", ...} # every concept option, each modelled to the repo's level
    CHOSEN = "A"                        # the option carried to the drawing, BOM and build plan
    def components(option): ...         # list of cad_parts.part() dicts for that option

and checks each option against the detail level the repo's stage requires (D1 at P0, D2 at P1 and P2,
D3 at P3; `cad_level` in project.yaml can only raise it). Results go to cad/fidelity.json with a hash of
the CAD sources, which `render.py --check` reads, so the slow geometry checks run only when the model
changes.

Usage (repo root):
    python .kit/cad_check.py            # check every option, write cad/fidelity.json, print a report
    python .kit/cad_check.py --export   # also write cad/step/<option>/<nn>-<part>.step and <option>-assembly.step (per-part files for the chosen option's made and bought parts only)
    python .kit/cad_check.py --status   # exit 1 if cad/fidelity.json is missing, stale or failed (used by render.py)
"""
from __future__ import annotations

import csv, hashlib, importlib, json, re, sys, time
from pathlib import Path

ROOT = Path.cwd()
KIT = Path(__file__).resolve().parent
OUT = ROOT / "cad/fidelity.json"
STAGE_LEVEL = {"P0": 1, "P1": 2, "P2": 2, "P3": 3, "P4": 3, "P5": 3, "P6": 3}

# Thresholds per level: (min parts per option, max share of bare primitives, fasteners needed, interference
# checked, STEP per part needed, BOM match needed)
RULES = {
    1: dict(min_parts=8, bare_max=0.50, fasteners=False, interference=False, step=False, bom=False),
    2: dict(min_parts=15, bare_max=0.25, fasteners=True, interference=True, step=False, bom=False),
    3: dict(min_parts=20, bare_max=0.15, fasteners=True, interference=True, step=True, bom=True),
}
INTERFERENCE_TOL_MM3 = 5.0


def src_hash():
    h = hashlib.sha256()
    for p in sorted((ROOT / "cad/src").glob("*.py")) + [KIT / "cad_parts.py", ROOT / "bom/bom.csv"]:
        if p.exists():
            h.update(p.read_bytes())
    return h.hexdigest()[:16]


def level_required():
    import yaml
    pm = yaml.safe_load((ROOT / "project.yaml").read_text())
    lv = STAGE_LEVEL.get(str(pm.get("stage", "P0")), 1)
    m = re.match(r"D?(\d)", str(pm.get("cad_level", "")))
    return max(lv, int(m.group(1)) if m else 0), pm


def is_bare(shape):
    """True for an untouched box (6 planar faces) or plain solid cylinder (3 faces): massing, not a part."""
    try:
        faces = shape.faces()
        n = len(faces)
        if n == 6 and all(f.geom_type.name == "PLANE" if hasattr(f.geom_type, "name") else str(f.geom_type) == "PLANE" for f in faces):
            return True
        if n == 3:
            return True
    except Exception:
        pass
    return False


def load_model():
    sys.path[:0] = [str(ROOT / "cad/src"), str(KIT)]
    return importlib.import_module("model")


def interference(parts, allowed):
    """Pairs of parts whose solids overlap by more than the tolerance (bounding boxes first)."""
    hits = []
    boxes = []
    for p in parts:
        try:
            boxes.append(p["shape"].bounding_box())
        except Exception:
            boxes.append(None)
    def ov(a, b):
        return not (a.max.X < b.min.X or b.max.X < a.min.X or a.max.Y < b.min.Y or b.max.Y < a.min.Y or a.max.Z < b.min.Z or b.max.Z < a.min.Z)
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            a, b = boxes[i], boxes[j]
            if a is None or b is None or not ov(a, b):
                continue
            ni, nj = parts[i]["name"], parts[j]["name"]
            if any((x in ni and y in nj) or (x in nj and y in ni) for x, y in allowed):
                continue
            try:
                v = (parts[i]["shape"] & parts[j]["shape"]).volume
            except Exception:
                continue
            if v > INTERFERENCE_TOL_MM3:
                hits.append((ni, nj, round(v, 1)))
    return hits


def bom_ids():
    f = ROOT / "bom/bom.csv"
    if not f.exists():
        return set()
    ids = set()
    for r in csv.DictReader(f.open()):
        m = re.match(r"\s*(\d+)", r.get("item", "") or r.get("Item", ""))
        if m:
            ids.add(int(m.group(1)))
    return ids


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]


def step_parts(opt, parts, chosen):
    """Parts that get their own STEP file: the made and bought parts of the chosen option. Fasteners and welds
    are catalogue items or process features and appear only in the assembly; every other option is exported as
    its assembly STEP alone (kit 1.9.1, keeps repos small)."""
    if opt != chosen:
        return []
    return [p for p in parts if p["kind"] in ("made", "bought")]


def export_step(opt, parts, chosen):
    from build123d import Compound, export_step as ex
    import copy
    d = ROOT / "cad/step" / opt
    d.mkdir(parents=True, exist_ok=True)
    for old in d.glob("*.step"):
        old.unlink()
    if not step_parts(opt, parts, chosen):
        d.rmdir()
    for n, p in enumerate(parts, 1):
        if p in step_parts(opt, parts, chosen):
            ex(p["shape"], str(d / f"{n:03d}-{slug(p['name'])}.step"))
    solids = [copy.copy(p["shape"]) for p in parts if p["kind"] != "context"]
    ex(Compound(solids), str(ROOT / "cad/step" / f"{opt}-assembly.step"))


def run(export=False):
    t0 = time.time()
    lv, pm = level_required()
    R = RULES[lv]
    model = load_model()
    report = dict(level=f"D{lv}", stage=pm.get("stage"), hash=src_hash(), options={}, failures=[], warnings=[])
    if not hasattr(model, "OPTIONS") or not hasattr(model, "components"):
        report["failures"].append("cad/src/model.py must define OPTIONS, CHOSEN and components(option) (kit 1.9)")
        return report
    chosen = getattr(model, "CHOSEN", None)
    allowed = getattr(model, "ALLOWED_CONTACTS", [])
    ids = bom_ids()
    for opt, title in model.OPTIONS.items():
        parts = model.components(opt)
        real = [p for p in parts if p.get("kind") != "context"]
        bare = [p["name"] for p in real if p["kind"] in ("made", "bought") and is_bare(p["shape"])]
        made_bought = [p for p in real if p["kind"] in ("made", "bought")]
        share = len(bare) / max(1, len(made_bought))
        fasteners = [p for p in real if p["kind"] == "fastener"]
        o = dict(title=title, parts=len(real), made_or_bought=len(made_bought), fasteners=len(fasteners),
                 welds=sum(p["kind"] == "weld" for p in real), bare=bare, bare_share=round(share, 3))
        fail = lambda msg: report["failures"].append(f"option {opt}: {msg}")
        if len(real) < R["min_parts"]:
            fail(f"{len(real)} parts, D{lv} needs at least {R['min_parts']} (every visible part its own solid)")
        if share > R["bare_max"]:
            fail(f"{share:.0%} of made or bought parts are bare boxes or cylinders, D{lv} allows {R['bare_max']:.0%}: {', '.join(bare[:8])}")
        if R["fasteners"] and not fasteners:
            fail(f"no fasteners; D{lv} models every bolt, nut, washer, pin and screw (cad_parts.hex_bolt_set and others)")
        for p in real:
            if not p.get("material_name"):
                fail(f"part '{p['name']}' has no material; build it with cad_parts.part()")
        if R["interference"]:
            hits = interference(real, allowed)
            o["interference"] = hits
            for a, b, v in hits[:10]:
                fail(f"'{a}' and '{b}' overlap by {v} mm3 (model the hole or the clearance)")
        if R["bom"] and opt == chosen:
            missing = sorted({p["name"] for p in made_bought if p.get("bom") is None})
            unknown = sorted({p["bom"] for p in made_bought if p.get("bom") is not None and p["bom"] not in ids})
            if missing:
                fail(f"chosen design: {len(missing)} made or bought parts have no BOM line: {', '.join(missing[:6])}")
            if unknown:
                fail(f"chosen design: BOM lines {unknown} are used in the model but missing from bom/bom.csv")
        try:
            import cad_parts
            o["mass_kg"] = round(sum(cad_parts.mass_kg(p) for p in real), 1)
        except Exception:
            pass
        if export or R["step"]:
            if export:
                export_step(opt, parts, chosen)
            d = ROOT / "cad/step" / opt
            n_step = len(list(d.glob("*.step"))) if d.exists() else 0
            need = len(step_parts(opt, real, chosen))
            o["step_files"] = n_step
            if R["step"] and n_step < need:
                fail(f"{n_step} STEP files in cad/step/{opt}/ for {need} made or bought parts; run python .kit/cad_check.py --export")
            if R["step"] and not (ROOT / "cad/step" / f"{opt}-assembly.step").exists():
                fail(f"cad/step/{opt}-assembly.step missing; run python .kit/cad_check.py --export")
        report["options"][opt] = o
    report["passed"] = not report["failures"]
    report["seconds"] = round(time.time() - t0, 1)
    return report


def main():
    if "--status" in sys.argv:
        if not OUT.exists():
            print("FAIL cad/fidelity.json missing; run python .kit/cad_check.py"); sys.exit(1)
        r = json.loads(OUT.read_text())
        lv, _ = level_required()
        if r.get("hash") != src_hash():
            print("FAIL cad/fidelity.json is stale (the model or BOM changed); run python .kit/cad_check.py"); sys.exit(1)
        if int(str(r.get("level", "D0"))[1:]) < lv:
            print(f"FAIL cad/fidelity.json was checked at {r.get('level')}, the stage needs D{lv}"); sys.exit(1)
        if not r.get("passed"):
            for f in r.get("failures", [])[:10]:
                print("FAIL", f)
            sys.exit(1)
        print(f"ok   CAD fidelity {r['level']}: " + ", ".join(f"{k} {v['parts']} parts" for k, v in r["options"].items()))
        return
    r = run(export="--export" in sys.argv)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(r, indent=1))
    for k, v in r["options"].items():
        print(f"option {k} ({v['title']}): {v['parts']} parts, {v['fasteners']} fasteners, {v['welds']} welds, "
              f"bare {v['bare_share']:.0%}, mass {v.get('mass_kg', '?')} kg")
    for f in r["failures"]:
        print("FAIL", f)
    print(("PASS" if r["passed"] else "FAIL") + f" CAD fidelity {r['level']} in {r['seconds']} s -> {OUT.relative_to(ROOT)}")
    sys.exit(0 if r["passed"] else 1)


if __name__ == "__main__":
    main()
