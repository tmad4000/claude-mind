# Research Proposal: Kinetic Pathways to Ambient-Pressure Mg₂IrH₆ Superconductivity

**Proposed by**: Jacob Cole (contact: [your email])
**Date**: November 2025
**Estimated Budget**: $200-500K (2-year postdoc project)
**Keywords**: high-temperature superconductivity, hydrides, ion implantation, non-equilibrium synthesis

---

## Executive Summary

Mg₂IrH₆ is computationally predicted to superconduct at **103-160K at ambient pressure**—above liquid nitrogen temperature, without requiring extreme pressures. The precursor Mg₂IrH₅ has already been synthesized (Strobel et al., PRB 2024), but thermal equilibrium approaches failed to insert the final hydrogen.

We propose **kinetic (non-equilibrium) pathways** to bypass thermodynamic barriers: cryogenic ion implantation, electrochemical gating, and plasma-assisted insertion. DFT calculations show no energy barrier for H insertion—the challenge is delivering hydrogen atoms to interstitial sites faster than they can recombine into H₂ or diffuse out.

---

## Background & Motivation

### The Prize
Room-temperature superconductivity remains one of the grand challenges in physics. Hydrogen-rich compounds under extreme pressure (LaH₁₀, H₃S) have achieved Tc up to 250-290K, proving high-Tc is physically possible. The barrier is stabilizing these phases at ambient pressure.

### The Opportunity
The Mg₂XH₆ family (X = Rh, Ir, Pd, Pt) represents a promising path:
- **Moderate synthesis pressures** (~250 bar for Mg₂IrH₅, vs. megabar for LaH₁₀)
- **Precursor already exists**: Mg₂IrH₅ synthesized at 450°C, 100-250 bar H₂ (Strobel group, 2024)
- **Small thermodynamic gap**: Mg₂IrH₆ is only 60 meV/atom above the convex hull
- **No insertion barrier**: DFT predicts barrierless H insertion (PRL 2024)

### Why Thermal Approaches Failed
Strobel's group attempted Mg₂IrH₆ synthesis up to 28 GPa and failed—Mg₂IrH₅ remained more stable under all equilibrium conditions tested. This tells us the problem is **thermodynamic, not kinetic at the atomic scale**.

The insight: if we can deliver hydrogen atoms to insertion sites *faster than equilibrium processes remove them*, we may trap the metastable Mg₂IrH₆ phase.

---

## Proposed Approach

### Strategy: Kinetic Trapping via Non-Equilibrium Hydrogen Insertion

We propose three parallel approaches, all targeting Mg₂IrH₅ thin films:

#### Approach 1: Cryogenic Ion Implantation
- **Method**: H⁺ or D⁺ implantation (1-10 keV) into Mg₂IrH₅ films at T < 77K
- **Rationale**: Low temperature suppresses hydrogen diffusion and H₂ recombination
- **Deuterium variant**: Heavier isotope diffuses slower, extending metastable lifetime
- **Dose optimization**: Target stoichiometric H insertion without excessive radiation damage

#### Approach 2: Electrochemical Gating
- **Method**: Ionic liquid gating of Mg₂IrH₅ thin films with H⁺ source
- **Rationale**: Electric field drives H⁺ into the lattice without thermal activation
- **Advantage**: Gentle, reversible, allows in-situ transport measurements
- **Challenge**: Requires high-quality epitaxial films with accessible surfaces

#### Approach 3: Plasma-Assisted Insertion
- **Method**: Low-energy H₂ plasma exposure of films at controlled temperature
- **Rationale**: Atomic H flux provides insertion-ready species
- **Temperature window**: Cold enough to suppress H₂ formation, warm enough for surface mobility

### Why Thin Films?

Thin films enable:
1. **Precise stoichiometry control** via deposition rate calibration
2. **In-situ characterization** (resistivity, Hall effect) during hydrogen insertion
3. **Rapid screening** of conditions via combinatorial approaches
4. **Access to advanced probes** (synchrotron XRD, neutron reflectometry)

Bulk synthesis can follow once proof-of-principle is established.

---

## Key Experiments

