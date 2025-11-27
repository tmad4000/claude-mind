#!/usr/bin/env python3
"""
Testing the "all bits matter" theory for chaos.

Hypothesis: Chaos requires that ALL THREE input bits (left, center, right)
have some influence on the output. If any bit is completely ignored or
only matters sometimes, the rule becomes periodic.

This makes intuitive sense: for information to propagate in all directions
and create mixing/chaos, all input positions must contribute.
"""

# The 12 chaotic rules
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

def bit_influence(rule):
    """
    For each input bit, count in how many contexts flipping it changes output.
    """
    table = rule_to_table(rule)

    influences = {}

    # Left bit (bit 2, position 4)
    left_influence = sum(1 for base in range(4)
                         if table[base] != table[base + 4])
    influences['left'] = left_influence

    # Center bit (bit 1, position 2)
    center_influence = 0
    for left in [0, 4]:
        for right in [0, 1]:
            base = left + right
            if table[base] != table[base + 2]:
                center_influence += 1
    influences['center'] = center_influence

    # Right bit (bit 0, position 1)
    right_influence = sum(1 for base in [0, 2, 4, 6]
                          if table[base] != table[base + 1])
    influences['right'] = right_influence

    return influences

# Find all max-mixing rules
four_ones = [r for r in range(256) if count_ones(r) == 4]
max_mixing = [r for r in four_ones if count_mixing(r) == 8]

print("=" * 70)
print("BIT INFLUENCE ANALYSIS")
print("=" * 70)

print("\nChaotic rules:")
for r in sorted(CHAOTIC_RULES):
    inf = bit_influence(r)
    print(f"  Rule {r:3d}: left={inf['left']}, center={inf['center']}, right={inf['right']}")

periodic_maxmix = [r for r in max_mixing if r not in CHAOTIC_RULES]
print("\nPeriodic max-mixing rules:")
for r in sorted(periodic_maxmix):
    inf = bit_influence(r)
    print(f"  Rule {r:3d}: left={inf['left']}, center={inf['center']}, right={inf['right']}")

# Test criterion: all bits must have influence >= 2
print("\n" + "=" * 70)
print("TESTING: All bits must have influence >= 2")
print("=" * 70)

def all_bits_matter(rule, threshold=2):
    inf = bit_influence(rule)
    return all(v >= threshold for v in inf.values())

passes_criterion = [r for r in max_mixing if all_bits_matter(r, 2)]
print(f"\nRules where all bits have influence >= 2: {len(passes_criterion)}")

chaotic_pass = [r for r in passes_criterion if r in CHAOTIC_RULES]
periodic_pass = [r for r in passes_criterion if r not in CHAOTIC_RULES]

print(f"  Chaotic: {len(chaotic_pass)}")
print(f"  Periodic: {len(periodic_pass)}")

if periodic_pass:
    print(f"\nPeriodic rules that pass (still need distinguishing):")
    for r in periodic_pass:
        inf = bit_influence(r)
        print(f"  Rule {r:3d}: left={inf['left']}, center={inf['center']}, right={inf['right']}")

# Let's look at more specific patterns
print("\n" + "=" * 70)
print("LOOKING FOR THE DISTINGUISHING PATTERN")
print("=" * 70)

# What's special about the periodic rules that pass?
# Maybe look at HOW the bits interact

def interaction_pattern(rule):
    """
    Analyze how bit changes interact.
    If changing left and then right gives same result as changing right then left,
    the rule has a certain "commutativity" property.
    """
    table = rule_to_table(rule)

    # XOR structure: is the rule XOR of some bits?
    is_xor = False
    xor_mask = None
    for mask in range(8):
        if all(table[i] == (bin(i & mask).count('1') % 2) for i in range(8)):
            is_xor = True
            xor_mask = mask
            break

    # Look at the "derivative" structure
    # d_left[i] = table[i+4] XOR table[i] for i in 0..3
    d_left = [(table[i+4] ^ table[i]) for i in range(4)]
    d_right = [(table[i+1] ^ table[i]) for i in [0, 2, 4, 6]]
    d_center = [(table[i+2] ^ table[i]) for i in [0, 1, 4, 5]]

    return {
        'is_xor': is_xor,
        'xor_mask': xor_mask,
        'd_left': d_left,
        'd_right': d_right,
        'd_center': d_center,
    }

