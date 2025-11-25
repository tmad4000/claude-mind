#!/usr/bin/env python3
"""
Test 3D GRAY-SCOTT PATTERNS.

3D Gray-Scott is MUCH LESS STUDIED than 2D because:
1. Computationally expensive (N^3 vs N^2)
2. Hard to visualize
3. Most applications are 2D (surface phenomena)

But 3D could reveal:
1. New pattern types not possible in 2D (surfaces, tubes, spheres)
2. Different stability properties
3. Genuinely novel phenomena

This is exploring a LESS MAPPED parameter regime.
"""

import numpy as np
import json

# Small grid for feasibility
N = 32
dx = 1.0
Du, Dv = 0.16, 0.08

def laplacian_3d(Z, dx):
    """3D Laplacian with periodic boundary conditions."""
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) +
            np.roll(Z, 1, 2) + np.roll(Z, -1, 2) - 6*Z) / (dx*dx)

def step_3d(U, V, f, k):
    uvv = U * V * V
    return (np.clip(U + Du * laplacian_3d(U, dx) - uvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian_3d(V, dx) + uvv - (k + f) * V, 0, 1))

def init_nucleated_3d(N, seed=42, n_seeds=5):
    """Initialize with spherical nucleation sites."""
    np.random.seed(seed)
    U = np.ones((N, N, N))
    V = np.zeros((N, N, N))

    for _ in range(n_seeds):
        cx = np.random.randint(N//4, 3*N//4)
        cy = np.random.randint(N//4, 3*N//4)
        cz = np.random.randint(N//4, 3*N//4)
        r = 3

        z, y, x = np.ogrid[:N, :N, :N]
        mask = (x-cx)**2 + (y-cy)**2 + (z-cz)**2 <= r*r
        U[mask] = 0.5
        V[mask] = 0.25

    return U, V

def measure_pattern_3d(V):
    """Measure 3D pattern properties."""
    v_std = np.std(V)
    if v_std < 0.02:
        return None, 'no_pattern'

    v_mean = np.mean(V)

    # Analyze 3D Fourier transform
    V_centered = V - v_mean
    fft = np.fft.fftn(V_centered)
    power = np.abs(np.fft.fftshift(fft))**2

    N = V.shape[0]
    center = N // 2

    # Zero out DC
    power[center-1:center+2, center-1:center+2, center-1:center+2] = 0

    # Find dominant wavelength using radial average
    z, y, x = np.ogrid[:N, :N, :N]
    r = np.sqrt((x-center)**2 + (y-center)**2 + (z-center)**2)
    r = r.astype(int)

    radial_power = np.bincount(r.ravel(), weights=power.ravel())
    radial_counts = np.bincount(r.ravel())
    radial_avg = radial_power / (radial_counts + 1e-10)

    # Find peak
    if len(radial_avg) > 3:
        peak_k = np.argmax(radial_avg[1:N//2]) + 1
        dominant_wavelength = N / peak_k if peak_k > 0 else N
    else:
        dominant_wavelength = N

    # Measure anisotropy: compare power in x, y, z directions
    x_power = np.sum(power[:, center-1:center+2, :])
    y_power = np.sum(power[center-1:center+2, :, :])
    z_power = np.sum(power[:, :, center-1:center+2])
    total = x_power + y_power + z_power + 1e-10

    # For isotropic (spherical) patterns, x_power ≈ y_power ≈ z_power
    anisotropy = np.std([x_power, y_power, z_power]) / (np.mean([x_power, y_power, z_power]) + 1e-10)

    # Measure topology: count connected components at threshold
    threshold = v_mean + 0.5 * v_std
    binary = V > threshold
    fill_fraction = np.mean(binary)

    return {
        'v_std': float(v_std),
        'v_mean': float(v_mean),
        'wavelength': float(dominant_wavelength),
        'anisotropy': float(anisotropy),
        'fill_fraction': float(fill_fraction)
    }, 'ok'

def classify_3d_pattern(V, threshold=None):
    """
    Attempt to classify 3D pattern type.

    Possible types:
    - spheres: isolated 3D spots
    - tubes: elongated structures
    - lamellae: layered sheets
    - gyroid: complex 3D surface
    - network: interconnected structure
    """
    if threshold is None:
        threshold = np.mean(V) + 0.5 * np.std(V)

    binary = V > threshold
    fill = np.mean(binary)

    if np.std(V) < 0.02:
        return 'uniform'

    # Analyze structure using autocorrelation
    V_centered = V - np.mean(V)
    fft = np.fft.fftn(V_centered)
    autocorr = np.fft.ifftn(np.abs(fft)**2).real
    autocorr = np.fft.fftshift(autocorr)
    autocorr = autocorr / autocorr.max()

    N = V.shape[0]
    center = N // 2

    # Correlation lengths in each direction
    x_decay = autocorr[center, center, center:]
    y_decay = autocorr[center, center:, center]
    z_decay = autocorr[center:, center, center]

    def correlation_length(profile):
        for i, val in enumerate(profile):
            if val < 0.5:
                return i
        return len(profile)

    lx = correlation_length(x_decay)
    ly = correlation_length(y_decay)
    lz = correlation_length(z_decay)

    lengths = [lx, ly, lz]
    mean_length = np.mean(lengths)
    length_anisotropy = np.std(lengths) / (mean_length + 1)

    if fill < 0.1:
        if length_anisotropy < 0.3:
            return 'spheres'
        else:
            return 'tubes'
    elif fill > 0.35 and fill < 0.65:
        if length_anisotropy > 0.5:
            return 'lamellae'
        else:
            return 'gyroid_or_network'
    elif fill > 0.8:
        return 'inverse_spheres'
    else:
        return 'mixed'

def run_3d_simulation(f, k, n_steps=20000):
    """Run 3D simulation and analyze."""
    U, V = init_nucleated_3d(N)

    for _ in range(n_steps):
        U, V = step_3d(U, V, f, k)

    measurements, status = measure_pattern_3d(V)
    if status != 'ok':
        return None, status

    pattern_type = classify_3d_pattern(V)
    measurements['pattern_type'] = pattern_type

    return measurements, 'ok'

def main():
    print("=" * 70)
    print("3D GRAY-SCOTT PATTERN EXPLORATION")
    print("=" * 70)
    print()
    print(f"Grid size: {N}x{N}x{N} (small for feasibility)")
    print("This is a LESS EXPLORED regime!")
    print()

    # Test across parameter space
    test_points = []
    for f in [0.024, 0.030, 0.036, 0.042, 0.048]:
        for k_offset in [-0.002, 0, 0.002, 0.004]:
            k = 0.054 + (f - 0.030) * 0.35 + k_offset
            test_points.append((f, k))

    results = []

    print(f"{'f':>6} {'k':>6} {'type':>15} {'wavelen':>8} {'aniso':>8} {'fill':>6}")
    print("-" * 55)

    for f, k in test_points:
        result, status = run_3d_simulation(f, k)

        if status == 'ok':
            ptype = result['pattern_type']
            wlen = result['wavelength']
            aniso = result['anisotropy']
            fill = result['fill_fraction']

            print(f"{f:6.3f} {k:6.3f} {ptype:>15} {wlen:8.2f} {aniso:8.4f} {fill:6.3f}")

            result['f'] = float(f)
            result['k'] = float(k)
            results.append(result)
        else:
            print(f"{f:6.3f} {k:6.3f} {'N/A':>15} {'N/A':>8} {'N/A':>8} {'N/A':>6}")

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    if len(results) < 3:
        print("Not enough valid results")
        return

    # Count pattern types
    type_counts = {}
    for r in results:
        t = r['pattern_type']
        type_counts[t] = type_counts.get(t, 0) + 1

    print("Pattern type distribution:")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t}: {c}")
    print()

    # Compare with 2D expectations
    print("NOVELTY ASSESSMENT:")
    print()

    # In 2D, we expect spots and stripes
    # In 3D, we might see spheres, tubes, lamellae, gyroids
    novel_types = ['gyroid_or_network', 'tubes', 'lamellae']
    novel_count = sum(type_counts.get(t, 0) for t in novel_types)
    total_count = len(results)

    if novel_count > 0:
        print(f"Found {novel_count}/{total_count} potentially 3D-specific patterns!")
        print("These structures may not have direct 2D analogues.")

        # Find examples
        for r in results:
            if r['pattern_type'] in novel_types:
                print(f"  Example: f={r['f']}, k={r['k']} -> {r['pattern_type']}")
    else:
        print("All patterns appear to be 3D versions of 2D patterns (spheres = spots)")

    # Check wavelengths vs 2D
    wavelengths = [r['wavelength'] for r in results if r['wavelength'] < N//2]
    if wavelengths:
        mean_wlen = np.mean(wavelengths)
        print(f"\nMean wavelength: {mean_wlen:.2f} pixels")
        print("(Compare with 2D: typically 6-12 pixels at these parameters)")

        if mean_wlen < 5 or mean_wlen > 15:
            print("[INTERESTING] Wavelength differs significantly from 2D!")

    # Save results
    with open('3d_grayscott_results.json', 'w') as file:
        json.dump({
            'results': results,
            'summary': {
                'type_counts': type_counts,
                'n_valid': len(results),
                'grid_size': N
            }
        }, file, indent=2)

    print()
    print("Results saved to 3d_grayscott_results.json")

if __name__ == '__main__':
    main()
