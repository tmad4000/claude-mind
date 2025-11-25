#!/usr/bin/env python3
"""
Test COMPUTATIONAL CAPABILITY of Gray-Scott patterns.

Can Gray-Scott patterns perform computation? This is a genuinely open question
that connects to:
1. Universal computation in physical systems
2. Chemical computing
3. The boundary between physics and information processing

We test:
1. Pattern collision/interaction rules
2. Signal propagation along channels
3. Logic-like behavior (AND/OR gates via collisions)

If patterns can compute, this would be a MAJOR finding connecting Gray-Scott
to fundamental questions in complexity theory.
"""

import numpy as np
import json

Du, Dv = 0.16, 0.08
N = 128
dx = 1.0

def laplacian(Z, dx):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) +
            np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4*Z) / (dx*dx)

def step(U, V, f, k):
    uvv = U * V * V
    return (np.clip(U + Du * laplacian(U, dx) - uvv + f * (1 - U), 0, 1),
            np.clip(V + Dv * laplacian(V, dx) + uvv - (k + f) * V, 0, 1))

def make_spot(U, V, cx, cy, r=4, amplitude=0.25):
    """Create a single spot at (cx, cy)."""
    y, x = np.ogrid[:N, :N]
    mask = (x-cx)**2 + (y-cy)**2 <= r*r
    U[mask] = 0.5
    V[mask] = amplitude
    return U, V

def make_stripe_channel(U, V, y_start, y_end, x_start, x_end, orientation='horizontal'):
    """Create a stripe channel (path for signal propagation)."""
    if orientation == 'horizontal':
        U[y_start:y_end, x_start:x_end] = 0.5
        V[y_start:y_end, x_start:x_end] = 0.25
    else:
        U[x_start:x_end, y_start:y_end] = 0.5
        V[x_start:x_end, y_start:y_end] = 0.25
    return U, V

def measure_at_region(V, x, y, radius=5):
    """Measure average V in a circular region."""
    yy, xx = np.ogrid[:N, :N]
    mask = (xx-x)**2 + (yy-y)**2 <= radius*radius
    return np.mean(V[mask])

def test_collision_outcome(spot1_pos, spot2_pos, f, k, n_steps=30000):
    """
    Test what happens when two spots collide.
    Returns the outcome: merge, annihilate, reflect, or pass
    """
    U, V = np.ones((N, N)), np.zeros((N, N))

    # Create two spots
    U, V = make_spot(U, V, spot1_pos[0], spot1_pos[1])
    U, V = make_spot(U, V, spot2_pos[0], spot2_pos[1])

    initial_pattern = V.copy()

    # Evolve
    for _ in range(n_steps):
        U, V = step(U, V, f, k)

    if np.std(V) < 0.02:
        return 'annihilate', V

    # Count remaining spots
    threshold = np.mean(V) + 0.5 * np.std(V)
    binary = V > threshold

    # Use simple connected component counting
    labeled = np.zeros_like(binary, dtype=int)
    current_label = 0

    for i in range(N):
        for j in range(N):
            if binary[i, j] and labeled[i, j] == 0:
                current_label += 1
                stack = [(i, j)]
                while stack:
                    ci, cj = stack.pop()
                    if 0 <= ci < N and 0 <= cj < N and binary[ci, cj] and labeled[ci, cj] == 0:
                        labeled[ci, cj] = current_label
                        stack.extend([(ci+1, cj), (ci-1, cj), (ci, cj+1), (ci, cj-1)])

    n_spots = current_label

    if n_spots == 1:
        return 'merge', V
    elif n_spots == 2:
        return 'reflect_or_pass', V
    else:
        return f'complex_{n_spots}', V

def test_signal_propagation(f, k, channel_length=80, n_steps=50000):
    """
    Test if a perturbation can propagate along a stripe channel.
    This tests the most basic requirement for computation: information transfer.
    """
    U, V = np.ones((N, N)), np.zeros((N, N))

    # Create a horizontal stripe channel
    y_center = N // 2
    channel_width = 8
    U, V = make_stripe_channel(U, V,
                               y_center - channel_width//2,
                               y_center + channel_width//2,
                               10, 10 + channel_length)

    # Let the channel stabilize
    for _ in range(10000):
        U, V = step(U, V, f, k)

    if np.std(V) < 0.02:
        return None, 'channel_collapsed'

    # Add a perturbation at the input end
    pulse_x = 15
    U, V = make_spot(U, V, pulse_x, y_center, r=3, amplitude=0.35)

    # Track the position of maximum V over time
    positions = []

    for step_num in range(n_steps):
        U, V = step(U, V, f, k)

        if step_num % 500 == 0:
            # Find position of maximum V along the channel
            channel_slice = V[y_center-2:y_center+3, :].mean(axis=0)
            if np.max(channel_slice) > 0.05:
                max_pos = np.argmax(channel_slice)
                positions.append((step_num, max_pos))

    if len(positions) < 5:
        return None, 'no_propagation'

    # Check if the signal propagated
    x_positions = [p[1] for p in positions]
    if max(x_positions) - min(x_positions) < 10:
        return None, 'signal_stalled'

    # Check velocity and direction
    times = [p[0] for p in positions[-10:]]
    x_vals = [p[1] for p in positions[-10:]]

    if len(times) >= 3:
        velocity = (x_vals[-1] - x_vals[0]) / (times[-1] - times[0]) if times[-1] != times[0] else 0
    else:
        velocity = 0

    return {
        'propagated': velocity > 0,
        'velocity': float(velocity),
        'final_position': int(x_positions[-1]) if x_positions else 0,
        'positions': [(int(t), int(x)) for t, x in positions[-20:]]
    }, 'ok'

