---
name: Prioritise The Feedback
description: Turns product-test sessions into one ranked change list and one ranked buyer list, so Friday builds the right three fixes and calls the warmest people first.
when_to_use: Day 4 GTM, after the product-test sessions. Between synthesise-interviews (product-test) and Day 5 selling.
---

# Prioritise The Feedback

**What this does.** Scores every requested change with RICE and MoSCoW, and ranks every tester by likelihood to buy.
**Why it matters.** By Friday you can build three things not thirty and phone a handful of people, so numbers decide, not the loudest voice.
**You are ready for this when.** `04-gtm/tests/sessions/` holds at least one session file from run-interview.

## Before you start
Read: `04-gtm/product-test-findings.md` (cross-session synthesis), `04-gtm/tests/sessions/*.md` (one per tester), `04-gtm/captures.jsonl` (live-page hand-raisers, treat as warmest), and `.spark/state.json` for `business_type` and name.
No capture store yet: carry on with sessions alone and note it. Do not invent enquiries.
Guardrail: this skill only reads and scores. Outreach happens Day 5 after your sign-off.

## Steps
1. Pull every distinct change request from the sessions, one per line, merge duplicates, keep a count (frequency feeds Reach).
2. Score each change with RICE. Reach: testers plus enquirers it touches (real count). Impact: 3 massive, 2 high, 1 medium, 0.5 low, 0.25 minimal. Confidence: % sure (100 watched it, 80 one clear account, 50 hunch; never round up). Effort: person-days. Score = (Reach x Impact x Confidence) / Effort.
3. Tag each change MoSCoW: Must (sale dies without it), Should (strong pull), Could (later), Won't (parked, written down).
4. Flag the top 3 by RICE, breaking ties for Must over Should. Read the three to the founder with the numbers behind them and ask "does this match what you watched?" A founder who sat in every session may overrule one, reason logged in DECISIONS.md. Those are Friday's build list.
5. Score each tester 0-3 on Pain, Budget, Timing, Pull, total out of 12. Capture-store people start top of the warmth order.
6. Run the scorer to do the arithmetic and write both files:
   `python3 ${CLAUDE_SKILL_DIR}/scripts/score.py --project .`
   It reads a YAML block you fill in (template prints on first run); falls back to key:value without PyYAML.

Worked example, MoSCoW definitions and tie-break rules: `${CLAUDE_SKILL_DIR}/references/scoring-guide.md`.

## The artefact
- `04-gtm/feedback-synthesis.md`: every change with Reach, Impact, Confidence, Effort, RICE and MoSCoW, sorted highest RICE first, top 3 flagged **BUILD FRIDAY**. Opening paragraph names the single clearest signal.
- `04-gtm/buying-signal-scorecard.csv`: one row per tester with four scores, total out of 12, warmth band (Hot 9-12, Warm 5-8, Cool 0-4), a "from live page" flag and rank, hottest first.

## Done when
- Every change has all four RICE inputs, a RICE score and a MoSCoW tag. No blanks.
- Exactly 3 changes carry **BUILD FRIDAY**.
- Every tester appears with a total out of 12 and a rank, sorted hottest first.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d4-prioritise \
  --artefact 04-gtm/feedback-synthesis.md \
  --result "<N> changes scored, top 3 flagged, <M> testers ranked"
```
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"4":{"outcome":"Feedback prioritised: 3 fixes chosen for Friday, <M> testers ranked by buying intent"}}}'
```
If a rationale drove a close call, add a line to DECISIONS.md.

## If it goes wrong
- **One or two sessions.** RICE still works, Confidence drops. Score honestly and note the build list is provisional.
- **Three-way tie.** Break with MoSCoW, then Effort: ship the cheapest so Friday has slack.
- **No captures, thin signals.** Rank on Pain and Timing, band Cool or Warm, treat Day 5 as a warm-up. Say so in the synthesis.
