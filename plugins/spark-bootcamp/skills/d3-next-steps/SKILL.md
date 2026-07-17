---
name: Plan Next Steps
description: Turn the messy end of Day 3 into a ranked launch checklist that names your top 3 blockers. Use after the build slice and landing page exist.
when_to_use: End of Day 3, after d3-mvp-build and the landing page. Last thing before Day 4.
---

# Plan Next Steps

**What this does.** Lists every open item between you and a paying customer, ranks them, and marks the top 3 blockers.
**Why it matters.** A ranked list with the three real blockers named is the difference between shipping on Friday and drifting into the wrong task.
**You are ready for this when.** `03-product/BUILD-LOG.md` and `03-product/requirements-moscow.md` both exist and your landing page is live or nearly live.

## Before you start
Read, in order: `03-product/BUILD-LOG.md` (built and skipped today), `03-product/requirements-moscow.md` (any undone Must is a candidate blocker), landing site status (URL live? CTA works? takes real payment intent or booking?), `.spark/state.json` (the day 3 target). This skill only plans. No money spent, nothing sent.

## Steps
1. **Dump every open item.** From the three inputs, list everything undone. Don't rank yet. 10 to 25 items is normal.
2. **Score each 1 to 3 on two axes.** Impact: blocks a sale (3), helps (2), polish (1). Effort: under an hour (1), half a day (2), a day or more (3). Run `${CLAUDE_SKILL_DIR}/scripts/rank.py` to sort.
3. **Rank by priority.** Impact first, lowest effort as tie-breaker. Every item gets a rank number, no ties.
4. **Name the top 3 blockers with the founder.** Present your three with the scores, then let them confirm or swap (a swap against the numbers gets its reason in DECISIONS.md). A blocker means a prospect cannot pay or book. Mark exactly three. Fewer: say so, you are ahead. More: the extras are urgent but not blockers.
5. **Sanity-check against the day 3 target.** If clearing the top 3 does not deliver the promised outcome, your ranking is wrong. Fix it.
6. **Write one line per blocker on how you clear it tomorrow.** Concrete: "Test the Stripe link with a 1 pound charge and refund it".
7. **Record the call in DECISIONS.md.** Why these three, and what you consciously leave undone.

## The artefact
Writes `03-product/NEXT-STEPS.md` in Markdown, shaped by `${CLAUDE_SKILL_DIR}/references/next-steps-template.md`. Good: one ranked table (rank, item, impact, effort, blocker yes/no); exactly 3 blockers each with a one-line plan; a "leaving undone on purpose" note; a count of total items and blockers at the top.

## Done when
Every item ranked (none unranked), exactly 3 marked as blockers with a clearing plan each, and DECISIONS.md carries the rationale. The blocker column reads "yes" exactly 3 times.

## Log it
Append one line to `CHANGELOG.md` via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: date, `d3-next-steps`, artefact path, numeric result (open items ranked, 3 blockers named). Then set the day 3 outcome and completion via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`.

## If it goes wrong
Over 25 items means you are mixing launch with roadmap: cut anything not needed to take one payment this week, park the rest under a "later" heading, unranked. If you cannot name 3 blockers because too much is broken, that is the finding: the day 3 target was too big. Note it in DECISIONS.md, pick the 3 that unblock a single sale, carry the rest into Day 4.
