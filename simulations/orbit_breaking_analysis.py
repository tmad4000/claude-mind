#!/usr/bin/env python3
"""
CRITICAL DISCOVERY: Orbits under complement/reflection split between chaotic and periodic!

The standard equivalence operations (complement, left-right reflection) don't preserve chaos.
This is surprising - these operations usually preserve dynamics.

This script investigates WHY orbits split and what distinguishes chaotic from periodic
members of the same orbit.
"""

# The 12 chaotic rules
CHAOTIC_RULES = set([30, 45, 75, 86, 89, 101, 102, 105, 106, 150, 153, 154])

def rule_to_table(rule):
    return [(rule >> i) & 1 for i in range(8)]

def reflect(rule):
    """Left-right reflection of a rule."""
    table = rule_to_table(rule)
    def reflect_input(i):
        return ((i & 1) << 2) | (i & 2) | ((i >> 2) & 1)
    reflected_table = [table[reflect_input(i)] for i in range(8)]
    return sum(reflected_table[i] << i for i in range(8))

def complement(rule):
    """Complement of a rule (flip all outputs)."""
    return 255 - rule

def get_orbit(rule):
    """Get full equivalence orbit under complement and reflection."""
    refl = reflect(rule)
    comp = complement(rule)
    comp_refl = complement(refl)
    return sorted(set([rule, refl, comp, comp_refl]))

# Define the orbits
orbits = []
seen = set()
for r in range(256):
    if r not in seen:
        orbit = get_orbit(r)
        seen.update(orbit)
        # Only keep orbits that contain at least one chaotic rule
        if any(x in CHAOTIC_RULES for x in orbit):
            orbits.append(orbit)

print("=" * 70)
print("ORBITS CONTAINING CHAOTIC RULES")
print("=" * 70)

for orbit in orbits:
    chaotic = [r for r in orbit if r in CHAOTIC_RULES]
    periodic = [r for r in orbit if r not in CHAOTIC_RULES]
    print(f"\nOrbit: {orbit}")
    print(f"  Chaotic: {chaotic}")
    print(f"  Periodic: {periodic}")

# Detailed analysis of each orbit
print("\n" + "=" * 70)
print("DETAILED ORBIT ANALYSIS")
print("=" * 70)

def analyze_rule_detail(rule):
    """Detailed analysis of a rule."""
    table = rule_to_table(rule)

    # Which inputs map to 0?
    zeros = [i for i in range(8) if table[i] == 0]

    # Information flow direction
    # Positive = info flows left-to-right (output depends more on left)
    # Negative = info flows right-to-left
    left_influence = sum(1 for base in range(4) if table[base] != table[base + 4])
    right_influence = sum(1 for base in [0, 2, 4, 6] if table[base] != table[base + 1])
    flow_asymmetry = left_influence - right_influence

    # Check if 000->0 and 111->1 (quiescent states)
    quiescent_0 = table[0] == 0
    quiescent_1 = table[7] == 1

    return {
        'rule': rule,
        'zeros': zeros,
        'left_influence': left_influence,
        'right_influence': right_influence,
        'flow_asymmetry': flow_asymmetry,
        'quiescent_0': quiescent_0,
        'quiescent_1': quiescent_1,
    }

for orbit in orbits:
    print(f"\n{'='*60}")
    print(f"Orbit: {orbit}")
    print(f"{'='*60}")

    for r in orbit:
        analysis = analyze_rule_detail(r)
        is_chaotic = r in CHAOTIC_RULES
        status = "CHAOTIC" if is_chaotic else "periodic"

        print(f"\n  Rule {r:3d} [{status}]:")
        print(f"    zeros = {analysis['zeros']} = {[f'{i:03b}' for i in analysis['zeros']]}")
        print(f"    left_influence = {analysis['left_influence']}, right_influence = {analysis['right_influence']}")
        print(f"    flow_asymmetry = {analysis['flow_asymmetry']}")
        print(f"    quiescent: 000->0 = {analysis['quiescent_0']}, 111->1 = {analysis['quiescent_1']}")

# Look for the pattern
print("\n" + "=" * 70)
print("SEARCHING FOR THE DISTINGUISHING PATTERN")
print("=" * 70)

# Hypothesis: chaos requires flow_asymmetry != 0 (directional bias)
# OR special symmetric structure

