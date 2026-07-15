---
name: Business Profile
description: The single source of truth for how the three business paths differ each day. Build and ship skills read it to branch consistently.
when_to_use: Read internally by any Day 1 to Day 5 skill that branches on business_type. Not run by the founder.
user-invocable: false
---

# Business Profile

**What this does.** Holds the one variance matrix for the three paths (software, hardware, services) so every build and ship skill branches from a single table.
**Why it matters.** One table read by every day skill keeps the week coherent: change the definition of done in one place and the whole week follows.
**You are ready for this when.** You are a build or ship skill that has read `.spark/state.json` and found `business_type`.

## Before you start
Read `.spark/state.json` via the journey-state helper and take `business_type` (`"software"`, `"hardware"` or `"services"`). The shared spine: by Day 5 the founder has a live page a real prospect can act on. The matrix tells you what that page is and what counts as done each day, per path. Do not re-decide it.

## Steps
1. Resolve `business_type` from state. If missing or not one of the three, stop and send the founder to Day 1 discovery. Do not assume a default.
2. Open `${CLAUDE_SKILL_DIR}/references/variance-matrix.md`.
3. Read the cell for your day (1 to 5) under the founder's path. That cell is the authority on "done"; Day 5 names the exact live page.
4. Build your day skill's artefact shaped to that path's definition of done.
5. If your day skill and the matrix disagree, the matrix wins. Fix the day skill, do not fork the definition.

## The artefact
None. The only file it owns is `${CLAUDE_SKILL_DIR}/references/variance-matrix.md`: one row per day, three columns, stating "done" and the live page for each path.

## Done when
The calling skill has read the correct cell (current day, founder's `business_type` column) and has one unambiguous definition of done. One cell, not three.

## Log it
Nothing to log. This skill produces no artefact. The calling day skill logs when its own artefact lands.

## If it goes wrong
If `business_type` is missing or malformed, or the matrix has no cell for the day and path, do not guess. Fall back to the software column for structure only, flag clearly that the path was not set, and point the founder back to Day 1 discovery.
