#!/usr/bin/env python3
"""
GEOMETRIC ANALYSIS OF ZERO SETS

The 8 possible inputs form the vertices of a 3D hypercube (binary cube).
The zero set (4 inputs that map to 0) forms a pattern on this cube.

Different patterns have different information-theoretic properties.
Let's classify all 4-ones max-mixing rules by their zero-set geometry.
"""

import numpy as np
from collections import defaultdict
from itertools import combinations

CHAOTIC_RULES = set([30, 45, 75, 86, 89, 101, 102, 105, 106, 150, 153, 154])

def rule_to_table(rule):
    return [(rule >> i) & 1 for i in range(8)]

def count_ones(rule):
    return bin(rule).count('1')

def count_mixing(rule):
    table = rule_to_table(rule)
    zero_inputs = set(i for i in range(8) if table[i] == 0)

    def can_follow(j, i):
        return ((j >> 0) & 3) == ((i >> 1) & 3)

    mixing = 0
    for j in range(8):
        for i in range(8):
            if can_follow(j, i):
                if (j in zero_inputs) != (i in zero_inputs):
                    mixing += 1
    return mixing

def hamming_distance(a, b):
    return bin(a ^ b).count('1')

def classify_zero_set(zeros):
    """
    Classify the geometric structure of a 4-element zero set on the 3D binary cube.

    Key structures:
    - Tetrahedron: all pairs at distance 2 (opposite corners)
    - Square: 4 edges (4 pairs at distance 1, 2 at distance 2)
    - Y-shape: 3 pairs at distance 1 from center
    - Line+point: 3 collinear + 1 off
    """
    zeros = sorted(zeros)

    # Compute all pairwise distances
    distances = []
    for i in range(4):
        for j in range(i+1, 4):
            distances.append(hamming_distance(zeros[i], zeros[j]))

    hist = {1: distances.count(1), 2: distances.count(2), 3: distances.count(3)}

    # Classify based on distance histogram
    if hist == {1: 0, 2: 6, 3: 0}:
        return "TETRAHEDRON"  # All pairs at distance 2 - two "anti-diagonal" pairs
    elif hist == {1: 4, 2: 2, 3: 0}:
        return "SQUARE"  # A face of the cube
    elif hist == {1: 2, 2: 4, 3: 0}:
        return "ZIGZAG"  # Two adjacent edges
    elif hist == {1: 3, 2: 3, 3: 0}:
        return "STAR"  # One vertex with 3 neighbors
    elif hist == {1: 2, 2: 3, 3: 1}:
        return "CHAIN"  # Path of length 3 (4 vertices)
    elif hist == {1: 2, 2: 2, 3: 2}:
        return "DIAGONAL_CHAIN"  # Path through diagonal
    else:
        return f"OTHER({hist})"

# Analyze all max-mixing 4-ones rules
four_ones_max_mixing = [r for r in range(256)
                        if count_ones(r) == 4 and count_mixing(r) == 8]

print("=" * 70)
print("ZERO SET GEOMETRY CLASSIFICATION")
print("=" * 70)

by_geometry = defaultdict(list)
for r in four_ones_max_mixing:
    table = rule_to_table(r)
    zeros = tuple(sorted(i for i in range(8) if table[i] == 0))
    geom = classify_zero_set(zeros)
    by_geometry[geom].append((r, zeros))

for geom, rules in sorted(by_geometry.items()):
    chaotic = [r for r, z in rules if r in CHAOTIC_RULES]
    periodic = [r for r, z in rules if r not in CHAOTIC_RULES]
    print(f"\n{geom}:")
    print(f"  Total: {len(rules)}, Chaotic: {len(chaotic)}, Periodic: {len(periodic)}")
    print(f"  Chaotic rules: {chaotic}")
    print(f"  Periodic rules: {periodic}")

# The key insight: what geometry correlates with chaos?
print("\n" + "=" * 70)
print("DEEP DIVE INTO CHAIN GEOMETRY")
print("=" * 70)

# Most chaotic rules seem to be CHAIN type - let's investigate further
chain_rules = [r for r, z in by_geometry.get("CHAIN", [])]
for r, zeros in by_geometry.get("CHAIN", []):
    is_chaotic = r in CHAOTIC_RULES
    status = "CHAOTIC" if is_chaotic else "periodic"
    table = rule_to_table(r)

    # Analyze the chain structure
    zeros_list = list(zeros)
    print(f"\n  Rule {r} [{status}]: zeros={zeros} = {[f'{z:03b}' for z in zeros]}")

    # Find the endpoints of the chain (vertices with only 1 neighbor in zeros)
    neighbors = {z: [] for z in zeros}
    for z1 in zeros:
        for z2 in zeros:
            if z1 != z2 and hamming_distance(z1, z2) == 1:
                neighbors[z1].append(z2)

    endpoints = [z for z in zeros if len(neighbors[z]) == 1]
    midpoints = [z for z in zeros if len(neighbors[z]) == 2]

    print(f"    Endpoints: {[f'{e:03b}' for e in endpoints]}")
    print(f"    Midpoints: {[f'{m:03b}' for m in midpoints]}")

    # Check which axis the chain travels along
    if endpoints:
        e1, e2 = endpoints
        chain_span = e1 ^ e2  # XOR gives which bits differ from end to end
        print(f"    Chain span: {chain_span:03b} (which bits change)")