def test_and_gate_analog(f, k, n_steps=50000):
    """
    Test if two colliding spots produce an output only when BOTH are present.
    This is an AND gate: output = A AND B

    Setup:
    - Two input regions (left-top and left-bottom)
    - One output region (right)
    - If both inputs active: output active
    - If only one input: no output (or different output)
    """
    results = {}

    # Test all 4 input combinations
    for input_A in [False, True]:
        for input_B in [False, True]:
            U, V = np.ones((N, N)), np.zeros((N, N))

            # Input A: top-left spot
            if input_A:
                U, V = make_spot(U, V, N//4, N//4, r=5, amplitude=0.3)

            # Input B: bottom-left spot
            if input_B:
                U, V = make_spot(U, V, N//4, 3*N//4, r=5, amplitude=0.3)

            # Evolve
            for _ in range(n_steps):
                U, V = step(U, V, f, k)

            # Measure output region (right side)
            output_val = measure_at_region(V, 3*N//4, N//2, radius=10)

            key = f"A{int(input_A)}_B{int(input_B)}"
            results[key] = float(output_val)

    # Check for AND-like behavior:
    # A0_B0 and A0_B1 and A1_B0 should be LOW
    # A1_B1 should be HIGH
    threshold = (results['A0_B0'] + results['A1_B1']) / 2

    is_and_gate = (
        results['A0_B0'] < threshold and
        results['A0_B1'] < threshold and
        results['A1_B0'] < threshold and
        results['A1_B1'] > threshold
    )

    return {
        'truth_table': results,
        'is_and_gate': is_and_gate,
        'threshold': float(threshold)
    }

def main():
    print("=" * 70)
    print("PATTERN COMPUTATION TEST")
    print("=" * 70)
    print()
    print("Can Gray-Scott patterns perform computation?")
    print()

    # Test parameters - use values known to produce stable spots
    f, k = 0.030, 0.057

    print("1. Testing spot collision outcomes...")
    print()

    collision_tests = [
        # Head-on collision
        ((N//3, N//2), (2*N//3, N//2), "head_on"),
        # Perpendicular approach
        ((N//2, N//3), (N//2, 2*N//3), "perpendicular"),
        # Diagonal
        ((N//3, N//3), (2*N//3, 2*N//3), "diagonal"),
        # Close spacing
        ((N//2 - 10, N//2), (N//2 + 10, N//2), "close"),
    ]

    collision_results = []

    print(f"{'Geometry':>15} {'Outcome':>15}")
    print("-" * 35)

    for pos1, pos2, name in collision_tests:
        outcome, V = test_collision_outcome(pos1, pos2, f, k)
        print(f"{name:>15} {outcome:>15}")
        collision_results.append({
            'geometry': name,
            'outcome': outcome,
            'pos1': pos1,
            'pos2': pos2
        })

    print()
    print("2. Testing signal propagation...")
    print()

    prop_result, prop_status = test_signal_propagation(f, k)
    if prop_status == 'ok' and prop_result:
        print(f"Signal propagation: {'YES' if prop_result['propagated'] else 'NO'}")
        print(f"Velocity: {prop_result['velocity']:.6f} px/step")
        print(f"Final position: {prop_result['final_position']} px")
    else:
        print(f"Signal propagation test: {prop_status}")
        prop_result = None

    print()
    print("3. Testing AND gate analog...")
    print()

    and_result = test_and_gate_analog(f, k)
    print("Truth table (output at right region):")
    for key, val in and_result['truth_table'].items():
        print(f"  {key}: {val:.4f}")
    print(f"Behaves like AND gate: {and_result['is_and_gate']}")

    print()
    print("=" * 70)
    print("ANALYSIS")
    print("=" * 70)
    print()

    # Assess computational capability
    print("Computational requirements:")
    print()

    # 1. Information storage
    can_store = any(r['outcome'] not in ['annihilate'] for r in collision_results)
    print(f"1. Information storage (spots persist): {'YES' if can_store else 'NO'}")

    # 2. Information transfer
    can_transfer = prop_result is not None and prop_result.get('propagated', False)
    print(f"2. Information transfer (propagation): {'YES' if can_transfer else 'NO'}")

    # 3. Information processing (logic)
    can_compute = and_result['is_and_gate']
    print(f"3. Information processing (AND gate): {'YES' if can_compute else 'NO'}")

    print()
    if can_store and can_transfer and can_compute:
        print("[POTENTIALLY MAJOR] System shows basic computational elements!")
        print("Further investigation needed for universal computation.")
    elif can_store or can_transfer:
        print("[PARTIAL] Some computational elements present, but not complete.")
    else:
        print("[EXPECTED] Standard pattern behavior without clear computation.")

    # Save results
    with open('computation_results.json', 'w') as file:
        json.dump({
            'collision_tests': collision_results,
            'propagation': {'result': prop_result, 'status': prop_status},
            'and_gate': and_result,
            'summary': {
                'can_store': can_store,
                'can_transfer': can_transfer,
                'can_compute': can_compute
            }
        }, file, indent=2)

    print()
    print("Results saved to computation_results.json")

if __name__ == '__main__':
    main()
