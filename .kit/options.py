#!/usr/bin/env python3
"""Concept options picture (STANDARDS section 21).

Reads cad/src/options.py, which defines

    OPTIONS = [
        {"key": "A", "name": "Bottle-jack press", "principle": "...", "parts": [Part(...), ...],
         "scale": "person" | "hand" | "none"},
        ...
    ]

and writes media/options.png: one massing render per option side by side, each with the same scale
reference (a 1.75 m person or a hand), its name and its one-line principle.

Usage (from the repo root):  python .kit/options.py            (kit 1.9: Cycles renders of model.py OPTIONS)
                             python .kit/options.py --export=DIR  then render DIR/*__options_jobs.json elsewhere,
                             python .kit/options.py --compose=DIR (compose the picture from the rendered panels)
                             python .kit/options.py --massing  (kit 1.8: massing models from cad/src/options.py)
"""
import importlib.util, sys, tempfile, textwrap
from pathlib import Path

KIT = Path(__file__).resolve().parent
ROOT = Path.cwd()
sys.path.insert(0, str(KIT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import concept

INK, MUTED, ACCENT = "#111827", "#4B5563", "#0F766E"




def _tess(shape):
    """Tessellate a part for the options picture. A face that does not mesh at the fine tolerance is retried
    coarser, then face by face, skipping only the face that fails (kit 1.9.1)."""
    for tol in ((0.05, 0.1), (0.2, 0.3)):
        try:
            return shape.tessellate(*tol)
        except Exception:
            pass
    verts, tris = [], []
    for f in shape.faces():
        try:
            v, t = f.tessellate(0.2, 0.3)
        except Exception:
            continue
        n = len(verts); verts += list(v); tris += [tuple(i + n for i in tri) for tri in t]
    return verts, tris

def _choice_label(from_model):
    """CHOSEN only when project.yaml records a decided concept_chosen; otherwise the option is the current design
    (kit 1.9.1: a proposed or open choice must not read as decided)."""
    try:
        import yaml
        c = str((yaml.safe_load((ROOT / "project.yaml").read_text()) or {}).get("concept_chosen") or "")
    except Exception:
        c = ""
    if c and "propos" not in c.lower() and "open" not in c.lower() and "await" not in c.lower():
        return "CHOSEN"
    return "CURRENT DESIGN" if from_model else "RECOMMENDED"

def load_options():
    src = ROOT / "cad/src/options.py"
    if not src.exists():
        sys.exit("cad/src/options.py not found (STANDARDS section 21)")
    sys.path.insert(0, str(src.parent))
    spec = importlib.util.spec_from_file_location("options_src", src)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    opts = mod.OPTIONS
    if len(opts) < 2:
        sys.exit("at least two concept options are required (STANDARDS section 21)")
    return opts, getattr(mod, "TITLE", ROOT.name)


def panel(opt, path):
    parts = list(opt["parts"])
    scale = opt.get("scale", "person")
    if scale == "person":
        parts = concept.with_scale_figure(parts)
    elif scale == "hand":
        import context_parts
        parts = parts + [concept.Part("Hand (scale)", context_parts.forearm_hand(), "#D6B4A0")]
    concept._render(parts, path, elev=opt.get("elev", 22), azim=opt.get("azim", -55), size=(5, 5), dpi=160)
    return Image.open(path).convert("RGB")


def model_options():
    """Kit 1.9: options come from cad/src/model.py (OPTIONS, components(option), optional PRINCIPLES, CHOSEN,
    OPTION_VIEWS) so the options picture shows the same detailed geometry the fidelity check reads."""
    src = ROOT / "cad/src/model.py"
    if not src.exists():
        return None
    sys.path[:0] = [str(src.parent), str(KIT)]
    try:
        spec = importlib.util.spec_from_file_location("model_src", src)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    except Exception as e:
        print("model.py did not load for the options picture:", e)
        return None
    if not (hasattr(mod, "OPTIONS") and hasattr(mod, "components")):
        return None
    pr = getattr(mod, "PRINCIPLES", {}); views = getattr(mod, "OPTION_VIEWS", {})
    opts = [dict(key=k, name=v, principle=pr.get(k, ""), chosen=(k == getattr(mod, "CHOSEN", None)),
                 parts=mod.components(k), view=views.get(k, {})) for k, v in mod.OPTIONS.items()]
    return opts, getattr(mod, "TITLE", ROOT.name)


def cycles_panel(opt, tmp):
    """Photoreal studio render of one option (Blender Cycles) with a 1.75 m mannequin for scale."""
    if COMPOSE_DIR:
        return Image.open(COMPOSE_DIR / f"{ROOT.name}__opt-{opt['key']}.png").convert("RGB")
    import json, subprocess
    import numpy as np
    import context_parts
    from build123d import Pos
    parts = [p for p in opt["parts"] if p.get("kind") != "context" or opt["view"].get("keep_context")]
    bb = None
    for p in parts:
        b = p["shape"].bounding_box()
        bb = b if bb is None else bb.add(b)
    arrays, meta = {}, []
    if opt["view"].get("scale", "person") == "person":
        gz = opt["view"].get("ground_z", bb.min.Z)   # OPTION_VIEWS "ground_z": ground level in model mm (parts may reach below it)
        man = Pos(bb.min.X - 450, bb.center().Y, gz) * context_parts.mannequin(1750.0, "stand")
        parts = parts + [dict(name="Person (scale)", shape=man, color="#9C9C9E", material="clay", kind="context")]
    for i, p in enumerate(parts):
        v, t = _tess(p["shape"])
        arrays[f"v{i}"] = np.array([[q.X, q.Y, q.Z] for q in v], dtype=np.float32) / 1000.0
        arrays[f"f{i}"] = np.array(t, dtype=np.int32)
        meta.append(dict(name=p["name"], color=p["color"], bom=p.get("bom"), alpha=1.0, material=p.get("material"),
                         context=p.get("kind") == "context"))
    npz = Path(tmp) / f"opt-{opt['key']}.npz"
    np.savez_compressed(npz, **arrays)
    npz.with_suffix(".json").write_text(json.dumps(dict(project="", title="", parts=meta)))
    out = Path(tmp) / f"opt-{opt['key']}.png"
    v = opt["view"]
    rargs = ["--product", "--res=1000x900", f"--el={v.get('el', 22)}", f"--az={v.get('az', -55)}"]
    if "ground_z" in v:
        rargs.append(f"--ground-z={v['ground_z']}")
    rargs += list(v.get("args", []))
    if EXPORT_DIR:   # render elsewhere (a GPU machine): write the scene and the job, compose later with --compose
        import shutil
        shutil.copy(npz, EXPORT_DIR / npz.name); shutil.copy(npz.with_suffix(".json"), EXPORT_DIR / npz.with_suffix(".json").name)
        JOBS.append(dict(npz=npz.name, out=f"{ROOT.name}__opt-{opt['key']}.png", args=rargs))
        return None
    if COMPOSE_DIR:
        return Image.open(COMPOSE_DIR / f"{ROOT.name}__opt-{opt['key']}.png").convert("RGB")
    args = [sys.executable, str(KIT / "photoreal.py"), str(npz), str(out), "--preview"] + rargs
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode or not out.exists():
        raise RuntimeError(r.stderr[-800:])
    return Image.open(out).convert("RGB")


EXPORT_DIR = COMPOSE_DIR = None
JOBS = []
for a in sys.argv:
    if a.startswith("--export="): EXPORT_DIR = Path(a[9:]); EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    if a.startswith("--compose="): COMPOSE_DIR = Path(a[10:])


def main():
    mo = model_options() if "--massing" not in sys.argv else None
    if mo:
        opts, title = mo
        if COMPOSE_DIR:
            imgs = [cycles_panel(o, None) for o in opts]
        else:
            with tempfile.TemporaryDirectory() as tmp:
                imgs = [cycles_panel(o, tmp) for o in opts]
        if EXPORT_DIR:
            import json
            (EXPORT_DIR / f"{ROOT.name}__options_jobs.json").write_text(json.dumps(JOBS, indent=1))
            print(f"exported {len(JOBS)} option scenes to {EXPORT_DIR}; render them, then run with --compose=<dir>")
            return
    else:
        opts, title = load_options()
        with tempfile.TemporaryDirectory() as tmp:
            imgs = [panel(o, Path(tmp) / f"opt-{o['key']}.png") for o in opts]
    n = len(opts)
    fig = plt.figure(figsize=(5.2 * n, 6.6), dpi=160)
    fig.text(0.015, 0.975, f"{title}: concept options", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.015, 0.935, "CONCEPT OPTIONS, NOT FOR FABRICATION. Same scale reference in every panel.", fontsize=8, color="#B45309", va="top")
    if concept._repo():
        fig.text(0.985, 0.975, concept._repo(), fontsize=8, color=ACCENT, va="top", ha="right", family="monospace")
    for i, (o, im) in enumerate(zip(opts, imgs)):
        ax = fig.add_axes([i / n + 0.01, 0.2, 1 / n - 0.02, 0.68])
        ax.imshow(im); ax.axis("off")
        fig.text(i / n + 0.02, 0.17, f"Option {o['key']}: {o['name']}", fontsize=11, fontweight="bold", color=INK, va="top")
        fig.text(i / n + 0.02, 0.12, textwrap.fill(o.get("principle", ""), 52), fontsize=8.5, color=MUTED, va="top")
        if o.get("chosen"):
            fig.text((i + 1) / n - 0.02, 0.195, _choice_label(mo), fontsize=8, fontweight="bold", color=ACCENT, va="top", ha="right")
    out = ROOT / "media/options.png"
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