### Phase 1: Film Growth & Characterization (Months 1-6)
1. Grow Mg₂IrH₅ thin films via pulsed laser deposition (PLD) or sputtering
2. Characterize structure (XRD), composition (RBS/NRA), and transport (resistivity vs. T)
3. Establish baseline superconducting properties (if any) of Mg₂IrH₅ films

### Phase 2: Hydrogen Insertion Trials (Months 6-18)
1. **Ion implantation series**: Vary dose, energy, temperature, isotope (H vs D)
2. **Electrochemical series**: Vary gate voltage, temperature, ionic liquid
3. **Plasma series**: Vary power, pressure, substrate temperature
4. After each treatment: measure resistivity vs. T, look for superconducting transition

### Phase 3: Characterization & Optimization (Months 18-24)
1. **Structural confirmation**: Synchrotron XRD to verify Mg₂IrH₆ phase
2. **Hydrogen quantification**: Nuclear reaction analysis (NRA) or neutron reflectometry
3. **Stability testing**: Monitor Tc decay over days/weeks at various storage temperatures
4. **Optimization**: Iterate on best-performing approach

---

## Risk Assessment

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Mg₂IrH₆ decomposes during/after insertion | High | Cryogenic processing, rapid characterization, deuterium isotope |
| Ion implantation damage destroys superconductivity | Medium | Optimize dose, post-implant anneal at low T |
| Films are poor quality (grain boundaries, defects) | Medium | Partner with experienced thin-film group |
| Mg₂IrH₆ Tc is lower than predicted | Low | Still scientifically valuable; DFT benchmarking |
| Approach doesn't work at all | Medium | Scientifically valuable negative result; publish and move on |

---

## Why This Hasn't Been Tried

1. **Strobel's success with Mg₂IrH₅ is very recent** (2024)—the community hasn't had time to pivot to kinetic approaches
2. **Thin-film hydride synthesis is rare**—most hydride groups use bulk/powder methods
3. **Ion implantation + superconductivity** is a niche intersection of expertise
4. **The "no barrier" DFT result** suggests kinetic approaches could work, but this insight isn't widely appreciated

---

## Required Expertise & Facilities

- **Thin film growth**: PLD or sputtering with Mg, Ir targets; hydrogenation capability
- **Ion implantation**: Access to low-energy implanter with cryogenic stage
- **Transport measurements**: Dilution refrigerator or PPMS down to 2K
- **Structural characterization**: Lab XRD + synchrotron beamtime
- **Hydrogen quantification**: NRA or SIMS

**Ideal collaborators**:
- High-pressure hydride group (for Mg₂IrH₅ powder/target synthesis)
- National lab beamline access (APS, NSLS-II)

---

## Expected Outcomes

**Best case**: Demonstration of superconductivity in Mg₂IrH₆ thin films at ambient pressure, Tc > 77K. This would be transformative and high-impact (Nature/Science level).

**Likely case**: Partial hydrogen insertion achieved, Tc enhancement observed but below predictions. Publishable in PRL/PRB, guides future bulk synthesis attempts.

**Worst case**: No stable Mg₂IrH₆ phase achieved. Publishable negative result with quantitative analysis of decomposition kinetics. Valuable for the field.

---

## References

1. Strobel et al., "Synthesis of Mg₂IrH₅," PRB 110, 214513 (2024)
2. Dolui et al., "Feasible Route to High-Tc Ambient Hydride Superconductors," PRL 132, 166001 (2024)
3. Gao et al., "Prediction of Mg₂XH₆ superconductors," npj Comp. Mat. (2024)
4. Deng & Chu, "Pressure-quench protocol," PNAS 122, e2501048122 (2025)
5. Sun et al., "FeSe pressure quench," PNAS 118, e2108938118 (2021)

---

## Contact

This proposal was developed through systematic analysis of the superconductor literature and computational predictions. For discussion or collaboration inquiries, contact:

**[Your name and email here]**

---

*Generated with assistance from Claude (Anthropic) as part of the Claude Mind research project.*
*Repository: https://github.com/tmad4000/claude-mind*
