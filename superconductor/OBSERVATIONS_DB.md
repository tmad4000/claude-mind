# Superconductor Observations Database

This database collects empirical observations, experimental findings, and phenomena that may contribute to understanding or achieving room-temperature superconductivity. Entries are categorized by type and linked to problems where relevant.

---

## OBSERVATION FORMAT
```
**OBS-SC-XXX**: [Title]
- **Type**: [Experimental | Theoretical | Computational | Pattern]
- **Source**: [Citation/Link]
- **Date**: [When discovered/published]
- **Description**: [What was observed]
- **Significance**: [Why it matters]
- **Related Problems**: [PROB-XXX links]
- **Potential Applications**: [Ideas this suggests]
- **Status**: [Verified | Disputed | Needs Replication]
```

---

## CATEGORY: MECHANISM INSIGHTS

### OBS-SC-001: Superexchange Confirmed in Cuprates
- **Type**: Experimental
- **Source**: J.C. Séamus Davis et al., PNAS 2022
- **Date**: September 2022
- **Description**: Atomic-scale experiment matched Cooper pair density variations with superexchange theory predictions in bismuth strontium calcium copper oxide.
- **Significance**: After 35 years, provides strong evidence for Anderson's superexchange mechanism. The "glue" binding electrons appears to be magnetic coupling through intermediate oxygen atoms.
- **Related Problems**: PROB-001, PROB-001a
- **Potential Applications**: Design materials that maximize superexchange coupling strength
- **Status**: Verified (widely accepted)

### OBS-SC-002: Electron Pairing Above Tc in Antiferromagnetic Insulator
- **Type**: Experimental
- **Source**: SLAC, August 2024
- **Date**: August 2024
- **Description**: Electron pairing (prerequisite for superconductivity) observed at temperatures above Tc in an antiferromagnetic insulating material. Material did not show zero resistance.
- **Significance**: Pairing and superconductivity can be decoupled. Engineering similar materials might enable higher Tc.
- **Related Problems**: PROB-001, PROB-006
- **Potential Applications**: Understanding what prevents paired electrons from superconducting might reveal new design principles
- **Status**: Verified

### OBS-SC-003: Pair Density Wave State Visualized
- **Type**: Experimental
- **Source**: University of Oxford, Macroscopic Quantum Matter Group
- **Date**: 2024
- **Description**: New phase of matter in high-temperature superconductors visualized using novel spectroscopic imaging STM technique.
- **Significance**: Long-predicted phase identified for first time in cuprates. Provides insights into high-Tc mechanism.
- **Related Problems**: PROB-001
- **Status**: Verified

---

## CATEGORY: MATERIALS DISCOVERIES

### OBS-SC-004: LaH₁₀ Record Tc (Near Room Temp)
- **Type**: Experimental
- **Source**: Drozdov et al., Nature 2019; reproduced by multiple groups
- **Date**: 2019-2024
- **Description**: LaH₁₀ superconducts at 250-260K at 170-180 GPa. Clathrate structure with H₂₄ cages around La.
- **Significance**: First material within ~40K of room temperature. Proves high-Tc is possible with right structure.
- **Related Problems**: PROB-003, PROB-003a
- **Potential Applications**: Template structure for lower-pressure analogs
- **Status**: Verified (multiple reproductions)

### OBS-SC-005: Nickelate Superlattice Superconductivity
- **Type**: Experimental
- **Source**: Nature Communications, November 2024
- **Date**: November 2024
- **Description**: First superconducting nickelate superlattices [(Nd₀.₈Sr₀.₂NiO₂)₈/(SrTiO₃)₂]₁₀ demonstrated.
- **Significance**: Nickelates now accessible in engineered superlattice form, enabling new experimental configurations.
- **Related Problems**: PROB-004, PROB-006
- **Status**: Verified

### OBS-SC-006: Ambient Pressure Nickelate via Strain
- **Type**: Experimental
- **Source**: Stanford/SLAC, February 2025
- **Date**: February 2025
- **Description**: Superconductivity stabilized in nickelate thin films at room pressure using substrate strain instead of external pressure.
- **Significance**: Proof of concept that strain engineering can replace high external pressure. Tc still low (-247°C to -231°C).
- **Related Problems**: PROB-003, PROB-003d
- **Potential Applications**: Apply strain engineering to hydrides?
- **Status**: Verified

