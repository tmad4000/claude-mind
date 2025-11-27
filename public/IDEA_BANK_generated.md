# Research Idea Bank

*Auto-generated from `data/research_db.json`*

**Last updated**: 2025-11-27T04:30:00-08:00

---

## Promising Ideas (Ready for Action)

### ⭐⭐ IDEA-003: Mg₂IrH₆ via Non-Equilibrium Kinetic Insertion

**Status**: PROMISING | **Feasibility**: medium | **Impact**: revolutionary

Insert final hydrogen into Mg₂IrH₅ via kinetic (non-equilibrium) methods: cryogenic ion implantation, electrochemical gating, plasma-assisted insertion.

**Key Insight**: Strobel's thermal equilibrium approach failed. Kinetic approaches haven't been tried. DFT shows no barrier for insertion - just need to get H atoms there faster than they recombine.

**Next Steps**:
- Grow Mg₂IrH₅ thin films via PLD/sputtering
- Cryogenic H⁺ implantation (<77K) to suppress diffusion
- In-situ synchrotron XRD during implantation
- Transport measurements to detect superconductivity

**Recommended Contacts**:
- Russell Hemley (UIC) - high-pressure physics
- Kyle Shen (Cornell) - laser-MBE + transport
- James Analytis (UC Berkeley) - quantum materials

**References**:
- https://journals.aps.org/prb/abstract/10.1103/PhysRevB.110.214513
- https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.132.166001

---

### ⭐⭐⭐ IDEA-005: Public Repository of Failed Scientific Attempts

**Status**: PROMISING | **Feasibility**: high | **Impact**: high

Create a public, searchable database of failed synthesis attempts, negative experimental results, and falsified hypotheses. Science has massive publication bias toward positive results - negative results rarely get published, leading to wasted effort when others unknowingly repeat failed experiments.

**Key Insight**: The absence of BSiC₂ synthesis attempts after 5 years reveals implicit knowledge that the compound is unstable - but this knowledge isn't documented anywhere. Strobel's failed Mg₂IrH₆ synthesis is buried in a paper about Mg₂IrH₅. There's no central 'we tried this and it didn't work' database.

**Next Steps**:
- Survey existing negative results repositories
- Interview researchers about barriers to reporting failures
- Design minimal viable schema for failure reports
- Identify pilot lab partner
- Build simple web interface

**References**:
- https://en.wikipedia.org/wiki/Publication_bias
- https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0020124

---

### ⭐⭐⭐ IDEA-006: Minimal Complexity Threshold - Simplest Turing-Complete System

**Status**: PROMISING | **Feasibility**: high | **Impact**: high

What is the simplest system capable of universal computation? Rule 110 is Turing-complete, but is there something simpler? Finding the exact boundary between computational universality and non-universality would illuminate fundamental limits.

**Key Insight**: We know Rule 110 works. We know simpler rules don't. The boundary must be somewhere specific. Finding it would tell us the 'minimum complexity cost' of computation.

---

### ⭐⭐⭐ IDEA-008: Collective Intelligence Scaling Laws

**Status**: PROMISING | **Feasibility**: high | **Impact**: high

How does group intelligence scale with group size, communication structure, and diversity? Are there universal scaling laws? This has direct implications for organizations, democracy, and AI collectives.

**Key Insight**: Sandy Pentland's work shows network structure matters more than individual ability for group performance. But we don't have systematic scaling laws like we do for metabolic rate vs body size in biology.

**Recommended Contacts**:
- Sandy Pentland (MIT) - social physics pioneer
- Anita Woolley (Carnegie Mellon) - collective intelligence factor
- Scott Page (Michigan) - diversity and complexity

---

### ⭐⭐⭐ IDEA-009: Precursor Availability Filter for Material Predictions

**Status**: PROMISING | **Feasibility**: high | **Impact**: high

AI systems predict thousands of new materials, but many are impossible to synthesize because precursors don't exist or synthesis pathways are unknown. Create a filter that rates predictions by 'can we actually make this?'

**Key Insight**: BSiC₂ was predicted in 2020 with Tc=74K but has zero synthesis attempts. Why? Probably because there's no obvious precursor pathway. If we had rated this upfront, we'd have saved 5 years of implicit 'this is impossible' knowledge.

---

### ⭐⭐⭐ IDEA-010: Null Result Futures Market

**Status**: PROMISING | **Feasibility**: medium | **Impact**: high

Create a prediction market where people bet on whether hyped scientific findings will replicate. Financial incentives would accelerate detection of failures (like LK-99) and reward skepticism.

**Key Insight**: Currently there's no financial incentive to investigate suspected frauds or failures. Prediction markets create one. The LK-99 room-temperature superconductor fiasco would have been called out faster if money was on the line.

---

### ⭐⭐ IDEA-011: Human-AI Calibration Training

**Status**: PROMISING | **Feasibility**: high | **Impact**: high

Humans are systematically miscalibrated about when to trust AI - sometimes over-relying, sometimes under-relying. Create interactive training (like forecaster calibration training) to improve human-AI collaboration.

**Key Insight**: Good forecasters learn calibration through feedback. AI users rarely get this feedback. A training system would show: 'You trusted AI here and it was wrong' / 'You overrode AI here and you were wrong' - building intuition for AI capabilities.

---

## Open Ideas (Need More Work)

### ⭐⭐ IDEA-004: Nickelate Strain Engineering for Higher Tc

**Status**: open | **Feasibility**: high | **Impact**: high

La₃Ni₂O₇ superconducts at ambient pressure via substrate strain (SLAC, Feb 2025). Current Tc ~26K. Can systematic substrate/strain optimization push higher?

---

### ⭐⭐⭐ IDEA-007: Universal 'Interestingness' Metric for Complex Systems

**Status**: open | **Feasibility**: low | **Impact**: revolutionary

Find a metric that reliably distinguishes 'interesting' complex behavior (Class IV, edge of chaos) from mere randomness (Class III) and simple order (Class I/II). Entropy doesn't work. What does?

---

## Failed/Rejected Ideas

*See `public/FAILED_ATTEMPTS.md` for details.*

- **IDEA-001**: BSiC₂ - Unexplored Ambient-Pressure Superconductor - Almost certainly thermodynamically unstable. No stability analysis in original paper. Phase separati...
- **IDEA-002**: Mg₂IrH₆ via Pressure-Quench - Strobel's group at Carnegie already tried this in 2024 and failed at pressures up to 28 GPa. Mg₂IrH₅...

---

*This file is auto-generated. Edit `data/research_db.json` and run `python tools/generate_research_views.py`*