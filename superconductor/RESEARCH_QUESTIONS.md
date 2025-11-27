# Research Questions for Room-Temperature Superconductivity

Generated 2025-11-27 thinking as a research director with full lab access.
**Revised 2025-11-27** based on internal evaluation feedback.

---

## TIER 1: High Priority Experimental Questions

### RQ-001: Non-equilibrium H insertion into Mg2IrH5 (REVISED)
**Question**: What non-equilibrium processing method can successfully insert hydrogen into Mg2IrH5 to form superconducting Mg2IrH6, and how do we characterize partial success?

**Specific experiments**:
1. H+ ion implantation at varying energies (1-10 keV) into Mg2IrH5 pellets
2. H2 plasma exposure of Mg2IrH5 thin films at various temperatures
3. Electrochemical hydrogenation in aprotic electrolytes
4. High-pressure H2 annealing (500-1000 bar) followed by rapid quench

**Characterization plan** (critical for interpreting results):
- **Neutron diffraction**: Determine H stoichiometry (distinguish H5 vs H5.5 vs H6)
- **XRD**: Track lattice parameter changes (expect ~2% expansion with full H6)
- **SQUID magnetometry**: Look for diamagnetic signal even if partial
- **Raman spectroscopy**: IrH6 octahedral modes should appear at ~1800-2000 cm⁻¹
- **Transport**: Four-probe resistivity down to 4K

**Partial success scenarios**:
- Mg2IrH5.5: May show reduced Tc or fluctuating superconductivity
- Inhomogeneous insertion: Could create superconducting domains (look for percolation effects)
- Surface-only insertion: Thin-film approach may work better than bulk

**Success metrics**:
- PRIMARY: Zero resistance + Meissner effect at T > 77K
- SECONDARY: Diamagnetic signal at any T, reduced resistivity with H content
- TERTIARY: Spectroscopic evidence of IrH6 formation

**Go/No-go criteria**:
- After 6 months: If no evidence of H insertion beyond H5, pivot to Mg2RhH6
- After 12 months: If Tc < 40K, reassess theoretical predictions

**Why this matters**: Mg2IrH5 is the closest precursor to any predicted ambient-pressure high-Tc superconductor. No energy barrier for H insertion predicted.

**Resources needed**: Ion implanter, plasma chamber, high-pressure H2 system, SQUID magnetometer, cryostat, neutron beamline access

---

### RQ-002: What makes Mg optimal in M2IrH6? (REVISED - reframed positively)
**Question**: What electronic structure features of Mg enable high-Tc superconductivity in Mg2IrH6, and can we find OTHER elements that share these features?

**Hypothesis**: Mg's lack of low-lying d-states prevents "d-backdonation" that would quench the IrH6⁴⁻ eg* states at the Fermi level. Elements with this property should work.

**Specific experiments**:
1. **Substitution series**: (Mg1-xMx)2IrH6 for M = Be, Zn, Cd, Sr
   - Be (no d-states, lighter than Mg) - might be BETTER
   - Zn (filled 3d¹⁰) - tests if filled d-shell is sufficient
   - Cd (filled 4d¹⁰) - same test, different period
   - Sr (like Ca, has empty d) - confirm d-backdonation kills Tc
2. **Electronic structure mapping**: ARPES on each variant to track eg* states
3. **XAS at Ir L-edge**: Probe Ir 5d occupancy as function of M
4. **Transport**: Systematic Tc vs M to find optimal cation

**Design principles to extract**:
- What electronegativity range works?
- What ionic radius range works?
- Is the rule simply "no accessible d-states"?

**Predictive output**: A set of design rules for M in M2IrH6-type superconductors

**Why this matters**: Transforms negative finding ("Ca doesn't work") into positive design principle for rational material discovery.

**Resources needed**: High-pressure synthesis, ARPES beamline, XAS beamline

---

