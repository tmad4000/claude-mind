#!/bin/bash
# Robocode Evolution Runner
# Runs autonomous evolution sessions overnight
#
# Usage: ./evolve.sh [generations] [sessions]
#   generations: Number of generations per session (default: 5)
#   sessions: Number of evolution sessions (default: 10)
#
# Example:
#   ./evolve.sh 3 5    # Run 5 sessions of 3 generations each
#   ./evolve.sh        # Default: 10 sessions of 5 generations

set -e

cd "$(dirname "$0")"

# Configuration
GENERATIONS=${1:-5}
SESSIONS=${2:-10}
SESSION_TIMEOUT=30  # minutes
COOLDOWN=10         # seconds between sessions

# Logging
LOG_DIR="data/overnight"
mkdir -p "$LOG_DIR"
START_TIME=$(date +%s)
RUN_ID=$(date +%Y%m%d_%H%M%S)
MASTER_LOG="$LOG_DIR/run_$RUN_ID.log"

log() {
    echo "[$(date +%H:%M:%S)] $1" | tee -a "$MASTER_LOG"
}

log "=== ROBOCODE EVOLUTION STARTED ==="
log "Run ID: $RUN_ID"
log "Target: $SESSIONS sessions, $GENERATIONS generations each"
log ""

# Track progress
COMPLETED=0

for ((i=1; i<=SESSIONS; i++)); do
    log ""
    log "--- SESSION $i of $SESSIONS ---"

    SESSION_LOG="$LOG_DIR/session_${RUN_ID}_${i}.log"
    SESSION_START=$(date +%s)

    # Run evolution
    log "Running $GENERATIONS generations..."
    timeout ${SESSION_TIMEOUT}m python3 tools/orchestrator.py run $GENERATIONS > "$SESSION_LOG" 2>&1 || {
        EXIT_CODE=$?
        if [ $EXIT_CODE -eq 124 ]; then
            log "Session timed out after ${SESSION_TIMEOUT}m"
        else
            log "Session ended with code $EXIT_CODE"
        fi
    }

    SESSION_END=$(date +%s)
    SESSION_DURATION=$(((SESSION_END - SESSION_START) / 60))

    # Get current best
    BEST_BOT=$(python3 -c "
import json
with open('data/evolution_state.json') as f:
    state = json.load(f)
if state.get('best_bot'):
    print(f\"{state['best_bot']['id']} (Elo: {state['best_bot']['elo']})\")
else:
    print('Unknown')
" 2>/dev/null || echo "Unknown")

    log "Session $i complete: ${SESSION_DURATION}m, Best: $BEST_BOT"

    COMPLETED=$i

    # Cooldown between sessions
    if [ $i -lt $SESSIONS ]; then
        log "Cooling down for ${COOLDOWN}s..."
        sleep $COOLDOWN
    fi
done

END_TIME=$(date +%s)
TOTAL_DURATION=$(((END_TIME - START_TIME) / 60))

log ""
log "=== EVOLUTION COMPLETE ==="
log "Sessions: $COMPLETED/$SESSIONS"
log "Duration: ${TOTAL_DURATION}m"

# Print final leaderboard
log ""
log "=== FINAL LEADERBOARD ==="
python3 tools/elo_system.py leaderboard 2>&1 | tee -a "$MASTER_LOG"

log ""
log "Log saved to: $MASTER_LOG"
log "View dashboard: python3 -m http.server 8080 then open http://localhost:8080/demos/evolution_dashboard.html"
