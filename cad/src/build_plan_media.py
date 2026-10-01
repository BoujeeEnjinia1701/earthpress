"""EarthPress prototype build plan pictures (EPR-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...] [only=NNN]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/EPR-DWG-101 to 115        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import (PARAMS as P, build_components, derived, geometry, theta_start, toggle_state,  # noqa: E402
                   knee_and_crank, ASSEMBLY_THETA, _box)

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived()
G = geometry()
C = build_components()


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


S = lambda *ks: _fuse([C[k].shape for k in ks])  # noqa: E731

COL = {"base": "#4B5563", "core": "#6B7280", "mold": "#0F766E", "lid": "#115E59", "piston": "#D4A017",
       "lower": "#C2410C", "upper": "#EA580C", "pin": "#9CA3AF", "spacer": "#374151", "conlink": "#B45309",
       "hub": "#1F2937", "lever": "#111827", "eject": "#7C3AED", "pawl": "#9333EA", "guard": "#94A3B8",
       "bolt": "#111827", "kit": "#2563EB", "sieve": "#A16207", "gauge": "#16A34A", "rest": "#111827"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def made():
    return {
        "base": part("Base frame", S("skids", "cross", "base_plate", "bracket", "rest", "ties", "posts"), COL["base"]),
        "core": part("Press core", S("columns", "feet", "beam", "lugs"), COL["core"]),
        "mold": part("Mold box", S("mold", "flanges", "mold_lugs"), COL["mold"]),
        "piston": part("Piston and push rod", C["piston"].shape, COL["piston"]),
        "lower": part("Lower links (2), base pin, spacers", S("lower_links", "base_pin", "base_spacers"), COL["lower"]),
        "upper": part("Upper links (2), knee pin, spacers", S("upper_links", "knee_pin", "knee_spacers"), COL["upper"]),
        "conlink": part("Connecting link", C["conlink"].shape, COL["conlink"]),
        "upin": part("Upper pin", C["upper_pin"].shape, COL["pin"]),
        "hub": part("Lever hub, shaft, crank pin", S("hub", "shaft", "crank_pin"), COL["hub"]),
        "latches": part("Rest catch and end pawl", S("pawl", "catch"), COL["pawl"]),
        "eject": part("Eject seesaw and pin", S("eject", "eject_pin"), COL["eject"]),
        "guard": part("Linkage guard", C["guard"].shape, COL["guard"]),
        "lid": part("Lid, hinge pin, latch pin", S("lid", "hinge_pin", "latch_pin"), COL["lid"]),
        "lever": part("Lever pipe and T-handle", S("lever", "lever_pin"), COL["lever"]),
    }


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"base": (0, 0, -620), "core": (0, 0, -160), "mold": (0, 0, 260), "piston": (0, 0, 720),
           "lower": (0, 520, -150), "upper": (0, 520, 60), "conlink": (0, 520, 330), "upin": (0, 520, 420),
           "hub": (-260, -380, -150), "latches": (-260, -700, -150), "eject": (520, 0, 330), "guard": (760, 0, -330),
           "lid": (0, 0, 1080), "lever": (-650, 0, -450)}
    order = ["base", "core", "mold", "piston", "lower", "upper", "conlink", "upin", "hub", "latches", "eject",
             "guard", "lid", "lever"]
    parts = []
    for k in order:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "EarthPress prototype: every component, pulled apart",
                       subtitle="Numbered in build order (sieve, test kit and gauge are separate). Seen from the front right and above",
                       elev=16, azim=-58, size=(11, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def flat_xz(shape, a, b_):
    """Move a part that lies in the XZ plane so that the line a -> b (XZ points) runs along +X from the origin."""
    import build123d as bd
    ang = math.degrees(math.atan2(b_[1] - a[1], b_[0] - a[0]))
    return bd.Rot(0, ang, 0) * bd.Pos(-a[0], 0, -a[1]) * shape


def sheets(only=None):
    import build123d as bd
    M = made()
    base = dict(project="EarthPress", date=DATE)
    out = []
    lx, lz = P["lever_x"], P["lever_z"]
    zb = G["z_b"]
    th0 = theta_start()
    (c0x, c0z), psi0 = knee_and_crank(th0)
    k0 = toggle_state(th0)[0]

    def want(n):
        return only is None or str(n) in only

    # 101 base frame (weldment)
    if want(101):
        out.append(bv.component_sheet(
            Part("Base frame", M["base"].shape, COL["base"]), [M["core"], M["mold"], M["hub"]],
            dwg_no="EPR-DWG-101", title="EarthPress base frame (one welded piece): making sketch",
            material="Mild steel tube 60 x 60 x 3 and 50 x 50 x 3; plate 12 and 10 mm; tube 40 x 3",
            inset_view=(22, -50),
            notes=["Skids: two 60 x 60 x 3 tubes 1,000 long, 520 apart (centres).",
                   "Cross tubes: four 50 x 50 x 3 tubes 460 long between the skids,",
                   "  tops flush with the skid tops, centred 25, 405, 670 and 975",
                   "  from the lever end of the skids. Weld all round.",
                   "Base plate 12 mm, 315 x 340, on the two middle cross tubes,",
                   "  380 to 695 from the lever end; 8 x 13.5 holes for the core",
                   "  feet and 2 x 11 holes for the guard feet (see the plan).",
                   "Lever bracket: two 10 mm plates (EPR-DWG-102), inner faces",
                   "  120 apart, standing on the end cross tube; weld both sides.",
                   "Rest stop: 30 mm round bar 120 long between the bracket plates.",
                   "Ties: two 40 x 3 round tubes 358 long, ends slotted over the",
                   "  bracket plates, other ends welded to 10 mm tabs 88 x 80.",
                   "Eject posts: two 10 mm plates 60 wide, 31 hole 536 above the",
                   "  base plate, 120 apart inside, welded upright on the base plate.",
                   "Weld with the bracket shaft and both tab holes on a dummy",
                   "  core jig, so the bolts line up. Check: frame sits flat."],
            **base))

    # 102 lever bracket plate
    if want(102):
        bp = C["bracket"].shape & _box(-600, -200, 55, 75, 0, 600)
        out.append(bv.component_sheet(
            Part("Lever bracket plate", bp, COL["base"]), [M["hub"], part("", S("skids", "cross"), COL["base"]), M["latches"]],
            dwg_no="EPR-DWG-102", title="EarthPress lever bracket plate (make 2, mirror pair): making sketch",
            material="Mild steel plate 10 mm", view_shape=bd.Pos(500, 0, -60) * bp, inset_view=(18, -120),
            notes=["Make two from 10 mm plate, about 230 x 272, cut to the outline.",
                   "Sizes along from the bottom left corner of the outline (the corner",
                   "  over the skid ends) and up from the bottom edge, which stands on",
                   "  the end cross tube. The outline bulges 21 left of that corner.",
                   "Shaft hole 40.5 at 32 along, 206 up (266 above the ground).",
                   f"Pawl shaft hole 16.5 (+Y plate) at {500 - 334.4:.0f} along, {179.2 - 60:.0f} up.",
                   f"Catch shaft hole 16.5 (-Y plate) at {500 - 309.0:.0f} along, {275.4 - 60:.0f} up.",
                   f"Crank pin access hole 31 (+Y plate) at {500 - 391.6:.0f} along, {191.1 - 60:.0f} up.",
                   "Ream the shaft holes in both plates clamped together, after",
                   "  welding, with a 40 mm bar through both to keep them in line.",
                   f"Rest stop bar 30 mm at {500 - 446.1:.0f} along, {188.4 - 60:.0f} up, welded across.",
                   "Fit: inner faces 120 apart; the hub (100 long) sits between",
                   "  them on two 10 mm washers. Ties weld to the outer faces.",
                   "Check: a 40 mm bar slides through both shaft holes."],
            **base))

    # 103 press core
    if want(103):
        out.append(bv.component_sheet(
            Part("Press core", M["core"].shape, COL["core"]), [M["base"], M["mold"], M["lower"]],
            dwg_no="EPR-DWG-103", title="EarthPress press core (one welded piece): making sketch",
            material="UPN 80 channel; mild steel plate 20 and 16 mm", inset_view=(20, -45),
            notes=["Columns: two UPN 80, 842 long, webs facing each other,",
                   "  196 apart (web faces); open sides face outward.",
                   "In each web: 4 x 18 holes at 18 each side of centre, 687 and",
                   "  767 up from the column foot (mold bolts).",
                   "In the +Y web only: two 40 access holes on the centre line,",
                   "  210 and 611 up from the foot (base pin and upper pin).",
                   "In the -X flange of each column: 2 x 13.5 holes 32 from the",
                   "  web face, 113 and 158 up from the foot (tie bolts).",
                   "Feet: 16 mm plates 140 x 90, 4 x 13.5 holes at 110 x 70.",
                   "Beam: two 20 x 100 plates 286 long, on the outside faces of",
                   "  the column flanges, tops 185 up from the foot; the -X plate",
                   "  drilled 13.5 through with the flange holes.",
                   "Lugs: two 20 mm plates 80 x 95 between the beam plates, 56",
                   "  apart inside, with a 41 bush hole 210 up from the foot.",
                   "Weld on a flat table; check the webs are parallel and 196 apart."],
            **base))

    # 104 mold box
    if want(104):
        out.append(bv.component_sheet(
            Part("Mold box", M["mold"].shape, COL["mold"]), [M["core"], M["lid"], M["piston"]],
            dwg_no="EPR-DWG-104", title="EarthPress mold box (one welded piece): making sketch",
            material="Mild steel plate 12, 16 and 20 mm", inset_view=(25, -60),
            notes=["Walls 12 mm, 200 tall: two long walls 314 long, two end walls",
                   "  140 long between them. Cavity 290 x 140, open top and bottom.",
                   "Weld outside only; grind the cavity faces flat and square,",
                   "  within 0.5 mm; break the top and bottom inside edges 1 mm.",
                   "Belt: 16 x 50 bar round the top, flush with the rim.",
                   "Side flanges: 16 mm plates 120 x 150 under the belt on the",
                   "  long walls. Before welding, drill 14 and tap M16 in 4 places:",
                   "  18 each side of centre, 35 and 115 up from the bottom edge.",
                   "Hinge lugs (+X end) and latch lugs (-X end): 20 mm plates on",
                   "  the belt ends, inner faces 144 apart; 31 holes 37 out from the",
                   "  belt, 10 above the rim (hinge) and 25 below it (latch).",
                   "Drill each lug pair together on a bar so the pins slide in.",
                   "Fit: flanges slide between the column webs (shim to 0.5 mm).",
                   "Check: a 288 x 138 plate passes through the cavity freely."],
            **base))

    # 105 lid
    if want(105):
        lid = C["lid"].shape
        out.append(bv.component_sheet(
            Part("Lid", lid, COL["lid"]), [M["mold"], part("", S("hinge_pin", "latch_pin"), COL["pin"])],
            dwg_no="EPR-DWG-105", title="EarthPress lid with ribs and pin ears: making sketch",
            material="Mild steel plate 20 mm", view_shape=bd.Pos(0, 0, -940) * lid, inset_view=(25, -60),
            notes=["Plate 20 mm, 360 x 230.",
                   "Ribs: two 20 mm plates, 488 long, cut to the outline in the",
                   "  front view: 70 high over the plate, with ears past both ends.",
                   "Hinge ear (+X): 31 hole 30 beyond the plate end, level with",
                   "  the plate's mid-thickness.",
                   "Latch ear (-X): 31 hole 30 beyond the plate end, 25 below the",
                   "  plate's underside.",
                   "Drill or bore both ribs clamped together so the holes line up.",
                   "Weld the ribs on the plate, 100 apart inside (centres 120),",
                   "  fillet both sides, full length.",
                   "Fit: the ears sit inside the mold's lugs with 2 mm each side.",
                   "The plate's underside sits flat on the mold rim.",
                   "Check: with the lid on the mold, both pins push through by hand."],
            **base))

    # 106 piston and push rod
    if want(106):
        pist = C["piston"].shape
        out.append(bv.component_sheet(
            Part("Piston and push rod", pist, COL["piston"]), [M["mold"], M["upin"], part("", C["upper_links"].shape, COL["upper"])],
            dwg_no="EPR-DWG-106", title="EarthPress piston, end skirts and push rod: making sketch",
            material="Mild steel plate 25 and 12 mm; 60 x 60 bright bar", inset_view=(-25, -55),
            view_shape=bd.Pos(0, 0, -527.5) * pist,
            notes=["Plate 25 mm, 288 x 138; corners broken 1 mm.",
                   "End skirts: two 12 mm plates 138 x 60, welded under the plate",
                   "  ends, flush with them. They keep the piston square in the mold.",
                   "Push rod: 60 x 60 bar, 238 long, welded square under the plate",
                   "  centre with a fillet all round.",
                   "Slot through the rod, side to side: 37 wide, 200 long; its top",
                   "  23 below the plate, its bottom 15 above the rod's foot.",
                   "  Chain drill and file, or mill; deburr.",
                   "Foot: the rod's bottom face, square and flat; the eject arm's",
                   "  nose pushes here. Face harden or fit a 6 mm wear pad if wanted.",
                   "Fit: 1 mm clearance each side in the mold; the upper pin sits",
                   "  in the slot, the upper links either side of the rod (2 mm).",
                   "Check: drops through the mold cavity under its own weight."],
            **base))

    # 107 toggle link
    if want(107):
        lk = C["lower_links"].shape & _box(-400, 200, 60, 96, 0, 1000)
        fl = flat_xz(lk, (0, zb), k0)
        out.append(bv.component_sheet(
            Part("Toggle link", lk, COL["lower"]), [M["core"], M["upper"], M["conlink"], M["piston"]],
            dwg_no="EPR-DWG-107", title="EarthPress toggle link (make 4): making sketch",
            material="Mild steel flat bar 70 x 28 mm", view_shape=fl, inset_view=(15, -40),
            notes=["Make four, all the same. Bar 70 x 28, 315 long.",
                   "Centres 245 apart on the bar's centre line, 35 from each end.",
                   "Round both ends to a 35 radius about the centres.",
                   "Bore 41 at both centres for the pressed-in bushes (35 bore),",
                   "  bores parallel within 0.2 mm over the 28 mm thickness.",
                   "Drill all four links clamped together, or on a jig, so the",
                   "  centres match within 0.2 mm.",
                   "Press in the bushes with a vice or press; ream to fit the",
                   "  35 pins with a light running fit; add a grease nipple at",
                   "  one end of each link (6 mm hole into the bore).",
                   "Fit: two lower links outside (64 to 92 from the centre line),",
                   "  two upper links inside (32 to 60), with spacers between.",
                   "Check: all four links stacked, a 35 pin passes through both ends."],
            **base))

    # 108 connecting link
    if want(108):
        cl = C["conlink"].shape
        fl = flat_xz(cl, (c0x, c0z), k0)
        out.append(bv.component_sheet(
            Part("Connecting link", cl, COL["conlink"]), [M["hub"], M["upper"], M["lower"]],
            dwg_no="EPR-DWG-108", title="EarthPress connecting link: making sketch",
            material="Mild steel flat bar 50 x 24 mm", view_shape=fl, inset_view=(15, -40),
            notes=["Bar 50 x 24, 470 long. Centres 420 apart, 25 from each end.",
                   "Round both ends to a 25 radius about the centres.",
                   "Crank end: bore 30.5 for the 30 mm crank pin.",
                   "Knee end: bore 35.5 for the 35 mm knee pin.",
                   "The 420 centre distance sets the stroke: hold it within 0.3 mm.",
                   "Fit: sits on the centre line between the two crank plates",
                   "  (4 mm each side) and between the knee spacers.",
                   "Check: measure the centre distance with the two pins fitted."],
            **base))

    # 109 hub, crank plates, socket
    if want(109):
        hb = C["hub"].shape
        out.append(bv.component_sheet(
            Part("Lever hub", hb, COL["hub"]), [M["base"], M["conlink"], part("", S("shaft", "crank_pin"), COL["pin"])],
            dwg_no="EPR-DWG-109", title="EarthPress lever hub, crank plates and socket: making sketch",
            material="80 mm bar or thick tube; plate 20 mm; tube 72 x 5", view_shape=bd.Pos(-lx, 0, -lz) * hb,
            inset_view=(18, -120),
            notes=["Hub: 80 round, 100 long, bored 40.5 through (or 80 x 20",
                   "  tube); press in two 40 mm bushes if wanted.",
                   "Crank plates: two 20 mm plates 50 wide, 107 centres, round",
                   "  ends, bored 40.5 (hub) and 30.5 (crank pin); 32 apart inside,",
                   "  welded on the hub. Bore the crank pin holes as a pair.",
                   "Socket: 72 x 5 tube (61.3 inside), 220 long, welded on the hub",
                   "  at 144 degrees from the crank plates (see the front view),",
                   "  its inner end 30 from the hub centre.",
                   "Locking pin hole 13 across the socket, 225 from the hub centre.",
                   "Fit: hub on the 40 shaft between the bracket plates, with a",
                   "  10 mm washer each side; the shaft has a circlip each end.",
                   "Check: turns freely on the shaft; the lever pipe slides in."],
            **base))

    # 110 lever pipe and T-handle
    if want(110):
        lv = C["lever"].shape
        phi = math.radians(math.degrees(psi0) + P["lever_offset"])
        a = (lx, lz); b_ = (lx + math.cos(phi), lz + math.sin(phi))
        fl = flat_xz(lv, a, b_)
        out.append(bv.component_sheet(
            Part("Lever pipe and T-handle", lv, COL["lever"]), [M["hub"], M["base"]],
            dwg_no="EPR-DWG-110", title="EarthPress lever pipe and T-handle: making sketch",
            material="2 in schedule 40 pipe (60.3 x 3.91); 1 in schedule 40 pipe", view_shape=fl, inset_view=(15, -60),
            notes=["Lever: 2 in schedule 40 pipe, 1,654 long, ends square.",
                   "T-handle: 1 in schedule 40 pipe, 500 long, through a 34 hole",
                   "  each side of the lever, 1,604 from the socket end; centre it",
                   "  and weld all round both sides. Rubber grips on both ends.",
                   "Locking pin hole 13 across the lever, 179 from the socket end.",
                   "The pipe goes 204 into the socket; the grip is then 1,650 from",
                   "  the hub centre.",
                   "Fit: slides into the hub socket or the eject socket; a 12 mm",
                   "  pin with an R-clip locks it in the hub socket.",
                   "Check: no burr inside the socket end; the pin goes in by hand."],
            **base))

    # 111 eject seesaw
    if want(111):
        ej = C["eject"].shape
        out.append(bv.component_sheet(
            Part("Eject seesaw", ej, COL["eject"]), [M["base"], M["piston"], M["core"]],
            dwg_no="EPR-DWG-111", title="EarthPress eject seesaw: making sketch",
            material="Plate 20 mm; 60 mm bar; tube 72 x 5", view_shape=bd.Pos(-P["eject_x"], 0, -P["eject_z"]) * ej,
            inset_view=(15, -40),
            notes=["Hub: 60 round, 110 long, bored 31 for the 30 mm pivot pin.",
                   "Arm: 20 mm plate, cut to the outline in the front view: from the",
                   "  hub, 40 wide, down to an elbow 179 away, then 30 wide up to a",
                   "  round nose of 15 radius. Nose top 160 from the pivot centre,",
                   "  80 below it and 139 toward the press. Weld on the hub centre.",
                   "Socket: 72 x 5 tube, 228 long, on the hub on the far side,",
                   "  30 degrees above the line from the pivot to the nose.",
                   "Fit: hub between the eject posts on the pin, circlips each end;",
                   "  the nose sits under the push rod's foot.",
                   "Smooth the nose; it slides on the rod foot as it lifts 160.",
                   "Check: swings freely; with the lever in the socket, a pull lifts",
                   "  the nose 160 without touching the column or the mold."],
            **base))

    # 112 pawl and catch
    if want(112):
        pw = C["pawl"].shape
        out.append(bv.component_sheet(
            Part("End pawl", pw, COL["pawl"]), [M["hub"]],
            dwg_no="EPR-DWG-112", title="EarthPress end pawl and rest catch (one of each, mirror pair): making sketch",
            material="Plate 12 and 10 mm; 16 mm bright round bar", inset_view=(15, 70),
            notes=["Make one pawl (+Y side) and one catch (-Y side), mirror images.",
                   "Shaft: 16 bright bar, 40 long.",
                   "Pawl plate: 12 mm, 24 wide, 90 between the shaft and the tip",
                   "  centre, round ends of 12 radius; weld on the shaft's inner end.",
                   "Handle: 10 mm plate 20 wide, from the shaft out to a 20 knob,",
                   "  welded on the shaft's outer end, outside the bracket plate.",
                   "Fit: shaft through the 16.5 hole in the bracket plate, washer",
                   "  and circlip; a torsion spring holds the tip against the crank pin.",
                   "Pawl: its tip drops in under the crank pin at the end of the",
                   "  stroke and takes the kickback end on, along its length.",
                   "Catch: its tip drops in above the crank pin at the start and",
                   "  stops the lever falling into the stroke.",
                   "Check: each snaps in by its spring and lifts out by the handle."],
            **base))

    # 113 linkage guard
    if want(113):
        gd = C["guard"].shape
        out.append(bv.component_sheet(
            Part("Linkage guard", gd, COL["guard"]), [M["base"], M["hub"], M["core"]],
            dwg_no="EPR-DWG-113", title="EarthPress linkage guard: making sketch",
            material="Expanded metal about 2 mm strand; angle 20 x 20 x 3", inset_view=(25, -130),
            notes=["Two side frames of 20 x 20 x 3 angle, 316 long and 568 tall,",
                   "  230 apart (outside faces 274), covered with expanded metal.",
                   "Top: expanded metal 210 x 230 over the crank end, 568 up.",
                   "Feet: one angle foot each side at the core end, 11 hole,",
                   "  M10 to the base plate.",
                   "Brackets: two angle brackets each side at the lever end, 45",
                   "  long, M10 with 35 mm spacer tubes to the bracket plates.",
                   "Mesh openings no larger than 12 mm so fingers stay out.",
                   "Fit: the crank, connecting link, ties and knee move inside;",
                   "  nothing touches the guard over the full stroke.",
                   "Check: work the lever slowly through the full stroke."],
            **base))

    # 114 block gauge
    if want(114):
        gg = C["gauge"].shape
        out.append(bv.component_sheet(
            Part("Block gauge", gg, COL["gauge"]), [part("", C["blocks"].shape & _box(700, 1300, -500, -100, 260, 400), "#C08A5B")],
            dwg_no="EPR-DWG-114", title="EarthPress block gauge: making sketch",
            material="Mild steel flat bar 40 x 12 mm and 12 mm square bar", view_shape=bd.Pos(-1000, 300, -360) * gg, inset_view=(25, -60),
            notes=["Bar 40 x 12, 340 long; two legs of 12 x 12 bar, 40 long,",
                   "  welded under the ends, 292 apart inside.",
                   "Notch 93 wide and 20 deep in the middle of the top edge.",
                   "Length: a good block drops between the legs (292 is the longest",
                   "  allowed, 290 plus 2).",
                   "Height: a good block, on its side, fits the notch (93 is the",
                   "  tallest allowed, 90 plus 3).",
                   "File the inside faces flat; check with a steel rule.",
                   "Paint the gauge so it is easy to find on site."],
            **base))

    # 115 soil sieve (laid flat)
    if want(115):
        from build123d import Box, Pos
        frame = Box(900, 700, 45) - Box(810, 610, 47)
        mesh = Pos(0, 0, 0) * Box(810, 610, 4)
        sv = frame + mesh
        out.append(bv.component_sheet(
            Part("Soil sieve", C["sieve"].shape, COL["sieve"]), [],
            dwg_no="EPR-DWG-115", title="EarthPress soil sieve: making sketch",
            material="Timber 45 x 45; 5 mm welded wire mesh", view_shape=sv, inset_view=(20, -60),
            notes=["Frame: timber 45 x 45, 900 x 700 outside, corners halved,",
                   "  glued and screwed.",
                   "Mesh: 5 mm welded wire mesh 810 x 610, stapled to the frame's",
                   "  top face and covered with a 20 x 10 batten screwed down.",
                   "Prop: two 24 mm hardwood legs 700 long, hinged to the frame's",
                   "  top rail, so the sieve leans back at about 65 degrees.",
                   "Use: throw dry soil at the mesh; what passes is used, what",
                   "  stays (stones, clods) is set aside."],
            **base))
    return out


# ----------------------------------------------------------------- joints
def win(sh, x0, x1, y0, y1, z0_, z1_):
    return sh & _box(x0, x1, y0, y1, z0_, z1_)


def joints(only=None):
    out = []
    zb = G["z_b"]

    def want(n):
        return only is None or str(n) in only

    def J(n, items, title, sub, **kw):
        out.append(bv.joint([part(nm, sh, col) for nm, sh, col in items], OUT / f"joint-{n:02d}.png",
                            f"Joint {n}: {title}", subtitle=sub, size=(8, 6), **kw))

    if want(1):   # column foot, cut through a row of bolts
        bx = (-20, 55, 60, 175, 40, 150)
        J(1, [("Base plate (12 mm)", win(C["base_plate"].shape, *bx), "#D6D3D1"),
              ("Column foot (16 mm)", win(C["feet"].shape, *bx), "#4B5563"),
              ("Column, UPN 80", win(C["columns"].shape, *bx), "#9CA3AF"),
              ("M12 bolts (4 per foot), nuts under the plate", win(C["bolts"].shape, *bx), COL["bolt"])],
          "column foot on the base plate (+Y side)", "Cut through two of the four bolts, seen from the eject end. The foot lies flat on the plate; nuts go on under the plate",
          elev=15, azim=5)
    if want(2):   # tie tab
        bx = (-110, 45, 50, 150, 170, 290)
        J(2, [("Tie tube and its tab", win(C["ties"].shape, *bx), "#78716C"),
              ("Base beam plate", win(C["beam"].shape, *bx), "#CBD5E1"),
              ("Column flange and web", win(C["columns"].shape, *bx), "#94A3B8"),
              ("2 x M12 through tab, beam and flange", win(C["bolts"].shape, *bx), COL["bolt"])],
          "tie tab on the base beam (+Y side)", "Seen from the lever side, above. The bolts pass the tab, the beam plate and the column flange; nuts inside the channel",
          elev=25, azim=-150)
    if want(3):   # mold flange to column, cut through one column of bolts
        zz0, zz1 = D["MB"] + 5, D["MB"] + 150
        bx = (-70, 18, 55, 150, zz0, zz1)
        J(3, [("Mold wall", win(C["mold"].shape, *bx), COL["mold"]),
              ("Side flange, tapped M16", win(C["flanges"].shape, *bx), "#14B8A6"),
              ("Column web and flanges", win(C["columns"].shape, *bx), "#9CA3AF"),
              ("M16 bolts from inside the channel", win(C["bolts"].shape, *bx), COL["bolt"])],
          "mold flange bolted to the column web (+Y side)", "Cut through a row of bolts, seen from the right. Each bolt passes the web and screws into the flange; head inside the open channel",
          elev=12, azim=10)
    if want(4):   # base pin
        bx = (-60, 60, -110, 110, zb - 60, zb + 50)
        J(4, [("Lugs, welded between the beam plates", win(C["lugs"].shape, *bx), "#64748B"),
              ("Spacers", win(C["base_spacers"].shape, *bx), "#1F2937"),
              ("Lower links, outside", win(C["lower_links"].shape, *bx), COL["lower"]),
              ("Base pin, 35 mm", win(C["base_pin"].shape, *bx), "#E5E7EB"),
              ("Column webs", win(C["columns"].shape, *bx), "#CBD5E1")],
          "base pin, lugs, spacers and lower links", "Cut through the pin's axis, seen from the lever side. Order across: web, link, spacer, lug, lug, spacer, link, web",
          cut="+X", elev=8, azim=180)
    if want(5):   # knee
        kx, kz = toggle_state(theta_start())[0]
        bx = (kx - 60, kx + 60, -110, 110, kz - 60, kz + 60)
        J(5, [("Lower links, outside", win(C["lower_links"].shape, *bx), COL["lower"]),
              ("Upper links", win(C["upper_links"].shape, *bx), COL["upper"]),
              ("Spacers", win(C["knee_spacers"].shape, *bx), COL["spacer"]),
              ("Connecting link, centre", win(C["conlink"].shape, *bx), COL["conlink"]),
              ("Knee pin, 35 mm", win(C["knee_pin"].shape, *bx), "#E5E7EB")],
          "the knee", "Cut through the pin's axis, seen from the lever side. Lower links outside, upper links inside, connecting link in the middle",
          cut="+X", elev=8, azim=180)
    if want(6):   # upper pin in slot, cut down the middle so the slot shows
        zp = D["zp0"]
        bx = (-80, 80, -90, 90, zp - 200, zp + 90)
        J(6, [("Push rod with its slot", win(C["piston"].shape, *bx), COL["piston"]),
              ("Upper link (far side)", win(C["upper_links"].shape, *bx), COL["upper"]),
              ("Upper pin, 35 mm", win(C["upper_pin"].shape, *bx), "#E5E7EB")],
          "upper pin in the push rod's slot", "Cut down the middle, seen from the front. The pin bears on the top of the slot when pressing; the rod rises 165 mm past it when ejecting",
          cut="+Y", elev=5, azim=-90)
    if want(7):   # hub and rest stop, catch
        lx, lz = P["lever_x"], P["lever_z"]
        bx = (lx - 70, lx + 190, -112, 112, lz - 120, lz + 120)
        J(7, [("Bracket plate (-Y)", win(C["bracket"].shape, *bx), "#CBD5E1"),
              ("Hub, crank plates, socket", win(C["hub"].shape, *bx), COL["hub"]),
              ("Shaft, 40 mm", win(C["shaft"].shape, *bx), COL["pin"]),
              ("Crank pin", win(C["crank_pin"].shape, *bx), "#D1D5DB"),
              ("Rest stop bar", win(C["rest"].shape, *bx), COL["rest"]),
              ("Rest catch (-Y side)", win(C["catch"].shape, *bx), COL["pawl"])],
          "lever hub on its shaft, at rest", "Seen from the +Y side; near half cut away. Crank plates on the rest stop; the catch's tip sits over the crank pin",
          cut="-Y", elev=10, azim=80)
    if want(8):   # end pawl at end of stroke
        Ce = build_components(theta=math.radians(P["theta_end"]))
        lx, lz = P["lever_x"], P["lever_z"]
        bx = (lx - 70, lx + 190, 38, 112, lz - 120, lz + 120)
        J(8, [("Bracket plate (+Y), behind, with the crank pin access hole", win(Ce["bracket"].shape, *bx), "#CBD5E1"),
              ("Hub", win(Ce["hub"].shape, *bx), COL["hub"]),
              ("Crank pin", win(Ce["crank_pin"].shape, *bx), COL["pin"]),
              ("End pawl and its handle", win(Ce["pawl"].shape, *bx), COL["pawl"])],
          "end pawl under the crank pin, end of the stroke", "Seen from inside the bracket, looking toward +Y. The pawl's tip sits 1 mm under the pin and takes the kickback end on",
          elev=8, azim=-90)
    if want(9):   # eject nose
        bx = (-40, 200, -60, 60, 430, 650)
        J(9, [("Push rod foot", win(C["piston"].shape, *bx), COL["piston"]),
              ("Eject arm and hub", win(C["eject"].shape, *bx), COL["eject"]),
              ("Eject posts", win(C["posts"].shape, *bx), COL["base"]),
              ("Pivot pin, 30 mm", win(C["eject_pin"].shape, *bx), COL["pin"])],
          "eject arm's nose under the push rod", "Seen from the -Y side; near post cut away. The round nose bears on the rod's foot and lifts it 160 mm",
          cut="+Y", elev=6, azim=-95)
    if want(10):  # hinge
        hx, hz = P["hinge_x"], P["hinge_z"]
        bx = (hx - 60, hx + 45, -110, 110, hz - 70, hz + 50)
        J(10, [("Mold hinge lugs", win(C["mold_lugs"].shape, *bx), "#2DD4BF"),
               ("Belt", win(C["mold"].shape, *bx), "#CCFBF1"),
               ("Lid ribs' hinge ears and plate", win(C["lid"].shape, *bx), COL["lid"]),
               ("Hinge pin, 30 mm", win(C["hinge_pin"].shape, *bx), COL["pin"])],
           "lid hinge", "Seen from the +X end, above. The rib ears sit inside the mold's lugs, 2 mm each side; one pin through all four",
           elev=25, azim=-20)
    if want(11):  # latch
        lxx, lzz = P["latch_x"], P["latch_z"]
        bx = (lxx - 45, lxx + 60, -150, 150, lzz - 60, lzz + 60)
        J(11, [("Mold latch lugs", win(C["mold_lugs"].shape, *bx), "#2DD4BF"),
               ("Belt", win(C["mold"].shape, *bx), "#CCFBF1"),
               ("Lid ribs' latch ears and plate", win(C["lid"].shape, *bx), COL["lid"]),
               ("Latch pin with T-handle", win(C["latch_pin"].shape, *bx), COL["pin"])],
           "lid latch", "Seen from the -X end, above. Push the pin through all four holes to latch; pull it to open",
           elev=25, azim=-160)
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    M = made()
    out = []

    def want(n):
        return only is None or str(n) in only

    def st(n, done, new, title, sub, **kw):
        if want(n):
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)

    th_asm = math.radians(ASSEMBLY_THETA)
    A = build_components(theta=th_asm)          # toggle folded for fitting the upper pin
    ground = part("Level ground", _box(-700, 700, -450, 450, -6, 0), "#E5E7EB")
    st(1, [], [mv(M["base"], (0, 0, 150))], "set the base frame level",
       "On firm, level ground; check level both ways across the base plate and shim the skids if needed",
       context=[ground], elev=22, azim=-55)
    st(2, [M["base"]], [mv(part("Press core", S("columns", "feet", "beam", "lugs"), COL["core"]), (0, 0, 250)),
                        mv(part("8 x M12, nuts under the plate", C["bolts"].shape & _box(-80, 80, -170, 170, 40, 100), COL["bolt"]), (0, 0, 120))],
       "press core onto the base plate", "Two people. Four M12 bolts through each foot; then bolt the two tie tabs to the beam (joint 2)",
       elev=20, azim=-55, label_done=False)
    st(3, [M["base"], M["core"]], [mv(M["mold"], (0, 0, 300))], "mold box between the columns",
       "Lower it between the column webs; four M16 bolts each side from inside the channels (joint 3)",
       elev=20, azim=-55, label_done=False)
    st(4, [M["base"], M["core"], M["mold"]], [mv(part("Piston and push rod", A["piston"].shape, COL["piston"]), (0, 0, 420))],
       "piston into the mold from the top", "Rod first; slot across the press (side to side). Let it down until the plate is just inside the mold's bottom",
       elev=22, azim=-55, label_done=False)
    done4 = [M["base"], M["core"], M["mold"], part("Piston", A["piston"].shape, COL["piston"])]
    st(5, done4, [mv(part("Lower links", A["lower_links"].shape, COL["lower"]), (-200, 0, 0)),
                  mv(part("Base pin, through the access hole", A["base_pin"].shape, COL["pin"]), (0, 280, 0)),
                  mv(part("Spacers", A["base_spacers"].shape, COL["spacer"]), (0, 0, 0))],
       "lower links on the base pin", "Hold links and spacers between the lugs; push the pin in through the +Y column's lower access hole; circlip",
       elev=18, azim=-125, label_done=False)
    done5 = done4 + [part("Lower links", S("lower_links", "base_pin", "base_spacers"), COL["lower"])]
    done5 = [done5[0], done5[1], done5[2], done5[3], part("Lower links", _fuse([A[k].shape for k in ("lower_links", "base_pin", "base_spacers")]), COL["lower"])]
    st(6, done5, [mv(part("Upper links", A["upper_links"].shape, COL["upper"]), (-200, 0, 80)),
                  mv(part("Knee pin and spacers", _fuse([A["knee_pin"].shape, A["knee_spacers"].shape]), COL["pin"]), (0, -300, 0)),
                  mv(part("Connecting link", A["conlink"].shape, COL["conlink"]), (-150, 0, -60))],
       "the knee", "Upper links inside the lower links, connecting link in the middle between two spacers; knee pin from the side; circlips",
       elev=18, azim=-125, label_done=False)
    done6 = done5 + [part("Upper links and knee", _fuse([A[k].shape for k in ("upper_links", "knee_pin", "knee_spacers", "conlink")]), COL["upper"])]
    st(7, done6, [mv(part("Upper pin, through the upper access hole", A["upper_pin"].shape, COL["pin"]), (0, 300, 0))],
       "upper pin through the rod's slot", f"Fold the knee back until the link holes line up with the slot and the upper access hole ({D['zp_asm']:.0f} mm up); pin in, circlip",
       elev=18, azim=-125, label_done=False)
    T = [M["base"], M["core"], M["mold"], M["piston"], part("Toggle", S("lower_links", "upper_links", "base_pin", "knee_pin", "upper_pin", "base_spacers", "knee_spacers", "conlink"), COL["lower"])]
    st(8, T, [mv(part("Lever hub", C["hub"].shape, COL["hub"]), (0, 0, 220)),
              mv(part("Shaft, 40 mm, and washers", C["shaft"].shape, COL["pin"]), (0, -260, 0)),
              mv(part("Crank pin", C["crank_pin"].shape, "#D1D5DB"), (0, 220, 0))],
       "lever hub on its shaft; crank pin", "Hub between the bracket plates on washers; shaft through, circlips. Crank on the rest stop; crank pin in through the +Y plate's access hole",
       elev=18, azim=-125, label_done=False)
    H = T + [part("Hub", S("hub", "shaft", "crank_pin"), COL["hub"])]
    st(9, [M["base"], part("Hub", S("hub", "shaft", "crank_pin"), COL["hub"])],
       [mv(part("End pawl (+Y plate)", C["pawl"].shape, COL["pawl"]), (0, 0, 180)),
        mv(part("Rest catch (-Y plate)", C["catch"].shape, "#C026D3"), (0, 0, 180))],
       "rest catch and end pawl", "Core, mold and toggle left out. Shaft through the bracket plate from inside, handle outside, washer and circlip; hook on the springs",
       elev=30, azim=-60, label_done=False)
    L = H + [part("Pawl and catch", S("pawl", "catch"), COL["pawl"])]
    st(10, L, [mv(part("Eject seesaw", C["eject"].shape, COL["eject"]), (280, 0, 40)),
               mv(part("Pivot pin, 30 mm", C["eject_pin"].shape, COL["pin"]), (0, -260, 0))],
       "eject seesaw between the posts", "Seen from the eject end. Nose under the push rod's foot; pin through posts and hub; circlips; grease",
       elev=18, azim=-20, label_done=False)
    E = L + [part("Eject", S("eject", "eject_pin"), COL["eject"])]
    st(11, E, [mv(M["guard"], (0, 0, 300))], "linkage guard",
       "Feet to the base plate with M10; brackets to the bracket plates with M10 and 35 mm spacers. Work the lever after (section 6)",
       elev=24, azim=-125, label_done=False)
    F = E + [M["guard"]]
    st(12, F, [mv(part("Lid", C["lid"].shape, COL["lid"]), (0, 0, 260)),
               mv(part("Hinge pin", C["hinge_pin"].shape, COL["pin"]), (0, 260, 0)),
               mv(part("Latch pin", C["latch_pin"].shape, "#D1D5DB"), (0, 300, 0))],
       "lid, hinge pin and latch pin", "Two people (27 kg). Ears inside the mold's lugs; hinge pin, circlips; latch pin pushed in to close",
       elev=22, azim=-55, label_done=False)
    st(13, F + [part("Lid", S("lid", "hinge_pin", "latch_pin"), COL["lid"])],
       [mv(part("Lever pipe and T-handle", C["lever"].shape, COL["lever"]), (-40, 0, 260)),
        mv(part("Locking pin, 12 mm", C["lever_pin"].shape, COL["pin"]), (0, 200, 0))],
       "lever into the hub socket", "Slide the pipe in past the locking hole; 12 mm pin and R-clip. Hold point: safety stop S4 (section 6)",
       elev=15, azim=-60, label_done=False)
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    only = None
    for a in list(args):
        if a.startswith("only="):
            only = set(a[5:].split(","))
            args.remove(a)
    what = args or ["overview", "sheets", "joints", "steps"]
    fns = {"overview": overview, "sheets": sheets, "joints": joints, "steps": steps}
    for w in what:
        r = fns[w]() if w == "overview" else fns[w](only)
        print(w, "->", r)
