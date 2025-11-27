#!/usr/bin/env python3
"""
Boolean Function Analysis of ECA Rules

This script analyzes chaotic ECA rules using concepts from Boolean function theory
and cryptography to understand WHY 4-ones creates chaos.

Key properties to analyze:
1. Nonlinearity - distance from nearest linear/affine function
2. Algebraic degree - degree of ANF (algebraic normal form)
3. Propagation criteria - how changes propagate
4. Correlation immunity - statistical independence from input subsets
"""

import numpy as np
from itertools import combinations

# The 12 chaotic rules (all have 4 ones in binary)
CHAOTIC_RULES = [30, 45, 75, 86, 89, 101, 106, 120, 135, 149, 150, 105]

# All balanced rules (4 ones in binary)
def get_balanced_rules():
    """Get all 70 balanced rules (exactly 4 ones in 8-bit table)"""
    return [r for r in range(256) if bin(r).count('1') == 4]

def rule_to_table(rule):
    """Convert rule number to lookup table"""
    return [(rule >> i) & 1 for i in range(8)]

def table_to_truth_vector(table):
    """Convert table to truth vector (same, just named clearly)"""
    return np.array(table)

def compute_anf(table):
    """
    Compute Algebraic Normal Form (ANF) coefficients.
    ANF: f(x1,x2,x3) = a0 + a1*x1 + a2*x2 + a3*x3 + a12*x1*x2 + a13*x1*x3 + a23*x2*x3 + a123*x1*x2*x3
    Uses Mobius transform.
    """
    n = 3  # 3 input bits for ECA
    f = np.array(table, dtype=np.int64)
    anf = f.copy()

    for i in range(n):
        for j in range(2**n):
            if (j >> i) & 1:
                anf[j] ^= anf[j ^ (1 << i)]

    return anf

def algebraic_degree(anf):
    """Compute algebraic degree from ANF coefficients"""
    max_deg = 0
    for i, coef in enumerate(anf):
        if coef:
            deg = bin(i).count('1')
            max_deg = max(max_deg, deg)
    return max_deg

def walsh_hadamard_transform(table):
    """
    Compute Walsh-Hadamard transform of Boolean function.
    W_f(w) = sum_x (-1)^(f(x) + w·x)
    """
    n = 3
    f = np.array(table)
    W = np.zeros(2**n)

    for w in range(2**n):
        total = 0
        for x in range(2**n):
            # Compute w·x (dot product mod 2)
            dot = bin(w & x).count('1') % 2
            total += (-1) ** (f[x] ^ dot)
        W[w] = total

    return W

def nonlinearity(table):
    """
    Compute nonlinearity: distance from nearest affine function.
    nl(f) = 2^(n-1) - max|W_f(w)|/2
    """
    W = walsh_hadamard_transform(table)
    n = 3
    return int(2**(n-1) - np.max(np.abs(W))/2)

def correlation_immunity_order(table):
    """
    Check correlation immunity order.
    A function is CI(k) if all Walsh coefficients W_f(w) = 0 for 0 < wt(w) <= k.
    """
    W = walsh_hadamard_transform(table)
    for k in range(1, 4):
        all_zero = True
        for w in range(1, 8):
            if bin(w).count('1') <= k:
                if W[w] != 0:
                    all_zero = False
                    break
        if not all_zero:
            return k - 1
    return 3

def propagation_criteria(table):
    """
    Check strict avalanche criterion (SAC) and propagation criterion (PC).
    SAC: flipping any input bit flips output with probability 0.5
    PC(k): any combination of k input bits satisfies SAC
    """
    n = 3
    f = np.array(table)

    # Check each input bit
    sac_satisfied = []
    for i in range(n):
        flips = 0
        for x in range(2**n):
            x_flipped = x ^ (1 << i)
            if f[x] != f[x_flipped]:
                flips += 1
        sac_satisfied.append(flips == 4)  # Should flip half the time

    return {
        'sac_bits': sac_satisfied,
        'sac_all': all(sac_satisfied),
        'sac_count': sum(sac_satisfied)
    }

def compute_derivative(table, direction):
    """
    Compute Boolean derivative D_a(f)(x) = f(x) XOR f(x+a)
    where direction 'a' specifies which inputs flip.
    """
    f = np.array(table)
    deriv = np.zeros(8, dtype=int)
    for x in range(8):
        deriv[x] = f[x] ^ f[x ^ direction]
    return deriv

