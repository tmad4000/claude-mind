#!/usr/bin/env python3
"""
Search for BREATHING/PULSATING patterns in Gray-Scott.

These would be spatially periodic patterns that oscillate in amplitude
over time in a REGULAR way (limit cycle), not chaotic.

Characteristics:
- Spatial structure persists (spots stay spots)
- Amplitude varies periodically
- Different from chaos (regular, predictable oscillations)

This would be distinct from:
- Static patterns (no oscillation)
- Chaotic dynamics (irregular oscillation)
- Traveling waves (pattern moves)

Finding breathing spots would be genuinely interesting if they exist
in a stable parameter region.
"""

import numpy as np
import json

Du, Dv = 0.16, 0.08
N = 64
dx = 1.0

def laplacian(Z, dx):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z) / (dx*dx)

def step(U, V, f, k):
    uvv = U * V * V
    return (np.clip(U + Du * laplacian(U, dx) - uvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv - (k + f) * V, 0, 1))

def init_spots(N, n=5):
    """Single well-separated spots."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    # Place spots on a regular grid
    spacing = N // 3
    for i in range(2):
        for j in range(2):
            cx = spacing + i * spacing
            cy = spacing + j * spacing
            r = 3
            y, x = np.ogrid[:N, :N]
            mask = ((np.minimum(np.abs(x-cx), N-np.abs(x-cx)))**2 +
                    (np.minimum(np.abs(y-cy), N-np.abs(y-cy)))**2) <= r*r
            U[mask], V[mask] = 0.5, 0.25
    return U, V

def analyze_dynamics(f, k, warmup=20000, measure=10000, sample_interval=50):
    """
    Analyze the temporal dynamics of the pattern.
    Returns: (pattern_type, details)
    """
    U, V = init_spots(N)

    # Warmup
    for _ in range(warmup):
        U, V = step(U, V, f, k)

    # Check if pattern exists
    if np.std(V) < 0.02:
        return 'uniform', {'final_std': float(np.std(V))}

    # Collect time series from a single spot
    # Find where V is highest
    max_idx = np.unravel_index(np.argmax(V), V.shape)

    v_at_spot = []
    v_means = []
    v_stds = []

    for i in range(measure):
        U, V = step(U, V, f, k)
        if i % sample_interval == 0:
            v_at_spot.append(V[max_idx])
            v_means.append(np.mean(V))
            v_stds.append(np.std(V))

    v_at_spot = np.array(v_at_spot)
    v_means = np.array(v_means)
    v_stds = np.array(v_stds)

    # Analyze for oscillations
    spot_variation = np.std(v_at_spot)
    mean_variation = np.std(v_means)

    if spot_variation < 1e-5:
        return 'static', {
            'spot_variation': float(spot_variation),
            'final_spot_value': float(v_at_spot[-1]),
            'pattern_std': float(np.std(V))
        }

    # Check for regularity via autocorrelation
    v_centered = v_at_spot - np.mean(v_at_spot)
    if np.std(v_centered) < 1e-8:
        return 'static', {'spot_variation': float(spot_variation)}

    autocorr = np.correlate(v_centered, v_centered, mode='full')
    autocorr = autocorr[len(autocorr)//2:]
    autocorr = autocorr / (autocorr[0] + 1e-10)

    # Find peaks in autocorrelation (indicates periodicity)
    peaks = []
    for i in range(10, len(autocorr) - 1):
        if autocorr[i] > autocorr[i-1] and autocorr[i] > autocorr[i+1]:
            if autocorr[i] > 0.3:  # Significant peak
                peaks.append((i * sample_interval, autocorr[i]))  # (period, strength)

    if peaks:
        period, strength = peaks[0]
        if strength > 0.6:
            # Strong periodic component = breathing pattern!
            return 'breathing', {
                'period': int(period),
                'autocorr_peak': float(strength),
                'amplitude_variation': float(np.max(v_at_spot) - np.min(v_at_spot)),
                'mean_value': float(np.mean(v_at_spot))
            }
        elif strength > 0.3:
            return 'quasi_periodic', {
                'period': int(period),
                'autocorr_peak': float(strength),
                'amplitude_variation': float(np.max(v_at_spot) - np.min(v_at_spot))
            }

    # Irregular oscillations = chaos
    if spot_variation > 0.01:
        return 'chaotic', {
            'spot_variation': float(spot_variation),
            'range': float(np.max(v_at_spot) - np.min(v_at_spot)),
            'mean': float(np.mean(v_at_spot))
        }

    return 'noisy_static', {'spot_variation': float(spot_variation)}

def main():
    print("=" * 70)
    print("SEARCHING FOR BREATHING/PULSATING PATTERNS")
    print("=" * 70)
    print()
    print("Looking for patterns with REGULAR oscillations (limit cycles)")
    print("This is different from chaos (irregular) or static patterns.")
    print()

    # Scan a grid in parameter space
    # Focus near the chaos region and boundary areas where dynamics are likely
    f_range = np.arange(0.020, 0.055, 0.004)
    k_range = np.arange(0.048, 0.068, 0.002)

    results = []
    breathing_points = []
    chaotic_points = []

    total = len(f_range) * len(k_range)
    count = 0

    for f in f_range:
        for k in k_range:
            count += 1
            pattern_type, details = analyze_dynamics(f, k)
            results.append({
                'f': float(f), 'k': float(k),
                'type': pattern_type,
                'details': details
            })

            marker = {
                'uniform': '×',
                'static': '○',
                'breathing': '★',
                'quasi_periodic': '~',
                'chaotic': '◆',
                'noisy_static': '·'
            }.get(pattern_type, '?')

            if pattern_type == 'breathing':
                breathing_points.append((f, k, details))
                print(f"★ BREATHING at f={f:.3f}, k={k:.3f}: period={details['period']}, amplitude={details['amplitude_variation']:.4f}")
            elif pattern_type == 'chaotic':
                chaotic_points.append((f, k, details))
            elif count % 20 == 0:
                print(f"Progress: {count}/{total} ({marker} at f={f:.3f}, k={k:.3f})")

    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print()

    # Count types
    types = {}
    for r in results:
        types[r['type']] = types.get(r['type'], 0) + 1

    print("Pattern type distribution:")
    for t, c in sorted(types.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")

    print()

    if breathing_points:
        print("*** BREATHING PATTERNS FOUND! ***")
        print("-" * 40)
        for f, k, details in breathing_points:
            print(f"  f={f:.3f}, k={k:.3f}")
            print(f"    Period: {details['period']} steps")
            print(f"    Amplitude variation: {details['amplitude_variation']:.4f}")
            print(f"    Autocorr peak: {details['autocorr_peak']:.3f}")
            print()

        print("Significance:")
        print("  Breathing patterns would be limit cycles in the local dynamics")
        print("  This is distinct from global chaos or static patterns")
        print("  Could represent a novel dynamical regime in Gray-Scott")
    else:
        print("No breathing patterns found in tested region.")
        if chaotic_points:
            print(f"Found {len(chaotic_points)} chaotic points - chaos exists but no regular oscillations.")

    # Save results
    with open('breathing_pattern_results.json', 'w') as file:
        json.dump({
            'results': results,
            'breathing_points': [(f, k) for f, k, _ in breathing_points],
            'chaotic_points': [(f, k) for f, k, _ in chaotic_points],
            'type_counts': types
        }, file, indent=2)

    print()
    print("Results saved to breathing_pattern_results.json")

if __name__ == '__main__':
    main()
