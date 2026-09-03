"""
Preliminary thermal scoping calculation - UAS avionics enclosure.

Purpose
-------
Order-of-magnitude check on whether a sealed 6061-T6 enclosure can reject the
avionics stack heat load within the ambient temperature allowable, BEFORE any
FEA is built. Establishes an expected answer to compare the FEA against.

This is a lumped-parameter calculation. It treats the enclosure as isothermal
and computes a single surface-to-ambient temperature rise. It does NOT resolve
internal gradients, component hot spots, or conduction through mounts. Those
require the FEA. If the FEA disagrees with this by more than ~30%, investigate
before trusting either.

Correlations used
-----------------
Natural convection : Churchill-Chu, vertical plate, laminar range
Forced convection  : Flat plate, laminar, Nu = 0.664 Re^0.5 Pr^(1/3)
Radiation          : Linearized about surface temperature

References: Incropera & DeWitt, Fundamentals of Heat and Mass Transfer.

Author: Akshar Patel
"""

import numpy as np

# ----------------------------------------------------------------------
# INPUTS - edit these
# ----------------------------------------------------------------------

# Heat load, from requirements.md Section 2
Q_TOTAL = 10.80                 # W, total stack dissipation

# Enclosure external dimensions (first-cut estimate)
L = 0.093                       # m, length (also used as characteristic length)
W = 0.063                     # m, width
H = 0.0333                       # m, height

# Environment, from requirements.md Section 3.3
T_AMB = 35.0                    # degC, hot-day ambient
V_CRUISE = 18.0                 # m/s, cruise freestream
V_HOVER = 0.0                   # m/s, hover (natural convection only)

# Surface finish
EMISSIVITY_BARE = 0.10          # bare / machined aluminum
EMISSIVITY_ANODIZED = 0.80      # hard anodized aluminum

# Allowable, from REQ-THM-001
T_ALLOW_AMBIENT = 40.0          # degC, binding internal air limit

# Air properties at ~50 degC film temperature, 1 atm
RHO = 1.09                      # kg/m^3
MU = 1.96e-5                    # Pa.s
K_AIR = 0.0281                  # W/m.K
PR = 0.71                       # Prandtl number
NU_KIN = MU / RHO               # m^2/s, kinematic viscosity
BETA = 1.0 / (273.15 + 50.0)    # 1/K, thermal expansion (ideal gas)
G = 9.81                        # m/s^2

SIGMA = 5.670374419e-8          # W/m^2.K^4, Stefan-Boltzmann


# ----------------------------------------------------------------------
# GEOMETRY
# ----------------------------------------------------------------------

def surface_area(l, w, h):
    """Total external area of a rectangular box, m^2."""
    return 2.0 * (l * w + l * h + w * h)


# ----------------------------------------------------------------------
# HEAT TRANSFER COEFFICIENTS
# ----------------------------------------------------------------------

def h_natural(dT, char_len=H):
    """
    Natural convection coefficient, W/m^2.K.
    Churchill-Chu for a vertical plate. Uses enclosure height as the
    characteristic length. Conservative for the top/bottom faces.
    """
    if dT <= 0:
        return 0.0
    Ra = (G * BETA * dT * char_len**3) / (NU_KIN**2) * PR
    # Churchill-Chu, valid across the laminar range
    num = 0.670 * Ra**0.25
    den = (1.0 + (0.492 / PR)**(9.0 / 16.0))**(4.0 / 9.0)
    Nu = 0.68 + num / den
    return Nu * K_AIR / char_len


def h_forced(velocity, char_len=L):
    """
    Forced convection coefficient, W/m^2.K.
    Flat-plate laminar correlation, average Nusselt number.
    Returns 0 for zero velocity.
    """
    if velocity <= 0:
        return 0.0
    Re = RHO * velocity * char_len / MU
    Nu = 0.664 * Re**0.5 * PR**(1.0 / 3.0)
    return Nu * K_AIR / char_len, Re


def h_radiation(T_surf_C, T_amb_C, emissivity):
    """
    Linearized radiation coefficient, W/m^2.K.
    Assumes the enclosure radiates to a large surrounding at ambient.
    """
    Ts = T_surf_C + 273.15
    Ta = T_amb_C + 273.15
    return emissivity * SIGMA * (Ts + Ta) * (Ts**2 + Ta**2)


# ----------------------------------------------------------------------
# SOLVER
# ----------------------------------------------------------------------

