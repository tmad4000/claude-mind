#!/usr/bin/env python3
"""
Deep investigation of Class III rules that are periodic.

These might be misclassifications by Wolfram, or they might represent
an interesting intermediate category.

Rules to investigate: 22, 73, 129, 161, 181, 182

Author: Claude (overnight session 3)
Date: 2025-11-27
"""

import numpy as np
# matplotlib removed - using text-based output only

# The outliers - Class III rules that are 100% periodic
OUTLIERS = [22, 73, 129, 161, 181, 182]

# Truly chaotic Class III for comparison
TRULY_CHAOTIC = [30, 45, 75, 86, 89, 101, 106, 120, 135, 149, 169, 225]

# Class IV for comparison
CLASS_IV = [110, 124, 137, 193]

def apply_rule(cells, rule_num):
    """Apply ECA rule to cell array."""
    rule_bits = [(rule_num >> i) & 1 for i in range(8)]
    n = len(cells)
    new_cells = np.zeros_like(cells)
    for i in range(n):
        left = cells[(i-1) % n]
        center = cells[i]
        right = cells[(i+1) % n]
        idx = (left << 2) | (center << 1) | right
        new_cells[i] = rule_bits[idx]
    return new_cells

def generate_spacetime(rule_num, width=100, steps=200, seed=42):
    """Generate spacetime diagram."""
    np.random.seed(seed)
    cells = np.random.randint(0, 2, width)
    history = [cells.copy()]

    for _ in range(steps):
        cells = apply_rule(cells, rule_num)
        history.append(cells.copy())

    return np.array(history)

def analyze_gliders(spacetime):
    """
    Look for glider-like structures (traveling patterns).
    Returns number of diagonal structures detected.
    """
    # Simple diagonal correlation analysis
    rows, cols = spacetime.shape
    diagonal_score = 0

    for offset in [-3, -2, -1, 1, 2, 3]:  # Check various diagonal offsets
        match_count = 0
        for t in range(rows - abs(offset)):
            for x in range(cols - abs(offset)):
                if offset > 0:
                    if spacetime[t, x] == spacetime[t + offset, (x + offset) % cols]:
                        match_count += 1
                else:
                    if spacetime[t, x] == spacetime[t - offset, (x + offset) % cols]:
                        match_count += 1

        diagonal_score += match_count / ((rows - abs(offset)) * (cols - abs(offset)))

    return diagonal_score / 6  # Normalize

def measure_block_entropy(spacetime, block_size=3):
    """Measure entropy of block patterns."""
    rows, cols = spacetime.shape
    patterns = {}

    for t in range(rows - block_size + 1):
        for x in range(cols - block_size + 1):
            block = tuple(spacetime[t:t+block_size, x:x+block_size].flatten())
            patterns[block] = patterns.get(block, 0) + 1

    total = sum(patterns.values())
    probs = [c / total for c in patterns.values()]
    entropy = -sum(p * np.log2(p) for p in probs if p > 0)

    # Normalize by max possible entropy
    max_entropy = block_size * block_size  # bits
    return entropy / max_entropy

