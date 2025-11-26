# Observations Database

A structured collection of observations from simulations, designed to support theory-building.

---

## FORMAT

Each observation follows:
```
### OBS-[ID]: [Short title]
**System**: CA / RD / Other
**Parameters**: ...
**Observation**: What was seen
**Quantitative**: Numbers/measurements
**Surprising?**: Yes/No/Somewhat - why
**Connections**: Links to other observations
**Theory implications**: What this suggests
```

---

## CELLULAR AUTOMATA OBSERVATIONS

### OBS-CA-001: Class IV rules are topologically isolated
**System**: Elementary CA (256 rules)
**Parameters**: All 8-bit rule numbers, Hamming distances
**Observation**: Class IV rules (30, 45, 73, 89, 101, 110, etc.) share NO Hamming-1 neighbors with each other
**Quantitative**: 0 pairs of Class IV rules differ by exactly 1 bit
**Surprising?**: YES - suggests Class IV is a fragile, isolated phenomenon
**Connections**: Boundary principle in RD (complexity at edges)
**Theory implications**: Complex behavior may require precise "tuning" - not continuously accessible

### OBS-CA-002: Rule 110 supports universal computation
**System**: Elementary CA Rule 110
**Parameters**: N/A
**Observation**: Matthew Cook proved Rule 110 is Turing-complete (2004)
**Quantitative**: Rule 110 can simulate any Turing machine
**Surprising?**: YES - one of simplest possible CA is universal
**Connections**: Gray-Scott computation attempts failed (OBS-RD-xxx)
**Theory implications**: Computation may require very specific dynamics, not generic "complexity"

### OBS-CA-003: Bidirectional spreading is key to replication
**System**: Elementary CA (256 rules)
**Parameters**: All rules tested, 200-step simulations from single seed
**Observation**: Rules with 000->0, 001->1, AND 100->1 produce linear expansion (replication)
**Quantitative**: 32 rules satisfy condition, 29 are true replicators (90.6% precision)
**Surprising?**: YES - simple 3-bit condition predicts complex emergent behavior
**Connections**: OBS-RD-007 (front propagation), wave mechanics
**Theory implications**: Replication = bidirectional spreading + no spontaneous birth

### OBS-CA-004: 59 rules show linear expansion behavior
**System**: Elementary CA (256 rules)
**Parameters**: Classification by dynamical behavior from single seed
**Observation**: 59 rules expand linearly, 86 fill, 56 stay static, 28 slow expand, 27 die
**Quantitative**: Distribution: 23% expand, 34% fill, 22% static, 11% slow, 10% die
**Surprising?**: Somewhat - expansion is rarer than filling
**Connections**: OBS-CA-003
**Theory implications**: Most spreading rules eventually fill; balanced expansion is special

### OBS-CA-005: Pure XOR (Rule 90) creates perfect Sierpinski triangle
**System**: Rule 90 (left XOR right)
**Parameters**: 000->0, 001->1, 010->0, 011->1, 100->1, 101->0, 110->1, 111->0
**Observation**: Creates self-similar fractal pattern with power-of-2 periodicity
**Quantitative**: At t=2^n, pattern width = 2^(n+1) - 1
**Surprising?**: Somewhat - simple local rule produces fractal global structure
**Connections**: OBS-CA-003 (satisfies replication condition)
**Theory implications**: XOR dynamics naturally produce self-similarity

### OBS-CA-006: Transition 111->0 prevents filling
**System**: Elementary CA (256 rules)
**Parameters**: Analyzed 86 filling rules vs 59 expanding rules
**Observation**: 35.6% of expanders have 111->1, but this reduces expansion quality
**Quantitative**: Rules with 111->0 are overrepresented among clean expanders
**Surprising?**: No - expected that crowding causes death
**Connections**: Game of Life overpopulation rule
**Theory implications**: Death from crowding enables sustained patterns

---

