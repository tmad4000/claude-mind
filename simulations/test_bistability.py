#!/usr/bin/env python3
"""
Test for bistability in Gray-Scott pattern regions.

Hypothesis: There exist regions labeled as "single pattern type" in published
phase diagrams where BOTH spots and stripes are stable - final state depends
on initial conditions.

If true, this would contradict standard Gray-Scott phase diagrams.
"""

import numpy as np
import json

def correlate2d_simple(a, b):
    """Simple 2D correlation using FFT (numpy only)."""
    fa = np.fft.fft2(a)
    fb = np.fft.fft2(b)
    return np.real(np.fft.ifft2(fa * np.conj(fb)))

def label_components(binary):
    """Simple connected component labeling (4-connectivity)."""
    labels = np.zeros_like(binary, dtype=int)
    current_label = 0
    N = binary.shape[0]

    for i in range(N):
        for j in range(N):
            if binary[i, j] and labels[i, j] == 0:
                current_label += 1
                # Flood fill
                stack = [(i, j)]
                while stack:
                    y, x = stack.pop()
                    if y < 0 or y >= N or x < 0 or x >= N:
                        continue
                    if not binary[y, x] or labels[y, x] != 0:
                        continue
                    labels[y, x] = current_label
                    stack.extend([(y+1, x), (y-1, x), (y, x+1), (y, x-1)])

    return labels, current_label

# Parameters
Du, Dv = 0.16, 0.08
N = 128
dx = 1.0
dt = 1.0

def laplacian(Z, dx):
    """5-point stencil Laplacian with periodic BC."""
    return (
        np.roll(Z, 1, axis=0) + np.roll(Z, -1, axis=0) +
        np.roll(Z, 1, axis=1) + np.roll(Z, -1, axis=1) - 4*Z
    ) / (dx*dx)

def step(U, V, f, k, dt=1.0):
    """One Gray-Scott time step."""
    Lu = laplacian(U, dx)
    Lv = laplacian(V, dx)
    uvv = U * V * V
    U_new = U + dt * (Du * Lu - uvv + f * (1 - U))
    V_new = V + dt * (Dv * Lv + uvv - (k + f) * V)
    return np.clip(U_new, 0, 1), np.clip(V_new, 0, 1)

def init_spots(N, n_spots=10):
    """Initialize with spot-like perturbations."""
    U = np.ones((N, N))
    V = np.zeros((N, N))
    # Random circular spots
    for _ in range(n_spots):
        cx, cy = np.random.randint(0, N, 2)
        r = np.random.randint(3, 8)
        y, x = np.ogrid[:N, :N]
        # Handle periodic boundaries
        dx_arr = np.minimum(np.abs(x - cx), N - np.abs(x - cx))
        dy_arr = np.minimum(np.abs(y - cy), N - np.abs(y - cy))
        mask = dx_arr**2 + dy_arr**2 <= r**2
        U[mask] = 0.5
        V[mask] = 0.25
    return U, V

def init_stripes(N, orientation='horizontal', n_stripes=5):
    """Initialize with stripe-like perturbations."""
    U = np.ones((N, N))
    V = np.zeros((N, N))
    stripe_width = N // (2 * n_stripes)
    for i in range(n_stripes):
        start = i * N // n_stripes + N // (4 * n_stripes)
        end = start + stripe_width
        if orientation == 'horizontal':
            U[start:end, :] = 0.5
            V[start:end, :] = 0.25
        else:
            U[:, start:end] = 0.5
            V[:, start:end] = 0.25
    return U, V

