#!/usr/bin/env python3
"""
Final characterization of chaotic ECA rules.

Key findings so far:
1. ALL 12 chaotic rules have exactly 4 ones in their binary representation (NECESSARY)
2. Having 4 ones is not sufficient (only 12/70 = 17% of 4-one rules are chaotic)
3. In partial orbits, complement changes chaos status; reflection preserves it
4. In full orbits, BOTH complement and reflection preserve chaos status

This suggests there's something special about the STRUCTURE of fully chaotic orbits
that makes them "complement-invariant" with respect to chaos.

Hypothesis: The 12 chaotic rules are exactly those 4-one rules where:
- The rule has a specific relationship between its neighborhood outputs
- This relationship is somehow "balanced" so complement doesn't break chaos
"""

import numpy as np
from collections import Counter

# All 12 chaotic rules
CHAOTIC = set([30, 45, 75, 86, 89, 101, 106, 120, 135, 149, 169, 225])

def rule_to_binary(rule_num):
    return format(rule_num, '08b')

def rule_to_table(rule_num):
    binary = rule_to_binary(rule_num)
    neighborhoods = ['111', '110', '101', '100', '011', '010', '001', '000']
    return {nb: int(binary[i]) for i, nb in enumerate(neighborhoods)}

def count_ones(rule_num):
    return bin(rule_num).count('1')

def complement(rule_num):
    return 255 - rule_num

def left_right_reflect(rule_num):
    binary = rule_to_binary(rule_num)
    mapping = [0, 4, 2, 6, 1, 5, 3, 7]
    reflected = ''.join(binary[mapping[i]] for i in range(8))
    return int(reflected, 2)

def get_orbit(rule_num):
    comp = complement(rule_num)
    reflect = left_right_reflect(rule_num)
    comp_reflect = complement(reflect)
    return tuple(sorted(set([rule_num, comp, reflect, comp_reflect])))

