#!/usr/bin/env python3
"""
Comprehensive periodicity survey of ALL 256 Elementary Cellular Automata.

This extends the periodicity discovery from session 2 to the full rule space.
The hypothesis: Periodicity correlates with Wolfram class and can potentially
be used as an objective classifier.

Author: Claude (overnight session 3)
Date: 2025-11-27
"""

import numpy as np
import json
from collections import defaultdict

# Wolfram's canonical classifications (as reference)
# These are used for comparison, not as ground truth
WOLFRAM_CLASS_IV = [110, 124, 137, 193]
WOLFRAM_CLASS_III = [22, 30, 45, 60, 73, 75, 86, 89, 90, 101, 102, 105, 106,
                     120, 129, 135, 149, 150, 153, 161, 165, 169, 181, 182, 195, 225]
WOLFRAM_CLASS_II = [4, 5, 12, 13, 28, 29, 32, 36, 44, 50, 51, 54, 56, 57, 58, 62,
                    72, 76, 77, 78, 94, 104, 108, 132, 140, 152, 156, 162, 164,
                    168, 172, 176, 184, 200, 204, 232]
WOLFRAM_CLASS_I = [0, 8, 32, 40, 64, 96, 128, 136, 160, 168, 192, 224, 234, 235, 238, 239, 248, 249, 252, 253, 254, 255]

def apply_rule(cells, rule_num):
    """Apply ECA rule to cell array."""
    rule_bits = [(rule_num >> i) & 1 for i in range(8)]
    n = len(cells)
    new_cells = np.zeros_like(cells)
    for i in range(n):
        left = cells[(i-1) % n]
        center = cells[i]
        right = cells[(i+1) % n]
        idx = (left << 2) | (center << 1) | right
        new_cells[i] = rule_bits[idx]
    return new_cells

def find_cycle(rule_num, width, max_steps=20000, seed=42):
    """
    Try to find a cycle (periodic orbit).
    Returns (found, transient_length, period) or (False, max_steps, None).
    """
    np.random.seed(seed + rule_num)
    cells = np.random.randint(0, 2, width)
    seen_states = {}

    for step in range(max_steps):
        state_key = hash(tuple(cells.tolist()))
        if state_key in seen_states:
            return True, seen_states[state_key], step - seen_states[state_key]
        seen_states[state_key] = step
        cells = apply_rule(cells, rule_num)

    return False, max_steps, None

def measure_entropy(rule_num, width=100, steps=500):
    """Measure average entropy over evolution."""
    np.random.seed(42)
    cells = np.random.randint(0, 2, width)
    entropies = []

    for _ in range(steps):
        cells = apply_rule(cells, rule_num)
        p1 = np.mean(cells)
        p0 = 1 - p1
        if p1 > 0 and p0 > 0:
            h = -p1 * np.log2(p1) - p0 * np.log2(p0)
        else:
            h = 0
        entropies.append(h)

    return np.mean(entropies[-100:])  # Average of last 100 steps

def is_trivial(rule_num, width=50, steps=100):
    """Check if rule is trivial (dies out or becomes uniform)."""
    np.random.seed(42)
    cells = np.random.randint(0, 2, width)

    for _ in range(steps):
        cells = apply_rule(cells, rule_num)

    density = np.mean(cells)
    return density < 0.02 or density > 0.98

def test_all_rules(widths=[31, 47, 61], max_steps=20000, num_seeds=3):
    """
    Test all 256 rules for periodicity across multiple widths and seeds.
    Returns detailed results dictionary.
    """
    results = {}

    for rule in range(256):
        rule_results = {
            'rule': rule,
            'periodic_tests': 0,
            'total_tests': 0,
            'transients': [],
            'periods': [],
            'is_trivial': is_trivial(rule),
            'entropy': measure_entropy(rule),
            'details': []
        }

        for width in widths:
            for seed in range(num_seeds):
                found, trans, period = find_cycle(rule, width, max_steps, seed=seed*1000)
                rule_results['total_tests'] += 1

                test_detail = {
                    'width': width,
                    'seed': seed,
                    'found_cycle': found,
                    'transient': trans,
                    'period': period
                }
                rule_results['details'].append(test_detail)

                if found:
                    rule_results['periodic_tests'] += 1
                    rule_results['transients'].append(trans)
                    rule_results['periods'].append(period)

        # Compute summary stats
        total = rule_results['total_tests']
        periodic = rule_results['periodic_tests']
        rule_results['periodicity_rate'] = periodic / total if total > 0 else 0
        rule_results['mean_period'] = np.mean(rule_results['periods']) if rule_results['periods'] else None
        rule_results['mean_transient'] = np.mean(rule_results['transients']) if rule_results['transients'] else None

        results[rule] = rule_results

        # Progress indicator
        if rule % 16 == 0:
            print(f"Tested rules 0-{rule}...")

    return results

