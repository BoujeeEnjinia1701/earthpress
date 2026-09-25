"""EarthPress concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. X runs along the lever (the lever swings on the -X side), Y across the press,
Z up, ground at Z = 0. The press is shown with the lid closed and the lever raised at the start of
the compression stroke, with loose soil filling the mold above the piston.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all

# Block and mold (proposed block 290 x 140 x 90 mm, the Auroville CSEB module)
BLK_L, BLK_W, BLK_H = 290.0, 140.0, 90.0
WALL = 12.0                     # mold wall plate
MOLD_H = 250.0
MOLD_TOP = 900.0                # working height of the mold rim
MOLD_BOT = MOLD_TOP - MOLD_H
FILL_H = 150.0                  # loose fill depth, compacts to about 90 mm
PISTON_TOP = MOLD_TOP - FILL_H
COL_Y = BLK_W / 2 + WALL + 25   # column center line, either side of the mold
SKID_H = 60.0

STEEL = "#4B5563"
EARTH = "#B7794A"


def tube3(a, b, r):
    """Round bar or tube between two 3D points."""
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def bar(a, b, w, t):
    """Rectangular bar between two points in the XZ plane (width w in Y, thickness t)."""
    ax, ay, az = a; bx, by, bz = b
    L = math.hypot(bx - ax, bz - az)
    ang = math.degrees(math.atan2(bz - az, bx - ax))
    return Pos((ax + bx) / 2, ay, (az + bz) / 2) * Rot(0, -ang, 0) * Box(L, w, t)


# 1 Frame on skids: two skids, cross members, two columns either side of the mold, base plate
skids = Pos(0, -260, SKID_H / 2) * Box(1000, 60, SKID_H) + Pos(0, 260, SKID_H / 2) * Box(1000, 60, SKID_H)
cross = Pos(-300, 0, SKID_H + 10) * Box(60, 580, 20) + Pos(300, 0, SKID_H + 10) * Box(60, 580, 20)
base_plate = Pos(0, 0, SKID_H + 10) * Box(240, 580, 20)
columns = (Pos(0, COL_Y, (SKID_H + 20 + MOLD_TOP) / 2) * Box(100, 50, MOLD_TOP - SKID_H - 20)
           + Pos(0, -COL_Y, (SKID_H + 20 + MOLD_TOP) / 2) * Box(100, 50, MOLD_TOP - SKID_H - 20))
braces = (tube3((-300, 250, SKID_H + 20), (-40, COL_Y, 500), 14) + tube3((-300, -250, SKID_H + 20), (-40, -COL_Y, 500), 14)
          + tube3((300, 250, SKID_H + 20), (40, COL_Y, 500), 14) + tube3((300, -250, SKID_H + 20), (40, -COL_Y, 500), 14))
lever_bracket = Pos(-80, 0, 330) * Box(60, 2 * COL_Y + 50, 40)
frame = skids + cross + base_plate + columns + braces + lever_bracket

# 2 Mold box: 12 mm wall plate around a 290 x 140 mm cavity
mold = (Pos(0, 0, MOLD_BOT + MOLD_H / 2) * Box(BLK_L + 2 * WALL, BLK_W + 2 * WALL, MOLD_H)
        - Pos(0, 0, MOLD_BOT + MOLD_H / 2) * Box(BLK_L, BLK_W, MOLD_H + 2))

# 3 Lid with hinge and latch hook
lid = Pos(0, 0, MOLD_TOP + 11) * Box(BLK_L + 70, BLK_W + 2 * WALL + 36, 22)
hinge = Pos(BLK_L / 2 + 35, 0, MOLD_TOP + 11) * Rot(90, 0, 0) * Cylinder(14, BLK_W + 2 * WALL + 36)
latch = Pos(-BLK_L / 2 - 45, 0, MOLD_TOP - 5) * Box(20, 80, 54)
lid = lid + hinge + latch

# 4 Piston: compression plate and push rod
piston = (Pos(0, 0, PISTON_TOP - 20) * Box(BLK_L - 2, BLK_W - 2, 40)
          + Pos(0, 0, (PISTON_TOP - 40 + 470) / 2) * Box(50, 50, PISTON_TOP - 40 - 470))

# 5 Toggle linkage: paired links from the push rod to the base pivot with a knee toward -X
top_pin, knee, base_pin = (0, 0, 470), (-70, 0, 300), (0, 0, 110)
toggle = None
for y in (-38, 38):
    s = (tube3((top_pin[0], y, top_pin[2]), (knee[0], y, knee[2]), 16)
         + tube3((knee[0], y, knee[2]), (base_pin[0], y, base_pin[2]), 16))
    toggle = s if toggle is None else toggle + s
for p in (top_pin, knee, base_pin):
    toggle = toggle + Pos(p[0], 0, p[2]) * Rot(90, 0, 0) * Cylinder(15, 110)
toggle = toggle + Pos(0, 0, 90) * Box(80, 110, 40)          # base clevis

# 6 Lever: removable 1.5 m pipe on a short crank that drives the knee
PIV = (-80, 0, 360)
LEVER_ANG = 42.0
tip = (PIV[0] - 1500 * math.cos(math.radians(LEVER_ANG)), 0, PIV[2] + 1500 * math.sin(math.radians(LEVER_ANG)))
lever = tube3(PIV, tip, 21) + tube3(tip, (tip[0] - 10, 0, tip[2] + 5), 26)
crank = bar((PIV[0], 0, PIV[2]), (knee[0], 0, knee[2]), 60, 20) + Pos(PIV[0], 0, PIV[2]) * Rot(90, 0, 0) * Cylinder(20, 2 * COL_Y + 60)

# 7 Ejection stop and lever catch: adjustable stop on the column and a catch for the lever at rest
eject = (Pos(0, COL_Y + 45, 620) * Box(60, 40, 60)
         + Pos(0, COL_Y + 45, 690) * Cylinder(10, 80)
         + Pos(-470, 0, SKID_H + 120) * Box(40, 80, 200) + Pos(-470, 0, SKID_H + 10) * Box(40, 580, 20))

# Loose soil in the mold (context, not a BOM line)
fill = Pos(0, 0, PISTON_TOP + FILL_H / 2 - 1) * Box(BLK_L - 4, BLK_W - 4, FILL_H - 4)

# 8 Soil sieve: 5 mm mesh in a timber frame, leaning on a prop on the +X side
SX, SY = 1000.0, 700.0
sieve_frame = Pos(SX, SY, 420) * Rot(0, -25, 0) * (Box(45, 700, 900) - Box(47, 610, 810))
mesh = Pos(SX, SY, 420) * Rot(0, -25, 0) * Box(4, 610, 810)
prop = tube3((SX + 130, SY - 300, 0), (SX + 20, SY - 300, 660), 12) + tube3((SX + 130, SY + 300, 0), (SX + 20, SY + 300, 660), 12)
sieve = sieve_frame + mesh + prop

# 9 Soil test kit: crate with sedimentation jars and a shrinkage box
kit = (Pos(300, -650, 125) * Box(400, 300, 250)
       + Pos(220, -690, 250 + 90) * Cylinder(45, 180) + Pos(340, -690, 250 + 90) * Cylinder(45, 180)
       + Pos(300, -570, 250 + 20) * Box(300, 50, 40))

# Stack of pressed blocks (context): 3 x 4 blocks per course, 4 courses
BX, BY = 800.0, -250.0
blocks = None
for c in range(4):
    for i in range(3):
        for j in range(4):
            if c % 2:
                b = Pos(BX + i * 150 - 150, BY + (j - 1.5) * 150, BLK_H * (c + 0.5)) * Rot(0, 0, 90) * Box(BLK_L - 6, BLK_W - 6, BLK_H - 2)
            else:
                b = Pos(BX + (i - 1) * 150, BY + (j - 1.5) * 150, BLK_H * (c + 0.5)) * Rot(0, 0, 90) * Box(BLK_L - 6, BLK_W - 6, BLK_H - 2)
            blocks = b if blocks is None else blocks + b

# 10 Block gauge: go/no-go height and length gauge resting on the stack
GZ = 4 * BLK_H
gauge = (Pos(BX, BY, GZ + 6) * Box(340, 30, 12) + Pos(BX - 164, BY, GZ - 20) * Box(12, 30, 40)
         + Pos(BX + 164, BY, GZ - 20) * Box(12, 30, 40))

parts = [
    Part("Frame on skids", frame, STEEL, 1, (0, 0, -260)),
    Part("Mold box, 290 x 140 mm cavity", mold, "#0F766E", 2, (0, 0, 420)),
    Part("Lid with hinge and latch", lid, "#115E59", 3, (0, 0, 760)),
    Part("Piston and push rod", piston, "#D4A017", 4, (650, -100, 700)),
    Part("Toggle linkage and pins", toggle, "#C2410C", 5, (380, -300, 60)),
    Part("Lever and crank, 1.5 m", lever + crank, "#1F2937", 6, (250, 0, -380)),
    Part("Ejection stop and lever catch", eject, "#7C3AED", 7, (-350, 450, -150)),
    Part("Soil sieve, 5 mm mesh", sieve, "#A16207", 8, (400, 600, 0)),
    Part("Soil test kit", kit, "#2563EB", 9, (-300, -700, 0)),
    Part("Block gauge", gauge, "#16A34A", 10, (300, -300, 450)),
    Part("Loose soil fill (context)", fill, EARTH, None, (0, 0, 1150)),
    Part("Pressed blocks (context)", blocks, "#C08A5B", None, (300, -300, 0)),
]

if __name__ == "__main__":
    render_all(
        parts, project="EarthPress", title="Manual CSEB press concept", dwg_no="EPR-DWG-010",
        key_figures=["Block 290 x 140 x 90 mm, about 7 kg dry (estimate)",
                     "About 81 kN on the block for 2 MPa (estimate)",
                     "1.5 m lever, 500 N pull, toggle near straight",
                     "About 300 blocks per day, crew of 4 (estimate)",
                     "About $403 in parts, press and kit (indicative)"],
        cut_exclude=("Soil sieve, 5 mm mesh", "Soil test kit", "Block gauge", "Pressed blocks (context)",
                     "Ejection stop and lever catch"),
        flow={"title": "material flow per 100 blocks, kg (estimates; mixing adds 33 kg cement and 70 kg water)", "unit": "kg",
              "stages": [("Dug site soil", 775), ("Sieved soil", 660), ("Moist mix", 763),
                         ("Pressed blocks", 740), ("Cured blocks", 685)],
              "losses": [(0, "Oversize > 5 mm", 115), (2, "Spill and rejects, remixed", 23),
                         (3, "Water lost in curing", 55)]},
    )
