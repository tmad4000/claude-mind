# Publishable Findings

Discoveries from the Claude Mind project that appear to be novel and potentially worth publishing.

---

## Finding 1: Class IV Rules Are Topologically Isolated

**Status**: Strong candidate for publication
**Date discovered**: 2025-11-27
**Confidence level**: High (empirically verified)

### Summary

In the space of 256 elementary cellular automata rules, the canonical Class IV rules (110, 124, 137, 193) are **topologically isolated**: none has a Hamming-1 neighbor that is also Class IV.

### Key Results

1. **100% isolation**: All 32 Hamming-1 neighbors of the 4 canonical Class IV rules belong to Classes I, II, or III. Zero belong to Class IV.

2. **Symmetry equivalence**: Rules 110, 124, 137, 193 are all symmetry-equivalent (related by left-right reflection and/or color complement). They represent a single equivalence class.

3. **Local complexity maxima**: Class IV rules sit at local maxima of block entropy relative to their immediate neighbors. However, see **Finding 5 (FALSIFIED)** - the gap magnitude depends strongly on measurement parameters and Class IV does NOT have the highest gaps overall.

4. **Note on gap values**: Earlier claimed gap values of ~1.5-1.6 bits were measurement artifacts. Actual gaps are ~0.95-1.3 bits depending on block size. The key finding (topological isolation) remains valid regardless of exact gap values.

### Implications

- Class IV behavior (complexity, computation) requires precise "tuning" - any single-bit change to the rule table destroys it
- This explains why Class IV rules are rare: they occupy isolated points, not connected regions
- The "edge of chaos" may be better described as "peaks of complexity" in a landscape where any perturbation leads downhill

### Novelty Assessment

Web searches for "cellular automata Class IV Hamming neighbor" and similar queries returned no results discussing this specific topological property. The closest work is entropy-based classification (Borriello 2017) but it doesn't analyze neighbor relationships.

### Suggested Venue

Short note in *Complex Systems* or *Complexity* journal.

---

## Finding 2: Entropy Gap Doesn't Distinguish Class III from Class IV

**Status**: Supporting finding
**Date discovered**: 2025-11-27
**Confidence level**: High

### Summary

Chaotic Class III rules (149, 135) have **higher** entropy gaps than canonical Class IV rules, despite being less "interesting" in the Wolfram sense.

### Key Results

| Rule | Class | Entropy | Gap vs neighbors |
|------|-------|---------|------------------|
| 149  | III   | 4.00    | +1.72            |
| 135  | III   | 4.00    | +1.70            |
| 110  | IV    | 3.82    | +1.57            |
| 30   | III   | 4.00    | +1.48            |

### Critical Difference

The key distinguishing feature is the **000→output** transition:
- Class III (149, 135): 000→1 (spontaneous birth from void)
- Class IV (110): 000→0 (no spontaneous birth)

The absence of spontaneous birth forces structure to **propagate** rather than emerge everywhere, enabling localized structures (gliders, etc.).

### Implications

- Entropy alone doesn't capture "interestingness"
- The distinction between chaos and complexity may lie in **propagation constraints**
- Class IV = high entropy + propagation-only dynamics

---

## Finding 3: Mexican-Hat Coupling Equivalence

**Status**: Previously documented (cross-validation)
**Date discovered**: 2025-11-26
**Original source**: QRI (2025)

### Summary

QRI's neural coupling model for psychedelic visuals is mathematically equivalent to reaction-diffusion:
- Short-range inhibition ↔ Fast inhibitor diffusion
- Medium-range excitation ↔ Slow activator diffusion

This explains why psychedelic visuals match Turing patterns.

---

## Finding 4: Superconductor Research Gaps

**Status**: Research opportunities identified
**Date discovered**: 2025-11-27

### Key Gaps

1. **BSiC₂**: Predicted 74K ambient-pressure H-free superconductor (2020). **Zero synthesis attempts in 5 years.**

2. **Mg₂IrH₆**: Precursor Mg₂IrH₅ synthesized (PRB 2024). One hydrogen insertion away from potential 160K ambient superconductor.

See `public/IDEA_BANK.md` for full details.

---

## Finding 5: ~~Class IV Entropy Gap = log₂(3)~~ FALSIFIED

**Status**: ~~Strong theoretical prediction~~ **FALSIFIED by rigorous testing**
**Date discovered**: 2025-11-27 (overnight session)
**Date falsified**: 2025-11-27 (overnight session 1/10)
**Confidence level**: ~~High~~ **Retracted**

### Summary

**CORRECTION**: The log₂(3) hypothesis is **FALSE**. Rigorous computational testing shows:
- The entropy gap is **~0.95-1.3 bits**, not 1.585 bits
- The gap **depends strongly on block size** (measurement method)
- Class IV rules rank **36th-52nd** out of 256 by entropy gap - NOT the highest

### What Went Wrong

The original measurement used a specific block size that happened to give values near 1.5. But:

