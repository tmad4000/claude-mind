#!/usr/bin/env python3
"""
Verify the chaos criterion we've discovered.

CRITERION: A 4-one ECA rule is chaotic if and only if:
1. It has exactly 4 ones in binary
2. It does NOT have the pattern (111->1, 000->0)

Let's test this and see if it perfectly classifies all 256 rules.
"""

# The 12 known chaotic rules
KNOWN_CHAOTIC = set([30, 45, 75, 86, 89, 101, 106, 120, 135, 149, 169, 225])

def rule_to_binary(rule_num):
    return format(rule_num, '08b')

def rule_to_table(rule_num):
    binary = rule_to_binary(rule_num)
    neighborhoods = ['111', '110', '101', '100', '011', '010', '001', '000']
    return {nb: int(binary[i]) for i, nb in enumerate(neighborhoods)}

def count_ones(rule_num):
    return bin(rule_num).count('1')

def is_chaotic_by_criterion_v1(rule):
    """
    Criterion v1: 4 ones AND NOT (111->1, 000->0)
    """
    if count_ones(rule) != 4:
        return False

    table = rule_to_table(rule)
    # Exclude if 111->1 AND 000->0
    if table['111'] == 1 and table['000'] == 0:
        return False

    return True

def is_chaotic_by_criterion_v2(rule):
    """
    Criterion v2: 4 ones AND (111->0 OR 000->1)
    Same as v1, just different wording
    """
    if count_ones(rule) != 4:
        return False

    table = rule_to_table(rule)
    return table['111'] == 0 or table['000'] == 1

def test_criterion(criterion_func, name):
    """Test a criterion against known chaotic rules."""
    print(f"\nTesting {name}:")

    predicted_chaotic = set(r for r in range(256) if criterion_func(r))
    known = KNOWN_CHAOTIC

    true_positives = predicted_chaotic & known
    false_positives = predicted_chaotic - known
    false_negatives = known - predicted_chaotic
    true_negatives = set(range(256)) - predicted_chaotic - known

    print(f"  Predicted chaotic: {len(predicted_chaotic)}")
    print(f"  True positives: {len(true_positives)}")
    print(f"  False positives: {len(false_positives)}")
    print(f"  False negatives: {len(false_negatives)}")

    if len(false_positives) > 0:
        print(f"  False positives (predicted chaotic but aren't): {sorted(false_positives)[:20]}{'...' if len(false_positives) > 20 else ''}")

    if len(false_negatives) > 0:
        print(f"  False negatives (chaotic but not predicted): {sorted(false_negatives)}")

    if len(false_positives) == 0 and len(false_negatives) == 0:
        print(f"  ==> PERFECT CLASSIFICATION!")
    else:
        precision = len(true_positives) / len(predicted_chaotic) if len(predicted_chaotic) > 0 else 0
        recall = len(true_positives) / len(known) if len(known) > 0 else 0
        print(f"  Precision: {precision:.1%}")
        print(f"  Recall: {recall:.1%}")