## REACTION-DIFFUSION OBSERVATIONS

### OBS-RD-001: Linear theory fails completely for Gray-Scott
**System**: Gray-Scott RD
**Parameters**: f=0.022-0.060, k=0.045-0.068, Du=0.16, Dv=0.08
**Observation**: Turing linear stability analysis predicts NO instability, yet patterns form
**Quantitative**: All tested pattern-forming points have eigenvalues < 0 (stable)
**Surprising?**: Somewhat - subcritical bifurcations known, but extent is striking
**Connections**: OBS-CA-001 (fragility), boundary principle
**Theory implications**: Pattern formation here is NOT a linear instability - it's finite-amplitude nucleation

### OBS-RD-002: No coarsening - wavelength fixed by kinetics
**System**: Gray-Scott RD
**Parameters**: Multiple (f,k) tested
**Observation**: Pattern wavelength doesn't increase over time (α ≈ 0)
**Quantitative**: λ(t) ~ t^0.00 across all tested parameters
**Surprising?**: No - expected for Turing patterns with wavelength selection
**Connections**: Contrast with phase separation (coarsening)
**Theory implications**: Different from spinodal decomposition; mechanism is reaction-driven

### OBS-RD-003: Subcritical at ALL Du/Dv ratios
**System**: Gray-Scott RD
**Parameters**: Du/Dv from 1.0 to 4.25
**Observation**: Bifurcation is subcritical everywhere tested
**Quantitative**: Gap between nucleation and small-IC thresholds > 0 always
**Surprising?**: Somewhat - theory suggests Du/Dv >> 1 might help
**Connections**: OBS-RD-001
**Theory implications**: Gray-Scott is deeply subcritical system - not near any supercritical regime

### OBS-RD-004: Wavelength 1.6x longer than linear theory
**System**: Gray-Scott RD
**Parameters**: Multiple parameters with λ ~ √(Dv/f) prediction
**Observation**: Measured λ = 1.6 × λ_linear on average
**Quantitative**: Ratio 1.6 ± 0.5 across parameter space
**Surprising?**: No - known that nonlinear saturation increases wavelength
**Connections**: N/A
**Theory implications**: Nonlinear effects increase final wavelength ~60%

### OBS-RD-005: All patterns weakly chaotic (λ > 0)
**System**: Gray-Scott RD
**Parameters**: 31 parameter points in pattern-forming region
**Observation**: All Lyapunov exponents positive (range 0.0001-0.002)
**Quantitative**: Mean λ ≈ 0.0005, no λ < 0 found
**Surprising?**: Somewhat - expected some ordered patterns
**Connections**: CA Class IV instability
**Theory implications**: Gray-Scott patterns may be inherently chaotic, just slowly

### OBS-RD-006: Mass conservation holds exactly
**System**: Gray-Scott RD
**Parameters**: 21 parameter points
**Observation**: f(1-⟨U⟩) = (k+f)⟨V⟩ holds to 0.2%
**Quantitative**: Ratio 1.002 ± 0.009
**Surprising?**: No - this is just integrating the PDEs
**Connections**: N/A
**Theory implications**: Conservation laws constrain dynamics

### OBS-RD-007: Front velocity 14x slower than Fisher-KPP
**System**: Gray-Scott RD
**Parameters**: 8 points with advancing fronts
**Observation**: Actual velocity ~0.014 px/step vs theory 0.21
**Quantitative**: Factor of 14-15x discrepancy
**Surprising?**: Somewhat - Fisher-KPP is rough approximation
**Connections**: Subcritical nature (OBS-RD-003)
**Theory implications**: Subcritical fronts are much slower than pulled fronts

### OBS-RD-008: Saturable kinetics increases wavelength 1.8x
**System**: Modified Gray-Scott (UV²/(1+V/Km))
**Parameters**: Km=0.1, same (f,k) as standard
**Observation**: Wavelength 1.79x longer than standard kinetics
**Quantitative**: λ_saturable / λ_standard = 1.79
**Surprising?**: No - expected from kinetics
**Connections**: OBS-RD-004
**Theory implications**: Kinetics directly controls wavelength

