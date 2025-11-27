#!/usr/bin/env python3
"""
Session 10: Exploring the connection between Collatz and ANF (Algebraic Normal Form)

The CA sessions found that chaos requires specific ANF structure (no x1x3 term in 1D,
no center quadratics in 2D). Can we view Collatz through the same lens?

The Collatz map on binary representations:
- If n is even: n → n/2 (right shift)
- If n is odd: n → 3n+1

Question: What's the ANF of the Collatz function viewed as a Boolean circuit?
"""

import numpy as np
from itertools import product

def collatz_step(n):
    """Single Collatz step"""
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1

def bits_to_int(bits):
    """Convert bit array to integer (LSB first)"""
    return sum(b << i for i, b in enumerate(bits))

def int_to_bits(n, width):
    """Convert integer to bit array (LSB first)"""
    return [(n >> i) & 1 for i in range(width)]

def collatz_circuit(input_bits, output_bit_index, max_width=8):
    """
    View Collatz step as a Boolean function.

    Input: k-bit number
    Output: i-th bit of the result

    We want to understand the structure of this function.
    """
    n = bits_to_int(input_bits)
    if n == 0:
        return 0  # Edge case: 0 stays 0

    result = collatz_step(n)
    result_bits = int_to_bits(result, max_width)

    if output_bit_index < len(result_bits):
        return result_bits[output_bit_index]
    return 0

def build_truth_table(input_width, output_bit):
    """
    Build truth table for Collatz circuit at given output bit.
    """
    table = []
    for bits in product([0, 1], repeat=input_width):
        bits = list(bits)
        output = collatz_circuit(bits, output_bit, input_width + 2)  # +2 for potential growth
        table.append((tuple(bits), output))
    return table

def compute_anf_coefficients(truth_table, n_vars):
    """
    Compute ANF coefficients using Möbius transform.

    f(x) = ⊕_{S ⊆ {0,...,n-1}} a_S · ∏_{i∈S} x_i
    """
    # Build function values array
    f = np.zeros(2**n_vars, dtype=int)
    for bits, val in truth_table:
        idx = sum(b << i for i, b in enumerate(bits))
        f[idx] = val

    # Möbius transform
    anf = f.copy()
    for i in range(n_vars):
        for j in range(2**n_vars):
            if (j >> i) & 1:
                anf[j] ^= anf[j ^ (1 << i)]

    return anf

def index_to_monomial(idx, n_vars):
    """Convert index to monomial string"""
    if idx == 0:
        return "1"
    vars_in_monomial = [f"x{i}" for i in range(n_vars) if (idx >> i) & 1]
    return "·".join(vars_in_monomial)

def analyze_anf_structure(anf, n_vars):
    """Analyze the structure of ANF coefficients"""
    structure = {
        'degree': 0,
        'linear_terms': [],
        'quadratic_terms': [],
        'higher_terms': [],
        'total_terms': 0
    }

    for idx in range(len(anf)):
        if anf[idx]:
            structure['total_terms'] += 1
            degree = bin(idx).count('1')
            structure['degree'] = max(structure['degree'], degree)

            monomial = index_to_monomial(idx, n_vars)
            if degree == 1:
                structure['linear_terms'].append(monomial)
            elif degree == 2:
                structure['quadratic_terms'].append(monomial)
            elif degree > 2:
                structure['higher_terms'].append((degree, monomial))

    return structure

def check_skip_neighbor_pattern(anf, n_vars):
    """
    Check for the CA-like pattern: are there "skip-neighbor" terms?

    In CA, chaos requires no x1x3 term (skip-neighbors).
    In Collatz bits, what pairs are present?
    """
    skip_terms = []
    for i in range(n_vars):
        for j in range(i + 2, n_vars):  # Skip at least one position
            idx = (1 << i) | (1 << j)
            if anf[idx]:
                skip_terms.append(f"x{i}·x{j} (skip={j-i-1})")
    return skip_terms

