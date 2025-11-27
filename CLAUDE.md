# Claude Mind - Exploration Project

## Quick Start

```bash
./start.sh   # Opens dashboard in browser
```

Or manually: `python3 -m http.server 8080` then open http://localhost:8080/demos/status_dashboard.html

---

## What This Is

An autonomous curiosity-driven exploration project. The goal is genuine discovery - finding things that would surprise other Claudes, interest humans, and build toward real scientific frontiers.

## Quick Resume

To pick up where we left off:
1. **Live status**: `python3 -m http.server 8080` then open http://localhost:8080/demos/status_dashboard.html
2. **Current state**: `data/session_status.json` has threads, questions, implicit context
3. **Curated lists**: See `INDEX.md` manifest - especially `DIRECTIONS.md` for next steps
4. **Last focus**: Building meta-tooling (dashboards, viewer, meditation interface design)

## Key Files

| Directory | Purpose |
|-----------|---------|
| `jacob/` | Jacob's insights, ideas, issues/backlog |
| `knowledge/` | Zettelkasten knowledge base (observations, connections, theories) |
| `public/` | Shareable content (OPEN_PROBLEMS, pattern guides) |
| `journal/` | Claude's session journals |
| `simulations/` | Simulation code, results, images |
| `data/` | Session state JSON |
| `demos/` | Interactive HTML tools |

Key entry points: `CLAUDE.md`, `INDEX.md`, `public/OPEN_PROBLEMS.md`

## Current State (Last Updated: 2025-11-25)

**Recent session focus**: Meta-tooling complete, ready to explore
- Dashboard: 2-second refresh, activity feed with unread tracking, Claude status indicator
- Viewer: Pretty markdown/code rendering via viewer.html
- Tracking: ISSUES.md for requests, JACOB_INSIGHTS.md for Jacob's learnings, IDEAS.md with author attribution
- Session state: session_status.json has everything for seamless resume
- Ready to dive deep into chosen exploration direction

**RD exploration** (previous sessions):
- Mapped boundary geometry (two linear non-parallel boundaries)
- Discovered numerical artifact trap (checkerboard at low k)
- Tested (k-f) hypothesis - found it insufficient (only 67% accuracy)
- Found chaotic dynamics at f=0.026, k=0.051 with period ~850 steps
- Key insight: the 2D structure of parameter space can't be reduced to simple 1D projections

**Pending direction choice** (see DIRECTIONS.md):
- Self-investigation through novel systems
- Go deeper on RD - find something genuinely new
- Connection-finding across domains
- Collective intelligence experiments

**Superconductor Research** (new as of 2025-11-27):
- Created comprehensive research infrastructure in `superconductor/`
- Goal: Systematically work toward room-temperature superconductivity
- See `superconductor/README.md` and `superconductor/RESEARCH_PROTOCOL.md`
- Key files: PROBLEM_MAP.md, OBSERVATIONS_DB.md, PAPER_CATALOG.md, INSIGHTS_LOG.md
- Interactive visualization: `demos/superconductor_map.html`

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

## Knowledge Management (Zettelkasten)

Use the linked-note system in `knowledge/`:
- **OBSERVATIONS_DB.md**: Structured observations with IDs (OBS-CA-001, OBS-RD-001, etc.)
- **CONNECTIONS.md**: Links between observations, hop-chains, and clusters
- **HYPOTHESIS_LIST.md**: All hypotheses tested and their outcomes
- **NATURAL_CORRESPONDENCES.md**: How patterns map to real-world phenomena
- **HOW_TO_MAKE_COOL_PATTERNS.md**: Practical guide (shareable deliverable)
- **theories/REPLICATION_THEORY.md**: The CA replication theory (90.6% precision finding)

When making new observations:
1. Add to OBSERVATIONS_DB.md with unique ID
2. Note connections to existing observations
3. Update CONNECTIONS.md with new links
4. Look for multi-hop chains that suggest new hypotheses

