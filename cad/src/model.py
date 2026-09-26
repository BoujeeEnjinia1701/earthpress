"""EarthPress parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl, and prints the main envelopes and piece masses.

Massing-plus detail: correct interfaces and main dimensions (mold cavity, lid with ribs, hinge
and latch, piston with slotted push rod, toggle links and pins, lever crank and connecting link,
eject lever and fork, bolted frame pieces), not fabrication detail. PRELIMINARY, NOT FOR FABRICATION.

Axes: X along the lever (the compaction lever swings on the -X side, the eject lever on the +X
side), Y across the press, Z up from the ground. Units mm. The piston axis is X = Y = 0.
The press is posed at the start of the compaction stroke: lid closed, toggle bent, lever up.

docs/04-calcs/sizing.py (EPR-CAL-001) imports PARAMS, toggle_state(), knee_and_crank() and
build_parts() so that the calculation note and the geometry use the same numbers.
"""
import math
from pathlib import Path

# Top-level parameters (mm, degrees). Edit these, not the geometry below.
PARAMS = {
    # Block and mold (EPR-DDR-001 item 3: 290 x 140 x 90 mm)
    "blk_l": 290.0, "blk_w": 140.0, "blk_h": 90.0,
    "fill_h": 150.0,             # loose fill depth struck level; compacts to 90 mm
    "mold_top": 940.0,           # rim height above ground (working height for filling)
    "mold_h": 200.0,
    "wall": 12.0,                # mold wall plate
    "belt_t": 16.0, "belt_h": 50.0,   # stiffening belt round the top of the mold
    "flange_t": 16.0,            # mold side flanges bolted to the columns
    # Lid (item 3): 20 mm plate with two 20 x 70 mm ribs along X, hinge on +X, latch on -X
    "lid_t": 20.0, "lid_l": 360.0, "lid_w": 230.0, "rib_t": 20.0, "rib_h": 70.0, "rib_y": 60.0,
    "hinge_pin_d": 30.0, "latch_pin_d": 30.0,
    # Piston and push rod (item 4)
    "piston_t": 25.0, "piston_clear": 1.0,     # clearance per side in the mold
    "rod": 60.0,                 # square push rod
    "pin_below_plate": 40.0,     # upper toggle pin below the piston plate at the end of the stroke
    "slot_len": 200.0,           # lost-motion slot for ejection (160 mm lift plus the pin)
    # Toggle (item 5): equal links, knee toward -X
    "link_l": 245.0, "link_w": 70.0, "link_t": 28.0, "pin_d": 35.0,
    "theta_end": 6.0,            # link angle from vertical at full compaction (nominal fill)
    "theta_stop": 6.0,           # hard stop on the crank at theta_end; limits the force (EPR-CAL-001)
    # Lever and crank (item 6): bell crank at O, connecting link from crank pin C to the knee K
    "lever_x": -468.0, "lever_z": 266.0,
    "crank": 107.0, "conlink": 420.0, "conlink_t": 24.0,
    "grip_r": 1650.0, "lever_len": 1700.0, "lever_od": 60.3, "lever_wall": 3.91,   # 2 in schedule 40
    "lever_offset": 144.0,       # lever angle minus crank angle (fixed by the hub)
    "tbar": 500.0,               # T-handle for a second operator
    # Eject lever (item 7): seesaw pivot on the +X side, fork under the push rod foot
    "eject_x": 160.0, "eject_z": 620.0, "eject_arm": 160.0, "eject_lift": 160.0,
    # Frame (item 1)
    "skid": 60.0, "skid_len": 1000.0, "skid_y": 260.0,
    "base_t": 12.0, "base_l": 240.0, "base_w": 380.0, "bracket_t": 10.0,
    "col_d": 80.0, "col_b": 45.0, "col_web": 6.0, "col_flange": 8.0,    # UPN 80
    "beam_d": 100.0, "beam_t": 20.0,             # two 20 x 100 mm plates spanning the columns
    "tie": 40.0,                 # 40 x 40 x 3 tubes from the lever bracket to the base beam
}