# NEW HYPOTHESIS: Within CHAIN geometry, what distinguishes chaotic?
print("\n" + "=" * 70)
print("CHAIN GEOMETRY: CHAOTIC VS PERIODIC")
print("=" * 70)

def analyze_chain_detail(rule, zeros):
    """Detailed analysis of chain structure."""
    table = rule_to_table(rule)

    # Find endpoints and midpoints
    zeros_list = list(zeros)
    neighbors = {z: [] for z in zeros}
    for z1 in zeros:
        for z2 in zeros:
            if z1 != z2 and hamming_distance(z1, z2) == 1:
                neighbors[z1].append(z2)

    endpoints = sorted([z for z in zeros if len(neighbors[z]) == 1])
    midpoints = sorted([z for z in zeros if len(neighbors[z]) == 2])

    if len(endpoints) == 2:
        e1, e2 = endpoints
        chain_span = e1 ^ e2

        # Which bits are the endpoints?
        contains_0 = 0 in zeros
        contains_7 = 7 in zeros

        # Direction of chain
        direction = "left" if (chain_span & 4) else "center" if (chain_span & 2) else "right"

        return {
            'rule': rule,
            'endpoints': endpoints,
            'midpoints': midpoints,
            'span': chain_span,
            'contains_0': contains_0,
            'contains_7': contains_7,
            'direction': direction,
        }
    return None

print("\nDetailed chain analysis:")
for r, zeros in by_geometry.get("CHAIN", []):
    analysis = analyze_chain_detail(r, zeros)
    if analysis:
        is_chaotic = r in CHAOTIC_RULES
        status = "C" if is_chaotic else "P"
        print(f"{status} Rule {r:3d}: endpoints={analysis['endpoints']}, span={analysis['span']:03b}, has0={analysis['contains_0']}, has7={analysis['contains_7']}")

# Look at other geometries too
print("\n" + "=" * 70)
print("TETRAHEDRON GEOMETRY ANALYSIS")
print("=" * 70)

for r, zeros in by_geometry.get("TETRAHEDRON", []):
    is_chaotic = r in CHAOTIC_RULES
    status = "C" if is_chaotic else "P"
    table = rule_to_table(r)
    print(f"{status} Rule {r:3d}: zeros={zeros} = {[f'{z:03b}' for z in zeros]}")

    # Tetrahedra have a special property: they're either
    # {odd parity} or {even parity} vertices
    parity_sum = sum(bin(z).count('1') % 2 for z in zeros)
    parity_type = "EVEN" if parity_sum == 0 else "ODD" if parity_sum == 4 else "MIXED"
    print(f"    Parity: {parity_type}")

print("\n" + "=" * 70)
print("DIAGONAL_CHAIN GEOMETRY ANALYSIS")
print("=" * 70)

for r, zeros in by_geometry.get("DIAGONAL_CHAIN", []):
    is_chaotic = r in CHAOTIC_RULES
    status = "C" if is_chaotic else "P"
    print(f"{status} Rule {r:3d}: zeros={zeros} = {[f'{z:03b}' for z in zeros]}")

# Summary
print("\n" + "=" * 70)
print("GEOMETRIC SUMMARY")
print("=" * 70)

print("\nChaos by geometry:")
for geom, rules in sorted(by_geometry.items()):
    chaotic = [r for r, z in rules if r in CHAOTIC_RULES]
    total = len(rules)
    print(f"  {geom}: {len(chaotic)}/{total} chaotic ({100*len(chaotic)/total:.0f}%)")

# KEY INSIGHT: Perhaps it's the COMBINATION of geometry + other features
print("\n" + "=" * 70)
print("FINAL CHARACTERIZATION ATTEMPT")
print("=" * 70)

# For CHAIN geometry (most common), what extra feature separates C from P?
chain_rules_data = []
for r, zeros in by_geometry.get("CHAIN", []):
    table = rule_to_table(r)
    analysis = analyze_chain_detail(r, zeros)
    if analysis:
        # Additional features
        q0 = table[0] == 0
        q7 = table[7] == 1
        center_influence = sum(1 for left in [0, 4] for right in [0, 1]
                              if table[left + right] != table[left + right + 2])

        chain_rules_data.append({
            'rule': r,
            'is_chaotic': r in CHAOTIC_RULES,
            'zeros': zeros,
            'span': analysis['span'],
            'contains_0': analysis['contains_0'],
            'contains_7': analysis['contains_7'],
            'q0': q0,
            'q7': q7,
            'center_influence': center_influence,
        })

print("\nCHAIN rules with features:")
for d in chain_rules_data:
    status = "C" if d['is_chaotic'] else "P"
    print(f"  {status} {d['rule']:3d}: span={d['span']:03b}, has0={d['contains_0']}, has7={d['contains_7']}, q0={d['q0']}, q7={d['q7']}, center={d['center_influence']}")

# Check if span pattern separates
span_patterns = defaultdict(list)
for d in chain_rules_data:
    span_patterns[d['span']].append(d)

print("\n Span pattern distribution:")
for span, data in sorted(span_patterns.items()):
    chaotic = [d for d in data if d['is_chaotic']]
    periodic = [d for d in data if not d['is_chaotic']]
    print(f"  Span {span:03b}: {len(chaotic)} chaotic, {len(periodic)} periodic")
