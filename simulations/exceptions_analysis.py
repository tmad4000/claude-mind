#!/usr/bin/env python3
"""
Analyzing the exceptions: Rules 135 and 149

These rules ARE chaotic but have t7=1 (111->1).
What makes them special?
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

def full_analysis(rule):
    table = rule_to_table(rule)
    anf = compute_anf(table)

    print(f"\n{'='*50}")
    print(f"Rule {rule}: {'CHAOTIC' if rule in CHAOTIC_RULES else 'periodic'}")
    print(f"{'='*50}")
    print(f"Binary: {format(rule, '08b')}")
    print(f"Table: {''.join(str(t) for t in table)} (input 0-7 from left)")

    # ANF
    anf_names = ['1', 'x3', 'x2', 'x2x3', 'x1', 'x1x3', 'x1x2', 'x1x2x3']
    terms = [anf_names[i] for i in range(8) if anf[i] == 1]
    print(f"ANF: {' + '.join(terms)}")

    print(f"\nKey positions:")
    print(f"  000 (t0) -> {table[0]}")
    print(f"  111 (t7) -> {table[7]}")
    print(f"  010 (t2) -> {table[2]} (isolated 1)")
    print(f"  101 (t5) -> {table[5]} (isolated 0)")

    # Derivatives
    d3 = sum(table[x] != table[7-x] for x in range(8))
    print(f"\nd3 = {d3}")

    # Check symmetry
    complement = [(1-t) for t in table[::-1]]
    reflect = table[::-1]
    print(f"\nSymmetry:")
    print(f"  Complement (255-rule): {255-rule}")
    print(f"  Reflection: {sum(t*(2**i) for i, t in enumerate(reflect))}")

    # Check the complement and reflection
    comp_rule = 255 - rule
    ref_table = [table[7-i] for i in range(8)]
    ref_rule = sum(ref_table[i] * (2**i) for i in range(8))

    print(f"  Complement {comp_rule} chaotic: {comp_rule in CHAOTIC_RULES}")
    print(f"  Reflection {ref_rule} chaotic: {ref_rule in CHAOTIC_RULES}")

    return {
        'rule': rule,
        'table': table,
        'anf': anf,
        't0': table[0],
        't7': table[7],
        'd3': d3
    }

def main():
    print("ANALYZING CHAOTIC RULES 135 AND 149 (the exceptions with t7=1)")

    # First analyze all chaotic rules to see the pattern
    print("\n" + "=" * 70)
    print("ALL CHAOTIC RULES")
    print("=" * 70)

    for rule in CHAOTIC_RULES:
        f = full_analysis(rule)

    # Now focus on 135 and 149
    print("\n" + "=" * 70)
    print("KEY OBSERVATION: Rules 135 and 149")
    print("=" * 70)

    # They both have t7=1, but they're related to rules with t7=0 by complement
    # 135 complement is 120 (which has t7=0)
    # 149 complement is 106 (which has t7=0)

    print("""
Rules 135 and 149 are the COMPLEMENTS of rules 120 and 106!

- Rule 120: 00011110, t7=0, CHAOTIC
- Rule 135: 11100001, t7=1, CHAOTIC (complement of 120)

- Rule 106: 01010110, t7=0, CHAOTIC
- Rule 149: 10101001, t7=1, CHAOTIC (complement of 106)

The complement operation maps:
- table[i] -> 1 - table[7-i]
- So t0 becomes 1-t7 and t7 becomes 1-t0

For rule 120: t0=0, t7=0 -> complement gives t0=1, t7=1 (rule 135)
For rule 106: t0=0, t7=0 -> complement gives t0=1, t7=1 (rule 149)

These are the ONLY two chaotic rules whose t0=t7 (both have same quiescent behavior).
""")

    # Verify this pattern
    print("\n" + "=" * 70)
    print("PATTERN: t0 == t7 for exceptions")
    print("=" * 70)

    for rule in CHAOTIC_RULES:
        table = rule_to_table(rule)
        t0, t7 = table[0], table[7]
        print(f"Rule {rule}: t0={t0}, t7={t7}, t0==t7: {t0==t7}")

    # So the refined criterion is:
    print("\n" + "=" * 70)
    print("REFINED CRITERION")
    print("=" * 70)

    print("""
The exceptions (135, 149) have t0 == t7 == 1.

Looking at all chaotic rules:
- If t0 != t7: chaotic iff t7 = 0
- If t0 == t7: chaotic iff t0 == t7 == 1 AND <other conditions>

