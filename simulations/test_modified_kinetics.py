#!/usr/bin/env python3
"""
Test MODIFIED KINETICS in Gray-Scott-like systems.

Standard Gray-Scott: reaction term is UV²
What happens with different kinetics?

Variations to test:
1. UV³ (cubic autocatalysis)
2. U²V (different stoichiometry)
3. UV²/(1+V) (saturable kinetics)
4. UV²·exp(-V/V0) (substrate inhibition)

These are GENUINELY DIFFERENT SYSTEMS that may exhibit:
- Different pattern types
- Different stability properties
- Novel dynamical behavior

This is exploring CHEMISTRY SPACE, not just parameter space.
"""

import numpy as np
import json

Du, Dv = 0.16, 0.08
N = 64
dx = 1.0

def laplacian(Z, dx):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z) / (dx*dx)

def step_standard(U, V, f, k):
    """Standard Gray-Scott: UV²"""
    uvv = U * V * V
    return (np.clip(U + Du * laplacian(U, dx) - uvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv - (k + f) * V, 0, 1))

def step_cubic(U, V, f, k):
    """Cubic autocatalysis: UV³"""
    uvvv = U * V * V * V
    # Scale f and k to account for different reaction rate
    return (np.clip(U + Du * laplacian(U, dx) - uvvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvvv - (k + f) * V, 0, 1))

def step_u2v(U, V, f, k):
    """Different stoichiometry: U²V"""
    uuv = U * U * V
    return (np.clip(U + Du * laplacian(U, dx) - uuv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uuv - (k + f) * V, 0, 1))

def step_saturable(U, V, f, k, Km=0.5):
    """Saturable kinetics: UV²/(1+V/Km)"""
    uvv_sat = U * V * V / (1 + V / Km)
    return (np.clip(U + Du * laplacian(U, dx) - uvv_sat + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv_sat - (k + f) * V, 0, 1))

def step_inhibited(U, V, f, k, Ki=0.3):
    """Substrate inhibition: UV²·exp(-V/Ki)"""
    uvv_inh = U * V * V * np.exp(-V / Ki)
    return (np.clip(U + Du * laplacian(U, dx) - uvv_inh + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv_inh - (k + f) * V, 0, 1))

