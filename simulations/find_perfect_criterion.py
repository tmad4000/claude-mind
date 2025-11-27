#!/usr/bin/env python3
"""
Find a perfect criterion to classify chaotic ECA rules.

We have:
- 4 ones (necessary, 100% recall)
- NOT (111->1, 000->0) (necessary with 4 ones)
- d3 == 1 (necessary)

Combined: 50% precision, 100% recall. We have 12 false positives.

Let's analyze the 12 false positives to find what distinguishes them from true chaotic rules.
"""

from collections import Counter

KNOWN_CHAOTIC = set([30, 45, 75, 86, 89, 101, 106, 120, 135, 149, 169, 225])

# The 12 false positives after applying current criteria
FALSE_POSITIVES = [27, 39, 53, 58, 78, 83, 92, 114, 141, 163, 177, 197]

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
    print("FINDING PERFECT CRITERION FOR CHAOTIC RULES")
    print("=" * 70)

    neighborhoods = ['111', '110', '101', '100', '011', '010', '001', '000']

    print("\n1. COMPARING TRUE CHAOTIC VS FALSE POSITIVES")
    print("-" * 50)

    true_chaotic = sorted(KNOWN_CHAOTIC)

    print("\nTrue chaotic rules:")
    print("Rule  111 110 101 100 011 010 001 000")
    for rule in true_chaotic:
        table = rule_to_table(rule)
        outputs = [table[nb] for nb in neighborhoods]
        print(f"{rule:3d}:   {outputs}")

    print("\nFalse positives:")
    print("Rule  111 110 101 100 011 010 001 000")
    for rule in FALSE_POSITIVES:
        table = rule_to_table(rule)
        outputs = [table[nb] for nb in neighborhoods]
        print(f"{rule:3d}:   {outputs}")

    print("\n2. ORBIT ANALYSIS")
    print("-" * 50)

    # Check orbits of false positives
    fp_orbits = {}
    for rule in FALSE_POSITIVES:
        orbit = get_orbit(rule)
        if orbit not in fp_orbits:
            fp_orbits[orbit] = []
        fp_orbits[orbit].append(rule)

    print("False positive orbits:")
    for orbit, members in sorted(fp_orbits.items()):
        orbit_members_fp = len([r for r in orbit if r in FALSE_POSITIVES])
        print(f"  {orbit}: {len(members)}/{len(orbit)} are FP")

    # Check: do false positive orbits have ANY chaotic members?
    print("\nDo FP orbits contain any chaotic rules?")
    for orbit in sorted(fp_orbits.keys()):
        chaotic_in_orbit = [r for r in orbit if r in KNOWN_CHAOTIC]
        print(f"  {orbit}: chaotic members = {chaotic_in_orbit}")

    print("\n3. DETAILED FEATURE ANALYSIS")
    print("-" * 50)

    def get_all_features(rule):
        table = rule_to_table(rule)

        # Basic features
        f = {nb: table[nb] for nb in neighborhoods}

        # XOR features
        f['xor_111_000'] = table['111'] ^ table['000']
        f['xor_110_011'] = table['110'] ^ table['011']
        f['xor_101_010'] = table['101'] ^ table['010']
        f['xor_100_001'] = table['100'] ^ table['001']

        # d3 components
        f['d3_110_011'] = abs(table['110'] - table['011'])
        f['d3_100_001'] = abs(table['100'] - table['001'])
        f['d3'] = f['d3_110_011'] + f['d3_100_001']

        # Sums
        f['sum_upper'] = table['111'] + table['110'] + table['101'] + table['100']  # First 4 bits
        f['sum_lower'] = table['011'] + table['010'] + table['001'] + table['000']  # Last 4 bits

        # Specific patterns
        f['110_minus_011'] = table['110'] - table['011']
        f['100_minus_001'] = table['100'] - table['001']

        # Center symmetry
        f['sym_center'] = table['101'] + table['010']

        # Edge asymmetry
        f['asym_edge'] = table['110'] + table['011']

        # Transition count (how many 0->1 or 1->0 transitions in the output)
        outputs = [table[nb] for nb in neighborhoods]
        f['transitions'] = sum(1 for i in range(7) if outputs[i] != outputs[i+1])

        # Specific bit patterns
        f['bit_pattern'] = tuple(table[nb] for nb in neighborhoods)

        return f

    features_chaotic = {r: get_all_features(r) for r in true_chaotic}
    features_fp = {r: get_all_features(r) for r in FALSE_POSITIVES}

    # Check each feature
    feature_names = ['xor_110_011', 'xor_101_010', 'xor_100_001', 'd3_110_011', 'd3_100_001',
                     'sum_upper', 'sum_lower', '110_minus_011', '100_minus_001',
                     'sym_center', 'asym_edge', 'transitions']

    print("\nFeature distributions:")
    for fname in feature_names:
        chaotic_vals = [features_chaotic[r][fname] for r in true_chaotic]
        fp_vals = [features_fp[r][fname] for r in FALSE_POSITIVES]
        print(f"  {fname}:")
        print(f"    Chaotic: {Counter(chaotic_vals)}")
        print(f"    FP:      {Counter(fp_vals)}")

    print("\n4. LOOKING FOR SEPARATING FEATURES")
    print("-" * 50)

    # Find features where chaotic and FP don't overlap
    for fname in feature_names:
        chaotic_vals = set(features_chaotic[r][fname] for r in true_chaotic)
        fp_vals = set(features_fp[r][fname] for r in FALSE_POSITIVES)

        if not chaotic_vals.intersection(fp_vals):
            print(f"  {fname}: NO OVERLAP!")
            print(f"    Chaotic: {chaotic_vals}")
            print(f"    FP:      {fp_vals}")

    print("\n5. CHECKING SPECIFIC VALUE CONSTRAINTS")
    print("-" * 50)

    # Check: do all chaotic have certain feature values?
    for fname in feature_names:
        chaotic_vals = set(features_chaotic[r][fname] for r in true_chaotic)
        if len(chaotic_vals) == 1:
            val = list(chaotic_vals)[0]
            # How many FP also have this value?
            fp_with_val = [r for r in FALSE_POSITIVES if features_fp[r][fname] == val]
            print(f"  All chaotic have {fname} = {val}")
            print(f"    FP with same value: {len(fp_with_val)}/{len(FALSE_POSITIVES)}")

    print("\n6. COMBINED FEATURE ANALYSIS")
    print("-" * 50)

    # Try combinations
    # All chaotic have d3 == 1, but so do some FPs

    # Let's look at (110-011, 100-001) pairs
    print("\n(110-011, 100-001) patterns:")
    chaotic_pairs = [
        (features_chaotic[r]['110_minus_011'], features_chaotic[r]['100_minus_001'])
        for r in true_chaotic
    ]
    fp_pairs = [
        (features_fp[r]['110_minus_011'], features_fp[r]['100_minus_001'])
        for r in FALSE_POSITIVES
    ]

    print(f"  Chaotic: {Counter(chaotic_pairs)}")
    print(f"  FP:      {Counter(fp_pairs)}")

    # Check: d3==1 means exactly one of |110-011|==1 or |100-001|==1, not both
    # But we need the XOR to be in a specific direction

    print("\n7. THE KEY INSIGHT: ASYMMETRY DIRECTION")
    print("-" * 50)

    # For d3==1, we either have:
    # - |110-011|=1 and |100-001|=0
    # - |110-011|=0 and |100-001|=1

    def get_asymmetry_type(rule):
        table = rule_to_table(rule)
        d_110_011 = table['110'] - table['011']  # Can be -1, 0, or 1
        d_100_001 = table['100'] - table['001']

        # Type A: 110 > 011 (positive d_110_011)
        # Type B: 110 < 011 (negative d_110_011)
        # Type C: 100 > 001
        # Type D: 100 < 001

        if abs(d_110_011) == 1 and d_100_001 == 0:
            return ('110_011', d_110_011)
        elif d_110_011 == 0 and abs(d_100_001) == 1:
            return ('100_001', d_100_001)
        elif abs(d_110_011) == 1 and abs(d_100_001) == 1:
            return ('both', (d_110_011, d_100_001))
        else:
            return ('zero', (d_110_011, d_100_001))

    print("\nAsymmetry types:")
    for rule in true_chaotic:
        atype = get_asymmetry_type(rule)
        print(f"  Chaotic {rule:3d}: {atype}")

    print()
    for rule in FALSE_POSITIVES:
        atype = get_asymmetry_type(rule)
        print(f"  FP {rule:3d}: {atype}")

    print("\n8. FINAL ANALYSIS: SPECIFIC POSITIONS")
    print("-" * 50)

    # Let's look at specific bit positions
    # Position 0 (111), Position 7 (000) we know are important

    # Check positions 1,2 (110,101) and 5,6 (010,001)
    def get_pair_pattern(rule):
        table = rule_to_table(rule)
        return (
            table['110'], table['101'],  # positions 1,2
            table['100'], table['011'],  # positions 3,4
            table['010'], table['001']   # positions 5,6
        )

    print("\nPair patterns (110,101,100,011,010,001):")
    chaotic_patterns = Counter(get_pair_pattern(r) for r in true_chaotic)
    fp_patterns = Counter(get_pair_pattern(r) for r in FALSE_POSITIVES)

    print("  Chaotic patterns:")
    for p, c in chaotic_patterns.most_common():
        print(f"    {p}: {c}")

    print("  FP patterns:")
    for p, c in fp_patterns.most_common(10):
        print(f"    {p}: {c}")

    # Check overlap
    common = set(chaotic_patterns.keys()) & set(fp_patterns.keys())
    print(f"\n  Common patterns: {len(common)}")
    if len(common) == 0:
        print("  ==> NO OVERLAP! This could be the key.")

    print("\n9. TRYING BINARY CONSTRAINT SEARCH")
    print("-" * 50)

    # Systematically search for boolean predicates that perfectly separate
    # True if: chaotic TP=12, FP=0
    # We'll check single-bit constraints and pairs

    def test_constraint(constraint_func):
        """Returns (TP, FP, FN, TN) for a constraint."""
        tp = sum(1 for r in true_chaotic if constraint_func(r))
        fp = sum(1 for r in FALSE_POSITIVES if constraint_func(r))
        fn = 12 - tp
        tn = 12 - fp
        return tp, fp, fn, tn

    # Single bit constraints on middle 6 bits
    print("\nSingle bit constraints (after 4-ones, NOT(111->1,000->0), d3==1):")
    for nb in neighborhoods[1:-1]:  # Exclude 111 and 000
        for val in [0, 1]:
            def make_constraint(n, v):
                return lambda r: rule_to_table(r)[n] == v
            tp, fp, fn, tn = test_constraint(make_constraint(nb, val))
            if tp == 12 and fp == 0:
                print(f"  FOUND: {nb} == {val} perfectly separates!")
            elif fp == 0 and tp > 0:
                print(f"  {nb} == {val}: TP={tp}, FP={fp}")

    # Try pairs of constraints
    print("\nPair constraints:")
    for i, nb1 in enumerate(neighborhoods):
        for nb2 in neighborhoods[i+1:]:
            for v1 in [0, 1]:
                for v2 in [0, 1]:
                    def make_pair_constraint(n1, val1, n2, val2):
                        return lambda r: rule_to_table(r)[n1] == val1 and rule_to_table(r)[n2] == val2
                    tp, fp, fn, tn = test_constraint(make_pair_constraint(nb1, v1, nb2, v2))
                    if tp > 0 and fp == 0:
                        print(f"  {nb1}=={v1} AND {nb2}=={v2}: TP={tp}, FP={fp}")

if __name__ == '__main__':
    main()