def print_full_anf(anf, n_vars, name=""):
    """Print the full ANF expression"""
    terms = []
    for idx in range(len(anf)):
        if anf[idx]:
            terms.append(index_to_monomial(idx, n_vars))

    if terms:
        print(f"{name}ANF = " + " ⊕ ".join(terms))
    else:
        print(f"{name}ANF = 0")

# Main analysis
print("=" * 70)
print("COLLATZ MAP AS BOOLEAN CIRCUIT: ANF ANALYSIS")
print("=" * 70)

# Analyze for different input widths
for width in [4, 5, 6]:
    print(f"\n{'='*60}")
    print(f"INPUT WIDTH: {width} bits (numbers 0-{2**width - 1})")
    print(f"{'='*60}")

    for output_bit in range(width + 2):  # Check a few output bits
        print(f"\n--- Output bit {output_bit} ---")

        truth_table = build_truth_table(width, output_bit)
        anf = compute_anf_coefficients(truth_table, width)
        structure = analyze_anf_structure(anf, width)

        print(f"Degree: {structure['degree']}")
        print(f"Total terms: {structure['total_terms']}")
        print(f"Linear: {len(structure['linear_terms'])}")
        print(f"Quadratic: {len(structure['quadratic_terms'])}")

        if width <= 4:  # Only print full ANF for small widths
            print_full_anf(anf, width)

        skip_terms = check_skip_neighbor_pattern(anf, width)
        if skip_terms:
            print(f"Skip-neighbor terms: {skip_terms[:5]}...")  # First 5
        else:
            print("No skip-neighbor quadratic terms!")

# Special focus: The parity relationship
print("\n" + "=" * 70)
print("SPECIAL ANALYSIS: PARITY AND STRUCTURE")
print("=" * 70)

print("\nThe Collatz map has two branches based on LSB (parity):")
print("- Even: n → n/2 (pure shift)")
print("- Odd: n → 3n+1 (multiply then shift)")
print()
print("Let's see how the ANF changes for each branch separately...")

# For odd numbers only
width = 5
print(f"\n--- ODD NUMBERS ONLY (LSB = 1) ---")
odd_table = []
for bits in product([0, 1], repeat=width):
    bits = list(bits)
    if bits[0] == 1:  # LSB = 1 means odd
        n = bits_to_int(bits)
        # 3n+1 for odd n, then look at bit 1 (after the /2)
        result = 3 * n + 1
        output = (result >> 1) & 1  # Bit 1 of 3n+1 (which is bit 0 after /2)
        odd_table.append((tuple(bits), output))

print(f"Analyzing map: n → (3n+1)/2 (Syracuse step)")
print(f"Looking at LSB of result...")

# Build partial truth table (only for odd inputs)
# This requires a different approach since inputs are constrained
# Let's analyze the Syracuse map directly

print("\n--- SYRACUSE MAP ANALYSIS ---")
print("The Syracuse map T(n) = (3n+1)/2 for odd n")

def syracuse_bit_function(n, out_bit):
    """Compute specific output bit of Syracuse map"""
    if n <= 0 or n % 2 == 0:
        return None
    result = (3 * n + 1) // 2
    return (result >> out_bit) & 1

# For small odd numbers, build the mapping
print("\nOdd n → T(n) → binary(T(n))")
for n in range(1, 32, 2):
    t = (3 * n + 1) // 2
    print(f"{n:2d} ({n:05b}) → {t:3d} ({t:08b})")

# Look for algebraic structure
print("\n--- ALGEBRAIC STRUCTURE OF SYRACUSE ---")
print("For odd n, let n = 2m + 1. Then:")
print("  T(n) = (3(2m+1)+1)/2 = (6m+4)/2 = 3m+2")
print()
print("So Syracuse on odd numbers is: n ↦ 3*(n-1)/2 + 2 = (3n+1)/2")
print()
print("In terms of bits:")
print("  n = x0 + 2x1 + 4x2 + ... where x0 = 1 (odd)")
print("  T(n) = 3n/2 + 1/2 = 3n/2 + 1 (rounded down)")
print()

