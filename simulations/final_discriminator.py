#!/usr/bin/env python3
"""
Finding the final discriminator for chaotic rules.

Key observations from previous analysis:
1. All chaotic rules have 4 ones (balanced) - necessary
2. No chaotic rule has x1x3 term - necessary (100% sensitivity)
3. Chaotic rules never have center_sensitivity=0
4. Chaotic rules never have left_active=0 or 4, same for right_active
5. 10/12 chaotic have exactly one of x1x2 or x2x3

Let's find the combination that gives 100% accuracy.
"""

import numpy as np
from itertools import combinations, product

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

def extract_features(rule):
    """Extract all features for a rule"""
    table = rule_to_table(rule)
    anf = compute_anf(table)

    # Basic
    ones_count = sum(table)

    # ANF terms
    const = anf[0]
    x3 = anf[1]
    x2 = anf[2]
    x2x3 = anf[3]
    x1 = anf[4]
    x1x3 = anf[5]
    x1x2 = anf[6]
    x1x2x3 = anf[7]

    linear = x1 + x2 + x3
    quadratic = x1x2 + x1x3 + x2x3

    # Quiescent states
    q000 = table[0]  # 000 -> ?
    q111 = table[7]  # 111 -> ?

    # Left/right/center activity
    left_active = sum(table[i] for i in [4, 5, 6, 7])
    right_active = sum(table[i] for i in [1, 3, 5, 7])
    center_active = sum(table[i] for i in [2, 3, 6, 7])

    # Sensitivity
    center_0 = [table[i] for i in [0, 1, 4, 5]]
    center_1 = [table[i] for i in [2, 3, 6, 7]]
    center_sens = sum(c0 != c1 for c0, c1 in zip(center_0, center_1))

    left_0 = [table[i] for i in [0, 1, 2, 3]]
    left_1 = [table[i] for i in [4, 5, 6, 7]]
    left_sens = sum(l0 != l1 for l0, l1 in zip(left_0, left_1))

    right_0 = [table[i] for i in [0, 2, 4, 6]]
    right_1 = [table[i] for i in [1, 3, 5, 7]]
    right_sens = sum(r0 != r1 for r0, r1 in zip(right_0, right_1))

    # d3 derivative
    d3 = sum(table[x] != table[7-x] for x in range(8))

    return {
        'rule': rule,
        'ones': ones_count,
        'const': const,
        'x1': x1, 'x2': x2, 'x3': x3,
        'x1x2': x1x2, 'x1x3': x1x3, 'x2x3': x2x3,
        'x1x2x3': x1x2x3,
        'linear': linear,
        'quadratic': quadratic,
        'q000': q000, 'q111': q111,
        'left_active': left_active,
        'right_active': right_active,
        'center_active': center_active,
        'center_sens': center_sens,
        'left_sens': left_sens,
        'right_sens': right_sens,
        'd3': d3,
        'is_chaotic': rule in CHAOTIC_RULES
    }

def test_criterion(features_list, criterion_func, name):
    """Test a criterion function against all rules"""
    matches = [f for f in features_list if criterion_func(f)]
    chaotic_matches = [f for f in matches if f['is_chaotic']]

    # Chaotic that don't match (false negatives)
    all_chaotic = [f for f in features_list if f['is_chaotic']]
    fn = len(all_chaotic) - len(chaotic_matches)

    precision = len(chaotic_matches) / len(matches) if matches else 0
    recall = len(chaotic_matches) / len(all_chaotic) if all_chaotic else 0

    return {
        'name': name,
        'matches': len(matches),
        'chaotic_matches': len(chaotic_matches),
        'false_neg': fn,
        'precision': precision,
        'recall': recall,
        'f1': 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    }

