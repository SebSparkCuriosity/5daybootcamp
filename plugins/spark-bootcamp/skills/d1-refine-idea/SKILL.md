---
name: Refine Your Idea
description: Sharpens a raw idea into one testable problem hypothesis and names the single assumption that, if wrong, kills it. The first thing you do on Day 1.
when_to_use: Day 1 discovery, the very first skill of the week, before you define who to interview or build any contact list. Run it once, at the start.
---

# Refine Your Idea

**What this does.** Turns "I have an idea" into "here is the problem I believe exists, for whom, and the one assumption that, if wrong, kills the whole thing".
**Why it matters.** An idea is a solution wearing a disguise. Underneath it is a bet: that a specific person has a specific problem worth paying to solve. Most first-time founders never say the bet out loud, so they spend the week defending a solution instead of testing a problem. Name the bet now and the rest of the week has something real to aim at.
**You are ready for this when.** `.spark/state.json` exists and its `idea` field is filled. If it is empty, the `start` skill has not run. Run that first.

## Before you start
Read the current state via the journey-state helper:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" --read
```

Take three fields: `founder`, `business_type` and `idea`. The `idea` is your raw material. If it is one line, good. If it is a paragraph of features, that is normal, we will strip it back to a problem.

Guardrail: you are not choosing the solution today. You are naming the problem and the riskiest bet. Resist every urge to design the product. That comes on Day 3.

## Steps
1. **Restate the idea as a problem, not a product.** Write one sentence in this shape: "I believe [specific person] struggles to [do a specific job] because [specific reason], and today they [current workaround]." No product name, no features. If you cannot name the person, that is your first finding: the idea is still a solution looking for a problem.
2. **Name the person precisely.** "Small businesses" is not a person. "The office manager at a 15-person Jersey trust company who reconciles client payments by hand" is. The narrower the better. You can widen later; you cannot test "everyone".
3. **State the pain as something they already feel.** Not a pain you think they should feel. A good problem hypothesis describes a workaround that already exists: a spreadsheet, a late night, a task they dread, a thing they pay too much for. If there is no current workaround, the pain may not be real. Flag that.
4. **List every assumption the idea rests on.** Aim for at least five. Push to eight. An assumption is anything that must be true for the bet to pay off. Cover four kinds: the problem exists and is felt often; these people are reachable and will talk to you; they would pay (and roughly how much); you can actually deliver a fix in the time and skill you have. Write each as a plain statement that could be proven true or false.
5. **Rank them by risk.** For each assumption score two things, 1 to 5: how damaging if it is wrong (5 = the whole idea dies), and how uncertain you are (5 = you genuinely do not know). Multiply the two. The highest score is your riskiest assumption. Ties break towards the one you can test with a conversation this week.
6. **Flag the single riskiest assumption at the top.** One, not three. This is the assumption Day 1 exists to prove or kill. Write one line on how you would know it is wrong: what you would have to hear in interviews to abandon the idea. If you cannot state a kill condition, the assumption is too vague; rewrite it until you can.
7. **Confirm the path.** Check `business_type` in state is one of `software`, `hardware` or `services` and that it matches how you would actually deliver a first fix. If it is empty or wrong, set it now, because every build skill from Day 3 branches on it. Note one line of why in DECISIONS.md (see Log it).

## The artefact
Writes `01-discovery/idea-brief.md` in Markdown, with four sections in this order:

1. **Problem hypothesis.** The single sentence from step 1, plus the precise person (step 2) and the current workaround (step 3).
2. **Assumptions, ranked.** A short table: assumption, damage (1-5), uncertainty (1-5), score (damage x uncertainty), sorted highest score first. At least five rows.
3. **Riskiest assumption.** The top row, restated, with its one-line kill condition: "I abandon or pivot this idea if I hear ___ in interviews."
4. **Path.** The `business_type` and one line on why it fits.

What good looks like: a stranger could read the brief and tell you, in ten seconds, who the customer is, what hurts, and the one thing you are about to go and check. No features. No solution. If the brief describes what you will build, you have written the wrong document.

## Done when
Three conditions, all observable in the file:
- Exactly one problem hypothesis sentence naming a specific person.
- At least five assumptions, each with a damage score, an uncertainty score and a computed risk score, sorted highest first.
- The single riskiest assumption is flagged at the top of its section with a written kill condition.

## Log it
Append one line to CHANGELOG.md and register the artefact via the logbook helper:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill d1-refine-idea \
  --artefact 01-discovery/idea-brief.md \
  --result "1 hypothesis, N assumptions ranked, riskiest flagged"
```

Replace `N` with your real count. Then set Day 1 progress and confirm the path in state:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
  --patch '{"business_type":"services","days":{"1":{"target":"Prove or kill the riskiest assumption","outcome":"idea-brief written"}}}'
```

If you set or changed `business_type`, log the reason as a decision:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --decision "Chose the services path" \
  --rationale "Founder already delivers this as advisory hours; fastest route to a first sale"
```

## If it goes wrong
If you cannot name a specific person in step 2, do not fudge it. That is a real result: the idea is a solution in search of a problem. Write the brief with the person left blank and the top assumption set to "a specific group of people actually has this problem", then let Day 1 interviews find who, if anyone, does. If the `idea` field is empty, stop and run the `start` skill, because there is nothing to refine yet.