STEEL = 7850.0e-9   # kg/mm3


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _rod(a, b, r):
    """Round bar or pin between two 3D points."""
    from build123d import Plane, Solid, Vector
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _pipe(a, b, ro, ri):
    return _rod(a, b, ro) - _rod(a, b, ri)


def _flat(a, b, w, t, y):
    """Flat bar of width w (in the XZ plane) and thickness t (in Y) between two XZ points at Y = y."""
    from build123d import Box, Pos, Rot
    (ax, az), (bx, bz) = a, b
    L = math.hypot(bx - ax, bz - az)
    ang = math.degrees(math.atan2(bz - az, bx - ax))
    return Pos((ax + bx) / 2, y, (az + bz) / 2) * Rot(0, -ang, 0) * Box(L, t, w)


def _ypin(x, z, d, length, y=0.0):
    from build123d import Cylinder, Pos, Rot
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(d / 2, length)


# ------------------------------------------------------------------ kinematics
def geometry(p=PARAMS):
    """Fixed heights of the toggle: upper pin at the end of the stroke and the base pin."""
    z_block_top = p["mold_top"]
    z_piston_end = z_block_top - p["blk_h"]                     # piston face at full compaction
    z_p_end = z_piston_end - p["piston_t"] - p["pin_below_plate"]
    z_b = z_p_end - 2 * p["link_l"] * math.cos(math.radians(p["theta_end"]))
    return dict(z_piston_end=z_piston_end, z_p_end=z_p_end, z_b=z_b)


def theta_start(p=PARAMS):
    """Toggle angle (rad) at the start of the stroke, 60 mm of piston travel before theta_end."""
    stroke = p["fill_h"] - p["blk_h"]
    c = math.cos(math.radians(p["theta_end"])) - stroke / (2 * p["link_l"])
    return math.acos(c)


def toggle_state(theta, p=PARAMS):
    """Knee (x, z), upper pin height zP and piston face height for a link angle theta (rad)."""
    g = geometry(p)
    L = p["link_l"]
    knee = (-L * math.sin(theta), g["z_b"] + L * math.cos(theta))
    z_p = g["z_b"] + 2 * L * math.cos(theta)
    z_face = z_p + p["pin_below_plate"] + p["piston_t"]
    return knee, z_p, z_face


def knee_and_crank(theta, p=PARAMS):
    """Crank pin (x, z) and crank angle (rad) for a toggle angle theta. Uses the elbow-down branch."""
    (kx, kz), _, _ = toggle_state(theta, p)
    ox, oz, c, m = p["lever_x"], p["lever_z"], p["crank"], p["conlink"]
    dx, dz = kx - ox, kz - oz
    d = math.hypot(dx, dz)
    if not abs(c - m) <= d <= c + m:
        raise ValueError("linkage cannot close at theta = %.2f deg" % math.degrees(theta))
    a = (c * c - m * m + d * d) / (2 * d)
    h = math.sqrt(max(c * c - a * a, 0.0))
    px, pz = ox + a * dx / d, oz + a * dz / d
    cx, cz = px + h * dz / d, pz - h * dx / d      # branch -1 of the design study
    return (cx, cz), math.atan2(cz - oz, cx - ox)


def lever_angle(theta, p=PARAMS):
    """Lever angle (deg, from +X, counterclockwise seen from -Y) for a toggle angle theta."""
    _, psi = knee_and_crank(theta, p)
    return math.degrees(psi) + p["lever_offset"]


