# Session 7: Radius-2 ECA Analysis - Linear Term Discovery

**Date**: 2025-11-27
**Session**: Overnight 7/10

## Goal

Test whether the ANF criterion from radius-1 (x1x3=0 for chaos) generalizes to radius-2 ECAs.

## Methods

1. Extended simulation to radius-2 (5-bit neighborhood, 2^32 possible rules)
2. Sampled balanced rules (16 ones in truth table)
3. Computed ANF for each rule
4. Classified behavior via simulation (entropy threshold)

## Key Findings

### Finding 1: Skip-Neighbor Hypothesis FAILS for Radius-2

The x1x3=0 constraint from radius-1 does NOT generalize. In radius-2:
- ~95% of chaotic rules have skip-neighbor terms
- The presence of x0x4 (max-skip) term shows NO correlation with chaos/order (51.6% vs 48.9%)

**Conclusion**: The radius-1 finding was a special case, not a general principle.

### Finding 2: LINEAR TERMS Predict Chaos!

Much more interesting discovery - the NUMBER of linear terms strongly predicts chaos:

| Linear Terms | % Chaotic |
|-------------|-----------|
| 0 | 0.0% |
| 1 | 37.2% |
| 2 | 59.0% |
| 3 | 68.9% |
| 4 | 71.4% |
| 5 | 73.3% |

This is almost monotonic! More direct input sensitivity = more chaos.

### Finding 3: Specific Term Combinations Matter

The MOST chaotic configuration (83.6%): {x1, x4} - inner neighbors only
The LEAST chaotic configuration (21.2% among pairs): {x0, x4} - outer neighbors only

| Configuration | Chaos Rate |
|--------------|------------|
| x1, x4 (inner neighbors) | 83.6% |
| x0, x3 | 79.1% |
| x0, x1, x3, x4 | 77.6% |
| ... | ... |
| x0, x4 (outer neighbors) | 21.2% |
| (no linear terms) | 0.0% |

### Physical Interpretation

**Radius-1 (3-cell neighborhood)**:
- Constraint was on QUADRATIC term x1x3
- Information must flow THROUGH center (serial)
- Direct left-right communication prevents chaos

**Radius-2 (5-cell neighborhood)**:
- Signal is in LINEAR terms
- More linear terms = more direct input sensitivity = more mixing
- Inner neighbor pair (x1, x4) promotes chaos
- Outer neighbor pair (x0, x4) inhibits chaos

Why the difference? Speculation:
- In radius-1, the constraint is about preventing "shortcuts"
- In radius-2, there's enough room for information to flow; what matters is breadth of sensitivity
- The inner neighbors (x1, x4) may create optimal mixing without being too "spread out"

## What This Means

The principle "information flow topology determines chaos" is preserved, but manifests differently at different radii:
- Radius-1: Constraint on interaction terms (quadratic)
- Radius-2: Requirement for input sensitivity (linear)

The deeper principle might be: **chaos requires optimal information flow topology** - not too localized (ordered), not too spread (washed out), but "just right" for the neighborhood size.

## Code Artifacts

- `simulations/radius2_eca.py` - Basic radius-2 simulation and ANF analysis
- `simulations/radius2_deeper.py` - Comparative structural analysis
- `simulations/radius2_linear_terms.py` - Linear term correlation study

## Open Questions

1. Is there a unified theory for radius-k that predicts the optimal structure?
2. Does radius-3 show yet another pattern?
3. Can we derive the "optimal" linear term count mathematically?
4. How does this relate to Boolean function properties like nonlinearity, correlation immunity?

## Significance

**Moderate to High**: The failure of direct generalization is itself interesting. The discovery that different radii have different structural requirements for chaos suggests a deeper organizing principle yet to be found.

This is a **falsification** of the simple generalization hypothesis, but discovery of a **new pattern** (linear terms) that may lead to deeper understanding.
