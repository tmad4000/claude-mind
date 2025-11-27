#!/usr/bin/env python3
"""
Investigate why some 4-one rule orbits are fully chaotic and others are only partially chaotic.

Fully chaotic orbits (all 4 members chaotic):
  - (30, 86, 169, 225)
  - (106, 120, 135, 149)

Partially chaotic orbits (only 2/4 chaotic):
  - (45, 101, 154, 210) - chaotic: 45, 101; periodic: 154, 210
  - (75, 89, 166, 180) - chaotic: 75, 89; periodic: 166, 180

Questions:
1. What's different between chaotic and periodic members of partial orbits?
2. Is there a pattern in which members are chaotic?
3. Can we predict which orbit members will be chaotic?
"""

import numpy as np

# Orbit definitions
FULL_ORBITS = [
    {'orbit': (30, 86, 169, 225), 'chaotic': {30, 86, 169, 225}},
    {'orbit': (106, 120, 135, 149), 'chaotic': {106, 120, 135, 149}}
]

PARTIAL_ORBITS = [
    {'orbit': (45, 101, 154, 210), 'chaotic': {45, 101}, 'periodic': {154, 210}},
    {'orbit': (75, 89, 166, 180), 'chaotic': {75, 89}, 'periodic': {166, 180}}
]

def rule_to_binary(rule_num):
    """Convert rule number to 8-bit binary string."""
    return format(rule_num, '08b')

def rule_to_table(rule_num):
    """Convert rule number to rule table."""
    binary = rule_to_binary(rule_num)
    neighborhoods = ['111', '110', '101', '100', '011', '010', '001', '000']
    return {nb: int(binary[i]) for i, nb in enumerate(neighborhoods)}

def complement(rule_num):
    """Get the complement rule."""
    return 255 - rule_num

def left_right_reflect(rule_num):
    """Get the left-right reflection of a rule."""
    binary = rule_to_binary(rule_num)
    mapping = [0, 4, 2, 6, 1, 5, 3, 7]
    reflected = ''.join(binary[mapping[i]] for i in range(8))
    return int(reflected, 2)

def get_transformations(rule_num):
    """Get all transformation relationships for a rule."""
    comp = complement(rule_num)
    reflect = left_right_reflect(rule_num)
    comp_reflect = complement(reflect)

    return {
        'original': rule_num,
        'complement': comp,
        'reflection': reflect,
        'complement_of_reflection': comp_reflect
    }

