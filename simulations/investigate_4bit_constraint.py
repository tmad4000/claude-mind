#!/usr/bin/env python3
"""
Investigate the 4-bit constraint on chaotic rules.

DISCOVERY: All 12 chaotic rules have EXACTLY 4 ones in their binary representation!
This is statistically unlikely (only 70/256 rules have 4 ones).

Questions:
1. How many rules have exactly 4 ones?
2. What fraction of 4-one rules are chaotic? (12/70 = 17%?)
3. Are there periodic rules with 4 ones? What distinguishes them?
4. Is having 4 ones necessary for chaos?
5. Is it sufficient? (Clearly not, since only 12/70 are chaotic)
6. What additional constraint makes a 4-one rule chaotic?
"""

import numpy as np
from collections import Counter
import json

# The 12 truly chaotic rules
CHAOTIC_RULES = set([30, 45, 75, 86, 89, 101, 106, 120, 135, 149, 169, 225])

def rule_to_binary(rule_num):
    """Convert rule number to 8-bit binary string."""
    return format(rule_num, '08b')

def count_ones(rule_num):
    """Count the number of 1s in the binary representation."""
    return bin(rule_num).count('1')

def complement(rule_num):
    """Get the complement rule."""
    return 255 - rule_num

def left_right_reflect(rule_num):
    """Get the left-right reflection of a rule."""
    binary = rule_to_binary(rule_num)
    mapping = [0, 4, 2, 6, 1, 5, 3, 7]
    reflected = ''.join(binary[mapping[i]] for i in range(8))
    return int(reflected, 2)

def get_orbit(rule_num):
    """Get the symmetry orbit of a rule."""
    comp = complement(rule_num)
    reflect = left_right_reflect(rule_num)
    comp_reflect = complement(reflect)
    return tuple(sorted(set([rule_num, comp, reflect, comp_reflect])))

def rule_to_table(rule_num):
    """Convert rule number to rule table."""
    binary = rule_to_binary(rule_num)
    neighborhoods = ['111', '110', '101', '100', '011', '010', '001', '000']
    return {nb: int(binary[i]) for i, nb in enumerate(neighborhoods)}