# ------------------------------------------------------------------ parts
def build_parts(p=PARAMS, theta=None):
    """Return a list of (name, shape, colour, bom_item, explode_offset). theta: toggle angle, default start."""
    from build123d import Box, Cylinder, Pos, Rot
    b = _box
    th = theta_start(p) if theta is None else theta
    g = geometry(p)
    BL, BW = p["blk_l"], p["blk_w"]
    W = p["wall"]
    MT = p["mold_top"]; MB = MT - p["mold_h"]
    ox, oy = BL / 2 + W, BW / 2 + W                       # mold outer half sizes
    col_y = oy + p["flange_t"] + p["col_b"] / 2           # column centre line (channel toes face the mold)
    sk, sy = p["skid"], p["skid_y"]
    zb_top = sk + p["base_t"]                             # top of the base plate
    parts = []

    # 1a Base on skids: skids, cross members, 12 mm base plate, lever bracket, ties to the base beam, lever catch
    def tube_x(x0, x1, yc, zc, s=sk, w=3.0):
        return b(x0, x1, yc - s / 2, yc + s / 2, zc - s / 2, zc + s / 2) - b(x0 - 1, x1 + 1, yc - s / 2 + w, yc + s / 2 - w, zc - s / 2 + w, zc + s / 2 - w)

    def tube_y(xc, y0, y1, zc, s=50.0, w=3.0):
        return b(xc - s / 2, xc + s / 2, y0, y1, zc - s / 2, zc + s / 2) - b(xc - s / 2 + w, xc + s / 2 - w, y0 - 1, y1 + 1, zc - s / 2 + w, zc + s / 2 - w)

    L2 = p["skid_len"] / 2
    skids = tube_x(-L2, L2, -sy, sk / 2) + tube_x(-L2, L2, sy, sk / 2)
    cross = (tube_y(-L2 + sk / 2, -sy + sk / 2, sy - sk / 2, sk / 2) + tube_y(L2 - sk / 2, -sy + sk / 2, sy - sk / 2, sk / 2)
             + tube_y(-120 - sk / 2, -sy + sk / 2, sy - sk / 2, sk / 2) + tube_y(120 + sk / 2, -sy + sk / 2, sy - sk / 2, sk / 2))
    base_plate = b(-p["base_l"] / 2, p["base_l"] / 2, -p["base_w"] / 2, p["base_w"] / 2, sk, zb_top)
    lx, lz = p["lever_x"], p["lever_z"]
    bt_ = p["bracket_t"]
    bracket = None
    for s_ in (-1, 1):
        y0_, y1_ = s_ * 60, s_ * (60 + bt_)
        pl = b(lx - 45, lx + 45, y0_, y1_, sk, lz + 45) + b(lx - 95, lx - 45, y0_, y1_, lz - 20, lz + 170)
        bracket = pl if bracket is None else bracket + pl
    t = p["tie"]
    ties = (_pipe((lx + 40, 65, lz - 20), (-p["beam_t"] - 30, 65, g["z_b"] - 60), t / 2, t / 2 - 3)
            + _pipe((lx + 40, -65, lz - 20), (-p["beam_t"] - 30, -65, g["z_b"] - 60), t / 2, t / 2 - 3))
    catch = b(lx - 95, lx - 60, -70, 70, lz + 100, lz + 160)                        # rest stop and catch bar
    base = skids + cross + base_plate + bracket + ties + catch
    parts.append(("Base on skids, lever bracket and catch post", base, "#4B5563", 1, (0, 0, -300)))

    # 1b Press core: two UPN 100 columns, base beam (two plates) with the toggle base lugs, gussets
    zc0 = zb_top; zc1 = MT - 10
    cols = None
    for s in (-1, 1):
        web = b(-p["col_d"] / 2, p["col_d"] / 2, s * (col_y + p["col_b"] / 2 - p["col_web"]), s * (col_y + p["col_b"] / 2), zc0, zc1)
        fl = (b(-p["col_d"] / 2, -p["col_d"] / 2 + p["col_flange"], s * (col_y - p["col_b"] / 2), s * (col_y + p["col_b"] / 2), zc0, zc1)
              + b(p["col_d"] / 2 - p["col_flange"], p["col_d"] / 2, s * (col_y - p["col_b"] / 2), s * (col_y + p["col_b"] / 2), zc0, zc1))
        c = web + fl
        cols = c if cols is None else cols + c
    bz1 = g["z_b"] - 25; bz0 = bz1 - p["beam_d"]
    beam = (b(-p["beam_t"] - 30, -30, -col_y, col_y, bz0, bz1) + b(30, 30 + p["beam_t"], -col_y, col_y, bz0, bz1)
            + b(-30, 30, -col_y, col_y, bz0, bz0 + 12))
    lugs = b(-30, 30, -48, -28, bz1 - 20, g["z_b"] + 40) + b(-30, 30, 28, 48, bz1 - 20, g["z_b"] + 40)
    feet = b(-70, 70, -col_y - 45, -col_y + 45, zc0, zc0 + 16) + b(-70, 70, col_y - 45, col_y + 45, zc0, zc0 + 16)
    core = cols + beam + lugs + feet
    parts.append(("Press core, columns and base beam", core, "#6B7280", 1, (0, 0, -150)))

    # 2 Mold box: 12 mm walls round the 290 x 140 cavity, top belt, side flanges, push rod guide plate
    mold = b(-ox, ox, -oy, oy, MB, MT) - b(-BL / 2, BL / 2, -BW / 2, BW / 2, MB - 1, MT + 1)
    bt, bh = p["belt_t"], p["belt_h"]
    belt = b(-ox - bt, ox + bt, -oy - bt, oy + bt, MT - bh, MT) - b(-ox, ox, -oy, oy, MT - bh - 1, MT + 1)
    fl = p["flange_t"]
    flanges = b(-p["col_d"] / 2 - 20, p["col_d"] / 2 + 20, oy, oy + fl, MB, MT - bh) \
        + b(-p["col_d"] / 2 - 20, p["col_d"] / 2 + 20, -oy - fl, -oy, MB, MT - bh)
    guide = b(-50, 50, -oy, oy, MB - 16, MB) - b(-p["rod"] / 2 - 1, p["rod"] / 2 + 1, -p["rod"] / 2 - 1, p["rod"] / 2 + 1, MB - 17, MB + 1)
    hx = p["lid_l"] / 2 + 5
    hinge_base = b(ox + bt, hx + 30, -p["lid_w"] / 2, p["lid_w"] / 2, MT - 40, MT - 10) - _ypin(hx, MT + 10, 62, p["lid_w"] + 2)
    keeper = b(-p["lid_l"] / 2 - 40, -ox - bt, -30, 30, MT - 95, MT - 65)          # latch keeper under the hook
    mold = mold + belt + flanges + guide + hinge_base + keeper
    parts.append(("Mold box, 290 x 140 mm cavity", mold, "#0F766E", 2, (0, 0, 420)))

    # 3 Lid: plate with two ribs, hinge knuckles on +X, latch hook on -X
    lt, ll, lw = p["lid_t"], p["lid_l"], p["lid_w"]
    lid = b(-ll / 2, ll / 2, -lw / 2, lw / 2, MT, MT + lt)
    for s in (-1, 1):
        lid = lid + b(-ll / 2, ll / 2, s * p["rib_y"] - p["rib_t"] / 2, s * p["rib_y"] + p["rib_t"] / 2, MT + lt, MT + lt + p["rib_h"])
    hx = ll / 2 + 5
    lid = lid + _ypin(hx, MT + 10, 60, lw) - _ypin(hx, MT + 10, p["hinge_pin_d"] + 1, lw + 2)   # hinge knuckle tube
    lid = lid + b(-ll / 2 - 40, -ll / 2, -45, 45, MT - 60, MT + lt)                 # latch hook
    parts.append(("Lid with ribs, hinge and latch", lid, "#115E59", 3, (0, 0, 780)))

    # 4 Piston plate and slotted push rod with foot pin
    knee, z_p, z_face = toggle_state(th, p)
    cl = p["piston_clear"]
    plate = b(-BL / 2 + cl, BL / 2 - cl, -BW / 2 + cl, BW / 2 - cl, z_face - p["piston_t"], z_face)
    r = p["rod"]
    slot_top = z_p + p["pin_d"] / 2
    rod_bot = slot_top - p["slot_len"] - 15
    rod = b(-r / 2, r / 2, -r / 2, r / 2, rod_bot, z_face - p["piston_t"])
    rod = rod - b(-p["pin_d"] / 2 - 1, p["pin_d"] / 2 + 1, -r / 2 - 1, r / 2 + 1, slot_top - p["slot_len"], slot_top)
    rod = rod + _ypin(0, rod_bot + 15, 25, 110)                                        # foot pin for the eject fork
    parts.append(("Piston and slotted push rod", plate + rod, "#D4A017", 4, (620, 0, 650)))

    # 5 Toggle: two lower links (outer), two upper links (inner, either side of the rod), three pins,
    #   connecting link from the crank pin to the knee
    zb = g["z_b"]
    kx, kz = knee
    lw_, lt_ = p["link_w"], p["link_t"]
    tog = None
    for y in (-(r / 2 + lt_ / 2 + 2), r / 2 + lt_ / 2 + 2):                         # upper links
        s_ = _flat((0, z_p), (kx, kz), lw_, lt_, y)
        tog = s_ if tog is None else tog + s_
    for y in (-(r / 2 + 1.5 * lt_ + 6), r / 2 + 1.5 * lt_ + 6):                    # lower links, outside
        tog = tog + _flat((0, zb), (kx, kz), lw_, lt_, y)
    for (x, z) in ((0, z_p), (kx, kz), (0, zb)):
        tog = tog + _ypin(x, z, p["pin_d"], 2 * (r / 2 + 2 * lt_ + 12))
    (cx, cz), psi = knee_and_crank(th, p)
    tog = tog + _flat((cx, cz), (kx, kz), 50, p["conlink_t"], 0)                  # connecting link, centre plane
    parts.append(("Toggle links, pins and bushes", tog, "#C2410C", 5, (380, 0, -60)))

    # 6 Lever: hub on a 40 mm shaft in the bracket, crank arm, socket and 2 in pipe with a T-handle
    lxz = (p["lever_x"], p["lever_z"])
    hub = _ypin(lxz[0], lxz[1], 80, 100) + _ypin(lxz[0], lxz[1], 40, 150)
    crank = _flat(lxz, (cx, cz), 50, 20, 26) + _flat(lxz, (cx, cz), 50, 20, -26) + _ypin(cx, cz, 30, 90)
    phi = math.radians(math.degrees(psi) + p["lever_offset"])
    ux, uz = math.cos(phi), math.sin(phi)
    ro = p["lever_od"] / 2
    sock_end = (lxz[0] + 250 * ux, 0, lxz[1] + 250 * uz)
    socket = _pipe((lxz[0], 0, lxz[1]), sock_end, ro + 6, ro + 0.5)
    tip = (lxz[0] + p["lever_len"] * ux, 0, lxz[1] + p["lever_len"] * uz)
    lever = _pipe((lxz[0] + 30 * ux, 0, lxz[1] + 30 * uz), tip, ro, ro - p["lever_wall"])
    grip = (lxz[0] + p["grip_r"] * ux, 0, lxz[1] + p["grip_r"] * uz)
    tbar = _pipe((grip[0], -p["tbar"] / 2, grip[2]), (grip[0], p["tbar"] / 2, grip[2]), 16.7, 13.0)
    parts.append(("Lever, crank hub and T-handle", hub + crank + socket + lever + tbar, "#1F2937", 6, (0, -500, -700)))

    # 7 Eject lever: seesaw on the +X side, fork under the push rod foot pin, socket for the lever; end pawl
    ex, ez = p["eject_x"], p["eject_z"]
    foot = (0, rod_bot + 15)
    a = math.atan2(foot[1] - ez, foot[0] - ex)
    fork_tip = foot                                                                  # tines slide on the foot pin
    fork = _flat((ex, ez), fork_tip, 40, 16, 45) + _flat((ex, ez), fork_tip, 40, 16, -45)
    ej_hub = _ypin(ex, ez, 60, 120) + b(ex - 30, ex + 30, -70, -60, sk - 5, ez + 30) + b(ex - 30, ex + 30, 60, 70, sk - 5, ez + 30)
    sa = a + math.pi + math.radians(30)                                             # socket 30 deg above the fork line
    ej_sock = _pipe((ex, 0, ez), (ex + 260 * math.cos(sa), 0, ez + 260 * math.sin(sa)), ro + 6, ro + 0.5)
    pawl = b(lx - 30, lx + 30, 75, 95, lz + 45, lz + 110)                           # end-of-stroke pawl on the bracket
    parts.append(("Eject lever, fork, catch and end pawl", fork + ej_hub + ej_sock + pawl, "#7C3AED", 7, (350, 450, -150)))

    # 8 Soil sieve (context of use, BOM line): 5 mm mesh in a timber frame on a prop, +Y side
    SX, SY = 1150.0, 750.0
    from build123d import Box as _B
    sieve = Pos(SX, SY, 420) * Rot(0, -25, 0) * (_B(45, 700, 900) - _B(47, 610, 810))
    sieve = sieve + Pos(SX, SY, 420) * Rot(0, -25, 0) * _B(4, 610, 810)
    sieve = sieve + _rod((SX + 130, SY - 300, 0), (SX + 20, SY - 300, 660), 12) + _rod((SX + 130, SY + 300, 0), (SX + 20, SY + 300, 660), 12)
    parts.append(("Soil sieve, 5 mm mesh", sieve, "#A16207", 8, (400, 600, 0)))

    # 9 Soil test kit: crate with sedimentation jars, shrinkage box and scale
    kit = (Pos(450, -700, 125) * Box(400, 300, 250)
           + Pos(370, -740, 340) * Cylinder(45, 180) + Pos(490, -740, 340) * Cylinder(45, 180)
           + Pos(450, -620, 270) * Box(300, 50, 40))
    parts.append(("Soil test kit", kit, "#2563EB", 9, (-300, -700, 0)))

    # 10 Block gauge on the block stack (context)
    BX, BY = 1000.0, -300.0
    GZ = 4 * p["blk_h"]
    gauge = (Pos(BX, BY, GZ + 6) * Box(340, 30, 12) + Pos(BX - 164, BY, GZ - 20) * Box(12, 30, 40)
             + Pos(BX + 164, BY, GZ - 20) * Box(12, 30, 40))
    parts.append(("Block gauge", gauge, "#16A34A", 10, (300, -300, 450)))

    # Context: loose soil in the mold and a stack of pressed blocks
    fill = b(-BL / 2 + 2, BL / 2 - 2, -BW / 2 + 2, BW / 2 - 2, z_face, MT - 2)
    parts.append(("Loose soil fill (context)", fill, "#B7794A", None, (0, 0, 1200)))
    blocks = None
    for c_ in range(4):
        for i in range(2):
            for j in range(4):
                bb_ = Pos(BX + (i - 0.5) * 300, BY + (j - 1.5) * 150, p["blk_h"] * (c_ + 0.5)) \
                    * Box(BL - 6, BW - 6, p["blk_h"] - 2)
                blocks = bb_ if blocks is None else blocks + bb_
    parts.append(("Pressed blocks (context)", blocks, "#C08A5B", None, (300, -300, 0)))
    return parts


