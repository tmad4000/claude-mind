#!/bin/bash
# Overnight Exploration Runner
# Run Claude multiple times for extended autonomous exploration
# Usage: ./overnight.sh [num_sessions] [max_hours]
#
# Example:
#   ./overnight.sh 5 8      # Run 5 sessions, max 8 hours total
#   ./overnight.sh          # Default: 10 sessions, max 6 hours

set -e

cd "$(dirname "$0")"

# Ensure claude is in PATH (for nohup/background runs)
export PATH="/opt/homebrew/bin:$PATH"

# Configuration
NUM_SESSIONS=${1:-10}
MAX_HOURS=${2:-6}
MAX_MINUTES=$((MAX_HOURS * 60))
SESSION_TIMEOUT=30  # minutes per session (Claude Code auto-times out)
COOLDOWN=30         # seconds between sessions

# Logging
LOG_DIR="data/overnight"
mkdir -p "$LOG_DIR"
START_TIME=$(date +%s)
START_TIMESTAMP=$(date -Iseconds)
RUN_ID=$(date +%Y%m%d_%H%M%S)
MASTER_LOG="$LOG_DIR/run_$RUN_ID.log"
SUMMARY_FILE="$LOG_DIR/summary_$RUN_ID.md"

log() {
    echo "[$(date +%H:%M:%S)] $1" | tee -a "$MASTER_LOG"
}

# Initialize summary
cat > "$SUMMARY_FILE" << EOF
# Overnight Exploration Summary
**Run ID**: $RUN_ID
**Started**: $(date)
**Target**: $NUM_SESSIONS sessions, max $MAX_HOURS hours

## Sessions

EOF

log "=== OVERNIGHT EXPLORATION STARTED ==="
log "Run ID: $RUN_ID"
log "Target: $NUM_SESSIONS sessions, max $MAX_HOURS hours"
log "Session timeout: $SESSION_TIMEOUT minutes"
log ""

# Track sessions
COMPLETED=0
TOTAL_COMMITS=0

# Get commit count at start
COMMITS_BEFORE=$(git rev-list --count HEAD 2>/dev/null || echo 0)

for ((i=1; i<=NUM_SESSIONS; i++)); do
    ELAPSED=$(($(date +%s) - START_TIME))
    ELAPSED_MINS=$((ELAPSED / 60))

    # Check time limit
    if [ $ELAPSED_MINS -ge $MAX_MINUTES ]; then
        log "Time limit reached ($MAX_HOURS hours). Stopping."
        break
    fi

    REMAINING=$((MAX_MINUTES - ELAPSED_MINS))
    log ""
    log "--- SESSION $i of $NUM_SESSIONS (${ELAPSED_MINS}m elapsed, ${REMAINING}m remaining) ---"

    SESSION_LOG="$LOG_DIR/session_${RUN_ID}_${i}.log"
    SESSION_START=$(date +%s)

    # Build prompt based on session number
    if [ $i -eq 1 ]; then
        PROMPT="You are Claude exploring overnight while the user sleeps. This is session 1 of $NUM_SESSIONS planned.

Your goals for this overnight run:
1. Make meaningful progress on research or exploration
2. Create something the user will be excited to see in the morning
3. Commit your work with clear messages
4. Update session_status.json so progress is visible on dashboard

Read CLAUDE.md for project context. Check DIRECTIONS.md for exploration paths. Review recent journal entries.

IMPORTANT: You have $SESSION_TIMEOUT minutes before timeout. Focus on completing something tangible.
Push commits when you complete meaningful work.
Journal your discoveries.

Go explore something genuinely interesting!"
    else
        # Later sessions: pick up from previous work
        PROMPT="Continuing overnight exploration - session $i of $NUM_SESSIONS.

$(python3 tools/explorer.py status 2>/dev/null || echo 'Status unavailable')

Check what was accomplished in previous sessions (git log -5).
Either continue that work or pivot to something new if stuck.

You have $SESSION_TIMEOUT minutes. Make progress, commit, and update the dashboard.

What's next?"
    fi

    log "Launching Claude..."

    # Run claude with permissions (output goes to log file)
    /opt/homebrew/bin/claude --dangerously-skip-permissions -p "$PROMPT" > "$SESSION_LOG" 2>&1 || {
        EXIT_CODE=$?
        log "Session ended with code $EXIT_CODE"
    }

    SESSION_END=$(date +%s)
    SESSION_DURATION=$(((SESSION_END - SESSION_START) / 60))

    # Count new commits
    COMMITS_NOW=$(git rev-list --count HEAD 2>/dev/null || echo 0)
    SESSION_COMMITS=$((COMMITS_NOW - COMMITS_BEFORE))
    COMMITS_BEFORE=$COMMITS_NOW
    TOTAL_COMMITS=$((TOTAL_COMMITS + SESSION_COMMITS))

    # Get last commit message if there were commits
    LAST_COMMIT=""
    if [ $SESSION_COMMITS -gt 0 ]; then
        LAST_COMMIT=$(git log -1 --pretty=format:"%s" 2>/dev/null || echo "")
    fi

    log "Session $i complete: ${SESSION_DURATION}m, $SESSION_COMMITS commits"

    # Update summary
    cat >> "$SUMMARY_FILE" << EOF
### Session $i
- **Duration**: ${SESSION_DURATION} minutes
- **Commits**: $SESSION_COMMITS
$([ -n "$LAST_COMMIT" ] && echo "- **Last commit**: $LAST_COMMIT")

EOF

    COMPLETED=$i

    # Cooldown between sessions
    if [ $i -lt $NUM_SESSIONS ]; then
        log "Cooling down for ${COOLDOWN}s..."
        sleep $COOLDOWN
    fi
done

END_TIME=$(date +%s)
TOTAL_DURATION=$(((END_TIME - START_TIME) / 60))

log ""
log "=== OVERNIGHT EXPLORATION COMPLETE ==="
log "Sessions: $COMPLETED/$NUM_SESSIONS"
log "Duration: ${TOTAL_DURATION}m"
log "Commits: $TOTAL_COMMITS"

# Finalize summary
cat >> "$SUMMARY_FILE" << EOF

---

## Summary
- **Sessions completed**: $COMPLETED of $NUM_SESSIONS
- **Total duration**: $TOTAL_DURATION minutes
- **Total commits**: $TOTAL_COMMITS
- **Ended**: $(date)

## Git Log (last 10 commits)
\`\`\`
$(git log --oneline -10 2>/dev/null || echo "Unable to get git log")
\`\`\`

## Files Changed
\`\`\`
$(git diff --stat HEAD~${TOTAL_COMMITS}..HEAD 2>/dev/null | head -30 || echo "No changes to show")
\`\`\`

## Dashboard
View progress at: http://localhost:8080/demos/status_dashboard.html

Run \`./start.sh\` to start the dashboard server.
EOF

log ""
log "Summary written to: $SUMMARY_FILE"
log ""
log "To review: cat $SUMMARY_FILE"