### RQ-003: Is there a lighter element that can replace Ir in Mg2MH6? (STRENGTHENED)
**Question**: Can we achieve similar or higher Tc with less expensive/lighter transition metals?

**Specific experiments**:
1. Systematic DFT screening of Mg2MH6 where M = all 4d and 5d transition metals
2. Focus on M = Ru, Rh, Pd (4d) as cheaper alternatives to Ir, Pt (5d)
3. Synthesize Mg2RuH6 - NOTE: Mg2RuH4 already synthesized! Same pathway as Mg2IrH5→H6
4. Test Mg2RhH6 - predicted 45-80K, Rh is ~10x cheaper than Ir

**Go/No-go criteria**:
- **DFT phase**: Screen completes in 2 months. Proceed only if predicted Tc > 40K for at least one 4d metal
- **Synthesis phase**: If no Mg2MH6 (M=4d) forms after 6 months, conclude 4d metals require different approach
- **Cost threshold**: Practical target is material cost <$10/g (vs Ir at $150/g)

**Priority ordering**:
1. **Ru** - Mg2RuH4 exists, cheapest ($15/g), similar chemistry
2. **Rh** - Higher predicted Tc (45-80K), mid-cost ($500/g but 10x cheaper than Ir)
3. **Pd** - Different d-electron count, interesting test case

**Why this matters**: Ir is $150/g. Even lab-scale studies require significant funding. Rh at $500/g is expensive but tractable. Ru at $15/g enables broader research.

**Resources needed**: DFT cluster (2-month allocation), high-pressure synthesis, superconductivity measurements

---

## TIER 2: Mechanistic Understanding Questions

### RQ-004: What's the actual Tc ceiling for BCS at ambient pressure?
**Question**: Is the ~100-150K ceiling for conventional superconductivity at ambient pressure a hard limit, and if so, why?

**Specific experiments**:
1. Comprehensive meta-analysis of all ambient-pressure superconductor predictions
2. Statistical analysis: What's the distribution of predicted Tc? Is there a cutoff?
3. Theoretical analysis: Derive the maximum possible λ×ω_log product at ambient pressure
4. Test the ceiling experimentally with Mg2IrH6 (predicted 103-160K)

**Why this matters**: If there's a hard ceiling, we need unconventional mechanisms for room-temp. If not, we just need to search harder.

**Resources needed**: Computational analysis, synthesis of highest-Tc candidates

---

### RQ-005: Can superexchange work at higher temperatures than cuprates?
**Question**: The cuprate mechanism (superexchange) reaches 135K. Is this a fundamental limit or an engineering problem?

**Specific experiments**:
1. Theoretical analysis: What sets the Tc in cuprates? J (exchange coupling) or something else?
2. Search for materials with stronger J values than cuprates
3. Nickelate optimization: La3Ni2O7 reaches 80K - can doping/strain push it higher?
4. Design new superexchange materials with DFT

**Why this matters**: If BCS has a ceiling, superexchange might not. But we don't understand it well enough.

**Resources needed**: Theory group, nickelate synthesis, ARPES

---

### RQ-006: Does the NH4 approach (B-C clathrates) have a higher ceiling?
**Question**: The NH4-in-clathrate approach (PbNH4B6C6 = 115K) is different from MH6 octahedra. Which has more headroom?

**Specific experiments**:
1. Systematic DFT of MNH4B6C6 family - which M gives highest Tc?
2. Can we substitute NH4 with other molecular hydrides (PH4+, BH4-)?
3. Synthesize SrB3C3 (precursor exists at 50 GPa) and attempt NH4 insertion
4. Compare phonon spectra and coupling between the two approaches

**Why this matters**: Two competing approaches to ambient-pressure superconductivity. Need to know which to prioritize.

**Resources needed**: DFT calculations, high-pressure synthesis, quenching experiments

---

## TIER 3: Exploratory/High-Risk Questions

### RQ-007: Can we combine multiple mechanisms?
**Question**: What if we combined phonon-mediated (BCS) and spin-mediated (superexchange) pairing in a single material?