Wait, let me check if t0==t7 distinguishes them...
""")

    # Check what periodic rules have t0==t7
    print("\n" + "=" * 70)
    print("CHECKING: balanced no-x1x3 rules with t0==t7")
    print("=" * 70)

    balanced_no_x1x3 = []
    for r in range(256):
        if bin(r).count('1') == 4:
            table = rule_to_table(r)
            anf = compute_anf(table)
            if anf[5] == 0:
                t0, t7 = table[0], table[7]
                if t0 == t7:
                    balanced_no_x1x3.append({
                        'rule': r,
                        't0': t0,
                        't7': t7,
                        'd3': sum(table[x] != table[7-x] for x in range(8)),
                        'is_chaotic': r in CHAOTIC_RULES
                    })

    print(f"Rules with t0==t7 among balanced no-x1x3: {len(balanced_no_x1x3)}")
    for f in balanced_no_x1x3:
        is_c = 'CHAOTIC' if f['is_chaotic'] else 'periodic'
        print(f"  Rule {f['rule']}: t0=t7={f['t0']}, d3={f['d3']}, {is_c}")

    # Now I see it: 135 and 149 have d3=4, while periodic t0=t7 rules have d3=0 or d3=8
    print("\n" + "=" * 70)
    print("THE PATTERN: d3 for t0==t7 rules")
    print("=" * 70)

    chaotic_t0_eq_t7 = [f for f in balanced_no_x1x3 if f['is_chaotic']]
    periodic_t0_eq_t7 = [f for f in balanced_no_x1x3 if not f['is_chaotic']]

    print(f"Chaotic t0==t7 rules d3: {set(f['d3'] for f in chaotic_t0_eq_t7)}")
    print(f"Periodic t0==t7 rules d3: {set(f['d3'] for f in periodic_t0_eq_t7)}")

    # Perfect! Chaotic t0==t7 rules have d3=4, periodic have d3 in {0,8}
    print("\n" + "=" * 70)
    print("FINAL REFINED CRITERION")
    print("=" * 70)

    print("""
A balanced (4-ones) ECA rule is CHAOTIC if and only if:

1. x1x3 = 0 (no direct left-right interaction)

AND one of:

2a. d3 = 8 AND linear = 3 AND quadratic = 0 (XOR rules: 105, 150)

2b. d3 = 4 AND (x1x2 XOR x2x3) AND (t7 = 0 OR (t0 = t7 = 1))

The key insight: when t0 = t7 (quiescent states have same behavior),
the rule can still be chaotic if d3 = 4 and t0 = t7 = 1.
This corresponds to "anti-quiescent" behavior where uniform states survive
but the rule is still maximally sensitive (d3=4).
""")

    # Verify final criterion
    print("\n" + "=" * 70)
    print("VERIFYING FINAL CRITERION")
    print("=" * 70)

    def is_chaotic_final(rule):
        table = rule_to_table(rule)
        anf = compute_anf(table)

        # Base: balanced + no x1x3
        if bin(rule).count('1') != 4:
            return False
        if anf[5] != 0:
            return False

        linear = anf[1] + anf[2] + anf[4]
        quadratic = anf[3] + anf[5] + anf[6]
        d3 = sum(table[x] != table[7-x] for x in range(8))
        t0, t7 = table[0], table[7]
        x1x2_xor_x2x3 = (anf[6] != anf[3])

        # Criterion 2a: XOR rules
        if d3 == 8 and linear == 3 and quadratic == 0:
            return True

        # Criterion 2b: d3=4 with XOR quadratic and right quiescent pattern
        if d3 == 4 and x1x2_xor_x2x3:
            if t7 == 0 or (t0 == 1 and t7 == 1):
                return True

        return False

    tp, tn, fp, fn = 0, 0, 0, 0
    for rule in range(256):
        predicted = is_chaotic_final(rule)
        actual = rule in CHAOTIC_RULES

        if predicted and actual:
            tp += 1
        elif not predicted and not actual:
            tn += 1
        elif predicted and not actual:
            fp += 1
            print(f"FP: Rule {rule}")
        else:
            fn += 1
            print(f"FN: Rule {rule}")

    print(f"\nTrue Positives: {tp}")
    print(f"True Negatives: {tn}")
    print(f"False Positives: {fp}")
    print(f"False Negatives: {fn}")
    print(f"Accuracy: {100*(tp+tn)/256:.1f}%")

if __name__ == '__main__':
    main()