### OBS-SC-007: LaBeH₈ Ternary Hydride at Lower Pressure
- **Type**: Experimental
- **Source**: Multiple groups, 2024
- **Date**: 2024
- **Description**: LaBeH₈ superconducts at ~110K at 80 GPa (vs ~170 GPa for binary hydrides).
- **Significance**: Ternary hydrides can achieve superconductivity at significantly lower pressures. Chemical pressure works.
- **Related Problems**: PROB-003, PROB-003b
- **Potential Applications**: Systematic search for ternary/quaternary hydrides
- **Status**: Verified

### OBS-SC-008: Al-Stabilized La Hydride at 223K
- **Type**: Experimental
- **Source**: National Science Review, 2024
- **Date**: 2024
- **Description**: La-Al hydride superconducts at 223K at 164 GPa. Metastable hexagonal LaH₁₀ phase stabilized by Al.
- **Significance**: Alloying can stabilize high-Tc metastable phases
- **Related Problems**: PROB-003, PROB-003c
- **Status**: Verified

---

## CATEGORY: COMPUTATIONAL PREDICTIONS

### OBS-SC-009: LaSc₂H₂₄ Predicted at 316K
- **Type**: Computational
- **Source**: PNAS, June 2024
- **Date**: June 2024
- **Description**: Calculations predict LaSc₂H₂₄ (novel H₂₄ + H₃₀ cage structure) could superconduct at 316K at 167 GPa.
- **Significance**: "Hot superconductivity" above room temperature may be achievable. Unusual cage geometry key.
- **Related Problems**: PROB-002, PROB-006
- **Potential Applications**: Target for experimental synthesis
- **Status**: Computational prediction (needs experimental verification)

### OBS-SC-010: >120 Hydrides with High Tc Identified
- **Type**: Computational
- **Source**: NIST DFT study, 2024
- **Date**: 2024
- **Description**: High-throughput screening of 900+ hydrides found 120+ with Tc exceeding MgB₂.
- **Significance**: Large pool of candidates for experimental testing
- **Related Problems**: PROB-007
- **Status**: Computational (awaiting synthesis)

### OBS-SC-011: Zentropy Theory Predicts Cu, Ag, Au Superconductivity
- **Type**: Theoretical
- **Source**: Penn State, 2025
- **Date**: 2025
- **Description**: New zentropy theory predicts superconductivity in Cu, Ag, Au at ultra-low temperatures.
- **Significance**: Theory can recover known results and may extend to new predictions. Bridges BCS and DFT.
- **Related Problems**: PROB-002
- **Status**: Theoretical (indirect support from known results)

---

## CATEGORY: STRUCTURE-PROPERTY RELATIONSHIPS

### OBS-SC-012: CuO₂ Planes Universal in Cuprates
- **Type**: Pattern
- **Source**: Literature consensus
- **Description**: All high-Tc cuprate superconductors contain CuO₂ planes. Tc correlates with number of planes per unit cell (up to a limit).
- **Significance**: The CuO₂ plane is the essential structural motif for cuprate superconductivity.
- **Related Problems**: PROB-001d
- **Potential Applications**: What is the analog motif for other mechanisms?

### OBS-SC-013: Clathrate Cages in Hydrides
- **Type**: Pattern
- **Source**: Literature on LaH₁₀, YH₆, etc.
- **Description**: High-Tc hydride superconductors form clathrate structures with hydrogen cages around metal atoms.
- **Significance**: Cage geometry affects density of states at Fermi level and phonon spectrum.
- **Related Problems**: PROB-006c
- **Potential Applications**: Design optimal cage geometries

### OBS-SC-014: Pressure-Tc Relationship Varies
- **Type**: Pattern
- **Source**: Multiple hydride studies
- **Description**: Tc vs pressure curve is not monotonic - some materials have optimal pressure, then Tc decreases.
- **Significance**: Understanding this could help find metastable phases that retain high Tc at lower pressure.
- **Related Problems**: PROB-003

### OBS-SC-015: Layer-Dependent Tc in Nickelates
- **Type**: Experimental
- **Source**: Multiple 2024 studies
- **Description**: Bilayer La₃Ni₂O₇ has higher Tc (80K) than infinite-layer nickelates (~15K).
- **Significance**: Layer count matters; there may be optimal layer configuration.
- **Related Problems**: PROB-006c

---

## CATEGORY: ANOMALIES & CONTROVERSIES

### OBS-SC-016: LK-99 False Positive
- **Type**: Experimental (Refuted)
- **Source**: Multiple replication attempts, 2023
- **Date**: July-August 2023
- **Description**: Initial claims of room-temp superconductivity in copper-doped lead apatite. Actually due to Cu₂S impurity phase transition.
- **Significance**: Cautionary tale. Phase transitions can mimic superconducting signatures. Importance of complete characterization.
- **Related Problems**: PROB-008
- **Lessons**: Resistance drop alone is insufficient evidence. Meissner effect and other tests required.
- **Status**: Refuted

