#!/usr/bin/env python3
"""
Complete Theory of ECA Chaos

We've found:
- d3=8 chaotic: linear=3 AND quadratic=0 (rules 105, 150) - XOR rules
- d3=4 chaotic: x1x2 XOR x2x3 = 1, plus something else

What distinguishes chaotic d3=4 rules from periodic ones with same quadratic structure?

Chaotic d3=4 with x1x2=0, x2x3=1: 30, 45, 75, 120, 135
Periodic d3=4 with x1x2=0, x2x3=1: 180, 210, 225

Chaotic d3=4 with x1x2=1, x2x3=0: 86, 89, 101, 106, 149
Periodic d3=4 with x1x2=1, x2x3=0: 29, 71, 154, 166, 169

What's the difference?
"""

import numpy as np

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

def analyze_rule(rule):
    table = rule_to_table(rule)
    anf = compute_anf(table)

    features = {
        'rule': rule,
        'binary': format(rule, '08b'),
        'is_chaotic': rule in CHAOTIC_RULES,
        'const': anf[0],
        'x1': anf[4], 'x2': anf[2], 'x3': anf[1],
        'x1x2': anf[6], 'x1x3': anf[5], 'x2x3': anf[3],
        # Table positions
        't0': table[0], 't1': table[1], 't2': table[2], 't3': table[3],
        't4': table[4], 't5': table[5], 't6': table[6], 't7': table[7],
    }

    # d3 derivative
    d3 = sum(table[x] != table[7-x] for x in range(8))
    features['d3'] = d3

    return features

