#!/usr/bin/env python3
"""
Investigation: Why are there TWO pattern regions?

The boundary finder revealed:
- Upper lobe: patterns at k ≈ 0.059-0.064, middle f values
- Lower lobe: patterns at k ≈ 0.030-0.033, higher f values

Are these producing different pattern types?
Is there a connection between them?
"""

import numpy as np
from reaction_diffusion import GrayScott, visualize_ascii
from typing import Tuple


def compare_pattern_types(params_list: list, names: list, steps: int = 4000):
    """Compare patterns produced at different parameter combinations."""

    print("=== COMPARING PATTERN TYPES ===\n")

    results = []

    for (f, k), name in zip(params_list, names):
        print(f"--- {name}: f={f}, k={k} ---")

        gs = GrayScott(size=60, f=f, k=k)
        gs.seed_center(radius=8)
        gs.run(steps=steps)

        metrics = gs.analyze()
        print(f"Mean V: {metrics['mean_v']:.3f}")
        print(f"Std V:  {metrics['std_v']:.3f}")
        print(f"Coverage: {metrics['coverage']:.1%}")
        print(f"Pattern type: {metrics['pattern']}")

        # Additional analysis
        v = gs.V

        # Spatial frequency analysis (rough)
        # Count zero-crossings in a row as proxy for spatial frequency
        mid_row = v[gs.size // 2, :]
        threshold = (mid_row.max() + mid_row.min()) / 2
        binary = mid_row > threshold
        crossings = np.sum(np.abs(np.diff(binary.astype(int))))
        wavelength_estimate = gs.size / max(crossings, 1)

        print(f"Estimated wavelength: {wavelength_estimate:.1f} cells")

        # Check for symmetry
        v_flipped = np.flipud(v)
        symmetry = np.corrcoef(v.flatten(), v_flipped.flatten())[0, 1]
        print(f"Vertical symmetry: {symmetry:.2f}")

        print()
        print(visualize_ascii(gs, width=50))
        print("\n" + "="*60 + "\n")

        results.append({
            'name': name,
            'f': f, 'k': k,
            'metrics': metrics,
            'wavelength': wavelength_estimate,
            'symmetry': symmetry
        })

    return results


def scan_between_lobes(f: float = 0.05, k_range: Tuple[float, float] = (0.03, 0.065),
                       n_points: int = 15):
    """
    Scan vertically through parameter space to see the transition between lobes.
    """
    print(f"=== VERTICAL SCAN at f={f} ===\n")

    k_values = np.linspace(k_range[0], k_range[1], n_points)

    for k in k_values:
        gs = GrayScott(size=50, f=f, k=k)
        gs.seed_center(radius=6)
        gs.run(steps=2000)
        metrics = gs.analyze()

        # Compact summary
        char = {
            'extinction': '.',
            'uniform': 'U',
            'pattern': 'P',
            'filled': 'F'
        }.get(metrics['pattern'], '?')

        bar_len = int(metrics['std_v'] * 100)
        bar = '#' * bar_len

        print(f"k={k:.3f}: {char} std={metrics['std_v']:.3f} {bar}")

    print()


def find_transition_details():
    """
    Look more closely at the transition points.
    What happens right at the boundary?
    """
    print("=== BOUNDARY TRANSITIONS ===\n")

    # Upper boundary (pattern -> extinction) at high k
    print("Upper boundary (pattern meets extinction):")
    for k in [0.062, 0.063, 0.064, 0.065, 0.066, 0.067]:
        gs = GrayScott(size=50, f=0.04, k=k)
        gs.seed_center(radius=6)
        gs.run(steps=3000)
        m = gs.analyze()
        print(f"  k={k:.3f}: {m['pattern']:12s} mean={m['mean_v']:.4f} std={m['std_v']:.4f}")

    print("\nLower boundary (pattern meets uniform at low k):")
    for k in [0.035, 0.036, 0.037, 0.038, 0.039, 0.040]:
        gs = GrayScott(size=50, f=0.04, k=k)
        gs.seed_center(radius=6)
        gs.run(steps=3000)
        m = gs.analyze()
        print(f"  k={k:.3f}: {m['pattern']:12s} mean={m['mean_v']:.4f} std={m['std_v']:.4f}")


if __name__ == '__main__':
    # Compare specific points in each lobe
    params = [
        (0.04, 0.061),   # Upper lobe
        (0.055, 0.062),  # Upper lobe, higher f
        (0.05, 0.032),   # Lower lobe
        (0.06, 0.032),   # Lower lobe, higher f
    ]
    names = ['Upper lobe (left)', 'Upper lobe (right)', 'Lower lobe (left)', 'Lower lobe (right)']

    results = compare_pattern_types(params, names)

    # Vertical scan through middle
    scan_between_lobes(f=0.05)
    scan_between_lobes(f=0.04)

    # Boundary details
    find_transition_details()

    # Summary
    print("\n=== KEY OBSERVATIONS ===")
    print("1. Do the two lobes produce different pattern types?")
    print("2. Is there a 'corridor' connecting them?")
    print("3. What determines which lobe you're in?")

    wavelengths = [(r['name'], r['wavelength']) for r in results if r['wavelength']]
    if wavelengths:
        print("\nWavelengths:")
        for name, wl in wavelengths:
            print(f"  {name}: {wl:.1f}")

        wl_values = [w for _, w in wavelengths]
        if len(set([round(w) for w in wl_values])) > 1:
            print("\n** Different wavelengths in different lobes! **")
            print("This suggests qualitatively different pattern types.")
