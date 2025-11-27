#!/usr/bin/env python3
"""
Testing if center dependency is the key distinguishing feature.

Key observation:
- Chaotic rules all have center_dep in {2, 4}
- Some periodic rules have center_dep = 0

Hypothesis: Chaos requires center_dep >= 2 (the rule must respond to center changes)
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

def center_dependency(rule):
    """How many times does flipping center change output?"""
    table = rule_to_table(rule)
    changes = 0
    for outer in range(4):  # (left, right) combinations
        left = (outer >> 1) & 1
        right = outer & 1
        input_0 = left * 4 + 0 * 2 + right  # center = 0
        input_1 = left * 4 + 1 * 2 + right  # center = 1
        if table[input_0] != table[input_1]:
            changes += 1
    return changes

# Analyze all max-mixing rules
four_ones = [r for r in range(256) if count_ones(r) == 4]
max_mixing = [r for r in four_ones if count_mixing(r) == 8]

print("Testing: center_dep >= 2 as criterion")
print("=" * 60)

# Filter by center dependency
with_center_dep = [r for r in max_mixing if center_dependency(r) >= 2]
print(f"\nMax-mixing rules with center_dep >= 2: {len(with_center_dep)}")

chaotic_in_set = [r for r in with_center_dep if r in CHAOTIC_RULES]
periodic_in_set = [r for r in with_center_dep if r not in CHAOTIC_RULES]

print(f"  Chaotic: {len(chaotic_in_set)}")
print(f"  Periodic: {len(periodic_in_set)}")

# What distinguishes these periodic rules?
print(f"\nRemaining periodic rules with center_dep >= 2:")
for r in periodic_in_set:
    table = rule_to_table(r)
    cd = center_dependency(r)
    print(f"  Rule {r:3d}: table={table}, center_dep={cd}")

# Maybe look at LEFT and RIGHT dependency as well
def side_dependency(rule):
    """How many times does flipping left/right change output?"""
    table = rule_to_table(rule)

    left_changes = 0
    right_changes = 0

    for i in range(8):
        # Flip left bit
        flipped_left = i ^ 4
        if table[i] != table[flipped_left]:
            left_changes += 1

        # Flip right bit
        flipped_right = i ^ 1
        if table[i] != table[flipped_right]:
            right_changes += 1

    # Each pair counted twice
    return left_changes // 2, right_changes // 2

print("\n" + "=" * 60)
print("ANALYZING SIDE DEPENDENCIES")
print("=" * 60)

print("\nChaotic rules:")
for r in sorted(CHAOTIC_RULES):
    left_dep, right_dep = side_dependency(r)
    cd = center_dependency(r)
    print(f"  Rule {r:3d}: center={cd}, left={left_dep}, right={right_dep}")

print("\nPeriodic max-mixing rules:")
for r in sorted(periodic_in_set):
    left_dep, right_dep = side_dependency(r)
    cd = center_dependency(r)
    print(f"  Rule {r:3d}: center={cd}, left={left_dep}, right={right_dep}")

# Check for patterns in the dependencies
print("\n" + "=" * 60)
print("DEPENDENCY PATTERN ANALYSIS")
print("=" * 60)

def analyze_dependencies(rule):
    table = rule_to_table(rule)

    # For each input bit position, how does output depend on it?
    deps = {}

    # Left (bit 2)
    left_dep = []
    for base in [0, 1, 2, 3]:  # center-right combinations
        i = base
        val_0 = table[i]
        val_1 = table[i + 4]  # flip bit 2 (left)
        left_dep.append((val_0, val_1))
    deps['left'] = left_dep

    # Center (bit 1)
    center_dep = []
    for base in [0, 4]:  # left bit
        for right in [0, 1]:
            i = base + right
            val_0 = table[i]
            val_1 = table[i + 2]  # flip bit 1 (center)
            center_dep.append((val_0, val_1))
    deps['center'] = center_dep

    # Right (bit 0)
    right_dep = []
    for base in [0, 2, 4, 6]:  # left-center combinations
        i = base
        val_0 = table[i]
        val_1 = table[i + 1]  # flip bit 0 (right)
        right_dep.append((val_0, val_1))
    deps['right'] = right_dep

    return deps

print("\nDependency patterns:")
for r in [30, 90]:  # One chaotic, one periodic
    deps = analyze_dependencies(r)
    is_chaotic = r in CHAOTIC_RULES
    status = "CHAOTIC" if is_chaotic else "periodic"
    print(f"\n  Rule {r:3d} [{status}]:")
    for key, vals in deps.items():
        changes = sum(1 for v0, v1 in vals if v0 != v1)
        print(f"    {key}: {vals} -> {changes} changes")

# Look for the "symmetric treatment" pattern
print("\n" + "=" * 60)
print("SYMMETRIC TREATMENT ANALYSIS")
print("=" * 60)

def is_left_right_symmetric(rule):
    """Check if rule treats left and right symmetrically."""
    table = rule_to_table(rule)

    # Reflect function
    def reflect(i):
        return ((i & 1) << 2) | (i & 2) | ((i >> 2) & 1)

    return all(table[i] == table[reflect(i)] for i in range(8))

def has_complementary_orbits(rule):
    """Check if complement of rule is in same equivalence class."""
    complement = 255 - rule

    # Reflect
    table = rule_to_table(rule)
    def reflect(i):
        return ((i & 1) << 2) | (i & 2) | ((i >> 2) & 1)
    reflected = sum(table[reflect(i)] << i for i in range(8))

    # Complement + reflect
    comp_reflected = 255 - reflected

    return complement, reflected, complement == reflected or rule == complement

print("\nSymmetry analysis:")
for r in sorted(CHAOTIC_RULES | set(periodic_in_set)):
    is_sym = is_left_right_symmetric(r)
    comp, refl, orbit_info = has_complementary_orbits(r)
    is_chaotic = r in CHAOTIC_RULES
    status = "CHAOTIC" if is_chaotic else "periodic"
    print(f"  Rule {r:3d} [{status}]: LR-symmetric={is_sym}, comp={comp}, refl={refl}")

# Key insight search
print("\n" + "=" * 60)
print("THE KEY SEARCH")
print("=" * 60)

# What if we look at the STRUCTURE of the zero-set?
# The 4 inputs that map to 0 - what patterns do they form?

def zero_set_structure(rule):
    """Analyze the geometric structure of zero-producing inputs."""
    table = rule_to_table(rule)
    zeros = [i for i in range(8) if table[i] == 0]

    # Compute pairwise Hamming distances
    def hamming(a, b):
        return bin(a ^ b).count('1')

    distances = [hamming(zeros[i], zeros[j])
                 for i in range(4) for j in range(i+1, 4)]

    # Distance histogram
    hist = {1: 0, 2: 0, 3: 0}
    for d in distances:
        hist[d] += 1

    # Check if zero-set forms a "plane" (2D subspace)
    # A plane in 3D binary space has 4 points with specific structure
    is_plane = (hist[2] == 6)  # All pairs at distance 2 = tetrahedron

    # Check if it's a "line + point" (3 collinear + 1 off)
    is_line_plus = (hist[1] == 2 and hist[2] == 4)

    return {
        'zeros': zeros,
        'distances': sorted(distances),
        'histogram': hist,
        'is_plane': is_plane,
        'is_line_plus': is_line_plus,
    }

print("\nZero-set structure analysis:")
print("\nChaotic rules:")
for r in sorted(CHAOTIC_RULES):
    struct = zero_set_structure(r)
    print(f"  Rule {r:3d}: zeros={struct['zeros']}, hist={struct['histogram']}, plane={struct['is_plane']}")

print("\nPeriodic (max-mixing, center_dep>=2) rules:")
for r in sorted(periodic_in_set):
    struct = zero_set_structure(r)
    print(f"  Rule {r:3d}: zeros={struct['zeros']}, hist={struct['histogram']}, plane={struct['is_plane']}")

# Check if plane structure separates
print("\nPlane structure distribution:")
chaotic_planes = sum(1 for r in CHAOTIC_RULES if zero_set_structure(r)['is_plane'])
periodic_planes = sum(1 for r in periodic_in_set if zero_set_structure(r)['is_plane'])
print(f"  Chaotic: {chaotic_planes}/{len(CHAOTIC_RULES)} are planes")
print(f"  Periodic: {periodic_planes}/{len(periodic_in_set)} are planes")
