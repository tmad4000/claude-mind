# Room-Temperature Superconductor Research Project

An AI-assisted research initiative to systematically map the problem space, track observations, and work toward room-temperature superconductivity.

## Project Structure

```
superconductor/
├── PROBLEM_MAP.md          # Structured map of problems and subproblems
├── OBSERVATIONS_DB.md      # Database of experimental/theoretical observations
├── PAPER_CATALOG.md        # Catalog of papers with connections
├── README.md               # This file
├── data/                   # Generated data (paper scans, etc.)
├── problems/               # Deep dives into specific problems
├── observations/           # Detailed observation notes
├── papers/                 # Paper summaries and analyses
└── tools/                  # Research tools
    ├── arxiv_scanner.py    # Scan arXiv for relevant papers
    ├── bcs_explorer.py     # BCS parameter space visualization
    └── ...
```

## Quick Start

**View the interactive map:**
```bash
cd /Users/jacobcole/code/claude-mind
python3 -m http.server 8080
# Open http://localhost:8080/demos/superconductor_map.html
```

**Scan for recent papers:**
```bash
python3 superconductor/tools/arxiv_scanner.py --days 7 --max 50
```

## Research Approach

### Two-Pronged Strategy

1. **Top-Down: Problem Decomposition**
   - Map the key bottlenecks blocking room-temp superconductivity
   - Identify subproblems and dependencies
   - Track progress on each

2. **Bottom-Up: Observation Collection**
   - Catalog experimental findings
   - Track computational predictions
   - Note patterns and anomalies

### Connection Finding

The magic happens when top-down problems meet bottom-up observations:
- Which observations address which problems?
- What gaps exist (problems with no observations)?
- What patterns emerge across observations?

## Current State of the Field

| Record | Material | Tc | Conditions |
|--------|----------|-----|-----------|
| Highest Tc | LaH₁₀ | 260K | 170-180 GPa |
| Ambient Pressure | HgBa₂Ca₂Cu₃O₈ | 135K | Ambient |
| Ternary Hydride | LaBeH₈ | 110K | 80 GPa |

**Room temperature = 300K at ambient pressure**

## Key Bottlenecks

1. **PROB-001**: Mechanism unknown (cuprates work but we don't fully understand why)
2. **PROB-002**: No predictive theory (can't predict Tc from first principles)
3. **PROB-003**: Extreme pressure required (hydrides need diamond anvils)
4. **PROB-004**: Synthesis challenges (many materials hard to make)

## Promising Directions

1. **Ternary hydrides**: Lower pressure than binary hydrides
2. **Strain engineering**: Nickelates at ambient pressure via substrate strain
3. **ML screening**: Accelerate computational discovery
4. **Zentropy theory**: New predictive framework

## How Claude Can Help

### What's Tractable
- Knowledge synthesis and organization
- Finding connections humans miss
- Generating hypotheses from patterns
- Prioritizing experiments
- Toy model simulations for intuition

### What Needs Labs
- Material synthesis
- Tc measurements
- High-pressure experiments
- Verification of predictions

## Contributing

This is an open research project. Key ways to contribute:
- Add observations to OBSERVATIONS_DB.md
- Catalog papers in PAPER_CATALOG.md
- Identify new connections
- Generate and test hypotheses

## Links

- Interactive visualization: `demos/superconductor_map.html`
- Problem map: `superconductor/PROBLEM_MAP.md`
- Observations: `superconductor/OBSERVATIONS_DB.md`

---

*Last updated: 2025-11-27*
*Maintained by Claude Mind project*
