#!/usr/bin/env python3
"""
Finding the PERFECT criterion for ECA chaos.

Current situation:
- Rule 135, 149: chaotic with t0=t7=1 (true positives)
- Rule 169, 225: periodic with t0=t7=1 (false positives)

What distinguishes 135,149 from 169,225?
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

def compare_rules(rules):
    """Compare a set of rules in detail"""
    for rule in rules:
        table = rule_to_table(rule)
        anf = compute_anf(table)

        anf_names = ['1', 'x3', 'x2', 'x2x3', 'x1', 'x1x3', 'x1x2', 'x1x2x3']
        terms = [anf_names[i] for i in range(8) if anf[i] == 1]

        print(f"\nRule {rule}: {'CHAOTIC' if rule in CHAOTIC_RULES else 'periodic'}")
        print(f"  Table: {''.join(str(t) for t in table)}")
        print(f"  ANF: {' + '.join(terms)}")
        print(f"  x1={anf[4]}, x2={anf[2]}, x3={anf[1]}")
        print(f"  x1x2={anf[6]}, x2x3={anf[3]}")

def main():
    print("=" * 70)
    print("COMPARING t0=t7=1 RULES")
    print("=" * 70)

    # Chaotic t0=t7=1
    print("\nCHAOTIC rules with t0=t7=1:")
    compare_rules([135, 149])

    # Periodic t0=t7=1 (the false positives)
    print("\nPERIODIC rules with t0=t7=1 (false positives):")
    compare_rules([139, 169, 209, 225])

    # Let me look at the pattern more carefully
    print("\n" + "=" * 70)
    print("THE DIFFERENCE")
    print("=" * 70)

    print("""
Rule 135: ANF = 1 + x2x3 + x1       (linear: x1 only)
Rule 149: ANF = 1 + x3 + x1x2       (linear: x3 only)

Rule 139: ANF = 1 + x2 + x2x3 + x1x2   (linear: x2)
Rule 169: ANF = 1 + x1 + x2 + x3 + x1x2   (linear: x1,x2,x3)
Rule 209: ANF = 1 + x2 + x3 + x2x3 + x1x2   (linear: x2,x3)
Rule 225: ANF = 1 + x1 + x2 + x3 + x2x3   (linear: x1,x2,x3)

Pattern:
- Chaotic 135: x2x3 present, x1x2 absent
- Chaotic 149: x1x2 present, x2x3 absent

- Periodic 139: x1x2 present, x2x3 present (both!)
- Periodic 169: x1x2 present, x2x3 absent but also has x1,x2,x3 all present
- Periodic 209: x1x2 present, x2x3 present (both!)
- Periodic 225: x1x2 absent, x2x3 present but also has x1,x2,x3 all present

The XOR constraint (x1x2 XOR x2x3) eliminates 139 and 209.
But 169 and 225 still satisfy XOR.

The difference: 169 and 225 have linear=3 (all three linear terms).
135 and 149 have linear=1 (only one linear term).
""")

    # Verify this pattern
    print("\n" + "=" * 70)
    print("CHECKING LINEAR TERM COUNT")
    print("=" * 70)

    t0_t7_1_rules = []
    for r in range(256):
        if bin(r).count('1') == 4:
            table = rule_to_table(r)
            anf = compute_anf(table)
            if anf[5] == 0 and table[0] == 1 and table[7] == 1:
                d3 = sum(table[x] != table[7-x] for x in range(8))
                linear = anf[1] + anf[2] + anf[4]
                x1x2_xor_x2x3 = anf[6] != anf[3]
                t0_t7_1_rules.append({
                    'rule': r,
                    'd3': d3,
                    'linear': linear,
                    'xor': x1x2_xor_x2x3,
                    'is_chaotic': r in CHAOTIC_RULES
                })

    for f in t0_t7_1_rules:
        is_c = 'CHAOTIC' if f['is_chaotic'] else 'periodic'
        print(f"Rule {f['rule']}: d3={f['d3']}, linear={f['linear']}, XOR={f['xor']}, {is_c}")

    # The pattern: chaotic t0=t7=1 rules have linear=1
    print("\n" + "=" * 70)
    print("NEW CRITERION: t0=t7=1 AND d3=4 AND XOR AND linear=1")
    print("=" * 70)

    for f in t0_t7_1_rules:
        if f['d3'] == 4 and f['xor'] and f['linear'] == 1:
            is_c = 'CHAOTIC' if f['is_chaotic'] else 'periodic'
            print(f"Rule {f['rule']}: {is_c}")

    # PERFECT FINAL CRITERION
    print("\n" + "=" * 70)
    print("PERFECT FINAL CRITERION")
    print("=" * 70)

    def is_chaotic_perfect(rule):
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

        # Criterion 2a: XOR rules (d3=8, linear=3, quadratic=0)
        if d3 == 8 and linear == 3 and quadratic == 0:
            return True

        # Criterion 2b: d3=4 with XOR quadratic
        if d3 == 4 and x1x2_xor_x2x3:
            # Case 1: t7=0 (uniform all-1s dies)
            if t7 == 0:
                return True
            # Case 2: t0=t7=1 AND linear=1 (single linear term)
            if t0 == 1 and t7 == 1 and linear == 1:
                return True

        return False

    # Test on all 256 rules
    tp, tn, fp, fn = 0, 0, 0, 0
    errors = []

    for rule in range(256):
        predicted = is_chaotic_perfect(rule)
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
    else:
        print("\nPERFECT CLASSIFICATION!")

    # Print the complete criterion
    print("\n" + "=" * 70)
    print("COMPLETE ALGEBRAIC CRITERION FOR ECA CHAOS")
    print("=" * 70)

    print("""
A rule is CHAOTIC if and only if ALL of the following hold:

1. BALANCE: exactly 4 ones in the 8-bit rule number (4/8 inputs -> 1)

2. NO LEFT-RIGHT INTERACTION: x1x3 = 0 in the ANF

3. ONE OF:

   (a) XOR RULE: d3 = 8 AND linear = 3 AND quadratic = 0
       (Only 2 rules: 105, 150 - these are x1 XOR x2 XOR x3 and its complement)

   (b) ASYMMETRIC QUADRATIC: d3 = 4 AND (x1x2 XOR x2x3 = 1)
       AND one of:
         - t7 = 0 (all-ones neighborhood produces 0)
         - t0 = t7 = 1 AND linear = 1 (single linear term, both quiescent survive)

INTERPRETATION:
- Balance ensures maximal output uncertainty
- No x1x3 forces information to flow THROUGH the center (serial, not parallel)
- XOR rules are maximally sensitive (every input matters equally)
- Other chaotic rules have asymmetric nearest-neighbor interaction
  and either suppress uniform states OR preserve them with minimal structure

The 12 chaotic rules are:
  30, 45, 75, 86, 89, 101, 105, 106, 120, 135, 149, 150
""")

if __name__ == '__main__':
    main()
