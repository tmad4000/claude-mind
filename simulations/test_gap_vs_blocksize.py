#!/usr/bin/env python3
"""
Test entropy gap vs block size scaling.

Key observation: The entropy gap INCREASES with block size.
At block size 6, mean gap = 1.41 (closer to log₂(3) = 1.58)

Question: Does the gap asymptotically approach log₂(3)?
"""

import math
import random
from collections import Counter
import sys
sys.path.insert(0, '/Users/jacobcole/code/claude-mind/simulations')

from cellular_automata import ElementaryCA

LOG2_3 = math.log2(3)

def compute_entropy(history, block_size, num_rows=40):
    """Compute block entropy."""
    if len(history) < num_rows:
        num_rows = len(history)

    final_rows = history[-num_rows:]
    combined = []
    for row in final_rows:
        combined.extend(row)

    blocks = []
    for i in range(0, len(combined) - block_size + 1, block_size):
        blocks.append(tuple(combined[i:i+block_size]))

    if not blocks:
        return 0.0

    counts = Counter(blocks)
    total = len(blocks)
    entropy = 0.0
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)

    return entropy


def get_hamming_neighbors(rule_number):
    return [rule_number ^ (1 << bit) for bit in range(8)]


def test_gap_scaling():
    """Test gap vs block size for canonical Class IV rules."""
    random.seed(42)

    canonical_4 = [110, 124, 137, 193]
    all_neighbors = set()
    for rule in canonical_4:
        for n in get_hamming_neighbors(rule):
            all_neighbors.add(n)
    test_rules = sorted(set(canonical_4) | all_neighbors)

    # Use larger width and more steps for better statistics
    width = 400
    steps = 200
    trials = 5

    print("="*70)
    print("ENTROPY GAP VS BLOCK SIZE")
    print("="*70)
    print(f"\nWidth={width}, Steps={steps}, Trials={trials}")
    print(f"log₂(3) = {LOG2_3:.6f}\n")

    block_sizes = [2, 3, 4, 5, 6, 7, 8, 9, 10]

    results = []

    for block_size in block_sizes:
        # Compute entropies
        entropies = {}
        for rule in test_rules:
            ents = []
            for _ in range(trials):
                initial = [random.randint(0, 1) for _ in range(width)]
                ca = ElementaryCA(rule, width)
                ca.run(initial, steps=steps)
                ents.append(compute_entropy(ca.history, block_size))
            entropies[rule] = sum(ents) / len(ents)

        # Compute gaps
        gaps = {}
        for rule in canonical_4:
            neighbors = get_hamming_neighbors(rule)
            neighbor_avg = sum(entropies[n] for n in neighbors) / len(neighbors)
            gaps[rule] = entropies[rule] - neighbor_avg

        mean_gap = sum(gaps.values()) / len(gaps)
        diff = abs(mean_gap - LOG2_3)

        results.append({
            'block_size': block_size,
            'mean_gap': mean_gap,
            'diff_from_log2_3': diff,
            'individual_gaps': gaps.copy()
        })

        print(f"Block size {block_size:2d}: mean gap = {mean_gap:+.4f}, "
              f"diff = {diff:.4f}, "
              f"ratio to log₂(3) = {mean_gap/LOG2_3:.3f}")

    # Analyze the scaling
    print("\n" + "="*70)
    print("SCALING ANALYSIS")
    print("="*70)

    # Does gap scale linearly with block size?
    print("\nGap / block_size:")
    for r in results:
        ratio = r['mean_gap'] / r['block_size']
        print(f"  BS={r['block_size']}: {ratio:.4f}")

    # Does gap = (block_size - 1) * constant?
    print("\nGap / (block_size - 1):")
    for r in results:
        if r['block_size'] > 1:
            ratio = r['mean_gap'] / (r['block_size'] - 1)
            print(f"  BS={r['block_size']}: {ratio:.4f}")

    # Gap = a * log(block_size) + b?
    import math
    print("\nGap / log(block_size):")
    for r in results:
        ratio = r['mean_gap'] / math.log2(r['block_size'])
        print(f"  BS={r['block_size']}: {ratio:.4f}")

    # Check if there's an asymptotic limit
    print("\n" + "="*70)
    print("EXTRAPOLATION")
    print("="*70)

    # Linear fit to last few points
    last_4 = results[-4:]
    x = [r['block_size'] for r in last_4]
    y = [r['mean_gap'] for r in last_4]

    # Simple linear regression
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi*yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi*xi for xi in x)

    slope = (n*sum_xy - sum_x*sum_y) / (n*sum_x2 - sum_x*sum_x)
    intercept = (sum_y - slope*sum_x) / n

    print(f"\nLinear fit (last 4 points): gap = {slope:.4f} * block_size + {intercept:.4f}")
    print(f"Extrapolated block_size for gap = log₂(3):")
    predicted_bs = (LOG2_3 - intercept) / slope
    print(f"  block_size = {predicted_bs:.1f}")

    # What's the gap rate?
    print(f"\nGap increase per block: {slope:.4f} bits/block")
    print(f"This suggests the gap grows ~{slope:.2f} bits for each additional block")

    return results


def test_at_log2_3_matching_block_size():
    """Test at the block size predicted to give log₂(3) gap."""
    random.seed(42)

    # From the extrapolation, let's try block_size around where we expect log₂(3)
    # Based on the trend, around block_size 8-9 seems likely

    canonical_4 = [110, 124, 137, 193]
    all_neighbors = set()
    for rule in canonical_4:
        for n in get_hamming_neighbors(rule):
            all_neighbors.add(n)
    test_rules = sorted(set(canonical_4) | all_neighbors)

    width = 500
    steps = 250
    trials = 10

    print("\n" + "="*70)
    print("PRECISION TEST AT LARGER BLOCK SIZES")
    print("="*70)
    print(f"\nWidth={width}, Steps={steps}, Trials={trials}")

    for block_size in [8, 9, 10, 12]:
        entropies = {}
        for rule in test_rules:
            ents = []
            for _ in range(trials):
                initial = [random.randint(0, 1) for _ in range(width)]
                ca = ElementaryCA(rule, width)
                ca.run(initial, steps=steps)
                ents.append(compute_entropy(ca.history, block_size))
            entropies[rule] = sum(ents) / len(ents)

        gaps = {}
        for rule in canonical_4:
            neighbors = get_hamming_neighbors(rule)
            neighbor_avg = sum(entropies[n] for n in neighbors) / len(neighbors)
            gaps[rule] = entropies[rule] - neighbor_avg

        mean_gap = sum(gaps.values()) / len(gaps)
        diff = abs(mean_gap - LOG2_3)

        print(f"\nBlock size {block_size}:")
        for rule in canonical_4:
            print(f"  Rule {rule}: entropy={entropies[rule]:.4f}, gap={gaps[rule]:+.4f}")
        print(f"  Mean gap: {mean_gap:.4f}")
        print(f"  log₂(3) = {LOG2_3:.4f}")
        print(f"  Difference: {diff:.4f} bits")
        print(f"  Ratio: {mean_gap/LOG2_3:.4f}")


if __name__ == '__main__':
    results = test_gap_scaling()
    test_at_log2_3_matching_block_size()