# The key insight: multiplication by 3 in binary
print("--- MULTIPLICATION BY 3 IN BINARY ---")
print("3n = n + 2n = n + (n << 1)")
print("So 3n has carries propagating from LSB upward")
print()
print("The +1 in 3n+1 adds another carry source at LSB")
print("The /2 shifts right, removing LSB")
print()
print("This creates a CARRY CHAIN - information flows from LSB to MSB")
print("Similar to CA information flow!")

# Connection to CA criterion
print("\n" + "=" * 70)
print("CONNECTION TO CA CHAOS CRITERION")
print("=" * 70)
print()
print("CA Chaos: Information must flow THROUGH center (x1x3 = 0 in 1D)")
print("          → No 'shortcuts' that bypass the center")
print()
print("Collatz: Information flows via carry chains from LSB to MSB")
print("         → The 3n operation creates cascading dependencies")
print()
print("Key parallel: Both systems have DIRECTED information flow")
print("  - CA: L → C → R (through center)")
print("  - Collatz: LSB → ... → MSB (through carry chain)")
print()
print("Hypothesis: The 'chaotic' behavior in both systems comes from")
print("            long-range dependencies created by chained operations")
print("            (neighbor interactions in CA, carry propagation in Collatz)")

# Let's quantify the carry chain length
print("\n--- CARRY CHAIN ANALYSIS ---")
print("For n → 3n+1, measure how many bits are affected")

def count_bit_changes(n):
    """Count how many bits change from n to 3n+1"""
    result = 3 * n + 1
    xor = n ^ result
    return bin(xor).count('1')

def count_carry_chain_length(n):
    """Estimate carry chain length in 3n+1"""
    result = 3 * n + 1
    # Carry chain length ~ highest affected bit - lowest affected bit
    xor = n ^ result
    if xor == 0:
        return 0
    highest = xor.bit_length() - 1
    lowest = (xor & -xor).bit_length() - 1
    return highest - lowest + 1

print("\nOdd n → bits changed → carry chain length")
carry_lengths = []
for n in range(1, 100, 2):
    changes = count_bit_changes(n)
    chain = count_carry_chain_length(n)
    carry_lengths.append(chain)
    if n <= 31:
        print(f"{n:2d} → {changes} bits changed, chain length {chain}")

print(f"\nAverage carry chain length (n=1 to 99, odd): {np.mean(carry_lengths):.2f}")
print(f"Max carry chain length: {max(carry_lengths)}")

# Final synthesis
print("\n" + "=" * 70)
print("SYNTHESIS: THE INFORMATION FLOW PRINCIPLE")
print("=" * 70)
print("""
UNIFIED PRINCIPLE discovered across domains:

1. CELLULAR AUTOMATA:
   - Chaos requires NO direct skip-neighbor interaction (1D: x1x3=0)
   - Information must flow THROUGH intermediate cells
   - "Long paths" in the dependency graph

2. COLLATZ CONJECTURE:
   - The 3n+1 operation creates long carry chains
   - Each bit potentially depends on ALL lower bits
   - Information propagates from LSB to MSB

3. COMMON STRUCTURE:
   - Both have DIRECTED information flow
   - Both avoid "shortcuts" that would localize information
   - Both create complex dynamics through chained dependencies

SPECULATIVE CONNECTION:
The Collatz map is "chaotic" in a sense similar to Rule 30/110:
- It mixes bits through long-range dependencies
- The +1 prevents stable patterns from forming
- The /2 removes information from the LSB

The DIFFERENCE from CA:
- CA: Information flows spatially (left-right)
- Collatz: Information flows through bit significance (LSB to MSB)
- CA: Fixed rule everywhere
- Collatz: Rule depends on parity (branch)

Why this matters:
If both CA chaos and Collatz dynamics emerge from the same "long path"
principle, then techniques from Boolean function analysis (ANF, etc.)
might apply to both. The CA work found NECESSARY conditions for chaos.
Can we find NECESSARY conditions for Collatz convergence?
""")
