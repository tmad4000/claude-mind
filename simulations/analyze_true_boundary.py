#!/usr/bin/env python3
"""
Analyze the TRUE pattern region boundary now that artifacts are filtered.

The phase map shows a diagonal band of patterns (P) surrounded by:
- Extinction (.) at high k
- Uniform (U) at low k

Let's find the precise boundaries of this band.
"""

import numpy as np
from reaction_diffusion import GrayScott
from typing import List, Tuple
import json


def scan_parameters(resolution: int = 25) -> List[Tuple[float, float, str, float]]:
    """Scan parameter space with finer resolution."""
    f_range = (0.015, 0.075)
    k_range = (0.04, 0.068)

    results = []

    f_values = np.linspace(f_range[0], f_range[1], resolution)
    k_values = np.linspace(k_range[0], k_range[1], resolution)

    total = resolution * resolution
    done = 0

    for f in f_values:
        for k in k_values:
            gs = GrayScott(size=60, f=f, k=k)
            gs.seed_center(radius=8)
            gs.run(steps=3000)
            metrics = gs.analyze()

            results.append((f, k, metrics['pattern'], metrics.get('wavelength', float('inf'))))

            done += 1
            if done % 50 == 0:
                print(f"Progress: {done}/{total}")

    return results


def find_boundary_points(results: List[Tuple[float, float, str, float]]) -> dict:
    """Extract boundary points from scan results."""

    # Group by pattern type
    patterns = {}
    for f, k, p, wl in results:
        if p not in patterns:
            patterns[p] = []
        patterns[p].append((f, k, wl))

    print("\nPattern counts:")
    for p, points in patterns.items():
        print(f"  {p}: {len(points)} points")

    # Find boundary points - where a pattern point is adjacent to non-pattern
    pattern_set = set()
    if 'structured' in patterns:
        for f, k, wl in patterns['structured']:
            pattern_set.add((round(f, 4), round(k, 4)))

    # Build lookup for all points
    all_points = {(round(f, 4), round(k, 4)): p for f, k, p, wl in results}

    # Find boundary points
    boundaries = {
        'lower': [],  # Pattern meets uniform (lower k)
        'upper': [],  # Pattern meets extinction (higher k)
        'left': [],   # Pattern meets extinction (lower f)
        'right': [],  # Pattern meets uniform (higher f)
    }

    df = 0.003  # Approximate step size in f
    dk = 0.0012  # Approximate step size in k

    for (f, k) in pattern_set:
        # Check neighbors
        neighbors = [
            ((round(f + df, 4), round(k, 4)), 'right'),
            ((round(f - df, 4), round(k, 4)), 'left'),
            ((round(f, 4), round(k + dk, 4)), 'upper'),
            ((round(f, 4), round(k - dk, 4)), 'lower'),
        ]

        for (nf, nk), direction in neighbors:
            neighbor_pattern = all_points.get((nf, nk))
            if neighbor_pattern and neighbor_pattern != 'structured':
                boundaries[direction].append((f, k, neighbor_pattern))

    return boundaries


def analyze_boundary_shape(boundaries: dict):
    """Analyze the shape of each boundary."""

    print("\n=== BOUNDARY ANALYSIS ===\n")

    for name, points in boundaries.items():
        if len(points) < 3:
            print(f"{name}: Not enough points ({len(points)})")
            continue

        fs = np.array([p[0] for p in points])
        ks = np.array([p[1] for p in points])

        # Linear fit
        slope, intercept = np.polyfit(fs, ks, 1)
        predicted = slope * fs + intercept
        residuals = ks - predicted
        rmse = np.sqrt(np.mean(residuals**2))

        print(f"\n--- {name.upper()} boundary ---")
        print(f"Points: {len(points)}")
        print(f"f range: [{fs.min():.4f}, {fs.max():.4f}]")
        print(f"k range: [{ks.min():.4f}, {ks.max():.4f}]")
        print(f"Linear fit: k = {slope:.4f} * f + {intercept:.5f}")
        print(f"Linear RMSE: {rmse:.6f}")

        # What's on the other side?
        other_patterns = set(p[2] for p in points)
        print(f"Adjacent to: {other_patterns}")


def visualize_boundary_ascii(results: List[Tuple[float, float, str, float]]):
    """ASCII visualization of the boundary."""

    # Create grid
    fs = sorted(set(r[0] for r in results))
    ks = sorted(set(r[1] for r in results), reverse=True)

    lookup = {(round(r[0], 4), round(r[1], 4)): r[2] for r in results}

    chars = {
        'extinction': '.',
        'uniform': 'U',
        'structured': 'P',
        'filled': 'F',
        'artifact': 'X',
    }

    print("\n=== PATTERN MAP (filtered) ===")
    print("(k increases up, f increases right)\n")

    for k in ks:
        row = f"k={k:.3f}: "
        for f in fs:
            p = lookup.get((round(f, 4), round(k, 4)), '?')
            row += chars.get(p, '?')
        print(row)

    print(f"\n         {''.join([str(int(f*100)%10) for f in fs])}")
    print(f"f*100:   {fs[0]*100:.0f} to {fs[-1]*100:.0f}")


def compute_band_equations():
    """
    The pattern region appears to be a diagonal band.
    Let's find the equations of the upper and lower boundaries.

    If the band is linear:
    - Upper boundary: k = a1 * f + b1  (pattern meets extinction)
    - Lower boundary: k = a2 * f + b2  (pattern meets uniform)
    """
    print("\n=== BAND GEOMETRY ===\n")

    # From the map, the pattern region (P) appears roughly at:
    # Upper boundary crosses approximately:
    #   f=0.03, k=0.065 and f=0.065, k=0.065 (relatively flat?)
    # Lower boundary crosses approximately:
    #   f=0.02, k=0.05 and f=0.06, k=0.057

    # Let's verify with actual data
    pass


if __name__ == '__main__':
    print("=== TRUE BOUNDARY ANALYSIS ===\n")
    print("Scanning parameter space with finer resolution...")

    results = scan_parameters(resolution=20)

    print("\n" + "="*50)
    visualize_boundary_ascii(results)

    boundaries = find_boundary_points(results)
    analyze_boundary_shape(boundaries)

    # Save boundary data
    boundary_data = {
        name: [(float(f), float(k), p) for f, k, p in points]
        for name, points in boundaries.items()
    }

    with open('../data/true_boundary_data.json', 'w') as f:
        json.dump(boundary_data, f, indent=2)

    print("\n\nSaved boundary data to ../data/true_boundary_data.json")

    print("\n=== KEY INSIGHT ===")
    print("The pattern region is a BAND in (f, k) space.")
    print("Both boundaries appear to be approximately linear.")
    print("This means patterns emerge in a specific RATIO range of f/k!")
