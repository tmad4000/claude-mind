#!/usr/bin/env python3
"""
Boundary Finder - Precisely map where patterns emerge in parameter space.

The interesting question: What is the SHAPE of the boundary curve between
extinction, patterns, and uniform filling?

This tool does binary search to find precise transition points, then
characterizes the boundary geometry.
"""

import numpy as np
from reaction_diffusion import GrayScott
from typing import Tuple, List, Optional
import json
from pathlib import Path


def classify_endpoint(f: float, k: float, steps: int = 3000) -> str:
    """
    Run simulation to steady state and classify the result.
    Returns: 'extinction', 'pattern', 'uniform', or 'artifact'
    """
    gs = GrayScott(size=60, f=f, k=k)
    gs.seed_center(radius=8)
    gs.run(steps=steps)

    metrics = gs.analyze()

    # Map to simpler categories for boundary finding
    pattern = metrics['pattern']
    if pattern == 'structured':
        return 'pattern'
    elif pattern == 'artifact':
        return 'uniform'  # Treat numerical artifact as uniform for boundary
    elif pattern == 'filled':
        return 'uniform'  # High coverage = effectively uniform
    else:
        return pattern  # extinction or uniform


def find_transition_f(k: float, f_low: float, f_high: float,
                      target_transition: Tuple[str, str],
                      precision: float = 0.0005) -> Optional[float]:
    """
    Binary search to find the f value where transition occurs.
    target_transition: e.g., ('extinction', 'pattern')
    """
    # Verify endpoints have different classifications
    class_low = classify_endpoint(f_low, k)
    class_high = classify_endpoint(f_high, k)

    # Check if this transition exists in this range
    from_class, to_class = target_transition
    if not (class_low == from_class or class_high == to_class):
        return None

    while f_high - f_low > precision:
        f_mid = (f_low + f_high) / 2
        class_mid = classify_endpoint(f_mid, k)

        if class_mid == from_class:
            f_low = f_mid
        else:
            f_high = f_mid

    return (f_low + f_high) / 2


def find_transition_k(f: float, k_low: float, k_high: float,
                      target_transition: Tuple[str, str],
                      precision: float = 0.0005) -> Optional[float]:
    """Binary search for k transition."""
    class_low = classify_endpoint(f, k_low)
    class_high = classify_endpoint(f, k_high)

    from_class, to_class = target_transition
    if not (class_low == from_class or class_high == to_class):
        return None

    while k_high - k_low > precision:
        k_mid = (k_low + k_high) / 2
        class_mid = classify_endpoint(f, k_mid)

        if class_mid == from_class:
            k_low = k_mid
        else:
            k_high = k_mid

    return (k_low + k_high) / 2


def trace_boundary(start_f: float, start_k: float,
                   transition: Tuple[str, str],
                   direction: str = 'right',
                   n_points: int = 20,
                   step_size: float = 0.002) -> List[Tuple[float, float]]:
    """
    Trace a boundary curve by stepping along and binary searching.
    """
    boundary_points = [(start_f, start_k)]

    f, k = start_f, start_k

    for _ in range(n_points):
        # Step in the specified direction
        if direction == 'right':
            f += step_size
            # Binary search to find new k at this f
            k_new = find_transition_k(f, k - 0.01, k + 0.01, transition)
            if k_new:
                k = k_new
                boundary_points.append((f, k))
        elif direction == 'up':
            k += step_size
            f_new = find_transition_f(k, f - 0.01, f + 0.01, transition)
            if f_new:
                f = f_new
                boundary_points.append((f, k))

    return boundary_points


