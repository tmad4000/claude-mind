#!/usr/bin/env python3
"""
Finding what distinguishes chaotic from non-chaotic rules among balanced rules without x1x3.

We know:
- All chaotic rules have 4 ones (balanced) - NECESSARY
- No chaotic rule has x1x3 term - NECESSARY
- But these together give ~32% precision (12/38)

What else distinguishes the 12 chaotic from 26 non-chaotic among no-x1x3 balanced rules?
"""

import numpy as np
from itertools import combinations

CHAOTIC_RULES = [30, 45, 75, 86, 89, 101, 105, 106, 120, 135, 149, 150]

def rule_to_table(rule):
    return [(rule >> i) & 1 for i in range(8)]

def compute_anf(table):
    n = 3
    anf = np.array(table, dtype=np.int64)
    for i in range(n):
        for j in range(2**n):
            if (j >> i) & 1:
                anf[j] ^= anf[j ^ (1 << i)]
    return anf

def get_balanced_no_x1x3():
    """Get balanced rules without x1x3 term"""
    rules = []
    for r in range(256):
        if bin(r).count('1') == 4:  # balanced
            table = rule_to_table(r)
            anf = compute_anf(table)
            if anf[5] == 0:  # no x1x3
                rules.append(r)
    return rules

def analyze_structure(rule):
    """Get structural features of a rule"""
    table = rule_to_table(rule)
    anf = compute_anf(table)

    # Which inputs produce 0 (the "zero-set")
    zeros = [i for i in range(8) if table[i] == 0]
    ones = [i for i in range(8) if table[i] == 1]

    # Position analysis: which bit patterns produce 1
    features = {
        'rule': rule,
        'is_chaotic': rule in CHAOTIC_RULES,
        'zeros': zeros,
        'ones': ones,

        # ANF terms
        'const': anf[0],
        'x3': anf[1],
        'x2': anf[2],
        'x2x3': anf[3],
        'x1': anf[4],
        'x1x2': anf[6],

        # Derived
        'linear_count': anf[1] + anf[2] + anf[4],
        'quadratic_count': anf[3] + anf[6],  # no x1x3 so only 2 possible

        # Pattern features
        'has_000': table[0] == 1,  # quiescent (all 0 -> 1?)
        'has_111': table[7] == 1,  # all 1 -> 1?
        'has_010': table[2] == 1,  # isolated 1 -> 1?
        'has_101': table[5] == 1,  # isolated 0 -> 1?
    }

    # XOR chain property: is the function XOR-like?
    # Rule 150 is x1 XOR x2 XOR x3
    xor_150 = [0, 1, 1, 0, 1, 0, 0, 1]
    features['matches_xor150'] = table == xor_150

    # Left-right balance: sum of left-heavy vs right-heavy outputs
    # Inputs 4,5,6,7 have left=1; inputs 1,3,5,7 have right=1
    left_active = sum(table[i] for i in [4, 5, 6, 7])  # when x1=1
    right_active = sum(table[i] for i in [1, 3, 5, 7])  # when x3=1
    features['left_active'] = left_active
    features['right_active'] = right_active
    features['lr_balance'] = abs(left_active - right_active)

    # Center influence: how much does x2 affect output
    center_0 = [table[i] for i in [0, 1, 4, 5]]  # x2=0
    center_1 = [table[i] for i in [2, 3, 6, 7]]  # x2=1
    center_diff = sum(c0 != c1 for c0, c1 in zip(center_0, center_1))
    features['center_sensitivity'] = center_diff

    return features

