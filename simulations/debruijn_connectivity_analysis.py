#!/usr/bin/env python3
"""
Deep investigation of de Bruijn graph connectivity and chaos.

Key observation from previous analysis:
ALL 12 chaotic rules have connectivity (2,2) for both 0-inputs and 1-inputs
in the de Bruijn adjacency structure. This is a striking constraint!

This script investigates:
1. What fraction of 4-ones rules have (2,2) connectivity?
2. Is (2,2) connectivity sufficient for chaos?
3. What does (2,2) connectivity mean dynamically?
"""

import numpy as np
from collections import defaultdict

# The 12 chaotic rules
CHAOTIC_RULES = [30, 45, 75, 86, 89, 101, 102, 105, 106, 150, 153, 154]

def rule_to_table(rule):
    """Convert rule number to lookup table."""
    return [(rule >> i) & 1 for i in range(8)]

def count_ones(rule):
    """Count ones in rule's binary representation."""
    return bin(rule).count('1')

def compute_connectivity(rule):
    """
    Compute the de Bruijn connectivity of zero-inputs and one-inputs.
    """
    table = rule_to_table(rule)

    # De Bruijn adjacency: which inputs can follow which?
    # Input i can follow input j if i's first two bits match j's last two bits
    def can_follow(j, i):
        # j -> i transition: j = (a,b,c), i = (b,c,d)
        return ((j >> 0) & 3) == ((i >> 1) & 3)

    zero_inputs = [i for i in range(8) if table[i] == 0]
    one_inputs = [i for i in range(8) if table[i] == 1]

    def count_internal_edges(inputs):
        """Count edges between inputs within the set."""
        count = 0
        for i in inputs:
            for j in inputs:
                if can_follow(j, i):  # j -> i is valid
                    count += 1
        return count

    zero_conn = count_internal_edges(zero_inputs)
    one_conn = count_internal_edges(one_inputs)

    return (zero_conn, one_conn)

def analyze_all_4ones_rules():
    """
    Find all rules with 4 ones and analyze their connectivity.
    """
    four_ones_rules = [r for r in range(256) if count_ones(r) == 4]
    print(f"Total rules with 4 ones: {len(four_ones_rules)}")

    # Group by connectivity
    by_connectivity = defaultdict(list)
    for rule in four_ones_rules:
        conn = compute_connectivity(rule)
        by_connectivity[conn].append(rule)

    print("\nConnectivity distribution among 4-ones rules:")
    for conn, rules in sorted(by_connectivity.items()):
        chaotic_in_group = [r for r in rules if r in CHAOTIC_RULES]
        print(f"  {conn}: {len(rules)} rules, {len(chaotic_in_group)} chaotic ({chaotic_in_group})")

    # Check if (2,2) is necessary and sufficient
    conn_22_rules = by_connectivity[(2, 2)]
    print(f"\n(2,2) connectivity rules: {len(conn_22_rules)}")
    print(f"Chaotic among them: {len([r for r in conn_22_rules if r in CHAOTIC_RULES])}")

    return by_connectivity

