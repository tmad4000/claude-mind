#!/usr/bin/env python3
"""
Search for mathematical constraints that Class IV rules satisfy.

Hypothesis: Class IV rules satisfy some balance condition that
non-Class IV rules don't.
"""

import numpy as np
from itertools import combinations

# All 256 rules as bit vectors
all_rules = np.array([[(r >> i) & 1 for i in range(8)] for r in range(256)])

# Class IV rules (known complex/interesting)
CLASS_IV = [30, 45, 73, 89, 101, 105, 110, 124, 137, 147, 149, 150, 193]

# Class III rules (chaotic)
CLASS_III = [22, 54, 60, 62, 90, 94, 102, 118, 122, 126, 146, 150, 182]

# Class II rules (periodic/simple)
CLASS_II = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 19, 23, 24, 25, 27, 28, 29, 33, 35, 36, 37, 38, 41, 42, 43, 44, 46, 50, 51, 56, 57, 58, 72, 74, 76, 77, 78, 104, 108, 130, 132, 134, 138, 140, 142, 152, 154, 156, 162, 164, 168, 170, 172, 178, 184, 200, 204, 232]

# Class I rules (die out)
CLASS_I = [0, 8, 32, 40, 64, 96, 128, 136, 160, 168, 192, 224]

class4_bits = all_rules[CLASS_IV]
class3_bits = all_rules[CLASS_III]
class2_bits = all_rules[CLASS_II]

print("=" * 70)
print("SEARCHING FOR LINEAR CONSTRAINTS")
print("=" * 70)

# Check if sum of any subset of bits is constant for Class IV
print("\n1. Checking if any bit-sum is constant for Class IV...")

for r in range(1, 9):  # check subsets of size 1-8
    for subset in combinations(range(8), r):
        sums = [sum(bits[list(subset)]) for bits in class4_bits]
        if len(set(sums)) == 1:  # all same!
            print(f"   FOUND: Bits {subset} always sum to {sums[0]} in Class IV")

print("\n2. Checking bit-sum distributions...")

for subset_size in [2, 3, 4]:
    print(f"\n   Subsets of size {subset_size}:")
    for subset in combinations(range(8), subset_size):
        c4_sums = [sum(bits[list(subset)]) for bits in class4_bits]
        c4_mean = np.mean(c4_sums)
        c4_std = np.std(c4_sums)

        c3_sums = [sum(bits[list(subset)]) for bits in class3_bits]
        c3_mean = np.mean(c3_sums)

        c2_sums = [sum(bits[list(subset)]) for bits in class2_bits]
        c2_mean = np.mean(c2_sums)

        # Is Class IV significantly different from others?
        if abs(c4_mean - c3_mean) > 0.5 or abs(c4_mean - c2_mean) > 0.5:
            print(f"   Bits {subset}: C4={c4_mean:.2f}±{c4_std:.2f}, C3={c3_mean:.2f}, C2={c2_mean:.2f}")

print("\n" + "=" * 70)
print("3. CHECKING TOTAL BIT COUNT (Hamming weight)")
print("=" * 70)

c4_weights = [sum(bits) for bits in class4_bits]
c3_weights = [sum(bits) for bits in class3_bits]
c2_weights = [sum(bits) for bits in class2_bits]

print(f"\nClass IV Hamming weights: {c4_weights}")
print(f"  Mean: {np.mean(c4_weights):.2f}, Std: {np.std(c4_weights):.2f}")
print(f"  Range: {min(c4_weights)} - {max(c4_weights)}")

print(f"\nClass III Hamming weights: {c3_weights}")
print(f"  Mean: {np.mean(c3_weights):.2f}")

print(f"\nClass II Hamming weights (sample): {c2_weights[:20]}...")
print(f"  Mean: {np.mean(c2_weights):.2f}")

print(f"\nRandom expectation: 4.0")

print("\n" + "=" * 70)
print("4. CHECKING LEFT-RIGHT SYMMETRY")
print("=" * 70)

# Bits 1 (001) and 4 (100) are symmetric
# Bits 3 (011) and 6 (110) are symmetric
# Bit 2 (010) and 7 (111), 0 (000), 5 (101) are self-symmetric

def get_symmetry_score(bits):
    """How symmetric is the rule under left-right reflection?"""
    # Symmetric pairs: (1,4), (3,6)
    score = 0
    if bits[1] == bits[4]: score += 1
    if bits[3] == bits[6]: score += 1
    return score

c4_sym = [get_symmetry_score(bits) for bits in class4_bits]
c3_sym = [get_symmetry_score(bits) for bits in class3_bits]
c2_sym = [get_symmetry_score(bits) for bits in class2_bits]

