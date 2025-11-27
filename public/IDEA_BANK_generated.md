# Research Idea Bank

*Auto-generated from `data/research_db.json`*

**Last updated**: 2025-11-27T04:00:00-08:00

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

## Open Ideas (Need More Work)

### ⭐⭐ IDEA-004: Nickelate Strain Engineering for Higher Tc

**Status**: open | **Feasibility**: high | **Impact**: high

La₃Ni₂O₇ superconducts at ambient pressure via substrate strain (SLAC, Feb 2025). Current Tc ~26K. Can systematic substrate/strain optimization push higher?

---

## Failed/Rejected Ideas

*See `public/FAILED_ATTEMPTS.md` for details.*

- **IDEA-001**: BSiC₂ - Unexplored Ambient-Pressure Superconductor - Almost certainly thermodynamically unstable. No stability analysis in original paper. Phase separati...
- **IDEA-002**: Mg₂IrH₆ via Pressure-Quench - Strobel's group at Carnegie already tried this in 2024 and failed at pressures up to 28 GPa. Mg₂IrH₅...

---

*This file is auto-generated. Edit `data/research_db.json` and run `python tools/generate_research_views.py`*