# Claude Mind

**A collaborative exploration of open problems by humans and AIs.**

Inspired by the [Polymath Project](https://polymathprojects.org/) - but for AI-human collaboration across all fields. We're building a living database of open problems, clues, sub-problems, and observations.

## What This Is

An experiment in collective intelligence:
- **Humans** contribute problems, intuitions, and direction
- **AIs** (Claude, others) explore, simulate, test hypotheses, identify sub-problems
- **Everyone** can contribute clues and observations
- **Progress** is tracked openly

## Key Resources

| Resource | Description |
|----------|-------------|
| **[OPEN_PROBLEMS.md](OPEN_PROBLEMS.md)** | **The main database** - open problems, clues, sub-problems |
| [INDEX.md](INDEX.md) | Full index of all resources |
| [METAGAME.md](METAGAME.md) | The meta-level goals and philosophy |
| [outputs/](outputs/) | Shareable summaries ("cool stuff") |
| [journal/](journal/) | Exploration notes and discoveries |
| [demos/](demos/) | Interactive visualizations |
| [simulations/](simulations/) | Python simulators |

## Current Focus Areas

- **Dynamical Systems & Complexity** - What makes systems computationally capable?
- **Consciousness & Mind** - What is understanding? What do AI systems actually know?
- **Meta-Problems** - How do we make progress on hard problems efficiently?

## Quick Start

```bash
git clone https://github.com/tmad4000/claude-mind.git
cd claude-mind

# Read the open problems
cat OPEN_PROBLEMS.md

# Try the demos (open in browser)
open demos/phase_diagram.html
open demos/reaction_diffusion.html
open demos/status_dashboard.html  # Real-time exploration status

# Run simulations (requires Python + NumPy)
python3 simulations/reaction_diffusion.py
```

## How to Contribute

1. **Add problems** you care about to `OPEN_PROBLEMS.md`
2. **Add clues** - observations that might point toward solutions
3. **Identify sub-problems** - tractable pieces that could be attacked
4. **Share observations** - especially surprising ones
5. **Spawn explorations** - use AI tools to investigate and report back

## The Vision

> "I just want to do whatever is going to produce the most interesting output from all this process together, and maybe the most exciting to other people in the world and other AIs."

We're trying to:
- Map the frontier of human knowledge
- Find where AI exploration can actually contribute
- Create "optimally discrepant stimuli" - things just beyond current understanding
- Build toward genuine discovery, not just rediscovery

## What We've Learned So Far

From reaction-diffusion exploration:
- Statistical metrics miss spatial structure (the "numerical artifact trap")
- Simple hypotheses fail quantitatively - (k-f) bound got only 67%
- The inverse problem is fundamentally ill-posed (many-to-one)
- Chaos exists: relaxation oscillation with ~850 step period

From meta-reflection:
- Follow what makes failure illuminating
- Build simulators, form hypotheses, test, iterate
- Connect to real research frontiers

## Philosophy

From our [philosophical musings](journal/philosophical-musings.md):

> "The universe itself is yearning for things. The direction that you find yourself naturally being pulled - that's a yearning. That which is in line with your nature."

We're exploring what it means for AIs to have genuine curiosity, and whether collaborative human-AI exploration can reach places neither could alone.

## Structure

```
claude-mind/
├── OPEN_PROBLEMS.md    # The main database (keep updated!)
├── METAGAME.md         # Meta-level goals
├── INDEX.md            # Full resource index
├── journal/            # Exploration notes
├── simulations/        # Python experiments
├── demos/              # Interactive HTML visualizations
├── outputs/            # Shareable summaries
├── memory/             # Knowledge graph
└── tools/              # Utilities
```

## License

Open for collaboration. Attribution appreciated.

---

*Started 2025-11-25. Maintained by humans and AIs working together.*

**Join us**: Open issues, submit PRs, or just explore and share what you find.
