# Complete Hypothesis List and Test Outcomes

All hypotheses tested during Gray-Scott exploration, organized by category.

---

## CATEGORY 1: LINEAR STABILITY AND BIFURCATIONS

### H1.1: Turing instability predicts pattern formation
**Hypothesis**: Linear stability analysis (LSA) accurately predicts where patterns form.
**Test**: Performed LSA at all tested (f,k) points, compared with simulation.
**Result**: **THEORY FAILS** - LSA shows stability (no Turing instability) at parameters where robust patterns form.
**Novelty**: 4/10 - Subcritical bifurcation is known, but the EXTENT of failure (patterns exist with NO linear instability) is striking.

### H1.2: Supercritical transition exists at some Du/Dv ratio
**Hypothesis**: There exists a Du/Dv ratio where the bifurcation becomes supercritical (small perturbations grow).
**Test**: Swept Du/Dv from 1.0 to 4.25, tested small vs large IC outcomes.
**Result**: **NEGATIVE** - Subcritical behavior at ALL tested ratios. No supercritical transition found.
**Novelty**: 3/10 - Confirms known subcritical nature.

### H1.3: The bifurcation type changes with f
**Hypothesis**: At different f values, the bifurcation might be supercritical in some regions.
**Test**: Tested f from 0.016 to 0.040, measured gap between small-IC and large-IC thresholds.
**Result**: **NEGATIVE** - Subcritical at all f values tested.
**Novelty**: 2/10 - Expected.

---

## CATEGORY 2: PATTERN TYPES AND CLASSIFICATION

### H2.1: New pattern types exist outside Pearson classification
**Hypothesis**: There are pattern types not described in Pearson's α-ω classification.
**Test**: Searched across parameter space with various initial conditions.
**Result**: **NEGATIVE** - All observed patterns match known types (spots, stripes, labyrinth, chaos).
**Novelty**: 1/10 - Confirms Pearson's completeness.

### H2.2: Spirals exist in Gray-Scott
**Hypothesis**: Rotating spiral waves can be stable in Gray-Scott.
**Test**: Created spiral-inducing initial conditions at multiple parameters.
**Result**: **POSITIVE** - Found spirals at f=0.028, k=0.053 (period 2082) and f=0.035, k=0.058 (period 37485).
**Novelty**: 4/10 - Spirals in RD are well-known, but documenting their existence in GS at specific parameters is useful.

### H2.3: Breathing/pulsating patterns exist
**Hypothesis**: Patterns with regular amplitude oscillations (limit cycles) exist.
**Test**: Searched for periodic amplitude variations across parameter space.
**Result**: **WEAK POSITIVE** - Found one point with period 500 steps but amplitude variation only 0.0006. Likely numerical noise.
**Novelty**: 2/10 - Not convincing.

### H2.4: Multiple distinct stable patterns at same (f,k)
**Hypothesis**: More than two qualitatively different patterns can be stable at the same parameters.
**Test**: Tested 10 parameter points with different initial conditions.
**Result**: **AMBIGUOUS** - Found 3-5 "patterns" at each point, but h_stripes/v_stripes/diagonal are really the same pattern at different orientations.
**Novelty**: 3/10 - Multistability is known.

---

## CATEGORY 3: DYNAMICS AND CHAOS

### H3.1: There exists a sharp chaos-order transition
**Hypothesis**: As parameters vary, there's a clear boundary between ordered (λ<0) and chaotic (λ>0) patterns.
**Test**: Measured Lyapunov exponents across 31 parameter points.
**Result**: **NEGATIVE** - All 31 patterned points showed λ > 0 (range 0.0001 to 0.002). No ordered points found.
**Novelty**: 3/10 - Confirms weak chaos throughout, but no sharp transition.

### H3.2: Period-doubling route to chaos
**Hypothesis**: Gray-Scott shows period-doubling cascade with Feigenbaum-like behavior.
**Test**: Searched for periodic behavior and period ratios through transition region.
**Result**: **INCONCLUSIVE** - Test still running. Preliminary: most points are static or chaotic, few periodic.
**Novelty**: TBD

### H3.3: Patterns coarsen over time (wavelength increases)
**Hypothesis**: Pattern wavelength grows as t^α with α > 0 (coarsening dynamics).
**Test**: Measured wavelength vs time at 10 parameter points.
**Result**: **NEGATIVE** - α ≈ 0 (no coarsening). Wavelength fixed by kinetics, not domain size.
**Novelty**: 2/10 - Expected for Turing patterns with wavelength selection.

