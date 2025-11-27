#!/usr/bin/env python3
"""
Test the log₂(3) Entropy Gap Hypothesis

HYPOTHESIS (from overnight session):
Class IV rules have an entropy gap of exactly log₂(3) = 1.5849625 bits
relative to their Hamming-1 neighbors.

THEORETICAL INTERPRETATION:
Class IV rules partition CA state space into exactly 3 macroscopic categories:
1. Dead (empty, stable regions)
2. Active (busy, chaotic regions)
3. Localized (gliders, persistent structures)

Neighbors only support 2 categories, hence the gap is one "ternary bit".

This script tests this hypothesis across ALL 256 ECA rules.
"""

import math
import random
from collections import defaultdict
import sys
sys.path.insert(0, '/Users/jacobcole/code/claude-mind/simulations')

from cellular_automata import ElementaryCA

# Constants
LOG2_3 = math.log2(3)  # 1.5849625007211563

def compute_block_entropy(history, block_size=4, num_rows=20):
    """Compute block entropy over final rows of CA history."""
    if len(history) < num_rows:
        return 0.0

    # Use final rows for steady-state behavior
    final_rows = history[-num_rows:]
    combined = []
    for row in final_rows:
        combined.extend(row)

    # Count blocks
    block_counts = {}
    for i in range(0, len(combined) - block_size + 1, block_size):
        block = tuple(combined[i:i+block_size])
        block_counts[block] = block_counts.get(block, 0) + 1

    if not block_counts:
        return 0.0

    total = sum(block_counts.values())
    entropy = 0.0
    for count in block_counts.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)

    return entropy


def compute_rule_entropy(rule_number, trials=5, width=200, steps=100):
    """Compute average block entropy for a rule across multiple trials."""
    entropies = []

    for _ in range(trials):
        # Random initial conditions
        initial = [random.randint(0, 1) for _ in range(width)]

        ca = ElementaryCA(rule_number, width)
        ca.run(initial, steps=steps)

        entropy = compute_block_entropy(ca.history)
        entropies.append(entropy)

    return sum(entropies) / len(entropies)


def get_hamming_neighbors(rule_number):
    """Get all rules that differ by exactly 1 bit."""
    neighbors = []
    for bit in range(8):
        neighbor = rule_number ^ (1 << bit)
        neighbors.append(neighbor)
    return neighbors


def get_void_transition(rule_number):
    """Get what 000 maps to (0 or 1)."""
    # Rule table: bit 0 is output for 000
    return rule_number & 1


def analyze_all_rules():
    """Compute entropy and gap for all 256 rules."""
    print("Computing entropies for all 256 rules...")
    print(f"Target gap value: log₂(3) = {LOG2_3:.6f} bits\n")

    # First pass: compute all rule entropies
    entropies = {}
    for rule in range(256):
        entropies[rule] = compute_rule_entropy(rule)
        if rule % 32 == 31:
            print(f"  Computed rules 0-{rule}...")

    print("\nComputing entropy gaps vs Hamming-1 neighbors...")

    # Second pass: compute gaps
    gaps = {}
    for rule in range(256):
        neighbors = get_hamming_neighbors(rule)
        neighbor_avg = sum(entropies[n] for n in neighbors) / len(neighbors)
        gaps[rule] = entropies[rule] - neighbor_avg

    return entropies, gaps


def find_log2_3_rules(entropies, gaps, tolerance=0.10):
    """Find rules with gap close to log₂(3)."""
    matches = []

    for rule in range(256):
        gap = gaps[rule]
        distance = abs(gap - LOG2_3)
        if distance < tolerance:
            void = get_void_transition(rule)
            matches.append({
                'rule': rule,
                'entropy': entropies[rule],
                'gap': gap,
                'distance_from_log2_3': distance,
                'void_stable': void == 0
            })

    # Sort by distance from log₂(3)
    matches.sort(key=lambda x: x['distance_from_log2_3'])
    return matches


