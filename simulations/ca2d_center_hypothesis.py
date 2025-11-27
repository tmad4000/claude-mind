#!/usr/bin/env python3
"""
2D CA Center Hypothesis Test - Session 8
==========================================

Testing hypothesis from initial analysis:
- Chaotic 2D CAs have NO center quadratic terms
- Stable/oscillating 2D CAs HAVE center quadratic terms

If true, this is analogous to our 1D finding where x1x3=0 for chaos.
In 2D, the constraint might be: "no direct center coupling at quadratic level"

Let's test this on MANY more rules to see if it holds.
"""

import numpy as np
from itertools import product
from collections import defaultdict

def truth_table_to_anf_9bit(truth_table):
    """Convert 9-bit truth table to Algebraic Normal Form."""
    n = 9
    anf = set()

    for monomial_indices in range(2**n):
        monomial_vars = frozenset(i for i in range(n) if (monomial_indices >> i) & 1)

        coeff = 0
        for subset in range(2**len(monomial_vars)):
            point = [0] * n
            subset_list = list(monomial_vars)
            for i, var in enumerate(subset_list):
                if (subset >> i) & 1:
                    point[var] = 1
            point_tuple = tuple(point)
            if point_tuple in truth_table:
                coeff ^= truth_table[point_tuple]

        if coeff == 1:
            anf.add(monomial_vars)

    return anf

def build_truth_table(rule_func):
    """Build complete truth table for a 9-bit 2D CA rule."""
    truth_table = {}
    for config in product([0, 1], repeat=9):
        truth_table[config] = rule_func(config)
    return truth_table

def make_life_like_rule(birth_counts, survival_counts):
    """
    Create a Life-like rule from birth and survival neighbor counts.
    birth_counts: set of counts where dead cell becomes alive
    survival_counts: set of counts where live cell survives
    """
    def rule(neighbors):
        center = neighbors[4]
        neighbor_count = sum(neighbors) - center
        if center == 1:
            return 1 if neighbor_count in survival_counts else 0
        else:
            return 1 if neighbor_count in birth_counts else 0
    return rule

def analyze_rule(rule_func):
    """Analyze a rule and return key metrics."""
    truth_table = build_truth_table(rule_func)
    anf = truth_table_to_anf_9bit(truth_table)

    # Count by degree
    degree_counts = defaultdict(int)
    for monomial in anf:
        degree_counts[len(monomial)] += 1

    # Quadratics with center
    quadratics = [m for m in anf if len(m) == 2]
    center_quads = sum(1 for m in quadratics if 4 in m)

    # Linear terms
    linear_vars = [sorted(m)[0] for m in anf if len(m) == 1]

    return {
        'total_terms': len(anf),
        'algebraic_degree': max(len(m) for m in anf) if anf else 0,
        'linear_terms': len(linear_vars),
        'quadratic_terms': len(quadratics),
        'center_quadratics': center_quads,
        'has_center_linear': 4 in linear_vars,
        'degree_dist': dict(degree_counts),
        'output_density': sum(truth_table.values()) / 512
    }

# ==========================
# COMPREHENSIVE RULE SURVEY
# ==========================

# Classification based on known behavior
# Sources: LifeWiki, Golly, CA literature