print(f"\nSymmetry scores (0-2, higher = more symmetric):")
print(f"  Class IV: {c4_sym}, mean={np.mean(c4_sym):.2f}")
print(f"  Class III: {c3_sym}, mean={np.mean(c3_sym):.2f}")
print(f"  Class II mean: {np.mean(c2_sym):.2f}")

print("\n" + "=" * 70)
print("5. CHECKING 'BALANCE' METRICS")
print("=" * 70)

def birth_potential(bits):
    """How likely is this rule to create new cells?"""
    # Transitions from 0 or 1 live neighbors to 1
    return bits[1] + bits[2] + bits[4]  # 001, 010, 100 → ?

def death_potential(bits):
    """How likely is this rule to kill cells?"""
    # Transitions from many neighbors to 0
    return (1 - bits[3]) + (1 - bits[5]) + (1 - bits[6]) + (1 - bits[7])  # 011,101,110,111 → 0?

def crowding_death(bits):
    """Does the rule kill overcrowded cells?"""
    return 1 - bits[7]  # 111 → 0?

def spread_potential(bits):
    """Can patterns spread? (our replication condition)"""
    return bits[1] + bits[4]  # 001→1 and 100→1

c4_birth = [birth_potential(bits) for bits in class4_bits]
c4_death = [death_potential(bits) for bits in class4_bits]
c4_balance = [birth_potential(bits) - death_potential(bits) for bits in class4_bits]

c3_balance = [birth_potential(bits) - death_potential(bits) for bits in class3_bits]
c2_balance = [birth_potential(bits) - death_potential(bits) for bits in class2_bits]

print(f"\nBirth-Death Balance (birth - death potential):")
print(f"  Class IV: {c4_balance}, mean={np.mean(c4_balance):.2f}")
print(f"  Class III mean: {np.mean(c3_balance):.2f}")
print(f"  Class II mean: {np.mean(c2_balance):.2f}")

c4_spread = [spread_potential(bits) for bits in class4_bits]
c3_spread = [spread_potential(bits) for bits in class3_bits]

print(f"\nSpread potential (001→1 + 100→1):")
print(f"  Class IV: {c4_spread}, mean={np.mean(c4_spread):.2f}")
print(f"  Class III: {c3_spread}, mean={np.mean(c3_spread):.2f}")

print("\n" + "=" * 70)
print("6. TESTING COMPOUND HYPOTHESES")
print("=" * 70)

def hypothesis_score(bits):
    """
    Hypothesis: Class IV rules have:
    - Bidirectional spread (001→1 AND 100→1)
    - No spontaneous birth (000→0)
    - Death from crowding (111→0)
    """
    score = 0
    if bits[1] == 1 and bits[4] == 1:  # bidirectional spread
        score += 1
    if bits[0] == 0:  # no spontaneous birth
        score += 1
    if bits[7] == 0:  # death from crowding
        score += 1
    return score

c4_hyp = [hypothesis_score(bits) for bits in class4_bits]
c3_hyp = [hypothesis_score(bits) for bits in class3_bits]
c2_hyp = [hypothesis_score(bits) for bits in class2_bits]

print(f"\nCompound hypothesis score (0-3):")
print(f"  Class IV: {c4_hyp}, mean={np.mean(c4_hyp):.2f}")
print(f"  Class III: {c3_hyp}, mean={np.mean(c3_hyp):.2f}")
print(f"  Class II mean: {np.mean(c2_hyp):.2f}")

# How many Class IV rules satisfy all 3?
full_match = sum(1 for s in c4_hyp if s == 3)
print(f"\n  Class IV rules with score=3: {full_match}/{len(CLASS_IV)}")

# Which Class IV rules DON'T match?
print("\n  Class IV rules that don't fully match:")
for rule, score in zip(CLASS_IV, c4_hyp):
    if score < 3:
        bits = all_rules[rule]
        violations = []
        if bits[1] != 1 or bits[4] != 1:
            violations.append("no bidirectional spread")
        if bits[0] != 0:
            violations.append("has spontaneous birth")
        if bits[7] != 0:
            violations.append("no crowding death")
        print(f"    Rule {rule} (score={score}): {', '.join(violations)}")

print("\n" + "=" * 70)
print("FINAL INSIGHT")
print("=" * 70)

print("""
Class IV rules are NOT defined by a simple constraint.
They occupy a 'balance region' with these tendencies:
  - Hamming weight near 4 (balanced 0s and 1s)
  - Mixed symmetry (not fully symmetric)
  - Spread potential often = 1 (partial spreading)
  - Death-birth roughly balanced

The isolation is because ANY single-bit change breaks this
delicate balance, pushing toward:
  - Too much death → extinction
  - Too much birth → fills everything
  - Too much chaos → Class III
  - Too much order → Class II
""")
