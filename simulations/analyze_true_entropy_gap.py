#!/usr/bin/env python3
"""
Analyze the TRUE entropy gap for Class IV rules.

Key finding: The log₂(3) hypothesis is FALSIFIED.
- Gap peaks at ~1.1-1.2 bits (not 1.585)
- Gap depends on block size
- Peak occurs around block size 5-8

Questions to answer:
1. What IS the true gap value?
2. Is there a theoretical explanation for ~1.1 bits?
3. Does the gap have a meaningful interpretation?

Possible interpretations of ~1.1 bits:
- log₂(2.14) = 1.1 (fractional state count?)
- It's the gap that distinguishes "balanced" from "unbalanced"
- It's specific to the measurement method (block entropy)
"""

import math
import random
from collections import Counter
import sys
sys.path.insert(0, '/Users/jacobcole/code/claude-mind/simulations')

from cellular_automata import ElementaryCA

# Special constants to check against
LOG2_3 = math.log2(3)           # 1.5850
LOG2_E = math.log2(math.e)      # 1.4427
PHI = (1 + math.sqrt(5)) / 2    # 1.6180
LOG2_PHI = math.log2(PHI)       # 0.6942
ONE_PLUS_LOG2_PHI = 1 + LOG2_PHI # 1.6942

def compute_entropy(history, block_size, num_rows=50):
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


def comprehensive_gap_analysis():
    """Comprehensive analysis across many rules and parameters."""
    random.seed(42)

    canonical_4 = [110, 124, 137, 193]

    # Include neighbors
    all_neighbors = set()
    for rule in canonical_4:
        for n in get_hamming_neighbors(rule):
            all_neighbors.add(n)
    test_rules = sorted(set(canonical_4) | all_neighbors)

    # High-precision run
    width = 500
    steps = 300
    trials = 10
    block_size = 6  # Near the peak

    print("="*70)
    print("HIGH-PRECISION GAP MEASUREMENT")
    print("="*70)
    print(f"\nParameters: width={width}, steps={steps}, trials={trials}, block_size={block_size}")

    # Compute entropies with error bars
    entropies = {}
    entropy_stds = {}
    for rule in test_rules:
        ents = []
        for _ in range(trials):
            initial = [random.randint(0, 1) for _ in range(width)]
            ca = ElementaryCA(rule, width)
            ca.run(initial, steps=steps)
            ents.append(compute_entropy(ca.history, block_size))
        entropies[rule] = sum(ents) / len(ents)
        entropy_stds[rule] = math.sqrt(sum((e - entropies[rule])**2 for e in ents) / len(ents))

    # Compute gaps
    gaps = {}
    gap_stds = {}
    for rule in canonical_4:
        neighbors = get_hamming_neighbors(rule)
        neighbor_avg = sum(entropies[n] for n in neighbors) / len(neighbors)
        neighbor_std_pooled = math.sqrt(sum(entropy_stds[n]**2 for n in neighbors)) / len(neighbors)
        gaps[rule] = entropies[rule] - neighbor_avg
        gap_stds[rule] = math.sqrt(entropy_stds[rule]**2 + neighbor_std_pooled**2)

    print("\n" + "-"*70)
    print("CANONICAL CLASS IV GAPS")
    print("-"*70)

    for rule in canonical_4:
        print(f"Rule {rule}:")
        print(f"  Entropy: {entropies[rule]:.4f} ± {entropy_stds[rule]:.4f}")
        print(f"  Gap: {gaps[rule]:+.4f} ± {gap_stds[rule]:.4f}")

    mean_gap = sum(gaps.values()) / len(gaps)
    pooled_std = math.sqrt(sum(gap_stds[r]**2 for r in canonical_4)) / len(canonical_4)

    print(f"\nMean gap: {mean_gap:.4f} ± {pooled_std:.4f} bits")

    # Compare to theoretical values
    print("\n" + "-"*70)
    print("COMPARISON TO THEORETICAL VALUES")
    print("-"*70)

    theoretical = {
        'log₂(3)': LOG2_3,
        'log₂(e)': LOG2_E,
        'φ (golden ratio)': PHI,
        'log₂(φ)': LOG2_PHI,
        '1': 1.0,
        'sqrt(2)': math.sqrt(2),
        'ln(3)': math.log(3),
        'log₂(2.2)': math.log2(2.2),
        'log₂(2.1)': math.log2(2.1),
        'log₂(2.15)': math.log2(2.15),
    }

    print(f"\nMeasured gap: {mean_gap:.4f} bits")
    print("\nComparison:")
    for name, value in sorted(theoretical.items(), key=lambda x: abs(x[1] - mean_gap)):
        diff = abs(value - mean_gap)
        sigma = diff / pooled_std if pooled_std > 0 else float('inf')
        print(f"  {name}: {value:.4f}, diff = {diff:.4f} ({sigma:.1f}σ)")

    # What value WOULD the gap correspond to?
    implied_base = 2 ** mean_gap
    print(f"\nImplied state ratio: 2^{mean_gap:.4f} = {implied_base:.4f}")
    print(f"(If gap represents log₂(N), then N ≈ {implied_base:.3f})")

    return {
        'mean_gap': mean_gap,
        'gap_std': pooled_std,
        'individual_gaps': gaps,
        'implied_base': implied_base
    }


