---
name: Validate The Problem
description: Make the persevere-or-pivot call from your interviews, then lock a one-sentence problem and a named segment.
when_to_use: End of Day 1, once discovery-findings.md exists, before Day 2 market work.
---

# Validate The Problem

**What this does.** Reads your interview synthesis, forces a verdict (persevere, pivot, or insufficient evidence), then writes a one-sentence problem and a named segment.
**Why it matters.** This is the week's biggest decision: everything after Day 1 points at whatever you lock here, so a fuzzy problem now means you cannot close on Friday.
**You are ready for this when.** `01-discovery/discovery-findings.md` exists.

## Before you start
Read `01-discovery/discovery-findings.md` and `00-prework/interview-target-spec.md`. Count your solid interviews against `references/interview-quality-bar.md`: real people in your segment with specific first-hand answers. Guardrail: the verdict follows the evidence, not your hopes. Under 5 solid interviews means insufficient evidence, no exceptions.

## Steps
1. Count solid interviews against `references/interview-quality-bar.md`. Write the number down. Warm answers from people who would never pay do not count.
2. If fewer than 5, record INSUFFICIENT EVIDENCE and stop. Your pre-work schedule may already hold Tuesday-morning overflow slots; count those first, then use the Digital Jersey shared interviewee pool if your network is dry. Reach 5 before calling it.
3. If 5 or more, score three tests yes/no with counts. Frequency: pain hits at least weekly? Intensity: people already spend money, time or workarounds on it? Consistency: same problem in at least 60 percent of interviews (6 of 10)?
4. Make the call. Three yeses on the same dominant problem: PERSEVERE. Problem real but not the one you tested, or a different segment feels it most: PIVOT and reframe. Fewer than two yeses, or mild and occasional: pivot to the sharper problem your interviews revealed.
5. Write the problem as one sentence in the customer's words: "[Segment] struggle to [specific job] because [specific reason], which costs them [time, money or risk]." No product, no solution.
6. Name the segment precisely: who, where they work, the one trait that makes them feel it most. Make it findable in Jersey.
7. Record the verdict, the three test scores, and one line of why in DECISIONS.md.

## The artefact
`01-discovery/validated-problem.md`: the one-sentence problem, the verdict, the three test scores with counts, the solid interview count.
`01-discovery/target-segment.md`: the named segment, where to find them in Jersey, the distinguishing trait.
Good looks like a problem sentence a stranger could instantly picture, backed by a number.

## Done when
`01-discovery/validated-problem.md` holds a single-sentence problem and one verdict. `01-discovery/target-segment.md` names one segment. DECISIONS.md has one dated line with the three scores. If INSUFFICIENT EVIDENCE: the count and a plan to reach 5 are recorded instead.

## Log it
Append one line to CHANGELOG.md via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`: date, skill id `d1-validated-problem`, artefact path `01-discovery/validated-problem.md`, numeric result (solid interview count). Then update state via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`: set days.1 outcome to the verdict and mark days.1 complete only if PERSEVERE or PIVOT. Append the decision and rationale to DECISIONS.md.

## If it goes wrong
Stuck between persevere and pivot: default to the problem the most people described in the most specific terms, and note the doubt in DECISIONS.md for Day 2. Cannot reach 5 by Tuesday midday even with the pool: narrow the segment. Do not start Day 2 on fewer than 5 solid interviews. Guessing the problem is the one mistake this week cannot recover from.
