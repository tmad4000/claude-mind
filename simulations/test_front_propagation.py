#!/usr/bin/env python3
"""
Test PATTERN FRONT PROPAGATION in Gray-Scott.

Instead of looking at final states, examine the DYNAMICS of how patterns
grow from nucleation sites. This could reveal:

1. Front velocity as a function of parameters
2. Pulled vs pushed front distinction
3. Velocity selection mechanism
4. Possible universal scaling near boundaries

In the theory of pattern fronts:
- PULLED fronts: velocity set by linear growth rate at leading edge
- PUSHED fronts: velocity set by nonlinear saturation (faster than pulled)

For deeply subcritical systems like Gray-Scott (where linear instability
doesn't exist), fronts MUST be pushed. This could be quantifiable.
"""

import numpy as np
import json

Du, Dv = 0.16, 0.08
N = 256  # Large domain to measure front velocity
dx = 1.0

def laplacian(Z, dx):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z) / (dx*dx)

def step(U, V, f, k):
    uvv = U * V * V
    return (np.clip(U + Du * laplacian(U, dx) - uvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv - (k + f) * V, 0, 1))

def init_single_spot(N):
    """Initialize with a single spot in the center."""
    U, V = np.ones((N, N)), np.zeros((N, N))
    cx, cy = N // 2, N // 2
    r = 5
    y, x = np.ogrid[:N, :N]
    mask = (x - cx)**2 + (y - cy)**2 <= r**2
    U[mask] = 0.5
    V[mask] = 0.25
    return U, V

def measure_front_radius(V, threshold=0.05):
    """Measure the radius of the pattern front from center."""
    N = V.shape[0]
    cx, cy = N // 2, N // 2

    # Find all points above threshold
    above = V > threshold
    if not np.any(above):
        return 0

    # Calculate distances from center for above-threshold points
    y, x = np.where(above)
    distances = np.sqrt((x - cx)**2 + (y - cy)**2)

    # Return the 95th percentile distance (to get the front, not the max)
    return np.percentile(distances, 95)

def measure_front_velocity(f, k, n_steps=50000, measure_interval=1000):
    """
    Measure the front propagation velocity.

    Returns:
    - velocity: pixels per step
    - radii: list of front radii over time
    - times: corresponding timesteps
    - final_state: 'growing', 'saturated', 'collapsed'
    """
    U, V = init_single_spot(N)

    radii = []
    times = []

    for step_num in range(n_steps):
        U, V = step(U, V, f, k)

        if step_num % measure_interval == 0:
            r = measure_front_radius(V)
            radii.append(r)
            times.append(step_num)

            # Check if front reached boundary
            if r > N // 2 - 10:
                break

            # Check if pattern collapsed
            if step_num > 5000 and r < 5:
                return 0, radii, times, 'collapsed'

    if len(radii) < 3:
        return 0, radii, times, 'too_short'

    # Calculate velocity from linear fit of radius vs time
    radii = np.array(radii)
    times = np.array(times)

    # Use middle portion to avoid initial transient and saturation
    start_idx = len(radii) // 4
    end_idx = 3 * len(radii) // 4

    if end_idx - start_idx < 3:
        return 0, radii.tolist(), times.tolist(), 'too_short'

    # Linear fit
    t_fit = times[start_idx:end_idx]
    r_fit = radii[start_idx:end_idx]

    slope, _ = np.polyfit(t_fit, r_fit, 1)

    # Check if growing, saturated, or still expanding
    final_r = radii[-1]
    if final_r > N // 2 - 10:
        state = 'reached_boundary'
    elif slope > 0.001:
        state = 'growing'
    else:
        state = 'saturated'

    return slope, radii.tolist(), times.tolist(), state

def theoretical_velocity_estimate(f, k):
    """
    Estimate front velocity from diffusion-reaction balance.

    For a pushed front, v ~ sqrt(D * reaction_rate)
    The relevant rate is approximately (k + f) for V decay.

    This is a crude estimate - real pushed front velocity depends
    on the nonlinear profile.
    """
    # Crude estimate based on Fisher-KPP type scaling
    # v ~ 2 * sqrt(D * growth_rate)
    # But for Gray-Scott, growth rate is complicated

    # Use an empirical estimate based on typical pattern wavelength
    wavelength = 2 * np.pi / np.sqrt((k + f) / (2 * Dv))
    growth_rate = 1.0 / wavelength  # Rough estimate

    v_estimate = 2 * np.sqrt(Dv * growth_rate)
    return v_estimate

