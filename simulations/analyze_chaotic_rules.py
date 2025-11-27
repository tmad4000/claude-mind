#!/usr/bin/env python3
"""
Analyze the 12 truly chaotic ECA rules to find what they have in common.

The 12 chaotic rules are: 30, 45, 75, 86, 89, 101, 106, 120, 135, 149, 169, 225

Questions:
1. What do their binary representations have in common?
2. What are their rule tables like?
3. Do they share algebraic properties?
4. What are their Wolfram classifications?
5. Do they form any symmetry groups?
"""

import numpy as np
from collections import Counter

# The 12 truly chaotic rules (never periodic in our comprehensive survey)
CHAOTIC_RULES = [30, 45, 75, 86, 89, 101, 106, 120, 135, 149, 169, 225]

# For comparison: Class IV rules (all periodic)
CLASS_IV = [54, 110, 124, 137, 147, 193]

# The 6 misclassified "Class III" rules (periodic but look chaotic)
MISCLASSIFIED = [22, 73, 129, 161, 181, 182]

def rule_to_binary(rule_num):
    """Convert rule number to 8-bit binary string."""
    return format(rule_num, '08b')

def rule_to_table(rule_num):
    """Convert rule number to rule table (what each neighborhood produces)."""
    binary = rule_to_binary(rule_num)
    # Neighborhoods in standard order: 111, 110, 101, 100, 011, 010, 001, 000
    neighborhoods = ['111', '110', '101', '100', '011', '010', '001', '000']
    table = {}
    for i, nb in enumerate(neighborhoods):
        table[nb] = int(binary[i])
    return table

def count_ones(rule_num):
    """Count the number of 1s in the binary representation."""
    return bin(rule_num).count('1')

def complement(rule_num):
    """Get the complement rule (swap 0s and 1s in output)."""
    return 255 - rule_num

def left_right_reflect(rule_num):
    """Get the left-right reflection of a rule."""
    binary = rule_to_binary(rule_num)
    # Reflect neighborhoods: 111<->111, 110<->011, 101<->101, 100<->001
    # Index mapping: 0->0, 1->4, 2->2, 3->6, 4->1, 5->5, 6->3, 7->7
    mapping = [0, 4, 2, 6, 1, 5, 3, 7]
    reflected = ''.join(binary[mapping[i]] for i in range(8))
    return int(reflected, 2)

def analyze_symmetry(rule_num):
    """Analyze symmetry properties of a rule."""
    comp = complement(rule_num)
    reflect = left_right_reflect(rule_num)
    comp_reflect = complement(reflect)

    return {
        'rule': rule_num,
        'complement': comp,
        'reflection': reflect,
        'comp_reflect': comp_reflect,
        'self_complement': rule_num == comp,
        'self_symmetric': rule_num == reflect,
        'orbit': sorted(set([rule_num, comp, reflect, comp_reflect]))
    }

def analyze_additivity(rule_num):
    """Check if rule is additive (XOR-based) or linear."""
    table = rule_to_table(rule_num)

    # Check if f(a,b,c) = a XOR b XOR c (Rule 150)
    # Check if f(a,b,c) = a XOR c (Rule 90)
    # etc.

    xor_abc = all(
        table[nb] == (int(nb[0]) ^ int(nb[1]) ^ int(nb[2]))
        for nb in table
    )

    xor_ac = all(
        table[nb] == (int(nb[0]) ^ int(nb[2]))
        for nb in table
    )

    return {
        'xor_abc': xor_abc,  # Rule 150
        'xor_ac': xor_ac,    # Rule 90
    }

def analyze_totalistic_component(rule_num):
    """Check if rule only depends on count of 1s in neighborhood."""
    table = rule_to_table(rule_num)

    # Group neighborhoods by sum
    by_sum = {0: [], 1: [], 2: [], 3: []}
    for nb, output in table.items():
        s = sum(int(c) for c in nb)
        by_sum[s].append(output)

    # Check if all neighborhoods with same sum give same output
    totalistic = all(len(set(outputs)) <= 1 for outputs in by_sum.values())

    # Even if not totalistic, check consistency
    consistency = {s: len(set(outputs)) for s, outputs in by_sum.items()}

    return {
        'is_totalistic': totalistic,
        'sum_consistency': consistency,
        'by_sum': {s: set(outputs) for s, outputs in by_sum.items()}
    }

