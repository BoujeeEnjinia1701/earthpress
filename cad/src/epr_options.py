"""EarthPress concept options B and C at detail level D3 (EPR-OPT-001, STANDARDS sections 21 and 24).

    B  Power screw press: an H frame of UPN 80 sections carries a bronze nut in its crosshead; two people turn a
       capstan on a self-locking two-start Tr 40 x 14 screw that drives a platen down into the mold to a stop
       collar. A removable stop pin holds the floor piston during pressing; an eject seesaw lifts it after.
    C  Rope-lifted drop rammer: the same base, columns, mold, floor piston and eject seesaw; a light crosshead
       guides a 40 mm rod carrying the plunger. Two people pull a rope over a head pulley on the rod to lift a
       20 kg sleeve weight 450 mm and let it fall on the anvil collar; a stop collar on the rod sets the height.

Both share the block (290 x 140 x 90 mm), the mold box and the soil kit with option A (cad/src/model.py). Axes
as model.py: X along the press, Y across, Z up from the ground (z = 0). Options are drawn at the start of the
stroke with loose soil in the mold. Sizes come from the first-order numbers in EPR-OPT-001 and the STEM check
rows B1 to B6 and C1 to C6 (docs/04-calcs/stem_check.py). CONCEPT OPTIONS, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Cylinder, Pos, Rot, Sketch, Circle, extrude  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402
import epr_parts as E  # noqa: E402

OPT = dict(
    BL=290.0, BW=140.0, BH=90.0, FILL=150.0, WALL=12.0, BELT_T=16.0, BELT_H=50.0, FLANGE_T=16.0,
    MT=900.0, MOLD_H=200.0,                     # rim at 900 mm for filling from the top
    SKID=60.0, SKID_LEN=1000.0, SKID_Y=260.0, CROSS=50.0, BASE_T=12.0,
    COL_D=80.0, COL_B=45.0, COL_W=6.0, COL_F=8.0,
    PLATE_T=25.0, ROD=60.0, STOP_PIN=30.0,
    # B: screw press
    SCREW_D=40.0, SCREW_LEAD=14.0, SCREW_L=760.0, NUT_L=90.0, NUT_W=80.0, CAP_BAR=1200.0, CAP_D=32.0,
    HEAD_Z0=1240.0,                             # crosshead underside
    # C: drop rammer
    GUIDE_ROD=40.0, WEIGHT_OD=160.0, WEIGHT_L=136.0, DROP=450.0, C_HEAD_Z0=1080.0,
)
O = OPT
MS, PS = "mild_steel", "painted_steel"
MOLD_BOLT_DZ = (20.0, 57.0, 93.0, 130.0)   # as option A (cad/src/model.py)


def _geo():
    BL, BW, W = O["BL"], O["BW"], O["WALL"]
    ox, oy = BL / 2 + W, BW / 2 + W
    MT = O["MT"]; MB = MT - O["MOLD_H"]
    zb_top = O["SKID"] + O["BASE_T"]
    col_in = oy + O["FLANGE_T"]
    floor_top = MT - O["FILL"]                    # floor piston face during pressing
    return dict(ox=ox, oy=oy, MT=MT, MB=MB, zb_top=zb_top, col_in=col_in, col_out=col_in + O["COL_B"],
                col_y=col_in + O["COL_B"] / 2, foot_z=zb_top + 16.0, floor_top=floor_top)


def _fx(out, nm, shp, grp="frame", ex=(0, 0, 0), mat="zinc_plated"):
    out.append(part(nm, shp, mat, kind="fastener", group=grp, explode=ex))


def _weld(out, nm, shp, grp="frame"):
    out.append(part(f"Weld, {nm}", shp, MS, kind="weld", group=grp))


def common(option, col_top):
    """Base on skids, columns, mold box, floor piston with push rod and stop pin, bottom beam and eject seesaw."""
    g = _geo()
    out = []
    sk, sy, cs = O["SKID"], O["SKID_Y"], O["CROSS"]
    L2 = O["SKID_LEN"] / 2
    yi = sy - sk / 2
    for s in (-1, 1):
        out.append(part(f"Skid, 60 x 60 x 3 SHS {'left' if s < 0 else 'right'}", Pos(-L2, s * sy, sk / 2) * cp.along(cp.shs(sk, 3, O["SKID_LEN"]), "x"),
                        PS, group="frame", explode=(0, 0, -250)))
    xs = (-L2 + cs / 2, -185.0, 185.0, L2 - cs / 2)
    for i, xc in enumerate(xs, 1):
        out.append(part(f"Cross tube, 50 x 50 x 3 SHS {i}", Pos(xc, -yi, sk - cs / 2) * cp.along(cp.shs(cs, 3, 2 * yi), "y"), PS,
                        group="frame", explode=(0, 0, -250)))
        for s in (-1, 1):
            for side in (-1, 1):
                if (i == 1 and side < 0) or (i == 4 and side > 0):
                    continue
                _weld(out, f"cross tube {i} to skid", E.bead((xc + side * cs / 2, s * yi, sk - cs), (0, 0, 1), cs, 5, (side, 0, 0), (0, -s, 0)))
    zb = g["zb_top"]
    bp = Pos(0, 0, sk) * cp.sheet(420, 360, O["BASE_T"], holes=[(fx, s * fy, 13.5) for fx in (-55, 55) for s in (-1, 1)
                                                                for fy in (g["col_y"] - 35, g["col_y"] + 35)], r_corner=6)
    out.append(part("Base plate, 12 mm", bp, PS, group="frame", explode=(0, 0, -250)))
    for sx in (-1, 1):
        _weld(out, "base plate to cross tube", E.bead((sx * 160, -180, sk), (0, 1, 0), 360, 6, (-sx, 0, 0), (0, 0, -1)))
    # columns, UPN 80, webs toward the mold, on bolted feet
    cd, cb, cw, cf = O["COL_D"], O["COL_B"], O["COL_W"], O["COL_F"]
    ci = g["col_in"]; zc0 = g["foot_z"]
    MB, MT = g["MB"], g["MT"]
    for s in (-1, 1):
        ch = cp.channel(cd, cb, cw, col_top - zc0, tf=cf)              # web along Y at x 0..6 -> turn it
        col = Pos(0, s * ci, zc0) * Rot(0, 0, 90 if s > 0 else -90) * ch
        for zz in [MB + dz_ for dz_ in MOLD_BOLT_DZ]:
            for xx in (0.0,):
                col = col - E.ypin(xx, zz, 18.0, s * (ci - 1), s * (ci + cw + 1), 0)
        for zz in (col_top - 60, col_top - 20, 530.0, 570.0):
            for xx in (0.0,):
                col = col - E.ypin(xx, zz, 18.0, s * (ci - 1), s * (ci + cw + 1), 0)
        out.append(part(f"Column, UPN 80 {'left' if s < 0 else 'right'}", col, PS, group="frame", explode=(0, s * 250, 0)))
        foot = Pos(0, s * g["col_y"], zb) * cp.sheet(140, 90, 16, holes=[(fx, fy, 13.5) for fx in (-55, 55) for fy in (-35, 35)], r_corner=4)
        out.append(part(f"Column foot, 16 mm {'left' if s < 0 else 'right'}", foot, PS, group="frame", explode=(0, s * 250, -120)))
        _weld(out, "column web to foot", E.bead((-cd / 2 + cf, s * ci, zc0), (1, 0, 0), cd - 2 * cf, 6, (0, -s, 0), (0, 0, 1)))
        for sx in (-1, 1):
            _weld(out, "column flange to foot", E.bead((sx * cd / 2, s * ci, zc0), (0, s, 0), cb, 6, (sx, 0, 0), (0, 0, 1)))
        for fx in (-55, 55):
            for fy in (g["col_y"] - 35, g["col_y"] + 35):
                for nm, shp in cp.hex_bolt_set(12, 16 + O["BASE_T"]):
                    _fx(out, nm + " grade 8.8, column foot", Pos(fx, s * fy, zc0) * shp)
    # mold box: walls and belt, side flanges tapped M16 and bolted to the column webs
    BL, BW, W = O["BL"], O["BW"], O["WALL"]
    ox, oy = g["ox"], g["oy"]
    bt, bh = O["BELT_T"], O["BELT_H"]
    mold = Pos(0, 0, (MB + MT) / 2) * (Box(2 * ox, 2 * oy, MT - MB) - Box(BL, BW, MT - MB + 2))
    belt = Pos(0, 0, MT - bh / 2) * (Box(2 * (ox + bt), 2 * (oy + bt), bh) - Box(2 * ox, 2 * oy, bh + 2))
    out.append(part("Mold walls and belt, 12 mm plate", mold + belt, MS, group="mold", explode=(0, 0, 400)))
    for s in (-1, 1):
        fl = Pos(0, s * (oy + O["FLANGE_T"] / 2), (MB + MT - bh) / 2) * Box(cd + 40, O["FLANGE_T"], MT - bh - MB)
        for zz in [MB + dz_ for dz_ in MOLD_BOLT_DZ]:
            for xx in (0.0,):
                fl = fl - E.ypin(xx, zz, 16.0, s * (oy - 1), s * (oy + O["FLANGE_T"] + 1), 0)
        out.append(part(f"Mold side flange, 16 mm, tapped M16 {'left' if s < 0 else 'right'}", break_edges(fl, 1.0), PS, group="mold", explode=(0, 0, 400)))
        for sx in (-1, 1):
            _weld(out, "mold side flange to wall", E.bead((sx * (cd / 2 + 20), s * oy, MB), (0, 0, 1), MT - bh - MB, 8, (sx, 0, 0), (0, s, 0)), "mold")
        _weld(out, "mold belt to end wall", E.bead((s * ox, -oy, MT - bh), (0, 1, 0), 2 * oy, 6, (s, 0, 0), (0, 0, -1)), "mold")
        for zz in [MB + dz_ for dz_ in MOLD_BOLT_DZ]:
            for xx in (0.0,):
                y0 = s * (ci + cw)
                rot = Rot(-90, 0, 0) if s > 0 else Rot(90, 0, 0)
                _fx(out, "M16 washer (ISO 7089), mold to column", Pos(xx, y0, zz) * rot * cp.washer(16))
                _fx(out, "M16x25 hex bolt (ISO 4017) grade 8.8, mold to column", Pos(xx, y0, zz) * rot * Pos(0, 0, 3) * cp.hex_bolt(16, 25))
    # bottom beam: two UPN 80 along Y, webs vertical either side of the push rod, on end plates bolted to the columns
    gap = O["ROD"] + 4
    bz0 = 510.0
    for sx in (-1, 1):
        ch = cp.channel(cd, cb, cw, 2 * (ci - 15), tf=cf)        # web along Y in the profile: turn it to stand vertical
        # profile in XZ: web vertical at x = sx * gap / 2, flanges outward
        beam = Pos(sx * gap / 2, -(ci - 15), bz0 + cd / 2) * Rot(-90, 0, 0) * Rot(0, 0, 0 if sx > 0 else 180) * ch
        out.append(part(f"Bottom beam, UPN 80 {'-X' if sx < 0 else '+X'}", beam, PS, group="frame", explode=(sx * 200, 0, -150)))
    for s in (-1, 1):
        ep = Pos(0, s * (ci - 7.5), bz0 + cd / 2) * Box(gap + 2 * cb, 15, cd)
        for zz in (530.0, 570.0):
            for xx in (0.0,):
                ep = ep - E.ypin(xx, zz, 18.0, s * (ci - 16), s * (ci + 1), 0)
        out.append(part(f"Bottom beam end plate, 15 mm {'left' if s < 0 else 'right'}", break_edges(ep, 1.0), PS, group="frame", explode=(0, 0, -150)))
        for zz in (530.0, 570.0):
            for xx in (0.0,):
                rot = Rot(-90, 0, 0) if s > 0 else Rot(90, 0, 0)
                for nm, shp in cp.hex_bolt_set(16, cw + 15):
                    _fx(out, nm + " grade 8.8, bottom beam to column", Pos(xx, s * (ci + cw), zz) * rot * shp)
        for sx in (-1, 1):
            _weld(out, "bottom beam to end plate", E.bead((sx * (gap / 2 + cb), s * (ci - 15), bz0), (0, 0, 1), cd, 6, (sx, 0, 0), (0, -s, 0)))
    # floor piston: plate with end skirts on a 60 mm push rod; stop pin through the rod resting on the bottom beam
    ft = g["floor_top"]; cl = 1.0; pt = O["PLATE_T"]; r = O["ROD"]
    fp = Pos(0, 0, ft - pt / 2) * Box(BL - 2 * cl, BW - 2 * cl, pt)
    for sx in (-1, 1):
        fp = fp + Pos(sx * (BL / 2 - cl - 6), 0, ft - pt - 30) * Box(12, BW - 2 * cl, 60)
    fp = break_edges(fp, 0.8)
    zpin = bz0 + cd + O["STOP_PIN"] / 2
    rod_bot = 330.0
    rod = Pos(0, 0, (rod_bot + ft - pt) / 2) * Box(r, r, ft - pt - rod_bot) - E.rod3((-40, 0, zpin), (40, 0, zpin), O["STOP_PIN"] + 1)
    out.append(part("Floor piston plate with end skirts", fp, MS, group="piston", explode=(0, 0, 250)))
    out.append(part("Floor piston push rod, 60 mm square, cross-drilled", break_edges(rod, 1.0), MS, group="piston", explode=(0, 0, 250)))
    for sx in (-1, 1):
        _weld(out, "push rod to floor plate", E.bead((sx * r / 2, -r / 2, ft - pt), (0, 1, 0), r, 6, (sx, 0, 0), (0, 0, -1)), "piston")
    sp = Pos(-gap / 2 - cb - 10, 0, zpin) * cp.along(cp.round_bar(O["STOP_PIN"], gap + 2 * cb + 30, 1.0), "x")
    out.append(part("Stop pin, 30 mm 42CrMo4 +QT, with ring handle", sp + Pos(-gap / 2 - cb - 18, 0, zpin) * Rot(90, 0, 0) * (Cylinder(16, 6) - Cylinder(10, 7)),
                    "zinc_plated", kind="bought", group="piston", explode=(-300, 0, 0)))
    # eject seesaw on two posts welded to the base plate; its arm's round nose sits under the push rod's foot
    ex, ez = 170.0, 300.0
    for s in (-1, 1):
        post = Pos(ex, s * 65, (zb + ez + 30) / 2) * Box(60, 10, ez + 30 - zb) - E.ypin(ex, ez, 31.0, s * 59, s * 71, 0)
        out.append(part(f"Eject post, 10 mm plate {'left' if s < 0 else 'right'}", break_edges(post, 1.0), PS, group="eject", explode=(200, 0, 0)))
        _weld(out, "eject post to base plate", E.bead((ex - 30, s * 70, zb), (1, 0, 0), 60, 6, (0, s, 0), (0, 0, 1)), "eject")
    nose = (0.0, rod_bot - 15.0)
    import model as M
    arm = M._link((ex, ez), nose, 30, 20, 0) + M._link((ex, ez), (ex + 260 * math.cos(math.radians(40)), ez + 260 * math.sin(math.radians(40))), 72.3, 20, 0)
    hub = M._ypin(ex, ez, 60, 110)
    sock = E.rod3((ex + 40 * math.cos(math.radians(40)), 0, ez + 40 * math.sin(math.radians(40))),
                  (ex + 260 * math.cos(math.radians(40)), 0, ez + 260 * math.sin(math.radians(40))), 72.3) - \
        E.rod3((ex, 0, ez), (ex + 270 * math.cos(math.radians(40)), 0, ez + 270 * math.sin(math.radians(40))), 61.3)
    see = (hub + arm - E.ypin(ex, ez, 31.0, -60, 60, 0)) + sock
    see = see - E.rod3((ex + 30 * math.cos(math.radians(40)), 0, ez + 30 * math.sin(math.radians(40))),
                       (ex + 270 * math.cos(math.radians(40)), 0, ez + 270 * math.sin(math.radians(40))), 61.3)
    out.append(part("Eject seesaw: hub, arm and socket", see, "safety_red", group="eject", explode=(250, 0, -100)))
    out.append(part("Eject pivot pin, 30 mm", E.ypin(ex, ez, 30.0, -76, 76), "zinc_plated", kind="bought", group="eject", explode=(250, 0, -100)))
    for s in (-1, 1):
        _fx(out, "Circlip DIN 471, 30 mm, eject pin", E.circlip(ex, ez, 30.0, s * 70, s), "eject")
    # loose soil fill (context)
    out.append(part("Loose soil fill (context)", Pos(0, 0, (ft + MT - 2) / 2) * Box(BL - 4, BW - 4, MT - 2 - ft), "soil", kind="context", group="context"))
    return out, g


def option_b():
    """Power screw press: crosshead with bronze nut, two-start Tr 40 x 14 screw, capstan, thrust swivel and platen."""
    hz0 = O["HEAD_Z0"]
    cd, cb, cw, cf = O["COL_D"], O["COL_B"], O["COL_W"], O["COL_F"]
    out, g = common("B", hz0 + cd)
    ci = g["col_in"]
    gapx = 90.0
    for sx in (-1, 1):
        ch = cp.channel(cd, cb, cw, 2 * (ci - 15), tf=cf)
        beam = Pos(sx * gapx / 2, -(ci - 15), hz0 + cd / 2) * Rot(-90, 0, 0) * Rot(0, 0, 0 if sx > 0 else 180) * ch
        for sy in (-1, 1):
            beam = beam - Pos(sx * 70, sy * 45, hz0 + cd) * Cylinder(6.75, 30)
        out.append(part(f"Crosshead, UPN 80 {'-X' if sx < 0 else '+X'}", beam, PS, group="head", explode=(sx * 200, 0, 300)))
    for s in (-1, 1):
        ep = Pos(0, s * (ci - 7.5), hz0 + cd / 2) * Box(gapx + 2 * cb, 15, cd)
        for zz in (hz0 + 20, hz0 + 60):
            for xx in (0.0,):
                ep = ep - E.ypin(xx, zz, 18.0, s * (ci - 16), s * (ci + 1), 0)
        out.append(part(f"Crosshead end plate, 15 mm {'left' if s < 0 else 'right'}", break_edges(ep, 1.0), PS, group="head", explode=(0, 0, 300)))
        for zz in (hz0 + 20, hz0 + 60):
            for xx in (0.0,):
                rot = Rot(-90, 0, 0) if s > 0 else Rot(90, 0, 0)
                for nm, shp in cp.hex_bolt_set(16, cw + 15):
                    _fx(out, nm + " grade 8.8, crosshead to column", Pos(xx, s * (ci + cw), zz) * rot * shp, "head")
        for sx in (-1, 1):
            _weld(out, "crosshead to end plate", E.bead((sx * (gapx / 2 + cb), s * (ci - 15), hz0), (0, 0, 1), cd, 6, (sx, 0, 0), (0, -s, 0)), "head")
    # bronze nut between the crosshead webs, its flange on the top flanges, four M12 sets
    nt = hz0 + cd
    nut = Pos(0, 0, nt - O["NUT_L"] / 2 + 15) * Box(O["NUT_W"], O["NUT_W"], O["NUT_L"])
    nut = nut + Pos(0, 0, nt + 7.5) * Box(160, 120, 15)
    holes = [(sx * 70, sy * 45) for sx in (-1, 1) for sy in (-1, 1)]
    for x, y in holes:
        nut = nut - Pos(x, y, nt) * Cylinder(6.75, 40)
    nut = nut - Pos(0, 0, nt) * Cylinder(O["SCREW_D"] / 2, 400)
    out.append(part("Screw nut, CuSn12 bronze, Tr 40 x 14 (P7), with flange", break_edges(nut, 1.0), "brass", kind="bought", group="head", explode=(0, 0, 500)))
    for x, y in holes:
        for nm, shp in cp.hex_bolt_set(12, 15 + cf):
            _fx(out, nm + " grade 8.8, nut flange", Pos(x, y, nt + 15) * shp, "head")
    # screw, shown with the platen resting on the loose fill (start of the stroke)
    MT = g["MT"]
    plat_b = MT                                       # platen underside on the loose fill at the rim
    pt = O["PLATE_T"]
    house_h = 60.0
    s_bot = plat_b + pt + house_h - 25
    s_top = s_bot + O["SCREW_L"]
    sc_z = hz0 + cd + 15 + (O["FILL"] - O["BH"]) + 5          # stop collar: meets the nut flange at the end of the stroke
    scr = Pos(0, 0, s_bot) * cp.round_bar(O["SCREW_D"], O["SCREW_L"], 1.5)
    scr = scr - Pos(0, 0, s_top - 35) * Rot(90, 0, 0) * Cylinder(4.0, 80) - Pos(0, 0, sc_z + 15) * Rot(0, 90, 0) * Cylinder(4.0, 80)
    out.append(part("Screw, Tr 40 x 14 (P7) two-start, C45, threads drawn plain", scr, "mild_steel", kind="bought", group="screw", explode=(0, 0, 700)))
    # platen with skirts, thrust housing welded on top, thrust bearing, cap with four M8 screws
    BL, BW = O["BL"], O["BW"]
    pl = Pos(0, 0, plat_b + pt / 2) * Box(BL - 2, BW - 2, pt)
    out.append(part("Platen, 25 mm plate", break_edges(pl, 0.8), MS, group="screw", explode=(0, 0, 600)))
    hs = Pos(0, 0, plat_b + pt) * (Pos(0, 0, house_h / 2) * Cylinder(55, house_h) - Pos(0, 0, house_h / 2 + 10) * Cylinder(36, house_h))
    for a in range(4):
        hs = hs - Pos(42 * math.cos(math.radians(45 + 90 * a)), 42 * math.sin(math.radians(45 + 90 * a)), plat_b + pt + house_h - 10) * Cylinder(4.0, 22)
    out.append(part("Thrust housing, 110 mm turned tube, welded to the platen", break_edges(hs, 1.0), MS, group="screw", explode=(0, 0, 600)))
    _weld(out, "thrust housing to platen", Pos(0, 0, plat_b + pt) * extrude(Sketch() + Circle(61) - Circle(55), 5), "screw")
    bz = plat_b + pt + 10
    out.append(part("Thrust ball bearing 51208 (40 x 68 x 19), lower ring", Pos(0, 0, bz) * cp.bush(68, 40.5, 7), "stainless", kind="bought", group="screw", explode=(0, 0, 640)))
    out.append(part("Thrust ball bearing 51208, upper ring", Pos(0, 0, bz + 12) * cp.bush(68, 40.5, 7), "stainless", kind="bought", group="screw", explode=(0, 0, 660)))
    out.append(part("Thrust ball bearing 51208, ball cage", Pos(0, 0, bz + 7) * cp.bush(60, 48, 5), "brass", kind="bought", group="screw", explode=(0, 0, 650)))
    cap = Pos(0, 0, plat_b + pt + house_h) * (Pos(0, 0, 6) * Cylinder(55, 12) - Pos(0, 0, 6) * Cylinder(21, 14))
    for a in range(4):
        cap = cap - Pos(42 * math.cos(math.radians(45 + 90 * a)), 42 * math.sin(math.radians(45 + 90 * a)), plat_b + pt + house_h + 6) * Cylinder(4.5, 14)
    out.append(part("Swivel retaining cap, 12 mm", break_edges(cap, 0.8), MS, group="screw", explode=(0, 0, 720)))
    for a in range(4):
        x, y = 42 * math.cos(math.radians(45 + 90 * a)), 42 * math.sin(math.radians(45 + 90 * a))
        _fx(out, "M8x20 hex bolt (ISO 4017), swivel cap", Pos(x, y, plat_b + pt + house_h + 12) * cp.hex_bolt(8, 20), "screw")
    # stop collar on the screw: meets the nut at the end of the stroke (block height 90 mm)
    col_ = Pos(0, 0, sc_z) * (Pos(0, 0, 15) * Cylinder(35, 30) - Pos(0, 0, 15) * Cylinder(20, 32)) - Pos(0, 0, sc_z + 15) * Rot(0, 90, 0) * Cylinder(4.25, 80)
    out.append(part("Stop collar, 70 mm, cross-pinned to the screw", break_edges(col_, 0.8), MS, group="screw", explode=(0, 0, 760)))
    _fx(out, "Spring pin ISO 8752, 8 x 70, stop collar", Pos(-35, 0, sc_z + 15) * Rot(0, 90, 0) * Pos(0, 0, 35) * cp.round_bar(8, 70, 0.5), "screw")
    # capstan hub and bar with grips
    hub = Pos(0, 0, s_top - 60) * (Pos(0, 0, 55) * Cylinder(40, 110) - Pos(0, 0, 30) * Cylinder(20, 60.01))
    hub = hub - Pos(0, 0, s_top - 35) * Rot(90, 0, 0) * Cylinder(4.25, 90) - Pos(0, 0, s_top + 25) * Rot(0, 90, 0) * Cylinder(16.5, 90)
    out.append(part("Capstan hub, 80 mm, cross-bored", break_edges(hub, 1.0), PS, group="screw", explode=(0, 0, 800)))
    out.append(part("Capstan bar, 32 mm round, 1.2 m", Pos(-O["CAP_BAR"] / 2, 0, s_top + 25) * cp.along(cp.round_bar(O["CAP_D"], O["CAP_BAR"], 1.5), "x"),
                    PS, group="screw", explode=(0, 0, 850)))
    for sx in (-1, 1):
        x0 = O["CAP_BAR"] / 2 - 130 if sx > 0 else -O["CAP_BAR"] / 2 + 10     # grips 120 mm long, 10 mm in from each end
        g_ = Pos(x0, 0, s_top + 25) * cp.along(cp.bush(40, 32, 120), "x")
        out.append(part(f"Rubber grip, capstan {'-X' if sx < 0 else '+X'}", g_, "epdm", kind="bought", group="screw", explode=(0, 0, 850)))
    _fx(out, "Spring pin ISO 8752, 8 x 80, capstan hub", Pos(0, -40, s_top - 35) * Rot(-90, 0, 0) * cp.round_bar(8, 80, 0.5), "screw")
    return out


def option_c():
    """Rope-lifted drop rammer: light crosshead with a guide sleeve, plunger on a guide rod, stop and anvil collars,
    a 20 kg sleeve weight, a head pulley on the rod top and a rope with a T-handle."""
    hz0 = O["C_HEAD_Z0"]
    cd, cb, cw, cf = O["COL_D"], O["COL_B"], O["COL_W"], O["COL_F"]
    out, g = common("C", hz0 + 50)
    ci = g["col_in"]
    for sx in (-1, 1):
        t = Pos(sx * 55, -(ci - 15), hz0 + 25) * cp.along(cp.shs(50, 3, 2 * (ci - 15)), "y")
        out.append(part(f"Crosshead, 50 x 50 x 3 SHS {'-X' if sx < 0 else '+X'}", t, PS, group="head", explode=(sx * 200, 0, 300)))
    for s in (-1, 1):
        ep = Pos(0, s * (ci - 7.5), hz0 + 25) * Box(170, 15, 50)
        for xx in (-55, 55):
            ep = ep - E.ypin(xx, hz0 + 25, 13.5, s * (ci - 16), s * (ci + 1), 0)
        out.append(part(f"Crosshead end plate, 15 mm {'left' if s < 0 else 'right'}", break_edges(ep, 1.0), PS, group="head", explode=(0, 0, 300)))
        for xx in (-55, 55):
            rot = Rot(-90, 0, 0) if s > 0 else Rot(90, 0, 0)
            for nm, shp in cp.hex_bolt_set(12, cw + 15):
                _fx(out, nm + " grade 8.8, crosshead to column", Pos(xx, s * (ci + cw), hz0 + 25) * rot * shp, "head")
    # guide sleeve between the crosshead tubes on two 10 mm plates
    gs = Pos(0, 0, hz0 - 60) * extrude(Sketch() + Circle(30) - Circle(O["GUIDE_ROD"] / 2 + 0.5), 200)
    out.append(part("Guide sleeve, 60 x 9.5 tube, 200 mm, bored", break_edges(gs, 0.5), MS, group="head", explode=(0, 0, 350)))
    for sy in (-1, 1):
        gp = Pos(0, sy * 35, hz0 + 25) * Box(60, 10, 50)
        out.append(part(f"Guide sleeve plate, 10 mm {'left' if sy < 0 else 'right'}", break_edges(gp, 1.0), PS, group="head", explode=(0, 0, 330)))
        _weld(out, "guide plate to crosshead", E.bead((-30, sy * 40, hz0 + 50), (1, 0, 0), 60, 5, (0, sy, 0), (0, 0, 1)), "head")
    # plunger resting on the loose fill, rod, collars, weight, pulley and rope
    MT = g["MT"]; pt = O["PLATE_T"]; BL, BW = O["BL"], O["BW"]
    pl_b = MT
    out.append(part("Plunger, 25 mm plate", break_edges(Pos(0, 0, pl_b + pt / 2) * Box(BL - 2, BW - 2, pt), 0.8), MS, group="ram", explode=(0, 0, 500)))
    rod_top = pl_b + pt + 1250.0
    rd = O["GUIDE_ROD"]
    gs_top = hz0 + 140
    stop_z = gs_top + (O["FILL"] - O["BH"])         # stop collar meets the sleeve when the block is 90 mm high
    grod = Pos(0, 0, pl_b + pt) * cp.round_bar(rd, rod_top - pl_b - pt, 1.0)
    for z_ in (stop_z + 15, stop_z + 50):
        grod = grod - Pos(0, 0, z_) * Rot(0, 90, 0) * Cylinder(4.0, 120)
    out.append(part("Guide rod, 40 mm C45, 1.25 m", grod, "mild_steel", kind="bought", group="ram", explode=(0, 0, 500)))
    _weld(out, "guide rod to plunger", Pos(0, 0, pl_b + pt) * extrude(Sketch() + Circle(rd / 2 + 6) - Circle(rd / 2), 6), "ram")
    for nm, z0, h, od in (("Stop collar, 80 mm, height stop", stop_z, 30.0, 80.0), ("Anvil collar, 100 mm", stop_z + 30.0, 40.0, 100.0)):
        c_ = Pos(0, 0, z0) * (Pos(0, 0, h / 2) * Cylinder(od / 2, h) - Pos(0, 0, h / 2) * Cylinder(rd / 2, h + 2))
        c_ = c_ - Pos(0, 0, z0 + h / 2) * Rot(0, 90, 0) * Cylinder(4.25, od + 4)
        out.append(part(nm, break_edges(c_, 1.0), MS, group="ram", explode=(0, 0, 550)))
        _fx(out, f"Spring pin ISO 8752, 8 x {od:.0f}, {nm.split(',')[0].lower()}", Pos(-od / 2, 0, z0 + h / 2) * Rot(0, 90, 0) * Pos(0, 0, od / 2) * cp.round_bar(8, od, 0.5), "ram")
    wz = stop_z + 70.0
    wt = Pos(0, 0, wz) * (Pos(0, 0, O["WEIGHT_L"] / 2) * Cylinder(O["WEIGHT_OD"] / 2, O["WEIGHT_L"]) - Pos(0, 0, O["WEIGHT_L"] / 2) * Cylinder(rd / 2 + 1, O["WEIGHT_L"] + 2))
    wt = wt + Pos(-49.0, 0, wz + O["WEIGHT_L"]) * (Pos(0, 0, 12) * Box(20, 60, 24) - Pos(0, 0, 12) * Rot(90, 0, 0) * Cylinder(8, 62))
    wt = wt - Pos(0, 0, wz + O["WEIGHT_L"] / 2) * Cylinder(rd / 2 + 1, O["WEIGHT_L"] + 60)
    out.append(part("Drop weight, 20 kg turned sleeve with rope eye", break_edges(wt, 1.5), "painted_steel", group="ram", explode=(0, 0, 650)))
    # head pulley on a fork at the rod top
    pz = rod_top + 87
    fork = Pos(0, 0, rod_top) * (Pos(0, 0, 15) * Cylinder(30, 30) - Pos(0, 0, 10) * Cylinder(rd / 2, 21))
    for sy in (-1, 1):
        fork = fork + Pos(0, sy * 22, rod_top + 30 + 45) * Box(50, 8, 90)
    fork = fork - E.ypin(0, pz, 16.5, -40, 40, 0)
    out.append(part("Pulley fork, welded, on the rod top", break_edges(fork, 0.8), PS, group="ram", explode=(0, 0, 750)))
    pul = Pos(0, 0, 0) * cp.pulley(100, 30, 16.5)
    out.append(part("Head pulley, 100 mm, 10 mm rope", Pos(0, 0, pz) * Rot(90, 0, 0) * pul, "cast_aluminium", kind="bought", group="ram", explode=(0, 0, 780)))
    out.append(part("Pulley axle, 16 mm", E.ypin(0, pz, 16.0, -32, 32), "zinc_plated", kind="bought", group="ram", explode=(0, 0, 780)))
    for s in (-1, 1):
        _fx(out, "Circlip DIN 471, 16 mm, pulley axle", E.circlip(0, pz, 16.0, s * 26, s), "ram")
    eye_z = wz + O["WEIGHT_L"] + 12
    rr = 49.0                                            # rope centre line in the pulley groove (groove floor at 42.5)
    arc = [(-rr * math.cos(math.radians(a)), 0, pz + rr * math.sin(math.radians(a))) for a in range(0, 181, 10)]
    pts = [(-rr, 0, eye_z + 18)] + arc + [(560, 0, 1060)]
    out.append(part("Rope, 10 mm polyester", cp.rope(pts, 10), "rope", kind="bought", group="ram", explode=(0, 0, 0)))
    th = Pos(560, -200, 1040) * cp.along(cp.round_bar(30, 400, 2), "y")
    out.append(part("Rope T-handle, 30 mm hardwood, 400 mm", th, "hardwood", kind="bought", group="ram", explode=(0, 0, 0)))
    return out


def build(option):
    return {"B": option_b, "C": option_c}[option]()
