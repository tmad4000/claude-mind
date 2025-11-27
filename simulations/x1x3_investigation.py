#!/usr/bin/env python3
"""
Investigating the x1x3 term absence in chaotic rules.

Discovery: NO chaotic rule has the x1x3 term in its ANF (Algebraic Normal Form).
This means no chaotic rule has direct interaction between left and right neighbors.

This suggests chaos requires a specific FLOW pattern where information passes
through the center cell rather than jumping across.
"""

import numpy as np
from itertools import combinations

# The 12 chaotic rules
CHAOTIC_RULES = [30, 45, 75, 86, 89, 101, 105, 106, 120, 135, 149, 150]

def rule_to_table(rule):
    """Convert rule number to lookup table"""
    return [(rule >> i) & 1 for i in range(8)]

def compute_anf(table):
    """Compute Algebraic Normal Form using Mobius transform"""
    n = 3
    anf = np.array(table, dtype=np.int64)

    for i in range(n):
        for j in range(2**n):
            if (j >> i) & 1:
                anf[j] ^= anf[j ^ (1 << i)]

    return anf

def has_x1x3_term(rule):
    """Check if rule has x1x3 term (index 5 in ANF)"""
    table = rule_to_table(rule)
    anf = compute_anf(table)
    return anf[5] == 1

def get_balanced_rules():
    """Get all 70 balanced rules"""
    return [r for r in range(256) if bin(r).count('1') == 4]

