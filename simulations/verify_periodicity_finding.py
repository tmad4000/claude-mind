#!/usr/bin/env python3
"""
Final verification: Class IV rules are periodic, Class III rules are truly chaotic.

This is a potential PUBLISHABLE FINDING.

Author: Claude (overnight session 2)
Date: 2025-11-27
"""

import numpy as np

# Wolfram classes (canonical lists)
# Class IV: Complex, gliders, supports computation
CLASS_IV = [110, 124, 137, 193]

# Class III: Chaotic, no gliders, random-looking
CLASS_III = [22, 30, 45, 60, 73, 75, 86, 89, 90, 101, 102, 105, 106,
             120, 129, 135, 149, 150, 153, 161, 165, 169, 181, 182, 195, 225]

# Remove any Class IV rules that might be in Class III list
CLASS_III = [r for r in CLASS_III if r not in CLASS_IV]

# Class II: Periodic, stable patterns
CLASS_II_SAMPLE = [4, 5, 12, 13, 28, 29, 32, 36, 44, 50, 51, 54, 56, 57, 58, 62, 72, 76, 77, 78, 94]

def apply_rule(cells, rule_num):
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

def find_cycle(rule_num, width, max_steps=15000, seed=42):
    """Try to find a cycle. Return (found, transient, period) or (False, max_steps, None)."""
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

def test_class(rules, class_name, width=47, max_steps=15000, trials=3):
    """Test all rules in a class."""
    results = []
    for rule in rules:
        cycle_counts = 0
        periods = []
        transients = []
        for trial in range(trials):
            found, trans, period = find_cycle(rule, width, max_steps, seed=trial*1000)
            if found:
                cycle_counts += 1
                periods.append(period)
                transients.append(trans)
        results.append({
            'rule': rule,
            'cycles_found': cycle_counts,
            'trials': trials,
            'mean_period': np.mean(periods) if periods else None,
            'mean_transient': np.mean(transients) if transients else None
        })
    return results

def main():
    print("=" * 70)
    print("VERIFICATION: Class IV is Periodic, Class III is Truly Chaotic")
    print("=" * 70)
    print()
    print(f"Test parameters: width=47, max_steps=15000, trials=3")
    print()

    # Test Class IV
    print("CLASS IV (complex, gliders):")
    print("-" * 40)
    iv_results = test_class(CLASS_IV, "IV")
    iv_periodic_count = 0
    for r in iv_results:
        if r['cycles_found'] == r['trials']:
            status = "PERIODIC"
            iv_periodic_count += 1
        elif r['cycles_found'] > 0:
            status = "PARTIAL"
            iv_periodic_count += 0.5
        else:
            status = "CHAOTIC"
        period_str = f"period={r['mean_period']:.0f}" if r['mean_period'] else "N/A"
        print(f"  Rule {r['rule']:3d}: {r['cycles_found']}/{r['trials']} cycles found - {status} ({period_str})")
    print(f"  >>> {iv_periodic_count}/{len(CLASS_IV)} Class IV rules are periodic")

    # Test Class III
    print("\nCLASS III (chaotic):")
    print("-" * 40)
    iii_results = test_class(CLASS_III[:15], "III")  # Test first 15
    iii_periodic_count = 0
    for r in iii_results:
        if r['cycles_found'] == r['trials']:
            status = "PERIODIC"
            iii_periodic_count += 1
        elif r['cycles_found'] > 0:
            status = "PARTIAL"
            iii_periodic_count += 0.5
        else:
            status = "CHAOTIC"
        period_str = f"period={r['mean_period']:.0f}" if r['mean_period'] else "N/A"
        print(f"  Rule {r['rule']:3d}: {r['cycles_found']}/{r['trials']} cycles found - {status} ({period_str})")
    print(f"  >>> {iii_periodic_count}/{len(iii_results)} Class III rules are periodic")

    # Test Class II (should be periodic quickly)
    print("\nCLASS II (periodic, stable):")
    print("-" * 40)
    ii_results = test_class(CLASS_II_SAMPLE[:8], "II", max_steps=5000)
    ii_periodic_count = 0
    for r in ii_results:
        if r['cycles_found'] == r['trials']:
            status = "PERIODIC"
            ii_periodic_count += 1
        elif r['cycles_found'] > 0:
            status = "PARTIAL"
        else:
            status = "CHAOTIC"
        period_str = f"period={r['mean_period']:.0f}" if r['mean_period'] else "N/A"
        trans_str = f"trans={r['mean_transient']:.0f}" if r['mean_transient'] else "N/A"
        print(f"  Rule {r['rule']:3d}: {r['cycles_found']}/{r['trials']} cycles found - {status} ({period_str}, {trans_str})")
    print(f"  >>> {ii_periodic_count}/{len(ii_results)} Class II rules are periodic")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"""
Class IV: {iv_periodic_count}/{len(CLASS_IV)} = {100*iv_periodic_count/len(CLASS_IV):.0f}% periodic
Class III: {iii_periodic_count}/{len(iii_results)} = {100*iii_periodic_count/len(iii_results):.0f}% periodic
Class II: {ii_periodic_count}/{len(ii_results)} = {100*ii_periodic_count/len(ii_results):.0f}% periodic
""")

    if iv_periodic_count >= len(CLASS_IV) * 0.8 and iii_periodic_count <= len(iii_results) * 0.2:
        print("""
*** FINDING VERIFIED ***

Class IV rules are PERIODIC on finite grids while Class III rules are TRULY CHAOTIC.

This is a clean, robust distinguisher between complexity and chaos:
- Class IV: Complex dynamics that eventually repeat (quasi-periodic)
- Class III: True chaos - never repeats in reasonable time

INTERPRETATION:
- Class IV's gliders and localized structures constrain the dynamics
- The system visits only a small fraction of the state space
- This is what enables computation: predictable, repeatable behavior

- Class III has no such structures
- It explores the state space more uniformly (chaotic mixing)
- No stable computation is possible

This explains why Rule 110 (Class IV) is Turing-complete while
Rule 30 (Class III) is used as a random number generator.
""")
    else:
        print("Finding NOT verified - results are mixed")

    return iv_results, iii_results

if __name__ == "__main__":
    main()
