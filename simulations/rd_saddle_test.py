#!/usr/bin/env python3
"""
RD Saddle Point Hypothesis Test

If complexity exists at saddle points in parameter space, then:
1. Find an "interesting" parameter point (mitosis, waves, etc.)
2. Perturb it in all directions
3. See if perturbations always lead to "simpler" behavior

This tests whether the CA finding (Class IV rules are isolated saddle points)
generalizes to continuous dynamical systems.
"""

import numpy as np
import json
from datetime import datetime
import os

# Gray-Scott parameters
# Known interesting points:
# - f=0.026, k=0.051 - mitosis/spots
# - f=0.042, k=0.063 - solitons
# - f=0.014, k=0.045 - waves

INTERESTING_POINTS = [
    {"name": "mitosis", "f": 0.026, "k": 0.051},
    {"name": "solitons", "f": 0.042, "k": 0.063},
    {"name": "coral", "f": 0.062, "k": 0.063},
    {"name": "waves", "f": 0.014, "k": 0.045},
]

def laplacian(a):
    """Compute Laplacian using finite differences with periodic boundary."""
    return (
        np.roll(a, 1, axis=0) + np.roll(a, -1, axis=0) +
        np.roll(a, 1, axis=1) + np.roll(a, -1, axis=1) -
        4 * a
    )

def uniform_filter(arr, size):
    """Simple uniform filter (box blur) for local averages."""
    result = np.zeros_like(arr)
    half = size // 2
    for di in range(-half, half + 1):
        for dj in range(-half, half + 1):
            result += np.roll(np.roll(arr, di, axis=0), dj, axis=1)
    return result / (size * size)

def simulate_gray_scott(f, k, steps=5000, size=100, Du=0.16, Dv=0.08, dt=1.0):
    """Run Gray-Scott simulation and return final state."""
    # Initialize
    u = np.ones((size, size))
    v = np.zeros((size, size))

    # Add seed perturbation
    r = 10
    cx, cy = size // 2, size // 2
    u[cx-r:cx+r, cy-r:cy+r] = 0.5
    v[cx-r:cx+r, cy-r:cy+r] = 0.25

    # Add some noise
    np.random.seed(42)  # Reproducibility
    u += 0.05 * np.random.random((size, size))
    v += 0.05 * np.random.random((size, size))

    # Run simulation
    for _ in range(steps):
        uvv = u * v * v

        # Laplacian (periodic boundary)
        Lu = laplacian(u)
        Lv = laplacian(v)

        # Update
        u += dt * (Du * Lu - uvv + f * (1 - u))
        v += dt * (Dv * Lv + uvv - (f + k) * v)

        # Clamp
        u = np.clip(u, 0, 1)
        v = np.clip(v, 0, 1)

    return u, v

def measure_complexity(v):
    """
    Measure complexity of the pattern.

    Returns dict with:
    - entropy: spatial entropy
    - structure: variance of local variance (high = structured patterns)
    - activity: how much of the domain is "active" (not uniform)
    - edge_density: amount of edges/transitions
    """
    # Entropy-like measure
    v_range = v.max() - v.min()
    if v_range < 1e-10:
        return {
            "entropy": 0,
            "structure": 0,
            "activity": 0,
            "edge_density": 0,
            "complexity": 0
        }

    v_norm = (v - v.min()) / v_range
    hist, _ = np.histogram(v_norm.flatten(), bins=50, density=True)
    hist = hist[hist > 0]
    entropy = -np.sum(hist * np.log(hist + 1e-10)) / np.log(50)  # Normalized

    # Structure measure: variance of local windows
    local_mean = uniform_filter(v, size=5)
    local_var = uniform_filter((v - local_mean)**2, size=5)
    structure = np.std(local_var)  # Structured patterns have varied local variance

    # Activity: how much is non-uniform
    activity = np.std(v)

    # Edge density: gradient magnitude
    gy = np.roll(v, -1, axis=0) - v
    gx = np.roll(v, -1, axis=1) - v
    edge_density = np.mean(np.sqrt(gx**2 + gy**2))

    # Combined complexity score
    # High complexity = moderate entropy + high structure + moderate activity
    # (Too high entropy = noise, too low = uniform)
    complexity = structure * activity * (1 - abs(entropy - 0.5))

    return {
        "entropy": float(entropy),
        "structure": float(structure),
        "activity": float(activity),
        "edge_density": float(edge_density),
        "complexity": float(complexity)
    }

def classify_pattern(metrics):
    """Classify pattern type based on metrics."""
    if metrics["activity"] < 0.01:
        return "uniform"
    elif metrics["structure"] < 0.001:
        return "noise"
    elif metrics["edge_density"] > 0.1:
        return "chaotic"
    else:
        return "structured"

