"""STEM check helpers (STANDARDS section 20).

Used from a project's docs/04-calcs/stem_check.py:

    import sys; sys.path.insert(0, ".kit")
    from stem_check import Check, limits
    c = Check()
    c.claim("S1", "Frame below yield at 1.5 x jack rating", "Physics", "Strength of materials",
            law="Beam bending, S275 yield 275 MPa (EN 10025-2)",
            value=212, limit=275, unit="MPa", rule="below")
    c.claim("S2", "Suction lift of the hand pump", "Physics", "Fluid mechanics",
            law="Atmospheric pressure less vapour pressure", value=6.0,
            limit=limits.suction_lift_m(altitude_m=1200, water_c=25), unit="m", rule="below")
    c.order_of_magnitude("S3", "Pots per 6 h", "Mathematics", "Orders of magnitude",
            claimed=69, estimate=6 * 60 / 5.2, unit="pots")
    c.write()      # docs/04-calcs/stem_results.csv, read by the STM document

Each check returns a verdict: "Within known science", "Plausible, to confirm at TRL 3", "Fails, fix proposed"
(a detail fails but a fix that keeps the working principle is proposed to Amish) or "Fails" (the working
principle itself does not hold).
A check is a first-order screen; it never replaces the calculation note (CAL).
"""
from __future__ import annotations
import csv, math
from pathlib import Path

WITHIN, PLAUSIBLE, FIX, FAILS = "Within known science", "Plausible, to confirm at TRL 3", "Fails, fix proposed", "Fails"
FIELDS = ("Physics", "Chemistry", "Biology", "Mathematics", "Engineering and technology")
G = 9.80665          # m/s2
R = 8.314462618      # J/(mol K)
SIGMA = 5.670374e-8  # W/(m2 K4)
SOLAR_CONSTANT = 1361.0   # W/m2, top of atmosphere
PEAK_SUN = 1000.0         # W/m2, standard test condition at ground level
LATENT_WATER = 2.257e6    # J/kg, evaporation at 100 C (about 2.43e6 at 25 C)


class limits:
    """Theoretical limits a claim must not exceed."""

    @staticmethod
    def carnot(t_hot_c: float, t_cold_c: float) -> float:
        th, tc = t_hot_c + 273.15, t_cold_c + 273.15
        return 1 - tc / th

    BETZ = 16 / 27                     # maximum share of wind kinetic power a turbine can extract
    SHOCKLEY_QUEISSER = 0.337          # single-junction solar cell, AM1.5
    HUMAN_SUSTAINED_W = 75.0           # sustained hand-cranking or pedalling by an average adult, W
    HUMAN_PEAK_W = 300.0

    @staticmethod
    def suction_lift_m(altitude_m: float = 0.0, water_c: float = 20.0) -> float:
        """Theoretical suction lift of water (before friction and NPSH margin)."""
        p_atm = 101325 * (1 - 2.25577e-5 * altitude_m) ** 5.25588
        p_vap = 610.94 * math.exp(17.625 * water_c / (water_c + 243.04))
        rho = 1000 - 0.0178 * abs(water_c - 4) ** 1.7
        return (p_atm - p_vap) / (rho * G)

    @staticmethod
    def evaporation_kg_per_m2_day(sun_kwh_m2_day: float, efficiency: float = 1.0) -> float:
        """Upper bound on water evaporated by sunlight alone (solar stills, dryers)."""
        return sun_kwh_m2_day * 3.6e6 * efficiency / 2.43e6

    @staticmethod
    def radiant_w_m2(t_c: float, emissivity: float = 0.95) -> float:
        return emissivity * SIGMA * (t_c + 273.15) ** 4


class Check:
    def __init__(self, out: str | Path = "docs/04-calcs/stem_results.csv"):
        self.rows, self.out = [], Path(out)

    def _add(self, sid, claim, field, branch, law, detail, verdict, closed_by=""):
        if field not in FIELDS:
            raise ValueError(f"{sid}: field must be one of {FIELDS}")
        self.rows.append(dict(id=sid, claim=claim, field=field, branch=branch, law=law,
                              check=detail, verdict=verdict, closed_by=closed_by))
        return verdict

    def claim(self, sid, claim, field, branch, law, value, limit, unit, rule="below", margin=0.0, closed_by=""):
        """rule 'below': value must not exceed limit; 'above': value must reach limit. margin: share of the
        limit inside which the verdict is only Plausible (for example 0.1 = within 10 % of the limit)."""
        ok = value <= limit if rule == "below" else value >= limit
        near = margin > 0 and abs(value - limit) <= margin * abs(limit)
        verdict = FAILS if not ok else (PLAUSIBLE if near else WITHIN)
        detail = f"{value:g} {unit} {'<=' if rule == 'below' else '>='} {limit:.4g} {unit}"
        return self._add(sid, claim, field, branch, law, detail, verdict, closed_by)

    def order_of_magnitude(self, sid, claim, field, branch, claimed, estimate, unit, factor=3.0, law="Back-of-envelope estimate", closed_by=""):
        ratio = claimed / estimate if estimate else math.inf
        verdict = WITHIN if 1 / factor <= ratio <= factor else (PLAUSIBLE if 1 / (3 * factor) <= ratio <= 3 * factor else FAILS)
        return self._add(sid, claim, field, branch, law, f"claimed {claimed:g} {unit}, estimate {estimate:.3g} {unit} (ratio {ratio:.2f})", verdict, closed_by)

    def balance(self, sid, claim, field, branch, inputs: dict, outputs: dict, unit, tolerance=0.05, law="Conservation of energy or mass", closed_by=""):
        """Inputs must cover outputs plus losses; outputs may not exceed inputs by more than the tolerance."""
        tin, tout = sum(inputs.values()), sum(outputs.values())
        verdict = WITHIN if tout <= tin * (1 + tolerance) else FAILS
        return self._add(sid, claim, field, branch, law, f"in {tin:.4g} {unit}, out {tout:.4g} {unit}", verdict, closed_by)

    def cited(self, sid, claim, field, branch, law, detail, verdict, closed_by=""):
        """A claim checked against a cited source rather than a formula (chemistry doses, biology effects)."""
        if verdict not in (WITHIN, PLAUSIBLE, FIX, FAILS):
            raise ValueError("verdict must be WITHIN, PLAUSIBLE, FIX or FAILS")
        return self._add(sid, claim, field, branch, law, detail, verdict, closed_by)

    def summary(self):
        n = {v: sum(r["verdict"] == v for r in self.rows) for v in (WITHIN, PLAUSIBLE, FIX, FAILS)}
        state = "fail" if n[FAILS] else ("open" if n[FIX] or any(r["verdict"] == PLAUSIBLE and not r["closed_by"] for r in self.rows) else "pass")
        return state, n

    def write(self):
        self.out.parent.mkdir(parents=True, exist_ok=True)
        with self.out.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(self.rows[0].keys()))
            w.writeheader(); w.writerows(self.rows)
        state, n = self.summary()
        print(f"STEM check {state}: {n[WITHIN]} within, {n[PLAUSIBLE]} plausible, {n[FIX]} fail with a fix proposed, {n[FAILS]} fail -> {self.out}")
        return state
