"""EarthPress product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders of the manual compressed earth block press: rounded
tube and plate edges, painted steel in a restrained palette, round-ended toggle and crank links,
bright turned pins with circlips, felt dust seals at the bush faces and grease nipples, M16 and M12 bolt heads, rubber
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
from model import (PARAMS, geometry, theta_start, toggle_state, knee_and_crank, derived, build_components,
                   _box, _rod, _pipe, _flat, _ypin)

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
C_FELT = "#7A5C3A"       # felt dust seals
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
    D = derived(p)
    C = build_components(p, theta=th)           # the constructable design at the pose, from model.py
    BL, BW = p["blk_l"], p["blk_w"]
    MT = D["MT"]
    sk, sy = p["skid"], p["skid_y"]
    L2 = p["skid_len"] / 2
    lx, lz = p["lever_x"], p["lever_z"]
    zb = g["z_b"]
    knee, z_p, z_face = toggle_state(th, p)
    kx, kz = knee
    (cx, cz), psi = knee_and_crank(th, p)
    ylw, yu = D["y_lower"], D["y_upper"]

    def sh(*keys):
        shp = _sum([C[k].shape for k in keys])
        if shp.is_valid:
            return shp
        return Compound(children=[C[k].shape for k in keys])      # keep the pieces apart where a fuse is not clean

    # Every steel part below is the shape from model.py itself (so the dimensions, holes, bosses, round link
    # ends, guard and bolts match the constructable design); only paint, rubber, felt, circlips and the like are
    # added as appearance. Explode offsets are for the exploded view only.
    ex_base, ex_core, ex_mold, ex_lid = (0, 0, -250), (0, 0, -150), (0, 0, 420), (0, 0, 780)
    ex_pis, ex_tog, ex_hub, ex_ej = (620, 0, 650), (380, 0, -60), (0, -350, -250), (350, 450, -150)
    add("Base skids and cross tubes", sh("skids", "cross"), C_FRAME, "painted", 1, "shell", ex_base)
    add("Base plate", sh("base_plate"), C_FRAME, "painted", 1, "shell", ex_base)
    add("Lever bracket, ties, rest stop and eject posts", sh("bracket", "rest", "ties", "posts"), C_FRAME, "painted", 1, "shell", ex_base)
    caps = []
    for yc in (-sy, sy):
        for xe, d in ((-L2, -1), (L2, 1)):
            c = Pos(xe + d * 1.5, yc, sk / 2) * Box(3.0, sk - 1, sk - 1)
            caps.append(_fillet_try(c, c.edges().filter_by(Axis.X), [4.5, 2.0]))
    add("Tube end caps", _sum(caps), C_RUBBER, "rubber", 1, "shell", ex_base)
    add("Press columns, UPN 80", sh("columns"), C_CORE, "painted", 1, "shell", ex_core)
    add("Base beam, lugs and column feet", sh("beam", "lugs", "feet"), C_CORE, "painted", 1, "shell", ex_core)
    add("Mold box, 290 x 140 mm cavity", sh("mold", "flanges", "mold_lugs"), C_MOLD, "painted", 2, "shell", ex_mold)
    add("Lid with ribs, hinge and latch ears", sh("lid"), C_LID, "painted", 3, "shell", ex_lid)
    add("Hinge and latch pins", sh("hinge_pin", "latch_pin"), C_STEEL, "metal", 3, "shell", ex_lid)
    add("Piston, end skirts and slotted push rod", sh("piston"), C_STEEL, "metal", 4, "internal", ex_pis)
    add("Toggle links", sh("lower_links", "upper_links"), C_LINK, "painted", 5, "internal", ex_tog)
    add("Connecting link", sh("conlink"), C_LINK, "painted", 5, "internal", ex_tog)
    add("Toggle pins, 35 mm", sh("base_pin", "knee_pin", "upper_pin"), C_STEEL, "metal", 5, "internal", ex_tog)
    add("Pin spacer tubes", sh("base_spacers", "knee_spacers"), C_CLIP, "metal", 5, "internal", ex_tog)
    add("Bush dust seals (felt)", sh("seals_base", "seals_knee", "seals_upper"), C_FELT, "fabric", 5, "internal", ex_tog)
    # circlips just outside the dust seals, and grease nipples on the -Y pin ends
    clips, nips = [], []
    yb_, yk_, yup_ = ylw[1] + p["seal_t"] + 0.75, ylw[1] + p["seal_t"] + 0.75, yu[1] + p["seal_t"] + 0.75
    for (x, z, yy) in ((0, zb, yb_), (kx, kz, yk_), (0, z_p, yup_)):
        for sg in (-1, 1):
            clips.append(Pos(x, sg * yy, z) * Rot(90, 0, 0) * (Cylinder(p["pin_d"] / 2 + 3.0, 1.5) - Cylinder(p["pin_d"] / 2 - 0.5, 2.0)))
        nips.append(_nipple(x, z, -(yy + 0.75), -1))
    add("Toggle pin circlips", _sum(clips), C_CLIP, "metal", 5, "internal", ex_tog)
    add("Grease nipples", _sum(nips), C_BRASS, "metal", 5, "internal", ex_tog)
    add("Lever hub, crank plates and socket", sh("hub"), C_LEVER, "painted", 6, "shell", ex_hub)
    add("Hub shaft and crank pin", sh("shaft", "crank_pin"), C_STEEL, "metal", 6, "internal", ex_hub)
    ex_lev = (-290, -350, -50)
    phi = math.radians(math.degrees(psi) + p["lever_offset"])
    ux, uz = math.cos(phi), math.sin(phi)
    ro = p["lever_od"] / 2
    add("Lever pipe and T-handle", sh("lever"), C_LEVER, "painted", 6, "accessory", ex_lev)
    add("Lever locking pin", sh("lever_pin"), C_STEEL, "metal", 6, "accessory", ex_lev)
    tip = (lx + p["lever_len"] * ux, 0, lz + p["lever_len"] * uz)
    gx, gz = lx + p["grip_r"] * ux, lz + p["grip_r"] * uz
    tb = p["tbar"]
    grips = None
    for s_ in (-1, 1):
        gr = _rod((gx, s_ * 60.0, gz), (gx, s_ * (tb / 2 - 2), gz), 19.5) - _rod((gx, s_ * 55.0, gz), (gx, s_ * (tb / 2 + 5), gz), 16.8)
        for k in range(8):   # shallow grip rings
            yk = s_ * (80.0 + 20.0 * k)
            gr -= Pos(gx, yk, gz) * Rot(90, 0, 0) * (Cylinder(21.0, 3.0) - Cylinder(18.6, 4.0))
        grips = gr if grips is None else grips + gr
    tcap = _rod((gx, tb / 2 - 4, gz), (gx, tb / 2 + 8, gz), 19.5) + _rod((gx, -tb / 2 + 4, gz), (gx, -tb / 2 - 8, gz), 19.5)
    tcap = _fillet_try(tcap, tcap.edges(), [3.0, 1.5])
    ecap = _rod((tip[0] - 4 * ux, 0, tip[2] - 4 * uz), (tip[0] + 10 * ux, 0, tip[2] + 10 * uz), ro + 1.5)
    ecap = _fillet_try(ecap, ecap.edges(), [4.0, 2.0])
    add("T-handle rubber grips", grips + tcap + ecap, C_RUBBER, "rubber", 6, "accessory", ex_lev)
    add("Eject lever, arm and socket", sh("eject"), C_EJECT, "painted", 7, "shell", ex_ej)
    add("Eject pivot pin", sh("eject_pin"), C_STEEL, "metal", 7, "shell", ex_ej)
    add("End pawl and rest catch", sh("pawl", "catch"), C_LINK, "painted", 7, "shell", (0, 250, -250))
    add("Linkage guard (expanded metal)", sh("guard"), C_YELLOW, "painted", 13, "shell", (0, 0, 200))
    add("Bolts, M16 and M12 and M10", sh("bolts"), C_ZINC, "metal", 11, "shell", ex_core)

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
    add("Block gauge", C["gauge"].shape, C_ZINC, "metal", 10, "accessory", (0, 0, 150))

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
    add("Loose soil fill (context)", C["fill"].shape, C_SOIL, "paper", None, "context", (0, 0, 0))

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
