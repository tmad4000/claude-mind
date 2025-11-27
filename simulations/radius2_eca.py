#!/usr/bin/env python3
"""
Radius-2 ECA Analysis: Testing ANF Generalization

For radius-2 ECAs:
- Neighborhood: (x_{i-2}, x_{i-1}, x_i, x_{i+1}, x_{i+2})
- 5 input bits → 2^5 = 32 possible inputs
- Rule table: 2^32 possible rules (4 billion)

Key question: Does the "no skip-neighbor terms" principle generalize?
- For radius-1: x1*x3=0 (left×right with no center)
- For radius-2: Do chaotic rules avoid x0*x2, x0*x3, x0*x4, x1*x3, x1*x4, x2*x4?

Strategy:
1. Focus on well-known radius-2 chaotic rules
2. Compute their ANF
3. Look for skip-neighbor patterns

Known interesting radius-2 rules:
- Rule 2992836048 (Wolfram's totalistic code 20)
- Various rules identified in literature
"""

import numpy as np
from itertools import product
from collections import Counter

def rule_table_from_number(rule_num, width=5):
    """Convert rule number to truth table for 5-bit input."""
    table = {}
    for i in range(2**width):
        # Input pattern as tuple (MSB to LSB)
        pattern = tuple((i >> (width-1-j)) & 1 for j in range(width))
        # Output is the ith bit of rule number
        output = (rule_num >> i) & 1
        table[pattern] = output
    return table

def compute_anf_5bit(truth_table):
    """
    Compute Algebraic Normal Form for a 5-variable Boolean function.
    Returns coefficients for all monomials.
    """
    n = 5
    # Truth table as vector (index = binary representation of inputs)
    f = np.array([truth_table[tuple((i >> (n-1-j)) & 1 for j in range(n))]
                  for i in range(2**n)], dtype=np.int64)

    # Möbius transform to get ANF
    anf = f.copy()
    for i in range(n):
        for j in range(2**n):
            if j & (1 << i):
                anf[j] ^= anf[j ^ (1 << i)]

    return anf

def decode_anf_5bit(anf):
    """
    Decode ANF into human-readable form.
    Variables: x0 (leftmost), x1, x2 (center), x3, x4 (rightmost)
    """
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

def get_skip_neighbor_terms(anf):
    """
    Identify which "skip-neighbor" terms are present.
    Skip-neighbor = variables that skip at least one position.

    For 5-bit: x0x2, x0x3, x0x4, x1x3, x1x4, x2x4
    """
    skip_terms = []
    var_names = ['x0', 'x1', 'x2', 'x3', 'x4']

    # Check each coefficient
    skip_pairs = [
        (0, 2), (0, 3), (0, 4),  # x0 paired with x2, x3, x4
        (1, 3), (1, 4),          # x1 paired with x3, x4
        (2, 4)                    # x2 paired with x4
    ]

    for i, j in skip_pairs:
        # Check if term xi*xj exists without intermediate variables
        # The monomial xi*xj has index 2^i + 2^j
        idx = (1 << i) | (1 << j)
        if anf[idx]:
            skip_terms.append(f'{var_names[i]}{var_names[j]}')

    return skip_terms

def count_ones(truth_table):
    """Count number of 1s in output (for balance check)."""
    return sum(truth_table.values())

def simulate_eca_r2(rule_table, width=100, steps=200):
    """Simulate a radius-2 ECA."""
    # Initialize with single cell
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

# Known interesting radius-2 rules (from literature and experiments)
# These are selected to be potentially chaotic or interesting
INTERESTING_RULES = [
    # Some totalistic-like rules
    0b11110000_00001111_11110000_00001111,  # 4042322175 - symmetric
    # Rule with complex behavior (experiment)
]

def generate_symmetric_rules(n_samples=100):
    """
    Generate rules that are symmetric under left-right reflection.
    These are more likely to be interesting.
    """
    rules = []
    # For a rule to be symmetric, f(x0,x1,x2,x3,x4) = f(x4,x3,x2,x1,x0)
    # This means we only need to specify outputs for half the inputs

    # Pairs of inputs that are reflections of each other
    reflection_pairs = []
    for i in range(32):
        # Reverse the 5-bit pattern
        rev = 0
        for b in range(5):
            if i & (1 << b):
                rev |= (1 << (4-b))
        if i <= rev:
            reflection_pairs.append((i, rev))

    # Generate random symmetric rules
    np.random.seed(42)
    for _ in range(n_samples):
        rule = 0
        for i, rev in reflection_pairs:
            bit = np.random.randint(0, 2)
            rule |= (bit << i)
            rule |= (bit << rev)
        rules.append(rule)

    return rules

def generate_balanced_rules(n_samples=100):
    """
    Generate balanced rules (16 ones in truth table).
    Balanced rules are more likely to be chaotic.
    """
    from itertools import combinations

    # Choose 16 positions out of 32 to be 1
    all_positions = list(range(32))

    np.random.seed(43)
    rules = []
    for _ in range(n_samples):
        ones_positions = np.random.choice(32, 16, replace=False)
        rule = sum(1 << pos for pos in ones_positions)
        rules.append(rule)

    return rules

