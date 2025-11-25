#!/usr/bin/env python3
"""
Verify the chaos/pattern coexistence finding at f=0.040, k=0.060.
Run longer simulations and visualize the dynamics.
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

def init_spots(N, n=8):
    U, V = np.ones((N, N)), np.zeros((N, N))
    np.random.seed(42)
    for _ in range(n):
        cx, cy = np.random.randint(0, N, 2)
        r = np.random.randint(2, 4)
        y, x = np.ogrid[:N, :N]
        mask = ((np.minimum(np.abs(x-cx), N-np.abs(x-cx)))**2 +
                (np.minimum(np.abs(y-cy), N-np.abs(y-cy)))**2) <= r*r
        U[mask], V[mask] = 0.5, 0.25
    return U, V

def init_stripes(N, n=4):
    U, V = np.ones((N, N)), np.zeros((N, N))
    w = N // (2 * n)
    for i in range(n):
        s = i * N // n + N // (4 * n)
        U[s:s+w, :], V[s:s+w, :] = 0.5, 0.25
    return U, V

def run_and_track(f, k, U0, V0, total_steps=100000, sample_interval=100):
    """Run simulation and track mean V over time."""
    U, V = U0.copy(), V0.copy()
    v_means = []
    v_stds = []

    for i in range(total_steps):
        U, V = step(U, V, f, k)
        if i % sample_interval == 0:
            v_means.append(np.mean(V))
            v_stds.append(np.std(V))

    return np.array(v_means), np.array(v_stds), V

def main():
    f, k = 0.040, 0.060
    print("=" * 60)
    print(f"VERIFYING CHAOS/PATTERN COEXISTENCE AT f={f}, k={k}")
    print("=" * 60)
    print()

    # Test from spots (claimed chaotic)
    print("Running from SPOTS initial condition (100k steps)...")
    U0, V0 = init_spots(N)
    v_means_spots, v_stds_spots, V_final_spots = run_and_track(f, k, U0, V0)

    # Test from stripes (claimed static)
    print("Running from STRIPES initial condition (100k steps)...")
    U0, V0 = init_stripes(N)
    v_means_stripes, v_stds_stripes, V_final_stripes = run_and_track(f, k, U0, V0)

    print()
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    print()

    # Analyze spots trajectory
    print("FROM SPOTS:")
    print(f"  Initial V mean: {v_means_spots[0]:.6f}")
    print(f"  Final V mean:   {v_means_spots[-1]:.6f}")
    print(f"  Final V std:    {v_stds_spots[-1]:.6f}")

    # Check dynamics in second half
    second_half_spots = v_means_spots[len(v_means_spots)//2:]
    spots_variation = np.std(second_half_spots)
    spots_range = np.max(second_half_spots) - np.min(second_half_spots)
    print(f"  Second half variation (std): {spots_variation:.6f}")
    print(f"  Second half range: {spots_range:.6f}")

    if v_stds_spots[-1] < 0.01:
        print("  --> Decayed to UNIFORM state")
    elif spots_variation < 1e-5:
        print("  --> STATIC PATTERN")
    else:
        print("  --> SUSTAINED DYNAMICS (possible chaos)")

    print()

    # Analyze stripes trajectory
    print("FROM STRIPES:")
    print(f"  Initial V mean: {v_means_stripes[0]:.6f}")
    print(f"  Final V mean:   {v_means_stripes[-1]:.6f}")
    print(f"  Final V std:    {v_stds_stripes[-1]:.6f}")

    second_half_stripes = v_means_stripes[len(v_means_stripes)//2:]
    stripes_variation = np.std(second_half_stripes)
    stripes_range = np.max(second_half_stripes) - np.min(second_half_stripes)
    print(f"  Second half variation (std): {stripes_variation:.6f}")
    print(f"  Second half range: {stripes_range:.6f}")

    if v_stds_stripes[-1] < 0.01:
        print("  --> Decayed to UNIFORM state")
    elif stripes_variation < 1e-5:
        print("  --> STATIC PATTERN")
    else:
        print("  --> SUSTAINED DYNAMICS (possible chaos)")

    print()
    print("=" * 60)
    print("COEXISTENCE CHECK")
    print("=" * 60)
    print()

    spots_is_static = v_stds_spots[-1] > 0.01 and spots_variation < 1e-5
    spots_is_chaotic = v_stds_spots[-1] > 0.01 and spots_variation > 1e-5
    spots_is_uniform = v_stds_spots[-1] < 0.01

    stripes_is_static = v_stds_stripes[-1] > 0.01 and stripes_variation < 1e-5
    stripes_is_chaotic = v_stds_stripes[-1] > 0.01 and stripes_variation > 1e-5
    stripes_is_uniform = v_stds_stripes[-1] < 0.01

    print(f"SPOTS IC outcome:   {'uniform' if spots_is_uniform else ('static' if spots_is_static else 'dynamic')}")
    print(f"STRIPES IC outcome: {'uniform' if stripes_is_uniform else ('static' if stripes_is_static else 'dynamic')}")
    print()

    if (spots_is_static or spots_is_chaotic) and (stripes_is_static or stripes_is_chaotic):
        if spots_is_static != stripes_is_static:
            print("*** COEXISTENCE CONFIRMED! ***")
            print("Different ICs lead to qualitatively different behaviors:")
            print(f"  Spots IC --> {'static pattern' if spots_is_static else 'chaos/oscillation'}")
            print(f"  Stripes IC --> {'static pattern' if stripes_is_static else 'chaos/oscillation'}")
        else:
            print("Both ICs lead to same type of behavior (no coexistence)")
    else:
        print("One or both ICs decay to uniform - no interesting coexistence")

    # Save time series for visualization
    results = {
        'f': f, 'k': k,
        'spots': {
            'v_means': v_means_spots.tolist(),
            'v_stds': v_stds_spots.tolist(),
            'final_std': float(v_stds_spots[-1]),
            'second_half_variation': float(spots_variation),
        },
        'stripes': {
            'v_means': v_means_stripes.tolist(),
            'v_stds': v_stds_stripes.tolist(),
            'final_std': float(v_stds_stripes[-1]),
            'second_half_variation': float(stripes_variation),
        }
    }

    with open('chaos_coexistence_verification.json', 'w') as file:
        json.dump(results, file, indent=2)

    print()
    print("Time series saved to chaos_coexistence_verification.json")

if __name__ == '__main__':
    main()