def analyze_orbit_structure():
    """Analyze the structure of partial orbits."""

    print("=" * 70)
    print("INVESTIGATING PARTIAL VS FULL CHAOTIC ORBITS")
    print("=" * 70)

    print("\n1. TRANSFORMATION STRUCTURE OF PARTIAL ORBITS")
    print("-" * 50)

    for orbit_data in PARTIAL_ORBITS:
        orbit = orbit_data['orbit']
        chaotic = orbit_data['chaotic']
        periodic = orbit_data['periodic']

        print(f"\nOrbit {orbit}:")
        print(f"  Chaotic: {sorted(chaotic)}")
        print(f"  Periodic: {sorted(periodic)}")

        # For each chaotic member, find what transforms relate it to periodic members
        for c in sorted(chaotic):
            t = get_transformations(c)
            print(f"\n  Rule {c} (chaotic):")
            print(f"    complement: {t['complement']} ({'chaotic' if t['complement'] in chaotic else 'PERIODIC'})")
            print(f"    reflection: {t['reflection']} ({'chaotic' if t['reflection'] in chaotic else 'PERIODIC'})")
            print(f"    comp_refl:  {t['complement_of_reflection']} ({'chaotic' if t['complement_of_reflection'] in chaotic else 'PERIODIC'})")

    print("\n2. PATTERN IN CHAOTIC VS PERIODIC PAIR RELATIONSHIPS")
    print("-" * 50)

    # Key observation: in partial orbits, which transformation connects chaotic to periodic?
    for orbit_data in PARTIAL_ORBITS:
        orbit = orbit_data['orbit']
        chaotic = orbit_data['chaotic']

        chaotic_list = sorted(chaotic)
        c1, c2 = chaotic_list

        print(f"\nOrbit {orbit}:")
        print(f"  Chaotic pair: {c1}, {c2}")

        # What's the relationship between the two chaotic members?
        t1 = get_transformations(c1)
        if t1['complement'] == c2:
            print(f"  Relationship: complement")
        elif t1['reflection'] == c2:
            print(f"  Relationship: reflection")
        elif t1['complement_of_reflection'] == c2:
            print(f"  Relationship: complement-reflection")

        # What transforms a chaotic member to a periodic one?
        periodic = orbit_data['periodic']
        for c in chaotic_list:
            t = get_transformations(c)
            for name, result in t.items():
                if result in periodic and name != 'original':
                    print(f"  {c} --({name})--> {result} (periodic)")

    print("\n3. RULE TABLE DIFFERENCES: CHAOTIC VS PERIODIC IN SAME ORBIT")
    print("-" * 50)

    neighborhoods = ['111', '110', '101', '100', '011', '010', '001', '000']

    for orbit_data in PARTIAL_ORBITS:
        orbit = orbit_data['orbit']
        chaotic = orbit_data['chaotic']
        periodic = orbit_data['periodic']

        print(f"\nOrbit {orbit}:")
        print("Neighborhood: 111 110 101 100 011 010 001 000")

        for rule in sorted(orbit):
            table = rule_to_table(rule)
            outputs = [str(table[nb]) for nb in neighborhoods]
            status = "CHAOTIC" if rule in chaotic else "periodic"
            print(f"Rule {rule:3d} ({status:7s}):   {' '.join(f' {o} ' for o in outputs)}")

    print("\n4. COMPARING FULLY CHAOTIC VS PARTIAL ORBITS")
    print("-" * 50)

    print("\nFully chaotic orbits:")
    for orbit_data in FULL_ORBITS:
        orbit = orbit_data['orbit']
        print(f"\nOrbit {orbit}:")
        print("Neighborhood: 111 110 101 100 011 010 001 000")
        for rule in sorted(orbit):
            table = rule_to_table(rule)
            outputs = [str(table[nb]) for nb in neighborhoods]
            print(f"Rule {rule:3d}:   {' '.join(f' {o} ' for o in outputs)}")

        # Check transformation relationships
        for rule in sorted(orbit):
            t = get_transformations(rule)
            others = [t[k] for k in ['complement', 'reflection', 'complement_of_reflection']]
            print(f"  {rule}: comp={t['complement']}, refl={t['reflection']}, c_r={t['complement_of_reflection']}")

    print("\n5. HYPOTHESIS: WHAT MAKES AN ORBIT FULLY VS PARTIALLY CHAOTIC?")
    print("-" * 50)

    # Check if it's about the relationship between the 4 members
    print("\nChecking orbit member relationships...")

    for orbit_data in FULL_ORBITS + PARTIAL_ORBITS:
        orbit = orbit_data['orbit']
        chaotic = orbit_data['chaotic']

        r0 = orbit[0]
        t = get_transformations(r0)

        # Build the orbit explicitly showing which transform gives which member
        print(f"\nOrbit {orbit}:")
        print(f"  r0={r0}")
        print(f"  complement(r0)={t['complement']}")
        print(f"  reflect(r0)={t['reflection']}")
        print(f"  comp_reflect(r0)={t['complement_of_reflection']}")

        # Check: are complement pairs together in chaotic status?
        comp_pairs = [(r0, t['complement']), (t['reflection'], t['complement_of_reflection'])]
        refl_pairs = [(r0, t['reflection']), (t['complement'], t['complement_of_reflection'])]

        for p1, p2 in comp_pairs:
            same_status = (p1 in chaotic) == (p2 in chaotic)
            print(f"  Complement pair ({p1}, {p2}): same status = {same_status}")

        for p1, p2 in refl_pairs:
            same_status = (p1 in chaotic) == (p2 in chaotic)
            print(f"  Reflection pair ({p1}, {p2}): same status = {same_status}")

    print("\n6. KEY STRUCTURAL DIFFERENCE")
    print("-" * 50)

    # Look at the actual binary patterns more carefully
    print("\nComparing rule binary patterns:")
    print("\nPartially chaotic orbit 1: (45, 101, 154, 210)")
    print("  45  (CHAOTIC):  00101101")
    print("  101 (CHAOTIC):  01100101")
    print("  154 (periodic): 10011010")
    print("  210 (periodic): 11010010")

    print("\nPartially chaotic orbit 2: (75, 89, 166, 180)")
    print("  75  (CHAOTIC):  01001011")
    print("  89  (CHAOTIC):  01011001")
    print("  166 (periodic): 10100110")
    print("  180 (periodic): 10110100")

    print("\nFully chaotic orbit 1: (30, 86, 169, 225)")
    print("  30  (CHAOTIC): 00011110")
    print("  86  (CHAOTIC): 01010110")
    print("  169 (CHAOTIC): 10101001")
    print("  225 (CHAOTIC): 11100001")

    print("\nFully chaotic orbit 2: (106, 120, 135, 149)")
    print("  106 (CHAOTIC): 01101010")
    print("  120 (CHAOTIC): 01111000")
    print("  135 (CHAOTIC): 10000111")
    print("  149 (CHAOTIC): 10010101")

    # Looking at the patterns...
    # In partial orbits: chaotic rules have lower values (< 128)
    # periodic rules have higher values (>= 128)!
    print("\n7. CRITICAL OBSERVATION: VALUE RANGES")
    print("-" * 50)

    for orbit_data in PARTIAL_ORBITS:
        orbit = orbit_data['orbit']
        chaotic = orbit_data['chaotic']
        periodic = orbit_data['periodic']

        print(f"\nOrbit {orbit}:")
        print(f"  Chaotic: {sorted(chaotic)} (all < 128? {all(r < 128 for r in chaotic)})")
        print(f"  Periodic: {sorted(periodic)} (all >= 128? {all(r >= 128 for r in periodic)})")

    # This means: in partial orbits, the 111 bit determines chaos!
    # 111 bit is 0 for rules < 128, and 1 for rules >= 128

    print("\n8. THE 111 BIT HYPOTHESIS")
    print("-" * 50)

    print("\nFor partial orbits:")
    print("  Rules with 111->0 (rule < 128): CHAOTIC")
    print("  Rules with 111->1 (rule >= 128): periodic")

    print("\nBut for full orbits, both 111->0 and 111->1 members are chaotic...")
    print("Let's check:")

    for orbit_data in FULL_ORBITS:
        orbit = orbit_data['orbit']
        for rule in orbit:
            table = rule_to_table(rule)
            print(f"  Rule {rule}: 111->{table['111']}, 000->{table['000']}")

if __name__ == '__main__':
    analyze_orbit_structure()
