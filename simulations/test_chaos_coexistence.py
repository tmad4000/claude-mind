#!/usr/bin/env python3
"""
Test for coexistence of STABLE PATTERNS and CHAOS at same (f,k).

This would be TRUE tristability in the dynamical systems sense:
- Spots (stable fixed point)
- Stripes (stable fixed point)
- Chaos (chaotic attractor with sustained oscillations)

Finding this would be genuinely novel - three QUALITATIVELY different
attractors (not just orientation variants).
"""

import numpy as np
import json

Du, Dv = 0.16, 0.08
N = 64  # Smaller for faster dynamics detection
dx = 1.0

def laplacian(Z, dx):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z) / (dx*dx)

def step(U, V, f, k):
    uvv = U * V * V
    return (np.clip(U + Du * laplacian(U, dx) - uvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv - (k + f) * V, 0, 1))

def init_spots(N, n=8):
    U, V = np.ones((N, N)), np.zeros((N, N))
    np.random.seed(42)
    for _ in range(n):
        cx, cy = np.random.randint(0, N, 2)
        r = np.random.randint(2, 4)
        y, x = np.ogrid[:N, :N]
        mask = ((np.minimum(np.abs(x-cx), N-np.abs(x-cx)))**2 +
                (np.minimum(np.abs(y-cy), N-np.abs(y-cy)))**2) <= r*r
        U[mask], V[mask] = 0.5, 0.25
    return U, V

def init_stripes(N, n=4):
    U, V = np.ones((N, N)), np.zeros((N, N))
    w = N // (2 * n)
    for i in range(n):
        s = i * N // n + N // (4 * n)
        U[s:s+w, :], V[s:s+w, :] = 0.5, 0.25
    return U, V

def init_chaos_seed(N):
    """Initialize with localized high-amplitude perturbation."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    # Strong central perturbation
    cx, cy = N//2, N//2
    r = N // 6
    y, x = np.ogrid[:N, :N]
    dist = np.sqrt((x - cx)**2 + (y - cy)**2)
    mask = dist < r
    # High V concentration to potentially trigger chaos
    U[mask] = 0.3
    V[mask] = 0.4
    return U, V

def init_random_patches(N):
    """Random patchy initial condition."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    np.random.seed(99)
    # Random patches
    for _ in range(20):
        cx, cy = np.random.randint(0, N, 2)
        r = np.random.randint(2, 6)
        y, x = np.ogrid[:N, :N]
        mask = ((np.minimum(np.abs(x-cx), N-np.abs(x-cx)))**2 +
                (np.minimum(np.abs(y-cy), N-np.abs(y-cy)))**2) <= r*r
        U[mask] = np.random.uniform(0.3, 0.6)
        V[mask] = np.random.uniform(0.2, 0.4)
    return U, V

