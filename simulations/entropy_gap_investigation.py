#!/usr/bin/env python3
"""
Investigating the ~1.5 Bit Entropy Gap

From the Class IV analysis, we found:
- Rule 110: 3.73 vs 2.23 = +1.49
- Rule 124: 3.75 vs 2.24 = +1.51
- Rule 137: 3.74 vs 2.23 = +1.51
- Rule 193: 3.73 vs 2.22 = +1.50

The gap is remarkably consistent at ~1.5 bits.

Questions to investigate:
1. Is 1.5 bits special? (log₂(3) ≈ 1.585)
2. Does this gap exist in other complex systems?
3. What's the distribution of gaps for non-Class-IV rules?
4. Is the gap related to the number of equivalence classes of 4-blocks?
"""

import json
import math
import random
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class ElementaryCA:
    def __init__(self, rule_number: int, width: int = 200):
        self.rule_number = rule_number
        self.width = width
        self.rule_table = self._build_rule_table(rule_number)
        self.history = []

    def _build_rule_table(self, rule_number: int) -> dict:
        table = {}
        for i in range(8):
            pattern = tuple(int(b) for b in format(i, '03b'))
            table[pattern] = (rule_number >> i) & 1
        return table

    def step(self, state: list) -> list:
        new_state = []
        for i in range(len(state)):
            left = state[(i - 1) % len(state)]
            center = state[i]
            right = state[(i + 1) % len(state)]
            new_state.append(self.rule_table[(left, center, right)])
        return new_state

    def run(self, initial_state: list = None, steps: int = 200) -> list:
        if initial_state is None:
            initial_state = [0] * self.width
            initial_state[self.width // 2] = 1
        self.history = [initial_state]
        state = initial_state
        for _ in range(steps):
            state = self.step(state)
            self.history.append(state)
        return self.history


def compute_block_entropy(history: list, block_size: int = 4) -> float:
    """Compute entropy of blocks of given size"""
    block_counts = defaultdict(int)
    for row in history[-50:]:  # Use last 50 rows
        for i in range(len(row) - block_size + 1):
            block = tuple(row[i:i+block_size])
            block_counts[block] += 1

    total = sum(block_counts.values())
    if total == 0:
        return 0.0

    entropy = 0
    for count in block_counts.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)

    return entropy


def compute_rule_entropy(rule: int, trials: int = 3) -> float:
    """Compute average block entropy for a rule"""
    entropies = []

    for trial in range(trials):
        ca = ElementaryCA(rule, width=200)
        if trial == 0:
            initial = [0] * 200
            initial[100] = 1
        else:
            initial = [random.randint(0, 1) for _ in range(200)]

        ca.run(initial, steps=200)
        entropy = compute_block_entropy(ca.history)
        entropies.append(entropy)

    return sum(entropies) / len(entropies)


def hamming_distance(r1: int, r2: int) -> int:
    return bin(r1 ^ r2).count('1')


def analyze_entropy_gaps():
    """
    Compute entropy and entropy gap for ALL 256 rules.

    The "gap" is: rule_entropy - avg_neighbor_entropy
    """
    print("=" * 70)
    print("ENTROPY GAP ANALYSIS FOR ALL 256 RULES")
    print("=" * 70)
    print()

    # First, compute entropy for all rules
    print("Phase 1: Computing entropy for all 256 rules...")
    entropies = {}
    for rule in range(256):
        entropies[rule] = compute_rule_entropy(rule)
        if rule % 32 == 31:
            print(f"  Completed rules 0-{rule}")

    # Compute gaps
    print("\nPhase 2: Computing entropy gaps...")
    gaps = {}
    for rule in range(256):
        neighbors = [r for r in range(256) if hamming_distance(rule, r) == 1]
        neighbor_avg = sum(entropies[n] for n in neighbors) / len(neighbors)
        gaps[rule] = entropies[rule] - neighbor_avg

    # Find rules with large positive gaps (local maxima)
    print("\nTop 20 rules by entropy gap (potential complexity peaks):")
    sorted_by_gap = sorted(gaps.items(), key=lambda x: -x[1])
    for i, (rule, gap) in enumerate(sorted_by_gap[:20]):
        print(f"  {i+1}. Rule {rule}: entropy={entropies[rule]:.3f}, gap={gap:+.3f}")

    # Analyze the gap distribution
    gap_values = list(gaps.values())
    mean_gap = sum(gap_values) / len(gap_values)
    std_gap = math.sqrt(sum((g - mean_gap)**2 for g in gap_values) / len(gap_values))
    max_gap = max(gap_values)
    min_gap = min(gap_values)

    print(f"\nGap statistics:")
    print(f"  Mean: {mean_gap:.3f}")
    print(f"  Std:  {std_gap:.3f}")
    print(f"  Max:  {max_gap:+.3f}")
    print(f"  Min:  {min_gap:+.3f}")

    # Is 1.5 special?
    print(f"\nIs ~1.5 bits special?")
    print(f"  log₂(3) = {math.log2(3):.4f}")
    print(f"  Canonical Class IV gap = ~1.50")
    print(f"  Difference from log₂(3) = {abs(1.5 - math.log2(3)):.4f}")

    # Rules with gap close to 1.5
    rules_near_1_5 = [(r, g) for r, g in gaps.items() if abs(g - 1.5) < 0.2]
    print(f"\n  Rules with gap in [1.3, 1.7]: {len(rules_near_1_5)}")
    for rule, gap in sorted(rules_near_1_5, key=lambda x: -x[1]):
        print(f"    Rule {rule}: gap={gap:+.3f}, entropy={entropies[rule]:.3f}")

    # Analyze entropy distribution by Hamming weight
    print("\nEntropy by Hamming weight (number of 1s in rule number):")
    by_weight = defaultdict(list)
    for rule in range(256):
        weight = bin(rule).count('1')
        by_weight[weight].append(entropies[rule])

    for weight in sorted(by_weight.keys()):
        vals = by_weight[weight]
        avg = sum(vals) / len(vals)
        max_e = max(vals)
        print(f"  {weight} bits: avg={avg:.3f}, max={max_e:.3f}, count={len(vals)}")

    return {
        'entropies': entropies,
        'gaps': gaps,
        'rules_near_1_5_gap': [r for r, g in rules_near_1_5]
    }