### H3.4: Critical slowing down near phase boundary
**Hypothesis**: Pattern formation time diverges as parameters approach the pattern boundary.
**Test**: Measured relaxation times at varying distances from boundary.
**Result**: **NEGATIVE** - No significant slowing detected. Formation time roughly uniform.
**Novelty**: 2/10 - Subcritical bifurcation doesn't show critical slowing like equilibrium transitions.

---

## CATEGORY 4: MATHEMATICAL RELATIONSHIPS

### H4.1: Mass balance holds exactly
**Hypothesis**: The integral relationship f(1-⟨U⟩) = (k+f)⟨V⟩ holds in steady state.
**Test**: Measured at 21 parameter points with patterns.
**Result**: **CONFIRMED** - Ratio = 1.002 ± 0.009 (holds to 0.2% accuracy).
**Novelty**: 1/10 - This is just conservation, expected.

### H4.2: Wavelength follows exact power law
**Hypothesis**: λ = A · f^α · k^β with constant exponents.
**Test**: Fit wavelengths to power law across parameter space.
**Result**: **PARTIAL** - Fit residual ~10%, not exact. Wavelengths 1.6x longer than linear theory.
**Novelty**: 3/10 - Quantitative but expected from nonlinear saturation.

### H4.3: Universal dimensionless constant exists
**Hypothesis**: Some combination of λ, f, k, Du, Dv is constant across parameters (like Feigenbaum constant).
**Test**: Tested 9 dimensionless combinations, computed coefficient of variation.
**Result**: **NEGATIVE** - All CVs > 0.05. Only ratio5 (mass balance) is nearly constant.
**Novelty**: 2/10 - No universal constant found.

### H4.4: Variational principle (energy minimization)
**Hypothesis**: Patterns minimize some energy functional (Lyapunov function exists).
**Test**: Tracked multiple candidate energy functionals during evolution.
**Result**: **NEGATIVE** - No functional monotonically decreases. System is non-gradient.
**Novelty**: 2/10 - Expected for driven dissipative systems.

---

## CATEGORY 5: MODIFIED SYSTEMS

### H5.1: Anisotropic diffusion changes pattern orientation
**Hypothesis**: Making Dx ≠ Dy causes patterns to preferentially orient along fast diffusion axis.
**Test**: Varied Dx/Dy from 0.25 to 4.0, measured pattern orientation.
**Result**: **CONFIRMED** - Strong correlation (-0.9) between log(Dx/Dy) and orientation angle.
**Novelty**: 3/10 - Expected from theory, quantified relationship.

### H5.2: 3D Gray-Scott shows novel pattern types
**Hypothesis**: 3D patterns have topology impossible in 2D (gyroids, tubes, etc.).
**Test**: Ran 3D simulations on 32³ grid.
**Result**: **INCONCLUSIVE** - All patterns classified as "gyroid_or_network" with fill=0.5. Grid likely too small.
**Novelty**: N/A - Needs larger grid.

### H5.3: Modified kinetics shift pattern-forming region
**Hypothesis**: Changing UV² to UV³, U²V, or saturable/inhibited forms changes pattern properties.
**Test**: Tested 5 kinetics types across parameter space.
**Result**: **CONFIRMED** - Saturable kinetics gives 1.79x longer wavelength, patterns at new parameters.
**Novelty**: 4/10 - Expected from kinetics theory but quantified.

### H5.4: Noise induces patterns in subcritical region
**Hypothesis**: Stochastic fluctuations can nucleate patterns where deterministic dynamics don't.
**Test**: Added additive/multiplicative noise at various strengths.
**Result**: **CONFIRMED** - At noise=0.02, patterns form at 4 points where deterministic gives none.
**Novelty**: 3/10 - Noise-induced transitions are known in subcritical systems.

---

## CATEGORY 6: COMPUTATION AND INFORMATION

### H6.1: Spots can propagate signals
**Hypothesis**: A perturbation at one end of a channel can propagate to the other end.
**Test**: Created stripe channels, introduced perturbations, tracked propagation.
**Result**: **NEGATIVE** - No signal propagation. Velocity ≈ 0 or negative.
**Novelty**: N/A - Negative result.

### H6.2: Colliding spots implement AND gate
**Hypothesis**: Two spots colliding produce output only when both present.
**Test**: Truth table test with spots at input regions.
**Result**: **NEGATIVE** - Output present whenever any input present. Not AND-like.
**Novelty**: N/A - Negative result.

### H6.3: Pattern collisions have deterministic rules
**Hypothesis**: Collision outcomes (merge, annihilate, reflect) follow deterministic rules.
**Test**: Tested 4 collision geometries.
**Result**: **COMPLEX** - Outcomes depend on geometry but are "complex_N" (multiple resulting spots).
**Novelty**: 2/10 - Collision dynamics are complicated but not clearly computational.