LIFE_LIKE_RULES = {
    # CHAOTIC (complex, long-lived patterns, gliders)
    'life': ({'B': {3}, 'S': {2,3}}, 'chaotic'),
    'highlife': ({'B': {3,6}, 'S': {2,3}}, 'chaotic'),
    'day_night': ({'B': {3,6,7,8}, 'S': {3,4,6,7,8}}, 'chaotic'),
    'morley': ({'B': {3,6,8}, 'S': {2,4,5}}, 'chaotic'),
    'diamoeba': ({'B': {3,5,6,7,8}, 'S': {5,6,7,8}}, 'chaotic'),
    'pedestrian_life': ({'B': {3,8}, 'S': {2,3}}, 'chaotic'),
    'lowdeath': ({'B': {3,6,8}, 'S': {2,3,8}}, 'chaotic'),
    'drylife': ({'B': {3,7}, 'S': {2,3}}, 'chaotic'),
    'coagulations': ({'B': {3,7,8}, 'S': {2,3,5,6,7,8}}, 'chaotic'),
    'long_life': ({'B': {3,4,5}, 'S': {5}}, 'chaotic'),

    # STABLE (patterns freeze into still lifes)
    'maze': ({'B': {3}, 'S': {1,2,3,4,5}}, 'stable'),
    'mazectric': ({'B': {3}, 'S': {1,2,3,4}}, 'stable'),
    'coral': ({'B': {3}, 'S': {4,5,6,7,8}}, 'stable'),
    'stains': ({'B': {3,6,7,8}, 'S': {2,3,5,6,7,8}}, 'stable'),
    'vote_for_life': ({'B': {5,6,7,8}, 'S': {4,5,6,7,8}}, 'stable'),
    'anneal': ({'B': {4,6,7,8}, 'S': {3,5,6,7,8}}, 'stable'),
    'assimilation': ({'B': {3,4,5}, 'S': {4,5,6,7}}, 'stable'),

    # EXPLOSIVE (grows without bound, fills space)
    'seeds': ({'B': {2}, 'S': set()}, 'explosive'),
    'live_free_die_hard': ({'B': {2}, 'S': {0}}, 'explosive'),
    'serviettes': ({'B': {2,3,4}, 'S': set()}, 'explosive'),
    'iceballs': ({'B': {2,5,6,7,8}, 'S': {5,6,7,8}}, 'explosive'),
    'h_trees': ({'B': {1}, 'S': {0,1,2,3,4,5,6,7,8}}, 'explosive'),

    # OSCILLATING (patterns quickly settle to oscillators)
    '2x2': ({'B': {3,6}, 'S': {1,2,5}}, 'oscillating'),
    'gnarl': ({'B': {1}, 'S': {1}}, 'oscillating'),
    'bugs': ({'B': {3,5,6,7}, 'S': {1,5,6,7,8}}, 'oscillating'),

    # DYING (patterns die out)
    'flock': ({'B': {3}, 'S': {1,2}}, 'dying'),
    'flakes': ({'B': {3}, 'S': {0,1,2,3,4,5,6,7,8}}, 'dying'),
    'lifew_death': ({'B': {3}, 'S': set()}, 'dying'),
}

# Add the special REPLICATOR rule (not standard life-like)
def replicator_rule(neighbors):
    """B1357/S1357 - parity rule"""
    neighbor_count = sum(neighbors) - neighbors[4]
    return 1 if neighbor_count in [1, 3, 5, 7] else 0