def analyze_what_22_means():
    """
    Try to understand what (2,2) connectivity means for dynamics.
    """
    print("\n" + "=" * 70)
    print("WHAT DOES (2,2) CONNECTIVITY MEAN?")
    print("=" * 70)

    # The de Bruijn graph for ECA has 4 nodes (2-bit patterns) and 8 edges (3-bit neighborhoods)
    # Each edge is labeled by the rule's output for that neighborhood

    # For (2,2) connectivity:
    # - The 4 inputs producing 0 have 2 internal edges
    # - The 4 inputs producing 1 have 2 internal edges

    # This means 4 edges go from 0-outputs to 1-outputs (mixing!)

    print("\nDe Bruijn structure analysis for Rule 30:")
    rule = 30
    table = rule_to_table(rule)

    # Visualize the graph
    print("\nEdge labels (input -> output):")
    for i in range(8):
        bits = f"{i:03b}"
        print(f"  {bits} ({i}) -> {table[i]}")

    # Show the flow between 0-outputs and 1-outputs
    zero_inputs = [i for i in range(8) if table[i] == 0]
    one_inputs = [i for i in range(8) if table[i] == 1]

    print(f"\n0-inputs: {[f'{i:03b}' for i in zero_inputs]}")
    print(f"1-inputs: {[f'{i:03b}' for i in one_inputs]}")

    # Count transitions between types
    def can_follow(j, i):
        return ((j >> 0) & 3) == ((i >> 1) & 3)

    zz, zo, oz, oo = 0, 0, 0, 0
    for j in range(8):
        for i in range(8):
            if can_follow(j, i):
                if j in zero_inputs:
                    if i in zero_inputs:
                        zz += 1
                    else:
                        zo += 1
                else:
                    if i in zero_inputs:
                        oz += 1
                    else:
                        oo += 1

    print(f"\nTransitions:")
    print(f"  0->0: {zz}")
    print(f"  0->1: {zo}")
    print(f"  1->0: {oz}")
    print(f"  1->1: {oo}")

    # KEY INSIGHT: (2,2) means zz=2, oo=2, and zo+oz=4
    # This forces constant mixing between 0-regions and 1-regions!
    print(f"\nTotal mixing transitions (0->1 + 1->0): {zo + oz}")

def analyze_mixing_and_chaos():
    """
    Test if mixing (cross-transitions) correlates with chaos.
    """
    print("\n" + "=" * 70)
    print("MIXING ANALYSIS")
    print("=" * 70)

    def count_mixing(rule):
        """Count transitions between 0-output and 1-output inputs."""
        table = rule_to_table(rule)
        zero_inputs = [i for i in range(8) if table[i] == 0]
        one_inputs = [i for i in range(8) if table[i] == 1]

        def can_follow(j, i):
            return ((j >> 0) & 3) == ((i >> 1) & 3)

        mixing = 0
        for j in range(8):
            for i in range(8):
                if can_follow(j, i):
                    if (j in zero_inputs) != (i in zero_inputs):
                        mixing += 1
        return mixing

    # Analyze all 4-ones rules
    four_ones_rules = [r for r in range(256) if count_ones(r) == 4]

    mixing_data = []
    for rule in four_ones_rules:
        mixing = count_mixing(rule)
        is_chaotic = rule in CHAOTIC_RULES
        mixing_data.append((rule, mixing, is_chaotic))

    # Group by mixing count
    by_mixing = defaultdict(list)
    for rule, mixing, is_chaotic in mixing_data:
        by_mixing[mixing].append((rule, is_chaotic))

    print("\nMixing count distribution among 4-ones rules:")
    for mixing, rules in sorted(by_mixing.items()):
        chaotic_count = sum(1 for r, c in rules if c)
        print(f"  mixing={mixing}: {len(rules)} rules, {chaotic_count} chaotic")

    # Find the critical mixing value
    chaotic_mixing = [count_mixing(r) for r in CHAOTIC_RULES]
    print(f"\nChaotic rules mixing values: {set(chaotic_mixing)}")

def find_precise_characterization():
    """
    Find the exact combination of features that characterizes chaos.
    """
    print("\n" + "=" * 70)
    print("PRECISE CHARACTERIZATION SEARCH")
    print("=" * 70)

    def rule_features(rule):
        table = rule_to_table(rule)

        # Feature 1: Connectivity
        def can_follow(j, i):
            return ((j >> 0) & 3) == ((i >> 1) & 3)

        zero_inputs = [i for i in range(8) if table[i] == 0]
        one_inputs = [i for i in range(8) if table[i] == 1]

        def count_internal(inputs):
            return sum(1 for i in inputs for j in inputs if can_follow(j, i))

        # Feature 2: Which specific inputs give 0?
        zero_set = frozenset(zero_inputs)

        # Feature 3: Quiescent states
        has_00_quiescent = table[0] == 0  # 000 -> 0
        has_11_quiescent = table[7] == 1  # 111 -> 1

        # Feature 4: XOR nature (output = parity of some inputs?)
        def check_xor():
            for mask in range(8):
                matches = all(table[i] == (bin(i & mask).count('1') % 2) for i in range(8))
                if matches:
                    return mask
            return None

        xor_mask = check_xor()

        return {
            'connectivity': (count_internal(zero_inputs), count_internal(one_inputs)),
            'zero_set': zero_set,
            'quiescent': (has_00_quiescent, has_11_quiescent),
            'xor_mask': xor_mask,
        }

    # Analyze all 4-ones rules with (2,2) connectivity
    four_ones = [r for r in range(256) if count_ones(r) == 4]
    conn_22 = [r for r in four_ones if compute_connectivity(r) == (2, 2)]

    print(f"\nRules with 4 ones AND (2,2) connectivity: {len(conn_22)}")

    # Detailed analysis
    for rule in conn_22:
        features = rule_features(rule)
        is_chaotic = rule in CHAOTIC_RULES
        status = "CHAOTIC" if is_chaotic else "periodic"
        print(f"\n  Rule {rule:3d} [{status}]:")
        print(f"    Zero set: {sorted(features['zero_set'])}")
        print(f"    Quiescent (00,11): {features['quiescent']}")
        print(f"    XOR mask: {features['xor_mask']}")

