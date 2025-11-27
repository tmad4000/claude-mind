#!/usr/bin/env python3
"""
VERIFYING THE GEOMETRIC CRITERION FOR CHAOS

Based on the analysis:
1. TETRAHEDRON → always chaotic
2. SQUARE, STAR → never chaotic
3. CHAIN → chaotic if and only if 7 is in zeros
4. DIAGONAL_CHAIN → need to determine the rule

Let's verify this gives 100% accuracy.
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

    hist = {1: distances.count(1), 2: distances.count(2), 3: distances.count(3)}

    if hist == {1: 0, 2: 6, 3: 0}:
        return "TETRAHEDRON"
    elif hist == {1: 4, 2: 2, 3: 0}:
        return "SQUARE"
    elif hist == {1: 3, 2: 3, 3: 0}:
        return "STAR"
    elif hist == {1: 2, 2: 3, 3: 1}:
        return "CHAIN"
    elif hist == {1: 2, 2: 2, 3: 2}:
        return "DIAGONAL_CHAIN"
    else:
        return f"OTHER({hist})"

def predict_chaos_geometric(rule):
    """
    Predict if a rule is chaotic based on geometric analysis.
    """
    table = rule_to_table(rule)
    zeros = tuple(sorted(i for i in range(8) if table[i] == 0))
    geom = classify_geometry(zeros)

    has_7 = 7 in zeros  # Is 111 in the zero set?
    has_0 = 0 in zeros  # Is 000 in the zero set?

    if geom == "TETRAHEDRON":
        return True  # Always chaotic
    elif geom in ["SQUARE", "STAR"]:
        return False  # Never chaotic
    elif geom == "CHAIN":
        # Hypothesis: chaotic if 7 is in zeros
        return has_7
    elif geom == "DIAGONAL_CHAIN":
        # Need to figure out the pattern
        # Looking at the data:
        # C 102: zeros=(0, 3, 4, 7) - has both 0 and 7
        # C 153: zeros=(1, 2, 5, 6) - has neither 0 nor 7
        # P 60: zeros=(0, 1, 6, 7) - has both
        # P 90: zeros=(0, 2, 5, 7) - has both
        # P 165: zeros=(1, 3, 4, 6) - has neither
        # P 195: zeros=(2, 3, 4, 5) - has neither

        # So it's not just about 0 and 7...
        # Let me look at specific patterns
        return None  # Unknown for now
    else:
        return None

# Test on all 4-ones max-mixing rules
four_ones_max_mixing = [r for r in range(256)
                        if count_ones(r) == 4 and count_mixing(r) == 8]

print("=" * 70)
print("TESTING GEOMETRIC PREDICTION")
print("=" * 70)

correct = 0
incorrect = 0
unknown = 0

for r in four_ones_max_mixing:
    table = rule_to_table(r)
    zeros = tuple(sorted(i for i in range(8) if table[i] == 0))
    geom = classify_geometry(zeros)

    predicted = predict_chaos_geometric(r)
    actual = r in CHAOTIC_RULES

    if predicted is None:
        status = "UNKNOWN"
        unknown += 1
    elif predicted == actual:
        status = "CORRECT"
        correct += 1
    else:
        status = "WRONG"
        incorrect += 1

    print(f"  Rule {r:3d}: {geom:15s} predicted={predicted}, actual={actual} [{status}]")

print(f"\nResults: {correct} correct, {incorrect} incorrect, {unknown} unknown")
print(f"Accuracy (excluding unknown): {100*correct/(correct+incorrect):.1f}%")

# Now let's figure out DIAGONAL_CHAIN
print("\n" + "=" * 70)
print("ANALYZING DIAGONAL_CHAIN")
print("=" * 70)

diagonal_chain_rules = []
for r in four_ones_max_mixing:
    table = rule_to_table(r)
    zeros = tuple(sorted(i for i in range(8) if table[i] == 0))
    geom = classify_geometry(zeros)
    if geom == "DIAGONAL_CHAIN":
        diagonal_chain_rules.append((r, zeros))

for r, zeros in diagonal_chain_rules:
    table = rule_to_table(r)
    is_chaotic = r in CHAOTIC_RULES
    status = "CHAOTIC" if is_chaotic else "periodic"

    # Various features
    has_0 = 0 in zeros
    has_7 = 7 in zeros
    has_both = has_0 and has_7
    has_neither = not has_0 and not has_7

    # Parity analysis
    zeros_parity = [bin(z).count('1') % 2 for z in zeros]
    even_count = zeros_parity.count(0)
    odd_count = zeros_parity.count(1)

    # XOR of all zeros
    xor_all = zeros[0] ^ zeros[1] ^ zeros[2] ^ zeros[3]

    print(f"\n  Rule {r} [{status}]: zeros={zeros} = {[f'{z:03b}' for z in zeros]}")
    print(f"    has_0={has_0}, has_7={has_7}, both={has_both}, neither={has_neither}")
    print(f"    Parity: {even_count} even, {odd_count} odd")
    print(f"    XOR of all: {xor_all:03b}")

# Look for the pattern
print("\n" + "=" * 70)
print("DIAGONAL_CHAIN PATTERN SEARCH")
print("=" * 70)

# The chaotic ones are 102 and 153
# 102: zeros=(0, 3, 4, 7) - XOR = 0^3^4^7 = 0
# 153: zeros=(1, 2, 5, 6) - XOR = 1^2^5^6 = 0

# The periodic ones are 60, 90, 165, 195
# 60: zeros=(0, 1, 6, 7) - XOR = 0
# 90: zeros=(0, 2, 5, 7) - XOR = 0
# 165: zeros=(1, 3, 4, 6) - XOR = 0
# 195: zeros=(2, 3, 4, 5) - XOR = 0

# So XOR doesn't separate them...

# Let's look at the specific pairs
print("\nDetailed pair analysis:")
for r, zeros in diagonal_chain_rules:
    is_chaotic = r in CHAOTIC_RULES

    # Find which pairs are at distance 3
    dist3_pairs = []
    for i in range(4):
        for j in range(i+1, 4):
            if hamming_distance(zeros[i], zeros[j]) == 3:
                dist3_pairs.append((zeros[i], zeros[j]))

    print(f"  Rule {r} [{'C' if is_chaotic else 'P'}]: distance-3 pairs = {dist3_pairs}")

    # Are the distance-3 pairs (0,7)?
    has_07_pair = (0, 7) in dist3_pairs or (7, 0) in dist3_pairs
    print(f"    Contains (0,7) pair: {has_07_pair}")

# Check hypothesis: chaotic if distance-3 pair is NOT (0,7)
print("\n" + "=" * 70)
print("HYPOTHESIS: Chaotic if dist-3 pair is not (0,7)")
print("=" * 70)

for r, zeros in diagonal_chain_rules:
    is_chaotic = r in CHAOTIC_RULES
    dist3_pairs = []
    for i in range(4):
        for j in range(i+1, 4):
            if hamming_distance(zeros[i], zeros[j]) == 3:
                dist3_pairs.append((zeros[i], zeros[j]))

    has_07_pair = any((0 in p and 7 in p) for p in dist3_pairs)
    predicted = not has_07_pair  # Chaotic if NOT (0,7)

    status = "CORRECT" if predicted == is_chaotic else "WRONG"
    print(f"  Rule {r}: has_07_pair={has_07_pair}, predicted_chaotic={predicted}, actual={is_chaotic} [{status}]")
