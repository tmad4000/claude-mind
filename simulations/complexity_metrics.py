#!/usr/bin/env python3
"""
Complexity Metrics for Cellular Automata

After my first exploration, I realized simple block entropy isn't enough.
This module develops better metrics for distinguishing:
- Class I: Convergence to uniformity
- Class II: Periodic/stable patterns
- Class III: Chaotic (random-like)
- Class IV: Complex (edge of chaos, computational)

Key insight: True complexity lives at the boundary between order and chaos.
"""

import math
from collections import Counter
from typing import List, Tuple
import sys
sys.path.append('/Users/jacobcole/code/claude-mind')
from simulations.cellular_automata import ElementaryCA

def entropy(probabilities: List[float]) -> float:
    """Calculate Shannon entropy."""
    return -sum(p * math.log2(p) for p in probabilities if p > 0)


def block_entropy(row: List[int], block_size: int = 4) -> float:
    """Calculate entropy of blocks of given size."""
    blocks = []
    for i in range(0, len(row) - block_size + 1, block_size):
        blocks.append(tuple(row[i:i+block_size]))

    if not blocks:
        return 0.0

    counts = Counter(blocks)
    total = sum(counts.values())
    probs = [c / total for c in counts.values()]
    return entropy(probs)


def multi_scale_entropy(history: List[List[int]], scales: List[int] = [2, 4, 8]) -> dict:
    """
    Calculate entropy at multiple block scales.

    Hypothesis: Complex patterns have different entropy signatures across scales
    - Random: high entropy at all scales
    - Ordered: low entropy at all scales
    - Complex: varies across scales (structure at multiple levels)
    """
    if len(history) < 4:
        return {s: 0.0 for s in scales}

    # Use final rows for steady-state behavior
    final_rows = history[-min(8, len(history)):]
    combined = []
    for row in final_rows:
        combined.extend(row)

    results = {}
    for scale in scales:
        results[scale] = block_entropy(combined, scale)

    return results


def entropy_variance(history: List[List[int]], block_size: int = 4) -> float:
    """
    Calculate how much entropy fluctuates over time.

    Hypothesis: Class IV rules have higher entropy variance because
    structures form and dissolve, creating local order/disorder.
    """
    if len(history) < 10:
        return 0.0

    entropies = [block_entropy(row, block_size) for row in history]
    mean_entropy = sum(entropies) / len(entropies)
    variance = sum((e - mean_entropy)**2 for e in entropies) / len(entropies)
    return variance


def compression_complexity(history: List[List[int]]) -> float:
    """
    Estimate Kolmogorov complexity via compression ratio.

    Complex patterns should be harder to compress than random data
    but easier than purely ordered patterns.

    Wait, that's backwards - truly random data is incompressible!
    But *pseudo*-random from simple rules should compress well.

    Actually, what I want: patterns that have INTERMEDIATE compressibility.
    - Ordered: very compressible (low ratio)
    - Random: incompressible (ratio ~1)
    - Complex: intermediate (has structure but not trivial)
    """
    import zlib

    # Convert to bytes
    data = bytes([cell for row in history for cell in row])

    compressed = zlib.compress(data, level=9)

    if len(data) == 0:
        return 0.0

    return len(compressed) / len(data)