def analyze_gap_structure():
    """Analyze what creates the gap - is it symmetric across all neighbors?"""
    random.seed(42)

    print("\n" + "="*70)
    print("GAP STRUCTURE ANALYSIS")
    print("="*70)

    canonical_4 = [110, 124, 137, 193]
    width = 400
    steps = 200
    trials = 5
    block_size = 6

    # Compute entropies for canonical rules and ALL their neighbors
    all_rules = set(canonical_4)
    neighbor_map = {}
    for rule in canonical_4:
        neighbor_map[rule] = get_hamming_neighbors(rule)
        all_rules.update(neighbor_map[rule])

    entropies = {}
    for rule in all_rules:
        ents = []
        for _ in range(trials):
            initial = [random.randint(0, 1) for _ in range(width)]
            ca = ElementaryCA(rule, width)
            ca.run(initial, steps=steps)
            ents.append(compute_entropy(ca.history, block_size))
        entropies[rule] = sum(ents) / len(ents)

    # For each Class IV rule, show the entropy of each neighbor
    for rule in canonical_4:
        print(f"\n--- Rule {rule} (entropy = {entropies[rule]:.4f}) ---")
        neighbors = neighbor_map[rule]

        # Which bit was flipped?
        for bit in range(8):
            neighbor = rule ^ (1 << bit)
            diff = entropies[rule] - entropies[neighbor]
            pattern_labels = ['000', '001', '010', '011', '100', '101', '110', '111']
            print(f"  Flip bit {bit} ({pattern_labels[bit]}→?): "
                  f"neighbor {neighbor}, entropy {entropies[neighbor]:.4f}, diff {diff:+.4f}")


def analyze_high_gap_rules():
    """Find ALL rules with high entropy gaps, see if Class IV is special."""
    random.seed(42)

    print("\n" + "="*70)
    print("FULL RULE SPACE GAP ANALYSIS")
    print("="*70)

    width = 300
    steps = 150
    trials = 3
    block_size = 6

    # Compute all entropies
    print("\nComputing entropies for all 256 rules...")
    entropies = {}
    for rule in range(256):
        ents = []
        for _ in range(trials):
            initial = [random.randint(0, 1) for _ in range(width)]
            ca = ElementaryCA(rule, width)
            ca.run(initial, steps=steps)
            ents.append(compute_entropy(ca.history, block_size))
        entropies[rule] = sum(ents) / len(ents)
        if rule % 32 == 31:
            print(f"  Computed rules 0-{rule}...")

    # Compute all gaps
    gaps = {}
    for rule in range(256):
        neighbors = get_hamming_neighbors(rule)
        neighbor_avg = sum(entropies[n] for n in neighbors) / len(neighbors)
        gaps[rule] = entropies[rule] - neighbor_avg

    # Sort by gap
    sorted_by_gap = sorted(range(256), key=lambda r: gaps[r], reverse=True)

    canonical_4 = [110, 124, 137, 193]

    print("\n" + "-"*70)
    print("TOP 30 RULES BY ENTROPY GAP")
    print("-"*70)
    print(f"\n{'Rank':>4} {'Rule':>6} {'Entropy':>8} {'Gap':>8} {'000→':>5} {'Class IV?':>10}")
    print("-"*50)

    for rank, rule in enumerate(sorted_by_gap[:30], 1):
        void = rule & 1
        is_c4 = "YES" if rule in canonical_4 else ""
        print(f"{rank:>4} {rule:>6} {entropies[rule]:>8.4f} {gaps[rule]:>+8.4f} "
              f"{void:>5} {is_c4:>10}")

    # Where do Class IV rules rank?
    print("\n" + "-"*70)
    print("CANONICAL CLASS IV RANKS")
    print("-"*70)

    for rule in canonical_4:
        rank = sorted_by_gap.index(rule) + 1
        print(f"Rule {rule}: rank {rank} out of 256")

    # Mean gap
    mean_gap = sum(gaps[r] for r in canonical_4) / len(canonical_4)
    print(f"\nMean Class IV gap: {mean_gap:.4f}")

    # What's the average gap for top-10 rules?
    top_10_gap = sum(gaps[sorted_by_gap[i]] for i in range(10)) / 10
    print(f"Mean top-10 gap: {top_10_gap:.4f}")


if __name__ == '__main__':
    results = comprehensive_gap_analysis()
    analyze_gap_structure()
    analyze_high_gap_rules()