def main():
    print("=" * 70)
    print("SYSTEMATIC SEARCH FOR PERFECT DISCRIMINATOR")
    print("=" * 70)

    # Get all balanced rules
    all_rules = [r for r in range(256) if bin(r).count('1') == 4]
    features = [extract_features(r) for r in all_rules]

    print(f"\nTotal balanced rules: {len(all_rules)}")
    print(f"Chaotic: {len([f for f in features if f['is_chaotic']])}")

    # First, verify base criterion
    base = lambda f: f['x1x3'] == 0
    result = test_criterion(features, base, "no x1x3")
    print(f"\nBase criterion (no x1x3): matches={result['matches']}, precision={result['precision']:.1%}, recall={result['recall']:.1%}")

    # Test additional constraints
    print("\n" + "=" * 70)
    print("TESTING ADDITIONAL CONSTRAINTS")
    print("=" * 70)

    candidates = [f for f in features if f['x1x3'] == 0]
    print(f"Starting with {len(candidates)} no-x1x3 rules ({len([c for c in candidates if c['is_chaotic']])} chaotic)")

    # Try all single-feature constraints
    constraints = [
        ('center_sens > 0', lambda f: f['center_sens'] > 0),
        ('center_sens == 2', lambda f: f['center_sens'] == 2),
        ('center_sens == 4', lambda f: f['center_sens'] == 4),
        ('left_active in {1,2,3}', lambda f: f['left_active'] in {1, 2, 3}),
        ('right_active in {1,2,3}', lambda f: f['right_active'] in {1, 2, 3}),
        ('left_sens > 0', lambda f: f['left_sens'] > 0),
        ('right_sens > 0', lambda f: f['right_sens'] > 0),
        ('left_sens == 4', lambda f: f['left_sens'] == 4),
        ('right_sens == 4', lambda f: f['right_sens'] == 4),
        ('d3 == 4', lambda f: f['d3'] == 4),
        ('d3 in {4,8}', lambda f: f['d3'] in {4, 8}),
        ('linear >= 2', lambda f: f['linear'] >= 2),
        ('linear == 3', lambda f: f['linear'] == 3),
        ('quadratic == 1', lambda f: f['quadratic'] == 1),
        ('x1x2 != x2x3', lambda f: f['x1x2'] != f['x2x3']),
        ('x1x2 == x2x3', lambda f: f['x1x2'] == f['x2x3']),
        ('NOT(q000 AND q111)', lambda f: not (f['q000'] and f['q111'])),
        ('q111 == 0', lambda f: f['q111'] == 0),
        ('q000 == 1', lambda f: f['q000'] == 1),
    ]

    results = []
    for name, func in constraints:
        result = test_criterion(candidates, func, name)
        results.append(result)

    # Sort by F1 score
    results.sort(key=lambda r: r['f1'], reverse=True)

    print(f"\n{'Constraint':<30} {'Match':>6} {'Chaotic':>8} {'Prec':>8} {'Recall':>8} {'F1':>8}")
    print("-" * 70)
    for r in results:
        print(f"{r['name']:<30} {r['matches']:>6} {r['chaotic_matches']:>8} {r['precision']:>7.1%} {r['recall']:>7.1%} {r['f1']:>7.3f}")

    # Now try combinations
    print("\n" + "=" * 70)
    print("TRYING COMBINATIONS OF 2 CONSTRAINTS")
    print("=" * 70)

    best_combos = []
    for i, (name1, func1) in enumerate(constraints):
        for j, (name2, func2) in enumerate(constraints):
            if j <= i:
                continue
            combined = lambda f, f1=func1, f2=func2: f1(f) and f2(f)
            result = test_criterion(candidates, combined, f"{name1} AND {name2}")
            if result['recall'] == 1.0 and result['precision'] > 0.3:
                best_combos.append(result)

    if best_combos:
        best_combos.sort(key=lambda r: r['precision'], reverse=True)
        print(f"\nCombinations with 100% recall and precision > 30%:")
        for r in best_combos[:10]:
            print(f"  {r['name']}: precision={r['precision']:.1%}, matches={r['matches']}")

    # The KEY insight: check what distinguishes chaotic from periodic among similar rules
    print("\n" + "=" * 70)
    print("DETAILED COMPARISON: Chaotic vs Periodic with similar features")
    print("=" * 70)

    # Rules that match d3=4 AND no x1x3 but are periodic
    periodic_d3_4 = [f for f in candidates if f['d3'] == 4 and not f['is_chaotic']]
    chaotic_d3_4 = [f for f in candidates if f['d3'] == 4 and f['is_chaotic']]

    print(f"\nAmong no-x1x3 rules with d3=4:")
    print(f"  Periodic: {len(periodic_d3_4)}")
    print(f"  Chaotic: {len(chaotic_d3_4)}")

    # Compare features
    if periodic_d3_4 and chaotic_d3_4:
        print("\nFeature comparison (mean values):")
        for key in ['const', 'x1', 'x2', 'x3', 'x1x2', 'x2x3', 'linear', 'quadratic',
                    'q000', 'q111', 'left_active', 'right_active', 'center_active',
                    'center_sens', 'left_sens', 'right_sens']:
            c_vals = [f[key] for f in chaotic_d3_4]
            p_vals = [f[key] for f in periodic_d3_4]
            c_mean = np.mean(c_vals)
            p_mean = np.mean(p_vals)
            c_set = set(c_vals)
            p_set = set(p_vals)
            if c_set != p_set:
                print(f"  {key}: chaotic={c_set}, periodic={p_set}")

    # Try a three-feature combination
    print("\n" + "=" * 70)
    print("TRYING: no x1x3 AND d3=4 AND one more constraint")
    print("=" * 70)

    d3_4_candidates = [f for f in candidates if f['d3'] == 4]

    for name, func in constraints:
        result = test_criterion(d3_4_candidates, func, f"d3=4 AND {name}")
        if result['recall'] == 1.0:
            print(f"  {name}: precision={result['precision']:.1%}, matches={result['matches']}")

    # Ultimate test: find the exact criterion
    print("\n" + "=" * 70)
    print("FINDING EXACT CRITERION")
    print("=" * 70)

    # What's different between chaotic and periodic with d3=4?
    print("\nPeriodic rules with d3=4 and no x1x3:")
    for f in periodic_d3_4:
        print(f"  Rule {f['rule']}: x1={f['x1']}, x2={f['x2']}, x3={f['x3']}, "
              f"x1x2={f['x1x2']}, x2x3={f['x2x3']}, linear={f['linear']}")

    print("\nChaotic rules with d3=4 and no x1x3:")
    for f in chaotic_d3_4:
        print(f"  Rule {f['rule']}: x1={f['x1']}, x2={f['x2']}, x3={f['x3']}, "
              f"x1x2={f['x1x2']}, x2x3={f['x2x3']}, linear={f['linear']}")

    # Check the pattern: x1==x3 (symmetric linear terms)?
    print("\n" + "=" * 70)
    print("TESTING: x1 == x3 (symmetric linear terms)")
    print("=" * 70)

    for f in d3_4_candidates:
        sym = f['x1'] == f['x3']
        is_c = 'CHAOTIC' if f['is_chaotic'] else 'periodic'
        if f['is_chaotic'] or sym:
            print(f"  Rule {f['rule']}: x1={f['x1']}, x3={f['x3']}, symmetric={sym}, {is_c}")

    sym_criterion = lambda f: f['x1'] == f['x3']
    result = test_criterion(d3_4_candidates, sym_criterion, "x1 == x3")
    print(f"\nSymmetric criterion: precision={result['precision']:.1%}, recall={result['recall']:.1%}")

    # What about x1+x3 >= 1 (at least one edge linear term)?
    print("\n" + "=" * 70)
    print("TESTING: x1 + x3 >= 1 (at least one edge linear)")
    print("=" * 70)

    edge_criterion = lambda f: f['x1'] + f['x3'] >= 1
    result = test_criterion(d3_4_candidates, edge_criterion, "x1 + x3 >= 1")
    print(f"Edge criterion: precision={result['precision']:.1%}, recall={result['recall']:.1%}")

    # What about x1*x3 != x1x2*x2x3 (asymmetric interaction)?
    print("\n" + "=" * 70)
    print("TESTING: asymmetric quadratic structure")
    print("=" * 70)

    for f in d3_4_candidates:
        both_zero = (f['x1x2'] == 0 and f['x2x3'] == 0)
        both_one = (f['x1x2'] == 1 and f['x2x3'] == 1)
        is_c = 'CHAOTIC' if f['is_chaotic'] else 'periodic'
        if f['is_chaotic'] or (not both_zero and not both_one):
            print(f"  Rule {f['rule']}: x1x2={f['x1x2']}, x2x3={f['x2x3']}, xor={f['x1x2'] != f['x2x3']}, {is_c}")

    xor_criterion = lambda f: f['x1x2'] != f['x2x3']
    result = test_criterion(d3_4_candidates, xor_criterion, "x1x2 XOR x2x3")
    print(f"\nXOR criterion: precision={result['precision']:.1%}, recall={result['recall']:.1%}")

    # FINAL: what if we check the exceptions (rules 105, 150)?
    print("\n" + "=" * 70)
    print("CHECKING THE EXCEPTIONS: Rules 105 and 150")
    print("=" * 70)

    for rule in [105, 150]:
        f = extract_features(rule)
        print(f"\nRule {rule}:")
        for k, v in f.items():
            print(f"  {k}: {v}")

    # They have d3=8, not d3=4!
    print("\n" + "=" * 70)
    print("REVELATION: Chaotic rules have d3 in {4, 8}, with specific ANF structure")
    print("=" * 70)

    # Final criterion: no x1x3 AND (d3==4 with certain features OR d3==8 with certain features)
    d3_8_chaotic = [f for f in candidates if f['d3'] == 8 and f['is_chaotic']]
    d3_8_periodic = [f for f in candidates if f['d3'] == 8 and not f['is_chaotic']]

    print(f"\nd3=8 rules: {len([f for f in candidates if f['d3'] == 8])}")
    print(f"  Chaotic: {len(d3_8_chaotic)}")
    print(f"  Periodic: {len(d3_8_periodic)}")

    if d3_8_chaotic:
        print("\nChaotic d3=8 rules:")
        for f in d3_8_chaotic:
            print(f"  Rule {f['rule']}: linear={f['linear']}, quadratic={f['quadratic']}")

    if d3_8_periodic:
        print("\nPeriodic d3=8 rules:")
        for f in d3_8_periodic:
            print(f"  Rule {f['rule']}: linear={f['linear']}, quadratic={f['quadratic']}")

    # The pattern: d3=8 AND linear=3 AND quadratic=0 are the XOR rules (105, 150)
    print("\n" + "=" * 70)
    print("TESTING: d3=8 AND linear=3 AND quadratic=0")
    print("=" * 70)

    xor_like = lambda f: f['d3'] == 8 and f['linear'] == 3 and f['quadratic'] == 0
    result = test_criterion(candidates, xor_like, "d3=8 AND linear=3 AND quad=0")
    print(f"XOR-like criterion: matches={result['matches']}, precision={result['precision']:.1%}")

    if result['matches'] > 0:
        print("Matching rules:")
        for f in candidates:
            if xor_like(f):
                is_c = 'CHAOTIC' if f['is_chaotic'] else 'periodic'
                print(f"  Rule {f['rule']}: {is_c}")

if __name__ == '__main__':
    main()
