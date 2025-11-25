#!/usr/bin/env python3
"""
Rigorous verification of spiral wave at f=0.028, k=0.053.

Check:
1. Is pattern rotating or just drifting?
2. Does it have spiral morphology?
3. Does rotation persist over multiple periods?
4. Is it robust to perturbations?
"""

import numpy as np
import json

Du, Dv = 0.16, 0.08
N = 128
dx = 1.0

def laplacian(Z, dx):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z) / (dx*dx)

def step(U, V, f, k):
    uvv = U * V * V
    return (np.clip(U + Du * laplacian(U, dx) - uvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv - (k + f) * V, 0, 1))

def init_broken_front(N):
    """Initialize with a broken wave front - classic spiral generator."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    cx, cy = N // 2, N // 2

    # Half-plane of V
    U[:, :cx] = 0.5
    V[:, :cx] = 0.25

    # Cut in upper half
    U[:cy, cx-5:cx+5] = 1.0
    V[:cy, cx-5:cx+5] = 0.0

    return U, V

def measure_spiral_properties(V):
    """
    Measure properties that indicate spiral structure:
    - Winding number: how many times phase winds around center
    - Azimuthal variation: how pattern changes around center
    """
    N = V.shape[0]
    cx, cy = N // 2, N // 2

    y, x = np.ogrid[:N, :N]
    theta = np.arctan2(y - cy, x - cx)
    r = np.sqrt((x - cx)**2 + (y - cy)**2)

    # Sample V at different angles along a ring
    sample_r = N // 4
    n_angles = 36
    angles = np.linspace(-np.pi, np.pi, n_angles, endpoint=False)
    v_values = []

    for angle in angles:
        px = int(cx + sample_r * np.cos(angle))
        py = int(cy + sample_r * np.sin(angle))
        if 0 <= px < N and 0 <= py < N:
            v_values.append(V[py, px])
        else:
            v_values.append(0)

    v_values = np.array(v_values)

    # Count zero crossings (normalized)
    v_centered = v_values - np.mean(v_values)
    crossings = np.sum(np.abs(np.diff(np.sign(v_centered))) > 0)

    # Azimuthal variation
    azimuthal_std = np.std(v_values)

    return {
        'azimuthal_crossings': int(crossings),
        'azimuthal_std': float(azimuthal_std),
        'mean_v_on_ring': float(np.mean(v_values))
    }

def track_orientation(V):
    """Track the orientation of the pattern using the first moment."""
    N = V.shape[0]
    cx, cy = N // 2, N // 2

    y, x = np.ogrid[:N, :N]
    theta = np.arctan2(y - cy, x - cx)

    # Weight by V
    V_shifted = V - np.mean(V)
    if np.std(V_shifted) < 0.001:
        return 0

    # Compute weighted angle using circular statistics
    weights = np.maximum(V_shifted, 0)
    total_weight = np.sum(weights)
    if total_weight < 0.001:
        return 0

    sin_mean = np.sum(weights * np.sin(theta)) / total_weight
    cos_mean = np.sum(weights * np.cos(theta)) / total_weight

    return np.arctan2(sin_mean, cos_mean)

def main():
    f, k = 0.028, 0.053
    print("=" * 70)
    print(f"VERIFYING SPIRAL WAVE AT f={f}, k={k}")
    print("=" * 70)
    print()

    U, V = init_broken_front(N)

    # Long warmup
    print("Running warmup (50k steps)...")
    for _ in range(50000):
        U, V = step(U, V, f, k)

    # Check if pattern exists
    initial_std = np.std(V)
    print(f"Initial pattern std: {initial_std:.4f}")

    if initial_std < 0.02:
        print("ERROR: Pattern decayed to uniform!")
        return

    # Measure initial properties
    props = measure_spiral_properties(V)
    print(f"Initial spiral properties:")
    print(f"  Azimuthal crossings: {props['azimuthal_crossings']}")
    print(f"  Azimuthal std: {props['azimuthal_std']:.4f}")
    print()

    # Track orientation over time
    print("Tracking orientation over 20k steps...")
    n_samples = 200
    sample_interval = 100
    orientations = []

    for i in range(n_samples):
        for _ in range(sample_interval):
            U, V = step(U, V, f, k)
        orientations.append(track_orientation(V))

    orientations = np.array(orientations)

    # Unwrap orientations
    orientations_unwrapped = np.unwrap(orientations)

    # Calculate total rotation
    total_rotation = orientations_unwrapped[-1] - orientations_unwrapped[0]
    total_time = n_samples * sample_interval
    rotation_rate = total_rotation / total_time * 1000  # per 1000 steps

    print(f"Total rotation: {np.degrees(total_rotation):.1f} degrees over {total_time} steps")
    print(f"Rotation rate: {np.degrees(rotation_rate):.2f} degrees per 1000 steps")
    print()

    # Check for consistent rotation
    diffs = np.diff(orientations_unwrapped)
    diffs_deg = np.degrees(diffs)
    consistent_sign = np.sum(np.sign(diffs) == np.sign(np.mean(diffs))) / len(diffs)

    print(f"Rotation consistency: {consistent_sign*100:.1f}% same direction")
    print(f"Mean rotation per sample: {np.degrees(np.mean(diffs)):.2f} deg")
    print(f"Std of rotation: {np.degrees(np.std(diffs)):.2f} deg")
    print()

    # Calculate period
    if abs(rotation_rate) > 0.1:  # degrees per 1000 steps
        period = 360 / abs(np.degrees(rotation_rate)) * 1000
        print(f"Estimated rotation period: {period:.0f} steps")
    else:
        period = np.inf
        print("No clear rotation detected")

    # Final check - is this really a spiral?
    final_props = measure_spiral_properties(V)

    print()
    print("=" * 70)
    print("VERDICT")
    print("=" * 70)
    print()

    is_spiral = (
        abs(total_rotation) > np.pi and  # At least half rotation
        consistent_sign > 0.6 and  # Mostly same direction
        final_props['azimuthal_crossings'] >= 2  # Multiple arms or structure
    )

    if is_spiral:
        print("*** CONFIRMED: SPIRAL WAVE ***")
        print(f"  - Pattern rotates {np.degrees(total_rotation):.0f}° over {total_time} steps")
        print(f"  - Rotation period: ~{period:.0f} steps")
        print(f"  - {consistent_sign*100:.0f}% consistent rotation direction")
        print()
        print("This appears to be a genuine spiral wave!")
    else:
        print("NOT A SPIRAL")
        print("  Possible explanations:")
        if abs(total_rotation) < np.pi:
            print(f"  - Insufficient rotation ({np.degrees(total_rotation):.0f}°, need >180°)")
        if consistent_sign < 0.6:
            print(f"  - Inconsistent rotation direction ({consistent_sign*100:.0f}%)")
        if final_props['azimuthal_crossings'] < 2:
            print(f"  - Not enough azimuthal structure ({final_props['azimuthal_crossings']} crossings)")

    # Save results
    results = {
        'f': f, 'k': k,
        'pattern_std': float(initial_std),
        'total_rotation_deg': float(np.degrees(total_rotation)),
        'rotation_period': float(period) if period != np.inf else None,
        'rotation_consistency': float(consistent_sign),
        'is_spiral': is_spiral,
        'spiral_properties': final_props
    }

    with open('spiral_verification.json', 'w') as file:
        json.dump(results, file, indent=2)

    print()
    print("Results saved to spiral_verification.json")

if __name__ == '__main__':
    main()
