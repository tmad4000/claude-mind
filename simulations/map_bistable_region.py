#!/usr/bin/env python3
"""
Map the boundaries of the bistable region in Gray-Scott parameter space.
"""

import numpy as np
import json

Du, Dv = 0.16, 0.08
N = 64  # Smaller for faster scanning
dx = 1.0

def laplacian(Z, dx):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z) / (dx*dx)

def step(U, V, f, k):
    uvv = U * V * V
    return (np.clip(U + Du * laplacian(U, dx) - uvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv - (k + f) * V, 0, 1))

def init_spots(N, n=10):
    U, V = np.ones((N, N)), np.zeros((N, N))
    np.random.seed(42)
    for _ in range(n):
        cx, cy = np.random.randint(0, N, 2)
        r = np.random.randint(2, 5)
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

def compute_anisotropy(V):
    V_c = V - np.mean(V)
    if np.std(V_c) < 0.01:
        return 0
    fft = np.fft.fft2(V_c)
    power = np.abs(fft)**2
    N = V.shape[0]
    c = N // 2
    h = np.sum(power[c-1:c+2, :])
    v = np.sum(power[:, c-1:c+2])
    return (h - v) / (h + v) if h + v > 0 else 0

def test_point(f, k, n_steps=40000):
    """Quick test for bistability at a point."""
    # From spots
    U, V = init_spots(N)
    for _ in range(n_steps):
        U, V = step(U, V, f, k)
    a_spot = compute_anisotropy(V)
    std_spot = np.std(V)

    # From stripes
    U, V = init_stripes(N)
    for _ in range(n_steps):
        U, V = step(U, V, f, k)
    a_stripe = compute_anisotropy(V)
    std_stripe = np.std(V)

    # Both uniform = no pattern
    if std_spot < 0.01 and std_stripe < 0.01:
        return 'uniform', 0

    # One uniform, one pattern = monostable
    if std_spot < 0.01:
        return 'stripe_only' if abs(a_stripe) > 0.5 else 'spot_only', abs(a_stripe)
    if std_stripe < 0.01:
        return 'spot_only', 0

    # Both have patterns - check if same or different
    if abs(a_spot - a_stripe) > 0.3:
        return 'BISTABLE', abs(a_spot - a_stripe)

    if abs(a_stripe) > 0.5:
        return 'stripes', abs(a_stripe)
    else:
        return 'spots_or_mixed', abs(a_stripe)

def main():
    print("=" * 60)
    print("MAPPING BISTABLE REGION")
    print("=" * 60)
    print()

    # Fine grid around the known bistable region
    f_range = np.arange(0.020, 0.052, 0.002)
    k_range = np.arange(0.050, 0.068, 0.001)

    results = {}
    bistable_points = []

    total = len(f_range) * len(k_range)
    count = 0

    print(f"Scanning {total} points...")
    print()

    for f in f_range:
        for k in k_range:
            count += 1
            pattern_type, metric = test_point(f, k)
            results[(f, k)] = (pattern_type, metric)

            if pattern_type == 'BISTABLE':
                bistable_points.append((f, k, metric))
                print(f"[{count}/{total}] f={f:.3f}, k={k:.3f}: BISTABLE (diff={metric:.3f})")
            elif count % 20 == 0:
                print(f"[{count}/{total}] f={f:.3f}, k={k:.3f}: {pattern_type}")

    print()
    print("=" * 60)
    print("BISTABLE REGION FOUND")
    print("=" * 60)
    print()

    if bistable_points:
        f_vals = [p[0] for p in bistable_points]
        k_vals = [p[1] for p in bistable_points]
        print(f"Number of bistable points: {len(bistable_points)}")
        print(f"f range: [{min(f_vals):.3f}, {max(f_vals):.3f}]")
        print(f"k range: [{min(k_vals):.3f}, {max(k_vals):.3f}]")
        print()

        # Print as a simple grid
        print("Bistable region map (B=bistable):")
        print()
        print("      ", end="")
        for k in k_range[::2]:
            print(f" {k:.3f}", end="")
        print()

        for f in f_range:
            print(f"f={f:.3f}", end=" ")
            for k in k_range[::2]:
                pt = results.get((f, k), ('?', 0))
                if pt[0] == 'BISTABLE':
                    print("   B  ", end="")
                elif pt[0] == 'uniform':
                    print("   .  ", end="")
                elif 'stripe' in pt[0]:
                    print("   S  ", end="")
                elif 'spot' in pt[0]:
                    print("   O  ", end="")
                else:
                    print("   ?  ", end="")
            print()

    # Save results
    save_results = {
        'bistable_points': [(float(f), float(k), float(m)) for f, k, m in bistable_points],
        'grid': {
            'f_range': [float(x) for x in f_range],
            'k_range': [float(x) for x in k_range],
        },
        'pattern_map': {f"{f:.3f},{k:.3f}": (t, float(m)) for (f, k), (t, m) in results.items()}
    }

    with open('bistable_region_map.json', 'w') as file:
        json.dump(save_results, file, indent=2)

    print()
    print("Results saved to bistable_region_map.json")

if __name__ == '__main__':
    main()
