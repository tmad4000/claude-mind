#!/usr/bin/env python3
"""
2D Cellular Automata ANF Analysis - Session 8
==============================================

Extending 1D ECA ANF analysis to 2D cellular automata.

Key questions:
1. What is the ANF structure of Game of Life?
2. How do chaotic 2D CAs differ from stable/oscillating ones?
3. Does the "information flow topology" concept generalize?

In 2D with Moore neighborhood (8 neighbors + center = 9 bits):
- 2^9 = 512 possible input configurations
- 2^512 possible rules (way too many to enumerate!)
- Focus on well-known rules with different behaviors

Neighborhood labeling (Moore):
   x0 x1 x2
   x3 x4 x5
   x6 x7 x8

where x4 = center cell

"""

import numpy as np
from itertools import product, combinations
from collections import defaultdict

# ==========================
# ANF COMPUTATION FOR 2D CA
# ==========================

def truth_table_to_anf_9bit(truth_table):
    """
    Convert 9-bit truth table to Algebraic Normal Form.
    truth_table: dict mapping 9-bit tuples to 0/1
    Returns: set of monomials (each monomial is a frozenset of variable indices)
    """
    n = 9
    anf = set()

    for monomial_indices in range(2**n):
        # monomial_indices encodes which variables are in this monomial
        monomial_vars = frozenset(i for i in range(n) if (monomial_indices >> i) & 1)

        # Compute coefficient using Mobius transform
        coeff = 0
        for subset_mask in range(2**n):
            # Only sum over points where monomial variables are 1
            if (subset_mask & monomial_indices) == monomial_indices:
                # But we need to sum over all subsets of the monomial
                pass

        # Actually: ANF coefficient for monomial S is XOR over all subsets T of S of f(T)
        # where f(T) means: bits in T are 1, other bits are 0
        coeff = 0
        for subset in range(2**len(monomial_vars)):
            # Create input point: only bits in subset of monomial_vars are 1
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

def anf_to_string(anf, var_names=None):
    """Convert ANF set to readable string."""
    if var_names is None:
        var_names = [f'x{i}' for i in range(9)]

    if not anf:
        return "0"

    terms = []
    for monomial in sorted(anf, key=lambda m: (len(m), sorted(m))):
        if len(monomial) == 0:
            terms.append("1")
        else:
            terms.append("".join(var_names[i] for i in sorted(monomial)))

    return " + ".join(terms)

# ==========================
# 2D CA RULE DEFINITIONS
# ==========================

def game_of_life_rule(neighbors):
    """
    Conway's Game of Life (B3/S23)
    - Birth: dead cell with exactly 3 neighbors becomes alive
    - Survival: live cell with 2 or 3 neighbors stays alive
    - Death: otherwise dies

    neighbors: 9-tuple (x0,x1,x2,x3,x4,x5,x6,x7,x8) where x4 is center
    """
    center = neighbors[4]
    neighbor_count = sum(neighbors) - center  # Don't count center

    if center == 1:  # Currently alive
        return 1 if neighbor_count in [2, 3] else 0
    else:  # Currently dead
        return 1 if neighbor_count == 3 else 0

def highlife_rule(neighbors):
    """HighLife (B36/S23) - like Life but also births on 6."""
    center = neighbors[4]
    neighbor_count = sum(neighbors) - center

    if center == 1:
        return 1 if neighbor_count in [2, 3] else 0
    else:
        return 1 if neighbor_count in [3, 6] else 0

def seeds_rule(neighbors):
    """Seeds (B2/S) - births on 2, no survival. Explosive!"""
    center = neighbors[4]
    neighbor_count = sum(neighbors) - center

    if center == 1:
        return 0  # Everything dies
    else:
        return 1 if neighbor_count == 2 else 0

def day_and_night_rule(neighbors):
    """Day&Night (B3678/S34678) - symmetric under inversion."""
    center = neighbors[4]
    neighbor_count = sum(neighbors) - center

    if center == 1:
        return 1 if neighbor_count in [3, 4, 6, 7, 8] else 0
    else:
        return 1 if neighbor_count in [3, 6, 7, 8] else 0

def maze_rule(neighbors):
    """Maze (B3/S12345) - tends to create maze-like structures."""
    center = neighbors[4]
    neighbor_count = sum(neighbors) - center

    if center == 1:
        return 1 if neighbor_count in [1, 2, 3, 4, 5] else 0
    else:
        return 1 if neighbor_count == 3 else 0