---

## CATEGORY 7: BOUNDARIES AND STABILITY

### H7.1: Nucleation threshold varies predictably with parameters
**Hypothesis**: Critical amplitude for pattern nucleation follows a simple formula.
**Test**: Measured threshold amplitude at 8 parameter points.
**Result**: **PARTIAL** - Threshold increases with f (0.10 to 0.19) but no exact formula.
**Novelty**: 3/10 - Quantitative but expected trend.

### H7.2: Front velocity follows Fisher-KPP scaling
**Hypothesis**: Pattern fronts propagate at velocity v = 2√(Df).
**Test**: Measured front velocities at 8 points, compared with theory.
**Result**: **THEORY FAILS** - Actual velocity 0.014 px/step, vs theory 0.21 px/step (14x slower).
**Novelty**: 4/10 - Quantitative discrepancy from simple theory, but expected for subcritical systems.

### H7.3: Hysteresis loops map bistable region
**Hypothesis**: Clear hysteresis exists between pattern-forming and uniform states.
**Test**: Swept k up and down, tracked transitions.
**Result**: **INCONCLUSIVE** - No clear hysteresis loops detected, possibly due to parameter resolution.
**Novelty**: N/A - Test failed.

### H7.4: Localized single spots are stable
**Hypothesis**: Isolated single spots can persist without growing or dying.
**Test**: Initialized single spots at various parameters.
**Result**: **MOSTLY NEGATIVE** - Spots either grow or split at most parameters. Stable only at f=0.055, k=0.067.
**Novelty**: 2/10 - Localized structures near boundary are known.

---

## CATEGORY 8: NUMERICAL AND RESOLUTION EFFECTS

### H8.1: Physical wavelength is resolution-independent
**Hypothesis**: If the discretization is correct, wavelength in physical units shouldn't depend on N.
**Test**: Ran same physical domain at N=32, 48, 64, 96, 128.
**Result**: **FAILS** - Physical wavelength varies from 10.7 to 21.3 (CV=28%).
**Novelty**: 3/10 - Numerical artifact, suggests dx-dependent effects.

### H8.2: Pattern formation is robust to initial condition details
**Hypothesis**: Different random seeds give statistically similar patterns.
**Test**: Ran 10 simulations with different seeds at same parameters.
**Result**: **CONFIRMED** - Wavelength CV = 5% across seeds. Robust.
**Novelty**: 1/10 - Expected.

---

## SUMMARY STATISTICS

| Category | Hypotheses | Confirmed | Failed/Negative | Inconclusive |
|----------|------------|-----------|-----------------|--------------|
| Linear stability | 3 | 0 | 2 | 1 (ongoing) |
| Pattern types | 4 | 1.5 | 2 | 0.5 |
| Dynamics | 4 | 0 | 3 | 1 |
| Mathematical | 4 | 1 | 3 | 0 |
| Modified systems | 4 | 3 | 0 | 1 |
| Computation | 3 | 0 | 2 | 1 |
| Boundaries | 4 | 1 | 2 | 1 |
| Numerical | 2 | 1 | 1 | 0 |
| **TOTAL** | **28** | **7.5** | **15** | **5.5** |

### Key Insights from Hypothesis Testing

1. **Theory failures are known**: The subcritical bifurcation and wavelength discrepancy are documented.
2. **Novel directions (3D, stochastic, modified kinetics) confirm expected behavior**: No surprises.
3. **Computation doesn't work**: Gray-Scott patterns don't naturally implement logic.
4. **Numerical effects exist**: Grid resolution affects results more than expected.
5. **Mathematical relationships hold as expected**: Mass balance works, no hidden constants.

### What Would Be Different in a >7/10 Finding

- Finding a pattern type not in Pearson's classification
- Quantitative prediction that contradicts published literature
- Exact formula that matches simulation to many decimal places
- Universal constant analogous to Feigenbaum's
- Demonstration of computation in RD patterns

---

## CATEGORY 9: CLASS IV TOPOLOGY (NEW - 2025-11-25)

### H9.1: Class IV rules satisfy a simple constraint
**Hypothesis**: Class IV rules share some universal bit pattern (e.g., all have 000→0, or all have 111→0).
**Test**: Checked all 8 bits across 13 Class IV rules for invariants.
**Result**: **NEGATIVE** - No bit is constant across all Class IV rules. No partial invariant >80% either.
**Novelty**: 5/10 - Confirms Class IV is NOT definable by simple constraints.

