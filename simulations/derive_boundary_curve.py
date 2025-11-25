#!/usr/bin/env python3
"""
Derive the THEORETICAL BOUNDARY CURVE k(f) from Linear Stability Analysis
and compare with simulation.

The boundary where patterns disappear should correspond to where the
Turing instability disappears. This happens when:
1. The homogeneous state becomes linearly stable with diffusion, OR
2. The nonlinear pattern amplitude goes to zero

A quantitative comparison could reveal:
- How well LSA predicts the actual boundary
- Whether there are systematic deviations
- The nature of the bifurcation (supercritical vs subcritical offset)

THEORETICAL DERIVATION:
For Gray-Scott: U + V² - UV² = 0, (f+k)V - UV² = 0
Homogeneous steady state: U₀ = (f+k)/V₀, V₀² = f(1 - U₀) = f(1 - (f+k)/V₀)
=> V₀³ - fV₀ + f(f+k) = 0

The Jacobian at (U₀, V₀) is:
J = [[-f - V₀², -2U₀V₀],
     [V₀², 2U₀V₀ - (f+k)]]

With diffusion, the stability matrix for mode q is:
M(q) = J - q²[Du, 0; 0, Dv]

Turing instability requires det(M(q)) < 0 for some q > 0.
"""

import numpy as np
import json

Du, Dv = 0.16, 0.08
N = 64
dx = 1.0

def laplacian(Z, dx):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z) / (dx*dx)

def step(U, V, f, k):
    uvv = U * V * V
    return (np.clip(U + Du * laplacian(U, dx) - uvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv - (k + f) * V, 0, 1))

# =============================================================================
# THEORETICAL ANALYSIS
# =============================================================================

def find_steady_state(f, k):
    """
    Find the non-trivial homogeneous steady state.
    V³ - fV + f(f+k) = 0
    """
    # Coefficients of V³ - fV + f(f+k) = 0
    # i.e., V³ + 0*V² - f*V + f(f+k) = 0
    coeffs = [1, 0, -f, f*(f+k)]
    roots = np.roots(coeffs)

    # Find real positive root
    real_roots = [r.real for r in roots if abs(r.imag) < 1e-10 and r.real > 0]

    if not real_roots:
        return None, None

    V0 = max(real_roots)  # Take the larger root (stable pattern state)
    U0 = (f + k) / V0

    # Check validity
    if U0 < 0 or U0 > 1 or V0 < 0:
        return None, None

    return U0, V0

def check_turing_instability(f, k):
    """
    Check if Turing instability exists at (f, k).
    Returns (is_unstable, critical_q, max_growth_rate)
    """
    U0, V0 = find_steady_state(f, k)
    if U0 is None:
        return False, 0, 0

    # Jacobian elements
    a = -f - V0**2
    b = -2 * U0 * V0
    c = V0**2
    d = 2 * U0 * V0 - (f + k)

    # For Turing: we need tr(J) < 0 and det(J) > 0 (stable without diffusion)
    # But det(M(q)) < 0 for some q > 0

    tr_J = a + d
    det_J = a * d - b * c

    if tr_J > 0 or det_J < 0:
        # Unstable without diffusion - not Turing pattern
        return False, 0, 0

    # Find q that minimizes det(M(q))
    # det(M(q)) = (a - Du*q²)(d - Dv*q²) - bc
    # = Du*Dv*q⁴ - (a*Dv + d*Du)*q² + (ad - bc)
    # = Du*Dv*q⁴ - (a*Dv + d*Du)*q² + det_J

    # Minimum at q² = (a*Dv + d*Du) / (2*Du*Dv)
    q2_min = (a * Dv + d * Du) / (2 * Du * Dv)

    if q2_min < 0:
        # Minimum is at q=0, no Turing instability
        return False, 0, 0

    q_min = np.sqrt(q2_min)

    # Value at minimum
    det_min = Du * Dv * q2_min**2 - (a * Dv + d * Du) * q2_min + det_J

    if det_min < 0:
        # Turing unstable!
        # Growth rate is -Re(eigenvalue), proportional to -det_min
        return True, q_min, -det_min
    else:
        return False, q_min, -det_min

def find_theoretical_boundary(f, k_range=np.arange(0.04, 0.08, 0.001)):
    """Find the k value where Turing instability disappears at given f."""
    k_boundary = None

    for k in k_range:
        is_unstable, _, _ = check_turing_instability(f, k)
        if is_unstable and k_boundary is None:
            k_boundary = k
        elif not is_unstable and k_boundary is not None:
            # Just crossed from unstable to stable
            return (k_boundary + k) / 2

    return k_boundary

