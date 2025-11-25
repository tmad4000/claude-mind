#!/usr/bin/env python3
"""
Corrected Gray-Scott Stability Analysis

Key insight: The pattern boundary is NOT the classical Turing condition.
Instead, it's where spatial modes become unstable while homogeneous state
may already be unstable.

The boundary is where max_q Re(λ(q)) = 0, transitioning from stable to unstable.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve, brentq

Du = 0.21
Dv = 0.105

def find_steady_state(f, k):
    """Find non-trivial steady state"""
    def equations(vars):
        U, V = vars
        if U <= 0 or V <= 0 or U > 1:
            return [1e10, 1e10]

        eq1 = -U * V**2 + f * (1 - U)
        eq2 = U * V**2 - (k + f) * V
        return [eq1, eq2]

    U_init = max(0.1, 1 - (k + f))
    V_init = f / max(k + f, 0.001)

    try:
        solution = fsolve(equations, [U_init, V_init], full_output=True)
        U0, V0 = solution[0]
        info = solution[1]

        if info['fvec'][0]**2 + info['fvec'][1]**2 < 1e-10 and 0 < U0 <= 1 and V0 > 0:
            return U0, V0
        else:
            return None, None
    except:
        return None, None

def jacobian_at_steady_state(U0, V0, f, k):
    """Compute Jacobian"""
    J11 = -V0**2 - f
    J12 = -2 * U0 * V0
    J21 = V0**2
    J22 = 2 * U0 * V0 - (k + f)

    return np.array([[J11, J12], [J21, J22]])

def max_growth_rate(f, k, q2_range=None):
    """
    Find maximum growth rate over all wavenumbers q²

    Returns: (max_growth_rate, critical_q2)
    """
    U0, V0 = find_steady_state(f, k)
    if U0 is None:
        return None, None

    J = jacobian_at_steady_state(U0, V0, f, k)

    if q2_range is None:
        # Smart range: focus around critical point
        J11, J22 = J[0, 0], J[1, 1]
        q2_crit = (J11 * Dv + J22 * Du) / (2 * Du * Dv)
        q2_range = np.linspace(max(0, q2_crit - 2), q2_crit + 2, 1000)

    max_gr = -np.inf
    max_q2 = 0

    for q2 in q2_range:
        # J - D*q²
        J_q = J.copy()
        J_q[0, 0] -= Du * q2
        J_q[1, 1] -= Dv * q2

        trace = np.trace(J_q)
        det = np.linalg.det(J_q)

        # Maximum eigenvalue (growth rate)
        discriminant = trace**2 - 4*det
        if discriminant >= 0:
            gr = (trace + np.sqrt(discriminant)) / 2
        else:
            gr = trace / 2

        if gr > max_gr:
            max_gr = gr
            max_q2 = q2

    return max_gr, max_q2

def find_pattern_boundary(f, k_range=None, tolerance=1e-5):
    """
    Find boundary k where max growth rate crosses zero

    Returns k where max_q Re(λ(q)) ≈ 0
    """
    if k_range is None:
        k_range = (0.001, 0.15)

    k_min, k_max = k_range

    # Check endpoints
    gr_min, _ = max_growth_rate(f, k_min)
    gr_max, _ = max_growth_rate(f, k_max)

    if gr_min is None or gr_max is None:
        return None

    # If both same sign, no crossing
    if gr_min * gr_max > 0:
        return None

    # Binary search for zero crossing
    def growth_at_k(k):
        gr, _ = max_growth_rate(f, k)
        return gr if gr is not None else np.inf

    try:
        k_boundary = brentq(growth_at_k, k_min, k_max, xtol=tolerance)
        return k_boundary
    except:
        return None

def main():
    print("=" * 80)
    print("CORRECTED Gray-Scott Pattern Boundary Analysis")
    print("=" * 80)
    print(f"\nParameters: Du = {Du}, Dv = {Dv}")
    print("\nSearching for boundary where max_q Re(λ(q)) = 0")
    print("This is where spatial instability emerges.\n")
    print("=" * 80)

    # Compute boundary
    f_values = np.linspace(0.015, 0.10, 40)
    k_boundary = []
    max_q2_values = []

    print(f"\n{'f':>8} {'k_boundary':>12} {'max_q²':>10} {'U0':>10} {'V0':>10}")
    print("-" * 60)

    for f in f_values:
        k_b = find_pattern_boundary(f)

        if k_b is not None:
            gr, q2 = max_growth_rate(f, k_b)
            U0, V0 = find_steady_state(f, k_b)

            k_boundary.append(k_b)
            max_q2_values.append(q2)

            print(f"{f:8.4f} {k_b:12.6f} {q2:10.4f} {U0:10.6f} {V0:10.6f}")
        else:
            k_boundary.append(np.nan)
            max_q2_values.append(np.nan)

    # Fit polynomial
    f_valid = f_values[~np.isnan(k_boundary)]
    k_valid = np.array([k for k in k_boundary if not np.isnan(k)])

    if len(k_valid) > 3:
        # Fit quadratic
        coeffs = np.polyfit(f_valid, k_valid, 2)
        a_theory, b_theory, c_theory = coeffs

        print("\n" + "=" * 80)
        print("THEORETICAL FIT: k(f) = a*f² + b*f + c")
        print("=" * 80)
        print(f"  a = {a_theory:10.4f}")
        print(f"  b = {b_theory:10.4f}")
        print(f"  c = {c_theory:10.4f}")

        print("\n" + "=" * 80)
        print("COMPARISON TO EMPIRICAL: k ≈ -6.5*f² + 0.8*f")
        print("=" * 80)
        print(f"  a_empirical = -6.5,  a_theory = {a_theory:8.4f},  ratio = {a_theory/(-6.5):8.4f}")
        print(f"  b_empirical =  0.8,  b_theory = {b_theory:8.4f},  ratio = {b_theory/0.8:8.4f}")

        # Calculate R² for fit quality
        k_predicted = np.polyval(coeffs, f_valid)
        ss_res = np.sum((k_valid - k_predicted)**2)
        ss_tot = np.sum((k_valid - np.mean(k_valid))**2)
        r_squared = 1 - (ss_res / ss_tot)
        print(f"\n  R² = {r_squared:.6f}")

        print("=" * 80)

        # Detailed comparison at specific points
        print("\nDETAILED COMPARISON at specific f values:")
        print(f"{'f':>8} {'k_theory':>12} {'k_empirical':>12} {'difference':>12}")
        print("-" * 48)

        test_f = [0.02, 0.03, 0.04, 0.05, 0.06]
        for f in test_f:
            if f_valid.min() <= f <= f_valid.max():
                k_th = np.polyval(coeffs, f)
                k_emp = -6.5 * f**2 + 0.8 * f
                diff = k_th - k_emp
                print(f"{f:8.4f} {k_th:12.6f} {k_emp:12.6f} {diff:+12.6f}")

        # Plot
        plt.figure(figsize=(14, 10))

        # Subplot 1: Boundary comparison
        plt.subplot(3, 1, 1)
        plt.plot(f_valid, k_valid, 'bo-', label='Theoretical boundary', markersize=5, linewidth=1.5)

        f_fine = np.linspace(f_valid.min(), f_valid.max(), 200)
        k_theory_fit = np.polyval(coeffs, f_fine)
        k_empirical = -6.5 * f_fine**2 + 0.8 * f_fine

        plt.plot(f_fine, k_theory_fit, 'r--',
                label=f'Theory fit: {a_theory:.2f}f² + {b_theory:.2f}f + {c_theory:.4f}', linewidth=2)
        plt.plot(f_fine, k_empirical, 'g--', label='Empirical: -6.5f² + 0.8f', linewidth=2)

        plt.xlabel('Feed rate f', fontsize=12)
        plt.ylabel('Kill rate k', fontsize=12)
        plt.title(f'Gray-Scott Pattern Boundary (Du={Du}, Dv={Dv})', fontsize=14, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)

        # Subplot 2: Difference
        plt.subplot(3, 1, 2)
        k_empirical_at_f = -6.5 * f_valid**2 + 0.8 * f_valid
        difference = k_valid - k_empirical_at_f

        plt.plot(f_valid, difference, 'ro-', markersize=5, linewidth=1.5)
        plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        plt.xlabel('Feed rate f', fontsize=12)
        plt.ylabel('k_theory - k_empirical', fontsize=12)
        plt.title('Difference between Theory and Empirical', fontsize=12)
        plt.grid(True, alpha=0.3)

        # Subplot 3: Critical wavelength
        plt.subplot(3, 1, 3)
        q2_valid = np.array([q for q in max_q2_values if not np.isnan(q)])
        wavelength = 2 * np.pi / np.sqrt(q2_valid)

        plt.plot(f_valid, wavelength, 'mo-', markersize=5, linewidth=1.5)
        plt.xlabel('Feed rate f', fontsize=12)
        plt.ylabel('Critical wavelength λ_c', fontsize=12)
        plt.title('Pattern wavelength at boundary', fontsize=12)
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('/Users/jacobcole/code/claude-mind/gray_scott_corrected_boundary.png',
                   dpi=150, bbox_inches='tight')
        print(f"\nPlot saved to: /Users/jacobcole/code/claude-mind/gray_scott_corrected_boundary.png")

if __name__ == "__main__":
    main()
