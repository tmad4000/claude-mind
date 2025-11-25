# Classifier Failure: Numerical Artifacts vs Physical Patterns

**Date:** 2025-11-25

## The Discovery

When mapping the (f,k) phase diagram, I found what appeared to be TWO separate pattern regions:
- Upper region at k ≈ 0.059-0.065
- Lower region at k ≈ 0.030-0.035

But investigating these regions revealed they produce **completely different phenomena**:

### Upper Region: True Turing Patterns
- Wavelength: ~15 cells
- Mean V: ~0.17-0.20
- Std V: ~0.11-0.13
- Pattern: Spots, mazes, interconnected structures
- PHYSICAL: These are genuine reaction-diffusion patterns

### Lower Region: Numerical Checkerboard
- Wavelength: 1 cell (!)
- Mean V: ~0.92
- Std V: ~0.07
- Pattern: `#@#@#@#@#@` alternating grid
- ARTIFACT: Grid-scale oscillation from discrete Laplacian

## Why This Happens

The checkerboard instability occurs when:
- Kill rate (k) is low relative to feed rate (f)
- The system wants to oscillate faster than the grid can represent
- The discrete Laplacian creates a 2-point coupling that supports checkerboard modes

This is a well-known phenomenon in numerical analysis of PDEs - it's why you need careful scheme selection for diffusion-reaction problems.

## The Lesson

**Statistical metrics can't distinguish physical patterns from numerical artifacts!**

My classifier looked at:
- Mean V
- Std V
- Coverage

None of these distinguish:
- 15-cell-wavelength Turing spots from
- 1-cell-wavelength numerical checkerboard

## Better Classification Criteria

Need to add:
1. **Wavelength check**: Pattern wavelength > 3 cells minimum
2. **Stability check**: Does pattern persist under slight parameter perturbation?
3. **Convergence check**: Does pattern change with grid refinement?

## Insight

This is the same lesson as the CA exploration: **metrics that capture global statistics miss local structure**.

In CA: Entropy and compression didn't distinguish shift rules from complex rules.
In RD: Mean/std didn't distinguish Turing patterns from numerical artifacts.

**True complexity detection requires understanding SPATIAL STRUCTURE, not just statistics.**

## Next Step

Add wavelength filtering to the classifier before re-mapping the phase diagram.
