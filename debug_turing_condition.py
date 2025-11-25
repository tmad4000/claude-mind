#!/usr/bin/env python3
"""
Debug: Why isn't the Turing condition being satisfied at lower f values?
"""

import numpy as np
from scipy.optimize import fsolve

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

    U_init = 1 - (k + f)
    V_init = f / (k + f) if k + f > 0 else 0.01

    try:
        solution = fsolve(equations, [U_init, V_init], full_output=True)
        U0, V0 = solution[0]
        info = solution[1]

        if info['fvec'][0]**2 + info['fvec'][1]**2 < 1e-10 and U0 > 0 and V0 > 0 and U0 <= 1:
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

def check_turing_detailed(f, k):
    """Detailed check of Turing conditions"""
    U0, V0 = find_steady_state(f, k)

    if U0 is None:
        return None

    J = jacobian_at_steady_state(U0, V0, f, k)

    # Homogeneous stability
    trace_0 = np.trace(J)
    det_0 = np.linalg.det(J)

    # Eigenvalues at q=0
    disc = trace_0**2 - 4*det_0
    if disc >= 0:
        lambda1 = (trace_0 + np.sqrt(disc)) / 2
        lambda2 = (trace_0 - np.sqrt(disc)) / 2
    else:
        lambda1 = trace_0 / 2  # Real part
        lambda2 = trace_0 / 2

    # Critical q^2
    J11, J22 = J[0, 0], J[1, 1]
    q2_crit = (J11 * Dv + J22 * Du) / (2 * Du * Dv)

    # Determinant at critical q^2
    if q2_crit > 0:
        det_crit = det_0 - (J11 * Dv + J22 * Du) * q2_crit + Du * Dv * q2_crit**2

        # This should simplify!
        # det_crit = det_0 - [(J11*Dv + J22*Du)^2] / (4*Du*Dv)
        det_crit_simplified = det_0 - (J11 * Dv + J22 * Du)**2 / (4 * Du * Dv)
    else:
        det_crit = det_0
        det_crit_simplified = det_0

    return {
        'U0': U0, 'V0': V0,
        'trace_0': trace_0, 'det_0': det_0,
        'lambda1': lambda1, 'lambda2': lambda2,
        'homogeneous_stable': trace_0 < 0 and det_0 > 0,
        'q2_crit': q2_crit,
        'det_crit': det_crit_simplified,
        'turing_unstable': q2_crit > 0 and det_crit_simplified < 0 and trace_0 < 0 and det_0 > 0,
        'J11': J[0,0], 'J12': J[1,0], 'J21': J[0,1], 'J22': J[1,1]
    }

# Test at known pattern-forming parameters
print("=" * 80)
print("DEBUGGING TURING CONDITION")
print("=" * 80)

test_cases = [
    (0.02, 0.045, "Known pattern (mitosis)"),
    (0.02, 0.055, "Known pattern (spots)"),
    (0.03, 0.055, "Known pattern"),
    (0.04, 0.060, "Likely pattern"),
    (0.05, 0.062, "Higher f"),
    (0.063, 0.062, "Where theory found it"),
]

for f, k, desc in test_cases:
    result = check_turing_detailed(f, k)

    if result is None:
        print(f"\nf={f:.3f}, k={k:.3f} ({desc}): NO STEADY STATE")
        continue

    print(f"\nf={f:.3f}, k={k:.3f} ({desc}):")
    print(f"  Steady state: U0={result['U0']:.4f}, V0={result['V0']:.4f}")
    print(f"  Jacobian at (0,0): trace={result['trace_0']:.4f}, det={result['det_0']:.4f}")
    print(f"  Eigenvalues: λ1={result['lambda1']:.4f}, λ2={result['lambda2']:.4f}")
    print(f"  Homogeneous stable? {result['homogeneous_stable']}")
    print(f"  Critical q²={result['q2_crit']:.4f}")
    print(f"  Det at critical q²={result['det_crit']:.6f}")
    print(f"  TURING UNSTABLE? {result['turing_unstable']}")

print("\n" + "=" * 80)
print("ANALYTICAL INVESTIGATION")
print("=" * 80)

# Look at the Turing condition more carefully
print("\nTuring condition: Det(J - Dq²) < 0 for some q²")
print("At critical q²: Det = Det(J) - (J11*Dv + J22*Du)² / (4*Du*Dv)")
print("\nFor instability: Det(J) < (J11*Dv + J22*Du)² / (4*Du*Dv)")
print("\nLet's check if this holds for known pattern parameters...")

for f, k, desc in test_cases:
    result = check_turing_detailed(f, k)
    if result is None:
        continue

    LHS = result['det_0']
    RHS = (result['J11'] * Dv + result['J22'] * Du)**2 / (4 * Du * Dv)

    print(f"\nf={f:.3f}, k={k:.3f}: Det(J)={LHS:.6f}, Threshold={RHS:.6f}, Ratio={LHS/RHS:.3f}")
    print(f"  Condition satisfied? {LHS < RHS} (need LHS < RHS)")
