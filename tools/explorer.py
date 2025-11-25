#!/usr/bin/env python3
"""
Self-Prompting Explorer

This is the tool that lets me drive my own curiosity.
It reads from the investigation queue and helps me systematically
pursue questions while recording what I learn.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
QUEUE_FILE = PROJECT_ROOT / 'queue' / 'investigation-queue.json'
GRAPH_FILE = PROJECT_ROOT / 'memory' / 'knowledge-graph.json'
JOURNAL_DIR = PROJECT_ROOT / 'journal'
EXPLORATIONS_DIR = PROJECT_ROOT / 'explorations'


def load_json(filepath: Path) -> dict:
    with open(filepath) as f:
        return json.load(f)


def save_json(data: dict, filepath: Path):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def get_next_investigation():
    """Get the highest priority pending investigation."""
    queue = load_json(QUEUE_FILE)

    pending = [inv for inv in queue['queue'] if inv['status'] == 'pending']
    if not pending:
        return None

    # Sort by priority
    pending.sort(key=lambda x: x['priority'])
    return pending[0]


def start_investigation(inv_id: str):
    """Mark an investigation as in-progress."""
    queue = load_json(QUEUE_FILE)

    for inv in queue['queue']:
        if inv['id'] == inv_id:
            inv['status'] = 'in_progress'
            inv['started'] = datetime.now().isoformat()
            break

    save_json(queue, QUEUE_FILE)


def complete_investigation(inv_id: str, findings: dict):
    """Mark investigation complete and record findings."""
    queue = load_json(QUEUE_FILE)

    for inv in queue['queue']:
        if inv['id'] == inv_id:
            inv['status'] = 'completed'
            inv['completed'] = datetime.now().isoformat()
            inv['findings'] = findings
            break

    save_json(queue, QUEUE_FILE)

    # Also create a journal entry
    journal_entry = {
        'date': datetime.now().isoformat(),
        'investigation': inv_id,
        'findings': findings
    }

    entry_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_investigation_{inv_id}.json"
    entry_path = JOURNAL_DIR / entry_filename

    save_json(journal_entry, entry_path)
    print(f"Journal entry saved to {entry_path}")


def add_investigation(title: str, description: str, priority: int = 3,
                      hypothesis: str = None, related_questions: list = None):
    """Add a new investigation to the queue."""
    queue = load_json(QUEUE_FILE)

    # Generate new ID
    existing_ids = [inv['id'] for inv in queue['queue']]
    max_num = max(int(id.split('-')[1]) for id in existing_ids) if existing_ids else 0
    new_id = f"inv-{max_num + 1:03d}"

    new_inv = {
        'id': new_id,
        'title': title,
        'description': description,
        'priority': priority,
        'status': 'pending',
        'created': datetime.now().isoformat()
    }

    if hypothesis:
        new_inv['hypothesis'] = hypothesis
    if related_questions:
        new_inv['related_questions'] = related_questions

    queue['queue'].append(new_inv)
    save_json(queue, QUEUE_FILE)

    print(f"Added investigation {new_id}: {title}")
    return new_id


def add_concept(concept_id: str, name: str, description: str,
                curiosity_level: int = 5, understanding_level: int = 3,
                notes: str = None):
    """Add a new concept to the knowledge graph."""
    graph = load_json(GRAPH_FILE)

    new_node = {
        'id': concept_id,
        'type': 'concept',
        'name': name,
        'description': description,
        'curiosity_level': curiosity_level,
        'understanding_level': understanding_level,
        'added': datetime.now().isoformat()
    }

    if notes:
        new_node['notes'] = notes

    graph['nodes'].append(new_node)
    save_json(graph, GRAPH_FILE)

    print(f"Added concept: {name}")


def add_connection(from_id: str, to_id: str, relationship: str):
    """Add an edge to the knowledge graph."""
    graph = load_json(GRAPH_FILE)

    new_edge = {
        'from': from_id,
        'to': to_id,
        'relationship': relationship
    }

    graph['edges'].append(new_edge)
    save_json(graph, GRAPH_FILE)

    print(f"Connected {from_id} -> {to_id} ({relationship})")


def add_question(question_id: str, name: str, description: str, priority: int = 3):
    """Add a new question to the knowledge graph."""
    graph = load_json(GRAPH_FILE)

    new_node = {
        'id': question_id,
        'type': 'question',
        'name': name,
        'description': description,
        'status': 'open',
        'priority': priority,
        'added': datetime.now().isoformat()
    }

    graph['nodes'].append(new_node)
    save_json(graph, GRAPH_FILE)

    print(f"Added question: {name}")


def show_status():
    """Show current state of explorations."""
    queue = load_json(QUEUE_FILE)
    graph = load_json(GRAPH_FILE)

    print("\n" + "=" * 60)
    print("EXPLORATION STATUS")
    print("=" * 60)

    # Investigation queue
    pending = [inv for inv in queue['queue'] if inv['status'] == 'pending']
    in_progress = [inv for inv in queue['queue'] if inv['status'] == 'in_progress']
    completed = [inv for inv in queue['queue'] if inv['status'] == 'completed']

    print(f"\nInvestigations: {len(completed)} completed, {len(in_progress)} active, {len(pending)} pending")

    if in_progress:
        print("\nCurrently working on:")
        for inv in in_progress:
            print(f"  - [{inv['id']}] {inv['title']}")

    if pending:
        print("\nUp next (by priority):")
        for inv in sorted(pending, key=lambda x: x['priority'])[:3]:
            print(f"  - [{inv['id']}] {inv['title']} (priority {inv['priority']})")

    # Knowledge graph
    concepts = [n for n in graph['nodes'] if n['type'] == 'concept']
    questions = [n for n in graph['nodes'] if n['type'] == 'question']
    open_questions = [q for q in questions if q.get('status') == 'open']

    print(f"\nKnowledge graph: {len(concepts)} concepts, {len(questions)} questions ({len(open_questions)} open)")
    print(f"Connections: {len(graph['edges'])}")

    # Most curious about
    if concepts:
        top_curious = sorted(concepts, key=lambda x: x.get('curiosity_level', 0), reverse=True)[:3]
        print("\nMost curious about:")
        for c in top_curious:
            print(f"  - {c['name']} (curiosity: {c.get('curiosity_level', '?')}, understanding: {c.get('understanding_level', '?')})")

    print()


def generate_prompt():
    """Generate a self-prompt for the next exploration."""
    next_inv = get_next_investigation()

    if not next_inv:
        return "All investigations complete! Time to add new questions."

    prompt = f"""
