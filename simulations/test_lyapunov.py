#!/usr/bin/env python3
"""
Calculate LYAPUNOV EXPONENT for Gray-Scott chaotic dynamics.

The Lyapunov exponent λ quantifies the rate of separation of infinitesimally
close trajectories. For chaos: λ > 0. Larger λ means faster divergence.

Method:
1. Run two trajectories starting from nearly identical states
2. Track how the distance between them grows: d(t) ~ d(0) * exp(λ*t)
3. Periodically renormalize to avoid saturation

Finding the Lyapunov exponent as a function of parameters could reveal:
- Onset of chaos (where λ becomes positive)
- Strength of chaos
- Comparison with theory

This is quantitative characterization that could be novel if it reveals
unexpected structure in the chaos or matches/contradicts theoretical predictions.
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

def init_nucleated(N, seed=42):
    """Initialize with nucleation sites."""
    np.random.seed(seed)
    U, V = np.ones((N, N)), np.zeros((N, N))
    for _ in range(8):
        cx, cy = np.random.randint(N//4, 3*N//4, 2)
        r = 4
        y, x = np.ogrid[:N, :N]
        mask = (x-cx)**2 + (y-cy)**2 <= r*r
        U[mask], V[mask] = 0.5, 0.25
    return U, V

def calculate_lyapunov(f, k, warmup=20000, n_renorm=50, steps_per_renorm=500):
    """
    Calculate the largest Lyapunov exponent.

    Method:
    1. Run to warmup to get on attractor
    2. Create a perturbed copy with small initial separation
    3. Track divergence, renormalizing periodically
    4. Average the log growth rate
    """
    # Warmup
    U1, V1 = init_nucleated(N)
    for _ in range(warmup):
        U1, V1 = step(U1, V1, f, k)

    # Check if pattern exists
    if np.std(V1) < 0.02:
        return None, 'no_pattern'

    # Create perturbed copy
    epsilon = 1e-8
    U2 = U1 + epsilon * np.random.randn(N, N)
    V2 = V1 + epsilon * np.random.randn(N, N)
    U2 = np.clip(U2, 0, 1)
    V2 = np.clip(V2, 0, 1)

    d0 = np.sqrt(np.sum((U2-U1)**2 + (V2-V1)**2))

    log_stretches = []

    for _ in range(n_renorm):
        # Evolve both trajectories
        for _ in range(steps_per_renorm):
            U1, V1 = step(U1, V1, f, k)
            U2, V2 = step(U2, V2, f, k)

        # Measure distance
        d = np.sqrt(np.sum((U2-U1)**2 + (V2-V1)**2))

        if d < 1e-15:
            # Trajectories collapsed - not chaotic
            return -np.inf, 'collapsed'

        # Calculate stretching factor
        stretch = d / d0
        log_stretches.append(np.log(stretch))

        # Renormalize: reset U2, V2 to be epsilon away from U1, V1
        delta_U = U2 - U1
        delta_V = V2 - V1
        norm = np.sqrt(np.sum(delta_U**2 + delta_V**2))

        U2 = U1 + (epsilon / norm) * delta_U
        V2 = V1 + (epsilon / norm) * delta_V
        U2 = np.clip(U2, 0, 1)
        V2 = np.clip(V2, 0, 1)
        d0 = epsilon

    # Average log stretch per step
    lyapunov = np.mean(log_stretches) / steps_per_renorm

    if lyapunov > 0:
        return lyapunov, 'chaotic'
    else:
        return lyapunov, 'non_chaotic'

def main():
    print("=" * 70)
    print("LYAPUNOV EXPONENT ANALYSIS")
    print("=" * 70)
    print()
    print("Calculating Lyapunov exponents across parameter space...")
    print()

    # Scan parameters including known chaotic region
    test_points = []

    # Known chaotic region (from previous exploration)
    for f in [0.024, 0.026, 0.028, 0.030]:
        for k in [0.049, 0.051, 0.053, 0.055]:
            test_points.append((f, k))

    # Also test in pattern region
    for f in [0.035, 0.040, 0.045]:
        for k in [0.058, 0.062, 0.066]:
            test_points.append((f, k))

    results = []

    print(f"{'f':>6} {'k':>6} {'λ':>12} {'status':>15}")
    print("-" * 45)

    for f, k in test_points:
        lyap, status = calculate_lyapunov(f, k)

        if lyap is not None:
            print(f"{f:6.3f} {k:6.3f} {lyap:12.6f} {status:>15}")
        else:
            print(f"{f:6.3f} {k:6.3f} {'N/A':>12} {status:>15}")

        results.append({
            'f': float(f),
            'k': float(k),
            'lyapunov': float(lyap) if lyap is not None else None,
            'status': status
        })

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    # Separate chaotic and non-chaotic
    chaotic = [r for r in results if r['status'] == 'chaotic']
    non_chaotic = [r for r in results if r['status'] == 'non_chaotic']

    print(f"Chaotic points: {len(chaotic)}")
    print(f"Non-chaotic points: {len(non_chaotic)}")
    print()

    if chaotic:
        lyapunovs = [r['lyapunov'] for r in chaotic]
        print(f"Lyapunov exponents in chaotic region:")
        print(f"  Min: {min(lyapunovs):.6f}")
        print(f"  Max: {max(lyapunovs):.6f}")
        print(f"  Mean: {np.mean(lyapunovs):.6f}")
        print()

        # Check for parameter dependence
        f_vals = [r['f'] for r in chaotic]
        k_vals = [r['k'] for r in chaotic]

        if len(set(f_vals)) > 1:
            corr_f = np.corrcoef(f_vals, lyapunovs)[0, 1]
            print(f"Correlation of λ with f: {corr_f:.3f}")

        if len(set(k_vals)) > 1:
            corr_k = np.corrcoef(k_vals, lyapunovs)[0, 1]
            print(f"Correlation of λ with k: {corr_k:.3f}")

    # Find chaos boundary
    print()
    print("Looking for chaos-order boundary...")

    # Group by f and find transition
    f_values = sorted(set(r['f'] for r in results))
    for f_val in f_values:
        f_results = [r for r in results if r['f'] == f_val]
        f_results.sort(key=lambda x: x['k'])

        chaotic_k = [r['k'] for r in f_results if r['status'] == 'chaotic']
        non_chaotic_k = [r['k'] for r in f_results if r['status'] == 'non_chaotic']

        if chaotic_k and non_chaotic_k:
            boundary = (max(chaotic_k) + min(non_chaotic_k)) / 2
            print(f"  f={f_val:.3f}: chaos → order at k ≈ {boundary:.3f}")

    # Save results
    with open('lyapunov_results.json', 'w') as file:
        json.dump({
            'results': results,
            'summary': {
                'n_chaotic': len(chaotic),
                'n_non_chaotic': len(non_chaotic),
                'mean_lyapunov': float(np.mean([r['lyapunov'] for r in chaotic])) if chaotic else None
            }
        }, file, indent=2)

    print()
    print("Results saved to lyapunov_results.json")

if __name__ == '__main__':
    main()