def analyze_x1x3():
    """Deep analysis of the x1x3 term"""
    print("=" * 70)
    print("THE x1x3 HYPOTHESIS: No chaotic rule has left-right interaction term")
    print("=" * 70)

    balanced = get_balanced_rules()

    # Check if this is a perfect discriminator
    rules_with_x1x3 = [r for r in balanced if has_x1x3_term(r)]
    rules_without_x1x3 = [r for r in balanced if not has_x1x3_term(r)]

    chaotic_with_x1x3 = [r for r in rules_with_x1x3 if r in CHAOTIC_RULES]
    chaotic_without_x1x3 = [r for r in rules_without_x1x3 if r in CHAOTIC_RULES]

    print(f"\nBalanced rules with x1x3: {len(rules_with_x1x3)}")
    print(f"Balanced rules without x1x3: {len(rules_without_x1x3)}")
    print(f"Chaotic rules with x1x3: {len(chaotic_with_x1x3)} -> {chaotic_with_x1x3}")
    print(f"Chaotic rules without x1x3: {len(chaotic_without_x1x3)} -> {chaotic_without_x1x3}")

    # Classification metrics
    print("\nIf we predict 'chaotic' for rules WITHOUT x1x3:")
    tp = len(chaotic_without_x1x3)
    fn = len(chaotic_with_x1x3)
    tn = len(rules_with_x1x3) - len(chaotic_with_x1x3)
    fp = len(rules_without_x1x3) - len(chaotic_without_x1x3)

    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0

    print(f"  True Positives: {tp}")
    print(f"  False Negatives: {fn}")
    print(f"  True Negatives: {tn}")
    print(f"  False Positives: {fp}")
    print(f"  Sensitivity: {sensitivity:.2%}")
    print(f"  Specificity: {specificity:.2%}")

    # Understanding what x1x3 absence means
    print("\n" + "=" * 70)
    print("INFORMATION FLOW INTERPRETATION")
    print("=" * 70)

    print("""
The x1x3 term represents: Does changing BOTH left and right neighbors
(while keeping center fixed) affect the output differently than predicted
by their individual effects?

x1x3 = 1 means: Left and right neighbors INTERACT (XOR together affects output)
x1x3 = 0 means: Left and right effects are INDEPENDENT

For chaotic rules: x1x3 = 0 ALWAYS

Interpretation: In chaotic rules, information from left and right neighbors
flows THROUGH the center cell independently. There's no "shortcut" where
left and right combine directly.

This creates a serial information flow:
  LEFT -> CENTER -> RIGHT (and vice versa)

Rather than parallel:
  LEFT + RIGHT -> CENTER (direct interaction)

Serial flow might be necessary for chaos because it prevents cancellation
and creates more complex dynamics.
""")

    # Look at the ANF structure of chaotic rules
    print("=" * 70)
    print("ANF STRUCTURE OF CHAOTIC RULES")
    print("=" * 70)

    anf_names = ['1', 'x3', 'x2', 'x2x3', 'x1', 'x1x3', 'x1x2', 'x1x2x3']

    for rule in CHAOTIC_RULES:
        table = rule_to_table(rule)
        anf = compute_anf(table)
        terms = [anf_names[i] for i in range(8) if anf[i] == 1]
        print(f"Rule {rule:3d}: {' + '.join(terms)}")

    # Group by structure
    print("\n" + "=" * 70)
    print("GROUPED BY ANF STRUCTURE")
    print("=" * 70)

    structures = {}
    for rule in CHAOTIC_RULES:
        table = rule_to_table(rule)
        anf = compute_anf(table)
        key = tuple(anf.tolist())
        if key not in structures:
            structures[key] = []
        structures[key].append(rule)

    for anf_tuple, rules in structures.items():
        terms = [anf_names[i] for i in range(8) if anf_tuple[i] == 1]
        print(f"ANF: {' + '.join(terms)}")
        print(f"  Rules: {rules}")

    # Check what happens with x1x2 term (also interesting)
    print("\n" + "=" * 70)
    print("x1x2 TERM ANALYSIS (left-center interaction)")
    print("=" * 70)

    for rule in CHAOTIC_RULES:
        table = rule_to_table(rule)
        anf = compute_anf(table)
        has_x1x2 = anf[6] == 1
        has_x2x3 = anf[3] == 1
        print(f"Rule {rule:3d}: x1x2={has_x1x2}, x2x3={has_x2x3}")

    # Check combined criteria
    print("\n" + "=" * 70)
    print("COMBINED CRITERION: NOT x1x3 AND (has x1 OR has x3)")
    print("=" * 70)

    candidates = []
    for rule in balanced:
        table = rule_to_table(rule)
        anf = compute_anf(table)
        has_x1 = anf[4] == 1
        has_x3 = anf[1] == 1
        no_x1x3 = anf[5] == 0

        if no_x1x3 and (has_x1 or has_x3):
            candidates.append(rule)

    print(f"Rules matching criterion: {len(candidates)}")
    print(f"Chaotic among them: {len([r for r in candidates if r in CHAOTIC_RULES])}")
    print(f"Precision: {100*len([r for r in candidates if r in CHAOTIC_RULES])/len(candidates):.1f}%")

    # The key pattern
    print("\n" + "=" * 70)
    print("COUNTING TERMS PATTERN")
    print("=" * 70)

    for rule in CHAOTIC_RULES:
        table = rule_to_table(rule)
        anf = compute_anf(table)
        linear_terms = anf[1] + anf[2] + anf[4]  # x1, x2, x3
        quadratic_terms = anf[3] + anf[5] + anf[6]  # x1x2, x1x3, x2x3
        constant = anf[0]
        print(f"Rule {rule:3d}: constant={constant}, linear={linear_terms}, quadratic={quadratic_terms}")

    # Check the pattern more carefully
    print("\n" + "=" * 70)
    print("TESTING: linear >= 2 AND no x1x3")
    print("=" * 70)

    for rule in balanced:
        table = rule_to_table(rule)
        anf = compute_anf(table)
        linear = anf[1] + anf[2] + anf[4]
        no_x1x3 = anf[5] == 0

        if linear >= 2 and no_x1x3:
            is_chaotic = rule in CHAOTIC_RULES
            print(f"Rule {rule:3d}: linear={linear}, chaotic={is_chaotic}")

if __name__ == '__main__':
    analyze_x1x3()