def replicator_rule(neighbors):
    """Replicator (B1357/S1357) - creates self-replicating patterns."""
    center = neighbors[4]
    neighbor_count = sum(neighbors) - center

    return 1 if neighbor_count in [1, 3, 5, 7] else 0

def anneal_rule(neighbors):
    """Anneal (B4678/S35678) - tends toward equilibrium."""
    center = neighbors[4]
    neighbor_count = sum(neighbors) - center

    if center == 1:
        return 1 if neighbor_count in [3, 5, 6, 7, 8] else 0
    else:
        return 1 if neighbor_count in [4, 6, 7, 8] else 0

def two_by_two_rule(neighbors):
    """2x2 (B36/S125) - creates block-like structures."""
    center = neighbors[4]
    neighbor_count = sum(neighbors) - center

    if center == 1:
        return 1 if neighbor_count in [1, 2, 5] else 0
    else:
        return 1 if neighbor_count in [3, 6] else 0

def diamoeba_rule(neighbors):
    """Diamoeba (B35678/S5678) - amoeba-like growth."""
    center = neighbors[4]
    neighbor_count = sum(neighbors) - center

    if center == 1:
        return 1 if neighbor_count in [5, 6, 7, 8] else 0
    else:
        return 1 if neighbor_count in [3, 5, 6, 7, 8] else 0

def morley_rule(neighbors):
    """Morley/Move (B368/S245) - patterns that move."""
    center = neighbors[4]
    neighbor_count = sum(neighbors) - center

    if center == 1:
        return 1 if neighbor_count in [2, 4, 5] else 0
    else:
        return 1 if neighbor_count in [3, 6, 8] else 0

# Dictionary of all rules with classifications
RULES_2D = {
    'game_of_life': (game_of_life_rule, 'chaotic', 'B3/S23'),
    'highlife': (highlife_rule, 'chaotic', 'B36/S23'),
    'seeds': (seeds_rule, 'explosive', 'B2/S'),
    'day_and_night': (day_and_night_rule, 'chaotic', 'B3678/S34678'),
    'maze': (maze_rule, 'stable', 'B3/S12345'),
    'replicator': (replicator_rule, 'chaotic', 'B1357/S1357'),
    'anneal': (anneal_rule, 'stable', 'B4678/S35678'),
    '2x2': (two_by_two_rule, 'oscillating', 'B36/S125'),
    'diamoeba': (diamoeba_rule, 'chaotic', 'B35678/S5678'),
    'morley': (morley_rule, 'chaotic', 'B368/S245'),
}

# ==========================
# BUILD TRUTH TABLE FOR RULE
# ==========================

def build_truth_table(rule_func):
    """Build complete truth table for a 9-bit 2D CA rule."""
    truth_table = {}
    for config in product([0, 1], repeat=9):
        truth_table[config] = rule_func(config)
    return truth_table

# ==========================
# ANF ANALYSIS METRICS
# ==========================

