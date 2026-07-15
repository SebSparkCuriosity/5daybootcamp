---
name: Business Profile
description: The single source of truth for how the three business paths differ each day. Build and ship skills read this to branch, so no two skills disagree about what "done" means.
when_to_use: Read internally by any Day 1 to Day 5 skill that must branch on business_type. Not run directly by the founder.
user-invocable: false
---

# Business Profile

**What this does.** Holds the one variance matrix for the three business paths (software, hardware, services) so every build and ship skill branches from a single table instead of each guessing on its own.
**Why it matters.** The bootcamp runs three kinds of business through one five-day spine. If each day skill invents its own idea of what "done" looks like for hardware versus services, they drift and contradict each other. One table, read by all of them, keeps the week coherent. Change the definition of done in one place and the whole week follows.
**You are ready for this when.** You are a build or ship skill that has read `.spark/state.json` and found `business_type`. This skill produces no artefact of its own.

## Before you start
Read `.spark/state.json` (via the journey-state helper) and take the `business_type` field: `"software"`, `"hardware"` or `"services"`. Then open `references/variance-matrix.md` in this skill directory (`${CLAUDE_SKILL_DIR}/references/variance-matrix.md`). Find the row for the current day and read down the column for that business type.

The shared spine across all three paths is one idea: by Day 5 the founder has a live page a real prospect can act on. The matrix tells you what that page is, and what counts as done each day, for each path. Do not re-decide it. Read it here.

## Steps
1. Resolve `business_type` from state. If it is missing or not one of the three values, stop and tell the founder to complete Day 1 discovery first, where the type is set. Do not assume a default.
2. Open `${CLAUDE_SKILL_DIR}/references/variance-matrix.md`.
3. Find the row for the day you are working (1 to 5) and read the cell under the founder's path. That cell is the authority on what "done" means for that day, and Day 5 names the exact live page.
4. Apply it. Build the artefact your own day skill defines, shaped to that path's definition of done.
5. If your day skill and this matrix disagree, the matrix wins. Fix your day skill or raise it, do not fork the definition.

## The artefact
None. This skill is a shared reference. The only file it owns is `${CLAUDE_SKILL_DIR}/references/variance-matrix.md`: a table with one row per day and three columns (software, hardware, services), stating what "done" means for each path each day, and what the "live page a real prospect can act on" is for each.

## Done when
The calling skill has read the correct cell: the current day's row under the founder's `business_type` column, and has a single, unambiguous definition of done to build against. One cell, not three.

## Log it
Nothing to log. This skill produces no artefact and writes neither CHANGELOG.md nor `.spark/state.json`. The day skill that called it does the logging when its own artefact lands.

## If it goes wrong
If `business_type` is missing, malformed, or the matrix has no cell for the day and path, do not guess. Fall back to the software column as the most fully specified path only for structure, flag clearly to the founder that the path was not set, and point them back to Day 1 discovery to fix it. A wrong path chosen silently is worse than a paused day.
