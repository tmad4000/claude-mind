#!/bin/bash
# Run Claude Code with output streaming to dashboard
# Usage: ./run-claude.sh [optional: prompt]

cd "$(dirname "$0")"

LOG_FILE="data/terminal.log"

# Create data dir if needed
mkdir -p data

# Clear and initialize log
cat > "$LOG_FILE" << EOF
=== Claude Code Session ===
Started: $(date)
Working directory: $(pwd)
==============================

EOF

echo ""
echo "Terminal output streaming to dashboard..."
echo "View at: http://localhost:8080/demos/status_dashboard.html"
echo ""
echo "Starting Claude Code..."
echo ""

# Use script command for proper TTY handling (captures colors)
# macOS and Linux have different script syntax
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS: script -q logfile command
    script -q "$LOG_FILE" claude "$@"
else
    # Linux: script -q -c "command" logfile
    script -q -c "claude $*" "$LOG_FILE"
fi

# Append end marker
echo "" >> "$LOG_FILE"
echo "=== Session ended: $(date) ===" >> "$LOG_FILE"
