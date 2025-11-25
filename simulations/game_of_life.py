#!/usr/bin/env python3
"""
Conway's Game of Life and Other 2D Cellular Automata

Moving from 1D to 2D opens up much richer possibilities for structure.
The classic Game of Life has well-studied gliders, glider guns, and even
computational constructs.

Key insight I want to explore: How does dimensionality affect emergence?
"""

import random
from typing import List, Tuple, Set


class GameOfLife:
    """
    Conway's Game of Life with arbitrary birth/survival rules.

    Standard Game of Life: B3/S23
    - Birth: Dead cell with exactly 3 neighbors becomes alive
    - Survival: Live cell with 2 or 3 neighbors survives
    """

    def __init__(self, width: int = 40, height: int = 20,
                 birth: Set[int] = {3}, survival: Set[int] = {2, 3}):
        self.width = width
        self.height = height
        self.birth = birth
        self.survival = survival
        self.grid = [[0] * width for _ in range(height)]
        self.history = []

    def randomize(self, density: float = 0.3):
        """Fill grid with random live cells."""
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = 1 if random.random() < density else 0

    def set_pattern(self, pattern: List[Tuple[int, int]], offset: Tuple[int, int] = (0, 0)):
        """Place a pattern on the grid."""
        ox, oy = offset
        for x, y in pattern:
            px, py = (ox + x) % self.width, (oy + y) % self.height
            self.grid[py][px] = 1

    def count_neighbors(self, x: int, y: int) -> int:
        """Count live neighbors (8-connectivity)."""
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = (x + dx) % self.width
                ny = (y + dy) % self.height
                count += self.grid[ny][nx]
        return count

    def step(self):
        """Advance one generation."""
        new_grid = [[0] * self.width for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.count_neighbors(x, y)
                current = self.grid[y][x]

                if current == 1:  # Live cell
                    new_grid[y][x] = 1 if neighbors in self.survival else 0
                else:  # Dead cell
                    new_grid[y][x] = 1 if neighbors in self.birth else 0

        self.grid = new_grid

    def run(self, steps: int = 50):
        """Run for multiple generations, storing history."""
        self.history = [self._copy_grid()]
        for _ in range(steps):
            self.step()
            self.history.append(self._copy_grid())
        return self.history

    def _copy_grid(self) -> List[List[int]]:
        return [row[:] for row in self.grid]

    def visualize(self) -> str:
        """Convert current grid to ASCII."""
        lines = []
        for row in self.grid:
            line = ''.join('#' if cell else '.' for cell in row)
            lines.append(line)
        return '\n'.join(lines)

    def population(self) -> int:
        """Count live cells."""
        return sum(sum(row) for row in self.grid)


# Famous patterns
PATTERNS = {
    'glider': [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)],
    'blinker': [(0, 0), (1, 0), (2, 0)],
    'block': [(0, 0), (1, 0), (0, 1), (1, 1)],
    'beacon': [(0, 0), (1, 0), (0, 1), (3, 2), (2, 3), (3, 3)],
    'toad': [(1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1)],
    'r_pentomino': [(1, 0), (2, 0), (0, 1), (1, 1), (1, 2)],  # Creates chaos!
    'diehard': [(6, 0), (0, 1), (1, 1), (1, 2), (5, 2), (6, 2), (7, 2)],  # Dies after 130 gen
    'acorn': [(1, 0), (3, 1), (0, 2), (1, 2), (4, 2), (5, 2), (6, 2)],  # Explodes, settles ~5200 gen
    'lwss': [(1, 0), (4, 0), (0, 1), (0, 2), (4, 2), (0, 3), (1, 3), (2, 3), (3, 3)],  # Lightweight spaceship
}


def demonstrate_glider():
    """
    Watch a glider move!

    The glider is the simplest spaceship - it translates diagonally
    by (1, 1) every 4 generations while returning to its original shape.
    """
    print("=== GLIDER DEMONSTRATION ===\n")
    print("The glider is the quintessential 'localized structure' I identified.\n")

    life = GameOfLife(width=20, height=10)
    life.set_pattern(PATTERNS['glider'], offset=(1, 1))

    for gen in range(5):
        print(f"Generation {gen * 4}:")
        print(life.visualize())
        print()
        for _ in range(4):
            life.step()

    print("Notice: the glider moved diagonally while preserving its shape!")


