"""Parts library for detailed CAD at every TRL (kit 1.9, STANDARDS section 24).

Real stock sections, ISO and DIN fasteners, weld beads, pins, hinges and other common hardware as
build123d solids, so a model reaches detail level D1, D2 or D3 without hand-modelling each part.
Every function returns a build123d solid in millimetres, built along +Z from the origin unless its
docstring says otherwise. Place parts with `at()`.

    import sys; sys.path.insert(0, ".kit")
    from cad_parts import part, rhs, angle, hex_bolt_set, weld_fillet, at, MATERIALS

    leg = part("Frame leg", at(shs(40, 3, 900), (0, 0, 0)), "painted_steel", kind="made", bom=3)

`part()` returns the dict that `cad_check.py`, `product_export.py`, `export_views.py` and `photoreal.py` read:
name, shape, material, color, kind (made, bought, fastener, weld, context), bom, group and explode.

Dimensions of fasteners follow ISO 4017 (hex bolts), ISO 4032 (hex nuts), ISO 7089 (plain washers) and
ISO 2341 (clevis pins) for the nominal sizes listed; threads are drawn as plain shanks, as is usual in
assembly CAD. Steel sections follow the common nominal sizes of EN 10219 (hollow sections) and EN 10056
(angles); corner radii are the typical values, not tolerances.
"""
from __future__ import annotations

import math
from build123d import (Axis, Box, Cylinder, Location, Pos, Rot, Solid, Compound, RegularPolygon, Polyline,
                       Rectangle, RectangleRounded, Circle, Plane, extrude, fillet, chamfer, Sketch, Mode, Polygon)

# ---------------------------------------------------------------------------------------------------------
# Materials: name -> (colour, render class used by photoreal.py, density kg/m3)
# ---------------------------------------------------------------------------------------------------------
MATERIALS = {
    "painted_steel":   ("#2F5D50", "painted", 7850),
    "galvanised":      ("#A7ADB2", "galvanised", 7850),
    "mild_steel":      ("#5B6066", "metal", 7850),
    "stainless":       ("#C9CDD1", "stainless", 7950),
    "aluminium":       ("#C4C8CC", "aluminium", 2700),
    "cast_aluminium":  ("#B7BBBF", "cast_metal", 2700),
    "zinc_plated":     ("#BFC4C8", "metal", 7850),
    "hdpe_black":      ("#1E2124", "hdpe", 950),
    "hdpe_natural":    ("#D9D6CC", "hdpe", 950),
    "hdpe_recycled":   ("#2B4A43", "hdpe", 950),
    "polycarbonate":   ("#DDE6EA", "clear", 1200),
    "epdm":            ("#151617", "rubber", 1150),
    "rubber_belt":     ("#202224", "rubber", 1300),
    "timber":          ("#A9784A", "wood", 600),
    "plywood":         ("#C9A46E", "plywood", 600),
    "hardwood":        ("#7A4B2A", "wood", 800),
    "bamboo":          ("#B9A25A", "bamboo", 700),
    "coir":            ("#8A5A2B", "coir", 120),
    "coir_net":        ("#7B5530", "rope", 500),
    "rope":            ("#C8B88A", "rope", 1100),
    "concrete":        ("#9A9893", "concrete", 2400),
    "mirror":          ("#E8EAEC", "mirror", 2700),
    "insulated_white": ("#F2F2EE", "painted_white", 120),
    "pe_tank_white":   ("#EDEDE8", "plastic_tank", 950),
    "pe_tank_silver":  ("#BFC3C6", "silver_paint", 950),
    "matte_black":     ("#141414", "matte_black", 950),
    "canvas":          ("#B8AD8F", "fabric", 500),
    "brass":           ("#B58B3A", "metal", 8500),
    "glass":           ("#E6EEF0", "clear", 2500),
    "water":           ("#3E5A5A", "water", 1000),
    "mud":             ("#4A3C2E", "mud", 1600),
    "sand":            ("#C8B48A", "sand", 1600),
    "soil":            ("#5A4632", "soil", 1500),
    "grass":           ("#55703A", "grass", 600),
    "safety_yellow":   ("#E3B21C", "painted", 7850),
    "safety_red":      ("#B3261E", "painted", 7850),
    "label":           ("#F4F1E6", "paper", 900),
    "skin":            ("#9C9C9E", "clay", 1000),
}
KINDS = ("made", "bought", "fastener", "weld", "context")


