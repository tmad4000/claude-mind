#!/usr/bin/env python3
"""
FINAL THEORY SYNTHESIS: Why does 4-ones create chaos?

Summary of findings:
1. All chaotic rules have exactly 4 ones (balanced output)
2. All chaotic rules have maximal mixing (8 cross-transitions in de Bruijn graph)
3. Neither complement nor reflection uniformly preserves chaos
4. The distinguishing factor seems related to quiescent states

Hypothesis: The combination of:
- 4 ones (balanced output)
- Maximal mixing (8)
- Specific quiescent state pattern
determines chaos.

Let's find the EXACT characterization.
"""

CHAOTIC_RULES = set([30, 45, 75, 86, 89, 101, 102, 105, 106, 150, 153, 154])

def rule_to_table(rule):
    return [(rule >> i) & 1 for i in range(8)]

def count_ones(rule):
    return bin(rule).count('1')

def count_mixing(rule):
    """Count cross-transitions in de Bruijn graph."""
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

# Get all rules with 4 ones and maximal mixing
four_ones_max_mixing = [r for r in range(256)
                        if count_ones(r) == 4 and count_mixing(r) == 8]

print(f"Rules with 4 ones and maximal mixing: {len(four_ones_max_mixing)}")
print(f"Chaotic among them: {len([r for r in four_ones_max_mixing if r in CHAOTIC_RULES])}")

# For each rule, compute key features
def compute_features(rule):
    table = rule_to_table(rule)

    # Quiescent states
    q0 = table[0] == 0  # 000 -> 0
    q7 = table[7] == 1  # 111 -> 1

    # Zero set structure
    zeros = tuple(sorted(i for i in range(8) if table[i] == 0))

    # Does the zero set include both 0 and 7?
    has_0 = 0 in zeros
    has_7 = 7 in zeros

    # Flow asymmetry
    left_inf = sum(1 for base in range(4) if table[base] != table[base + 4])
    right_inf = sum(1 for base in [0, 2, 4, 6] if table[base] != table[base + 1])
    asymmetry = left_inf - right_inf

    # Center influence
    center_inf = 0
    for left in [0, 4]:
        for right in [0, 1]:
            base = left + right
            if table[base] != table[base + 2]:
                center_inf += 1

    return {
        'rule': rule,
        'q0': q0,
        'q7': q7,
        'both_quiescent': q0 and q7,
        'neither_quiescent': not q0 and not q7,
        'zeros': zeros,
        'has_0': has_0,
        'has_7': has_7,
        'asymmetry': asymmetry,
        'center_inf': center_inf,
        'left_inf': left_inf,
        'right_inf': right_inf,
    }

# Analyze all rules
all_features = [compute_features(r) for r in four_ones_max_mixing]

# Look for the distinguishing pattern
print("\n" + "=" * 70)
print("QUIESCENT STATE ANALYSIS")
print("=" * 70)

# Group by quiescent pattern
from collections import defaultdict
by_quiescent = defaultdict(list)
for f in all_features:
    pattern = (f['q0'], f['q7'])
    by_quiescent[pattern].append(f)

for pattern, features in sorted(by_quiescent.items()):
    chaotic = [f for f in features if f['rule'] in CHAOTIC_RULES]
    periodic = [f for f in features if f['rule'] not in CHAOTIC_RULES]
    print(f"\nQuiescent (000->0={pattern[0]}, 111->1={pattern[1]}):")
    print(f"  Total: {len(features)}, Chaotic: {len(chaotic)}, Periodic: {len(periodic)}")
    if chaotic:
        print(f"  Chaotic rules: {sorted([f['rule'] for f in chaotic])}")
    if periodic:
        print(f"  Periodic rules: {sorted([f['rule'] for f in periodic])}")

# NEW INSIGHT: Check has_0 and has_7 separately
print("\n" + "=" * 70)
print("ZERO SET STRUCTURE (has 0 and 7)")
print("=" * 70)

by_zero_structure = defaultdict(list)
for f in all_features:
    pattern = (f['has_0'], f['has_7'])
    by_zero_structure[pattern].append(f)

for pattern, features in sorted(by_zero_structure.items()):
    chaotic = [f for f in features if f['rule'] in CHAOTIC_RULES]
    periodic = [f for f in features if f['rule'] not in CHAOTIC_RULES]
    print(f"\nZeros include 0={pattern[0]}, 7={pattern[1]}:")
    print(f"  Total: {len(features)}, Chaotic: {len(chaotic)}, Periodic: {len(periodic)}")
    if chaotic:
        print(f"  Chaotic rules: {sorted([f['rule'] for f in chaotic])}")
    if periodic:
        print(f"  Periodic rules: {sorted([f['rule'] for f in periodic])}")

# Key insight: look at XOR of has_0 and has_7
print("\n" + "=" * 70)
print("THE KEY: has_0 XOR has_7")
print("=" * 70)

for f in all_features:
    xor_07 = f['has_0'] != f['has_7']  # XOR
    is_chaotic = f['rule'] in CHAOTIC_RULES
    status = "C" if is_chaotic else "P"
    print(f"  {status} Rule {f['rule']:3d}: has_0={f['has_0']}, has_7={f['has_7']}, XOR={xor_07}")

# Count
xor_true = [f for f in all_features if (f['has_0'] != f['has_7'])]
xor_false = [f for f in all_features if not (f['has_0'] != f['has_7'])]

