# Boundary Geometry Discovery - 2025-11-25

## Key Finding

The pattern region in Gray-Scott reaction-diffusion is bounded by **linear** boundaries in (f, k) space, characterized by the difference **(k - f)**.

## The Boundaries

```
Upper boundary: k = 0.1285 * f + 0.0606
Lower boundary: k = 0.5005 * f + 0.0371
```

### Key Properties:

1. **Both boundaries are LINEAR** (RMSE < 0.002)
2. **The boundaries are NOT parallel** - slopes differ significantly (0.13 vs 0.50)
3. **The band NARROWS as f increases**

## The Critical Parameter: (k - f)

Along each boundary, the value (k - f) is roughly constant:
- Upper boundary: k - f ≈ 0.023-0.035
- Lower boundary: k - f ≈ 0.023-0.026

This means:
- **Patterns emerge when 0.02 < (k - f) < 0.04 approximately**
- The "extra kill rate" relative to feed rate determines pattern formation

## Physical Interpretation

In the Gray-Scott model:
- f = feed rate (how fast substrate U is added)
- k = kill rate (how fast product V decays)

The quantity (k - f) represents the **net removal rate** of V:
- Too low (k - f) < 0.02 → V grows too fast → uniform filling
- Too high (k - f) > 0.04 → V dies too fast → extinction
- Just right → Turing patterns!

## Why the Band Narrows

The lower boundary has a steeper slope (0.50) than the upper (0.13).

This means as f increases:
- The viable range of k shrinks
- At high f, only a narrow range of k produces patterns
- At low f, there's more "room" for patterns

## Comparison to Literature

The Gray-Scott phase diagram is well-studied. Known regions include:
- λ (lambda): spots
- μ (mu): stripes
- κ (kappa): mitosis patterns

My findings are consistent with the known structure, but the explicit linear characterization of boundaries by (k - f) is a useful formulation.

## What This Tells Us

1. **Patterns require balance**: Not too much, not too little reactivity
2. **The balance is linear**: Simple ratio/difference relationships
3. **The "edge of chaos" has specific geometry**: Not fractal or complex - just two lines!

## Questions for Further Investigation

1. Why is the lower boundary steeper than the upper?
2. Does the (k - f) characterization generalize to other RD systems?
3. What happens at the intersection of the two boundary lines?
4. Is there a theoretical derivation of these slopes?

## Hypothesis Refinement

Initial hypothesis: Patterns emerge when 0.02 < (k-f) < 0.04

Testing showed only 67% accuracy! The scan along constant (k-f) lines revealed:
- k-f = 0.015: Mostly uniform, 1 pattern at high f
- k-f = 0.020: Pattern only at f≈0.04
- k-f = 0.025: Pattern only at f≈0.04
- k-f = 0.030: Patterns at f≈0.02-0.03
- k-f = 0.035: Pattern only at f≈0.02
- k-f ≥ 0.040: No patterns

**Refined understanding**: (k-f) is NOT constant in the pattern region.
Instead, **(k-f) DECREASES as f increases** along the pattern region.

This is consistent with the non-parallel boundaries:
- Lower boundary slope: 0.50
- Upper boundary slope: 0.13

Since the lower boundary rises faster than the upper, the "height" (k-f) of the pattern region shrinks as you move to higher f.

## Better Characterization

The pattern region is not characterized by simple (k-f) bounds.
It's a true 2D region with non-trivial geometry - a diagonal band that narrows toward higher f.

## What Would Surprise Another Claude?

The explicit failure of the (k-f) hypothesis is instructive:
1. Simple 1D projections of 2D phase space can be misleading
2. The pattern region's geometry encodes information about the dynamics
3. Testing hypotheses with simulations quickly reveals their limits

The methodological lesson: Build simulators, test predictions, iterate.