def analyze_damage_spreading(rule_num, width=100, steps=200):
    """Measure how fast perturbations spread (Lyapunov-like)."""
    np.random.seed(42)
    cells1 = np.random.randint(0, 2, width)
    cells2 = cells1.copy()

    # Flip one bit
    cells2[width // 2] = 1 - cells2[width // 2]

    damages = []
    for _ in range(steps):
        cells1 = apply_rule(cells1, rule_num)
        cells2 = apply_rule(cells2, rule_num)
        damage = np.sum(cells1 != cells2) / width
        damages.append(damage)

    # Measure growth rate in early steps
    early_damages = damages[:50]
    if early_damages[-1] > early_damages[0]:
        # Fit exponential growth
        growth_rate = np.log(early_damages[-1] / max(early_damages[0], 0.01)) / 50
    else:
        growth_rate = 0

    return np.mean(damages[-50:]), growth_rate, damages

def find_cycle_and_period(rule_num, width, max_steps=20000, seed=42):
    """Find cycle and return period, transient, and attractor size estimate."""
    np.random.seed(seed + rule_num)
    cells = np.random.randint(0, 2, width)
    seen_states = {}

    for step in range(max_steps):
        state_key = hash(tuple(cells.tolist()))
        if state_key in seen_states:
            return True, seen_states[state_key], step - seen_states[state_key]
        seen_states[state_key] = step
        cells = apply_rule(cells, rule_num)

    return False, max_steps, None

def main():
    print("=" * 70)
    print("DEEP INVESTIGATION: CLASS III OUTLIERS (PERIODIC)")
    print("=" * 70)
    print()
    print("These rules are classified as Class III (chaotic) by Wolfram,")
    print("but our periodicity test shows they always find cycles.")
    print()
    print("Hypothesis: These might be misclassified or represent an")
    print("intermediate category between Class III and Class IV.")
    print()

    # Detailed analysis of each outlier
    print("=" * 70)
    print("DETAILED ANALYSIS OF OUTLIERS")
    print("=" * 70)

    outlier_data = []
    for rule in OUTLIERS:
        print(f"\n--- Rule {rule} ---")

        # Generate spacetime
        spacetime = generate_spacetime(rule, width=100, steps=200)

        # Glider analysis
        glider_score = analyze_gliders(spacetime)
        print(f"  Glider score (diagonal correlation): {glider_score:.3f}")

        # Block entropy
        block_entropy = measure_block_entropy(spacetime)
        print(f"  Block entropy (normalized): {block_entropy:.3f}")

        # Damage spreading
        final_damage, growth_rate, damages = analyze_damage_spreading(rule)
        print(f"  Final damage spread: {final_damage:.3f}")
        print(f"  Damage growth rate: {growth_rate:.3f}")

        # Periodicity details
        found, trans, period = find_cycle_and_period(rule, 47, max_steps=30000)
        if found:
            print(f"  Cycle found: transient={trans}, period={period}")
        else:
            print(f"  No cycle found in 30000 steps")

        outlier_data.append({
            'rule': rule,
            'glider_score': glider_score,
            'block_entropy': block_entropy,
            'final_damage': final_damage,
            'growth_rate': growth_rate,
            'period': period
        })

    # Compare with truly chaotic
    print("\n" + "=" * 70)
    print("COMPARISON WITH TRULY CHAOTIC (Class III)")
    print("=" * 70)

    chaotic_data = []
    for rule in TRULY_CHAOTIC[:6]:  # Test first 6
        spacetime = generate_spacetime(rule, width=100, steps=200)
        glider_score = analyze_gliders(spacetime)
        block_entropy = measure_block_entropy(spacetime)
        final_damage, growth_rate, _ = analyze_damage_spreading(rule)
        found, trans, period = find_cycle_and_period(rule, 47, max_steps=30000)

        chaotic_data.append({
            'rule': rule,
            'glider_score': glider_score,
            'block_entropy': block_entropy,
            'final_damage': final_damage,
            'growth_rate': growth_rate,
            'period': period
        })

        print(f"  Rule {rule}: glider={glider_score:.3f}, entropy={block_entropy:.3f}, damage={final_damage:.3f}, period={period}")

    # Compare with Class IV
    print("\n" + "=" * 70)
    print("COMPARISON WITH CLASS IV (Complex)")
    print("=" * 70)

    class4_data = []
    for rule in CLASS_IV:
        spacetime = generate_spacetime(rule, width=100, steps=200)
        glider_score = analyze_gliders(spacetime)
        block_entropy = measure_block_entropy(spacetime)
        final_damage, growth_rate, _ = analyze_damage_spreading(rule)
        found, trans, period = find_cycle_and_period(rule, 47, max_steps=30000)

        class4_data.append({
            'rule': rule,
            'glider_score': glider_score,
            'block_entropy': block_entropy,
            'final_damage': final_damage,
            'growth_rate': growth_rate,
            'period': period
        })

        print(f"  Rule {rule}: glider={glider_score:.3f}, entropy={block_entropy:.3f}, damage={final_damage:.3f}, period={period}")

    # Statistical comparison
    print("\n" + "=" * 70)
    print("STATISTICAL SUMMARY")
    print("=" * 70)

    def summarize(data, name):
        gliders = [d['glider_score'] for d in data]
        entropies = [d['block_entropy'] for d in data]
        damages = [d['final_damage'] for d in data]
        periods = [d['period'] for d in data if d['period']]

        print(f"\n{name}:")
        print(f"  Glider score: mean={np.mean(gliders):.3f}, std={np.std(gliders):.3f}")
        print(f"  Block entropy: mean={np.mean(entropies):.3f}, std={np.std(entropies):.3f}")
        print(f"  Final damage: mean={np.mean(damages):.3f}, std={np.std(damages):.3f}")
        if periods:
            print(f"  Period: mean={np.mean(periods):.0f}, range={min(periods)}-{max(periods)}")
        else:
            print(f"  Period: None found")

    summarize(outlier_data, "OUTLIERS (Class III but periodic)")
    summarize(chaotic_data, "TRULY CHAOTIC (Class III)")
    summarize(class4_data, "CLASS IV (Complex)")

    # Key insight
    print("\n" + "=" * 70)
    print("KEY INSIGHT")
    print("=" * 70)

    outlier_glider_mean = np.mean([d['glider_score'] for d in outlier_data])
    chaotic_glider_mean = np.mean([d['glider_score'] for d in chaotic_data])
    class4_glider_mean = np.mean([d['glider_score'] for d in class4_data])

    outlier_damage_mean = np.mean([d['final_damage'] for d in outlier_data])
    chaotic_damage_mean = np.mean([d['final_damage'] for d in chaotic_data])
    class4_damage_mean = np.mean([d['final_damage'] for d in class4_data])

    print(f"""
Glider scores (higher = more structure):
  Outliers:      {outlier_glider_mean:.3f}
  Truly Chaotic: {chaotic_glider_mean:.3f}
  Class IV:      {class4_glider_mean:.3f}

Damage spreading (higher = more chaotic):
  Outliers:      {outlier_damage_mean:.3f}
  Truly Chaotic: {chaotic_damage_mean:.3f}
  Class IV:      {class4_damage_mean:.3f}
""")

    if outlier_glider_mean > chaotic_glider_mean:
        print("The outliers have MORE structure than truly chaotic rules.")
        print("This suggests they might be misclassified.")
    else:
        print("The outliers have similar or less structure than chaotic rules.")
        print("Periodicity alone doesn't indicate misclassification.")

    # Skip visualization (no matplotlib)

    return outlier_data, chaotic_data, class4_data

if __name__ == "__main__":
    outlier_data, chaotic_data, class4_data = main()
