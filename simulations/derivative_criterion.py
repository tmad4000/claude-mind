#!/usr/bin/env python3
"""
TESTING DERIVATIVE CRITERION

Hypothesis: A rule is chaotic iff (d_left = all 1s) OR (d_right = all 1s)
This means at least one side bit has FULL influence on output.
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

def get_derivatives(rule):
    table = rule_to_table(rule)
    d_left = tuple(table[i+4] ^ table[i] for i in range(4))
    d_center = tuple(table[i+2] ^ table[i] for i in [0, 1, 4, 5])
    d_right = tuple(table[i+1] ^ table[i] for i in [0, 2, 4, 6])
    return d_left, d_center, d_right

def predict_chaos_derivative(rule):
    """Predict chaos based on derivative criterion."""
    if count_ones(rule) != 4 or count_mixing(rule) != 8:
        return False

    d_left, d_center, d_right = get_derivatives(rule)

    # Criterion: at least one side has full influence
    left_full = d_left == (1, 1, 1, 1)
    right_full = d_right == (1, 1, 1, 1)

    return left_full or right_full

# Test on all 4-ones max-mixing rules
four_ones_max_mixing = [r for r in range(256)
                        if count_ones(r) == 4 and count_mixing(r) == 8]

print("=" * 70)
print("TESTING DERIVATIVE CRITERION")
print("=" * 70)

correct = 0
incorrect = 0

for r in four_ones_max_mixing:
    d_left, d_center, d_right = get_derivatives(r)
    predicted = predict_chaos_derivative(r)
    actual = r in CHAOTIC_RULES

    left_full = d_left == (1, 1, 1, 1)
    right_full = d_right == (1, 1, 1, 1)

    if predicted == actual:
        status = "✓"
        correct += 1
    else:
        status = "✗ WRONG"
        incorrect += 1

    print(f"  Rule {r:3d}: L_full={left_full}, R_full={right_full}, pred={predicted}, actual={actual} {status}")

print(f"\n{'='*70}")
print(f"RESULTS: {correct} correct, {incorrect} incorrect")
print(f"ACCURACY: {100*correct/(correct+incorrect):.1f}%")
print(f"{'='*70}")

if incorrect == 0:
    print("\n🎉 PERFECT CLASSIFICATION ACHIEVED!")

    # Verify we get exactly the chaotic rules
    predicted_chaotic = [r for r in range(256) if predict_chaos_derivative(r)]
    print(f"\nPredicted chaotic rules: {sorted(predicted_chaotic)}")
    print(f"Actual chaotic rules:    {sorted(CHAOTIC_RULES)}")
    print(f"Match: {set(predicted_chaotic) == CHAOTIC_RULES}")

    # Summarize
    print("\n" + "=" * 70)
    print("COMPLETE CHARACTERIZATION OF CHAOTIC ECA RULES")
    print("=" * 70)
    print("""
A rule is CHAOTIC if and only if ALL of the following hold:

1. BALANCED OUTPUT: Exactly 4 ones in binary representation

2. MAXIMAL MIXING: 8 cross-transitions in de Bruijn graph

3. DIRECTIONAL INFLUENCE: At least one of d_left or d_right equals (1,1,1,1)
   - d_left[i] = table[i+4] XOR table[i] for i in 0..3
   - d_right[i] = table[i+1] XOR table[i] for i in 0,2,4,6
   - (1,1,1,1) means that bit ALWAYS affects output

PHYSICAL INTERPRETATION:
- Balanced output preserves information
- Maximal mixing spreads information across the lattice
- Directional influence ensures information flows through the system
  without "escape routes" where changes get absorbed

The key insight is that chaos requires UNIDIRECTIONAL information flow:
- Either left-to-right OR right-to-left must be perfectly efficient
- If both directions have partial influence, periodicity can emerge
""")

# But wait - let me also check if this simplifies to something more elegant
print("\n" + "=" * 70)
print("SIMPLIFICATION CHECK")
print("=" * 70)

# Is the criterion equivalent to: left_influence = 4 OR right_influence = 4?
# (since d_X = (1,1,1,1) means X_influence = 4)

for r in four_ones_max_mixing:
    table = rule_to_table(r)
    d_left, d_center, d_right = get_derivatives(r)

    left_inf = sum(d_left)
    right_inf = sum(d_right)

    left_full = left_inf == 4
    right_full = right_inf == 4

    predicted = left_full or right_full
    actual = r in CHAOTIC_RULES

    if predicted != actual:
        print(f"  MISMATCH: Rule {r} - L={left_inf}, R={right_inf}, pred={predicted}, actual={actual}")

print("  (No output = all match)")
