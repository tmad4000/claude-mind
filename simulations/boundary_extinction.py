#!/usr/bin/env python3
"""
Boundary Extinction Investigation

Question: The upper and lower boundaries of the pattern region intersect
at approximately (f=0.063, k=0.069). What happens there?

Does the pattern region actually vanish?
Are there any "islands" of patterns outside the main region?
What's the fine structure of the boundary?
"""

import numpy as np
from reaction_diffusion import GrayScott
import json

# Calculated intersection point
# Upper: k = 0.1285f + 0.0606
# Lower: k = 0.5005f + 0.0371
# Intersection: f ≈ 0.063, k ≈ 0.069

def scan_extinction_region():
    """Scan the region around the predicted extinction point."""
    print("=== SCANNING EXTINCTION REGION ===\n")

    # Focus on f from 0.05 to 0.08, k from 0.06 to 0.09
    f_values = np.linspace(0.05, 0.08, 15)
    k_values = np.linspace(0.06, 0.09, 15)

    results = []
    pattern_map = []

    for f in f_values:
        row = []
        for k in k_values:
            # Calculate expected boundaries
            upper_k = 0.1285 * f + 0.0606
            lower_k = 0.5005 * f + 0.0371

            expected = 'pattern' if lower_k < k < upper_k else 'no_pattern'

            # Run simulation
            gs = GrayScott(size=60, f=f, k=k)
            gs.seed_center(radius=8)
            gs.run(steps=3000)
            metrics = gs.analyze()
            actual = metrics['pattern']

            results.append({
                'f': f,
                'k': k,
                'expected': expected,
                'actual': actual,
                'metrics': metrics
            })

            # Simple char: S=structured, E=extinction, U=uniform, ?=other
            char_map = {'structured': 'S', 'extinction': '.', 'uniform': 'U',
                       'filled': 'F', 'artifact': 'A'}
            row.append(char_map.get(actual, '?'))

        pattern_map.append(''.join(row))

    print("Pattern map (f increases down, k increases right):")
    print("k →")
    print(f"     {k_values[0]:.3f}" + " " * 10 + f"{k_values[-1]:.3f}")
    for i, row in enumerate(pattern_map):
        prefix = f"f={f_values[i]:.3f} " if i % 3 == 0 else "        "
        print(prefix + row)

    print("\nLegend: S=structured . =extinction U=uniform F=filled")

    return results

def find_islands():
    """Look for isolated pattern regions outside the main band."""
    print("\n=== SEARCHING FOR PATTERN ISLANDS ===\n")

    # Scan a wider region
    f_values = np.linspace(0.01, 0.10, 25)
    k_values = np.linspace(0.02, 0.10, 25)

    islands = []

    total = len(f_values) * len(k_values)
    done = 0

    pattern_grid = []

    for f in f_values:
        row = []
        for k in k_values:
            # Calculate expected boundaries
            upper_k = 0.1285 * f + 0.0606
            lower_k = 0.5005 * f + 0.0371

            in_band = lower_k < k < upper_k

            # Run simulation
            gs = GrayScott(size=50, f=f, k=k)
            gs.seed_center(radius=6)
            gs.run(steps=2000)
            metrics = gs.analyze()

            has_pattern = metrics['pattern'] == 'structured'

            # Island = pattern outside predicted band
            if has_pattern and not in_band:
                islands.append({
                    'f': f,
                    'k': k,
                    'upper_k': upper_k,
                    'lower_k': lower_k,
                    'metrics': metrics
                })

            char = 'S' if has_pattern else '.'
            row.append(char)

            done += 1
            if done % 100 == 0:
                print(f"Progress: {done}/{total}")

        pattern_grid.append(''.join(row))

    print("\nFull pattern map:")
    print("k →")
    for i, row in enumerate(pattern_grid):
        if i % 5 == 0:
            print(f"f={f_values[i]:.3f} " + row)
        else:
            print("        " + row)

    if islands:
        print(f"\n*** FOUND {len(islands)} ISLANDS! ***")
        for island in islands:
            print(f"  f={island['f']:.4f}, k={island['k']:.4f}")
            print(f"    Expected band: k ∈ [{island['lower_k']:.4f}, {island['upper_k']:.4f}]")
    else:
        print("\nNo islands found - pattern region is contiguous")

    return islands, pattern_grid

def fine_structure_scan():
    """High-resolution scan of boundary fine structure."""
    print("\n=== FINE STRUCTURE SCAN ===\n")

    # Focus on one section of the boundary
    f = 0.04  # Fix f, vary k across boundary
    k_values = np.linspace(0.055, 0.075, 40)

    print(f"Scanning k at fixed f={f}")
    print("Looking for non-monotonic behavior or multiple transitions\n")

    results = []
    pattern_sequence = []

    for k in k_values:
        gs = GrayScott(size=60, f=f, k=k)
        gs.seed_center(radius=8)
        gs.run(steps=3000)
        metrics = gs.analyze()

        results.append({
            'k': k,
            'pattern': metrics['pattern'],
            'std_v': metrics['std_v'],
            'mean_v': metrics['mean_v']
        })

        char = 'S' if metrics['pattern'] == 'structured' else '.'
        pattern_sequence.append(char)

    print("Pattern sequence (k increases →):")
    print(''.join(pattern_sequence))

    # Count transitions
    transitions = 0
    for i in range(len(pattern_sequence) - 1):
        if pattern_sequence[i] != pattern_sequence[i+1]:
            transitions += 1
            print(f"  Transition at k≈{k_values[i]:.4f}: {pattern_sequence[i]} → {pattern_sequence[i+1]}")

    if transitions > 2:
        print(f"\n*** INTERESTING: {transitions} transitions found! ***")
        print("The boundary may have complex structure")
    else:
        print(f"\nSimple boundary structure ({transitions} transitions)")

    return results

if __name__ == '__main__':
    print("=" * 60)
    print("BOUNDARY EXTINCTION INVESTIGATION")
    print("=" * 60)

    # Run investigations
    extinction_results = scan_extinction_region()

    islands, grid = find_islands()

    fine_results = fine_structure_scan()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(f"\nIslands found: {len(islands)}")
    print("If islands exist, this suggests the pattern region has disconnected components")
    print("If no islands, the simple linear boundary model is approximately correct")
