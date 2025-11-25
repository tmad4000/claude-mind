#!/usr/bin/env python3
"""
Test STOCHASTIC GRAY-SCOTT with noise.

Adding noise to Gray-Scott could reveal:
1. Noise-induced pattern formation (patterns at parameters where deterministic system is uniform)
2. Noise-induced transitions between pattern types
3. Stochastic resonance effects
4. Pattern selection by noise

This is GENUINELY LESS STUDIED than deterministic Gray-Scott.
Most simulations use deterministic dynamics.

We test:
1. Additive noise (thermal fluctuations)
2. Multiplicative noise (concentration-dependent fluctuations)
3. Both together
"""

import numpy as np
import json

Du, Dv = 0.16, 0.08
N = 64
dx = 1.0
dt = 1.0

def laplacian(Z, dx):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z) / (dx*dx)

def step_deterministic(U, V, f, k):
    uvv = U * V * V
    return (np.clip(U + Du * laplacian(U, dx) - uvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv - (k + f) * V, 0, 1))

def step_stochastic(U, V, f, k, noise_strength=0.01, noise_type='additive'):
    """
    Stochastic Gray-Scott step.

    noise_type:
    - 'additive': add Gaussian noise to both U and V
    - 'multiplicative': noise proportional to concentration
    - 'both': both types together
    """
    uvv = U * V * V

    # Deterministic part
    dU = Du * laplacian(U, dx) - uvv + f * (1 - U)
    dV = Dv * laplacian(V, dx) + uvv - (k + f) * V

    # Noise part
    noise_U = np.random.randn(N, N)
    noise_V = np.random.randn(N, N)

    if noise_type == 'additive':
        dU += noise_strength * noise_U
        dV += noise_strength * noise_V
    elif noise_type == 'multiplicative':
        dU += noise_strength * U * noise_U
        dV += noise_strength * V * noise_V
    elif noise_type == 'both':
        dU += noise_strength * (noise_U + U * np.random.randn(N, N))
        dV += noise_strength * (noise_V + V * np.random.randn(N, N))

    return (np.clip(U + dU, 0, 1), np.clip(V + dV, 0, 1))

def init_uniform(N):
    """Initialize at uniform state (small perturbations)."""
    U = np.ones((N, N))
    V = np.zeros((N, N))
    return U, V