def main():
    print("=" * 70)
    print("INVESTIGATING THE 4-BIT CONSTRAINT ON CHAOTIC RULES")
    print("=" * 70)

    # 1. Count rules by number of ones
    print("\n1. DISTRIBUTION OF RULES BY NUMBER OF ONES")
    print("-" * 40)
    by_ones = {i: [] for i in range(9)}
    for rule in range(256):
        ones = count_ones(rule)
        by_ones[ones].append(rule)

    for ones, rules in by_ones.items():
        n = len(rules)
        from math import comb
        expected = comb(8, ones)
        chaotic_in_group = len(set(rules) & CHAOTIC_RULES)
        print(f"  {ones} ones: {n} rules (C(8,{ones})={expected}), {chaotic_in_group} chaotic")

    # 2. All 4-one rules
    print("\n2. ALL 70 RULES WITH EXACTLY 4 ONES")
    print("-" * 40)
    four_one_rules = by_ones[4]
    print(f"Total: {len(four_one_rules)}")

    # Group by whether they're chaotic
    chaotic_4 = sorted(set(four_one_rules) & CHAOTIC_RULES)
    periodic_4 = sorted(set(four_one_rules) - CHAOTIC_RULES)

    print(f"\nChaotic (12): {chaotic_4}")
    print(f"\nPeriodic (58): {periodic_4}")

    # 3. What distinguishes chaotic 4-one rules from periodic ones?
    print("\n3. COMPARING CHAOTIC VS PERIODIC 4-ONE RULES")
    print("-" * 40)

    # Group periodic rules by orbit with chaotic rules
    print("\nSymmetry orbit analysis:")
    chaotic_orbits = set()
    for rule in chaotic_4:
        chaotic_orbits.add(get_orbit(rule))

    print(f"Unique chaotic orbits: {len(chaotic_orbits)}")
    for orbit in sorted(chaotic_orbits):
        # Check if all orbit members are in 4-one rules
        all_4 = all(count_ones(r) == 4 for r in orbit)
        chaotic_count = len(set(orbit) & CHAOTIC_RULES)
        print(f"  {orbit}: all 4-ones={all_4}, chaotic={chaotic_count}/{len(orbit)}")

    # 4. Look at specific rule table properties
    print("\n4. RULE TABLE ANALYSIS OF 4-ONE RULES")
    print("-" * 40)

    # Check 111 -> 0 vs 111 -> 1 split
    print("\nSplit by 111 output:")
    for output_111 in [0, 1]:
        chaotic_with = [r for r in chaotic_4 if rule_to_table(r)['111'] == output_111]
        periodic_with = [r for r in periodic_4 if rule_to_table(r)['111'] == output_111]
        print(f"  111->{output_111}: {len(chaotic_with)} chaotic, {len(periodic_with)} periodic")

    # Check 000 output
    print("\nSplit by 000 output:")
    for output_000 in [0, 1]:
        chaotic_with = [r for r in chaotic_4 if rule_to_table(r)['000'] == output_000]
        periodic_with = [r for r in periodic_4 if rule_to_table(r)['000'] == output_000]
        print(f"  000->{output_000}: {len(chaotic_with)} chaotic, {len(periodic_with)} periodic")

    # Check combined quiescent state
    print("\nSplit by quiescent state pattern:")
    patterns = {}
    for rule in four_one_rules:
        table = rule_to_table(rule)
        pattern = f"000->{table['000']}, 111->{table['111']}"
        if pattern not in patterns:
            patterns[pattern] = {'chaotic': 0, 'periodic': 0, 'rules': []}
        if rule in CHAOTIC_RULES:
            patterns[pattern]['chaotic'] += 1
        else:
            patterns[pattern]['periodic'] += 1
        patterns[pattern]['rules'].append(rule)

    for pattern, counts in patterns.items():
        print(f"  {pattern}: {counts['chaotic']} chaotic, {counts['periodic']} periodic")

    # 5. Check if chaotic rules have specific neighborhood patterns
    print("\n5. NEIGHBORHOOD OUTPUT PATTERNS")
    print("-" * 40)

    neighborhoods = ['111', '110', '101', '100', '011', '010', '001', '000']

    print("For each neighborhood, P(chaotic | output=1):")
    for nb in neighborhoods:
        chaotic_1 = len([r for r in chaotic_4 if rule_to_table(r)[nb] == 1])
        periodic_1 = len([r for r in periodic_4 if rule_to_table(r)[nb] == 1])
        total_1 = chaotic_1 + periodic_1
        if total_1 > 0:
            prob = chaotic_1 / total_1
            print(f"  {nb}->1: {chaotic_1}/{total_1} = {prob:.2%}")

    # 6. Look for specific patterns unique to chaotic rules
    print("\n6. PATTERNS UNIQUE TO CHAOTIC 4-ONE RULES")
    print("-" * 40)

    # For each chaotic rule, find the "minimal distinguishing feature"
    # What's the smallest set of neighborhood outputs that separates it from all periodic rules?

    # First, encode all rules as vectors
    def rule_to_vector(rule):
        table = rule_to_table(rule)
        return tuple(table[nb] for nb in neighborhoods)

    chaotic_vectors = {r: rule_to_vector(r) for r in chaotic_4}
    periodic_vectors = {r: rule_to_vector(r) for r in periodic_4}

    # Check for patterns that NO periodic rule has
    # A "pattern" is a partial specification: some positions fixed, others free
    from itertools import combinations

    print("\nSearching for distinguishing partial patterns...")
    found_distinguisher = False

    for num_fixed in range(1, 9):
        if found_distinguisher:
            break
        for positions in combinations(range(8), num_fixed):
            # For each chaotic rule, extract the pattern at these positions
            chaotic_patterns = set()
            for rule in chaotic_4:
                vec = chaotic_vectors[rule]
                pattern = tuple(vec[p] for p in positions)
                chaotic_patterns.add(pattern)

            periodic_patterns = set()
            for rule in periodic_4:
                vec = periodic_vectors[rule]
                pattern = tuple(vec[p] for p in positions)
                periodic_patterns.add(pattern)

            # Check if there's a pattern in chaotic but not periodic
            unique_to_chaotic = chaotic_patterns - periodic_patterns
            unique_to_periodic = periodic_patterns - chaotic_patterns

            if unique_to_chaotic:
                pos_names = [neighborhoods[p] for p in positions]
                print(f"\n  Positions {pos_names}:")
                print(f"    Patterns unique to chaotic: {unique_to_chaotic}")
                # found_distinguisher = True  # Don't stop, show all

    # 7. The key question: can we characterize chaotic rules precisely?
    print("\n7. ATTEMPTING PRECISE CHARACTERIZATION")
    print("-" * 40)

    # Hypothesis: Chaotic rules are exactly the 4-one rules whose orbits...
    # Let's look at the symmetry more carefully

    print("\nAll 4-one rule orbits, categorized:")
    all_orbits_4 = set()
    for rule in four_one_rules:
        all_orbits_4.add(get_orbit(rule))

    for orbit in sorted(all_orbits_4):
        chaotic_count = len(set(orbit) & CHAOTIC_RULES)
        total = len(orbit)
        ones_counts = [count_ones(r) for r in orbit]
        all_same_ones = len(set(ones_counts)) == 1
        label = "CHAOTIC" if chaotic_count > 0 else "periodic"
        # Note: complement flips the number of ones (x -> 8-x)
        # So if orbit has varying ones counts, complement is involved
        print(f"  {orbit}: {label} ({chaotic_count}/{total}), ones={ones_counts}")

    # Count total
    full_chaotic = len([o for o in all_orbits_4 if len(set(o) & CHAOTIC_RULES) == len(o)])
    partial_chaotic = len([o for o in all_orbits_4 if 0 < len(set(o) & CHAOTIC_RULES) < len(o)])
    print(f"\nFully chaotic orbits (all members chaotic): {full_chaotic}")
    print(f"Partially chaotic orbits: {partial_chaotic}")

    # 8. The additive vs non-additive distinction
    print("\n8. XOR/ADDITIVE STRUCTURE")
    print("-" * 40)

    def is_xor_rule(rule):
        """Check if rule is equivalent to some XOR of inputs."""
        table = rule_to_table(rule)
        # XOR patterns: a, b, c, a^b, a^c, b^c, a^b^c, and their negations
        for pattern_type in ['a', 'b', 'c', 'ab', 'ac', 'bc', 'abc']:
            for negate in [False, True]:
                matches = True
                for nb in neighborhoods:
                    a, b, c = int(nb[0]), int(nb[1]), int(nb[2])
                    if pattern_type == 'a':
                        expected = a
                    elif pattern_type == 'b':
                        expected = b
                    elif pattern_type == 'c':
                        expected = c
                    elif pattern_type == 'ab':
                        expected = a ^ b
                    elif pattern_type == 'ac':
                        expected = a ^ c
                    elif pattern_type == 'bc':
                        expected = b ^ c
                    elif pattern_type == 'abc':
                        expected = a ^ b ^ c

                    if negate:
                        expected = 1 - expected

                    if table[nb] != expected:
                        matches = False
                        break

                if matches:
                    return True, pattern_type, negate

        return False, None, None

    # Check XOR structure
    for rule in chaotic_4:
        is_xor, pattern, negate = is_xor_rule(rule)
        neg_str = "NOT " if negate else ""
        if is_xor:
            print(f"  Rule {rule:3d}: {neg_str}XOR({pattern})")
        else:
            print(f"  Rule {rule:3d}: non-XOR")

    print("\n  For comparison, some periodic 4-one rules:")
    for rule in periodic_4[:10]:
        is_xor, pattern, negate = is_xor_rule(rule)
        neg_str = "NOT " if negate else ""
        if is_xor:
            print(f"  Rule {rule:3d}: {neg_str}XOR({pattern})")
        else:
            print(f"  Rule {rule:3d}: non-XOR")

if __name__ == '__main__':
    main()