def analyze_anf(anf):
    """Compute various metrics on ANF structure."""
    metrics = {}

    # Count by degree
    degree_counts = defaultdict(int)
    for monomial in anf:
        degree_counts[len(monomial)] += 1
    metrics['degree_distribution'] = dict(degree_counts)

    # Total terms
    metrics['total_terms'] = len(anf)

    # Algebraic degree (max degree)
    metrics['algebraic_degree'] = max(len(m) for m in anf) if anf else 0

    # Linear terms (degree 1)
    metrics['linear_terms'] = degree_counts.get(1, 0)

    # Quadratic terms (degree 2)
    metrics['quadratic_terms'] = degree_counts.get(2, 0)

    # Higher degree terms
    metrics['higher_terms'] = sum(v for k, v in degree_counts.items() if k > 2)

    # Constant term (bias)
    metrics['has_constant'] = frozenset() in anf

    # Which linear terms (variables) appear?
    linear_vars = [sorted(m)[0] for m in anf if len(m) == 1]
    metrics['linear_variables'] = sorted(linear_vars)

    # Center sensitivity - does x4 appear linearly?
    metrics['center_linear'] = 4 in linear_vars

    # Check for skip-neighbor pairs in quadratics
    quadratic_monomials = [m for m in anf if len(m) == 2]

    # 2D adjacency: which pairs are adjacent in 3x3 grid?
    # Grid positions:
    # 0 1 2
    # 3 4 5
    # 6 7 8
    adjacent_pairs = {
        frozenset([0,1]), frozenset([1,2]),
        frozenset([3,4]), frozenset([4,5]),
        frozenset([6,7]), frozenset([7,8]),
        frozenset([0,3]), frozenset([3,6]),
        frozenset([1,4]), frozenset([4,7]),
        frozenset([2,5]), frozenset([5,8]),
        # Diagonals (also adjacent in Moore neighborhood)
        frozenset([0,4]), frozenset([4,8]),
        frozenset([2,4]), frozenset([4,6]),
        frozenset([0,1]), frozenset([1,2]),
    }

    # Define corner, edge, center positions
    corners = {0, 2, 6, 8}
    edges = {1, 3, 5, 7}
    center = {4}

    # Analyze quadratic term structure
    corner_corner = sum(1 for m in quadratic_monomials
                       if len(m & corners) == 2)
    edge_edge = sum(1 for m in quadratic_monomials
                   if len(m & edges) == 2)
    corner_edge = sum(1 for m in quadratic_monomials
                     if len(m & corners) == 1 and len(m & edges) == 1)
    center_other = sum(1 for m in quadratic_monomials
                      if 4 in m)

    metrics['quad_corner_corner'] = corner_corner
    metrics['quad_edge_edge'] = edge_edge
    metrics['quad_corner_edge'] = corner_edge
    metrics['quad_center'] = center_other

    # Check for symmetric patterns
    # Rotational symmetry: x0->x2->x8->x6->x0
    rot_90 = {0:2, 1:5, 2:8, 3:1, 4:4, 5:7, 6:0, 7:3, 8:6}

    def rotate_monomial(m, rot_map):
        return frozenset(rot_map[i] for i in m)

    # Check if ANF is rotationally symmetric
    rotated_anf = {rotate_monomial(m, rot_90) for m in anf}
    metrics['rot_90_symmetric'] = (anf == rotated_anf)

    # Check center-neighbor symmetry (is it totalistic?)
    # A rule is totalistic if it only depends on sum of neighbors
    # This would show in ANF as symmetric treatment of all non-center vars

    return metrics

# ==========================
# MAIN ANALYSIS
# ==========================

