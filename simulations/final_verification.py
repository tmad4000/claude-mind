#!/usr/bin/env python3
"""
FINAL VERIFICATION OF COMPLETE CHARACTERIZATION

Based on all analysis:
1. TETRAHEDRON -> always chaotic
2. SQUARE -> never chaotic
3. STAR -> never chaotic
4. CHAIN -> chaotic if (has_7 AND NOT q7) where q7 means table[7]==1
5. DIAGONAL_CHAIN -> chaotic if center==left^right pattern is uniform (all same)

Let's verify 100% accuracy.
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

def predict_chaos(rule):
    """
    Predict if a rule is chaotic based on complete characterization.
    """
    if count_ones(rule) != 4 or count_mixing(rule) != 8:
        return False  # Not in the candidate set

    table = rule_to_table(rule)
    zeros = tuple(sorted(i for i in range(8) if table[i] == 0))
    geom = classify_geometry(zeros)

    if geom == "TETRAHEDRON":
        return True
    elif geom == "SQUARE":
        return False
    elif geom == "STAR":
        return False
    elif geom == "CHAIN":
        has_7 = 7 in zeros
        q7 = table[7] == 1  # Output for 111 is 1
        return has_7 and not q7
    elif geom == "DIAGONAL_CHAIN":
        # Check if center == left XOR right pattern is uniform
        pattern = []
        for z in zeros:
            left = (z >> 2) & 1
            center = (z >> 1) & 1
            right = z & 1
            pattern.append(center == (left ^ right))
        # Uniform means all True or all False
        return len(set(pattern)) == 1
    else:
        return None

# Test on all 4-ones max-mixing rules
four_ones_max_mixing = [r for r in range(256)
                        if count_ones(r) == 4 and count_mixing(r) == 8]

print("=" * 70)
print("FINAL VERIFICATION")
print("=" * 70)

correct = 0
incorrect = 0

results = []
for r in four_ones_max_mixing:
    table = rule_to_table(r)
    zeros = tuple(sorted(i for i in range(8) if table[i] == 0))
    geom = classify_geometry(zeros)

    predicted = predict_chaos(r)
    actual = r in CHAOTIC_RULES

    if predicted == actual:
        status = "✓"
        correct += 1
    else:
        status = "✗ WRONG"
        incorrect += 1

    results.append((r, geom, predicted, actual, status))

for r, geom, predicted, actual, status in results:
    print(f"  Rule {r:3d}: {geom:15s} predicted={predicted}, actual={actual} {status}")

print(f"\n{'='*70}")
print(f"RESULTS: {correct} correct, {incorrect} incorrect")
print(f"ACCURACY: {100*correct/(correct+incorrect):.1f}%")
print(f"{'='*70}")

if incorrect == 0:
    print("\n🎉 PERFECT CLASSIFICATION ACHIEVED!")

    # Summarize the characterization
    print("\n" + "=" * 70)
    print("COMPLETE ALGEBRAIC CHARACTERIZATION OF CHAOTIC ECA RULES")
    print("=" * 70)
    print("""
A rule is CHAOTIC if and only if ALL of the following hold:

1. BALANCED OUTPUT: Exactly 4 ones in binary (rule outputs 4 zeros and 4 ones)

2. MAXIMAL MIXING: 8 cross-transitions in de Bruijn graph
   (0-outputs and 1-outputs are maximally interleaved)

3. GEOMETRIC CRITERION based on zero-set structure:
   a) TETRAHEDRON (all pairs at distance 2): Always chaotic
   b) SQUARE (face of cube): Never chaotic
   c) STAR (one vertex + 3 neighbors): Never chaotic
   d) CHAIN (path through cube): Chaotic iff (7 ∈ zeros AND table[7] = 0)
   e) DIAGONAL_CHAIN (two diagonals): Chaotic iff center-XOR pattern is uniform

The key insight is that chaos requires:
- Balanced output (information preservation)
- Maximal mixing (information spreading)
- Specific geometric structure (no symmetric "escape routes")
""")

# Now let's verify this is EXACTLY the 12 chaotic rules
predicted_chaotic = [r for r in range(256) if predict_chaos(r)]
print(f"\nPredicted chaotic rules: {sorted(predicted_chaotic)}")
print(f"Actual chaotic rules:    {sorted(CHAOTIC_RULES)}")
print(f"Match: {set(predicted_chaotic) == CHAOTIC_RULES}")