def analyze_quiescent(rule_num):
    """Check quiescent states (self-replicating patterns of all 0s or all 1s)."""
    table = rule_to_table(rule_num)

    return {
        'zeros_quiescent': table['000'] == 0,
        'ones_quiescent': table['111'] == 1,
        'both_quiescent': table['000'] == 0 and table['111'] == 1,
    }

def get_wolfram_class(rule_num):
    """Return Wolfram's original classification (approximate)."""
    # Based on standard references
    class_i = [0, 8, 32, 40, 128, 136, 160, 168, 64, 72, 96, 104, 192, 200, 224, 232]  # Homogeneous
    class_ii = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 19, 23, 24, 25, 26, 27, 28, 29, 33, 34, 35, 36, 37, 38, 42, 43, 44, 46, 50, 51, 56, 57, 58, 62, 74, 76, 77, 78, 94, 108, 130, 132, 134, 138, 140, 142, 152, 154, 156, 162, 164, 170, 172, 178, 184, 194, 196, 204, 206]  # Periodic (partial list)
    class_iii = [18, 22, 30, 45, 60, 73, 90, 105, 122, 126, 129, 146, 150, 161, 182]  # Chaotic
    class_iv = [54, 110, 124, 137, 147, 193]  # Complex

    if rule_num in class_i:
        return 'I'
    elif rule_num in class_iv:
        return 'IV'
    elif rule_num in class_iii:
        return 'III'
    else:
        return 'II'  # Default

