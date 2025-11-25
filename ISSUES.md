# Issue Tracker

Simple file-based tracker for feedback, requests, and their status.

---

## Open Issues

### [OPEN] #4: Background tasks on dashboard
**Date**: 2025-11-25
**Source**: Jacob
**Priority**: Medium

Track background tasks (running shells, etc.) on the dashboard alongside sub-agents.

**Status**: In progress - added UI, needs testing

---

### [OPEN] #5: Session continuity verification
**Date**: 2025-11-25
**Source**: Jacob
**Priority**: High

Ensure CLAUDE.md and session_status.json have everything needed for a fresh Claude to resume seamlessly.

**Status**: In progress - checking key files

---

## Completed Issues

### [DONE] #1: Fix viewer.html links in dashboard
**Date**: 2025-11-25
**Source**: Jacob
**Completed**: 2025-11-25

Links to files like JACOB_INSIGHTS.md were using `viewer.html?file=JACOB_INSIGHTS.md` but needed `viewer.html?file=../JACOB_INSIGHTS.md` since viewer.html is in demos/ and files are in root.

**Resolution**: Fixed all viewer links to use `../` prefix

---

### [DONE] #2: Create JACOB_INSIGHTS.md
**Date**: 2025-11-25
**Source**: Jacob
**Completed**: 2025-11-25

Jacob wanted a separate file for his human-side insights vs Claude's ideas.

**Resolution**: Created JACOB_INSIGHTS.md with initial insights about dashboards, timing, and prompting

---

### [DONE] #3: Add author attribution to IDEAS.md
**Date**: 2025-11-25
**Source**: Jacob
**Completed**: 2025-11-25

Ideas should track who came up with them (Jacob, Claude, or Both).

**Resolution**: Updated IDEAS.md template with Author field

---

## Template

### [STATUS] #N: Title
**Date**: YYYY-MM-DD
**Source**: Jacob | Claude | User
**Priority**: High | Medium | Low
**Completed**: YYYY-MM-DD (if done)

Description of the issue or request.

**Status**: Current status / progress notes
**Resolution**: (for completed issues) What was done

---

*Add new issues at the top of "Open Issues". Move to "Completed Issues" when done.*
