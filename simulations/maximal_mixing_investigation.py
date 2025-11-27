#!/usr/bin/env python3
"""
CRITICAL FINDING: Chaotic rules have MAXIMAL MIXING (8 cross-transitions)

There are 34 rules with:
- 4 ones (balanced output)
- (4,4) connectivity = 8 mixing transitions (maximal)

Only 12 of these are chaotic. What distinguishes them?
"""

import numpy as np
from collections import defaultdict
from itertools import combinations

# The 12 chaotic rules
CHAOTIC_RULES = set([30, 45, 75, 86, 89, 101, 102, 105, 106, 150, 153, 154])

def rule_to_table(rule):
    return [(rule >> i) & 1 for i in range(8)]

def count_ones(rule):
    return bin(rule).count('1')

def get_zero_set(rule):
    """Return the set of inputs that map to 0."""
    table = rule_to_table(rule)
    return frozenset(i for i in range(8) if table[i] == 0)

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

# Find all rules with 4 ones and maximal mixing
four_ones = [r for r in range(256) if count_ones(r) == 4]
max_mixing = [r for r in four_ones if count_mixing(r) == 8]

print(f"Rules with 4 ones and maximal mixing (8): {len(max_mixing)}")
print(f"Chaotic: {sorted([r for r in max_mixing if r in CHAOTIC_RULES])}")
print(f"Non-chaotic: {sorted([r for r in max_mixing if r not in CHAOTIC_RULES])}")

# Analyze the zero-sets
print("\n" + "=" * 70)
print("ZERO-SET ANALYSIS")
print("=" * 70)

chaotic_zero_sets = [get_zero_set(r) for r in max_mixing if r in CHAOTIC_RULES]
nonchaotic_zero_sets = [get_zero_set(r) for r in max_mixing if r not in CHAOTIC_RULES]

print(f"\nChaotic zero-sets:")
for r in sorted([x for x in max_mixing if x in CHAOTIC_RULES]):
    zs = get_zero_set(r)
    print(f"  Rule {r:3d}: {sorted(zs)} = {[f'{i:03b}' for i in sorted(zs)]}")

print(f"\nNon-chaotic zero-sets:")
for r in sorted([x for x in max_mixing if x not in CHAOTIC_RULES]):
    zs = get_zero_set(r)
    print(f"  Rule {r:3d}: {sorted(zs)} = {[f'{i:03b}' for i in sorted(zs)]}")

# Check if 0 (000) and 7 (111) are in the zero set
print("\n" + "=" * 70)
print("QUIESCENT STATE ANALYSIS")
print("=" * 70)

print("\nDoes 000->0 (quiescent zeros)?")
for r in sorted(max_mixing):
    table = rule_to_table(r)
    has_000_quiescent = table[0] == 0
    is_chaotic = r in CHAOTIC_RULES
    status = "CHAOTIC" if is_chaotic else "periodic"
    print(f"  Rule {r:3d} [{status}]: 000->0 = {has_000_quiescent}, 111->1 = {table[7] == 1}")

# Count quiescent patterns
print("\nQuiescent pattern distribution:")
patterns = defaultdict(lambda: {'chaotic': [], 'periodic': []})
for r in max_mixing:
    table = rule_to_table(r)
    pattern = (table[0] == 0, table[7] == 1)
    key = 'chaotic' if r in CHAOTIC_RULES else 'periodic'
    patterns[pattern][key].append(r)

for pattern, groups in sorted(patterns.items()):
    print(f"  (000->0={pattern[0]}, 111->1={pattern[1]}): chaotic={len(groups['chaotic'])}, periodic={len(groups['periodic'])}")

# Deep dive: what else distinguishes them?
print("\n" + "=" * 70)
print("DEEP DISTINGUISHING ANALYSIS")
print("=" * 70)

def analyze_rule_deeply(rule):
    table = rule_to_table(rule)

    # Symmetry under complement: rule(~x) = ~rule(x)?
    # Complement of rule n is 255-n
    complement = 255 - rule
    is_self_complement = rule == complement

    # Left-right reflection
    def reflect(i):
        # Swap bits: 4->1, 1->4, keep 2
        return ((i & 1) << 2) | (i & 2) | ((i >> 2) & 1)

    reflected_table = [table[reflect(i)] for i in range(8)]
    reflected_rule = sum(reflected_table[i] << i for i in range(8))

    # Totalistic component: output depends on count of 1s?
    counts_to_output = defaultdict(set)
    for i in range(8):
        count = bin(i).count('1')
        counts_to_output[count].add(table[i])

    is_totalistic = all(len(v) == 1 for v in counts_to_output.values())

    # Outer totalistic: output depends on center + outer sum?
    # Input i = (left, center, right)
    outer_to_output = defaultdict(set)
    for i in range(8):
        center = (i >> 1) & 1
        outer_sum = ((i >> 2) & 1) + (i & 1)
        outer_to_output[(center, outer_sum)].add(table[i])

    is_outer_totalistic = all(len(v) == 1 for v in outer_to_output.values())

    # Additive degree
    # Check if it's XOR of some subset of inputs
    def is_additive():
        for mask in range(8):
            matches = all(table[i] == (bin(i & mask).count('1') % 2) for i in range(8))
            if matches:
                return mask
        return None

    # Check center-dependency
    # Does flipping center always flip output?
    center_flip_changes = 0
    for i in range(4):  # Iterate over (left, right) combinations
        left, right = (i >> 1) & 1, i & 1
        input_0 = left * 4 + 0 * 2 + right
        input_1 = left * 4 + 1 * 2 + right
        if table[input_0] != table[input_1]:
            center_flip_changes += 1

    return {
        'rule': rule,
        'complement': complement,
        'self_complement': is_self_complement,
        'reflected_rule': reflected_rule,
        'is_totalistic': is_totalistic,
        'is_outer_totalistic': is_outer_totalistic,
        'additive_mask': is_additive(),
        'center_dependency': center_flip_changes,  # 0-4
    }

