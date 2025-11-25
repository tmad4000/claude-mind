#!/usr/bin/env python3
"""
Test PATTERN COARSENING DYNAMICS in Gray-Scott.

When patterns form from random initial conditions, they undergo coarsening:
small structures merge into larger ones over time. The characteristic
length scale L(t) often follows a power law:

    L(t) ~ t^α

where α is a coarsening exponent. Different physics gives different exponents:
- α = 1/3: Curvature-driven coarsening (Lifshitz-Slyozov-Wagner)
- α = 1/2: Diffusion-limited coarsening
- α = 1: Reaction-limited coarsening

Finding a precise coarsening exponent for Gray-Scott could be novel if it:
1. Matches a known universality class
2. Is anomalous (different from expected)
3. Shows crossover behavior
4. Depends on parameters in interesting ways

Method: Track the dominant wavelength over time using FFT.
"""

import numpy as np
import json

Du, Dv = 0.16, 0.08
N = 256  # Large grid for coarsening
dx = 1.0

def laplacian(Z, dx):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z) / (dx*dx)

def step(U, V, f, k):
    uvv = U * V * V
    return (np.clip(U + Du * laplacian(U, dx) - uvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv - (k + f) * V, 0, 1))

def init_random_nucleation(N, seed=42):
    """Initialize with many random nucleation sites."""
    np.random.seed(seed)
    U, V = np.ones((N, N)), np.zeros((N, N))

    # Create many small spots
    n_spots = 100
    for _ in range(n_spots):
        cx, cy = np.random.randint(0, N, 2)
        r = 3
        y, x = np.ogrid[:N, :N]
        # Handle periodic boundaries
        dist_x = np.minimum(np.abs(x - cx), N - np.abs(x - cx))
        dist_y = np.minimum(np.abs(y - cy), N - np.abs(y - cy))
        mask = dist_x**2 + dist_y**2 <= r**2
        U[mask] = 0.5
        V[mask] = 0.25

    return U, V

def measure_characteristic_length(V, threshold=0.05):
    """
    Measure characteristic length scale from the power spectrum.
    Returns the wavelength of the dominant mode.
    """
    v_std = np.std(V)
    if v_std < 0.01:
        return None  # No pattern

    V_centered = V - np.mean(V)
    fft = np.fft.fft2(V_centered)
    power = np.abs(np.fft.fftshift(fft))**2

    N = V.shape[0]
    center = N // 2

    # Mask DC
    power[center-2:center+3, center-2:center+3] = 0

    # Compute radial average of power spectrum
    y, x = np.ogrid[:N, :N]
    r = np.sqrt((x - center)**2 + (y - center)**2).astype(int)

    r_max = N // 2
    radial_power = np.zeros(r_max)
    counts = np.zeros(r_max)

    for i in range(N):
        for j in range(N):
            if r[i, j] < r_max:
                radial_power[r[i, j]] += power[i, j]
                counts[r[i, j]] += 1

    radial_power[counts > 0] /= counts[counts > 0]

    # Find peak in radial power (excluding DC)
    if len(radial_power) < 5:
        return None

    peak_r = np.argmax(radial_power[3:]) + 3

    if peak_r < 3:
        return None

    wavelength = N / peak_r
    return wavelength

def track_coarsening(f, k, max_steps=200000, measure_interval=2000):
    """
    Track the characteristic length scale over time.
    """
    U, V = init_random_nucleation(N)

    times = []
    lengths = []
    v_stds = []

    for step_num in range(max_steps):
        U, V = step(U, V, f, k)

        if step_num % measure_interval == 0 and step_num > 0:
            L = measure_characteristic_length(V)
            v_std = np.std(V)

            if L is not None and L > 3:
                times.append(step_num)
                lengths.append(L)
                v_stds.append(v_std)

            # Early termination if no pattern
            if step_num > 20000 and v_std < 0.01:
                return None, None, None, 'no_pattern'

    if len(times) < 5:
        return None, None, None, 'insufficient_data'

    return times, lengths, v_stds, 'ok'

def fit_power_law(times, lengths):
    """
    Fit L(t) ~ t^α using log-log linear regression.
    """
    log_t = np.log(times)
    log_L = np.log(lengths)

    # Use only the later half to avoid transients
    n = len(times)
    start = n // 3

    if n - start < 5:
        return None, None

    log_t_fit = log_t[start:]
    log_L_fit = log_L[start:]

    # Linear fit
    alpha, log_A = np.polyfit(log_t_fit, log_L_fit, 1)

    # R-squared
    y_pred = alpha * log_t_fit + log_A
    ss_res = np.sum((log_L_fit - y_pred)**2)
    ss_tot = np.sum((log_L_fit - np.mean(log_L_fit))**2)
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    return alpha, r_squared

