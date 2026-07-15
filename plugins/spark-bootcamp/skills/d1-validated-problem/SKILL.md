---
name: Validate The Problem
description: Make the persevere-or-pivot call from your interviews, then lock a one-sentence problem and a named segment. Use at the end of Day 1 once discovery-findings.md exists.
when_to_use: Day 1 discovery, the last step of the day, straight after you have synthesised your interviews into discovery-findings.md and before Day 2 market work.
---

# Validate The Problem

**What this does.** Reads your interview synthesis and forces an explicit verdict: persevere, pivot, or insufficient evidence. Then it writes a one-sentence problem and a named segment you will build the rest of the week on.
**Why it matters.** This is the most important decision of the week. Everything after Day 1, the market map, the proposition, the thing you ship, points at whatever you decide here. Founders who skip this call carry a fuzzy problem into Day 5 and cannot close. Decide now, on the evidence, in writing.
**You are ready for this when.** `01-discovery/discovery-findings.md` exists.

## Before you start
Read `01-discovery/discovery-findings.md` and `01-discovery/interview-target-spec.md`. You also need the raw count of interviews you actually completed. Count only solid ones: a real person in your segment who gave you specific, first-hand answers. A five-minute chat with a mate does not count. The bar is in `references/interview-quality-bar.md`.

Guardrail: you are not allowed to talk yourself into a yes. The verdict follows the evidence, not your hopes. If the number of solid interviews is below 5, the answer is decided for you: insufficient evidence.

## Steps
1. Count your solid interviews against the bar in `references/interview-quality-bar.md`. Write the number down. Be honest: warm, agreeable answers from people who would never pay do not count.
2. If you have fewer than 5 solid interviews, stop and record INSUFFICIENT EVIDENCE. Do not pivot, do not persevere. You do not have enough to decide. Keep interviewing into Tuesday morning. If your own network is dry, the Digital Jersey shared interviewee pool is your backup: it exists exactly for this. Aim to reach 5 solid interviews before you make the call.
3. If you have 5 or more, score the problem on three tests, each a plain yes or no. Frequency: does the pain hit at least weekly, or is it a once-a-year annoyance? Intensity: do people already spend money, time or workarounds on it today? Consistency: did the same problem surface in at least 60 percent of your solid interviews (for example 6 of 10)? Write the count for each.
4. Make the call. Three yeses, and the dominant problem is clearly the same one across interviews: PERSEVERE. Problem is real but it is not the one you set out to test, or the segment that feels it most is not the one you targeted: PIVOT, and reframe. Fewer than two yeses, or the pain is mild and occasional: this is a weak problem, treat it as a pivot signal and reframe to the sharper problem your interviews actually revealed.
5. Write the problem as one sentence, in the customer's words, not yours. Format: "[Segment] struggle to [do a specific job] because [specific reason], which costs them [time, money or risk]." No product in the sentence. No solution. Just the problem.
6. Name the segment precisely: who they are, where they work, and the one trait that makes them feel this problem more than anyone else. This is the segment you will hunt for the rest of the week, so make it findable in Jersey.
7. Record the decision and its rationale in DECISIONS.md. State which verdict, the three test scores, and one line on why. A future you, on Thursday, needs to know why you chose this.

## The artefact
Writes two files.
`01-discovery/validated-problem.md`: the one-sentence problem, the verdict (PERSEVERE, PIVOT or INSUFFICIENT EVIDENCE), the three test scores with counts, and the number of solid interviews behind it.
`01-discovery/target-segment.md`: the named segment, where to find them in Jersey, and the one distinguishing trait.

Good looks like a problem sentence a stranger could read and instantly picture the person who has it, backed by a number.

## Done when
`01-discovery/validated-problem.md` holds a single-sentence problem and one of the three verdicts. `01-discovery/target-segment.md` names one segment. DECISIONS.md has one dated decision line with the three test scores. If the verdict is INSUFFICIENT EVIDENCE, the done-condition is instead: the count is recorded and a plan to reach 5 solid interviews is written.

## Log it
Append one line to CHANGELOG.md via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: date, skill id `d1-validated-problem`, artefact path `01-discovery/validated-problem.md`, and the numeric result (solid interview count). Then update state via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`: set days.1 outcome to the verdict and mark days.1 complete only if the verdict is PERSEVERE or PIVOT. Also append the go/pivot/insufficient decision with its rationale to DECISIONS.md.

## If it goes wrong
If you are stuck between persevere and pivot, default to the version of the problem the most people described in the most specific terms, and note the doubt in DECISIONS.md so Day 2 can test it. If you cannot reach 5 solid interviews by Tuesday midday even with the Digital Jersey pool, narrow the segment: a tighter segment is easier to reach and easier to sell to. Do not proceed to Day 2 on fewer than 5 solid interviews. Guessing the problem is the one mistake this whole week cannot recover from.