print("\nDerivative structure:")
print("\nChaotic rules:")
for r in sorted(CHAOTIC_RULES):
    ip = interaction_pattern(r)
    print(f"  Rule {r:3d}: XOR={ip['is_xor']} mask={ip['xor_mask']}")
    print(f"    d_left={ip['d_left']}, d_right={ip['d_right']}, d_center={ip['d_center']}")

print("\nPeriodic rules that pass 'all bits matter':")
for r in periodic_pass:
    ip = interaction_pattern(r)
    print(f"  Rule {r:3d}: XOR={ip['is_xor']} mask={ip['xor_mask']}")
    print(f"    d_left={ip['d_left']}, d_right={ip['d_right']}, d_center={ip['d_center']}")

# Look for complement/reflection relationships
print("\n" + "=" * 70)
print("ORBIT STRUCTURE")
print("=" * 70)

def get_orbit(rule):
    """Get the full equivalence orbit of a rule under complement and reflection."""
    table = rule_to_table(rule)

    def reflect(i):
        return ((i & 1) << 2) | (i & 2) | ((i >> 2) & 1)

    reflected_table = [table[reflect(i)] for i in range(8)]
    reflected = sum(reflected_table[i] << i for i in range(8))

    complement = 255 - rule
    comp_reflected = 255 - reflected

    return sorted(set([rule, reflected, complement, comp_reflected]))

print("\nChaotic orbits:")
seen = set()
for r in sorted(CHAOTIC_RULES):
    if r not in seen:
        orbit = get_orbit(r)
        seen.update(orbit)
        in_chaotic = [x for x in orbit if x in CHAOTIC_RULES]
        not_chaotic = [x for x in orbit if x not in CHAOTIC_RULES]
        print(f"  Orbit of {r}: {orbit}")
        print(f"    Chaotic: {in_chaotic}, Not chaotic: {not_chaotic}")

print("\nPeriodic (all-bits-matter) orbits:")
seen = set()
for r in sorted(periodic_pass):
    if r not in seen:
        orbit = get_orbit(r)
        seen.update(orbit)
        in_chaotic = [x for x in orbit if x in CHAOTIC_RULES]
        not_chaotic = [x for x in orbit if x not in CHAOTIC_RULES]
        print(f"  Orbit of {r}: {orbit}")
        print(f"    Chaotic: {in_chaotic}, Not chaotic: {not_chaotic}")

# FINAL TEST: Can we separate chaotic from periodic?
print("\n" + "=" * 70)
print("FINAL DISTINGUISHING TEST")
print("=" * 70)

# Observation: the derivative patterns differ!
# Let's count the number of 1s in each derivative

def derivative_signature(rule):
    ip = interaction_pattern(rule)
    return (sum(ip['d_left']), sum(ip['d_center']), sum(ip['d_right']))

print("\nDerivative signatures (sum of d_left, d_center, d_right):")

chaotic_sigs = set()
for r in sorted(CHAOTIC_RULES):
    sig = derivative_signature(r)
    chaotic_sigs.add(sig)
    print(f"  Rule {r:3d}: {sig}")

print("\nPeriodic all-bits-matter rules:")
periodic_sigs = set()
for r in sorted(periodic_pass):
    sig = derivative_signature(r)
    periodic_sigs.add(sig)
    print(f"  Rule {r:3d}: {sig}")

print(f"\nChaotic signatures: {sorted(chaotic_sigs)}")
print(f"Periodic signatures: {sorted(periodic_sigs)}")

overlap = chaotic_sigs & periodic_sigs
if overlap:
    print(f"OVERLAP: {overlap}")
else:
    print("NO OVERLAP - Perfect separation!")