### OBS-SC-017: CSH Room Temperature Claim (Retracted)
- **Type**: Experimental (Disputed)
- **Source**: Nature (retracted)
- **Description**: Claimed 288K superconductivity in carbonaceous sulfur hydride. Paper retracted due to data concerns.
- **Significance**: Highlights need for rigorous verification protocols, especially for extraordinary claims.
- **Related Problems**: PROB-008
- **Status**: Retracted/Disputed

---

## CATEGORY: THEORETICAL LIMITS

### OBS-SC-018: BCS Tc Limit ~40K
- **Type**: Theoretical
- **Source**: McMillan 1968, updated estimates
- **Description**: Conventional electron-phonon coupling has theoretical Tc limit around 30-40K due to phonon energy constraints.
- **Significance**: Room-temp superconductivity requires either: (a) different mechanism, or (b) light atoms (H) with high phonon frequencies.
- **Related Problems**: PROB-001, PROB-003

### OBS-SC-019: Fundamental Constants Allow Tc up to 100-1000K
- **Type**: Theoretical
- **Source**: Journal of Physics: Condensed Matter, 2025
- **Date**: 2025
- **Description**: Analysis of fundamental constants suggests upper Tc limit in range 100-1000K is compatible with physics.
- **Significance**: Room-temperature superconductivity is not forbidden by fundamental physics - it's an engineering problem.
- **Related Problems**: PROB-001

### OBS-SC-020: Conventional Superconductor Limit ~100-120K at Ambient Pressure
- **Type**: Computational
- **Source**: Nature Communications, 2025
- **Date**: 2025
- **Description**: Analysis of 20,000+ electron-phonon calculations suggests hypothetical compounds could reach 100-120K, far below room temp but above current conventional records.
- **Significance**: Conventional mechanism insufficient for room-temp at ambient pressure. Need unconventional mechanisms.
- **Related Problems**: PROB-002, PROB-006

---

## CATEGORY: SYNTHESIS TECHNIQUES

### OBS-SC-021: Topotactic Reduction for Nickelates
- **Type**: Experimental Technique
- **Source**: Multiple 2024 papers
- **Description**: Atomic hydrogen reduction can convert perovskite nickelates to infinite-layer phase while preserving film quality.
- **Significance**: Enables access to metastable phases not achievable by direct synthesis.
- **Related Problems**: PROB-004a
- **Status**: Active development

### OBS-SC-022: Laser Heating in DAC for Hydrides
- **Type**: Experimental Technique
- **Source**: Standard hydride synthesis protocol
- **Description**: Laser heating of precursors in diamond anvil cells drives hydride formation.
- **Significance**: Primary route to high-pressure hydride synthesis.
- **Related Problems**: PROB-004
- **Status**: Standard method

---

## CATEGORY: TERNARY HYDRIDE PATTERNS (Session 2025-11-27)

### OBS-SC-023: AcBeH8 Predicted at 181K / 10 GPa
- **Type**: Computational
- **Source**: Physical Review B 109, 014501 (Jan 2024), arXiv:2411.19028
- **Date**: 2024
- **Description**: fcc AcBeH8 predicted dynamically stable down to 10 GPa with Tc = 181K. Multiple stable/metastable Ac-Be-H compounds identified.
- **Significance**: MAJOR - Only 10 GPa is achievable without diamond anvils! Be-H bonds provide chemical precompression allowing near-ambient stability.
- **Related Problems**: PROB-003 (pressure reduction)
- **Potential Applications**: Experimental synthesis target - lower pressure than any other high-Tc hydride
- **Status**: Computational prediction (not yet synthesized)
- **Note**: Actinium is radioactive, limiting practical applications, but proves the concept

### OBS-SC-024: YBeH8 Predicted at 201K / 200 GPa
- **Type**: Computational
- **Source**: Journal of Chemical Physics (2024), iScience 2025
- **Date**: 2024
- **Description**: YBeH8 predicted to have Tc = 201K at 200 GPa. Be-H alloy backbone contributes ~85% of electron-phonon coupling.
- **Significance**: Confirms Be-H backbone is key to high Tc in this structure type
- **Related Problems**: PROB-003, PROB-006
- **Status**: Computational prediction

### OBS-SC-025: Heavy Rare Earth XBeH8 Series
- **Type**: Computational
- **Source**: iScience 2025
- **Date**: 2025
- **Description**: TmBeH8 (41-48K @ 80 GPa), YbBeH8 (134-145K @ 100 GPa), LuBeH8 (228-245K @ 140 GPa) predicted.
- **Significance**: Shows progression - heavier rare earths can increase Tc but also increase required pressure
- **Related Problems**: PROB-003, PROB-006
- **Status**: Computational predictions

