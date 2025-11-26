#!/usr/bin/env python3
"""
RD Diagnostic - Check what patterns are actually forming
"""

import numpy as np
import json

def laplacian(a):
    return (
        np.roll(a, 1, axis=0) + np.roll(a, -1, axis=0) +
        np.roll(a, 1, axis=1) + np.roll(a, -1, axis=1) -
        4 * a
    )

def simulate_gray_scott(f, k, steps=10000, size=100, Du=0.16, Dv=0.08, dt=1.0):
    """Run Gray-Scott simulation with progress."""
    u = np.ones((size, size))
    v = np.zeros((size, size))

    # Add seed
    r = 15
    cx, cy = size // 2, size // 2
    u[cx-r:cx+r, cy-r:cy+r] = 0.5
    v[cx-r:cx+r, cy-r:cy+r] = 0.25
    u += 0.05 * np.random.random((size, size))
    v += 0.05 * np.random.random((size, size))

    for i in range(steps):
        uvv = u * v * v
        Lu = laplacian(u)
        Lv = laplacian(v)
        u += dt * (Du * Lu - uvv + f * (1 - u))
        v += dt * (Dv * Lv + uvv - (f + k) * v)
        u = np.clip(u, 0, 1)
        v = np.clip(v, 0, 1)

    return u, v

# Test different points
points = [
    {"name": "mitosis", "f": 0.026, "k": 0.051},
    {"name": "solitons", "f": 0.042, "k": 0.063},
    {"name": "coral", "f": 0.062, "k": 0.063},
]

print("RD Pattern Diagnostic")
print("=" * 60)

for p in points:
    print(f"\nTesting {p['name']} (f={p['f']}, k={p['k']})...")
    u, v = simulate_gray_scott(p['f'], p['k'], steps=10000)

    print(f"  v stats: min={v.min():.4f}, max={v.max():.4f}, mean={v.mean():.4f}, std={v.std():.4f}")
    print(f"  u stats: min={u.min():.4f}, max={u.max():.4f}, mean={u.mean():.4f}, std={u.std():.4f}")

    # Check if pattern formed
    v_range = v.max() - v.min()
    if v_range < 0.01:
        print(f"  Pattern status: UNIFORM (no pattern formed)")
    elif v.std() < 0.05:
        print(f"  Pattern status: WEAK PATTERN")
    else:
        print(f"  Pattern status: PATTERN FORMED")

    # Show a slice of the pattern
    mid = 50
    row = v[mid, :]
    print(f"  Middle row sample (0-20): {' '.join([f'{x:.2f}' for x in row[:20]])}")
