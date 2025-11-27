#!/usr/bin/env python3
"""
Investigating High-Gap Rules: 149 and 135

These rules have even HIGHER entropy gaps than canonical Class IV:
- Rule 149: gap +1.72
- Rule 135: gap +1.70
- vs Rule 110: gap +1.57

Are these "super Class IV" or something different?
"""

import random
from datetime import datetime


class ElementaryCA:
    def __init__(self, rule_number: int, width: int = 80):
        self.rule_number = rule_number
        self.width = width
        self.rule_table = self._build_rule_table(rule_number)
        self.history = []

    def _build_rule_table(self, rule_number: int) -> dict:
        table = {}
        for i in range(8):
            pattern = tuple(int(b) for b in format(i, '03b'))
            table[pattern] = (rule_number >> i) & 1
        return table

    def step(self, state: list) -> list:
        new_state = []
        for i in range(len(state)):
            left = state[(i - 1) % len(state)]
            center = state[i]
            right = state[(i + 1) % len(state)]
            new_state.append(self.rule_table[(left, center, right)])
        return new_state

    def run(self, initial_state: list = None, steps: int = 40) -> list:
        if initial_state is None:
            initial_state = [0] * self.width
            initial_state[self.width // 2] = 1
        self.history = [initial_state]
        state = initial_state
        for _ in range(steps):
            state = self.step(state)
            self.history.append(state)
        return self.history

    def visualize(self) -> str:
        lines = []
        for row in self.history:
            line = ''.join('█' if cell else ' ' for cell in row)
            lines.append(line)
        return '\n'.join(lines)


def investigate_rule(rule: int):
    """Deep investigation of a single rule"""
    print(f"\n{'='*70}")
    print(f"RULE {rule} (binary: {format(rule, '08b')})")
    print('='*70)

    # Rule table
    ca = ElementaryCA(rule, 80)
    print("\nRule table (neighborhood → next state):")
    for i in range(7, -1, -1):
        pattern = format(i, '03b')
        output = ca.rule_table[tuple(int(b) for b in pattern)]
        print(f"  {pattern} → {output}")

    # Single seed evolution
    print("\n--- Single seed (40 steps) ---")
    ca.run(steps=40)
    print(ca.visualize())

    # Random initial conditions
    print("\n--- Random initial (50% density) ---")
    ca2 = ElementaryCA(rule, 80)
    random_init = [random.randint(0, 1) for _ in range(80)]
    ca2.run(random_init, steps=40)
    print(ca2.visualize())

    # Compare to Rule 110
    print("\n--- Rule 110 for comparison ---")
    ca110 = ElementaryCA(110, 80)
    ca110.run(steps=40)
    print(ca110.visualize())


def analyze_rule_properties():
    """Compare properties of high-gap rules vs canonical Class IV"""
    print("\n" + "="*70)
    print("PROPERTY COMPARISON: High-gap rules vs Canonical Class IV")
    print("="*70)

    rules_to_compare = {
        149: "Highest gap (+1.72)",
        135: "Second highest (+1.70)",
        110: "Canonical Class IV",
        30: "Famous chaotic (+1.48)",
    }

    for rule, description in rules_to_compare.items():
        print(f"\n--- Rule {rule}: {description} ---")
        print(f"Binary: {format(rule, '08b')}")
        print(f"Hamming weight: {bin(rule).count('1')}")

        # Count specific transitions
        ca = ElementaryCA(rule, 80)
        print("Key transitions:")
        print(f"  000→{ca.rule_table[(0,0,0)]} (spontaneous birth from void)")
        print(f"  111→{ca.rule_table[(1,1,1)]} (survival in crowd)")
        print(f"  001→{ca.rule_table[(0,0,1)]} (right edge birth)")
        print(f"  100→{ca.rule_table[(1,0,0)]} (left edge birth)")
        print(f"  010→{ca.rule_table[(0,1,0)]} (isolated survival)")

        # Replication condition check
        replication_condition = (
            ca.rule_table[(0,0,0)] == 0 and  # No spontaneous birth
            ca.rule_table[(0,0,1)] == 1 and  # Right edge spreads
            ca.rule_table[(1,0,0)] == 1      # Left edge spreads
        )
        print(f"  Replication condition: {'YES' if replication_condition else 'NO'}")


def get_equivalent_rules(rule: int) -> dict:
    """Get symmetry-equivalent rules"""
    # Left-right reflection
    reflected = 0
    for i in range(8):
        left = (i >> 2) & 1
        center = (i >> 1) & 1
        right = i & 1
        reflected_i = (right << 2) | (center << 1) | left
        if (rule >> i) & 1:
            reflected |= (1 << reflected_i)

    # Color complement
    complemented = 0
    for i in range(8):
        comp_i = 7 - i
        if not ((rule >> i) & 1):
            complemented |= (1 << comp_i)

    # Both
    both = 0
    for i in range(8):
        left = (i >> 2) & 1
        center = (i >> 1) & 1
        right = i & 1
        reflected_i = (right << 2) | (center << 1) | left
        comp_reflected_i = 7 - reflected_i
        if not ((rule >> i) & 1):
            both |= (1 << comp_reflected_i)

    return {
        'original': rule,
        'reflected': reflected,
        'complemented': complemented,
        'both': both
    }


def check_equivalence_classes():
    """Check if high-gap rules are related by symmetry"""
    print("\n" + "="*70)
    print("EQUIVALENCE CLASSES")
    print("="*70)

    high_gap_rules = [149, 135, 137, 124, 193, 110, 101, 86, 75, 89, 45, 30]

    equivalence_classes = {}
    for rule in high_gap_rules:
        equiv = get_equivalent_rules(rule)
        canonical = min(equiv.values())
        if canonical not in equivalence_classes:
            equivalence_classes[canonical] = set()
        for name, r in equiv.items():
            equivalence_classes[canonical].add(r)

    print("\nEquivalence classes among high-gap rules:")
    for canonical, members in sorted(equivalence_classes.items()):
        members_in_list = [m for m in members if m in high_gap_rules]
        print(f"  Class {canonical}: {sorted(members)} -> in list: {sorted(members_in_list)}")


def main():
    print("Investigating High-Gap Rules")
    print(f"Time: {datetime.now().isoformat()}\n")

    # Visual investigation
    investigate_rule(149)
    investigate_rule(135)
    investigate_rule(110)  # For comparison

    # Property analysis
    analyze_rule_properties()

    # Equivalence check
    check_equivalence_classes()


if __name__ == '__main__':
    main()
