#!/usr/bin/env python3
"""
Search for SPIRAL WAVES in Gray-Scott.

Spiral waves are rotating patterns that are topologically distinct from
spots and stripes. They exist in Belousov-Zhabotinsky reactions but are
less commonly reported in Gray-Scott.

Finding stable spirals in Gray-Scott would be genuinely novel if they
exist in a robust parameter region.

Strategy:
1. Seed with a spiral-like initial condition
2. See if it stabilizes into a rotating spiral
3. Or see if other ICs spontaneously generate spirals
"""

import numpy as np
import json

Du, Dv = 0.16, 0.08
N = 128  # Larger domain for spirals
dx = 1.0

def laplacian(Z, dx):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z) / (dx*dx)

def step(U, V, f, k):
    uvv = U * V * V
    return (np.clip(U + Du * laplacian(U, dx) - uvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv - (k + f) * V, 0, 1))

def init_spiral_seed(N):
    """
    Initialize with a broken wavefront that could curl into a spiral.
    """
    U, V = np.ones((N, N)), np.zeros((N, N))
    cx, cy = N // 2, N // 2

    y, x = np.ogrid[:N, :N]
    # Create an Archimedean spiral seed
    theta = np.arctan2(y - cy, x - cx)
    r = np.sqrt((x - cx)**2 + (y - cy)**2)

    # Spiral arm
    arm_width = 3
    for phase in [0]:
        spiral_r = (theta + phase) / (2 * np.pi) * 15 + 10
        mask = (np.abs(r - spiral_r) < arm_width) & (r < N//3)
        U[mask] = 0.5
        V[mask] = 0.25

    return U, V

def init_broken_front(N):
    """
    Initialize with a broken wave front - classic spiral generator.
    """
    U, V = np.ones((N, N)), np.zeros((N, N))
    cx, cy = N // 2, N // 2

    # Half-plane of V
    U[:, :cx] = 0.5
    V[:, :cx] = 0.25

    # Cut in upper half
    U[:cy, cx-5:cx+5] = 1.0
    V[:cy, cx-5:cx+5] = 0.0

    return U, V

def init_vortex_pair(N):
    """
    Initialize with two counter-rotating vortex seeds.
    """
    U, V = np.ones((N, N)), np.zeros((N, N))

    y, x = np.ogrid[:N, :N]

    # First vortex
    cx1, cy1 = N//3, N//2
    theta1 = np.arctan2(y - cy1, x - cx1)
    r1 = np.sqrt((x - cx1)**2 + (y - cy1)**2)
    mask1 = (theta1 > 0) & (r1 < 15)
    U[mask1] = 0.5
    V[mask1] = 0.25

    # Second vortex (opposite chirality)
    cx2, cy2 = 2*N//3, N//2
    theta2 = np.arctan2(y - cy2, x - cx2)
    r2 = np.sqrt((x - cx2)**2 + (y - cy2)**2)
    mask2 = (theta2 < 0) & (r2 < 15)
    U[mask2] = 0.5
    V[mask2] = 0.25

    return U, V

def detect_rotation(V_history):
    """
    Detect if the pattern is rotating by tracking the center of mass
    of V in different sectors.
    """
    n_frames = len(V_history)
    N = V_history[0].shape[0]
    cx, cy = N // 2, N // 2

    y, x = np.ogrid[:N, :N]
    theta = np.arctan2(y - cy, x - cx)

    # Track center of mass angle over time
    angles = []
    for V in V_history:
        # Weight by V
        V_centered = V - np.mean(V)
        if np.sum(np.abs(V_centered)) < 0.01:
            angles.append(0)
            continue

        # Compute weighted average angle
        weights = np.abs(V_centered)
        weighted_sin = np.sum(weights * np.sin(theta))
        weighted_cos = np.sum(weights * np.cos(theta))
        avg_angle = np.arctan2(weighted_sin, weighted_cos)
        angles.append(avg_angle)

    angles = np.array(angles)

    # Check for rotation: should see monotonic change in angle
    # Account for wraparound
    angle_diffs = np.diff(angles)
    # Unwrap
    angle_diffs = np.where(angle_diffs > np.pi, angle_diffs - 2*np.pi, angle_diffs)
    angle_diffs = np.where(angle_diffs < -np.pi, angle_diffs + 2*np.pi, angle_diffs)

    # Consistent rotation means most diffs have same sign
    positive_diffs = np.sum(angle_diffs > 0.01)
    negative_diffs = np.sum(angle_diffs < -0.01)
    total_diffs = len(angle_diffs)

    if max(positive_diffs, negative_diffs) > 0.7 * total_diffs:
        rotation_rate = np.mean(angle_diffs)  # radians per sample
        return True, rotation_rate
    return False, 0

def test_for_spirals(f, k, init_func, warmup=30000, observe=10000, sample_interval=200):
    """Test if spiral waves form and persist."""
    U, V = init_func(N)

    # Warmup
    for _ in range(warmup):
        U, V = step(U, V, f, k)

    # Check if pattern exists
    if np.std(V) < 0.02:
        return 'uniform', {}

    # Collect snapshots
    V_history = []
    for i in range(observe):
        U, V = step(U, V, f, k)
        if i % sample_interval == 0:
            V_history.append(V.copy())

    # Check for rotation
    is_rotating, rotation_rate = detect_rotation(V_history)

    if is_rotating:
        period = 2 * np.pi / np.abs(rotation_rate) * sample_interval if rotation_rate != 0 else np.inf
        return 'spiral', {
            'rotation_rate': float(rotation_rate),
            'period_steps': float(period),
            'pattern_std': float(np.std(V))
        }

    # Check for other dynamic patterns
    v_means = [np.mean(v) for v in V_history]
    variation = np.std(v_means)

    if variation > 0.001:
        return 'dynamic', {'variation': float(variation)}
    else:
        return 'static', {'pattern_std': float(np.std(V))}

def main():
    print("=" * 70)
    print("SEARCHING FOR SPIRAL WAVES IN GRAY-SCOTT")
    print("=" * 70)
    print()
    print("Spirals are rotating patterns that would be topologically distinct")
    print("from spots and stripes. Testing with spiral-inducing initial conditions.")
    print()

    # Test parameters - include known dynamic regions
    test_points = [
        # Near chaos region (more likely to have excitable dynamics)
        (0.024, 0.050),
        (0.026, 0.052),
        (0.028, 0.053),
        # Pattern region
        (0.030, 0.055),
        (0.035, 0.058),
        (0.040, 0.060),
        # Lower f (might be more excitable)
        (0.018, 0.045),
        (0.020, 0.048),
        (0.022, 0.050),
    ]

    init_funcs = [
        ('spiral_seed', init_spiral_seed),
        ('broken_front', init_broken_front),
        ('vortex_pair', init_vortex_pair),
    ]

    results = []
    spirals_found = []

    for f, k in test_points:
        print(f"\nTesting f={f:.3f}, k={k:.3f}")
        print("-" * 40)

        for name, init_func in init_funcs:
            pattern_type, details = test_for_spirals(f, k, init_func)
            results.append({
                'f': f, 'k': k,
                'init': name,
                'type': pattern_type,
                'details': details
            })

            marker = {
                'spiral': '★',
                'dynamic': '~',
                'static': '○',
                'uniform': '×'
            }.get(pattern_type, '?')

            if pattern_type == 'spiral':
                spirals_found.append((f, k, name, details))
                print(f"  {name}: ★ SPIRAL! period={details['period_steps']:.0f} steps")
            else:
                print(f"  {name}: {marker} {pattern_type}")

    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print()

    if spirals_found:
        print("*** SPIRAL WAVES FOUND! ***")
        print("-" * 40)
        for f, k, init_name, details in spirals_found:
            print(f"  f={f:.3f}, k={k:.3f} (from {init_name})")
            print(f"    Rotation period: {details['period_steps']:.0f} steps")
            print()

        print("Significance:")
        print("  Stable spiral waves in Gray-Scott would be a distinct pattern type")
        print("  Most GS literature focuses on spots, stripes, and chaos")
        print("  Spirals would add to the known pattern zoo")
    else:
        print("No spiral waves found in tested region.")
        print()
        # Summary
        types = {}
        for r in results:
            types[r['type']] = types.get(r['type'], 0) + 1
        print("Pattern types found:")
        for t, c in sorted(types.items(), key=lambda x: -x[1]):
            print(f"  {t}: {c}")

    # Save results
    with open('spiral_wave_results.json', 'w') as file:
        json.dump({
            'results': results,
            'spirals_found': [(f, k, name) for f, k, name, _ in spirals_found],
        }, file, indent=2)

    print()
    print("Results saved to spiral_wave_results.json")

if __name__ == '__main__':
    main()