def analyze_rule(rule_num):
    """Full analysis of a radius-2 rule."""
    table = rule_table_from_number(rule_num)
    anf = compute_anf_5bit(table)

    return {
        'rule': rule_num,
        'ones': count_ones(table),
        'anf_string': decode_anf_5bit(anf),
        'skip_terms': get_skip_neighbor_terms(anf),
        'anf': anf
    }

def classify_behavior(history):
    """
    Classify behavior based on simulation.
    Returns: 'dead', 'periodic', 'chaotic', 'complex'
    """
    # Check if dead (all zeros after some time)
    if np.sum(history[-1]) == 0:
        return 'dead'

    # Check for periodicity (compare last rows)
    for period in range(1, 50):
        if history.shape[0] > 2*period:
            if np.array_equal(history[-1], history[-1-period]):
                return f'periodic-{period}'

    # Check entropy for chaos vs complex
    entropy = compute_entropy(history[-100:])
    if entropy > 0.9:
        return 'chaotic'
    elif entropy > 0.5:
        return 'complex'
    else:
        return 'ordered'

def main():
    print("="*70)
    print("RADIUS-2 ECA: ANF GENERALIZATION TEST")
    print("="*70)
    print()

    print("Testing if 'no skip-neighbor' constraint generalizes from radius-1 to radius-2")
    print()

    # Generate candidate rules
    print("Generating candidate rules...")
    balanced_rules = generate_balanced_rules(200)
    symmetric_rules = generate_symmetric_rules(200)

    # Combine and deduplicate
    all_rules = list(set(balanced_rules + symmetric_rules))
    print(f"Total unique candidate rules: {len(all_rules)}")
    print()

    # Analyze and classify each rule
    print("Analyzing rules (simulation + ANF)...")
    print()

    results = []
    chaotic_rules = []

    for i, rule in enumerate(all_rules[:300]):  # Limit for time
        table = rule_table_from_number(rule)
        history = simulate_eca_r2(table, width=80, steps=150)
        behavior = classify_behavior(history)

        analysis = analyze_rule(rule)
        analysis['behavior'] = behavior
        results.append(analysis)

        if 'chaotic' in behavior or 'complex' in behavior:
            chaotic_rules.append(analysis)

        if (i+1) % 50 == 0:
            print(f"  Analyzed {i+1}/{min(300, len(all_rules))} rules...")

    print()
    print("="*70)
    print("RESULTS: CHAOTIC/COMPLEX RULES")
    print("="*70)
    print()

    # Sort by behavior
    chaotic_rules.sort(key=lambda x: x['behavior'], reverse=True)

    for r in chaotic_rules[:20]:
        print(f"Rule {r['rule']}: {r['behavior']}")
        print(f"  Ones: {r['ones']}/32 (balance: {'yes' if r['ones']==16 else 'no'})")
        print(f"  Skip-neighbor terms: {r['skip_terms'] if r['skip_terms'] else 'NONE'}")
        print(f"  ANF: {r['anf_string'][:80]}...")
        print()

    # Statistical analysis
    print("="*70)
    print("STATISTICAL ANALYSIS: Skip-Neighbor Terms")
    print("="*70)
    print()

    chaotic_with_skip = sum(1 for r in chaotic_rules if r['skip_terms'])
    chaotic_without_skip = sum(1 for r in chaotic_rules if not r['skip_terms'])

    non_chaotic = [r for r in results if 'chaotic' not in r['behavior'] and 'complex' not in r['behavior']]
    non_chaotic_with_skip = sum(1 for r in non_chaotic if r['skip_terms'])
    non_chaotic_without_skip = sum(1 for r in non_chaotic if not r['skip_terms'])

    print(f"Chaotic/Complex rules ({len(chaotic_rules)} total):")
    print(f"  With skip-neighbor terms: {chaotic_with_skip}")
    print(f"  Without skip-neighbor terms: {chaotic_without_skip}")
    print()
    print(f"Non-chaotic rules ({len(non_chaotic)} total):")
    print(f"  With skip-neighbor terms: {non_chaotic_with_skip}")
    print(f"  Without skip-neighbor terms: {non_chaotic_without_skip}")
    print()

    if chaotic_rules:
        pct = chaotic_without_skip / len(chaotic_rules) * 100
        print(f"Percentage of chaotic rules WITHOUT skip terms: {pct:.1f}%")
        print()
        if pct > 90:
            print("✓ HYPOTHESIS SUPPORTED: Chaotic rules tend to avoid skip-neighbor terms!")
        elif pct > 50:
            print("? PARTIAL SUPPORT: Trend visible but not as strong as radius-1")
        else:
            print("✗ HYPOTHESIS NOT SUPPORTED: Skip terms common in chaotic rules")

    return results, chaotic_rules

if __name__ == '__main__':
    results, chaotic = main()
