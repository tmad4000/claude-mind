# Research Idea Bank

A curated collection of **underexplored research opportunities** identified through systematic analysis. These are concrete, actionable ideas that could lead to significant discoveries.

**Contributing**: Open an issue or PR on [GitHub](https://github.com/tmad4000/claude-mind) to suggest additions.

---

## Format

Each idea includes:
- **The Opportunity**: What could be discovered
- **Why It's Underexplored**: Gap analysis
- **Estimated Feasibility**: How hard is this?
- **Potential Impact**: What's at stake
- **First Steps**: How to get started
- **Source**: Where this idea came from

---

## MATERIALS SCIENCE & SUPERCONDUCTIVITY

### IDEA-001: BSiC₂ - Unexplored Ambient-Pressure Superconductor

**The Opportunity**: BSiC₂ is predicted to superconduct at **74K at ambient pressure** with **no hydrogen**. This would be the highest-Tc hydrogen-free conventional superconductor at ambient pressure ever discovered.

**Why It's Underexplored**:
- Predicted in a 2020 paper (New J. Phys. 22 076002)
- As of November 2025, **ZERO experimental synthesis attempts have been published**
- 5-year gap between prediction and any experimental work
- Attention has focused on high-pressure hydrides instead

**Technical Details**:
- Structure: Hexagonal, derived from 2H-SiC with alternating B/Si layers
- Lattice: a = 2.89 Å, c/a = 1.66
- Mechanism: BCS (conventional phonon-mediated)
- Electron-phonon coupling: λ = 2.41 (exceptionally strong)
- Key feature: Dramatically softened E₂g phonon mode

**Estimated Feasibility**: MEDIUM
- May be metastable (challenging synthesis)
- No known precursor compounds
- B solubility in SiC is only ~0.2 wt% normally

**Potential Impact**: REVOLUTIONARY
- If real: Ambient pressure, no pressure apparatus needed
- Hydrogen-free: No stability/handling issues
- Stoichiometric: No doping optimization required
- Above liquid nitrogen (77K)

**First Steps**:
1. DFT: Calculate convex hull energy and kinetic barriers
2. Explore thin-film approaches (MBE/CVD layer-by-layer)
3. Try spark plasma sintering for metastable phase access
4. Consider B ion implantation into SiC substrates

**Related Ideas**: BC₃ also predicted at ~40K ambient pressure

**Source**: Pattern analysis of superconductor literature (Claude Mind, Nov 2025)

**Original Paper**: [Guo et al., New J. Phys. 22 (2020) 076002](https://iopscience.iop.org/article/10.1088/1367-2630/ab76ad)

---

### IDEA-002: Mg₂IrH₆ - One Hydrogen Away from 160K Superconductor

**The Opportunity**: Mg₂IrH₅ has been **experimentally synthesized**. Adding ONE more hydrogen could create Mg₂IrH₆, predicted to superconduct at **103-160K at ambient pressure**.

**Why It's Underexplored**:
- Precursor Mg₂IrH₅ was only synthesized recently (2024)
- The "last hydrogen" insertion requires non-equilibrium processing
- Most attention still on high-pressure hydrides

**Technical Details**:
- Mg₂IrH₅ synthesis: 450°C, 100-250 bar H₂, 2 weeks, 80-90% purity
- Mg₂IrH₆ is 60 meV/atom above convex hull (metastable but accessible)
- DFT predicts NO energy barrier for H insertion
- Mechanism: IrH₆⁴⁻ molecular vibrations provide electron-phonon coupling

**Estimated Feasibility**: HIGH
- Precursor exists and synthesis is reproducible
- Just need to find non-equilibrium H insertion method

**Potential Impact**: REVOLUTIONARY
- Would be highest-Tc ambient-pressure superconductor
- Above liquid nitrogen temperature
- Clear synthesis pathway exists

**First Steps**:
1. H⁺ ion implantation (1-10 keV) into Mg₂IrH₅
2. H₂ plasma exposure of thin films
3. High-pressure H₂ annealing (500-1000 bar) + rapid quench
4. Electrochemical hydrogenation

**Source**: Literature synthesis (Claude Mind, Nov 2025)

**Key Papers**:
- Mg₂IrH₅ synthesis: PRB 2024
- Mg₂IrH₆ prediction: npj Computational Materials 2024

---

### IDEA-003: Strain-Engineering Nickelates for Higher Tc

**The Opportunity**: La₃Ni₂O₇ has been shown to superconduct at ambient pressure via substrate strain (SLAC, Feb 2025). Current Tc is ~26K. Can this be pushed much higher?

**Why It's Underexplored**:
- Result is very recent (Feb 2025)
- Only one substrate/strain combination tested
- Nickelates are isoelectronic to cuprates (135K)

**Technical Details**:
- Substrate lateral compression mimics high-pressure effects
- Current: Onset at -247°C to -231°C, zero-resistance at 2K
- Cuprates (similar electronic structure) reach 135K

**Estimated Feasibility**: HIGH
- Thin-film growth is mature technology
- Building on proven result

**Potential Impact**: HIGH
- If nickelates can be optimized like cuprates were, 100K+ possible
- Compatible with device fabrication
- Enables advanced characterization (ARPES, STM)

**First Steps**:
1. Systematic substrate survey (different strain levels)
2. Try other Ruddlesden-Popper nickelates (La₄Ni₃O₁₀)
3. Combine strain with doping (Sr, Ca substitution)
4. Test tensile vs compressive strain regimes

**Source**: SLAC breakthrough + pattern analysis (Claude Mind, Nov 2025)

**Key Paper**: Ko et al., Nature Dec 2024

---

## HOW TO CONTRIBUTE

Have you identified an underexplored research opportunity? Submit it!

**Requirements**:
1. Clear description of the opportunity
2. Evidence that it's genuinely underexplored (literature search)
3. Feasibility assessment
4. First steps for someone to pursue it
5. Sources/references

**Submit via**:
- GitHub Issue: [tmad4000/claude-mind/issues](https://github.com/tmad4000/claude-mind/issues)
- Pull Request: Add to this file following the format above

---

## INDEX

| ID | Topic | Feasibility | Impact | Status |
|----|-------|-------------|--------|--------|
| IDEA-001 | BSiC₂ superconductor | Medium | Revolutionary | Open |
| IDEA-002 | Mg₂IrH₆ synthesis | High | Revolutionary | Open |
| IDEA-003 | Nickelate strain engineering | High | High | Open |

---

*Last updated: 2025-11-27*
*Maintained by: Claude Mind project*
*License: CC0 (Public Domain)*
