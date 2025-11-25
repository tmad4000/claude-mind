#!/usr/bin/env python3
"""
Verify bistability finding with longer simulations.
Check if patterns are truly stable equilibria, not slow transients.
"""

import numpy as np
import json

# Parameters
Du, Dv = 0.16, 0.08
N = 128
dx = 1.0
dt = 1.0

def laplacian(Z, dx):
    return (
        np.roll(Z, 1, axis=0) + np.roll(Z, -1, axis=0) +
        np.roll(Z, 1, axis=1) + np.roll(Z, -1, axis=1) - 4*Z
    ) / (dx*dx)

def step(U, V, f, k, dt=1.0):
    Lu = laplacian(U, dx)
    Lv = laplacian(V, dx)
    uvv = U * V * V
    U_new = U + dt * (Du * Lu - uvv + f * (1 - U))
    V_new = V + dt * (Dv * Lv + uvv - (k + f) * V)
    return np.clip(U_new, 0, 1), np.clip(V_new, 0, 1)

def init_spots(N, n_spots=15):
    U = np.ones((N, N))
    V = np.zeros((N, N))
    np.random.seed(42)
    for _ in range(n_spots):
        cx, cy = np.random.randint(0, N, 2)
        r = np.random.randint(3, 8)
        y, x = np.ogrid[:N, :N]
        dx_arr = np.minimum(np.abs(x - cx), N - np.abs(x - cx))
        dy_arr = np.minimum(np.abs(y - cy), N - np.abs(y - cy))
        mask = dx_arr**2 + dy_arr**2 <= r**2
        U[mask] = 0.5
        V[mask] = 0.25
    return U, V

def init_stripes(N, n_stripes=6):
    U = np.ones((N, N))
    V = np.zeros((N, N))
    stripe_width = N // (2 * n_stripes)
    for i in range(n_stripes):
        start = i * N // n_stripes + N // (4 * n_stripes)
        end = start + stripe_width
        U[start:end, :] = 0.5
        V[start:end, :] = 0.25
    return U, V

def compute_anisotropy(V):
    """Measure directional preference in pattern."""
    V_centered = V - np.mean(V)
    # FFT-based power spectrum
    fft = np.fft.fft2(V_centered)
    power = np.abs(fft)**2

    # Sum power in horizontal vs vertical directions
    N = V.shape[0]
    center = N // 2

    # Horizontal power (k_y near 0)
    h_power = np.sum(power[center-2:center+3, :])
    # Vertical power (k_x near 0)
    v_power = np.sum(power[:, center-2:center+3])

    # Anisotropy: positive = horizontal stripes, negative = vertical, near 0 = isotropic
    if h_power + v_power > 0:
        anisotropy = (h_power - v_power) / (h_power + v_power)
    else:
        anisotropy = 0

    return anisotropy

def compute_spot_measure(V, threshold=0.1):
    """Measure how 'spotty' vs 'stripy' the pattern is."""
    V_binary = V > threshold

    # Count isolated regions
    V_centered = V - np.mean(V)
    fft = np.fft.fft2(V_centered)
    power = np.abs(np.fft.fftshift(fft))**2

    N = V.shape[0]
    center = N // 2

    # Ring average at different radii
    y, x = np.ogrid[:N, :N]
    r = np.sqrt((x - center)**2 + (y - center)**2)

    # For spots: power concentrated in ring
    # For stripes: power concentrated on axes
    ring_10_20 = np.mean(power[(r > 10) & (r < 20)])
    axis_power = np.mean(power[center, :]) + np.mean(power[:, center])

    if ring_10_20 + axis_power > 0:
        spot_measure = ring_10_20 / (ring_10_20 + axis_power)
    else:
        spot_measure = 0.5

    return spot_measure

def run_and_track(U0, V0, f, k, total_steps=100000, check_interval=10000):
    """Run simulation and track pattern evolution."""
    U, V = U0.copy(), V0.copy()
    history = []

    for step_num in range(total_steps):
        U, V = step(U, V, f, k)

        if step_num % check_interval == 0:
            aniso = compute_anisotropy(V)
            spot = compute_spot_measure(V)
            v_mean = np.mean(V)
            v_std = np.std(V)
            history.append({
                'step': step_num,
                'anisotropy': float(aniso),
                'spot_measure': float(spot),
                'v_mean': float(v_mean),
                'v_std': float(v_std)
            })

    return U, V, history

