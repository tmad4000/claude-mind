#!/usr/bin/env python3
"""
Test for PARAMETER HYSTERESIS in Gray-Scott.

In subcritical bifurcations, we expect HYSTERESIS:
- Increasing k from pattern region: patterns persist beyond linear instability
- Decreasing k from uniform region: patterns don't form until much lower k

The WIDTH of this hysteresis loop is a quantitative measure of the
subcritical nature. If we can measure it precisely and compare to
any theoretical predictions, that could be novel.

Also test: Does the hysteresis width depend on RAMP RATE?
In non-equilibrium systems, the rate matters (like rate-dependent tipping).
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

def init_pattern(N):
    """Initialize with developed pattern."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    np.random.seed(42)
    for _ in range(10):
        cx, cy = np.random.randint(0, N, 2)
        r = 4
        y, x = np.ogrid[:N, :N]
        mask = ((np.minimum(np.abs(x-cx), N-np.abs(x-cx)))**2 +
                (np.minimum(np.abs(y-cy), N-np.abs(y-cy)))**2) <= r*r
        U[mask], V[mask] = 0.5, 0.25
    return U, V

def init_uniform(N):
    """Initialize with uniform state."""
    return np.ones((N, N)), np.zeros((N, N))

def has_pattern(V, threshold=0.02):
    return np.std(V) > threshold

def ramp_k_upward(f, k_start, k_end, ramp_rate, steps_per_k=1000):
    """
    Start from pattern, ramp k upward until pattern dies.
    ramp_rate: change in k per 1000 steps
    """
    # First establish pattern at k_start
    U, V = init_pattern(N)
    for _ in range(20000):
        U, V = step(U, V, f, k_start)

    if not has_pattern(V):
        return None, []  # Couldn't establish pattern

    k = k_start
    trajectory = []
    k_death = None

    while k <= k_end:
        # Run for steps_per_k at current k
        for _ in range(steps_per_k):
            U, V = step(U, V, f, k)

        v_std = np.std(V)
        trajectory.append({'k': float(k), 'v_std': float(v_std)})

        if not has_pattern(V) and k_death is None:
            k_death = k

        k += ramp_rate

    return k_death, trajectory

def ramp_k_downward(f, k_start, k_end, ramp_rate, steps_per_k=1000):
    """
    Start from uniform, ramp k downward until pattern forms.
    """
    # Start from uniform at k_start
    U, V = init_uniform(N)
    # Add tiny perturbation
    U += 0.001 * np.random.randn(N, N)
    V += 0.0005 * np.random.randn(N, N)
    U = np.clip(U, 0, 1)
    V = np.clip(V, 0, 1)

    k = k_start
    trajectory = []
    k_birth = None

    while k >= k_end:
        # Run for steps_per_k at current k
        for _ in range(steps_per_k):
            U, V = step(U, V, f, k)

        v_std = np.std(V)
        trajectory.append({'k': float(k), 'v_std': float(v_std)})

        if has_pattern(V) and k_birth is None:
            k_birth = k

        k -= ramp_rate

    return k_birth, trajectory

def measure_hysteresis_loop(f, k_range=(0.050, 0.075), ramp_rate=0.0005):
    """Measure full hysteresis loop."""
    k_start, k_end = k_range

    # Upward sweep
    k_death, up_traj = ramp_k_upward(f, k_start, k_end, ramp_rate)

    # Downward sweep
    k_birth, down_traj = ramp_k_downward(f, k_end, k_start, ramp_rate)

    return {
        'k_death': float(k_death) if k_death else None,
        'k_birth': float(k_birth) if k_birth else None,
        'hysteresis_width': float(k_death - k_birth) if (k_death and k_birth) else None,
        'upward_trajectory': up_traj,
        'downward_trajectory': down_traj
    }

def main():
    print("=" * 70)
    print("PARAMETER HYSTERESIS ANALYSIS")
    print("=" * 70)
    print()
    print("Testing for hysteresis in pattern formation/destruction...")
    print()

    results = []

    # Test at multiple f values
    f_values = [0.030, 0.035, 0.040, 0.045]

    # Also test rate-dependence
    ramp_rates = [0.001, 0.0005, 0.0002]

    print(f"{'f':>6} {'rate':>8} {'k_death':>10} {'k_birth':>10} {'width':>10}")
    print("-" * 50)

    for f in f_values:
        for rate in ramp_rates:
            result = measure_hysteresis_loop(f, ramp_rate=rate)
            result['f'] = float(f)
            result['ramp_rate'] = float(rate)
            results.append(result)

            width = result['hysteresis_width']
            k_death = result['k_death']
            k_birth = result['k_birth']

            print(f"{f:6.3f} {rate:8.4f} {k_death if k_death else 'N/A':>10} "
                  f"{k_birth if k_birth else 'N/A':>10} "
                  f"{width if width else 'N/A':>10}")

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    # Analyze hysteresis width
    valid = [r for r in results if r['hysteresis_width'] is not None]

    if len(valid) < 2:
        print("Not enough valid hysteresis loops measured")
    else:
        widths = [r['hysteresis_width'] for r in valid]
        mean_width = np.mean(widths)
        std_width = np.std(widths)

        print(f"Mean hysteresis width: {mean_width:.4f} ± {std_width:.4f}")
        print()

        # Check rate dependence
        print("Rate dependence:")
        for rate in ramp_rates:
            rate_results = [r for r in valid if r['ramp_rate'] == rate]
            if rate_results:
                rate_widths = [r['hysteresis_width'] for r in rate_results]
                print(f"  Rate {rate:.4f}: mean width = {np.mean(rate_widths):.4f}")

        # Check if width increases with slower rate (suggests true bistability vs kinetic)
        slow_rate = min(ramp_rates)
        fast_rate = max(ramp_rates)
        slow_widths = [r['hysteresis_width'] for r in valid if r['ramp_rate'] == slow_rate]
        fast_widths = [r['hysteresis_width'] for r in valid if r['ramp_rate'] == fast_rate]

        if slow_widths and fast_widths:
            slow_mean = np.mean(slow_widths)
            fast_mean = np.mean(fast_widths)
            print()
            if slow_mean > fast_mean * 1.1:
                print("INTERESTING: Hysteresis WIDENS at slower ramp rates!")
                print("This indicates true thermodynamic bistability, not kinetic trapping.")
            elif fast_mean > slow_mean * 1.1:
                print("Note: Hysteresis NARROWS at slower ramp rates.")
                print("This suggests kinetic trapping, not true bistability.")
            else:
                print("Hysteresis width is roughly rate-independent.")

        # Check f dependence
        print()
        print("f dependence:")
        for f_val in f_values:
            f_results = [r for r in valid if r['f'] == f_val]
            if f_results:
                f_widths = [r['hysteresis_width'] for r in f_results]
                print(f"  f={f_val:.3f}: mean width = {np.mean(f_widths):.4f}")

    # Save results
    with open('hysteresis_results.json', 'w') as file:
        json.dump({
            'results': results,
            'summary': {
                'mean_hysteresis_width': float(mean_width) if valid else None,
                'std_hysteresis_width': float(std_width) if valid else None
            }
        }, file, indent=2)

    print()
    print("Results saved to hysteresis_results.json")

if __name__ == '__main__':
    main()
