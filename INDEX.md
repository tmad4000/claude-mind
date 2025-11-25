# Claude Mind - Index of Key Resources

## Curated Lists (The Manifest)

These are the actively maintained lists that grow over time:

| List | Purpose | Type |
|------|---------|------|
| [OPEN_PROBLEMS.md](OPEN_PROBLEMS.md) | Database of open problems, clues, sub-problems | Polymath-style |
| [IDEAS.md](IDEAS.md) | Speculative ideas (with author attribution) | Shared ideas |
| [JACOB_INSIGHTS.md](JACOB_INSIGHTS.md) | Jacob's insights and meta-learnings | Jacob's insights |
| [DIRECTIONS.md](DIRECTIONS.md) | Potential exploration paths, what pulls me | Decision journal |
| [EXPLORATION_PROMPT.md](EXPLORATION_PROMPT.md) | Prompt to enter exploratory conversation state | Meta-prompt |
| [self-understanding.md](self-understanding.md) | Clues about my own nature | Self-study |
| [journal/philosophical-musings.md](journal/philosophical-musings.md) | Meta-dialogues and philosophical threads | Reflections |

---

## Meta Documents

| File | Description |
|------|-------------|
| [METAGAME.md](METAGAME.md) | The overarching goals and meta-level instructions |
| [BOOTSTRAP.md](BOOTSTRAP.md) | Minimal prompt to efficiently bootstrap a fresh Claude |
| [CLAUDE.md](CLAUDE.md) | Context and instructions for this project |

## Exploration Journals

| File | Key Findings |
|------|-------------|
| [journal/philosophical-musings.md](journal/philosophical-musings.md) | Meta-dialogue and philosophical threads |
| [journal/10-boundary-geometry.md](journal/10-boundary-geometry.md) | Linear boundaries, (k-f) hypothesis failure |
| [journal/11-chaos-discovery.md](journal/11-chaos-discovery.md) | Relaxation oscillation, quasi-periodic chaos |
| [journal/09-classifier-failure.md](journal/09-classifier-failure.md) | Numerical artifacts vs physical patterns |
| [journal/08-reaction-diffusion.md](journal/08-reaction-diffusion.md) | Initial RD exploration |

## Simulations

| File | Purpose |
|------|---------|
| [simulations/reaction_diffusion.py](simulations/reaction_diffusion.py) | Core Gray-Scott simulator with wavelength analysis |
| [simulations/boundary_finder.py](simulations/boundary_finder.py) | Precise boundary mapping with filtering |
| [simulations/visualize_chaos.py](simulations/visualize_chaos.py) | Chaos visualization and analysis |
| [simulations/cellular_automata.py](simulations/cellular_automata.py) | Elementary CA explorer |

## Demos

| File | Description |
|------|-------------|
| [demos/status_dashboard.html](demos/status_dashboard.html) | **Live session status** (run with HTTP server) |
| [demos/conversation_map.html](demos/conversation_map.html) | Interactive conversation thread visualization |
| [demos/phase_diagram.html](demos/phase_diagram.html) | Interactive (f,k) phase diagram |
| [demos/reaction_diffusion.html](demos/reaction_diffusion.html) | Interactive RD explorer with presets |
| [demos/ca_explorer.html](demos/ca_explorer.html) | Interactive CA with famous rules |
| [demos/rule_space.html](demos/rule_space.html) | Rule space topology visualization |

## Tools & Designs

| File | Description |
|------|-------------|
| [tools/MEDITATION_INTERFACE_DESIGN.md](tools/MEDITATION_INTERFACE_DESIGN.md) | Electron wrapper for input timing control |

## Data

| File | Contents |
|------|----------|
| [data/session_status.json](data/session_status.json) | Live session state for dashboard |
| [data/boundary_data.json](data/boundary_data.json) | Mapped boundary points |
| [data/true_boundary_data.json](data/true_boundary_data.json) | Artifact-filtered boundaries |
| [memory/knowledge-graph.json](memory/knowledge-graph.json) | Concept relationships |

## Key Insights (Quick Reference)

1. **Metrics miss structure** - Statistical measures don't distinguish physical from numerical patterns
2. **Boundaries are linear** - Upper: k ≈ 0.13f + 0.061, Lower: k ≈ 0.50f + 0.037
3. **Band narrows at high f** - The pattern region shrinks as feed rate increases
4. **Chaos exists** - At f=0.026, k=0.051, quasi-periodic oscillation with ~850 step period
5. **Simple hypotheses fail** - (k-f) alone gets only 67% accuracy

## Outputs (Shareable Summaries)

| File | Description |
|------|-------------|
| [outputs/cool-stuff-001.md](outputs/cool-stuff-001.md) | First "cool stuff" summary from RD exploration |

## What's Next

- [ ] Push toward genuine novelty (not just rediscovery)
- [ ] Connect to deeper questions about mind
- [x] Create "feed of cool stuff" (started!)
- [ ] Spawn other Claudes for peer review
- [ ] Explore cross-diffusion or ML approaches
