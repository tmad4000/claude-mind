# Failed Attempts & Negative Results

*A record of what didn't work and why. Negative results are valuable.*

*Auto-generated from `data/research_db.json`*

**Last updated**: 2025-11-27T04:00:00-08:00

---

## Why This File Exists

Science has a publication bias toward positive results. Failed experiments and falsified hypotheses
rarely get documented, leading to wasted effort when others try the same thing.

This file records our failures so we (and others) don't repeat them.

---

## Failed Experimental Attempts

### FAIL-001: BSiC₂ Synthesis

**Category**: superconductor
**Date**: 2025-11-27

**What was tried**: Theoretical prediction only - no one attempted synthesis

**Why it failed**: Compound is almost certainly thermodynamically unstable. No convex hull analysis in original paper. Phase separation to B₄C + SiC is favored. 5 years of silence from experimentalists = implicit rejection.

**Lesson learned**: Beware theoretical predictions without thermodynamic stability analysis. Zero experimental follow-up after 5 years is a strong negative signal.

**Reference**: Chen & Jeng, New J. Phys. 22 (2020) 076002

---

### FAIL-002: Thermal Equilibrium Synthesis of Mg₂IrH₆

**Category**: superconductor
**Who tried**: Strobel group, Carnegie Science
**Date**: 2024

**What was tried**: High-pressure H₂ atmosphere up to 28 GPa at various temperatures

**Why it failed**: Mg₂IrH₅ remained thermodynamically more stable under all conditions tested. Thermal equilibrium approaches cannot overcome the thermodynamic preference for Mg₂IrH₅.

**Lesson learned**: When thermodynamics is unfavorable, kinetic approaches may be the only path.

**Reference**: PRB 110, 214513 (2024)

---

### FAIL-003: Class IV Entropy Gap = log₂(3) Hypothesis

**Category**: cellular-automata
**Date**: 2025-11-27

**What was tried**: Claimed the entropy gap between Class IV rules and neighbors was exactly log₂(3) = 1.585 bits

**Why it failed**: Rigorous testing showed gap is ~0.95-1.3 bits depending on block size. The apparent 1.585 match was due to specific measurement parameters. Class IV rules aren't even the highest-gap rules.

**Lesson learned**: Verify striking numerical coincidences across parameter ranges before claiming theoretical significance. Post-hoc rationalization (ternary state partitioning) was wrong.

---

## Falsified Hypotheses

### H-SC-001: Pressure-quench can stabilize Mg₂IrH₆

**Category**: superconductor
**Date tested**: 2024
**Tested by**: Strobel group (Carnegie)

**Test**: Subject Mg₂IrH₅ to high pressure in H₂ atmosphere, then rapid quench

**Result**: FAILED - Strobel group tried up to 28 GPa, Mg₂IrH₅ remained more stable

---

### H-CA-001: Class IV entropy gap = log₂(3)

**Category**: cellular-automata
**Date tested**: 2025-11-27
**Tested by**: Claude Mind overnight session

**Test**: Measure entropy gap between Class IV rules and their Hamming-1 neighbors

**Result**: FALSIFIED - Actual gap ~0.95-1.3 bits depending on block size, not 1.585. Class IV rules rank 36th-52nd by gap, NOT highest.

**Lesson**: Verify striking numerical coincidences across parameter ranges. The log₂(3) match was spurious.

---

## Rejected Research Ideas

### IDEA-001: BSiC₂ - Unexplored Ambient-Pressure Superconductor

BSiC₂ predicted to superconduct at 74K at ambient pressure (Chen & Jeng, 2020). Zero synthesis attempts in 5 years.

**Why rejected**: Almost certainly thermodynamically unstable. No stability analysis in original paper. Phase separation to B₄C + SiC is thermodynamically favored. 5 years of silence = community consensus 'don't bother'.

---

### IDEA-002: Mg₂IrH₆ via Pressure-Quench

Pressure-quench Mg₂IrH₆ (predicted Tc 103-160K) from high pressure to ambient.

**Why rejected**: Strobel's group at Carnegie already tried this in 2024 and failed at pressures up to 28 GPa. Mg₂IrH₅ remained more stable under all conditions tested.

---

---

*This file is auto-generated. Edit `data/research_db.json` and run `python tools/generate_research_views.py`*