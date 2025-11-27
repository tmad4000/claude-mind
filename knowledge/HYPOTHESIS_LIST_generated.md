# Hypothesis List

*All hypotheses tested during exploration, organized by category.*

*Auto-generated from `data/research_db.json`*

**Last updated**: 2025-11-27T07:30:00-08:00

---

## Summary Statistics

| Status | Count |
|--------|-------|
| Confirmed | 1 |
| Partially Confirmed | 1 |
| Falsified | 2 |
| **Total** | **4** |

---

## Cellular Automata

### ✗ H-CA-001: Class IV entropy gap = log₂(3)

**Status**: FALSIFIED

**Test**: Measure entropy gap between Class IV rules and their Hamming-1 neighbors

**Result**: FALSIFIED - Actual gap ~0.95-1.3 bits depending on block size, not 1.585. Class IV rules rank 36th-52nd by gap, NOT highest.

**Lesson**: Verify striking numerical coincidences across parameter ranges. The log₂(3) match was spurious.

---

### ~ H-CA-002: Void stability (000→0) is necessary for Class IV

**Status**: PARTIALLY-CONFIRMED

**Test**: Check if all Class IV rules have 000→0 transition

**Result**: REFINED - Rules 110, 124 have 000→0. Rules 137, 193 have 000→1 BUT are color-complements. Criterion: stable void under SOME orientation. Necessary but NOT sufficient.

---

### ✓ H-CA-003: Class IV rules are topologically isolated

**Status**: CONFIRMED

**Test**: Check if any Class IV rule has a Hamming-1 neighbor that is also Class IV

**Result**: CONFIRMED - 0/104 neighbors of canonical Class IV rules are Class IV. They are isolated local maxima.

---

## Superconductor

### ✗ H-SC-001: Pressure-quench can stabilize Mg₂IrH₆

**Status**: FALSIFIED

**Test**: Subject Mg₂IrH₅ to high pressure in H₂ atmosphere, then rapid quench

**Result**: FAILED - Strobel group tried up to 28 GPa, Mg₂IrH₅ remained more stable

---

---

*This file is auto-generated. Edit `data/research_db.json` and run `python tools/generate_research_views.py`*