def main():
    print("=" * 70)
    print("FINDING THE CHAOTIC DISCRIMINATOR")
    print("Among balanced rules without x1x3")
    print("=" * 70)

    candidates = get_balanced_no_x1x3()
    print(f"\nCandidate pool: {len(candidates)} rules")
    print(f"Chaotic: {len([r for r in candidates if r in CHAOTIC_RULES])}")

    # Analyze all
    analyses = [analyze_structure(r) for r in candidates]
    chaotic = [a for a in analyses if a['is_chaotic']]
    periodic = [a for a in analyses if not a['is_chaotic']]

    print(f"\n" + "=" * 70)
    print("FEATURE COMPARISON")
    print("=" * 70)

    # Binary features
    for feature in ['has_000', 'has_111', 'has_010', 'has_101']:
        c_has = sum(a[feature] for a in chaotic)
        p_has = sum(a[feature] for a in periodic)
        print(f"\n{feature}:")
        print(f"  Chaotic: {c_has}/{len(chaotic)} = {100*c_has/len(chaotic):.0f}%")
        print(f"  Periodic: {p_has}/{len(periodic)} = {100*p_has/len(periodic):.0f}%")

    # Numeric features
    for feature in ['linear_count', 'quadratic_count', 'lr_balance', 'center_sensitivity',
                    'left_active', 'right_active']:
        c_vals = [a[feature] for a in chaotic]
        p_vals = [a[feature] for a in periodic]
        print(f"\n{feature}:")
        print(f"  Chaotic: vals={set(c_vals)}, mean={np.mean(c_vals):.2f}")
        print(f"  Periodic: vals={set(p_vals)}, mean={np.mean(p_vals):.2f}")

        # Check for discrimination
        c_only = set(c_vals) - set(p_vals)
        p_only = set(p_vals) - set(c_vals)
        if c_only:
            print(f"  --> CHAOTIC-ONLY values: {c_only}")
        if p_only:
            print(f"  --> PERIODIC-ONLY values: {p_only}")

    # The key: quiescent state constraint from earlier finding
    print("\n" + "=" * 70)
    print("TESTING QUIESCENT CONSTRAINT: NOT(000->1 AND 111->1)")
    print("(From earlier characterization: chaotic rules don't have both quiescent states stable)")
    print("=" * 70)

    # NOT(has_000 AND has_111) = NOT(both quiescent states die)
    # i.e., at least one of 000 or 111 produces 0
    for a in analyses:
        stable_both = a['has_000'] and a['has_111']
        is_c = 'CHAOTIC' if a['is_chaotic'] else 'periodic'
        print(f"Rule {a['rule']:3d}: 000->{a['has_000']}, 111->{a['has_111']}, both_stable={stable_both}, {is_c}")

    # Count
    c_stable = sum(a['has_000'] and a['has_111'] for a in chaotic)
    p_stable = sum(a['has_000'] and a['has_111'] for a in periodic)
    print(f"\nBoth quiescent states stable:")
    print(f"  Chaotic: {c_stable}/{len(chaotic)}")
    print(f"  Periodic: {p_stable}/{len(periodic)}")

    # Try the combined criterion
    print("\n" + "=" * 70)
    print("COMBINED CRITERION: no x1x3 AND NOT(000->1 AND 111->1)")
    print("=" * 70)

    matches = [a for a in analyses if not (a['has_000'] and a['has_111'])]
    chaotic_matches = [a for a in matches if a['is_chaotic']]

    print(f"Rules matching: {len(matches)}")
    print(f"Chaotic among matches: {len(chaotic_matches)}")
    print(f"Precision: {100*len(chaotic_matches)/len(matches):.1f}%")

    # What about the opposite constraint?
    print("\n" + "=" * 70)
    print("TESTING: NOT(000->0 AND 111->0) = at least one quiescent state stable")
    print("=" * 70)

    for a in analyses:
        neither = not a['has_000'] and not a['has_111']
        is_c = 'CHAOTIC' if a['is_chaotic'] else 'periodic'
        if a['is_chaotic'] or neither:
            print(f"Rule {a['rule']:3d}: 000->{'1' if a['has_000'] else '0'}, 111->{'1' if a['has_111'] else '0'}, neither_stable={neither}, {is_c}")

    # What about XOR with specific term?
    print("\n" + "=" * 70)
    print("TESTING: presence of x1x2 or x2x3 term (exactly one quadratic)")
    print("=" * 70)

    for a in analyses:
        x1x2 = a['x1x2']
        x2x3 = a['x2x3']
        xor = x1x2 != x2x3  # exactly one
        is_c = 'CHAOTIC' if a['is_chaotic'] else 'periodic'
        if a['is_chaotic']:
            print(f"Rule {a['rule']:3d}: x1x2={x1x2}, x2x3={x2x3}, exactly_one={xor}, {is_c}")

    c_exact_one = sum((a['x1x2'] != a['x2x3']) for a in chaotic)
    p_exact_one = sum((a['x1x2'] != a['x2x3']) for a in periodic)
    print(f"\nExactly one of x1x2 or x2x3:")
    print(f"  Chaotic: {c_exact_one}/{len(chaotic)}")
    print(f"  Periodic: {p_exact_one}/{len(periodic)}")

    # The key insight from earlier: check the d3 derivative
    print("\n" + "=" * 70)
    print("TESTING d3 DERIVATIVE (from earlier characterization)")
    print("d3 = number of times flipping all 3 bits changes output")
    print("=" * 70)

    for a in analyses:
        table = rule_to_table(a['rule'])
        d3 = 0
        for x in range(8):
            if table[x] != table[7-x]:  # x XOR 111 = complement
                d3 += 1
        a['d3'] = d3
        is_c = 'CHAOTIC' if a['is_chaotic'] else 'periodic'
        print(f"Rule {a['rule']:3d}: d3={d3}, {is_c}")

    c_d3 = [a['d3'] for a in chaotic]
    p_d3 = [a['d3'] for a in periodic]
    print(f"\nd3 values:")
    print(f"  Chaotic: {set(c_d3)}")
    print(f"  Periodic: {set(p_d3)}")

    # Try: d3=4 or d3=0 for chaotic?
    c_d3_extreme = sum(a['d3'] in [0, 4, 8] for a in chaotic)
    p_d3_extreme = sum(a['d3'] in [0, 4, 8] for a in periodic)
    print(f"\nd3 in {{0, 4, 8}} (extreme values):")
    print(f"  Chaotic: {c_d3_extreme}/{len(chaotic)}")
    print(f"  Periodic: {p_d3_extreme}/{len(periodic)}")

    # Final combined test
    print("\n" + "=" * 70)
    print("FINAL TEST: no x1x3 AND d3 == 4")
    print("=" * 70)

    for a in analyses:
        if a['d3'] == 4:
            is_c = 'CHAOTIC' if a['is_chaotic'] else 'periodic'
            print(f"Rule {a['rule']:3d}: {is_c}")

    matches_final = [a for a in analyses if a['d3'] == 4]
    chaotic_final = [a for a in matches_final if a['is_chaotic']]
    print(f"\nMatching d3==4: {len(matches_final)}")
    print(f"Chaotic: {len(chaotic_final)}")
    print(f"Precision: {100*len(chaotic_final)/len(matches_final):.1f}%")

if __name__ == '__main__':
    main()
