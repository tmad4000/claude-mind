#!/usr/bin/env python3
"""
RD Saddle Point Hypothesis Test v2

Fixed complexity metric to properly detect RD patterns.
"""

import numpy as np
import json
from datetime import datetime
import os

INTERESTING_POINTS = [
    {"name": "mitosis", "f": 0.026, "k": 0.051},
    {"name": "solitons", "f": 0.042, "k": 0.063},
    {"name": "coral", "f": 0.062, "k": 0.063},
    {"name": "worms", "f": 0.054, "k": 0.063},
]

def laplacian(a):
    return (
        np.roll(a, 1, axis=0) + np.roll(a, -1, axis=0) +
        np.roll(a, 1, axis=1) + np.roll(a, -1, axis=1) -
        4 * a
    )

def simulate_gray_scott(f, k, steps=10000, size=100, Du=0.16, Dv=0.08, dt=1.0):
    """Run Gray-Scott simulation."""
    u = np.ones((size, size))
    v = np.zeros((size, size))

    r = 15
    cx, cy = size // 2, size // 2
    u[cx-r:cx+r, cy-r:cy+r] = 0.5
    v[cx-r:cx+r, cy-r:cy+r] = 0.25

    np.random.seed(42)
    u += 0.05 * np.random.random((size, size))
    v += 0.05 * np.random.random((size, size))

    for _ in range(steps):
        uvv = u * v * v
        Lu = laplacian(u)
        Lv = laplacian(v)
        u += dt * (Du * Lu - uvv + f * (1 - u))
        v += dt * (Dv * Lv + uvv - (f + k) * v)
        u = np.clip(u, 0, 1)
        v = np.clip(v, 0, 1)

    return u, v

def measure_complexity_v2(v):
    """
    Improved complexity measure for RD patterns.

    Uses multiple metrics tuned for continuous systems:
    - pattern_strength: contrast between high/low regions
    - structure: spatial organization (not just noise)
    - diversity: variety of values in the pattern
    """
    v_std = np.std(v)
    v_range = v.max() - v.min()

    # Pattern strength: how much contrast exists
    pattern_strength = v_std / (v.mean() + 0.001)

    # Structure: autocorrelation at typical pattern scales
    # High for organized patterns, low for uniform or pure noise
    def local_autocorr(arr, lag=5):
        shifted = np.roll(arr, lag, axis=0)
        return np.corrcoef(arr.flatten(), shifted.flatten())[0, 1]

    autocorr = abs(local_autocorr(v, 5))

    # Diversity: entropy of histogram
    if v_range > 0.01:
        v_norm = (v - v.min()) / v_range
        hist, _ = np.histogram(v_norm.flatten(), bins=50, density=True)
        hist = hist[hist > 0]
        entropy = -np.sum(hist * np.log(hist + 1e-10)) / np.log(50)
    else:
        entropy = 0

    # Edge presence: gradient magnitude
    gy = np.roll(v, -1, axis=0) - v
    gx = np.roll(v, -1, axis=1) - v
    edge_density = np.mean(np.sqrt(gx**2 + gy**2))

    # Combined complexity:
    # Good patterns have: moderate strength + high structure + moderate entropy
    complexity = pattern_strength * autocorr * (0.3 + entropy) * (0.1 + edge_density)

    return {
        "pattern_strength": float(pattern_strength),
        "autocorrelation": float(autocorr),
        "entropy": float(entropy),
        "edge_density": float(edge_density),
        "complexity": float(complexity),
        "v_std": float(v_std),
        "v_range": float(v_range)
    }

def classify_pattern_v2(metrics):
    """Classify pattern type based on improved metrics."""
    if metrics["v_range"] < 0.05:
        return "uniform"
    elif metrics["autocorrelation"] < 0.3 and metrics["pattern_strength"] > 0.5:
        return "noise"
    elif metrics["autocorrelation"] > 0.6 and metrics["pattern_strength"] > 0.3:
        return "structured"
    elif metrics["pattern_strength"] < 0.1:
        return "weak"
    else:
        return "transitional"

def test_perturbations(center_f, center_k, delta=0.003, n_directions=8):
    """Test perturbations around a center point."""
    results = []

    print(f"  Testing center: f={center_f:.4f}, k={center_k:.4f}")
    u, v = simulate_gray_scott(center_f, center_k)
    metrics = measure_complexity_v2(v)
    results.append({
        "f": center_f,
        "k": center_k,
        "direction": "center",
        **metrics,
        "pattern_type": classify_pattern_v2(metrics)
    })

    angles = np.linspace(0, 2*np.pi, n_directions, endpoint=False)

    for i, angle in enumerate(angles):
        df = delta * np.cos(angle)
        dk = delta * np.sin(angle)
        f = center_f + df
        k = center_k + dk

        if f < 0.01 or f > 0.1 or k < 0.03 or k > 0.08:
            continue

        print(f"  Testing direction {i}: f={f:.4f}, k={k:.4f}")
        u, v = simulate_gray_scott(f, k)
        metrics = measure_complexity_v2(v)

        results.append({
            "f": f,
            "k": k,
            "direction": f"angle_{int(np.degrees(angle))}",
            **metrics,
            "pattern_type": classify_pattern_v2(metrics)
        })

    return results

