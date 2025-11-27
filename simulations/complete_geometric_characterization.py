#!/usr/bin/env python3
"""
COMPLETE GEOMETRIC CHARACTERIZATION

The geometric approach works for TETRAHEDRON, SQUARE, STAR perfectly.
For CHAIN and DIAGONAL_CHAIN, need additional criteria.

Let's find the EXACT characterization that gives 100% accuracy.
"""

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

def classify_geometry(zeros):
    zeros = sorted(zeros)
    distances = []
    for i in range(4):
        for j in range(i+1, 4):
            distances.append(hamming_distance(zeros[i], zeros[j]))

    hist = (distances.count(1), distances.count(2), distances.count(3))

    if hist == (0, 6, 0):
        return "TETRAHEDRON"
    elif hist == (4, 2, 0):
        return "SQUARE"
    elif hist == (3, 3, 0):
        return "STAR"
    elif hist == (2, 3, 1):
        return "CHAIN"
    elif hist == (2, 2, 2):
        return "DIAGONAL_CHAIN"
    else:
        return f"OTHER({hist})"

# Get all 4-ones max-mixing rules
four_ones_max_mixing = [r for r in range(256)
                        if count_ones(r) == 4 and count_mixing(r) == 8]

# Focus on CHAIN and DIAGONAL_CHAIN
print("=" * 70)
print("CHAIN RULES - FINDING THE EXACT CRITERION")
print("=" * 70)

chain_rules = []
for r in four_ones_max_mixing:
    table = rule_to_table(r)
    zeros = tuple(sorted(i for i in range(8) if table[i] == 0))
    geom = classify_geometry(zeros)
    if geom == "CHAIN":
        chain_rules.append((r, zeros, r in CHAOTIC_RULES))

# For each chain rule, compute all possible features
def compute_chain_features(rule, zeros, is_chaotic):
    table = rule_to_table(rule)

    # Basic features
    has_0 = 0 in zeros
    has_7 = 7 in zeros

    # Find endpoints (vertices with 1 neighbor in zeros)
    neighbors = {z: [] for z in zeros}
    for z1 in zeros:
        for z2 in zeros:
            if z1 != z2 and hamming_distance(z1, z2) == 1:
                neighbors[z1].append(z2)
    endpoints = sorted([z for z in zeros if len(neighbors[z]) == 1])
    midpoints = sorted([z for z in zeros if len(neighbors[z]) == 2])

    # Endpoint analysis
    endpoint_0 = 0 in endpoints
    endpoint_7 = 7 in endpoints
    midpoint_0 = 0 in midpoints
    midpoint_7 = 7 in midpoints

    # Output analysis
    q0 = table[0] == 0  # 000 -> 0
    q7 = table[7] == 1  # 111 -> 1

    # Chain direction (which bits change from end to end)
    if len(endpoints) == 2:
        span = endpoints[0] ^ endpoints[1]
    else:
        span = 0

    return {
        'rule': rule,
        'zeros': zeros,
        'is_chaotic': is_chaotic,
        'has_0': has_0,
        'has_7': has_7,
        'endpoint_0': endpoint_0,
        'endpoint_7': endpoint_7,
        'midpoint_0': midpoint_0,
        'midpoint_7': midpoint_7,
        'endpoints': endpoints,
        'midpoints': midpoints,
        'span': span,
        'q0': q0,
        'q7': q7,
    }

chain_features = [compute_chain_features(r, z, c) for r, z, c in chain_rules]

print("\nAll CHAIN rules with features:")
for f in chain_features:
    status = "C" if f['is_chaotic'] else "P"
    print(f"{status} {f['rule']:3d}: zeros={f['zeros']}, endpoints={f['endpoints']}, midpoint_7={f['midpoint_7']}, q0={f['q0']}, q7={f['q7']}")

# Find distinguishing feature
print("\n" + "-" * 60)
print("TESTING HYPOTHESIS: midpoint_7 (7 is in midpoint position)")
print("-" * 60)

