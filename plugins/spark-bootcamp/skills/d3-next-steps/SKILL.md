---
name: Plan Next Steps
description: Turn the messy end of Day 3 into an honest, ranked launch checklist that names your top 3 blockers. Use after the build slice and landing page exist.
when_to_use: Day 3, at the end of build, after d3-build and the landing page are up. The last thing you do before Day 4 go-to-market.
---

# Plan Next Steps

**What this does.** Lists every open item between you and a paying customer, ranks them, and marks the top 3 as blockers so you know exactly what to fix first.
**Why it matters.** By the end of Day 3 you have a half-built thing and a head full of loose ends. Founders lose Day 4 to the wrong task: polishing a button while the payment link is broken. A ranked list, with the three real blockers named, is the difference between shipping on Friday and drifting.
**You are ready for this when.** `03-product/BUILD-LOG.md` and `03-product/requirements-moscow.md` both exist, and your landing page is live or nearly live.

## Before you start
Read these, in this order:
- `03-product/BUILD-LOG.md`: what you actually built today and what you skipped.
- `03-product/requirements-moscow.md`: the Must, Should, Could, Won't list. Anything Must that is not done is a candidate blocker.
- Your landing site status: is the URL live? Does the call to action work? Does it take a real payment intent or booking?
- `.spark/state.json`: the day 3 target, so you rank against the outcome you promised, not against a wish list.

No money is spent and nothing is sent here. This skill only plans. The pause for sign-off comes on Day 4.

## Steps
1. **Dump every open item.** Read the three inputs and write down everything still undone. Do not rank yet. Include half-finished features, an untested payment link, a missing privacy note, a logo that looks wrong. Aim for a full list, 10 to 25 items is normal.
2. **Score each item on two axes, 1 to 3.** Impact: does it stand between you and a customer paying (3), does it help (2), or is it polish (1)? Effort: quick under an hour (1), half a day (2), a day or more (3). Write both numbers next to each item. Use `${CLAUDE_SKILL_DIR}/scripts/rank.py` to sort them if you want the arithmetic done for you.
3. **Rank by priority.** Priority is impact first, then lowest effort as the tie-breaker. High impact and low effort goes to the top. Low impact and high effort sinks. Every item gets a rank number, no ties.
4. **Name the top 3 blockers.** A blocker is an item that, if left undone, means a prospect physically cannot pay or book. Mark exactly three. Not five, not one. If you have fewer than three true blockers, say so plainly and note you are ahead. If you have more than three, the extra ones are urgent but not blockers, and you must still choose the three that come first.
5. **Sanity-check against the day 3 target.** Look at the outcome you promised in state.json. Do the top 3 blockers, once cleared, deliver it? If not, your ranking is wrong. Fix it.
6. **Write one line per blocker on how you clear it tomorrow.** Concrete. "Test the Stripe link with a 1 pound charge and refund it" beats "sort out payments".
7. **Record the call in DECISIONS.md.** Log why these three are the blockers and what you consciously chose to leave undone (the Won't-for-now list matters as much as the To-do list).

## The artefact
Writes `03-product/NEXT-STEPS.md` in Markdown. Use `${CLAUDE_SKILL_DIR}/references/next-steps-template.md` as the shape.

What good looks like:
- A single ranked table: rank, item, impact, effort, blocker (yes or no).
- Exactly 3 items flagged as blockers, each with a one-line plan to clear it.
- A short "leaving undone on purpose" note listing what you are consciously skipping and why.
- A count at the top: total open items, and how many are blockers.

## Done when
Every open item has a rank (no unranked items), exactly 3 are marked as blockers with a one-line clearing plan each, and DECISIONS.md carries the rationale. Observable check: the table row count equals your open-item count, and the blocker column reads "yes" exactly 3 times.

## Log it
Append one line to `CHANGELOG.md` via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: date, `d3-next-steps`, the artefact path, and the numeric result (open items ranked, 3 blockers named). Then update `.spark/state.json` through `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`: set the day 3 outcome and mark day 3 complete if the target is met.

## If it goes wrong
If you cannot get the list below 25 items, you are mixing the launch with the roadmap. Cut anything that is not needed to take one payment from one customer this week. Park the rest in a "later" heading, unranked, out of scope. If you genuinely cannot name 3 blockers because too much is broken, that is the finding: the day 3 target was too big. Note it in DECISIONS.md, pick the 3 that unblock a single sale, and carry the rest into Day 4 honestly.
