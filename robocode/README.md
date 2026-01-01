# Robocode Evolution System

An autonomous system that evolves Robocode bots through genetic algorithms and LLM-driven strategy improvement.

## Quick Start

```bash
# Run a quick evolution (1 generation)
python3 tools/orchestrator.py run 1

# Run overnight evolution
./evolve.sh 5 10   # 5 generations per session, 10 sessions

# Check progress
./check-progress.sh

# View dashboard
python3 -m http.server 8080
# Open http://localhost:8080/demos/evolution_dashboard.html
```

## Architecture

### Modular Bot System
Bots are composed of three swappable modules:

**Movement Modules:**
- `Perpendicular` - Moves perpendicular to enemy, oscillating
- `Random` - Unpredictable movement with random direction changes
- `BasicSurfer` - Attempts to dodge bullets via wave tracking

**Gun Modules:**
- `HeadOn` - Fires directly at enemy's current position
- `Linear` - Predicts enemy position assuming constant velocity
- `GuessFactor` - Statistical targeting based on observed patterns

**Radar Modules:**
- `Spin` - Continuous 360° radar sweep
- `Lock` - Locks onto enemy for continuous tracking

### Evolution Process

1. **Initialize Population** - Create random bots with different module combinations
2. **Evaluate** - Each bot battles against benchmark bots (sample.Walls, sample.SpinBot, etc.)
3. **Update Elo** - Win/loss updates Elo ratings
4. **Select** - Tournament selection chooses parents
5. **Evolve** - Crossover and mutation create next generation
6. **Repeat**

### Files

```
robocode/
├── evolve.sh              # Overnight runner
├── check-progress.sh      # Morning status check
├── config/
│   ├── robocode.json     # Robocode paths and settings
│   └── evolution.json    # GA parameters
├── data/
│   ├── evolution_state.json  # Current status
│   ├── population.json       # Bot population
│   └── elo_ratings.json      # Elo rankings
├── bots/
│   ├── templates/        # Bot templates
│   │   ├── BaseAdvancedBot.java
│   │   ├── movement/     # Movement modules
│   │   ├── gun/          # Gun modules
│   │   └── radar/        # Radar modules
│   └── generated/        # Generated bot source
├── tools/
│   ├── orchestrator.py   # Main evolution loop
│   ├── battle_runner.py  # Headless battle execution
│   ├── bot_generator.py  # Module composition
│   ├── elo_system.py     # Elo rating system
│   ├── claude_advisor.py # LLM strategy advisor
│   └── history_tracker.py # Battle/bot archiving
├── demos/
│   ├── evolution_dashboard.html  # Live monitoring
│   └── evolution_history.html    # Evolution replay viewer
└── robocode-install/     # Robocode installation
```

## Current Results

After Generation 1 (with LLM guidance):
- **Evo_Gen1_002** (Perpendicular + HeadOn) - Elo 1629 (#2)
- **Evo_Gen1_001** (Random + HeadOn) - Elo 1603 (#5)
- Beat sample.Walls consistently!
- Closing in on sample.SpinBot (Elo 1699)

**LLM Insights Applied:**
- Claude recommended switching Random → Perpendicular for wall tactics
- Claude recommended Linear → GuessFactor for spinning targets
- Confidence threshold: only apply advice with ≥50% confidence

## Requirements

- Java 8+ (tested with OpenJDK 25)
- Python 3.8+
- Robocode 1.10.1 (included)

## Commands

```bash
# Initialize fresh population
python3 tools/orchestrator.py init

# Run N generations
python3 tools/orchestrator.py run 5

# Check status
python3 tools/orchestrator.py status

# View leaderboard
python3 tools/elo_system.py leaderboard

# Run single battle
python3 tools/battle_runner.py run sample.Walls sample.SpinBot

# Create new bot
python3 tools/bot_generator.py create MyBot
```

## Roadmap

- [x] Robocode installation and setup
- [x] Modular bot template system
- [x] Battle runner and Elo ratings
- [x] Evolution orchestrator
- [x] Real-time dashboard
- [x] Overnight autonomous runner
- [x] LLM-driven strategy improvement (Claude advisor)
- [x] Battle/bot archiving for replay viewing
- [ ] Multi-agent competition (Aggressor vs Survivor vs Adaptive)
- [ ] Download and compete with RoboRumble top bots

## Viewing History

```bash
# Export history data for viewer
python3 tools/history_tracker.py export

# View evolution history
python3 -m http.server 8080
# Open http://localhost:8080/demos/evolution_history.html
```
