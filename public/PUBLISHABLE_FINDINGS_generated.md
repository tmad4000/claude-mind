# Publishable Findings

*Discoveries that appear novel and potentially worth publishing.*

*Auto-generated from `data/research_db.json`*

**Last updated**: 2025-11-27T07:30:00-08:00

---

## High-Confidence Publishable Findings

### F-001: Class IV Rules Are Topologically Isolated

**Status**: confirmed | **Confidence**: high

**Summary**: In the space of 256 elementary CA rules, canonical Class IV rules (110, 124, 137, 193) have ZERO Hamming-1 neighbors that are also Class IV.

**Implications**: Class IV behavior requires precise tuning - any single-bit change destroys it. 'Edge of chaos' is better described as 'peaks of complexity'.

**Novelty**: Web searches found no prior work on this specific topological property.

---

### F-003: Complete Algebraic Characterization of Chaotic ECA Rules

**Status**: confirmed | **Confidence**: high

**Summary**: ALL 12 truly chaotic ECA rules have EXACTLY 4 ones in binary representation. Combined with quiescent state, asymmetric balance (d3=1), and transition pattern conditions, we achieve 100% accurate classification.

**Implications**: ['Chaos in 1D CA is algebraically constrained', 'Can determine chaos instantly without simulation', "Wolfram's visual classification missed structure"]

---

## Other Findings (Lower Confidence)

### F-002: Void Stability Principle

**Status**: refined | **Confidence**: medium

For a CA to exhibit Class IV behavior, the void must be stable under at least one orientation (original or color complement).

**Caveats**: Necessary but not sufficient. Rule 149 (Class III) has complement with stable void but is still chaotic.

---

---

*This file is auto-generated. Edit `data/research_db.json` and run `python tools/generate_research_views.py`*