print("\nDetailed analysis:")
for r in sorted(max_mixing):
    analysis = analyze_rule_deeply(r)
    is_chaotic = r in CHAOTIC_RULES
    status = "CHAOTIC" if is_chaotic else "periodic"
    print(f"\n  Rule {r:3d} [{status}]:")
    print(f"    Complement: {analysis['complement']}, self-complement: {analysis['self_complement']}")
    print(f"    Reflected: {analysis['reflected_rule']}")
    print(f"    Totalistic: {analysis['is_totalistic']}, Outer-totalistic: {analysis['is_outer_totalistic']}")
    print(f"    Additive mask: {analysis['additive_mask']}")
    print(f"    Center dependency: {analysis['center_dependency']}/4")

# Summary of potential distinguishing features
print("\n" + "=" * 70)
print("SUMMARY: POTENTIAL DISTINGUISHING FEATURES")
print("=" * 70)

features = []
for r in max_mixing:
    a = analyze_rule_deeply(r)
    table = rule_to_table(r)
    features.append({
        'rule': r,
        'is_chaotic': r in CHAOTIC_RULES,
        'quiescent_00': table[0] == 0,
        'quiescent_11': table[7] == 1,
        'totalistic': a['is_totalistic'],
        'outer_totalistic': a['is_outer_totalistic'],
        'additive': a['additive_mask'] is not None,
        'center_dep': a['center_dependency'],
    })

# Check each feature
print("\nFeature analysis:")
for feat_name in ['quiescent_00', 'quiescent_11', 'totalistic', 'outer_totalistic', 'additive', 'center_dep']:
    chaotic_vals = [f[feat_name] for f in features if f['is_chaotic']]
    periodic_vals = [f[feat_name] for f in features if not f['is_chaotic']]

    if isinstance(chaotic_vals[0], bool):
        c_true = sum(chaotic_vals)
        p_true = sum(periodic_vals)
        print(f"  {feat_name}: chaotic={c_true}/{len(chaotic_vals)} True, periodic={p_true}/{len(periodic_vals)} True")
    else:
        print(f"  {feat_name}: chaotic={set(chaotic_vals)}, periodic={set(periodic_vals)}")

# Find the combination that works
print("\n" + "=" * 70)
print("FINDING THE EXACT COMBINATION")
print("=" * 70)

# Based on previous session's finding: NOT(111->1,000->0) is key
# Let's verify and understand WHY
for f in features:
    both_quiescent = f['quiescent_00'] and f['quiescent_11']
    neither_quiescent = not f['quiescent_00'] and not f['quiescent_11']

    status = "CHAOTIC" if f['is_chaotic'] else "periodic"
    if f['is_chaotic']:
        print(f"  Rule {f['rule']:3d} [{status}]: both_quiescent={both_quiescent}, neither={neither_quiescent}")

print("\nNon-chaotic rules in max-mixing set:")
for f in features:
    if not f['is_chaotic']:
        both_quiescent = f['quiescent_00'] and f['quiescent_11']
        neither_quiescent = not f['quiescent_00'] and not f['quiescent_11']
        print(f"  Rule {f['rule']:3d}: both_quiescent={both_quiescent}, neither={neither_quiescent}, center_dep={f['center_dep']}")

# THE KEY INSIGHT
print("\n" + "=" * 70)
print("THE KEY INSIGHT")
print("=" * 70)

# From session 4: The rule shouldn't have BOTH quiescent states
# Check if this alone is sufficient among max-mixing rules

without_both_quiescent = [f for f in features if not (f['quiescent_00'] and f['quiescent_11'])]
print(f"\nMax-mixing rules WITHOUT both quiescent states: {len(without_both_quiescent)}")
print(f"  Chaotic: {len([f for f in without_both_quiescent if f['is_chaotic']])}")
print(f"  Periodic: {len([f for f in without_both_quiescent if not f['is_chaotic']])}")

# What distinguishes the remaining non-chaotic ones?
remaining_periodic = [f for f in without_both_quiescent if not f['is_chaotic']]
print(f"\nRemaining periodic rules (need additional criteria):")
for f in remaining_periodic:
    table = rule_to_table(f['rule'])
    print(f"  Rule {f['rule']:3d}: table={table}, center_dep={f['center_dep']}")
