---
name: Write The Build Brief
description: Turn your story map and MoSCoW cut into the one build brief Claude Code builds from. Every Must a numbered requirement, one success number. Day 3.
when_to_use: Day 3, after d3-story-map and d3-moscow, before you build the working slice.
---

# Write The Build Brief

**What this does.** Turns your story map and MoSCoW cut into a single build brief Claude Code (or you) can build from without guessing.
**Why it matters.** A vague brief is the most expensive thing you carry into build day, because every ambiguity becomes an hour-long question you do not have this week.
**You are ready for this when.** `03-product/story-map.md` and `03-product/requirements-moscow.md` both exist.

## Before you start
Read `03-product/story-map.md` (the journey), `03-product/requirements-moscow.md` (your cut), and `.spark/state.json` (`business_type`, `idea`, `headline_target`). Only Musts become requirements this week. If a Must does not trace to a story-map step, send it back.

## Steps
1. **Restate the outcome as a number.** One sentence: what a real prospect can do by end of Day 3 and the single metric that proves it. Pull the number from `headline_target`, narrowed to what Day 3 alone proves.
2. **Turn every Must into a numbered requirement.** "R1: The system must [specific thing], measured by [observable]." No observable means it is a wish. Split a two-part Must into R2 and R3.
3. **Write the non-goals.** List every Won't and every Should you are not building: "Not in scope: user accounts, payment capture." This stops the build sprawling.
4. **Define the acceptance test.** For each requirement, the one check that proves it: "R1 passes when a prospect submits and a row appears within 5 seconds."
5. **Write the functional spec.** Go one layer down: screens or steps, fields, states (empty, loading, error, done), what each action does. Name every field, button and message.
6. **Branch by path (below) for the parts that differ.**
7. **Run the checker.** `python3 ${CLAUDE_SKILL_DIR}/scripts/check-brief.py 03-product/docs/PRD.md`. Fix what it flags.

## For software
Functional spec names routes, the data the page reads/writes, and the one Supabase table. Requirements describe visible behaviour, e.g. "let a visitor submit email and one line of context, and store it"; acceptance "a new row appears in `leads` within 5 seconds". Metric is completions, not deploys.

## For hardware
Split the brief in two: prototype and intent page. Prototype requirements state what the CAD render or physical mock must show (dimensions, the selling feature, the render angle). Intent-page requirements state the waitlist or pre-order page capturing real payment intent (a card hold or deposit, not just email). Metric is signed intent, e.g. "8 sign-ups with a £10 deposit by Friday".

## For services
Requirements describe the productised package and the one sample deliverable proving quality (filled template, worked example, two-page sample). Intake page is a bookable form. Example R: "present a fixed-scope, fixed-price package and let a prospect book a 20-minute intake call"; acceptance "a booking lands in the calendar with name and sector". Metric is booked intakes.

## The artefact
Writes two Markdown files: `03-product/docs/PRD.md` (outcome sentence with number, numbered requirements each with an acceptance test, non-goals, success metric) from `${CLAUDE_SKILL_DIR}/references/prd-template.md`; and `03-product/docs/functional-spec.md` (screen-by-screen or step-by-step detail) from `${CLAUDE_SKILL_DIR}/references/functional-spec-template.md`. Good: a stranger can build the right thing without asking you a question.

## Done when
Checker passes: every Must in `requirements-moscow.md` maps to a numbered requirement in `PRD.md`, non-goals is non-empty, the metric contains a number. Both files exist and `functional-spec.md` names every field and action on every screen or step.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d3-prd \
  --artefact 03-product/docs/PRD.md \
  --result "<N> requirements, metric set"
```
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"3":{"target":"Build brief written, <N> requirements"}}}'
```
Record any scope call (a Must demoted, a Should refused) in `DECISIONS.md` with one line of rationale.

## If it goes wrong
More than 7 Musts means you have not cut hard enough: a five-day week builds 3 to 5 Musts well, or 8 badly. Demote the weakest to Should in `requirements-moscow.md` and note why in `DECISIONS.md`. If you cannot state the metric as a number, return to Day 1's idea brief and sharpen the outcome first.
