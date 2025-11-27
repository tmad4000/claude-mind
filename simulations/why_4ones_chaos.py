#!/usr/bin/env python3
"""
Investigating WHY the 4-ones constraint leads to chaos in ECA rules.

The complete characterization found:
- ALL 12 chaotic rules have EXACTLY 4 ones in binary representation
- This means the rule table outputs exactly 4 ones and 4 zeros for 8 inputs
- The rule is "output balanced"

Questions to explore:
1. What does output balance mean for information flow?
2. How does this interact with the structure of the input space?
3. What specific property of 4-ones prevents periodicity?
"""

import numpy as np
from collections import defaultdict
import json

# The 12 chaotic rules (discovered in session 3-4)
CHAOTIC_RULES = [30, 45, 75, 86, 89, 101, 102, 105, 106, 150, 153, 154]

# For comparison: some periodic rules with various numbers of ones
PERIODIC_RULES = [110, 54, 62, 73, 18, 146, 90, 165]  # Class IV and some Class III-ish

def rule_to_table(rule):
    """Convert rule number to lookup table."""
    return [(rule >> i) & 1 for i in range(8)]

def count_ones(rule):
    """Count ones in rule's binary representation."""
    return bin(rule).count('1')

def analyze_input_output_structure(rule):
    """
    Analyze the structure of input->output mapping.

    Key insight: The 8 inputs form a specific graph structure where
    adjacent inputs (differing by one bit) can transition to each other.
    """
    table = rule_to_table(rule)

    # The 8 possible neighborhoods as (left, center, right) tuples
    neighborhoods = [(i>>2, (i>>1)&1, i&1) for i in range(8)]

    # For each output value, which inputs produce it?
    output_to_inputs = defaultdict(list)
    for i, out in enumerate(table):
        output_to_inputs[out].append(i)

    # Analyze the spatial structure of inputs that give 0 vs 1
    # Adjacent inputs in the de Bruijn graph structure
    debruijn_adjacency = {}
    for i in range(8):
        # Left shift: next input has center,right,? pattern
        center, right = (i>>1)&1, i&1
        neighbors = [center*4 + right*2 + b for b in [0, 1]]
        debruijn_adjacency[i] = neighbors

    # Check if 0-outputs and 1-outputs form connected vs fragmented sets
    def count_adjacent_pairs(inputs):
        pairs = 0
        for i in inputs:
            for j in debruijn_adjacency[i]:
                if j in inputs:
                    pairs += 1
        return pairs // 2  # Each pair counted twice

    zero_inputs = output_to_inputs[0]
    one_inputs = output_to_inputs[1]

    zero_connectivity = count_adjacent_pairs(zero_inputs)
    one_connectivity = count_adjacent_pairs(one_inputs)

    return {
        'zero_inputs': zero_inputs,
        'one_inputs': one_inputs,
        'zero_connectivity': zero_connectivity,
        'one_connectivity': one_connectivity,
        'total_connectivity': zero_connectivity + one_connectivity,
        'balance': len(one_inputs) - len(zero_inputs)
    }

def compute_boolean_properties(rule):
    """
    Compute boolean function properties that might explain chaos.

    Possible relevant properties:
    - Nonlinearity (distance to nearest linear function)
    - Algebraic degree
    - Propagation characteristics
    """
    table = rule_to_table(rule)

    # Compute Walsh-Hadamard transform for nonlinearity
    # This measures distance from linear functions
    def walsh_hadamard():
        wh = []
        for w in range(8):  # All linear combinations of inputs
            sum_val = 0
            for x in range(8):
                # f(x) XOR <w,x>
                linear = bin(w & x).count('1') % 2
                sum_val += (-1) ** (table[x] ^ linear)
            wh.append(sum_val)
        return wh

    wh = walsh_hadamard()
    max_correlation = max(abs(v) for v in wh)
    nonlinearity = (8 - max_correlation) // 2

    # Algebraic Normal Form (ANF) representation
    # f(x,y,z) = a0 + a1*x + a2*y + a3*z + a4*xy + a5*xz + a6*yz + a7*xyz
    def compute_anf():
        # Möbius transform to get ANF coefficients
        anf = table.copy()
        for i in range(3):  # 3 variables
            step = 1 << i
            for j in range(8):
                if j & step:
                    anf[j] ^= anf[j ^ step]
        return anf

    anf = compute_anf()

    # Algebraic degree = highest weight term with non-zero coefficient
    weights = [bin(i).count('1') for i in range(8)]
    degree = 0
    for i in range(8):
        if anf[i]:
            degree = max(degree, weights[i])

    # Count of each degree term
    degree_counts = defaultdict(int)
    for i in range(8):
        if anf[i]:
            degree_counts[weights[i]] += 1

    return {
        'nonlinearity': nonlinearity,
        'algebraic_degree': degree,
        'degree_counts': dict(degree_counts),
        'anf': anf,
        'has_xyz_term': bool(anf[7]),  # Does it have the x*y*z term?
        'linear_terms': sum(anf[i] for i in [1,2,4]),  # Count of x, y, z terms
        'quadratic_terms': sum(anf[i] for i in [3,5,6])  # Count of xy, xz, yz terms
    }

