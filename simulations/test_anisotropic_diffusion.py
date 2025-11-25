#!/usr/bin/env python3
"""
Test ANISOTROPIC DIFFUSION in Gray-Scott.

Standard Gray-Scott uses isotropic diffusion (same in x and y).
What happens when Dx != Dy?

This breaks the rotational symmetry of the system and could:
1. Create oriented stripes preferring one direction
2. Create elliptical spots instead of circular
3. Create entirely new pattern types not in Pearson's classification
4. Change the stability of different pattern types

This is LESS STUDIED because most theoretical analysis assumes isotropy.
"""

import numpy as np
import json

N = 128
dx = 1.0

def anisotropic_laplacian(Z, dx, ratio_x=1.0, ratio_y=1.0):
    """
    Anisotropic Laplacian with different weights in x and y.
    ratio_x * d²Z/dx² + ratio_y * d²Z/dy²
    """
    d2x = (np.roll(Z, 1, axis=1) + np.roll(Z, -1, axis=1) - 2*Z) / (dx*dx)
    d2y = (np.roll(Z, 1, axis=0) + np.roll(Z, -1, axis=0) - 2*Z) / (dx*dx)
    return ratio_x * d2x + ratio_y * d2y

def step(U, V, f, k, Du_x, Du_y, Dv_x, Dv_y):
    uvv = U * V * V
    return (np.clip(U + anisotropic_laplacian(U, dx, Du_x, Du_y) - uvv + f * (1 - U), 0, 1),
            np.clip(V + anisotropic_laplacian(V, dx, Dv_x, Dv_y) + uvv - (k + f) * V, 0, 1))