def init_nucleated(N, seed=42):
    np.random.seed(seed)
    U, V = np.ones((N, N)), np.zeros((N, N))
    for _ in range(8):
        cx, cy = np.random.randint(N//4, 3*N//4, 2)
        r = 4
        y, x = np.ogrid[:N, :N]
        mask = (x-cx)**2 + (y-cy)**2 <= r*r
        U[mask], V[mask] = 0.5, 0.25
    return U, V

def classify_pattern(V):
    """Classify pattern type."""
    v_std = np.std(V)
    if v_std < 0.02:
        return 'uniform', {}

    v_mean = np.mean(V)

    # FFT analysis
    V_centered = V - v_mean
    fft = np.fft.fft2(V_centered)
    power = np.abs(np.fft.fftshift(fft))**2

    center = N // 2
    power[center-2:center+3, center-2:center+3] = 0

    # Anisotropy
    horiz_power = np.sum(power[center-3:center+4, :])
    vert_power = np.sum(power[:, center-3:center+4])
    total_power = np.sum(power)

    anisotropy = abs(horiz_power - vert_power) / (total_power + 1e-10)

    # Find dominant wavelength
    y, x = np.ogrid[:N, :N]
    r = np.sqrt((x - center)**2 + (y - center)**2)
    r = r.astype(int)
    radial_power = np.bincount(r.ravel(), weights=power.ravel())
    radial_counts = np.bincount(r.ravel())
    radial_avg = radial_power / (radial_counts + 1e-10)

    peak_k = np.argmax(radial_avg[1:N//3]) + 1
    wavelength = N / peak_k if peak_k > 0 else N

    if anisotropy > 0.3:
        pattern_type = 'stripes'
    else:
        pattern_type = 'spots'

    return pattern_type, {
        'v_std': float(v_std),
        'v_mean': float(v_mean),
        'anisotropy': float(anisotropy),
        'wavelength': float(wavelength)
    }

def run_kinetics_test(step_func, kinetics_name, f, k, n_steps=40000):
    """Run simulation with specific kinetics."""
    U, V = init_nucleated(N)

    for _ in range(n_steps):
        U, V = step_func(U, V, f, k)

    pattern_type, metrics = classify_pattern(V)

    if pattern_type == 'uniform':
        return None, 'no_pattern'

    return {
        'kinetics': kinetics_name,
        'f': float(f),
        'k': float(k),
        'pattern_type': pattern_type,
        **metrics
    }, 'ok'

def main():
    print("=" * 70)
    print("MODIFIED KINETICS IN GRAY-SCOTT-LIKE SYSTEMS")
    print("=" * 70)
    print()
    print("Testing different reaction kinetics...")
    print("  Standard: UV²")
    print("  Cubic: UV³")
    print("  U²V: Different stoichiometry")
    print("  Saturable: UV²/(1+V/Km)")
    print("  Inhibited: UV²·exp(-V/Ki)")
    print()

    kinetics_funcs = [
        (step_standard, 'UV2_standard'),
        (step_cubic, 'UV3_cubic'),
        (step_u2v, 'U2V_stoich'),
        (step_saturable, 'saturable'),
        (step_inhibited, 'inhibited'),
    ]

    # Test across parameter range - expand for cubic (needs higher k)
    test_params = [
        (0.030, 0.057),
        (0.035, 0.060),
        (0.040, 0.063),
        (0.045, 0.065),
        # Extended range for different kinetics
        (0.030, 0.045),
        (0.035, 0.050),
        (0.025, 0.055),
    ]

    results = []

    print(f"{'kinetics':>15} {'f':>6} {'k':>6} {'type':>10} {'wavelen':>8} {'aniso':>8}")
    print("-" * 60)

    for step_func, kinetics_name in kinetics_funcs:
        for f, k in test_params:
            result, status = run_kinetics_test(step_func, kinetics_name, f, k)

            if status == 'ok':
                ptype = result['pattern_type']
                wlen = result['wavelength']
                aniso = result['anisotropy']
                print(f"{kinetics_name:>15} {f:6.3f} {k:6.3f} {ptype:>10} {wlen:8.2f} {aniso:8.4f}")
                results.append(result)
            else:
                print(f"{kinetics_name:>15} {f:6.3f} {k:6.3f} {'N/A':>10} {'N/A':>8} {'N/A':>8}")

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    if len(results) < 3:
        print("Not enough results for analysis")
        return

    # Compare pattern-forming ability across kinetics
    print("Pattern formation by kinetics:")
    for step_func, kinetics_name in kinetics_funcs:
        k_results = [r for r in results if r['kinetics'] == kinetics_name]
        n_patterns = len(k_results)
        total_tested = len(test_params)
        print(f"  {kinetics_name}: {n_patterns}/{total_tested} parameters form patterns")
        if k_results:
            wavelengths = [r['wavelength'] for r in k_results]
            print(f"    Mean wavelength: {np.mean(wavelengths):.2f} px")
    print()

    # Look for differences in pattern properties
    print("Wavelength comparison:")
    standard_results = [r for r in results if r['kinetics'] == 'UV2_standard']
    if standard_results:
        standard_wlen = np.mean([r['wavelength'] for r in standard_results])
        print(f"  Standard (UV²): {standard_wlen:.2f} px")

        for step_func, kinetics_name in kinetics_funcs[1:]:
            k_results = [r for r in results if r['kinetics'] == kinetics_name]
            if k_results:
                mod_wlen = np.mean([r['wavelength'] for r in k_results])
                ratio = mod_wlen / standard_wlen
                print(f"  {kinetics_name}: {mod_wlen:.2f} px (ratio: {ratio:.2f})")

                if abs(ratio - 1) > 0.2:
                    print(f"    [INTERESTING] Significant wavelength difference!")
    print()

    # Look for novel pattern types
    print("NOVELTY ASSESSMENT:")
    print()

    # Check if any kinetics produces patterns where standard doesn't
    standard_params = set((r['f'], r['k']) for r in results if r['kinetics'] == 'UV2_standard')
    for step_func, kinetics_name in kinetics_funcs[1:]:
        k_params = set((r['f'], r['k']) for r in results if r['kinetics'] == kinetics_name)
        novel_params = k_params - standard_params

        if novel_params:
            print(f"[POTENTIALLY NOVEL] {kinetics_name} forms patterns at parameters where standard doesn't:")
            for p in novel_params:
                print(f"  f={p[0]}, k={p[1]}")

    # Check for different pattern types at same parameters
    print()
    for f, k in test_params:
        param_results = [r for r in results if r['f'] == f and r['k'] == k]
        if len(param_results) >= 2:
            types = set(r['pattern_type'] for r in param_results)
            if len(types) > 1:
                print(f"[INTERESTING] Different kinetics produce different pattern types at f={f}, k={k}")
                for r in param_results:
                    print(f"  {r['kinetics']}: {r['pattern_type']}")

    # Save results
    with open('modified_kinetics_results.json', 'w') as file:
        json.dump({
            'results': results,
            'summary': {
                'n_results': len(results),
                'kinetics_tested': [name for _, name in kinetics_funcs]
            }
        }, file, indent=2)

    print()
    print("Results saved to modified_kinetics_results.json")

if __name__ == '__main__':
    main()
