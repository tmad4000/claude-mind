#!/usr/bin/env python3
"""
Particle Tracker for Cellular Automata

The hypothesis: what distinguishes Class IV (complex) from other classes
is the presence of PARTICLES (localized structures) that INTERACT.

This module attempts to:
1. Detect particles (local structures) in CA evolution
2. Track them across time steps
3. Detect and classify interactions (collisions)
4. Use interaction patterns to identify complexity

This is exploratory - I don't know if it will work!
"""

from typing import List, Tuple, Optional, Set
from dataclasses import dataclass
from collections import defaultdict
import sys
sys.path.append('/Users/jacobcole/code/claude-mind')
from simulations.cellular_automata import ElementaryCA


@dataclass
class Particle:
    """A localized structure in the CA."""
    id: int
    time: int
    position: int  # Center of mass
    cells: Set[int]  # Which cells are part of this particle
    size: int

    def overlaps_with(self, other: 'Particle', threshold: int = 3) -> bool:
        """Check if two particles are close enough to potentially interact."""
        return abs(self.position - other.position) <= threshold


def find_particles(row: List[int], min_gap: int = 2) -> List[Tuple[int, Set[int]]]:
    """
    Find localized structures (particles) in a row.

    A particle is a connected group of live cells separated from
    other groups by at least min_gap dead cells.

    Returns list of (center_position, set_of_cell_indices)
    """
    particles = []
    current_particle = set()
    gap_count = 0

    for i, cell in enumerate(row):
        if cell == 1:
            current_particle.add(i)
            gap_count = 0
        else:
            gap_count += 1
            if current_particle and gap_count >= min_gap:
                # End of particle
                center = sum(current_particle) // len(current_particle)
                particles.append((center, current_particle))
                current_particle = set()

    # Don't forget last particle
    if current_particle:
        center = sum(current_particle) // len(current_particle)
        particles.append((center, current_particle))

    return particles