def investigate_xor_structure():
    """
    Check if chaotic rules have XOR-like algebraic structure.
    """
    print("\n" + "=" * 70)
    print("XOR/ADDITIVE STRUCTURE ANALYSIS")
    print("=" * 70)

    def check_additive_structure(rule):
        """Check if the rule is additive (linear over GF(2))."""
        table = rule_to_table(rule)

        # Additive means f(a XOR b) = f(a) XOR f(b)
        # For 3-variable function, this means it's of form:
        # f(x,y,z) = ax XOR by XOR cz for some constants a,b,c

        # Check if it matches any XOR pattern
        for a in [0, 1]:
            for b in [0, 1]:
                for c in [0, 1]:
                    matches = True
                    for i in range(8):
                        x, y, z = (i >> 2) & 1, (i >> 1) & 1, i & 1
                        expected = (a * x + b * y + c * z) % 2
                        if table[i] != expected:
                            matches = False
                            break
                    if matches:
                        return (a, b, c)
        return None

    def check_affine_structure(rule):
        """Check if the rule is affine (linear + constant)."""
        table = rule_to_table(rule)

        for const in [0, 1]:
            for a in [0, 1]:
                for b in [0, 1]:
                    for c in [0, 1]:
                        matches = True
                        for i in range(8):
                            x, y, z = (i >> 2) & 1, (i >> 1) & 1, i & 1
                            expected = (const + a * x + b * y + c * z) % 2
                            if table[i] != expected:
                                matches = False
                                break
                        if matches:
                            return (const, a, b, c)
        return None

    print("\nLinear/Affine structure of chaotic rules:")
    for rule in CHAOTIC_RULES:
        linear = check_additive_structure(rule)
        affine = check_affine_structure(rule)
        print(f"  Rule {rule:3d}: linear={linear}, affine={affine}")

    # Check non-chaotic 4-ones rules
    four_ones = [r for r in range(256) if count_ones(r) == 4]
    non_chaotic_4ones = [r for r in four_ones if r not in CHAOTIC_RULES]

    print("\nLinear/Affine structure of NON-chaotic 4-ones rules (sample):")
    for rule in non_chaotic_4ones[:10]:
        linear = check_additive_structure(rule)
        affine = check_affine_structure(rule)
        print(f"  Rule {rule:3d}: linear={linear}, affine={affine}")

    # Count how many chaotic vs non-chaotic are affine
    chaotic_affine = sum(1 for r in CHAOTIC_RULES if check_affine_structure(r) is not None)
    nonchaotic_affine = sum(1 for r in non_chaotic_4ones if check_affine_structure(r) is not None)

    print(f"\nAffine structure summary:")
    print(f"  Chaotic rules that are affine: {chaotic_affine}/{len(CHAOTIC_RULES)}")
    print(f"  Non-chaotic 4-ones rules that are affine: {nonchaotic_affine}/{len(non_chaotic_4ones)}")

def main():
    by_connectivity = analyze_all_4ones_rules()
    analyze_what_22_means()
    analyze_mixing_and_chaos()
    find_precise_characterization()
    investigate_xor_structure()

if __name__ == '__main__':
    main()
