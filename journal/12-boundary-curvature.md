# Boundary Curvature Discovery - 2025-11-25

## The Question

Previous exploration found two "linear" boundaries:
- Upper: k = 0.1285f + 0.0606
- Lower: k = 0.5005f + 0.0371

These boundaries intersect at f≈0.063, k≈0.069, where the pattern region should theoretically vanish.

**But is this right?**

## The Discovery

The boundaries are NOT linear - they're **CURVED**!

### Actual Boundary Equations

**Upper boundary** (pattern → extinction):
```
k = -6.74f² + 0.79f + 0.043
```

**Lower boundary** (uniform → pattern):
```
k = -6.48f² + 0.81f + 0.036
```

Both have:
- Significant negative quadratic terms (~-6.5)
- Similar linear coefficients (~0.8)
- Different constants (0.043 vs 0.036)

### The Evidence

| f | k_actual (upper) | k_linear (upper) | Deviation |
|---|------------------|------------------|-----------|
| 0.02 | 0.0505 | 0.0632 | -0.0127 |
| 0.04 | 0.0655 | 0.0657 | -0.0002 |
| 0.06 | 0.0655 | 0.0683 | -0.0028 |
| 0.08 | 0.0625 | 0.0709 | -0.0084 |
| 0.10 | 0.0565 | 0.0735 | -0.0169 |

Correlation with f: **-0.664** (upper), **-0.952** (lower)

At f=0.04, the linear model works fine (deviation ~0.0002)
At f=0.10, the deviation is -0.017 - almost 20x larger!

## Why the Linear Model Seemed Correct

The original boundary mapping was done in the range f ∈ [0.02, 0.06].
In this restricted range, the curvature is small enough that linear fits work.

But extrapolating to higher f values reveals the true quadratic nature.

## Physical Interpretation

Both boundaries curve downward at high f. This means:

1. **Pattern region doesn't vanish** - it persists to high f values
2. **Valid k range shifts DOWN** as f increases
3. **The band narrows AND descends**

At f = 0.10:
- Actual upper: k ≈ 0.057
- Actual lower: k ≈ 0.054
- Band width: ~0.003

The pattern region becomes a thin "sliver" at high f, not a vanishing point.

## Why Quadratic?

The quadratic term (-6.5f²) in both boundaries suggests:
- The pattern-forming mechanism has a nonlinear dependence on f
- At high feed rates, the system dynamics change qualitatively
- The "balance point" between growth and decay shifts nonlinearly

This might relate to:
- Saturation effects in the reaction kinetics
- Changes in the effective diffusion balance
- Higher-order coupling between f and k

## What This Teaches

1. **Linear models are local approximations** - they work in limited ranges
2. **Extrapolation is dangerous** - even good fits can fail outside their domain
3. **Always extend the search** - pushing to extreme parameters reveals structure
4. **The interesting physics is in the curvature** - the quadratic term encodes dynamics

## Open Questions

1. Why are the quadratic coefficients nearly equal (-6.74 vs -6.48)?
2. Is the boundary truly quadratic, or is there higher-order structure?
3. What theoretical derivation gives k ~ af² + bf + c?
4. Does this pattern persist to f > 0.10?

## Summary

**The Gray-Scott pattern boundaries are QUADRATIC, not linear.**

The linear model works locally but fails at high f. The pattern region curves downward and persists well beyond where linear extrapolation predicts extinction.

This is a refinement of the earlier finding - the 2D geometry is even richer than initially thought.
