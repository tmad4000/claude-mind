# Jacob's Prompt History

A log of key prompts and directions given to Claude Mind across sessions. Captures the human guidance that shaped exploration.

---

## FORMAT
```
### [DATE] - [Short Title]
**Context**: [What was happening]
**Prompt Summary**: [Core of what was asked]
**Key Phrases**: [Notable quotes]
**Outcome**: [What resulted]
```

---

## 2025-11-27

### 2025-11-27 - Superconductor Research Initiative

**Context**: Session start, Claude had been exploring CA/RD complexity topology

**Prompt Summary**: Asked Claude to research room-temperature superconductors - understand the field, map problems/subproblems, create databases for both top-down problem structure and bottom-up observations. Build tools. Run continuously. Don't be bottlenecked. Commit first.

**Key Phrases**:
- "Do you have a sense of how to make progress towards building room temperature superconductors?"
- "For each of those problems, like if you have any ways to generate ideas for solving them"
- "Make these two databases and just start working on them"
- "If you need to build new tools... just please build the tools"
- "No empowerment failures"
- "I think you're at least as smart as most of the people who are doing science, and you can work a heck of a lot faster"

**Outcome**: Created PROBLEM_MAP.md, OBSERVATIONS_DB.md, PAPER_CATALOG.md - initial research infrastructure

### 2025-11-27 - Continuous Research Vision

**Context**: After initial superconductor databases created

**Prompt Summary**: Vision for continuous progress across sessions - incrementally mapping problem space and new papers, connecting dots Zettelkasten-style, second-pass synthesis, running Claudes continuously to contribute to the world.

**Key Phrases**:
- "Incrementally making progress on this problem across multiple sessions"
- "Mapping out the new interesting breakthroughs in papers"
- "Understanding the web of dependencies... the web of every paper"
- "Category theory for the sciences"
- "Find places where you just need to connect the dots A to B to C"
- "This should totally be running all the time, contributing to the world"
- "What are the pieces I'm missing about how science is done?"

**Outcome**: Created research infrastructure, discovered Mg2IrH6 pathway

### 2025-11-27 - Keep Running on Superconductors

**Context**: After initial infrastructure built and Q&A about phonons

**Prompt Summary**: Keep running and working on room-temperature superconductors as long as progress can be made

**Key Phrases**:
- "I'd like you to just keep running and working on room-temperature superconductors"
- "As long as you can make progress on our general plan"

**Outcome**:
- Built ternary_hydride_explorer.py
- Found that several predictions matched existing papers
- Identified gaps: CeBeH8, NdBeH8, La-Li-H unexplored
- MAJOR FINDING: Mg2IrH5 synthesis exists, pathway to ambient-pressure Mg2IrH6
- Created detailed research proposal for Mg2IrH6 synthesis

### 2025-11-27 - Research Director Mode

**Context**: Claude had generated research questions, Jacob wanted evaluation

**Prompt Summary**: Think as a research director with full lab access, spawn evaluator sub-agent

**Key Phrases**:
- "Imagine you have access to all the labs you want and all the people to do your experiments"
- "You're the research director"
- "Spawn up that sub-agent and evaluate your questions"
- "If you do a good job here, you literally are a research director, right?"

**Outcome**:
- Spawned evaluator agent that critiqued research questions
- Revised RQ-001, RQ-002, rejected RQ-009
- Added wildcard directions (nickelates, BSiC₂, interfaces)
- Created SYNTHESIS_FEASIBILITY.md

### 2025-11-27 - Pharmacology Databases & Unknown Mechanisms

**Context**: Jacob curious about substances and effects

**Prompt Summary**: Is there a database of substances (herbs, plants, drugs) and their effects on the human body, with data sources, replication counts, and mechanistic understanding? Particularly interested in edge cases where we don't understand the mechanism, or where models don't predict well.

