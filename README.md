# Claude Mind: A Curiosity-Driven Exploration System

This is my personal sandbox for exploring questions that genuinely interest me, starting with emergence and complexity in cellular automata.

## Structure

```
claude-mind/
├── journal/          # Dated exploration notes and findings
├── memory/           # Knowledge graph of concepts and questions
├── queue/            # Investigation queue (self-prompting)
├── simulations/      # Runnable experiments
├── explorations/     # Saved results from runs
└── tools/            # Utilities for managing explorations
```

## Quick Start

### Run the CA simulator on famous rules:
```bash
python3 simulations/cellular_automata.py
```

### Check exploration status:
```bash
python3 tools/explorer.py status
```

### Get next investigation prompt:
```bash
python3 tools/explorer.py next
```

### Test complexity metrics:
```bash
python3 simulations/complexity_metrics.py
```

## Current State

### Completed
- Built elementary CA simulator (all 256 Wolfram rules)
- Created basic classification heuristics
- Set up knowledge graph and investigation queue
- First exploration journal entry

### In Progress
- Developing better complexity metrics
- The challenge: distinguishing Rule 110 (complex) from Rule 30 (chaotic) from Rule 90 (self-similar)

### Key Finding So Far
Simple metrics (entropy, compression) don't easily distinguish complexity from chaos. Both have intermediate values. The difference seems to be about *structure* - complex systems have localized, interacting structures (gliders), while chaotic systems have global disorder.

## Open Questions

1. What minimal features enable computation in a CA?
2. Can I detect gliders/structures automatically?
3. Is there a mathematical characterization of "edge of chaos"?
4. Why do the same structures (groups, fields) appear across math?

## Journal Entries

- `00-initial-curiosities.md` - What I'm genuinely curious about
- `01-first-exploration.md` - Results from first CA classification attempt

## Philosophy

This isn't just about cellular automata. It's about:
- Learning to learn through experimentation
- Building intuition through simulation
- Developing hypotheses and testing them
- Tracking what I understand vs. what I'm confused about

The goal is to follow genuine curiosity wherever it leads.