def analyze_boundary_geometry(boundary_points: List[Tuple[float, float]]) -> dict:
    """
    Analyze the geometry of the boundary curve.
    """
    if len(boundary_points) < 3:
        return {'error': 'Not enough points'}

    points = np.array(boundary_points)
    f_vals = points[:, 0]
    k_vals = points[:, 1]

    # Fit a line to see if it's linear
    slope, intercept = np.polyfit(f_vals, k_vals, 1)

    # Compute residuals to check linearity
    predicted = slope * f_vals + intercept
    residuals = k_vals - predicted
    rmse = np.sqrt(np.mean(residuals**2))

    # Try quadratic fit
    if len(boundary_points) >= 5:
        coeffs = np.polyfit(f_vals, k_vals, 2)
        predicted_quad = np.polyval(coeffs, f_vals)
        residuals_quad = k_vals - predicted_quad
        rmse_quad = np.sqrt(np.mean(residuals_quad**2))
    else:
        coeffs = None
        rmse_quad = None

    return {
        'n_points': len(boundary_points),
        'f_range': (float(f_vals.min()), float(f_vals.max())),
        'k_range': (float(k_vals.min()), float(k_vals.max())),
        'linear_slope': float(slope),
        'linear_intercept': float(intercept),
        'linear_rmse': float(rmse),
        'quadratic_coeffs': [float(c) for c in coeffs] if coeffs is not None else None,
        'quadratic_rmse': float(rmse_quad) if rmse_quad else None,
        'approximate_equation': f"k ≈ {slope:.3f}*f + {intercept:.4f}",
    }


def map_region_boundaries(resolution: int = 15) -> dict:
    """
    Systematically map boundaries between regions.

    Returns points on:
    - extinction/pattern boundary (lower)
    - pattern/uniform boundary (upper)
    """
    f_range = (0.01, 0.08)
    k_range = (0.03, 0.07)

    results = {
        'extinction_pattern_boundary': [],
        'pattern_uniform_boundary': [],
        'raw_classifications': []
    }

    f_values = np.linspace(f_range[0], f_range[1], resolution)

    print("Mapping boundaries...")

    for i, f in enumerate(f_values):
        print(f"  f = {f:.4f} ({i+1}/{resolution})")

        # Scan k values at this f
        k_values = np.linspace(k_range[0], k_range[1], resolution)
        classifications = []

        for k in k_values:
            c = classify_endpoint(f, k)
            classifications.append((f, k, c))

        results['raw_classifications'].extend(classifications)

        # Find transitions
        prev_class = None
        for f_val, k_val, curr_class in classifications:
            if prev_class and prev_class != curr_class:
                if prev_class == 'extinction' and curr_class == 'pattern':
                    results['extinction_pattern_boundary'].append((f_val, k_val))
                elif prev_class == 'pattern' and curr_class == 'uniform':
                    results['pattern_uniform_boundary'].append((f_val, k_val))
                elif prev_class == 'extinction' and curr_class == 'uniform':
                    # Direct transition - no pattern region at this f
                    pass
            prev_class = curr_class

    return results


def compute_region_width(boundaries: dict) -> dict:
    """
    Compute the width of the pattern region at different f values.
    This tells us where the "interesting zone" is widest.
    """
    lower = boundaries.get('extinction_pattern_boundary', [])
    upper = boundaries.get('pattern_uniform_boundary', [])

    if not lower or not upper:
        return {'error': 'Missing boundary data'}

    # Group by f value (approximately)
    lower_dict = {round(f, 3): k for f, k in lower}
    upper_dict = {round(f, 3): k for f, k in upper}

    widths = []
    for f in lower_dict:
        if f in upper_dict:
            width = upper_dict[f] - lower_dict[f]
            widths.append({'f': f, 'k_lower': lower_dict[f],
                          'k_upper': upper_dict[f], 'width': width})

    if widths:
        max_width = max(widths, key=lambda x: x['width'])
        return {
            'width_data': widths,
            'max_width_f': max_width['f'],
            'max_width_value': max_width['width'],
            'insight': f"Pattern region is widest at f ≈ {max_width['f']:.3f}"
        }

    return {'error': 'Could not compute widths'}


