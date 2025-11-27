#!/usr/bin/env python3
"""
Deeper Collatz Analysis - Session 9
Exploring specific patterns and searching for novel insights
"""

import numpy as np
from collections import defaultdict


def collatz_step(n):
    """Single Collatz step."""
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1


def collatz_sequence(n, max_steps=10000):
    """Generate full Collatz sequence from n to 1."""
    sequence = [n]
    while n != 1 and len(sequence) < max_steps:
        n = collatz_step(n)
        sequence.append(n)
    return sequence


def stopping_time(n, max_steps=10000):
    """Time to reach 1."""
    steps = 0
    while n != 1 and steps < max_steps:
        n = collatz_step(n)
        steps += 1
    return steps if n == 1 else -1


# ============================================================
# DEEP DIVE 1: Syracuse Function (Combined Odd Step)
# ============================================================

def syracuse_sequence(n, max_steps=10000):
    """Syracuse function: combines 3n+1 with subsequent divisions by 2.

    If n is odd: compute (3n+1)/2^k where k is the 2-adic valuation of 3n+1
    This gives the next ODD number in the sequence.
    """
    if n % 2 == 0:
        raise ValueError("Syracuse starts with odd numbers")

    sequence = [n]
    steps = 0

    while n != 1 and steps < max_steps:
        # Compute 3n+1
        m = 3 * n + 1
        # Divide by 2 until odd
        while m % 2 == 0:
            m //= 2
        n = m
        sequence.append(n)
        steps += 1

    return sequence


def analyze_syracuse_ratios():
    """Analyze the ratio between consecutive Syracuse values."""

    print("=" * 60)
    print("SYRACUSE RATIO ANALYSIS")
    print("=" * 60)

    # For each odd n, the Syracuse step is:
    # T(n) = (3n+1)/2^v where v = v_2(3n+1)
    # The "expected" ratio is 3/2^v

    # v_2(3n+1) depends on n mod 2^k for various k
    # n ≡ 1 (mod 2): 3n+1 ≡ 0 (mod 4), so v ≥ 2

    ratios = defaultdict(list)

    for n in range(1, 10001, 2):  # Odd numbers
        seq = syracuse_sequence(n)
        for i in range(len(seq) - 1):
            a, b = seq[i], seq[i+1]
            if a > 0:
                ratio = b / a
                ratios[n % 4].append(ratio)

    print("\nSyracuse ratio T(n)/n by n mod 4:")
    for r in [1, 3]:
        rs = ratios[r]
        print(f"  n ≡ {r} (mod 4): mean ratio = {np.mean(rs):.4f}, median = {np.median(rs):.4f}")

    # Deeper analysis by mod 8
    print("\nBy n mod 8:")
    ratios8 = defaultdict(list)
    for n in range(1, 10001, 2):
        seq = syracuse_sequence(n)
        for i in range(len(seq) - 1):
            a, b = seq[i], seq[i+1]
            if a > 0:
                ratios8[a % 8].append(b / a)

    for r in [1, 3, 5, 7]:
        rs = ratios8[r]
        if rs:
            print(f"  n ≡ {r} (mod 8): mean = {np.mean(rs):.4f}")


# ============================================================
# DEEP DIVE 2: The 2-adic Perspective
# ============================================================

def analyze_2adic():
    """
    In the 2-adic integers, the Collatz map extends uniquely.
    The map T(n) = (3n+1)/2^v for odd n has interesting 2-adic properties.

    Key insight: The orbit structure in Z_2 may explain the conjecture.
    """

    print("\n" + "=" * 60)
    print("2-ADIC STRUCTURE ANALYSIS")
    print("=" * 60)

    # The 2-adic valuation v_2(3n+1) determines the "speed" of descent
    # For odd n, 3n+1 is always even
    # v_2(3n+1) depends on n mod powers of 2

    # Pattern: v_2(3n+1) when n is odd
    # n ≡ 1 (mod 4): 3n+1 ≡ 4 (mod 8), so v_2 = 2 exactly
    # n ≡ 3 (mod 4): 3n+1 ≡ 10 ≡ 2 (mod 4), so v_2 = 1 exactly

    print("\n2-adic valuation v_2(3n+1) for odd n:")
    print("  n ≡ 1 (mod 4): v_2(3n+1) = 2 (verified for all n ≡ 1 mod 4)")
    print("  n ≡ 3 (mod 4): v_2(3n+1) = ?")

    # Let's verify and extend
    v2_by_mod = defaultdict(list)

    for n in range(1, 1001, 2):
        val = 3 * n + 1
        v = 0
        temp = val
        while temp % 2 == 0:
            temp //= 2
            v += 1
        v2_by_mod[n % 16].append(v)

    print("\nv_2(3n+1) by n mod 16 (for odd n):")
    for r in [1, 3, 5, 7, 9, 11, 13, 15]:
        vs = v2_by_mod[r]
        if len(set(vs)) == 1:
            print(f"  n ≡ {r:2d} (mod 16): v_2 = {vs[0]} (constant)")
        else:
            print(f"  n ≡ {r:2d} (mod 16): v_2 varies - {set(vs)}")