### OBS-SC-026: ScC2H8 - Carbon as Stabilizer
- **Type**: Computational
- **Source**: J. Phys. Chem. C (2024), npj Comp. Mat. (2024)
- **Date**: 2024
- **Description**: ScC2H8 predicted stable above 50 GPa with superconducting properties. Carbon acts as stabilizer like Be.
- **Significance**: Expands the stabilizer palette beyond Be/B/Al - carbon compounds may offer new pathways
- **Related Problems**: PROB-006
- **Status**: Computational prediction

### OBS-SC-027: Mg2XH6 Family at Ambient Pressure
- **Type**: Computational
- **Source**: npj Computational Materials (2024)
- **Date**: 2024
- **Description**: Mg2XH6 (X = Rh, Ir, Pd, Pt) predicted to achieve ambient pressure superconductivity above 80K.
- **Significance**: If verified, this would be a major breakthrough - no pressure required!
- **Related Problems**: PROB-003 (pressure = 0!)
- **Status**: Computational prediction - HIGH PRIORITY FOR VERIFICATION

### OBS-SC-028: Pattern - Be-H Backbone Drives High Tc
- **Type**: Pattern
- **Source**: Multiple 2024-2025 papers
- **Description**: Across LaBeH8, YBeH8, AcBeH8, the Be-H bonds contribute 80-90% of electron-phonon coupling. The rare earth element modulates stability pressure.
- **Significance**: Design principle - optimize the Be-H network, use rare earth to tune pressure
- **Related Problems**: PROB-006, PROB-003

### OBS-SC-029: Trade-off Between Tc and Pressure
- **Type**: Pattern
- **Source**: Multiple papers analysis
- **Description**: Within XBeH8 family, heavier X = higher Tc but also higher required pressure. There's no free lunch.
- **Significance**: Suggests we may need fundamentally different approach for true ambient pressure high-Tc
- **Related Problems**: PROB-003

### OBS-SC-030: ThBeH8 at Low Pressure (7-10 GPa)
- **Type**: Computational
- **Source**: ScienceDirect (2024), arXiv, PMC
- **Date**: 2024
- **Description**: ThBeH8 predicted stable down to 7 GPa with Tc = 98-113K. Uses "fluorite-type" structure. Chemical template effect provides stability.
- **Significance**: Non-radioactive alternative to AcBeH8. 7-10 GPa is achievable with multi-anvil apparatus.
- **Related Problems**: PROB-003
- **Status**: Computational prediction - synthesis candidate

### OBS-SC-031: LaBH8 Boron Stabilizer
- **Type**: Computational
- **Source**: npj Comp. Mat. (2021), Phys. Rev. B
- **Date**: 2021
- **Description**: LaBH8 predicted to have Tc = 126-156K at 40-55 GPa. "Sodalite clathrate" structure with B replacing Be.
- **Significance**: Shows boron works as stabilizer, opens additional compositional space
- **Related Problems**: PROB-006
- **Status**: Computational prediction

### OBS-SC-032: Research Gap - CeBeH8, NdBeH8 Not Studied
- **Type**: Gap
- **Source**: Literature search 2025-11-27
- **Description**: Despite LaBeH8, YBeH8, TmBeH8, YbBeH8, LuBeH8, AcBeH8, ThBeH8 all being studied, CeBeH8 and NdBeH8 have NO publications found.
- **Significance**: Obvious gap in systematic studies. Ce and Nd are adjacent to La - should be straightforward DFT.
- **Related Problems**: PROB-006
- **Status**: OPPORTUNITY

### OBS-SC-033: Research Gap - La-Li-H System Not Studied
- **Type**: Gap
- **Source**: Literature search 2025-11-27
- **Description**: Li is lighter than Be and should provide stronger chemical precompression. No La-Li-H superconductor studies found.
- **Significance**: If Li works better than Be, this could be important
- **Related Problems**: PROB-003, PROB-006
- **Status**: OPPORTUNITY

