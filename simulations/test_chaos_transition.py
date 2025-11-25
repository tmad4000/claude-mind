#!/usr/bin/env python3
"""
Examine the CHAOS-TO-ORDER TRANSITION in detail.

The Lyapunov analysis showed:
- Chaos at f=0.024-0.026, k~0.051-0.055 (λ~0.0005)
- Non-chaotic patterns at f>0.030

What happens in between? Possibilities:
1. Sharp transition (first-order-like)
2. Gradual transition (continuous, possibly critical)
3. Intermittency (alternating chaos/order)
4. Different route to chaos (period doubling, quasiperiodicity)

Finding a specific route to chaos or critical exponents could be novel.
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
    np.random.seed(seed)
    U, V = np.ones((N, N)), np.zeros((N, N))
    for _ in range(8):
        cx, cy = np.random.randint(N//4, 3*N//4, 2)
        r = 4
        y, x = np.ogrid[:N, :N]
        mask = (x-cx)**2 + (y-cy)**2 <= r*r
        U[mask], V[mask] = 0.5, 0.25
    return U, V

def analyze_time_series(f, k, warmup=30000, measure=20000, sample_interval=50):
    """
    Analyze time series for chaos indicators.
    """
    U, V = init_nucleated(N)

    # Warmup
    for _ in range(warmup):
        U, V = step(U, V, f, k)

    if np.std(V) < 0.02:
        return None, 'no_pattern'

    # Collect time series
    v_mean_series = []
    v_std_series = []

    for step_num in range(measure):
        U, V = step(U, V, f, k)
        if step_num % sample_interval == 0:
            v_mean_series.append(np.mean(V))
            v_std_series.append(np.std(V))

    v_mean_series = np.array(v_mean_series)
    v_std_series = np.array(v_std_series)

    # Analyze time series

    # 1. Variance of time series (measure of variability)
    variance = np.var(v_std_series)

    # 2. Autocorrelation at lag 1
    if len(v_std_series) > 10:
        autocorr = np.corrcoef(v_std_series[:-1], v_std_series[1:])[0, 1]
    else:
        autocorr = 0

    # 3. Power spectrum - look for peaks
    fft = np.fft.fft(v_std_series - np.mean(v_std_series))
    power = np.abs(fft[:len(fft)//2])**2

    # Find dominant frequency
    if len(power) > 3:
        # Exclude DC
        peak_idx = np.argmax(power[1:]) + 1
        peak_freq = peak_idx / len(v_std_series)
        peak_power = power[peak_idx]
        total_power = np.sum(power[1:])
        spectral_concentration = peak_power / total_power if total_power > 0 else 0
    else:
        peak_freq = 0
        spectral_concentration = 0

    # 4. Classify dynamics
    if variance < 1e-8:
        dynamics = 'static'
    elif spectral_concentration > 0.5:
        dynamics = 'periodic'
    elif autocorr > 0.8:
        dynamics = 'quasiperiodic'
    elif variance > 1e-5:
        dynamics = 'chaotic'
    else:
        dynamics = 'weakly_varying'

    return {
        'variance': float(variance),
        'autocorr': float(autocorr),
        'peak_freq': float(peak_freq),
        'spectral_concentration': float(spectral_concentration),
        'dynamics': dynamics
    }, 'ok'

def compute_lyapunov_quick(f, k, n_steps=30000, epsilon=1e-8):
    """Quick Lyapunov estimate."""
    U1, V1 = init_nucleated(N)

    # Warmup
    for _ in range(20000):
        U1, V1 = step(U1, V1, f, k)

    if np.std(V1) < 0.02:
        return None

    # Perturb
    U2 = U1 + epsilon * np.random.randn(N, N)
    V2 = V1 + epsilon * np.random.randn(N, N)
    U2 = np.clip(U2, 0, 1)
    V2 = np.clip(V2, 0, 1)

    d0 = np.sqrt(np.sum((U2-U1)**2 + (V2-V1)**2))

    total_log_stretch = 0
    n_renorm = 0

    for _ in range(n_steps):
        U1, V1 = step(U1, V1, f, k)
        U2, V2 = step(U2, V2, f, k)

        if _ % 500 == 0 and _ > 0:
            d = np.sqrt(np.sum((U2-U1)**2 + (V2-V1)**2))
            if d < 1e-15:
                return -10  # Collapsed

            total_log_stretch += np.log(d / epsilon)
            n_renorm += 1

            # Renormalize
            delta_U = U2 - U1
            delta_V = V2 - V1
            norm = np.sqrt(np.sum(delta_U**2 + delta_V**2))
            U2 = U1 + (epsilon / norm) * delta_U
            V2 = V1 + (epsilon / norm) * delta_V
            U2 = np.clip(U2, 0, 1)
            V2 = np.clip(V2, 0, 1)

    if n_renorm == 0:
        return None

    return total_log_stretch / (n_renorm * 500)

def main():
    print("=" * 70)
    print("CHAOS-TO-ORDER TRANSITION ANALYSIS")
    print("=" * 70)
    print()
    print("Fine scan of parameters between chaotic and ordered regions...")
    print()

    results = []

    # Fine scan of f at fixed k values
    k_values = [0.053, 0.055, 0.057]

    for k in k_values:
        print(f"\nk = {k}")
        print(f"{'f':>6} {'λ':>10} {'variance':>12} {'autocorr':>10} {'dynamics':>15}")
        print("-" * 60)

        for f in np.arange(0.022, 0.036, 0.001):
            lyap = compute_lyapunov_quick(f, k)
            analysis, status = analyze_time_series(f, k)

            if status == 'ok' and lyap is not None:
                var = analysis['variance']
                ac = analysis['autocorr']
                dyn = analysis['dynamics']

                print(f"{f:6.3f} {lyap:10.6f} {var:12.2e} {ac:10.4f} {dyn:>15}")

                results.append({
                    'f': float(f),
                    'k': float(k),
                    'lyapunov': float(lyap),
                    'variance': float(var),
                    'autocorr': float(ac),
                    'dynamics': dyn,
                    'spectral_concentration': float(analysis['spectral_concentration'])
                })
            else:
                print(f"{f:6.3f} {'N/A':>10} {'N/A':>12} {'N/A':>10} {status:>15}")

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    # Look for transition
    chaotic = [r for r in results if r['lyapunov'] > 0]
    ordered = [r for r in results if r['lyapunov'] < 0]

    print(f"Chaotic points (λ > 0): {len(chaotic)}")
    print(f"Ordered points (λ < 0): {len(ordered)}")

    if chaotic and ordered:
        # Find boundary
        for k in k_values:
            k_results = [r for r in results if r['k'] == k]
            k_chaotic = [r for r in k_results if r['lyapunov'] > 0]
            k_ordered = [r for r in k_results if r['lyapunov'] < 0]

            if k_chaotic and k_ordered:
                boundary_f = (max(r['f'] for r in k_chaotic) + min(r['f'] for r in k_ordered)) / 2
                print(f"\nk = {k}: chaos-order boundary at f ≈ {boundary_f:.3f}")

                # Check Lyapunov scaling near boundary
                near_boundary = [r for r in k_results if abs(r['f'] - boundary_f) < 0.005]
                if near_boundary:
                    lyaps = [r['lyapunov'] for r in near_boundary]
                    f_vals = [r['f'] for r in near_boundary]
                    print(f"  λ near boundary: {[f'{l:.6f}' for l in lyaps]}")

                    # Check for power-law scaling
                    # λ ~ |f - f_c|^β for some exponent β
                    epsilon = [abs(r['f'] - boundary_f) for r in near_boundary if r['lyapunov'] > 0]
                    lambda_vals = [r['lyapunov'] for r in near_boundary if r['lyapunov'] > 0]

                    if len(epsilon) >= 3:
                        log_eps = np.log(epsilon)
                        log_lam = np.log(lambda_vals)
                        beta, _ = np.polyfit(log_eps, log_lam, 1)
                        print(f"  Scaling exponent β ≈ {beta:.2f} (λ ~ |f-f_c|^β)")

    # Save results
    with open('chaos_transition_results.json', 'w') as file:
        json.dump({
            'results': results,
            'summary': {
                'n_chaotic': len(chaotic),
                'n_ordered': len(ordered)
            }
        }, file, indent=2)

    print()
    print("Results saved to chaos_transition_results.json")

if __name__ == '__main__':
    main()