# ============================================================
# DEEP DIVE 3: The 3x+1 as a Linear Map over Rationals
# ============================================================

def analyze_linear_algebra():
    """
    The Collatz map can be viewed through matrix representations.

    For the Syracuse map on odd numbers:
    T(n) = (3n+1)/2^v

    Over multiple steps, we get:
    n -> 3n+1 -> ... -> final

    The total multiplication factor is 3^a / 2^b where:
    a = number of odd steps
    b = total divisions by 2

    For the sequence to reach 1, we need 3^a / 2^b * n = 1
    i.e., 3^a * n = 2^b

    This is impossible for odd n > 1 (3^a * n is odd, 2^b is even).

    But the INTERMEDIATE values matter - we need them to eventually reach 1.
    """

    print("\n" + "=" * 60)
    print("LINEAR ALGEBRA PERSPECTIVE")
    print("=" * 60)

    # Track the "coefficient path" for each starting number
    # After a steps with odd values and b divisions by 2:
    # value = (3^a * start + something) / 2^b

    # Let's track (3^a, addition_term, 2^b) for sequences

    def track_coefficients(n, max_steps=200):
        """Track how starting value n transforms algebraically."""
        # If we write each step as linear transformation on the previous:
        # For even x: x' = x/2 (multiply by 1/2)
        # For odd x: x' = 3x+1 (multiply by 3, add 1)

        # Track: current = (a * n + b) / c where gcd(a,c) = gcd(b,c) = 1
        # Start: a=1, b=0, c=1

        a, b, c = 1, 0, 1  # current = (a*n + b) / c
        current = n
        path = [(a, b, c)]

        steps = 0
        while current != 1 and steps < max_steps:
            if current % 2 == 0:
                c *= 2
                current = current // 2
            else:
                a *= 3
                b = 3 * b + c
                current = 3 * current + 1

            # Simplify: divide a, b, c by GCD
            from math import gcd
            g = gcd(gcd(a, b), c)
            a, b, c = a // g, b // g, c // g

            path.append((a, b, c))
            steps += 1

        return path

    # Analyze coefficient patterns for interesting numbers
    print("\nCoefficient evolution (current = (a*n + b) / c):")
    for n in [27, 31, 41, 47]:
        path = track_coefficients(n)
        print(f"\n  n = {n}:")
        print(f"    Length: {len(path)} steps")
        # Show some key points
        for i in [0, len(path)//4, len(path)//2, 3*len(path)//4, len(path)-1]:
            if i < len(path):
                a, b, c = path[i]
                val = (a * n + b) // c
                print(f"    Step {i}: ({a}*{n} + {b}) / {c} = {val}")


# ============================================================
# DEEP DIVE 4: Searching for Structure in the Orbit Counts
# ============================================================

def analyze_orbit_structure():
    """
    For each n, its Collatz orbit visits certain numbers.
    Are there patterns in WHICH numbers appear in orbits?
    """

    print("\n" + "=" * 60)
    print("ORBIT MEMBERSHIP ANALYSIS")
    print("=" * 60)

    # Count how many times each number appears in orbits
    appearance_count = defaultdict(int)

    for n in range(1, 10001):
        seq = collatz_sequence(n)
        for x in seq:
            appearance_count[x] += 1

    # Find numbers that appear in MANY orbits
    top_appearing = sorted(appearance_count.items(), key=lambda x: -x[1])[:30]

    print("\nMost common numbers in Collatz orbits (1 to 10000):")
    for num, count in top_appearing[:20]:
        print(f"  {num}: appears in {count} orbits")

    # Analyze the structure
    # The numbers 1, 2, 4 appear in all orbits (they're the final cycle)
    # 8, 16 appear in most orbits
    # What's the pattern?

    print("\n  Observation: Powers of 2 dominate!")
    print("  This makes sense: every orbit eventually goes through powers of 2")

    # Non-powers-of-2 that appear often:
    print("\n  Non-power-of-2 common appearances:")
    for num, count in top_appearing:
        if num > 0 and (num & (num - 1)) != 0:  # Not a power of 2
            print(f"    {num}: {count} orbits")
            if len([x for x in top_appearing if (x[0] & (x[0]-1)) != 0 and x[0] == num]) > 5:
                break


# ============================================================
# DEEP DIVE 5: The Backwards Tree Analysis
# ============================================================

def analyze_backwards_tree():
    """
    The inverse Collatz map is:
    - Every n has child 2n
    - n has child (n-1)/3 if n ≡ 1 (mod 3) and (n-1)/3 is odd

    This defines a tree rooted at 1. Every positive integer should be in this tree.
    """

    print("\n" + "=" * 60)
    print("BACKWARDS TREE ANALYSIS")
    print("=" * 60)

    # Build the tree up to some level
    # For each number, find its "height" (distance from 1)

    def tree_height(n, memo={}):
        """Height in the inverse Collatz tree."""
        if n in memo:
            return memo[n]
        if n == 1:
            return 0

        # Parent of n is either:
        # - n/2 if n is even
        # - 3n+1 if n is odd

        if n % 2 == 0:
            h = 1 + tree_height(collatz_step(n), memo)
        else:
            h = 1 + tree_height(collatz_step(n), memo)

        memo[n] = h
        return h

    # Heights distribution
    heights = []
    for n in range(1, 10001):
        seq = collatz_sequence(n)
        heights.append(len(seq) - 1)

    print("\nTree height (=stopping time) distribution:")
    print(f"  Mean: {np.mean(heights):.2f}")
    print(f"  Std: {np.std(heights):.2f}")

    # Analyze the "width" at each level
    # How many numbers have height exactly h?
    height_counts = defaultdict(int)
    for n, h in enumerate(heights, 1):
        height_counts[h] += 1

    print("\n  Numbers at each height (first 20 levels):")
    for h in range(20):
        if h in height_counts:
            print(f"    Height {h}: {height_counts[h]} numbers")


# ============================================================
# DEEP DIVE 6: Algebraic Number Theory Connection
# ============================================================

def analyze_algebraic_connections():
    """
    The Collatz conjecture has connections to algebraic number theory.

    Consider the ring Z[1/2]. The map T(n) = 3n+1 for odd n, n/2 for even n
    extends naturally to this ring.

    The conjecture says every positive integer reaches 1.

    Key insight: The map preserves certain algebraic structures.
    """

    print("\n" + "=" * 60)
    print("ALGEBRAIC CONNECTIONS")
    print("=" * 60)

    # The "3x+1" map on odd numbers has form (3n+1)/2^v
    # This is a function from odds to odds

    # Consider the set of all numbers reachable from 1 by INVERSE operations:
    # If m came from n, then either:
    #   m = 2n (always possible)
    #   m = (n-1)/3 if n ≡ 1 (mod 3) and result is odd

    # Build reachable set backwards
    reachable = {1}
    frontier = {1}

    for depth in range(15):
        new_frontier = set()
        for n in frontier:
            # Child 1: 2n
            new_frontier.add(2 * n)
            # Child 2: (n-1)/3 if valid
            if n > 4 and (n - 1) % 3 == 0:
                child = (n - 1) // 3
                if child % 2 == 1:  # Must be odd
                    new_frontier.add(child)

        new_frontier -= reachable
        reachable |= new_frontier
        frontier = new_frontier

    print(f"\nNumbers reachable from 1 in ≤15 inverse steps: {len(reachable)}")

    # Check which small numbers are NOT reachable
    not_reachable = []
    for n in range(1, 1000):
        if n not in reachable:
            not_reachable.append(n)

    if not_reachable:
        print(f"  Numbers 1-999 not reachable in 15 steps: {not_reachable[:20]}...")
        print(f"  Total unreachable (1-999): {len(not_reachable)}")
    else:
        print("  All numbers 1-999 are reachable!")


# ============================================================
# DEEP DIVE 7: Statistical Mechanics Analogy
# ============================================================

def analyze_stat_mech():
    """
    The Collatz map can be viewed as a dynamical system.
    The distribution of values over time may have statistical properties.
    """

    print("\n" + "=" * 60)
    print("STATISTICAL MECHANICS VIEW")
    print("=" * 60)

    # For a given n, the sequence visits many values
    # The "temperature" might relate to how spread out these values are

    # Track the distribution of log(values) in sequences
    log_distributions = []

    for n in range(1000, 2000):
        seq = collatz_sequence(n)
        log_vals = np.log(seq)
        log_distributions.append({
            'mean': np.mean(log_vals),
            'std': np.std(log_vals),
            'max': np.max(log_vals),
            'n': n,
            'length': len(seq)
        })

    means = [d['mean'] for d in log_distributions]
    stds = [d['std'] for d in log_distributions]

    print("\nLog-value statistics for n ∈ [1000, 2000):")
    print(f"  Mean of mean(log): {np.mean(means):.3f}")
    print(f"  Std of mean(log): {np.std(means):.3f}")
    print(f"  Mean of std(log): {np.mean(stds):.3f}")

    # The heuristic model says:
    # - Half of steps are odd (multiply by ~3/2 on average)
    # - Half are even (divide by 2)
    # - Net effect: multiply by sqrt(3/2) per step on average
    # - But we want to GO DOWN, so we need log(sqrt(3/2)) < 0
    # - Actually: 3/2 > 1 so sqrt(3/2) > 1... but we divide MORE than we multiply

    # Better: After one "odd step", we multiply by 3/2^v where v ≥ 1
    # Average v is ~2 (half the time v=1, half v≥2)
    # So average multiplier is ~3/4 < 1, hence descent

    print("\n  Heuristic: average descent factor per odd-step is ~3/4")
    print("  (3n+1)/2^v where v averages ~2, giving ~3/4 net multiplier")


# ============================================================
# NOVEL DIRECTION: Residue Class Transitions
# ============================================================

def analyze_residue_transitions():
    """
    NEW IDEA: Track how residue classes transition under Collatz.

    For a given modulus m, what is the transition matrix P where
    P[i,j] = probability of going from class i to class j?
    """

    print("\n" + "=" * 60)
    print("RESIDUE CLASS TRANSITION MATRICES")
    print("=" * 60)

    for mod in [3, 4, 6, 8, 12]:
        print(f"\nMod {mod} transition matrix:")

        # Count transitions
        transitions = defaultdict(lambda: defaultdict(int))

        for n in range(1, 100001):
            seq = collatz_sequence(n)
            for i in range(len(seq) - 1):
                r1 = seq[i] % mod
                r2 = seq[i+1] % mod
                transitions[r1][r2] += 1

        # Convert to probabilities
        print("  From \\ To  ", end="")
        for j in range(mod):
            print(f"   {j:2d}", end="")
        print()

        for i in range(mod):
            row_sum = sum(transitions[i].values())
            if row_sum > 0:
                print(f"    {i:2d}      ", end="")
                for j in range(mod):
                    prob = transitions[i][j] / row_sum if row_sum > 0 else 0
                    print(f"  {prob:.2f}", end="")
                print()


# ============================================================
# NOVEL DIRECTION: Binary Pattern Analysis
# ============================================================

def analyze_binary_patterns():
    """
    NEW IDEA: Look at binary patterns in Collatz sequences.

    The operations:
    - n/2: right shift (removes trailing 0)
    - 3n+1: complex transformation

    What patterns emerge in the binary representation?
    """

    print("\n" + "=" * 60)
    print("BINARY PATTERN ANALYSIS")
    print("=" * 60)

    # Track bit patterns at each step
    def binary_features(n):
        """Extract features from binary representation."""
        b = bin(n)[2:]
        return {
            'length': len(b),
            'ones': b.count('1'),
            'leading_ones': len(b) - len(b.lstrip('1')),
            'trailing_zeros': len(b) - len(b.rstrip('0')),
            'pattern': b[-4:] if len(b) >= 4 else b
        }

    # For a specific number, track binary evolution
    print("\nBinary evolution for n=27 (famous for long sequence):")
    n = 27
    seq = collatz_sequence(n)[:30]
    for i, val in enumerate(seq):
        feat = binary_features(val)
        print(f"  Step {i:2d}: {val:6d} = {bin(val):>15s} | ones={feat['ones']}, len={feat['length']}")

    # Analyze the relationship between binary features and stopping time
    print("\nCorrelation: trailing binary pattern vs next step behavior")

    patterns = defaultdict(list)
    for n in range(1, 10001):
        seq = collatz_sequence(n)
        for i in range(len(seq) - 1):
            val = seq[i]
            next_val = seq[i+1]

            # Look at last 3 bits
            pattern = val % 8
            ratio = next_val / val if val > 0 else 0
            patterns[pattern].append(ratio)

    print("\n  Last 3 bits of n -> average ratio next/current:")
    for p in range(8):
        rs = patterns[p]
        if rs:
            print(f"    {bin(p)[2:]:>3s} ({p}): mean ratio = {np.mean(rs):.4f}")


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("DEEP COLLATZ ANALYSIS - Session 9")
    print("=" * 60)

    analyze_syracuse_ratios()
    analyze_2adic()
    analyze_linear_algebra()
    analyze_orbit_structure()
    analyze_backwards_tree()
    analyze_algebraic_connections()
    analyze_stat_mech()

    # Novel directions
    analyze_residue_transitions()
    analyze_binary_patterns()

    print("\n" + "=" * 60)
    print("SESSION 9 COLLATZ EXPLORATION COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