def classify_by_periodicity(results):
    """Classify rules based on periodicity behavior."""
    classifications = {
        'always_periodic': [],      # 100% cycles found
        'usually_periodic': [],     # 60-99% cycles found
        'sometimes_periodic': [],   # 20-59% cycles found
        'rarely_periodic': [],      # 1-19% cycles found
        'never_periodic': [],       # 0% cycles found (chaotic)
        'trivial': []               # Dies out or becomes uniform
    }

    for rule, data in results.items():
        if data['is_trivial']:
            classifications['trivial'].append(rule)
        elif data['periodicity_rate'] == 1.0:
            classifications['always_periodic'].append(rule)
        elif data['periodicity_rate'] >= 0.6:
            classifications['usually_periodic'].append(rule)
        elif data['periodicity_rate'] >= 0.2:
            classifications['sometimes_periodic'].append(rule)
        elif data['periodicity_rate'] > 0:
            classifications['rarely_periodic'].append(rule)
        else:
            classifications['never_periodic'].append(rule)

    return classifications

def compare_with_wolfram(results):
    """Compare our periodicity classification with Wolfram's classes."""
    comparison = {
        'Class IV': {'periodic_rate': [], 'rules': []},
        'Class III': {'periodic_rate': [], 'rules': []},
        'Class II': {'periodic_rate': [], 'rules': []},
        'Class I': {'periodic_rate': [], 'rules': []},
        'Unclassified': {'periodic_rate': [], 'rules': []}
    }

    for rule, data in results.items():
        if rule in WOLFRAM_CLASS_IV:
            comparison['Class IV']['periodic_rate'].append(data['periodicity_rate'])
            comparison['Class IV']['rules'].append(rule)
        elif rule in WOLFRAM_CLASS_III:
            comparison['Class III']['periodic_rate'].append(data['periodicity_rate'])
            comparison['Class III']['rules'].append(rule)
        elif rule in WOLFRAM_CLASS_II:
            comparison['Class II']['periodic_rate'].append(data['periodicity_rate'])
            comparison['Class II']['rules'].append(rule)
        elif rule in WOLFRAM_CLASS_I:
            comparison['Class I']['periodic_rate'].append(data['periodicity_rate'])
            comparison['Class I']['rules'].append(rule)
        else:
            comparison['Unclassified']['periodic_rate'].append(data['periodicity_rate'])
            comparison['Unclassified']['rules'].append(rule)

    # Compute averages
    for cls in comparison:
        rates = comparison[cls]['periodic_rate']
        comparison[cls]['mean_rate'] = np.mean(rates) if rates else None
        comparison[cls]['count'] = len(rates)

    return comparison

