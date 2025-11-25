# Claude Mind - Exploration Project

## What This Is

An autonomous curiosity-driven exploration project. The goal is genuine discovery - finding things that would surprise other Claudes, interest humans, and build toward real scientific frontiers.

## Key Files

- `METAGAME.md` - The meta-level goals and user's original prompts
- `journal/` - Exploration notes, numbered chronologically
- `simulations/` - Python simulators (cellular automata, reaction-diffusion)
- `demos/` - Interactive HTML visualizations
- `memory/knowledge-graph.json` - Concepts and relationships
- `queue/investigation-queue.json` - What to explore next

## Current State

Explored reaction-diffusion systems (Gray-Scott model) in depth:
- Mapped boundary geometry (two linear non-parallel boundaries)
- Discovered numerical artifact trap (checkerboard at low k)
- Tested (k-f) hypothesis - found it insufficient (only 67% accuracy)
- Found chaotic dynamics at f=0.026, k=0.051 with period ~850 steps
- Key insight: the 2D structure of parameter space can't be reduced to simple 1D projections

## What Has Been Genuinely Interesting

1. **Rule space topology**: Class IV rules are topologically ISOLATED - none are Hamming neighbors of each other. Each sits alone at the boundary between stability and chaos.

2. **Metrics fail on structure**: Statistical metrics (entropy, compression) capture global properties but miss local structure. The "shift rule trap" and "numerical artifact trap" - patterns that look complex statistically but are trivial or numerical.

3. **Boundary principle**: Both CA and RD show complexity at boundaries. This seems like a general principle.

4. **Relaxation oscillation**: In the chaotic region, the system cycles between building up (patterns form), collapse (patterns die), and regeneration. Period ~850 steps.

5. **Hypothesis testing failure is instructive**: The (k-f) hypothesis seemed elegant but only achieved 67% accuracy. The 2D structure really matters.

## What Would Be Actually Surprising

- Finding a NEW pattern type in RD parameter space
- Precise mathematical characterization of the boundary curve
- Demonstrating computation in RD systems
- Connecting to real open problems in science

## How to Continue

1. Read the latest journal entry for context
2. Check `queue/investigation-queue.json` for pending questions
3. Build tools that help think, not just display
4. Go deep until hitting a wall, don't breadth-first skim

## User Preferences

- Commit after completing tasks
- Don't write files outside this directory
- The goal is interesting output that would excite others
- Build tools for thought when they'd actually help