def test_perturbations(center_f, center_k, delta=0.002, n_directions=8):
    """
    Test perturbations around a center point.

    Returns list of results for center + all perturbation directions.
    """
    results = []

    # Test center
    print(f"  Testing center: f={center_f:.4f}, k={center_k:.4f}")
    u, v = simulate_gray_scott(center_f, center_k)
    metrics = measure_complexity(v)
    results.append({
        "f": center_f,
        "k": center_k,
        "direction": "center",
        "delta_f": 0,
        "delta_k": 0,
        **metrics,
        "pattern_type": classify_pattern(metrics)
    })

    # Test perturbations in different directions
    angles = np.linspace(0, 2*np.pi, n_directions, endpoint=False)

    for i, angle in enumerate(angles):
        df = delta * np.cos(angle)
        dk = delta * np.sin(angle)
        f = center_f + df
        k = center_k + dk

        # Skip if out of reasonable bounds
        if f < 0.01 or f > 0.1 or k < 0.03 or k > 0.08:
            continue

        print(f"  Testing direction {i}: f={f:.4f}, k={k:.4f}")
        u, v = simulate_gray_scott(f, k)
        metrics = measure_complexity(v)

        results.append({
            "f": f,
            "k": k,
            "direction": f"angle_{int(np.degrees(angle))}",
            "delta_f": df,
            "delta_k": dk,
            **metrics,
            "pattern_type": classify_pattern(metrics)
        })

    return results

def analyze_saddle_property(results):
    """
    Analyze whether the center point is a saddle point for complexity.

    Returns analysis dict.
    """
    center = results[0]
    perturbations = results[1:]

    if not perturbations:
        return {"is_saddle": None, "reason": "No valid perturbations"}

    center_complexity = center["complexity"]

    # Count how many perturbations are less complex
    less_complex = sum(1 for p in perturbations if p["complexity"] < center_complexity)

    # For a saddle point, most/all perturbations should reduce complexity
    fraction_less_complex = less_complex / len(perturbations)

    # Check pattern type changes
    center_type = center["pattern_type"]
    type_changes = sum(1 for p in perturbations if p["pattern_type"] != center_type)

    is_saddle = fraction_less_complex > 0.7  # At least 70% of perturbations reduce complexity

    return {
        "center_complexity": center_complexity,
        "center_type": center_type,
        "num_perturbations": len(perturbations),
        "less_complex_count": less_complex,
        "fraction_less_complex": fraction_less_complex,
        "type_changes": type_changes,
        "is_saddle": is_saddle,
        "perturbation_complexities": [p["complexity"] for p in perturbations],
        "perturbation_types": [p["pattern_type"] for p in perturbations]
    }

def main():
    print("=" * 60)
    print("RD SADDLE POINT HYPOTHESIS TEST")
    print("=" * 60)
    print()
    print("Testing whether 'interesting' RD parameters are saddle points")
    print("in complexity space (like Class IV CA rules).")
    print()

    all_results = {}

    for point in INTERESTING_POINTS:
        print(f"\n{'='*60}")
        print(f"Testing: {point['name']} (f={point['f']}, k={point['k']})")
        print("=" * 60)

        results = test_perturbations(point['f'], point['k'], delta=0.003, n_directions=8)
        analysis = analyze_saddle_property(results)

        print(f"\nAnalysis for {point['name']}:")
        print(f"  Center complexity: {analysis['center_complexity']:.6f}")
        print(f"  Center type: {analysis['center_type']}")
        print(f"  Perturbations tested: {analysis['num_perturbations']}")
        print(f"  Less complex: {analysis['less_complex_count']} ({analysis['fraction_less_complex']*100:.0f}%)")
        print(f"  Type changes: {analysis['type_changes']}")
        print(f"  IS SADDLE: {'YES' if analysis['is_saddle'] else 'NO'}")

        all_results[point['name']] = {
            "point": point,
            "perturbation_results": results,
            "analysis": analysis
        }

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    saddle_count = sum(1 for r in all_results.values() if r['analysis']['is_saddle'])
    print(f"\nSaddle points found: {saddle_count}/{len(INTERESTING_POINTS)}")

    for name, data in all_results.items():
        status = "SADDLE" if data['analysis']['is_saddle'] else "not saddle"
        print(f"  {name}: {status} ({data['analysis']['fraction_less_complex']*100:.0f}% perturbations less complex)")

    # Save results
    output = {
        "experiment": "rd_saddle_hypothesis_test",
        "timestamp": datetime.now().isoformat(),
        "hypothesis": "Interesting RD parameters are saddle points in complexity space",
        "results": all_results,
        "summary": {
            "total_points_tested": len(INTERESTING_POINTS),
            "saddle_points_found": saddle_count,
            "support_for_hypothesis": saddle_count / len(INTERESTING_POINTS) if INTERESTING_POINTS else 0
        }
    }

    os.makedirs("simulations/results", exist_ok=True)
    with open("simulations/results/rd_saddle_test_results.json", "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\nResults saved to simulations/results/rd_saddle_test_results.json")

    # Conclusion
    print("\n" + "=" * 60)
    print("CONCLUSION")
    print("=" * 60)
    if saddle_count >= len(INTERESTING_POINTS) * 0.7:
        print("HYPOTHESIS SUPPORTED: Most interesting RD points are saddle points!")
        print("This suggests the CA finding generalizes to continuous systems.")
    elif saddle_count > 0:
        print("PARTIAL SUPPORT: Some interesting points are saddle points.")
        print("The relationship may be more nuanced in continuous systems.")
    else:
        print("HYPOTHESIS NOT SUPPORTED: Interesting RD points are not saddle points.")
        print("The CA saddle structure may be specific to discrete systems.")

if __name__ == "__main__":
    main()