def demonstrate_chaos():
    """
    The R-pentomino creates surprising complexity from just 5 cells.
    """
    print("\n=== R-PENTOMINO CHAOS ===\n")
    print("Five cells that create incredible complexity:\n")

    life = GameOfLife(width=50, height=25)
    life.set_pattern(PATTERNS['r_pentomino'], offset=(25, 12))

    checkpoints = [0, 10, 50, 100]
    populations = []

    for gen in range(101):
        if gen in checkpoints:
            print(f"Generation {gen} (population: {life.population()}):")
            print(life.visualize())
            print()
        populations.append(life.population())
        life.step()

    print(f"Population over time: started at 5, max was {max(populations)}")


def explore_rule_space():
    """
    Explore different birth/survival rules (Life-like automata).

    Standard Life is B3/S23. What about other rules?
    """
    print("\n=== EXPLORING RULE SPACE ===\n")

    rules_to_test = [
        ('{3}', '{2,3}', 'Standard Life (B3/S23)'),
        ('{3,6}', '{2,3}', 'HighLife (B36/S23) - has replicators!'),
        ('{3}', '{1,2,3,4,5,6,7,8}', 'B3/S12345678 - very different'),
        ('{3,5,7}', '{2,4,6,8}', 'Custom: odd birth, even survival'),
    ]

    for birth_str, surv_str, name in rules_to_test:
        birth = eval(birth_str)
        survival = eval(surv_str)

        life = GameOfLife(width=30, height=15, birth=birth, survival=survival)
        life.randomize(density=0.3)

        # Run for a bit
        life.run(steps=50)

        print(f"{name}:")
        print(life.visualize())
        print(f"Final population: {life.population()}")
        print()


def measure_structure(life: GameOfLife) -> dict:
    """
    Attempt to measure structural properties of the current state.

    This connects to my earlier insight: what makes complexity
    different from chaos is localized structure.
    """
    metrics = {
        'population': life.population(),
        'density': life.population() / (life.width * life.height),
    }

    # Look for isolated clusters
    visited = set()
    clusters = []

    def flood_fill(x, y):
        if (x, y) in visited or life.grid[y][x] == 0:
            return []
        visited.add((x, y))
        cells = [(x, y)]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = (x + dx) % life.width, (y + dy) % life.height
            cells.extend(flood_fill(nx, ny))
        return cells

    for y in range(life.height):
        for x in range(life.width):
            if (x, y) not in visited and life.grid[y][x] == 1:
                cluster = flood_fill(x, y)
                if cluster:
                    clusters.append(len(cluster))

    metrics['num_clusters'] = len(clusters)
    metrics['avg_cluster_size'] = sum(clusters) / len(clusters) if clusters else 0
    metrics['max_cluster_size'] = max(clusters) if clusters else 0

    return metrics


def investigate_emergence():
    """
    My core question: why does complexity emerge from simple rules?

    In Game of Life:
    - Local rules (8 neighbors, birth/death)
    - Global patterns (gliders, oscillators, still lifes)
    - Computational universality (can build logic gates!)

    Let me measure how structure develops over time from random initial conditions.
    """
    print("\n=== INVESTIGATING EMERGENCE ===\n")
    print("Tracking structure development from random initial state...\n")

    life = GameOfLife(width=60, height=30)
    life.randomize(density=0.3)

    measurements = []
    checkpoints = [0, 5, 20, 50, 100]

    for gen in range(101):
        metrics = measure_structure(life)
        metrics['generation'] = gen
        measurements.append(metrics)

        if gen in checkpoints:
            print(f"Gen {gen}: pop={metrics['population']}, clusters={metrics['num_clusters']}, "
                  f"avg_size={metrics['avg_cluster_size']:.1f}")
            if gen <= 50:
                print(life.visualize())
                print()

        life.step()

    # Analyze trajectory
    initial = measurements[0]
    final = measurements[-1]

    print(f"\nTrajectory analysis:")
    print(f"  Initial: {initial['population']} cells, {initial['num_clusters']} clusters")
    print(f"  Final: {final['population']} cells, {final['num_clusters']} clusters")
    print(f"  Population change: {final['population'] - initial['population']}")
    print(f"  Cluster count change: {final['num_clusters'] - initial['num_clusters']}")

    # Key insight: random soup typically settles to stable + oscillating patterns
    # The number of clusters often decreases (structures merge or die)
    # But some persist! Those survivors are the interesting ones


if __name__ == '__main__':
    demonstrate_glider()
    demonstrate_chaos()
    explore_rule_space()
    investigate_emergence()
