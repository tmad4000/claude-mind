#!/usr/bin/env python3
"""
Examine the "pinch point" where the pattern region closes (f ≈ 0.063).

Near this critical point, there might be:
1. Critical slowing down (diverging relaxation time)
2. Diverging wavelength
3. Anomalous fluctuations
4. Universal scaling behavior

Finding any of these would be interesting from a phase transition perspective.
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

def init_small_perturbation(N):
    """Small random perturbation - tests linear instability."""
    U = np.ones((N, N))
    V = np.zeros((N, N))
    np.random.seed(42)
    # Small perturbation
    U += 0.01 * np.random.randn(N, N)
    V += 0.005 * np.random.randn(N, N)
    return np.clip(U, 0, 1), np.clip(V, 0, 1)

def measure_pattern_strength(V):
    """Measure the pattern amplitude (deviation from mean)."""
    return np.std(V)

def measure_wavelength(V):
    """Estimate the dominant wavelength from the power spectrum."""
    V_centered = V - np.mean(V)
    if np.std(V_centered) < 0.001:
        return np.inf  # No pattern

    fft = np.fft.fft2(V_centered)
    power = np.abs(np.fft.fftshift(fft))**2

    # Find peak (excluding DC)
    center = N // 2
    power[center-2:center+3, center-2:center+3] = 0  # Mask DC component

    peak_idx = np.unravel_index(np.argmax(power), power.shape)
    peak_dist = np.sqrt((peak_idx[0] - center)**2 + (peak_idx[1] - center)**2)

    if peak_dist < 1:
        return np.inf  # No clear periodicity

    wavelength = N / peak_dist
    return wavelength

def find_k_boundary(f, k_range, threshold=0.02, n_steps=30000):
    """Find the k value where patterns first appear for a given f."""
    for k in k_range:
        U, V = init_small_perturbation(N)
        for _ in range(n_steps):
            U, V = step(U, V, f, k)
        strength = measure_pattern_strength(V)
        if strength > threshold:
            return k
    return None

def measure_dynamics_near_pinch(f, k, n_warmup=10000, n_measure=5000):
    """Measure pattern formation dynamics."""
    U, V = init_small_perturbation(N)

    # Track growth
    strengths = []
    wavelengths = []

    for i in range(n_warmup + n_measure):
        U, V = step(U, V, f, k)
        if i >= n_warmup and i % 100 == 0:
            strengths.append(measure_pattern_strength(V))
            wavelengths.append(measure_wavelength(V))

    return {
        'final_strength': float(strengths[-1]) if strengths else 0,
        'mean_strength': float(np.mean(strengths)) if strengths else 0,
        'wavelength': float(np.median([w for w in wavelengths if w < 100])) if any(w < 100 for w in wavelengths) else np.inf,
        'strength_variation': float(np.std(strengths)) if strengths else 0
    }

def main():
    print("=" * 60)
    print("PINCH POINT ANALYSIS")
    print("=" * 60)
    print()

    # Find where patterns exist for f values approaching the pinch
    print("Finding pattern boundaries near the pinch point...")
    print()

    # Our earlier analysis found patterns roughly up to f ≈ 0.062
    # Let's scan more carefully
    f_values = np.arange(0.054, 0.066, 0.002)
    k_range = np.arange(0.060, 0.072, 0.001)

    boundaries = []
    for f in f_values:
        print(f"Scanning f={f:.3f}...", end=" ", flush=True)
        k_lower = find_k_boundary(f, k_range)
        if k_lower:
            # Also find upper boundary
            k_upper = find_k_boundary(f, k_range[::-1])
            print(f"patterns exist for k in [{k_lower:.3f}, {k_upper:.3f}]")
            boundaries.append({
                'f': float(f),
                'k_lower': float(k_lower),
                'k_upper': float(k_upper),
                'width': float(k_upper - k_lower) if k_upper else 0
            })
        else:
            print("no patterns found")
            boundaries.append({
                'f': float(f),
                'k_lower': None,
                'k_upper': None,
                'width': 0
            })

    print()
    print("=" * 60)
    print("PATTERN REGION WIDTH vs f")
    print("=" * 60)
    print()

    for b in boundaries:
        if b['k_lower']:
            print(f"f={b['f']:.3f}: width = {b['width']:.4f} (k: {b['k_lower']:.3f} to {b['k_upper']:.3f})")
        else:
            print(f"f={b['f']:.3f}: NO PATTERNS")

    # Find the pinch point (where width goes to zero)
    widths = [(b['f'], b['width']) for b in boundaries if b['width'] > 0]
    if len(widths) >= 2:
        # Linear extrapolation to find where width = 0
        f_vals = [w[0] for w in widths]
        w_vals = [w[1] for w in widths]

        # Simple linear fit
        if len(f_vals) >= 2:
            slope = (w_vals[-1] - w_vals[0]) / (f_vals[-1] - f_vals[0])
            intercept = w_vals[0] - slope * f_vals[0]
            f_pinch = -intercept / slope if slope != 0 else None

            print()
            print(f"Estimated pinch point (linear extrapolation): f ≈ {f_pinch:.4f}" if f_pinch else "Could not estimate pinch point")

    # Measure dynamics near the boundary
    print()
    print("=" * 60)
    print("DYNAMICS NEAR PINCH")
    print("=" * 60)
    print()

    # For the last f value with patterns, measure wavelength and relaxation
    pattern_f_values = [b['f'] for b in boundaries if b['width'] > 0]
    if pattern_f_values:
        f_near_pinch = max(pattern_f_values)
        b = next(b for b in boundaries if b['f'] == f_near_pinch)

        if b['k_lower']:
            k_test = (b['k_lower'] + b['k_upper']) / 2
            print(f"Testing at f={f_near_pinch:.3f}, k={k_test:.3f} (middle of viable range)...")

            dynamics = measure_dynamics_near_pinch(f_near_pinch, k_test)
            print(f"  Pattern strength: {dynamics['final_strength']:.4f}")
            print(f"  Wavelength: {dynamics['wavelength']:.2f}")
            print(f"  Strength variation: {dynamics['strength_variation']:.6f}")

            # Compare with lower f
            if len(pattern_f_values) >= 3:
                f_lower = pattern_f_values[len(pattern_f_values)//2]
                b_lower = next(b for b in boundaries if b['f'] == f_lower)
                if b_lower['k_lower']:
                    k_test_lower = (b_lower['k_lower'] + b_lower['k_upper']) / 2
                    print()
                    print(f"Comparing with f={f_lower:.3f}, k={k_test_lower:.3f}...")

                    dynamics_lower = measure_dynamics_near_pinch(f_lower, k_test_lower)
                    print(f"  Pattern strength: {dynamics_lower['final_strength']:.4f}")
                    print(f"  Wavelength: {dynamics_lower['wavelength']:.2f}")
                    print(f"  Strength variation: {dynamics_lower['strength_variation']:.6f}")

                    print()
                    print("Comparison:")
                    ratio = dynamics['wavelength'] / dynamics_lower['wavelength'] if dynamics_lower['wavelength'] > 0 else np.inf
                    print(f"  Wavelength ratio (near/far from pinch): {ratio:.2f}")

    # Save results
    results = {
        'boundaries': boundaries,
        'pinch_analysis': 'see above'
    }

    with open('pinch_point_analysis.json', 'w') as file:
        json.dump(results, file, indent=2)

    print()
    print("Results saved to pinch_point_analysis.json")

if __name__ == '__main__':
    main()