def analyze_de_bruijn_dynamics(rule):
    """
    Analyze the rule through its de Bruijn graph dynamics.

    The de Bruijn graph has 4 nodes (for 2-bit patterns) and represents
    how information flows through the CA. Each rule induces edge labels
    on this graph.
    """
    table = rule_to_table(rule)

    # 4 nodes: 00, 01, 10, 11
    # Edges: each node can go to two others (shift left, add 0 or 1)
    # Label each edge with the output of the rule

    edge_labels = {}
    for left_pattern in range(4):
        for right_bit in range(2):
            # From pattern (a,b), adding right_bit r, we get neighborhood (a,b,r)
            neighborhood = left_pattern * 2 + right_bit
            output = table[neighborhood]
            new_pattern = (left_pattern & 1) * 2 + right_bit
            edge_labels[(left_pattern, new_pattern, right_bit)] = output

    # Count balanced vs unbalanced node outputs
    node_balance = {}
    for node in range(4):
        out0 = table[node * 2 + 0]  # Output when right bit is 0
        out1 = table[node * 2 + 1]  # Output when right bit is 1
        node_balance[node] = abs(out0 - out1)  # 0 = balanced, 1 = unbalanced

    total_balance = sum(node_balance.values())

    return {
        'edge_labels': edge_labels,
        'node_balance': node_balance,
        'total_node_balance': total_balance,  # 0 means all nodes output both 0 and 1
    }

