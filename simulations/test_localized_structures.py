#!/usr/bin/env python3
"""
Search for LOCALIZED STRUCTURES (isolated spots) in Gray-Scott.

In the homoclinic snaking regime, SINGLE SPOTS can exist stably
in an otherwise uniform background. This is different from:
- Extended spot patterns (many interacting spots)
- Stripes or labyrinths

The boundary of this regime and the behavior of localized structures
could reveal interesting dynamics:
1. Minimum stable spot size
2. Interaction between isolated spots
3. The snaking region in parameter space

Finding something unexpected here could be novel.
"""

import numpy as np
import json

Du, Dv = 0.16, 0.08
N = 128  # Large domain for isolation
dx = 1.0

def laplacian(Z, dx):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z) / (dx*dx)

def step(U, V, f, k):
    uvv = U * V * V
    return (np.clip(U + Du * laplacian(U, dx) - uvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv - (k + f) * V, 0, 1))

def init_single_spot(N, amplitude=0.3, radius=3):
    """Initialize with a single spot in the center."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    cx, cy = N // 2, N // 2

    y, x = np.ogrid[:N, :N]
    r2 = (x - cx)**2 + (y - cy)**2

    # Gaussian spot
    mask = r2 <= radius**2
    U[mask] = 1.0 - amplitude
    V[mask] = amplitude

    return U, V

def init_two_spots(N, amplitude=0.3, radius=3, separation=30):
    """Initialize with two spots at specified separation."""
    U, V = np.ones((N, N)), np.zeros((N, N))

    y, x = np.ogrid[:N, :N]

    # First spot
    cx1, cy1 = N // 2 - separation // 2, N // 2
    r2_1 = (x - cx1)**2 + (y - cy1)**2
    mask1 = r2_1 <= radius**2
    U[mask1] = 1.0 - amplitude
    V[mask1] = amplitude

    # Second spot
    cx2, cy2 = N // 2 + separation // 2, N // 2
    r2_2 = (x - cx2)**2 + (y - cy2)**2
    mask2 = r2_2 <= radius**2
    U[mask2] = 1.0 - amplitude
    V[mask2] = amplitude

    return U, V

def count_spots(V, threshold=0.05):
    """Count the number of distinct high-V regions."""
    binary = (V > threshold).astype(int)

    # Simple flood-fill counting
    visited = np.zeros_like(binary, dtype=bool)
    count = 0

    def flood_fill(i, j):
        stack = [(i, j)]
        while stack:
            ci, cj = stack.pop()
            if ci < 0 or ci >= N or cj < 0 or cj >= N:
                continue
            if visited[ci, cj] or binary[ci, cj] == 0:
                continue
            visited[ci, cj] = True
            stack.extend([(ci+1, cj), (ci-1, cj), (ci, cj+1), (ci, cj-1)])

    for i in range(N):
        for j in range(N):
            if binary[i, j] == 1 and not visited[i, j]:
                flood_fill(i, j)
                count += 1

    return count

def measure_spot_properties(V, threshold=0.05):
    """Measure properties of the spots."""
    binary = (V > threshold).astype(int)
    total_area = np.sum(binary)

    if total_area == 0:
        return {'exists': False}

    # Center of mass
    y_indices, x_indices = np.where(V > threshold)
    if len(y_indices) == 0:
        return {'exists': False}

    com_y = np.mean(y_indices)
    com_x = np.mean(x_indices)

    # Max V value
    max_v = np.max(V)

    return {
        'exists': True,
        'area': int(total_area),
        'max_v': float(max_v),
        'com': (float(com_x), float(com_y))
    }

def test_single_spot_stability(f, k, n_steps=50000):
    """Test if a single spot survives or dies/grows."""
    U, V = init_single_spot(N)

    for _ in range(n_steps):
        U, V = step(U, V, f, k)

    # Analyze final state
    n_spots = count_spots(V)
    props = measure_spot_properties(V)

    if not props['exists']:
        return 'decayed', props
    elif n_spots == 1 and props['area'] < 200:
        return 'stable_single', props
    elif n_spots == 1 and props['area'] >= 200:
        return 'grew_single', props
    elif n_spots > 1:
        return f'split_into_{n_spots}', props
    else:
        return 'other', props

def test_spot_interaction(f, k, separation, n_steps=50000):
    """Test how two spots interact at given separation."""
    U, V = init_two_spots(N, separation=separation)

    for _ in range(n_steps):
        U, V = step(U, V, f, k)

    n_spots = count_spots(V)
    props = measure_spot_properties(V)

    return n_spots, props

def main():
    print("=" * 70)
    print("LOCALIZED STRUCTURES ANALYSIS")
    print("=" * 70)
    print()
    print("Testing stability of isolated spots and their interactions")
    print()

    # Test single spot stability across parameter space
    print("SINGLE SPOT STABILITY")
    print("-" * 70)

    test_points = [
        (0.030, 0.055),
        (0.035, 0.058),
        (0.040, 0.060),
        (0.045, 0.062),
        (0.050, 0.065),
        (0.055, 0.067),
        (0.028, 0.054),
        (0.032, 0.056),
    ]

    single_spot_results = []
    for f, k in test_points:
        print(f"f={f:.3f}, k={k:.3f}...", end=" ", flush=True)
        outcome, props = test_single_spot_stability(f, k)
        print(f"{outcome}")
        single_spot_results.append({
            'f': f, 'k': k, 'outcome': outcome,
            'props': props if props['exists'] else {}
        })

    # Find where isolated spots are stable
    stable_points = [r for r in single_spot_results if r['outcome'] == 'stable_single']

    print()
    print(f"Found {len(stable_points)} parameter points with stable single spots")

    if stable_points:
        print()
        print("SPOT INTERACTION TEST")
        print("-" * 70)
        print("Testing how two spots interact at different separations")
        print()

        # Use first stable point
        f, k = stable_points[0]['f'], stable_points[0]['k']
        print(f"Using f={f}, k={k}")

        separations = [15, 20, 25, 30, 40, 50]
        interaction_results = []

        for sep in separations:
            print(f"  Separation {sep}...", end=" ", flush=True)
            n_spots, props = test_spot_interaction(f, k, sep)
            print(f"{n_spots} spots remain")
            interaction_results.append({
                'separation': sep,
                'final_spots': n_spots,
                'props': props if props['exists'] else {}
            })

        # Analyze interaction
        print()
        print("INTERACTION ANALYSIS")
        print("-" * 40)

        # Find critical separation where spots start interacting
        critical_sep = None
        for i, r in enumerate(interaction_results):
            if r['final_spots'] != 2:
                if i > 0:
                    critical_sep = (interaction_results[i-1]['separation'] + r['separation']) / 2
                break

        if critical_sep:
            print(f"Critical separation (merge distance): ~{critical_sep:.0f} pixels")
            print()
            print("This defines the 'interaction range' of spots")
        else:
            print("Spots remain separate at all tested separations")

    print()
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print()

    # Count outcomes
    outcomes = {}
    for r in single_spot_results:
        outcomes[r['outcome']] = outcomes.get(r['outcome'], 0) + 1

    print("Single spot outcomes:")
    for outcome, count in sorted(outcomes.items()):
        print(f"  {outcome}: {count}")

    # Save results
    results = {
        'single_spot_tests': single_spot_results,
        'interaction_tests': interaction_results if stable_points else [],
        'outcomes': outcomes
    }

    with open('localized_structure_results.json', 'w') as file:
        json.dump(results, file, indent=2, default=str)

    print()
    print("Results saved to localized_structure_results.json")

if __name__ == '__main__':
    main()