CONTEXT = ("Soil sieve, 5 mm mesh", "Soil test kit", "Block gauge", "Loose soil fill (context)", "Pressed blocks (context)")


def assemblies(parts=None):
    """Named compounds for export: the press (steel parts only) and the full set with kit and context."""
    import copy
    from build123d import Compound
    parts = parts or build_parts()
    press = [copy.copy(s) for n, s, *_ in parts if n not in CONTEXT]
    return {
        "earthpress-assembly": Compound(children=press),
        "earthpress-set": Compound(children=[copy.copy(s) for n, s, *_ in parts]),
    }


def piece_masses(parts=None):
    """Mass (kg) of each steel piece of the press, from the model volumes at 7,850 kg/m3."""
    parts = parts or build_parts()
    return {n: s.volume * STEEL for n, s, *_ in parts if n not in CONTEXT}


if __name__ == "__main__":
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    asm = assemblies(parts)
    for name, shape in asm.items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"))
    for n, s, *_ in parts:
        if n.startswith("Lid") or n.startswith("Mold") or n.startswith("Toggle"):
            slug = n.split(",")[0].split(" ")[0].lower()
            export_step(s, str(root / "step" / f"earthpress-{slug}.step"))
            export_stl(s, str(root / "stl" / f"earthpress-{slug}.stl"))
    bb = asm["earthpress-assembly"].bounding_box()
    print("press envelope (mm): %.0f x %.0f x %.0f" % (bb.size.X, bb.size.Y, bb.size.Z))
    for n, m in piece_masses(parts).items():
        print("  %-48s %6.1f kg" % (n, m))
    print("wrote cad/step and cad/stl")
