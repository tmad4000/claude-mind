#!/usr/bin/env python3
"""
Visualize the chaotic dynamics to understand what's happening.
Is it spatiotemporal chaos or global oscillation?
"""

import numpy as np
from reaction_diffusion import GrayScott, visualize_ascii


def visualize_chaos_evolution(f: float = 0.026, k: float = 0.051, interval: int = 200):
    """
    Show ASCII snapshots of chaotic evolution.
    """
    print(f"=== CHAOS VISUALIZATION: f={f}, k={k} ===\n")

    gs = GrayScott(size=60, f=f, k=k)
    gs.seed_center(radius=12)

    for step in range(0, 3001, interval):
        if step > 0:
            gs.run(steps=interval)

        m = gs.analyze()
        print(f"\n--- Step {step} ---")
        print(f"Pattern: {m['pattern']}, std: {m['std_v']:.3f}, mean: {m['mean_v']:.3f}")
        print(visualize_ascii(gs, width=50))


def measure_local_activity(f: float = 0.026, k: float = 0.051):
    """
    Measure how much activity is LOCAL vs GLOBAL.
    If chaos is spatiotemporal, different regions should be out of phase.
    """
    print(f"\n=== LOCAL VS GLOBAL ACTIVITY ===\n")

    gs = GrayScott(size=80, f=f, k=k)
    gs.seed_random(n_seeds=30, radius=4)
    gs.run(steps=1000)

    # Take two snapshots
    snapshot1 = gs.V.copy()
    gs.run(steps=200)
    snapshot2 = gs.V.copy()

    # Measure local change in different quadrants
    size = gs.size
    quadrants = [
        ('Top-left', snapshot1[:size//2, :size//2], snapshot2[:size//2, :size//2]),
        ('Top-right', snapshot1[:size//2, size//2:], snapshot2[:size//2, size//2:]),
        ('Bot-left', snapshot1[size//2:, :size//2], snapshot2[size//2:, :size//2]),
        ('Bot-right', snapshot1[size//2:, size//2:], snapshot2[size//2:, size//2:]),
    ]

    print("Change in different regions over 200 steps:")
    for name, v1, v2 in quadrants:
        change = np.abs(v2 - v1).mean()
        print(f"  {name}: {change:.4f}")

    global_change = np.abs(snapshot2 - snapshot1).mean()
    print(f"\n  Global mean change: {global_change:.4f}")

    # Check correlation between quadrants
    changes = [np.abs(v2 - v1) for _, v1, v2 in quadrants]
    print("\nIf changes are correlated, chaos is global. If uncorrelated, it's local.")


def track_mass_over_time(f: float = 0.026, k: float = 0.051, steps: int = 5000):
    """
    Track total V mass over time to see oscillation structure.
    """
    print(f"\n=== V MASS OSCILLATION ===\n")

    gs = GrayScott(size=60, f=f, k=k)
    gs.seed_center(radius=10)

    masses = []
    stds = []

    for step in range(0, steps + 1, 50):
        if step > 0:
            gs.run(steps=50)
        masses.append(gs.V.sum())
        stds.append(gs.V.std())

    # Print as a simple time series
    print("Time series of total V mass (normalized):")
    max_mass = max(masses)
    for i in range(0, len(masses), 10):
        bar_len = int(50 * masses[i] / max_mass)
        print(f"step {i*50:4d}: {'#' * bar_len}")

    # Look for periodicity
    masses_arr = np.array(masses)
    masses_centered = masses_arr - masses_arr.mean()

    # Autocorrelation
    autocorr = np.correlate(masses_centered, masses_centered, mode='full')
    autocorr = autocorr[len(autocorr)//2:]
    autocorr = autocorr / autocorr[0]

    # Find period (first peak after lag 0)
    for i in range(2, min(50, len(autocorr)-1)):
        if autocorr[i] > autocorr[i-1] and autocorr[i] > autocorr[i+1]:
            print(f"\nFirst autocorr peak at lag {i} (period ≈ {i * 50} steps)")
            break
    else:
        print("\nNo clear periodicity detected - possibly chaotic (aperiodic)")


def compare_chaos_and_patterns():
    """
    Compare the chaotic region with the pattern region.
    """
    print("\n=== CHAOS vs PATTERNS ===\n")

    comparison = [
        ("Chaotic", 0.026, 0.051),
        ("Pattern (spots)", 0.035, 0.060),
        ("Pattern (maze)", 0.029, 0.057),
    ]

    for name, f, k in comparison:
        gs = GrayScott(size=60, f=f, k=k)
        gs.seed_center(radius=10)

        # Run to near-steady state
        gs.run(steps=3000)
        v1 = gs.V.copy()

        # Run more
        gs.run(steps=1000)
        v2 = gs.V.copy()

        change = np.abs(v2 - v1).mean()
        m = gs.analyze()

        print(f"\n{name} (f={f}, k={k}):")
        print(f"  After 4000 steps: pattern={m['pattern']}, std={m['std_v']:.3f}")
        print(f"  Change over last 1000 steps: {change:.4f}")
        print(f"  {'>>> STILL EVOLVING <<<' if change > 0.01 else '(stable)'}")


if __name__ == '__main__':
    # Compare chaos vs patterns first (quick)
    compare_chaos_and_patterns()

    # Track mass oscillation
    track_mass_over_time()

    # Local vs global activity
    measure_local_activity()

    # Detailed visualization (optional - takes more time)
    print("\n\n" + "="*60)
    print("SHOWING SNAPSHOTS OF CHAOTIC EVOLUTION")
    print("="*60)
    visualize_chaos_evolution(interval=400)
