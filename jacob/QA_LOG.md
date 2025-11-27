# Q&A Log

A running log of questions Jacob asks and the key insights from answers, across all topics. This captures the "conversational knowledge" that emerges from dialogue.

---

## Format

```markdown
### [DATE] Q: [Question summary]
**Context**: [What we were working on]
**Answer Summary**: [Key points]
**Key Insight**: [The most important takeaway]
```

---

## 2025-11-27

### Q: How do phonons relate to superconductivity?

**Context**: Building superconductor research infrastructure, Jacob wanted to understand the physics

**Answer Summary**:
1. **Phonons = quantized lattice vibrations** - collective atomic vibrations in crystals, quantized into discrete packets
2. **They enable electron attraction** - normally electrons repel, but:
   - Electron 1 moves through lattice, attracts positive ions
   - Creates temporary positive region
   - Electron 2 attracted to that region
   - Net effect: electrons attract through lattice distortion
3. **Key parameters**:
   - ω (phonon frequency): light atoms → fast vibrations → higher Tc potential
   - λ (coupling strength): stronger coupling → higher Tc, but too strong destabilizes lattice
4. **Why hydrogen matters**: Lightest element → highest phonon frequencies → why hydrides can reach 260K
5. **BCS ceiling**: ~30-40K for normal metals due to atom mass limits
6. **Cuprates are different**: Use superexchange (magnetic coupling through oxygen), not phonons - bypasses BCS ceiling but mechanism not fully understood

**Key Insight**: There are two fundamentally different paths to high-Tc: (1) maximize phonon frequency with light atoms (requires pressure), or (2) use a different mechanism like superexchange (works at ambient pressure but we don't understand it well enough to optimize)

---

### Q: Are you logging terminal output / key insights somewhere?

**Context**: During superconductor discussion

**Answer Summary**: Was not logging conversational insights. Created:
- `superconductor/INSIGHTS_LOG.md` for superconductor-specific insights
- `jacob/QA_LOG.md` (this file) for general Q&A across all topics

**Key Insight**: Conversational knowledge is valuable and should be captured systematically. The structured databases (OBSERVATIONS_DB, PROBLEM_MAP) capture facts, but Q&A captures understanding and explanations.

---

### Q: What can Claude actually do for superconductor research vs what needs labs?

**Context**: Discussing research approach

**Answer Summary**:
- **Can do**: Knowledge synthesis, finding connections, pattern matching, hypothesis generation, toy simulations for intuition, paper scanning
- **Cannot do**: Material synthesis, Tc measurements, high-pressure experiments, verification
- **Missing from pure-AI approach**: Tacit experimental knowledge, closing the loop with real experiments, quality filtering, truly novel mechanisms

**Key Insight**: Claude's role is "computational science cartography" - mapping territory, finding gaps, generating hypotheses. But real science needs wet labs to close the loop.

---

*This file should be updated every session with significant Q&A exchanges.*
