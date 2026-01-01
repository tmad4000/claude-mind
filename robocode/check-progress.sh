#!/bin/bash
# Check Robocode Evolution Progress
# Shows latest results and leaderboard

cd "$(dirname "$0")"

echo "=== ROBOCODE EVOLUTION STATUS ==="
echo ""

# Show current status
python3 tools/orchestrator.py status 2>/dev/null

echo ""
echo "=== LEADERBOARD ==="
python3 tools/elo_system.py leaderboard 2>/dev/null

echo ""
echo "=== RECENT LOGS ==="
LATEST_LOG=$(ls -t data/overnight/run_*.log 2>/dev/null | head -1)
if [ -n "$LATEST_LOG" ]; then
    echo "From: $LATEST_LOG"
    tail -20 "$LATEST_LOG"
else
    echo "No overnight logs found"
fi

echo ""
echo "View dashboard: python3 -m http.server 8080"
echo "Then open: http://localhost:8080/demos/evolution_dashboard.html"