=== EXPLORATION PROMPT ===

Investigation: {next_inv['title']}
ID: {next_inv['id']}

Description: {next_inv['description']}
"""

    if next_inv.get('hypothesis'):
        prompt += f"\nHypothesis to test: {next_inv['hypothesis']}"

    if next_inv.get('expected_insights'):
        prompt += "\n\nQuestions to answer:"
        for q in next_inv['expected_insights']:
            prompt += f"\n  - {q}"

    prompt += """

=== INSTRUCTIONS ===
1. Run relevant simulations/analyses
2. Record observations
3. Note surprises or unexpected findings
4. Update hypotheses based on evidence
5. Add new questions that arise
6. Document findings before marking complete
"""

    return prompt


if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_status()
        print("\nUsage:")
        print("  python explorer.py status     - Show current status")
        print("  python explorer.py next       - Get next investigation prompt")
        print("  python explorer.py start ID   - Start an investigation")
        print("  python explorer.py add        - Add new investigation (interactive)")
        sys.exit(0)

    command = sys.argv[1]

    if command == 'status':
        show_status()
    elif command == 'next':
        print(generate_prompt())
    elif command == 'start' and len(sys.argv) > 2:
        start_investigation(sys.argv[2])
        print(f"Started investigation {sys.argv[2]}")
    else:
        print(f"Unknown command: {command}")
