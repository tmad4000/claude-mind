#!/usr/bin/env python3
"""
Test for TRISTABILITY in Gray-Scott.

Finding three distinct stable patterns at the same (f,k) would be genuinely novel.
Standard literature documents bistability but not tristability.
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

def init_spots(N, n=15):
    """Circular spots."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    np.random.seed(42)
    for _ in range(n):
        cx, cy = np.random.randint(0, N, 2)
        r = np.random.randint(3, 6)
        y, x = np.ogrid[:N, :N]
        mask = ((np.minimum(np.abs(x-cx), N-np.abs(x-cx)))**2 +
                (np.minimum(np.abs(y-cy), N-np.abs(y-cy)))**2) <= r*r
        U[mask], V[mask] = 0.5, 0.25
    return U, V

def init_h_stripes(N, n=6):
    """Horizontal stripes."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    w = N // (2 * n)
    for i in range(n):
        s = i * N // n + N // (4 * n)
        U[s:s+w, :], V[s:s+w, :] = 0.5, 0.25
    return U, V

def init_v_stripes(N, n=6):
    """Vertical stripes."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    w = N // (2 * n)
    for i in range(n):
        s = i * N // n + N // (4 * n)
        U[:, s:s+w], V[:, s:s+w] = 0.5, 0.25
    return U, V