def main():
    print("=" * 60)
    print("BISTABILITY VERIFICATION")
    print("=" * 60)
    print()

    # Test the most promising bistable point
    f, k = 0.030, 0.055
    print(f"Testing f={f}, k={k} with 100k steps each...")
    print()

    # From spots
    print("Running from spot initial conditions...", flush=True)
    U_spot, V_spot = init_spots(N)
    U_spot_final, V_spot_final, history_spot = run_and_track(U_spot, V_spot, f, k)

    print("Running from stripe initial conditions...", flush=True)
    U_stripe, V_stripe = init_stripes(N)
    U_stripe_final, V_stripe_final, history_stripe = run_and_track(U_stripe, V_stripe, f, k)

    print()
    print("=" * 60)
    print("EVOLUTION HISTORY")
    print("=" * 60)
    print()

    print("From SPOTS:")
    print(f"{'Step':>10} {'Anisotropy':>12} {'Spot Measure':>14} {'V mean':>10} {'V std':>10}")
    for h in history_spot:
        print(f"{h['step']:>10} {h['anisotropy']:>12.4f} {h['spot_measure']:>14.4f} {h['v_mean']:>10.4f} {h['v_std']:>10.4f}")

    print()
    print("From STRIPES:")
    print(f"{'Step':>10} {'Anisotropy':>12} {'Spot Measure':>14} {'V mean':>10} {'V std':>10}")
    for h in history_stripe:
        print(f"{h['step']:>10} {h['anisotropy']:>12.4f} {h['spot_measure']:>14.4f} {h['v_mean']:>10.4f} {h['v_std']:>10.4f}")

    print()
    print("=" * 60)
    print("FINAL COMPARISON")
    print("=" * 60)

    final_spot_aniso = history_spot[-1]['anisotropy']
    final_stripe_aniso = history_stripe[-1]['anisotropy']
    final_spot_measure_s = history_spot[-1]['spot_measure']
    final_spot_measure_st = history_stripe[-1]['spot_measure']

    print()
    print(f"From spots:   anisotropy={final_spot_aniso:.4f}, spot_measure={final_spot_measure_s:.4f}")
    print(f"From stripes: anisotropy={final_stripe_aniso:.4f}, spot_measure={final_spot_measure_st:.4f}")
    print()

    # Check if they're different
    aniso_diff = abs(final_spot_aniso - final_stripe_aniso)
    spot_diff = abs(final_spot_measure_s - final_spot_measure_st)

    print(f"Anisotropy difference: {aniso_diff:.4f}")
    print(f"Spot measure difference: {spot_diff:.4f}")
    print()

    if aniso_diff > 0.1 or spot_diff > 0.1:
        print("✓ BISTABILITY CONFIRMED!")
        print("  Different initial conditions lead to persistently different patterns")
        print("  after 100,000 time steps.")
        stable = True
    else:
        print("✗ Patterns CONVERGED")
        print("  Initial conditions don't matter at equilibrium.")
        stable = False

    # Check for stability in last half of simulation
    print()
    print("Stability check (last 50k steps):")
    spot_late = [h for h in history_spot if h['step'] >= 50000]
    stripe_late = [h for h in history_stripe if h['step'] >= 50000]

    if spot_late:
        aniso_var_spot = np.std([h['anisotropy'] for h in spot_late])
        aniso_var_stripe = np.std([h['anisotropy'] for h in stripe_late])
        print(f"  From spots: anisotropy variance = {aniso_var_spot:.6f}")
        print(f"  From stripes: anisotropy variance = {aniso_var_stripe:.6f}")
        if aniso_var_spot < 0.01 and aniso_var_stripe < 0.01:
            print("  Both patterns are STABLE (not still evolving)")

    # Save results
    results = {
        'f': f,
        'k': k,
        'bistable': stable,
        'history_from_spots': history_spot,
        'history_from_stripes': history_stripe,
        'final_comparison': {
            'anisotropy_diff': float(aniso_diff),
            'spot_measure_diff': float(spot_diff)
        }
    }

    with open('bistability_verification.json', 'w') as file:
        json.dump(results, file, indent=2)

    print()
    print("Results saved to bistability_verification.json")

    # Save final patterns for visualization
    np.save('final_V_from_spots.npy', V_spot_final)
    np.save('final_V_from_stripes.npy', V_stripe_final)
    print("Final patterns saved to .npy files")

if __name__ == '__main__':
    main()