def main():
    print("=" * 70)
    print("WHY DOES 4-ONES CREATE CHAOS?")
    print("=" * 70)

    # Analyze chaotic rules
    print("\n" + "=" * 70)
    print("ANALYSIS OF CHAOTIC RULES (all have 4 ones)")
    print("=" * 70)

    chaotic_analysis = []
    for rule in CHAOTIC_RULES:
        io_struct = analyze_input_output_structure(rule)
        bool_props = compute_boolean_properties(rule)
        db_dyn = analyze_de_bruijn_dynamics(rule)

        analysis = {
            'rule': rule,
            'ones': count_ones(rule),
            **io_struct,
            **bool_props,
            **db_dyn
        }
        chaotic_analysis.append(analysis)

    # Analyze periodic rules for comparison
    print("\n" + "=" * 70)
    print("ANALYSIS OF PERIODIC RULES (comparison)")
    print("=" * 70)

    periodic_analysis = []
    for rule in PERIODIC_RULES:
        io_struct = analyze_input_output_structure(rule)
        bool_props = compute_boolean_properties(rule)
        db_dyn = analyze_de_bruijn_dynamics(rule)

        analysis = {
            'rule': rule,
            'ones': count_ones(rule),
            **io_struct,
            **bool_props,
            **db_dyn
        }
        periodic_analysis.append(analysis)

    # Print comparative analysis
    print("\n" + "=" * 70)
    print("COMPARATIVE ANALYSIS")
    print("=" * 70)

    # Compare nonlinearity
    chaotic_nonlin = [a['nonlinearity'] for a in chaotic_analysis]
    periodic_nonlin = [a['nonlinearity'] for a in periodic_analysis]
    print(f"\nNonlinearity:")
    print(f"  Chaotic rules:  {set(chaotic_nonlin)}")
    print(f"  Periodic rules: {set(periodic_nonlin)}")

    # Compare algebraic degree
    chaotic_deg = [a['algebraic_degree'] for a in chaotic_analysis]
    periodic_deg = [a['algebraic_degree'] for a in periodic_analysis]
    print(f"\nAlgebraic Degree:")
    print(f"  Chaotic rules:  {set(chaotic_deg)}")
    print(f"  Periodic rules: {set(periodic_deg)}")

    # Compare xyz term presence
    chaotic_xyz = [a['has_xyz_term'] for a in chaotic_analysis]
    periodic_xyz = [a['has_xyz_term'] for a in periodic_analysis]
    print(f"\nHas x*y*z term:")
    print(f"  Chaotic rules:  {sum(chaotic_xyz)}/{len(chaotic_xyz)} have xyz term")
    print(f"  Periodic rules: {sum(periodic_xyz)}/{len(periodic_xyz)} have xyz term")

    # Compare de Bruijn node balance
    chaotic_db = [a['total_node_balance'] for a in chaotic_analysis]
    periodic_db = [a['total_node_balance'] for a in periodic_analysis]
    print(f"\nDe Bruijn Node Balance (0=all nodes output both values):")
    print(f"  Chaotic rules:  {chaotic_db}")
    print(f"  Periodic rules: {periodic_db}")

    # Compare connectivity of zero/one inputs
    print(f"\nConnectivity of zero-inputs in de Bruijn graph:")
    for a in chaotic_analysis:
        print(f"  Rule {a['rule']:3d}: zero_conn={a['zero_connectivity']}, one_conn={a['one_connectivity']}")
    print("  ---")
    for a in periodic_analysis:
        print(f"  Rule {a['rule']:3d}: zero_conn={a['zero_connectivity']}, one_conn={a['one_connectivity']}")

    # Deep dive on specific properties
    print("\n" + "=" * 70)
    print("DETAILED ANF ANALYSIS")
    print("=" * 70)

    # The ANF tells us the algebraic structure
    # Variables: x=left, y=center, z=right
    terms = ['1', 'z', 'y', 'yz', 'x', 'xz', 'xy', 'xyz']

    print("\nChaotic Rules ANF:")
    for a in chaotic_analysis:
        anf_terms = [terms[i] for i in range(8) if a['anf'][i]]
        print(f"  Rule {a['rule']:3d}: {' + '.join(anf_terms)}")

    print("\nPeriodic Rules ANF:")
    for a in periodic_analysis:
        anf_terms = [terms[i] for i in range(8) if a['anf'][i]]
        print(f"  Rule {a['rule']:3d}: {' + '.join(anf_terms)}")

    # KEY INSIGHT SEARCH
    print("\n" + "=" * 70)
    print("SEARCHING FOR THE KEY INSIGHT")
    print("=" * 70)

    # Hypothesis: Chaos requires a specific balance in the ANF
    print("\nTerm counts (linear, quadratic, cubic):")
    for a in chaotic_analysis:
        print(f"  Rule {a['rule']:3d}: linear={a['linear_terms']}, quad={a['quadratic_terms']}, cubic={1 if a['has_xyz_term'] else 0}")
    print("  ---")
    for a in periodic_analysis:
        print(f"  Rule {a['rule']:3d}: linear={a['linear_terms']}, quad={a['quadratic_terms']}, cubic={1 if a['has_xyz_term'] else 0}")

    # Summary statistics
    print("\n" + "=" * 70)
    print("SUMMARY OF DISTINGUISHING FEATURES")
    print("=" * 70)

    # Find features that perfectly separate chaotic from periodic
    features_to_check = [
        ('ones', lambda a: a['ones']),
        ('nonlinearity', lambda a: a['nonlinearity']),
        ('algebraic_degree', lambda a: a['algebraic_degree']),
        ('has_xyz_term', lambda a: a['has_xyz_term']),
        ('linear_terms', lambda a: a['linear_terms']),
        ('quadratic_terms', lambda a: a['quadratic_terms']),
        ('total_node_balance', lambda a: a['total_node_balance']),
    ]

    for name, getter in features_to_check:
        chaotic_vals = set(getter(a) for a in chaotic_analysis)
        periodic_vals = set(getter(a) for a in periodic_analysis)
        overlap = chaotic_vals & periodic_vals
        if not overlap:
            print(f"  {name}: SEPARATING! chaotic={chaotic_vals}, periodic={periodic_vals}")
        else:
            print(f"  {name}: overlap={overlap}")

    return chaotic_analysis, periodic_analysis

if __name__ == '__main__':
    chaotic, periodic = main()
