#!/usr/bin/env python3
"""
Map the SUBCRITICAL→SUPERCRITICAL TRANSITION by varying Du/Dv ratio.

The peer reviewer suggested this could be genuinely novel if mapped carefully.
At Du/Dv=2, Gray-Scott is subcritical (patterns require nucleation).
Question: At what Du/Dv ratio does it become supercritical (patterns grow from noise)?

This would map a previously unexplored dimension of the Gray-Scott parameter space.
"""

import numpy as np
import json

# Fixed Dv, vary Du
Dv = 0.08
N = 64
dx = 1.0

def laplacian(Z, dx):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z) / (dx*dx)

def step(U, V, f, k, Du):
    uvv = U * V * V
    return (np.clip(U + Du * laplacian(U, dx) - uvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv - (k + f) * V, 0, 1))

def init_small_perturbation(N):
    """Small random perturbation - tests if patterns grow from infinitesimal noise."""
    U = np.ones((N, N))
    V = np.zeros((N, N))
    np.random.seed(42)
    # Very small perturbation
    U += 0.005 * np.random.randn(N, N)
    V += 0.002 * np.random.randn(N, N)
    return np.clip(U, 0, 1), np.clip(V, 0, 1)

def init_finite_amplitude(N):
    """Finite amplitude spots - tests if patterns survive when nucleated."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    np.random.seed(42)
    for _ in range(8):
        cx, cy = np.random.randint(0, N, 2)
        r = np.random.randint(2, 4)
        y, x = np.ogrid[:N, :N]
        mask = ((np.minimum(np.abs(x-cx), N-np.abs(x-cx)))**2 +
                (np.minimum(np.abs(y-cy), N-np.abs(y-cy)))**2) <= r*r
        U[mask], V[mask] = 0.5, 0.25
    return U, V

def test_bifurcation_type(f, k, Du, n_steps=30000, threshold=0.02):
    """
    Test bifurcation type:
    - SUPERCRITICAL: patterns grow from small perturbations
    - SUBCRITICAL: patterns only form from finite amplitude IC
    """
    # Test 1: Small perturbation
    U, V = init_small_perturbation(N)
    for _ in range(n_steps):
        U, V = step(U, V, f, k, Du)
    small_ic_pattern = np.std(V) > threshold
    small_ic_std = np.std(V)

    # Test 2: Finite amplitude
    U, V = init_finite_amplitude(N)
    for _ in range(n_steps):
        U, V = step(U, V, f, k, Du)
    large_ic_pattern = np.std(V) > threshold
    large_ic_std = np.std(V)

    if small_ic_pattern:
        return 'supercritical', small_ic_std, large_ic_std
    elif large_ic_pattern:
        return 'subcritical', small_ic_std, large_ic_std
    else:
        return 'no_pattern', small_ic_std, large_ic_std

def find_transition_ratio(f, k, du_dv_range, verbose=True):
    """Find the Du/Dv ratio where bifurcation type changes."""
    results = []

    for du_dv in du_dv_range:
        Du = Dv * du_dv
        bif_type, small_std, large_std = test_bifurcation_type(f, k, Du)
        results.append({
            'du_dv': float(du_dv),
            'Du': float(Du),
            'type': bif_type,
            'small_ic_std': float(small_std),
            'large_ic_std': float(large_std)
        })
        if verbose:
            marker = "★" if bif_type == 'supercritical' else ("○" if bif_type == 'subcritical' else "×")
            print(f"  Du/Dv={du_dv:.2f}: {bif_type:13s} (small={small_std:.4f}, large={large_std:.4f}) {marker}")

    return results

def main():
    print("=" * 70)
    print("MAPPING SUBCRITICAL → SUPERCRITICAL TRANSITION vs Du/Dv")
    print("=" * 70)
    print()
    print("At Du/Dv=2.0, Gray-Scott is SUBCRITICAL (patterns need nucleation).")
    print("Question: Does it become SUPERCRITICAL at different Du/Dv ratios?")
    print()
    print("Legend: ★ = supercritical, ○ = subcritical, × = no pattern")
    print()

    # Test points in the known pattern-forming region
    test_points = [
        (0.030, 0.055),  # Classic bistable region
        (0.040, 0.060),  # Higher f
        (0.026, 0.051),  # Near chaos region
    ]

    # Scan Du/Dv ratios from 1.0 to 4.0
    du_dv_values = np.arange(1.0, 4.5, 0.25)

    all_results = {}
    transitions = []

    for f, k in test_points:
        print(f"\n{'='*70}")
        print(f"Testing f={f:.3f}, k={k:.3f}")
        print("-" * 70)

        results = find_transition_ratio(f, k, du_dv_values)
        all_results[f"{f}_{k}"] = results

        # Find transition point
        for i in range(len(results) - 1):
            if results[i]['type'] != results[i+1]['type']:
                if results[i]['type'] == 'supercritical' or results[i+1]['type'] == 'supercritical':
                    trans_low = results[i]['du_dv']
                    trans_high = results[i+1]['du_dv']
                    transitions.append({
                        'f': f, 'k': k,
                        'transition_range': (trans_low, trans_high),
                        'from': results[i]['type'],
                        'to': results[i+1]['type']
                    })

    print()
    print("=" * 70)
    print("TRANSITION SUMMARY")
    print("=" * 70)
    print()

    if transitions:
        print("TRANSITIONS FOUND:")
        for t in transitions:
            print(f"  f={t['f']:.3f}, k={t['k']:.3f}: {t['from']} → {t['to']} at Du/Dv ∈ [{t['transition_range'][0]:.2f}, {t['transition_range'][1]:.2f}]")

        print()
        print("This could be novel! A phase diagram in (f, k, Du/Dv) space showing")
        print("the subcritical-supercritical boundary has not been mapped.")
    else:
        print("No subcritical↔supercritical transitions found in tested range.")
        print()
        # Summarize what we found
        for key, results in all_results.items():
            types = set(r['type'] for r in results)
            print(f"  {key}: {types}")

    # Save results
    with open('bifurcation_transition_results.json', 'w') as file:
        json.dump({
            'du_dv_range': du_dv_values.tolist(),
            'test_points': test_points,
            'results': all_results,
            'transitions': transitions
        }, file, indent=2)

    print()
    print("Results saved to bifurcation_transition_results.json")

if __name__ == '__main__':
    main()
