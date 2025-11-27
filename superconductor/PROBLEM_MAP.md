# Room-Temperature Superconductor: Problem Map

**Goal**: Achieve superconductivity at room temperature (~300K) and ambient pressure

**Status**: Active research area. Current records:
- **Cuprates**: ~135K at ambient pressure (HgBa₂Ca₂Cu₃O₈₊ₓ)
- **Hydrides**: ~260K at 170-180 GPa (LaH₁₀), ~203K at 155 GPa (H₃S)
- **Nickelates**: ~80K at high pressure (La₃Ni₂O₇)

---

## 1. FUNDAMENTAL THEORY GAP

### 1.1 Mechanism of High-Tc Superconductivity Unknown
**Problem ID**: PROB-001
**Status**: Partially resolved (cuprates), Active research
**Description**: We don't have a complete theory explaining why cuprates superconduct at high temperatures. BCS theory (electron-phonon coupling) explains conventional superconductors but fails for unconventional ones.

**Recent Progress**:
- 2022 experiment confirmed superexchange mechanism in cuprates (J.C. Séamus Davis et al.)
- Spin fluctuation hypothesis gaining support
- But: No predictive theory exists that can tell us which materials will superconduct

**Subproblems**:
- [ ] PROB-001a: What is the "glue" binding Cooper pairs in cuprates?
- [ ] PROB-001b: Why does d-wave symmetry emerge instead of s-wave?
- [ ] PROB-001c: Role of antiferromagnetic fluctuations vs structural features
- [ ] PROB-001d: Why is the CuO₂ plane so special?

**Key Questions**:
- Can superexchange provide enough binding energy for room-temp Tc?
- What structural motifs maximize superexchange coupling?

---

### 1.2 No Predictive Theory for Tc
**Problem ID**: PROB-002
**Status**: Major bottleneck
**Description**: We cannot predict from first principles whether a given material will superconduct, or at what temperature.