def classify_dynamics(f, k, U0, V0, warmup=20000, measure=10000, sample_interval=100):
    """
    Classify the dynamics as:
    - 'uniform': system decays to uniform state
    - 'static_pattern': stable non-uniform pattern (spots or stripes)
    - 'oscillating': regular oscillations (limit cycle)
    - 'chaotic': irregular sustained dynamics (chaos)
    """
    U, V = U0.copy(), V0.copy()

    # Warmup
    for _ in range(warmup):
        U, V = step(U, V, f, k)

    # Check if uniform
    if np.std(V) < 0.01:
        return 'uniform', 0, 0

    # Collect time series
    v_means = []
    for i in range(measure):
        U, V = step(U, V, f, k)
        if i % sample_interval == 0:
            v_means.append(np.mean(V))

    v_means = np.array(v_means)

    # Measure dynamics
    v_variation = np.std(v_means)
    v_range = np.max(v_means) - np.min(v_means)

    # Static pattern: very low variation
    if v_variation < 1e-5:
        # Check if it's a pattern (not uniform)
        if np.std(V) > 0.02:
            return 'static_pattern', np.std(V), v_variation
        else:
            return 'uniform', np.std(V), v_variation

    # Check for regularity (oscillations vs chaos)
    # Compute autocorrelation at different lags
    v_centered = v_means - np.mean(v_means)
    if np.std(v_centered) < 1e-8:
        return 'static_pattern', np.std(V), v_variation

    autocorr = np.correlate(v_centered, v_centered, mode='full')
    autocorr = autocorr[len(autocorr)//2:]  # Keep positive lags
    autocorr = autocorr / autocorr[0]  # Normalize

    # Find first minimum and check for periodic return
    # Look for secondary peak (indicates periodicity)
    peaks = []
    for i in range(2, len(autocorr) - 1):
        if autocorr[i] > autocorr[i-1] and autocorr[i] > autocorr[i+1]:
            if autocorr[i] > 0.3:  # Significant peak
                peaks.append((i, autocorr[i]))

    if peaks and peaks[0][1] > 0.5:
        # Strong periodic return = limit cycle
        return 'oscillating', v_range, peaks[0][1]
    elif v_variation > 1e-4:
        # Sustained variation without clear periodicity = chaos
        return 'chaotic', v_range, v_variation
    else:
        return 'static_pattern', np.std(V), v_variation

def test_coexistence(f, k):
    """Test if multiple dynamical behaviors coexist at this (f,k)."""
    init_funcs = [
        ('spots', init_spots),
        ('stripes', init_stripes),
        ('chaos_seed', init_chaos_seed),
        ('random', init_random_patches),
    ]

    results = {}
    behaviors = set()

    for name, init_func in init_funcs:
        U0, V0 = init_func(N)
        behavior, metric1, metric2 = classify_dynamics(f, k, U0, V0)
        results[name] = {
            'behavior': behavior,
            'metric1': float(metric1),
            'metric2': float(metric2)
        }
        behaviors.add(behavior)

    # Remove uniform from interesting behaviors
    behaviors.discard('uniform')

    # Check for TRUE coexistence: pattern + chaos
    has_static = 'static_pattern' in behaviors
    has_oscillating = 'oscillating' in behaviors
    has_chaotic = 'chaotic' in behaviors

    coexistence_type = 'none'
    if has_static and (has_oscillating or has_chaotic):
        coexistence_type = 'PATTERN_CHAOS_COEXISTENCE'
    elif has_oscillating and has_chaotic:
        coexistence_type = 'oscillating_chaos'
    elif len(behaviors) > 1:
        coexistence_type = f"mixed_{list(behaviors)}"

    return {
        'f': f,
        'k': k,
        'results': results,
        'behaviors': list(behaviors),
        'coexistence_type': coexistence_type,
        'novel': coexistence_type == 'PATTERN_CHAOS_COEXISTENCE'
    }

def main():
    print("=" * 60)
    print("CHAOS/PATTERN COEXISTENCE TEST")
    print("=" * 60)
    print()
    print("Looking for parameters where BOTH stable patterns AND chaos exist...")
    print("This would be TRUE tristability (qualitatively different attractors)")
    print()

    # Test points near the known chaos region (f=0.026, k=0.051)
    # and spanning the pattern-forming region
    test_points = [
        # Near chaos region
        (0.026, 0.051),
        (0.026, 0.052),
        (0.027, 0.051),
        (0.027, 0.052),
        (0.025, 0.050),
        (0.028, 0.053),
        # Boundary region
        (0.024, 0.049),
        (0.025, 0.051),
        (0.029, 0.053),
        # Pattern region (for comparison)
        (0.030, 0.055),
        (0.035, 0.058),
        (0.040, 0.060),
    ]

    novel_points = []

    for i, (f, k) in enumerate(test_points):
        print(f"Testing {i+1}/{len(test_points)}: f={f:.3f}, k={k:.3f}...", end=" ", flush=True)
        result = test_coexistence(f, k)

        if result['novel']:
            novel_points.append(result)
            print(f"*** NOVEL: {result['behaviors']} ***")
        else:
            print(f"{result['behaviors']} ({result['coexistence_type']})")

    print()
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    print()

    if novel_points:
        print("PATTERN/CHAOS COEXISTENCE FOUND!")
        print("-" * 40)
        for np_result in novel_points:
            print(f"\nf={np_result['f']:.3f}, k={np_result['k']:.3f}:")
            for ic_name, data in np_result['results'].items():
                print(f"  {ic_name}: {data['behavior']} (metrics: {data['metric1']:.4f}, {data['metric2']:.4f})")

        print()
        print("SIGNIFICANCE:")
        print("-" * 40)
        print("Finding stable patterns AND chaos at same parameters")
        print("would demonstrate TRUE tristability:")
        print("- Static spots (fixed point attractor)")
        print("- Static stripes (fixed point attractor)")
        print("- Chaos (strange attractor)")
        print()
        print("This goes beyond known bistability (Mazin et al. 1996)")
        print("because chaos is a QUALITATIVELY different dynamical regime.")
    else:
        print("No pattern/chaos coexistence found at tested points.")
        print()
        print("Behaviors found:")
        all_behaviors = set()
        for (f, k) in test_points:
            result = test_coexistence(f, k)
            for b in result['behaviors']:
                all_behaviors.add(b)
        print(f"  {all_behaviors}")

    # Save results
    all_results = [test_coexistence(f, k) for f, k in test_points]
    with open('chaos_coexistence_results.json', 'w') as file:
        json.dump({
            'test_points': test_points,
            'results': all_results,
            'novel_points': novel_points
        }, file, indent=2)

    print()
    print("Results saved to chaos_coexistence_results.json")

if __name__ == '__main__':
    main()