def analyze_saddle_property(results):
    """Analyze whether the center point is a saddle point."""
    center = results[0]
    perturbations = results[1:]

    if not perturbations:
        return {"is_saddle": None, "reason": "No valid perturbations"}

    center_complexity = center["complexity"]
    complexities = [p["complexity"] for p in perturbations]

    less_complex = sum(1 for c in complexities if c < center_complexity * 0.9)  # 10% tolerance
    fraction_less_complex = less_complex / len(perturbations)

    # Also check if center is a local maximum
    is_local_max = center_complexity > np.mean(complexities)

    is_saddle = fraction_less_complex > 0.6 and is_local_max

    return {
        "center_complexity": center_complexity,
        "center_type": center["pattern_type"],
        "mean_neighbor_complexity": np.mean(complexities),
        "num_perturbations": len(perturbations),
        "less_complex_count": less_complex,
        "fraction_less_complex": fraction_less_complex,
        "is_local_max": is_local_max,
        "is_saddle": is_saddle,
        "perturbation_complexities": complexities,
        "perturbation_types": [p["pattern_type"] for p in perturbations]
    }

def main():
    print("=" * 60)
    print("RD SADDLE POINT HYPOTHESIS TEST v2")
    print("=" * 60)
    print()
    print("Testing with improved complexity metrics")
    print()

    all_results = {}

    for point in INTERESTING_POINTS:
        print(f"\n{'='*60}")
        print(f"Testing: {point['name']} (f={point['f']}, k={point['k']})")
        print("=" * 60)

        results = test_perturbations(point['f'], point['k'], delta=0.004, n_directions=8)
        analysis = analyze_saddle_property(results)

        center = results[0]
        print(f"\nMetrics for {point['name']}:")
        print(f"  Pattern type: {center['pattern_type']}")
        print(f"  Complexity: {center['complexity']:.6f}")
        print(f"  Pattern strength: {center['pattern_strength']:.4f}")
        print(f"  Autocorrelation: {center['autocorrelation']:.4f}")

        print(f"\nSaddle Analysis:")
        print(f"  Center complexity: {analysis['center_complexity']:.6f}")
        print(f"  Mean neighbor complexity: {analysis['mean_neighbor_complexity']:.6f}")
        print(f"  Is local max: {analysis['is_local_max']}")
        print(f"  Less complex neighbors: {analysis['less_complex_count']}/{analysis['num_perturbations']} ({analysis['fraction_less_complex']*100:.0f}%)")
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
    local_max_count = sum(1 for r in all_results.values() if r['analysis']['is_local_max'])

    print(f"\nSaddle points: {saddle_count}/{len(INTERESTING_POINTS)}")
    print(f"Local maxima: {local_max_count}/{len(INTERESTING_POINTS)}")

    for name, data in all_results.items():
        a = data['analysis']
        status = "SADDLE" if a['is_saddle'] else ("local max" if a['is_local_max'] else "neither")
        print(f"  {name}: {status} (complexity={a['center_complexity']:.4f}, {a['fraction_less_complex']*100:.0f}% lower)")

    # Save
    output = {
        "experiment": "rd_saddle_hypothesis_test_v2",
        "timestamp": datetime.now().isoformat(),
        "hypothesis": "Interesting RD parameters are saddle points in complexity space",
        "results": all_results,
        "summary": {
            "total_points_tested": len(INTERESTING_POINTS),
            "saddle_points_found": saddle_count,
            "local_maxima_found": local_max_count,
        }
    }

    os.makedirs("simulations/results", exist_ok=True)
    with open("simulations/results/rd_saddle_test_v2_results.json", "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\nResults saved to simulations/results/rd_saddle_test_v2_results.json")

    # Conclusion
    print("\n" + "=" * 60)
    print("CONCLUSION")
    print("=" * 60)

    if local_max_count >= len(INTERESTING_POINTS) * 0.7:
        if saddle_count >= len(INTERESTING_POINTS) * 0.5:
            print("STRONG SUPPORT: Interesting points ARE complexity maxima AND saddle points!")
        else:
            print("PARTIAL SUPPORT: Interesting points are complexity maxima but not strict saddle points.")
            print("RD parameter space may have broader 'ridges' rather than isolated peaks.")
    else:
        print("WEAK SUPPORT: Results are mixed.")

if __name__ == "__main__":
    main()
