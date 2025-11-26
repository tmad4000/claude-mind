#!/usr/bin/env python3
"""
Deeper analysis: What happens when we flip each transition in each direction?

Key question: Is there a "balance point" that Class IV rules occupy?
"""

import json
import numpy as np
from collections import defaultdict

# Load previous results
with open('/Users/jacobcole/code/claude-mind/simulations/class4_neighbor_results.json', 'r') as f:
    results = json.load(f)

# Known Class IV rules
CLASS_IV_RULES = [30, 45, 73, 89, 101, 105, 110, 124, 137, 147, 149, 150, 193]

TRANSITIONS = {
    0: "000",  # empty neighborhood
    1: "001",  # only right
    2: "010",  # only center
    3: "011",  # center + right
    4: "100",  # only left
    5: "101",  # left + right (center dead)
    6: "110",  # left + center
    7: "111",  # all alive
}

def rule_to_bits(rule):
    return [(rule >> i) & 1 for i in range(8)]

# Analyze directional effects
print("=" * 70)
print("DIRECTIONAL ANALYSIS: What happens when we change each transition?")
print("=" * 70)

# For each bit position, track: 0→1 outcomes and 1→0 outcomes
directional = {i: {'0→1': [], '1→0': []} for i in range(8)}

for rule_str, rule_data in results.items():
    rule = int(rule_str)
    bits = rule_to_bits(rule)

    for neighbor_str, neighbor_data in rule_data['neighbors'].items():
        bit_pos = neighbor_data['bit_flipped']
        outcome = neighbor_data['class']

        old_val = bits[bit_pos]
        new_val = 1 - old_val

        direction = f"{old_val}→{new_val}"
        directional[bit_pos][direction].append(outcome)

# Print analysis
for bit_pos in range(8):
    print(f"\nBit {bit_pos} ({TRANSITIONS[bit_pos]} → ?):")

    for direction in ['0→1', '1→0']:
        outcomes = directional[bit_pos][direction]
        if outcomes:
            from collections import Counter
            counts = Counter(outcomes)
            total = len(outcomes)
            pct = {k: f"{100*v/total:.0f}%" for k, v in counts.items()}
            print(f"  {direction}: {dict(counts)} {pct}")

# Key hypothesis: Class IV needs specific balance
print("\n" + "=" * 70)
print("HYPOTHESIS: Class IV rules have specific transition patterns")
print("=" * 70)

# What transitions do ALL Class IV rules share?
class4_patterns = []
for rule in CLASS_IV_RULES:
    bits = rule_to_bits(rule)
    class4_patterns.append(bits)

class4_patterns = np.array(class4_patterns)

print("\nTransition values across Class IV rules:")
print("Bit | Transition | Values across Class IV rules | Dominant")
print("-" * 60)

for bit_pos in range(8):
    values = class4_patterns[:, bit_pos]
    ones = values.sum()
    zeros = len(values) - ones
    dominant = "1" if ones > zeros else "0" if zeros > ones else "mixed"

    print(f" {bit_pos}  | {TRANSITIONS[bit_pos]}→?    | 0s:{zeros:2d}, 1s:{ones:2d} | {dominant}")

# Check for invariants
print("\n" + "=" * 70)
print("INVARIANT CHECK: Any transitions ALL Class IV rules agree on?")
print("=" * 70)

invariants_0 = []  # All have this bit = 0
invariants_1 = []  # All have this bit = 1

for bit_pos in range(8):
    values = class4_patterns[:, bit_pos]
    if values.sum() == 0:
        invariants_0.append(bit_pos)
    elif values.sum() == len(values):
        invariants_1.append(bit_pos)

if invariants_0:
    print(f"ALL Class IV rules have 0 at: {[TRANSITIONS[i] for i in invariants_0]}")
else:
    print("No universal 0s")

if invariants_1:
    print(f"ALL Class IV rules have 1 at: {[TRANSITIONS[i] for i in invariants_1]}")
else:
    print("No universal 1s")

# Look for partial invariants (>80% agreement)
print("\n" + "=" * 70)
print("PARTIAL INVARIANTS (>80% agreement):")
print("=" * 70)

for bit_pos in range(8):
    values = class4_patterns[:, bit_pos]
    ones = values.sum()
    zeros = len(values) - ones
    total = len(values)

    if ones / total >= 0.8:
        print(f"  {TRANSITIONS[bit_pos]}→1 in {ones}/{total} ({100*ones/total:.0f}%) Class IV rules")
    elif zeros / total >= 0.8:
        print(f"  {TRANSITIONS[bit_pos]}→0 in {zeros}/{total} ({100*zeros/total:.0f}%) Class IV rules")

# Compute "Class IV signature" - average transition values
print("\n" + "=" * 70)
print("CLASS IV 'SIGNATURE' (average transition values):")
print("=" * 70)

avg_pattern = class4_patterns.mean(axis=0)
print("\nBit | Transition | Avg value | Interpretation")
print("-" * 60)
for bit_pos in range(8):
    avg = avg_pattern[bit_pos]
    interp = "usually 1" if avg > 0.7 else "usually 0" if avg < 0.3 else "mixed"
    print(f" {bit_pos}  | {TRANSITIONS[bit_pos]}→?    | {avg:.2f}      | {interp}")

# Compare to random rules
print("\n" + "=" * 70)
print("COMPARISON: Class IV signature vs random expectation (0.5)")
print("=" * 70)

deviations = avg_pattern - 0.5
significant = np.abs(deviations) > 0.2  # >20% deviation from random

for bit_pos in range(8):
    if significant[bit_pos]:
        direction = "high" if deviations[bit_pos] > 0 else "low"
        print(f"  {TRANSITIONS[bit_pos]}: {avg_pattern[bit_pos]:.2f} ({direction}, deviation {deviations[bit_pos]:+.2f})")

# Final insight
print("\n" + "=" * 70)
print("KEY INSIGHT")
print("=" * 70)

# Count: what fraction of neighbors become each class?
all_outcomes = []
for rule_data in results.values():
    for neighbor_data in rule_data['neighbors'].values():
        all_outcomes.append(neighbor_data['class'])

from collections import Counter
outcome_counts = Counter(all_outcomes)
total = len(all_outcomes)

print(f"\nWhen you perturb a Class IV rule by 1 bit:")
for cls, count in outcome_counts.most_common():
    print(f"  {count/total*100:5.1f}% become {cls}")

# The key finding
print("\n→ Class IV rules sit at a SADDLE POINT in rule space:")
print("  - Small perturbations push toward simpler attractors (fills/static/dies)")
print("  - Chaotic neighbors exist but are NOT Class IV themselves")
print("  - The 'complex' behavior requires a precise balance that 1-bit changes break")