def init_nucleated(N, seed=42):
    np.random.seed(seed)
    U, V = np.ones((N, N)), np.zeros((N, N))
    for _ in range(8):
        cx, cy = np.random.randint(N//4, 3*N//4, 2)
        r = 4
        y, x = np.ogrid[:N, :N]
        mask = (x-cx)**2 + (y-cy)**2 <= r*r
        U[mask], V[mask] = 0.5, 0.25
    return U, V

def measure_pattern(V):
    """Measure pattern properties."""
    v_std = np.std(V)
    v_mean = np.mean(V)

    if v_std < 0.02:
        return {'has_pattern': False, 'v_std': float(v_std), 'v_mean': float(v_mean)}

    # FFT analysis
    V_centered = V - v_mean
    fft = np.fft.fft2(V_centered)
    power = np.abs(np.fft.fftshift(fft))**2

    center = N // 2
    power[center-2:center+3, center-2:center+3] = 0

    # Find dominant wavelength
    y, x = np.ogrid[:N, :N]
    r = np.sqrt((x - center)**2 + (y - center)**2)
    r = r.astype(int)
    radial_power = np.bincount(r.ravel(), weights=power.ravel())
    radial_counts = np.bincount(r.ravel())
    radial_avg = radial_power / (radial_counts + 1e-10)

    peak_k = np.argmax(radial_avg[1:N//3]) + 1
    wavelength = N / peak_k if peak_k > 0 else N

    return {
        'has_pattern': True,
        'v_std': float(v_std),
        'v_mean': float(v_mean),
        'wavelength': float(wavelength)
    }

def run_stochastic_test(f, k, noise_strength, noise_type, init_type='uniform', n_steps=30000):
    """Run stochastic simulation."""
    if init_type == 'uniform':
        U, V = init_uniform(N)
    else:
        U, V = init_nucleated(N)

    for _ in range(n_steps):
        U, V = step_stochastic(U, V, f, k, noise_strength, noise_type)

    return measure_pattern(V)

def run_deterministic_test(f, k, init_type='uniform', n_steps=30000):
    """Run deterministic simulation for comparison."""
    if init_type == 'uniform':
        U, V = init_uniform(N)
    else:
        U, V = init_nucleated(N)

    for _ in range(n_steps):
        U, V = step_deterministic(U, V, f, k)

    return measure_pattern(V)

def main():
    print("=" * 70)
    print("STOCHASTIC GRAY-SCOTT ANALYSIS")
    print("=" * 70)
    print()
    print("Testing noise effects on pattern formation...")
    print()

    # Test at parameters near the boundary where deterministic system
    # should be subcritical (patterns don't form from uniform IC)
    test_points = [
        # At these points, deterministic from uniform IC gives no patterns
        # but nucleated IC gives patterns (subcritical region)
        (0.028, 0.056),
        (0.032, 0.059),
        (0.036, 0.061),
        # Also test well inside pattern region
        (0.040, 0.063),
    ]

    noise_strengths = [0.0, 0.001, 0.005, 0.01, 0.02]
    noise_types = ['additive', 'multiplicative']

    results = []

    # First, establish baseline: deterministic from uniform IC
    print("BASELINE: Deterministic from uniform IC")
    print(f"{'f':>6} {'k':>6} {'pattern?':>10}")
    print("-" * 25)

    for f, k in test_points:
        det_result = run_deterministic_test(f, k, init_type='uniform')
        print(f"{f:6.3f} {k:6.3f} {det_result['has_pattern']!s:>10}")

    print()
    print("STOCHASTIC: From uniform IC with noise")
    print(f"{'f':>6} {'k':>6} {'noise':>8} {'type':>14} {'pattern?':>10} {'v_std':>8}")
    print("-" * 60)

    for f, k in test_points:
        for noise_type in noise_types:
            for noise in noise_strengths:
                if noise == 0:
                    continue  # Skip zero noise (same as deterministic)

                stoch_result = run_stochastic_test(f, k, noise, noise_type, init_type='uniform')
                has_pattern = stoch_result['has_pattern']
                v_std = stoch_result['v_std']

                print(f"{f:6.3f} {k:6.3f} {noise:8.4f} {noise_type:>14} {has_pattern!s:>10} {v_std:8.4f}")

                results.append({
                    'f': float(f),
                    'k': float(k),
                    'noise_strength': float(noise),
                    'noise_type': noise_type,
                    'init_type': 'uniform',
                    **stoch_result
                })

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    # Look for noise-induced pattern formation
    print("NOISE-INDUCED PATTERN FORMATION:")
    print()

    for f, k in test_points:
        # Check deterministic baseline
        det_result = run_deterministic_test(f, k, init_type='uniform')
        det_has_pattern = det_result['has_pattern']

        if det_has_pattern:
            print(f"f={f}, k={k}: Deterministic already forms patterns - can't test noise induction")
            continue

        # Check if any noise level induced patterns
        point_results = [r for r in results if r['f'] == f and r['k'] == k]
        noise_induced = [r for r in point_results if r['has_pattern']]

        if noise_induced:
            print(f"[POTENTIALLY NOVEL] f={f}, k={k}:")
            print(f"  Deterministic: no pattern (v_std={det_result['v_std']:.4f})")
            print(f"  NOISE INDUCED PATTERNS at:")
            for r in noise_induced:
                print(f"    noise={r['noise_strength']}, type={r['noise_type']}, v_std={r['v_std']:.4f}")
        else:
            print(f"f={f}, k={k}: No noise-induced pattern formation detected")

    print()
    print("NOVELTY ASSESSMENT:")
    print()

    # Count noise-induced patterns
    noise_induced_count = 0
    for f, k in test_points:
        det_result = run_deterministic_test(f, k, init_type='uniform')
        if not det_result['has_pattern']:
            point_results = [r for r in results if r['f'] == f and r['k'] == k and r['has_pattern']]
            if point_results:
                noise_induced_count += 1

    if noise_induced_count > 0:
        print(f"Found {noise_induced_count} parameter points with noise-induced patterns!")
        print("This could be a NOVEL FINDING if not previously documented for Gray-Scott.")
        print()
        print("Physical interpretation:")
        print("  Noise can kick the system over the nucleation barrier")
        print("  that normally prevents pattern formation in subcritical region.")
    else:
        print("No noise-induced pattern formation detected.")
        print("This is expected - the subcritical barrier is likely too high")
        print("for the noise strengths tested.")

    # Save results
    with open('stochastic_grayscott_results.json', 'w') as file:
        json.dump({
            'results': results,
            'summary': {
                'noise_induced_count': noise_induced_count,
                'test_points': test_points,
                'noise_strengths': noise_strengths
            }
        }, file, indent=2)

    print()
    print("Results saved to stochastic_grayscott_results.json")

if __name__ == '__main__':
    main()
