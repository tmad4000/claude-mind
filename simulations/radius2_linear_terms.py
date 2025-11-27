#!/usr/bin/env python3
"""
Radius-2 ECA: Linear Term Analysis

Key finding: Chaotic rules have MORE linear terms (2.77 vs 2.10 for ordered).
This is the opposite intuition from radius-1!

In radius-1: The constraint was on QUADRATIC terms (no x1x3).
In radius-2: The signal is in LINEAR terms (more = more chaotic).

What does this mean? Linear terms mean the output depends DIRECTLY on that input.
More linear terms = more inputs have direct influence = more "mixing".
"""

import numpy as np
from itertools import combinations
from collections import Counter

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

def count_linear_terms(anf):
    """Count number of linear terms (x0, x1, x2, x3, x4)."""
    count = 0
    for i in range(5):
        if anf[1 << i]:
            count += 1
    return count

def get_linear_terms(anf):
    """Get which linear terms are present."""
    terms = []
    for i in range(5):
        if anf[1 << i]:
            terms.append(f'x{i}')
    return terms

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

def main():
    print("="*70)
    print("RADIUS-2 ECA: LINEAR TERM ANALYSIS")
    print("="*70)
    print()

    print("Testing hypothesis: Number of linear terms predicts chaos")
    print()

    np.random.seed(46)

    # Collect data by number of linear terms
    data_by_linear = {i: {'chaotic': 0, 'ordered': 0, 'total': 0} for i in range(6)}

    n_samples = 1000

    for _ in range(n_samples):
        # Generate balanced rule
        ones_positions = np.random.choice(32, 16, replace=False)
        rule = sum(1 << pos for pos in ones_positions)

        table = rule_table_from_number(rule)
        anf = compute_anf_5bit(table)
        num_linear = count_linear_terms(anf)

        # Classify behavior
        history = simulate_eca_r2(table, width=80, steps=200)

        # Check for death/periodicity
        is_chaotic = False
        if np.sum(history[-1]) > 0:
            periodic = False
            for period in range(1, 50):
                if history.shape[0] > 2*period:
                    if np.array_equal(history[-1], history[-1-period]):
                        periodic = True
                        break

            if not periodic:
                entropy = compute_entropy(history[-100:])
                if entropy > 0.8:
                    is_chaotic = True

        data_by_linear[num_linear]['total'] += 1
        if is_chaotic:
            data_by_linear[num_linear]['chaotic'] += 1
        else:
            data_by_linear[num_linear]['ordered'] += 1

    print("Results by number of linear terms:")
    print("-" * 50)
    print(f"{'Linear Terms':<15} {'Chaotic':<10} {'Ordered':<10} {'% Chaotic':<12}")
    print("-" * 50)

    for i in range(6):
        d = data_by_linear[i]
        if d['total'] > 0:
            pct = 100 * d['chaotic'] / d['total']
            print(f"{i:<15} {d['chaotic']:<10} {d['ordered']:<10} {pct:.1f}%")

    print("-" * 50)
    print()

    # Test specific configurations
    print("="*70)
    print("PHASE 2: Which LINEAR TERMS matter most?")
    print("="*70)
    print()

    # Track which specific linear terms correlate with chaos
    term_chaos_count = {f'x{i}': {'with': 0, 'without': 0, 'with_total': 0, 'without_total': 0}
                        for i in range(5)}

    np.random.seed(47)
    n_samples = 1500

    for _ in range(n_samples):
        ones_positions = np.random.choice(32, 16, replace=False)
        rule = sum(1 << pos for pos in ones_positions)

        table = rule_table_from_number(rule)
        anf = compute_anf_5bit(table)
        linear_terms = set(get_linear_terms(anf))

        # Classify
        history = simulate_eca_r2(table, width=80, steps=200)
        is_chaotic = False
        if np.sum(history[-1]) > 0:
            periodic = False
            for period in range(1, 50):
                if history.shape[0] > 2*period:
                    if np.array_equal(history[-1], history[-1-period]):
                        periodic = True
                        break
            if not periodic:
                entropy = compute_entropy(history[-100:])
                if entropy > 0.8:
                    is_chaotic = True

        for i in range(5):
            term = f'x{i}'
            if term in linear_terms:
                term_chaos_count[term]['with_total'] += 1
                if is_chaotic:
                    term_chaos_count[term]['with'] += 1
            else:
                term_chaos_count[term]['without_total'] += 1
                if is_chaotic:
                    term_chaos_count[term]['without'] += 1

    print("Chaos rate by presence of each linear term:")
    print("-" * 60)
    print(f"{'Term':<10} {'With Term':<15} {'Without Term':<15} {'Difference':<12}")
    print("-" * 60)

    for i in range(5):
        term = f'x{i}'
        d = term_chaos_count[term]
        with_pct = 100 * d['with'] / d['with_total'] if d['with_total'] > 0 else 0
        without_pct = 100 * d['without'] / d['without_total'] if d['without_total'] > 0 else 0
        diff = with_pct - without_pct
        print(f"{term:<10} {with_pct:.1f}%{'':<9} {without_pct:.1f}%{'':<9} {diff:+.1f}%")

    print("-" * 60)
    print()

    # Test combination effects
    print("="*70)
    print("PHASE 3: Synergistic effects of linear term combinations")
    print("="*70)
    print()

    # Check pairs of linear terms
    pair_chaos = {}
    np.random.seed(48)
    n_samples = 2000

    for _ in range(n_samples):
        ones_positions = np.random.choice(32, 16, replace=False)
        rule = sum(1 << pos for pos in ones_positions)

        table = rule_table_from_number(rule)
        anf = compute_anf_5bit(table)
        linear_terms = frozenset(get_linear_terms(anf))

        # Classify
        history = simulate_eca_r2(table, width=80, steps=200)
        is_chaotic = False
        if np.sum(history[-1]) > 0:
            periodic = False
            for period in range(1, 50):
                if history.shape[0] > 2*period:
                    if np.array_equal(history[-1], history[-1-period]):
                        periodic = True
                        break
            if not periodic:
                entropy = compute_entropy(history[-100:])
                if entropy > 0.8:
                    is_chaotic = True

        if linear_terms not in pair_chaos:
            pair_chaos[linear_terms] = {'chaotic': 0, 'total': 0}
        pair_chaos[linear_terms]['total'] += 1
        if is_chaotic:
            pair_chaos[linear_terms]['chaotic'] += 1

    # Sort by chaos rate
    chaos_rates = [(k, v['chaotic']/v['total'] if v['total'] >= 10 else -1, v['total'])
                   for k, v in pair_chaos.items()]
    chaos_rates.sort(key=lambda x: -x[1])

    print("Top 10 linear term configurations (by chaos rate, min 10 samples):")
    print("-" * 60)
    count = 0
    for config, rate, total in chaos_rates:
        if rate >= 0 and total >= 10:
            config_str = ', '.join(sorted(config)) if config else '(none)'
            print(f"{config_str:<30} {100*rate:.1f}% chaotic (n={total})")
            count += 1
            if count >= 10:
                break

    print()
    print("Bottom 10 (least chaotic):")
    print("-" * 60)
    count = 0
    for config, rate, total in reversed(chaos_rates):
        if rate >= 0 and total >= 10:
            config_str = ', '.join(sorted(config)) if config else '(none)'
            print(f"{config_str:<30} {100*rate:.1f}% chaotic (n={total})")
            count += 1
            if count >= 10:
                break

    return data_by_linear, term_chaos_count, pair_chaos

if __name__ == '__main__':
    main()
