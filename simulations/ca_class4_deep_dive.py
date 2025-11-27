#!/usr/bin/env python3
"""
Deep Dive: Class IV Rule Topology

The previous analysis found 54 "Class IV" rules with liberal heuristics.
This script focuses on the CANONICAL Class IV rules identified by Wolfram
and others, then checks their topological isolation.

Canonical Class IV rules (from literature):
- Rule 110 (Turing complete!)
- Rule 54
- Rule 124
- Rule 137
- Rule 193

Plus their left-right and complement equivalents.
"""

import json
import math
import random
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class ElementaryCA:
    """1D Elementary Cellular Automata"""

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


def hamming_distance(r1: int, r2: int) -> int:
    return bin(r1 ^ r2).count('1')


def get_equivalent_rules(rule: int) -> dict:
    """
    Get equivalent rules under symmetry transformations:
    - Left-right reflection
    - Color complement (0<->1)
    """
    # Original
    original = rule

    # Left-right reflection
    # Swaps the meaning of left and right neighbors
    reflected = 0
    for i in range(8):
        # i encodes (left, center, right) as 3 bits
        left = (i >> 2) & 1
        center = (i >> 1) & 1
        right = i & 1
        # Reflected: (right, center, left)
        reflected_i = (right << 2) | (center << 1) | left
        if (rule >> i) & 1:
            reflected |= (1 << reflected_i)

    # Color complement
    # Swap 0s and 1s in both input and output
    complemented = 0
    for i in range(8):
        comp_i = 7 - i  # Complement the input pattern
        # Also complement the output
        if not ((rule >> i) & 1):
            complemented |= (1 << comp_i)

    # Both transformations
    both = 0
    for i in range(8):
        left = (i >> 2) & 1
        center = (i >> 1) & 1
        right = i & 1
        reflected_i = (right << 2) | (center << 1) | left
        comp_reflected_i = 7 - reflected_i
        if not ((rule >> i) & 1):
            both |= (1 << comp_reflected_i)

    return {
        'original': original,
        'reflected': reflected,
        'complemented': complemented,
        'both': both
    }