# =============================================================================
# SIMULATION
# =============================================================================

def init_nucleated(N):
    U, V = np.ones((N, N)), np.zeros((N, N))
    np.random.seed(42)
    for _ in range(5):
        cx, cy = np.random.randint(N//4, 3*N//4, 2)
        r = 3
        y, x = np.ogrid[:N, :N]
        mask = (x-cx)**2 + (y-cy)**2 <= r*r
        U[mask], V[mask] = 0.5, 0.25
    return U, V

def find_simulation_boundary(f, k_range, n_steps=30000):
    """Find the k value where patterns disappear in simulation."""
    k_boundary = None

    for k in k_range:
        U, V = init_nucleated(N)
        for _ in range(n_steps):
            U, V = step(U, V, f, k)

        has_pattern = np.std(V) > 0.02

        if has_pattern and k_boundary is None:
            k_boundary = k
        elif not has_pattern and k_boundary is not None:
            return (k_boundary + k) / 2

    return k_boundary

# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 70)
    print("BOUNDARY CURVE: THEORY vs SIMULATION")
    print("=" * 70)
    print()
    print("Comparing LSA-predicted boundary with simulation...")
    print()

    f_values = np.arange(0.020, 0.056, 0.004)

    results = []

    print(f"{'f':>6} {'k_theory':>10} {'k_sim':>10} {'difference':>12} {'ratio':>8}")
    print("-" * 50)

    for f in f_values:
        k_theory = find_theoretical_boundary(f)
        k_sim = find_simulation_boundary(f, np.arange(0.045, 0.075, 0.001))

        if k_theory and k_sim:
            diff = k_sim - k_theory
            ratio = k_sim / k_theory
            print(f"{f:6.3f} {k_theory:10.4f} {k_sim:10.4f} {diff:+12.4f} {ratio:8.3f}")
            results.append({
                'f': float(f),
                'k_theory': float(k_theory),
                'k_sim': float(k_sim),
                'difference': float(diff),
                'ratio': float(ratio)
            })
        elif k_theory:
            print(f"{f:6.3f} {k_theory:10.4f} {'N/A':>10} {'N/A':>12} {'N/A':>8}")
            results.append({
                'f': float(f),
                'k_theory': float(k_theory),
                'k_sim': None,
                'difference': None,
                'ratio': None
            })
        else:
            print(f"{f:6.3f} {'N/A':>10} {k_sim if k_sim else 'N/A':>10}")
            results.append({
                'f': float(f),
                'k_theory': None,
                'k_sim': float(k_sim) if k_sim else None,
                'difference': None,
                'ratio': None
            })

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    valid_results = [r for r in results if r['difference'] is not None]

    if len(valid_results) >= 2:
        diffs = [r['difference'] for r in valid_results]
        ratios = [r['ratio'] for r in valid_results]

        mean_diff = np.mean(diffs)
        std_diff = np.std(diffs)
        mean_ratio = np.mean(ratios)

        print(f"Mean difference (k_sim - k_theory): {mean_diff:+.4f} ± {std_diff:.4f}")
        print(f"Mean ratio (k_sim / k_theory): {mean_ratio:.3f}")
        print()

        if mean_diff > 0.002:
            print("Simulation boundary is HIGHER than LSA predicts.")
            print("This indicates subcritical bifurcation: patterns exist beyond")
            print("the linear instability boundary due to nonlinear hysteresis.")
        elif mean_diff < -0.002:
            print("Simulation boundary is LOWER than LSA predicts.")
            print("This is unexpected and could indicate numerical issues or")
            print("that patterns are less stable than theory predicts.")
        else:
            print("Theory and simulation boundaries are close.")
            print("The bifurcation appears nearly supercritical at this scale.")

        # Check for systematic trend
        f_vals = [r['f'] for r in valid_results]
        if len(f_vals) >= 3:
            corr = np.corrcoef(f_vals, diffs)[0, 1]
            print()
            print(f"Correlation of difference with f: {corr:.3f}")
            if abs(corr) > 0.7:
                if corr > 0:
                    print("The offset INCREASES with f - the subcritical gap widens")
                else:
                    print("The offset DECREASES with f - approaching supercritical")

    # Save results
    with open('boundary_curve_results.json', 'w') as file:
        json.dump({
            'results': results,
            'mean_difference': float(mean_diff) if valid_results else None,
            'mean_ratio': float(mean_ratio) if valid_results else None
        }, file, indent=2)

    print()
    print("Results saved to boundary_curve_results.json")

if __name__ == '__main__':
    main()
