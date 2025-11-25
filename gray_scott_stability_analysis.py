#!/usr/bin/env python3
"""
Rigorous Linear Stability Analysis for Gray-Scott System
Derives the Turing instability boundary k(f) from first principles
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve, minimize_scalar

# Parameters
Du = 0.21
Dv = 0.105

def find_steady_state(f, k, max_iter=1000, tol=1e-10):
    """
    Find non-trivial steady state (U0, V0) for given f, k
    Solves:
        -U*V^2 + f*(1-U) = 0
        U*V^2 - (k+f)*V = 0
    """
    def equations(vars):
        U, V = vars
        if U <= 0 or V <= 0 or U > 1:
            return [1e10, 1e10]  # Penalize unphysical values

        eq1 = -U * V**2 + f * (1 - U)
        eq2 = U * V**2 - (k + f) * V
        return [eq1, eq2]

    # Initial guess: small V, U near 1
    U_init = 1 - (k + f)
    V_init = f / (k + f) if k + f > 0 else 0.01

    try:
        solution = fsolve(equations, [U_init, V_init], full_output=True)
        U0, V0 = solution[0]
        info = solution[1]

        # Check if solution converged and is physical
        if info['fvec'][0]**2 + info['fvec'][1]**2 < tol and U0 > 0 and V0 > 0 and U0 <= 1:
            return U0, V0
        else:
            return None, None
    except:
        return None, None

def jacobian_at_steady_state(U0, V0, f, k):
    """
    Compute Jacobian matrix at steady state (U0, V0)

    For F = -UV^2 + f(1-U), G = UV^2 - (k+f)V:

    J = [ ∂F/∂U   ∂F/∂V ]   [ -V0^2 - f      -2*U0*V0     ]
        [ ∂G/∂U   ∂G/∂V ] = [ V0^2           2*U0*V0-(k+f) ]
    """
    J11 = -V0**2 - f
    J12 = -2 * U0 * V0
    J21 = V0**2
    J22 = 2 * U0 * V0 - (k + f)

    return np.array([[J11, J12], [J21, J22]])

def dispersion_relation(q2, J, Du, Dv):
    """
    Compute eigenvalues of J - D*q^2

    Returns: (trace, determinant, max_real_eigenvalue)
    """
    # J - D*q^2
    J_q = J.copy()
    J_q[0, 0] -= Du * q2
    J_q[1, 1] -= Dv * q2

    trace = np.trace(J_q)
    det = np.linalg.det(J_q)

    # Eigenvalues from characteristic equation: λ^2 - trace*λ + det = 0
    discriminant = trace**2 - 4*det
    if discriminant >= 0:
        lambda1 = (trace + np.sqrt(discriminant)) / 2
        lambda2 = (trace - np.sqrt(discriminant)) / 2
        max_real = max(lambda1.real, lambda2.real)
    else:
        # Complex eigenvalues
        max_real = trace / 2

    return trace, det, max_real

def find_turing_boundary(f, k_range, tolerance=1e-6):
    """
    For given f, find critical k where Turing instability begins

    Turing condition:
    1. Homogeneous state stable: Tr(J) < 0, Det(J) > 0
    2. Spatial instability: max_q Re(λ(q)) > 0
    """
    for k in k_range:
        U0, V0 = find_steady_state(f, k)
        if U0 is None:
            continue

        J = jacobian_at_steady_state(U0, V0, f, k)

        # Check homogeneous stability
        trace_0 = J[0, 0] + J[1, 1]
        det_0 = np.linalg.det(J)

        if trace_0 >= 0 or det_0 <= 0:
            continue  # Homogeneous state unstable

        # Search over wavenumbers for instability
        q2_values = np.linspace(0.01, 100, 1000)
        max_real_eigenvalue = -np.inf

        for q2 in q2_values:
            _, _, max_real = dispersion_relation(q2, J, Du, Dv)
            if max_real > max_real_eigenvalue:
                max_real_eigenvalue = max_real

        # If any spatial mode is unstable, we found the boundary
        if max_real_eigenvalue > tolerance:
            return k

    return None

def compute_critical_q_squared(J, Du, Dv):
    """
    Find q^2 that minimizes Det(J - D*q^2)

    Det = Det(J) + [J11*Dv + J22*Du - Tr(J)*Du*Dv]*q^2 + Du*Dv*q^4

    Taking derivative: d(Det)/d(q^2) = 0
    2*Du*Dv*q^2 + [J11*Dv + J22*Du] = 0

    Actually, let me derive this carefully:

    J - D*q^2 = [ J11 - Du*q^2    J12          ]
                [ J21              J22 - Dv*q^2 ]

    Det = (J11 - Du*q^2)(J22 - Dv*q^2) - J12*J21
        = J11*J22 - J11*Dv*q^2 - J22*Du*q^2 + Du*Dv*q^4 - J12*J21
        = Det(J) - (J11*Dv + J22*Du)*q^2 + Du*Dv*q^4

    d(Det)/d(q^2) = -(J11*Dv + J22*Du) + 2*Du*Dv*q^2 = 0

    q^2_crit = (J11*Dv + J22*Du) / (2*Du*Dv)
    """
    J11, J22 = J[0, 0], J[1, 1]

    q2_crit = (J11 * Dv + J22 * Du) / (2 * Du * Dv)

    return q2_crit if q2_crit > 0 else 0

def turing_boundary_condition_direct(f, k):
    """
    Direct computation of Turing condition
    Returns True if parameters (f, k) are in the Turing region
    """
    U0, V0 = find_steady_state(f, k)
    if U0 is None:
        return False

    J = jacobian_at_steady_state(U0, V0, f, k)

    # Homogeneous stability
    trace_0 = np.trace(J)
    det_0 = np.linalg.det(J)

    if trace_0 >= 0 or det_0 <= 0:
        return False

    # Find critical q^2
    q2_crit = compute_critical_q_squared(J, Du, Dv)

    if q2_crit <= 0:
        return False

    # Check if Det(J - D*q^2) < 0 at critical q^2
    _, det_crit, _ = dispersion_relation(q2_crit, J, Du, Dv)

    return det_crit < 0

def main():
    """
    Main analysis: compute Turing boundary k(f) and compare to empirical
    """
    print("=" * 80)
    print("Gray-Scott Turing Instability Boundary - Theoretical Derivation")
    print("=" * 80)
    print(f"\nParameters: Du = {Du}, Dv = {Dv}, Du/Dv = {Du/Dv:.3f}")
    print(f"Empirical boundary: k ≈ -6.5*f^2 + 0.8*f + c")
    print("\n" + "=" * 80)

    # Compute boundary for range of f values
    f_values = np.linspace(0.01, 0.10, 50)
    k_boundary = []

    print("\nComputing Turing boundary k(f)...")
    print(f"{'f':>8} {'k_theory':>12} {'U0':>10} {'V0':>10}")
    print("-" * 45)

    for f in f_values:
        # Search for boundary k by scanning
        k_test_values = np.linspace(0.001, 0.15, 500)
        k_boundary_val = None

        # Find first k where Turing condition is satisfied
        for k in k_test_values:
            if turing_boundary_condition_direct(f, k):
                k_boundary_val = k
                break

        if k_boundary_val is not None:
            U0, V0 = find_steady_state(f, k_boundary_val)
            if U0 is not None:
                k_boundary.append(k_boundary_val)
                print(f"{f:8.4f} {k_boundary_val:12.6f} {U0:10.6f} {V0:10.6f}")
            else:
                k_boundary.append(np.nan)
        else:
            k_boundary.append(np.nan)

    # Fit polynomial to theoretical boundary
    f_valid = f_values[~np.isnan(k_boundary)]
    k_valid = np.array([k for k in k_boundary if not np.isnan(k)])

    if len(k_valid) > 3:
        # Fit quadratic: k = a*f^2 + b*f + c
        coeffs = np.polyfit(f_valid, k_valid, 2)
        a_theory, b_theory, c_theory = coeffs

        print("\n" + "=" * 80)
        print("THEORETICAL FIT: k(f) = a*f^2 + b*f + c")
        print("=" * 80)
        print(f"  a (coefficient of f^2): {a_theory:10.4f}")
        print(f"  b (coefficient of f):   {b_theory:10.4f}")
        print(f"  c (constant):           {c_theory:10.4f}")
        print("\n" + "=" * 80)
        print("COMPARISON TO EMPIRICAL: k ≈ -6.5*f^2 + 0.8*f + c")
        print("=" * 80)
        print(f"  a_empirical = -6.5,  a_theory = {a_theory:8.4f},  ratio = {a_theory/(-6.5):8.4f}")
        print(f"  b_empirical =  0.8,  b_theory = {b_theory:8.4f},  ratio = {b_theory/0.8:8.4f}")
        print("=" * 80)

        # Plot
        plt.figure(figsize=(12, 8))

        # Subplot 1: Boundary curves
        plt.subplot(2, 1, 1)
        plt.plot(f_valid, k_valid, 'bo-', label='Theoretical boundary', markersize=4)

        f_fine = np.linspace(f_valid.min(), f_valid.max(), 200)
        k_theory_fit = np.polyval(coeffs, f_fine)
        k_empirical = -6.5 * f_fine**2 + 0.8 * f_fine

        plt.plot(f_fine, k_theory_fit, 'r--', label=f'Theory fit: {a_theory:.2f}f² + {b_theory:.2f}f + {c_theory:.3f}', linewidth=2)
        plt.plot(f_fine, k_empirical, 'g--', label='Empirical: -6.5f² + 0.8f', linewidth=2)

        plt.xlabel('Feed rate f', fontsize=12)
        plt.ylabel('Kill rate k', fontsize=12)
        plt.title(f'Gray-Scott Turing Boundary (Du={Du}, Dv={Dv})', fontsize=14, fontweight='bold')
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)

        # Subplot 2: Residuals
        plt.subplot(2, 1, 2)
        k_theory_at_f = np.polyval(coeffs, f_valid)
        k_empirical_at_f = -6.5 * f_valid**2 + 0.8 * f_valid

        residual_theory = k_valid - k_theory_at_f
        residual_empirical = k_valid - k_empirical_at_f

        plt.plot(f_valid, residual_empirical, 'go-', label='Empirical residual', markersize=4)
        plt.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        plt.xlabel('Feed rate f', fontsize=12)
        plt.ylabel('Residual (k_computed - k_fit)', fontsize=12)
        plt.title('Fit Quality', fontsize=12)
        plt.legend(fontsize=10)
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('/Users/jacobcole/code/claude-mind/gray_scott_boundary_theory_vs_empirical.png', dpi=150, bbox_inches='tight')
        print(f"\nPlot saved to: /Users/jacobcole/code/claude-mind/gray_scott_boundary_theory_vs_empirical.png")

        # Additional analysis: steady state properties
        print("\n" + "=" * 80)
        print("STEADY STATE ANALYSIS at boundary")
        print("=" * 80)
        print(f"{'f':>8} {'k':>10} {'U0':>10} {'V0':>10} {'V0^2':>10} {'U0*V0':>10}")
        print("-" * 70)

        for f, k in zip(f_valid[::5], k_valid[::5]):  # Sample every 5th point
            U0, V0 = find_steady_state(f, k)
            if U0 is not None:
                print(f"{f:8.4f} {k:10.6f} {U0:10.6f} {V0:10.6f} {V0**2:10.6f} {U0*V0:10.6f}")

        print("\n" + "=" * 80)
        print("KEY INSIGHTS")
        print("=" * 80)

        # Check if theory matches empirical
        ratio_a = abs(a_theory / (-6.5))
        ratio_b = abs(b_theory / 0.8)

        if 0.8 < ratio_a < 1.2 and 0.8 < ratio_b < 1.2:
            print("✓ Theory MATCHES empirical coefficients within 20%!")
            print("  The empirical boundary is well-explained by linear stability analysis.")
        else:
            print("✗ Theory DIFFERS from empirical coefficients")
            print("  Possible reasons:")
            print("    1. Nonlinear effects beyond linear stability")
            print("    2. Numerical artifacts in empirical measurement")
            print("    3. Different definition of 'pattern boundary'")
            print("    4. Finite domain effects in simulations")

        print("\n" + "=" * 80)

    else:
        print("\nInsufficient data points to fit boundary")

if __name__ == "__main__":
    main()
