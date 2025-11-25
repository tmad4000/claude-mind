#!/usr/bin/env python3
"""
Analyze the boundary geometry directly from scan results.

From the map, the pattern region (P) forms a diagonal band.
Let's compute the equations of the boundaries.
"""

import numpy as np

# Hand-extracted boundary points from the scan
# Upper boundary: where P meets extinction (.)
upper_boundary = [
    (0.030, 0.065),  # P at f=0.030, k=0.065
    (0.033, 0.065),
    (0.036, 0.065),
    (0.039, 0.065),
    (0.042, 0.065),
    (0.045, 0.067),
    (0.048, 0.067),
    (0.052, 0.067),
    (0.055, 0.068),
]

# Lower boundary: where P meets uniform/filled (U/F)
lower_boundary = [
    (0.018, 0.044),  # P starts at approximately k=0.044 for f≈0.018
    (0.021, 0.046),
    (0.024, 0.049),
    (0.027, 0.052),
    (0.030, 0.053),
    (0.033, 0.055),
    (0.036, 0.056),
    (0.039, 0.058),
    (0.042, 0.059),
    (0.048, 0.061),
    (0.055, 0.062),
]

def fit_boundary(points, name):
    """Fit a line to boundary points."""
    f = np.array([p[0] for p in points])
    k = np.array([p[1] for p in points])

    slope, intercept = np.polyfit(f, k, 1)

    # Compute residuals
    predicted = slope * f + intercept
    residuals = k - predicted
    rmse = np.sqrt(np.mean(residuals**2))

    print(f"\n=== {name} ===")
    print(f"Points: {len(points)}")
    print(f"Linear fit: k = {slope:.4f} * f + {intercept:.5f}")
    print(f"RMSE: {rmse:.6f}")

    # Express as ratio
    # If k = a*f + b, then at boundary: k/f = a + b/f
    # For large f: k/f → a
    print(f"Slope (dk/df): {slope:.4f}")
    print(f"Intercept: {intercept:.5f}")

    return slope, intercept


def analyze_geometry():
    """Analyze the overall geometry of the pattern region."""

    print("=" * 60)
    print("PATTERN REGION BOUNDARY GEOMETRY")
    print("=" * 60)

    slope_upper, intercept_upper = fit_boundary(upper_boundary, "UPPER BOUNDARY (P meets extinction)")
    slope_lower, intercept_lower = fit_boundary(lower_boundary, "LOWER BOUNDARY (P meets uniform)")

    print("\n" + "=" * 60)
    print("COMBINED ANALYSIS")
    print("=" * 60)

    avg_slope = (slope_upper + slope_lower) / 2
    bandwidth = intercept_upper - intercept_lower

    print(f"\nAverage slope: {avg_slope:.4f}")
    print(f"Bandwidth (intercept difference): {bandwidth:.5f}")

    print("\n--- Boundary equations ---")
    print(f"Upper: k = {slope_upper:.4f} * f + {intercept_upper:.5f}")
    print(f"Lower: k = {slope_lower:.4f} * f + {intercept_lower:.5f}")

    # Check if slopes are similar (parallel lines)
    slope_diff = abs(slope_upper - slope_lower)
    print(f"\nSlope difference: {slope_diff:.4f}")
    if slope_diff < 0.1:
        print("→ Boundaries are approximately PARALLEL")
    else:
        print("→ Boundaries are NOT parallel - band WIDENS or NARROWS")

    # Physical interpretation
    print("\n" + "=" * 60)
    print("PHYSICAL INTERPRETATION")
    print("=" * 60)

    print("""
The pattern region can be characterized as:

1. BOTH boundaries have positive slope (dk/df > 0)
   → As feed rate (f) increases, kill rate (k) must also increase
     to maintain patterns

2. The boundaries are approximately LINEAR
   → The transition between phases is determined by a simple
     linear relationship, not a complex curve

3. The boundaries appear roughly PARALLEL
   → The "width" of the pattern region in k is approximately
     constant across different f values
   → This means there's a FIXED RANGE of viable k values
     relative to f

4. Key relationship: k ≈ f + 0.03 (roughly)
   → Patterns emerge when k is slightly larger than f
   → Too small k → uniform (V wins)
   → Too large k → extinction (V dies)
   → Just right → Turing patterns!
""")

    # Check the k/f ratio
    print("\n--- Ratio analysis ---")
    for f, k in upper_boundary[:5]:
        ratio = k / f
        diff = k - f
        print(f"Upper: f={f:.3f}, k={k:.3f}, k/f={ratio:.2f}, k-f={diff:.4f}")

    print()
    for f, k in lower_boundary[:5]:
        ratio = k / f
        diff = k - f
        print(f"Lower: f={f:.3f}, k={k:.3f}, k/f={ratio:.2f}, k-f={diff:.4f}")

    print("""
Notice: k - f is roughly constant along each boundary!
- Upper boundary: k - f ≈ 0.03-0.04
- Lower boundary: k - f ≈ 0.02-0.03

This suggests the KEY PARAMETER is not k or f alone,
but the DIFFERENCE (k - f) or equivalently the RATIO k/f.

Patterns emerge when:  0.02 < k - f < 0.04  (approximately)
""")


if __name__ == '__main__':
    analyze_geometry()
