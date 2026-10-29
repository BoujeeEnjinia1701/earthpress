"""EarthPress parametric model (build123d), TRL 3, constructable design (EPR-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl, print masses
    python cad/src/model.py --check    run the constructability checks (overlaps, contacts, sweeps)

Every part is modelled as it is made: plates and sections cut to size, holes where the pins and
bolts go, round ends on every link, and the fixings (pins, spacers, bolts) that hold the parts
together. build_components() returns the parts one by one (for the checks and the build plan
pictures); build_parts() groups them into the ten numbered BOM lines for the concept media and
the calculation note. PRELIMINARY, NOT FOR FABRICATION.

Axes: X along the lever (the compaction lever swings on the -X side, the eject lever on the +X
side), Y across the press, Z up from the ground. Units mm. The piston axis is X = Y = 0.
The default pose is the start of the compaction stroke: lid closed, toggle bent, lever on its
rest stop, leaning 8 degrees over the press.

docs/04-calcs/sizing.py (EPR-CAL-001) imports PARAMS, toggle_state(), knee_and_crank() and
piece_masses() so that the calculation note and the geometry use the same numbers.
"""
import math
import sys
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
    "flange_t": 16.0,            # mold side flanges, tapped M16, bolted to the column webs
    # Lid (item 3): 20 mm plate with two 20 x 70 mm ribs along X; the rib ends are cut as ears
    # that carry the hinge pin (+X) and the latch pin (-X) (EPR-DDR-003 P6, P7)
    "lid_t": 20.0, "lid_l": 360.0, "lid_w": 230.0, "rib_t": 20.0, "rib_h": 70.0, "rib_y": 60.0,
    "hinge_pin_d": 30.0, "latch_pin_d": 30.0,
    "hinge_x": 210.0, "hinge_z": 950.0, "latch_x": -210.0, "latch_z": 915.0,
    "lug_t": 20.0, "lug_y0": 72.0,     # mold hinge and latch lugs, 20 mm plate, inner face 72 mm off centre
    # Piston and push rod (item 4)
    "piston_t": 25.0, "piston_clear": 1.0,     # clearance per side in the mold
    "skirt_t": 12.0, "skirt_h": 60.0,          # end skirts keep the piston square in the mold (P3)
    "rod": 60.0,                 # square push rod
    "pin_below_plate": 40.0,     # upper toggle pin below the piston plate at the end of the stroke
    "rod_foot": 12.5,            # solid rod below the slot (was 15; keeps the eject nose on the foot with the longer slot)
    "slot_len": 205.0,           # lost-motion slot for ejection (160 mm lift plus the 40 mm pin and 5 mm; was 200)
    # Toggle (item 5): equal links, knee toward -X
    "seal_t": 2.0, "seal_od": 56.0, "seal_id": 40.5,   # dust seal washers at the bush faces (cover the 46 mm bush)
    # toggle pins 40 mm 42CrMo4 +QT in 40 x 46 mm bushes (were 35 mm C45 in 35 x 41 mm): the 35 mm pins yielded in
    # bending (EPR-STM-001 S9, EPR-DEC-001 decision of 2026-10-25 under the standing instruction of 2026-10-23)
    "link_l": 245.0, "link_w": 70.0, "link_t": 28.0, "pin_d": 40.0, "bush_od": 46.0,
    "base_lug_t": 28.0,          # base pin lugs, 28 mm plate (were 20 mm): lug bearing and pin bending arm (S10)
    "theta_end": 6.0,            # link angle from vertical at full compaction (nominal fill)
    "theta_stop": 6.0,           # hard stop on the crank at theta_end; limits the force (EPR-CAL-001)
    # Lever and crank (item 6): bell crank at O, connecting link from crank pin C to the knee K
    "lever_x": -468.0, "lever_z": 266.0,
    "crank": 107.0, "conlink": 420.0, "conlink_t": 24.0, "conlink_w": 60.0,   # 60 wide for the 40.5 knee hole (was 50)
    "crank_pin_d": 30.0,
    "grip_r": 1650.0, "lever_len": 1700.0, "lever_od": 60.3, "lever_wall": 3.91,   # 2 in schedule 40
    "lever_offset": 144.0,       # lever angle minus crank angle (fixed by the hub)
    "tbar": 500.0,               # T-handle for a second operator
    # Eject lever (item 7): seesaw on the +X side; one central arm pushes on the push rod's foot (P9)
    "eject_x": 160.0, "eject_z": 607.5, "eject_arm": 160.0, "eject_lift": 160.0,
    # Frame (item 1)
    "skid": 60.0, "skid_len": 1000.0, "skid_y": 260.0, "cross": 50.0,
    "base_t": 12.0, "base_x0": -120.0, "base_x1": 195.0, "base_w": 340.0, "bracket_t": 10.0,
    "col_d": 80.0, "col_b": 45.0, "col_web": 6.0, "col_flange": 8.0,    # UPN 80, web toward the mold (P2)
    "beam_d": 100.0, "beam_t": 20.0,             # two 20 x 100 mm plates on the column flanges
    "tie": 40.0, "tie_y": 90.0,  # 40 x 40 x 3 tubes from the lever bracket to the base beam
    "guard_y": 115.0,            # linkage guard side panels
}

STEEL = 7850.0e-9   # kg/mm3
# mold to column bolts: four M16 per side in one line on the UPN 80 web centre (a 30 mm washer does not fit two
# lines inside the 48 mm flat of the web between its root radii; EPR-DEC-001, 2026-10-25)
MOLD_BOLT_DZ = (20.0, 57.0, 93.0, 130.0)
GUARD_FILL = 0.35   # expanded metal: share of a solid 2 mm sheet's mass


# ------------------------------------------------------------------ geometry helpers
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


def _yspan(x, z, d, y0, y1):
    """Cylinder along Y from y0 to y1."""
    return _ypin(x, z, d, abs(y1 - y0), (y0 + y1) / 2)


def _link(a, b, w, t, y, holes=()):
    """Flat bar with round ends (radius w/2) centred on XZ points a and b, thickness t at Y = y,
    with holes (diameter) at a and b."""
    s = _flat(a, b, w, t, y) + _ypin(a[0], a[1], w, t, y) + _ypin(b[0], b[1], w, t, y)
    for (pt, d) in holes:
        s = s - _ypin(pt[0], pt[1], d, t + 2, y)
    return s