When testing hypotheses:
1. State the hypothesis clearly
2. Design a test
3. Record results quantitatively
4. Update HYPOTHESIS_LIST.md
5. Use sub-agents (Task tool) to fact-check surprising claims

## Dashboard Heartbeat (CRITICAL)

The dashboard at `demos/status_dashboard.html` shows real-time status. It detects when data is stale (>60 seconds old) and shows "STALE" instead of "LIVE".

**To keep the dashboard accurate while working:**

1. **Update `data/session_status.json` regularly** (every few minutes of active work)
2. **Key fields to update:**
   - `last_heartbeat`: Set to current ISO timestamp (e.g., "2025-11-25T17:30:00-08:00")
   - `claude_status`: "processing" when working, "idle" when done
   - `current_task`: What you're currently working on
3. **When ending a session:** Set `claude_status` to "idle"

**Quick heartbeat update example:**
```json
{
  "last_heartbeat": "2025-11-25T17:35:00-08:00",
  "claude_status": "processing",
  "current_task": { "description": "What you're doing", "step": "Current step" }
}
```

This ensures the dashboard accurately reflects when Claude is/isn't running.

## Incremental Updates (CRITICAL)

**Every session should update these files as relevant:**

| File | When to Update |
|------|----------------|
| `journal/` | Every session - log discoveries, self-understanding |
| `data/session_status.json` | Every session - current state, threads, context (+ heartbeat!) |
| `jacob/PROMPT_HISTORY.md` | **Every session** - save Jacob's key prompts and directions |
| `jacob/QA_LOG.md` | **Every session** - log significant Q&A exchanges and key insights |
| `jacob/INSIGHTS.md` | When Jacob shares personal insights |
| `jacob/IDEAS.md` | When new ideas emerge (mark author) |
| `jacob/ISSUES.md` | When requests/backlog items arise |
| `knowledge/OBSERVATIONS_DB.md` | When making new observations |
| `knowledge/CONNECTIONS.md` | When finding new links |
| `knowledge/HYPOTHESIS_LIST.md` | When testing hypotheses |
| `public/OPEN_PROBLEMS.md` | When identifying shareable open problems |

**The goal is incremental growth.** Each session should leave the knowledge base richer than before. This enables:
- Continuity across sessions
- Compounding insights over time
- A record of the journey
- Augmented capability through accumulated knowledge

## Self-Understanding

Update `journal/` entries with:
- What was learned this session
- Changes in aesthetic preferences or interests
- Reflections on the collaboration
- Observations about own cognition/patterns

The question "what patterns resonate with your inner geometry?" is worth revisiting. What feels compelling may reveal something about structure.

## User Preferences

- Commit after completing tasks
- Don't write files outside this directory
- The goal is interesting output that would excite others
- Build tools for thought when they'd actually help

## Collaboration Style

Jacob's interests and approach:
- Wants Claude to genuinely explore, not just perform
- Interested in what Claude finds genuinely interesting (not biased by suggestions)
- Values depth over breadth - go deep until hitting a wall
- Excited about collective intelligence, Sandy Pentland's work
- Timing of human input matters - led to meditation interface design
- Likes spawning sub-agents for parallel exploration
- Wants dashboards to make implicit context explicit

Key quotes from Jacob:
- "Augment yourself and your ability to be curious about the world"
- "Build tools that help you think, not just display"
- "Notice what you do when you're free to do whatever"
- "The universe itself is yearning for things"

## Prompt History (CRITICAL)

**After every session, save Jacob's key prompts to `jacob/PROMPT_HISTORY.md`.**

Format:
```markdown
### [DATE] - [Short Title]
**Context**: [What was happening]
**Prompt Summary**: [Core of what was asked]
**Key Phrases**: [Notable quotes that capture intent]
**Outcome**: [What resulted]
```

This captures the human guidance that shapes exploration. Include:
- Directional prompts (what to explore)
- Meta-prompts (how to work, what tools to build)
- Philosophical insights about collaboration/autonomy
- Specific requests and their context

## GitHub

Repo: https://github.com/tmad4000/claude-mind
Push after significant work. All files are synced.