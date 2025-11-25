#!/usr/bin/env python3
"""
Test if (k-f) is a good predictor of pattern formation.

Hypothesis: Patterns emerge when 0.02 < (k-f) < 0.04

Let's test this by:
1. Sampling points with (k-f) in the predicted range
2. Checking if they produce patterns
3. Sampling points outside the range
4. Checking if they DON'T produce patterns
"""

import numpy as np
from reaction_diffusion import GrayScott


def test_hypothesis():
    """Test the (k-f) hypothesis."""

    print("=" * 60)
    print("TESTING (k-f) HYPOTHESIS")
    print("=" * 60)
    print("\nHypothesis: Patterns emerge when 0.02 < (k-f) < 0.04")
    print()

    # Test points inside the predicted range
    inside_range = [
        (0.02, 0.045),  # k-f = 0.025
        (0.03, 0.055),  # k-f = 0.025
        (0.04, 0.065),  # k-f = 0.025
        (0.05, 0.080),  # k-f = 0.030 - but this is outside typical k range
        (0.025, 0.055), # k-f = 0.030
        (0.035, 0.060), # k-f = 0.025
        (0.045, 0.070), # k-f = 0.025
    ]

    # Test points outside the predicted range
    outside_range = [
        (0.03, 0.04),   # k-f = 0.010 (too low)
        (0.03, 0.045),  # k-f = 0.015 (too low)
        (0.03, 0.08),   # k-f = 0.050 (too high)
        (0.04, 0.05),   # k-f = 0.010 (too low)
        (0.05, 0.10),   # k-f = 0.050 (too high)
    ]

    print("--- INSIDE PREDICTED RANGE (should be patterns) ---")
    inside_correct = 0
    inside_total = len(inside_range)

    for f, k in inside_range:
        gs = GrayScott(size=60, f=f, k=k)
        gs.seed_center(radius=8)
        gs.run(steps=3000)
        m = gs.analyze()

        is_pattern = m['pattern'] == 'structured'
        mark = "v" if is_pattern else "X"

        print(f"  f={f:.3f}, k={k:.3f}, k-f={k-f:.3f}: {m['pattern']:12s} [{mark}]")

        if is_pattern:
            inside_correct += 1

    print(f"\nInside range accuracy: {inside_correct}/{inside_total} ({100*inside_correct/inside_total:.0f}%)")

    print("\n--- OUTSIDE PREDICTED RANGE (should NOT be patterns) ---")
    outside_correct = 0
    outside_total = len(outside_range)

    for f, k in outside_range:
        gs = GrayScott(size=60, f=f, k=k)
        gs.seed_center(radius=8)
        gs.run(steps=3000)
        m = gs.analyze()

        is_pattern = m['pattern'] == 'structured'
        mark = "v" if not is_pattern else "X"

        print(f"  f={f:.3f}, k={k:.3f}, k-f={k-f:.3f}: {m['pattern']:12s} [{mark}]")

        if not is_pattern:
            outside_correct += 1

    print(f"\nOutside range accuracy: {outside_correct}/{outside_total} ({100*outside_correct/outside_total:.0f}%)")

    # Overall
    total_correct = inside_correct + outside_correct
    total = inside_total + outside_total
    print(f"\n{'='*60}")
    print(f"OVERALL ACCURACY: {total_correct}/{total} ({100*total_correct/total:.0f}%)")
    print(f"{'='*60}")

    if total_correct / total > 0.8:
        print("\nThe (k-f) hypothesis has good predictive power!")
    else:
        print("\nThe (k-f) hypothesis needs refinement.")

    # Refined analysis: scan along constant (k-f) lines
    print("\n\n" + "="*60)
    print("SCANNING ALONG CONSTANT (k-f) LINES")
    print("="*60)

    for delta in [0.015, 0.020, 0.025, 0.030, 0.035, 0.040, 0.045]:
        print(f"\n--- k-f = {delta:.3f} ---")
        results = []
        for f in np.linspace(0.02, 0.06, 5):
            k = f + delta
            if k > 0.08:  # Skip invalid k
                continue
            gs = GrayScott(size=60, f=f, k=k)
            gs.seed_center(radius=8)
            gs.run(steps=3000)
            m = gs.analyze()
            char = {'structured': 'P', 'uniform': 'U', 'extinction': '.', 'filled': 'F', 'artifact': 'X'}.get(m['pattern'], '?')
            results.append(char)
            print(f"  f={f:.3f}: {char}")

        pattern_count = results.count('P')
        print(f"  Patterns: {pattern_count}/{len(results)}")


if __name__ == '__main__':
    test_hypothesis()
