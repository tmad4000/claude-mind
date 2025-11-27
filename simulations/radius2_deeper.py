#!/usr/bin/env python3
"""
Deeper analysis of radius-2 ECA rules.

Key finding from initial analysis:
- Skip-neighbor terms DON'T separate chaos from order in radius-2
- Only 5.3% of chaotic rules lack skip terms

New questions:
1. What DO the chaotic rules without skip terms look like?
2. Is there a DIFFERENT pattern that separates chaos?
3. What about "adjacent-only" terms - does that matter?
"""

import numpy as np
from itertools import product, combinations
from collections import Counter
# import matplotlib.pyplot as plt  # Not needed for analysis

def rule_table_from_number(rule_num, width=5):
    """Convert rule number to truth table for 5-bit input."""
    table = {}
    for i in range(2**width):
        pattern = tuple((i >> (width-1-j)) & 1 for j in range(width))
        output = (rule_num >> i) & 1
        table[pattern] = output
    return table

def compute_anf_5bit(truth_table):
    """Compute Algebraic Normal Form for a 5-variable Boolean function."""
    n = 5
    f = np.array([truth_table[tuple((i >> (n-1-j)) & 1 for j in range(n))]
                  for i in range(2**n)], dtype=np.int64)

    anf = f.copy()
    for i in range(n):
        for j in range(2**n):
            if j & (1 << i):
                anf[j] ^= anf[j ^ (1 << i)]

    return anf

def decode_anf_5bit(anf):
    """Decode ANF into human-readable form."""
    terms = []
    var_names = ['x0', 'x1', 'x2', 'x3', 'x4']

    for idx, coef in enumerate(anf):
        if coef:
            if idx == 0:
                terms.append('1')
            else:
                monomial = []
                for bit in range(5):
                    if idx & (1 << bit):
                        monomial.append(var_names[bit])
                terms.append(''.join(monomial))

    return ' ⊕ '.join(terms) if terms else '0'

def analyze_anf_structure(anf):
    """
    Detailed analysis of ANF structure.
    Returns various metrics about the term structure.
    """
    results = {
        'constant': bool(anf[0]),
        'linear_terms': [],
        'quadratic_terms': [],
        'cubic_terms': [],
        'quartic_terms': [],
        'quintic_term': False,
        'adjacent_pairs': [],      # x0x1, x1x2, x2x3, x3x4
        'skip_1_pairs': [],        # x0x2, x1x3, x2x4
        'skip_2_pairs': [],        # x0x3, x1x4
        'skip_3_pair': False,      # x0x4
        'degree': 0,
        'num_terms': sum(1 for x in anf if x),
    }

    var_names = ['x0', 'x1', 'x2', 'x3', 'x4']

    # Adjacent pairs (distance 1)
    adjacent_indices = [(0,1), (1,2), (2,3), (3,4)]
    # Skip-1 pairs (distance 2)
    skip1_indices = [(0,2), (1,3), (2,4)]
    # Skip-2 pairs (distance 3)
    skip2_indices = [(0,3), (1,4)]
    # Skip-3 pair (distance 4)
    skip3_index = (0,4)

    for idx, coef in enumerate(anf):
        if not coef:
            continue

        # Count set bits to get degree
        bits = [b for b in range(5) if idx & (1 << b)]
        degree = len(bits)
        results['degree'] = max(results['degree'], degree)

        if degree == 1:
            results['linear_terms'].append(var_names[bits[0]])
        elif degree == 2:
            pair = (bits[0], bits[1])
            term_name = var_names[bits[0]] + var_names[bits[1]]
            results['quadratic_terms'].append(term_name)

            if pair in adjacent_indices:
                results['adjacent_pairs'].append(term_name)
            elif pair in skip1_indices:
                results['skip_1_pairs'].append(term_name)
            elif pair in skip2_indices:
                results['skip_2_pairs'].append(term_name)
            elif pair == skip3_index:
                results['skip_3_pair'] = True
        elif degree == 3:
            results['cubic_terms'].append(''.join(var_names[b] for b in bits))
        elif degree == 4:
            results['quartic_terms'].append(''.join(var_names[b] for b in bits))
        elif degree == 5:
            results['quintic_term'] = True

    return results

