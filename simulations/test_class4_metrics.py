#!/usr/bin/env python3
"""
Test new metrics to distinguish Class IV from Class III cellular automata.

Key question: What DOES distinguish Class IV from Class III if not entropy gap?

Metrics to test:
1. Transient length - how long before periodic/quasi-periodic behavior
2. Damage spreading - how perturbations propagate over time
3. Two-point correlation decay - spatial structure
4. Block entropy convergence rate - information theoretic
5. Attractor diversity - different ICs -> different patterns

Author: Claude (overnight session 2)
Date: 2025-11-27
"""

import numpy as np
from collections import defaultdict

# Key rules to test
CLASS_IV = [110, 124, 137, 193]  # canonical Class IV
CLASS_III = [30, 45, 73, 89, 101, 105, 110, 135, 149, 150, 153]  # chaotic rules
CLASS_II = [4, 32, 36, 50, 54, 108, 122, 132, 164]  # periodic rules

# Remove 110 from Class III (it's actually Class IV)
CLASS_III = [r for r in CLASS_III if r not in CLASS_IV]

def apply_rule(cells, rule_num):
    """Apply ECA rule to get next generation."""
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

def run_ca(rule_num, width, steps, ic=None):
    """Run CA and return history."""
    if ic is None:
        cells = np.random.randint(0, 2, width)
    else:
        cells = np.array(ic)
    history = [cells.copy()]
    for _ in range(steps):
        cells = apply_rule(cells, rule_num)
        history.append(cells.copy())
    return np.array(history)

def state_to_tuple(state):
    """Convert state array to hashable tuple."""
    return tuple(state.tolist())

# =============================================================================
# METRIC 1: TRANSIENT LENGTH
# How many steps before the CA enters a periodic cycle?
# Hypothesis: Class IV has LONGER transients (more "computation" before settling)
# =============================================================================

def measure_transient(rule_num, width=100, max_steps=5000):
    """Measure transient length until periodic behavior detected."""
    cells = np.random.randint(0, 2, width)
    seen_states = {}

    for step in range(max_steps):
        state_key = state_to_tuple(cells)
        if state_key in seen_states:
            # Found cycle
            period = step - seen_states[state_key]
            return step, period
        seen_states[state_key] = step
        cells = apply_rule(cells, rule_num)

    return max_steps, None  # No cycle found

def test_transient_lengths():
    """Compare transient lengths across classes."""
    print("=" * 60)
    print("METRIC 1: TRANSIENT LENGTH")
    print("=" * 60)
    print("How long before entering periodic behavior?")
    print()

    results = {}
    trials = 10
    width = 50  # Small width so we can detect cycles

    for label, rules in [("Class IV", CLASS_IV), ("Class III", CLASS_III), ("Class II", CLASS_II)]:
        print(f"\n{label}:")
        class_transients = []
        for rule in rules[:4]:  # Test first 4 rules of each class
            transients = []
            periods = []
            for _ in range(trials):
                trans, period = measure_transient(rule, width=width)
                transients.append(trans)
                if period:
                    periods.append(period)

            mean_trans = np.mean(transients)
            class_transients.append(mean_trans)
            cycle_found = len(periods) / trials * 100
            mean_period = np.mean(periods) if periods else float('inf')
            print(f"  Rule {rule:3d}: transient={mean_trans:7.1f}, cycle_found={cycle_found:.0f}%, period={mean_period:.0f}")

        results[label] = np.mean(class_transients)

    print(f"\n>>> Class means: IV={results.get('Class IV', 'N/A'):.1f}, III={results.get('Class III', 'N/A'):.1f}, II={results.get('Class II', 'N/A'):.1f}")
    return results

# =============================================================================
# METRIC 2: DAMAGE SPREADING (Lyapunov-like)
# How does a small perturbation grow/shrink over time?
# Hypothesis: Class IV has CONTROLLED spreading (not too fast, not dying out)
# =============================================================================

