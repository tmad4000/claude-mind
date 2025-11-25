#!/usr/bin/env python3
"""
Test TOPOLOGICAL PROPERTIES of Gray-Scott patterns.

Topology captures global structure independent of scale:
- Euler characteristic χ = #spots - #holes + #connected_components
- For spots: χ > 0 (many isolated spots)
- For stripes: χ ≈ 0 (balanced spots/holes)
- For inverse (holes in background): χ < 0

The topology could:
1. Distinguish pattern types
2. Show characteristic values at transitions
3. Reveal topological defects

Also examine:
- Number of connected components
- Percolation transition (when pattern spans domain)
- Genus/hole count

Finding universal topological invariants could be novel.
"""

import numpy as np
import json
from scipy import ndimage

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

def init_nucleated(N, seed=42):
    """Initialize with nucleation sites."""
    np.random.seed(seed)
    U, V = np.ones((N, N)), np.zeros((N, N))
    for _ in range(10):
        cx, cy = np.random.randint(N//4, 3*N//4, 2)
        r = 4
        y, x = np.ogrid[:N, :N]
        mask = (x-cx)**2 + (y-cy)**2 <= r*r
        U[mask], V[mask] = 0.5, 0.25
    return U, V

def calculate_euler_characteristic(binary):
    """
    Calculate Euler characteristic using the quad-vertex formula.
    χ = n1 - n2 + n3 - n4 where ni is the count of 2x2 patterns
    with i foreground pixels.
    """
    # Pad to handle edges
    padded = np.pad(binary, 1, mode='wrap')

    n1 = n2 = n3 = n4 = 0

    for i in range(padded.shape[0] - 1):
        for j in range(padded.shape[1] - 1):
            quad = padded[i:i+2, j:j+2]
            s = np.sum(quad)
            if s == 1:
                n1 += 1
            elif s == 2:
                # Check for diagonal
                if (quad[0,0] == quad[1,1]) or (quad[0,1] == quad[1,0]):
                    n2 += 1
                else:
                    n2 += 1  # Adjacent counts as 2
            elif s == 3:
                n3 += 1
            elif s == 4:
                n4 += 1

    # Simplified Euler for 2D: components - holes
    chi = (n1 - n2 + n3 - n4) // 4
    return chi

def count_components_and_holes(binary):
    """Count connected components and holes."""
    # Connected components in foreground
    labeled, n_components = ndimage.label(binary)

    # Holes = components in background (excluding infinite component)
    labeled_bg, n_bg = ndimage.label(1 - binary)
    # Subtract 1 for the "infinite" background
    n_holes = max(0, n_bg - 1)

    return n_components, n_holes

def check_percolation(binary):
    """Check if pattern percolates (spans domain in x or y)."""
    labeled, n_components = ndimage.label(binary)

    # Check x-percolation: does any component touch both left and right?
    x_percolates = False
    for comp_id in range(1, n_components + 1):
        mask = labeled == comp_id
        if np.any(mask[:, 0]) and np.any(mask[:, -1]):
            x_percolates = True
            break

    # Check y-percolation
    y_percolates = False
    for comp_id in range(1, n_components + 1):
        mask = labeled == comp_id
        if np.any(mask[0, :]) and np.any(mask[-1, :]):
            y_percolates = True
            break

    return x_percolates or y_percolates

def calculate_topology(V, threshold=None):
    """Calculate topological properties of pattern."""
    if threshold is None:
        threshold = np.mean(V) + 0.5 * np.std(V)

    binary = (V > threshold).astype(int)

    # Basic stats
    fill_fraction = np.mean(binary)

    if fill_fraction < 0.01 or fill_fraction > 0.99:
        return {
            'euler': 0,
            'n_components': 0,
            'n_holes': 0,
            'percolates': False,
            'fill_fraction': float(fill_fraction),
            'normalized_euler': 0.0
        }

    euler = calculate_euler_characteristic(binary)
    n_components, n_holes = count_components_and_holes(binary)
    percolates = check_percolation(binary)

    # Normalized Euler per unit area
    normalized_euler = euler / (N * N / 100)

    return {
        'euler': int(euler),
        'n_components': int(n_components),
        'n_holes': int(n_holes),
        'percolates': bool(percolates),
        'fill_fraction': float(fill_fraction),
        'normalized_euler': float(normalized_euler)
    }

def test_topology(f, k, n_steps=50000):
    """Test topology at a parameter point."""
    U, V = init_nucleated(N)

    for _ in range(n_steps):
        U, V = step(U, V, f, k)

    if np.std(V) < 0.02:
        return None, 'no_pattern'

    topology = calculate_topology(V)
    return topology, 'ok'

def main():
    print("=" * 70)
    print("TOPOLOGICAL ANALYSIS OF PATTERNS")
    print("=" * 70)
    print()
    print("Measuring Euler characteristic and connectivity across parameters...")
    print()

    # Test across parameter space
    test_points = []

    for f in [0.028, 0.032, 0.036, 0.040, 0.044, 0.048]:
        for k_offset in [-0.002, 0, 0.002, 0.004]:
            k = 0.054 + (f - 0.028) * 0.4 + k_offset
            test_points.append((f, k))

    results = []

    print(f"{'f':>6} {'k':>6} {'χ':>6} {'#comp':>6} {'#holes':>7} {'frac':>6} {'perc':>5} {'χ_norm':>8}")
    print("-" * 65)

    for f, k in test_points:
        topology, status = test_topology(f, k)

        if status == 'ok':
            chi = topology['euler']
            n_comp = topology['n_components']
            n_holes = topology['n_holes']
            fill = topology['fill_fraction']
            perc = 'Y' if topology['percolates'] else 'N'
            chi_norm = topology['normalized_euler']

            print(f"{f:6.3f} {k:6.3f} {chi:6d} {n_comp:6d} {n_holes:7d} {fill:6.3f} {perc:>5} {chi_norm:8.3f}")

            topology['f'] = float(f)
            topology['k'] = float(k)
            topology['status'] = status
            results.append(topology)
        else:
            print(f"{f:6.3f} {k:6.3f} {'N/A':>6} {'N/A':>6} {'N/A':>7} {'N/A':>6} {'N/A':>5} {'N/A':>8}")

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    valid = [r for r in results if 'euler' in r]

    if len(valid) < 3:
        print("Not enough valid topology data")
    else:
        eulers = [r['euler'] for r in valid]
        fill_fracs = [r['fill_fraction'] for r in valid]
        n_percolating = sum(1 for r in valid if r['percolates'])

        print(f"Euler characteristic range: {min(eulers)} to {max(eulers)}")
        print(f"Mean Euler: {np.mean(eulers):.1f}")
        print(f"Fill fraction range: {min(fill_fracs):.3f} to {max(fill_fracs):.3f}")
        print(f"Percolating patterns: {n_percolating}/{len(valid)}")
        print()

        # Check for correlation between Euler and parameters
        f_vals = [r['f'] for r in valid]
        if len(set(f_vals)) > 1:
            corr = np.corrcoef(f_vals, eulers)[0, 1]
            print(f"Correlation of χ with f: {corr:.3f}")

        k_vals = [r['k'] for r in valid]
        if len(set(k_vals)) > 1:
            corr = np.corrcoef(k_vals, eulers)[0, 1]
            print(f"Correlation of χ with k: {corr:.3f}")

        # Check for topological transition
        positive_chi = [r for r in valid if r['euler'] > 10]
        negative_chi = [r for r in valid if r['euler'] < -10]

        if positive_chi and negative_chi:
            print()
            print("INTERESTING: Topological transition detected!")
            print(f"Positive χ (spots): f={np.mean([r['f'] for r in positive_chi]):.3f}")
            print(f"Negative χ (holes): f={np.mean([r['f'] for r in negative_chi]):.3f}")

        # Look for percolation transition
        print()
        print("Percolation analysis:")
        perc_by_f = {}
        for r in valid:
            f_val = r['f']
            if f_val not in perc_by_f:
                perc_by_f[f_val] = []
            perc_by_f[f_val].append(r['percolates'])

        for f_val in sorted(perc_by_f.keys()):
            frac = np.mean(perc_by_f[f_val])
            print(f"  f={f_val:.3f}: {frac*100:.0f}% percolating")

    # Save results
    with open('topology_results.json', 'w') as file:
        json.dump({
            'results': results,
            'summary': {
                'mean_euler': float(np.mean(eulers)) if valid else None,
                'n_percolating': n_percolating if valid else 0
            }
        }, file, indent=2)

    print()
    print("Results saved to topology_results.json")

if __name__ == '__main__':
    main()