def main():
    print("=" * 70)
    print("COMPREHENSIVE PERIODICITY SURVEY: ALL 256 ECA RULES")
    print("=" * 70)
    print()
    print("Parameters: widths=[31, 47, 61], max_steps=20000, seeds=3")
    print("Total tests per rule: 9")
    print()

    # Run the comprehensive test
    print("Testing all 256 rules...")
    print("-" * 50)
    results = test_all_rules()

    # Classify by periodicity
    print("\n" + "=" * 70)
    print("CLASSIFICATION BY PERIODICITY")
    print("=" * 70)
    classifications = classify_by_periodicity(results)

    for category, rules in classifications.items():
        print(f"\n{category.upper()} ({len(rules)} rules):")
        if len(rules) <= 20:
            print(f"  Rules: {sorted(rules)}")
        else:
            print(f"  Rules: {sorted(rules)[:10]}... and {len(rules)-10} more")

    # Compare with Wolfram's classification
    print("\n" + "=" * 70)
    print("COMPARISON WITH WOLFRAM CLASSIFICATION")
    print("=" * 70)
    comparison = compare_with_wolfram(results)

    for cls, data in comparison.items():
        if data['count'] > 0:
            print(f"\n{cls}: {data['count']} rules")
            print(f"  Mean periodicity rate: {data['mean_rate']:.2%}")

            # Show which rules are periodic vs chaotic
            periodic_rules = [r for r in data['rules'] if results[r]['periodicity_rate'] == 1.0]
            chaotic_rules = [r for r in data['rules'] if results[r]['periodicity_rate'] == 0.0]

            if periodic_rules:
                print(f"  Always periodic: {periodic_rules[:10]}{'...' if len(periodic_rules) > 10 else ''}")
            if chaotic_rules:
                print(f"  Never periodic:  {chaotic_rules[:10]}{'...' if len(chaotic_rules) > 10 else ''}")

    # Key finding: Does periodicity cleanly separate Class IV from Class III?
    print("\n" + "=" * 70)
    print("KEY FINDING: CLASS IV vs CLASS III SEPARATION")
    print("=" * 70)

    iv_rates = comparison['Class IV']['periodic_rate']
    iii_rates = comparison['Class III']['periodic_rate']

    if iv_rates and iii_rates:
        iv_mean = np.mean(iv_rates)
        iii_mean = np.mean(iii_rates)

        iv_periodic = sum(1 for r in iv_rates if r == 1.0)
        iii_periodic = sum(1 for r in iii_rates if r == 1.0)

        print(f"""
Class IV (complex, computation):
  - Mean periodicity: {iv_mean:.2%}
  - Always periodic:  {iv_periodic}/{len(iv_rates)} = {iv_periodic/len(iv_rates):.0%}

Class III (chaotic):
  - Mean periodicity: {iii_mean:.2%}
  - Always periodic:  {iii_periodic}/{len(iii_rates)} = {iii_periodic/len(iii_rates):.0%}

Separation gap: {iv_mean - iii_mean:.2%} difference in mean periodicity
""")

        if iv_mean > 0.8 and iii_mean < 0.3:
            print("*** STRONG SEPARATION: Periodicity distinguishes Class IV from Class III ***")
        elif iv_mean > iii_mean:
            print("*** MODERATE SEPARATION: Class IV more periodic than Class III ***")
        else:
            print("*** WEAK/NO SEPARATION: Hypothesis not supported ***")

    # Look for interesting outliers
    print("\n" + "=" * 70)
    print("INTERESTING OUTLIERS")
    print("=" * 70)

    # Class III rules that are periodic (potential misclassifications?)
    periodic_class_iii = [r for r in WOLFRAM_CLASS_III if results[r]['periodicity_rate'] > 0.5]
    if periodic_class_iii:
        print(f"\nClass III rules that are PERIODIC (possible misclassifications?):")
        for r in periodic_class_iii:
            print(f"  Rule {r}: {results[r]['periodicity_rate']:.0%} periodic, entropy={results[r]['entropy']:.3f}")

    # Class IV rules that are NOT periodic (concerning)
    nonperiodic_class_iv = [r for r in WOLFRAM_CLASS_IV if results[r]['periodicity_rate'] < 0.5]
    if nonperiodic_class_iv:
        print(f"\nClass IV rules that are NOT periodic (concerning):")
        for r in nonperiodic_class_iv:
            print(f"  Rule {r}: {results[r]['periodicity_rate']:.0%} periodic, entropy={results[r]['entropy']:.3f}")
    else:
        print(f"\nAll Class IV rules are periodic - finding confirmed!")

    # High entropy but periodic (interesting)
    high_entropy_periodic = [r for r in range(256)
                             if results[r]['entropy'] > 0.9
                             and results[r]['periodicity_rate'] == 1.0
                             and not results[r]['is_trivial']]
    if high_entropy_periodic:
        print(f"\nHigh-entropy but PERIODIC rules (pseudo-chaotic?):")
        for r in high_entropy_periodic[:10]:
            print(f"  Rule {r}: entropy={results[r]['entropy']:.3f}, period={results[r]['mean_period']:.0f}")

    # Save results to JSON for further analysis
    output_data = {
        'parameters': {
            'widths': [31, 47, 61],
            'max_steps': 20000,
            'num_seeds': 3
        },
        'summary': {
            'always_periodic_count': len(classifications['always_periodic']),
            'never_periodic_count': len(classifications['never_periodic']),
            'trivial_count': len(classifications['trivial']),
            'class_iv_mean_periodicity': np.mean(comparison['Class IV']['periodic_rate']) if comparison['Class IV']['periodic_rate'] else None,
            'class_iii_mean_periodicity': np.mean(comparison['Class III']['periodic_rate']) if comparison['Class III']['periodic_rate'] else None
        },
        'classifications': {k: sorted(v) for k, v in classifications.items()},
        'wolfram_comparison': {
            cls: {
                'rules': sorted(data['rules']),
                'mean_rate': float(data['mean_rate']) if data['mean_rate'] else None,
                'count': data['count']
            }
            for cls, data in comparison.items()
        }
    }

    with open('all_256_periodicity_results.json', 'w') as f:
        json.dump(output_data, f, indent=2)

    print("\n" + "=" * 70)
    print("Results saved to all_256_periodicity_results.json")
    print("=" * 70)

    return results, classifications, comparison

if __name__ == "__main__":
    results, classifications, comparison = main()
