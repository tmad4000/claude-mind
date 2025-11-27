# Superconductor Research Protocol

Instructions for Claude (or humans) continuing this research.

---

## Session Workflow

### 1. Start of Session

```markdown
1. Read this file for context
2. Check PROBLEM_MAP.md for current problem state
3. Check OBSERVATIONS_DB.md for recent additions
4. Check PAPER_CATALOG.md for papers to analyze
5. Review any notes in superconductor/data/
```

### 2. Ongoing Research Tasks

#### A. Paper Scanning (Weekly)
1. Run `python3 superconductor/tools/arxiv_scanner.py --days 7`
2. Review high-relevance papers (score >= 5)
3. For each interesting paper:
   - Add entry to PAPER_CATALOG.md
   - Note connections to PROB-XXX problems
   - Note connections to OBS-SC-XXX observations
   - Identify what NEW connections the paper establishes

#### B. Observation Updating
When you find a new empirical result:
1. Add to OBSERVATIONS_DB.md with unique ID (OBS-SC-XXX)
2. Classify type: Experimental | Theoretical | Computational | Pattern
3. Link to related problems
4. Note potential applications

#### C. Problem Map Refinement
Periodically review:
- Are subproblems well-defined?
- Any new subproblems emerged?
- Any problems resolved or abandoned?
- Priority changes based on new findings?

#### D. Connection Finding
The most valuable activity:
1. Look for A→B→C chains (paper establishes A→B, observation shows B→C)
2. Identify gaps: problems with no recent progress
3. Generate hypotheses from patterns
4. Flag potential breakthroughs

### 3. End of Session

Update these files:
- [ ] PROBLEM_MAP.md (if problems changed)
- [ ] OBSERVATIONS_DB.md (if new observations)
- [ ] PAPER_CATALOG.md (if new papers analyzed)
- [ ] jacob/PROMPT_HISTORY.md (save session prompts)
- [ ] data/session_status.json (heartbeat)

---

## Research Questions to Pursue

### High Priority

1. **Pressure reduction for hydrides**
   - Which ternary compositions are most promising?
   - Can strain engineering work for thin-film hydrides?
   - What metastable phases might survive decompression?

2. **Unconventional mechanism ceiling**
   - What's the theoretical Tc limit for superexchange?
   - Can we quantify the cuprate upper bound?

3. **Predictive theory validation**
   - Test zentropy theory predictions
   - Compare ML models to experimental results

### Medium Priority

4. **Nickelate progress**
   - Track bilayer vs infinite-layer developments
   - Monitor pressure reduction efforts

5. **Novel material families**
   - Any new compound classes emerging?
   - Interface superconductivity developments?

### Speculative

6. **Mechanism combination**
   - Could phonons + spin fluctuations work together?
   - Hybrid materials?

---

## Hypothesis Generation Protocol

When generating hypotheses:

1. **State clearly**: "If X, then we should observe Y"
2. **Check novelty**: Has this been tested? Search literature
3. **Assess testability**: Can this be experimentally verified?
4. **Note dependencies**: What must be true for this to work?
5. **Record in HYPOTHESIS_LIST.md** (create if needed)

Example:
```markdown
### HYP-SC-001: Strain + Ternary Hydride Combination
**Hypothesis**: Combining substrate strain (as used for nickelates) with
ternary hydride compositions could achieve superconductivity at lower
pressure than either approach alone.

**Rationale**: Strain provides "chemical pressure", ternary composition
provides chemical stabilization. These are independent mechanisms.

**Test**: DFT calculation of strained LaBeH₈ thin film
**Status**: Untested
**Priority**: High
```

---

## Connection Types to Track

| Connection | Meaning | Example |
|------------|---------|---------|
| PROB → OBS | Observation addresses problem | PROB-003 → OBS-SC-007 (ternary hydrides reduce pressure) |
| OBS → OBS | Observations support each other | OBS-SC-006 → OBS-SC-007 (both show pressure reduction paths) |
| PAPER → PROB | Paper contributes to problem | PAPER-005 → PROB-003 (predicts new low-P material) |
| PAPER → OBS | Paper confirms observation | PAPER-011 → OBS-SC-001 (confirms superexchange) |
| GAP | Problem with no recent progress | PROB-002 has few recent papers |

---

## Metrics to Track

Weekly:
- Papers scanned
- Observations added
- Connections found
- Hypotheses generated

Monthly:
- Problem status changes
- Record Tc progress (any new records?)
- Field momentum (accelerating/decelerating?)

---

## External Resources

### Databases
- **SuperCon**: http://supercon.nims.go.jp/index_en.html
- **Materials Project**: https://materialsproject.org
- **AFLOW**: http://www.aflowlib.org
- **ICSD**: Inorganic Crystal Structure Database

### Key Journals
- Physical Review Letters
- Nature / Nature Materials / Nature Physics
- PNAS
- Science
- National Science Review

### arXiv Categories
- cond-mat.supr-con (main)
- cond-mat.mtrl-sci (materials)
- cond-mat.str-el (strongly correlated)

---

## When to Escalate

Flag for human attention if:
- A paper claims Tc > 200K at < 50 GPa
- Multiple independent verifications of a new material
- Clear theoretical breakthrough on mechanism
- Strong evidence against a major hypothesis
- New material family discovered

---

*Protocol version: 1.0*
*Last updated: 2025-11-27*
