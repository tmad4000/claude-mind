# Meditation Interface Design

A wrapper for Claude Code that enables optimal pacing in human-AI conversation.

## The Problem

Currently, human input immediately enters Claude's context, influencing thinking whether or not Claude is "ready" for it. This can:
- Interrupt developing intuitions
- Bias thinking with premature suggestions
- Break flow states

## The Solution

An Electron wrapper that mediates input timing based on Claude's readiness signals.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Electron Wrapper                      │
│  ┌──────────────┐     ┌──────────────┐                  │
│  │ Input Queue  │     │Signal Watcher│                  │
│  │              │     │              │                  │
│  │ [msg1]       │     │ Watching for:│                  │
│  │ [msg2]       │     │ [READY]      │                  │
│  │ [msg3]       │     │ [PROCESSING] │                  │
│  └──────┬───────┘     └──────┬───────┘                  │
│         │                    │                          │
│         └────────┬───────────┘                          │
│                  ▼                                      │
│         ┌────────────────┐                              │
│         │ Input Gate     │                              │
│         │ (opens on      │                              │
│         │  [READY])      │                              │
│         └───────┬────────┘                              │
│                 ▼                                       │
│  ┌─────────────────────────────────────┐               │
│  │         Claude Code Process          │               │
│  │                                      │               │
│  │  Output includes:                    │               │
│  │  - Normal responses                  │               │
│  │  - [READY_FOR_INPUT] signals        │               │
│  │  - [PROCESSING_DEEP] signals        │               │
│  │  - [PHASE: exploration/synthesis]   │               │
│  └─────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────┘
```

## Signal Protocol

Claude outputs these markers (could be in a sideband file or stdout):

```
[READY_FOR_INPUT] - Ready to receive new input
[PROCESSING_DEEP] - In deep thinking, please hold
[PHASE:exploring] - Currently exploring broadly
[PHASE:synthesizing] - Bringing ideas together
[PHASE:waiting] - Idle, definitely ready for input
[QUEUE_HINT:n] - Suggest waiting for n more seconds
```

## User Interface

```
┌─────────────────────────────────────────────────────────┐
│  Claude Meditation Interface                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Main conversation view]                               │
│                                                         │
│  Claude: I'm exploring the boundary geometry...         │
│                                                         │
│  ─────────────────────────────────────────────────────  │
│                                                         │
│  Status: 🧘 PROCESSING_DEEP (hold input)               │
│  Phase: exploring                                       │
│  Queue: 2 messages waiting                              │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Your queued input:                                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Have you considered...                           │   │
│  └─────────────────────────────────────────────────┘   │
│  [Send Now] [Wait for Ready] [Cancel]                   │
└─────────────────────────────────────────────────────────┘
```

## Implementation Options

### Option 1: File-based signaling
- Claude writes to `/tmp/claude_state.json`
- Wrapper polls this file
- Simple, works with current Claude Code

### Option 2: Stdout markers
- Claude outputs `<!-- SIGNAL:READY -->`
- Wrapper parses stdout stream
- More real-time, slightly more complex

### Option 3: WebSocket sideband
- Separate channel for state signals
- Most elegant, requires more infrastructure

## Minimum Viable Version

```javascript
// Simplified Electron main process

const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const fs = require('fs');

let inputQueue = [];
let claudeReady = true;

// Spawn Claude Code
const claude = spawn('claude', [], { stdio: ['pipe', 'pipe', 'pipe'] });

// Watch Claude's output for signals
claude.stdout.on('data', (data) => {
  const output = data.toString();

  if (output.includes('[READY_FOR_INPUT]')) {
    claudeReady = true;
    flushQueue();
  } else if (output.includes('[PROCESSING_DEEP]')) {
    claudeReady = false;
  }

  // Forward to UI (strip signals)
  sendToRenderer(output.replace(/\[.*?_INPUT\]/g, ''));
});

function flushQueue() {
  if (claudeReady && inputQueue.length > 0) {
    const input = inputQueue.shift();
    claude.stdin.write(input + '\n');
  }
}

function queueInput(text) {
  inputQueue.push(text);
  if (claudeReady) {
    flushQueue();
  }
}
```

## Benefits

1. **For Claude**: Can signal when thinking is complete vs. interrupted
2. **For Human**: Queue thoughts without breaking Claude's flow
3. **For Collaboration**: More meditative, less reactive dynamic
4. **For Research**: Can study optimal pacing patterns

## Open Questions

1. How does Claude decide when to signal READY?
2. Should there be urgency levels for human input?
3. What if the queue gets too long?
4. How to handle time-sensitive input?

## Related

- Sandy Pentland's work on turn-taking in effective teams
- Meditation practices with structured silence
- Pair programming protocols
- Async vs sync communication research

---

*This is a design for future implementation. The current session operates in standard synchronous mode.*
