# Synthesis Feasibility Assessment for Ambient-Pressure Superconductor Candidates

Generated 2025-11-27 as part of research director exercise.

This document assesses the practical feasibility of synthesizing the most promising ambient-pressure high-Tc superconductor candidates.

---

## TIER 1: CLOSEST TO SUCCESS

### Mg₂IrH₆ (Predicted 103-160K)

**Feasibility: HIGH**

**Why it's close**:
- Precursor Mg₂IrH₅ has been **synthesized experimentally** (PRB 2024)
- Synthesis conditions: 450°C, 100-250 bar H₂, 2 weeks
- Purity achieved: 80-90%
- Only ONE hydrogen atom away from the predicted superconductor
- DFT predicts **no energy barrier** for H insertion

**Remaining challenges**:
- Mg₂IrH₆ is 60 meV/atom above convex hull (metastable)
- Need non-equilibrium processing to kinetically trap the phase
- May require rapid quench, ion implantation, or plasma treatment

**Equipment needed**:
- High-pressure H₂ system (100-1000 bar)
- Ion implanter (1-10 keV H⁺)
- Plasma chamber
- SQUID magnetometer
- Neutron beamline (for H stoichiometry)

**Cost estimate**: $$ (standard equipment, Ir cost ~$150/g is significant but tractable)

**Timeline to first attempt**: 3-6 months

---

### Mg₂RhH₆ / Mg₂RuH₆ (Predicted 45-80K)

**Feasibility: HIGH**

**Why it's promising**:
- Mg₂RuH₄ already synthesized - same pathway as Ir case
- Ru is 10x cheaper than Ir ($15/g vs $150/g)
- Rh is also cheaper (~$500/g)
- Lower predicted Tc but still above liquid nitrogen

**Remaining challenges**:
- Need to demonstrate H insertion works for 4d metals like it should for 5d
- May have different kinetics than Ir case

**Equipment needed**: Same as Mg₂IrH₆

**Cost estimate**: $ (cheaper metals)

**Timeline to first attempt**: 3-6 months (could run in parallel with Ir)

---

## TIER 2: PROMISING BUT HARDER

### BSiC₂ (Predicted 74K)

**Feasibility: MEDIUM-LOW**

**Why it's attractive**:
- **Hydrogen-free** - eliminates all H-related challenges
- Stoichiometric - no doping optimization
- Ambient pressure - no diamond anvil cells
- Based on well-known SiC technology

**Remaining challenges**:
- **No precursor compound** - must synthesize from scratch
- Specific BSiC₂ stoichiometry may be metastable
- B solubility in SiC is only 0.2 wt% under normal conditions
- Never attempted in 5 years since prediction - unknown unknowns

**Possible synthesis routes**:
1. **MBE/CVD**: Layer-by-layer deposition (B-C-Si-C-B-C...)
2. **High-P/High-T**: Force B into SiC under extreme conditions
3. **Spark plasma sintering**: Rapid access to metastable phases
4. **Ion implantation**: Heavy B implantation into SiC

**Equipment needed**:
- MBE or CVD system
- High-temperature/high-pressure apparatus
- Spark plasma sintering system
- XRD, Raman for structure verification

**Cost estimate**: $$$ (significant equipment, many unknowns)

**Timeline to first attempt**: 6-12 months

**Recommendation**: Worth doing DFT to calculate convex hull energy and identify barriers before experimental work.

---

### La₃Ni₂O₇ (Strain-Stabilized, ~26K zero-resistance)

**Feasibility: HIGH (but lower Tc)**

**Why it works**:
- **Already demonstrated** at SLAC (Feb 2025)
- Thin-film growth is mature technology
- Substrate strain substitutes for pressure
- Compatible with device fabrication

**Current status**:
- Transition onset: -247°C to -231°C
- True zero-resistance: -271°C (2K)
- This is proof-of-concept, not optimized

**Optimization opportunities**:
- Different substrates for different strain levels
- Other Ruddlesden-Popper nickelates (La₄Ni₃O₁₀)
- Doping (Sr, Ca substitution)
- Could potentially reach higher Tc

**Equipment needed**:
- MBE or PLD system
- Various substrates (SrTiO₃, LSAT, LaAlO₃)
- Low-temperature transport measurement

**Cost estimate**: $$ (standard thin-film growth)

**Timeline to first attempt**: 1-3 months (building on published work)

---

## TIER 3: HIGH-RISK/HIGH-REWARD

### B-C Clathrates with NH₄ (PbNH₄B₆C₆: 115K, SrNH₄B₆C₆: 85K)

**Feasibility: LOW-MEDIUM**

**Why it's interesting**:
- Different structural approach from hydrides
- SrB₃C₃ precursor synthesized (at 50 GPa)
- 24 compounds predicted stable

**Remaining challenges**:
- Precursor requires 50 GPa - not easy to access
- NH₄ insertion step is speculative
- Complex ternary/quaternary chemistry

**Equipment needed**:
- Diamond anvil cell (50 GPa capability)
- Quenching apparatus
- NH₄ source for insertion

**Cost estimate**: $$$ (high-pressure synthesis is expensive)

**Timeline**: 12+ months

---

## SYNTHESIS PRIORITY RANKING

| Rank | Material | Feasibility | Potential | Recommendation |
|------|----------|-------------|-----------|----------------|
| 1 | Mg₂IrH₆ | HIGH | 103-160K | **START NOW** |
| 2 | Mg₂RuH₆/RhH₆ | HIGH | 45-80K | Run in parallel |
| 3 | La₃Ni₂O₇ (strain) | HIGH | ~40K (optimized?) | Build on SLAC work |
| 4 | BSiC₂ | MEDIUM | 74K | DFT first, then attempt |
| 5 | B-C clathrates | LOW | 85-115K | Long-term exploration |

---

## RESOURCE ALLOCATION RECOMMENDATION

For a research group with $1M annual budget and 5 researchers:

**Year 1**:
- 50% on Mg₂IrH₆/Mg₂RhH₆ synthesis (2-3 researchers)
- 30% on La₃Ni₂O₇ strain optimization (1-2 researchers)
- 20% on BSiC₂ DFT + initial synthesis attempts (1 researcher)

**Decision point at 12 months**:
- If Mg₂IrH₆ works → scale up
- If Mg₂IrH₆ fails → pivot to cheaper Rh/Ru variants or BSiC₂
- If La₃Ni₂O₇ reaches >50K → major effort on nickelate optimization

---

## KEY CONTACTS (Suggested Collaborations)

Based on published work:
- **Mg₂IrH₅ synthesis**: Authors of PRB 2024 paper on Mg₂IrH₅
- **Nickelate thin films**: Harold Hwang's group at SLAC/Stanford
- **High-pressure hydrides**: Russell Hemley (U. Illinois Chicago), Mikhail Eremets (MPI Mainz)
- **BSiC₂ theory**: Authors of New J. Phys. 2020 paper

---

*Last updated: 2025-11-27*
*Status: Initial assessment - to be refined with expert input*
