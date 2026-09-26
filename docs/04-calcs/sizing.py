"""EarthPress sizing calculations, EPR-CAL-001 v0.2 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes docs/04-calcs/results.csv.
Geometry comes from cad/src/model.py (PARAMS, toggle_state, knee_and_crank, piece_masses) and
costs from bom/bom.csv. All inputs are stated assumptions for a paper design; nothing is measured.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as P, geometry, theta_start, toggle_state, knee_and_crank, lever_angle, piece_masses  # noqa: E402

G = 9.81

# ---------------------------------------------------------------- assumptions
A = {
    "p_target_MPa": 2.0,          # R2, EPR-DDR-001 item 4
    "rho_dry": 1900.0,            # dry block density, kg/m3 (TRL 2 assumption)
    "cement_frac": 0.05,          # of dry soil mass (item 5)
    "water_frac": 0.10,           # of dry mix mass
    "decade_mm": 14.0,            # soil law: pressure rises tenfold over the last 14 mm of the stroke
    "decade_lo": 10.0, "decade_hi": 20.0,
    "G_one": 500.0,               # one operator, R5 limit (N)
    "G_two": 1000.0,              # two operators on the T-handle, also the abuse case for the structure
    "grip_lo": 800.0, "grip_hi": 1900.0,   # working grip band used for the design study (mm)
    "fy_plate": 250.0,            # MPa, mild steel plate and sections (A36 / S235 lower bound)
    "fy_pipe": 240.0,             # MPa, A53 grade B pipe
    "fy_pin": 370.0,              # MPa, C45 turned pins
    "bush_allow": 100.0,          # MPa, hardened steel bush, greased, slow oscillation (assumed)
    "E": 200000.0,                # MPa
    "K0": 0.5,                    # lateral to vertical pressure ratio in the mold
    "ej_lateral_MPa": 0.10,       # residual lateral pressure after unloading (assumed)
    "ej_mu": 0.6,                 # soil on steel friction
    "rebound_mm": 1.0,            # soil elastic rebound at 2 MPa (assumed)
    "bolt_FvRd_kN": 60.3,         # M16 8.8, single shear through the thread: 0.6 x 800 x 157 / 1.25
    "n_bolts_mold": 8,
    "fat_range_MPa": 243.0,       # FAT 71 detail at 50,000 cycles: 71 x (2e6 / 5e4)^(1/3)
    "steel_usd_kg": 1.30,
    # output and crew (R4)
    "cycle_s": {"weigh and fill": 25, "strike, close and latch": 8, "press (two on the lever)": 10,
                "return lever, unlatch, open lid": 7, "move lever to eject socket": 6, "eject": 6,
                "lift off, gauge, carry to stack": 15, "return lever, brush mold": 8},
    "work_h": 7.0,                # effective hours in an 8 h day
    "oversize": 0.15,             # fraction of dug soil retained on the 5 mm sieve
    "sieve_kg_h": 400.0, "mix_kg_h": 600.0,   # per person (assumed)
    "reject_frac": 0.03,          # spill and rejects, remixed
    "bound_water": 0.23,          # of cement mass
    "resid_moist": 0.015,         # of dry mass in cured blocks
    # small house (R11)
    "perimeter_m": 22.0, "wall_h_m": 2.7, "openings": 0.15, "joint_mm": 10.0,
    "co2_cseb": 49.0, "co2_brick": 643.0,     # kg CO2/m3, Auroville Earth Institute
}

rows = []   # (section, quantity, value, unit)


def out(section, name, value, unit="", fmt="{:.1f}"):
    v = fmt.format(value) if isinstance(value, (int, float)) else str(value)
    rows.append((section, name, v, unit))
    print(f"  {name:<58} {v:>12} {unit}")


def head(t):
    print("\n" + t)


# ---------------------------------------------------------------- 1 block and force
head("1. Block and compaction force (R1, R2)")
BL, BW, BH = P["blk_l"], P["blk_w"], P["blk_h"]
area = BL * BW                                # mm2
F_nom = A["p_target_MPa"] * area              # N
vol_L = BL * BW * BH / 1e6
m_dry = vol_L / 1000 * A["rho_dry"]
m_soil = m_dry / (1 + A["cement_frac"])
m_cem = m_dry - m_soil
m_moist = m_dry * (1 + A["water_frac"])
out("block", "Block face area", area / 1e6, "m2", "{:.4f}")
out("block", "Block volume", vol_L, "L", "{:.2f}")
out("block", "Dry block mass", m_dry, "kg", "{:.2f}")
out("block", "Moist mass at the press", m_moist, "kg", "{:.2f}")
out("block", "Cement per block", m_cem, "kg", "{:.2f}")
out("block", "Force for 2 MPa (nominal)", F_nom / 1000, "kN")
out("block", "Force for 4 MPa", 2 * F_nom / 1000, "kN")
fill_ratio = P["fill_h"] / BH
out("block", "Loose to pressed height ratio", fill_ratio, "", "{:.2f}")
out("block", "Loose dry density in the mold", A["rho_dry"] / fill_ratio, "kg/m3", "{:.0f}")

# ---------------------------------------------------------------- 2 kinematics
head("2. Linkage kinematics (R2, R5)")
g = geometry()
th_s = theta_start(); th_e = math.radians(P["theta_end"])
N = 601
ths = [th_s + (th_e - th_s) * i / (N - 1) for i in range(N)]
zface = [toggle_state(t)[2] for t in ths]
s_mm = [z - zface[0] for z in zface]
lev = [lever_angle(t) for t in ths]
R = P["grip_r"]
grip_z = [P["lever_z"] + R * math.sin(math.radians(a)) for a in lev]
out("kin", "Toggle link length", P["link_l"], "mm", "{:.0f}")
out("kin", "Toggle angle at start / end (from vertical)", f"{math.degrees(th_s):.1f} / {P['theta_end']:.1f}", "deg")
out("kin", "Piston stroke", s_mm[-1], "mm")
out("kin", "Base pin height / upper pin height at end", f"{g['z_b']:.0f} / {g['z_p_end']:.0f}", "mm")
out("kin", "Lever angle at start / end (from +X)", f"{lev[0]:.1f} / {lev[-1]:.1f}", "deg")
arc = abs(lev[-1] - lev[0])
out("kin", "Lever arc", arc, "deg")
out("kin", "Grip path length", R * math.radians(arc) / 1000, "m", "{:.2f}")
out("kin", "Grip height at start / end", f"{grip_z[0]:.0f} / {grip_z[-1]:.0f}", "mm")
# the R5 band 0.9 to 1.6 m: largest arc any lever of this radius can sweep inside it
band_arc = 2 * math.degrees(math.asin((1600 - 900) / 2 / R))
out("kin", "Largest arc inside 0.9 to 1.6 m with this grip radius", band_arc, "deg")
out("kin", "Grip inside the R5 band 0.8 to 1.9 m (EPR-DDR-002)", "yes" if min(grip_z) >= 800 and max(grip_z) <= 1900 else "no")
out("kin", "Arc of the TRL 2 proposal (800 mm pivot, 100 deg)", 100.0, "deg", "{:.0f}")
out("kin", "Lowest grip height for that proposal (symmetric arc)", 800 - R * math.sin(math.radians(50)), "mm", "{:.0f}")

# mechanical advantage ds_grip / dz_piston
MA = []
for i in range(N):
    j0, j1 = max(i - 1, 0), min(i + 1, N - 1)
    dz = zface[j1] - zface[j0]
    dg = R * math.radians(abs(lev[j1] - lev[j0]))
    MA.append(dg / dz)
out("kin", "Overall force ratio at the end of the stroke", MA[-1], ":1", "{:.0f}")
i30 = min(range(N), key=lambda k: abs(s_mm[k] - 30.0))
out("kin", "Force ratio at mid-stroke (30 mm)", MA[i30], ":1", "{:.1f}")
mono = all(MA[i + 1] >= MA[i] for i in range(N - 1))
out("kin", "Force ratio rises monotonically to the stop", "yes" if mono else "no")


# ---------------------------------------------------------------- 3 soil law and grip force
def soil_force(s, dec, shift=0.0):
    """Piston force (N) at piston travel s (mm); shift > 0 means the soil reaches 2 MPa shift mm earlier."""
    lam = dec / math.log(10)
    stroke = s_mm[-1]
    return F_nom * math.exp(-(stroke - shift - s) / lam)


def grip_profile(dec, shift=0.0):
    return [soil_force(s_mm[i], dec, shift) / MA[i] for i in range(N)]


def reach(dec, Gmax, shift=0.0):
    """Travel and force where the operators stall (grip force needed exceeds Gmax), or the stop."""
    for i in range(N):
        if soil_force(s_mm[i], dec, shift) / MA[i] > Gmax:
            return s_mm[i], soil_force(s_mm[i], dec, shift), False
    return s_mm[-1], soil_force(s_mm[-1], dec, shift), True


head("3. Grip force and work (R2, R5)")
Gb = grip_profile(A["decade_mm"])
ipk = max(range(N), key=lambda i: Gb[i])
out("grip", "Peak grip force, base soil (14 mm per decade)", Gb[ipk], "N", "{:.0f}")
out("grip", "Travel at the peak", s_mm[ipk], "mm")
out("grip", "Grip height at the peak", grip_z[ipk], "mm", "{:.0f}")
out("grip", "Peak at 1.0 m or higher (R5, EPR-DDR-002)", "yes" if grip_z[ipk] >= 1000 else "no")
out("grip", "Grip force at the end of the stroke", Gb[-1], "N", "{:.0f}")
for dec in (A["decade_lo"], A["decade_hi"]):
    out("grip", f"Peak grip force, soil {dec:.0f} mm per decade", max(grip_profile(dec)), "N", "{:.0f}")
s1, F1, ok1 = reach(A["decade_mm"], A["G_one"])
out("grip", "One operator at 500 N: stalls at travel", s1, "mm")
out("grip", "One operator at 500 N: pressure reached", F1 / area, "MPa", "{:.2f}")
s2, F2, ok2 = reach(A["decade_mm"], A["G_two"])
out("grip", "Two operators at 1,000 N: reach the stop", "yes" if ok2 else "no")
out("grip", "Two operators: pressure at the stop", F2 / area, "MPa", "{:.2f}")
out("grip", "Share per operator at the peak (two on the T-handle)", Gb[ipk] / 2, "N", "{:.0f}")
lam = A["decade_mm"] / math.log(10)
W_need = F_nom * lam * (1 - math.exp(-s_mm[-1] / lam)) / 1000
out("grip", "Compaction work, base soil", W_need, "J", "{:.0f}")
for dec in (A["decade_lo"], A["decade_hi"]):
    l_ = dec / math.log(10)
    out("grip", f"Compaction work, soil {dec:.0f} mm per decade", F_nom * l_ / 1000, "J", "{:.0f}")
out("grip", "Work one operator can give at 500 N over the arc", A["G_one"] * R * math.radians(arc) / 1000, "J", "{:.0f}")
out("grip", "Matching efficiency needed for one operator", W_need / (A["G_one"] * R * math.radians(arc) / 1000) * 100, "%", "{:.0f}")
print("  Profile (travel mm, piston kN, force ratio, grip N, grip height mm):")
prof = []
for sv in (0, 20, 30, 40, 45, 50, 53, 55, 57, 59, 60):
    i = min(range(N), key=lambda k: abs(s_mm[k] - sv))
    prof.append((s_mm[i], soil_force(s_mm[i], A["decade_mm"]) / 1000, MA[i], Gb[i], grip_z[i]))
    print("   %5.1f %7.2f %7.1f %6.0f %6.0f" % prof[-1])
    rows.append(("profile", f"s = {s_mm[i]:.1f} mm", f"{prof[-1][1]:.2f} kN; ratio {MA[i]:.1f}; grip {Gb[i]:.0f} N; height {grip_z[i]:.0f} mm", ""))

# ---------------------------------------------------------------- 4 fill window
head("4. Fill tolerance (R1, R2)")
# fill mass error e: the soil reaches 2 MPa at height 90(1 + e), i.e. shift = 90 e mm earlier in the stroke
window = []
for k in range(-50, 101):
    e = k / 1000
    sft = BH * e
    s_, F_, at_stop = reach(A["decade_mm"], A["G_two"], sft)
    h = BH + (s_mm[-1] - s_)
    window.append((e, F_ / area, h, at_stop))
ok = [w for w in window if w[1] >= A["p_target_MPa"] - 1e-9 and w[3]]
e_lo, e_hi = min(w[0] for w in ok), max(w[0] for w in ok)
out("fill", "Fill mass window for 2 MPa at the stop, two operators", f"{e_lo * 100:+.1f} to {e_hi * 100:+.1f}", "%")
out("fill", "Same window in grams of moist mix", f"{e_lo * m_moist * 1000:+.0f} to {e_hi * m_moist * 1000:+.0f}", "g")
for e in (-0.02, -0.01, 0.0, 0.02, 0.04):
    w = min(window, key=lambda x: abs(x[0] - e))
    out("fill", f"Fill {e * 100:+.0f} %: pressure, block height", f"{w[1]:.2f} MPa, {w[2]:.1f} mm", "")
w_one = [reach(A["decade_mm"], A["G_one"], BH * e) for e in [k / 1000 for k in range(0, 101)]]
best_one = max(F / area for (_, F, st) in w_one if st) if any(st for (_, _, st) in w_one) else max(F / area for (_, F, _) in w_one)
out("fill", "Best pressure one operator reaches at any overfill", best_one, "MPa", "{:.2f}")

# ---------------------------------------------------------------- 5 design load and structure
head("5. Design load and structure (R12, R8)")
F_abuse = A["G_two"] * MA[-1]
out("str", "Abuse load: 1,000 N at the grip at the stop", F_abuse / 1000, "kN")
out("str", "Equivalent pressure on the block", F_abuse / area, "MPa", "{:.2f}")
out("str", "R12 latch requirement, 1.5 x nominal block force", 1.5 * F_nom / 1000, "kN")
cth = math.cos(th_e)
d = P["pin_d"]; Apin = math.pi * d * d / 4
checks = []


def chk(name, stress, allow, unit="MPa"):
    sf = allow / stress
    checks.append((name, stress, allow, sf))
    out("str", f"{name}", f"{stress:.0f} {unit} (SF {sf:.2f})", "")


for F, tag in ((F_nom, "nominal"), (F_abuse, "abuse")):
    print(f"  -- at {tag} load {F / 1000:.1f} kN")
    link = F / cth
    chk(f"Toggle pin {d:.0f} mm, double shear, {tag}", link / (2 * Apin), 0.577 * A["fy_pin"])
    chk(f"Bush bearing, 2 x {P['link_t']:.0f} mm links, {tag}", link / (2 * P["link_t"] * d), A["bush_allow"])
    net = (P["link_w"] - d - 2) * P["link_t"]
    chk(f"Link net section at the pin hole, {tag}", link / 2 / net, A["fy_plate"])
    Iw = P["link_w"] * P["link_t"] ** 3 / 12
    Pcr = math.pi ** 2 * A["E"] * Iw / P["link_l"] ** 2
    checks.append((f"Link buckling out of plane, {tag}", link / 2, Pcr, Pcr / (link / 2)))
    out("str", f"Link buckling out of plane, {tag}", f"{link / 2 / 1000:.0f} kN on {Pcr / 1000:.0f} kN (SF {Pcr / (link / 2):.1f})", "")
    r = P["rod"]
    chk(f"Push rod net section at the slot, {tag}", F / ((r - d - 2) * r), A["fy_plate"])
    # lid: simply supported between hinge and latch, block pressure over the middle 290 mm
    span = P["lid_l"] / 2 + 5 + P["lid_l"] / 2 + 20
    M = F / 2 * (span / 2) - F / 2 * (BL / 4)
    b_, t_, rt, rh, = P["lid_w"], P["lid_t"], P["rib_t"], P["rib_h"]
    A1, A2 = b_ * t_, 2 * rt * rh
    yb = (A1 * t_ / 2 + A2 * (t_ + rh / 2)) / (A1 + A2)
    I = b_ * t_ ** 3 / 12 + A1 * (yb - t_ / 2) ** 2 + 2 * rt * rh ** 3 / 12 + A2 * (t_ + rh / 2 - yb) ** 2
    Zt = I / (t_ + rh - yb)
    chk(f"Lid bending (plate {t_:.0f} + ribs {rt:.0f} x {rh:.0f}), {tag}", M / Zt, A["fy_plate"])
    defl = 5 * F * span ** 3 / (384 * A["E"] * I)
    out("str", f"Lid deflection at mid-span, {tag}", defl, "mm", "{:.2f}")
    chk(f"Hinge and latch pins {P['hinge_pin_d']:.0f} mm, double shear, {tag}", F / 2 / (2 * math.pi * P["hinge_pin_d"] ** 2 / 4), 0.577 * A["fy_pin"])
    # mold long wall with top belt, fixed-fixed over 302 mm, lateral K0 p over the block height
    pl = A["K0"] * F / area
    w = pl * BH
    Lw = BL + P["wall"]
    fw, ft, bt, bh = BH + 10, P["wall"], P["belt_t"], P["belt_h"]
    a1, a2 = fw * ft, bh * bt
    yb2 = (a1 * ft / 2 + a2 * (ft + bt / 2)) / (a1 + a2)
    I2 = fw * ft ** 3 / 12 + a1 * (yb2 - ft / 2) ** 2 + bh * bt ** 3 / 12 + a2 * (ft + bt / 2 - yb2) ** 2
    M2 = w * Lw ** 2 / 12
    chk(f"Mold long wall with belt, {tag}", M2 / (I2 / max(yb2, ft + bt - yb2)), A["fy_plate"])
    if tag == "nominal":
        dw = w * Lw ** 4 / (384 * A["E"] * I2)
        out("str", "Mold wall bulge at 2 MPa", dw, "mm", "{:.3f}")
    chk(f"Columns UPN 80 in tension, {tag}", F / 2 / 1100.0, A["fy_plate"])
    out("str", f"Mold to column bolts, {A['n_bolts_mold']} x M16 8.8, {tag}",
        f"{F / 1000:.0f} kN on {A['n_bolts_mold'] * A['bolt_FvRd_kN']:.0f} kN (SF {A['n_bolts_mold'] * A['bolt_FvRd_kN'] * 1000 / F:.1f})", "")
    col_y = BW / 2 + P["wall"] + P["flange_t"] + P["col_b"] / 2
    Mb = F * (2 * col_y) / 4
    chk(f"Base beam, 2 x {P['beam_t']:.0f} x {P['beam_d']:.0f} plates, {tag}", Mb / (2 * P["beam_t"] * P["beam_d"] ** 2 / 6), A["fy_plate"])

# TRL 2 lid: plain 22 mm plate 220 mm wide over the same span, nominal load
span = P["lid_l"] / 2 + 5 + P["lid_l"] / 2 + 20
M22 = F_nom / 2 * (span / 2) - F_nom / 2 * (BL / 4)
out("str", "TRL 2 lid, plain 22 mm plate, at nominal load", M22 / (220 * 22 ** 2 / 6), "MPa", "{:.0f}")

# connecting link, lever and tie loads at the abuse case
(cx, cz), psi = knee_and_crank(th_e)
kx, kz = toggle_state(th_e)[0]
ox, oz = P["lever_x"], P["lever_z"]
ux, uz = (kx - cx), (kz - cz)
Lc = math.hypot(ux, uz)
arm = abs((cx - ox) * uz - (cz - oz) * ux) / Lc          # perpendicular distance from O to the link line
T = A["G_two"] * R
Fc = T / arm
out("str", "Connecting link moment arm about the lever pivot at the stop", arm, "mm")
out("str", "Connecting link force at the abuse case", Fc / 1000, "kN")
Ic = 50 * P["conlink_t"] ** 3 / 12
Pc = math.pi ** 2 * A["E"] * Ic / P["conlink"] ** 2
out("str", "Connecting link buckling capacity (50 x 24 flat)", f"{Pc / 1000:.0f} kN (SF {Pc / Fc:.1f})", "")
out("str", "Tie tube load (two 40 mm tubes), horizontal component", abs(Fc * ux / Lc) / 1000, "kN")
Do, t = P["lever_od"], P["lever_wall"]
Di = Do - 2 * t
Zp = math.pi * (Do ** 4 - Di ** 4) / (32 * Do)
for Gv, tag in ((Gb[ipk], "working peak"), (A["G_two"], "abuse")):
    chk(f"Lever 2 in sch 40 at the socket mouth, {tag}", Gv * (R - 250) / Zp, A["fy_pipe"])
min_sf = min(c[3] for c in checks)
out("str", "Lowest safety factor on yield or capacity (abuse case)", min_sf, "", "{:.2f}")

# fatigue at nominal load, 50,000 blocks
ranges = [c[1] for c in checks if "nominal" in c[0] and "buckling" not in c[0] and "Bush" not in c[0]]
out("str", "Highest nominal stress range per block", max(ranges), "MPa", "{:.0f}")
out("str", "Allowed range, FAT 71 welded detail at 50,000 cycles", A["fat_range_MPa"], "MPa", "{:.0f}")

# kickback
d_loop = F_nom / 2 / 1100.0 / A["E"] * (P["mold_top"] - 72.0)
E_kick = 0.5 * F_nom * (A["rebound_mm"] + d_loop) / 1000
out("str", "Column stretch at 2 MPa", d_loop, "mm", "{:.2f}")
out("str", "Energy returned to the lever if released at the end", E_kick, "J", "{:.0f}")
out("str", "Clearance from the T-handle to the ground at the end", grip_z[-1] - 17, "mm", "{:.0f}")

# ---------------------------------------------------------------- 6 ejection
head("6. Ejection (R2, R5)")
wall_area = 2 * (BL + BW) * BH
F_fric = A["ej_lateral_MPa"] * A["ej_mu"] * wall_area
masses = piece_masses()
m_pist = masses["Piston and slotted push rod"]
F_ej = F_fric + (m_pist + m_moist) * G
ratio_ej = R / P["eject_arm"]
out("ej", "Wall friction to break the block free", F_fric / 1000, "kN", "{:.2f}")
out("ej", "Ejection force including piston and block weight", F_ej / 1000, "kN", "{:.2f}")
out("ej", "Eject lever ratio", ratio_ej, ":1", "{:.1f}")
out("ej", "Grip force to eject", F_ej / ratio_ej, "N", "{:.0f}")
out("ej", "Force to lift the lid at the latch end", masses["Lid with ribs, hinge and latch"] * G / 2, "N", "{:.0f}")
out("ej", "Eject lift (60 mm to the block, 90 mm out, 10 mm clear)", P["eject_lift"], "mm", "{:.0f}")
out("ej", "Eject lever arc", 2 * math.degrees(math.asin(P["eject_lift"] / 2 / P["eject_arm"])), "deg")

# ---------------------------------------------------------------- 7 mass
head("7. Mass (R7)")
for n, m in masses.items():
    out("mass", n, m, "kg")
tot = sum(masses.values())
out("mass", "Press total, steel", tot, "kg")
out("mass", "Heaviest single piece", max(masses.values()), "kg")
out("mass", "Margin to the R7 total of 190 kg (EPR-DDR-002)", 190.0 - tot, "kg")
out("mass", "Lever pipe alone (removable)", math.pi / 4 * (Do ** 2 - Di ** 2) * P["lever_len"] * 7850e-9, "kg")

# ---------------------------------------------------------------- 8 output and crew
head("8. Output and crew (R4)")
cyc = sum(A["cycle_s"].values())
per_day = A["work_h"] * 3600 / cyc
out("out", "Cycle time", cyc, "s", "{:.0f}")
out("out", "Blocks per 8 h day (7 h working)", per_day, "", "{:.0f}")
dry_day = per_day * m_dry
soil_dry = per_day * m_soil * (1 + A["reject_frac"])
dug = soil_dry / (1 - A["oversize"])
prep_h = dug / A["sieve_kg_h"] + per_day * m_moist * (1 + A["reject_frac"]) / A["mix_kg_h"]
out("out", "Soil dug per day", dug, "kg", "{:.0f}")
out("out", "Sieving and mixing, person-hours", prep_h, "h", "{:.1f}")
out("out", "Available from two helpers", 2 * 8.0, "h", "{:.0f}")

# ---------------------------------------------------------------- 9 material flow, house, carbon
head("9. Material flow, house and carbon (R10, R11)")
n = 100
f_soil = n * m_soil
f_dug = f_soil / (1 - A["oversize"])
f_cem = n * m_cem
f_water = n * m_dry * A["water_frac"]
f_press = n * m_moist
f_rej = f_press * A["reject_frac"]
f_mix = f_press + f_rej
f_cured = n * (m_dry + A["bound_water"] * m_cem + A["resid_moist"] * m_dry)
for k_, v_ in (("Dug soil per 100 blocks", f_dug), ("Oversize removed", f_dug - f_soil), ("Sieved soil", f_soil),
               ("Cement added", f_cem), ("Water added", f_water), ("Moist mix incl. remixed rejects", f_mix),
               ("Spill and rejects, remixed", f_rej), ("Pressed blocks", f_press), ("Cured blocks", f_cured),
               ("Water lost in curing", f_press - f_cured)):
    out("flow", k_, v_, "kg", "{:.0f}")
wall_m2 = A["perimeter_m"] * A["wall_h_m"] * (1 - A["openings"])
per_m2 = 1e6 / ((BL + A["joint_mm"]) * (BH + A["joint_mm"]))
nb = wall_m2 * per_m2
vol = wall_m2 * BW / 1000
out("house", "Wall area, small house", wall_m2, "m2")
out("house", "Blocks per m2 (10 mm joints)", per_m2, "", "{:.1f}")
out("house", "Blocks for the house", nb, "", "{:.0f}")
out("house", "Press days", nb / per_day, "", "{:.1f}")
out("house", "Wall per day", per_day / per_m2, "m2", "{:.1f}")
out("house", "Cement for the house", nb * m_cem, "kg", "{:.0f}")
out("house", "50 kg bags", nb * m_cem / 50, "", "{:.1f}")
out("house", "Walling volume", vol, "m3", "{:.2f}")
out("house", "CO2, CSEB", vol * A["co2_cseb"] / 1000, "t", "{:.2f}")
out("house", "CO2, fired brick", vol * A["co2_brick"] / 1000, "t", "{:.2f}")
out("house", "CSEB as a share of fired brick", A["co2_cseb"] / A["co2_brick"] * 100, "%", "{:.1f}")

# ---------------------------------------------------------------- 10 cost
head("10. Cost (R13)")
total = 0.0
with open(ROOT / "bom/bom.csv", newline="") as f:
    for r_ in csv.DictReader(f):
        total += float(r_["qty"]) * float(r_["unit_cost_usd"])
out("cost", "BOM total, press and kit", total, "USD", "{:.0f}")
budget = next(float(l.split(":")[1].split("#")[0]) for l in (ROOT / "project.yaml").read_text().splitlines() if l.startswith("budget_usd:"))
out("cost", "Budget in project.yaml", budget, "USD", "{:.0f}")
out("cost", "Under budget by", budget - total, "USD", "{:.0f}")
out("cost", "Steel in the press at the indicative price", tot * A["steel_usd_kg"], "USD", "{:.0f}")

with open(ROOT / "docs/04-calcs/results.csv", "w", newline="") as f:
    wtr = csv.writer(f)
    wtr.writerow(["section", "quantity", "value", "unit"])
    wtr.writerows(rows)
print("\nwrote docs/04-calcs/results.csv")
