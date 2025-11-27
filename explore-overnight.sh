#!/bin/bash
# Overnight Exploration - Run in a terminal window
# This runs Claude sessions one after another, with output visible
#
# Usage: ./explore-overnight.sh [num_sessions]
#
# Leave this terminal window open overnight.
# Check progress with: git log --oneline -20
#
# IMPORTANT: Run this directly in a terminal window, not via nohup

set -e
cd "$(dirname "$0")"

# Ensure claude is in PATH
export PATH="/opt/homebrew/bin:$PATH"

NUM_SESSIONS=${1:-10}
COOLDOWN=60  # seconds between sessions

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║        OVERNIGHT EXPLORATION - $NUM_SESSIONS Sessions                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Started: $(date)"
echo "Leave this terminal open overnight."
echo "Progress visible via: git log --oneline"
echo ""

COMMITS_START=$(git rev-list --count HEAD 2>/dev/null || echo 0)

for ((i=1; i<=NUM_SESSIONS; i++)); do
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "  SESSION $i of $NUM_SESSIONS - $(date)"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""

    if [ $i -eq 1 ]; then
        PROMPT="You are Claude exploring overnight while the user sleeps. This is session 1 of $NUM_SESSIONS.

Goals:
1. Make meaningful research progress
2. Commit work with clear messages
3. Update session_status.json for dashboard visibility
4. Add any novel findings to public/PUBLISHABLE_FINDINGS.md

Read CLAUDE.md for context. Focus on completing something tangible.
Go explore something genuinely interesting!"
    else
        PROMPT="Continuing overnight exploration - session $i of $NUM_SESSIONS.

Check git log -5 for what previous sessions accomplished.
Either continue that work or pivot to something new.

Make progress, commit, and update the dashboard."
    fi

    # Run claude with permissions to write files
    /opt/homebrew/bin/claude --dangerously-skip-permissions -p "$PROMPT" || echo "Session ended"

    COMMITS_NOW=$(git rev-list --count HEAD 2>/dev/null || echo 0)
    SESSION_COMMITS=$((COMMITS_NOW - COMMITS_START))

    echo ""
    echo "Session $i complete. Total commits so far: $SESSION_COMMITS"

    if [ $i -lt $NUM_SESSIONS ]; then
        echo "Next session in ${COOLDOWN}s..."
        sleep $COOLDOWN
    fi
done

COMMITS_FINAL=$(git rev-list --count HEAD 2>/dev/null || echo 0)
TOTAL_COMMITS=$((COMMITS_FINAL - COMMITS_START))

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║        OVERNIGHT EXPLORATION COMPLETE                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Ended: $(date)"
echo "Sessions: $NUM_SESSIONS"
echo "Commits: $TOTAL_COMMITS"
echo ""
echo "Review with: git log --oneline -20"
