#!/usr/bin/env python3
"""
Final Gray-Scott Boundary Derivation

The key insight: We need to find where the NON-TRIVIAL steady state's
most unstable spatial mode crosses from stable to unstable.

The empirical boundary appears to be where stripe/spot patterns emerge from
a spatially perturbed state.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

Du = 0.21
Dv = 0.105

def find_nontrivial_steady_state(f, k):
    """
    Find NON-TRIVIAL steady state (U0 < 1, V0 > 0)

    From steady state equations:
        U*V^2 = f*(1-U)
        U*V^2 = (k+f)*V

    This gives: V = f*(1-U)/(k+f)
    And: U*[f*(1-U)/(k+f)]^2 = f*(1-U)

    Simplifying: U*f*(1-U)/(k+f)^2 = 1
                 U*(1-U) = (k+f)^2/f
    """
    # Solve U*(1-U) = (k+f)^2/f
    # U - U^2 = (k+f)^2/f
    # U^2 - U + (k+f)^2/f = 0

    if f <= 0:
        return None, None

    discriminant = 1 - 4*(k+f)**2/f

    if discriminant < 0:
        return None, None  # No real solution

    # Two solutions: take the smaller one (closer to bifurcation)
    U1 = (1 - np.sqrt(discriminant)) / 2
    U2 = (1 + np.sqrt(discriminant)) / 2

    # Choose the physical one (0 < U < 1)
    if 0 < U1 < 1:
        U0 = U1
    elif 0 < U2 < 1:
        U0 = U2
    else:
        return None, None

    V0 = f * (1 - U0) / (k + f)

    # Verify
    check1 = abs(U0 * V0**2 - f * (1 - U0))
    check2 = abs(U0 * V0**2 - (k + f) * V0)

    if check1 > 1e-8 or check2 > 1e-8:
        return None, None

    return U0, V0

def jacobian_at_steady_state(U0, V0, f, k):
    """Compute Jacobian matrix"""
    J11 = -V0**2 - f
    J12 = -2 * U0 * V0
    J21 = V0**2
    J22 = 2 * U0 * V0 - (k + f)

    return np.array([[J11, J12], [J21, J22]])

def dispersion_relation_explicit(f, k, q2):
    """
    Compute the dispersion relation analytically

    Returns the maximum eigenvalue (growth rate) as a function of q²
    """
    U0, V0 = find_nontrivial_steady_state(f, k)

    if U0 is None:
        return None

    J = jacobian_at_steady_state(U0, V0, f, k)

    # J - D*q²
    trace_q = J[0,0] - Du*q2 + J[1,1] - Dv*q2
    trace_q = J[0,0] + J[1,1] - (Du + Dv)*q2

    det_q = (J[0,0] - Du*q2)*(J[1,1] - Dv*q2) - J[0,1]*J[1,0]

    # Expand determinant
    det_q = J[0,0]*J[1,1] - J[0,1]*J[1,0] - (J[0,0]*Dv + J[1,1]*Du)*q2 + Du*Dv*q2**2

    # Maximum eigenvalue
    discriminant = trace_q**2 - 4*det_q

    if discriminant < 0:
        # Complex eigenvalues
        return trace_q / 2
    else:
        return (trace_q + np.sqrt(discriminant)) / 2

def find_critical_wavenumber(f, k):
    """
    Find q² that maximizes growth rate

    The growth rate as function of q² is:
    λ(q²) = [trace(J) - (Du+Dv)q² + sqrt((trace(J)-(Du+Dv)q²)² - 4*det(q²))] / 2

    To find maximum, we can use the fact that for Turing instability,
    the critical q² minimizes the determinant:

    det(q²) = det(J) - (J11*Dv + J22*Du)*q² + Du*Dv*q⁴

    d(det)/d(q²) = -(J11*Dv + J22*Du) + 2*Du*Dv*q² = 0

    q²_crit = (J11*Dv + J22*Du) / (2*Du*Dv)
    """
    U0, V0 = find_nontrivial_steady_state(f, k)

    if U0 is None:
        return None

    J = jacobian_at_steady_state(U0, V0, f, k)

    q2_crit = (J[0,0]*Dv + J[1,1]*Du) / (2*Du*Dv)

    return q2_crit if q2_crit > 0 else 0

def max_growth_rate(f, k):
    """Find maximum growth rate over all q²"""
    q2_crit = find_critical_wavenumber(f, k)

    if q2_crit is None:
        return None, None

    gr = dispersion_relation_explicit(f, k, q2_crit)

    return gr, q2_crit

def compute_boundary():
    """
    Compute the pattern boundary by finding where max growth rate = 0
    """
    print("=" * 80)
    print("GRAY-SCOTT PATTERN BOUNDARY: ANALYTICAL DERIVATION")
    print("=" * 80)
    print(f"\nParameters: Du = {Du}, Dv = {Dv}")
    print("\nComputing boundary where Re(λ_max) = 0 for non-trivial steady state")
    print("=" * 80)

    # Strategy: For each f, scan k to find where max_growth_rate ≈ 0
    f_values = np.linspace(0.01, 0.08, 50)
    k_boundary = []
    q2_critical = []
    steady_states = []

    print(f"\n{'f':>8} {'k':>10} {'max_gr':>10} {'q²_crit':>10} {'U0':>10} {'V0':>10}")
    print("-" * 70)

    for f in f_values:
        # Scan k values
        k_values = np.linspace(0.03, 0.10, 300)

        k_found = None
        q2_found = None
        gr_closest = np.inf

        for k in k_values:
            gr, q2 = max_growth_rate(f, k)

            if gr is None:
                continue

            # Find where growth rate crosses zero
            if abs(gr) < abs(gr_closest):
                gr_closest = gr
                k_found = k
                q2_found = q2

        if k_found is not None and abs(gr_closest) < 0.005:  # Close enough to zero
            U0, V0 = find_nontrivial_steady_state(f, k_found)

            if U0 is not None and V0 > 0.01:  # Significant V (not trivial state)
                k_boundary.append(k_found)
                q2_critical.append(q2_found)
                steady_states.append((U0, V0))

                print(f"{f:8.4f} {k_found:10.6f} {gr_closest:+10.6f} {q2_found:10.4f} {U0:10.6f} {V0:10.6f}")
            else:
                k_boundary.append(np.nan)
                q2_critical.append(np.nan)
                steady_states.append((None, None))
        else:
            k_boundary.append(np.nan)
            q2_critical.append(np.nan)
            steady_states.append((None, None))

    # Fit polynomial
    f_valid_mask = ~np.isnan(k_boundary)
    f_valid = f_values[f_valid_mask]
    k_valid = np.array(k_boundary)[f_valid_mask]

    if len(k_valid) > 5:
        # Fit quadratic
        coeffs = np.polyfit(f_valid, k_valid, 2)
        a, b, c = coeffs

        print("\n" + "=" * 80)
        print("THEORETICAL BOUNDARY FIT: k(f) = a*f² + b*f + c")
        print("=" * 80)
        print(f"  a = {a:10.4f}")
        print(f"  b = {b:10.4f}")
        print(f"  c = {c:10.4f}")

        print("\n" + "=" * 80)
        print("COMPARISON TO EMPIRICAL: k ≈ -6.5*f² + 0.8*f")
        print("=" * 80)
        print(f"  a_empirical = -6.5,  a_theory = {a:8.4f},  ratio = {a/(-6.5):8.4f}")
        print(f"  b_empirical =  0.8,  b_theory = {b:8.4f},  ratio = {b/0.8:8.4f}")

        # R²
        k_pred = np.polyval(coeffs, f_valid)
        r2 = 1 - np.sum((k_valid - k_pred)**2) / np.sum((k_valid - np.mean(k_valid))**2)
        print(f"\n  R² = {r2:.6f}")
        print("=" * 80)

        # Plot
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))

        # Boundary
        ax = axes[0]
        ax.plot(f_valid, k_valid, 'bo-', label='Theoretical boundary', markersize=5)

        f_fine = np.linspace(f_valid.min(), f_valid.max(), 200)
        k_theory = np.polyval(coeffs, f_fine)
        k_empirical = -6.5 * f_fine**2 + 0.8 * f_fine

        ax.plot(f_fine, k_theory, 'r--', label=f'Theory: {a:.2f}f² + {b:.2f}f + {c:.4f}', linewidth=2)
        ax.plot(f_fine, k_empirical, 'g--', label='Empirical: -6.5f² + 0.8f', linewidth=2)

        ax.set_xlabel('Feed rate f', fontsize=12)
        ax.set_ylabel('Kill rate k', fontsize=12)
        ax.set_title(f'Gray-Scott Pattern Boundary (Du={Du}, Dv={Dv})', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

        # Difference
        ax = axes[1]
        k_emp_at_f = -6.5 * f_valid**2 + 0.8 * f_valid
        diff = k_valid - k_emp_at_f

        ax.plot(f_valid, diff, 'ro-', markersize=5)
        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax.set_xlabel('Feed rate f', fontsize=12)
        ax.set_ylabel('k_theory - k_empirical', fontsize=12)
        ax.set_title('Difference', fontsize=12)
        ax.grid(True, alpha=0.3)

        # Critical wavelength
        ax = axes[2]
        q2_valid = np.array(q2_critical)[f_valid_mask]
        q2_valid = q2_valid[~np.isnan(q2_valid)]
        wavelength = 2 * np.pi / np.sqrt(q2_valid[q2_valid > 0])
        f_wavelength = f_valid[:len(wavelength)]

        if len(wavelength) > 0:
            ax.plot(f_wavelength, wavelength, 'mo-', markersize=5)
            ax.set_xlabel('Feed rate f', fontsize=12)
            ax.set_ylabel('Critical wavelength', fontsize=12)
            ax.set_title('Pattern wavelength at boundary', fontsize=12)
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('/Users/jacobcole/code/claude-mind/gray_scott_final_boundary.png',
                   dpi=150, bbox_inches='tight')
        print(f"\nPlot saved to: gray_scott_final_boundary.png")

    else:
        print("\nInsufficient data points for fit")

if __name__ == "__main__":
    compute_boundary()
