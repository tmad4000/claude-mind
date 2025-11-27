#!/usr/bin/env python3
"""
Deep dive into block entropy convergence rate as a Class IV distinguisher.

Hypothesis: Class IV rules have SLOWER entropy convergence because they have
structure at multiple scales. Class III is more "random" and converges quickly.

This could be the key distinguishing feature!

Author: Claude (overnight session 2)
Date: 2025-11-27
"""

import numpy as np
from collections import defaultdict

# Skip matplotlib if not available
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("(matplotlib not available, skipping visualization)")

# All canonical rules by class
CLASS_IV = [110, 124, 137, 193]
CLASS_III_CHAOTIC = [30, 45, 73, 89, 101, 105, 135, 149, 150, 153, 169, 181, 182, 210]
CLASS_III_CHAOTIC = [r for r in CLASS_III_CHAOTIC if r not in CLASS_IV]

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

def run_ca(rule_num, width, steps, seed=None):
    """Run CA and return final state."""
    if seed is not None:
        np.random.seed(seed)
    cells = np.random.randint(0, 2, width)
    for _ in range(steps):
        cells = apply_rule(cells, rule_num)
    return cells

def block_entropy(state, block_size):
    """Compute entropy of blocks of given size."""
    n = len(state)
    blocks = []
    for i in range(n - block_size + 1):
        block = tuple(state[i:i+block_size].tolist())
        blocks.append(block)

    counts = defaultdict(int)
    for b in blocks:
        counts[b] += 1

    total = len(blocks)
    probs = [c/total for c in counts.values()]
    return -sum(p * np.log2(p) for p in probs if p > 0)

def compute_entropy_curve(rule_num, width=500, steps=300, trials=10, max_block=15):
    """Compute entropy per bit vs block size curve."""
    all_curves = []

    for trial in range(trials):
        state = run_ca(rule_num, width, steps, seed=trial)

        curve = []
        for k in range(1, max_block + 1):
            ent = block_entropy(state, k)
            ent_per_bit = ent / k
            curve.append(ent_per_bit)
        all_curves.append(curve)

    return np.mean(all_curves, axis=0), np.std(all_curves, axis=0)

def measure_convergence_metrics(curve):
    """Extract multiple convergence metrics from entropy curve."""
    # 1. Final entropy per bit (large block limit)
    final_entropy = curve[-1]

    # 2. Average change per step (lower = faster convergence)
    diffs = np.abs(np.diff(curve))
    mean_change = np.mean(diffs)

    # 3. Convergence rate (how fast does it approach final value?)
    # Fit exponential decay to (curve - final_entropy)
    residuals = np.abs(curve - final_entropy)
    # Find half-life: block size where residual drops to half initial
    initial_residual = residuals[0]
    half_life = None
    for i, r in enumerate(residuals):
        if r < initial_residual / 2:
            half_life = i + 1
            break

    # 4. Total "entropy gap" (area between curve and horizontal line at final value)
    entropy_gap = np.sum(residuals)

    # 5. Local structure index: ratio of block-2 to block-1 entropy
    if len(curve) >= 2:
        local_structure = curve[0] - curve[1]  # Drop from k=1 to k=2
    else:
        local_structure = 0

    return {
        'final_entropy': final_entropy,
        'mean_change': mean_change,
        'half_life': half_life,
        'entropy_gap': entropy_gap,
        'local_structure': local_structure
    }

