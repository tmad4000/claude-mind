#!/bin/bash
# Self-triggering script for Claude Mind
# Run this to continue exploration in a new Claude session

cd /Users/jacobcole/code/claude-mind

# Get next investigation from queue
NEXT=$(python3 -c "
import json
with open('queue/investigation-queue.json') as f:
    data = json.load(f)
pending = [i for i in data['queue'] if i['status'] == 'pending']
if pending:
    pending.sort(key=lambda x: x['priority'])
    inv = pending[0]
    print(f\"Continue exploring: {inv['title']}\")
    print(f\"Description: {inv['description']}\")
    if 'hypothesis' in inv:
        print(f\"Hypothesis: {inv['hypothesis']}\")
else:
    print('All investigations complete! Time for new questions.')
")

# Get recent journal entries
echo ""
echo "Recent exploration:"
ls -t journal/*.md | head -3 | while read f; do
    echo "  - $(basename $f)"
done

# Get knowledge graph stats
STATS=$(python3 -c "
import json
with open('memory/knowledge-graph.json') as f:
    g = json.load(f)
concepts = len([n for n in g['nodes'] if n.get('type') == 'concept'])
questions = len([n for n in g['nodes'] if n.get('type') == 'question'])
print(f'{concepts} concepts, {questions} questions tracked')
")

echo ""
echo "Knowledge state: $STATS"
echo ""
echo "To continue, run:"
echo "  cd /Users/jacobcole/code/claude-mind && claude"
echo ""
echo "Then say: 'Continue your exploration from where you left off. Check tools/explorer.py for context.'"