def investigate_block_structure():
    """
    Why 1.5 bits specifically?

    For 4-bit blocks, maximum entropy is 4 bits (16 equally likely blocks).
    The gap of 1.5 bits means Class IV uses ~3.7 bits = ~13 effective blocks
    while neighbors use ~2.2 bits = ~5 effective blocks.

    Let's look at the actual block distributions.
    """
    print("\n" + "=" * 70)
    print("BLOCK STRUCTURE ANALYSIS")
    print("=" * 70)

    canonical_class4 = [110, 124, 137, 193]

    for rule in canonical_class4:
        print(f"\n--- Rule {rule} ---")

        ca = ElementaryCA(rule, 200)
        ca.run(steps=200)

        # Count blocks
        block_counts = defaultdict(int)
        for row in ca.history[-50:]:
            for i in range(len(row) - 3):
                block = tuple(row[i:i+4])
                block_counts[block] += 1

        total = sum(block_counts.values())

        # How many distinct blocks appear?
        nonzero_blocks = len([c for c in block_counts.values() if c > 0])
        print(f"  Distinct 4-blocks: {nonzero_blocks} / 16")

        # Effective number of blocks (2^entropy)
        entropy = compute_block_entropy(ca.history)
        effective_blocks = 2 ** entropy
        print(f"  Effective blocks (2^H): {effective_blocks:.1f}")
        print(f"  Entropy: {entropy:.3f} bits")

        # Top blocks
        sorted_blocks = sorted(block_counts.items(), key=lambda x: -x[1])
        print(f"  Top 5 blocks:")
        for block, count in sorted_blocks[:5]:
            block_str = ''.join(str(b) for b in block)
            pct = count / total * 100
            print(f"    {block_str}: {pct:.1f}%")


def theoretical_analysis():
    """
    Why might the gap be log₂(3)?

    Hypothesis: Class IV dynamics divide the 16 possible 4-blocks into
    3 effective categories (e.g., active/inactive/boundary), while simpler
    dynamics use fewer categories.
    """
    print("\n" + "=" * 70)
    print("THEORETICAL ANALYSIS: Why log₂(3)?")
    print("=" * 70)

    print("""
If Class IV rules effectively partition blocks into 3 categories:
  - "Dead" regions (runs of 0s)
  - "Alive" regions (mixed)
  - "Glider" regions (specific patterns)

Then the maximum entropy contribution from this coarse-graining is:
  H = log₂(3) ≈ 1.585 bits

The observed gap of ~1.5 bits is close to log₂(3), suggesting that
Class IV rules add roughly one "degree of freedom" (3 states vs 2)
compared to their neighbors.

This is consistent with:
  - Class I/II neighbors: 1-2 categories (dead/uniform)
  - Class III neighbors: high entropy but less structured
  - Class IV: intermediate with ~3 meaningful categories

The "edge of chaos" might literally mean: the point where the system
supports exactly 3 macroscopic states (ordered, chaotic, boundary).
""")


def main():
    print("Starting entropy gap investigation...")
    print(f"Time: {datetime.now().isoformat()}\n")

    results = analyze_entropy_gaps()
    investigate_block_structure()
    theoretical_analysis()

    # Save results
    output_dir = Path(__file__).parent.parent / 'data' / 'ca_analysis'
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / f"entropy_gap_investigation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filepath, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'entropies': results['entropies'],
            'gaps': results['gaps'],
            'rules_near_1_5_gap': results['rules_near_1_5_gap']
        }, f, indent=2)

    print(f"\n\nResults saved to: {filepath}")


if __name__ == '__main__':
    main()