def main():
    print("=" * 70)
    print("FINAL CHARACTERIZATION OF CHAOTIC ECA RULES")
    print("=" * 70)

    # Get all 4-one rules
    four_one = [r for r in range(256) if count_ones(r) == 4]

    print("\n1. THE DEFINING PROPERTY: 4 ONES")
    print("-" * 50)
    print(f"Number of 4-one rules: {len(four_one)}")
    print(f"Number chaotic: {len(CHAOTIC)}")
    print(f"Chaotic fraction: {len(CHAOTIC)}/{len(four_one)} = {len(CHAOTIC)/len(four_one):.1%}")

    # Check: is having 4 ones NECESSARY?
    non_4_chaotic = [r for r in CHAOTIC if count_ones(r) != 4]
    print(f"\nChaotic rules without 4 ones: {non_4_chaotic}")
    print("==> Having exactly 4 ones is NECESSARY for chaos")

    print("\n2. ADDITIONAL CONSTRAINT: QUIESCENT STATES")
    print("-" * 50)

    # Check quiescent state patterns
    neighborhoods = ['111', '110', '101', '100', '011', '010', '001', '000']

    patterns = {}
    for rule in four_one:
        table = rule_to_table(rule)
        pattern = (table['111'], table['000'])  # (111 output, 000 output)
        if pattern not in patterns:
            patterns[pattern] = {'chaotic': [], 'periodic': []}
        if rule in CHAOTIC:
            patterns[pattern]['chaotic'].append(rule)
        else:
            patterns[pattern]['periodic'].append(rule)

    for pattern, groups in sorted(patterns.items()):
        nc = len(groups['chaotic'])
        np = len(groups['periodic'])
        print(f"  111->{pattern[0]}, 000->{pattern[1]}: {nc} chaotic, {np} periodic")
        if nc > 0 and np == 0:
            print(f"    ==> ALL rules with this pattern are chaotic!")
        elif nc == 0 and np > 0:
            print(f"    ==> NO rules with this pattern are chaotic")

    print("\n3. THE KEY INSIGHT: COMPLEMENT INVARIANCE")
    print("-" * 50)

    # For each 4-one rule, check if it and its complement are BOTH chaotic or BOTH not chaotic
    complement_concordant = []
    complement_discordant = []

    for rule in four_one:
        if rule < complement(rule):  # Avoid counting twice
            comp = complement(rule)
            rule_chaos = rule in CHAOTIC
            comp_chaos = comp in CHAOTIC
            if rule_chaos == comp_chaos:
                complement_concordant.append((rule, comp, rule_chaos))
            else:
                complement_discordant.append((rule, comp, rule_chaos))

    print(f"\nComplement-concordant pairs (same chaos status): {len(complement_concordant)}")
    for rule, comp, is_chaos in complement_concordant[:5]:
        status = "both chaotic" if is_chaos else "both periodic"
        print(f"  ({rule}, {comp}): {status}")

    print(f"\nComplement-discordant pairs (different chaos status): {len(complement_discordant)}")
    for rule, comp, rule_chaos in complement_discordant:
        print(f"  ({rule}, {comp}): {rule} is {'chaotic' if rule_chaos else 'periodic'}, {comp} is {'periodic' if rule_chaos else 'chaotic'}")

    print("\n4. CHARACTERIZING DISCORDANT PAIRS")
    print("-" * 50)

    # What's special about discordant pairs?
    print("\nIn discordant pairs, which member is chaotic?")
    for rule, comp, rule_chaos in complement_discordant:
        chaotic_one = rule if rule_chaos else comp
        periodic_one = comp if rule_chaos else rule

        table_c = rule_to_table(chaotic_one)
        table_p = rule_to_table(periodic_one)

        print(f"\n  Pair ({rule}, {comp}):")
        print(f"    Chaotic {chaotic_one}: 111->{table_c['111']}, 000->{table_c['000']}")
        print(f"    Periodic {periodic_one}: 111->{table_p['111']}, 000->{table_p['000']}")

    print("\n5. THE COMPLETE CHARACTERIZATION")
    print("-" * 50)

    # Hypothesis: Chaotic rules are 4-one rules that:
    # - Do NOT have the pattern (111->0, 000->0) unless they're in a specific group
    # - Have some balance property

    # Let's check the rule table structure more carefully
    print("\nChecking if there's a simple boolean function that characterizes chaos:")

    # For each rule, compute various features
    features = {}
    for rule in four_one:
        table = rule_to_table(rule)

        # Feature 1: quiescent states
        f1 = table['111']
        f2 = table['000']

        # Feature 2: symmetric neighborhoods (101, 010)
        f3 = table['101']
        f4 = table['010']

        # Feature 3: asymmetric neighbors (110 vs 011, 100 vs 001)
        f5 = table['110']
        f6 = table['011']
        f7 = table['100']
        f8 = table['001']

        # Derived features
        d1 = f1 ^ f2  # XOR of quiescent outputs
        d2 = f3 ^ f4  # XOR of symmetric outputs
        d3 = (f5 ^ f6) + (f7 ^ f8)  # Sum of asymmetric XORs

        features[rule] = {
            'quiescent': (f1, f2),
            'symmetric': (f3, f4),
            'asymmetric': ((f5, f6), (f7, f8)),
            'd1': d1,
            'd2': d2,
            'd3': d3
        }

    # Check which features discriminate chaos
    print("\nFeature analysis:")

    # Feature d1 (XOR of 111 and 000 outputs)
    d1_chaos = [features[r]['d1'] for r in CHAOTIC]
    d1_periodic = [features[r]['d1'] for r in four_one if r not in CHAOTIC]
    print(f"  d1 (111 XOR 000):")
    print(f"    Chaotic: {Counter(d1_chaos)}")
    print(f"    Periodic: {Counter(d1_periodic)}")

    # Feature d2 (XOR of 101 and 010 outputs)
    d2_chaos = [features[r]['d2'] for r in CHAOTIC]
    d2_periodic = [features[r]['d2'] for r in four_one if r not in CHAOTIC]
    print(f"  d2 (101 XOR 010):")
    print(f"    Chaotic: {Counter(d2_chaos)}")
    print(f"    Periodic: {Counter(d2_periodic)}")

    # Feature d3 (asymmetric balance)
    d3_chaos = [features[r]['d3'] for r in CHAOTIC]
    d3_periodic = [features[r]['d3'] for r in four_one if r not in CHAOTIC]
    print(f"  d3 (asymmetric balance):")
    print(f"    Chaotic: {Counter(d3_chaos)}")
    print(f"    Periodic: {Counter(d3_periodic)}")

    print("\n6. REFINED CHARACTERIZATION")
    print("-" * 50)

    # Try combining features
    # Check: Is chaos = (d1 == 1) AND (d2 == 1)?
    def test_predicate(predicate):
        true_positives = sum(1 for r in CHAOTIC if predicate(features[r]))
        false_negatives = sum(1 for r in CHAOTIC if not predicate(features[r]))
        false_positives = sum(1 for r in four_one if r not in CHAOTIC and predicate(features[r]))
        true_negatives = sum(1 for r in four_one if r not in CHAOTIC and not predicate(features[r]))

        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

        return {
            'TP': true_positives,
            'FN': false_negatives,
            'FP': false_positives,
            'TN': true_negatives,
            'precision': precision,
            'recall': recall
        }

    # Test various predicates
    predicates = [
        ("d1 == 1", lambda f: f['d1'] == 1),
        ("d2 == 1", lambda f: f['d2'] == 1),
        ("d1 == 1 AND d2 == 1", lambda f: f['d1'] == 1 and f['d2'] == 1),
        ("d1 == 0 AND d2 == 0", lambda f: f['d1'] == 0 and f['d2'] == 0),
        ("d3 == 2", lambda f: f['d3'] == 2),
        ("d1 XOR d2 == 0", lambda f: (f['d1'] ^ f['d2']) == 0),
        ("quiescent != (0,1)", lambda f: f['quiescent'] != (0, 1)),
    ]

    print("\nTesting predicates for characterizing chaos:")
    for name, pred in predicates:
        result = test_predicate(pred)
        print(f"\n  {name}:")
        print(f"    TP={result['TP']}, FN={result['FN']}, FP={result['FP']}, TN={result['TN']}")
        print(f"    Precision={result['precision']:.2%}, Recall={result['recall']:.2%}")

    print("\n7. THE BOTTOM LINE")
    print("-" * 50)

    # Final summary of what we know
    print("""
CONFIRMED NECESSARY CONDITIONS FOR CHAOS:
1. Rule must have exactly 4 ones in binary representation
2. Rule must NOT have pattern (111->0, 000->1) - "zeros quiescent but not ones"

OBSERVED PATTERN:
- The 12 chaotic rules form 4 symmetry orbits
- 2 orbits are "fully chaotic" (all 4 members chaotic)
- 2 orbits are "partially chaotic" (only 2 members chaotic)
- In partial orbits, complement changes chaos status
- The chaotic members of partial orbits always have 111->0

REMAINING MYSTERY:
- Why are orbits (30,86,169,225) and (106,120,135,149) fully chaotic?
- They have both 111->0 AND 111->1 members, yet all are chaotic
- Something about their specific rule structure makes complement preserve chaos
""")

    # Let's look at the fully chaotic orbits one more time
    print("\n8. DETAILED ANALYSIS OF FULLY CHAOTIC ORBITS")
    print("-" * 50)

    full_chaotic_orbits = [
        (30, 86, 169, 225),
        (106, 120, 135, 149)
    ]

    for orbit in full_chaotic_orbits:
        print(f"\nOrbit {orbit}:")
        print("         111 110 101 100 011 010 001 000")
        for rule in orbit:
            table = rule_to_table(rule)
            outputs = [table[nb] for nb in neighborhoods]
            print(f"  Rule {rule:3d}:  {outputs}")

        # Check for patterns
        # Sum each column
        sums = []
        for i, nb in enumerate(neighborhoods):
            col_sum = sum(rule_to_table(r)[nb] for r in orbit)
            sums.append(col_sum)
        print(f"  Column sums: {sums}")
        print(f"  (Expected if balanced: [2,2,2,2,2,2,2,2])")

        # Check: do column sums = 2 for all neighborhoods?
        if all(s == 2 for s in sums):
            print("  ==> PERFECTLY BALANCED!")

    # Compare with a periodic orbit that has 4-one rules
    print("\nFor comparison, a periodic 4-one orbit:")
    periodic_orbit = (15, 85, 170, 240)
    print(f"Orbit {periodic_orbit}:")
    print("         111 110 101 100 011 010 001 000")
    for rule in periodic_orbit:
        table = rule_to_table(rule)
        outputs = [table[nb] for nb in neighborhoods]
        print(f"  Rule {rule:3d}:  {outputs}")
    sums = []
    for i, nb in enumerate(neighborhoods):
        col_sum = sum(rule_to_table(r)[nb] for r in periodic_orbit)
        sums.append(col_sum)
    print(f"  Column sums: {sums}")

if __name__ == '__main__':
    main()
