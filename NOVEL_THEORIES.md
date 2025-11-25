# Novel Theories to Test

Explicit predictions that can be validated with simulation. Each theory should be:
1. Non-obvious (baseline Claude might not predict it)
2. Testable with numerical simulation
3. Falsifiable

---

## Theory 1: Hysteresis in Pattern Boundaries

**Prediction**: The pattern boundary is NOT the same going in vs out.

- If you START with patterns and slowly increase k, patterns should PERSIST beyond the "birth" boundary
- If you START uniform and decrease k, patterns should appear at a LOWER k
- There should be a hysteresis loop of width Δk

**Specific prediction**: Hysteresis width Δk ≈ 0.005-0.01 (order of magnitude)

**Test**: Run two simulations at same (f,k) near boundary - one starting patterned, one starting uniform. Compare final states.

**Why non-obvious**: Linear stability analysis gives ONE boundary. Hysteresis requires nonlinear analysis.

**Status**: TESTED - BASELINE WRONG!

**Result**:
- Baseline predicted Δk ≈ 0.005-0.015 with 7/10 confidence
- Actual: Δk ≈ 0.0003 (essentially zero)
- The subcritical bifurcation / energy barrier reasoning was incorrect for Gray-Scott

**Implication**: Gray-Scott appears to have a SUPERCRITICAL Turing bifurcation, not subcritical. No nucleation barrier, no hysteresis.

---

## Theory 2: Pattern Wavelength Scales as 1/√f

**Prediction**: The characteristic pattern wavelength λ should depend on f as:

λ ∝ √(D/f) where D is a diffusion coefficient

At the pattern boundary, this gives λ ∝ 1/√f

**Specific prediction**: λ(f=0.02) / λ(f=0.08) ≈ 2.0

**Test**: Measure autocorrelation length at multiple f values along the viable k range.

**Why non-obvious**: The wavelength selection in Turing patterns comes from the balance of diffusion and reaction rates. The √f scaling is a specific prediction from dimensional analysis.

**Status**: UNTESTED

---

## Theory 3: Critical Slowing Down Near Boundaries

**Prediction**: Near the pattern boundary, perturbations should decay SLOWLY.

The relaxation time τ should diverge as: τ ∝ 1/|k - k_c| where k_c is the critical k.

**Specific prediction**: τ at k = k_c - 0.001 should be ~10x longer than at k = k_c - 0.01

**Test**: Perturb a steady state, measure how long until it returns to equilibrium.

**Why non-obvious**: This is a general feature of continuous phase transitions but hasn't been verified for Gray-Scott.

**Status**: UNTESTED

---

## Theory 4: Defect Density Minimum at "Sweet Spot"

**Prediction**: Pattern defects (dislocations, grain boundaries) should be MINIMIZED at a specific (f,k) point - not at the center of the viable region but offset toward the upper boundary.

**Specific prediction**: Minimum defect density at k ≈ k_upper - 0.3*(k_upper - k_lower)

**Rationale**: Too close to boundaries → patterns unstable → more defects. But asymmetric because the two boundaries have different physical origins.

**Test**: Count defects (points where pattern orientation changes rapidly) across parameter space.

**Why non-obvious**: The asymmetry prediction is novel.

**Status**: UNTESTED

---

## Theory 5: Chaos Boundary is Fractal

**Prediction**: The boundary between chaotic and patterned regions (around f=0.026, k=0.051) has FRACTAL structure, not a smooth curve.

**Specific prediction**: If you zoom in on the chaos-pattern boundary, you'll find interlocking "fingers" of chaos and pattern at finer scales.

**Test**: High-resolution scan of the chaos region boundary.

**Why non-obvious**: The pattern boundary being smooth (quadratic) doesn't imply the chaos boundary is also smooth.

**Status**: UNTESTED

---

## Theory 6: Multi-Stability Region Exists

**Prediction**: There exists a region in (f,k) space where BOTH spots and stripes are stable - final state depends on initial conditions.

**Specific prediction**: Multi-stability region is near f ≈ 0.04, k ≈ 0.062 (overlap of spot and stripe stability regions).

**Test**: At candidate points, run simulations with (a) spot-like initial conditions, (b) stripe-like initial conditions. Check if both persist.

**Why non-obvious**: Standard phase diagrams show one pattern per region, but bistability is possible.

**Status**: UNTESTED

---

## Priority Order

1. **Hysteresis** (Theory 1) - Easy to test, clear prediction
2. **Multi-stability** (Theory 6) - Interesting if true, testable
3. **Wavelength scaling** (Theory 2) - Quantitative test of dimensional analysis
4. **Critical slowing** (Theory 3) - Tests phase transition physics
5. **Defect minimum** (Theory 4) - Novel asymmetry prediction
6. **Fractal chaos boundary** (Theory 5) - Computationally expensive but exciting

---

## Validation Protocol

For each theory:
1. **Before testing**: Get baseline Claude prediction (skeptical reviewer)
2. **Run simulation**: Generate data
3. **Compare**: Theory vs baseline vs actual
4. **Update**: If theory wrong, why? If right, what else does it predict?