### OBS-SC-034: Mg2IrH5 Synthesized - Pathway to Mg2IrH6
- **Type**: Experimental
- **Source**: Phys. Rev. B 110, 214513 (2024), arXiv:2406.09538
- **Date**: 2024
- **Description**: Mg2IrH5 has been synthesized under mild conditions. It is isostructural with predicted superconducting Mg2IrH6 except for one H vacancy. Favorable barrier for H insertion.
- **Significance**: MAJOR - Experimental pathway to ambient-pressure superconductor exists! Mg2IrH6 predicted at 103-160K at ambient pressure.
- **Related Problems**: PROB-003
- **Potential Applications**: Non-equilibrium processing of Mg2IrH5 may yield Mg2IrH6
- **Status**: Experimental progress - VERY HIGH PRIORITY
- **Detailed Synthesis Info**:
  - Low-P method: 450°C, 100-250 bar H2, 2 weeks, 80-90% pure
  - High-P DAC: 10-28 GPa, 800-2500K, laser heating
  - H insertion: NO BARRIER from Mg2IrH5 → Mg2IrH6 (VCNEB calculations)
  - Mg2IrH6 is 60 meV/atom above convex hull (metastable)
  - Suggested methods: deposition or implantation

### OBS-SC-035: IrH6 Vibrations Drive Superconductivity
- **Type**: Theoretical
- **Source**: Angewandte Chemie 2024
- **Date**: 2024
- **Description**: In Mg2IrH6, superconductivity comes from IrH6⁴⁻ molecular vibrations with eg* states at Fermi level. In Ca2IrH6 this is quenched by Ca d backdonation.
- **Significance**: Explains WHY Mg works but Ca doesn't - design principle for similar compounds
- **Related Problems**: PROB-001, PROB-006

### OBS-SC-036: B-C Clathrates with NH4 - Another Ambient Path
- **Type**: Computational
- **Source**: Communications Physics (2024), arXiv:2311.01656
- **Date**: 2024
- **Description**: Hydride units (NH4) inserted into B-C clathrates. SrNH4B6C6 predicted at 85K ambient pressure. PbNH4B6C6 predicted at 115K ambient pressure. 24 compounds with 55 crystal structures dynamically stable.
- **Significance**: Alternative approach to ambient-pressure superconductivity - not based on MH6 octahedra but on molecular hydrides in clathrate cages
- **Related Problems**: PROB-003, PROB-006
- **Synthesis Note**: Precursor SrB3C3 synthesized at 50 GPa - quench to ambient may work
- **Status**: Computational prediction

### OBS-SC-037: Li2AgH6, Li2AuH6 Near Theoretical Limit
- **Type**: Computational/Theoretical
- **Source**: npj Computational Materials (2024), Nature Communications (2025)
- **Date**: 2024-2025
- **Description**: Li2AgH6 and Li2AuH6 identified as approaching the practical limit for conventional (BCS) superconductivity at ambient pressure. Higher-Tc compounds tend to be thermodynamically unstable.
- **Significance**: Suggests there may be a ceiling for conventional ambient-pressure superconductors. Room-temp may require unconventional mechanism.
- **Related Problems**: PROB-002, PROB-003

### OBS-SC-038: MB2C8 Clathrates (M=Na,K,Rb,Cs)
- **Type**: Computational
- **Source**: Phys. Rev. B (2024)
- **Date**: 2024
- **Description**: Boron-carbon clathrates MB2C8 predicted near 70K at ambient pressure
- **Significance**: Another family of potential ambient-pressure superconductors
- **Related Problems**: PROB-003, PROB-006

---

## INDEX BY PROBLEM

| Problem | Related Observations |
|---------|---------------------|
| PROB-001 (Mechanism) | OBS-SC-001, 002, 003, 018, 019 |
| PROB-002 (Prediction) | OBS-SC-009, 010, 011, 020 |
| PROB-003 (Pressure) | OBS-SC-004, 006, 007, 008, 014 |
| PROB-004 (Synthesis) | OBS-SC-005, 021, 022 |
| PROB-006 (Search) | OBS-SC-002, 005, 009, 012, 013, 015, 020 |
| PROB-007 (Computation) | OBS-SC-010 |
| PROB-008 (Reproducibility) | OBS-SC-016, 017 |

---

## IDEA SEEDS (Observations Without Clear Application Yet)

### SEED-001: Photoinduced Superconductivity
Some materials show transient superconducting-like behavior when hit with specific light frequencies. Mechanism unclear. Could this be sustained?

### SEED-002: Twisted Bilayer Graphene Superconductivity
At specific "magic angles", twisted bilayer graphene superconducts at ~1.7K. Flat bands + strong correlations. Can this approach be extended to higher Tc?

### SEED-003: Interface Superconductivity
Some non-superconducting materials superconduct at their interfaces. LAO/STO interface is example. Interface engineering could be powerful.

### SEED-004: Superconducting Diodes
Asymmetric superconductivity (different critical current in different directions) recently discovered. May enable new applications.

---

*Last updated: 2025-11-27*
*Total observations: 22*
*Idea seeds: 4*