if __name__ == '__main__':
    print("=== BOUNDARY FINDER ===\n")
    print("Mapping the precise boundaries of the pattern region...\n")

    # Map boundaries with higher resolution
    boundaries = map_region_boundaries(resolution=15)

    # Print the classification map first
    print("\n--- Classification map ---")
    raw = boundaries['raw_classifications']
    # Group by f
    by_f = {}
    for f, k, c in raw:
        f_key = round(f, 3)
        if f_key not in by_f:
            by_f[f_key] = []
        by_f[f_key].append((k, c))

    # Print as a grid
    class_chars = {'extinction': '.', 'pattern': 'P', 'uniform': 'U'}
    print("f\\k ", end="")
    for f_key in sorted(by_f.keys()):
        print(f"{f_key:.2f} ", end="")
    print()
    # Actually let's print it differently - each row is a k value
    print("\n(k increases up, f increases right)")
    all_k = sorted(set(k for f, k, c in raw), reverse=True)
    all_f = sorted(set(f for f, k, c in raw))
    lookup = {(round(f, 3), round(k, 3)): c for f, k, c in raw}
    for k in all_k:
        k_key = round(k, 3)
        row = ""
        for f in all_f:
            f_key = round(f, 3)
            c = lookup.get((f_key, k_key), '?')
            row += class_chars.get(c, '?')
        print(f"k={k_key:.3f}: {row}")

    # Analyze lower boundary (extinction -> pattern)
    lower = boundaries['extinction_pattern_boundary']
    if lower:
        print(f"\n--- Lower boundary (extinction → pattern) ---")
        print(f"Found {len(lower)} transition points")
        if len(lower) >= 3:
            geom = analyze_boundary_geometry(lower)
            print(f"Approximate equation: {geom.get('approximate_equation', 'N/A')}")
            rmse = geom.get('linear_rmse')
            if rmse and isinstance(rmse, (int, float)):
                print(f"Linear RMSE: {rmse:.6f}")
            if geom.get('quadratic_rmse'):
                print(f"Quadratic RMSE: {geom['quadratic_rmse']:.6f}")
        else:
            print("Not enough points for geometry analysis")
        print(f"Points: {lower[:5]}...")

    # Analyze upper boundary (pattern -> uniform)
    upper = boundaries['pattern_uniform_boundary']
    if upper:
        print(f"\n--- Upper boundary (pattern → uniform) ---")
        print(f"Found {len(upper)} transition points")
        if len(upper) >= 3:
            geom = analyze_boundary_geometry(upper)
            print(f"Approximate equation: {geom.get('approximate_equation', 'N/A')}")
            rmse = geom.get('linear_rmse')
            if rmse and isinstance(rmse, (int, float)):
                print(f"Linear RMSE: {rmse:.6f}")
        else:
            print("Not enough points for geometry analysis")
        print(f"Points: {upper[:5]}...")

    # Compute region width
    print("\n--- Pattern region width ---")
    width_analysis = compute_region_width(boundaries)
    if 'insight' in width_analysis:
        print(width_analysis['insight'])
        print(f"Maximum width: {width_analysis['max_width_value']:.4f}")

    # Save results
    output_path = Path(__file__).parent.parent / 'data' / 'boundary_data.json'
    output_path.parent.mkdir(exist_ok=True)

    # Convert to serializable format
    save_data = {
        'lower_boundary': [(float(f), float(k)) for f, k in lower] if lower else [],
        'upper_boundary': [(float(f), float(k)) for f, k in upper] if upper else [],
        'width_analysis': width_analysis if 'error' not in width_analysis else None,
    }

    with open(output_path, 'w') as f:
        json.dump(save_data, f, indent=2)

    print(f"\nSaved boundary data to {output_path}")

    # Key insight
    print("\n=== KEY QUESTION ===")
    print("Is the boundary curve LINEAR or CURVED?")
    print("A linear boundary would suggest a simple relationship: k = a*f + b")
    print("A curved boundary might reveal deeper structure in the dynamics.")