**Specific experiments**:
1. Theoretical: Can both mechanisms cooperate or do they interfere?
2. Design a material with both: e.g., cuprate layer + hydrogen-rich layer heterostructure
3. Interface superconductivity: What happens at cuprate/hydride interfaces?
4. Twisted bilayer experiments with hydrogen intercalation

**Why this matters**: If mechanisms can add, we might break the ceiling of either one alone.

**Resources needed**: MBE for heterostructures, theory, low-T measurements

---

### RQ-008: What happens to Mg2IrH6 under light illumination?
**Question**: Can photoinduced effects enhance or stabilize superconductivity?

**Specific experiments**:
1. Transient optical spectroscopy on Mg2IrH6 (if synthesized)
2. Does light excitation of IrH6 vibrations enhance pairing?
3. Can we photostabilize the metastable Mg2IrH6 phase?
4. Compare to photoinduced superconductivity in K3C60

**Why this matters**: Non-equilibrium approaches are underexplored. Light could be a knob.

**Resources needed**: Ultrafast laser, cryogenic optical setup

---

### ~~RQ-009: Li as stabilizer instead of Be~~ REJECTED
**Original question**: Does La-Li-H system offer better properties than LaBeH8?

**Why rejected**: The premise "Li is lighter so it should be better" is mechanistically flawed. Mass is only ONE factor. Li vs Be differ in:
- Electron count (Li: 1s²2s¹ vs Be: 1s²2s²)
- Ionic charge tendency (Li⁺ vs Be²⁺)
- Bonding character (Li more ionic, Be more covalent)
- Atomic radius

The "chemical precompression" from Be comes from Be-H covalent bonding, not just mass. Li-H bonding is more ionic and likely creates different structures entirely.

**If pursuing anyway**: Would need to first establish WHY Be works via bonding analysis (not mass), then look for Li structures that achieve similar bonding. This is a theory project, not direct substitution.

---

### RQ-010: Can strain engineering work for hydrides like it does for nickelates?
**Question**: Substrate strain allowed nickelates to superconduct at ambient pressure. Can this work for hydrides?

**Specific experiments**:
1. Grow Mg2IrH5 thin films on various substrates with different lattice constants
2. Measure if H insertion is easier under tensile vs compressive strain
3. DFT: How does strain affect the Mg2IrH6 convex hull energy?
4. Could strain stabilize the metastable phase?

**Why this matters**: Would provide an alternative route to Mg2IrH6 that doesn't require non-equilibrium processing.

**Resources needed**: MBE/PVD, various substrates, in-situ characterization

---

## Questions for Experts

### For a high-pressure synthesis expert:
- What's the failure mode when trying to synthesize Mg2IrH6 from Mg2IrH5?
- Has anyone tried and failed? What did they observe?
- What non-equilibrium methods have you seen work for metastable hydrides?

### For a superconductivity theorist:
- Is the ~150K ceiling for BCS at ambient pressure fundamental or just current materials?
- What would it take to design a superexchange material with Tc > 200K?
- Are there mechanisms beyond BCS and superexchange we should explore?

### For an experimentalist working on cuprates:
- What's the actual bottleneck to higher Tc in cuprates? Is it understood?
- Has anyone tried cuprate/hydride heterostructures?
- What measurement challenges should we expect with Mg2IrH6?

---

## WILDCARD: Non-Hydride Approaches (added per evaluator suggestion)

The hydride field is crowded and competitive. These alternatives offer potentially less-traveled paths:

### RQ-011: Strain-engineered nickelates at ambient pressure (NEW)
**Question**: Can substrate strain achieve higher Tc nickelate superconductivity than the SLAC/Stanford result (26K true zero-resistance)?

**Background**: In Feb 2025, Harold Hwang's group at SLAC demonstrated that La₃Ni₂O₇ becomes superconducting at ambient pressure when grown as a thin film on a substrate providing lateral compression. This mimics high-pressure effects without diamond anvil cells.

