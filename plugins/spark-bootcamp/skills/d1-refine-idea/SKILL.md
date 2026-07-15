---
name: Refine Your Idea
description: Sharpen a raw idea into one testable problem hypothesis and name the single assumption that, if wrong, kills it. The first thing you do on Day 1.
when_to_use: Day 1 discovery, first skill of the week, before you define who to interview. Run once, at the start.
---

# Refine Your Idea

**What this does.** Turns "I have an idea" into "here is the problem I believe exists, for whom, and the one assumption that, if wrong, kills it".
**Why it matters.** An idea is a solution in disguise; underneath is a bet that a specific person has a specific problem worth paying to solve, so name the bet now and the whole week has something real to aim at.
**You are ready for this when.** `.spark/state.json` exists with its `idea` field filled. If empty, run `start` first.

## Before you start
Read state: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" --read`. Take `founder`, `business_type`, `idea`. You are naming the problem and the riskiest bet, not designing the product. That is Day 3.

## Steps
1. Restate the idea as a problem, not a product: "I believe [specific person] struggles to [specific job] because [specific reason], and today they [current workaround]." No features. If you cannot name the person, that is your first finding.
2. Name the person precisely. Not "small businesses" but "the office manager at a 15-person Jersey trust company who reconciles client payments by hand". Narrow beats broad; you can widen later.
3. State the pain as something they already feel, evidenced by a current workaround (a spreadsheet, a late night, a task they dread). No workaround, no real pain: flag it.
4. List every assumption the idea rests on. At least five, push to eight. Cover: the problem is felt often; these people are reachable and will talk; they would pay (roughly how much); you can deliver a fix in your time and skill. Each must be provably true or false.
5. Rank by risk. Score each 1 to 5 for damage if wrong (5 = idea dies) and uncertainty (5 = you do not know). Multiply. Highest is riskiest. Ties break to what a conversation can test this week.
6. Flag the single riskiest assumption at the top, with a one-line kill condition: what you would have to hear in interviews to abandon the idea. Cannot state one? Rewrite until you can.
7. Confirm `business_type` is `software`, `hardware` or `services` and matches how you would deliver a first fix. If empty or wrong, set it now (every build skill from Day 3 branches on it) and note why in DECISIONS.md.

## The artefact
Writes `01-discovery/idea-brief.md` in Markdown, four sections in order:
1. **Problem hypothesis.** The sentence from step 1, plus the precise person and current workaround.
2. **Assumptions, ranked.** Table: assumption, damage (1-5), uncertainty (1-5), score, sorted highest first. At least five rows.
3. **Riskiest assumption.** The top row restated with its kill condition: "I abandon or pivot if I hear ___ in interviews."
4. **Path.** The `business_type` and one line on why it fits.

A stranger should read it and tell you in ten seconds who the customer is, what hurts, and the one thing you are about to check. No solution.

## Done when
- Exactly one problem hypothesis sentence naming a specific person.
- At least five assumptions, each with damage, uncertainty and computed risk score, sorted highest first.
- The single riskiest assumption flagged at the top of its section with a written kill condition.

## Log it
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill d1-refine-idea \
  --artefact 01-discovery/idea-brief.md \
  --result "1 hypothesis, N assumptions ranked, riskiest flagged"
```
Set Day 1 progress and confirm the path (N is your real count):
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
  --patch '{"business_type":"services","days":{"1":{"target":"Prove or kill the riskiest assumption","outcome":"idea-brief written"}}}'
```
If you set or changed `business_type`, log the decision:
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --decision "Chose the services path" \
  --rationale "Founder already delivers this as advisory hours; fastest route to a first sale"
```

## If it goes wrong
Cannot name a specific person? Do not fudge it. Write the brief with the person left blank and the top assumption set to "a specific group of people actually has this problem", then let Day 1 interviews find who. If `idea` is empty, stop and run `start`.