def main():
    print("=" * 70)
    print("ANALYSIS OF THE 12 TRULY CHAOTIC ECA RULES")
    print("Rules: 30, 45, 75, 86, 89, 101, 106, 120, 135, 149, 169, 225")
    print("=" * 70)

    print("\n1. BINARY REPRESENTATIONS")
    print("-" * 40)
    one_counts = []
    for rule in CHAOTIC_RULES:
        binary = rule_to_binary(rule)
        ones = count_ones(rule)
        one_counts.append(ones)
        print(f"Rule {rule:3d}: {binary} ({ones} ones)")

    print(f"\nDistribution of 1s: {Counter(one_counts)}")
    print(f"Mean: {np.mean(one_counts):.2f}, Std: {np.std(one_counts):.2f}")

    # Compare with other groups
    print("\nComparison of 1-bit counts:")
    class_iv_ones = [count_ones(r) for r in CLASS_IV]
    misclass_ones = [count_ones(r) for r in MISCLASSIFIED]
    print(f"  Chaotic:       mean={np.mean(one_counts):.2f} ({Counter(one_counts)})")
    print(f"  Class IV:      mean={np.mean(class_iv_ones):.2f} ({Counter(class_iv_ones)})")
    print(f"  Misclassified: mean={np.mean(misclass_ones):.2f} ({Counter(misclass_ones)})")

    print("\n2. SYMMETRY ANALYSIS")
    print("-" * 40)
    orbits = []
    for rule in CHAOTIC_RULES:
        sym = analyze_symmetry(rule)
        print(f"Rule {rule:3d}: orbit = {sym['orbit']}")
        orbits.append(tuple(sym['orbit']))

    # Check for orbit overlaps with chaotic rules
    unique_orbits = set(orbits)
    print(f"\nUnique orbits: {len(unique_orbits)}")

    # Check if chaotic rules form complete orbits
    all_chaotic = set(CHAOTIC_RULES)
    for orbit in unique_orbits:
        overlap = all_chaotic & set(orbit)
        non_overlap = set(orbit) - all_chaotic
        if len(overlap) < len(orbit):
            print(f"  Orbit {orbit}: {len(overlap)}/{len(orbit)} chaotic, non-chaotic: {non_overlap}")

    print("\n3. QUIESCENT STATE ANALYSIS")
    print("-" * 40)
    quiescent_stats = {'zeros': 0, 'ones': 0, 'both': 0, 'neither': 0}
    for rule in CHAOTIC_RULES:
        q = analyze_quiescent(rule)
        if q['both_quiescent']:
            quiescent_stats['both'] += 1
            status = "both"
        elif q['zeros_quiescent']:
            quiescent_stats['zeros'] += 1
            status = "zeros"
        elif q['ones_quiescent']:
            quiescent_stats['ones'] += 1
            status = "ones"
        else:
            quiescent_stats['neither'] += 1
            status = "neither"
        print(f"Rule {rule:3d}: 000->{rule_to_table(rule)['000']}, 111->{rule_to_table(rule)['111']} ({status})")

    print(f"\nQuiescent statistics: {quiescent_stats}")

    print("\n4. TOTALISTIC COMPONENT ANALYSIS")
    print("-" * 40)
    for rule in CHAOTIC_RULES:
        tot = analyze_totalistic_component(rule)
        print(f"Rule {rule:3d}: totalistic={tot['is_totalistic']}, by_sum={tot['by_sum']}")

    print("\n5. RULE TABLE STRUCTURE")
    print("-" * 40)
    print("Neighborhood: 111 110 101 100 011 010 001 000")
    for rule in CHAOTIC_RULES:
        table = rule_to_table(rule)
        outputs = [str(table[nb]) for nb in ['111', '110', '101', '100', '011', '010', '001', '000']]
        print(f"Rule {rule:3d}:     {' '.join(f' {o} ' for o in outputs)}")

    # Look for common patterns in the rule table
    print("\n6. LOOKING FOR COMMON PATTERNS")
    print("-" * 40)

    # Check specific neighborhood behaviors
    neighborhoods = ['111', '110', '101', '100', '011', '010', '001', '000']
    for nb in neighborhoods:
        outputs = [rule_to_table(rule)[nb] for rule in CHAOTIC_RULES]
        print(f"  {nb}: {outputs} (mean: {np.mean(outputs):.2f})")

    # Check for universal patterns
    print("\nChecking for universal constraints on chaotic rules:")

    # Is there any neighborhood that's always 0 or always 1 for chaotic rules?
    for nb in neighborhoods:
        outputs = [rule_to_table(rule)[nb] for rule in CHAOTIC_RULES]
        if len(set(outputs)) == 1:
            print(f"  FOUND: All chaotic rules have {nb} -> {outputs[0]}")

    # Check pairs of neighborhoods
    print("\nChecking neighborhood correlations:")
    for i, nb1 in enumerate(neighborhoods):
        for nb2 in neighborhoods[i+1:]:
            outputs1 = [rule_to_table(rule)[nb1] for rule in CHAOTIC_RULES]
            outputs2 = [rule_to_table(rule)[nb2] for rule in CHAOTIC_RULES]
            # Check if they're always equal or always opposite
            always_equal = all(o1 == o2 for o1, o2 in zip(outputs1, outputs2))
            always_opposite = all(o1 != o2 for o1, o2 in zip(outputs1, outputs2))
            if always_equal:
                print(f"  {nb1} == {nb2} for all chaotic rules")
            if always_opposite:
                print(f"  {nb1} != {nb2} for all chaotic rules")

    print("\n7. ALGEBRAIC PROPERTIES")
    print("-" * 40)
    for rule in CHAOTIC_RULES:
        add = analyze_additivity(rule)
        if add['xor_abc']:
            print(f"Rule {rule:3d}: XOR(a,b,c)")
        elif add['xor_ac']:
            print(f"Rule {rule:3d}: XOR(a,c)")
        else:
            print(f"Rule {rule:3d}: non-additive")

    print("\n8. RELATIONSHIP TO WOLFRAM CLASSIFICATION")
    print("-" * 40)
    for rule in CHAOTIC_RULES:
        wclass = get_wolfram_class(rule)
        print(f"Rule {rule:3d}: Wolfram Class {wclass}")

    # Count by class
    classes = [get_wolfram_class(r) for r in CHAOTIC_RULES]
    print(f"\nDistribution: {Counter(classes)}")

    print("\n9. COMPLEMENT AND REFLECTION RELATIONSHIPS")
    print("-" * 40)
    # Which chaotic rules are related by complement/reflection?
    all_chaotic_set = set(CHAOTIC_RULES)
    for rule in CHAOTIC_RULES:
        sym = analyze_symmetry(rule)
        related = []
        if sym['complement'] in all_chaotic_set and sym['complement'] != rule:
            related.append(f"comp={sym['complement']}")
        if sym['reflection'] in all_chaotic_set and sym['reflection'] != rule:
            related.append(f"refl={sym['reflection']}")
        if sym['comp_reflect'] in all_chaotic_set and sym['comp_reflect'] != rule:
            related.append(f"c_r={sym['comp_reflect']}")

        if related:
            print(f"Rule {rule:3d}: {', '.join(related)}")
        else:
            print(f"Rule {rule:3d}: no chaotic relatives in orbit")

if __name__ == '__main__':
    main()
