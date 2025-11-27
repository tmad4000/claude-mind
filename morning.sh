#!/bin/bash
# Morning Check - See what Claude did overnight
# Usage: ./morning.sh

cd "$(dirname "$0")"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║              Good Morning! Here's what happened              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Find latest overnight summary
LATEST_SUMMARY=$(ls -t data/overnight/summary_*.md 2>/dev/null | head -1)

if [ -n "$LATEST_SUMMARY" ]; then
    echo "📋 OVERNIGHT SUMMARY"
    echo "────────────────────"
    cat "$LATEST_SUMMARY"
    echo ""
else
    echo "No overnight runs found yet."
    echo "Run ./overnight.sh to start an overnight exploration."
    echo ""
fi

echo ""
echo "📊 RECENT COMMITS"
echo "─────────────────"
git log --oneline --since="12 hours ago" 2>/dev/null || echo "No recent commits"

echo ""
echo "📁 FILES CHANGED (last 12 hours)"
echo "─────────────────────────────────"
git diff --stat $(git log -1 --before="12 hours ago" --format="%H" 2>/dev/null || echo "HEAD~10")..HEAD 2>/dev/null | head -20 || echo "Unable to determine changes"

echo ""
echo "🚀 Quick actions:"
echo "  ./start.sh          - Open dashboard"
echo "  ./overnight.sh      - Run another overnight session"
echo "  git log --oneline   - Full commit history"
echo ""
