"""EarthPress repo-specific CAD helpers beside .kit/cad_parts.py (kit 1.9, STANDARDS section 24).

    bead()        a convex fillet weld bead along any direction, its legs on any two faces
    ypin()        a turned pin along Y with chamfered ends, an optional cross-drilled grease hole
    ybush()       a plain bush along Y (cad_parts.bush placed and turned)
    circlip()     a DIN 471 external retaining ring drawn as a ring with its lug ears, on a pin along Y
    nipple()      a grease nipple (M6 straight) on any axis, its shank in a drilled hole
    ytube(), yrod(), rod3()   tube and bar between points
    solids()      the separate solids of a fused shape, for one part per piece of stock

All sizes in millimetres. These are candidates for a later kit release; see docs/REVIEW.md.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import (Face, Wire, Vector, Plane, Location, Pos, Rot, Solid, Cylinder, Box,  # noqa: E402
                       extrude, Sketch, Circle, Rectangle)
import cad_parts as cp  # noqa: E402


def _v(t):
    return Vector(*t)


def bead(start, direction, length, leg, n1, n2):
    """Fillet weld bead from `start` along `direction` for `length`, legs of `leg` along the unit vectors n1 and
    n2 (the two faces it joins), drawn slightly convex so it reads as a weld."""
    c, d, a, b = _v(start), _v(direction).normalized(), _v(n1).normalized(), _v(n2).normalized()
    pts = [c, c + a * leg, c + a * (0.6 * leg) + b * (0.6 * leg), c + b * leg]
    f = Face(Wire.make_polygon(pts, close=True))
    return extrude(f, amount=length, dir=d)


def ypin(x, z, d, y0, y1, chamfer=1.0):
    """Turned pin of diameter d along Y from y0 to y1, chamfered ends."""
    y0, y1 = sorted((y0, y1))
    return Pos(x, y0, z) * cp.along(cp.round_bar(d, y1 - y0, chamfer), "y")


def ybush(x, z, od, id_, y0, y1):
    y0, y1 = sorted((y0, y1))
    return Pos(x, y0, z) * cp.along(cp.bush(od, id_, y1 - y0), "y")


def ytube(x, z, od, id_, y0, y1):
    y0, y1 = sorted((y0, y1))
    s = extrude(Sketch() + Circle(od / 2) - Circle(id_ / 2), y1 - y0)
    return Pos(x, y0, z) * cp.along(cp.break_edges(s, 0.3), "y")


def circlip(x, z, d, y, side=1, t=1.75):
    """DIN 471 external ring on a pin of diameter d along Y: a ring from the pin surface out about d/8 + 3 mm,
    t thick, starting at y and growing toward +Y (side 1) or -Y (side -1), with two lug ears and the gap."""
    ro = d / 2 + max(3.0, d * 0.12)
    ring = Sketch() + Circle(ro) - Circle(d / 2)
    ring += Pos(ro, 4.0) * Circle(2.8) + Pos(ro, -4.0) * Circle(2.8)        # lug ears, clear of the pin
    ring -= Pos(d / 2 + 2.5, 0) * Rectangle(8.0, 2.4)
    ring -= Pos(ro, 4.0) * Circle(1.0) + Pos(ro, -4.0) * Circle(1.0)
    s = extrude(ring, t)
    s = cp.along(s, "y")
    y0 = y if side > 0 else y - t
    return Pos(x, y0, z) * s


def nipple(origin, axis):
    """Straight M6 grease nipple: 7 mm hex body and ball head outside the face at `origin`, an M6 shank 6 mm
    into the part (the caller drills the hole). `axis` points out of the face."""
    a = _v(axis).normalized()
    hexb = cp._hex(7.0, 5.0)
    neck = Pos(0, 0, 6.5) * Cylinder(2.2, 3.0)
    head = Pos(0, 0, 9.5) * Cylinder(3.0, 3.0)
    shank = Pos(0, 0, -3.0) * Cylinder(3.0, 6.0)
    body = hexb + neck + head + shank
    pl = Plane(origin=_v(origin), z_dir=a)
    return Location(pl) * body


def nipple_hole(origin, axis, depth=6.0):
    a = _v(axis).normalized()
    pl = Plane(origin=_v(origin) - a * depth, z_dir=a)
    return Location(pl) * Pos(0, 0, depth / 2) * Cylinder(3.0, depth)


def rod3(a, b, d):
    a, b = _v(a), _v(b)
    v = b - a
    return Solid.make_cylinder(d / 2, v.length, Plane(origin=a, z_dir=v.normalized()))


def solids(shape):
    """The separate solids of a shape (a fused pair of mirrored plates becomes two parts)."""
    try:
        s = [Solid(x.wrapped) for x in shape.solids()]      # detached, so a later fillet acts on this solid only
        return s if s else [shape]
    except Exception:
        return [shape]