def part(name, shape, material, kind="made", bom=None, group="shell", explode=(0, 0, 0), color=None, note=""):
    """A named part for models, renders and the fidelity check. kind: made, bought, fastener, weld or context."""
    if material not in MATERIALS:
        raise ValueError(f"{name}: material '{material}' is not in cad_parts.MATERIALS")
    if kind not in KINDS:
        raise ValueError(f"{name}: kind must be one of {KINDS}")
    col, cls, _ = MATERIALS[material]
    return dict(name=name, shape=shape, material=cls, material_name=material, color=color or col, kind=kind,
                bom=bom, group=group, explode=explode, note=note)


def mass_kg(p):
    """Mass of a part dict from its volume and material density."""
    return p["shape"].volume * 1e-9 * MATERIALS[p["material_name"]][2]


# ---------------------------------------------------------------------------------------------------------
# Placement and edges
# ---------------------------------------------------------------------------------------------------------
def at(shape, xyz=(0, 0, 0), rot=(0, 0, 0)):
    """Rotate (degrees about X, then Y, then Z) and then move a shape."""
    return Pos(*xyz) * Rot(*rot) * shape


def along(shape, axis):
    """Turn a part built along +Z to lie along 'x' or 'y' (or leave it on 'z')."""
    return {"x": Rot(0, 90, 0), "y": Rot(-90, 0, 0), "z": Rot(0, 0, 0)}[axis] * shape


def break_edges(shape, r=1.0):
    """Round (or, failing that, chamfer) every edge by r mm, as a real cut, sawn or moulded part has.
    Returns the shape unchanged if neither works (very thin or complex parts)."""
    for op in (fillet, chamfer):
        try:
            out = op(shape.edges(), r)
            ok = out.is_valid() if callable(out.is_valid) else out.is_valid
            if ok:
                return out
        except Exception:
            pass
    return shape


def _prism(profile, length):
    return extrude(profile, length)


# ---------------------------------------------------------------------------------------------------------
# Stock: steel sections, bar, tube, sheet (all along +Z, profile centred on the Z axis)
# ---------------------------------------------------------------------------------------------------------
def rhs(w, h, t, length):
    """Rectangular hollow section w x h x t (EN 10219), outer corner radius 2t, inner t."""
    outer = RectangleRounded(w, h, min(2 * t, min(w, h) / 2 - 0.01))
    inner = RectangleRounded(w - 2 * t, h - 2 * t, max(t, 0.1))
    return extrude(Sketch() + outer - inner, length)


def shs(a, t, length):
    """Square hollow section a x a x t (EN 10219)."""
    return rhs(a, a, t, length)


def round_tube(od, t, length):
    """Circular hollow section or pipe, outside diameter od, wall t."""
    return extrude(Sketch() + Circle(od / 2) - Circle(od / 2 - t), length)


def round_bar(d, length, chamfer_ends=0.5):
    """Round bar or rod along +Z with chamfered ends."""
    s = Pos(0, 0, length / 2) * Cylinder(d / 2, length)
    return break_edges(s, chamfer_ends) if chamfer_ends else s


def flat_bar(w, t, length, r=0.8):
    """Flat bar w x t with lightly rounded long edges."""
    return extrude(RectangleRounded(w, t, min(r, t / 2 - 0.01)), length)


def angle(a, b, t, length):
    """Equal or unequal angle (EN 10056): legs a (along X) and b (along Y) from the heel at the origin."""
    pts = [(0, 0), (a, 0), (a, t), (t, t), (t, b), (0, b)]
    s = extrude(Polygon(*pts, align=None), length)
    try:
        inner = s.edges().filter_by(Axis.Z).sort_by_distance((t, t, 0))[0]
        s = fillet([inner], t * 0.9)
    except Exception:
        pass
    return s


def channel(h, b, t, length, tf=None):
    """Parallel-flange channel h (web, along Y) x b (flanges, along +X) with web t and flange tf."""
    tf = tf or t * 1.4
    pts = [(0, -h / 2), (b, -h / 2), (b, -h / 2 + tf), (t, -h / 2 + tf), (t, h / 2 - tf), (b, h / 2 - tf), (b, h / 2), (0, h / 2)]
    return extrude(Polygon(*pts, align=None), length)