def analyze_void_stability(entropies, gaps):
    """Analyze relationship between void stability and entropy gap."""
    void_stable = []  # Rules where 000→0
    void_unstable = []  # Rules where 000→1

    for rule in range(256):
        if get_void_transition(rule) == 0:
            void_stable.append(rule)
        else:
            void_unstable.append(rule)

    # Compare average gaps
    avg_gap_stable = sum(gaps[r] for r in void_stable) / len(void_stable)
    avg_gap_unstable = sum(gaps[r] for r in void_unstable) / len(void_unstable)

    # Compare average entropies
    avg_ent_stable = sum(entropies[r] for r in void_stable) / len(void_stable)
    avg_ent_unstable = sum(entropies[r] for r in void_unstable) / len(void_unstable)

    return {
        'void_stable_count': len(void_stable),
        'void_unstable_count': len(void_unstable),
        'avg_gap_void_stable': avg_gap_stable,
        'avg_gap_void_unstable': avg_gap_unstable,
        'avg_entropy_void_stable': avg_ent_stable,
        'avg_entropy_void_unstable': avg_ent_unstable
    }


def canonical_class_4_analysis(entropies, gaps):
    """Deep analysis of canonical Class IV rules."""
    canonical_4 = [110, 124, 137, 193]  # The symmetry-equivalent cluster

    print("\n" + "="*70)
    print("CANONICAL CLASS IV RULES ANALYSIS")
    print("="*70)

    print(f"\nTheoretical prediction: gap = log₂(3) = {LOG2_3:.6f} bits")
    print("(This represents ternary state discrimination: dead/active/localized)\n")

    gaps_list = []
    for rule in canonical_4:
        gap = gaps[rule]
        ent = entropies[rule]
        void = get_void_transition(rule)

        print(f"Rule {rule}:")
        print(f"  Entropy: {ent:.4f} bits")
        print(f"  Gap vs neighbors: {gap:.4f} bits")
        print(f"  Distance from log₂(3): {abs(gap - LOG2_3):.6f} bits")
        print(f"  Void stable (000→0): {void == 0}")
        print()

        gaps_list.append(gap)

    mean_gap = sum(gaps_list) / len(gaps_list)
    print(f"Mean gap across canonical Class IV: {mean_gap:.6f} bits")
    print(f"log₂(3) = {LOG2_3:.6f} bits")
    print(f"Difference: {abs(mean_gap - LOG2_3):.6f} bits")

    return mean_gap


def find_high_gap_classes(entropies, gaps):
    """Categorize all rules by their gap magnitude."""
    # Sort all rules by gap
    sorted_rules = sorted(range(256), key=lambda r: gaps[r], reverse=True)

    print("\n" + "="*70)
    print("TOP 20 RULES BY ENTROPY GAP")
    print("="*70)
    print(f"\n{'Rule':>6} {'Entropy':>8} {'Gap':>8} {'Dist from log₂(3)':>18} {'000→':>5}")
    print("-"*50)

    for rule in sorted_rules[:20]:
        ent = entropies[rule]
        gap = gaps[rule]
        dist = abs(gap - LOG2_3)
        void = "0" if get_void_transition(rule) == 0 else "1"
        print(f"{rule:>6} {ent:>8.4f} {gap:>+8.4f} {dist:>18.6f} {void:>5}")

    return sorted_rules


def test_gap_distribution(gaps):
    """Statistical analysis of gap distribution."""
    all_gaps = list(gaps.values())

    mean_gap = sum(all_gaps) / len(all_gaps)
    variance = sum((g - mean_gap)**2 for g in all_gaps) / len(all_gaps)
    std_gap = math.sqrt(variance)
    max_gap = max(all_gaps)
    min_gap = min(all_gaps)

    # How many rules have gap > log₂(3) - 0.1?
    near_log2_3_count = sum(1 for g in all_gaps if abs(g - LOG2_3) < 0.1)

    print("\n" + "="*70)
    print("GAP DISTRIBUTION STATISTICS")
    print("="*70)
    print(f"\nMean gap: {mean_gap:.4f} bits")
    print(f"Std dev: {std_gap:.4f} bits")
    print(f"Max gap: {max_gap:.4f} bits")
    print(f"Min gap: {min_gap:.4f} bits")
    print(f"\nRules with gap within 0.1 of log₂(3): {near_log2_3_count}")
    print(f"Expected if random: ~{256 * 0.2 / (max_gap - min_gap):.1f}")

    return {
        'mean': mean_gap,
        'std': std_gap,
        'max': max_gap,
        'min': min_gap,
        'near_log2_3_count': near_log2_3_count
    }