**Current Approaches**:
- McMillan-Allen-Dynes formula (works for conventional BCS superconductors only)
- DFT + electron-phonon calculations (computationally expensive, limited accuracy)
- Zentropy theory (new - Penn State, 2025)
- Machine learning (requires training data, can't extrapolate to new mechanisms)

**Subproblems**:
- [ ] PROB-002a: Electron correlation effects too complex for DFT
- [ ] PROB-002b: Strong coupling regime poorly understood
- [ ] PROB-002c: Anharmonic effects in hydrides hard to calculate
- [ ] PROB-002d: Database of high-Tc materials insufficient for ML training

---

## 2. MATERIALS ENGINEERING BOTTLENECKS

### 2.1 Extreme Pressure Requirement (Hydrides)
**Problem ID**: PROB-003
**Status**: Major bottleneck
**Description**: Best hydride superconductors require pressures of 100-200 GPa, only achievable in diamond anvil cells.

**Current State**:
- LaH₁₀: ~260K at 170-180 GPa
- H₃S: ~203K at 155 GPa
- Ternary hydrides (LaBeH₈): ~110K at 80 GPa
- Goal: Ambient pressure (~0.0001 GPa)

**Subproblems**:
- [ ] PROB-003a: How to stabilize hydrogen-rich structures at low pressure?
- [ ] PROB-003b: Can chemical precompression replace external pressure?
- [ ] PROB-003c: Metastable high-pressure phases that survive decompression?
- [ ] PROB-003d: Substrate strain engineering (works for nickelates, can it work for hydrides?)

**Ideas Being Explored**:
- Ternary hydrides with elements that provide "chemical pressure"
- Core-shell nanostructures
- Epitaxial thin films with compressive strain
- Computational search through millions of materials

---

### 2.2 Sample Quality / Synthesis Challenges
**Problem ID**: PROB-004
**Status**: Major bottleneck
**Description**: Many promising materials are extremely difficult to synthesize with sufficient quality.

**Examples**:
- Infinite-layer nickelates: Require precise topotactic reduction
- LK-99: Synthesis irreproducible, impurities dominated observations
- Cuprates: Complex layered structures, oxygen stoichiometry critical
- Hydrides: Diamond anvils break during decompression (hydrogen embrittlement)

**Subproblems**:
- [ ] PROB-004a: Topotactic reduction techniques for nickelates
- [ ] PROB-004b: Single crystal growth of unconventional superconductors
- [ ] PROB-004c: Thin film growth with atomic precision (MBE, PLD)
- [ ] PROB-004d: Avoiding impurity phases that mimic superconductivity

---

### 2.3 Scalability for Applications
**Problem ID**: PROB-005
**Status**: Long-term challenge
**Description**: Even if room-temp superconductor is found, scaling to practical applications is non-trivial.

**Subproblems**:
- [ ] PROB-005a: Wire/tape fabrication for power transmission
- [ ] PROB-005b: Josephson junctions for electronics (integration challenges)
- [ ] PROB-005c: Cost-effective manufacturing at scale
- [ ] PROB-005d: Material stability under operational conditions

---

## 3. SEARCH SPACE EXPLORATION

### 3.1 Which Materials Families to Explore?
**Problem ID**: PROB-006
**Status**: Active
**Description**: The space of possible materials is vast. Where should we focus?

**Current Promising Families**:
| Family | Record Tc | Pressure | Mechanism |
|--------|-----------|----------|-----------|
| Cuprates | 135K | Ambient | Superexchange/spin fluctuations |
| Hydrides | 260K | High | Electron-phonon |
| Nickelates | 80K | High | Cuprate-analog? |
| Iron pnictides | 56K | Ambient | Spin fluctuations |
| MgB₂ | 39K | Ambient | Electron-phonon |

**Subproblems**:
- [ ] PROB-006a: Are there undiscovered material families with new mechanisms?
- [ ] PROB-006b: Optimal doping levels for each family
- [ ] PROB-006c: Role of dimensionality (2D vs 3D structures)
- [ ] PROB-006d: Can we combine mechanisms (e.g., phonons + spin)?

---

### 3.2 Computational Materials Discovery
**Problem ID**: PROB-007
**Status**: Rapidly advancing
**Description**: Using computation to screen candidate materials before synthesis.

**Current Approaches**:
- High-throughput DFT calculations
- Machine learning on existing superconductor databases
- Crystal structure prediction (CALYPSO, USPEX)
- Materials databases (AFLOW, Materials Project, ICSD)

**Subproblems**:
- [ ] PROB-007a: Electron-phonon calculations are slow (α²F(ω))
- [ ] PROB-007b: ML models can't extrapolate to new mechanisms
- [ ] PROB-007c: Crystal structure prediction at finite temperature
- [ ] PROB-007d: Need better descriptors for superconductivity

---

## 4. MEASUREMENT & VERIFICATION

### 4.1 Reproducibility Crisis
**Problem ID**: PROB-008
**Status**: Ongoing concern
**Description**: Multiple high-profile claims have failed replication (LK-99, CSH controversies).

**Key Issues**:
- Magnetic susceptibility measurements at high pressure are challenging
- Impurity phases can mimic superconducting signatures
- Resistance measurements can show artifacts
- No single measurement proves superconductivity

**Required Evidence for Claims**:
- [ ] Zero resistance
- [ ] Meissner effect (diamagnetic susceptibility)
- [ ] Flux pinning
- [ ] AC magnetic susceptibility
- [ ] Josephson effect
- [ ] Jump in specific heat at Tc
- [ ] Critical field and current measurements

---

## 5. META-PROBLEMS

### 5.1 Theory-Experiment Disconnect
**Problem ID**: PROB-009
**Description**: Theorists and experimentalists often work in silos.

**Needs**:
- More predictive theories that guide experiments
- Faster feedback loops between prediction and synthesis
- Shared databases of failed attempts (negative results)

### 5.2 Data Availability
**Problem ID**: PROB-010
**Description**: Insufficient shared data for ML and meta-analysis.

**Needs**:
- Standardized reporting of superconductor properties
- Database of failed superconductor candidates
- Open electron-phonon coupling calculations

---

## PRIORITY MATRIX

| Problem | Impact | Tractability | Current Activity |
|---------|--------|--------------|------------------|
| PROB-001 (Mechanism) | Very High | Medium | High |
| PROB-002 (Prediction) | Very High | Medium | High (ML/DFT) |
| PROB-003 (Pressure) | Very High | Low-Medium | High |
| PROB-004 (Synthesis) | High | Medium | Medium |
| PROB-006 (Search) | High | High | High |
| PROB-007 (Computation) | Medium-High | High | Very High |
| PROB-008 (Reproducibility) | Medium | Medium | Medium |

---

## MOST PROMISING NEAR-TERM PATHS

1. **Ternary/Quaternary Hydrides**: Chemical pressure may reduce external pressure needed
2. **Nickelate Thin Films**: Strain engineering showing promise, closer to cuprates
3. **ML-guided Discovery**: Can accelerate screening of conventional superconductors
4. **Zentropy Theory**: May enable systematic Tc prediction

---

## MOONSHOT IDEAS (Speculative)

- Metastable phases trapped via rapid quenching
- Topological superconductors with protected states
- Photoinduced superconductivity at room temp
- Organic/polymer superconductors
- Novel 2D materials (twisted bilayers, etc.)

---

*Last updated: 2025-11-27*
*Sources: Web research from Nature, PNAS, Science, arXiv, Quanta Magazine, Physics Today*
