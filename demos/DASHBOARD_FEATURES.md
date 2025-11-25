# Status Dashboard Features

Documentation for the Claude Mind Status Dashboard (`status_dashboard.html`).

## Quick Start

```bash
cd /path/to/claude-mind
python3 -m http.server 8080
# Open http://localhost:8080/demos/status_dashboard.html
```

## Features

### Header

| Feature | Description |
|---------|-------------|
| **LIVE indicator** | Green pulsing badge showing dashboard is active |
| **Current time** | Real-time clock with timezone (updates every 1s) |
| **Claude Status** | Shows processing/idle/waiting state with colored indicator |
| **Last fetch** | Shows seconds since last data fetch (green if <10s, red if stale) |

### Main Panels

#### What's Happening Now
- Shows the current active task Claude is working on
- Updates every 2 seconds from `current_task` in session_status.json
- Displays description, details, start time, and current step

#### Active Threads
- List of ongoing work threads
- Color-coded by status: green (in_progress), yellow (pending), blue (completed)
- Shows progress bars, subtasks, agent tags

#### Pending Questions
- Questions waiting for resolution
- Priority indicators (high/medium)

#### Sub-Agents
- Shows spawned sub-agents and their status
- Collapsible section

#### Recent Completions
- Timeline of recently finished work
- Collapsible section

### Right Column

#### Current Direction
- Focus, rationale, next steps, open questions

#### Key Facts
- Important learnings from the session

#### Working Assumptions (collapsible)
- Current operating assumptions

#### Domain Knowledge (collapsible)
- Status by domain (CA, RD, philosophy, meta-tools)

### Bottom Row

#### Cool Artifacts
- Links to interactive demos
- Phase Diagram, RD Explorer, CA Explorer, Conversation Map

#### Key Files
- Organized file tree with categories
- Featured badges for important files (START HERE, OVERVIEW, etc.)
- GitHub links for each file
- Uses viewer.html for pretty rendering

#### Meta State (collapsible)
- Exploration mode, confidence, energy level
- Last surprise, tools needed

### Activity Feed (Sidebar)

| Feature | Description |
|---------|-------------|
| **Toggle button** | Top-right "Activity" button |
| **Unread badge** | Red pulsing count of unread items |
| **Activity types** | task (green), update (blue), discovery (yellow), question (red) |
| **Mark all read** | Button to clear unread state |
| **Persistence** | Read state saved to localStorage |

## Data Source

All data comes from `data/session_status.json`. The dashboard polls this file every 2 seconds.

### JSON Structure

```json
{
  "session_id": "string",
  "timestamp": "ISO8601",
  "claude_status": "processing|idle|waiting",
  "current_task": {
    "description": "string",
    "details": "string",
    "started": "ISO8601",
    "step": "string"
  },
  "activity_feed": [
    {
      "id": "string",
      "timestamp": "ISO8601",
      "type": "task|update|discovery|question",
      "message": "string"
    }
  ],
  "active_threads": [...],
  "pending_questions": [...],
  "recent_completions": [...],
  "current_direction": {...},
  "implicit_context": {...},
  "meta_state": {...},
  "sub_agents": [...],
  "system_info": {...}
}
```

## Updating Status

To update what the dashboard shows, modify `data/session_status.json`:

1. **Claude status**: Set `claude_status` to "processing", "idle", or "waiting"
2. **Current task**: Update `current_task` object
3. **Activity**: Prepend new items to `activity_feed` array
4. **Threads**: Update `active_threads` array

The dashboard will pick up changes within 2 seconds.

## Related Files

- `data/session_status.json` - Data source
- `viewer.html` - Pretty file viewer (markdown/code)
- `conversation_map.html` - Thread visualization
- `DASHBOARD_FEATURES.md` - This file

---

*Last updated: 2025-11-25*