def sheet(w, h, t, holes=(), r_corner=3.0, edge=0.4):
    """Flat sheet or plate w (X) x h (Y) x t (Z, from 0), with rounded corners and holes [(x, y, d), ...]
    measured from the plate centre."""
    sk = Sketch() + RectangleRounded(w, h, min(r_corner, min(w, h) / 2 - 0.01))
    for x, y, d in holes:
        sk -= Pos(x, y) * Circle(d / 2)
    s = extrude(sk, t)
    return break_edges(s, min(edge, t / 3)) if edge else s


def bent_channel_sheet(w, flange, t, length, r_in=None):
    """A sheet folded into a U (press-brake section): web w along X, two flanges of height 'flange' up +Y."""
    r_in = r_in or t
    sk = Sketch() + Polygon((-w / 2, 0), (w / 2, 0), (w / 2, flange), (w / 2 - t, flange), (w / 2 - t, t),
                            (-w / 2 + t, t), (-w / 2 + t, flange), (-w / 2, flange), align=None)
    s = extrude(sk, length)
    try:
        s = fillet(s.edges().filter_by(Axis.Z).group_by(Axis.Y)[0], r_in + t)
    except Exception:
        pass
    return s


def mesh_panel(w, h, pitch, wire_d, frame=None):
    """Welded wire mesh panel w (X) x h (Z) in the XZ plane, wires at 'pitch', optional flat-bar frame width."""
    rods = []
    nx, nz = int(w // pitch), int(h // pitch)
    for i in range(nx + 1):
        rods.append(Pos(-w / 2 + i * w / nx, 0, h / 2) * Cylinder(wire_d / 2, h))
    for j in range(nz + 1):
        rods.append(Pos(0, wire_d, j * h / nz) * Rot(0, 90, 0) * Cylinder(wire_d / 2, w))
    out = Compound(rods)
    if frame:
        fr = [Pos(0, 0, -frame / 2) * Box(w + frame, 3, frame), Pos(0, 0, h + frame / 2) * Box(w + frame, 3, frame),
              Pos(-w / 2 - frame / 2, 0, h / 2) * Box(frame, 3, h), Pos(w / 2 + frame / 2, 0, h / 2) * Box(frame, 3, h)]
        out = Compound(rods + fr)
    return out


# ---------------------------------------------------------------------------------------------------------
# Fasteners (ISO), drawn along +Z: head on the XY plane at z = 0, shank down -Z
# ---------------------------------------------------------------------------------------------------------
# nominal d: (s across flats, k head height, m nut height, washer d2, washer h, pitch)
ISO = {
    5: (8, 3.5, 4.7, 10, 1.0, 0.8), 6: (10, 4.0, 5.2, 12, 1.6, 1.0), 8: (13, 5.3, 6.8, 16, 1.6, 1.25),
    10: (16, 6.4, 8.4, 20, 2.0, 1.5), 12: (18, 7.5, 10.8, 24, 2.5, 1.75), 16: (24, 10.0, 14.8, 30, 3.0, 2.0),
    20: (30, 12.5, 18.0, 37, 3.0, 2.5), 24: (36, 15.0, 21.5, 44, 4.0, 3.0),
}


def _hex(s, h):
    prism = extrude(RegularPolygon(s / math.sqrt(3), 6), h)
    try:   # the 30 degree chamfer on hex heads and nuts: intersect with a cone-like chamfered cylinder
        cap = Pos(0, 0, h / 2) * Cylinder(s / math.sqrt(3), h)
        cap = chamfer(cap.edges(), s / math.sqrt(3) - s / 2 * 0.95)
        return prism & cap
    except Exception:
        return prism


def hex_bolt(d, length):
    """ISO 4017 hex head screw Md x length; head on top (z 0 to k), shank from z 0 down to -length."""
    s, k = ISO[d][0], ISO[d][1]
    head = _hex(s, k)
    shank = Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
    try:
        shank = chamfer(shank.edges().sort_by(Axis.Z)[0], d * 0.08)
    except Exception:
        pass
    return head + shank


def hex_nut(d):
    """ISO 4032 hex nut, from z 0 to m, with a clearance bore."""
    s, m = ISO[d][0], ISO[d][2]
    return _hex(s, m) - Pos(0, 0, m / 2) * Cylinder(d / 2, m)


def washer(d):
    """ISO 7089 plain washer, from z 0 to h."""
    d2, h = ISO[d][3], ISO[d][4]
    return extrude(Sketch() + Circle(d2 / 2) - Circle(d * 0.54), h)


def hex_bolt_set(d, grip, extra=None):
    """Bolt, two washers and nut clamping a joint 'grip' mm thick. The joint's top face is at z = 0 and its
    bottom face at z = -grip. Returns a list of (name, shape) for part(); the bolt length is rounded up
    to the next 5 mm so the thread shows 2 to 3 pitches beyond the nut."""
    s, k, m, d2, h, p = ISO[d]
    L = math.ceil((grip + 2 * h + m + (extra if extra is not None else 2.5 * p)) / 5) * 5
    return [
        (f"M{d}x{L} hex bolt (ISO 4017)", Pos(0, 0, h) * hex_bolt(d, L)),
        (f"M{d} washer (ISO 7089)", washer(d)),
        (f"M{d} washer (ISO 7089)", Pos(0, 0, -grip - h) * washer(d)),
        (f"M{d} hex nut (ISO 4032)", Pos(0, 0, -grip - h - m) * hex_nut(d)),
    ]


def coach_screw(d, length):
    """Hex head coach screw for timber (DIN 571), head on top, tapered tip."""
    s, k = ISO[d][0], ISO[d][1]
    shank = Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
    try:
        shank = chamfer(shank.edges().sort_by(Axis.Z)[0], d * 0.4)
    except Exception:
        pass
    return _hex(s, k) + shank


def anchor_bolt(d, embed):
    """Through-bolt concrete anchor (stud, washer, nut), concrete face at z = 0, embedded to -embed."""
    s, k, m, d2, h, p = ISO[d]
    stud = Pos(0, 0, (m + h + 2 * p - embed) / 2) * Cylinder(d / 2, embed + m + h + 2 * p)
    return stud + washer(d) + Pos(0, 0, h) * hex_nut(d)


def clevis_pin(d, grip):
    """ISO 2341 type B clevis pin with head and split-pin hole; head at z 0, pin down to -(grip + 2d)."""
    L = grip + 2 * d
    head = Pos(0, 0, d * 0.35) * Cylinder(d * 0.8, d * 0.7)
    pin = Pos(0, 0, -L / 2) * Cylinder(d / 2, L)
    hole = Pos(0, 0, -grip - d) * Rot(0, 90, 0) * Cylinder(d * 0.16, d * 2)
    out = head + pin - hole
    try:
        out = break_edges(out, d * 0.06)
    except Exception:
        pass
    return out


def split_pin(d_pin):
    """ISO 1234 split pin to suit a clevis pin of diameter d_pin, lying along X through the origin."""
    dp = d_pin * 0.32
    return Rot(0, 90, 0) * (Cylinder(dp / 2, d_pin * 1.6) + Pos(0, 0, d_pin * 0.8) * Cylinder(dp * 0.9, dp))


# ---------------------------------------------------------------------------------------------------------
# Joints and hardware
# ---------------------------------------------------------------------------------------------------------
def weld_fillet(length, leg):
    """Fillet weld bead along +X from 0 to length, legs along +Y and +Z (place it in the joint corner),
    drawn as a slightly convex bead so it reads as a weld."""
    tri = Polygon((0, 0), (leg, 0), (0, leg), align=None)
    bead = extrude(tri, length)                     # along +Z
    bead = Rot(0, 90, 0) * bead                     # now along +X, profile in the YZ plane
    bead = Rot(90, 0, 0) * bead
    # re-orient so the legs lie along +Y and +Z
    bead = Pos(0, 0, 0) * bead
    try:
        bead = fillet(bead.edges().filter_by(Axis.X), leg * 0.15)
    except Exception:
        pass
    return bead


def butt_hinge(length, leaf_w, t, pin_d, open_deg=180):
    """Butt hinge along Z with its knuckle on the Z axis; leaf 1 along +X, leaf 2 at open_deg about Z."""
    knuckle = Pos(0, 0, length / 2) * Cylinder(pin_d / 2 + t, length)
    leaf = Pos(leaf_w / 2 + pin_d / 2, 0, length / 2) * Box(leaf_w, t, length)
    l2 = Rot(0, 0, open_deg) * leaf
    pin = Pos(0, 0, length / 2) * Cylinder(pin_d / 2, length + 2 * t)
    return break_edges(knuckle + leaf + l2, min(0.5, t / 3)), pin


def bush(od, id_, length):
    """Plain bush (sleeve bearing) along +Z."""
    return break_edges(extrude(Sketch() + Circle(od / 2) - Circle(id_ / 2), length), 0.3)


def pulley(d, w, bore):
    """Grooved pulley (sheave) along +Z centred on z = 0: rim diameter d, width w, V groove."""
    body = Pos(0, 0, 0) * Cylinder(d / 2, w)
    groove = Cylinder(d / 2 + 1, w * 0.45)
    try:
        groove = chamfer(groove.edges(), w * 0.2)
    except Exception:
        pass
    ring = Cylinder(d / 2 + 2, w * 0.45) - Cylinder(d / 2 - w * 0.25, w * 0.45)
    return body - ring - Cylinder(bore / 2, w * 2)


def drum_200l(closed=True):
    """200 L steel drum (ISO 15750 class): 585 mm diameter, 880 mm tall, two rolling hoops, along +Z."""
    r, h = 292.5, 880
    shell = Pos(0, 0, h / 2) * Cylinder(r, h)
    hoops = [Pos(0, 0, z) * (Cylinder(r + 6, 14) - Cylinder(r - 1, 14)) for z in (h / 3, 2 * h / 3)]
    chime = [Pos(0, 0, z) * (Cylinder(r + 4, 10) - Cylinder(r - 6, 10)) for z in (5, h - 5)]
    bung = Pos(r * 0.6, 0, h + 4) * Cylinder(28, 8)
    return Compound([shell] + hoops + chime + [bung])


def rope(points, d):
    """A rope through points [(x, y, z), ...], drawn as round segments with spherical joints."""
    from build123d import Sphere
    segs = []
    for a, b in zip(points, points[1:]):
        ax, ay, az = a; bx, by, bz = b
        L = math.dist(a, b)
        if L < 1e-6:
            continue
        mid = ((ax + bx) / 2, (ay + by) / 2, (az + bz) / 2)
        dx, dy, dz = (bx - ax) / L, (by - ay) / L, (bz - az) / L
        ry = math.degrees(math.atan2(math.hypot(dx, dy), dz))
        rz = math.degrees(math.atan2(dy, dx))
        segs.append(Pos(*mid) * Rot(0, 0, rz) * Rot(0, ry, 0) * Cylinder(d / 2, L))
        segs.append(Pos(*b) * Sphere(d / 2))
    return Compound(segs)


def handwheel(d, rim_d=20, spokes=3, hub_d=40, hub_h=40):
    """Hand wheel in the XY plane centred at the origin, hub along +Z."""
    from build123d import Torus
    rim = Torus(d / 2 - rim_d / 2, rim_d / 2)
    hub = Pos(0, 0, hub_h / 2 - rim_d / 2) * Cylinder(hub_d / 2, hub_h)
    sp = [Rot(0, 0, i * 360 / spokes) * Pos(d / 4, 0, 0) * Rot(0, 90, 0) * Cylinder(rim_d * 0.3, d / 2 - rim_d / 2) for i in range(spokes)]
    return Compound([rim, hub] + sp)


def lever_handle(length, d=30, grip_len=120):
    """Tube lever along +X with a rubber grip at the free end (returns tube, grip)."""
    tube = Pos(length / 2, 0, 0) * Rot(0, 90, 0) * Cylinder(d / 2, length)
    grip = Pos(length - grip_len / 2, 0, 0) * Rot(0, 90, 0) * Cylinder(d / 2 + 3, grip_len)
    return tube, break_edges(grip, 2)


def label_plate(w, h, t=0.8):
    """A small nameplate or warning label, in the XZ plane, facing -Y."""
    return Pos(0, -t / 2, 0) * Box(w, t, h)


def ballast_bar(w, h, length):
    """Cast concrete or steel ballast bar along +X with chamfered edges."""
    return break_edges(Pos(length / 2, 0, h / 2) * Box(length, w, h), min(w, h) * 0.08)