print("\nFlow asymmetry distribution:")
for orbit in orbits:
    print(f"\nOrbit {orbit}:")
    for r in orbit:
        analysis = analyze_rule_detail(r)
        is_chaotic = r in CHAOTIC_RULES
        status = "CHAOTIC" if is_chaotic else "periodic"
        print(f"  Rule {r:3d} [{status}]: asymmetry={analysis['flow_asymmetry']}")

# Check if flow_asymmetry separates
print("\n" + "=" * 70)
print("FLOW ASYMMETRY ANALYSIS")
print("=" * 70)

chaotic_asymmetries = []
periodic_asymmetries = []

for r in range(256):
    if r in CHAOTIC_RULES or r in [x for orbit in orbits for x in orbit if x not in CHAOTIC_RULES]:
        analysis = analyze_rule_detail(r)
        if r in CHAOTIC_RULES:
            chaotic_asymmetries.append((r, analysis['flow_asymmetry']))
        elif any(r in orbit for orbit in orbits):
            periodic_asymmetries.append((r, analysis['flow_asymmetry']))

print("\nChaotic rules and their flow asymmetry:")
for r, asym in sorted(chaotic_asymmetries):
    print(f"  Rule {r:3d}: {asym}")

print("\nPeriodic rules (in chaotic orbits) and their flow asymmetry:")
for r, asym in sorted(periodic_asymmetries):
    print(f"  Rule {r:3d}: {asym}")

# Summary
chaotic_asym_vals = set(a for _, a in chaotic_asymmetries)
periodic_asym_vals = set(a for _, a in periodic_asymmetries)
print(f"\nChaotic asymmetry values: {sorted(chaotic_asym_vals)}")
print(f"Periodic asymmetry values: {sorted(periodic_asym_vals)}")

# NEW INSIGHT: Check if it's about the DIRECTION of asymmetry
# Maybe chaos requires asymmetry pointing a specific way?

print("\n" + "=" * 70)
print("ASYMMETRY DIRECTION ANALYSIS")
print("=" * 70)

for orbit in orbits:
    print(f"\nOrbit {orbit}:")
    for r in orbit:
        analysis = analyze_rule_detail(r)
        is_chaotic = r in CHAOTIC_RULES
        status = "C" if is_chaotic else "P"

        # Determine direction
        if analysis['flow_asymmetry'] > 0:
            direction = "LEFT_DOMINANT"
        elif analysis['flow_asymmetry'] < 0:
            direction = "RIGHT_DOMINANT"
        else:
            direction = "BALANCED"

        print(f"  {status} Rule {r:3d}: asym={analysis['flow_asymmetry']:+d} ({direction})")

# Check correlation with reflection
print("\n" + "=" * 70)
print("REFLECTION RELATIONSHIP")
print("=" * 70)

for orbit in orbits:
    print(f"\nOrbit {orbit}:")

    # Identify which pairs are reflections of each other
    members = orbit
    for i, r1 in enumerate(members):
        for r2 in members[i+1:]:
            if reflect(r1) == r2:
                c1 = "CHAOTIC" if r1 in CHAOTIC_RULES else "periodic"
                c2 = "CHAOTIC" if r2 in CHAOTIC_RULES else "periodic"
                print(f"  {r1} ({c1}) <--reflect--> {r2} ({c2})")

            if complement(r1) == r2:
                c1 = "CHAOTIC" if r1 in CHAOTIC_RULES else "periodic"
                c2 = "CHAOTIC" if r2 in CHAOTIC_RULES else "periodic"
                print(f"  {r1} ({c1}) <--complement--> {r2} ({c2})")

# MAJOR INSIGHT: Does reflection preserve chaos but complement doesn't?
print("\n" + "=" * 70)
print("WHICH OPERATIONS PRESERVE CHAOS?")
print("=" * 70)

reflect_preserves = True
complement_preserves = True

for r in CHAOTIC_RULES:
    refl = reflect(r)
    comp = complement(r)

    if refl not in CHAOTIC_RULES:
        reflect_preserves = False
        print(f"  Reflection BREAKS chaos: {r} -> {refl}")

    if comp not in CHAOTIC_RULES:
        complement_preserves = False
        print(f"  Complement BREAKS chaos: {r} -> {comp}")

print(f"\nReflection preserves chaos: {reflect_preserves}")
print(f"Complement preserves chaos: {complement_preserves}")
