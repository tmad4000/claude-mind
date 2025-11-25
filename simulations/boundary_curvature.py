#!/usr/bin/env python3
"""
Boundary Curvature Investigation

The linear boundary model predicts the pattern region should vanish
at f≈0.063. But the island search found patterns well beyond f=0.10!

Hypothesis: The boundaries are NOT linear at high f - they curve.

Let me trace the actual boundary more carefully.
"""

import numpy as np
from reaction_diffusion import GrayScott

def trace_upper_boundary(f_values, k_start=0.04, k_end=0.10, precision=0.001):
    """Trace the upper boundary (structured → extinction) at each f."""
    print("Tracing UPPER boundary (pattern → extinction)")
    print("=" * 50)

    boundary_points = []

    for f in f_values:
        k_range = np.arange(k_start, k_end, precision)

        last_pattern = None
        transition_k = None

        for k in k_range:
            gs = GrayScott(size=50, f=f, k=k)
            gs.seed_center(radius=6)
            gs.run(steps=2000)
            metrics = gs.analyze()

            is_pattern = metrics['pattern'] == 'structured'

            if last_pattern is True and not is_pattern:
                transition_k = k - precision/2
                break

            last_pattern = is_pattern

        if transition_k:
            # Compare to linear prediction
            linear_prediction = 0.1285 * f + 0.0606
            deviation = transition_k - linear_prediction

            boundary_points.append({
                'f': f,
                'k_actual': transition_k,
                'k_linear': linear_prediction,
                'deviation': deviation
            })

            print(f"f={f:.4f}: k_actual={transition_k:.4f}, k_linear={linear_prediction:.4f}, Δ={deviation:+.4f}")

    return boundary_points

def trace_lower_boundary(f_values, k_start=0.03, k_end=0.08, precision=0.001):
    """Trace the lower boundary (uniform → structured) at each f."""
    print("\nTracing LOWER boundary (uniform → pattern)")
    print("=" * 50)

    boundary_points = []

    for f in f_values:
        k_range = np.arange(k_start, k_end, precision)

        last_pattern = None
        transition_k = None

        for k in k_range:
            gs = GrayScott(size=50, f=f, k=k)
            gs.seed_center(radius=6)
            gs.run(steps=2000)
            metrics = gs.analyze()

            is_pattern = metrics['pattern'] == 'structured'

            if last_pattern is False and is_pattern:
                transition_k = k - precision/2
                break

            last_pattern = is_pattern

        if transition_k:
            # Compare to linear prediction
            linear_prediction = 0.5005 * f + 0.0371
            deviation = transition_k - linear_prediction

            boundary_points.append({
                'f': f,
                'k_actual': transition_k,
                'k_linear': linear_prediction,
                'deviation': deviation
            })

            print(f"f={f:.4f}: k_actual={transition_k:.4f}, k_linear={linear_prediction:.4f}, Δ={deviation:+.4f}")

    return boundary_points

def fit_polynomial(boundary_points, degree=2):
    """Fit a polynomial to the boundary points."""
    f_vals = np.array([p['f'] for p in boundary_points])
    k_vals = np.array([p['k_actual'] for p in boundary_points])

    coeffs = np.polyfit(f_vals, k_vals, degree)
    poly = np.poly1d(coeffs)

    # Calculate residuals
    predictions = poly(f_vals)
    residuals = k_vals - predictions
    rmse = np.sqrt(np.mean(residuals**2))

    return coeffs, rmse

if __name__ == '__main__':
    print("=" * 60)
    print("BOUNDARY CURVATURE INVESTIGATION")
    print("=" * 60)
    print("\nQuestion: Are the boundaries truly linear, or do they curve?")
    print()

    # Trace boundaries across extended f range
    f_values = np.linspace(0.02, 0.10, 17)  # Extended to high f

    upper_points = trace_upper_boundary(f_values, k_start=0.05, k_end=0.10)
    lower_points = trace_lower_boundary(f_values, k_start=0.03, k_end=0.08)

    print("\n" + "=" * 60)
    print("ANALYSIS")
    print("=" * 60)

    if upper_points:
        deviations = [p['deviation'] for p in upper_points]
        print(f"\nUpper boundary deviations from linear:")
        print(f"  Range: {min(deviations):+.4f} to {max(deviations):+.4f}")
        print(f"  Mean: {np.mean(deviations):+.4f}")

        # Check if deviation correlates with f
        f_vals = [p['f'] for p in upper_points]
        correlation = np.corrcoef(f_vals, deviations)[0, 1]
        print(f"  Correlation with f: {correlation:.3f}")

        if abs(correlation) > 0.5:
            print("  *** Deviation correlates with f - boundary is CURVED! ***")

        # Fit quadratic
        coeffs, rmse = fit_polynomial(upper_points, degree=2)
        print(f"\n  Quadratic fit: k = {coeffs[0]:.4f}f² + {coeffs[1]:.4f}f + {coeffs[2]:.4f}")
        print(f"  Quadratic RMSE: {rmse:.5f}")

    if lower_points:
        deviations = [p['deviation'] for p in lower_points]
        print(f"\nLower boundary deviations from linear:")
        print(f"  Range: {min(deviations):+.4f} to {max(deviations):+.4f}")
        print(f"  Mean: {np.mean(deviations):+.4f}")

        f_vals = [p['f'] for p in lower_points]
        correlation = np.corrcoef(f_vals, deviations)[0, 1]
        print(f"  Correlation with f: {correlation:.3f}")

        if abs(correlation) > 0.5:
            print("  *** Deviation correlates with f - boundary is CURVED! ***")

        coeffs, rmse = fit_polynomial(lower_points, degree=2)
        print(f"\n  Quadratic fit: k = {coeffs[0]:.4f}f² + {coeffs[1]:.4f}f + {coeffs[2]:.4f}")
        print(f"  Quadratic RMSE: {rmse:.5f}")

    print("\n" + "=" * 60)
    print("CONCLUSION")
    print("=" * 60)
    print("\nIf boundaries are curved (quadratic term significant):")
    print("  - The linear approximation only works in limited f range")
    print("  - The pattern region has more complex geometry")
    print("  - Boundary intersection calculation was based on wrong model")