def main():
    print("=" * 70)
    print("PATTERN COARSENING ANALYSIS")
    print("=" * 70)
    print()
    print("Measuring how the characteristic length scale grows over time...")
    print("Looking for power-law scaling: L(t) ~ t^α")
    print()

    # Test at multiple parameter points
    test_points = [
        (0.030, 0.057),
        (0.035, 0.060),
        (0.040, 0.062),
        (0.045, 0.064),
        (0.028, 0.055),
    ]

    results = []

    print(f"{'f':>6} {'k':>6} {'α':>8} {'R²':>8} {'L_final':>10} {'status':>15}")
    print("-" * 60)

    for f, k in test_points:
        times, lengths, v_stds, status = track_coarsening(f, k)

        if status == 'ok' and len(times) > 5:
            alpha, r_squared = fit_power_law(times, lengths)
            L_final = lengths[-1]

            print(f"{f:6.3f} {k:6.3f} {alpha:8.4f} {r_squared:8.3f} {L_final:10.2f} {status:>15}")

            results.append({
                'f': float(f),
                'k': float(k),
                'alpha': float(alpha) if alpha else None,
                'r_squared': float(r_squared) if r_squared else None,
                'L_final': float(L_final),
                'times': times,
                'lengths': lengths,
                'status': status
            })
        else:
            print(f"{f:6.3f} {k:6.3f} {'N/A':>8} {'N/A':>8} {'N/A':>10} {status:>15}")
            results.append({
                'f': float(f),
                'k': float(k),
                'alpha': None,
                'r_squared': None,
                'status': status
            })

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    valid = [r for r in results if r['alpha'] is not None]

    if len(valid) < 2:
        print("Not enough valid coarsening data")
    else:
        alphas = [r['alpha'] for r in valid]
        r_squareds = [r['r_squared'] for r in valid]

        mean_alpha = np.mean(alphas)
        std_alpha = np.std(alphas)

        print(f"Mean coarsening exponent α: {mean_alpha:.4f} ± {std_alpha:.4f}")
        print(f"Mean R²: {np.mean(r_squareds):.3f}")
        print()

        # Interpret the exponent
        if abs(mean_alpha - 0.333) < 0.05:
            print("α ≈ 1/3: Consistent with CURVATURE-DRIVEN coarsening (LSW)")
            print("This is typical for phase separation with surface tension.")
        elif abs(mean_alpha - 0.5) < 0.05:
            print("α ≈ 1/2: Consistent with DIFFUSION-LIMITED coarsening")
        elif abs(mean_alpha - 1.0) < 0.1:
            print("α ≈ 1: Consistent with REACTION-LIMITED coarsening")
        elif mean_alpha < 0.2:
            print(f"α ≈ {mean_alpha:.2f}: VERY SLOW coarsening (possibly frozen)")
        elif mean_alpha > 0.7:
            print(f"α ≈ {mean_alpha:.2f}: FAST coarsening (possibly super-diffusive)")
        else:
            print(f"α ≈ {mean_alpha:.2f}: INTERMEDIATE exponent")
            print("This might indicate crossover or mixed dynamics.")

        # Check parameter dependence
        if len(valid) >= 3:
            f_vals = [r['f'] for r in valid]
            if len(set(f_vals)) > 1:
                corr = np.corrcoef(f_vals, alphas)[0, 1]
                print()
                print(f"Correlation of α with f: {corr:.3f}")
                if abs(corr) > 0.7:
                    print("Strong parameter dependence of coarsening exponent!")

    # Save results
    with open('coarsening_results.json', 'w') as file:
        # Convert lists to avoid numpy serialization issues
        clean_results = []
        for r in results:
            clean_r = {k: v for k, v in r.items()}
            if 'times' in clean_r and clean_r['times']:
                clean_r['times'] = [int(t) for t in clean_r['times']]
            if 'lengths' in clean_r and clean_r['lengths']:
                clean_r['lengths'] = [float(L) for L in clean_r['lengths']]
            clean_results.append(clean_r)

        json.dump({
            'results': clean_results,
            'summary': {
                'mean_alpha': float(mean_alpha) if valid else None,
                'std_alpha': float(std_alpha) if valid else None
            }
        }, file, indent=2)

    print()
    print("Results saved to coarsening_results.json")

if __name__ == '__main__':
    main()
