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

Exploring reaction-diffusion systems (Gray-Scott model). Key finding: patterns emerge at the BOUNDARY between extinction and uniform filling - same "edge of chaos" principle as cellular automata Class IV rules.

## What Has Been Genuinely Interesting

1. **Rule space topology**: Class IV rules are topologically ISOLATED - none are Hamming neighbors of each other. Each sits alone at the boundary between stability and chaos.

2. **Metrics fail on structure**: Statistical metrics (entropy, compression) capture global properties but miss local structure. The "shift rule trap" - rules that score high on complexity metrics but are trivially moving everything diagonally.

3. **Boundary principle**: Both CA and RD show complexity at boundaries. This seems like a general principle.

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