def _yplate(pts, y0, y1):
    """Plate with an XZ outline (list of (x, z)) between y0 and y1."""
    from build123d import Plane, Polygon, extrude
    pl = Plane(origin=(0, min(y0, y1), 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    from build123d import Pos
    face = pl * Polygon(*[(x, z) for x, z in pts], align=None)
    sol = extrude(face, amount=-abs(y1 - y0))
    return Pos(0, min(y0, y1) - sol.bounding_box().min.Y, 0) * sol     # either winding


def _bolt(axis, at, d, length, head=True):
    """Simple hex-head bolt as a cylinder with a head, along +X, +Y or +Z from `at` (head at `at`)."""
    from build123d import Cylinder, Pos, Rot, RegularPolygon, extrude, Plane
    x, y, z = at
    af = {12: 18, 16: 24, 10: 16, 8: 13}.get(int(d), 1.5 * d)
    rot = {"x": Rot(0, 90, 0), "-x": Rot(0, -90, 0), "y": Rot(-90, 0, 0), "-y": Rot(90, 0, 0), "z": Rot(0, 0, 0), "-z": Rot(180, 0, 0)}[axis]
    from build123d import Align
    shank = Cylinder(d / 2, length, align=(Align.CENTER, Align.CENTER, Align.MIN))
    hd = extrude(RegularPolygon(af / 2 / math.cos(math.pi / 6), 6), amount=-0.65 * d)
    return Pos(x, y, z) * rot * (shank + hd if head else shank)


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


ASSEMBLY_THETA = 35.0   # deg: toggle folded past the start so the upper pin lines up with the column access hole


def derived(p=PARAMS):
    """Named positions used by the parts, the checks and the build plan pictures."""
    g = geometry(p)
    BL, BW, W = p["blk_l"], p["blk_w"], p["wall"]
    MT = p["mold_top"]; MB = MT - p["mold_h"]
    ox, oy = BL / 2 + W, BW / 2 + W
    zb_top = p["skid"] + p["base_t"]
    col_in = oy + p["flange_t"]                 # column web face against the mold flange
    col_out = col_in + p["col_b"]
    beam_z1 = g["z_b"] - 25.0
    beam_z0 = beam_z1 - p["beam_d"]
    r = p["rod"]
    _, zp0, _ = toggle_state(theta_start(p), p)
    _, zp_asm, _ = toggle_state(math.radians(ASSEMBLY_THETA), p)
    slot_top0 = zp0 + p["pin_d"] / 2
    rod_bot0 = slot_top0 - p["slot_len"] - p["rod_foot"]          # rod foot at the start of the stroke
    return dict(MT=MT, MB=MB, ox=ox, oy=oy, zb_top=zb_top, col_in=col_in, col_out=col_out,
                col_y=(col_in + col_out) / 2, beam_z0=beam_z0, beam_z1=beam_z1, z_b=g["z_b"],
                foot_z=zb_top + 16.0, rod_bot0=rod_bot0, zp0=zp0, zp_asm=zp_asm,
                y_upper=(r / 2 + 2, r / 2 + 2 + p["link_t"]),              # 32 to 60
                y_lower=(r / 2 + p["link_t"] + 6, r / 2 + 2 * p["link_t"] + 6),   # 64 to 92
                lug_y=(28.0, 28.0 + p["base_lug_t"]))


# ------------------------------------------------------------------ parts, one by one
class Comp:
    """One component: name, shape, colour, BOM line, piece (the assembly it is welded or fitted into)."""
    def __init__(self, name, shape, color, bom, piece, moving=False):
        self.name, self.shape, self.color, self.bom, self.piece, self.moving = name, shape, color, bom, piece, moving


def build_components(p=PARAMS, theta=None, eject=0.0):
    """Every component of the press and kit. theta: toggle angle (rad), default the start of the
    stroke. eject: push rod lift (mm) by the eject lever, 0 to eject_lift (with theta at the start)."""
    from build123d import Box, Cylinder, Pos, Rot
    b = _box
    th = theta_start(p) if theta is None else theta
    D = derived(p)
    g = geometry(p)
    BL, BW, W = p["blk_l"], p["blk_w"], p["wall"]
    MT, MB, ox, oy = D["MT"], D["MB"], D["ox"], D["oy"]
    sk, sy = p["skid"], p["skid_y"]
    zb_top = D["zb_top"]
    lx, lz = p["lever_x"], p["lever_z"]
    C = {}
    # end pawl pivot: on the line of the crank pin's kickback, 90 mm below the pin at the stop
    (cxe, cze), pse = knee_and_crank(math.radians(p["theta_end"]), p)
    kick = (math.sin(pse), -math.cos(pse))             # direction the crank pin moves if the lever kicks back
    PAWL_TIP = (cxe + (p["crank_pin_d"] / 2 + 13) * kick[0], cze + (p["crank_pin_d"] / 2 + 13) * kick[1])
    PAWL_PIV = (PAWL_TIP[0] + 90 * kick[0], PAWL_TIP[1] + 90 * kick[1])
    # rest catch: the same part mirrored onto the -Y plate, on the line the crank pin moves at the start
    (cxs, czs), pss = knee_and_crank(theta_start(p), p)
    fall = (-math.sin(pss), math.cos(pss))             # direction the crank pin moves when the lever falls into the stroke
    CATCH_TIP = (cxs + (p["crank_pin_d"] / 2 + 13) * fall[0], czs + (p["crank_pin_d"] / 2 + 13) * fall[1])
    CATCH_PIV = (CATCH_TIP[0] + 90 * fall[0], CATCH_TIP[1] + 90 * fall[1])
    # rest stop: a 30 mm bar under the crank arms at the start of the stroke
    ra = 70.0
    REST = (lx + ra * math.cos(pss) + 40.1 * math.sin(pss), lz + ra * math.sin(pss) - 40.1 * math.cos(pss))

    def add(key, name, shape, color, bom, piece, moving=False):
        C[key] = Comp(name, shape, color, bom, piece, moving)

    # ---------------- 1 Base frame (one welded piece)
    def tube_x(x0, x1, yc, z0, s, w=3.0):
        return b(x0, x1, yc - s / 2, yc + s / 2, z0, z0 + s) - b(x0 - 1, x1 + 1, yc - s / 2 + w, yc + s / 2 - w, z0 + w, z0 + s - w)

    def tube_y(xc, y0, y1, z0, s, w=3.0):
        return b(xc - s / 2, xc + s / 2, y0, y1, z0, z0 + s) - b(xc - s / 2 + w, xc + s / 2 - w, y0 - 1, y1 + 1, z0 + w, z0 + s - w)

    L2 = p["skid_len"] / 2
    cs = p["cross"]
    yi = sy - sk / 2                                   # inner face of the skids
    add("skids", "Skids (2)", tube_x(-L2, L2, -sy, 0, sk) + tube_x(-L2, L2, sy, 0, sk), "#4B5563", 1, "base")
    # cross tubes welded between the skids with their tops flush with the skid tops (P1)
    xs_cross = (-L2 + cs / 2, p["base_x0"] + cs / 2, p["base_x1"] - cs / 2, L2 - cs / 2)
    cross = None
    for xc in xs_cross:
        t_ = tube_y(xc, -yi, yi, sk - cs, cs)
        cross = t_ if cross is None else cross + t_
    add("cross", "Cross tubes (4)", cross, "#4B5563", 1, "base")
    bp = b(p["base_x0"], p["base_x1"], -p["base_w"] / 2, p["base_w"] / 2, sk, zb_top)
    for fx in (-55, 55):                               # M12 holes for the core feet
        for fy in (D["col_y"] - 35, D["col_y"] + 35):
            for s in (-1, 1):
                bp = bp - Pos(fx, s * fy, sk + 6) * Cylinder(6.75, 14)
    for s in (-1, 1):                                  # guard feet: holes tapped M10 (a nut would land in the cross tube below)
        bp = bp - Pos(-94, s * (p["guard_y"] - 12), sk + 6) * Cylinder(5.0, 14)
    add("base_plate", "Base plate", bp, "#6B7280", 1, "base")
    # lever bracket: two shaped 10 mm plates standing on the -X cross tube
    bt_ = p["bracket_t"]
    outline = [(-500, sk), (-440, sk), (-318, 150), (-294, 200), (-291, 300), (-330, 322), (-420, 328), (-470, 332),
               (-515, 312), (-521, 250), (-512, 200)]
    brk = None
    for s in (-1, 1):
        y0_, y1_ = s * 60, s * (60 + bt_)
        pl = _yplate(outline, y0_, y1_) - _yspan(lx, lz, 40.5, y0_ - s, y1_ + s)
        pv_ = PAWL_PIV if s > 0 else CATCH_PIV
        pl = pl - _yspan(pv_[0], pv_[1], 16.5, y0_ - s, y1_ + s)
        if s > 0:                                      # access hole for fitting the crank pin at rest
            pl = pl - _yspan(cxs, czs, 31, y0_ - s, y1_ + s)
        brk = pl if brk is None else brk + pl
    add("bracket", "Lever bracket plates (2)", brk, "#374151", 1, "base")
    # rest stop: 30 mm round bar across the bracket, touching the socket's +X face at the start
    add("rest", "Rest stop bar with rubber sleeve", _yspan(REST[0], REST[1], 30, -60, 60), "#111827", 1, "base")
    # ties from the bracket to the base beam: tubes slotted over the bracket plates, bolted tabs at the beam
    t = p["tie"]; ty = p["tie_y"]
    beam_x0 = -p["col_d"] / 2 - p["beam_t"]            # outer face of the -X beam plate (-60)
    tie_z0, tie_z1 = lz - 20, g["z_b"] - 60
    ties = None
    for s in (-1, 1):
        tb = _pipe((lx + 40, s * ty, tie_z0), (beam_x0 - 10, s * ty, tie_z1), t / 2, t / 2 - 3)
        tab = b(beam_x0 - 10, beam_x0, s * 60, s * 148, tie_z1 - 55, tie_z1 + 25)
        for zz in (tie_z1 - 37, tie_z1 + 8):
            tab = tab - _box(beam_x0 - 11, beam_x0 + 1, s * 130 - 6.75, s * 130 + 6.75, zz - 6.75, zz + 6.75)
        ties = tb + tab if ties is None else ties + tb + tab
    add("ties", "Tie tubes with bolted end tabs (2)", ties, "#4B5563", 1, "base")
    # eject seesaw posts, welded to the base plate
    ex, ez = p["eject_x"], p["eject_z"]
    posts = None
    for s in (-1, 1):
        po = _yplate([(ex - 30, zb_top), (ex + 30, zb_top), (ex + 30, ez), (ex, ez + 30), (ex - 30, ez)], s * 60, s * 70)
        po = po - _yspan(ex, ez, 31, s * 59, s * 71)
        posts = po if posts is None else posts + po
    add("posts", "Eject posts (2)", posts, "#4B5563", 1, "base")

    # ---------------- 2 Press core (one welded piece)
    cd, cf, cw = p["col_d"], p["col_flange"], p["col_web"]
    ci, co = D["col_in"], D["col_out"]
    zc0, zc1 = D["foot_z"], MT - 10
    cols = None
    for s in (-1, 1):
        web = b(-cd / 2, cd / 2, s * ci, s * (ci + cw), zc0, zc1)
        fl = b(-cd / 2, -cd / 2 + cf, s * ci, s * co, zc0, zc1) + b(cd / 2 - cf, cd / 2, s * ci, s * co, zc0, zc1)
        c = web + fl
        for zz in [MB + dz_ for dz_ in MOLD_BOLT_DZ]:                 # clearance holes for the M16 mold bolts
            for xx in (0.0,):
                c = c - _box(xx - 9, xx + 9, s * ci - s, s * (ci + cw) + s, zz - 9, zz + 9)
        if s > 0:                                      # access holes for the base pin and the upper pin
            for zz in (g["z_b"], D["zp_asm"]):
                c = c - _yspan(0, zz, p["pin_d"] + 6, ci - 1, ci + cw + 1)   # 46 for the 40 mm pins
        for zz in (D["beam_z1"] - 72, D["beam_z1"] - 27):   # tie tab bolts through the -X flange
            c = c - _box(-cd / 2 - 1, -cd / 2 + cf + 1, s * 130 - 6.75, s * 130 + 6.75, zz - 6.75, zz + 6.75)
        cols = c if cols is None else cols + c
    add("columns", "Columns, UPN 80 (2)", cols, "#6B7280", 2, "core")
    feet = None
    for s in (-1, 1):
        f = b(-70, 70, s * (D["col_y"] - 45), s * (D["col_y"] + 45), zb_top, zc0)
        for fx in (-55, 55):
            for fy in (D["col_y"] - 35, D["col_y"] + 35):
                f = f - Pos(fx, s * fy, zb_top + 8) * Cylinder(6.75, 18)
        feet = f if feet is None else feet + f
    add("feet", "Column feet (2)", feet, "#6B7280", 2, "core")
    bz0, bz1 = D["beam_z0"], D["beam_z1"]
    beam = None
    for s in (-1, 1):
        x0_, x1_ = s * cd / 2, s * (cd / 2 + p["beam_t"])
        pl = b(x0_, x1_, -co, co, bz0, bz1)
        if s < 0:
            for sy_ in (-1, 1):
                for zz in (bz1 - 72, bz1 - 27):
                    pl = pl - _box(x1_ - 1, x0_ + 1, sy_ * 130 - 6.75, sy_ * 130 + 6.75, zz - 6.75, zz + 6.75)
        beam = pl if beam is None else beam + pl
    add("beam", "Base beam plates and bottom plate", beam, "#6B7280", 2, "core")
    lugs = None
    for s in (-1, 1):
        lg = b(-cd / 2, cd / 2, s * D["lug_y"][0], s * D["lug_y"][1], bz1 - 30, g["z_b"] + 40)
        lg = lg - _yspan(0, g["z_b"], p["bush_od"], s * (D["lug_y"][0] - 1), s * (D["lug_y"][1] + 1))
        lugs = lg if lugs is None else lugs + lg
    add("lugs", "Base pin lugs (2)", lugs, "#6B7280", 2, "core")

    # ---------------- 3 Mold box (one welded piece)
    mold = b(-ox, ox, -oy, oy, MB, MT) - b(-BL / 2, BL / 2, -BW / 2, BW / 2, MB - 1, MT + 1)
    bt, bh = p["belt_t"], p["belt_h"]
    belt = b(-ox - bt, ox + bt, -oy - bt, oy + bt, MT - bh, MT) - b(-ox, ox, -oy, oy, MT - bh - 1, MT + 1)
    fl = p["flange_t"]
    flanges = None
    for s in (-1, 1):
        f = b(-cd / 2 - 20, cd / 2 + 20, s * oy, s * (oy + fl), MB, MT - bh)
        for zz in [MB + dz_ for dz_ in MOLD_BOLT_DZ]:
            for xx in (0.0,):
                f = f - _yspan(xx, zz, 16.0, s * (oy - 1), s * (oy + fl + 1))   # tapped M16 (drawn at the nominal size)
        flanges = f if flanges is None else flanges + f
    add("mold", "Mold walls and belt", mold + belt, "#0F766E", 3, "mold")
    add("flanges", "Mold side flanges (tapped M16)", flanges, "#0F766E", 3, "mold")
    lt = p["lug_t"]; ly0 = p["lug_y0"]
    hx, hz, lxx, lzz = p["hinge_x"], p["hinge_z"], p["latch_x"], p["latch_z"]
    mlugs = None
    for s in (-1, 1):
        y0_, y1_ = s * ly0, s * (ly0 + lt)
        hl = _yplate([(ox + bt, MT - bh), (hx + 15, MT - bh), (hx + 35, hz), (hx + 35, hz + 10), (hx, hz + 35), (hx - 28, hz + 12), (hx - 28, MT - 1), (ox + bt, MT - 1)], y0_, y1_)
        hl = hl - _yspan(hx, hz, p["hinge_pin_d"] + 1, y0_ - s, y1_ + s)
        ll = _yplate([(-ox - bt, MT - bh - 20), (lxx - 15, MT - bh - 20), (lxx - 35, lzz), (lxx - 30, lzz + 25), (-ox - bt, MT - 5)], y0_, y1_)
        ll = ll - _yspan(lxx, lzz, p["latch_pin_d"] + 1, y0_ - s, y1_ + s)
        mlugs = hl + ll if mlugs is None else mlugs + hl + ll
    add("mold_lugs", "Hinge and latch lugs on the mold (4)", mlugs, "#0F766E", 3, "mold")

    # ---------------- 4 Lid (one welded piece) and its pins
    lid_t, ll_, lw = p["lid_t"], p["lid_l"], p["lid_w"]
    lid = b(-ll_ / 2, ll_ / 2, -lw / 2, lw / 2, MT, MT + lid_t)
    ribs = None
    ry0 = p["rib_y"] - p["rib_t"] / 2
    for s in (-1, 1):
        y0_, y1_ = s * ry0, s * (ry0 + p["rib_t"])
        top = MT + lid_t + p["rib_h"]
        e0, e1 = -ll_ / 2, ll_ / 2
        rib = _yplate([(lxx - 35, lzz - 30), (e0, lzz - 30), (e0, MT + lid_t), (e1, MT + lid_t), (e1, hz - 32),
                       (hx + 20, hz - 32), (hx + 33, hz - 15), (hx + 33, hz + 30), (hx - 5, top), (lxx + 5, top),
                       (lxx - 35, lzz + 30)], y0_, y1_)
        rib = rib - _yspan(hx, hz, p["hinge_pin_d"] + 1, y0_ - s, y1_ + s) - _yspan(lxx, lzz, p["latch_pin_d"] + 1, y0_ - s, y1_ + s)
        ribs = rib if ribs is None else ribs + rib
    add("lid", "Lid plate and ribs with hinge and latch ears", lid + ribs, "#115E59", 4, "lid")
    pin_l = ly0 + lt + 6
    add("hinge_pin", "Hinge pin, 30 mm", _yspan(hx, hz, p["hinge_pin_d"], -pin_l, pin_l), "#9CA3AF", 4, "lid")
    add("latch_pin", "Latch pin, 30 mm, with T-handle", _yspan(lxx, lzz, p["latch_pin_d"], -pin_l, pin_l)
        + _yspan(lxx, lzz, 16, pin_l, pin_l + 25) + _box(lxx - 8, lxx + 8, pin_l + 17, pin_l + 25, lzz - 45, lzz + 45), "#9CA3AF", 4, "lid")

    # ---------------- 5 Piston, skirts and push rod (one welded piece)
    knee, z_p, z_face = toggle_state(th, p)
    lift = eject
    zf = z_face + lift
    cl = p["piston_clear"]
    plate = b(-BL / 2 + cl, BL / 2 - cl, -BW / 2 + cl, BW / 2 - cl, zf - p["piston_t"], zf)
    sk_ = p["skirt_t"]
    for s in (-1, 1):
        plate = plate + b(s * (BL / 2 - cl), s * (BL / 2 - cl - sk_), -BW / 2 + cl, BW / 2 - cl, zf - p["piston_t"] - p["skirt_h"], zf - p["piston_t"])
    r = p["rod"]
    slot_top = z_p + p["pin_d"] / 2 + lift
    rod_bot = slot_top - p["slot_len"] - p["rod_foot"]
    rod = b(-r / 2, r / 2, -r / 2, r / 2, rod_bot, zf - p["piston_t"])
    rod = rod - b(-p["pin_d"] / 2 - 1, p["pin_d"] / 2 + 1, -r / 2 - 1, r / 2 + 1, slot_top - p["slot_len"], slot_top)
    add("piston", "Piston plate, end skirts and slotted push rod", plate + rod, "#D4A017", 5, "piston", True)

    # ---------------- 6 Toggle: links, pins, spacers, connecting link
    zb = g["z_b"]
    kx, kz = knee
    lw_, lt_, pd = p["link_w"], p["link_t"], p["pin_d"]
    yu, ylw = D["y_upper"], D["y_lower"]
    bo = p["bush_od"]
    up = lo = None
    for s in (-1, 1):
        u = _link((0, z_p), (kx, kz), lw_, lt_, s * (yu[0] + yu[1]) / 2, holes=(((0, z_p), bo), ((kx, kz), bo)))
        l_ = _link((0, zb), (kx, kz), lw_, lt_, s * (ylw[0] + ylw[1]) / 2, holes=(((0, zb), bo), ((kx, kz), bo)))
        up = u if up is None else up + u
        lo = l_ if lo is None else lo + l_
    add("lower_links", "Lower toggle links (2)", lo, "#C2410C", 6, "toggle", True)
    add("upper_links", "Upper toggle links (2)", up, "#EA580C", 6, "toggle", True)
    pin_long = ylw[1] + 4            # ends 2 mm past the dust seal, room for the circlip
    add("base_pin", "Base pin, 35 mm", _yspan(0, zb, pd, -pin_long, pin_long), "#9CA3AF", 6, "toggle")
    add("knee_pin", "Knee pin, 35 mm", _yspan(kx, kz, pd, -pin_long, pin_long), "#9CA3AF", 6, "toggle", True)
    add("upper_pin", "Upper pin, 35 mm", _yspan(0, z_p, pd, -(yu[1] + 4), yu[1] + 4), "#9CA3AF", 6, "toggle", True)
    sp_base = None
    for s in (-1, 1):
        sp = _yspan(0, zb, 50, s * D["lug_y"][1], s * ylw[0]) - _yspan(0, zb, pd + 0.5, s * (D["lug_y"][1] - 1), s * (ylw[0] + 1))
        sp_base = sp if sp_base is None else sp_base + sp
    add("base_spacers", "Base pin spacers (2)", sp_base, "#4B5563", 6, "toggle")
    ct, cwid = p["conlink_t"], p["conlink_w"]
    sp_knee = None
    for s in (-1, 1):
        sp = _yspan(kx, kz, 50, s * ct / 2, s * yu[0]) - _yspan(kx, kz, pd + 0.5, s * (ct / 2 - 1), s * (yu[0] + 1))
        sp_knee = sp if sp_knee is None else sp_knee + sp
    add("knee_spacers", "Knee pin spacers (2)", sp_knee, "#4B5563", 6, "toggle", True)
    # dust seals (BOM line 5, decision of 2026-10-02): a 2 mm felt or rubber washer on each pin against the
    # outer face of a link, round the bush, so grit does not reach the bush faces. Base pin and knee pin: on the
    # lower links' outer faces; knee pin: also on the upper links' outer faces (in the 4 mm gap); upper pin: on
    # the upper links' outer faces.
    st_, so_, si_ = p["seal_t"], p["seal_od"], p["seal_id"]

    def ring(x, z, y0, y1):
        y0, y1 = min(y0, y1), max(y0, y1)
        return _yspan(x, z, so_, y0, y1) - _yspan(x, z, si_, y0 - 1, y1 + 1)
    sb, sk, su = [], [], []
    for s in (-1, 1):
        sb.append(ring(0, zb, s * ylw[1], s * (ylw[1] + st_)))
        sk += [ring(kx, kz, s * ylw[1], s * (ylw[1] + st_)), ring(kx, kz, s * yu[1], s * (yu[1] + st_))]
        su.append(ring(0, z_p, s * yu[1], s * (yu[1] + st_)))
    from build123d import Compound as _Cmp
    sb, sk, su = _Cmp(children=sb), _Cmp(children=sk), _Cmp(children=su)
    add("seals_base", "Dust seals, base pin (2)", sb, "#F59E0B", 5, "toggle")
    add("seals_knee", "Dust seals, knee pin (4)", sk, "#F59E0B", 5, "toggle", True)
    add("seals_upper", "Dust seals, upper pin (2)", su, "#F59E0B", 5, "toggle", True)
    (cx, cz), psi = knee_and_crank(th, p)
    add("conlink", "Connecting link", _link((cx, cz), (kx, kz), cwid, ct, 0, holes=(((cx, cz), p["crank_pin_d"] + 0.5), ((kx, kz), pd + 0.5))),
        "#B45309", 6, "toggle", True)

    # ---------------- 7 Lever hub, crank, socket; shaft; crank pin; lever pipe and T-handle
    hub = _ypin(lx, lz, 80, 100) - _ypin(lx, lz, 40.5, 102)
    crank = None
    for s in (-1, 1):
        cp = _link((lx, lz), (cx, cz), 50, 20, s * 26, holes=(((cx, cz), p["crank_pin_d"] + 0.5),)) - _ypin(lx, lz, 40.5, 22, s * 26)
        crank = cp if crank is None else crank + cp
    phi = math.radians(math.degrees(psi) + p["lever_offset"])
    ux, uz = math.cos(phi), math.sin(phi)
    ro = p["lever_od"] / 2
    sock = _pipe((lx + 30 * ux, 0, lz + 30 * uz), (lx + 250 * ux, 0, lz + 250 * uz), ro + 6, ro + 0.5) - _ypin(lx, lz, 80, 102)
    sock = sock - _rod((lx + 225 * ux - 50 * uz, 0, lz + 225 * uz + 50 * ux), (lx + 225 * ux + 50 * uz, 0, lz + 225 * uz - 50 * ux), 6.5)
    add("hub", "Lever hub with crank plates and socket", hub + crank + sock, "#1F2937", 6, "hub", True)
    add("shaft", "Hub shaft, 40 mm", _yspan(lx, lz, 40, -77, 77), "#9CA3AF", 6, "hub")
    add("crank_pin", "Crank pin, 30 mm", _yspan(cx, cz, p["crank_pin_d"], -56, 56), "#9CA3AF", 6, "hub", True)
    tip = (lx + p["lever_len"] * ux, 0, lz + p["lever_len"] * uz)
    lever = _pipe((lx + 46 * ux, 0, lz + 46 * uz), tip, ro, ro - p["lever_wall"])
    lever = lever - _rod((lx + 225 * ux - 50 * uz, 0, lz + 225 * uz + 50 * ux), (lx + 225 * ux + 50 * uz, 0, lz + 225 * uz - 50 * ux), 6.5)
    grip = (lx + p["grip_r"] * ux, 0, lz + p["grip_r"] * uz)
    tbar = _pipe((grip[0], -p["tbar"] / 2, grip[2]), (grip[0], p["tbar"] / 2, grip[2]), 16.7, 13.0)
    lever = lever - _yspan(grip[0], grip[2], 33.4, -ro - 1, ro + 1)
    add("lever", "Lever pipe and T-handle (removable)", lever + tbar, "#111827", 6, "lever", True)
    add("lever_pin", "Lever locking pin, 12 mm", _rod((lx + 225 * ux - 45 * uz, 0, lz + 225 * uz + 45 * ux), (lx + 225 * ux + 45 * uz, 0, lz + 225 * uz - 45 * ux), 6), "#9CA3AF", 6, "lever", True)

    # ---------------- 8 Eject seesaw: hub, central arm with a round nose, socket; pivot pin
    # The arm is cut from 20 mm plate as a cranked profile (hub, elbow, nose) so that it stays below the
    # push rod everywhere except the round nose, which bears on the rod's foot. Pivot 160 mm from the nose.
    rb0 = D["rod_bot0"]
    hub_c = (ex, ez)
    nose_r = 15.0
    ang0 = math.radians(210.0)                       # contact point at rest: 30 deg below the hub's level
    R_ = p["eject_arm"]
    contact0 = (ex + R_ * math.cos(ang0), ez + R_ * math.sin(ang0))   # (21.4, 527.5): on the rod foot
    N0 = (contact0[0], contact0[1] - nose_r)
    E0 = (45.0, 470.0)
    Rn = math.hypot(N0[0] - ex, N0[1] - ez)
    an0 = math.atan2(N0[1] - ez, N0[0] - ex) % (2 * math.pi)
    da = 0.0
    if eject > 0:
        an1 = math.pi - math.asin((N0[1] + eject - ez) / Rn)
        da = an1 - an0                               # negative: clockwise seen from -Y
    rot = lambda q: (ex + (q[0] - ex) * math.cos(da) - (q[1] - ez) * math.sin(da),   # noqa: E731
                     ez + (q[0] - ex) * math.sin(da) + (q[1] - ez) * math.cos(da))
    N, E = rot(N0), rot(E0)
    arm = _link(hub_c, E, 40, 20, 0) + _link(E, N, 2 * nose_r, 20, 0)
    arm = arm - _ypin(ex, ez, 31, 22)
    ehub = _ypin(ex, ez, 60, 110) - _ypin(ex, ez, 31, 112)
    sa = math.atan2(N[1] - ez, N[0] - ex) + math.pi + math.radians(30)
    esock = _pipe((ex + 32 * math.cos(sa), 0, ez + 32 * math.sin(sa)), (ex + 260 * math.cos(sa), 0, ez + 260 * math.sin(sa)), ro + 6, ro + 0.5)
    add("eject", "Eject seesaw: hub, arm and socket", ehub + arm + esock, "#7C3AED", 7, "eject", True)
    add("eject_pin", "Eject pivot pin, 30 mm", _yspan(ex, ez, 30, -76, 76), "#9CA3AF", 7, "eject")

    # ---------------- 9 End pawl: a 12 mm plate inside the +Y bracket plate, welded to a 16 mm pivot
    # shaft that turns in the bracket plate, with a release handle outside the plate. A spring keeps it
    # against the crank pin; it drops in under the pin at the stop and takes the kickback in compression.
    def latch(pv, tipp, s, rise):
        part_ = _link(pv, tipp, 24, 12, s * 50) + _yspan(pv[0], pv[1], 16, s * 44, s * 84)
        hdl_end = (-430.0, pv[1] + rise)
        return part_ + _link(pv, hdl_end, 20, 10, s * 77) + _yspan(hdl_end[0], hdl_end[1], 20, s * 72, s * 110)
    add("pawl", "End pawl, pivot shaft and release handle", latch(PAWL_PIV, PAWL_TIP, 1, 25), "#7C3AED", 7, "pawl")
    add("catch", "Rest catch, pivot shaft and release handle", latch(CATCH_PIV, CATCH_TIP, -1, 55), "#7C3AED", 7, "pawl")

    # ---------------- 10 Linkage guard (BOM 13): angle frame and expanded metal, top and both sides
    gy = p["guard_y"]
    gx0, gx1, gz0, gz1 = -400.0, -84.0, zb_top, 640.0
    gtop_x0 = -370.0
    guard = None
    for s in (-1, 1):
        side = b(gx0, gx1, s * gy, s * (gy + 2), gz0 + 20, gz1)
        frame = (b(gx0, gx1, s * (gy + 2), s * (gy + 22), gz1 - 20, gz1) + b(gx0, gx0 + 20, s * (gy + 2), s * (gy + 22), gz0 + 20, gz1)
                 + b(gx1 - 20, gx1, s * (gy + 2), s * (gy + 22), gz0 + 3, gz1) + b(-118, gx1, s * (gy - 25), s * (gy + 22), gz0, gz0 + 3))
        frame = frame - Pos(-94, s * (gy - 12), gz0 + 1.5) * Cylinder(5.5, 5)     # foot bolt clear of the vertical member
        guard = side + frame if guard is None else guard + side + frame
    guard = guard + b(gtop_x0, -160, -gy, gy, gz1 - 2, gz1)
    # spacer brackets to the bracket plates (two M10 each side)
    for s in (-1, 1):
        guard = guard + b(-400, -380, s * 70, s * gy, 120, 145) + b(-400, -380, s * 70, s * gy, 270, 295)
    add("guard", "Linkage guard", guard, "#9CA3AF", 13, "guard")

    # ---------------- bolts (BOM 11)
    bolts = None
    for s in (-1, 1):
        for zz in [MB + dz_ for dz_ in MOLD_BOLT_DZ]:
            for xx in (0.0,):
                bo_ = _bolt("-y" if s > 0 else "y", (xx, s * (ci + cw), zz), 16, 6 + 16 - 2)
                bolts = bo_ if bolts is None else bolts + bo_
        for fx in (-55, 55):
            for fy in (D["col_y"] - 35, D["col_y"] + 35):
                bolts = bolts + _bolt("-z", (fx, s * fy, zc0), 12, 16 + 12 + 6)
        for zz in (bz1 - 72, bz1 - 27):
            bolts = bolts + _bolt("x", (beam_x0 - 10, s * 130, zz), 12, 10 + 20 + 8 + 8)
    add("bolts", "Bolts: 8 x M16 mold, 8 x M12 feet, 4 x M12 ties", bolts, "#111827", 11, "hardware")

    # ---------------- context and kit
    SX, SY = 1150.0, 750.0
    sieve = Pos(SX, SY, 420) * Rot(0, -25, 0) * (Box(45, 700, 900) - Box(47, 610, 810))
    sieve = sieve + Pos(SX, SY, 420) * Rot(0, -25, 0) * Box(4, 610, 810)
    sieve = sieve + _rod((SX + 130, SY - 300, 0), (SX + 20, SY - 300, 660), 12) + _rod((SX + 130, SY + 300, 0), (SX + 20, SY + 300, 660), 12)
    add("sieve", "Soil sieve, 5 mm mesh", sieve, "#A16207", 8, "kit")
    kit = (Pos(450, -700, 125) * Box(400, 300, 250)
           + Pos(370, -740, 340) * Cylinder(45, 180) + Pos(490, -740, 340) * Cylinder(45, 180)
           + Pos(450, -620, 270) * Box(300, 50, 40))
    add("kit", "Soil test kit", kit, "#2563EB", 9, "kit")
    BX, BY = 1000.0, -300.0
    GZ = 4 * p["blk_h"]
    # length and height gauge: a 12 mm bar, 40 mm deep, with legs 292 mm apart inside (longest good block)
    # and a 93 mm notch in its top edge (tallest good block)
    gauge = (Pos(BX, BY, GZ + 20) * Box(340, 12, 40) + Pos(BX - 152, BY, GZ - 20) * Box(12, 12, 40)
             + Pos(BX + 152, BY, GZ - 20) * Box(12, 12, 40)) - Pos(BX, BY, GZ + 30) * Box(93, 14, 20.01)
    add("gauge", "Block gauge", gauge, "#16A34A", 10, "kit")
    fill = b(-BL / 2 + 2, BL / 2 - 2, -BW / 2 + 2, BW / 2 - 2, zf, MT - 2)
    add("fill", "Loose soil fill (context)", fill, "#B7794A", None, "context")
    blocks = None
    for c_ in range(4):
        for i in range(2):
            for j in range(4):
                bb_ = Pos(BX + (i - 0.5) * 300, BY + (j - 1.5) * 150, p["blk_h"] * (c_ + 0.5)) * Box(BL - 6, BW - 6, p["blk_h"] - 2)
                blocks = bb_ if blocks is None else blocks + bb_
    add("blocks", "Pressed blocks (context)", blocks, "#C08A5B", None, "context")
    return C


# BOM groups for the concept media, the exploded view and the calculation note (numbers = BOM lines)
GROUPS = [
    ("Frame: base on skids and press core", 1, "#4B5563", (0, 0, -300),
     ("skids", "cross", "base_plate", "bracket", "rest", "ties", "posts", "columns", "feet", "beam", "lugs")),
    ("Mold box, 290 x 140 mm cavity", 2, "#0F766E", (0, 0, 420), ("mold", "flanges", "mold_lugs")),
    ("Lid with ribs, hinge and latch", 3, "#115E59", (0, 0, 780), ("lid", "hinge_pin", "latch_pin")),
    ("Piston and slotted push rod", 4, "#D4A017", (620, 0, 650), ("piston",)),
    ("Toggle links, pins and bushes", 5, "#C2410C", (380, 0, -60),
     ("lower_links", "upper_links", "base_pin", "knee_pin", "upper_pin", "base_spacers", "knee_spacers", "conlink",
      "seals_base", "seals_knee", "seals_upper")),
    ("Lever, crank hub and T-handle", 6, "#1F2937", (0, -500, -700), ("hub", "shaft", "crank_pin", "lever", "lever_pin")),
    ("Eject lever, rest catch and end pawl", 7, "#7C3AED", (350, 450, -150), ("eject", "eject_pin", "pawl", "catch")),
    ("Soil sieve, 5 mm mesh", 8, "#A16207", (400, 600, 0), ("sieve",)),
    ("Soil test kit", 9, "#2563EB", (-300, -700, 0), ("kit",)),
    ("Block gauge", 10, "#16A34A", (300, -300, 450), ("gauge",)),
    ("Loose soil fill (context)", None, "#B7794A", (0, 0, 1200), ("fill",)),
    ("Pressed blocks (context)", None, "#C08A5B", (300, -300, 0), ("blocks",)),
]
CONTEXT = ("Soil sieve, 5 mm mesh", "Soil test kit", "Block gauge", "Loose soil fill (context)", "Pressed blocks (context)")
# pieces as they are lifted and moved (R7): (name, component keys)
PIECES = [
    ("Base frame with lever bracket, ties and eject posts", ("skids", "cross", "base_plate", "bracket", "rest", "ties", "posts")),
    ("Press core, columns and base beam", ("columns", "feet", "beam", "lugs")),
    ("Mold box with hinge and latch lugs", ("mold", "flanges", "mold_lugs")),
    ("Lid with ribs, hinge and latch pins", ("lid", "hinge_pin", "latch_pin")),
    ("Piston and slotted push rod", ("piston",)),
    ("Toggle links, pins and spacers", ("lower_links", "upper_links", "base_pin", "knee_pin", "upper_pin", "base_spacers", "knee_spacers", "conlink")),
    ("Lever hub, crank, shaft and crank pin", ("hub", "shaft", "crank_pin")),
    ("Lever pipe and T-handle", ("lever", "lever_pin")),
    ("Eject seesaw, pivot pin, end pawl and rest catch", ("eject", "eject_pin", "pawl", "catch")),
    ("Linkage guard", ("guard",)),
    ("Bolts", ("bolts",)),
]


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def build_parts(p=PARAMS, theta=None):
    """Return a list of (name, shape, colour, bom_item, explode_offset), one per BOM group, for the
    concept media. The linkage guard and the bolts are left out of the media so the linkage shows."""
    C = build_components(p, theta)
    return [(n, _fuse([C[k].shape for k in keys]), col, bom, ex) for n, bom, col, ex, keys in GROUPS]


def assemblies(parts=None, comps=None):
    """Named compounds for export and the GA drawing: the press (every part of option A except the soil kit and the
    context, with guard, bushes, fasteners and weld beads) and the full set (with the kit)."""
    import copy
    from build123d import Compound
    ps = parts or components("A")
    press = [copy.copy(q["shape"]) for q in ps if q["kind"] != "context" and q["group"] != "kit"]
    full = [copy.copy(q["shape"]) for q in ps if q["kind"] != "context"]
    return {"earthpress-assembly": Compound(children=press), "earthpress-set": Compound(children=full)}


def ga_assembly():
    """The press for line drawings (GA EPR-DWG-001, concept blueprint): the constructable Comp model above, the same
    dimensions as components("A") but without edge breaks, bushes, nuts, washers and weld beads, so hidden-line
    projection finishes on a small machine (the detailed assembly of 251 parts did not, 2026-10-25)."""
    import copy
    from build123d import Compound
    C = build_components()
    kit = ("sieve", "kit", "gauge", "fill", "blocks")
    return Compound(children=[copy.copy(c.shape) for k, c in C.items() if k not in kit])


def piece_masses_v1(parts=None, comps=None):
    """Kit 1.7 masses from the Comp model (kept for comparison). Mass (kg) of each piece of the press as it is lifted (R7), from the model at 7,850 kg/m3.
    The guard's expanded metal counts at GUARD_FILL of a solid 2 mm sheet."""
    C = comps or build_components()
    out = {}
    for name, keys in PIECES:
        m = 0.0
        for k in keys:
            m += C[k].shape.volume * STEEL * (GUARD_FILL if k == "guard" else 1.0)
        out[name] = m
    return out


# ------------------------------------------------------------------ constructability checks
def check(verbose=True):
    """Build123d checks: parts that must not touch are apart (at several poses through the stroke and
    the eject), and parts that must touch do touch. Returns (n_pass, n_fail, lines)."""
    import itertools
    lines = []
    npass = nfail = 0

    def rec(ok, msg):
        nonlocal npass, nfail
        if ok:
            npass += 1
        else:
            nfail += 1
        lines.append(("PASS " if ok else "FAIL ") + msg)

    def inter(a, b_):
        A, B = a.bounding_box(), b_.bounding_box()
        if (A.min.X > B.max.X or B.min.X > A.max.X or A.min.Y > B.max.Y or B.min.Y > A.max.Y
                or A.min.Z > B.max.Z or B.min.Z > A.max.Z):
            return 0.0
        try:
            v = (a & b_).volume
        except Exception:
            v = 0.0
        return v

    def gap(a, b_):
        A, B = a.bounding_box(), b_.bounding_box()
        if (A.min.X > B.max.X + 3 or B.min.X > A.max.X + 3 or A.min.Y > B.max.Y + 3 or B.min.Y > A.max.Y + 3
                or A.min.Z > B.max.Z + 3 or B.min.Z > A.max.Z + 3):
            return 99.0
        try:
            return a.distance_to(b_)
        except Exception:
            return float("nan")

    th0 = theta_start()
    the = math.radians(PARAMS["theta_end"])
    poses = [("start", th0, 0.0), ("assembly fold 35 deg", math.radians(ASSEMBLY_THETA), 0.0),
             ("one third", th0 + (the - th0) / 3, 0.0), ("two thirds", th0 + 2 * (the - th0) / 3, 0.0),
             ("end of stroke", the, 0.0), ("eject half", th0, 80.0), ("eject full", th0, PARAMS["eject_lift"])]
    kit = {"sieve", "kit", "gauge", "fill", "blocks"}
    # pairs that are joined on purpose (welded, bolted or pinned); every other pair must not overlap
    joined = {frozenset(x) for x in [
        ("skids", "cross"), ("cross", "base_plate"), ("cross", "bracket"), ("base_plate", "posts"),
        ("bracket", "rest"), ("bracket", "pawl"), ("bracket", "catch"), ("bracket", "ties"), ("bracket", "shaft"),
        ("columns", "feet"), ("columns", "beam"), ("beam", "lugs"), ("mold", "flanges"), ("mold", "mold_lugs"),
        ("lid", "hinge_pin"), ("lid", "latch_pin"), ("mold_lugs", "hinge_pin"), ("mold_lugs", "latch_pin"),
        ("lugs", "base_pin"), ("lower_links", "base_pin"), ("base_spacers", "base_pin"), ("lower_links", "knee_pin"),
        ("upper_links", "knee_pin"), ("knee_spacers", "knee_pin"), ("conlink", "knee_pin"), ("upper_links", "upper_pin"),
        ("piston", "upper_pin"), ("hub", "shaft"), ("hub", "crank_pin"), ("conlink", "crank_pin"), ("hub", "lever"),
        ("hub", "lever_pin"), ("lever", "lever_pin"), ("eject", "eject_pin"), ("posts", "eject_pin"),
        ("seals_base", "base_pin"), ("seals_base", "lower_links"), ("seals_knee", "knee_pin"), ("seals_knee", "lower_links"),
        ("seals_knee", "upper_links"), ("seals_upper", "upper_pin"), ("seals_upper", "upper_links"),
        ("bolts", "columns"), ("bolts", "flanges"), ("bolts", "feet"), ("bolts", "base_plate"), ("bolts", "beam"), ("bolts", "ties"),
    ]}
    # designed sliding fits and bearing contacts: (pair, least clearance allowed in mm)
    fits = {frozenset(("piston", "mold")): 0.9, frozenset(("piston", "upper_links")): 1.9,
            frozenset(("knee_pin", "columns")): 1.9, frozenset(("base_pin", "columns")): 1.9,
            frozenset(("lower_links", "base_spacers")): 0.0, frozenset(("knee_spacers", "upper_links")): 0.0,
            frozenset(("conlink", "knee_spacers")): 0.0, frozenset(("hub", "rest")): 0.0,
            frozenset(("eject", "piston")): 0.0, frozenset(("crank_pin", "pawl")): 0.5, frozenset(("crank_pin", "catch")): 0.5,
            frozenset(("lower_links", "upper_links")): 1.9, frozenset(("seals_knee", "lower_links")): 1.9,
            frozenset(("seals_base", "columns")): 3.9, frozenset(("seals_knee", "columns")): 3.9,
            frozenset(("seals_base", "base_spacers")): 0.0, frozenset(("seals_upper", "piston")): 0.0, frozenset(("upper_pin", "upper_links")): 0.0}
    for pname, th, ej in poses:
        C = build_components(theta=th, eject=ej)
        skip = set(kit)
        if ej > 0:
            skip |= {"lid", "latch_pin", "hinge_pin", "lever", "lever_pin"}     # lid open; lever moved to the eject socket
        if pname.startswith("assembly"):
            skip |= {"hub", "crank_pin", "lever", "lever_pin", "conlink", "pawl", "catch", "eject"}   # fitted after the upper pin
        keys = [k for k in C if k not in skip]
        # the pawl and the catch are spring ratchets: the crank pin pushes them aside as it passes
        joined_here = set(joined)
        if pname != "end of stroke":
            joined_here.add(frozenset(("crank_pin", "pawl")))
        if not (pname == "start" or ej > 0):
            joined_here.add(frozenset(("crank_pin", "catch")))
        bad = []
        for a, b_ in itertools.combinations(keys, 2):
            if frozenset((a, b_)) in joined_here:
                continue
            v = inter(C[a].shape, C[b_].shape)
            if v > 1.0:
                bad.append(f"{a} x {b_} ({v:.0f} mm3)")
        rec(not bad, f"[{pname}] no unintended overlaps among {len(keys)} parts" + ("" if not bad else ": " + "; ".join(bad)))
        if pname in ("start", "one third", "two thirds", "end of stroke", "eject half", "eject full"):
            # moving parts keep at least 3 mm from everything they are not joined to
            near = []
            for a in keys:
                if not C[a].moving:
                    continue
                for b_ in keys:
                    if a == b_ or frozenset((a, b_)) in joined_here or (C[b_].moving and b_ < a):
                        continue
                    d_ = gap(C[a].shape, C[b_].shape)
                    need = fits.get(frozenset((a, b_)), 3.0)
                    if d_ < need - 1e-6:
                        near.append(f"{a} to {b_} {d_:.1f} mm")
            rec(not near, f"[{pname}] moving parts clear by 3 mm or more" + ("" if not near else ": " + "; ".join(near)))
    C = build_components()
    D = derived()
    touch = [("skids", "cross"), ("cross", "base_plate"), ("cross", "bracket"), ("base_plate", "feet"), ("feet", "columns"),
             ("columns", "beam"), ("beam", "lugs"), ("flanges", "columns"), ("mold", "flanges"), ("mold", "mold_lugs"),
             ("lid", "mold"), ("ties", "beam"), ("posts", "base_plate"), ("guard", "base_plate"), ("guard", "bracket"),
             ("piston", "upper_pin"), ("eject", "piston"), ("seals_base", "lower_links"), ("seals_knee", "upper_links"), ("seals_upper", "upper_links"), ("hub", "rest"), ("pawl", "bracket"), ("catch", "bracket")]
    for a, b_ in touch:
        d_ = gap(C[a].shape, C[b_].shape)
        rec(d_ < 0.6, f"contact {a} / {b_}: gap {d_:.2f} mm")
    # piston stays inside the mold walls with its plate at the start and the end
    rec(D["zp0"] + PARAMS["pin_d"] / 2 <= D["MB"] + 5, "upper pin top no higher than 5 mm above the mold's lower edge at the start (assembly from the side)")
    rec(D["zp_asm"] + PARAMS["pin_d"] / 2 < D["MB"] - 2, f"upper pin clears the mold at the assembly fold ({D['zp_asm']:.0f} mm)")
    # dust seals: each seal sits against a link face and leaves the pin end room for a 1.5 mm circlip
    rec(PARAMS["seal_t"] + 1.5 + 0.2 <= 4.0, "pin ends 4 mm past the link face: room for a 2 mm dust seal and a 1.5 mm circlip")
    rec(D["col_in"] - (D["y_lower"][1] + PARAMS["seal_t"]) >= 3.0, f"dust seals on the base and knee pins clear the column webs by {D['col_in'] - D['y_lower'][1] - PARAMS['seal_t']:.1f} mm")
    # pins clear the column webs
    rec(D["y_lower"][1] + 4 < D["col_in"], f"base and knee pins end {D['col_in'] - D['y_lower'][1] - 4:.1f} mm inside the column webs")
    # eject: the slot leaves the pin 5 mm below its lower end at full lift
    rec(PARAMS["slot_len"] - PARAMS["pin_d"] - PARAMS["eject_lift"] >= 4.9, "eject lift fits the lost-motion slot")
    # lever grip band
    gz = [PARAMS["lever_z"] + PARAMS["grip_r"] * math.sin(math.radians(lever_angle(t))) for t in (th0, the)]
    rec(min(gz) >= 800, f"grip heights {gz[0]:.0f} to {gz[1]:.0f} mm; lowest grip above 0.8 m")
    # every made part can be made by its process: plate thickness and pieces of stock
    for k in ("lid", "mold_lugs", "bracket", "posts", "lower_links", "upper_links", "conlink", "pawl", "catch"):
        bb = C[k].shape.bounding_box()
        rec(min(bb.size.X, bb.size.Y, bb.size.Z) > 5, f"{k} cut from plate (thinnest size {min(bb.size.X, bb.size.Y, bb.size.Z):.0f} mm)")
    if verbose:
        for l in lines:
            print(l)
        print(f"{npass} pass, {nfail} fail")
    return npass, nfail, lines



# ================================================================== kit 1.9 interface (STANDARDS section 24)
# OPTIONS, PRINCIPLES, CHOSEN, OPTION_VIEWS, ALLOWED_CONTACTS and components(option), read by .kit/cad_check.py,
# .kit/options.py and cad/src/product_model.py. Option A is the constructable design above, part by part, with real
# stock, bushes, circlips, ISO fasteners and weld beads; options B and C are in cad/src/epr_options.py.
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

TITLE = "EarthPress"
OPTIONS = {"A": "Lever and toggle press", "B": "Power screw press", "C": "Rope-lifted drop rammer"}
PRINCIPLES = {
    "A": "A 1.7 m lever drives a toggle under a bottom piston; the force ratio climbs to 173:1 at a crank stop, "
         "so two people press a weighed fill to 2 MPa and a 90 mm block (static pressing).",
    "B": "Two people turn a capstan on a self-locking two-start Tr 40 x 14 screw in a bronze nut; the screw drives "
         "a platen down into the mold to a stop collar (static pressing by a power screw).",
    "C": "Two people pull a rope over a head pulley to lift a 20 kg weight 450 mm up a guide rod and let it drop "
         "on a plunger, about 25 blows per block to a height stop (dynamic, impact compaction).",
}
CHOSEN = "A"
OPTION_VIEWS = {k: {"el": 20, "az": -55, "scale": "person", "keep_context": False, "ground_z": 0} for k in OPTIONS}
# Joined on purpose: a pin or shaft in its bush or bore at zero clearance, a bolt in a tapped hole drawn at its
# nominal size, tube ends slotted over the bracket plates. Matching is by substring of the part names.
ALLOWED_CONTACTS = [
    ("Tie tube", "Lever bracket plate"),
    ("Split pin", "Clevis pin"),
    ("M16x25 hex bolt", "Mold side flange"),
    ("M10x16 hex bolt", "Base plate"),
]

PIN_STEEL = "42CrMo4 +QT"     # EPR-DEC-001, decision of 2026-10-25 under the standing instruction (EPR-STM-001 S9)
BOM_OF = {  # Comp key -> (BOM line, material, kind, piece for R7)
    "skids": (1, "painted_steel", "made", "base"), "cross": (1, "painted_steel", "made", "base"),
    "base_plate": (1, "painted_steel", "made", "base"), "bracket": (1, "painted_steel", "made", "base"),
    "rest": (1, "painted_steel", "made", "base"), "ties": (1, "painted_steel", "made", "base"),
    "posts": (1, "painted_steel", "made", "base"), "columns": (1, "painted_steel", "made", "core"),
    "feet": (1, "painted_steel", "made", "core"), "beam": (1, "painted_steel", "made", "core"),
    "lugs": (1, "painted_steel", "made", "core"),
    "mold": (2, "mild_steel", "made", "mold"), "flanges": (2, "painted_steel", "made", "mold"),
    "mold_lugs": (2, "painted_steel", "made", "mold"),
    "lid": (3, "painted_steel", "made", "lid"), "hinge_pin": (3, "zinc_plated", "bought", "lid"),
    "latch_pin": (3, "zinc_plated", "bought", "lid"),
    "piston": (4, "mild_steel", "made", "piston"),
    "lower_links": (5, "safety_yellow", "made", "toggle"), "upper_links": (5, "safety_yellow", "made", "toggle"),
    "base_pin": (5, "zinc_plated", "bought", "toggle"), "knee_pin": (5, "zinc_plated", "bought", "toggle"),
    "upper_pin": (5, "zinc_plated", "bought", "toggle"), "base_spacers": (5, "zinc_plated", "bought", "toggle"),
    "knee_spacers": (5, "zinc_plated", "bought", "toggle"), "conlink": (5, "safety_yellow", "made", "toggle"),
    "seals_base": (5, "epdm", "bought", "toggle"), "seals_knee": (5, "epdm", "bought", "toggle"),
    "seals_upper": (5, "epdm", "bought", "toggle"),
    "hub": (6, "painted_steel", "made", "hub"), "shaft": (6, "zinc_plated", "bought", "hub"),
    "crank_pin": (6, "zinc_plated", "bought", "hub"), "lever": (6, "safety_red", "made", "lever"),
    "eject": (7, "safety_red", "made", "eject"), "eject_pin": (7, "zinc_plated", "bought", "eject"),
    "pawl": (7, "safety_red", "made", "eject"), "catch": (7, "safety_red", "made", "eject"),
    "guard": (13, "galvanised", "made", "guard"),
}
NAMES = {
    "skids": "Skid, 60 x 60 x 3 SHS, 1.0 m", "cross": "Cross tube, 50 x 50 x 3 SHS", "base_plate": "Base plate, 12 mm",
    "bracket": "Lever bracket plate, 10 mm", "rest": "Rest stop bar, 30 mm round", "ties": "Tie tube, 40 x 3 CHS, with bolted end tab",
    "posts": "Eject post, 10 mm plate", "columns": "Column, UPN 80", "feet": "Column foot, 16 mm plate",
    "beam": "Base beam plate, 20 x 100 mm", "lugs": "Base pin lug, 28 mm plate", "mold": "Mold walls and belt, 12 mm plate",
    "flanges": "Mold side flange, 16 mm, tapped M16", "mold_lugs": "Mold hinge or latch lug, 20 mm plate",
    "lid": "Lid, 20 mm plate with two 20 x 70 mm ribs", "hinge_pin": "Hinge pin, 30 mm 42CrMo4 +QT",
    "latch_pin": "Latch pin, 30 mm 42CrMo4 +QT, with T-handle", "piston": "Piston plate, skirts and slotted push rod",
    "lower_links": "Lower toggle link, 28 x 70 mm", "upper_links": "Upper toggle link, 28 x 70 mm",
    "base_pin": "Base pin, 40 mm 42CrMo4 +QT", "knee_pin": "Knee pin, 40 mm 42CrMo4 +QT", "upper_pin": "Upper pin, 40 mm 42CrMo4 +QT",
    "base_spacers": "Base pin spacer tube, 8 mm", "knee_spacers": "Knee pin spacer tube, 20 mm",
    "conlink": "Connecting link, 24 x 60 mm", "seals_base": "Dust seal washer, base pin", "seals_knee": "Dust seal washer, knee pin",
    "seals_upper": "Dust seal washer, upper pin", "hub": "Lever hub with crank plates and socket", "shaft": "Hub shaft, 40 mm",
    "crank_pin": "Crank pin, 30 mm", "lever": "Lever, 2 in schedule 40 pipe with T-handle", "eject": "Eject seesaw: hub, arm and socket",
    "eject_pin": "Eject pivot pin, 30 mm", "pawl": "End pawl with pivot shaft and release handle",
    "catch": "Rest catch with pivot shaft and release handle", "guard": "Linkage guard, expanded metal on angle frame",
}
EXPLODE = {1: (0, 0, -300), 2: (0, 0, 420), 3: (0, 0, 780), 4: (620, 0, 650), 5: (380, 0, -60), 6: (0, -500, -700),
           7: (350, 450, -150), 8: (400, 600, 0), 9: (-300, -700, 0), 10: (300, -300, 450), 11: (0, 0, 0), 13: (-300, 0, 0)}


def _option_a(p=PARAMS):
    """Option A, the constructable lever and toggle press (EPR-DDR-003), as detailed parts (D3)."""
    import cad_parts as cp
    from cad_parts import part, break_edges
    import epr_parts as E
    from build123d import Box, Cylinder, Pos, Rot, Plane, Location, Vector
    C = build_components(p)
    D = derived(p)
    g = geometry(p)
    out = []

    def add(name, shape, key=None, mat=None, kind=None, bom=None, piece=None, ex=None):
        b_, m_, k_, pc = BOM_OF.get(key, (bom, mat, kind, piece)) if key else (bom, mat, kind, piece)
        out.append(part(name, shape, mat or m_, kind=kind or k_, bom=bom if bom is not None else b_, group=piece or pc,
                        explode=ex or EXPLODE.get(bom if bom is not None else b_, (0, 0, 0))))

    sk, sy, cs = p["skid"], p["skid_y"], p["cross"]
    L2 = p["skid_len"] / 2
    yi = sy - sk / 2
    # ---- base: skids and cross tubes as real SHS with rounded corners
    for s in (-1, 1):
        sh = Pos(-L2, s * sy, sk / 2) * cp.along(cp.shs(sk, 3, p["skid_len"]), "x")
        add(f"{NAMES['skids']}, {'left' if s < 0 else 'right'}", break_edges(sh, 0.5), "skids")
    xs_cross = (-L2 + cs / 2, p["base_x0"] + cs / 2, p["base_x1"] - cs / 2, L2 - cs / 2)
    for i, xc in enumerate(xs_cross, 1):
        ct = Pos(xc, -yi, sk - cs / 2) * cp.along(cp.shs(cs, 3, 2 * yi), "y")
        add(f"{NAMES['cross']} {i}", ct, "cross")
    # ---- every other steel part from the constructable model, one part per piece of stock
    simple = {"base_plate", "feet", "beam", "lugs", "flanges", "posts", "lid", "mold", "conlink", "lower_links", "upper_links",
              "mold_lugs", "columns", "piston", "hub", "eject", "pawl", "catch", "ties", "bracket", "base_spacers", "knee_spacers",
              "seals_base", "seals_knee", "seals_upper", "guard", "latch_pin", "lever"}
    gx_b = (-390.0, (132.5, 282.5))                      # guard bracket bolts, through the bracket plates
    for key in sorted(simple, key=lambda k: list(C).index(k)):
        sols = E.solids(C[key].shape)
        for j, sol in enumerate(sols, 1):
            if key == "bracket":
                for zz in gx_b[1]:
                    sol = sol - E.ypin(gx_b[0], zz, 11.0, -80, 80, 0)
            if key == "guard":
                for zz in gx_b[1]:
                    sol = sol - E.ypin(gx_b[0], zz, 11.0, -140, 140, 0)
            if key in ("base_plate", "feet", "beam", "lugs", "posts", "flanges"):
                sol = break_edges(sol, 1.0)
            nm = NAMES[key] + (f" {j}" if len(sols) > 1 else "")
            add(nm, sol, key)
    # ---- turned pins, shaft and stop bar with chamfered ends; circlips (DIN 471) where the pin is retained
    zb = g["z_b"]
    th = theta_start(p)
    (kx, kz), z_p, _ = toggle_state(th, p)
    (cx, cz), psi = knee_and_crank(th, p)
    yu, ylw = D["y_upper"], D["y_lower"]
    pd = p["pin_d"]
    L_tog = ylw[1] + 4
    hx, hz, lxx, lzz = p["hinge_x"], p["hinge_z"], p["latch_x"], p["latch_z"]
    pin_l = p["lug_y0"] + p["lug_t"] + 6
    pins = [("base_pin", 0, zb, pd, L_tog, ylw[1] + p["seal_t"]), ("knee_pin", kx, kz, pd, L_tog, ylw[1] + p["seal_t"]),
            ("upper_pin", 0, z_p, pd, yu[1] + 4, yu[1] + p["seal_t"]),
            ("hinge_pin", hx, hz, p["hinge_pin_d"], pin_l, p["lug_y0"] + p["lug_t"]),
            ("shaft", p["lever_x"], p["lever_z"], 40.0, 77, 60 + p["bracket_t"]),
            ("crank_pin", cx, cz, p["crank_pin_d"], 56, 36.0), ("eject_pin", p["eject_x"], p["eject_z"], 30.0, 76, 70.0)]
    for key, x, z, d, L, yc in pins:
        add(NAMES[key], E.ypin(x, z, d, -L, L), key)
        for s in (-1, 1):
            out.append(part(f"Circlip DIN 471, {d:.0f} mm, {NAMES[key].split(',')[0].lower()}", Pos(0, 0, 0) * E.circlip(x, z, d, s * yc, s),
                            "zinc_plated", kind="fastener", bom=11, group=BOM_OF[key][3], explode=EXPLODE[BOM_OF[key][0]]))
    REST = C["rest"].shape.bounding_box().center()
    add(NAMES["rest"], E.ypin(REST.X, REST.Z, 30.0, -60, 60), "rest")
    # ---- bushes: case-hardened steel, 40 bore x 46 outside, in every link end and in the two base pin lugs
    bo = p["bush_od"]
    for s in (-1, 1):
        for (x, z, y0, y1, nm) in ((0, zb, ylw[0], ylw[1], "lower link, base end"), (kx, kz, ylw[0], ylw[1], "lower link, knee end"),
                                   (kx, kz, yu[0], yu[1], "upper link, knee end"), (0, z_p, yu[0], yu[1], "upper link, piston end"),
                                   (0, zb, D["lug_y"][0], D["lug_y"][1], "base pin lug")):
            add(f"Bush 40 x 46, case-hardened, {nm} {'left' if s < 0 else 'right'}", E.ybush(x, z, bo, pd, s * y0, s * y1),
                bom=5, mat="stainless", kind="bought", piece="toggle")
    # ---- grease nipples: six, one in each lower link end and each upper link piston end, radial in the link's plane
    def link_nipple(a, b_, ycen, nm):
        ax_, az_ = a; bx_, bz_ = b_
        L_ = math.hypot(bx_ - ax_, bz_ - az_)
        ux_, uz_ = (bx_ - ax_) / L_, (bz_ - az_) / L_
        nx_, nz_ = uz_, -ux_                                # in the link plane, square to the link
        r_ = p["link_w"] / 2
        o = (ax_ + nx_ * r_ * 0.0 + (-ux_) * 0.0 + nx_ * r_, ycen, az_ + nz_ * r_)
        return E.nipple(o, (nx_, 0, nz_)), E.nipple_hole(o, (nx_, 0, nz_)), nm
    nips = []
    for s in (-1, 1):
        yl_c = s * (ylw[0] + ylw[1]) / 2; yu_c = s * (yu[0] + yu[1]) / 2
        nips += [link_nipple((0, zb), (kx, kz), yl_c, "lower link base end"), link_nipple((kx, kz), (0, zb), yl_c, "lower link knee end"),
                 link_nipple((0, z_p), (kx, kz), yu_c, "upper link piston end")]
    for n_, hole, nm in nips:
        out.append(part(f"Grease nipple M6, {nm}", n_, "brass", kind="fastener", bom=5, group="toggle", explode=EXPLODE[5]))
        for q in out:
            if q["name"].startswith(("Lower toggle link", "Upper toggle link")) and q["shape"].bounding_box().center().Y * hole.bounding_box().center().Y > 0:
                bb1, bb2 = q["shape"].bounding_box(), hole.bounding_box()
                if not (bb1.max.X < bb2.min.X or bb2.max.X < bb1.min.X or bb1.max.Z < bb2.min.Z or bb2.max.Z < bb1.min.Z or bb1.max.Y < bb2.min.Y or bb2.max.Y < bb1.min.Y):
                    q["shape"] = q["shape"] - hole
    # ---- lever locking pin: ISO 2341 clevis pin with split pin, square to the lever through the socket
    phi = math.radians(math.degrees(psi) + p["lever_offset"])
    ux, uz = math.cos(phi), math.sin(phi)
    lx, lz = p["lever_x"], p["lever_z"]
    n_ = Vector(-uz, 0, ux) * -1
    p0 = Vector(lx + 225 * ux, 0, lz + 225 * uz) - n_ * 45
    loc = Location(Plane(origin=p0, x_dir=Vector(ux, 0, uz), z_dir=n_ * -1))
    grip = 90.0
    add("Clevis pin ISO 2341, 12 mm, lever locking pin", loc * cp.clevis_pin(12, grip), bom=6, mat="zinc_plated", kind="bought", piece="lever")
    out.append(part("Split pin ISO 1234, lever locking pin", loc * Pos(0, 0, -grip - 12) * cp.split_pin(12), "zinc_plated",
                    kind="fastener", bom=6, group="lever", explode=EXPLODE[6]))
    # ---- rubber grips on the T-handle ends (BOM 6)
    gpt = (lx + p["grip_r"] * ux, lz + p["grip_r"] * uz)
    for s in (-1, 1):
        add(f"Rubber grip, T-handle {'left' if s < 0 else 'right'}", E.ytube(gpt[0], gpt[1], 42.0, 33.4, s * 130, s * 250),
            bom=6, mat="epdm", kind="bought", piece="lever")
    # ---- fasteners (BOM 11)
    MB = D["MB"]; ci, cw = D["col_in"], p["col_web"]
    FX = lambda nm, shp, pc, ex: out.append(part(nm, shp, "zinc_plated", kind="fastener", bom=11, group=pc, explode=ex))
    for s in (-1, 1):
        for zz in [MB + dz_ for dz_ in MOLD_BOLT_DZ]:
            for xx in (0.0,):
                y0 = s * (ci + cw)
                rot = Rot(-90, 0, 0) if s > 0 else Rot(90, 0, 0)      # local +Z out of the column web
                FX("M16 washer (ISO 7089), mold to column", Pos(xx, y0, zz) * rot * cp.washer(16), "bolts", EXPLODE[2])
                FX("M16x25 hex bolt (ISO 4017) grade 8.8, mold to column", Pos(xx, y0, zz) * rot * Pos(0, 0, 3) * cp.hex_bolt(16, 25), "bolts", EXPLODE[2])
        for fx in (-55, 55):
            for fy in (D["col_y"] - 35, D["col_y"] + 35):
                for nm, shp in cp.hex_bolt_set(12, 16 + p["base_t"]):
                    FX(nm + " grade 8.8, column foot", Pos(fx, s * fy, D["foot_z"]) * shp, "bolts", EXPLODE[1])
        bz1 = D["beam_z1"]; beam_x0 = -p["col_d"] / 2 - p["beam_t"]
        for zz in (bz1 - 72, bz1 - 27):
            for nm, shp in cp.hex_bolt_set(12, 10 + p["beam_t"] + p["col_flange"]):
                FX(nm + " grade 8.8, tie tab", Pos(beam_x0 - 10, s * 130, zz) * Rot(0, -90, 0) * shp, "bolts", EXPLODE[1])
        # guard: feet into tapped holes in the base plate; side frames through the welded spacer brackets
        gy = p["guard_y"]
        FX("M10 washer (ISO 7089), guard foot", Pos(-94, s * (gy - 12), D["zb_top"] + 3) * cp.washer(10), "bolts", EXPLODE[13])
        FX("M10x16 hex bolt (ISO 4017), guard foot", Pos(-94, s * (gy - 12), D["zb_top"] + 5) * cp.hex_bolt(10, 16), "bolts", EXPLODE[13])
        for zz in gx_b[1]:
            rot = Rot(-90, 0, 0) if s > 0 else Rot(90, 0, 0)
            for nm, shp in cp.hex_bolt_set(10, 60 + 10 + 2 + 5):
                FX(nm + ", guard bracket", Pos(gx_b[0], s * (gy + 22), zz) * rot * shp, "bolts", EXPLODE[13])
    # ---- weld beads (BOM 12 consumables; shown as beads)
    W = lambda nm, shp, pc, bom: out.append(part(f"Weld, {nm}", shp, "mild_steel", kind="weld", bom=12, group=pc, explode=EXPLODE[bom]))
    for s in (-1, 1):
        for i, xc in enumerate(xs_cross):
            for side in (-1, 1):
                if (i == 0 and side < 0) or (i == 3 and side > 0):
                    continue
                W(f"cross tube {i + 1} to skid", E.bead((xc + side * cs / 2, s * yi, sk - cs), (0, 0, 1), cs, 5, (side, 0, 0), (0, -s, 0)), "base", 1)
        W("bracket plate to cross tube, outer", E.bead((-L2, s * (60 + p["bracket_t"]), sk), (1, 0, 0), cs, 6, (0, s, 0), (0, 0, 1)), "base", 1)
        W("bracket plate to cross tube, inner", E.bead((-L2, s * 60, sk), (1, 0, 0), cs, 6, (0, -s, 0), (0, 0, 1)), "base", 1)
        ex_ = p["eject_x"]
        W("eject post to base plate, outer", E.bead((ex_ - 30, s * 70, D["zb_top"]), (1, 0, 0), 60, 6, (0, s, 0), (0, 0, 1)), "base", 1)
        W("eject post to base plate, inner", E.bead((ex_ - 30, s * 60, D["zb_top"]), (1, 0, 0), 60, 5, (0, -s, 0), (0, 0, 1)), "base", 1)
        cd = p["col_d"]
        W("column web to foot", E.bead((-cd / 2 + p["col_flange"], s * ci, D["foot_z"]), (1, 0, 0), cd - 2 * p["col_flange"], 6, (0, -s, 0), (0, 0, 1)), "core", 1)
        for sx in (-1, 1):
            W("column flange to foot", E.bead((sx * cd / 2, s * ci, D["foot_z"]), (0, s, 0), p["col_b"], 6, (sx, 0, 0), (0, 0, 1)), "core", 1)
            W("column flange to base beam plate", E.bead((sx * cd / 2, s * ci, D["beam_z1"]), (0, s, 0), p["col_b"], 8, (sx, 0, 0), (0, 0, 1)), "core", 1)
            W("base pin lug to base beam plate", E.bead((sx * cd / 2, s * D["lug_y"][1], D["beam_z1"] - 30), (0, 0, 1), 30, 6, (-sx, 0, 0), (0, s, 0)), "core", 1)
        # mold: belt to walls, flanges to walls
        ox, oy, MT, bh = D["ox"], D["oy"], D["MT"], p["belt_h"]
        W("mold belt to end wall", E.bead((s * ox, -oy, MT - bh), (0, 1, 0), 2 * oy, 6, (s, 0, 0), (0, 0, -1)), "mold", 2)
        for a0, a1 in ((-ox, -cd / 2 - 28), (cd / 2 + 28, ox)):
            W("mold belt to side wall", E.bead((a0, s * oy, MT - bh), (1, 0, 0), a1 - a0, 6, (0, s, 0), (0, 0, -1)), "mold", 2)
        for sx in (-1, 1):
            W("mold side flange to wall", E.bead((sx * (cd / 2 + 20), s * oy, MB), (0, 0, 1), MT - bh - MB, 8, (sx, 0, 0), (0, s, 0)), "mold", 2)
        # lid ribs
        ry0 = p["rib_y"] - p["rib_t"] / 2
        for yy, n2 in ((s * (ry0 + p["rib_t"]), s), (s * ry0, -s)):
            W("lid rib to lid plate", E.bead((-p["lid_l"] / 2, yy, MT + p["lid_t"]), (1, 0, 0), p["lid_l"], 8, (0, n2, 0), (0, 0, 1)), "lid", 3)
    # piston: push rod to plate (all four faces), skirts to plate
    zf = toggle_state(th, p)[2]; zpb = zf - p["piston_t"]; r = p["rod"]; cl = p["piston_clear"]
    for sx in (-1, 1):
        W("push rod to piston plate", E.bead((sx * r / 2, -r / 2, zpb), (0, 1, 0), r, 8, (sx, 0, 0), (0, 0, -1)), "piston", 4)
        W("push rod to piston plate", E.bead((-r / 2, sx * r / 2, zpb), (1, 0, 0), r, 4, (0, sx, 0), (0, 0, -1)), "piston", 4)
        xs_ = sx * (p["blk_l"] / 2 - cl - p["skirt_t"])
        W("skirt to piston plate", E.bead((xs_, -p["blk_w"] / 2 + cl, zpb), (0, 1, 0), p["blk_w"] - 2 * cl, 6, (-sx, 0, 0), (0, 0, -1)), "piston", 4)
    W("base plate to cross tube 3", E.bead((p["base_x1"] - cs, -p["base_w"] / 2, sk), (0, 1, 0), p["base_w"], 6, (-1, 0, 0), (0, 0, -1)), "base", 1)
    W("base plate to cross tube 2", E.bead((p["base_x0"] + cs, -60, sk), (0, 1, 0), 120, 6, (1, 0, 0), (0, 0, -1)), "base", 1)
    # ---- soil sieve (8), soil test kit (9), block gauge (10)
    SX, SY = 1150.0, 750.0
    loc_s = Pos(SX, SY, 420) * Rot(0, -25, 0)
    for nm, (bx, by, bz), (px_, py_, pz_) in (("Sieve frame side, timber 45 x 45", (45, 45, 900), (0, -327.5, 0)),
                                              ("Sieve frame side, timber 45 x 45", (45, 45, 900), (0, 327.5, 0)),
                                              ("Sieve frame rail, timber 45 x 45", (45, 610, 45), (0, 0, -427.5)),
                                              ("Sieve frame rail, timber 45 x 45", (45, 610, 45), (0, 0, 427.5))):
        add(nm, loc_s * Pos(px_, py_, pz_) * break_edges(Box(bx, by, bz), 3), bom=8, mat="timber", kind="made", piece="kit")
    mesh = loc_s * Pos(-2, 0, 0) * Rot(0, 90, 0) * Pos(0, 0, -2) * cp.sheet(810, 610, 4, r_corner=4)
    add("Sieve mesh, 5 mm welded wire (drawn as a sheet)", mesh, bom=8, mat="galvanised", kind="made", piece="kit")
    nx_, nz_ = math.cos(math.radians(25)), math.sin(math.radians(25))      # back face normal of the tilted sieve
    top_x, top_z = SX + (22.5 + 14) * nx_ - 300 * nz_, 420 + (22.5 + 14) * nz_ + 300 * nx_
    for sy_ in (-1, 1):
        prop = break_edges(E.rod3((top_x + 400, SY + sy_ * 327.5, 0), (top_x, SY + sy_ * 327.5, top_z), 24), 1.5)
        add(f"Sieve prop, timber 24 mm {'left' if sy_ < 0 else 'right'}", prop, bom=8, mat="timber", kind="made", piece="kit")
    add("Soil test kit box", Pos(450, -700, 125) * break_edges(Box(400, 300, 250) - Pos(0, 0, 10) * Box(380, 280, 240), 2), bom=9, mat="hdpe_natural", kind="bought", piece="kit")
    for jx in (370, 490):
        jar = Pos(jx, -740, 250) * (Pos(0, 0, 80) * Cylinder(45, 160) - Pos(0, 0, 84) * Cylinder(42, 156))
        add("Sedimentation jar, 1 L", break_edges(jar, 1), bom=9, mat="glass", kind="bought", piece="kit")
        add("Jar lid", Pos(jx, -740, 410) * break_edges(Pos(0, 0, 10) * Cylinder(47, 20), 2), bom=9, mat="hdpe_black", kind="bought", piece="kit")
    sb = Pos(450, -620, 270) * (Box(600, 40, 40) - Pos(0, 0, 8) * Box(580, 24, 26))
    add("Shrinkage box, 600 x 40 x 40 mm", break_edges(sb, 1), bom=9, mat="timber", kind="bought", piece="kit")
    BX, BY = 1000.0, -300.0
    GZ = 4 * p["blk_h"]
    gauge = (Pos(BX, BY, GZ + 20) * Box(340, 12, 40) + Pos(BX - 152, BY, GZ - 20) * Box(12, 12, 40)
             + Pos(BX + 152, BY, GZ - 20) * Box(12, 12, 40)) - Pos(BX, BY, GZ + 30) * Box(93, 14, 20.01)
    add("Block gauge, 12 mm flat bar", break_edges(gauge, 0.8), bom=10, mat="painted_steel", kind="made", piece="kit")
    # ---- context: the loose fill and a stack of pressed blocks
    out.append(part("Loose soil fill (context)", C["fill"].shape, "soil", kind="context", group="context"))
    out.append(part("Pressed blocks (context)", C["blocks"].shape, "soil", kind="context", group="context"))
    return out


def components(option=CHOSEN):
    """Kit 1.9: every part of a concept option as cad_parts.part() dicts (made, bought, fastener, weld, context)."""
    if option == "A":
        return _option_a()
    import epr_options
    return epr_options.build(option)


PIECE_NAMES = [("base", "Base frame with lever bracket, ties and eject posts"), ("core", "Press core, columns and base beam"),
               ("mold", "Mold box with hinge and latch lugs"), ("lid", "Lid with ribs, hinge and latch pins"),
               ("piston", "Piston and slotted push rod"), ("toggle", "Toggle links, pins, bushes, spacers and seals"),
               ("hub", "Lever hub, crank, shaft and crank pin"), ("lever", "Lever pipe and T-handle"),
               ("eject", "Eject seesaw, pivot pin, end pawl and rest catch"), ("guard", "Linkage guard"),
               ("bolts", "Bolts, nuts and washers")]


def piece_masses(parts=None, comps=None):
    """Mass (kg) of each piece of the press as it is lifted (R7, PR-007), from the detailed option A model:
    every made and bought part, fastener and weld bead at its material's density, the guard's expanded metal
    panels at GUARD_FILL of solid sheet. The soil kit, sieve and gauge are not part of the press."""
    import cad_parts as cp
    ps = parts or components("A")
    out = {n: 0.0 for _, n in PIECE_NAMES}
    key = dict(PIECE_NAMES)
    for q in ps:
        if q["kind"] == "context" or q["group"] in ("kit", "context"):
            continue
        m = cp.mass_kg(q)
        if q["name"].startswith("Linkage guard"):
            m = q["shape"].volume * STEEL * GUARD_FILL
        out[key[q["group"]]] += m
    return out


if __name__ == "__main__":
    # python cad/src/model.py --check : constructability checks of the Comp model (overlaps, contacts, sweeps)
    # python cad/src/model.py         : part list with masses and STL of the chosen design (cad/stl/); the STEP files
    #                                   come from python .kit/cad_check.py --export (cad/step/A/, cad/step/<option>-assembly.step)
    if "--check" in sys.argv:
        _, nf, _ = check()
        sys.exit(1 if nf else 0)
    import copy
    import cad_parts as cp
    from build123d import Compound, export_stl
    for opt in OPTIONS:
        ps = components(opt)
        real = [q for q in ps if q["kind"] != "context"]
        print(f"option {opt}: {len(real)} parts, {sum(cp.mass_kg(q) for q in real):.1f} kg (guard as solid sheet)")
    ps = components(CHOSEN)
    for n, m in piece_masses(ps).items():
        print("  %-52s %6.1f kg" % (n, m))
    out = HERE.parents[0] / "stl"
    out.mkdir(exist_ok=True)
    for old in out.glob("earthpress-*.stl"):
        old.unlink()
    asm = assemblies(ps)
    export_stl(asm["earthpress-assembly"], str(out / "earthpress-assembly.stl"), tolerance=0.15, angular_tolerance=0.3)
    for slug, keys in (("mold", ("Mold walls", "Mold side flange", "Mold hinge or latch lug")), ("lid", ("Lid,",)),
                       ("toggle", ("Lower toggle link", "Upper toggle link", "Connecting link", "Base pin,", "Knee pin,", "Upper pin,", "Bush 40 x 46"))):
        sel = [copy.copy(q["shape"]) for q in ps if q["name"].startswith(keys)]
        export_stl(Compound(children=sel), str(out / f"earthpress-{slug}.stl"), tolerance=0.15, angular_tolerance=0.3)
    print("wrote cad/stl (tolerance 0.15 mm)")
