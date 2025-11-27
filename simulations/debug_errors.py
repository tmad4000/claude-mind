#!/usr/bin/env python3
"""Debug the 4 error cases to find the correct criterion."""

CHAOTIC_RULES = set([30, 45, 75, 86, 89, 101, 102, 105, 106, 150, 153, 154])

def rule_to_table(rule):
    return [(rule >> i) & 1 for i in range(8)]

def hamming_distance(a, b):
    return bin(a ^ b).count('1')

ERROR_RULES = [102, 120, 153, 154]

print("=" * 70)
print("DEBUGGING ERROR CASES")
print("=" * 70)

for r in ERROR_RULES:
    table = rule_to_table(r)
    zeros = tuple(sorted(i for i in range(8) if table[i] == 0))
    is_chaotic = r in CHAOTIC_RULES

    # Distance histogram
    distances = []
    for i in range(4):
        for j in range(i+1, 4):
            distances.append(hamming_distance(zeros[i], zeros[j]))
    hist = (distances.count(1), distances.count(2), distances.count(3))

    # Classify geometry
    if hist == (0, 6, 0):
        geom = "TETRAHEDRON"
    elif hist == (4, 2, 0):
        geom = "SQUARE"
    elif hist == (3, 3, 0):
        geom = "STAR"
    elif hist == (2, 3, 1):
        geom = "CHAIN"
    elif hist == (2, 2, 2):
        geom = "DIAGONAL_CHAIN"
    else:
        geom = "OTHER"

    # Features
    has_7 = 7 in zeros
    q7 = table[7] == 1

    # Center XOR pattern for diagonal chain
    pattern = []
    for z in zeros:
        left = (z >> 2) & 1
        center = (z >> 1) & 1
        right = z & 1
        pattern.append(center == (left ^ right))
    uniform = len(set(pattern)) == 1

    status = "CHAOTIC" if is_chaotic else "periodic"
    print(f"\n  Rule {r} [{status}]:")
    print(f"    Table: {table}")
    print(f"    Zeros: {zeros} = {[f'{z:03b}' for z in zeros]}")
    print(f"    Geometry: {geom} (hist={hist})")
    print(f"    has_7={has_7}, q7={q7}")
    print(f"    Center XOR pattern: {pattern}, uniform={uniform}")

# Let me check what makes 102, 153 chaotic and 120 not
print("\n" + "=" * 70)
print("COMPARING SIMILAR CASES")
print("=" * 70)

# 102 and 153 are DIAGONAL_CHAIN and chaotic
# 60, 90, 165, 195 are DIAGONAL_CHAIN and periodic

# 120 is CHAIN with has_7 and not q7, but is periodic
# while 30, 45, 75, 86, 89, 101, 106 are CHAIN with has_7 and not q7, and ARE chaotic

# 154 is CHAIN but doesn't have 7 in zeros, yet IS chaotic

# Let me look at the complement relationship
print("\nComplement analysis:")
for r in ERROR_RULES:
    comp = 255 - r
    print(f"  Rule {r} <-> {comp}")
    print(f"    {r} is {'' if r in CHAOTIC_RULES else 'not '}chaotic")
    print(f"    {comp} is {'' if comp in CHAOTIC_RULES else 'not '}chaotic")

# Reflection
def reflect(rule):
    table = rule_to_table(rule)
    def reflect_input(i):
        return ((i & 1) << 2) | (i & 2) | ((i >> 2) & 1)
    reflected_table = [table[reflect_input(i)] for i in range(8)]
    return sum(reflected_table[i] << i for i in range(8))

print("\nReflection analysis:")
for r in ERROR_RULES:
    refl = reflect(r)
    print(f"  Rule {r} <-> {refl} (reflect)")
    print(f"    {r} is {'' if r in CHAOTIC_RULES else 'not '}chaotic")
    print(f"    {refl} is {'' if refl in CHAOTIC_RULES else 'not '}chaotic")

# What if we look at the derivative structure?
print("\n" + "=" * 70)
print("DERIVATIVE STRUCTURE ANALYSIS")
print("=" * 70)

for r in [30, 120, 102, 60]:  # Compare chaotic vs periodic in same geometry
    table = rule_to_table(r)
    is_chaotic = r in CHAOTIC_RULES

    # Derivatives
    d_left = [table[i+4] ^ table[i] for i in range(4)]
    d_center = [table[i+2] ^ table[i] for i in [0, 1, 4, 5]]
    d_right = [table[i+1] ^ table[i] for i in [0, 2, 4, 6]]

    status = "C" if is_chaotic else "P"
    print(f"\n  {status} Rule {r}:")
    print(f"    d_left = {d_left}")
    print(f"    d_center = {d_center}")
    print(f"    d_right = {d_right}")

# What's common to ALL chaotic rules?
print("\n" + "=" * 70)
print("COMMON FEATURES OF ALL CHAOTIC RULES")
print("=" * 70)

chaotic_derivatives = []
for r in CHAOTIC_RULES:
    table = rule_to_table(r)
    d_left = tuple(table[i+4] ^ table[i] for i in range(4))
    d_center = tuple(table[i+2] ^ table[i] for i in [0, 1, 4, 5])
    d_right = tuple(table[i+1] ^ table[i] for i in [0, 2, 4, 6])
    chaotic_derivatives.append((r, d_left, d_center, d_right))

# Check if any derivative is all-1s (full influence)
print("\nDerivatives with all 1s:")
for r, dl, dc, dr in chaotic_derivatives:
    all1_left = dl == (1,1,1,1)
    all1_center = dc == (1,1,1,1)
    all1_right = dr == (1,1,1,1)
    print(f"  Rule {r}: left_all1={all1_left}, center_all1={all1_center}, right_all1={all1_right}")

# Check for the ERROR RULES
print("\nError rules derivatives:")
for r in ERROR_RULES:
    table = rule_to_table(r)
    d_left = tuple(table[i+4] ^ table[i] for i in range(4))
    d_center = tuple(table[i+2] ^ table[i] for i in [0, 1, 4, 5])
    d_right = tuple(table[i+1] ^ table[i] for i in [0, 2, 4, 6])
    is_chaotic = r in CHAOTIC_RULES
    all1_right = dr == (1,1,1,1)

    status = "C" if is_chaotic else "P"
    print(f"  {status} Rule {r}: d_left={d_left}, d_center={d_center}, d_right={d_right}")