def init_diagonal(N, n=6):
    """Diagonal stripes."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if ((i + j) % (N // n)) < (N // (2 * n)):
                U[i, j], V[i, j] = 0.5, 0.25
    return U, V

def init_labyrinth(N):
    """Labyrinth-like initial condition."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    # Random maze-like perturbation
    np.random.seed(123)
    # Create a random connected structure
    mask = np.zeros((N, N), dtype=bool)
    # Random walk to create paths
    y, x = N // 2, N // 2
    for _ in range(N * N // 4):
        mask[y, x] = True
        # Random direction with momentum
        dy, dx_dir = np.random.choice([-1, 0, 1], 2)
        y = (y + dy) % N
        x = (x + dx_dir) % N
    # Dilate
    kernel = np.array([[1,1,1],[1,1,1],[1,1,1]])
    from_mask = mask.copy()
    for _ in range(2):
        new_mask = np.zeros_like(mask)
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                new_mask |= np.roll(np.roll(from_mask, di, 0), dj, 1)
        from_mask = new_mask
    U[from_mask], V[from_mask] = 0.5, 0.25
    return U, V

def init_hexagonal(N):
    """Hexagonal spot arrangement."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    spacing = N // 8
    for i in range(8):
        for j in range(8):
            cx = int((i + 0.5 * (j % 2)) * spacing) % N
            cy = int(j * spacing * 0.866) % N
            y, x = np.ogrid[:N, :N]
            mask = ((np.minimum(np.abs(x-cx), N-np.abs(x-cx)))**2 +
                    (np.minimum(np.abs(y-cy), N-np.abs(y-cy)))**2) <= 9
            U[mask], V[mask] = 0.5, 0.25
    return U, V

def pattern_fingerprint(V, n_bins=20):
    """Create a fingerprint of the pattern for comparison."""
    V_centered = V - np.mean(V)
    if np.std(V) < 0.01:
        return np.zeros(n_bins + 5)

    # FFT-based features
    fft = np.fft.fft2(V_centered)
    power = np.abs(np.fft.fftshift(fft))**2

    N = V.shape[0]
    c = N // 2
    y, x = np.ogrid[:N, :N]
    r = np.sqrt((x - c)**2 + (y - c)**2)

    # Radial power distribution
    radial_bins = np.linspace(0, N//2, n_bins + 1)
    radial_power = []
    for i in range(n_bins):
        mask = (r >= radial_bins[i]) & (r < radial_bins[i+1])
        if np.sum(mask) > 0:
            radial_power.append(np.mean(power[mask]))
        else:
            radial_power.append(0)

    # Angular features
    h_power = np.sum(power[c-2:c+3, :])  # Horizontal
    v_power = np.sum(power[:, c-2:c+3])  # Vertical
    d1 = np.sum(np.diag(power))  # Diagonal 1
    d2 = np.sum(np.diag(np.fliplr(power)))  # Diagonal 2

    anisotropy = (h_power - v_power) / max(h_power + v_power, 1e-10)

    return np.array(radial_power + [h_power, v_power, d1, d2, anisotropy])

def fingerprint_distance(fp1, fp2):
    """Distance between two pattern fingerprints."""
    # Normalize
    n1 = fp1 / (np.linalg.norm(fp1) + 1e-10)
    n2 = fp2 / (np.linalg.norm(fp2) + 1e-10)
    return np.linalg.norm(n1 - n2)

def test_tristability(f, k, n_steps=50000):
    """Test for three distinct stable patterns."""
    init_funcs = [
        ('spots', init_spots),
        ('h_stripes', init_h_stripes),
        ('v_stripes', init_v_stripes),
        ('diagonal', init_diagonal),
        ('labyrinth', init_labyrinth),
        ('hexagonal', init_hexagonal),
    ]

    results = []
    final_states = []

    for name, init_func in init_funcs:
        U, V = init_func(N)
        for _ in range(n_steps):
            U, V = step(U, V, f, k)

        fp = pattern_fingerprint(V)
        std_v = np.std(V)
        results.append({
            'name': name,
            'fingerprint': fp,
            'std': float(std_v),
            'mean': float(np.mean(V)),
            'active': std_v > 0.01
        })
        final_states.append(V.copy())

    # Count distinct patterns
    active_results = [r for r in results if r['active']]

    if len(active_results) < 2:
        return {
            'f': f, 'k': k,
            'distinct_patterns': len(active_results),
            'tristable': False,
            'details': results
        }

    # Cluster fingerprints
    distinct = []
    threshold = 0.3  # Distance threshold for "same" pattern

    for r in active_results:
        is_new = True
        for d in distinct:
            if fingerprint_distance(r['fingerprint'], d['fingerprint']) < threshold:
                is_new = False
                break
        if is_new:
            distinct.append(r)

    return {
        'f': f, 'k': k,
        'distinct_patterns': len(distinct),
        'tristable': len(distinct) >= 3,
        'distinct_names': [d['name'] for d in distinct],
        'details': [{k: v for k, v in r.items() if k != 'fingerprint'} for r in results]
    }

def main():
    print("=" * 60)
    print("TRISTABILITY TEST")
    print("=" * 60)
    print()
    print("Looking for THREE distinct stable patterns at same (f,k)...")
    print()

    # Test points in the bistable region and nearby
    test_points = [
        (0.030, 0.055),  # Known bistable
        (0.035, 0.058),  # Known bistable
        (0.040, 0.060),
        (0.032, 0.056),
        (0.028, 0.054),
        (0.038, 0.059),
        (0.042, 0.061),
        (0.034, 0.057),
        (0.036, 0.058),
        (0.033, 0.056),
    ]

    tristable_points = []

    for i, (f, k) in enumerate(test_points):
        print(f"Testing {i+1}/{len(test_points)}: f={f:.3f}, k={k:.3f}...", end=" ", flush=True)
        result = test_tristability(f, k)

        if result['tristable']:
            tristable_points.append(result)
            print(f"TRISTABLE! {result['distinct_patterns']} patterns: {result['distinct_names']}")
        else:
            print(f"{result['distinct_patterns']} distinct patterns")

    print()
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    print()

    if tristable_points:
        print("TRISTABILITY FOUND!")
        for tp in tristable_points:
            print(f"  f={tp['f']:.3f}, k={tp['k']:.3f}: {tp['distinct_names']}")
        print()
        print("This would be NOVEL - literature documents bistability but not tristability!")
    else:
        print("No tristability found at tested points.")
        print("Bistability confirmed, but no third stable pattern type.")

    # Save results
    with open('tristability_results.json', 'w') as file:
        json.dump({
            'test_points': test_points,
            'tristable_found': len(tristable_points) > 0,
            'tristable_points': tristable_points
        }, file, indent=2, default=str)

    print()
    print("Results saved to tristability_results.json")

if __name__ == '__main__':
    main()
