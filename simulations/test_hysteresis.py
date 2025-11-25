#!/usr/bin/env python3
"""
Test Theory 1: Hysteresis in Pattern Boundaries

Prediction: The pattern boundary differs for going IN vs OUT.
Baseline Claude prediction: Hysteresis exists, Δk ≈ 0.005-0.015

Test protocol:
1. Find the approximate boundary at a fixed f
2. Start BELOW boundary (uniform), scan UP - find where patterns appear
3. Start ABOVE boundary (patterned), scan DOWN - find where patterns disappear
4. Compare the two boundaries
"""

import numpy as np
from reaction_diffusion import GrayScott

def has_pattern(gs, threshold_std=0.05):
    """Check if the system has a pattern (not uniform or extinct)."""
    v = gs.V
    mean_v = np.mean(v)
    std_v = np.std(v)

    if mean_v < 0.01:  # Extinction
        return False
    if std_v < threshold_std:  # Uniform
        return False
    return True

def test_hysteresis_at_f(f, k_range, k_step=0.001, equilibration_steps=3000):
    """Test for hysteresis at a fixed f value."""

    print(f"\n=== Testing hysteresis at f={f} ===")
    print(f"k range: {k_range[0]:.4f} to {k_range[1]:.4f}")

    k_values = np.arange(k_range[0], k_range[1], k_step)

    # Direction A: Start patterned (high k), scan DOWN
    print("\n[A] Starting with patterns, scanning DOWN (decreasing k)...")
    gs_down = GrayScott(size=60, f=f, k=k_range[1])
    gs_down.seed_center(radius=10)
    gs_down.run(steps=5000)  # Establish pattern

    k_pattern_dies = None
    for k in reversed(k_values):
        gs_down.k = k
        gs_down.run(steps=equilibration_steps)
        if not has_pattern(gs_down):
            k_pattern_dies = k
            print(f"  Pattern dies at k={k:.4f}")
            break

    if k_pattern_dies is None:
        print("  Pattern persisted through entire range")
        k_pattern_dies = k_range[0]

    # Direction B: Start uniform (low k), scan UP
    print("\n[B] Starting uniform, scanning UP (increasing k)...")
    gs_up = GrayScott(size=60, f=f, k=k_range[0])
    # Don't seed - start uniform
    gs_up.V = np.random.random((60, 60)) * 0.01  # Small noise
    gs_up.run(steps=2000)  # Let it settle

    k_pattern_born = None
    for k in k_values:
        gs_up.k = k
        gs_up.run(steps=equilibration_steps)
        if has_pattern(gs_up):
            k_pattern_born = k
            print(f"  Pattern born at k={k:.4f}")
            break

    if k_pattern_born is None:
        print("  No pattern formed through entire range")
        k_pattern_born = k_range[1]

    return k_pattern_dies, k_pattern_born

def main():
    print("=" * 60)
    print("HYSTERESIS TEST")
    print("=" * 60)
    print("\nBaseline prediction: Hysteresis exists, Δk ≈ 0.005-0.015")

    # Test at multiple f values
    test_points = [
        (0.030, (0.050, 0.070)),  # Low f
        (0.040, (0.055, 0.070)),  # Mid f
        (0.055, (0.060, 0.075)),  # High f
    ]

    results = []

    for f, k_range in test_points:
        k_dies, k_born = test_hysteresis_at_f(f, k_range, k_step=0.001)

        hysteresis = k_born - k_dies
        results.append({
            'f': f,
            'k_pattern_dies': k_dies,
            'k_pattern_born': k_born,
            'hysteresis_width': hysteresis
        })

        print(f"\n  RESULT at f={f}:")
        print(f"    Pattern dies (going down): k={k_dies:.4f}")
        print(f"    Pattern born (going up):   k={k_born:.4f}")
        print(f"    Hysteresis width:          Δk={hysteresis:.4f}")

        if hysteresis > 0:
            print(f"    --> HYSTERESIS DETECTED!")
        elif hysteresis < 0:
            print(f"    --> REVERSE HYSTERESIS (unexpected!)")
        else:
            print(f"    --> No hysteresis")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    avg_hysteresis = np.mean([r['hysteresis_width'] for r in results])

    print(f"\nResults across f values:")
    for r in results:
        print(f"  f={r['f']}: Δk = {r['hysteresis_width']:.4f}")

    print(f"\nAverage hysteresis width: Δk = {avg_hysteresis:.4f}")
    print(f"Baseline prediction:      Δk = 0.005-0.015")

    if avg_hysteresis > 0.003:
        print("\n✓ HYSTERESIS CONFIRMED - baseline prediction correct")
        if 0.005 <= avg_hysteresis <= 0.015:
            print("✓ Width matches baseline prediction!")
        elif avg_hysteresis < 0.005:
            print("⚠ Width SMALLER than predicted")
        else:
            print("⚠ Width LARGER than predicted")
    else:
        print("\n✗ NO SIGNIFICANT HYSTERESIS - baseline prediction WRONG")
        print("  This would be a genuine surprise!")

    return results

if __name__ == '__main__':
    results = main()
