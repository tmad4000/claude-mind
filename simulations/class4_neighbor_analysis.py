#!/usr/bin/env python3
"""
Analyze why Class IV CA rules are topologically isolated.

For each Class IV rule, examine all 8 Hamming-1 neighbors and classify them.
Look for patterns in which bit flips cause which behavioral changes.
"""

import numpy as np
from collections import defaultdict
import json

# Known Class IV rules (complex/interesting behavior)
CLASS_IV_RULES = [30, 45, 73, 89, 101, 105, 110, 124, 137, 147, 149, 150, 193]

# Transition names for the 8 bits (from LSB to MSB)
# Bit i corresponds to the transition where neighborhood = i in binary
# neighborhood is [left, center, right], so:
TRANSITIONS = {
    0: "000→?",  # all dead → ?
    1: "001→?",  # only right alive → ?
    2: "010→?",  # only center alive → ?
    3: "011→?",  # center+right alive → ?
    4: "100→?",  # only left alive → ?
    5: "101→?",  # left+right alive (center dead) → ?
    6: "110→?",  # left+center alive → ?
    7: "111→?",  # all alive → ?
}


def rule_to_bits(rule):
    """Convert rule number to 8-bit transition table."""
    return [(rule >> i) & 1 for i in range(8)]


def bits_to_rule(bits):
    """Convert 8-bit transition table to rule number."""
    return sum(b << i for i, b in enumerate(bits))


def get_hamming_neighbors(rule):
    """Get all 8 rules that differ by exactly 1 bit."""
    bits = rule_to_bits(rule)
    neighbors = []
    for i in range(8):
        new_bits = bits.copy()
        new_bits[i] = 1 - new_bits[i]  # flip bit i
        neighbors.append((i, bits_to_rule(new_bits)))
    return neighbors


