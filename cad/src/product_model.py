"""EarthPress product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders of the manual compressed earth block press: rounded
tube and plate edges, painted steel in a restrained palette, round-ended toggle and crank links,
bright turned pins with circlips, bush flanges and grease nipples, M16 and M12 bolt heads, rubber
T-handle grips, a raised nameplate and pinch-point labels, and the soil test kit with clear jars
showing the settled soil layers. Context: a compact patch of compacted earth, a stack of finished
blocks and the shared clay mannequin pushing down on the T-handle.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS and the kinematics in model.py (geometry(),
toggle_state(), knee_and_crank()). Axes as model.py: X along the lever (compaction lever on the -X
side, eject lever on the +X side), Y across the press, Z up from the ground. Units mm.
The press is posed at POSE_F of the compaction stroke (model.py poses it at the start) so the
operator's push reads; differences from model.py are listed in docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / ".kit"))

from build123d import (Align, Axis, Box, Compound, Cylinder, Plane, Polygon, Pos, RectangleRounded, RegularPolygon,
                       Rot, Sphere, Text, extrude, fillet)
from model import (PARAMS, geometry, theta_start, toggle_state, knee_and_crank, _box, _rod, _pipe,
                   _flat, _ypin)

TITLE = "EarthPress: manual lever and toggle press for compressed earth blocks"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 22, "az": -40,
     "note": "Product render from the front right and above (about 22 deg elevation); operator pushing the "
             "lever at left, teal mold box on the press, test kit in front, blocks and gauge at right"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): lid, mold box, piston, "
             "toggle, press core, base, lever, eject lever, sieve, test kit and gauge"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 18, "az": -125,
     "note": "Detail view from the front left, slightly above (about 18 deg elevation): toggle links, connecting "
             "link and lever hub under the mold box; lever pipe and operator left out"},
]

# Pose: fraction of the compaction stroke (0 = start, as model.py; 1 = crank stop)
POSE_F = 0.85

# Colours (restrained; kit accent #0F766E on the mold and lid)
C_FRAME = "#3F4650"      # graphite powder coat
C_CORE = "#4B5360"
C_MOLD = "#0F766E"
C_LID = "#115E59"
C_LINK = "#C2410C"       # moving linkage in safety orange
C_LEVER = "#1F2328"
C_EJECT = "#5B6470"
C_STEEL = "#B8BEC6"      # bright turned pins, piston
C_ZINC = "#9AA3AE"       # bolts
C_CLIP = "#4A4F57"
C_BRASS = "#C9A227"
C_RUBBER = "#24272C"
C_LABEL = "#F2F4F5"
C_YELLOW = "#E3B21C"
C_INK = "#111827"
C_BLOCK = "#B98A62"
C_SOIL = "#8B5E3C"
C_GROUND = "#D9CDB8"
C_WOOD = "#B08A5A"
C_MESH = "#8A9099"
C_CRATE = "#2F5D73"
C_JAR = "#E6EEF2"
C_CLAY = "#9CA3AF"

FONT = str(HERE.parents[1] / ".kit/fonts/IBMPlexSans-SemiBold.ttf")
MQ_HEIGHT = 1750.0
MQ_JOINTS = dict(shoulder_flex_l=51.2, shoulder_flex_r=51.2, elbow_flex_l=70.0, elbow_flex_r=70.0, torso_lean=13.0)


# ------------------------------------------------------------------ helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _rbox(x0, x1, y0, y1, z0, z1, axis=Axis.Z, radii=(4.0, 2.0, 1.0)):
    """Axis-aligned box with the edges parallel to `axis` rounded."""
    b = _box(x0, x1, y0, y1, z0, z1)
    return _fillet_try(b, b.edges().filter_by(axis), radii)


def _rhs(axis, a0, a1, c1, c2, s, t=3.0, r=5.0):
    """Rectangular hollow section of size s along `axis` ("x" or "y") from a0 to a1, centred at (c1, c2)
    in the other two axes (y, z for "x"; x, z for "y"), with rounded outer corners."""
    prof = RectangleRounded(s, s, r) - RectangleRounded(s - 2 * t, s - 2 * t, max(r - t, 0.5))
    if axis == "x":
        return Pos(a0, c1, c2) * extrude(Plane.YZ * prof, amount=a1 - a0)
    return Pos(c1, a1, c2) * extrude(Plane.XZ * prof, amount=a1 - a0)


def _link(a, b, w, t, y, ext=None):
    """Round-ended flat link in the XZ plane between pin centres a and b (x, z), thickness t at Y = y.
    The ends extend w/2 past the pin centres (model.py stops the bar at the centres)."""
    (ax, az), (bx, bz) = a, b
    L = math.hypot(bx - ax, bz - az)
    e = w / 2 if ext is None else ext
    ang = math.degrees(math.atan2(bz - az, bx - ax))
    bar = Box(L + 2 * e, t, w)
    bar = _fillet_try(bar, bar.edges().filter_by(Axis.Y), [w / 2 - 0.5, w / 3, 4.0])
    bar = _fillet_try(bar, bar.faces().sort_by(Axis.Y)[-1].edges(), [1.5, 0.8])
    bar = _fillet_try(bar, bar.faces().sort_by(Axis.Y)[0].edges(), [1.5, 0.8])
    return Pos((ax + bx) / 2, y, (az + bz) / 2) * Rot(0, -ang, 0) * bar


def _pin(x, z, d, length, y=0.0):
    """Turned pin along Y with chamfer-like rounded ends."""
    p = Cylinder(d / 2, length)
    p = _fillet_try(p, p.edges(), [2.0, 1.0])
    return Pos(x, y, z) * Rot(90, 0, 0) * p


def _clip(x, z, d, y):
    """Circlip ring on a pin along Y at Y = y."""
    return Pos(x, y, z) * Rot(90, 0, 0) * (Cylinder(d / 2 + 3.0, 2.0) - Cylinder(d / 2 - 0.5, 3.0))


def _nipple(x, z, y, sgn=-1):
    """Grease nipple on a pin end facing sgn*Y (hex, neck and ball)."""
    hexb = extrude(RegularPolygon(5.5, 6), amount=6.0)
    neck = Pos(0, 0, 6.0) * Cylinder(2.5, 4.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
    ball = Pos(0, 0, 11.0) * Sphere(3.2)
    n = hexb + neck + ball
    rot = Rot(90, 0, 0) if sgn < 0 else Rot(-90, 0, 0)
    return Pos(x, y, z) * rot * n


def _bolt_y(x, y, z, d, sgn):
    """Hex bolt head with washer on a face looking toward sgn*Y at Y = y (M16: d = 16)."""
    s = 1.5 * d
    washer = Cylinder(d, 0.18 * d, align=(Align.CENTER, Align.CENTER, Align.MIN))
    head = Pos(0, 0, 0.18 * d) * extrude(RegularPolygon(s / 2 / math.cos(math.radians(30)), 6), amount=0.62 * d)
    head = _fillet_try(head, head.faces().sort_by(Axis.Z)[-1].edges(), [0.08 * d, 0.04 * d])
    stub = Pos(0, 0, 0.8 * d) * Cylinder(d / 2, 0.35 * d, align=(Align.CENTER, Align.CENTER, Align.MIN))
    b = washer + head + stub
    rot = Rot(90, 0, 0) if sgn < 0 else Rot(-90, 0, 0)
    return Pos(x, y, z) * rot * b


def _bolt_z(x, y, z, d):
    """Hex bolt head with washer on an upward face at height z."""
    s = 1.5 * d
    washer = Cylinder(d, 0.18 * d, align=(Align.CENTER, Align.CENTER, Align.MIN))
    head = Pos(0, 0, 0.18 * d) * extrude(RegularPolygon(s / 2 / math.cos(math.radians(30)), 6), amount=0.62 * d)
    head = _fillet_try(head, head.faces().sort_by(Axis.Z)[-1].edges(), [0.08 * d, 0.04 * d])
    return Pos(x, y, z) * (washer + head)


def _text(txt, size, h):
    """Raised text on the local XY plane, centred, extruded +Z by h (None on failure)."""
    try:
        t = extrude(Text(txt, font_size=size, font_path=FONT, align=(Align.CENTER, Align.CENTER)), amount=h)
        return t if t.is_valid else None
    except Exception:
        return None


def _front(shape, x, y_face, z):
    """Place a local-XY feature (thickness +Z) on a face looking toward -Y at y_face."""
    return Pos(x, y_face, z) * Rot(90, 0, 0) * shape


def _cmp(shapes):
    shapes = [s for s in shapes if s is not None]
    return shapes[0] if len(shapes) == 1 else Compound(children=shapes)


def _sum(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


# ------------------------------------------------------------------ parts
def product_parts(P=PARAMS, with_person=True):
    p = P
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    th0, th1 = theta_start(p), math.radians(p["theta_end"])
    th = th0 + (th1 - th0) * POSE_F
    g = geometry(p)
    BL, BW, W = p["blk_l"], p["blk_w"], p["wall"]
    MT = p["mold_top"]; MB = MT - p["mold_h"]
    ox, oy = BL / 2 + W, BW / 2 + W
    col_y = oy + p["flange_t"] + p["col_b"] / 2
    sk, sy = p["skid"], p["skid_y"]
    zb_top = sk + p["base_t"]
    L2 = p["skid_len"] / 2
    lx, lz = p["lever_x"], p["lever_z"]
    r = p["rod"]

    # ============================================================ 1a base on skids (BOM 1)
    ex_base = (0, 0, -250)
    skids = _rhs("x", -L2, L2, -sy, sk / 2, sk) + _rhs("x", -L2, L2, sy, sk / 2, sk)
    cross = _sum([_rhs("y", -sy + sk / 2, sy - sk / 2, xc, sk / 2, 50.0)
                  for xc in (-L2 + sk / 2, L2 - sk / 2, -120 - sk / 2, 120 + sk / 2)])
    plate = _rbox(-p["base_l"] / 2, p["base_l"] / 2, -p["base_w"] / 2, p["base_w"] / 2, sk, zb_top, radii=(10.0, 5.0))
    bt_ = p["bracket_t"]
    bracket = None
    for s_ in (-1, 1):
        y0_, y1_ = sorted((s_ * 60, s_ * (60 + bt_)))
        pl = _rbox(lx - 45, lx + 45, y0_, y1_, sk, lz + 45, axis=Axis.Y, radii=(12.0, 6.0)) + \
            _rbox(lx - 95, lx - 45, y0_, y1_, lz - 20, lz + 170, axis=Axis.Y, radii=(10.0, 5.0))
        bracket = pl if bracket is None else bracket + pl
    t = p["tie"]
    ties = (_pipe((lx + 40, 65, lz - 20), (-p["beam_t"] - 30, 65, g["z_b"] - 60), t / 2, t / 2 - 3)
            + _pipe((lx + 40, -65, lz - 20), (-p["beam_t"] - 30, -65, g["z_b"] - 60), t / 2, t / 2 - 3))
    catch = _rbox(lx - 95, lx - 60, -70, 70, lz + 100, lz + 160, axis=Axis.Y, radii=(6.0, 3.0))
    add("Base skids and cross tubes", skids + cross, C_FRAME, "painted", 1, "shell", ex_base)
    add("Base plate", plate, C_FRAME, "painted", 1, "shell", ex_base)
    add("Lever bracket, ties and rest stop", bracket + ties + catch, C_FRAME, "painted", 1, "shell", ex_base)
    caps = []
    for yc in (-sy, sy):
        for xe, d in ((-L2, -1), (L2, 1)):
            c = Pos(xe + d * 1.5, yc, sk / 2) * Box(3.0, sk - 1, sk - 1)
            caps.append(_fillet_try(c, c.edges().filter_by(Axis.X), [4.5, 2.0]))
    add("Tube end caps", _sum(caps), C_RUBBER, "rubber", 1, "shell", ex_base)
    # rubber pad under the rest stop, where the lever lands
    add("Rest stop pad", _rbox(lx - 97, lx - 58, -60, 60, lz + 160, lz + 168, radii=(3.0, 1.5)), C_RUBBER,
        "rubber", 1, "shell", ex_base)

    # ============================================================ 1b press core (BOM 1)
    ex_core = (0, 0, -150)
    zc0 = zb_top; zc1 = MT - 10
    cols = None
    for s in (-1, 1):
        yw0, yw1 = sorted((s * (col_y + p["col_b"] / 2 - p["col_web"]), s * (col_y + p["col_b"] / 2)))
        yf0, yf1 = sorted((s * (col_y - p["col_b"] / 2), s * (col_y + p["col_b"] / 2)))
        c = _rbox(-p["col_d"] / 2, p["col_d"] / 2, yw0, yw1, zc0, zc1, radii=(2.0, 1.0)) \
            + _rbox(-p["col_d"] / 2, -p["col_d"] / 2 + p["col_flange"], yf0, yf1, zc0, zc1, radii=(2.0, 1.0)) \
            + _rbox(p["col_d"] / 2 - p["col_flange"], p["col_d"] / 2, yf0, yf1, zc0, zc1, radii=(2.0, 1.0))
        cols = c if cols is None else cols + c
    bz1 = g["z_b"] - 25; bz0 = bz1 - p["beam_d"]
    beam = (_rbox(-p["beam_t"] - 30, -30, -col_y, col_y, bz0, bz1, axis=Axis.X, radii=(4.0, 2.0))
            + _rbox(30, 30 + p["beam_t"], -col_y, col_y, bz0, bz1, axis=Axis.X, radii=(4.0, 2.0))
            + _box(-30, 30, -col_y, col_y, bz0, bz0 + 12))
    lugs = _box(-30, 30, -48, -28, bz1 - 20, g["z_b"] + 40) + _box(-30, 30, 28, 48, bz1 - 20, g["z_b"] + 40)
    lugs = _fillet_try(lugs, lugs.faces().sort_by(Axis.Z)[-1].edges().filter_by(Axis.Y), [20.0, 10.0])
    feet = _rbox(-70, 70, -col_y - 45, -col_y + 45, zc0, zc0 + 16, radii=(8.0, 4.0)) \
        + _rbox(-70, 70, col_y - 45, col_y + 45, zc0, zc0 + 16, radii=(8.0, 4.0))
    add("Press columns, UPN 80", cols, C_CORE, "painted", 1, "shell", ex_core)
    add("Base beam, lugs and column feet", beam + lugs + feet, C_CORE, "painted", 1, "shell", ex_core)
    fb = [_bolt_z(xb, yc + dy, zc0 + 16, 12.0) for xb in (-55, 55) for yc in (-col_y, col_y) for dy in (-30, 30)]
    add("M12 bolts, column feet", _sum(fb), C_ZINC, "metal", 11, "shell", ex_core)
    # pinch-point labels on both column webs (yellow square, black triangle and bar)
    lab = []
    ywf = -(col_y + p["col_b"] / 2)
    for zc in (560.0,):
        sq = _front(_fillet_try(Box(56, 56, 0.8, align=(Align.CENTER, Align.CENTER, Align.MIN)),
                                Box(56, 56, 0.8, align=(Align.CENTER, Align.CENTER, Align.MIN)).edges().filter_by(Axis.Z),
                                [4.0, 2.0]), 0, ywf, zc)
        lab.append(sq)
    add("Pinch-point label", _sum(lab), C_YELLOW, "paper", None, "shell", ex_core)
    tri = extrude(RegularPolygon(22, 3, rotation=90) - RegularPolygon(16, 3, rotation=90), amount=0.6)
    mark = Pos(0, 3.0, 0) * tri + Pos(0, 0, 0) * Box(4.0, 14.0, 0.6, align=(Align.CENTER, Align.CENTER, Align.MIN))
    add("Pinch-point label symbol", _front(Pos(0, 0, 0.8) * mark, 0, ywf, 560.0), C_INK, "paper", None, "shell", ex_core)

    # ============================================================ 2 mold box (BOM 2)
    ex_mold = (0, 0, 420)
    mold = _rbox(-ox, ox, -oy, oy, MB, MT, radii=(3.0, 1.5)) - _box(-BL / 2, BL / 2, -BW / 2, BW / 2, MB - 1, MT + 1)
    bt, bh = p["belt_t"], p["belt_h"]
    belt = _rbox(-ox - bt, ox + bt, -oy - bt, oy + bt, MT - bh, MT, radii=(8.0, 4.0)) \
        - _box(-ox + 1, ox - 1, -oy + 1, oy - 1, MT - bh - 1, MT + 1)
    fl = p["flange_t"]
    flanges = _rbox(-p["col_d"] / 2 - 20, p["col_d"] / 2 + 20, oy, oy + fl, MB, MT - bh, axis=Axis.Y, radii=(6.0, 3.0)) \
        + _rbox(-p["col_d"] / 2 - 20, p["col_d"] / 2 + 20, -oy - fl, -oy, MB, MT - bh, axis=Axis.Y, radii=(6.0, 3.0))
    guide = _rbox(-50, 50, -oy, oy, MB - 16, MB, axis=Axis.Y, radii=(4.0, 2.0)) \
        - _box(-r / 2 - 1, r / 2 + 1, -r / 2 - 1, r / 2 + 1, MB - 17, MB + 1)
    hx = p["lid_l"] / 2 + 5
    hinge_base = _rbox(ox + bt, hx + 30, -p["lid_w"] / 2, p["lid_w"] / 2, MT - 40, MT - 10, axis=Axis.Y, radii=(5.0, 2.0)) \
        - _ypin(hx, MT + 10, 62, p["lid_w"] + 2)
    keeper = _rbox(-p["lid_l"] / 2 - 40, -ox - bt, -30, 30, MT - 95, MT - 65, axis=Axis.X, radii=(4.0, 2.0))
    add("Mold box, 290 x 140 mm cavity", mold + belt + flanges + guide + hinge_base + keeper, C_MOLD, "painted", 2,
        "shell", ex_mold)
    # wear-bright rim on the mold top (ground flat), a thin band inside the belt
    rim = _box(-ox - bt + 0.5, ox + bt - 0.5, -oy - bt + 0.5, oy + bt - 0.5, MT - 0.6, MT) - \
        _box(-BL / 2, BL / 2, -BW / 2, BW / 2, MT - 2, MT + 1)
    add("Mold rim, ground face", rim, C_STEEL, "metal", 2, "shell", ex_mold)
    # nameplate on the belt front
    yb = -oy - bt
    NPX = (p["col_d"] / 2 + ox + bt) / 2 + 2      # right of the -Y column, clear of it
    npl = Box(118, 32, 1.2, align=(Align.CENTER, Align.CENTER, Align.MIN))
    npl = _fillet_try(npl, npl.edges().filter_by(Axis.Z), [4.0, 2.0])
    add("Nameplate", _front(npl, NPX, yb, MT - bh / 2), C_LABEL, "paper", None, "shell", ex_mold)
    txt = _text("EARTHPRESS", 13.0, 0.8)
    if txt is not None:
        add("Nameplate lettering", _front(Pos(0, 0, 1.2) * txt, NPX, yb, MT - bh / 2), C_LID, "painted",
            None, "shell", ex_mold)
    # M16 bolt heads on the column webs (eight, through the mold flanges)
    mb = []
    for s in (-1, 1):
        yw = s * (col_y + p["col_b"] / 2)
        for xb in (-22, 22):
            for zb_ in (MB + 35, MT - bh - 35):
                mb.append(_bolt_y(xb, yw, zb_, 16.0, s))
    add("M16 bolts, mold flanges", _sum(mb), C_ZINC, "metal", 11, "shell", ex_mold)

    # ============================================================ 3 lid (BOM 3)
    ex_lid = (0, 0, 780)
    lt, ll, lw = p["lid_t"], p["lid_l"], p["lid_w"]
    lid = _rbox(-ll / 2, ll / 2, -lw / 2, lw / 2, MT, MT + lt, radii=(12.0, 6.0))
    lid = _fillet_try(lid, lid.faces().sort_by(Axis.Z)[-1].edges(), [3.0, 1.5])
    for s in (-1, 1):
        rb = _box(-ll / 2 + 8, ll / 2 - 8, s * p["rib_y"] - p["rib_t"] / 2, s * p["rib_y"] + p["rib_t"] / 2,
                  MT + lt - 1, MT + lt + p["rib_h"])
        rb = _fillet_try(rb, rb.faces().sort_by(Axis.Z)[-1].edges(), [5.0, 3.0, 1.5])
        lid = lid + rb
    lid = lid + _ypin(hx, MT + 10, 60, lw) - _ypin(hx, MT + 10, p["hinge_pin_d"] + 1, lw + 2)
    hook = _rbox(-ll / 2 - 40, -ll / 2 + 2, -45, 45, MT - 60, MT + lt, axis=Axis.Y, radii=(10.0, 5.0))
    lid = lid + hook
    add("Lid with ribs, hinge and latch", lid, C_LID, "painted", 3, "shell", ex_lid)
    hpin = _pin(hx, MT + 10, p["hinge_pin_d"], lw + 30)
    hclips = _clip(hx, MT + 10, p["hinge_pin_d"], lw / 2 + 5) + _clip(hx, MT + 10, p["hinge_pin_d"], -lw / 2 - 5)
    lpx, lpz = -ll / 2 - 20, MT - 40
    lpin = _pin(lpx, lpz, p["latch_pin_d"], 120)
    add("Hinge and latch pins", hpin + lpin, C_STEEL, "metal", 3, "shell", ex_lid)
    add("Hinge pin circlips", hclips + _clip(lpx, lpz, 30, 55) + _clip(lpx, lpz, 30, -55), C_CLIP, "metal", 3,
        "shell", ex_lid)
    # rubber grip on the latch hook, where the operator lifts the lid
    lg = _rbox(-ll / 2 - 44, -ll / 2 - 34, -40, 40, MT - 30, MT + lt - 4, axis=Axis.Y, radii=(3.0, 1.5))
    add("Latch hook grip", lg, C_RUBBER, "rubber", 3, "shell", ex_lid)

    # ============================================================ 4 piston and push rod (BOM 4)
    ex_pis = (620, 0, 650)
    knee, z_p, z_face = toggle_state(th, p)
    cl = p["piston_clear"]
    pl_ = _rbox(-BL / 2 + cl, BL / 2 - cl, -BW / 2 + cl, BW / 2 - cl, z_face - p["piston_t"], z_face, radii=(3.0, 1.5))
    slot_top = z_p + p["pin_d"] / 2
    rod_bot = slot_top - p["slot_len"] - 15
    rod = _rbox(-r / 2, r / 2, -r / 2, r / 2, rod_bot, z_face - p["piston_t"], radii=(3.0, 1.5))
    slot = _box(-p["pin_d"] / 2 - 1, p["pin_d"] / 2 + 1, -r / 2 - 1, r / 2 + 1, slot_top - p["slot_len"] + p["pin_d"] / 2 + 1,
                slot_top - p["pin_d"] / 2 - 1)
    slot += _ypin(0, slot_top - p["slot_len"] + p["pin_d"] / 2 + 1, p["pin_d"] + 2, r + 2)
    slot += _ypin(0, slot_top - p["pin_d"] / 2 - 1, p["pin_d"] + 2, r + 2)
    rod = rod - slot
    foot = _pin(0, rod_bot + 15, 25, 110)
    add("Piston and slotted push rod", pl_ + rod + foot, C_STEEL, "metal", 4, "internal", ex_pis)

    # ============================================================ 5 toggle (BOM 5)
    ex_tog = (380, 0, -60)
    zb = g["z_b"]
    kx, kz = knee
    lw_, lt_ = p["link_w"], p["link_t"]
    links = []
    ys_up = (-(r / 2 + lt_ / 2 + 2), r / 2 + lt_ / 2 + 2)
    ys_lo = (-(r / 2 + 1.5 * lt_ + 6), r / 2 + 1.5 * lt_ + 6)
    for y in ys_up:
        links.append(_link((0, z_p), (kx, kz), lw_, lt_, y))
    for y in ys_lo:
        links.append(_link((0, zb), (kx, kz), lw_, lt_, y))
    add("Toggle links", _sum(links), C_LINK, "painted", 5, "internal", ex_tog)
    (cx, cz), psi = knee_and_crank(th, p)
    add("Connecting link", _link((cx, cz), (kx, kz), 50, p["conlink_t"], 0), C_LINK, "painted", 5, "internal", ex_tog)
    plen = 2 * (r / 2 + 2 * lt_ + 12)
    pins, clips, nips, bushes = [], [], [], []
    for (x, z) in ((0, z_p), (kx, kz), (0, zb)):
        pins.append(_pin(x, z, p["pin_d"], plen))
        clips += [_clip(x, z, p["pin_d"], plen / 2 - 4), _clip(x, z, p["pin_d"], -plen / 2 + 4)]
        nips.append(_nipple(x, z, -plen / 2, -1))
    # bush flanges on the outer faces of the links (case-hardened bushes)
    for y in ys_lo:
        yo = y + math.copysign(lt_ / 2 + 0.75, y)
        for (x, z) in ((kx, kz), (0, zb)):
            bushes.append(Pos(x, yo, z) * Rot(90, 0, 0) * (Cylinder(p["pin_d"] / 2 + 6, 1.5) - Cylinder(p["pin_d"] / 2, 2.0)))
    for y in ys_up:
        yo = y + math.copysign(lt_ / 2 + 0.75, y)
        bushes.append(Pos(0, yo, z_p) * Rot(90, 0, 0) * (Cylinder(p["pin_d"] / 2 + 6, 1.5) - Cylinder(p["pin_d"] / 2, 2.0)))
    add("Toggle pins, 35 mm", _sum(pins), C_STEEL, "metal", 5, "internal", ex_tog)
    add("Toggle pin circlips", _sum(clips), C_CLIP, "metal", 5, "internal", ex_tog)
    add("Bush flanges", _sum(bushes), C_ZINC, "metal", 5, "internal", ex_tog)
    add("Grease nipples", _sum(nips), C_BRASS, "metal", 5, "internal", ex_tog)

    # ============================================================ 6 lever hub, crank and lever (BOM 6)
    ex_hub = (0, -350, -250)
    lxz = (lx, lz)
    hub = _pin(lx, lz, 80, 100) + _pin(lx, lz, 40, 150)
    crank = _link(lxz, (cx, cz), 50, 20, 26) + _link(lxz, (cx, cz), 50, 20, -26)
    phi = math.radians(math.degrees(psi) + p["lever_offset"])
    ux, uz = math.cos(phi), math.sin(phi)
    ro = p["lever_od"] / 2
    sock_end = (lx + 250 * ux, 0, lz + 250 * uz)
    socket = _pipe((lx, 0, lz), sock_end, ro + 6, ro + 0.5)
    add("Lever hub, crank plates and socket", hub + crank + socket, C_LEVER, "painted", 6, "shell", ex_hub)
    cpin = _pin(cx, cz, 30, 90)
    add("Crank pin", cpin, C_STEEL, "metal", 6, "internal", ex_hub)
    add("Crank pin circlips", _clip(cx, cz, 30, 40) + _clip(cx, cz, 30, -40), C_CLIP, "metal", 6, "internal", ex_hub)
    add("Hub shaft circlips", _clip(lx, lz, 40, 70) + _clip(lx, lz, 40, -70), C_CLIP, "metal", 6, "shell", ex_hub)
    # removable lever: 2 in pipe in the socket, T-handle, rubber grips and end caps
    ex_lev = (-290 + 0 * ux, -350, -50)
    tip = (lx + p["lever_len"] * ux, 0, lz + p["lever_len"] * uz)
    lever = _pipe((lx + 30 * ux, 0, lz + 30 * uz), tip, ro, ro - p["lever_wall"])
    gx, gz = lx + p["grip_r"] * ux, lz + p["grip_r"] * uz
    tb = p["tbar"]
    tbar = _pipe((gx, -tb / 2, gz), (gx, tb / 2, gz), 16.7, 13.0)
    add("Lever pipe and T-handle", lever + tbar, C_LEVER, "painted", 6, "accessory", ex_lev)
    grips = None
    for s in (-1, 1):
        gr = _rod((gx, s * 60.0, gz), (gx, s * (tb / 2 - 2), gz), 19.5) - _rod((gx, s * 55.0, gz), (gx, s * (tb / 2 + 5), gz), 16.8)
        for k in range(8):   # shallow grip rings
            yk = s * (80.0 + 20.0 * k)
            gr -= Pos(gx, yk, gz) * Rot(90, 0, 0) * (Cylinder(21.0, 3.0) - Cylinder(18.6, 4.0))
        grips = gr if grips is None else grips + gr
    tcap = _rod((gx, tb / 2 - 4, gz), (gx, tb / 2 + 8, gz), 19.5) + _rod((gx, -tb / 2 + 4, gz), (gx, -tb / 2 - 8, gz), 19.5)
    tcap = _fillet_try(tcap, tcap.edges(), [3.0, 1.5])
    ecap = _rod((tip[0] - 4 * ux, 0, tip[2] - 4 * uz), (tip[0] + 10 * ux, 0, tip[2] + 10 * uz), ro + 1.5)
    ecap = _fillet_try(ecap, ecap.edges(), [4.0, 2.0])
    add("T-handle rubber grips", grips + tcap + ecap, C_RUBBER, "rubber", 6, "accessory", ex_lev)

    # ============================================================ 7 eject lever, fork, pawl (BOM 7)
    ex_ej = (350, 450, -150)
    exx, ezz = p["eject_x"], p["eject_z"]
    footp = (0, rod_bot + 15)
    a = math.atan2(footp[1] - ezz, footp[0] - exx)
    fork = _link((exx, ezz), footp, 40, 16, 45) + _link((exx, ezz), footp, 40, 16, -45)
    ej_hub = _pin(exx, ezz, 60, 120) + _rbox(exx - 30, exx + 30, -70, -60, sk - 5, ezz, axis=Axis.Y, radii=(6.0, 3.0)) \
        + _rbox(exx - 30, exx + 30, 60, 70, sk - 5, ezz, axis=Axis.Y, radii=(6.0, 3.0))
    ej_hub += Pos(exx, -65, ezz) * Rot(90, 0, 0) * Cylinder(30, 10) + Pos(exx, 65, ezz) * Rot(90, 0, 0) * Cylinder(30, 10)
    sa = a + math.pi + math.radians(30)
    ej_sock = _pipe((exx, 0, ezz), (exx + 260 * math.cos(sa), 0, ezz + 260 * math.sin(sa)), ro + 6, ro + 0.5)
    add("Eject lever, fork and socket", fork + ej_hub + ej_sock, C_EJECT, "painted", 7, "shell", ex_ej)
    add("Eject pivot pin", _pin(exx, ezz, 30, 160), C_STEEL, "metal", 7, "shell", ex_ej)
    pawl = _rbox(lx - 30, lx + 30, 75, 95, lz + 45, lz + 110, axis=Axis.Y, radii=(8.0, 4.0))
    add("End-of-stroke pawl", pawl, C_LINK, "painted", 7, "shell", (0, 250, -250))

    # ============================================================ 8 soil sieve (BOM 8), accessory
    ex_sv = (500, 750, 0)
    SX, SY = 250.0, 690.0
    loc = Pos(SX, SY, 420) * Rot(0, -25, 0)
    frame = Box(45, 700, 900) - Box(47, 610, 810)
    frame = _fillet_try(frame, frame.edges().filter_by(Axis.X), [4.0, 2.0])
    add("Soil sieve timber frame", loc * frame, C_WOOD, "wood", 8, "accessory", ex_sv)
    wires = []
    for yy in range(-285, 300, 30):
        wires.append(Pos(0, yy, 0) * Cylinder(1.6, 812))
    for zz in range(-390, 400, 30):
        wires.append(Pos(0, 0, zz) * Rot(90, 0, 0) * Cylinder(1.6, 612))
    add("Sieve mesh, 5 mm (shown coarse)", loc * Compound(children=wires), C_MESH, "metal", 8, "accessory", ex_sv)
    props = _rod((SX + 130, SY - 300, 0), (SX + 20, SY - 300, 660), 14) + _rod((SX + 130, SY + 300, 0), (SX + 20, SY + 300, 660), 14)
    add("Sieve prop", props, C_WOOD, "wood", 8, "accessory", ex_sv)

    # ============================================================ 9 soil test kit (BOM 9), accessory
    ex_kit = (300, -650, 0)
    KX, KY = 450.0, -650.0
    crate = _rbox(KX - 200, KX + 200, KY - 150, KY + 150, 0, 250, radii=(14.0, 8.0))
    crate = _fillet_try(crate, crate.faces().sort_by(Axis.Z)[-1].edges(), [3.0, 1.5])
    crate -= _rbox(KX - 188, KX + 188, KY - 138, KY + 138, 10, 260, radii=(8.0, 4.0))
    for xs in (-1, 1):   # hand holes in the end walls
        crate -= Pos(KX + xs * 195, KY, 205) * Rot(0, 90, 0) * extrude(RectangleRounded(30, 110, 14.9), amount=30,
                                                                     both=True)
    for k in range(-3, 4):   # vent slots on the long walls
        crate -= Pos(KX + k * 48, KY, 110) * Box(14, 320, 120)
    add("Test kit crate", crate, C_CRATE, "plastic", 9, "accessory", ex_kit)
    lid_s = _rbox(KX - 150, KX + 150, KY + 55, KY + 105, 250, 290, radii=(3.0, 1.5))
    add("Shrinkage box", lid_s, C_WOOD, "wood", 9, "accessory", ex_kit)
    jars, lids, layers = [], [], []
    for jx in (KX - 80, KX + 40):
        jy = KY - 40
        j = Pos(jx, jy, 250 + 80) * Cylinder(45, 160)
        j = _fillet_try(j, j.faces().sort_by(Axis.Z)[0].edges(), [6.0, 3.0])
        j -= Pos(jx, jy, 250 + 88) * Cylinder(42, 160)
        jars.append(j)
        lc = Pos(jx, jy, 410 + 10) * Cylinder(47, 20)
        lc = _fillet_try(lc, lc.faces().sort_by(Axis.Z)[-1].edges(), [3.0, 1.5])
        lids.append(lc)
        z0 = 258.5
        for hgt, col in ((34.0, "#A77B52"), (26.0, "#8C6A4F"), (22.0, "#6F5A4A")):
            layers.append((Pos(jx, jy, z0 + hgt / 2) * Cylinder(41.5, hgt), col))
            z0 += hgt
        layers.append((Pos(jx, jy, z0 + 40) * Cylinder(41.5, 80), "#C9B79A"))
    add("Sedimentation jars, 1 L", _sum(jars), C_JAR, "clear", 9, "accessory", ex_kit)
    add("Jar lids", _sum(lids), C_LID, "plastic", 9, "accessory", ex_kit)
    add("Settled sand layer", _sum([s for s, c in layers[0::4]]), "#A77B52", "paper", 9, "accessory", ex_kit)
    add("Settled silt layer", _sum([s for s, c in layers[1::4]]), "#8C6A4F", "paper", 9, "accessory", ex_kit)
    add("Settled clay layer", _sum([s for s, c in layers[2::4]]), "#6F5A4A", "paper", 9, "accessory", ex_kit)
    add("Cloudy water", _sum([s for s, c in layers[3::4]]), "#C9B79A", "clear", 9, "accessory", ex_kit)
    chart = Pos(KX + 110, KY - 151, 150) * Rot(90, 0, 0) * Box(120, 170, 1.0)
    add("Laminated test chart label", chart, C_LABEL, "paper", 9, "accessory", ex_kit)
    cbar = Pos(KX + 110, KY - 152, 215) * Rot(90, 0, 0) * Box(120, 26, 1.0)
    add("Test chart header", cbar, C_MOLD, "paper", 9, "accessory", ex_kit)

    # ============================================================ context: ground, blocks, fill, person
    BX, BY = 1000.0, -300.0
    GZ = 4 * p["blk_h"]
    gauge = (Pos(BX, BY, GZ + 6) * Box(340, 30, 12) + Pos(BX - 164, BY, GZ - 20) * Box(12, 30, 40)
             + Pos(BX + 164, BY, GZ - 20) * Box(12, 30, 40))
    gauge = _fillet_try(gauge, gauge.edges().filter_by(Axis.Y), [2.0, 1.0])
    add("Block gauge", gauge, C_ZINC, "metal", 10, "accessory", (0, 0, 150))
    add("Block gauge grip", Pos(BX, BY, GZ + 13) * _fillet_try(Box(90, 26, 4), Box(90, 26, 4).edges(), [1.5, 0.8]),
        C_MOLD, "rubber", 10, "accessory", (0, 0, 150))

    # compact patch hugging the operator, press, test kit, blocks and sieve (plan polygon)
    pts = [(-3000, -400), (150, -880), (720, -880), (1260, -620), (1260, 120), (560, 1100), (-560, 1100),
           (-3000, 400)]
    ground = Pos(0, 0, -40) * extrude(Polygon(*pts, align=None), amount=40)
    ground = _fillet_try(ground, ground.edges().filter_by(Axis.Z), [80.0, 40.0])
    ground = _fillet_try(ground, ground.faces().sort_by(Axis.Z)[-1].edges(), [8.0, 4.0])
    add("Ground patch (compacted earth)", ground, C_GROUND, "paper", None, "context", (0, 0, 0))
    blocks = []
    for c_ in range(4):
        for i in range(2):
            for j in range(4):
                bb_ = Box(BL - 6, BW - 6, p["blk_h"] - 2)
                bb_ = _fillet_try(bb_, bb_.edges(), [3.0, 1.5])
                blocks.append(Pos(BX + (i - 0.5) * 300, BY + (j - 1.5) * 150, p["blk_h"] * (c_ + 0.5)) * bb_)
    add("Pressed blocks (context)", Compound(children=blocks), C_BLOCK, "paper", None, "context", (0, 0, 0))
    fill = _box(-BL / 2 + 2, BL / 2 - 2, -BW / 2 + 2, BW / 2 - 2, z_face, MT - 2)
    add("Loose soil fill (context)", fill, C_SOIL, "paper", None, "context", (0, 0, 0))

    if with_person:
        from context_parts import mannequin, mannequin_landmarks
        lm = mannequin_landmarks(MQ_HEIGHT, "push", **MQ_JOINTS)
        hx_l, hy_l, hz_l = lm["hands"][0]
        # figure faces -Y; Rot(0, 0, 90) turns it to face +X: local (x, y) -> world (-y, x)
        person = Pos(gx + hy_l, 0, 0) * Rot(0, 0, 90) * mannequin(MQ_HEIGHT, "push", **MQ_JOINTS)
        add("Operator, 1.75 m (clay mannequin, pushing)", person, C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for q in product_parts():
        s = q["shape"]
        print(f"{q['name']:44s} {q['group']:9s} {q['material']:8s} valid={s.is_valid} vol={s.volume / 1e6:8.3f} L")