for f in chain_features:
    predicted = f['midpoint_7']
    actual = f['is_chaotic']
    status = "CORRECT" if predicted == actual else "WRONG"
    print(f"  {f['rule']:3d}: midpoint_7={f['midpoint_7']}, predicted={predicted}, actual={actual} [{status}]")

# Count accuracy
correct = sum(1 for f in chain_features if f['midpoint_7'] == f['is_chaotic'])
print(f"\nAccuracy: {correct}/{len(chain_features)}")

# Alternative: has_7 AND NOT endpoint_7
print("\n" + "-" * 60)
print("TESTING: has_7 AND (NOT endpoint_7 OR has_0)")
print("-" * 60)

for f in chain_features:
    predicted = f['has_7'] and (not f['endpoint_7'] or f['has_0'])
    actual = f['is_chaotic']
    status = "CORRECT" if predicted == actual else "WRONG"
    print(f"  {f['rule']:3d}: predicted={predicted}, actual={actual} [{status}]")

correct = sum(1 for f in chain_features if (f['has_7'] and (not f['endpoint_7'] or f['has_0'])) == f['is_chaotic'])
print(f"\nAccuracy: {correct}/{len(chain_features)}")

# Let's try: has_7 AND midpoint_7
print("\n" + "-" * 60)
print("TESTING: midpoint_7 = True")
print("-" * 60)

for f in chain_features:
    predicted = f['midpoint_7']
    actual = f['is_chaotic']
    status = "CORRECT" if predicted == actual else "WRONG"
    print(f"  {f['rule']:3d}: midpoint_7={f['midpoint_7']}, actual={actual} [{status}]")

# Actually let me check which SPECIFIC feature separates
print("\n" + "=" * 70)
print("SYSTEMATIC FEATURE SEARCH FOR CHAIN")
print("=" * 70)

chaotic_chain = [f for f in chain_features if f['is_chaotic']]
periodic_chain = [f for f in chain_features if not f['is_chaotic']]

# Check each feature
features_to_test = ['has_0', 'has_7', 'endpoint_0', 'endpoint_7', 'midpoint_0', 'midpoint_7', 'q0', 'q7']

for feat in features_to_test:
    c_true = sum(1 for f in chaotic_chain if f[feat])
    c_false = len(chaotic_chain) - c_true
    p_true = sum(1 for f in periodic_chain if f[feat])
    p_false = len(periodic_chain) - p_true

    # Check if this feature separates
    if (c_true == len(chaotic_chain) and p_true == 0) or (c_false == len(chaotic_chain) and p_false == 0):
        print(f"  {feat}: PERFECT SEPARATOR!")
    print(f"  {feat}: chaotic({c_true}T/{c_false}F), periodic({p_true}T/{p_false}F)")

# Check span value
print("\nSpan analysis:")
for f in chain_features:
    status = "C" if f['is_chaotic'] else "P"
    print(f"  {status} {f['rule']:3d}: span={f['span']:03b}")

# Group by span
from collections import defaultdict
by_span = defaultdict(list)
for f in chain_features:
    by_span[f['span']].append(f)

print("\nBy span:")
for span, features in sorted(by_span.items()):
    chaotic = [f for f in features if f['is_chaotic']]
    periodic = [f for f in features if not f['is_chaotic']]
    print(f"  Span {span:03b}: {len(chaotic)} chaotic, {len(periodic)} periodic")

# Now analyze DIAGONAL_CHAIN
print("\n" + "=" * 70)
print("DIAGONAL_CHAIN RULES")
print("=" * 70)

diag_rules = []
for r in four_ones_max_mixing:
    table = rule_to_table(r)
    zeros = tuple(sorted(i for i in range(8) if table[i] == 0))
    geom = classify_geometry(zeros)
    if geom == "DIAGONAL_CHAIN":
        diag_rules.append((r, zeros, r in CHAOTIC_RULES))