def detect_periodicity(history: List[List[int]], max_period: int = 50) -> Tuple[bool, int]:
    """
    Check if the CA eventually becomes periodic.

    Returns (is_periodic, period_length or None)
    """
    if len(history) < max_period + 10:
        return False, None

    final_state = tuple(history[-1])

    for period in range(1, min(max_period, len(history) // 2)):
        # Check if state at -1 equals state at -1-period
        if len(history) > period:
            earlier_state = tuple(history[-(period+1)])
            if earlier_state == final_state:
                # Verify it's actually periodic by checking intermediate states
                is_periodic = True
                for i in range(1, min(period, 5)):  # Spot check
                    if tuple(history[-(i+1)]) != tuple(history[-(period+i+1)]):
                        is_periodic = False
                        break
                if is_periodic:
                    return True, period

    return False, None


def detect_convergence(history: List[List[int]], tolerance: int = 5) -> Tuple[bool, str]:
    """
    Check if CA converges to a uniform or near-uniform state.

    Returns (converged, type) where type is 'all_0', 'all_1', 'mixed', or None
    """
    if not history:
        return False, None

    final = history[-1]
    density = sum(final) / len(final)

    if density < 0.01:  # Almost all 0s
        return True, 'all_0'
    elif density > 0.99:  # Almost all 1s
        return True, 'all_1'

    # Check if density is stable near 0 or 1
    if len(history) >= 10:
        recent_densities = [sum(row)/len(row) for row in history[-10:]]
        variance = sum((d - density)**2 for d in recent_densities) / 10
        if variance < 0.001 and (density < 0.1 or density > 0.9):
            return True, 'sparse' if density < 0.1 else 'dense'

    return False, None


def find_gliders(history: List[List[int]], max_width: int = 10, max_period: int = 10) -> List[dict]:
    """
    Attempt to detect gliders (structures that translate over time).

    This is a simplified heuristic - true glider detection is complex.
    I look for small patterns that repeat with spatial offset.

    This is something I genuinely want to improve - detecting structure!
    """
    gliders = []

    if len(history) < max_period + 5:
        return gliders

    width = len(history[0])

    # For each starting position and time
    for start_t in range(0, len(history) - max_period, max_period):
        for start_x in range(width - max_width):
            # Extract pattern
            pattern = [tuple(history[start_t + t][start_x:start_x + max_width])
                      for t in range(max_period)]

            # Look for the same pattern offset in space
            for offset in range(-3, 4):  # Check small translations
                if offset == 0:
                    continue

                found_match = False
                for check_t in range(start_t + 1, min(start_t + 20, len(history) - max_period)):
                    check_x = (start_x + offset) % width
                    check_pattern = [tuple(history[check_t + t][(check_x):(check_x + max_width)])
                                    for t in range(max_period)]

                    if pattern == check_pattern:
                        found_match = True
                        # Found a translating pattern
                        gliders.append({
                            'start_pos': start_x,
                            'start_time': start_t,
                            'width': max_width,
                            'velocity': offset / (check_t - start_t),
                            'period': check_t - start_t
                        })
                        break

                if found_match:
                    break

    return gliders


def comprehensive_classify(rule_number: int, trials: int = 5, steps: int = 100) -> dict:
    """
    Improved classification using multiple metrics.

    This is my refined hypothesis about what distinguishes the classes.
    """
    import random

    all_metrics = []

    for _ in range(trials):
        # Random initial conditions
        width = 100
        initial = [random.randint(0, 1) for _ in range(width)]

        ca = ElementaryCA(rule_number, width)
        ca.run(initial, steps=steps)

        metrics = {
            'compression': compression_complexity(ca.history),
            'multi_entropy': multi_scale_entropy(ca.history),
            'entropy_var': entropy_variance(ca.history),
        }

        periodic, period = detect_periodicity(ca.history)
        metrics['periodic'] = periodic
        metrics['period'] = period

        converged, conv_type = detect_convergence(ca.history)
        metrics['converged'] = converged
        metrics['convergence_type'] = conv_type

        # Check final density
        final_density = sum(ca.history[-1]) / len(ca.history[-1])
        metrics['final_density'] = final_density

        all_metrics.append(metrics)

    # Aggregate
    result = {
        'rule': rule_number,
        'avg_compression': sum(m['compression'] for m in all_metrics) / len(all_metrics),
        'avg_entropy_var': sum(m['entropy_var'] for m in all_metrics) / len(all_metrics),
        'periodic_count': sum(1 for m in all_metrics if m['periodic']),
        'converged_count': sum(1 for m in all_metrics if m['converged']),
        'avg_final_density': sum(m['final_density'] for m in all_metrics) / len(all_metrics),
    }

    # Multi-scale entropy averages
    for scale in [2, 4, 8]:
        result[f'entropy_{scale}'] = sum(m['multi_entropy'][scale] for m in all_metrics) / len(all_metrics)

    # Classification logic
    if result['converged_count'] >= trials * 0.8:
        result['class'] = 'I'
        result['confidence'] = 'high'
        result['reasoning'] = 'Converges to uniform state'
    elif result['periodic_count'] >= trials * 0.6:
        result['class'] = 'II'
        result['confidence'] = 'high'
        result['reasoning'] = 'Shows periodic behavior'
    elif result['avg_compression'] > 0.85:
        # High compression ratio suggests randomness (incompressible)
        result['class'] = 'III'
        result['confidence'] = 'medium'
        result['reasoning'] = 'High incompressibility suggests chaos'
    elif result['avg_entropy_var'] > 0.3 and 0.4 < result['avg_compression'] < 0.75:
        # Intermediate compression + high variance = complex!
        result['class'] = 'IV'
        result['confidence'] = 'medium'
        result['reasoning'] = 'Intermediate complexity with dynamic behavior'
    elif result['entropy_4'] > result['entropy_2'] * 0.9 and result['entropy_8'] < result['entropy_4'] * 0.8:
        # Entropy drops at larger scales suggests structure
        result['class'] = 'IV?'
        result['confidence'] = 'low'
        result['reasoning'] = 'Multi-scale structure detected'
    else:
        result['class'] = 'uncertain'
        result['confidence'] = 'low'
        result['reasoning'] = 'Does not fit clear pattern'

    return result


def classify_all_rules(progress_every: int = 32) -> List[dict]:
    """Classify all 256 elementary rules."""
    results = []

    for rule in range(256):
        result = comprehensive_classify(rule, trials=3, steps=80)
        results.append(result)

        if rule % progress_every == progress_every - 1:
            print(f"Classified rules 0-{rule}...")

    return results


def summarize_classifications(results: List[dict]):
    """Summarize classification results."""
    from collections import Counter

    class_counts = Counter(r['class'] for r in results)

    print("\n" + "="*60)
    print("CLASSIFICATION SUMMARY")
    print("="*60)

    print(f"\nClass distribution:")
    for cls, count in sorted(class_counts.items()):
        print(f"  Class {cls}: {count} rules ({100*count/256:.1f}%)")

    print(f"\nClass IV candidates (the interesting ones!):")
    class_4 = [r for r in results if r['class'] in ('IV', 'IV?')]
    for r in class_4:
        print(f"  Rule {r['rule']}: {r['reasoning']} (confidence: {r['confidence']})")

    return class_counts


if __name__ == '__main__':
    print("Testing improved complexity metrics on known rules...\n")

    # Test on famous rules
    for rule in [110, 30, 90, 0, 255, 184]:
        print(f"\n{'='*50}")
        print(f"Rule {rule}")
        print('='*50)
        result = comprehensive_classify(rule, trials=3)
        for key, value in result.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.3f}")
            else:
                print(f"  {key}: {value}")
