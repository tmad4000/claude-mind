#!/usr/bin/env python3
"""
Verify entropy calculation methodology.

The log₂(3) hypothesis test showed a discrepancy:
- Previous measurements: Rule 110 gap = +1.57
- My measurements: Rule 110 gap = +0.95

This script investigates why.
"""

import math
import random
from collections import Counter
import sys
sys.path.insert(0, '/Users/jacobcole/code/claude-mind/simulations')

from cellular_automata import ElementaryCA

def compute_entropy_v1(history, block_size=4, num_rows=20):
    """Version 1: Use final rows, non-overlapping blocks."""
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


def compute_entropy_v2(history, block_size=4, num_rows=20):
    """Version 2: Use final rows, OVERLAPPING blocks (more samples)."""
    if len(history) < num_rows:
        num_rows = len(history)

    final_rows = history[-num_rows:]
    combined = []
    for row in final_rows:
        combined.extend(row)

    blocks = []
    for i in range(len(combined) - block_size + 1):  # Overlapping!
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


def compute_entropy_v3(history, block_size=4):
    """Version 3: Use ALL rows (not just final), non-overlapping blocks."""
    combined = []
    for row in history:
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


def compute_entropy_v4(history, block_size=4):
    """Version 4: 2D blocks (spacetime blocks, not just 1D)."""
    if len(history) < block_size:
        return 0.0

    width = len(history[0])
    blocks = []

    # Extract 4x4 spacetime blocks
    for t in range(0, len(history) - block_size + 1, block_size):
        for x in range(0, width - block_size + 1, block_size):
            block = []
            for dt in range(block_size):
                for dx in range(block_size):
                    block.append(history[t + dt][(x + dx) % width])
            blocks.append(tuple(block))

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
    """Get all rules that differ by exactly 1 bit."""
    return [rule_number ^ (1 << bit) for bit in range(8)]


def test_all_versions(rule_list, trials=5, width=200, steps=100):
    """Test all entropy versions on given rules."""

    results = {version: {} for version in ['v1', 'v2', 'v3', 'v4']}

    for rule in rule_list:
        entropies = {'v1': [], 'v2': [], 'v3': [], 'v4': []}

        for _ in range(trials):
            initial = [random.randint(0, 1) for _ in range(width)]
            ca = ElementaryCA(rule, width)
            ca.run(initial, steps=steps)

            entropies['v1'].append(compute_entropy_v1(ca.history))
            entropies['v2'].append(compute_entropy_v2(ca.history))
            entropies['v3'].append(compute_entropy_v3(ca.history))
            entropies['v4'].append(compute_entropy_v4(ca.history))

        for v in ['v1', 'v2', 'v3', 'v4']:
            results[v][rule] = sum(entropies[v]) / len(entropies[v])

    return results


def compute_gaps(entropies):
    """Compute gaps for all rules in entropies dict."""
    gaps = {}
    for rule in entropies:
        neighbors = get_hamming_neighbors(rule)
        neighbor_entropies = [entropies.get(n, 0) for n in neighbors]
        if all(n in entropies for n in neighbors):
            neighbor_avg = sum(neighbor_entropies) / len(neighbor_entropies)
            gaps[rule] = entropies[rule] - neighbor_avg
    return gaps


def main():
    random.seed(42)

    # Rules to analyze: canonical Class IV + their neighbors
    canonical_4 = [110, 124, 137, 193]
    all_neighbors = set()
    for rule in canonical_4:
        for n in get_hamming_neighbors(rule):
            all_neighbors.add(n)

    test_rules = sorted(set(canonical_4) | all_neighbors)

    print("="*70)
    print("ENTROPY CALCULATION METHOD COMPARISON")
    print("="*70)
    print(f"\nTesting {len(test_rules)} rules (Class IV + neighbors)")
    print("Versions:")
    print("  v1: Final rows, non-overlapping blocks")
    print("  v2: Final rows, overlapping blocks")
    print("  v3: All rows, non-overlapping blocks")
    print("  v4: 2D spacetime blocks")
    print()

    results = test_all_versions(test_rules)

    # Compute gaps for each version
    gaps_by_version = {}
    for v in ['v1', 'v2', 'v3', 'v4']:
        gaps_by_version[v] = compute_gaps(results[v])

    print("\n" + "="*70)
    print("CANONICAL CLASS IV ENTROPIES")
    print("="*70)
    print(f"\n{'Rule':>6} {'v1':>8} {'v2':>8} {'v3':>8} {'v4':>8}")
    print("-"*42)

    for rule in canonical_4:
        print(f"{rule:>6} {results['v1'][rule]:>8.4f} {results['v2'][rule]:>8.4f} "
              f"{results['v3'][rule]:>8.4f} {results['v4'][rule]:>8.4f}")

    print("\n" + "="*70)
    print("CANONICAL CLASS IV GAPS")
    print("="*70)
    print(f"\n{'Rule':>6} {'v1':>8} {'v2':>8} {'v3':>8} {'v4':>8}")
    print("-"*42)

    for rule in canonical_4:
        print(f"{rule:>6} {gaps_by_version['v1'].get(rule, 0):>+8.4f} "
              f"{gaps_by_version['v2'].get(rule, 0):>+8.4f} "
              f"{gaps_by_version['v3'].get(rule, 0):>+8.4f} "
              f"{gaps_by_version['v4'].get(rule, 0):>+8.4f}")

    print("\n" + "="*70)
    print("MEAN GAPS ACROSS CANONICAL CLASS IV")
    print("="*70)

    LOG2_3 = math.log2(3)
    print(f"\nlog₂(3) = {LOG2_3:.6f} bits")
    print()

    for v in ['v1', 'v2', 'v3', 'v4']:
        gaps = [gaps_by_version[v].get(r, 0) for r in canonical_4]
        mean_gap = sum(gaps) / len(gaps)
        diff = abs(mean_gap - LOG2_3)
        print(f"  {v}: mean gap = {mean_gap:.4f}, diff from log₂(3) = {diff:.4f}")

    # Also check different block sizes
    print("\n" + "="*70)
    print("BLOCK SIZE SENSITIVITY (using v1 method)")
    print("="*70)

    for block_size in [2, 3, 4, 5, 6]:
        print(f"\nBlock size = {block_size}")

        # Recompute with different block size
        entropies_bs = {}
        for rule in test_rules:
            ents = []
            for _ in range(5):
                initial = [random.randint(0, 1) for _ in range(200)]
                ca = ElementaryCA(rule, 200)
                ca.run(initial, steps=100)
                ents.append(compute_entropy_v1(ca.history, block_size=block_size))
            entropies_bs[rule] = sum(ents) / len(ents)

        gaps_bs = compute_gaps(entropies_bs)

        for rule in canonical_4:
            print(f"  Rule {rule}: entropy={entropies_bs[rule]:.4f}, gap={gaps_bs.get(rule, 0):+.4f}")

        mean_gap = sum(gaps_bs.get(r, 0) for r in canonical_4) / len(canonical_4)
        print(f"  Mean gap: {mean_gap:.4f} (diff from log₂(3): {abs(mean_gap - LOG2_3):.4f})")


if __name__ == '__main__':
    main()