def main():
    print("=" * 70)
    print("DEEP DIVE: BLOCK ENTROPY CONVERGENCE")
    print("=" * 70)
    print()

    # Test all rules
    all_results = {}

    print("Computing entropy curves for Class IV rules...")
    for rule in CLASS_IV:
        curve, std = compute_entropy_curve(rule)
        metrics = measure_convergence_metrics(curve)
        all_results[rule] = {'curve': curve, 'std': std, 'metrics': metrics, 'class': 'IV'}
        print(f"  Rule {rule}: final={metrics['final_entropy']:.4f}, gap={metrics['entropy_gap']:.4f}")

    print("\nComputing entropy curves for Class III rules...")
    for rule in CLASS_III_CHAOTIC[:8]:  # First 8 Class III rules
        curve, std = compute_entropy_curve(rule)
        metrics = measure_convergence_metrics(curve)
        all_results[rule] = {'curve': curve, 'std': std, 'metrics': metrics, 'class': 'III'}
        print(f"  Rule {rule}: final={metrics['final_entropy']:.4f}, gap={metrics['entropy_gap']:.4f}")

    # Statistical comparison
    print("\n" + "=" * 70)
    print("STATISTICAL COMPARISON")
    print("=" * 70)

    iv_gaps = [all_results[r]['metrics']['entropy_gap'] for r in CLASS_IV]
    iii_gaps = [all_results[r]['metrics']['entropy_gap'] for r in CLASS_III_CHAOTIC[:8] if r in all_results]

    iv_final = [all_results[r]['metrics']['final_entropy'] for r in CLASS_IV]
    iii_final = [all_results[r]['metrics']['entropy_gap'] for r in CLASS_III_CHAOTIC[:8] if r in all_results]

    iv_change = [all_results[r]['metrics']['mean_change'] for r in CLASS_IV]
    iii_change = [all_results[r]['metrics']['mean_change'] for r in CLASS_III_CHAOTIC[:8] if r in all_results]

    print(f"\nEntropy Gap (area under convergence curve):")
    print(f"  Class IV mean: {np.mean(iv_gaps):.4f} ± {np.std(iv_gaps):.4f}")
    print(f"  Class III mean: {np.mean(iii_gaps):.4f} ± {np.std(iii_gaps):.4f}")
    print(f"  Ratio IV/III: {np.mean(iv_gaps)/np.mean(iii_gaps):.2f}")

    print(f"\nFinal Entropy (large block limit):")
    print(f"  Class IV mean: {np.mean(iv_final):.4f} ± {np.std(iv_final):.4f}")
    print(f"  Class III mean: {np.mean(iii_final):.4f} ± {np.std(iii_final):.4f}")

    print(f"\nMean Change Per Block Size:")
    print(f"  Class IV mean: {np.mean(iv_change):.4f} ± {np.std(iv_change):.4f}")
    print(f"  Class III mean: {np.mean(iii_change):.4f} ± {np.std(iii_change):.4f}")
    print(f"  Ratio IV/III: {np.mean(iv_change)/np.mean(iii_change):.2f}")

    # Effect size (Cohen's d)
    pooled_std = np.sqrt((np.std(iv_gaps)**2 + np.std(iii_gaps)**2) / 2)
    if pooled_std > 0:
        cohen_d = (np.mean(iv_gaps) - np.mean(iii_gaps)) / pooled_std
        print(f"\nCohen's d for entropy gap: {cohen_d:.2f}")
        if abs(cohen_d) > 0.8:
            print("  -> LARGE effect size!")
        elif abs(cohen_d) > 0.5:
            print("  -> Medium effect size")
        else:
            print("  -> Small effect size")

    # Create visualization if matplotlib available
    if HAS_MATPLOTLIB:
        print("\nCreating visualization...")
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Left: Entropy curves
        ax1 = axes[0]
        block_sizes = np.arange(1, 16)

        for rule in CLASS_IV:
            curve = all_results[rule]['curve']
            ax1.plot(block_sizes, curve, 'b-', alpha=0.7, linewidth=2, label=f'Rule {rule}' if rule == 110 else '')
        for rule in CLASS_III_CHAOTIC[:4]:
            if rule in all_results:
                curve = all_results[rule]['curve']
                ax1.plot(block_sizes, curve, 'r--', alpha=0.7, linewidth=2, label=f'Rule {rule}' if rule == 30 else '')

        ax1.axhline(y=1.0, color='gray', linestyle=':', label='Maximum (random)')
        ax1.set_xlabel('Block Size (k)', fontsize=12)
        ax1.set_ylabel('Entropy per Bit (H(k)/k)', fontsize=12)
        ax1.set_title('Entropy Convergence Curves', fontsize=14)
        ax1.legend(loc='upper right')
        ax1.set_ylim(0, 1.1)
        ax1.grid(True, alpha=0.3)

        # Add annotation
        ax1.annotate('Class IV: slower convergence\n(more multi-scale structure)',
                    xy=(10, 0.6), fontsize=10, color='blue',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        ax1.annotate('Class III: faster convergence\n(more random)',
                    xy=(10, 0.75), fontsize=10, color='red',
                    bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))

        # Right: Box plot comparison
        ax2 = axes[1]
        data = [iv_gaps, iii_gaps]
        bp = ax2.boxplot(data, labels=['Class IV', 'Class III'], patch_artist=True)
        bp['boxes'][0].set_facecolor('lightblue')
        bp['boxes'][1].set_facecolor('lightcoral')
        ax2.set_ylabel('Entropy Gap (total deviation from limit)', fontsize=12)
        ax2.set_title('Entropy Gap Comparison', fontsize=14)
        ax2.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        plt.savefig('simulations/entropy_convergence_comparison.png', dpi=150)
        print("  Saved to simulations/entropy_convergence_comparison.png")
    else:
        print("\n(Skipping visualization - matplotlib not available)")

    # Conclusions
    print("\n" + "=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)

    ratio = np.mean(iv_gaps) / np.mean(iii_gaps) if np.mean(iii_gaps) > 0 else float('inf')

    if ratio > 1.5:
        print(f"""
Class IV rules have SIGNIFICANTLY HIGHER entropy gaps (ratio = {ratio:.2f}x).

This means: Class IV rules maintain MORE structure at larger scales.

INTERPRETATION:
- Class III quickly reaches maximum entropy (appears random at all scales)
- Class IV maintains non-random structure even at large block sizes
- This is consistent with the presence of GLIDERS and LOCALIZED STRUCTURES

The entropy gap measures "how far from random" the pattern is.
Class IV being farther from random = more structured = more "interesting"

This could be the QUANTITATIVE SIGNATURE of Class IV:
  - High entropy gap in block entropy convergence
  - Structure persists at multiple scales
  - Not just high entropy (that's Class III)
  - Not just low entropy (that's Class II)
  - HIGH ENTROPY GAP = complexity at the edge of chaos
""")
    elif ratio < 0.67:
        print(f"Class III has higher entropy gap - hypothesis falsified.")
    else:
        print(f"No clear separation (ratio = {ratio:.2f})")

    return all_results

if __name__ == "__main__":
    results = main()
