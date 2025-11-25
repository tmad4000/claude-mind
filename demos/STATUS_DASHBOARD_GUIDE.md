# Status Dashboard Guide

## Overview

The Status Dashboard is a real-time interface prototype for monitoring Claude's exploration progress in the claude-mind project. It provides visibility into active work, implicit context, and the current direction of investigation.

## Files

- **Dashboard**: `/demos/status_dashboard.html`
- **Data Source**: `/data/session_status.json`

## Features

### Two-Column Layout

#### Left Column: Active Work
1. **Active Threads**
   - Shows currently running investigations
   - Progress bars for each thread
   - Sub-agent assignments
   - Current focus and subtasks

2. **Pending Questions**
   - Questions awaiting user input or decisions
   - Priority indicators (high/medium/low)
   - Context for each question

3. **Recent Completions**
   - Timeline of finished work
   - Outcomes and significance ratings
   - Links to artifacts produced

#### Right Column: Implicit Context
1. **Current Direction**
   - Overall focus and rationale
   - Next planned steps
   - Open questions

2. **Key Facts**
   - Essential discoveries and observations
   - Domain-specific knowledge
   - Validated findings

3. **Working Assumptions**
   - Methodological principles
   - Heuristics being applied
   - Constraints and boundaries

4. **Domain Knowledge**
   - Status of each research area
   - Key insights per domain
   - Cross-domain connections

### Meta State Panel

Shows the exploration's current "mental state":
- **Exploration Mode**: depth-first, breadth-first, etc.
- **Confidence Level**: how certain the system is
- **Energy Level**: momentum and engagement
- **Curiosity Direction**: what's pulling attention
- **Last Surprise**: most recent unexpected finding
- **Tools Needed**: capabilities that would help

## How to Use

### Basic Usage

1. Open the dashboard in a browser:
   ```bash
   open demos/status_dashboard.html
   ```

2. The dashboard will automatically:
   - Load `session_status.json`
   - Refresh every 30 seconds
   - Update the "LIVE" indicator

3. Click "Refresh" button to manually reload data

### Updating Status Data

To update the dashboard, modify `/data/session_status.json`:

```bash
# Edit the JSON file with current status
vim data/session_status.json

# The dashboard will automatically pick up changes
# within 30 seconds (or click Refresh)
```

### Status JSON Structure

```json
{
  "session_id": "unique_id",
  "timestamp": "ISO 8601 timestamp",
  "active_threads": [
    {
      "id": "thread_id",
      "title": "Thread Name",
      "status": "in_progress|pending|completed",
      "agent": "agent_name",
      "description": "What this thread is doing",
      "current_focus": "Immediate focus",
      "subtasks": ["task1", "task2"],
      "progress": 0-100
    }
  ],
  "pending_questions": [...],
  "recent_completions": [...],
  "current_direction": {...},
  "implicit_context": {...},
  "meta_state": {...}
}
```

## Design Philosophy

This dashboard demonstrates several UI/UX concepts for AI interaction:

1. **Transparency**: Make AI's "thought process" visible
2. **Context Awareness**: Show what the AI "knows" and assumes
3. **Progress Tracking**: Clear indication of what's done/in-progress/pending
4. **Priority Management**: Surface questions and blockers
5. **Meta-Cognition**: Expose the AI's self-assessment

## Use Cases

### For Humans
- Monitor long-running explorations
- Understand AI's current context
- Identify when decisions are needed
- Track progress toward goals
- Review recent discoveries

### For AI Systems
- Maintain continuity across sessions
- Share context between agents
- Coordinate parallel investigations
- Surface blockers and questions
- Document implicit knowledge

### For Collaboration
- Shared understanding of status
- Clear handoff points
- Decision points highlighted
- Progress visibility for stakeholders

## Future Enhancements

Potential improvements for a production system:

1. **Interactive Updates**: Click to expand threads, mark questions as answered
2. **History Tracking**: Time-travel through previous states
3. **Agent Communication**: Show inter-agent messages and coordination
4. **Confidence Visualization**: Heat maps for uncertainty
5. **Dependency Graphs**: Show thread relationships
6. **Resource Monitoring**: Token usage, API calls, computation time
7. **Alert System**: Notify when questions or blockers arise
8. **Export/Share**: Generate status reports
9. **Integration**: Connect to actual Claude API for real-time updates
10. **Multi-Session**: Compare multiple exploration sessions

## Technical Notes

- Pure HTML/CSS/JavaScript (no dependencies)
- Auto-refresh via `setInterval`
- Responsive design (works on mobile)
- Error handling for missing/invalid JSON
- Graceful degradation if data unavailable

## Example Workflow

1. **Start Exploration**: Initialize `session_status.json` with starting state
2. **Update Regularly**: As work progresses, update the JSON file
3. **Monitor Dashboard**: Keep dashboard open to track progress
4. **Answer Questions**: Check "Pending Questions" and provide input
5. **Review Completions**: See what's been accomplished
6. **Adjust Direction**: Use context panel to understand current focus

## Comparison to Existing Tools

| Feature | Status Dashboard | Traditional Logs | Chat Interface |
|---------|------------------|------------------|----------------|
| Real-time | ✓ | ✗ | ~ |
| Structured | ✓ | ✗ | ✗ |
| Context Visible | ✓ | ✗ | ~ |
| Progress Tracking | ✓ | ✗ | ✗ |
| Multi-thread | ✓ | ~ | ✗ |
| Historical | ~ | ✓ | ✓ |

## Philosophy

This is a prototype for **"observable AI"** - making AI systems' internal states, assumptions, and processes visible and understandable to humans. Rather than a black box that produces outputs, we want:

- Transparent reasoning
- Visible context
- Clear priorities
- Explicit uncertainty
- Traceable progress

The goal is to make AI collaboration feel more like working with a thoughtful colleague who shares their thinking, rather than querying an oracle.

---

Created: 2025-11-25
Part of: claude-mind project
Purpose: Better human-AI collaboration interfaces