def compute_complexity_metrics(rule: int, trials: int = 5) -> dict:
    """More sophisticated complexity analysis"""
    metrics_list = []

    for trial in range(trials):
        width = 200
        if trial == 0:
            # Single cell
            initial = [0] * width
            initial[width // 2] = 1
        else:
            # Random with different densities
            density = 0.3 + (trial - 1) * 0.1
            initial = [1 if random.random() < density else 0 for _ in range(width)]

        ca = ElementaryCA(rule, width)
        ca.run(initial, steps=200)

        # Skip first 50 steps (transient)
        history = ca.history[50:]

        # Compute metrics on settled behavior
        m = {}

        # Density statistics
        densities = [sum(row) / len(row) for row in history]
        m['mean_density'] = sum(densities) / len(densities)
        m['density_variance'] = sum((d - m['mean_density'])**2 for d in densities) / len(densities)

        # Activity: cells that change between steps
        activities = []
        for i in range(1, len(history)):
            changes = sum(a ^ b for a, b in zip(history[i], history[i-1]))
            activities.append(changes / len(history[i]))
        m['mean_activity'] = sum(activities) / len(activities) if activities else 0
        m['activity_variance'] = sum((a - m['mean_activity'])**2 for a in activities) / len(activities) if activities else 0

        # Block entropy (4-cell blocks)
        block_counts = defaultdict(int)
        for row in history:
            for i in range(len(row) - 3):
                block = tuple(row[i:i+4])
                block_counts[block] += 1
        total = sum(block_counts.values())
        entropy = 0
        for count in block_counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        m['block_entropy'] = entropy
        m['unique_blocks'] = len(block_counts)

        # "Structure" - look for localized patterns
        # Count isolated structures (groups of 1s separated by 0s)
        final = history[-1]
        structures = 0
        in_structure = False
        for cell in final:
            if cell == 1 and not in_structure:
                structures += 1
                in_structure = True
            elif cell == 0:
                in_structure = False
        m['structure_count'] = structures

        metrics_list.append(m)

    # Average across trials
    result = {'rule': rule}
    for key in metrics_list[0].keys():
        values = [m[key] for m in metrics_list]
        result[f'avg_{key}'] = sum(values) / len(values)
        result[f'std_{key}'] = math.sqrt(sum((v - result[f'avg_{key}'])**2 for v in values) / len(values))

    return result


def analyze_canonical_class4():
    """
    Analyze the CANONICAL Class IV rules and their neighborhoods.

    Canonical Class IV rules (Wolfram, Chua):
    - 110, 124, 137, 193 (core set)
    - Plus equivalents under symmetry

    Question: Are these topologically isolated?
    """
    print("=" * 70)
    print("CANONICAL CLASS IV RULES - TOPOLOGY ANALYSIS")
    print("=" * 70)
    print()

    # The core canonical Class IV rules
    canonical_class4 = [110, 124, 137, 193]

    # Add their equivalents
    all_class4 = set()
    for rule in canonical_class4:
        equiv = get_equivalent_rules(rule)
        for name, r in equiv.items():
            all_class4.add(r)
            print(f"Rule {rule} {name}: {r}")

    all_class4 = sorted(all_class4)
    print(f"\nAll canonical Class IV rules (including equivalents): {all_class4}")
    print(f"Total: {len(all_class4)} rules")

    # Analyze topology
    print("\n" + "-" * 70)
    print("TOPOLOGY ANALYSIS: Hamming-1 neighbors of canonical Class IV rules")
    print("-" * 70)

    for rule in all_class4:
        neighbors = [r for r in range(256) if hamming_distance(rule, r) == 1]
        class4_neighbors = [n for n in neighbors if n in all_class4]

        print(f"\nRule {rule} (binary: {format(rule, '08b')}):")
        print(f"  Hamming-1 neighbors: {neighbors}")
        print(f"  Class IV neighbors:  {class4_neighbors if class4_neighbors else 'NONE (ISOLATED!)'}")

    # Check isolation
    isolated = []
    for rule in all_class4:
        neighbors = [r for r in range(256) if hamming_distance(rule, r) == 1]
        if not any(n in all_class4 for n in neighbors):
            isolated.append(rule)

    print("\n" + "=" * 70)
    print("KEY FINDING")
    print("=" * 70)
    if len(isolated) == len(all_class4):
        print(f"\n*** ALL {len(all_class4)} canonical Class IV rules are TOPOLOGICALLY ISOLATED! ***")
        print("None has a Hamming-1 neighbor that is also Class IV.")
    else:
        print(f"\n{len(isolated)} of {len(all_class4)} canonical Class IV rules are isolated:")
        print(f"  Isolated: {isolated}")
        clustered = [r for r in all_class4 if r not in isolated]
        print(f"  Clustered: {clustered}")

    return {
        'canonical_class4': canonical_class4,
        'all_class4_with_equivalents': all_class4,
        'isolated_rules': isolated,
        'all_isolated': len(isolated) == len(all_class4)
    }


def compare_complexity_class4_vs_neighbors():
    """
    Compare complexity metrics between Class IV rules and their neighbors.

    Hypothesis: Class IV rules sit at a complexity peak - neighbors are either
    more ordered (Class I/II) or more chaotic (Class III).
    """
    print("\n" + "=" * 70)
    print("COMPLEXITY COMPARISON: Class IV vs neighbors")
    print("=" * 70)

    canonical = [110, 124, 137, 193]

    for rule in canonical:
        print(f"\n--- Rule {rule} ---")

        # Compute metrics for rule
        rule_metrics = compute_complexity_metrics(rule)
        print(f"Rule {rule}: entropy={rule_metrics['avg_block_entropy']:.2f}, "
              f"activity={rule_metrics['avg_mean_activity']:.3f}, "
              f"structures={rule_metrics['avg_structure_count']:.1f}")

        # Compute for all Hamming-1 neighbors
        neighbors = [r for r in range(256) if hamming_distance(rule, r) == 1]
        neighbor_metrics = []
        for n in neighbors:
            nm = compute_complexity_metrics(n, trials=3)
            neighbor_metrics.append(nm)
            print(f"  Neighbor {n}: entropy={nm['avg_block_entropy']:.2f}, "
                  f"activity={nm['avg_mean_activity']:.3f}, "
                  f"structures={nm['avg_structure_count']:.1f}")

        # Summary
        avg_neighbor_entropy = sum(nm['avg_block_entropy'] for nm in neighbor_metrics) / len(neighbor_metrics)
        avg_neighbor_activity = sum(nm['avg_mean_activity'] for nm in neighbor_metrics) / len(neighbor_metrics)

        print(f"\n  Rule {rule} entropy:     {rule_metrics['avg_block_entropy']:.2f}")
        print(f"  Avg neighbor entropy: {avg_neighbor_entropy:.2f}")
        print(f"  Difference: {rule_metrics['avg_block_entropy'] - avg_neighbor_entropy:+.2f}")


def main():
    print("Starting Class IV deep analysis...")
    print(f"Time: {datetime.now().isoformat()}\n")

    # Main analysis
    results = analyze_canonical_class4()

    # Complexity comparison (takes longer)
    print("\nRunning complexity comparison (this takes a few minutes)...")
    compare_complexity_class4_vs_neighbors()

    # Save results
    output_dir = Path(__file__).parent.parent / 'data' / 'ca_analysis'
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / f"class4_deep_dive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2, default=list)

    print(f"\n\nResults saved to: {filepath}")

    return results


if __name__ == '__main__':
    main()