def track_particles(history: List[List[int]], min_gap: int = 2) -> dict:
    """
    Track particles through the CA evolution.

    Returns a dictionary with:
    - particles: dict of particle_id -> list of (time, position, size)
    - births: list of (time, position) when new particles appear
    - deaths: list of (time, position) when particles disappear
    - collisions: list of (time, position, particle_ids_involved)
    """
    particle_id = 0
    active_particles = {}  # id -> last_position
    all_tracks = defaultdict(list)  # id -> [(time, pos, size), ...]

    births = []
    deaths = []
    collisions = []

    prev_particles = []

    for t, row in enumerate(history):
        current_particles = find_particles(row, min_gap)

        if t == 0:
            # Initialize - all particles are births
            for pos, cells in current_particles:
                active_particles[particle_id] = pos
                all_tracks[particle_id].append((t, pos, len(cells)))
                births.append((t, pos))
                particle_id += 1
            prev_particles = [(pid, pos, cells) for (pid, (pos, cells)) in
                             zip(range(particle_id), current_particles)]
            continue

        # Match current particles to previous ones
        # Simple greedy matching by proximity
        matched_current = set()
        matched_prev = set()

        # Sort by size to match larger particles first (more stable)
        current_by_size = sorted(enumerate(current_particles),
                                 key=lambda x: len(x[1][1]), reverse=True)

        for curr_idx, (curr_pos, curr_cells) in current_by_size:
            best_match = None
            best_dist = float('inf')

            for prev_pid, prev_pos, prev_cells in prev_particles:
                if prev_pid in matched_prev:
                    continue
                dist = abs(curr_pos - prev_pos)
                # Allow some movement (gliders!)
                if dist < best_dist and dist <= 3:
                    best_dist = dist
                    best_match = prev_pid

            if best_match is not None:
                matched_current.add(curr_idx)
                matched_prev.add(best_match)
                all_tracks[best_match].append((t, curr_pos, len(curr_cells)))
                active_particles[best_match] = curr_pos
            else:
                # New particle (birth)
                active_particles[particle_id] = curr_pos
                all_tracks[particle_id].append((t, curr_pos, len(curr_cells)))
                births.append((t, curr_pos))
                matched_current.add(curr_idx)
                particle_id += 1

        # Check for deaths
        for prev_pid, prev_pos, prev_cells in prev_particles:
            if prev_pid not in matched_prev:
                deaths.append((t, prev_pos))
                if prev_pid in active_particles:
                    del active_particles[prev_pid]

        # Detect potential collisions (particles that merged)
        # If multiple prev particles map to one current, or vice versa
        # This is a simplification - real collision detection is harder

        # For now, detect when particles get very close
        for i, (pos1, cells1) in enumerate(current_particles):
            for j, (pos2, cells2) in enumerate(current_particles):
                if i < j and abs(pos1 - pos2) <= 4:
                    collisions.append((t, (pos1 + pos2) // 2, 'close_approach'))

        prev_particles = [(pid, pos, cells) for curr_idx, (pos, cells) in enumerate(current_particles)
                         for pid in active_particles if active_particles[pid] == pos]

        # Rebuild prev_particles properly
        prev_particles = []
        for curr_idx, (pos, cells) in enumerate(current_particles):
            for pid, last_pos in active_particles.items():
                if abs(pos - last_pos) <= 1:
                    prev_particles.append((pid, pos, cells))
                    break

    return {
        'tracks': dict(all_tracks),
        'births': births,
        'deaths': deaths,
        'collisions': collisions,
        'total_particles': particle_id,
    }


def compute_particle_metrics(tracking_result: dict, total_time: int) -> dict:
    """
    Compute metrics from particle tracking.

    These metrics should help distinguish complexity!
    """
    tracks = tracking_result['tracks']
    births = tracking_result['births']
    deaths = tracking_result['deaths']

    metrics = {
        'total_particles_created': tracking_result['total_particles'],
        'birth_count': len(births),
        'death_count': len(deaths),
        'close_approaches': len(tracking_result['collisions']),
    }

    if not tracks:
        metrics['avg_lifetime'] = 0
        metrics['max_lifetime'] = 0
        metrics['long_lived_count'] = 0
        return metrics

    # Compute lifetimes
    lifetimes = []
    for pid, track in tracks.items():
        lifetime = track[-1][0] - track[0][0] + 1
        lifetimes.append(lifetime)

    metrics['avg_lifetime'] = sum(lifetimes) / len(lifetimes) if lifetimes else 0
    metrics['max_lifetime'] = max(lifetimes) if lifetimes else 0

    # Long-lived particles (survive > 50% of simulation)
    metrics['long_lived_count'] = sum(1 for l in lifetimes if l > total_time * 0.5)

    # Velocity detection (are particles moving?)
    velocities = []
    for pid, track in tracks.items():
        if len(track) >= 5:
            start_pos = track[0][1]
            end_pos = track[-1][1]
            time_span = track[-1][0] - track[0][0]
            if time_span > 0:
                vel = (end_pos - start_pos) / time_span
                velocities.append(abs(vel))

    metrics['avg_velocity'] = sum(velocities) / len(velocities) if velocities else 0
    metrics['moving_particles'] = sum(1 for v in velocities if v > 0.1)

    return metrics


def analyze_rule(rule_number: int, width: int = 100, steps: int = 100) -> dict:
    """
    Full particle analysis of a CA rule.
    """
    # Single seed
    ca = ElementaryCA(rule_number, width)
    ca.run(steps=steps)

    tracking = track_particles(ca.history)
    metrics = compute_particle_metrics(tracking, steps)

    return {
        'rule': rule_number,
        **metrics
    }


def compare_rules(rules: List[int]):
    """
    Compare particle dynamics across multiple rules.
    """
    print("=" * 70)
    print("PARTICLE DYNAMICS COMPARISON")
    print("=" * 70)
    print()

    results = []
    for rule in rules:
        metrics = analyze_rule(rule, width=100, steps=100)
        results.append(metrics)

        print(f"Rule {rule}:")
        print(f"  Particles created: {metrics['total_particles_created']}")
        print(f"  Births: {metrics['birth_count']}, Deaths: {metrics['death_count']}")
        print(f"  Avg lifetime: {metrics['avg_lifetime']:.1f}")
        print(f"  Max lifetime: {metrics['max_lifetime']}")
        print(f"  Long-lived (>50%): {metrics['long_lived_count']}")
        print(f"  Avg velocity: {metrics['avg_velocity']:.2f}")
        print(f"  Moving particles: {metrics['moving_particles']}")
        print(f"  Close approaches: {metrics['close_approaches']}")
        print()

    return results


def visualize_tracking(rule_number: int, width: int = 60, steps: int = 40):
    """
    Visualize a CA with particle positions marked.
    """
    ca = ElementaryCA(rule_number, width)
    ca.run(steps=steps)

    print(f"\n=== Rule {rule_number} with particle tracking ===\n")

    for t, row in enumerate(ca.history):
        particles = find_particles(row)

        # Create display with particle centers marked
        display = []
        particle_centers = {pos for pos, cells in particles}

        for i, cell in enumerate(row):
            if cell == 1:
                if i in particle_centers:
                    display.append('O')  # Particle center
                else:
                    display.append('#')
            else:
                display.append(' ')

        line = ''.join(display)
        n_particles = len(particles)
        print(f"{line} | {n_particles} particles")


if __name__ == '__main__':
    # Compare known rules with different behaviors
    print("Testing particle tracker on known rules...\n")

    # These should show different particle dynamics:
    # Rule 110: Complex - gliders, interactions
    # Rule 54: Self-similar - structure but no interaction
    # Rule 30: Chaotic - no persistent structure
    # Rule 90: Sierpinski - fractal, no particles
    # Rule 184: Shift - trivial

    test_rules = [110, 54, 30, 90, 184]
    compare_rules(test_rules)

    print("\n" + "=" * 70)
    print("VISUALIZATION OF PARTICLE TRACKING")
    print("=" * 70)

    visualize_tracking(110, width=50, steps=25)
    visualize_tracking(54, width=50, steps=25)
