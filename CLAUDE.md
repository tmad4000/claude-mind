# Claude Mind - Exploration Project

## Quick Start

```bash
./start.sh      # Opens dashboard in browser
./overnight.sh  # Run autonomous exploration overnight (10 sessions, 6 hours)
./morning.sh    # Check what happened overnight
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

## Current State (Last Updated: 2025-11-27)

**Recent session focus**: Pharmacology research + infrastructure
- Explored substance/effect databases (NatMed, HERB 2.0, DrugBank)
- Discovered 7-18% of FDA drugs have unknown mechanisms
- Key examples: acetaminophen (100+ years), lithium (70+ years), metformin, anesthesia
- Added 4 pharmacology ideas to IDEA_BANK (IDEA-008 through IDEA-011)
- Created dashboard launcher app (`Claude Mind.app`)
- Fixed INDEX.md paths, added Curated Lists to homepage

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

## Research Database (NEW)

The project now uses a **single JSON database** as source of truth for research tracking:

**Primary file**: `data/research_db.json`

Contains:
- `ideas[]` - Research ideas with status (open/promising/failed), ratings, next steps
- `hypotheses[]` - Tested hypotheses with results (confirmed/falsified/partial)
- `findings[]` - Confirmed discoveries, tagged if publishable
- `failed_attempts[]` - Negative results and why they failed (valuable!)

**Workflow**:
1. Update `data/research_db.json` when adding ideas, testing hypotheses, or recording failures
2. Run `python tools/generate_research_views.py` to regenerate Markdown views
3. Generated files:
   - `public/IDEA_BANK_generated.md`
   - `public/FAILED_ATTEMPTS.md`
   - `public/PUBLISHABLE_FINDINGS_generated.md`
   - `knowledge/HYPOTHESIS_LIST_generated.md`

**Why this approach**:
- Single source of truth (no sync issues)
- Easy to query/filter programmatically
- Failed attempts are tracked (rare and valuable)
- Scripts ensure consistency

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
| `public/IDEA_BANK.md` | When discovering research gaps or opportunities |
| `INDEX.md` | When adding new curated lists or key files |
| `index.html` | When adding major new sections or features |

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

## Research Idea Bank (CRITICAL)

**Maintain `public/IDEA_BANK.md` as a curated collection of underexplored research opportunities.**

**Interactive viewer**: `demos/idea_bank.html` - collapsible cards, star filtering, better UX

### Philosophy & Properties

The Idea Bank is a living document of *actionable* research opportunities:
- Quality over quantity - only genuinely promising gaps
- Cross-domain: superconductors, pharmacology, dynamical systems, AI, etc.
- Ideas must be specific enough that a researcher could pursue them

### Star Rating System

- **⭐⭐⭐ Exceptional**: High feasibility + Revolutionary impact + Clear path forward
- **⭐⭐ Strong**: Either high feasibility OR high impact, with reasonable path
- **⭐ Promising**: Worth pursuing but with significant unknowns

### What Qualifies for Inclusion

✅ Include:
- Predicted but never tested experimentally
- Clear synthesis pathway exists but no one has tried it
- Cross-domain connection no one has made
- Specific parameter regime unexplored
- Existing data that hasn't been analyzed a certain way

❌ Exclude:
- Vague "interesting questions" without clear next steps
- Already being actively pursued by multiple groups
- Requires resources beyond plausible reach

### When Adding New Ideas

1. Add to `public/IDEA_BANK.md` following the format there
2. Include: opportunity, why unexplored, feasibility, impact, first steps
3. Assign star rating based on criteria above
4. Update the INDEX table at the bottom (sorted by stars)
5. Update `demos/idea_bank.html` data array to keep viewer in sync

### Maintenance Each Session

- Review discoveries made during exploration
- Look for connections others might have missed
- Ask: "Would a researcher want to know about this?"
- Update ratings as new information emerges
- Mark ideas as "In Progress" or "Completed" when pursued

## Overnight Exploration

The overnight runner lets Claude explore autonomously while you sleep:

```bash
./overnight.sh          # Default: 10 sessions, max 6 hours
./overnight.sh 5 8      # Custom: 5 sessions, max 8 hours
./morning.sh            # View overnight summary
```

**How it works:**
1. Runs multiple Claude sessions sequentially
2. Each session gets context from previous sessions
3. Commits progress after meaningful work
4. Generates a summary with git log and file changes
5. Logs stored in `data/overnight/`

**For overnight Claude sessions:**
- Check git log from previous sessions
- Continue meaningful work or pivot if stuck
- Commit early and often
- Update dashboard status
- Journal discoveries

## GitHub

Repo: https://github.com/tmad4000/claude-mind
Push after significant work. All files are synced.