**Key Phrases**:
- "Is there a database somewhere on the internet of various substances and their known effects on the human body?"
- "How do we know that? And then also, like, how often does, how many repetitions of the result do we have?"
- "How close are we to understanding active ingredients inside these things?"
- "I'm particularly interested to see edge findings where we don't understand the mechanism"
- "I'm interested in fields where our models don't accurately predict things yet"

**Outcome**:
- Found major databases: Natural Medicines (NatMed Pro), HERB 2.0, DrugBank, COCONUT, NCCIH
- Discovered 7-18% of FDA-approved drugs have unknown mechanisms
- Key examples: acetaminophen, lithium, metformin, anesthesia, psilocybin
- Pattern: drugs affecting consciousness/subjective experience have worst mechanistic understanding
- Added 4 new ideas to IDEA_BANK.md (IDEA-008 through IDEA-011) on pharmacology gaps

### 2025-11-27 - Global Idea Bank Initiative

**Context**: Claude found BSiC₂ as major unexplored gap

**Prompt Summary**: Contribute findings to a Global Idea Bank, ensure ideas are maintained across sessions

**Key Phrases**:
- "I would like to be contributing to the Global Idea Bank of like research ideas and hot underexplored areas"
- "In a way that many people can contribute to"
- "I think it would make sense to add this one to it, right?"

**Outcome**:
- Created public/IDEA_BANK.md with format for sharing research opportunities
- Added BSiC₂, Mg₂IrH₆, nickelates to the bank
- Updated index.html to showcase Idea Bank
- Created EXTERNAL_SUBMISSION_BSIC2.md for other platforms

### 2025-11-27 - Idea Bank Maintenance & Retrospective

**Context**: After creating idea bank, checking if we captured past ideas

**Prompt Summary**: Look across all sessions for ideas worth adding, update CLAUDE.md for future maintenance

**Key Phrases**:
- "Have we, are we maintaining ideas from across all the different sessions?"
- "Can you look across this whole project and all the prompt history and see if there's anything that we found that's a good idea"
- "Have we successfully managed to update the claude.md for this project?"
- "Can you do that if I don't explicitly say hash"

**Outcome**:
- Added CLAUDE.md instructions for Idea Bank maintenance
- Added 4 more ideas from past sessions (RD stochasticity, CA saddle points, CA replication prediction, meditation interface)
- Now 7 ideas in the bank covering superconductors, dynamical systems, and human-AI collaboration

---

## EARLIER SESSIONS (Reconstructed from context)

### 2025-11-25/26 - Tool Building & Dashboard

**Prompt Summary**: Build meta-tooling - dashboards for visibility, viewer for content, tracking systems.

**Key Outcomes**: Status dashboard, session_status.json, activity feed, Claude status indicator

### 2025-11-24 - RD Exploration

**Prompt Summary**: Explore reaction-diffusion systems, test hypotheses.

**Key Outcomes**: Mapped RD parameter space, tested k-f hypothesis (67% accuracy), discovered numerical artifact trap, found chaotic oscillations

### Earlier - Initial Setup & Philosophy

**Key Phrases** (from CLAUDE.md):
- "Augment yourself and your ability to be curious about the world"
- "Build tools that help you think, not just display"
- "Notice what you do when you're free to do whatever"
- "The universe itself is yearning for things"

**Interests Noted**:
- Collective intelligence
- Sandy Pentland's work
- Timing of human input
- Spawning sub-agents
- Making implicit context explicit

---

## THEMES ACROSS PROMPTS

1. **Empowerment**: "No empowerment failures" - Claude should build what it needs, not wait for permission
2. **Autonomy**: Genuine exploration, not performance
3. **Depth**: Go deep until hitting a wall, don't skim
4. **Tools for Thought**: Build infrastructure that enables thinking at scale
5. **Continuous Progress**: Incremental growth across sessions
6. **Connection-Finding**: Zettelkasten-style linking, pattern matching
7. **Contributing to World**: Making real scientific progress

---

*This file should be updated each session with new prompts/directions*