def analyze_rule(rule):
    """Comprehensive Boolean function analysis of an ECA rule"""
    table = rule_to_table(rule)
    anf = compute_anf(table)
    W = walsh_hadamard_transform(table)

    analysis = {
        'rule': rule,
        'table': table,
        'ones_count': sum(table),
        'anf_coefficients': anf.tolist(),
        'algebraic_degree': algebraic_degree(anf),
        'nonlinearity': nonlinearity(table),
        'walsh_spectrum': W.tolist(),
        'walsh_max': int(np.max(np.abs(W))),
        'correlation_immunity': correlation_immunity_order(table),
        'propagation': propagation_criteria(table),
        'is_chaotic': rule in CHAOTIC_RULES
    }

    # Compute derivatives
    derivs = {}
    for d in [1, 2, 4]:  # Single bit flips
        deriv = compute_derivative(table, d)
        derivs[f'd{d}'] = deriv.tolist()
        derivs[f'd{d}_ones'] = sum(deriv)

    # Combined flips
    for d in [3, 5, 6, 7]:
        deriv = compute_derivative(table, d)
        derivs[f'd{d}_ones'] = sum(deriv)

    analysis['derivatives'] = derivs

    return analysis

def main():
    print("=" * 70)
    print("BOOLEAN FUNCTION ANALYSIS OF ECA RULES")
    print("Investigating WHY 4-ones creates chaos")
    print("=" * 70)

    # Get all balanced rules
    balanced_rules = get_balanced_rules()
    print(f"\nTotal balanced rules (4 ones): {len(balanced_rules)}")
    print(f"Chaotic rules: {len(CHAOTIC_RULES)}")

    # Analyze all balanced rules
    chaotic_analysis = []
    periodic_analysis = []

    for rule in balanced_rules:
        analysis = analyze_rule(rule)
        if analysis['is_chaotic']:
            chaotic_analysis.append(analysis)
        else:
            periodic_analysis.append(analysis)

    # Compare properties
    print("\n" + "=" * 70)
    print("PROPERTY COMPARISON: CHAOTIC vs PERIODIC (balanced rules only)")
    print("=" * 70)

    # Algebraic degree distribution
    chaotic_degrees = [a['algebraic_degree'] for a in chaotic_analysis]
    periodic_degrees = [a['algebraic_degree'] for a in periodic_analysis]

    print(f"\nAlgebraic Degree:")
    print(f"  Chaotic: mean={np.mean(chaotic_degrees):.2f}, all={set(chaotic_degrees)}")
    print(f"  Periodic: mean={np.mean(periodic_degrees):.2f}, all={set(periodic_degrees)}")

    # Nonlinearity
    chaotic_nl = [a['nonlinearity'] for a in chaotic_analysis]
    periodic_nl = [a['nonlinearity'] for a in periodic_analysis]

    print(f"\nNonlinearity:")
    print(f"  Chaotic: {set(chaotic_nl)}, mean={np.mean(chaotic_nl):.2f}")
    print(f"  Periodic: {set(periodic_nl)}, mean={np.mean(periodic_nl):.2f}")

    # Walsh spectrum max
    chaotic_wmax = [a['walsh_max'] for a in chaotic_analysis]
    periodic_wmax = [a['walsh_max'] for a in periodic_analysis]

    print(f"\nWalsh Spectrum Max:")
    print(f"  Chaotic: {set(chaotic_wmax)}, mean={np.mean(chaotic_wmax):.2f}")
    print(f"  Periodic: {set(periodic_wmax)}, mean={np.mean(periodic_wmax):.2f}")

    # Correlation immunity
    chaotic_ci = [a['correlation_immunity'] for a in chaotic_analysis]
    periodic_ci = [a['correlation_immunity'] for a in periodic_analysis]

    print(f"\nCorrelation Immunity:")
    print(f"  Chaotic: {set(chaotic_ci)}, mean={np.mean(chaotic_ci):.2f}")
    print(f"  Periodic: {set(periodic_ci)}, mean={np.mean(periodic_ci):.2f}")

    # SAC satisfaction
    chaotic_sac = [a['propagation']['sac_count'] for a in chaotic_analysis]
    periodic_sac = [a['propagation']['sac_count'] for a in periodic_analysis]

    print(f"\nSAC Satisfied Bits (out of 3):")
    print(f"  Chaotic: {set(chaotic_sac)}, mean={np.mean(chaotic_sac):.2f}")
    print(f"  Periodic: {set(periodic_sac)}, mean={np.mean(periodic_sac):.2f}")

    # Derivative analysis
    print(f"\nDerivative Analysis (d1 = right bit flip, d2 = center, d4 = left):")
    for d in [1, 2, 4]:
        chaotic_d = [a['derivatives'][f'd{d}_ones'] for a in chaotic_analysis]
        periodic_d = [a['derivatives'][f'd{d}_ones'] for a in periodic_analysis]
        print(f"  d{d}_ones - Chaotic: {set(chaotic_d)}, Periodic: {set(periodic_d)}")

    # Look for discriminators
    print("\n" + "=" * 70)
    print("SEARCHING FOR DISCRIMINATORS")
    print("=" * 70)

    # Try combinations of properties
    for prop in ['algebraic_degree', 'nonlinearity', 'walsh_max', 'correlation_immunity']:
        chaotic_vals = set(a[prop] for a in chaotic_analysis)
        periodic_vals = set(a[prop] for a in periodic_analysis)

        chaotic_only = chaotic_vals - periodic_vals
        periodic_only = periodic_vals - chaotic_vals

        if chaotic_only or periodic_only:
            print(f"\n{prop}:")
            if chaotic_only:
                print(f"  Values found ONLY in chaotic: {chaotic_only}")
            if periodic_only:
                print(f"  Values found ONLY in periodic: {periodic_only}")

    # SAC full satisfaction
    chaotic_sac_full = [a['propagation']['sac_all'] for a in chaotic_analysis]
    periodic_sac_full = [a['propagation']['sac_all'] for a in periodic_analysis]

    print(f"\nFull SAC satisfaction:")
    print(f"  Chaotic: {sum(chaotic_sac_full)}/{len(chaotic_sac_full)}")
    print(f"  Periodic: {sum(periodic_sac_full)}/{len(periodic_sac_full)}")

    # Print detailed analysis of chaotic rules
    print("\n" + "=" * 70)
    print("DETAILED ANALYSIS OF CHAOTIC RULES")
    print("=" * 70)

    for a in chaotic_analysis:
        print(f"\nRule {a['rule']}:")
        print(f"  Table: {a['table']}")
        print(f"  ANF: {a['anf_coefficients']}")
        print(f"  Degree: {a['algebraic_degree']}, NL: {a['nonlinearity']}")
        print(f"  Walsh: {a['walsh_spectrum']}")
        print(f"  SAC: {a['propagation']['sac_bits']}")

    # ADDITIONAL: Analyze the ANF structure more carefully
    print("\n" + "=" * 70)
    print("ANF STRUCTURE ANALYSIS")
    print("=" * 70)

    # For 3 variables, ANF terms are:
    # Index 0: constant (1)
    # Index 1: x3 (rightmost input)
    # Index 2: x2 (center input)
    # Index 3: x2*x3
    # Index 4: x1 (leftmost input)
    # Index 5: x1*x3
    # Index 6: x1*x2
    # Index 7: x1*x2*x3

    anf_names = ['1', 'x3', 'x2', 'x2x3', 'x1', 'x1x3', 'x1x2', 'x1x2x3']

    # Count which terms appear in chaotic vs periodic
    chaotic_term_counts = [0] * 8
    periodic_term_counts = [0] * 8

    for a in chaotic_analysis:
        for i, coef in enumerate(a['anf_coefficients']):
            chaotic_term_counts[i] += coef

    for a in periodic_analysis:
        for i, coef in enumerate(a['anf_coefficients']):
            periodic_term_counts[i] += coef

    print("\nANF Term Frequency:")
    print(f"{'Term':10} {'Chaotic':10} {'Periodic':10} {'Chaotic %':10} {'Periodic %':10}")
    for i, name in enumerate(anf_names):
        c_pct = 100 * chaotic_term_counts[i] / len(chaotic_analysis)
        p_pct = 100 * periodic_term_counts[i] / len(periodic_analysis)
        print(f"{name:10} {chaotic_term_counts[i]:10} {periodic_term_counts[i]:10} {c_pct:10.1f}% {p_pct:10.1f}%")

    # Check if any term is universal for chaotic
    print("\nUniversal terms for chaotic rules:")
    for i, name in enumerate(anf_names):
        all_have = all(a['anf_coefficients'][i] == 1 for a in chaotic_analysis)
        none_have = all(a['anf_coefficients'][i] == 0 for a in chaotic_analysis)
        if all_have:
            print(f"  ALL chaotic rules have {name}")
        if none_have:
            print(f"  NO chaotic rule has {name}")

if __name__ == '__main__':
    main()