def main():
    print("=" * 70)
    print("PATTERN FRONT PROPAGATION ANALYSIS")
    print("=" * 70)
    print()
    print("Measuring how fast patterns spread from nucleation sites...")
    print()

    # Test across parameter space
    test_points = []

    # Scan along lines of constant f
    for f in [0.030, 0.035, 0.040, 0.045]:
        for k_offset in [-0.002, 0, 0.002, 0.004, 0.006]:
            k = 0.055 + (f - 0.030) * 0.4 + k_offset
            test_points.append((f, k))

    results = []

    print(f"{'f':>6} {'k':>6} {'v_sim':>10} {'v_theory':>10} {'ratio':>8} {'state':>15}")
    print("-" * 70)

    for f, k in test_points:
        velocity, radii, times, state = measure_front_velocity(f, k)
        v_theory = theoretical_velocity_estimate(f, k)

        if velocity > 0:
            ratio = velocity / v_theory
            print(f"{f:6.3f} {k:6.3f} {velocity:10.6f} {v_theory:10.4f} {ratio:8.4f} {state:>15}")
        else:
            print(f"{f:6.3f} {k:6.3f} {'N/A':>10} {v_theory:10.4f} {'N/A':>8} {state:>15}")
            ratio = None

        results.append({
            'f': float(f),
            'k': float(k),
            'velocity': float(velocity) if velocity else None,
            'v_theory': float(v_theory),
            'ratio': float(ratio) if ratio else None,
            'state': state,
            'radii': radii,
            'times': times
        })

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    # Analyze velocity scaling
    valid = [r for r in results if r['velocity'] is not None and r['velocity'] > 0]

    if len(valid) < 3:
        print("Not enough valid data points for analysis")
    else:
        velocities = [r['velocity'] for r in valid]
        v_theories = [r['v_theory'] for r in valid]
        ratios = [r['ratio'] for r in valid]

        mean_v = np.mean(velocities)
        std_v = np.std(velocities)
        mean_ratio = np.mean(ratios)
        std_ratio = np.std(ratios)

        print(f"Mean velocity: {mean_v:.6f} ± {std_v:.6f} pixels/step")
        print(f"Mean ratio (sim/theory): {mean_ratio:.4f} ± {std_ratio:.4f}")
        print()

        # Check for velocity variation with parameters
        f_values = [r['f'] for r in valid]
        k_values = [r['k'] for r in valid]

        if len(set(f_values)) > 1:
            corr_f = np.corrcoef(f_values, velocities)[0, 1]
            print(f"Correlation of velocity with f: {corr_f:.3f}")

        if len(set(k_values)) > 1:
            corr_k = np.corrcoef(k_values, velocities)[0, 1]
            print(f"Correlation of velocity with k: {corr_k:.3f}")

        print()

        # Look for velocity near boundaries
        # Group by state
        collapsed = [r for r in results if r['state'] == 'collapsed']
        growing = [r for r in results if r['state'] in ['growing', 'reached_boundary']]

        print(f"Growing fronts: {len(growing)}")
        print(f"Collapsed: {len(collapsed)}")

        if growing and collapsed:
            # Find boundary between growing and collapsed
            growing_k = [r['k'] for r in growing]
            collapsed_k = [r['k'] for r in collapsed]

            if min(growing_k) < max(collapsed_k):
                print()
                print("Interesting: growing and collapsed regions OVERLAP in k!")
                print("This suggests bistability in front propagation.")

    # Save results
    with open('front_propagation_results.json', 'w') as f:
        json.dump({
            'results': results,
            'summary': {
                'mean_velocity': float(mean_v) if valid else None,
                'std_velocity': float(std_v) if valid else None,
                'mean_ratio': float(mean_ratio) if valid else None,
                'n_growing': len([r for r in results if r['state'] in ['growing', 'reached_boundary']]),
                'n_collapsed': len([r for r in results if r['state'] == 'collapsed'])
            }
        }, f, indent=2)

    print()
    print("Results saved to front_propagation_results.json")

if __name__ == '__main__':
    main()