def simulate_ca(rule, width=201, steps=200):
    """Simulate elementary CA from single cell seed."""
    grid = np.zeros((steps, width), dtype=np.uint8)
    grid[0, width // 2] = 1  # single cell in center

    bits = rule_to_bits(rule)

    for t in range(steps - 1):
        for x in range(width):
            left = grid[t, (x - 1) % width]
            center = grid[t, x]
            right = grid[t, (x + 1) % width]
            neighborhood = (left << 2) | (center << 1) | right
            grid[t + 1, x] = bits[neighborhood]

    return grid


def classify_behavior(grid):
    """
    Classify CA behavior into categories.
    Returns: 'dies', 'static', 'periodic', 'chaotic', 'complex'
    """
    steps, width = grid.shape

    # Check if dies (all zeros in last rows)
    if grid[-50:].sum() == 0:
        return 'dies'

    # Check activity in last portion
    last_quarter = grid[-50:]

    # Count live cells over time
    live_counts = [row.sum() for row in grid]

    # Check if static (same pattern repeating)
    if np.array_equal(grid[-1], grid[-2]):
        return 'static'

    # Check for simple periodicity
    for period in range(1, 20):
        if steps > period * 2:
            if np.array_equal(grid[-1], grid[-1 - period]):
                return 'periodic'

    # Check expansion rate
    first_nonzero = [np.where(row)[0] for row in grid if row.sum() > 0]
    if len(first_nonzero) > 10:
        widths = [row.max() - row.min() + 1 if len(row) > 0 else 0
                  for row in [np.where(r)[0] for r in grid]]

        # Linear expansion = complex or chaotic
        early_width = np.mean(widths[10:30]) if len(widths) > 30 else 0
        late_width = np.mean(widths[-30:]) if len(widths) > 30 else 0

        if late_width > early_width * 1.5:
            # Expanding - check if structured or chaotic
            # Use compression as proxy
            last_rows = grid[-30:]
            unique_rows = len(set(tuple(r) for r in last_rows))

            if unique_rows > 25:
                # Many unique rows - likely chaotic
                return 'chaotic'
            else:
                return 'complex'

    # Check if fills entire space
    fill_ratio = grid[-1].sum() / width
    if fill_ratio > 0.4:
        return 'fills'

    return 'other'


def analyze_class4_neighbors():
    """Main analysis: examine all Class IV rules and their neighbors."""

    results = {}
    transition_effects = defaultdict(lambda: defaultdict(int))

    print("=" * 60)
    print("CLASS IV NEIGHBOR ANALYSIS")
    print("=" * 60)

    for rule in CLASS_IV_RULES:
        print(f"\n--- Rule {rule} ---")

        # Classify the rule itself
        grid = simulate_ca(rule)
        own_class = classify_behavior(grid)
        print(f"  Own classification: {own_class}")

        results[rule] = {
            'own_class': own_class,
            'neighbors': {}
        }

        # Get and classify neighbors
        neighbors = get_hamming_neighbors(rule)

        for bit_pos, neighbor_rule in neighbors:
            neighbor_grid = simulate_ca(neighbor_rule)
            neighbor_class = classify_behavior(neighbor_grid)

            # What transition was flipped?
            old_bits = rule_to_bits(rule)
            new_bits = rule_to_bits(neighbor_rule)
            old_output = old_bits[bit_pos]
            new_output = new_bits[bit_pos]

            transition_name = TRANSITIONS[bit_pos].replace('?', str(new_output))
            flip_desc = f"{bit_pos:03b}→{old_output} to {bit_pos:03b}→{new_output}"

            results[rule]['neighbors'][neighbor_rule] = {
                'bit_flipped': bit_pos,
                'flip_desc': flip_desc,
                'class': neighbor_class
            }

            # Track transition effects
            transition_effects[bit_pos][(old_output, new_output, neighbor_class)] += 1

            print(f"  Flip bit {bit_pos} ({flip_desc}): Rule {neighbor_rule} → {neighbor_class}")

    return results, transition_effects


def summarize_findings(results, transition_effects):
    """Summarize patterns in the data."""

    print("\n" + "=" * 60)
    print("SUMMARY: TRANSITION EFFECTS")
    print("=" * 60)

    for bit_pos in range(8):
        print(f"\nBit {bit_pos} ({TRANSITIONS[bit_pos]}):")
        effects = transition_effects[bit_pos]
        for (old, new, cls), count in sorted(effects.items()):
            print(f"  {old}→{new}: {cls} ({count}x)")

    # Count how many neighbors of each class
    class_counts = defaultdict(int)
    for rule_data in results.values():
        for neighbor_data in rule_data['neighbors'].values():
            class_counts[neighbor_data['class']] += 1

    print("\n" + "=" * 60)
    print("NEIGHBOR CLASS DISTRIBUTION")
    print("=" * 60)
    total = sum(class_counts.values())
    for cls, count in sorted(class_counts.items(), key=lambda x: -x[1]):
        print(f"  {cls}: {count} ({100*count/total:.1f}%)")

    # Check: are ANY neighbors also Class IV?
    print("\n" + "=" * 60)
    print("CLASS IV NEIGHBORS OF CLASS IV RULES")
    print("=" * 60)
    class4_neighbors = []
    for rule, rule_data in results.items():
        for neighbor_rule, neighbor_data in rule_data['neighbors'].items():
            if neighbor_data['class'] == 'complex':
                class4_neighbors.append((rule, neighbor_rule, neighbor_data['flip_desc']))

    if class4_neighbors:
        for r1, r2, flip in class4_neighbors:
            print(f"  Rule {r1} → Rule {r2} ({flip})")
    else:
        print("  NONE - Class IV rules are indeed isolated!")

    # Look for patterns: which flips consistently kill complexity?
    print("\n" + "=" * 60)
    print("PATTERNS: WHICH FLIPS KILL COMPLEXITY?")
    print("=" * 60)

    for bit_pos in range(8):
        outcomes = []
        for rule_data in results.values():
            for neighbor_rule, neighbor_data in rule_data['neighbors'].items():
                if neighbor_data['bit_flipped'] == bit_pos:
                    outcomes.append(neighbor_data['class'])

        if outcomes:
            # What % become chaotic, dies, etc?
            from collections import Counter
            counts = Counter(outcomes)
            total = len(outcomes)
            summary = ", ".join(f"{c}:{n}" for c, n in counts.most_common())
            print(f"  Bit {bit_pos} ({TRANSITIONS[bit_pos]}): {summary}")


if __name__ == "__main__":
    results, transition_effects = analyze_class4_neighbors()
    summarize_findings(results, transition_effects)

    # Save results
    with open('/Users/jacobcole/code/claude-mind/simulations/class4_neighbor_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n\nResults saved to class4_neighbor_results.json")
