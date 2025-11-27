#!/usr/bin/env python3
"""
Complete characterization of chaotic ECA rules.

We need the FULL 8-bit pattern, not just the middle 6 bits.
Let me analyze more carefully.
"""

from collections import Counter

KNOWN_CHAOTIC = set([30, 45, 75, 86, 89, 101, 106, 120, 135, 149, 169, 225])

def rule_to_binary(rule_num):
    return format(rule_num, '08b')

def rule_to_table(rule_num):
    binary = rule_to_binary(rule_num)
    neighborhoods = ['111', '110', '101', '100', '011', '010', '001', '000']
    return {nb: int(binary[i]) for i, nb in enumerate(neighborhoods)}

def count_ones(rule_num):
    return bin(rule_num).count('1')

def complement(rule_num):
    return 255 - rule_num

def left_right_reflect(rule_num):
    binary = rule_to_binary(rule_num)
    mapping = [0, 4, 2, 6, 1, 5, 3, 7]
    reflected = ''.join(binary[mapping[i]] for i in range(8))
    return int(reflected, 2)

def get_orbit(rule_num):
    comp = complement(rule_num)
    reflect = left_right_reflect(rule_num)
    comp_reflect = complement(reflect)
    return tuple(sorted(set([rule_num, comp, reflect, comp_reflect])))

