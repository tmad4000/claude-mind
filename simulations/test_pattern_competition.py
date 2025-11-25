#!/usr/bin/env python3
"""
Test PATTERN COMPETITION in Gray-Scott.

In the bistable region, spots and stripes can both be stable.
What happens when they compete? Starting from mixed initial conditions,
which pattern type wins?

This could reveal:
1. Basin boundary structure (which IC leads to which pattern)
2. Dominance hierarchy between pattern types
3. Coexistence dynamics (fronts between patterns)
4. Parameter-dependent selection

Finding universal rules for pattern competition could be novel.
"""

import numpy as np
import json

Du, Dv = 0.16, 0.08
N = 128  # Large domain for competition
dx = 1.0

def laplacian(Z, dx):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z) / (dx*dx)

def step(U, V, f, k):
    uvv = U * V * V
    return (np.clip(U + Du * laplacian(U, dx) - uvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv - (k + f) * V, 0, 1))

def init_spots_left_stripes_right(N):
    """Initialize with spots on left, stripes on right."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    np.random.seed(42)

    # Left half: spots
    for _ in range(20):
        cx = np.random.randint(5, N//2 - 5)
        cy = np.random.randint(5, N - 5)
        r = 4
        y, x = np.ogrid[:N, :N]
        mask = (x-cx)**2 + (y-cy)**2 <= r*r
        U[mask], V[mask] = 0.5, 0.25

    # Right half: vertical stripes
    for i in range(N//2 + 5, N - 5, 12):
        U[:, i-2:i+3] = 0.5
        V[:, i-2:i+3] = 0.25

    return U, V

def init_spots_top_stripes_bottom(N):
    """Initialize with spots on top, stripes on bottom."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    np.random.seed(43)

    # Top half: spots
    for _ in range(20):
        cx = np.random.randint(5, N - 5)
        cy = np.random.randint(5, N//2 - 5)
        r = 4
        y, x = np.ogrid[:N, :N]
        mask = (x-cx)**2 + (y-cy)**2 <= r*r
        U[mask], V[mask] = 0.5, 0.25

    # Bottom half: horizontal stripes
    for i in range(N//2 + 5, N - 5, 12):
        U[i-2:i+3, :] = 0.5
        V[i-2:i+3, :] = 0.25

    return U, V

def classify_pattern_type(V):
    """Determine if pattern is more spot-like or stripe-like."""
    v_std = np.std(V)
    if v_std < 0.02:
        return 'uniform', 0.0

    V_centered = V - np.mean(V)
    fft = np.fft.fft2(V_centered)
    power = np.abs(np.fft.fftshift(fft))**2

    N = V.shape[0]
    center = N // 2
    power[center-2:center+3, center-2:center+3] = 0

    # Analyze anisotropy: spots have isotropic power, stripes are anisotropic
    # Calculate ratio of power in x vs y directions

    # Power along horizontal and vertical axes
    horiz_power = np.sum(power[center-3:center+4, :])
    vert_power = np.sum(power[:, center-3:center+4])
    total_power = np.sum(power)

    axis_power = (horiz_power + vert_power) / total_power

    # High axis_power = stripes (anisotropic)
    # Low axis_power = spots (isotropic)

    if axis_power > 0.4:
        return 'stripes', axis_power
    elif axis_power < 0.2:
        return 'spots', axis_power
    else:
        return 'mixed', axis_power

def measure_domain_sizes(V, threshold=0.05):
    """Measure how much of the domain has each pattern type."""
    # Left half
    left_half = V[:, :V.shape[1]//2]
    left_mean = np.mean(left_half > threshold)

    # Right half
    right_half = V[:, V.shape[1]//2:]
    right_mean = np.mean(right_half > threshold)

    return left_mean, right_mean

def run_competition(f, k, init_func, n_steps=100000, track_interval=5000):
    """Run pattern competition and track evolution."""
    U, V = init_func(N)

    history = []

    for step_num in range(n_steps):
        U, V = step(U, V, f, k)

        if step_num % track_interval == 0:
            pattern_type, anisotropy = classify_pattern_type(V)
            left_frac, right_frac = measure_domain_sizes(V)

            history.append({
                'step': step_num,
                'pattern_type': pattern_type,
                'anisotropy': float(anisotropy),
                'left_frac': float(left_frac),
                'right_frac': float(right_frac)
            })

    return history, classify_pattern_type(V)

def main():
    print("=" * 70)
    print("PATTERN COMPETITION ANALYSIS")
    print("=" * 70)
    print()
    print("Testing which pattern type wins when starting from mixed ICs...")
    print()

    # Test at bistable points
    test_points = [
        (0.030, 0.057),
        (0.035, 0.060),
        (0.040, 0.062),
        (0.045, 0.064),
        (0.032, 0.058),
        (0.038, 0.061),
    ]

    results = []

    print(f"{'f':>6} {'k':>6} {'init':>15} {'winner':>12} {'anisotropy':>12}")
    print("-" * 55)

    for f, k in test_points:
        # Test both initial conditions
        for init_name, init_func in [
            ('left_spots', init_spots_left_stripes_right),
            ('top_spots', init_spots_top_stripes_bottom)
        ]:
            history, (final_type, final_aniso) = run_competition(f, k, init_func)

            print(f"{f:6.3f} {k:6.3f} {init_name:>15} {final_type:>12} {final_aniso:12.4f}")

            results.append({
                'f': float(f),
                'k': float(k),
                'init_type': init_name,
                'final_pattern': final_type,
                'final_anisotropy': float(final_aniso),
                'history': history
            })

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    # Count winners
    winners = {}
    for r in results:
        w = r['final_pattern']
        winners[w] = winners.get(w, 0) + 1

    print("Final pattern counts:")
    for w, c in sorted(winners.items(), key=lambda x: -x[1]):
        print(f"  {w}: {c}")

    # Check if winner depends on parameters
    spots_wins = [r for r in results if r['final_pattern'] == 'spots']
    stripes_wins = [r for r in results if r['final_pattern'] == 'stripes']

    if spots_wins and stripes_wins:
        print()
        print("INTERESTING: Both spots and stripes can win!")
        print()

        spots_f = np.mean([r['f'] for r in spots_wins])
        stripes_f = np.mean([r['f'] for r in stripes_wins])

        print(f"Spots win more often at f ≈ {spots_f:.3f}")
        print(f"Stripes win more often at f ≈ {stripes_f:.3f}")

        # Check for selection rule
        if spots_f < stripes_f:
            print()
            print("POSSIBLE RULE: Lower f favors spots, higher f favors stripes")
        elif stripes_f < spots_f:
            print()
            print("POSSIBLE RULE: Lower f favors stripes, higher f favors spots")

    # Save results
    with open('pattern_competition_results.json', 'w') as file:
        # Simplify history for JSON
        clean_results = []
        for r in results:
            clean_r = {k: v for k, v in r.items() if k != 'history'}
            clean_r['history'] = r['history'][::2]  # Sample every other
            clean_results.append(clean_r)

        json.dump({
            'results': clean_results,
            'winners': winners
        }, file, indent=2)

    print()
    print("Results saved to pattern_competition_results.json")

if __name__ == '__main__':
    main()
