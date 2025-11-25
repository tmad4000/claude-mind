#!/usr/bin/env python3
"""
INTERACTIVE PATTERN PLAYGROUND

Run this and play with Gray-Scott parameters!

Usage:
    python3 play_patterns.py              # Use defaults (pretty stripes)
    python3 play_patterns.py 0.035 0.060  # Custom f and k
    python3 play_patterns.py --spots      # Preset: spots
    python3 play_patterns.py --chaos      # Preset: chaotic
    python3 play_patterns.py --labyrinth  # Preset: labyrinths
    python3 play_patterns.py --ca 90      # Cellular automaton rule 90

Controls (when running):
    - Watch it evolve in real-time
    - Close window to stop
    - Output saved as output.png
"""

import sys
import numpy as np

# Check for matplotlib
try:
    import matplotlib
    matplotlib.use('TkAgg')  # Interactive backend
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("matplotlib not found - will save static image instead")

from scipy.ndimage import laplace

# Presets
PRESETS = {
    'spots': (0.034, 0.057),
    'stripes': (0.040, 0.063),
    'labyrinth': (0.040, 0.064),
    'chaos': (0.025, 0.053),
    'mixed': (0.035, 0.060),
    'mitosis': (0.030, 0.060),
    'worms': (0.050, 0.065),
}

def run_gray_scott(f=0.035, k=0.060, N=200, steps=10000, animate=True):
    """Run Gray-Scott and optionally animate."""
    Du, Dv, dt = 0.16, 0.08, 1.0

    U = np.ones((N, N))
    V = np.zeros((N, N))

    # Seed
    r = 15
    V[N//2-r:N//2+r, N//2-r:N//2+r] = 0.25
    U[N//2-r:N//2+r, N//2-r:N//2+r] = 0.5

    # Add some random noise for variety
    V += 0.01 * np.random.random((N, N))

    print(f"Running Gray-Scott: f={f}, k={k}")
    print(f"Expected pattern: ", end="")

    # Predict pattern type
    if k > 0.065:
        print("uniform (k too high)")
    elif f > 0.045 and k < 0.055:
        print("uniform (f too high for low k)")
    elif f < 0.025:
        print("chaos/turbulent")
    elif k > 0.062:
        print("stripes/labyrinth")
    elif k < 0.060:
        print("spots or mixed")
    else:
        print("mixed spots/stripes")

    if animate and HAS_MATPLOTLIB:
        fig, ax = plt.subplots(figsize=(8, 8))
        im = ax.imshow(V, cmap='magma', vmin=0, vmax=0.4)
        ax.set_title(f'Gray-Scott: f={f}, k={k}\nStep: 0')
        ax.axis('off')

        def update(frame):
            nonlocal U, V
            for _ in range(50):  # 50 steps per frame
                uvv = U * V * V
                U += dt * (Du * laplace(U, mode='wrap') - uvv + f * (1 - U))
                V += dt * (Dv * laplace(V, mode='wrap') + uvv - (f + k) * V)
                U = np.clip(U, 0, 1)
                V = np.clip(V, 0, 1)

            im.set_array(V)
            ax.set_title(f'Gray-Scott: f={f}, k={k}\nStep: {frame * 50}')
            return [im]

        ani = FuncAnimation(fig, update, frames=steps//50, interval=50, blit=True)
        plt.show()

        # Save final state
        plt.figure(figsize=(8, 8))
        plt.imshow(V, cmap='magma', vmin=0, vmax=0.4)
        plt.axis('off')
        plt.savefig('output.png', dpi=150, bbox_inches='tight', pad_inches=0)
        print("Saved: output.png")
    else:
        # No animation - just run and save
        for step in range(steps):
            uvv = U * V * V
            U += dt * (Du * laplace(U, mode='wrap') - uvv + f * (1 - U))
            V += dt * (Dv * laplace(V, mode='wrap') + uvv - (f + k) * V)
            U = np.clip(U, 0, 1)
            V = np.clip(V, 0, 1)

            if step % 1000 == 0:
                print(f"  Step {step}/{steps}")

        if HAS_MATPLOTLIB:
            plt.figure(figsize=(8, 8))
            plt.imshow(V, cmap='magma', vmin=0, vmax=0.4)
            plt.axis('off')
            plt.savefig('output.png', dpi=150, bbox_inches='tight', pad_inches=0)
            print("Saved: output.png")
        else:
            np.save('output.npy', V)
            print("Saved: output.npy (numpy array)")

    return V

def run_ca(rule=90, width=401, steps=200):
    """Run 1D cellular automaton."""
    print(f"Running CA Rule {rule}")

    table = [(rule >> i) & 1 for i in range(8)]
    state = np.zeros(width, dtype=int)
    state[width // 2] = 1

    history = [state.copy()]
    for _ in range(steps):
        new = np.zeros(width, dtype=int)
        for i in range(width):
            idx = state[(i-1)%width]*4 + state[i]*2 + state[(i+1)%width]
            new[i] = table[idx]
        state = new
        history.append(state.copy())

    history = np.array(history)

    if HAS_MATPLOTLIB:
        plt.figure(figsize=(12, 8))
        plt.imshow(history, cmap='binary', aspect='auto')
        plt.title(f'Rule {rule}')
        plt.xlabel('Cell')
        plt.ylabel('Time')
        plt.savefig('output_ca.png', dpi=150, bbox_inches='tight')
        plt.show()
        print("Saved: output_ca.png")
    else:
        np.save('output_ca.npy', history)
        print("Saved: output_ca.npy")

    return history

if __name__ == '__main__':
    args = sys.argv[1:]

    # Check for CA mode
    if '--ca' in args:
        idx = args.index('--ca')
        rule = int(args[idx + 1]) if idx + 1 < len(args) else 90
        run_ca(rule)
        sys.exit(0)

    # Check for presets
    for preset, (f, k) in PRESETS.items():
        if f'--{preset}' in args:
            run_gray_scott(f, k)
            sys.exit(0)

    # Check for custom parameters
    if len(args) >= 2:
        try:
            f = float(args[0])
            k = float(args[1])
            run_gray_scott(f, k)
            sys.exit(0)
        except ValueError:
            pass

    # Default
    if args and args[0] == '--help':
        print(__doc__)
    else:
        print("No parameters given, using default (mixed spots/stripes)")
        print("Try: python3 play_patterns.py --spots")
        print("     python3 play_patterns.py --chaos")
        print("     python3 play_patterns.py 0.030 0.057")
        print("     python3 play_patterns.py --ca 110")
        print()
        run_gray_scott(0.035, 0.060)
