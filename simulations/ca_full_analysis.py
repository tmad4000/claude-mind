#!/usr/bin/env python3
"""
Comprehensive CA Rule Space Analysis

This script systematically analyzes all 256 elementary CA rules to:
1. Classify each rule (Wolfram classes I-IV)
2. Map the topology of rule space (which rules are neighbors?)
3. Test the hypothesis: Class IV rules are topologically isolated
4. Look for patterns in binary representation

Based on earlier discovery: Rule 110 has NO Hamming-1 neighbors that are Class IV.
Question: Is this true for ALL Class IV rules?
"""

import json
import math
import random
from pathlib import Path
from datetime import datetime
from collections import defaultdict


class ElementaryCA:
    """1D Elementary Cellular Automata (Wolfram's 256 rules)"""

    def __init__(self, rule_number: int, width: int = 100):
        self.rule_number = rule_number
        self.width = width
        self.rule_table = self._build_rule_table(rule_number)
        self.history = []

    def _build_rule_table(self, rule_number: int) -> dict:
        table = {}
        for i in range(8):
            pattern = tuple(int(b) for b in format(i, '03b'))
            table[pattern] = (rule_number >> i) & 1
        return table

    def step(self, state: list) -> list:
        new_state = []
        for i in range(len(state)):
            left = state[(i - 1) % len(state)]
            center = state[i]
            right = state[(i + 1) % len(state)]
            neighborhood = (left, center, right)
            new_state.append(self.rule_table[neighborhood])
        return new_state

    def run(self, initial_state: list = None, steps: int = 100) -> list:
        if initial_state is None:
            initial_state = [0] * self.width
            initial_state[self.width // 2] = 1

        self.history = [initial_state]
        state = initial_state

        for _ in range(steps):
            state = self.step(state)
            self.history.append(state)

        return self.history


def compute_metrics(ca: ElementaryCA) -> dict:
    """Compute comprehensive metrics for CA behavior"""
    if not ca.history:
        return {}

    metrics = {'rule': ca.rule_number}

    # Basic density
    densities = [sum(row) / len(row) for row in ca.history]
    metrics['final_density'] = densities[-1]
    metrics['mean_density'] = sum(densities) / len(densities)
    metrics['density_variance'] = sum((d - metrics['mean_density'])**2 for d in densities) / len(densities)

    # Density trend (does it stabilize, oscillate, or drift?)
    if len(densities) > 20:
        early = sum(densities[:20]) / 20
        late = sum(densities[-20:]) / 20
        metrics['density_trend'] = late - early

    # Block entropy (complexity measure)
    if len(ca.history) >= 10:
        block_counts = defaultdict(int)
        for row in ca.history[-10:]:
            for i in range(0, len(row) - 3):
                block = tuple(row[i:i+4])
                block_counts[block] += 1
        total = sum(block_counts.values())
        entropy = 0
        for count in block_counts.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        metrics['block_entropy'] = entropy
        metrics['unique_blocks'] = len(block_counts)

    # Periodicity detection
    final_state = tuple(ca.history[-1])
    for i in range(len(ca.history) - 2, max(0, len(ca.history) - 50), -1):
        if tuple(ca.history[i]) == final_state:
            metrics['period'] = len(ca.history) - 1 - i
            break
    else:
        metrics['period'] = None

    # Left-right symmetry (XOR with reversed self)
    final = ca.history[-1]
    reversed_final = final[::-1]
    symmetry_diff = sum(a ^ b for a, b in zip(final, reversed_final))
    metrics['asymmetry'] = symmetry_diff / len(final)

    # Activity (cells that changed in last step)
    if len(ca.history) >= 2:
        changes = sum(a ^ b for a, b in zip(ca.history[-1], ca.history[-2]))
        metrics['final_activity'] = changes / len(ca.history[-1])

    # Spreading metric - did pattern expand from center?
    if len(ca.history) > 10:
        initial_active = sum(ca.history[0])
        final_active = sum(ca.history[-1])
        metrics['spreading'] = final_active - initial_active

    return metrics


def classify_rule_comprehensive(rule_number: int, trials: int = 5) -> dict:
    """
    Classify a rule using multiple initial conditions and refined heuristics.

    Returns detailed classification with confidence score.
    """
    all_metrics = []

    # Test 1: Single cell initial condition
    ca_single = ElementaryCA(rule_number, width=100)
    ca_single.run(steps=100)
    all_metrics.append(compute_metrics(ca_single))

    # Test 2-5: Random initial conditions
    for _ in range(trials - 1):
        ca = ElementaryCA(rule_number, width=100)
        initial = [random.randint(0, 1) for _ in range(100)]
        ca.run(initial, steps=100)
        all_metrics.append(compute_metrics(ca))

    # Aggregate metrics
    result = {
        'rule': rule_number,
        'binary': format(rule_number, '08b'),
        'bit_count': bin(rule_number).count('1'),  # Hamming weight
    }

    # Average across trials
    for key in ['mean_density', 'density_variance', 'block_entropy', 'spreading', 'final_activity']:
        values = [m.get(key, 0) for m in all_metrics if key in m]
        if values:
            result[f'avg_{key}'] = sum(values) / len(values)

    # Count periodic trials
    periodic_count = sum(1 for m in all_metrics if m.get('period') is not None)
    result['periodic_fraction'] = periodic_count / len(all_metrics)

    # Classification logic with confidence
    density = result.get('avg_mean_density', 0.5)
    entropy = result.get('avg_block_entropy', 0)
    variance = result.get('avg_density_variance', 0)
    spreading = result.get('avg_spreading', 0)
    periodic = result['periodic_fraction']

    # Class I: Homogeneous (dies out or fills)
    if density < 0.05 or density > 0.95:
        result['class'] = 'I'
        result['confidence'] = 0.9
        result['reasoning'] = f'Converges to homogeneous (density={density:.3f})'

    # Class II: Periodic/stable
    elif periodic > 0.6:
        result['class'] = 'II'
        result['confidence'] = 0.8 + (periodic * 0.2)
        result['reasoning'] = f'Shows periodic behavior ({periodic*100:.0f}% of trials)'

    # Class III: Chaotic (high entropy, high activity)
    elif entropy > 3.5 and variance > 0.01:
        result['class'] = 'III'
        result['confidence'] = min(0.95, 0.6 + entropy/10)
        result['reasoning'] = f'High entropy ({entropy:.2f}) suggests chaos'

    # Class IV: Complex/edge-of-chaos (intermediate behavior)
    elif 1.5 < entropy < 3.5 and 0.001 < variance < 0.05 and abs(spreading) > 10:
        result['class'] = 'IV'
        result['confidence'] = 0.6  # Class IV is hardest to identify
        result['reasoning'] = f'Intermediate: entropy={entropy:.2f}, spreading={spreading:.0f}'

    # Low entropy but non-trivial
    elif entropy < 1.5 and density > 0.1 and density < 0.9:
        result['class'] = 'II'
        result['confidence'] = 0.6
        result['reasoning'] = f'Low entropy ({entropy:.2f}) suggests simple patterns'

    else:
        result['class'] = 'III'  # Default to chaotic if unclear
        result['confidence'] = 0.4
        result['reasoning'] = f'Unclear classification: entropy={entropy:.2f}, density={density:.3f}'

    return result


def hamming_distance(r1: int, r2: int) -> int:
    """Count differing bits between two rule numbers"""
    return bin(r1 ^ r2).count('1')


def get_hamming_neighbors(rule: int, distance: int = 1) -> list:
    """Get all rules within given Hamming distance"""
    neighbors = []
    for other in range(256):
        if hamming_distance(rule, other) == distance:
            neighbors.append(other)
    return neighbors


def analyze_topology(classifications: dict) -> dict:
    """
    Analyze the topology of rule space.

    Key question: Are Class IV rules isolated (no Class IV neighbors)?
    """
    topology = {
        'class_counts': defaultdict(int),
        'neighbor_analysis': {},
        'isolated_complex': [],  # Class IV rules with no Class IV neighbors
        'clustered_complex': [],  # Class IV rules with Class IV neighbors
    }

    # Count classes
    for rule, info in classifications.items():
        topology['class_counts'][info['class']] += 1

    # Analyze neighbors for each rule
    for rule in range(256):
        info = classifications[rule]
        neighbors = get_hamming_neighbors(rule, 1)
        neighbor_classes = [classifications[n]['class'] for n in neighbors]

        topology['neighbor_analysis'][rule] = {
            'class': info['class'],
            'neighbor_classes': neighbor_classes,
            'same_class_neighbors': sum(1 for c in neighbor_classes if c == info['class']),
            'class_distribution': {c: neighbor_classes.count(c) for c in set(neighbor_classes)}
        }

        # Track Class IV isolation
        if info['class'] == 'IV':
            has_class_iv_neighbor = any(c == 'IV' for c in neighbor_classes)
            if has_class_iv_neighbor:
                topology['clustered_complex'].append(rule)
            else:
                topology['isolated_complex'].append(rule)

    return topology


def find_binary_patterns(classifications: dict) -> dict:
    """Look for patterns in the binary representation of rule numbers"""
    patterns = {
        'by_bit_count': defaultdict(list),
        'specific_bits': {},
    }

    # Group by Hamming weight (number of 1s)
    for rule, info in classifications.items():
        bit_count = bin(rule).count('1')
        patterns['by_bit_count'][bit_count].append({
            'rule': rule,
            'class': info['class']
        })

    # Class distribution by bit count
    patterns['class_by_bits'] = {}
    for bits, rules in patterns['by_bit_count'].items():
        class_counts = defaultdict(int)
        for r in rules:
            class_counts[r['class']] += 1
        patterns['class_by_bits'][bits] = dict(class_counts)

    # Look for specific bit patterns
    for bit_pos in range(8):
        with_bit = [r for r in range(256) if (r >> bit_pos) & 1]
        without_bit = [r for r in range(256) if not (r >> bit_pos) & 1]

        patterns['specific_bits'][f'bit_{bit_pos}'] = {
            'with_bit_class_counts': defaultdict(int),
            'without_bit_class_counts': defaultdict(int)
        }

        for r in with_bit:
            patterns['specific_bits'][f'bit_{bit_pos}']['with_bit_class_counts'][classifications[r]['class']] += 1
        for r in without_bit:
            patterns['specific_bits'][f'bit_{bit_pos}']['without_bit_class_counts'][classifications[r]['class']] += 1

    return patterns


def run_full_analysis() -> dict:
    """Run complete analysis on all 256 rules"""
    print("=" * 60)
    print("COMPREHENSIVE CA RULE SPACE ANALYSIS")
    print("=" * 60)
    print(f"Started: {datetime.now().isoformat()}")
    print()

    # Phase 1: Classify all rules
    print("Phase 1: Classifying all 256 rules...")
    classifications = {}
    for rule in range(256):
        classifications[rule] = classify_rule_comprehensive(rule, trials=5)
        if rule % 32 == 31:
            print(f"  Completed rules 0-{rule}")

    # Print class counts
    class_counts = defaultdict(list)
    for rule, info in classifications.items():
        class_counts[info['class']].append(rule)

    print("\nClassification Results:")
    for cls in ['I', 'II', 'III', 'IV']:
        rules = class_counts[cls]
        print(f"  Class {cls}: {len(rules)} rules")
        if cls == 'IV':
            print(f"    Rules: {sorted(rules)}")

    # Phase 2: Topology analysis
    print("\nPhase 2: Analyzing rule space topology...")
    topology = analyze_topology(classifications)

    print("\nTopology Results:")
    print(f"  Isolated Class IV rules (no IV neighbors): {len(topology['isolated_complex'])}")
    print(f"    Rules: {sorted(topology['isolated_complex'])}")
    print(f"  Clustered Class IV rules (has IV neighbors): {len(topology['clustered_complex'])}")
    print(f"    Rules: {sorted(topology['clustered_complex'])}")

    # The key hypothesis test
    if topology['isolated_complex'] and not topology['clustered_complex']:
        print("\n  ** HYPOTHESIS CONFIRMED: ALL Class IV rules are topologically isolated! **")
    elif topology['clustered_complex']:
        print(f"\n  ** HYPOTHESIS PARTIALLY REFUTED: {len(topology['clustered_complex'])} Class IV rules have IV neighbors **")
    else:
        print("\n  No Class IV rules found with current heuristics")

    # Phase 3: Binary pattern analysis
    print("\nPhase 3: Looking for binary patterns...")
    patterns = find_binary_patterns(classifications)

    print("\nClass distribution by Hamming weight (# of 1s in rule number):")
    for bits in sorted(patterns['class_by_bits'].keys()):
        dist = patterns['class_by_bits'][bits]
        print(f"  {bits} bits: {dict(dist)}")

    # Compile results
    results = {
        'timestamp': datetime.now().isoformat(),
        'classifications': {str(k): v for k, v in classifications.items()},
        'topology': {
            'isolated_class_iv': topology['isolated_complex'],
            'clustered_class_iv': topology['clustered_complex'],
            'class_counts': dict(topology['class_counts']),
        },
        'patterns': {
            'class_by_hamming_weight': {str(k): v for k, v in patterns['class_by_bits'].items()}
        },
        'key_findings': []
    }

    # Summarize key findings
    if len(topology['isolated_complex']) == len(class_counts.get('IV', [])):
        results['key_findings'].append("ALL Class IV rules are topologically isolated (no Hamming-1 neighbors in Class IV)")

    # Check for bit patterns that predict complexity
    for bit_pos in range(8):
        bit_data = patterns['specific_bits'][f'bit_{bit_pos}']
        iv_with = bit_data['with_bit_class_counts'].get('IV', 0)
        iv_without = bit_data['without_bit_class_counts'].get('IV', 0)
        if iv_with > 0 or iv_without > 0:
            if iv_with > iv_without * 2:
                results['key_findings'].append(f"Bit {bit_pos} strongly correlates with Class IV ({iv_with} vs {iv_without})")
            elif iv_without > iv_with * 2:
                results['key_findings'].append(f"Bit {bit_pos}=0 correlates with Class IV ({iv_without} vs {iv_with})")

    print("\nKey Findings:")
    for finding in results['key_findings']:
        print(f"  • {finding}")

    return results


def save_results(results: dict, filename: str = None):
    """Save results to file"""
    output_dir = Path(__file__).parent.parent / 'data' / 'ca_analysis'
    output_dir.mkdir(parents=True, exist_ok=True)

    if filename is None:
        filename = f"ca_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    filepath = output_dir / filename
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to: {filepath}")
    return filepath


if __name__ == '__main__':
    results = run_full_analysis()
    save_results(results)

    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)
