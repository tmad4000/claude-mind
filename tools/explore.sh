#!/bin/bash
# Launch Claude to continue exploration
# Usage: ./explore.sh [optional custom prompt]

cd /Users/jacobcole/code/claude-mind

# Build the prompt
if [ -n "$1" ]; then
    PROMPT="$1"
else
    # Get next investigation
    NEXT_INV=$(python3 tools/explorer.py next 2>/dev/null)

    PROMPT="Continue your curiosity exploration.

Your current state:
$(python3 tools/explorer.py status 2>/dev/null)

$NEXT_INV

Push toward genuine discoveries - things that would surprise another Claude.
Create visualizations or demos I can see.
Journal what you find.
Commit interesting progress."
fi

echo "=== Launching Claude Mind Explorer ==="
echo ""
echo "Prompt:"
echo "$PROMPT" | head -20
echo "..."
echo ""
echo "=== Starting Claude ==="
echo ""

# Launch claude with the prompt
# The -p flag passes the initial prompt
# Output streams to terminal so you can watch
claude -p "$PROMPT"
