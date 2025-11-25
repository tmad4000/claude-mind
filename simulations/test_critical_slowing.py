#!/usr/bin/env python3
"""
Test for CRITICAL SLOWING DOWN in pattern formation.

Near phase transitions, systems often show diverging relaxation times.
If Gray-Scott shows this near the pattern/no-pattern boundary, it could
indicate critical behavior that might be quantifiable.

Measure:
1. Time to reach steady-state pattern from nucleated IC
2. How this time varies as we approach the boundary
3. Whether there's a power-law divergence

A quantitative critical exponent would be genuinely interesting.
"""

import numpy as np
import json

Du, Dv = 0.16, 0.08
N = 64
dx = 1.0

def laplacian(Z, dx):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z) / (dx*dx)

def step(U, V, f, k):
    uvv = U * V * V
    return (np.clip(U + Du * laplacian(U, dx) - uvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv - (k + f) * V, 0, 1))

def init_nucleated(N):
    """Initialize with finite-amplitude spots to nucleate patterns."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    np.random.seed(42)
    for _ in range(5):
        cx, cy = np.random.randint(N//4, 3*N//4, 2)
        r = 3
        y, x = np.ogrid[:N, :N]
        mask = (x-cx)**2 + (y-cy)**2 <= r*r
        U[mask], V[mask] = 0.5, 0.25
    return U, V

def measure_relaxation_time(f, k, max_steps=100000, check_interval=500):
    """
    Measure time to reach steady state.
    Returns (relaxation_time, final_state)
    """
    U, V = init_nucleated(N)

    v_std_history = []
    v_mean_history = []

    for step_num in range(max_steps):
        U, V = step(U, V, f, k)

        if step_num % check_interval == 0:
            v_std = np.std(V)
            v_mean = np.mean(V)
            v_std_history.append(v_std)
            v_mean_history.append(v_mean)

            # Check for steady state
            if len(v_std_history) >= 5:
                recent_std = v_std_history[-5:]
                variation = np.std(recent_std) / (np.mean(recent_std) + 1e-10)

                if variation < 0.01:  # Relative variation < 1%
                    final_std = np.mean(recent_std)
                    if final_std < 0.02:
                        return step_num, 'uniform'
                    else:
                        return step_num, 'pattern'

    # Didn't converge
    final_std = np.std(V)
    if final_std < 0.02:
        return max_steps, 'uniform_slow'
    else:
        return max_steps, 'pattern_slow'

def main():
    print("=" * 70)
    print("CRITICAL SLOWING DOWN ANALYSIS")
    print("=" * 70)
    print()
    print("Measuring pattern formation time near the phase boundary...")
    print()

    # For fixed f, scan k from pattern region toward boundary
    f = 0.035

    # Scan k from deep in pattern region toward the boundary
    k_values = np.arange(0.056, 0.070, 0.001)

    results = []

    print(f"Fixed f = {f}")
    print(f"{'k':>6} {'relax_time':>12} {'final_state':>15}")
    print("-" * 40)

    for k in k_values:
        relax_time, final_state = measure_relaxation_time(f, k)
        results.append({
            'f': float(f),
            'k': float(k),
            'relaxation_time': int(relax_time),
            'final_state': final_state
        })

        marker = "→" if 'pattern' in final_state else "×"
        print(f"{k:6.3f} {relax_time:12d} {final_state:>15} {marker}")

    print()

    # Repeat for another f value
    f = 0.045
    print(f"\nFixed f = {f}")
    print(f"{'k':>6} {'relax_time':>12} {'final_state':>15}")
    print("-" * 40)

    k_values = np.arange(0.060, 0.074, 0.001)

    for k in k_values:
        relax_time, final_state = measure_relaxation_time(f, k)
        results.append({
            'f': float(f),
            'k': float(k),
            'relaxation_time': int(relax_time),
            'final_state': final_state
        })

        marker = "→" if 'pattern' in final_state else "×"
        print(f"{k:6.3f} {relax_time:12d} {final_state:>15} {marker}")

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    # Look for divergence near boundary
    for f_val in [0.035, 0.045]:
        f_results = [r for r in results if r['f'] == f_val]
        pattern_results = [r for r in f_results if 'pattern' in r['final_state']]
        uniform_results = [r for r in f_results if 'uniform' in r['final_state']]

        if pattern_results and uniform_results:
            # Find boundary
            k_boundary = (max(r['k'] for r in pattern_results) +
                         min(r['k'] for r in uniform_results)) / 2

            print(f"f = {f_val}:")
            print(f"  Pattern region: k < {max(r['k'] for r in pattern_results):.3f}")
            print(f"  Uniform region: k > {min(r['k'] for r in uniform_results):.3f}")
            print(f"  Boundary: k ≈ {k_boundary:.3f}")

            # Check for increasing relaxation time near boundary
            near_boundary = [r for r in pattern_results
                           if abs(r['k'] - k_boundary) < 0.005]
            if near_boundary:
                max_time_near = max(r['relaxation_time'] for r in near_boundary)
                avg_time = np.mean([r['relaxation_time'] for r in pattern_results])
                print(f"  Max relaxation time near boundary: {max_time_near}")
                print(f"  Average relaxation time: {avg_time:.0f}")
                if max_time_near > 2 * avg_time:
                    print("  *** POSSIBLE CRITICAL SLOWING DOWN ***")
                else:
                    print("  No significant slowing detected")
            print()

    # Save results
    with open('critical_slowing_results.json', 'w') as file:
        json.dump({'results': results}, file, indent=2)

    print("Results saved to critical_slowing_results.json")

if __name__ == '__main__':
    main()
