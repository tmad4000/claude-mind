#!/usr/bin/env python3
"""
Explore EXTREME PARAMETER REGIONS in Gray-Scott.

The standard Pearson classification covers f ∈ [0.01, 0.07], k ∈ [0.03, 0.07].
But what happens outside this region? Possible surprises:

1. New pattern morphologies at extreme parameters
2. Different bifurcation structure
3. Patterns where none are expected
4. Oscillatory behavior not seen in standard range

Let's systematically explore:
- Very low f (< 0.01): Slow feed rate
- Very high f (> 0.07): Fast feed rate
- Very low k (< 0.03): Slow removal
- Very high k (> 0.07): Fast removal
- Corners of parameter space
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

def init_nucleated(N):
    """Initialize with nucleation sites."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    np.random.seed(42)
    for _ in range(8):
        cx, cy = np.random.randint(N//4, 3*N//4, 2)
        r = 4
        y, x = np.ogrid[:N, :N]
        mask = (x-cx)**2 + (y-cy)**2 <= r*r
        U[mask], V[mask] = 0.5, 0.25
    return U, V

def classify_pattern(V, U, n_samples=5000, sample_interval=10):
    """Classify the pattern type based on statistics."""
    v_std = np.std(V)
    v_mean = np.mean(V)
    u_std = np.std(U)
    u_mean = np.mean(U)

    if v_std < 0.01:
        if v_mean < 0.01:
            return 'uniform_trivial'  # V ≈ 0
        else:
            return 'uniform_nontrivial'  # V > 0 but uniform

    # Has pattern - analyze structure
    # Use FFT to check dominant wavelength
    V_centered = V - v_mean
    fft = np.fft.fft2(V_centered)
    power = np.abs(np.fft.fftshift(fft))**2
    center = N // 2
    power[center-2:center+3, center-2:center+3] = 0

    # Find peak
    y_idx, x_idx = np.unravel_index(np.argmax(power), power.shape)
    peak_dist = np.sqrt((y_idx - center)**2 + (x_idx - center)**2)

    if peak_dist < 3:
        return 'large_scale'  # Very long wavelength

    # Estimate spot vs stripe
    # Spots have more isotropic power spectrum
    # Stripes have anisotropic

    # Simple heuristic: check if pattern looks like spots
    binary = V > (v_mean + v_std)
    spot_ratio = np.sum(binary) / N**2

    if spot_ratio < 0.15:
        return 'sparse_spots'
    elif spot_ratio > 0.4:
        return 'stripes_or_dense'
    else:
        return 'medium_spots'

def test_parameters(f, k, n_steps=50000):
    """Test a single parameter point."""
    U, V = init_nucleated(N)

    # Track dynamics
    v_history = []
    sample_interval = 500

    for step_num in range(n_steps):
        U, V = step(U, V, f, k)

        if step_num % sample_interval == 0:
            v_history.append({
                'step': step_num,
                'v_mean': float(np.mean(V)),
                'v_std': float(np.std(V)),
                'v_max': float(np.max(V))
            })

    # Check for oscillation
    v_stds = [h['v_std'] for h in v_history[-20:]]
    is_oscillating = np.std(v_stds) > 0.01 * np.mean(v_stds)

    pattern_type = classify_pattern(V, U)

    return {
        'pattern_type': pattern_type,
        'final_v_std': float(np.std(V)),
        'final_v_mean': float(np.mean(V)),
        'is_oscillating': is_oscillating,
        'history': v_history[-10:]  # Keep last 10 samples
    }

def main():
    print("=" * 70)
    print("EXTREME PARAMETER EXPLORATION")
    print("=" * 70)
    print()
    print("Exploring parameter regions outside standard Pearson classification...")
    print()

    results = []

    # Define extreme parameter regions to explore
    extreme_regions = {
        'very_low_f': [(f, k) for f in [0.002, 0.005, 0.008] for k in [0.040, 0.050, 0.060]],
        'very_high_f': [(f, k) for f in [0.080, 0.100, 0.120] for k in [0.040, 0.060, 0.080]],
        'very_low_k': [(f, k) for f in [0.020, 0.035, 0.050] for k in [0.015, 0.020, 0.025]],
        'very_high_k': [(f, k) for f in [0.020, 0.035, 0.050] for k in [0.080, 0.090, 0.100]],
        'corners': [
            (0.005, 0.020),  # low f, low k
            (0.005, 0.090),  # low f, high k
            (0.100, 0.020),  # high f, low k
            (0.100, 0.090),  # high f, high k
        ]
    }

    for region_name, points in extreme_regions.items():
        print(f"\n{region_name.upper()}")
        print("-" * 40)
        print(f"{'f':>6} {'k':>6} {'pattern_type':>20} {'v_std':>8} {'osc':>5}")
        print("-" * 50)

        for f, k in points:
            result = test_parameters(f, k)
            result['f'] = float(f)
            result['k'] = float(k)
            result['region'] = region_name
            results.append(result)

            osc_marker = "~" if result['is_oscillating'] else ""
            print(f"{f:6.3f} {k:6.3f} {result['pattern_type']:>20} "
                  f"{result['final_v_std']:8.4f} {osc_marker:>5}")

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    # Look for unusual findings
    unusual = []

    for r in results:
        # Patterns where uniform expected
        if r['region'] in ['very_high_f', 'very_high_k'] and 'spots' in r['pattern_type']:
            unusual.append(f"Patterns at extreme {r['region']}: f={r['f']}, k={r['k']}")

        # Oscillations
        if r['is_oscillating']:
            unusual.append(f"Oscillating at f={r['f']}, k={r['k']}: {r['pattern_type']}")

        # Non-trivial uniform states
        if r['pattern_type'] == 'uniform_nontrivial':
            unusual.append(f"Non-trivial uniform at f={r['f']}, k={r['k']}: V_mean={r['final_v_mean']:.3f}")

    if unusual:
        print("UNUSUAL FINDINGS:")
        for finding in unusual:
            print(f"  * {finding}")
    else:
        print("No unusual findings in extreme parameter regions.")

    # Count pattern types
    print()
    print("Pattern type counts:")
    type_counts = {}
    for r in results:
        t = r['pattern_type']
        type_counts[t] = type_counts.get(t, 0) + 1
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")

    # Save results
    with open('extreme_parameters_results.json', 'w') as file:
        json.dump({
            'results': results,
            'unusual': unusual,
            'type_counts': type_counts
        }, file, indent=2)

    print()
    print("Results saved to extreme_parameters_results.json")

if __name__ == '__main__':
    main()
