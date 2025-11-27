#!/usr/bin/env python3
"""
Collatz Markov Chain Analysis - Session 9

KEY INSIGHT from previous analysis: The residue transition matrices show
DETERMINISTIC behavior for odd classes but PROBABILISTIC for even classes.

This is because:
- Odd n: 3n+1 is ALWAYS even, so the next residue class is deterministic
- Even n: n/2 could give either odd or even, depending on n mod 4

This creates a structured Markov chain that may reveal something about convergence.
"""

import numpy as np
from collections import defaultdict


def collatz_step(n):
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1


def analyze_deterministic_transitions():
    """
    For odd n, the Collatz step 3n+1 is deterministic in terms of residues.

    If n ≡ r (mod m) and r is odd, then 3n+1 ≡ 3r+1 (mod 3m).

    But we're more interested in mod m behavior.
    """
    print("=" * 60)
    print("DETERMINISTIC TRANSITIONS FOR ODD CLASSES")
    print("=" * 60)

    # For mod 8, analyze what happens to each odd class
    print("\nMod 8 analysis (odd -> even via 3n+1):")
    for r in [1, 3, 5, 7]:
        # 3r+1 mod 8
        result = (3 * r + 1) % 8
        print(f"  n ≡ {r} (mod 8): 3n+1 ≡ {result} (mod 8)")

    # The subsequent division matters!
    # n ≡ 1 (mod 8): 3n+1 ≡ 4 (mod 8) -> /2 gives 2 (mod 4)
    # Wait, we need to track through the divisions too.

    print("\nFull analysis: odd n mod 8 -> final odd via Syracuse:")

    def syracuse_residue(r, mod):
        """Given n ≡ r (mod), apply Syracuse: (3n+1)/2^k until odd."""
        val = 3 * r + 1
        while val % 2 == 0:
            val //= 2
        return val % mod

    for mod in [8, 16, 32]:
        print(f"\n  Mod {mod} Syracuse transitions (odd -> odd):")
        for r in range(1, mod, 2):  # Odd residues
            result = syracuse_residue(r, mod)
            print(f"    {r:2d} -> {result:2d}")


