#!/usr/bin/env python3
"""
Search for Genuinely Surprising Behavior

The boundary geometry work was instructive but mostly rediscovered known structure.
Let's search for something that might actually be surprising:

1. Multi-stability: Can different initial conditions produce different patterns?
2. Transient complexity: More interesting dynamics BEFORE steady state?
3. Edge of extinction: What happens at the very boundary?
4. Unusual diffusion ratios: What if Du/Dv is very different?
"""

import numpy as np
from reaction_diffusion import GrayScott
import time


def test_multistability(f: float, k: float, n_trials: int = 5):
    """
    Test if the same parameters produce different patterns from different
    initial conditions. This would indicate multi-stability.
    """
    patterns = []

    for trial in range(n_trials):
        gs = GrayScott(size=60, f=f, k=k)

        if trial == 0:
            gs.seed_center(radius=8)
        elif trial == 1:
            gs.seed_random(n_seeds=20, radius=3)
        elif trial == 2:
            # Edge seeding
            gs.V[0, :] = 1
            gs.V[-1, :] = 1
        elif trial == 3:
            # Multiple centers
            gs.seed_center(radius=5)
            for offset in [(-20, -20), (-20, 20), (20, -20), (20, 20)]:
                cx, cy = gs.size // 2 + offset[0], gs.size // 2 + offset[1]
                y, x = np.ogrid[:gs.size, :gs.size]
                mask = (x - cx)**2 + (y - cy)**2 < 5**2
                gs.V[mask] = 1
        else:
            # Random position single seed
            cx = np.random.randint(20, gs.size - 20)
            cy = np.random.randint(20, gs.size - 20)
            y, x = np.ogrid[:gs.size, :gs.size]
            mask = (x - cx)**2 + (y - cy)**2 < 8**2
            gs.V[mask] = 1

        gs.run(steps=4000)
        m = gs.analyze()
        patterns.append(m['pattern'])

    return patterns


def probe_transient_dynamics(f: float, k: float):
    """
    Look at how complexity evolves over time.
    Is there transient complexity before settling?
    """
    gs = GrayScott(size=60, f=f, k=k)
    gs.seed_center(radius=8)

    snapshots = []
    for step in range(0, 5001, 500):
        if step > 0:
            gs.run(steps=500)
        m = gs.analyze()
        snapshots.append({
            'step': step,
            'pattern': m['pattern'],
            'std': m['std_v'],
            'wavelength': m.get('wavelength', float('inf'))
        })

    return snapshots


def explore_diffusion_ratios():
    """
    Standard is Du=0.21, Dv=0.105 (ratio 2:1).
    What happens with different ratios?
    """
    print("\n=== DIFFUSION RATIO EXPLORATION ===")

    ratios = [
        (0.21, 0.21, "1:1"),
        (0.21, 0.07, "3:1"),
        (0.21, 0.05, "4:1"),
        (0.30, 0.10, "3:1 scaled"),
        (0.15, 0.15, "1:1 slow"),
    ]

    f, k = 0.035, 0.060  # Known pattern region

    for Du, Dv, name in ratios:
        # Can't use standard GrayScott - need to modify
        gs = GrayScott(size=60, f=f, k=k, Du=Du, Dv=Dv)
        gs.seed_center(radius=8)
        gs.run(steps=3000)
        m = gs.analyze()
        print(f"Du={Du}, Dv={Dv} ({name}): {m['pattern']}, wl={m.get('wavelength', 'inf'):.1f}")


def search_for_chaos():
    """
    Are there parameter regions with chaotic (non-repeating) dynamics?
    """
    print("\n=== SEARCHING FOR CHAOTIC DYNAMICS ===")

    # Known chaotic region from literature: f≈0.026, k≈0.051
    test_points = [
        (0.026, 0.051),  # Literature chaotic
        (0.024, 0.050),
        (0.028, 0.052),
        (0.020, 0.048),
        (0.030, 0.054),
    ]

    for f, k in test_points:
        gs = GrayScott(size=80, f=f, k=k)
        gs.seed_center(radius=10)

        # Run for a while, then check if still changing
        gs.run(steps=3000)
        snapshot1 = gs.V.copy()

        gs.run(steps=1000)
        snapshot2 = gs.V.copy()

        # Measure change
        change = np.abs(snapshot2 - snapshot1).mean()

        print(f"f={f}, k={k}: mean change = {change:.6f} {'(still evolving!)' if change > 0.001 else '(stable)'}")


def explore_boundary_region():
    """
    What happens RIGHT at the boundary? Phase transitions can be interesting.
    """
    print("\n=== BOUNDARY REGION EXPLORATION ===")

    # Upper boundary: k ≈ 0.13*f + 0.061
    # Let's walk along just below and just above

    for f in np.linspace(0.02, 0.06, 5):
        k_boundary = 0.13 * f + 0.061

        for dk in [-0.003, -0.001, 0, 0.001, 0.003]:
            k = k_boundary + dk
            gs = GrayScott(size=60, f=f, k=k)
            gs.seed_center(radius=8)
            gs.run(steps=3000)
            m = gs.analyze()

            char = {'structured': 'P', 'uniform': 'U', 'extinction': '.', 'filled': 'F', 'artifact': 'X'}.get(m['pattern'], '?')
            print(f"f={f:.3f}, k={k:.4f} (dk={dk:+.3f}): {char}")
        print()


if __name__ == '__main__':
    print("=" * 60)
    print("SEARCHING FOR GENUINELY SURPRISING BEHAVIOR")
    print("=" * 60)

    # Test multi-stability
    print("\n=== MULTI-STABILITY TEST ===")
    print("Testing if different initial conditions produce different patterns...")

    test_points = [
        (0.035, 0.060),  # Known pattern region
        (0.040, 0.062),  # Boundary region
        (0.030, 0.058),  # Different spot
    ]

    for f, k in test_points:
        patterns = test_multistability(f, k)
        unique_patterns = set(patterns)
        print(f"\nf={f}, k={k}:")
        print(f"  Patterns from 5 initial conditions: {patterns}")
        if len(unique_patterns) > 1:
            print(f"  *** MULTI-STABILITY DETECTED! ***")
        else:
            print(f"  Monostable (same pattern regardless of IC)")

    # Transient dynamics
    print("\n=== TRANSIENT DYNAMICS ===")
    for f, k in [(0.035, 0.060), (0.026, 0.051)]:
        print(f"\nf={f}, k={k}:")
        snapshots = probe_transient_dynamics(f, k)
        for s in snapshots:
            wl = s['wavelength'] if s['wavelength'] != float('inf') else '∞'
            print(f"  step {s['step']:4d}: {s['pattern']:12s} std={s['std']:.3f} wl={wl}")

    # Diffusion ratios
    explore_diffusion_ratios()

    # Chaos search
    search_for_chaos()

    # Boundary exploration
    explore_boundary_region()

    print("\n" + "=" * 60)
    print("SUMMARY: Looking for genuine surprises...")
    print("=" * 60)