def simulate_eca_r2(rule_table, width=100, steps=200):
    """Simulate a radius-2 ECA."""
    state = np.zeros(width, dtype=int)
    state[width//2] = 1

    history = [state.copy()]

    for _ in range(steps):
        new_state = np.zeros(width, dtype=int)
        for i in range(width):
            neighborhood = tuple(
                state[(i + j) % width] for j in range(-2, 3)
            )
            new_state[i] = rule_table[neighborhood]
        state = new_state
        history.append(state.copy())

    return np.array(history)

def compute_entropy(history):
    """Compute column entropy of CA history."""
    entropies = []
    for col in range(history.shape[1]):
        column = history[:, col]
        counts = Counter(column)
        total = len(column)
        entropy = 0
        for count in counts.values():
            if count > 0:
                p = count / total
                entropy -= p * np.log2(p)
        entropies.append(entropy)
    return np.mean(entropies)

def classify_detailed(history):
    """
    More detailed classification with entropy score.
    """
    total_cells = np.sum(history[-1])
    if total_cells == 0:
        return 'dead', 0.0

    # Check for periodicity
    for period in range(1, 50):
        if history.shape[0] > 2*period:
            if np.array_equal(history[-1], history[-1-period]):
                return f'periodic-{period}', 0.0

    entropy = compute_entropy(history[-100:])
    return 'dynamic', entropy

# The 6 chaotic rules without skip-neighbor terms (from previous analysis)
NO_SKIP_CHAOTIC = [4013130892]  # We need to recompute to find all 6

def find_no_skip_chaotic(n_samples=500):
    """Find chaotic rules without any skip-neighbor terms."""
    from itertools import combinations

    np.random.seed(44)
    no_skip_chaotic = []

    for _ in range(n_samples):
        # Generate balanced rule
        ones_positions = np.random.choice(32, 16, replace=False)
        rule = sum(1 << pos for pos in ones_positions)

        table = rule_table_from_number(rule)
        anf = compute_anf_5bit(table)
        structure = analyze_anf_structure(anf)

        # Check for NO skip terms at all
        if not structure['skip_1_pairs'] and not structure['skip_2_pairs'] and not structure['skip_3_pair']:
            # Simulate to check if chaotic
            history = simulate_eca_r2(table, width=80, steps=200)
            behavior, entropy = classify_detailed(history)

            if behavior == 'dynamic' and entropy > 0.8:
                no_skip_chaotic.append({
                    'rule': rule,
                    'entropy': entropy,
                    'anf': decode_anf_5bit(anf),
                    'structure': structure
                })

    return no_skip_chaotic

def analyze_chaotic_vs_ordered_patterns(n_samples=300):
    """
    Look for ANY pattern that distinguishes chaotic from ordered rules.
    """
    np.random.seed(45)

    chaotic_structures = []
    ordered_structures = []

    for _ in range(n_samples):
        # Balanced rules
        ones_positions = np.random.choice(32, 16, replace=False)
        rule = sum(1 << pos for pos in ones_positions)

        table = rule_table_from_number(rule)
        anf = compute_anf_5bit(table)
        structure = analyze_anf_structure(anf)

        history = simulate_eca_r2(table, width=80, steps=200)
        behavior, entropy = classify_detailed(history)

        if behavior == 'dynamic' and entropy > 0.8:
            chaotic_structures.append(structure)
        elif behavior == 'dead' or 'periodic' in behavior:
            ordered_structures.append(structure)

    return chaotic_structures, ordered_structures

def main():
    print("="*70)
    print("RADIUS-2 ECA: DEEPER ANF ANALYSIS")
    print("="*70)
    print()

    print("Phase 1: Finding chaotic rules WITHOUT skip-neighbor terms...")
    no_skip = find_no_skip_chaotic(1000)
    print(f"Found {len(no_skip)} chaotic rules without skip terms")
    print()

    for r in no_skip[:5]:
        print(f"Rule {r['rule']} (entropy={r['entropy']:.3f})")
        print(f"  ANF: {r['anf'][:100]}...")
        print(f"  Adjacent pairs: {r['structure']['adjacent_pairs']}")
        print(f"  Degree: {r['structure']['degree']}")
        print()

    print("="*70)
    print("Phase 2: Comparing chaotic vs ordered ANF structures...")
    print("="*70)
    print()

    chaotic, ordered = analyze_chaotic_vs_ordered_patterns(500)

    print(f"Chaotic rules: {len(chaotic)}")
    print(f"Ordered rules: {len(ordered)}")
    print()

    # Compare various metrics
    metrics = ['degree', 'num_terms']

    for metric in metrics:
        c_vals = [s[metric] for s in chaotic]
        o_vals = [s[metric] for s in ordered]

        if c_vals and o_vals:
            print(f"{metric}:")
            print(f"  Chaotic: mean={np.mean(c_vals):.2f}, std={np.std(c_vals):.2f}")
            print(f"  Ordered: mean={np.mean(o_vals):.2f}, std={np.std(o_vals):.2f}")
            print()

    # Check adjacent vs non-adjacent term counts
    print("Adjacent pair terms (x0x1, x1x2, x2x3, x3x4):")
    c_adj = [len(s['adjacent_pairs']) for s in chaotic]
    o_adj = [len(s['adjacent_pairs']) for s in ordered]
    if c_adj and o_adj:
        print(f"  Chaotic: mean={np.mean(c_adj):.2f}")
        print(f"  Ordered: mean={np.mean(o_adj):.2f}")
    print()

    print("Skip-1 pair terms (x0x2, x1x3, x2x4):")
    c_s1 = [len(s['skip_1_pairs']) for s in chaotic]
    o_s1 = [len(s['skip_1_pairs']) for s in ordered]
    if c_s1 and o_s1:
        print(f"  Chaotic: mean={np.mean(c_s1):.2f}")
        print(f"  Ordered: mean={np.mean(o_s1):.2f}")
    print()

    print("Skip-2 pair terms (x0x3, x1x4):")
    c_s2 = [len(s['skip_2_pairs']) for s in chaotic]
    o_s2 = [len(s['skip_2_pairs']) for s in ordered]
    if c_s2 and o_s2:
        print(f"  Chaotic: mean={np.mean(c_s2):.2f}")
        print(f"  Ordered: mean={np.mean(o_s2):.2f}")
    print()

    print("Skip-3 term (x0x4):")
    c_s3 = [1 if s['skip_3_pair'] else 0 for s in chaotic]
    o_s3 = [1 if s['skip_3_pair'] else 0 for s in ordered]
    if c_s3 and o_s3:
        print(f"  Chaotic: {100*np.mean(c_s3):.1f}% have x0x4")
        print(f"  Ordered: {100*np.mean(o_s3):.1f}% have x0x4")
    print()

    # Check linear terms
    print("Linear terms (x0, x1, x2, x3, x4):")
    c_lin = [len(s['linear_terms']) for s in chaotic]
    o_lin = [len(s['linear_terms']) for s in ordered]
    if c_lin and o_lin:
        print(f"  Chaotic: mean={np.mean(c_lin):.2f}")
        print(f"  Ordered: mean={np.mean(o_lin):.2f}")
    print()

    # Check for center term x2
    print("Center linear term (x2):")
    c_x2 = [1 if 'x2' in s['linear_terms'] else 0 for s in chaotic]
    o_x2 = [1 if 'x2' in s['linear_terms'] else 0 for s in ordered]
    if c_x2 and o_x2:
        print(f"  Chaotic: {100*np.mean(c_x2):.1f}% have x2")
        print(f"  Ordered: {100*np.mean(o_x2):.1f}% have x2")
    print()

    print("="*70)
    print("Phase 3: What IS different about chaotic rules?")
    print("="*70)
    print()

    # Check quintic term
    print("Quintic term (x0x1x2x3x4):")
    c_q = [1 if s['quintic_term'] else 0 for s in chaotic]
    o_q = [1 if s['quintic_term'] else 0 for s in ordered]
    if c_q and o_q:
        print(f"  Chaotic: {100*np.mean(c_q):.1f}% have quintic")
        print(f"  Ordered: {100*np.mean(o_q):.1f}% have quintic")
    print()

    # Check total quadratic terms
    print("Total quadratic terms:")
    c_quad = [len(s['quadratic_terms']) for s in chaotic]
    o_quad = [len(s['quadratic_terms']) for s in ordered]
    if c_quad and o_quad:
        print(f"  Chaotic: mean={np.mean(c_quad):.2f}")
        print(f"  Ordered: mean={np.mean(o_quad):.2f}")
    print()

    # RATIO of adjacent to non-adjacent
    print("Ratio of adjacent to skip quadratic terms:")
    c_ratio = []
    for s in chaotic:
        skip_count = len(s['skip_1_pairs']) + len(s['skip_2_pairs']) + (1 if s['skip_3_pair'] else 0)
        adj_count = len(s['adjacent_pairs'])
        if skip_count > 0:
            c_ratio.append(adj_count / skip_count)

    o_ratio = []
    for s in ordered:
        skip_count = len(s['skip_1_pairs']) + len(s['skip_2_pairs']) + (1 if s['skip_3_pair'] else 0)
        adj_count = len(s['adjacent_pairs'])
        if skip_count > 0:
            o_ratio.append(adj_count / skip_count)

    if c_ratio and o_ratio:
        print(f"  Chaotic: mean={np.mean(c_ratio):.2f}")
        print(f"  Ordered: mean={np.mean(o_ratio):.2f}")
    print()

    return chaotic, ordered, no_skip

if __name__ == '__main__':
    chaotic, ordered, no_skip = main()
