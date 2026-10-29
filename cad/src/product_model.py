"""EarthPress product appearance model for photoreal renders (STANDARDS sections 12 and 24), TRL 3, kit 1.9.1.

Every product part is components(CHOSEN) from cad/src/model.py as it is: the base frame, press core, mold box,
ribbed lid, piston, toggle links in their bushes, pins with circlips and grease nipples, lever hub, crank, catch,
pawl, eject seesaw, guard, every bolt, nut, washer and weld bead, and the soil sieve, test kit and block gauge.
The press is posed at the start of the stroke (lever on its rest catch, lid closed, loose soil in the mold), as
in model.py. Only the site is added, as context parts: a block yard on bare soil with a heap of sieved soil, a
200 L water drum, a stack of pressed blocks (from model.py) and two 1.75 m mannequins standing at the lever end,
the two operators the press needs. Ground level is model z = 0; every site part reaches below it.
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (the press without the lever), "lever" (lever, T-handle, grips and locking pin), "kit" (sieve,
test kit, gauge), "context" (site, blocks and mannequins).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Cone, Pos, Rot  # noqa: E402
import model as M  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402

TITLE = "EarthPress: an open, welder-buildable lever and toggle press for compressed earth blocks"

_SITE = ["--scene=outdoor", "--ground=soil", "--ground-z=0", "--sun=42,-75", "--lens=50"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "lever", "kit", "context"], "explode": False, "el": 16, "az": -48, "args": _SITE,
     "note": "Site render in a block yard on bare soil from the front right and a little above (about 16 deg elevation): "
             "the press at the start of the stroke with its lever on the rest catch, soil sieve and test kit beside it, a heap "
             "of sieved soil, a water drum and a stack of blocks; two 1.75 m people at the lever end for scale"},
    {"name": "studio", "groups": ["shell", "lever", "kit"], "explode": False, "el": 22, "az": -40,
     "note": "Studio render from the front right and above (about 22 deg elevation): the whole press with its lever, "
             "sieve, test kit and block gauge"},
    {"name": "exploded", "groups": ["shell", "lever"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): lid, mold box, piston, toggle, "
             "press core, base, lever and eject parts pulled apart with their fasteners"},
    {"name": "detail", "groups": ["shell"], "explode": False, "el": 18, "az": -125,
     "note": "Detail view from the front left, slightly above (about 18 deg elevation): toggle links in their bushes, "
             "connecting link, lever hub, catch and pawl under the mold box; the lever and kit left out"},
]


def _group(p):
    if p["group"] == "kit":
        return "kit"
    if p["group"] == "lever":
        return "lever"
    return "shell"


def site():
    """Block yard context: soil heap, water drum and two operators. Every site part reaches below z = 0."""
    out = []
    ctx = lambda n, sh, mat: out.append(part(f"{n} (site)", sh, mat, kind="context", group="context"))
    heap = Pos(1550, 2100, 125) * Cone(900, 120, 650)      # Cone is centred: z -200 to 450
    ctx("Heap of sieved soil", heap, "soil")
    drum = Pos(-650, 1250, -20) * cp.drum_200l()
    ctx("Water drum, 200 L", drum, "hdpe_recycled")
    try:
        import context_parts
        for sy, rz in ((-430, 95), (430, 85)):
            man = Pos(-1250, sy, 0) * Rot(0, 0, rz) * context_parts.mannequin(1750.0, "stand")
            out.append(part(f"Operator 1.75 m {'left' if sy < 0 else 'right'} (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:   # the mannequins are for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    out = []
    for p in M.components(M.CHOSEN):
        q = dict(p)
        if p["kind"] == "context":
            q["group"] = "context"
        else:
            q["group"] = _group(p)
        out.append(q)
    return out + site()


if __name__ == "__main__":
    ps = product_parts()
    from collections import Counter
    print(len(ps), "parts;", dict(Counter(p["group"] for p in ps)))