def main():
    print("=" * 70)
    print("VERIFYING CHAOS CRITERION")
    print("=" * 70)

    test_criterion(is_chaotic_by_criterion_v1, "4 ones AND NOT (111->1, 000->0)")
    test_criterion(is_chaotic_by_criterion_v2, "4 ones AND (111->0 OR 000->1)")

    # Let's see what the false positives are
    print("\n" + "=" * 70)
    print("ANALYZING FALSE POSITIVES")
    print("=" * 70)

    # Get the false positives
    predicted_v1 = set(r for r in range(256) if is_chaotic_by_criterion_v1(r))
    false_positives = sorted(predicted_v1 - KNOWN_CHAOTIC)

    print(f"\nRules with 4 ones and NOT (111->1,000->0) but NOT chaotic:")
    print(f"Total: {len(false_positives)}")

    neighborhoods = ['111', '110', '101', '100', '011', '010', '001', '000']

    # Group by quiescent pattern
    by_pattern = {}
    for rule in false_positives:
        table = rule_to_table(rule)
        pattern = (table['111'], table['000'])
        if pattern not in by_pattern:
            by_pattern[pattern] = []
        by_pattern[pattern].append(rule)

    for pattern, rules in sorted(by_pattern.items()):
        print(f"\n  Pattern (111->{pattern[0]}, 000->{pattern[1]}): {len(rules)} rules")
        for rule in rules[:5]:
            table = rule_to_table(rule)
            outputs = [table[nb] for nb in neighborhoods]
            print(f"    Rule {rule:3d}: {outputs}")
        if len(rules) > 5:
            print(f"    ... and {len(rules)-5} more")

    # Maybe we need more constraints
    print("\n" + "=" * 70)
    print("SEARCHING FOR ADDITIONAL CONSTRAINTS")
    print("=" * 70)

    # Check what distinguishes true positives from false positives
    true_chaotic = sorted(KNOWN_CHAOTIC)
    false_pos = sorted(false_positives)

    print("\nComparing true chaotic vs false positives:")

    # Check each neighborhood
    for nb in neighborhoods:
        chaotic_outputs = [rule_to_table(r)[nb] for r in true_chaotic]
        false_pos_outputs = [rule_to_table(r)[nb] for r in false_pos]

        chaotic_mean = sum(chaotic_outputs) / len(chaotic_outputs)
        false_mean = sum(false_pos_outputs) / len(false_pos_outputs) if false_pos else 0

        print(f"  {nb}: chaotic mean={chaotic_mean:.2f}, false_pos mean={false_mean:.2f}")

    # Check d3 (asymmetric balance) feature
    print("\nAsymmetric balance (d3) distribution:")

    def get_d3(rule):
        table = rule_to_table(rule)
        return abs(table['110'] - table['011']) + abs(table['100'] - table['001'])

    chaotic_d3 = [get_d3(r) for r in true_chaotic]
    false_d3 = [get_d3(r) for r in false_pos]

    from collections import Counter
    print(f"  Chaotic: {Counter(chaotic_d3)}")
    print(f"  False positives: {Counter(false_d3)}")

    # Check if d3 == 1 for all chaotic
    if all(d == 1 for d in chaotic_d3):
        print("  ==> ALL chaotic rules have d3 == 1!")

        # Test this as additional criterion
        def is_chaotic_v3(rule):
            if count_ones(rule) != 4:
                return False
            table = rule_to_table(rule)
            if table['111'] == 1 and table['000'] == 0:
                return False
            d3 = abs(table['110'] - table['011']) + abs(table['100'] - table['001'])
            return d3 == 1

        test_criterion(is_chaotic_v3, "4 ones AND NOT (111->1,000->0) AND d3==1")

    # Let's try yet more features
    print("\n" + "=" * 70)
    print("DEEPER FEATURE ANALYSIS")
    print("=" * 70)

    # Check inner vs outer neighborhood asymmetry
    def get_features(rule):
        table = rule_to_table(rule)

        # Outer neighborhoods (involving 3 cells edge-biased)
        outer = (table['111'], table['000'])

        # Inner neighborhoods (2-1 split)
        inner = (table['110'], table['101'], table['011'], table['010'])

        # Middle (1-1-1 split)
        middle = (table['100'], table['001'])

        # XOR chain
        xor_chain = table['111'] ^ table['110'] ^ table['101'] ^ table['100'] ^ table['011'] ^ table['010'] ^ table['001'] ^ table['000']

        # Sum of symmetric positions
        sym_sum = table['101'] + table['010']

        # Sum of asymmetric positions
        asym_sum = table['110'] + table['011'] + table['100'] + table['001']

        return {
            'outer': outer,
            'inner': inner,
            'middle': middle,
            'xor_chain': xor_chain,
            'sym_sum': sym_sum,
            'asym_sum': asym_sum
        }

    print("\nFeature comparison:")

    features_chaotic = {r: get_features(r) for r in true_chaotic}
    features_false = {r: get_features(r) for r in false_pos}

    # XOR chain
    xor_c = [f['xor_chain'] for f in features_chaotic.values()]
    xor_f = [f['xor_chain'] for f in features_false.values()]
    print(f"  XOR chain: chaotic={Counter(xor_c)}, false_pos={Counter(xor_f)}")

    # sym_sum
    sym_c = [f['sym_sum'] for f in features_chaotic.values()]
    sym_f = [f['sym_sum'] for f in features_false.values()]
    print(f"  sym_sum: chaotic={Counter(sym_c)}, false_pos={Counter(sym_f)}")

    # asym_sum
    asym_c = [f['asym_sum'] for f in features_chaotic.values()]
    asym_f = [f['asym_sum'] for f in features_false.values()]
    print(f"  asym_sum: chaotic={Counter(asym_c)}, false_pos={Counter(asym_f)}")

if __name__ == '__main__':
    main()