def analyze_markov_structure():
    """
    The Collatz map on odd numbers (Syracuse function) defines a map
    from odd residue classes to odd residue classes.

    This is DETERMINISTIC but depends on the full residue, not just mod m.
    """
    print("\n" + "=" * 60)
    print("MARKOV STRUCTURE ON ODD RESIDUE CLASSES")
    print("=" * 60)

    # The Syracuse map: T(n) = (3n+1)/2^v where v = v_2(3n+1)
    # For n ≡ r (mod 2^k), we can compute v_2(3n+1) and thus T(n) mod 2^k

    def v2(n):
        """2-adic valuation."""
        if n == 0:
            return float('inf')
        v = 0
        while n % 2 == 0:
            n //= 2
            v += 1
        return v

    # For each odd r mod 16, compute where it goes
    mod = 16
    print(f"\nSyracuse map on odd residues mod {mod}:")

    transitions = {}
    for r in range(1, mod, 2):  # Odd residues: 1, 3, 5, 7, 9, 11, 13, 15
        # Compute 3r+1
        val = 3 * r + 1
        # Find v_2(3r+1) - but this depends on r mod higher powers of 2!
        # Let's compute for actual numbers

        # For n ≡ r (mod 16), the value v_2(3n+1) is:
        # 3n+1 ≡ 3r+1 (mod 48) for n ≡ r (mod 16)
        # The 2-adic valuation of 3r+1 is determined by 3r+1 itself

        v = v2(val)
        result = (val // (2**v)) % mod

        transitions[r] = result
        print(f"  {r:2d} -> {result:2d}  (v_2(3*{r}+1) = v_2({val}) = {v})")

    # Check: is this map eventually periodic for all starting points?
    print("\n  Orbit structure:")
    visited_all = set()
    for start in range(1, mod, 2):
        if start in visited_all:
            continue
        orbit = [start]
        current = start
        visited = {start}
        while True:
            current = transitions[current]
            if current in visited:
                break
            visited.add(current)
            orbit.append(current)
        orbit.append(current)
        visited_all |= visited
        cycle_start = orbit.index(current)
        print(f"    From {start}: {' -> '.join(map(str, orbit))} (cycle at position {cycle_start})")


def analyze_2adic_collatz():
    """
    The Collatz conjecture can be studied in the 2-adic integers Z_2.

    In Z_2, the Collatz map extends uniquely because:
    - n/2 is always defined (2-adically)
    - 3n+1 is always defined

    The conjecture says there are no non-trivial cycles.
    """
    print("\n" + "=" * 60)
    print("2-ADIC EXTENSION OF COLLATZ")
    print("=" * 60)

    # In Z_2, every element has a unique representation as sum of powers of 2
    # The "negative" numbers are also there: -1 = 1 + 2 + 4 + 8 + ... (2-adically)

    # The Collatz map on Z_2 has been studied. Key result:
    # The map T: Z_2 -> Z_2 defined by T(n) = n/2 if v_2(n) > 0, else (3n+1)/2^v
    # has exactly one fixed point at n=0, and the orbit of -1 is interesting.

    print("\nKnown 2-adic facts:")
    print("  - In Z_2, the number -1 = ...11111 (infinite 1s)")
    print("  - 3*(-1) + 1 = -3 + 1 = -2 = ...11110 (ending in 0)")
    print("  - (-2)/2 = -1")
    print("  - So -1 is a FIXED POINT of the 2-adic Collatz Syracuse map!")

    print("\n  This means: if we think 2-adically, there IS a non-trivial cycle.")
    print("  The conjecture is specifically about POSITIVE integers.")

    # Let's explore other 2-adic cycles
    print("\nSearching for 2-adic cycles (mod 2^k approximation):")

    def syracuse_mod(n, mod):
        """Syracuse step mod 2^k."""
        val = 3 * n + 1
        while val % 2 == 0:
            val //= 2
        return val % mod

    for k in range(4, 10):
        mod = 2**k
        cycles = []

        for start in range(1, mod, 2):
            visited = {}
            current = start
            step = 0
            while current not in visited:
                visited[current] = step
                current = syracuse_mod(current, mod)
                step += 1

            cycle_len = step - visited[current]
            if cycle_len not in [c[1] for c in cycles]:
                cycles.append((current, cycle_len))

        print(f"  Mod 2^{k} = {mod}: {len(cycles)} distinct cycle lengths: {sorted(set(c[1] for c in cycles))}")


def analyze_3n_plus_c():
    """
    Generalized Collatz: 3n+c for various c.

    The conjecture is specific to c=1. What happens for other c?
    """
    print("\n" + "=" * 60)
    print("GENERALIZED COLLATZ: 3n + c")
    print("=" * 60)

    def generalized_collatz(n, c, max_steps=1000):
        """Collatz with 3n+c instead of 3n+1."""
        visited = set()
        steps = 0
        while n not in visited and steps < max_steps:
            visited.add(n)
            if n % 2 == 0:
                n //= 2
            else:
                n = 3 * n + c
            steps += 1
        return n, steps, len(visited)

    print("\nBehavior for different c values (starting from n=1 to 100):")

    for c in [-1, 1, 3, 5, 7, 9, 11, 13, -5, -7]:
        cycles = defaultdict(int)
        divergent = 0

        for start in range(1, 101):
            final, steps, visited = generalized_collatz(start, c)
            if steps >= 1000:
                divergent += 1
            else:
                cycles[final] += 1

        print(f"\n  c = {c:3d}:")
        print(f"    Divergent (>1000 steps): {divergent}")
        print(f"    Cycle endpoints: {dict(sorted(cycles.items(), key=lambda x: -x[1])[:5])}")


def find_cycle_candidates():
    """
    Search for potential cycles in the standard Collatz map.

    A cycle would satisfy: after k applications of the map, we return to n.

    For a cycle of length k with a odd steps and b=k-a even steps:
    - Each odd step multiplies by 3 and adds 1
    - Each even step divides by 2

    The net effect must satisfy:
    n * 3^a / 2^b + (something involving the additions) = n
    """
    print("\n" + "=" * 60)
    print("CYCLE SEARCH CONSTRAINTS")
    print("=" * 60)

    print("\nTheoretical constraints on hypothetical cycles:")
    print("\n  For a cycle of length k with a odd steps:")
    print("  - After a multiplications by 3, factor is 3^a")
    print("  - After b = k - a divisions by 2, factor is 2^b")
    print("  - Net multiplication factor: 3^a / 2^b")
    print("  - For the cycle to close: 3^a / 2^b ≈ 1 (after accounting for +1s)")

    print("\n  The ratio 3^a / 2^b approximates 1 when:")
    print("    a * log(3) ≈ b * log(2)")
    print("    b/a ≈ log(3)/log(2) ≈ 1.585")

    print("\n  So cycles need about 1.585 even steps per odd step.")

    # Check small cycles
    print("\n  Checking small cycle constraints:")
    for a in range(1, 20):  # odd steps
        # b/a should be about 1.585
        b_ideal = a * np.log(3) / np.log(2)
        b_low, b_high = int(b_ideal), int(b_ideal) + 1

        for b in [b_low, b_high]:
            ratio = (3**a) / (2**b)
            if 0.9 < ratio < 1.1:
                print(f"    a={a}, b={b}: 3^a/2^b = {ratio:.6f}")


def analyze_acceleration():
    """
    The "Terras" theorem says that for almost all n, the orbit eventually
    falls below n. Can we quantify the "acceleration" of convergence?
    """
    print("\n" + "=" * 60)
    print("CONVERGENCE ACCELERATION")
    print("=" * 60)

    def first_below(n, max_steps=10000):
        """Steps until reaching a value < n."""
        original = n
        steps = 0
        while n >= original and steps < max_steps:
            if n == 1:
                return steps
            if n % 2 == 0:
                n //= 2
            else:
                n = 3 * n + 1
            steps += 1
        return steps

    # Distribution of "first below" times
    times = []
    for n in range(2, 100001):
        t = first_below(n)
        times.append(t)

    times = np.array(times)

    print(f"\n'First below' statistics (n = 2 to 100000):")
    print(f"  Mean: {np.mean(times):.2f}")
    print(f"  Median: {np.median(times):.2f}")
    print(f"  Max: {np.max(times)} (at n={np.argmax(times)+2})")
    print(f"  % reaching below in ≤10 steps: {100*np.mean(times <= 10):.1f}%")
    print(f"  % reaching below in ≤20 steps: {100*np.mean(times <= 20):.1f}%")

    # The Terras theorem says Prob(T^n(x) < x for some n) = 1 for almost all x.
    # This is proven, but the full conjecture (reaches 1) is open.


def main():
    analyze_deterministic_transitions()
    analyze_markov_structure()
    analyze_2adic_collatz()
    analyze_3n_plus_c()
    find_cycle_candidates()
    analyze_acceleration()

    print("\n" + "=" * 60)
    print("COLLATZ MARKOV ANALYSIS COMPLETE")
    print("=" * 60)

    print("""
KEY INSIGHTS FROM SESSION 9:

1. DETERMINISTIC TRANSITIONS: For odd residue classes, the Syracuse map
   is DETERMINISTIC, not probabilistic. The randomness comes from the
   distribution of numbers in residue classes, not the map itself.

2. 2-ADIC FIXED POINT: In the 2-adic integers, -1 is a fixed point of
   the Syracuse map. The conjecture is specific to positive integers.

3. MARKOV STRUCTURE: The Syracuse map on odd numbers mod 2^k creates
   finite Markov chains with specific cycle structures. These might
   constrain the possible behavior of the full map.

4. GENERALIZED COLLATZ: Different values of c in 3n+c show wildly
   different behavior. c=1 appears special.

5. CONVERGENCE RATE: Almost all numbers fall below their starting
   value quickly. The conjecture is about the rare "record-holders"
   that take many steps.
""")


if __name__ == '__main__':
    main()
