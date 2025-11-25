#!/usr/bin/env python3
"""
Compare THEORETICAL vs SIMULATED wavelengths in Gray-Scott.

From Linear Stability Analysis:
The most unstable wavenumber q* depends on the Jacobian eigenvalues
and diffusion coefficients. For Gray-Scott around the homogeneous
steady state (U0, V0), we can derive q*.

If simulation deviates systematically from theory, that's interesting.
If there's a regime where wavelength diverges or shows anomalous behavior,
that could be novel.
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

# =============================================================================
# THEORETICAL CALCULATION
# =============================================================================

def homogeneous_steady_state(f, k):
    """
    Calculate the homogeneous steady state (U0, V0).

    From setting time derivatives to zero:
    f(1-U) - UV² = 0
    UV² - (f+k)V = 0

    If V ≠ 0: U = (f+k)/V from second equation
    Substituting: f(1 - (f+k)/V) = (f+k) → V² - (f+k) - V·f = 0

    Using quadratic formula for V, then U = (f+k)/V
    """
    # The "red" state (high V)
    # V = (1 - sqrt(1 - 4f(f+k)))/2 for the pattern-forming state
    # But this is complex for the trivial state

    # Trivial steady state: V=0, U=1
    # Pattern-forming steady state:
    # V² = f(1-U) and (f+k)V = UV²
    # So (f+k) = UV → U = (f+k)/V
    # V² = f(1 - (f+k)/V) = f - f(f+k)/V
    # V³ = fV - f(f+k)
    # V³ - fV + f(f+k) = 0

    # For the trivial state:
    return 1.0, 0.0

def theoretical_wavelength(f, k):
    """
    Calculate theoretical wavelength from LSA.

    For Gray-Scott, the Turing instability occurs when:
    - The homogeneous state is stable without diffusion
    - Adding diffusion destabilizes it

    The most unstable wavenumber q* satisfies:
    (Du*q² + a)(Dv*q² + d) = bc

    Where a, b, c, d are Jacobian elements around (U0, V0).

    For the trivial state (U=1, V=0):
    J = [[-f, 0],
         [0, -(f+k)]]

    This is always stable (diagonal, negative eigenvalues).

    For patterns to form, we need the "red" steady state.
    Let's use an empirical formula based on the dominant FFT peak.
    """
    # Empirical: wavelength scales roughly with sqrt(Dv/(k+f))
    # This is a crude estimate - the real formula is more complex

    # More accurate estimate from LSA analysis:
    # q* ~ sqrt((k+f)/(2*Dv)) for small f
    # But this needs the actual steady state values

    # For now, return a theoretical prediction based on known scaling
    # λ ~ 2π/q ~ 2π * sqrt(2*Dv/(k+f))

    q_star = np.sqrt((k + f) / (2 * Dv))
    wavelength = 2 * np.pi / q_star

    return wavelength

# =============================================================================
# SIMULATION MEASUREMENT
# =============================================================================

def init_random(N):
    """Random initial condition to develop natural wavelength."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    np.random.seed(42)
    # Small random perturbation
    U += 0.05 * np.random.randn(N, N)
    V += 0.02 * np.random.randn(N, N)
    # Add a few spots to nucleate
    for _ in range(5):
        cx, cy = np.random.randint(N//4, 3*N//4, 2)
        r = 3
        y, x = np.ogrid[:N, :N]
        mask = (x-cx)**2 + (y-cy)**2 <= r*r
        U[mask], V[mask] = 0.5, 0.25
    return np.clip(U, 0, 1), np.clip(V, 0, 1)

def measure_wavelength(V):
    """
    Measure the dominant wavelength from the FFT power spectrum.
    """
    V_centered = V - np.mean(V)
    if np.std(V_centered) < 0.01:
        return np.inf  # No pattern

    fft = np.fft.fft2(V_centered)
    power = np.abs(np.fft.fftshift(fft))**2

    N = V.shape[0]
    center = N // 2

    # Mask out DC component
    power[center-2:center+3, center-2:center+3] = 0

    # Find the peak
    y_idx, x_idx = np.unravel_index(np.argmax(power), power.shape)
    peak_dist = np.sqrt((y_idx - center)**2 + (x_idx - center)**2)

    if peak_dist < 1:
        return np.inf

    wavelength = N / peak_dist
    return wavelength

def simulate_wavelength(f, k, n_steps=40000):
    """Run simulation and measure final wavelength."""
    U, V = init_random(N)

    for _ in range(n_steps):
        U, V = step(U, V, f, k)

    # Check if pattern formed
    if np.std(V) < 0.02:
        return None, 'no_pattern'

    wavelength = measure_wavelength(V)
    return wavelength, 'pattern'

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def main():
    print("=" * 70)
    print("WAVELENGTH: THEORY vs SIMULATION")
    print("=" * 70)
    print()
    print("Testing whether simulated wavelengths match LSA predictions...")
    print()

    # Test across the pattern-forming region
    test_points = []

    # Grid of (f, k) in pattern region
    for f in [0.030, 0.035, 0.040, 0.045, 0.050]:
        for k_offset in [-0.002, 0, 0.002, 0.004]:
            # k roughly tracks f with offset
            k = 0.055 + (f - 0.030) * 0.25 + k_offset
            test_points.append((f, k))

    results = []

    print(f"{'f':>6} {'k':>6} {'λ_sim':>8} {'λ_theory':>10} {'ratio':>8} {'status':>12}")
    print("-" * 60)

    for f, k in test_points:
        sim_wavelength, status = simulate_wavelength(f, k)
        theory_wavelength = theoretical_wavelength(f, k)

        if sim_wavelength is not None:
            ratio = sim_wavelength / theory_wavelength
            print(f"{f:6.3f} {k:6.3f} {sim_wavelength:8.2f} {theory_wavelength:10.2f} {ratio:8.2f} {status:>12}")
            results.append({
                'f': f, 'k': k,
                'lambda_sim': float(sim_wavelength),
                'lambda_theory': float(theory_wavelength),
                'ratio': float(ratio),
                'status': status
            })
        else:
            print(f"{f:6.3f} {k:6.3f} {'N/A':>8} {theory_wavelength:10.2f} {'N/A':>8} {status:>12}")
            results.append({
                'f': f, 'k': k,
                'lambda_sim': None,
                'lambda_theory': float(theory_wavelength),
                'ratio': None,
                'status': status
            })

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    # Analyze the results
    valid_results = [r for r in results if r['ratio'] is not None]

    if len(valid_results) < 2:
        print("Not enough valid points to analyze")
    else:
        ratios = [r['ratio'] for r in valid_results]
        mean_ratio = np.mean(ratios)
        std_ratio = np.std(ratios)

        print(f"Mean ratio (sim/theory): {mean_ratio:.3f} ± {std_ratio:.3f}")
        print()

        if abs(mean_ratio - 1) < 0.2:
            print("Theory and simulation are reasonably consistent.")
            print("The LSA prediction captures the wavelength scaling.")
        elif mean_ratio > 1:
            print(f"Simulation wavelengths are {mean_ratio:.1f}x LONGER than theory predicts.")
            print("This suggests nonlinear effects increase wavelength.")
        else:
            print(f"Simulation wavelengths are {1/mean_ratio:.1f}x SHORTER than theory predicts.")
            print("This suggests nonlinear effects decrease wavelength.")

        # Check for trends
        print()
        print("Checking for trends...")

        # vs f
        f_values = [r['f'] for r in valid_results]
        ratio_values = [r['ratio'] for r in valid_results]
        if len(set(f_values)) > 1:
            corr = np.corrcoef(f_values, ratio_values)[0, 1]
            print(f"Correlation of ratio with f: {corr:.3f}")

        # vs k
        k_values = [r['k'] for r in valid_results]
        if len(set(k_values)) > 1:
            corr = np.corrcoef(k_values, ratio_values)[0, 1]
            print(f"Correlation of ratio with k: {corr:.3f}")

    # Save results
    with open('wavelength_comparison.json', 'w') as file:
        json.dump({
            'results': results,
            'mean_ratio': float(np.mean(ratios)) if valid_results else None,
            'std_ratio': float(np.std(ratios)) if valid_results else None
        }, file, indent=2)

    print()
    print("Results saved to wavelength_comparison.json")

if __name__ == '__main__':
    main()