def solve_surface_temp(Q, area, velocity, emissivity, T_amb,
                       tol=1e-4, max_iter=200):
    """
    Iterate to a converged surface temperature.

    Both the natural convection and radiation coefficients depend on the
    surface temperature, so this cannot be solved in closed form. Fixed-point
    iteration with under-relaxation.
    """
    T_surf = T_amb + 10.0        # initial guess
    relax = 0.3

    for i in range(max_iter):
        dT = T_surf - T_amb

        if velocity > 0:
            h_conv, _ = h_forced(velocity)
        else:
            h_conv = h_natural(dT)

        h_rad = h_radiation(T_surf, T_amb, emissivity)
        h_tot = h_conv + h_rad

        if h_tot <= 0:
            return np.nan, np.nan, np.nan, False

        T_new = T_amb + Q / (h_tot * area)
        T_surf = T_surf + relax * (T_new - T_surf)

        if abs(T_new - T_surf) < tol:
            return T_surf, h_conv, h_rad, True

    return T_surf, h_conv, h_rad, False


# ----------------------------------------------------------------------
# RUN CASES
# ----------------------------------------------------------------------

def run():
    area = surface_area(L, W, H)

    print("=" * 74)
    print("PRELIMINARY THERMAL SCOPING - UAS AVIONICS ENCLOSURE")
    print("=" * 74)
    print(f"Heat load                 : {Q_TOTAL:.2f} W")
    print(f"Enclosure                 : {L*1000:.0f} x {W*1000:.0f} "
          f"x {H*1000:.0f} mm")
    print(f"External surface area     : {area:.4f} m^2")
    print(f"Ambient                   : {T_AMB:.1f} degC")
    print(f"Allowable (REQ-THM-001)   : {T_ALLOW_AMBIENT:.1f} degC")
    print()

    cases = [
        ("Hover,  bare Al",     V_HOVER,  EMISSIVITY_BARE),
        ("Hover,  anodized",    V_HOVER,  EMISSIVITY_ANODIZED),
        ("Cruise, bare Al",     V_CRUISE, EMISSIVITY_BARE),
        ("Cruise, anodized",    V_CRUISE, EMISSIVITY_ANODIZED),
    ]

    print(f"{'Case':<20} {'h_conv':>8} {'h_rad':>8} {'dT':>8} "
          f"{'T_surf':>9} {'Margin':>9} {'Status':>7}")
    print(f"{'':<20} {'W/m2K':>8} {'W/m2K':>8} {'degC':>8} "
          f"{'degC':>9} {'':>9} {'':>7}")
    print("-" * 74)

    results = {}
    for label, vel, eps in cases:
        T_surf, h_c, h_r, ok = solve_surface_temp(
            Q_TOTAL, area, vel, eps, T_AMB)
        dT = T_surf - T_AMB
        margin = (T_ALLOW_AMBIENT / T_surf) - 1.0
        status = "PASS" if T_surf <= T_ALLOW_AMBIENT else "FAIL"
        conv = "" if ok else "  (no conv.)"
        print(f"{label:<20} {h_c:>8.1f} {h_r:>8.1f} {dT:>8.1f} "
              f"{T_surf:>9.1f} {margin:>+9.2f} {status:>7}{conv}")
        results[label] = T_surf

    print("-" * 74)
    print()

    # Reynolds number for the cruise case
    _, Re = h_forced(V_CRUISE)
    print(f"Cruise Reynolds number    : {Re:,.0f}")
    if Re < 5e5:
        print("  Laminar. Flat-plate laminar correlation is appropriate.")
    else:
        print("  WARNING: transitional/turbulent. Laminar correlation invalid.")
    print()

    # Required area to close the binding case
    dT_allow = T_ALLOW_AMBIENT - T_AMB
    print(f"Available temperature rise: {dT_allow:.1f} degC")
    for label in ("Hover,  anodized", "Cruise, anodized"):
        T_s = results[label]
        h_eff = Q_TOTAL / ((T_s - T_AMB) * area)
        area_req = Q_TOTAL / (h_eff * dT_allow)
        ratio = area_req / area
        print(f"  {label:<18} area required = {area_req:.4f} m^2 "
              f"({ratio:.1f}x current)")
    print()

    print("NOTES")
    print("  - Lumped isothermal assumption. Internal air will run hotter than")
    print("    the computed surface temperature. Treat these as optimistic.")
    print("  - Radiation share at hover is substantial. Surface finish is a")
    print("    first-order design variable, not a detail.")
    print("  - Compare against thermal FEA. Divergence >30% needs explanation.")
    print("=" * 74)


if __name__ == "__main__":
    run()