def measure_damage_spreading(rule_num, width=100, steps=200, trials=10):
    """Measure how a single-cell perturbation spreads over time."""
    spreading_curves = []

    for _ in range(trials):
        # Start with same random IC
        cells1 = np.random.randint(0, 2, width)
        cells2 = cells1.copy()
        # Flip one cell in the middle
        cells2[width // 2] = 1 - cells2[width // 2]

        damages = [1]  # Initial difference is 1 cell
        for _ in range(steps):
            cells1 = apply_rule(cells1, rule_num)
            cells2 = apply_rule(cells2, rule_num)
            damage = np.sum(cells1 != cells2)
            damages.append(damage)
        spreading_curves.append(damages)

    # Average over trials
    mean_curve = np.mean(spreading_curves, axis=0)

    # Compute spreading rate (slope of log damage in early phase)
    early = mean_curve[1:50]
    early = early[early > 0]  # Only positive values
    if len(early) > 10:
        log_damage = np.log(early + 0.1)
        spreading_rate = (log_damage[-1] - log_damage[0]) / len(log_damage)
    else:
        spreading_rate = 0

    # Final damage fraction
    final_damage = mean_curve[-1] / width

    return spreading_rate, final_damage, mean_curve

def test_damage_spreading():
    """Compare damage spreading across classes."""
    print("\n" + "=" * 60)
    print("METRIC 2: DAMAGE SPREADING")
    print("=" * 60)
    print("How does a single-cell perturbation spread?")
    print()

    results = {}

    for label, rules in [("Class IV", CLASS_IV), ("Class III", CLASS_III), ("Class II", CLASS_II)]:
        print(f"\n{label}:")
        class_rates = []
        class_final = []
        for rule in rules[:4]:
            rate, final, _ = measure_damage_spreading(rule)
            class_rates.append(rate)
            class_final.append(final)
            print(f"  Rule {rule:3d}: spreading_rate={rate:.4f}, final_damage={final:.2%}")

        results[label] = {
            'mean_rate': np.mean(class_rates),
            'mean_final': np.mean(class_final)
        }

    print(f"\n>>> Class means:")
    for label, r in results.items():
        print(f"    {label}: rate={r['mean_rate']:.4f}, final={r['mean_final']:.2%}")
    return results

# =============================================================================
# METRIC 3: SPATIAL AUTOCORRELATION DECAY
# How correlated are cells at distance d?
# Hypothesis: Class IV has POWER-LAW decay (scale-free structure)
#             Class III has EXPONENTIAL decay (characteristic scale)
# =============================================================================

def measure_spatial_correlation(rule_num, width=200, steps=200, trials=5):
    """Measure spatial autocorrelation function."""
    correlations = []

    for _ in range(trials):
        # Run CA to steady state
        history = run_ca(rule_num, width, steps)
        state = history[-1]

        # Compute autocorrelation at different lags
        mean_state = np.mean(state)
        var_state = np.var(state)
        if var_state < 1e-10:
            continue  # Skip uniform states

        max_lag = width // 4
        corr = []
        for lag in range(max_lag):
            shifted = np.roll(state, lag)
            c = np.mean((state - mean_state) * (shifted - mean_state)) / var_state
            corr.append(c)
        correlations.append(corr)

    if not correlations:
        return None, None

    mean_corr = np.mean(correlations, axis=0)

    # Fit exponential and power law decay
    lags = np.arange(1, len(mean_corr))
    corr_values = mean_corr[1:]

    # Find characteristic decay length (where correlation drops to 1/e)
    decay_length = None
    threshold = 1.0 / np.e
    for i, c in enumerate(corr_values):
        if c < threshold:
            decay_length = i + 1
            break

    return decay_length, mean_corr

def test_spatial_correlation():
    """Compare spatial correlation across classes."""
    print("\n" + "=" * 60)
    print("METRIC 3: SPATIAL AUTOCORRELATION")
    print("=" * 60)
    print("How far does spatial structure extend?")
    print()

    results = {}

    for label, rules in [("Class IV", CLASS_IV), ("Class III", CLASS_III)]:
        print(f"\n{label}:")
        decay_lengths = []
        for rule in rules[:4]:
            decay, _ = measure_spatial_correlation(rule)
            if decay is not None:
                decay_lengths.append(decay)
                print(f"  Rule {rule:3d}: decay_length={decay}")
            else:
                print(f"  Rule {rule:3d}: uniform state (no correlation)")

        if decay_lengths:
            results[label] = np.mean(decay_lengths)

    print(f"\n>>> Class means: {results}")
    return results

# =============================================================================
# METRIC 4: BLOCK ENTROPY CONVERGENCE
# How quickly does block entropy converge as block size increases?
# Hypothesis: Class IV converges SLOWLY (structure at all scales)
# =============================================================================

def block_entropy(state, block_size):
    """Compute entropy of blocks of given size."""
    n = len(state)
    blocks = []
    for i in range(n - block_size + 1):
        block = tuple(state[i:i+block_size].tolist())
        blocks.append(block)

    # Count frequencies
    counts = defaultdict(int)
    for b in blocks:
        counts[b] += 1

    # Compute entropy
    total = len(blocks)
    probs = [c/total for c in counts.values()]
    return -sum(p * np.log2(p) for p in probs if p > 0)

def measure_entropy_convergence(rule_num, width=300, steps=200, trials=5):
    """Measure how block entropy scales with block size."""
    entropies = []

    for _ in range(trials):
        history = run_ca(rule_num, width, steps)
        state = history[-1]

        trial_ent = []
        for block_size in range(1, 12):
            ent = block_entropy(state, block_size)
            # Normalize by maximum possible entropy
            ent_per_bit = ent / block_size
            trial_ent.append(ent_per_bit)
        entropies.append(trial_ent)

    mean_ent = np.mean(entropies, axis=0)

    # Measure convergence rate: how fast does ent_per_bit stabilize?
    diffs = np.abs(np.diff(mean_ent))
    convergence_rate = np.mean(diffs[:5])  # Early convergence rate

    return convergence_rate, mean_ent

def test_entropy_convergence():
    """Compare entropy convergence across classes."""
    print("\n" + "=" * 60)
    print("METRIC 4: BLOCK ENTROPY CONVERGENCE")
    print("=" * 60)
    print("How quickly does entropy-per-bit stabilize with block size?")
    print()

    results = {}

    for label, rules in [("Class IV", CLASS_IV), ("Class III", CLASS_III)]:
        print(f"\n{label}:")
        rates = []
        for rule in rules[:4]:
            rate, ent = measure_entropy_convergence(rule)
            rates.append(rate)
            print(f"  Rule {rule:3d}: convergence_rate={rate:.4f}, final_ent={ent[-1]:.3f}")

        results[label] = np.mean(rates)

    print(f"\n>>> Class means: {results}")
    print("Lower = faster convergence = less multi-scale structure")
    return results

# =============================================================================
# METRIC 5: INITIAL CONDITION SENSITIVITY (Basin Diversity)
# How different are the final states from different ICs?
# Hypothesis: Class IV has INTERMEDIATE diversity
# =============================================================================

def measure_ic_sensitivity(rule_num, width=50, steps=500, n_ics=20):
    """Measure diversity of final states from different initial conditions."""
    final_states = []

    for _ in range(n_ics):
        history = run_ca(rule_num, width, steps)
        final_state = state_to_tuple(history[-1])
        final_states.append(final_state)

    # Count unique final states
    unique_states = len(set(final_states))
    diversity = unique_states / n_ics

    return diversity, unique_states

def test_ic_sensitivity():
    """Compare IC sensitivity across classes."""
    print("\n" + "=" * 60)
    print("METRIC 5: INITIAL CONDITION SENSITIVITY")
    print("=" * 60)
    print("How many different final states from different ICs?")
    print()

    results = {}

    for label, rules in [("Class IV", CLASS_IV), ("Class III", CLASS_III), ("Class II", CLASS_II)]:
        print(f"\n{label}:")
        diversities = []
        for rule in rules[:4]:
            div, unique = measure_ic_sensitivity(rule)
            diversities.append(div)
            print(f"  Rule {rule:3d}: diversity={div:.2%} ({unique} unique)")

        results[label] = np.mean(diversities)

    print(f"\n>>> Class means: {results}")
    return results

# =============================================================================
# METRIC 6: GLIDER DETECTION
# Do coherent, propagating structures exist?
# This is THE defining feature of Class IV!
# =============================================================================

def detect_gliders(rule_num, width=100, steps=200):
    """Attempt to detect glider-like structures."""
    history = run_ca(rule_num, width, steps)

    # Simple approach: look for diagonal lines in space-time plot
    # A glider shows as a line at angle != 0 or 90

    # Compute temporal autocorrelation at different spatial offsets
    glider_scores = []

    for offset in range(-5, 6):
        if offset == 0:
            continue
        correlations = []
        for t in range(10, steps - 10):
            state1 = history[t]
            state2 = history[t + abs(offset)]
            # Roll state2 by offset to align if there's a glider
            rolled = np.roll(state2, offset)
            corr = np.corrcoef(state1, rolled)[0, 1]
            if not np.isnan(corr):
                correlations.append(corr)
        if correlations:
            glider_scores.append((offset, np.mean(correlations)))

    if not glider_scores:
        return 0, None

    # Find max correlation at non-zero offset
    max_score = max(glider_scores, key=lambda x: x[1])

    return max_score[1], max_score[0]

def test_glider_detection():
    """Compare glider presence across classes."""
    print("\n" + "=" * 60)
    print("METRIC 6: GLIDER DETECTION")
    print("=" * 60)
    print("Are there propagating structures?")
    print()

    results = {}

    for label, rules in [("Class IV", CLASS_IV), ("Class III", CLASS_III)]:
        print(f"\n{label}:")
        scores = []
        for rule in rules[:4]:
            score, offset = detect_gliders(rule)
            scores.append(score)
            print(f"  Rule {rule:3d}: glider_score={score:.4f}, best_offset={offset}")

        results[label] = np.mean(scores)

    print(f"\n>>> Class means: {results}")
    return results

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("Testing metrics to distinguish Class IV from Class III CAs")
    print("=" * 70)

    all_results = {}

    all_results['transient'] = test_transient_lengths()
    all_results['damage'] = test_damage_spreading()
    all_results['correlation'] = test_spatial_correlation()
    all_results['entropy_conv'] = test_entropy_convergence()
    all_results['ic_sensitivity'] = test_ic_sensitivity()
    all_results['gliders'] = test_glider_detection()

    print("\n" + "=" * 70)
    print("SUMMARY: WHAT DISTINGUISHES CLASS IV?")
    print("=" * 70)

    # Analyze which metrics show clear separation
    separating_metrics = []

    for name, result in all_results.items():
        if isinstance(result, dict):
            iv = result.get('Class IV')
            iii = result.get('Class III')
            if iv is not None and iii is not None:
                if isinstance(iv, dict):
                    iv = iv.get('mean_rate', iv.get('mean_final'))
                if isinstance(iii, dict):
                    iii = iii.get('mean_rate', iii.get('mean_final'))
                if iv and iii and iv != iii:
                    ratio = iv / iii if iii != 0 else float('inf')
                    if ratio > 1.5 or ratio < 0.67:  # At least 50% difference
                        separating_metrics.append((name, iv, iii, ratio))

    if separating_metrics:
        print("\nMetrics that show >50% difference between Class IV and III:")
        for name, iv, iii, ratio in separating_metrics:
            print(f"  {name}: IV={iv:.3f}, III={iii:.3f}, ratio={ratio:.2f}")
    else:
        print("\nNo metrics showed >50% separation between Class IV and III")

    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