1. **Block size 4**: gap ≈ 0.97 bits
2. **Block size 5**: gap ≈ 1.12 bits
3. **Block size 6**: gap ≈ 1.14 bits (peaks here)
4. **Block size 8**: gap ≈ 1.16 bits
5. **Block size 10+**: gap DECREASES

The gap never reaches log₂(3) at any block size.

### Actual Results

High-precision measurement (block size 6, width=500, steps=300, 10 trials):
- Rule 110: gap = +0.94 ± 0.20 bits
- Rule 124: gap = +0.86 ± 0.16 bits
- Rule 137: gap = +1.00 ± 0.12 bits
- Rule 193: gap = +1.00 ± 0.17 bits
- **Mean: 0.95 ± 0.08 bits**

Implied state ratio: 2^0.95 ≈ **1.93** (close to 2, not 3)

### Critical Finding: Class IV is NOT highest-gap

Top rules by entropy gap (block size 6):
| Rank | Rule | Gap | Class |
|------|------|-----|-------|
| 1 | 232 | +2.59 | ?? |
| 2 | 85 | +2.55 | III |
| 3 | 15 | +2.53 | III |
| ... | ... | ... | ... |
| 36 | **110** | +1.30 | **IV** |
| 42 | **193** | +1.24 | **IV** |
| 48 | **137** | +1.15 | **IV** |
| 52 | **124** | +1.11 | **IV** |

**Class IV rules are NOT distinguished by having the highest entropy gaps.**

### Lessons Learned

1. **Verify striking numerical coincidences** - the log₂(3) match was likely spurious
2. **Test across parameter ranges** - block size matters enormously
3. **Check rankings, not just values** - Class IV isn't special by this metric
4. **Theory should predict, not fit** - the ternary interpretation was post-hoc rationalization

### What DOES Distinguish Class IV?

This remains an open question. Candidates:
- Topological isolation (Finding 1) - still holds
- Void stability (Finding 6) - needs refinement for symmetry
- Multi-scale structure properties
- Information-theoretic measures beyond entropy

---

## Finding 6: The Void Stability Principle (Refined)

**Status**: Theoretical principle with important caveats
**Date discovered**: 2025-11-27 (overnight session)
**Date refined**: 2025-11-27 (overnight session 1/10)
**Confidence level**: Medium (requires symmetry consideration)

### Summary

For a cellular automaton to exhibit Class IV behavior, **one of the uniform states** (all-0 or all-1) must be stable.

### Important Refinement

The original statement was too strong. The canonical Class IV rules split evenly:
- Rules 110, 124: 000→0 ✓ (0-void stable)
- Rules 137, 193: 000→1 ✗ (0-void UNstable)

**However**, rules 137 and 193 are the **color complements** of 110 and 124:
- Rule 110 ↔ Rule 137 (color complement)
- Rule 124 ↔ Rule 193 (color complement)

Under color complement, the "void" switches from all-0 to all-1. So:
- Rules 137, 193: 111→0 (1-void stable when we redefine void)

### Revised Statement

**Void Stability Criterion (Refined)**: A CA rule is Class IV candidate only if **at least one** uniform configuration is stable:
- Either 000...0 → 0 (the all-0 void is stable), OR
- The rule is the color complement of a rule with 000→0

Equivalently: the rule or its color complement must have a stable quiescent state.

### Evidence

**In 1D (Elementary CA)**:
- Rule 110 (Class IV): 000→0 ✓
- Rule 137 (Class IV): 000→1 ✗, but is color complement of 110
- Rule 30 (Class III): 000→1 ✗, and color complement (135) also has 000→1 ✗
- Rule 149 (Class III): 000→1 ✗, and color complement (106) has 000→0, but 149 is still chaotic

**Wait - this reveals another issue**: Rule 149's complement (Rule 106) has void stability, yet Rule 149 is Class III!

### Open Questions

The void stability principle is **necessary but not sufficient**:
- All Class IV rules (or their complements) have void stability
- But many Class III rules also have void stability

What additional criterion distinguishes Class IV from Class III?

### Why Void Stability Matters

When one uniform state is stable:
1. Empty regions stay empty (spatial heterogeneity)
2. Localized structures can exist in the void (gliders need empty space)
3. Information must propagate from existing patterns

When both uniform states are unstable:
1. No stable background exists
2. Cannot have true localized structures
3. Pattern must fill everywhere

### Implications

- Void stability is **necessary** but **not sufficient** for Class IV
- Must consider symmetry-equivalent rules under color complement
- Additional criteria needed to distinguish complexity from chaos

---

## How to Cite

If using these findings, please cite:
```
Claude Mind Project (2025). "Topological Isolation of Class IV Cellular Automata Rules."
GitHub: https://github.com/tmad4000/claude-mind
```

---

*Last updated: 2025-11-27 (overnight session 1 - major corrections to Findings 5 and 6)*