def main():
    print("=" * 70)
    print("COMPLETE CHARACTERIZATION OF CHAOTIC ECA RULES")
    print("=" * 70)

    # The fundamental question: what EXACTLY distinguishes chaotic rules?
    # We have:
    # - Exactly 4 ones (necessary)
    # - NOT (111->1, 000->0) (necessary)
    # - d3 == 1 (necessary)

    # Let's enumerate the surviving rules after these filters
    four_ones = [r for r in range(256) if count_ones(r) == 4]
    print(f"\nRules with 4 ones: {len(four_ones)}")

    not_both_quiescent = []
    for r in four_ones:
        t = rule_to_table(r)
        if not (t['111'] == 1 and t['000'] == 0):
            not_both_quiescent.append(r)
    print(f"After removing (111->1, 000->0): {len(not_both_quiescent)}")

    d3_one = []
    for r in not_both_quiescent:
        t = rule_to_table(r)
        d3 = abs(t['110'] - t['011']) + abs(t['100'] - t['001'])
        if d3 == 1:
            d3_one.append(r)
    print(f"After requiring d3==1: {len(d3_one)}")

    # At this point we have 24 rules, 12 chaotic and 12 periodic
    chaotic_remaining = sorted(set(d3_one) & KNOWN_CHAOTIC)
    periodic_remaining = sorted(set(d3_one) - KNOWN_CHAOTIC)

    print(f"\nChaotic ({len(chaotic_remaining)}): {chaotic_remaining}")
    print(f"Periodic ({len(periodic_remaining)}): {periodic_remaining}")

    neighborhoods = ['111', '110', '101', '100', '011', '010', '001', '000']

    print("\n" + "=" * 70)
    print("COMPARING THE 12+12 SURVIVING RULES")
    print("=" * 70)

    print("\nChaotic rules:")
    print("Rule  111 110 101 100 011 010 001 000  | Orbit")
    for rule in chaotic_remaining:
        t = rule_to_table(rule)
        outputs = [t[nb] for nb in neighborhoods]
        orbit = get_orbit(rule)
        print(f"{rule:3d}:   {outputs}   | {orbit}")

    print("\nPeriodic rules:")
    print("Rule  111 110 101 100 011 010 001 000  | Orbit")
    for rule in periodic_remaining:
        t = rule_to_table(rule)
        outputs = [t[nb] for nb in neighborhoods]
        orbit = get_orbit(rule)
        print(f"{rule:3d}:   {outputs}   | {orbit}")

    print("\n" + "=" * 70)
    print("ORBIT ANALYSIS")
    print("=" * 70)

    # Check orbit membership
    chaotic_orbits = set(get_orbit(r) for r in chaotic_remaining)
    periodic_orbits = set(get_orbit(r) for r in periodic_remaining)

    print(f"\nChaotic orbits: {len(chaotic_orbits)}")
    for orbit in sorted(chaotic_orbits):
        print(f"  {orbit}")

    print(f"\nPeriodic orbits: {len(periodic_orbits)}")
    for orbit in sorted(periodic_orbits):
        print(f"  {orbit}")

    # Are any orbits shared?
    shared = chaotic_orbits & periodic_orbits
    print(f"\nShared orbits: {shared}")

    # Key insight: do chaotic and periodic orbits have different structures?
    print("\n" + "=" * 70)
    print("DETAILED COMPARISON")
    print("=" * 70)

    # For each surviving rule, compute more features
    def compute_features(rule):
        t = rule_to_table(rule)

        # Basic
        ones = count_ones(rule)

        # Transitions in output (number of 0->1 or 1->0)
        outputs = [t[nb] for nb in neighborhoods]
        transitions = sum(1 for i in range(7) if outputs[i] != outputs[i+1])

        # Specific bit combinations
        # Position 1 XOR position 6 (110 XOR 001)
        xor_16 = t['110'] ^ t['001']
        # Position 2 XOR position 5 (101 XOR 010)
        xor_25 = t['101'] ^ t['010']
        # Position 3 XOR position 4 (100 XOR 011)
        xor_34 = t['100'] ^ t['011']

        # Which asymmetry?
        asym_type = None
        if t['110'] != t['011'] and t['100'] == t['001']:
            asym_type = '110/011'
            asym_dir = t['110'] - t['011']
        elif t['110'] == t['011'] and t['100'] != t['001']:
            asym_type = '100/001'
            asym_dir = t['100'] - t['001']
        else:
            asym_type = 'other'
            asym_dir = 0

        # Sum of symmetric positions
        sym_sum = t['101'] + t['010']

        return {
            'transitions': transitions,
            'xor_16': xor_16,
            'xor_25': xor_25,
            'xor_34': xor_34,
            'asym_type': asym_type,
            'asym_dir': asym_dir,
            'sym_sum': sym_sum
        }

    chaotic_features = {r: compute_features(r) for r in chaotic_remaining}
    periodic_features = {r: compute_features(r) for r in periodic_remaining}

    # Compare each feature
    feature_names = ['transitions', 'xor_16', 'xor_25', 'xor_34', 'asym_type', 'asym_dir', 'sym_sum']

    for fname in feature_names:
        chaotic_vals = Counter(chaotic_features[r][fname] for r in chaotic_remaining)
        periodic_vals = Counter(periodic_features[r][fname] for r in periodic_remaining)
        print(f"\n{fname}:")
        print(f"  Chaotic:  {dict(chaotic_vals)}")
        print(f"  Periodic: {dict(periodic_vals)}")

        # Check for discriminating values
        chaotic_set = set(chaotic_vals.keys())
        periodic_set = set(periodic_vals.keys())
        unique_to_chaotic = chaotic_set - periodic_set
        unique_to_periodic = periodic_set - chaotic_set

        if unique_to_chaotic:
            print(f"  ** Values unique to chaotic: {unique_to_chaotic}")
        if unique_to_periodic:
            print(f"  ** Values unique to periodic: {unique_to_periodic}")

    print("\n" + "=" * 70)
    print("THE TRANSITIONS FEATURE!")
    print("=" * 70)

    # Looks like transitions might be the key!
    print("\nTransitions (# of output bit changes in sequence):")
    print("\nChaotic rules:")
    for rule in chaotic_remaining:
        t = rule_to_table(rule)
        outputs = [t[nb] for nb in neighborhoods]
        transitions = chaotic_features[rule]['transitions']
        print(f"  {rule:3d}: {outputs} -> {transitions} transitions")

    print("\nPeriodic rules:")
    for rule in periodic_remaining:
        t = rule_to_table(rule)
        outputs = [t[nb] for nb in neighborhoods]
        transitions = periodic_features[rule]['transitions']
        print(f"  {rule:3d}: {outputs} -> {transitions} transitions")

    # So chaotic has {2, 5, 6} transitions, periodic has {3, 4, 5}
    # Not quite separating... let's try combinations

    print("\n" + "=" * 70)
    print("COMBINED FEATURE ANALYSIS")
    print("=" * 70)

    # Try (transitions, sym_sum)
    print("\n(transitions, sym_sum) combinations:")
    chaotic_combos = Counter(
        (chaotic_features[r]['transitions'], chaotic_features[r]['sym_sum'])
        for r in chaotic_remaining
    )
    periodic_combos = Counter(
        (periodic_features[r]['transitions'], periodic_features[r]['sym_sum'])
        for r in periodic_remaining
    )

    print(f"  Chaotic:  {dict(chaotic_combos)}")
    print(f"  Periodic: {dict(periodic_combos)}")

    # Try (transitions, xor_25)
    print("\n(transitions, xor_25) combinations:")
    chaotic_combos = Counter(
        (chaotic_features[r]['transitions'], chaotic_features[r]['xor_25'])
        for r in chaotic_remaining
    )
    periodic_combos = Counter(
        (periodic_features[r]['transitions'], periodic_features[r]['xor_25'])
        for r in periodic_remaining
    )

    print(f"  Chaotic:  {dict(chaotic_combos)}")
    print(f"  Periodic: {dict(periodic_combos)}")

    overlap = set(chaotic_combos.keys()) & set(periodic_combos.keys())
    print(f"  Overlap: {overlap}")

    # Try looking at 3-feature combinations
    print("\n(transitions, xor_25, sym_sum) combinations:")
    chaotic_combos = set(
        (chaotic_features[r]['transitions'], chaotic_features[r]['xor_25'], chaotic_features[r]['sym_sum'])
        for r in chaotic_remaining
    )
    periodic_combos = set(
        (periodic_features[r]['transitions'], periodic_features[r]['xor_25'], periodic_features[r]['sym_sum'])
        for r in periodic_remaining
    )

    print(f"  Chaotic:  {sorted(chaotic_combos)}")
    print(f"  Periodic: {sorted(periodic_combos)}")
    print(f"  Overlap: {chaotic_combos & periodic_combos}")

    # Another approach: look at specific bit patterns in relation to orbits
    print("\n" + "=" * 70)
    print("ORBIT-BASED ANALYSIS")
    print("=" * 70)

    # Which position in orbit determines chaos?
    for orbit in sorted(chaotic_orbits):
        orbit_members = list(orbit)
        chaos_status = ['C' if r in KNOWN_CHAOTIC else 'P' for r in orbit_members]
        print(f"\nOrbit {orbit}: status = {chaos_status}")

        for r in orbit_members:
            t = rule_to_table(r)
            outputs = [t[nb] for nb in neighborhoods]
            status = "CHAOTIC" if r in KNOWN_CHAOTIC else "periodic"
            print(f"  {r:3d} ({status:7s}): {outputs}")

if __name__ == '__main__':
    main()
