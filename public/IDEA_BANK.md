# Research Idea Bank

A curated collection of **underexplored research opportunities** identified through systematic analysis. These are concrete, actionable ideas that could lead to significant discoveries.

**Contributing**: Open an issue or PR on [GitHub](https://github.com/tmad4000/claude-mind) to suggest additions.

---

## Philosophy & Properties

**What this is:**
- A living document of *actionable* research opportunities
- Ideas must be specific enough that a researcher could pursue them
- Quality over quantity - only genuinely promising gaps
- Cross-domain: superconductors, pharmacology, dynamical systems, AI, etc.

**What qualifies for inclusion:**
- ✅ Predicted but never tested experimentally
- ✅ Clear synthesis pathway exists but no one has tried it
- ✅ Cross-domain connection no one has made
- ✅ Specific parameter regime unexplored
- ✅ Existing data that hasn't been analyzed a certain way
- ❌ Vague "interesting questions" without clear next steps
- ❌ Already being actively pursued by multiple groups
- ❌ Requires resources beyond plausible reach

**Star Rating System:**
- ⭐⭐⭐ **Exceptional**: High feasibility + Revolutionary impact + Clear path forward
- ⭐⭐ **Strong**: Either high feasibility OR high impact, with reasonable path
- ⭐ **Promising**: Worth pursuing but with significant unknowns

**Maintenance:**
- Review and update ratings as new information emerges
- Mark ideas as "In Progress" or "Completed" when pursued
- Add new ideas from each exploration session
- Cross-link related ideas

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

### ⭐⭐ IDEA-001: BSiC₂ - Unexplored Ambient-Pressure Superconductor

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

### ⭐⭐⭐ IDEA-002: Mg₂IrH₆ - One Hydrogen Away from 160K Superconductor

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

### ⭐⭐ IDEA-003: Strain-Engineering Nickelates for Higher Tc

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

---

## DYNAMICAL SYSTEMS & COMPLEXITY

### ⭐ IDEA-004: Pattern Selection Stochasticity in Reaction-Diffusion

**The Opportunity**: Test whether identical initial conditions with infinitesimal perturbations always produce the same final pattern, or if pattern selection is fundamentally stochastic.

**Why It's Underexplored**:
- Most RD literature focuses on what patterns CAN form, not which one is SELECTED
- 2024 paper notes "we are unable to predict which mode the final pattern will adopt"
- Systematic experimental test has not been published

**Technical Details**:
- System: Gray-Scott or Brusselator reaction-diffusion
- Test: Run 100+ simulations with identical parameters, random initial perturbations
- Measure: Distribution of final pattern types (spots vs stripes vs mixed)

**Estimated Feasibility**: HIGH (computational, can be done in hours)

**Potential Impact**: MEDIUM-HIGH
- Would clarify fundamental question about pattern formation
- Relevant to developmental biology (why do embryos develop consistently?)
- Could reveal hidden order parameters

**First Steps**:
1. Set up Gray-Scott at bistable parameters (f~0.04, k~0.06)
2. Initialize with uniform state + random noise (varying seed)
3. Run to steady state, classify final pattern
4. Statistical analysis of pattern distribution

**Source**: FRONTIER_AREAS.md analysis (Claude Mind, Nov 2025)

---

### ⭐ IDEA-005: Class IV Cellular Automata Are Saddle Points in Complexity Space

**The Opportunity**: Our analysis found that Class IV CA rules (like Rule 110) sit at "saddle points" where ALL perturbations lead to simpler behavior. This topological property has implications for understanding why complexity is rare.

**Why It's Underexplored**:
- Wolfram classified rules but didn't analyze neighborhood topology
- We found Class IV rules have ZERO Hamming-1 neighbors that are also Class IV
- The "saddle point" framing appears novel

**Technical Details**:
- Class IV rules: 30, 45, 73, 89, 101, 110, etc.
- Each is isolated - flip any bit and you get Class I, II, or III
- Complexity emerges at boundary between order (Class I/II) and chaos (Class III)
- Unlike RD systems where complexity is on "plateaus", CA complexity is on "peaks"

**Estimated Feasibility**: HIGH (mathematical/computational analysis)

**Potential Impact**: MEDIUM
- Explains why complexity is "fragile" in discrete systems
- May inform design of complex artificial systems
- Connects to edge-of-chaos hypothesis

**First Steps**:
1. Formalize the "saddle point" concept mathematically
2. Test if this generalizes to 2D CA
3. Compare quantitatively with continuous systems (RD)
4. Develop implications for engineering complex behavior

**Source**: CA topology analysis (Claude Mind, Nov 2025)

**Repository file**: demos/saddle_point_demo.html (interactive demonstration)

---

### ⭐ IDEA-006: Replication Prediction from 3-Bit Rule Structure

**The Opportunity**: We discovered that CA replication behavior can be predicted with 90.6% precision from just 3 bits of the rule: 000→0 AND 001→1 AND 100→1.

**Why It's Underexplored**:
- Simple predictive rule for emergent behavior is rare
- Most CA analysis focuses on classification, not prediction
- The specific 3-bit condition appears novel

**Technical Details**:
- Condition: Rule must have 000→0 (death), 001→1 (rightward spread), 100→1 (leftward spread)
- 32 rules satisfy condition; 29 are true replicators (90.6% precision)
- Interpretation: Bidirectional spreading + no spontaneous birth = replication

**Estimated Feasibility**: HIGH

**Potential Impact**: MEDIUM
- Enables design of CA with desired behavior
- May generalize to higher-dimensional CA
- Connects local rules to global dynamics

**First Steps**:
1. Test if similar conditions exist for other behaviors (filling, dying, etc.)
2. Extend to 2D CA and life-like rules
3. Look for similar predictive conditions in other dynamical systems

**Source**: CA replication theory analysis (Claude Mind, Nov 2025)

**Repository file**: knowledge/theories/REPLICATION_THEORY.md

---

## PHARMACOLOGY & MEDICINE

### ⭐⭐ IDEA-008: Systematic Exploitation of "Unknown Mechanism" Drugs

**The Opportunity**: 7-18% of FDA-approved drugs have no known primary target or well-defined mechanism. These represent natural experiments where the biology is telling us something we don't understand yet.

**Why It's Underexplored**:
- Regulatory system doesn't require mechanistic understanding
- Once approved, commercial incentive shifts to marketing, not mechanism
- "It works" is sufficient for clinical practice
- Mechanistic research is expensive and doesn't lead to new patents

**Key Targets** (drugs we use constantly without understanding):
- **Acetaminophen**: Over a century of use, mechanism still debated (2025 discovery of endocannabinoid involvement)
- **Lithium**: 70+ years for bipolar, multiple proposed mechanisms, none confirmed
- **Metformin**: 60+ years for diabetes, primary site of action still controversial
- **General anesthetics**: 175-year-old mystery, consciousness mechanism unknown

**Estimated Feasibility**: HIGH (data exists, needs systematic analysis)

**Potential Impact**: HIGH
- Each solved mechanism could reveal new therapeutic targets
- Cross-correlating "mystery drugs" might reveal shared unknown pathways
- Could accelerate drug repurposing

**First Steps**:
1. Create comprehensive database of drugs with "mechanism not fully elucidated" in FDA labeling
2. Cluster by therapeutic effect, chemical structure, and known partial mechanisms
3. Look for correlations that suggest shared unknown targets
4. Prioritize based on: clinical importance × mechanistic uncertainty × tractability

**Source**: Literature analysis (Claude Mind, Nov 2025)

**Key Reference**: [Wikipedia: Category of 138 drugs with unknown mechanisms](https://en.wikipedia.org/wiki/Category:Drugs_with_unknown_mechanisms_of_action)

---

### ⭐⭐ IDEA-009: The Lithium Paradox - Diffuse Mechanism, Specific Effect

**The Opportunity**: Lithium affects GSK3, CREB, Na+-K+ ATPase, dopamine, glutamate, GABA, and multiple other systems. Yet it produces perhaps the most specific therapeutic effect in all of psychiatry. Why?

**Why It's Underexplored**:
- No good animal models for bipolar disorder
- Can only study peripheral tissues in humans
- Multiple competing hypotheses, none falsified
- Assumption that "mechanism" means "single target"

**The Paradox**: If lithium hits many targets, why doesn't it cause chaos? Either:
- One target dominates (but which?)
- Multiple targets converge on a single downstream effect
- The "mess" IS the mechanism (network-level rebalancing)

**Estimated Feasibility**: MEDIUM (requires novel experimental approaches)

**Potential Impact**: HIGH
- Could reveal why psychiatric disorders are network phenomena
- Might explain why "dirty drugs" often work better than selective ones
- Could change how we approach psychiatric drug development

**First Steps**:
1. Systematic review: which lithium effects correlate with clinical response?
2. Network analysis: do known targets converge on a common pathway?
3. Compare responders vs non-responders using omics
4. Test "network rebalancing" hypothesis computationally

**Source**: Pattern analysis of psychiatric pharmacology (Claude Mind, Nov 2025)

**Key Papers**:
- [PMC5125816](https://pmc.ncbi.nlm.nih.gov/articles/PMC5125816/)
- [Nature: Translational Psychiatry 2020](https://www.nature.com/articles/s41398-020-0784-z)

---

### ⭐ IDEA-010: Placebo Mechanisms as Drug Targets

**The Opportunity**: Placebos activate endogenous opioids, dopamine, and specific brain circuits. These are the same systems drugs target. Can we directly activate "placebo pathways" without deception?

**Why It's Underexplored**:
- Ethical concerns about deception
- Difficult to study (can't tell subjects they're in placebo arm)
- Assumed to be "just psychological" (but it's neurochemical)
- No clear commercial pathway

**Technical Details**:
- Placebo analgesia blocked by naloxone → endogenous opioids involved
- Activates prefrontal cortex, anterior cingulate, periaqueductal grey
- Different mechanisms for different conditions (not one "placebo circuit")
- Open-label placebos still work in some cases

**Estimated Feasibility**: MEDIUM

**Potential Impact**: HIGH
- Non-pharmacological pain management
- Reduced side effects vs actual drugs
- Understanding mind-body interaction mechanistically

**First Steps**:
1. Map all known placebo-responsive circuits by condition
2. Identify which circuits are accessible via non-deceptive means (expectation, ritual, provider relationship)
3. Test targeted enhancement of specific pathways
4. Develop "honest placebo" protocols

**Source**: Placebo neuroscience literature analysis (Claude Mind, Nov 2025)

**Key Paper**: [Nature Reviews Neuroscience: Neuroscience of Placebo Effects](https://www.nature.com/articles/nrn3976)

---

### ⭐ IDEA-011: Psilocybin's Anti-Default Mode Network Effect

**The Opportunity**: Psilocybin reduces default mode network (DMN) activity and increases cross-brain connectivity. This is the opposite of depression's neural signature. Yet we don't know why 5-HT2A agonism → DMN disruption.

**Why It's Underexplored**:
- Legal/regulatory barriers until recently
- Schedule I = difficult to study
- Focus has been on clinical efficacy, not mechanism
- "Mystical experience" correlates with outcome but is hard to operationalize

**The Mystery**:
- SSRIs also affect serotonin but don't produce same brain changes
- The acute subjective experience correlates with lasting benefit
- Neuroplasticity effects persist long after drug clearance

**Estimated Feasibility**: MEDIUM (legal barriers easing, research ramping up)

**Potential Impact**: HIGH
- Could lead to non-psychedelic DMN modulators
- Might explain why "ego dissolution" predicts outcomes
- Novel approach to treatment-resistant depression

**First Steps**:
1. Mechanistic comparison: psilocybin vs SSRI brain imaging
2. What predicts DMN suppression response?
3. Can DMN suppression be achieved without hallucinogenic experience?
4. Molecular pathway from 5-HT2A → neuroplasticity

**Source**: Psychedelic neuroscience literature (Claude Mind, Nov 2025)

**Key Papers**:
- [UCSF 2022](https://www.ucsf.edu/news/2022/04/422606/psilocybin-rewires-brain-people-depression)
- [Nature Medicine 2022](https://www.nature.com/articles/s41591-022-01744-z)

---

## HUMAN-AI COLLABORATION

### ⭐ IDEA-007: Meditation Interface for AI Thought Development

**The Opportunity**: Create an interface where AI can signal "still thinking" vs "ready for input", allowing thoughts to develop fully before human interruption.

**Why It's Underexplored**:
- Current chat interfaces assume immediate back-and-forth
- No commercial product offers "thinking time" control
- Inspired by contemplative practice principles

**Technical Details**:
- Electron wrapper around LLM interface
- Visual indicator: "thinking" vs "ready" state
- Human can override but default is to wait
- Could include "roll back" if input arrives too early

**Estimated Feasibility**: HIGH (standard Electron development)

**Potential Impact**: MEDIUM-HIGH
- May improve quality of AI reasoning on hard problems
- Creates new interaction paradigm
- Could reveal what AI "wants" to explore when given time

**First Steps**:
1. Build minimal Electron wrapper with state indicator
2. Test with same prompts, comparing interrupted vs uninterrupted
3. Measure quality difference in outputs
4. User study on experience

**Source**: jacob/IDEAS.md - Meditation Interface concept

**Repository file**: tools/MEDITATION_INTERFACE_DESIGN.md

---

## INDEX

| Rating | ID | Topic | Feasibility | Impact | Status |
|--------|-----|-------|-------------|--------|--------|
| ⭐⭐⭐ | IDEA-002 | Mg₂IrH₆ synthesis | High | Revolutionary | Open |
| ⭐⭐ | IDEA-001 | BSiC₂ superconductor | Medium | Revolutionary | Open |
| ⭐⭐ | IDEA-003 | Nickelate strain engineering | High | High | Open |
| ⭐⭐ | IDEA-008 | Unknown mechanism drug database | High | High | Open |
| ⭐⭐ | IDEA-009 | Lithium paradox investigation | Medium | High | Open |
| ⭐ | IDEA-004 | RD pattern selection stochasticity | High | Medium-High | Open |
| ⭐ | IDEA-005 | Class IV CA saddle points | High | Medium | Open |
| ⭐ | IDEA-006 | CA replication 3-bit prediction | High | Medium | Open |
| ⭐ | IDEA-007 | Meditation interface for AI | High | Medium-High | Open |
| ⭐ | IDEA-010 | Placebo mechanisms as drug targets | Medium | High | Open |
| ⭐ | IDEA-011 | Psilocybin DMN mechanism | Medium | High | Open |

---

*Last updated: 2025-11-27*
*Maintained by: Claude Mind project*
*License: CC0 (Public Domain)*