print(f"\nhas_0 XOR has_7 = True: {len(xor_true)} rules")
print(f"  Chaotic: {len([f for f in xor_true if f['rule'] in CHAOTIC_RULES])}")
print(f"  Periodic: {len([f for f in xor_true if f['rule'] not in CHAOTIC_RULES])}")

print(f"\nhas_0 XOR has_7 = False: {len(xor_false)} rules")
print(f"  Chaotic: {len([f for f in xor_false if f['rule'] in CHAOTIC_RULES])}")
print(f"  Periodic: {len([f for f in xor_false if f['rule'] not in CHAOTIC_RULES])}")

# Maybe it's about q0 XOR q7?
print("\n" + "=" * 70)
print("THE KEY: q0 XOR q7 (output-based)")
print("=" * 70)

for f in all_features:
    xor_q = f['q0'] != f['q7']  # XOR
    is_chaotic = f['rule'] in CHAOTIC_RULES
    status = "C" if is_chaotic else "P"
    print(f"  {status} Rule {f['rule']:3d}: q0={f['q0']}, q7={f['q7']}, XOR={xor_q}")

xor_q_true = [f for f in all_features if (f['q0'] != f['q7'])]
xor_q_false = [f for f in all_features if not (f['q0'] != f['q7'])]

print(f"\nq0 XOR q7 = True: {len(xor_q_true)} rules")
print(f"  Chaotic: {len([f for f in xor_q_true if f['rule'] in CHAOTIC_RULES])}")
print(f"  Periodic: {len([f for f in xor_q_true if f['rule'] not in CHAOTIC_RULES])}")

print(f"\nq0 XOR q7 = False: {len(xor_q_false)} rules")
print(f"  Chaotic: {len([f for f in xor_q_false if f['rule'] in CHAOTIC_RULES])}")
print(f"  Periodic: {len([f for f in xor_q_false if f['rule'] not in CHAOTIC_RULES])}")

# FINAL SYNTHESIS
print("\n" + "=" * 70)
print("FINAL SYNTHESIS")
print("=" * 70)

# Based on session 4's characterization, let's verify
# The criterion was: 4-ones + NOT(both quiescent) + d3==1 + transition pattern

# d3 = difference at position 3 (binary 011 vs 111)
# or more generally, the derivative structure

def d_criterion(rule):
    """Previous session's d3 criterion."""
    table = rule_to_table(rule)
    return table[3] != table[7]  # Does output differ for 011 vs 111?

# Check d3 separation
print("\nd3 criterion (output differs for 011 vs 111):")
d3_true = [f for f in all_features if d_criterion(f['rule'])]
d3_false = [f for f in all_features if not d_criterion(f['rule'])]

print(f"d3 = True: {len(d3_true)} rules")
print(f"  Chaotic: {len([f for f in d3_true if f['rule'] in CHAOTIC_RULES])}")

print(f"d3 = False: {len(d3_false)} rules")
print(f"  Chaotic: {len([f for f in d3_false if f['rule'] in CHAOTIC_RULES])}")

# Combined criterion
print("\n" + "=" * 70)
print("COMBINED CRITERION TEST")
print("=" * 70)

# Test: 4-ones + maximal mixing + (q0 XOR q7)
# This should separate chaotic from periodic

def final_criterion(rule):
    f = compute_features(rule)
    return count_ones(rule) == 4 and count_mixing(rule) == 8 and (f['q0'] != f['q7'])

passes = [r for r in range(256) if final_criterion(r)]
print(f"\nRules passing (4-ones + max-mixing + q0 XOR q7): {len(passes)}")
print(f"Chaotic: {len([r for r in passes if r in CHAOTIC_RULES])}")
print(f"Periodic: {len([r for r in passes if r not in CHAOTIC_RULES])}")
print(f"Rules: {sorted(passes)}")

# Check what we're missing
missed_chaotic = [r for r in CHAOTIC_RULES if r not in passes]
false_positives = [r for r in passes if r not in CHAOTIC_RULES]
print(f"\nMissed chaotic: {missed_chaotic}")
print(f"False positives: {false_positives}")

# For the missed ones, what's their quiescent pattern?
for r in missed_chaotic:
    f = compute_features(r)
    print(f"  Rule {r}: q0={f['q0']}, q7={f['q7']}")

print("\n" + "=" * 70)
print("UNDERSTANDING THE EXCEPTIONS")
print("=" * 70)

# Rules 105, 150, 154 have both quiescent states but are still chaotic
# What makes them special?

special_chaotic = [r for r in CHAOTIC_RULES if compute_features(r)['both_quiescent']]
print(f"\nChaotic rules with BOTH quiescent states: {special_chaotic}")

for r in special_chaotic:
    f = compute_features(r)
    table = rule_to_table(r)
    print(f"\n  Rule {r}:")
    print(f"    Table: {table}")
    print(f"    Zeros: {f['zeros']}")
    print(f"    Asymmetry: {f['asymmetry']}")
    print(f"    Center influence: {f['center_inf']}")

# What distinguishes 150, 154 from 166, 170, 180, etc.?
both_quiescent = [f for f in all_features if f['both_quiescent']]
print(f"\nAll rules with both quiescent: {len(both_quiescent)}")
for f in both_quiescent:
    is_chaotic = f['rule'] in CHAOTIC_RULES
    status = "C" if is_chaotic else "P"
    print(f"  {status} Rule {f['rule']:3d}: zeros={f['zeros']}, asym={f['asymmetry']}, center={f['center_inf']}")