def init_nucleated(N, seed=42):
    np.random.seed(seed)
    U, V = np.ones((N, N)), np.zeros((N, N))
    for _ in range(12):
        cx, cy = np.random.randint(N//4, 3*N//4, 2)
        r = 4
        y, x = np.ogrid[:N, :N]
        mask = (x-cx)**2 + (y-cy)**2 <= r*r
        U[mask], V[mask] = 0.5, 0.25
    return U, V

def measure_anisotropy(V, threshold=0.05):
    """Measure orientation preference of pattern."""
    v_std = np.std(V)
    if v_std < 0.02:
        return None, 'no_pattern'

    V_centered = V - np.mean(V)
    fft = np.fft.fft2(V_centered)
    power = np.abs(np.fft.fftshift(fft))**2

    N = V.shape[0]
    center = N // 2
    power[center-2:center+3, center-2:center+3] = 0

    # Power along horizontal (x-direction stripes)
    horiz_power = np.sum(power[center-3:center+4, :])
    # Power along vertical (y-direction stripes)
    vert_power = np.sum(power[:, center-3:center+4])
    total_power = np.sum(power)

    horiz_frac = horiz_power / total_power if total_power > 0 else 0
    vert_frac = vert_power / total_power if total_power > 0 else 0

    # Orientation index: positive = horizontal stripes, negative = vertical
    orientation_index = horiz_frac - vert_frac

    return {
        'horiz_frac': float(horiz_frac),
        'vert_frac': float(vert_frac),
        'orientation_index': float(orientation_index),
        'anisotropy_strength': float(abs(orientation_index))
    }, 'ok'

def measure_spot_ellipticity(V, threshold=None):
    """Measure if spots are elliptical."""
    if threshold is None:
        threshold = np.mean(V) + 0.5 * np.std(V)

    binary = V > threshold

    # Use autocorrelation to measure average spot shape
    V_centered = V - np.mean(V)
    fft = np.fft.fft2(V_centered)
    autocorr = np.fft.ifft2(np.abs(fft)**2).real
    autocorr = np.fft.fftshift(autocorr)
    autocorr = autocorr / autocorr.max()

    # Measure width in x and y directions
    center = N // 2
    x_profile = autocorr[center, center:]
    y_profile = autocorr[center:, center]

    # Half-width at half maximum
    def half_width(profile):
        half_max = profile[0] / 2
        for i, val in enumerate(profile):
            if val < half_max:
                return i
        return len(profile)

    width_x = half_width(x_profile)
    width_y = half_width(y_profile)

    ellipticity = width_x / width_y if width_y > 0 else 1.0

    return float(ellipticity)

def run_anisotropic(f, k, aniso_ratio, n_steps=50000):
    """
    Run with anisotropic diffusion.
    aniso_ratio > 1: faster diffusion in x than y
    aniso_ratio < 1: faster diffusion in y than x

    We scale so that the MEAN diffusion is constant.
    Du_mean = 0.16, Dv_mean = 0.08
    """
    Du_mean = 0.16
    Dv_mean = 0.08

    # Du_x * Du_y = Du_mean^2 (geometric mean)
    # Du_x / Du_y = aniso_ratio
    Du_x = Du_mean * np.sqrt(aniso_ratio)
    Du_y = Du_mean / np.sqrt(aniso_ratio)

    Dv_x = Dv_mean * np.sqrt(aniso_ratio)
    Dv_y = Dv_mean / np.sqrt(aniso_ratio)

    U, V = init_nucleated(N)

    for _ in range(n_steps):
        U, V = step(U, V, f, k, Du_x, Du_y, Dv_x, Dv_y)

    aniso_result, status = measure_anisotropy(V)
    if status != 'ok':
        return None, status

    ellipticity = measure_spot_ellipticity(V)

    return {
        **aniso_result,
        'ellipticity': ellipticity,
        'Du_x': float(Du_x),
        'Du_y': float(Du_y),
        'Dv_x': float(Dv_x),
        'Dv_y': float(Dv_y)
    }, 'ok'

def main():
    print("=" * 70)
    print("ANISOTROPIC DIFFUSION IN GRAY-SCOTT")
    print("=" * 70)
    print()
    print("Testing how patterns respond to anisotropic diffusion...")
    print("aniso_ratio > 1: faster x-diffusion, expect y-stripes")
    print("aniso_ratio < 1: faster y-diffusion, expect x-stripes")
    print()

    # Test at a few parameter points known to form patterns
    test_params = [
        (0.030, 0.057),  # spots/mitosis region
        (0.040, 0.062),  # stripes region
        (0.045, 0.064),  # near boundary
    ]

    aniso_ratios = [0.25, 0.5, 1.0, 2.0, 4.0]

    results = []

    print(f"{'f':>6} {'k':>6} {'ratio':>8} {'orient':>10} {'ellip':>8} {'status':>10}")
    print("-" * 60)

    for f, k in test_params:
        for ratio in aniso_ratios:
            result, status = run_anisotropic(f, k, ratio)

            if status == 'ok':
                orient = result['orientation_index']
                ellip = result['ellipticity']
                print(f"{f:6.3f} {k:6.3f} {ratio:8.2f} {orient:10.4f} {ellip:8.3f} {'ok':>10}")

                result['f'] = float(f)
                result['k'] = float(k)
                result['aniso_ratio'] = float(ratio)
                results.append(result)
            else:
                print(f"{f:6.3f} {k:6.3f} {ratio:8.2f} {'N/A':>10} {'N/A':>8} {status:>10}")

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    if len(results) < 3:
        print("Not enough valid results for analysis")
        return

    # Check if anisotropy creates expected orientation
    for f, k in test_params:
        f_results = [r for r in results if r['f'] == f and r['k'] == k]
        if len(f_results) < 3:
            continue

        print(f"f={f}, k={k}:")

        # Check correlation between aniso_ratio and orientation_index
        ratios = [r['aniso_ratio'] for r in f_results]
        orients = [r['orientation_index'] for r in f_results]
        ellips = [r['ellipticity'] for r in f_results]

        # Expected: ratio > 1 → orient < 0 (vertical stripes)
        # Expected: ratio < 1 → orient > 0 (horizontal stripes)

        if len(ratios) >= 3:
            corr = np.corrcoef(np.log(ratios), orients)[0, 1]
            print(f"  Correlation log(ratio) vs orientation: {corr:.3f}")

            # Expected correlation should be negative
            if corr < -0.5:
                print("  [EXPECTED] Higher x-diffusion → vertical stripes")
            elif corr > 0.5:
                print("  [UNEXPECTED] Higher x-diffusion → horizontal stripes!")
            else:
                print("  [WEAK] No clear orientation preference")

            # Check ellipticity
            ellip_corr = np.corrcoef(np.log(ratios), ellips)[0, 1]
            print(f"  Correlation log(ratio) vs ellipticity: {ellip_corr:.3f}")

            if abs(ellip_corr) > 0.5:
                print("  [INTERESTING] Anisotropy affects spot shape!")
        print()

    # Look for novel behavior
    print("NOVELTY ASSESSMENT:")
    print()

    # Does anisotropy create stronger orientation than expected?
    strong_aniso = [r for r in results if r['aniso_ratio'] in [0.25, 4.0]]
    if strong_aniso:
        max_orient = max(abs(r['orientation_index']) for r in strong_aniso)
        print(f"Max orientation index at 4x anisotropy: {max_orient:.4f}")

        if max_orient > 0.5:
            print("  [POTENTIALLY NOVEL] Strong orientation response")
        elif max_orient > 0.2:
            print("  [EXPECTED] Moderate orientation response")
        else:
            print("  [EXPECTED] Weak orientation response - pattern is robust")

    # Save results
    with open('anisotropic_results.json', 'w') as file:
        json.dump({
            'results': results,
            'summary': {
                'n_valid': len(results),
                'aniso_ratios_tested': aniso_ratios
            }
        }, file, indent=2)

    print()
    print("Results saved to anisotropic_results.json")

if __name__ == '__main__':
    main()
