#!/usr/bin/env python3
"""
Measure the CRITICAL NUCLEATION AMPLITUDE for pattern formation.

Since Gray-Scott is subcritical everywhere, patterns need finite-amplitude
perturbations to nucleate. This script measures:
1. The minimum amplitude needed to trigger patterns at each (f,k)
2. How this threshold varies across parameter space
3. Whether there are interesting structures (like divergence near boundaries)

A quantitative map of nucleation thresholds could be genuinely novel.
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

def init_with_amplitude(N, v_amplitude, n_spots=5):
    """
    Initialize with spots of specified amplitude.
    v_amplitude controls how much V is present in spots (0 to 1).
    """
    U, V = np.ones((N, N)), np.zeros((N, N))
    np.random.seed(42)
    for _ in range(n_spots):
        cx, cy = np.random.randint(0, N, 2)
        r = 3  # Fixed radius
        y, x = np.ogrid[:N, :N]
        mask = ((np.minimum(np.abs(x-cx), N-np.abs(x-cx)))**2 +
                (np.minimum(np.abs(y-cy), N-np.abs(y-cy)))**2) <= r*r
        # Scale perturbation by amplitude
        U[mask] = 1.0 - v_amplitude  # Depress U where V is high
        V[mask] = v_amplitude
    return U, V

def test_nucleation(f, k, amplitude, n_steps=30000, threshold=0.02):
    """Test if patterns nucleate from given amplitude."""
    U, V = init_with_amplitude(N, amplitude)
    for _ in range(n_steps):
        U, V = step(U, V, f, k)
    return np.std(V) > threshold

def find_critical_amplitude(f, k, amp_range=np.logspace(-3, 0, 30)):
    """
    Binary search to find the critical nucleation amplitude.
    Returns (critical_amplitude, was_pattern_ever_found)
    """
    # First check if any amplitude works
    if not test_nucleation(f, k, 0.5):
        return None, False  # No patterns even at high amplitude

    # Binary search for threshold
    low, high = 0.0, 0.5
    for _ in range(15):  # ~15 iterations gives precision to ~0.00001
        mid = (low + high) / 2
        if test_nucleation(f, k, mid):
            high = mid
        else:
            low = mid

    return high, True

def main():
    print("=" * 70)
    print("CRITICAL NUCLEATION AMPLITUDE MAPPING")
    print("=" * 70)
    print()
    print("For subcritical bifurcations, patterns need finite perturbations.")
    print("Mapping the critical amplitude could reveal interesting structure.")
    print()

    # Test points across the pattern region
    test_points = [
        # Core pattern region
        (0.030, 0.055),
        (0.035, 0.058),
        (0.040, 0.060),
        (0.045, 0.063),
        (0.050, 0.065),
        # Near boundaries
        (0.030, 0.052),  # Lower k boundary
        (0.030, 0.058),  # Upper k boundary
        (0.055, 0.066),  # Near upper f limit
        (0.020, 0.048),  # Low f
        # Near chaos region
        (0.026, 0.052),
        (0.028, 0.053),
    ]

    results = []

    print("Scanning (f, k) space for nucleation thresholds...")
    print("-" * 70)

    for f, k in test_points:
        print(f"f={f:.3f}, k={k:.3f}...", end=" ", flush=True)
        critical_amp, patterns_exist = find_critical_amplitude(f, k)

        if patterns_exist:
            print(f"critical amplitude ≈ {critical_amp:.4f}")
            results.append({
                'f': f, 'k': k,
                'critical_amplitude': critical_amp,
                'patterns_exist': True
            })
        else:
            print("NO PATTERNS (even at high amplitude)")
            results.append({
                'f': f, 'k': k,
                'critical_amplitude': None,
                'patterns_exist': False
            })

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    # Analyze the results
    valid_results = [r for r in results if r['patterns_exist']]

    if len(valid_results) < 2:
        print("Not enough valid points to analyze trends.")
    else:
        amplitudes = [r['critical_amplitude'] for r in valid_results]
        min_amp = min(amplitudes)
        max_amp = max(amplitudes)

        print(f"Critical amplitude range: {min_amp:.4f} to {max_amp:.4f}")
        print(f"Ratio (max/min): {max_amp/min_amp:.2f}x")
        print()

        # Look for trends
        print("Variation with f (fixed k≈0.055-0.065):")
        for r in sorted(valid_results, key=lambda x: x['f']):
            if 0.052 < r['k'] < 0.066:
                print(f"  f={r['f']:.3f}, k={r['k']:.3f}: A_c = {r['critical_amplitude']:.4f}")

        print()
        print("Variation with k (fixed f≈0.030):")
        for r in sorted(valid_results, key=lambda x: x['k']):
            if 0.028 < r['f'] < 0.032:
                print(f"  f={r['f']:.3f}, k={r['k']:.3f}: A_c = {r['critical_amplitude']:.4f}")

        # Check for divergence near boundaries
        print()
        if max_amp > 2 * min_amp:
            print("** SIGNIFICANT VARIATION in nucleation threshold across parameter space **")
            print("This suggests the saddle-node bifurcation structure varies with (f,k).")
        else:
            print("Nucleation threshold is relatively uniform across tested region.")

    # Save results
    with open('nucleation_threshold_results.json', 'w') as file:
        json.dump({
            'test_points': test_points,
            'results': results,
            'min_amplitude': min(amplitudes) if valid_results else None,
            'max_amplitude': max(amplitudes) if valid_results else None
        }, file, indent=2)

    print()
    print("Results saved to nucleation_threshold_results.json")

if __name__ == '__main__':
    main()
