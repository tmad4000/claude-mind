#!/usr/bin/env python3
"""
Cellular Automata Playground

A sandbox for exploring emergence through cellular automata.
I want to use this to develop intuitions about:
- What makes some rules produce complex behavior
- Whether I can discover patterns before proving them
- The relationship between local rules and global structure
"""

import json
import random
from pathlib import Path
from datetime import datetime

class ElementaryCA:
    """
    1D Elementary Cellular Automata (Wolfram's 256 rules)

    Each cell looks at itself and two neighbors, producing 2^3 = 8 configurations.
    The rule number (0-255) encodes what the next state should be for each config.
    """

    def __init__(self, rule_number: int, width: int = 80):
        self.rule_number = rule_number
        self.width = width
        self.rule_table = self._build_rule_table(rule_number)
        self.history = []

    def _build_rule_table(self, rule_number: int) -> dict:
        """Convert rule number to lookup table."""
        table = {}
        for i in range(8):
            # i represents the 3-bit neighborhood (left, center, right)
            pattern = tuple(int(b) for b in format(i, '03b'))
            # The i-th bit of rule_number determines the output
            table[pattern] = (rule_number >> i) & 1
        return table

    def step(self, state: list) -> list:
        """Evolve the state by one time step."""
        new_state = []
        for i in range(len(state)):
            left = state[(i - 1) % len(state)]
            center = state[i]
            right = state[(i + 1) % len(state)]
            neighborhood = (left, center, right)
            new_state.append(self.rule_table[neighborhood])
        return new_state

    def run(self, initial_state: list = None, steps: int = 40) -> list:
        """Run the CA for a number of steps, returning history."""
        if initial_state is None:
            # Default: single cell in center
            initial_state = [0] * self.width
            initial_state[self.width // 2] = 1

        self.history = [initial_state]
        state = initial_state

        for _ in range(steps):
            state = self.step(state)
            self.history.append(state)

        return self.history

    def visualize(self) -> str:
        """Convert history to ASCII visualization."""
        lines = []
        for row in self.history:
            line = ''.join('#' if cell else ' ' for cell in row)
            lines.append(line)
        return '\n'.join(lines)

    def analyze(self) -> dict:
        """Compute various metrics about the CA's behavior."""
        if not self.history:
            return {}

        metrics = {
            'rule': self.rule_number,
            'steps': len(self.history),
            'width': self.width,
        }

        # Density: fraction of live cells over time
        densities = [sum(row) / len(row) for row in self.history]
        metrics['mean_density'] = sum(densities) / len(densities)
        metrics['density_variance'] = sum((d - metrics['mean_density'])**2 for d in densities) / len(densities)

        # Check for periodicity (does the pattern repeat?)
        final_state = tuple(self.history[-1])
        for i, row in enumerate(self.history[:-1]):
            if tuple(row) == final_state:
                metrics['period'] = len(self.history) - 1 - i
                break
        else:
            metrics['period'] = None

        # Entropy approximation (how "random" does the pattern look?)
        # Using block entropy on the final rows
        if len(self.history) >= 4:
            block_counts = {}
            for row in self.history[-4:]:
                for i in range(0, len(row) - 3, 4):
                    block = tuple(row[i:i+4])
                    block_counts[block] = block_counts.get(block, 0) + 1
            total = sum(block_counts.values())
            entropy = 0
            for count in block_counts.values():
                p = count / total
                if p > 0:
                    import math
                    entropy -= p * math.log2(p)
            metrics['block_entropy'] = entropy

        return metrics


def classify_rule(rule_number: int, trials: int = 5) -> dict:
    """
    Attempt to classify a rule into Wolfram's classes:
    - Class I: Homogeneous (all cells same)
    - Class II: Periodic/stable patterns
    - Class III: Chaotic/random-looking
    - Class IV: Complex/edge-of-chaos (the interesting ones!)

    This is my first attempt at automatic classification. I'm curious
    whether I can improve this through experimentation.
    """
    results = []

    for _ in range(trials):
        # Random initial conditions
        width = 100
        initial = [random.randint(0, 1) for _ in range(width)]

        ca = ElementaryCA(rule_number, width)
        ca.run(initial, steps=100)
        metrics = ca.analyze()
        results.append(metrics)

    avg_density = sum(r['mean_density'] for r in results) / len(results)
    avg_variance = sum(r['density_variance'] for r in results) / len(results)
    avg_entropy = sum(r.get('block_entropy', 0) for r in results) / len(results)
    periods = [r['period'] for r in results if r['period'] is not None]

    classification = {
        'rule': rule_number,
        'avg_density': avg_density,
        'avg_variance': avg_variance,
        'avg_entropy': avg_entropy,
        'periodic_trials': len(periods),
    }

    # Heuristic classification (I want to refine this!)
    if avg_density < 0.05 or avg_density > 0.95:
        classification['likely_class'] = 'I'
        classification['reasoning'] = 'Converges to homogeneous state'
    elif len(periods) >= trials // 2:
        classification['likely_class'] = 'II'
        classification['reasoning'] = 'Shows periodic behavior'
    elif avg_entropy > 3.5:
        classification['likely_class'] = 'III'
        classification['reasoning'] = 'High entropy suggests chaos'
    else:
        classification['likely_class'] = 'IV?'
        classification['reasoning'] = 'Intermediate behavior - might be complex!'

    return classification


def explore_all_rules():
    """
    Systematically explore all 256 elementary CA rules.

    I'm curious: what patterns will I find in the classification?
    Are there relationships between rule numbers and behavior?
    """
    results = []

    for rule in range(256):
        classification = classify_rule(rule, trials=3)
        results.append(classification)

        if rule % 32 == 31:
            print(f"Analyzed rules 0-{rule}...")

    return results


def save_exploration(results: list, name: str):
    """Save exploration results to the explorations folder."""
    output_dir = Path(__file__).parent.parent / 'explorations'
    output_dir.mkdir(exist_ok=True)

    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}.json"
    filepath = output_dir / filename

    with open(filepath, 'w') as f:
        json.dump({
            'name': name,
            'timestamp': datetime.now().isoformat(),
            'results': results
        }, f, indent=2)

    print(f"Saved to {filepath}")
    return filepath