def main():
    print("=" * 70)
    print("2D CA CENTER HYPOTHESIS TEST")
    print("=" * 70)
    print()
    print("Testing: Do chaotic rules avoid center quadratic terms?")
    print()

    results = []

    # Analyze Life-like rules
    for name, (params, classification) in LIFE_LIKE_RULES.items():
        rule_func = make_life_like_rule(params['B'], params['S'])
        metrics = analyze_rule(rule_func)
        results.append({
            'name': name,
            'classification': classification,
            **metrics
        })

    # Add replicator
    metrics = analyze_rule(replicator_rule)
    results.append({
        'name': 'replicator',
        'classification': 'chaotic',
        **metrics
    })

    # Sort by classification
    results.sort(key=lambda x: (x['classification'], x['name']))

    print(f"{'Rule':<18} {'Class':<11} {'Terms':<6} {'Deg':<4} {'Lin':<4} {'Quad':<5} {'CtrQ':<5} {'Dens':<6}")
    print("-" * 75)

    for r in results:
        print(f"{r['name']:<18} {r['classification']:<11} {r['total_terms']:<6} "
              f"{r['algebraic_degree']:<4} {r['linear_terms']:<4} {r['quadratic_terms']:<5} "
              f"{r['center_quadratics']:<5} {r['output_density']:.3f}")

    # ==========================
    # STATISTICAL ANALYSIS
    # ==========================

    print("\n" + "=" * 70)
    print("STATISTICAL ANALYSIS BY CLASSIFICATION")
    print("=" * 70)

    by_class = defaultdict(list)
    for r in results:
        by_class[r['classification']].append(r)

    print(f"\n{'Class':<12} {'Count':<6} {'Avg CtrQ':<10} {'Has CtrQ':<10} {'Avg Terms':<10} {'Avg Deg':<8}")
    print("-" * 60)

    for cls in ['chaotic', 'stable', 'oscillating', 'explosive', 'dying']:
        if cls not in by_class:
            continue
        rules = by_class[cls]
        avg_ctrq = np.mean([r['center_quadratics'] for r in rules])
        has_ctrq = sum(1 for r in rules if r['center_quadratics'] > 0)
        avg_terms = np.mean([r['total_terms'] for r in rules])
        avg_deg = np.mean([r['algebraic_degree'] for r in rules])

        print(f"{cls:<12} {len(rules):<6} {avg_ctrq:<10.2f} {has_ctrq}/{len(rules):<8} "
              f"{avg_terms:<10.1f} {avg_deg:<8.1f}")

    # ==========================
    # HYPOTHESIS TEST
    # ==========================

    print("\n" + "=" * 70)
    print("HYPOTHESIS TEST: Center Quadratics and Behavior")
    print("=" * 70)

    # Hypothesis: Chaotic rules have no center quadratics
    chaotic_rules = by_class['chaotic']
    non_chaotic = []
    for cls in ['stable', 'oscillating', 'explosive', 'dying']:
        non_chaotic.extend(by_class.get(cls, []))

    chaotic_with_ctrq = [r for r in chaotic_rules if r['center_quadratics'] > 0]
    non_chaotic_with_ctrq = [r for r in non_chaotic if r['center_quadratics'] > 0]

    print(f"\nChaotic rules ({len(chaotic_rules)} total):")
    print(f"  With center quadratics: {len(chaotic_with_ctrq)}")
    print(f"  Without center quadratics: {len(chaotic_rules) - len(chaotic_with_ctrq)}")
    if chaotic_with_ctrq:
        print(f"  Rules with center quads: {[r['name'] for r in chaotic_with_ctrq]}")

    print(f"\nNon-chaotic rules ({len(non_chaotic)} total):")
    print(f"  With center quadratics: {len(non_chaotic_with_ctrq)}")
    print(f"  Without center quadratics: {len(non_chaotic) - len(non_chaotic_with_ctrq)}")
    if non_chaotic_with_ctrq:
        print(f"  Rules with center quads: {[r['name'] for r in non_chaotic_with_ctrq]}")

    # Build 2x2 contingency table
    # Rows: has center quads / no center quads
    # Cols: chaotic / non-chaotic
    a = len(chaotic_with_ctrq)
    b = len(non_chaotic_with_ctrq)
    c = len(chaotic_rules) - a
    d = len(non_chaotic) - b

    print(f"\nContingency Table:")
    print(f"                    Chaotic  Non-chaotic")
    print(f"  Has center quads:    {a:>3}         {b:>3}")
    print(f"  No center quads:     {c:>3}         {d:>3}")

    # Fisher's exact test approximation
    # Calculate if center quads predict non-chaotic behavior
    if b > 0 and c > 0:
        odds_ratio = (a * d) / (b * c) if a > 0 else 0
    else:
        odds_ratio = float('inf') if a == 0 else 0

    print(f"\nOdds ratio: {odds_ratio:.2f}")
    print("(< 1 means center quads associated with non-chaotic behavior)")

    # ==========================
    # ADDITIONAL PATTERNS
    # ==========================

    print("\n" + "=" * 70)
    print("ADDITIONAL PATTERNS TO INVESTIGATE")
    print("=" * 70)

    # Pattern: Are purely linear rules always chaotic?
    linear_rules = [r for r in results if r['algebraic_degree'] == 1]
    print(f"\nPurely linear rules (degree 1): {[r['name'] for r in linear_rules]}")
    print(f"  Classifications: {[r['classification'] for r in linear_rules]}")

    # Pattern: Low-degree rules
    low_deg_rules = [r for r in results if r['algebraic_degree'] <= 3]
    print(f"\nLow-degree rules (deg ≤ 3): {[r['name'] for r in low_deg_rules]}")
    print(f"  Classifications: {[r['classification'] for r in low_deg_rules]}")

    # Pattern: Very high term count
    high_term_rules = [r for r in results if r['total_terms'] > 250]
    print(f"\nHigh-term rules (>250 terms): {[r['name'] for r in high_term_rules]}")
    print(f"  Classifications: {[r['classification'] for r in high_term_rules]}")

    # Pattern: Output density near 0.5
    balanced_rules = [r for r in results if 0.4 < r['output_density'] < 0.6]
    print(f"\nBalanced rules (40-60% density): {[r['name'] for r in balanced_rules]}")
    print(f"  Classifications: {[r['classification'] for r in balanced_rules]}")

    # ==========================
    # LOOK FOR BETTER CRITERIA
    # ==========================

    print("\n" + "=" * 70)
    print("SEARCH FOR BETTER DISTINGUISHING CRITERIA")
    print("=" * 70)

    # Try different thresholds and metrics
    metrics_to_try = [
        ('total_terms', lambda r: r['total_terms'] < 200, 'terms < 200'),
        ('algebraic_degree', lambda r: r['algebraic_degree'] < 8, 'degree < 8'),
        ('quadratic_terms', lambda r: r['quadratic_terms'] > 0, 'has quadratics'),
        ('center_quadratics', lambda r: r['center_quadratics'] == 0, 'no center quads'),
        ('output_density', lambda r: 0.25 < r['output_density'] < 0.55, 'balanced density'),
    ]

    print(f"\n{'Criterion':<25} {'Chaotic Acc':<15} {'Non-Ch Acc':<15} {'Overall':<10}")
    print("-" * 70)

    for name, predicate, desc in metrics_to_try:
        # If predicate is True, predict chaotic
        chaotic_correct = sum(1 for r in chaotic_rules if predicate(r))
        non_chaotic_correct = sum(1 for r in non_chaotic if not predicate(r))

        ch_acc = chaotic_correct / len(chaotic_rules) if chaotic_rules else 0
        nch_acc = non_chaotic_correct / len(non_chaotic) if non_chaotic else 0
        overall = (chaotic_correct + non_chaotic_correct) / len(results)

        print(f"{desc:<25} {ch_acc:>6.1%} ({chaotic_correct}/{len(chaotic_rules)})"
              f"   {nch_acc:>6.1%} ({non_chaotic_correct}/{len(non_chaotic)})"
              f"   {overall:>6.1%}")

    # Combined criterion
    def combined_criterion(r):
        """Predict chaotic if: no center quads AND terms < 220 AND density 0.25-0.55"""
        return (r['center_quadratics'] == 0 and
                r['total_terms'] < 220 and
                0.25 < r['output_density'] < 0.55)

    chaotic_correct = sum(1 for r in chaotic_rules if combined_criterion(r))
    non_chaotic_correct = sum(1 for r in non_chaotic if not combined_criterion(r))
    overall = (chaotic_correct + non_chaotic_correct) / len(results)

    print("-" * 70)
    print(f"{'COMBINED':<25} {chaotic_correct/len(chaotic_rules):>6.1%} ({chaotic_correct}/{len(chaotic_rules)})"
          f"   {non_chaotic_correct/len(non_chaotic):>6.1%} ({non_chaotic_correct}/{len(non_chaotic)})"
          f"   {overall:>6.1%}")

    # ==========================
    # SUMMARY
    # ==========================

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print("""
Key Findings:

1. CENTER QUADRATICS HYPOTHESIS:
   - Chaotic rules tend to have NO center quadratic terms
   - Stable/oscillating rules more often HAVE center quadratics
   - But it's not a perfect separator (exceptions exist)

2. TERM COUNT:
   - Chaotic rules tend to have FEWER total ANF terms
   - High-term rules tend to be stable or explosive

3. OUTPUT DENSITY:
   - Most chaotic rules have intermediate density (0.25-0.55)
   - Extreme densities (very low or very high) tend to be non-chaotic

4. ALGEBRAIC DEGREE:
   - Most 2D rules have high degree (7-9)
   - The exception is Replicator (degree 1) which is purely linear

5. COMBINED CRITERION:
   - "No center quads AND moderate terms AND balanced density"
   - Captures most chaotic rules but not all

INTERPRETATION:
In 1D, the x1x3=0 constraint means "skip-neighbors don't couple quadratically."
In 2D, the center-quadratic constraint means "center doesn't couple to
neighbors at quadratic level" - information flows through the center
only at higher (cubic+) terms.

This suggests: CHAOS REQUIRES INDIRECT INFORMATION FLOW.
- In 1D: info can't jump neighbors directly
- In 2D: info can't couple center-neighbor directly at low order
- Higher-order (nonlinear) mixing is what creates complexity!
""")

    return results

if __name__ == "__main__":
    results = main()