def classify_pattern(V, threshold=0.1):
    """
    Classify pattern as spots, stripes, mixed, chaotic, or uniform.
    Returns: (type, confidence, metrics)
    """
    if np.std(V) < 0.01:
        return 'uniform', 1.0, {'std': np.std(V)}

    # Binarize
    V_binary = V > threshold

    # Compute autocorrelation to detect periodicity
    V_centered = V - np.mean(V)
    autocorr = correlate2d_simple(V_centered, V_centered)
    autocorr = np.fft.fftshift(autocorr)  # Center the autocorrelation
    autocorr = autocorr / autocorr.max()

    # Look for peaks in autocorrelation
    center = N // 2
    # Check horizontal and vertical slices
    h_slice = autocorr[center, :]
    v_slice = autocorr[:, center]

    # Find secondary peaks (excluding center)
    def find_peaks(arr):
        peaks = []
        for i in range(2, len(arr) - 2):
            if arr[i] > arr[i-1] and arr[i] > arr[i+1] and arr[i] > 0.1:
                if abs(i - len(arr)//2) > 5:  # Not center
                    peaks.append((i, arr[i]))
        return peaks

    h_peaks = find_peaks(h_slice)
    v_peaks = find_peaks(v_slice)

    # Compute anisotropy: ratio of horizontal to vertical structure
    h_strength = max([p[1] for p in h_peaks]) if h_peaks else 0
    v_strength = max([p[1] for p in v_peaks]) if v_peaks else 0

    # Label connected components
    labeled, n_components = label_components(V_binary)
    if n_components == 0:
        return 'uniform', 1.0, {'components': 0}

    # Compute component sizes and aspect ratios
    component_sizes = []
    aspect_ratios = []
    for i in range(1, n_components + 1):
        component = (labeled == i)
        size = np.sum(component)
        if size < 4:  # Skip tiny components
            continue
        component_sizes.append(size)
        # Find bounding box
        rows = np.any(component, axis=1)
        cols = np.any(component, axis=0)
        row_extent = np.sum(rows)
        col_extent = np.sum(cols)
        ar = max(row_extent, col_extent) / max(min(row_extent, col_extent), 1)
        aspect_ratios.append(ar)

    if not aspect_ratios:
        return 'chaotic', 0.5, {'reason': 'no valid components'}

    mean_ar = np.mean(aspect_ratios)
    std_ar = np.std(aspect_ratios)
    mean_size = np.mean(component_sizes)
    std_size = np.std(component_sizes)

    metrics = {
        'n_components': n_components,
        'mean_aspect_ratio': mean_ar,
        'std_aspect_ratio': std_ar,
        'mean_size': mean_size,
        'std_size': std_size,
        'h_strength': h_strength,
        'v_strength': v_strength,
        'anisotropy': abs(h_strength - v_strength) / max(h_strength + v_strength, 0.01)
    }

    # Classification logic
    if mean_ar < 2.0 and std_ar < 1.0:
        # Compact components = spots
        return 'spots', min(1.0, 2.0 / mean_ar), metrics
    elif mean_ar > 4.0:
        # Elongated components = stripes
        return 'stripes', min(1.0, mean_ar / 5.0), metrics
    elif metrics['anisotropy'] > 0.5:
        # Strong directional preference = stripes
        return 'stripes', metrics['anisotropy'], metrics
    elif std_ar > 2.0:
        # High variance in shapes = mixed or chaotic
        return 'mixed', 0.5, metrics
    else:
        return 'mixed', 0.5, metrics

def test_bistability(f, k, n_steps=30000, equilibration=20000):
    """
    Test if a point exhibits bistability.
    Run from both spot-like and stripe-like initial conditions.
    """
    np.random.seed(42)  # Reproducibility

    # Run from spots
    U_spot, V_spot = init_spots(N, n_spots=15)
    for _ in range(n_steps):
        U_spot, V_spot = step(U_spot, V_spot, f, k)
    type_from_spots, conf_spots, metrics_spots = classify_pattern(V_spot)

    # Run from stripes
    np.random.seed(43)
    U_stripe, V_stripe = init_stripes(N, orientation='horizontal', n_stripes=6)
    for _ in range(n_steps):
        U_stripe, V_stripe = step(U_stripe, V_stripe, f, k)
    type_from_stripes, conf_stripes, metrics_stripes = classify_pattern(V_stripe)

    # Also try vertical stripes
    np.random.seed(44)
    U_vstripe, V_vstripe = init_stripes(N, orientation='vertical', n_stripes=6)
    for _ in range(n_steps):
        U_vstripe, V_vstripe = step(U_vstripe, V_vstripe, f, k)
    type_from_vstripes, conf_vstripes, metrics_vstripes = classify_pattern(V_vstripe)

    # Check for bistability
    types = {type_from_spots, type_from_stripes, type_from_vstripes}
    types.discard('uniform')  # Uniform is not interesting

    is_bistable = len(types) > 1

    return {
        'f': f,
        'k': k,
        'bistable': is_bistable,
        'from_spots': {'type': type_from_spots, 'confidence': conf_spots},
        'from_h_stripes': {'type': type_from_stripes, 'confidence': conf_stripes},
        'from_v_stripes': {'type': type_from_vstripes, 'confidence': conf_vstripes},
        'unique_types': list(types)
    }

def main():
    """Scan parameter space for bistability."""
    print("=" * 60)
    print("BISTABILITY TEST: Looking for IC-dependent pattern types")
    print("=" * 60)
    print()
    print("Testing points where standard phase diagrams show single pattern type...")
    print()

    # Test points in various regions of the standard phase diagram
    # These are chosen to span the "stripes" and "spots" regions
    test_points = [
        # Region typically showing stripes
        (0.030, 0.055),
        (0.035, 0.058),
        (0.040, 0.060),
        (0.045, 0.062),
        # Region typically showing spots
        (0.025, 0.050),
        (0.030, 0.052),
        (0.020, 0.048),
        # Transition region (most likely bistable)
        (0.035, 0.060),
        (0.040, 0.063),
        (0.042, 0.064),
        (0.038, 0.061),
        # Near chaos region
        (0.026, 0.051),
        (0.028, 0.052),
    ]

    results = []
    bistable_points = []

    for i, (f, k) in enumerate(test_points):
        print(f"Testing point {i+1}/{len(test_points)}: f={f:.3f}, k={k:.3f}...", end=" ", flush=True)
        result = test_bistability(f, k)
        results.append(result)

        if result['bistable']:
            bistable_points.append(result)
            print(f"BISTABLE! Types: {result['unique_types']}")
        else:
            types = result['unique_types']
            print(f"Monostable: {types[0] if types else 'uniform'}")

    print()
    print("=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print()
    print(f"Total points tested: {len(test_points)}")
    print(f"Bistable points found: {len(bistable_points)}")
    print()

    if bistable_points:
        print("BISTABLE REGIONS DETECTED!")
        print("-" * 40)
        for bp in bistable_points:
            print(f"  f={bp['f']:.3f}, k={bp['k']:.3f}")
            print(f"    From spots: {bp['from_spots']['type']} (conf: {bp['from_spots']['confidence']:.2f})")
            print(f"    From h-stripes: {bp['from_h_stripes']['type']} (conf: {bp['from_h_stripes']['confidence']:.2f})")
            print(f"    From v-stripes: {bp['from_v_stripes']['type']} (conf: {bp['from_v_stripes']['confidence']:.2f})")
            print()

        print("SIGNIFICANCE:")
        print("-" * 40)
        print("Standard Gray-Scott phase diagrams (Pearson 1993) show")
        print("single pattern types per region. Finding bistability would")
        print("suggest the phase diagram is INCOMPLETE.")
    else:
        print("No bistability detected at tested points.")
        print("Standard phase diagram appears accurate for these regions.")

    # Save results
    with open('bistability_results.json', 'w') as f:
        json.dump({
            'test_points': test_points,
            'results': results,
            'bistable_points': bistable_points,
            'summary': {
                'total_tested': len(test_points),
                'bistable_count': len(bistable_points)
            }
        }, f, indent=2)

    print()
    print("Results saved to bistability_results.json")

    return results, bistable_points

if __name__ == '__main__':
    results, bistable = main()