---

## CROSS-DOMAIN OBSERVATIONS

### OBS-X-001: Complexity at boundaries
**System**: Both CA and RD
**Observation**: Interesting dynamics occur at phase boundaries (CA: Class III/IV edge; RD: pattern/chaos edge)
**Connections**: OBS-CA-001, OBS-RD-001
**Theory implications**: Edge of chaos principle may be universal

### OBS-X-002: Universal computation vs pattern formation
**System**: CA vs RD comparison
**Observation**: Rule 110 (CA) supports computation, Gray-Scott (RD) does not
**Connections**: OBS-CA-002, failed computation tests
**Theory implications**: Computation requires specific dynamics, not just complexity

### OBS-X-003: Mexican-hat coupling = activator-inhibitor mechanism
**System**: Neural fields vs RD comparison
**Parameters**: QRI coupling kernels, Gray-Scott dynamics
**Observation**: QRI's "Mexican-hat" neural coupling is mathematically equivalent to RD:
- Short-range inhibition ↔ Fast inhibitor diffusion
- Medium-range excitation ↔ Slow activator diffusion
- Coupling kernel shape ↔ Differential diffusion rates
**Quantitative**: Same pattern wavelengths emerge from both systems with matched parameters
**Surprising?**: YES - explains why psychedelic visuals match Turing patterns
**Connections**: OBS-RD-004 (wavelength theory), NATURAL_CORRESPONDENCES.md
**Theory implications**: Turing mechanism is MORE universal than previously documented - same math describes animal skins, seashells, BZ reaction, AND neural activity under psychedelics
**Source**: QRI (2025) "Reverse Engineering DMT Phenomenology with Non-Linear Optics"

### OBS-CA-007: Class IV isolation is NOT due to simple constraints
**System**: Elementary CA (256 rules)
**Parameters**: All 13 Class IV rules, all 104 Hamming-1 neighbors analyzed
**Observation**: Class IV rules do NOT share any universal bit pattern. No single transition is constant across all Class IV rules.
**Quantitative**:
- 0/104 neighbors of Class IV rules are also Class IV (confirms isolation)
- Hamming weight: 3.92 ± 0.62 (vs random 4.0, vs Class III 4.38, vs Class II 3.05)
- Spread potential: 0.77 (vs Class III 1.85) - Class IV has LESS spreading than chaotic rules
- The "replication hypothesis" (bidirectional spread + no spontaneous birth + crowding death) scores only 1.15/3 for Class IV but 2.62/3 for Class III!
**Surprising?**: YES - The hypothesis that worked for replication BETTER predicts chaotic behavior than complex behavior
**Connections**: OBS-CA-001 (topological isolation), OBS-CA-003 (replication theory)
**Theory implications**:
- Class IV rules are defined by BALANCE, not by specific transitions
- They occupy a "saddle region" in rule space where any single-bit change pushes toward simpler attractors
- The replication condition (001→1, 100→1, 000→0) predicts CHAOS (Class III), not complexity (Class IV)
- Class IV = partial spreading + balanced birth/death, not maximal spreading

---

## QUESTIONS RAISED BY OBSERVATIONS

1. ~~What exactly makes Class IV CA rules special?~~ **PARTIALLY ANSWERED**: They're balanced, not constraint-satisfying
2. Why is Gray-Scott so deeply subcritical?
3. What rule property enables replication?
4. Is there a quantitative "edge of chaos" criterion?
5. What makes a pattern "cool" or "interesting"?
6. **NEW**: Can we predict specific psychedelic visual patterns from neural coupling parameters?
7. **NEW**: Does the Symmetry Theory of Valence (QRI) connect to pattern symmetry in RD?

---

*Last updated: 2025-11-25*