def main():
    print("=" * 70)
    print("COMPLETE THEORY OF ECA CHAOS")
    print("=" * 70)

    # Get all balanced no-x1x3 rules
    balanced_no_x1x3 = []
    for r in range(256):
        if bin(r).count('1') == 4:  # balanced
            table = rule_to_table(r)
            anf = compute_anf(table)
            if anf[5] == 0:  # no x1x3
                balanced_no_x1x3.append(r)

    # Group by quadratic structure
    groups = {
        'x2x3_only': [],  # x1x2=0, x2x3=1
        'x1x2_only': [],  # x1x2=1, x2x3=0
        'both': [],       # x1x2=1, x2x3=1
        'neither': [],    # x1x2=0, x2x3=0
    }

    for r in balanced_no_x1x3:
        f = analyze_rule(r)
        if f['d3'] != 4:
            continue  # Focus on d3=4 rules for now

        if f['x1x2'] == 0 and f['x2x3'] == 1:
            groups['x2x3_only'].append(f)
        elif f['x1x2'] == 1 and f['x2x3'] == 0:
            groups['x1x2_only'].append(f)
        elif f['x1x2'] == 1 and f['x2x3'] == 1:
            groups['both'].append(f)
        else:
            groups['neither'].append(f)

    # Analyze each group
    for group_name, rules in groups.items():
        chaotic = [r for r in rules if r['is_chaotic']]
        periodic = [r for r in rules if not r['is_chaotic']]

        print(f"\n{group_name}: {len(chaotic)} chaotic, {len(periodic)} periodic")

        if chaotic and periodic:
            print("  Comparing features:")

            # Look at each table position
            for pos in ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7']:
                c_vals = [r[pos] for r in chaotic]
                p_vals = [r[pos] for r in periodic]
                c_set = set(c_vals)
                p_set = set(p_vals)
                if c_set != p_set:
                    print(f"    {pos}: chaotic={c_set}, periodic={p_set}")

            # Look at linear terms
            for term in ['const', 'x1', 'x2', 'x3']:
                c_vals = [r[term] for r in chaotic]
                p_vals = [r[term] for r in periodic]
                c_set = set(c_vals)
                p_set = set(p_vals)
                if c_set != p_set:
                    print(f"    {term}: chaotic={c_set}, periodic={p_set}")

    # Focus on x2x3_only group (chaotic: 30, 45, 75, 120, 135)
    print("\n" + "=" * 70)
    print("DETAILED: x2x3_only group (x1x2=0, x2x3=1)")
    print("=" * 70)

    x2x3_rules = groups['x2x3_only']
    print("\nChaotic rules:")
    for r in [f for f in x2x3_rules if f['is_chaotic']]:
        print(f"  Rule {r['rule']}: const={r['const']}, x1={r['x1']}, x2={r['x2']}, x3={r['x3']}")
        print(f"    Table: {r['t0']}{r['t1']}{r['t2']}{r['t3']}{r['t4']}{r['t5']}{r['t6']}{r['t7']}")

    print("\nPeriodic rules:")
    for r in [f for f in x2x3_rules if not f['is_chaotic']]:
        print(f"  Rule {r['rule']}: const={r['const']}, x1={r['x1']}, x2={r['x2']}, x3={r['x3']}")
        print(f"    Table: {r['t0']}{r['t1']}{r['t2']}{r['t3']}{r['t4']}{r['t5']}{r['t6']}{r['t7']}")

    # Key insight: Look at specific table positions
    print("\n" + "=" * 70)
    print("LOOKING FOR THE KEY POSITION")
    print("=" * 70)

    # For x2x3_only rules, check t7 (111 -> ?)
    chaotic_t7 = [r['t7'] for r in x2x3_rules if r['is_chaotic']]
    periodic_t7 = [r['t7'] for r in x2x3_rules if not r['is_chaotic']]
    print(f"\nt7 (111->?): chaotic={set(chaotic_t7)}, periodic={set(periodic_t7)}")

    # Check t0 (000 -> ?)
    chaotic_t0 = [r['t0'] for r in x2x3_rules if r['is_chaotic']]
    periodic_t0 = [r['t0'] for r in x2x3_rules if not r['is_chaotic']]
    print(f"t0 (000->?): chaotic={set(chaotic_t0)}, periodic={set(periodic_t0)}")

    # Interesting! Let's check if t7=0 characterizes chaotic in this group
    print("\n" + "=" * 70)
    print("HYPOTHESIS: In x2x3_only group, chaotic iff t7=0")
    print("=" * 70)

    for r in x2x3_rules:
        is_c = 'CHAOTIC' if r['is_chaotic'] else 'periodic'
        print(f"  Rule {r['rule']}: t7={r['t7']}, {is_c}")

    # Now check x1x2_only group
    print("\n" + "=" * 70)
    print("DETAILED: x1x2_only group (x1x2=1, x2x3=0)")
    print("=" * 70)

    x1x2_rules = groups['x1x2_only']
    print("\nChaotic rules:")
    for r in [f for f in x1x2_rules if f['is_chaotic']]:
        print(f"  Rule {r['rule']}: const={r['const']}, x1={r['x1']}, x2={r['x2']}, x3={r['x3']}")
        print(f"    Table: {r['t0']}{r['t1']}{r['t2']}{r['t3']}{r['t4']}{r['t5']}{r['t6']}{r['t7']}")

    print("\nPeriodic rules:")
    for r in [f for f in x1x2_rules if not f['is_chaotic']]:
        print(f"  Rule {r['rule']}: const={r['const']}, x1={r['x1']}, x2={r['x2']}, x3={r['x3']}")
        print(f"    Table: {r['t0']}{r['t1']}{r['t2']}{r['t3']}{r['t4']}{r['t5']}{r['t6']}{r['t7']}")

    # Check t7 for this group
    chaotic_t7 = [r['t7'] for r in x1x2_rules if r['is_chaotic']]
    periodic_t7 = [r['t7'] for r in x1x2_rules if not r['is_chaotic']]
    print(f"\nt7 (111->?): chaotic={set(chaotic_t7)}, periodic={set(periodic_t7)}")

    # Check t0
    chaotic_t0 = [r['t0'] for r in x1x2_rules if r['is_chaotic']]
    periodic_t0 = [r['t0'] for r in x1x2_rules if not r['is_chaotic']]
    print(f"t0 (000->?): chaotic={set(chaotic_t0)}, periodic={set(periodic_t0)}")

    print("\n" + "=" * 70)
    print("HYPOTHESIS: In x1x2_only group, chaotic iff t7=0")
    print("=" * 70)

    for r in x1x2_rules:
        is_c = 'CHAOTIC' if r['is_chaotic'] else 'periodic'
        print(f"  Rule {r['rule']}: t7={r['t7']}, {is_c}")

    # UNIFIED CRITERION!
    print("\n" + "=" * 70)
    print("UNIFIED CRITERION FOR d3=4 RULES")
    print("The output for input 111 determines chaos!")
    print("=" * 70)

    # All d3=4 rules with exactly one of x1x2, x2x3
    d3_4_xor_quad = [f for f in groups['x1x2_only'] + groups['x2x3_only']]

    print(f"\nTesting: chaotic iff t7=0 (among d3=4 rules with x1x2 XOR x2x3)")
    print(f"Total rules: {len(d3_4_xor_quad)}")

    correct = 0
    for r in d3_4_xor_quad:
        predicted_chaotic = (r['t7'] == 0)
        actual_chaotic = r['is_chaotic']
        match = predicted_chaotic == actual_chaotic
        if match:
            correct += 1
        else:
            print(f"  MISMATCH: Rule {r['rule']}, t7={r['t7']}, actual={actual_chaotic}")

    print(f"\nAccuracy: {correct}/{len(d3_4_xor_quad)} = {100*correct/len(d3_4_xor_quad):.1f}%")

    # What about "both" group?
    print("\n" + "=" * 70)
    print("CHECKING 'both' group (x1x2=1, x2x3=1)")
    print("=" * 70)

    for r in groups['both']:
        is_c = 'CHAOTIC' if r['is_chaotic'] else 'periodic'
        print(f"  Rule {r['rule']}: t7={r['t7']}, {is_c}")

    # The 'both' group has no chaotic rules (they all have x1x3=0 but both quadratic terms)
    print(f"\nNo chaotic rules in 'both' group (as expected - they violate the XOR constraint)")

    # FINAL COMPLETE CRITERION
    print("\n" + "=" * 70)
    print("FINAL COMPLETE CRITERION")
    print("=" * 70)

    print("""
A balanced (4-ones) ECA rule is CHAOTIC if and only if:

1. x1x3 = 0 (no direct left-right interaction in ANF)

AND one of:

2a. d3 = 8 AND linear = 3 AND quadratic = 0
    (XOR rules: 105, 150)

2b. d3 = 4 AND (x1x2 XOR x2x3) AND t7 = 0
    (All other chaotic rules)

Equivalently for 2b: 111 -> 0 (the all-ones neighborhood produces 0)
""")

    # Verify this criterion on ALL rules
    print("\n" + "=" * 70)
    print("VERIFICATION ON ALL 256 RULES")
    print("=" * 70)

    def is_predicted_chaotic(rule):
        table = rule_to_table(rule)
        anf = compute_anf(table)

        # Base requirement
        if bin(rule).count('1') != 4:  # not balanced
            return False
        if anf[5] != 0:  # has x1x3
            return False

        # Check criterion 2a: XOR rules
        linear = anf[1] + anf[2] + anf[4]
        quadratic = anf[3] + anf[5] + anf[6]
        d3 = sum(table[x] != table[7-x] for x in range(8))

        if d3 == 8 and linear == 3 and quadratic == 0:
            return True

        # Check criterion 2b
        x1x2_xor_x2x3 = (anf[6] != anf[3])
        t7 = table[7]

        if d3 == 4 and x1x2_xor_x2x3 and t7 == 0:
            return True

        return False

    tp, tn, fp, fn = 0, 0, 0, 0
    errors = []

    for rule in range(256):
        predicted = is_predicted_chaotic(rule)
        actual = rule in CHAOTIC_RULES

        if predicted and actual:
            tp += 1
        elif not predicted and not actual:
            tn += 1
        elif predicted and not actual:
            fp += 1
            errors.append(f"FP: Rule {rule}")
        else:
            fn += 1
            errors.append(f"FN: Rule {rule}")

    print(f"True Positives: {tp}")
    print(f"True Negatives: {tn}")
    print(f"False Positives: {fp}")
    print(f"False Negatives: {fn}")
    print(f"Accuracy: {100*(tp+tn)/256:.1f}%")

    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  {e}")

if __name__ == '__main__':
    main()