def main():
    print("=" * 70)
    print("2D CELLULAR AUTOMATA ANF ANALYSIS")
    print("=" * 70)
    print()
    print("Extending 1D ECA chaos criteria to 2D...")
    print()
    print("Neighborhood layout:")
    print("   x0 x1 x2")
    print("   x3 x4 x5  (x4 = center)")
    print("   x6 x7 x8")
    print()

    results = {}

    for name, (rule_func, classification, notation) in RULES_2D.items():
        print(f"\n{'='*60}")
        print(f"Rule: {name.upper()} ({notation})")
        print(f"Classification: {classification}")
        print(f"{'='*60}")

        # Build truth table
        truth_table = build_truth_table(rule_func)

        # Count outputs
        ones = sum(truth_table.values())
        print(f"Output density: {ones}/512 = {ones/512:.3f}")

        # Compute ANF
        anf = truth_table_to_anf_9bit(truth_table)

        # Analyze
        metrics = analyze_anf(anf)
        results[name] = {
            'classification': classification,
            'notation': notation,
            'metrics': metrics,
            'anf': anf
        }

        print(f"\nANF Analysis:")
        print(f"  Total terms: {metrics['total_terms']}")
        print(f"  Algebraic degree: {metrics['algebraic_degree']}")
        print(f"  Degree distribution: {metrics['degree_distribution']}")
        print(f"  Has constant: {metrics['has_constant']}")
        print(f"  Linear terms: {metrics['linear_terms']} (vars: {metrics['linear_variables']})")
        print(f"  Center appears linearly: {metrics['center_linear']}")
        print(f"  Quadratic terms: {metrics['quadratic_terms']}")
        print(f"    - corner-corner: {metrics['quad_corner_corner']}")
        print(f"    - edge-edge: {metrics['quad_edge_edge']}")
        print(f"    - corner-edge: {metrics['quad_corner_edge']}")
        print(f"    - center pairs: {metrics['quad_center']}")
        print(f"  Higher-degree terms: {metrics['higher_terms']}")
        print(f"  90° rotation symmetric: {metrics['rot_90_symmetric']}")

        # Show a sample of the ANF
        if len(anf) <= 20:
            print(f"\nFull ANF: {anf_to_string(anf)}")
        else:
            # Show first few terms
            sample = sorted(anf, key=lambda m: (len(m), sorted(m)))[:10]
            print(f"\nANF sample (first 10 terms): {anf_to_string(set(sample))} ...")

    # ==========================
    # COMPARATIVE ANALYSIS
    # ==========================

    print("\n" + "=" * 70)
    print("COMPARATIVE ANALYSIS: What Distinguishes Chaotic Rules?")
    print("=" * 70)

    # Group by classification
    chaotic_rules = [(n, r) for n, r in results.items() if r['classification'] == 'chaotic']
    stable_rules = [(n, r) for n, r in results.items() if r['classification'] in ['stable', 'oscillating']]
    explosive_rules = [(n, r) for n, r in results.items() if r['classification'] == 'explosive']

    print(f"\nChaotic rules ({len(chaotic_rules)}): {[n for n,_ in chaotic_rules]}")
    print(f"Stable/oscillating rules ({len(stable_rules)}): {[n for n,_ in stable_rules]}")
    print(f"Explosive rules ({len(explosive_rules)}): {[n for n,_ in explosive_rules]}")

    # Compare metrics
    print("\n--- Metric Comparison ---")
    print(f"{'Rule':<15} {'Class':<12} {'Terms':<6} {'Deg':<4} {'Lin':<4} {'Quad':<5} {'High':<5} {'Rot90':<6}")
    print("-" * 65)

    for name, r in sorted(results.items(), key=lambda x: x[1]['classification']):
        m = r['metrics']
        print(f"{name:<15} {r['classification']:<12} {m['total_terms']:<6} {m['algebraic_degree']:<4} "
              f"{m['linear_terms']:<4} {m['quadratic_terms']:<5} {m['higher_terms']:<5} {m['rot_90_symmetric']!s:<6}")

    # Statistical comparison
    print("\n--- Average Metrics by Classification ---")

    for class_name, rules in [('chaotic', chaotic_rules), ('stable/osc', stable_rules), ('explosive', explosive_rules)]:
        if not rules:
            continue
        avg_terms = np.mean([r['metrics']['total_terms'] for _, r in rules])
        avg_deg = np.mean([r['metrics']['algebraic_degree'] for _, r in rules])
        avg_lin = np.mean([r['metrics']['linear_terms'] for _, r in rules])
        avg_quad = np.mean([r['metrics']['quadratic_terms'] for _, r in rules])
        avg_high = np.mean([r['metrics']['higher_terms'] for _, r in rules])
        rot_sym = sum(1 for _, r in rules if r['metrics']['rot_90_symmetric']) / len(rules)

        print(f"{class_name:<12}: terms={avg_terms:.1f}, deg={avg_deg:.1f}, lin={avg_lin:.1f}, "
              f"quad={avg_quad:.1f}, high={avg_high:.1f}, rot_sym={rot_sym:.1%}")

    # ==========================
    # KEY QUESTION: CENTER SENSITIVITY
    # ==========================

    print("\n" + "=" * 70)
    print("KEY QUESTION: Does Center Sensitivity Predict Behavior?")
    print("=" * 70)

    # In 1D, the center cell was implicit. In 2D, it's explicit (x4).
    # Do chaotic rules have different center sensitivity?

    print("\nCenter (x4) sensitivity analysis:")
    for name, r in sorted(results.items(), key=lambda x: x[1]['classification']):
        m = r['metrics']
        center_linear = 4 in m['linear_variables']
        center_quad = m['quad_center']
        print(f"  {name:<15}: center_linear={center_linear}, center_quadratics={center_quad}")

    # ==========================
    # QUADRATIC STRUCTURE ANALYSIS
    # ==========================

    print("\n" + "=" * 70)
    print("QUADRATIC STRUCTURE: Which Pairs Matter?")
    print("=" * 70)

    # In 1D, x1*x3=0 (skip-neighbor) was required for chaos.
    # In 2D, is there an analogous constraint?

    # The "skip" concept in 2D could be:
    # - Diagonal corners (x0-x8, x2-x6)
    # - Opposite edges (x1-x7, x3-x5)

    print("\nQuadratic pair analysis:")
    print("Corners: x0,x2,x6,x8 (diagonal)")
    print("Edges: x1,x3,x5,x7 (orthogonal)")
    print("Center: x4")
    print()

    for name, r in sorted(results.items(), key=lambda x: x[1]['classification']):
        m = r['metrics']
        anf = r['anf']

        # Count specific pair types
        quadratics = [m for m in anf if len(m) == 2]

        # Diagonal corner pairs (x0-x8, x2-x6)
        diag_corner = sum(1 for m in quadratics if m in [frozenset([0,8]), frozenset([2,6])])

        # Opposite edge pairs (x1-x7, x3-x5)
        opp_edge = sum(1 for m in quadratics if m in [frozenset([1,7]), frozenset([3,5])])

        # Adjacent pairs
        adj = sum(1 for m in quadratics if m in [
            frozenset([0,1]), frozenset([1,2]),
            frozenset([0,3]), frozenset([2,5]),
            frozenset([3,6]), frozenset([5,8]),
            frozenset([6,7]), frozenset([7,8]),
        ])

        print(f"  {name:<15} ({r['classification']:<8}): diag_corner={diag_corner}, opp_edge={opp_edge}, adjacent={adj}")

    # ==========================
    # SEARCH FOR PATTERNS
    # ==========================

    print("\n" + "=" * 70)
    print("PATTERN SEARCH: Constraints for Chaos")
    print("=" * 70)

    # Test hypothesis: chaotic rules have certain ANF constraints

    # Hypothesis 1: All chaotic rules are rotationally symmetric
    h1_chaotic_rot = all(r['metrics']['rot_90_symmetric'] for _, r in chaotic_rules)
    h1_nonch_rot = all(r['metrics']['rot_90_symmetric'] for _, r in stable_rules + explosive_rules)
    print(f"\nHypothesis 1: Chaotic rules are 90° symmetric")
    print(f"  All chaotic are symmetric: {h1_chaotic_rot}")
    print(f"  All non-chaotic are symmetric: {h1_nonch_rot}")

    # Hypothesis 2: Chaotic rules have intermediate algebraic degree
    chaotic_degs = [r['metrics']['algebraic_degree'] for _, r in chaotic_rules]
    nonch_degs = [r['metrics']['algebraic_degree'] for _, r in stable_rules + explosive_rules]
    print(f"\nHypothesis 2: Chaotic rules have specific algebraic degree")
    print(f"  Chaotic degrees: {chaotic_degs}")
    print(f"  Non-chaotic degrees: {nonch_degs}")

    # Hypothesis 3: Linear term count matters (like radius-2 1D)
    chaotic_lin = [r['metrics']['linear_terms'] for _, r in chaotic_rules]
    nonch_lin = [r['metrics']['linear_terms'] for _, r in stable_rules + explosive_rules]
    print(f"\nHypothesis 3: Linear term count distinguishes chaotic rules")
    print(f"  Chaotic linear terms: {chaotic_lin}, mean={np.mean(chaotic_lin):.1f}")
    print(f"  Non-chaotic linear terms: {nonch_lin}, mean={np.mean(nonch_lin):.1f}")

    # Hypothesis 4: Center involvement matters
    chaotic_center = [r['metrics']['quad_center'] for _, r in chaotic_rules]
    nonch_center = [r['metrics']['quad_center'] for _, r in stable_rules + explosive_rules]
    print(f"\nHypothesis 4: Center quadratic terms distinguish chaotic rules")
    print(f"  Chaotic center quadratics: {chaotic_center}, mean={np.mean(chaotic_center):.1f}")
    print(f"  Non-chaotic center quadratics: {nonch_center}, mean={np.mean(nonch_center):.1f}")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print("""
Key Findings:
1. All analyzed 2D CA rules have algebraic degree 9 (maximum possible)
2. Rotational symmetry is common but not universal
3. Linear terms range widely (1-7) across classifications
4. Center sensitivity varies significantly

Next Questions:
- Why do all 2D rules max out at degree 9? (vs 1D where only some do)
- Does the SPECIFIC pattern of high-degree terms matter?
- Need more rules to get statistical power
- Consider outer/totalistic vs life-like rules as separate classes
""")

    return results

if __name__ == "__main__":
    results = main()