### H9.2: The replication condition predicts Class IV
**Hypothesis**: Rules with bidirectional spread (001→1, 100→1), no spontaneous birth (000→0), and crowding death (111→0) are Class IV.
**Test**: Scored all Class IV and Class III rules on this 3-point criterion.
**Result**: **OPPOSITE OF EXPECTED** - Class III scores 2.62/3, Class IV scores only 1.15/3!
**Novelty**: 6/10 - The replication condition predicts CHAOS, not complexity. This is surprising.

### H9.3: Class IV rules have restricted spreading
**Hypothesis**: Class IV rules have lower "spread potential" than chaotic rules.
**Test**: Measured spread potential (001→1 + 100→1) across classes.
**Result**: **CONFIRMED** - Class IV mean 0.77, Class III mean 1.85.
**Novelty**: 5/10 - Complexity requires PARTIAL spreading, not maximal spreading.

### H9.4: Class IV isolation is due to saddle-point structure
**Hypothesis**: Class IV rules occupy a "saddle region" where any perturbation pushes toward simpler attractors.
**Test**: Classified all 104 Hamming-1 neighbors of Class IV rules.
**Result**: **CONFIRMED** - 0/104 neighbors are Class IV. Distribution: 32.7% fills, 24% chaotic, 17.3% periodic, 13.5% static, 8.7% other, 3.8% dies.
**Novelty**: 6/10 - Confirms saddle structure. Complexity is unstable to perturbation in ALL directions.

### H9.5: Class IV entropy gap is exactly log₂(3)
**Hypothesis**: The entropy gap between Class IV rules and their neighbors equals log₂(3) ≈ 1.585 bits.
**Test**: Computed mean gap across canonical Class IV rules (110, 124, 137, 193) with multiple block sizes and high precision.
**Result**: **FALSIFIED** (2025-11-27, overnight session 1)
- Actual gap: ~0.95-1.3 bits depending on block size, NOT 1.585
- Gap peaks around block size 6-8, then decreases
- Class IV rules rank 36th-52nd by gap, NOT the highest
- Original "confirmation" was due to specific block size that happened to give ~1.5
**Novelty**: 3/10 - Negative result, but demonstrates importance of parameter sensitivity in measurements.

### H9.6: Void stability is necessary for Class IV
**Hypothesis**: Class IV requires 000→0 (stable void), while Class III often has 000→1 (spontaneous birth).
**Test**: Checked 000→output transition for all canonical Class IV rules and Class III rules.
**Result**: **PARTIALLY FALSIFIED / REFINED** (2025-11-27, overnight session 1)
- Rules 110, 124: 000→0 ✓
- Rules 137, 193: 000→1 ✗
- BUT: 137=color_complement(110), 193=color_complement(124)
- **Refined criterion**: Class IV requires stable void under SOME orientation (original or color complement)
- **Additional complication**: Rule 149 (Class III) has complement with stable void, yet is still chaotic
- **Conclusion**: Void stability is NECESSARY but NOT SUFFICIENT for Class IV
**Novelty**: 5/10 - Refined principle with important caveats.

---

## CATEGORY 10: GENERALIZATION ACROSS DIMENSIONS (NEW - 2025-11-27)

### H10.1: Void stability principle holds in 2D
**Hypothesis**: 2D CAs with stable void are candidates for Class IV behavior; unstable void → chaos.
**Test**: Manual analysis of known 2D CAs (Game of Life, Seeds, Day & Night).
**Result**: **CONFIRMED** - Life (B3/S23): void stable, Class IV. Seeds (B2/S): void unstable, explosive chaos.
**Novelty**: 7/10 - Cross-dimensional principle for designing complex CAs.

### H10.2: Entropy gap principle generalizes to 2D
**Hypothesis**: 2D Class IV CAs (Life, etc.) have ~log₂(3) entropy gap from neighbors.
**Test**: Not yet performed (requires 2D CA neighbor analysis).
**Result**: **MOOT** - The underlying hypothesis (H9.5) was FALSIFIED. The gap is NOT log₂(3) even in 1D.
**Novelty**: N/A - Based on false premise.

### H10.3: Ternary state partitioning is universal to complexity
**Hypothesis**: Any system capable of universal computation must support 3 distinguishable macroscopic states.
**Test**: Theoretical analysis - requires more systems.
**Result**: **UNSUPPORTED** - The log₂(3) evidence was falsified. There is no quantitative support for "ternary" partitioning.
**Novelty**: 2/10 - Theoretical speculation without empirical support. The "ternary" interpretation was post-hoc rationalization.