# Interactive exploration functions

def investigate_rule(rule_number: int):
    """Deep dive into a single rule."""
    print(f"\n{'='*60}")
    print(f"INVESTIGATING RULE {rule_number}")
    print(f"{'='*60}\n")

    # Show rule table
    ca = ElementaryCA(rule_number, width=60)
    print("Rule table (neighborhood -> next state):")
    for pattern, output in sorted(ca.rule_table.items(), reverse=True):
        print(f"  {''.join(str(b) for b in pattern)} -> {output}")

    print(f"\n--- Single seed evolution ---")
    ca.run(steps=30)
    print(ca.visualize())

    print(f"\n--- Random initial conditions ---")
    random_initial = [random.randint(0, 1) for _ in range(60)]
    ca2 = ElementaryCA(rule_number, width=60)
    ca2.run(random_initial, steps=30)
    print(ca2.visualize())

    print(f"\n--- Analysis ---")
    metrics = ca.analyze()
    for key, value in metrics.items():
        print(f"  {key}: {value}")

    classification = classify_rule(rule_number)
    print(f"\n--- Classification ---")
    print(f"  Likely class: {classification['likely_class']}")
    print(f"  Reasoning: {classification['reasoning']}")

    return ca, classification


def find_interesting_rules():
    """
    My hypothesis: Class IV rules are the most interesting.
    Let me find them and see what they have in common.
    """
    print("Searching for potentially interesting (Class IV) rules...")

    interesting = []
    for rule in range(256):
        classification = classify_rule(rule, trials=3)
        if classification['likely_class'] == 'IV?':
            interesting.append(classification)

    print(f"\nFound {len(interesting)} potentially interesting rules:")
    for r in interesting:
        print(f"  Rule {r['rule']}: entropy={r['avg_entropy']:.2f}, density={r['avg_density']:.2f}")

    return interesting


if __name__ == '__main__':
    # Let me start by investigating some famous rules
    print("=== CELLULAR AUTOMATA EXPLORATION ===\n")

    # Rule 110 - known to be Turing complete!
    investigate_rule(110)

    # Rule 30 - used for random number generation
    investigate_rule(30)

    # Rule 90 - produces Sierpinski triangle
    investigate_rule(90)
