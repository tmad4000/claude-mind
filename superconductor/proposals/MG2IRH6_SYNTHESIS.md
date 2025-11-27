# Research Proposal: Completing Mg2IrH6 Synthesis

**Goal**: Achieve ambient-pressure high-temperature superconductivity by inserting one hydrogen atom into existing Mg2IrH5

**Potential Impact**: If successful, this would be the first ambient-pressure superconductor above liquid nitrogen temperature (77K). Predicted Tc: 103-160K.

---

## Background

### The Problem
Room-temperature superconductivity has been achieved in hydrides, but only at extreme pressures (100-200 GPa) requiring diamond anvil cells. Practical applications require ambient pressure.

### The Breakthrough
In 2024, researchers synthesized Mg2IrH5, which is:
- Structurally identical to superconducting Mg2IrH6 except for one H vacancy per formula unit
- Synthesizable under mild conditions (450°C, 100-250 bar H2)
- A direct precursor to Mg2IrH6 with NO ENERGY BARRIER for H insertion

### Current Status
- Mg2IrH5: Successfully synthesized, 80-90% phase pure
- Mg2IrH6: NOT YET SYNTHESIZED despite having a clear pathway
- Mg2IrH6 is metastable (60 meV/atom above convex hull) but kinetically accessible

---

## Proposed Approaches

### 1. Ion Implantation (HIGH PRIORITY)
**Method**: Implant H+ ions directly into Mg2IrH5 crystal structure
**Rationale**:
- No energy barrier for H insertion (VCNEB calculations)
- Can achieve non-equilibrium states
- Well-established technique for doping semiconductors

**Challenges**:
- Damage to crystal structure from implantation
- Achieving uniform distribution
- Optimal energy/dose to reach hydrogen sites

**Suggested Protocol**:
1. Prepare high-quality Mg2IrH5 thin films or pellets
2. H+ implantation at various energies (1-10 keV)
3. Post-implant anneal at moderate temperature
4. Characterize with XRD for structure, resistivity for Tc

### 2. High-Pressure H2 Annealing
**Method**: Expose Mg2IrH5 to high H2 pressure at elevated temperature
**Rationale**:
- Higher chemical potential of H should drive insertion
- Original synthesis uses 100-250 bar; try higher?
- Temperature may provide kinetic energy to overcome any subtle barriers

**Suggested Protocol**:
1. Synthesize Mg2IrH5 (standard conditions)
2. Anneal under 500-1000 bar H2 at 300-500°C
3. Rapid quench to trap metastable Mg2IrH6
4. Measure immediately before H loss

### 3. Electrochemical Hydrogenation
**Method**: Electrochemically drive H into Mg2IrH5
**Rationale**:
- Precise control of H chemical potential
- Room temperature process
- Can monitor in situ

**Challenges**:
- Need appropriate electrolyte
- Mg2IrH5 may not be stable in electrolyte
- Interface effects

### 4. Thin Film + H2 Plasma
**Method**: Deposit Mg2IrH5 thin film, expose to H2 plasma
**Rationale**:
- Atomic H is more reactive than molecular H2
- Thin films may more easily achieve full hydrogenation
- Can integrate with superconductor characterization

**Suggested Protocol**:
1. PVD/MBE deposition of Mg-Ir alloy
2. Anneal in H2 to form Mg2IrH5
3. Expose to H2 plasma at various conditions
4. In-situ resistance measurement

---

## Characterization Needs

### To Confirm Mg2IrH6 Formation
1. **XRD**: Should show Fm3̄m structure (same as Mg2IrH5 but higher symmetry)
2. **Neutron diffraction**: Locate hydrogen positions precisely
3. **Raman/IR spectroscopy**: IrH6 vibrational modes

### To Confirm Superconductivity
1. **Resistivity vs Temperature**: Sharp transition to zero resistance
2. **Magnetic susceptibility**: Meissner effect (diamagnetic below Tc)
3. **Specific heat**: Jump at Tc

---

## Resource Requirements

### Equipment
- Ion implanter with H+ capability
- High-pressure H2 furnace (up to 1000 bar)
- Thin film deposition system (MBE or PVD)
- Low-temperature resistivity measurement (down to 4K)
- SQUID magnetometer
- XRD

### Materials
- Mg powder (high purity)
- Ir powder or sputtering target (expensive but small amounts)
- H2 gas (high purity)

### Estimated Timeline
- 3 months: Set up synthesis of Mg2IrH5
- 3 months: Attempt H insertion via multiple methods
- 3 months: Characterization and iteration
- Total: ~9 months for initial results

---

## Why This Hasn't Been Done

1. **Recent discovery**: The Mg2IrH5 synthesis paper is from 2024
2. **Iridium cost**: Ir is expensive (~$150/g), limiting large-scale attempts
3. **Non-equilibrium challenge**: Standard equilibrium synthesis favors Mg2IrH5
4. **Metastability**: Mg2IrH6 is above convex hull, needs kinetic trapping

---

## Risk Assessment

**Technical Risks**:
- H insertion may require more activation than predicted
- Mg2IrH6 may decompose before measurement
- Actual Tc may be lower than predicted (DFT has uncertainties)

**Mitigation**:
- Multiple insertion methods increase probability of success
- Rapid quench and in-situ measurement
- Even 80K would be transformative (above LN2)

**Probability of Success**: Medium-High
- Precursor exists
- No barrier predicted
- Clear structural relationship

---

## Collaboration Opportunities

This would benefit from collaboration between:
- **Synthesis group**: Experience with metal hydrides, high-pressure
- **Theory group**: DFT calculations to optimize conditions
- **Characterization group**: Low-T measurement expertise

---

## If Successful

Achievement of Mg2IrH6 would:
1. Demonstrate first ambient-pressure high-Tc hydride superconductor
2. Open pathway to similar materials (Mg2RhH6, Mg2PdH6, etc.)
3. Enable practical superconductor applications without pressure apparatus
4. Validate computational predictions for ambient-pressure superconductors

---

*Proposal drafted: 2025-11-27*
*Based on: PRB 110, 214513 (2024), arXiv:2406.09538*
