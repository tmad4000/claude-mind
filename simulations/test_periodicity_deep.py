#!/usr/bin/env python3
"""
Deep test of periodicity: Is Class IV actually periodic while Class III is truly chaotic?

Key insight from previous tests:
- Class IV finds cycles in ~600 steps on width-50 grids
- Class III never finds cycles (hits max 5000 steps)

This could be THE defining difference:
- Class IV = quasi-periodic (complex but ultimately deterministic cycles)
- Class III = truly chaotic (never repeats)

Author: Claude (overnight session 2)
Date: 2025-11-27
"""

import numpy as np
from collections import defaultdict

CLASS_IV = [110, 124, 137, 193]
CLASS_III = [30, 45, 89, 101, 105, 135, 149, 150]

def apply_rule(cells, rule_num):
    """Apply ECA rule to get next generation."""
    rule_bits = [(rule_num >> i) & 1 for i in range(8)]
    n = len(cells)
    new_cells = np.zeros_like(cells)
    for i in range(n):
        left = cells[(i-1) % n]
        center = cells[i]
        right = cells[(i+1) % n]
        idx = (left << 2) | (center << 1) | right
        new_cells[i] = rule_bits[idx]
    return new_cells

def state_to_hash(state):
    """Convert state array to hashable value."""
    return hash(tuple(state.tolist()))

def measure_periodicity(rule_num, width, max_steps=10000, trials=5):
    """Measure if rule reaches periodic cycle."""
    results = []

    for trial in range(trials):
        np.random.seed(trial * 1000 + rule_num)
        cells = np.random.randint(0, 2, width)
        seen_states = {}

        for step in range(max_steps):
            state_hash = state_to_hash(cells)
            if state_hash in seen_states:
                # Found cycle
                period = step - seen_states[state_hash]
                results.append({
                    'found_cycle': True,
                    'transient': seen_states[state_hash],
                    'period': period
                })
                break
            seen_states[state_hash] = step
            cells = apply_rule(cells, rule_num)
        else:
            results.append({
                'found_cycle': False,
                'transient': max_steps,
                'period': None
            })

    return results

def main():
    print("=" * 70)
    print("PERIODICITY TEST: Is Class IV periodic while Class III is chaotic?")
    print("=" * 70)
    print()

    # Test at multiple widths
    widths = [31, 47, 61, 79]  # Prime widths to avoid trivial symmetries

    for width in widths:
        print(f"\n{'='*60}")
        print(f"WIDTH = {width}")
        print(f"{'='*60}")

        print("\nClass IV rules:")
        iv_cycles = []
        for rule in CLASS_IV:
            results = measure_periodicity(rule, width, max_steps=20000, trials=5)
            found = sum(1 for r in results if r['found_cycle'])
            if found > 0:
                periods = [r['period'] for r in results if r['found_cycle']]
                transients = [r['transient'] for r in results if r['found_cycle']]
                print(f"  Rule {rule:3d}: {found}/5 found cycles, period={np.mean(periods):.0f}±{np.std(periods):.0f}, transient={np.mean(transients):.0f}")
                iv_cycles.append(found)
            else:
                print(f"  Rule {rule:3d}: 0/5 found cycles (chaotic or very long period)")
                iv_cycles.append(0)

        print("\nClass III rules:")
        iii_cycles = []
        for rule in CLASS_III[:4]:
            results = measure_periodicity(rule, width, max_steps=20000, trials=5)
            found = sum(1 for r in results if r['found_cycle'])
            if found > 0:
                periods = [r['period'] for r in results if r['found_cycle']]
                transients = [r['transient'] for r in results if r['found_cycle']]
                print(f"  Rule {rule:3d}: {found}/5 found cycles, period={np.mean(periods):.0f}±{np.std(periods):.0f}, transient={np.mean(transients):.0f}")
                iii_cycles.append(found)
            else:
                print(f"  Rule {rule:3d}: 0/5 found cycles (chaotic)")
                iii_cycles.append(0)

        print(f"\n  Summary: Class IV avg cycles found = {np.mean(iv_cycles):.1f}/5")
        print(f"           Class III avg cycles found = {np.mean(iii_cycles):.1f}/5")

    # Theoretical analysis
    print("\n" + "=" * 70)
    print("THEORETICAL ANALYSIS")
    print("=" * 70)
    print("""
On a finite grid of width N with periodic boundaries:
- Total possible states: 2^N
- For N=31: 2^31 = 2.1 billion states
- For N=47: 2^47 = 140 trillion states

If a CA is truly chaotic, it should visit states quasi-randomly,
meaning cycle detection would require exploring a significant
fraction of the state space.

If Class IV finds cycles in 10000-20000 steps on width-47 grids,
while Class III doesn't, this suggests:

1. Class IV has LOWER effective dimensionality
   - It visits a small subset of possible states
   - Localized structures (gliders) constrain the dynamics

2. Class III explores the full state space
   - Truly chaotic mixing
   - No localized structures to constrain dynamics

This would mean Class IV is "complex but constrained" while
Class III is "chaotically unconstrained".
""")

    # Final test: How does cycle-finding scale with width?
    print("\n" + "=" * 70)
    print("SCALING TEST: How does cycle-finding probability scale with width?")
    print("=" * 70)

    test_widths = [21, 31, 41, 51, 61]
    print("\nRule 110 (Class IV):")
    for w in test_widths:
        results = measure_periodicity(110, w, max_steps=30000, trials=3)
        found = sum(1 for r in results if r['found_cycle'])
        if found > 0:
            periods = [r['period'] for r in results if r['found_cycle']]
            print(f"  Width {w:2d}: {found}/3 found cycles, mean period = {np.mean(periods):.0f}")
        else:
            print(f"  Width {w:2d}: 0/3 found cycles")

    print("\nRule 30 (Class III):")
    for w in test_widths:
        results = measure_periodicity(30, w, max_steps=30000, trials=3)
        found = sum(1 for r in results if r['found_cycle'])
        if found > 0:
            periods = [r['period'] for r in results if r['found_cycle']]
            print(f"  Width {w:2d}: {found}/3 found cycles, mean period = {np.mean(periods):.0f}")
        else:
            print(f"  Width {w:2d}: 0/3 found cycles")

    print("\n" + "=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)

if __name__ == "__main__":
    main()
