#!/usr/bin/env python3
"""
Reaction-Diffusion System Explorer

The Gray-Scott model:
  ∂U/∂t = Du∇²U - UV² + f(1-U)
  ∂V/∂t = Dv∇²V + UV² - (k+f)V

Where:
  U, V = chemical concentrations
  Du, Dv = diffusion rates
  f = feed rate (how fast U is added)
  k = kill rate (how fast V dies)

The parameter space (f, k) is RICH - different regions produce
different patterns: spots, stripes, spirals, chaos, extinction.

I want to map this space and find the boundaries between regimes.
"""

import numpy as np
from typing import Tuple, List
import json
from pathlib import Path


class GrayScott:
    """Gray-Scott reaction-diffusion system."""

    def __init__(self, size: int = 100, f: float = 0.055, k: float = 0.062,
                 Du: float = 0.21, Dv: float = 0.105):
        self.size = size
        self.f = f
        self.k = k
        self.Du = Du
        self.Dv = Dv

        # Initialize grids
        self.U = np.ones((size, size))
        self.V = np.zeros((size, size))

    def seed_center(self, radius: int = 10):
        """Add V chemical in center."""
        cx, cy = self.size // 2, self.size // 2
        y, x = np.ogrid[:self.size, :self.size]
        mask = (x - cx)**2 + (y - cy)**2 < radius**2
        self.V[mask] = 1.0

    def seed_random(self, n_seeds: int = 20, radius: int = 3):
        """Add random seeds of V."""
        for _ in range(n_seeds):
            cx = np.random.randint(0, self.size)
            cy = np.random.randint(0, self.size)
            y, x = np.ogrid[:self.size, :self.size]
            mask = (x - cx)**2 + (y - cy)**2 < radius**2
            self.V[mask] = 1.0

    def laplacian(self, grid: np.ndarray) -> np.ndarray:
        """Compute discrete Laplacian with periodic boundaries."""
        return (
            np.roll(grid, 1, axis=0) +
            np.roll(grid, -1, axis=0) +
            np.roll(grid, 1, axis=1) +
            np.roll(grid, -1, axis=1) -
            4 * grid
        )

    def step(self, dt: float = 1.0):
        """Advance one time step."""
        lap_U = self.laplacian(self.U)
        lap_V = self.laplacian(self.V)

        uvv = self.U * self.V * self.V

        self.U += dt * (self.Du * lap_U - uvv + self.f * (1 - self.U))
        self.V += dt * (self.Dv * lap_V + uvv - (self.k + self.f) * self.V)

        # Clamp to [0, 1]
        np.clip(self.U, 0, 1, out=self.U)
        np.clip(self.V, 0, 1, out=self.V)

    def run(self, steps: int = 1000) -> np.ndarray:
        """Run simulation and return final V field."""
        for _ in range(steps):
            self.step()
        return self.V.copy()

    def estimate_wavelength(self) -> float:
        """Estimate dominant wavelength using autocorrelation."""
        v = self.V
        # Use center row for speed
        row = v[self.size // 2, :]
        row = row - row.mean()

        if row.std() < 0.01:
            return float('inf')  # No variation

        # Autocorrelation
        autocorr = np.correlate(row, row, mode='full')
        autocorr = autocorr[len(autocorr)//2:]  # Take positive lags
        autocorr = autocorr / autocorr[0]  # Normalize

        # Find first minimum then first maximum after that
        # This gives us the half-wavelength
        for i in range(1, len(autocorr) - 1):
            if autocorr[i] < autocorr[i-1] and autocorr[i] < autocorr[i+1]:
                # Found minimum, now look for next max
                for j in range(i+1, len(autocorr) - 1):
                    if autocorr[j] > autocorr[j-1] and autocorr[j] > autocorr[j+1]:
                        return float(j)  # This is approximately the wavelength
                break

        # Fallback: count zero crossings
        threshold = (row.max() + row.min()) / 2
        binary = row > threshold
        crossings = np.sum(np.abs(np.diff(binary.astype(int))))
        if crossings > 0:
            return float(self.size / crossings)

        return float('inf')

    def analyze(self) -> dict:
        """Analyze current state."""
        v = self.V

        metrics = {
            'mean_v': float(np.mean(v)),
            'std_v': float(np.std(v)),
            'max_v': float(np.max(v)),
            'coverage': float(np.mean(v > 0.1)),  # Fraction with significant V
        }

        # Estimate wavelength to detect numerical artifacts
        wavelength = self.estimate_wavelength()
        metrics['wavelength'] = wavelength

        # Pattern detection heuristics
        if metrics['mean_v'] < 0.01:
            metrics['pattern'] = 'extinction'
        elif metrics['std_v'] < 0.05:
            metrics['pattern'] = 'uniform'
        elif wavelength < 3:
            # Grid-scale pattern = numerical artifact
            metrics['pattern'] = 'artifact'
        elif metrics['coverage'] > 0.8 and wavelength > 10:
            metrics['pattern'] = 'filled'
        else:
            metrics['pattern'] = 'structured'

        return metrics


def explore_parameter_space(f_range: Tuple[float, float] = (0.01, 0.08),
                            k_range: Tuple[float, float] = (0.03, 0.07),
                            resolution: int = 20,
                            steps: int = 2000) -> dict:
    """
    Map the (f, k) parameter space.

    This is where the interesting science is - finding the boundaries
    between different pattern regimes.
    """
    f_values = np.linspace(f_range[0], f_range[1], resolution)
    k_values = np.linspace(k_range[0], k_range[1], resolution)

    results = {
        'f_values': f_values.tolist(),
        'k_values': k_values.tolist(),
        'patterns': [],
        'metrics': []
    }

    total = resolution * resolution
    done = 0

    for i, f in enumerate(f_values):
        row_patterns = []
        row_metrics = []
        for j, k in enumerate(k_values):
            gs = GrayScott(size=50, f=f, k=k)
            gs.seed_center(radius=5)
            gs.run(steps=steps)
            metrics = gs.analyze()

            row_patterns.append(metrics['pattern'])
            row_metrics.append(metrics)

            done += 1
            if done % 50 == 0:
                print(f"Progress: {done}/{total} ({100*done/total:.0f}%)")

        results['patterns'].append(row_patterns)
        results['metrics'].append(row_metrics)

    return results


def find_phase_boundaries(results: dict) -> List[dict]:
    """
    Find parameter values where pattern type changes.

    These boundaries are the "interesting" regions - where the system
    is poised between different behaviors.
    """
    patterns = results['patterns']
    f_values = results['f_values']
    k_values = results['k_values']

    boundaries = []

    for i in range(len(f_values) - 1):
        for j in range(len(k_values) - 1):
            current = patterns[i][j]
            right = patterns[i+1][j]
            down = patterns[i][j+1]

            if current != right:
                boundaries.append({
                    'f': (f_values[i] + f_values[i+1]) / 2,
                    'k': k_values[j],
                    'transition': f'{current} -> {right}',
                    'direction': 'horizontal'
                })

            if current != down:
                boundaries.append({
                    'f': f_values[i],
                    'k': (k_values[j] + k_values[j+1]) / 2,
                    'transition': f'{current} -> {down}',
                    'direction': 'vertical'
                })

    return boundaries


def visualize_ascii(gs: GrayScott, width: int = 60) -> str:
    """Create ASCII visualization of the V field."""
    v = gs.V

    # Downsample if needed
    if gs.size > width:
        factor = gs.size // width
        v = v[::factor, ::factor]

    chars = ' .:-=+*#%@'
    lines = []
    for row in v:
        line = ''
        for val in row:
            idx = int(val * (len(chars) - 1))
            line += chars[idx]
        lines.append(line)

    return '\n'.join(lines)


# Known interesting parameter combinations
KNOWN_PATTERNS = {
    'mitosis': (0.0367, 0.0649),  # Cell-like division
    'coral': (0.0545, 0.062),      # Coral-like growth
    'spirals': (0.018, 0.051),     # Rotating spirals
    'spots': (0.03, 0.06),         # Leopard spots
    'stripes': (0.04, 0.06),       # Zebra stripes
    'maze': (0.029, 0.057),        # Labyrinthine patterns
    'waves': (0.014, 0.045),       # Traveling waves
    'chaos': (0.026, 0.051),       # Chaotic turbulence
    'solitons': (0.03, 0.055),     # Stable moving blobs
}


if __name__ == '__main__':
    print("=== REACTION-DIFFUSION EXPLORER ===\n")

    # Show a few known patterns
    print("Known patterns from literature:\n")
    for name, (f, k) in list(KNOWN_PATTERNS.items())[:4]:
        print(f"--- {name.upper()} (f={f}, k={k}) ---")
        gs = GrayScott(size=60, f=f, k=k)
        gs.seed_center(radius=8)
        gs.run(steps=3000)
        metrics = gs.analyze()
        print(f"Coverage: {metrics['coverage']:.1%}, Pattern: {metrics['pattern']}")
        print(visualize_ascii(gs))
        print()

    # Quick parameter space exploration
    print("\n=== EXPLORING PARAMETER SPACE ===\n")
    print("Mapping (f, k) space to find pattern boundaries...")
    print("This is where complexity lives!\n")

    results = explore_parameter_space(resolution=10, steps=1500)

    print("\nPattern map (f increases right, k increases down):")
    pattern_chars = {'extinction': '.', 'uniform': 'U', 'filled': 'F', 'structured': 'S'}
    for row in results['patterns']:
        print('  ' + ''.join(pattern_chars.get(p, '?') for p in row))

    boundaries = find_phase_boundaries(results)
    print(f"\nFound {len(boundaries)} boundary points")
    print("These are the 'edge of chaos' regions where interesting patterns emerge!")