**Specific experiments**:
1. Survey substrates with different lattice mismatch to La₃Ni₂O₇
2. Test both compressive and tensile strain regimes
3. Explore other Ruddlesden-Popper nickelates: La₄Ni₃O₁₀, La₂NiO₄
4. Combine strain with doping (Sr, Ca substitution)

**Advantage over hydrides**:
- Thin-film synthesis is mature technology
- Compatible with device fabrication
- Can use advanced characterization (ARPES, STM) impossible under high pressure

**Why promising**: Nickelates are isoelectronic to cuprates. Cuprates reach 135K. If nickelates can be optimized similarly, 100K+ at ambient pressure is plausible.

**Resources needed**: MBE/PLD growth, various substrates, transport/magnetometry

---

### RQ-012: BSiC₂ synthesis - hydrogen-free 74K superconductor (NEW)
**Question**: Can BSiC₂ be synthesized and does it actually superconduct at 74K as predicted?

**Background**: DFT predicts BSiC₂ is a BCS superconductor at 74K at AMBIENT PRESSURE with NO hydrogen. This would be revolutionary - hydrogen-free, no pressure required, stoichiometric.

**Status**: PURELY THEORETICAL - no experimental attempts found in literature. This is a gap.

**Specific experiments**:
1. High-temperature CVD from B, Si, C precursors
2. Arc melting of B₄C + Si
3. Mechanical alloying of elemental powders followed by high-P/high-T treatment
4. Thin-film deposition via co-sputtering

**Challenges**:
- BSiC₂ may be metastable - need to explore synthesis conditions
- May require non-equilibrium processing (like hydrides)
- No precursor compounds known

**Why pursue**: If successful, this circumvents ALL the problems of hydrides (pressure, stability, hydrogen handling). Even if Tc is lower than predicted, any ambient-pressure superconductor >30K is significant.

**Resources needed**: CVD/PVD systems, high-temperature furnaces, XRD, transport

---

### RQ-013: Interface superconductivity at oxide heterostructures (NEW)
**Question**: Can interface effects between different oxides create higher-Tc superconductivity than bulk materials?

**Background**: LaAlO₃/SrTiO₃ interface shows 2D superconductivity. Cuprate/manganite interfaces show enhanced pairing. What about designed interfaces between known superconductors and other functional oxides?

**Specific experiments**:
1. YBCO/La₃Ni₂O₇ interface - combine cuprate with nickelate
2. YBCO/SrTiO₃ - interface with quantum paraelectric
3. Superlattices of multiple cuprate types
4. Electric-field tuning of interface carrier density

**Why speculative but worthwhile**: Interface effects can stabilize phases that don't exist in bulk. The 2D confinement may enhance pairing. This is relatively unexplored territory.

**Resources needed**: MBE, RHEED, transport, STEM

---

## Risk/Reward Assessment

| Question | Risk | Potential Reward | Time to Result |
|----------|------|------------------|----------------|
| RQ-001 (Mg2IrH6) | Medium | Revolutionary if works | 6-12 months |
| RQ-002 (Design rules) | Low | High scientific value | 12-18 months |
| RQ-003 (Cheaper metals) | Medium | Practical applications | 6-12 months |
| RQ-011 (Nickelates) | Low | Incremental progress | 6 months |
| RQ-012 (BSiC₂) | Very High | Revolutionary if works | 12+ months |
| RQ-013 (Interfaces) | High | Unknown - exploratory | 12+ months |

**Portfolio recommendation**:
- 60% effort on RQ-001/002/003 (hydrides - closest to success)
- 25% on RQ-011 (nickelates - proven approach, lower risk)
- 15% on RQ-012/013 (wildcards - high risk, high potential)

---

*Generated: 2025-11-27*
*Revised: 2025-11-27 based on internal evaluation*
*Status: READY FOR EXPERT REVIEW*