for r, zeros, is_chaotic in diag_rules:
    table = rule_to_table(r)
    status = "CHAOTIC" if is_chaotic else "periodic"

    # Find distance-3 pairs
    dist3 = []
    for i in range(4):
        for j in range(i+1, 4):
            if hamming_distance(zeros[i], zeros[j]) == 3:
                dist3.append((zeros[i], zeros[j]))

    # Check center influence
    center_inf = sum(1 for left in [0, 4] for right in [0, 1]
                    if table[left + right] != table[left + right + 2])

    # Left influence
    left_inf = sum(1 for base in range(4) if table[base] != table[base + 4])

    # Right influence
    right_inf = sum(1 for base in [0, 2, 4, 6] if table[base] != table[base + 1])

    print(f"\n  Rule {r} [{status}]: zeros={zeros}")
    print(f"    dist-3 pairs: {dist3}")
    print(f"    influences: left={left_inf}, center={center_inf}, right={right_inf}")

# The pattern for diagonal chain seems to involve center/left/right influence
print("\n" + "-" * 60)
print("DIAGONAL_CHAIN: Testing influence-based criterion")
print("-" * 60)

for r, zeros, is_chaotic in diag_rules:
    table = rule_to_table(r)

    # Influence values
    center_inf = sum(1 for left in [0, 4] for right in [0, 1]
                    if table[left + right] != table[left + right + 2])
    left_inf = sum(1 for base in range(4) if table[base] != table[base + 4])
    right_inf = sum(1 for base in [0, 2, 4, 6] if table[base] != table[base + 1])

    # Hypothesis: chaotic if left_inf == 0 OR right_inf == 0
    # (completely ignoring one side)
    predicted = (left_inf == 0) or (right_inf == 0)

    status = "CORRECT" if predicted == is_chaotic else "WRONG"
    print(f"  Rule {r}: left={left_inf}, right={right_inf}, predicted={predicted}, actual={is_chaotic} [{status}]")

# Let me check rule-specific patterns
print("\n" + "=" * 70)
print("FINAL COMPLETE CHARACTERIZATION ATTEMPT")
print("=" * 70)

# Based on all the analysis, let me build a complete characterization:
# 1. TETRAHEDRON -> chaotic
# 2. SQUARE -> periodic
# 3. STAR -> periodic
# 4. CHAIN -> chaotic if midpoint_7 == True
# 5. DIAGONAL_CHAIN -> chaotic if specific pattern...

# For DIAGONAL_CHAIN: the chaotic ones are 102 and 153
# Let me compare them directly to periodic ones

print("\nDiagonal chain comparison:")
for r, zeros, is_chaotic in diag_rules:
    table = rule_to_table(r)

    # XOR of zeros
    xor = zeros[0] ^ zeros[1] ^ zeros[2] ^ zeros[3]

    # Sum of zeros
    sum_z = sum(zeros)

    # Specific bit patterns
    bit_pattern = tuple(sorted(bin(z).count('1') for z in zeros))

    status = "C" if is_chaotic else "P"
    print(f"  {status} {r}: zeros={zeros}, sum={sum_z}, bit_counts={bit_pattern}")

# Aha! The sum might be the key
print("\nSum analysis:")
for r, zeros, is_chaotic in diag_rules:
    sum_z = sum(zeros)
    status = "C" if is_chaotic else "P"
    predicted = (sum_z == 14)  # 0+3+4+7=14, 1+2+5+6=14
    print(f"  {status} {r}: sum={sum_z}, predicted={predicted}")

# That doesn't work either. Let me look at specific positions
print("\nPosition analysis:")
for r, zeros, is_chaotic in diag_rules:
    # Check if zeros form a specific pattern
    # 102: (0,3,4,7) - corners where center bit matches left-right XOR
    # 153: (1,2,5,6) - corners where center bit differs from left-right XOR

    # For each position, check: center == left XOR right
    pattern = []
    for z in zeros:
        left = (z >> 2) & 1
        center = (z >> 1) & 1
        right = z & 1
        pattern.append(center == (left ^ right))

    status = "C" if is_chaotic else "P"
    print(f"  {status} {r}: zeros={zeros}, center==L^R: {pattern}")