def main():
    print("="*70)
    print("LOG₂(3) ENTROPY GAP HYPOTHESIS TEST")
    print("="*70)
    print()

    # Set seed for reproducibility
    random.seed(42)

    # Compute all entropies and gaps
    entropies, gaps = analyze_all_rules()

    # Analyze canonical Class IV
    mean_canonical_gap = canonical_class_4_analysis(entropies, gaps)

    # Find high-gap rules
    sorted_rules = find_high_gap_classes(entropies, gaps)

    # Void stability analysis
    void_analysis = analyze_void_stability(entropies, gaps)

    print("\n" + "="*70)
    print("VOID STABILITY ANALYSIS")
    print("="*70)
    print(f"\nRules with void stable (000→0): {void_analysis['void_stable_count']}")
    print(f"Rules with void unstable (000→1): {void_analysis['void_unstable_count']}")
    print(f"\nAvg gap for void-stable rules: {void_analysis['avg_gap_void_stable']:.4f} bits")
    print(f"Avg gap for void-unstable rules: {void_analysis['avg_gap_void_unstable']:.4f} bits")
    print(f"\nAvg entropy for void-stable rules: {void_analysis['avg_entropy_void_stable']:.4f} bits")
    print(f"Avg entropy for void-unstable rules: {void_analysis['avg_entropy_void_unstable']:.4f} bits")

    # Gap distribution
    gap_stats = test_gap_distribution(gaps)

    # Find rules close to log₂(3)
    log2_3_matches = find_log2_3_rules(entropies, gaps, tolerance=0.10)

    print("\n" + "="*70)
    print(f"RULES WITH GAP WITHIN 0.10 OF log₂(3) = {LOG2_3:.6f}")
    print("="*70)
    print(f"\n{'Rule':>6} {'Entropy':>8} {'Gap':>8} {'Distance':>10} {'Void Stable':>12}")
    print("-"*50)

    for m in log2_3_matches:
        print(f"{m['rule']:>6} {m['entropy']:>8.4f} {m['gap']:>+8.4f} {m['distance_from_log2_3']:>10.6f} {'Yes' if m['void_stable'] else 'No':>12}")

    # Final summary
    print("\n" + "="*70)
    print("HYPOTHESIS VERDICT")
    print("="*70)

    canonical_4_gaps = [gaps[r] for r in [110, 124, 137, 193]]
    mean_c4 = sum(canonical_4_gaps) / 4

    print(f"\nCanonical Class IV mean gap: {mean_c4:.6f} bits")
    print(f"log₂(3) prediction:          {LOG2_3:.6f} bits")
    print(f"Difference:                  {abs(mean_c4 - LOG2_3):.6f} bits")

    if abs(mean_c4 - LOG2_3) < 0.05:
        print("\n*** HYPOTHESIS STRONGLY SUPPORTED ***")
        print("The entropy gap is within 0.05 bits of log₂(3)!")
    elif abs(mean_c4 - LOG2_3) < 0.15:
        print("\n*** HYPOTHESIS MODERATELY SUPPORTED ***")
        print("The entropy gap is close to but not exactly log₂(3).")
    else:
        print("\n*** HYPOTHESIS NOT SUPPORTED ***")
        print("The entropy gap differs significantly from log₂(3).")

    # Save detailed results
    results = {
        'log2_3': LOG2_3,
        'canonical_class_4_mean_gap': mean_c4,
        'difference': abs(mean_c4 - LOG2_3),
        'gap_stats': gap_stats,
        'void_analysis': void_analysis,
        'top_20_by_gap': sorted_rules[:20],
        'log2_3_matches': log2_3_matches,
        'all_entropies': entropies,
        'all_gaps': gaps
    }

    return results


if __name__ == '__main__':
    results = main()
