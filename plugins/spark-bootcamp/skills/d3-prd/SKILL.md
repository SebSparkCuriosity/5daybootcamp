---
name: Write The Build Brief
description: Turn your story map and MoSCoW cut into the one build brief Claude Code builds from. Every Must becomes a numbered requirement, non-goals are named, the success metric is a number. Use on Day 3.
when_to_use: Day 3 product, straight after d3-story-map and d3-moscow, before you build the working slice. The last thing you write before code, CAD or a sample deliverable exists.
---

# Write The Build Brief

**What this does.** Turns your story map and your MoSCoW cut into a single build brief Claude Code (or you) can build from without guessing.
**Why it matters.** A vague brief is the most expensive thing you can carry into build day. Every ambiguity becomes a question mid-build, and every question is an hour you do not have this week. Nail the brief and the build is mechanical. Every Must becomes a numbered requirement, every Won't becomes a written non-goal, and the whole thing points at one number.
**You are ready for this when.** `03-product/story-map.md` and your MoSCoW cut (usually `03-product/requirements-moscow.md`) both exist.

## Before you start
Read these three, in this order:

- `03-product/story-map.md`: the user journey, step by step.
- `03-product/requirements-moscow.md`: your Must, Should, Could, Won't cut.
- `.spark/state.json`: `business_type`, `idea` and `headline_target`. The brief must serve the headline target, not drift off it.

One rule before you touch the brief: only the **Musts** go in as requirements this week. Shoulds and Coulds are listed as "later", never built now. If a Must does not trace back to a step on the story map, it is not really a Must. Send it back.

## Steps
1. **Restate the outcome as a number.** Open the brief with one sentence: what a real prospect can do by end of Day 3, and the single metric that proves it. Not "a working app". Instead "a prospect can request a trust review and gets a booking confirmation, and 3 real prospects complete this by Friday". Pull the number from `headline_target` and narrow it to what Day 3 alone can prove.
2. **Turn every Must into a numbered requirement.** One Must, one requirement, one number. Write each as "R1: The system must [do this specific thing], measured by [this observable]". A requirement with no observable is a wish, not a requirement. If a Must is really two things, split it into R2 and R3.
3. **Write the non-goals.** List every Won't and every Should you are deliberately not building this week. Say it plainly: "Not in scope: user accounts, payment capture, email reminders." This is the most valuable section. It is what stops the build sprawling.
4. **Define the acceptance test.** For each requirement, write the one check that proves it works. "R1 passes when a prospect submits the form and a row appears in the bookings table within 5 seconds." Observable, not aspirational.
5. **Write the functional spec.** Now go one layer down: the actual screens or steps, the fields, the states (empty, loading, error, done), and what happens on each action. This is the layer Claude Code reads to build. Keep it concrete: name every field, name every button, name every message.
6. **Branch by path (see below) for the parts that differ.**
7. **Run the checker.** `python3 ${CLAUDE_SKILL_DIR}/scripts/check-brief.py 03-product/docs/PRD.md`. It confirms every Must has a numbered requirement, non-goals are present, and the metric is a number. Fix what it flags.

## For software
The functional spec names the routes, the data the page reads and writes, and the one Supabase table behind the slice. Requirements describe behaviour a user can see, not implementation. Example R: "The system must let a visitor submit their email and one line of context, and store it." Acceptance: "a new row appears in `leads` within 5 seconds of submit." The metric is completions, not deploys.

## For hardware
Split the brief in two, because you are building two things: the prototype and the intent page.

- Prototype requirements describe what the CAD render or physical mock must show a prospect: dimensions, the one feature that sells it, the angle it is rendered at.
- Intent-page requirements describe the waitlist or pre-order page that captures real payment intent (a card hold or a deposit, not just an email).

The metric is signed-up intent, for example "8 waitlist sign-ups with a £10 deposit by Friday".

## For services
Requirements describe the productised package and the one sample deliverable that proves the quality (a filled-in template, a worked example, a two-page sample report). The intake page is a bookable form. Example R: "The system must present a fixed-scope, fixed-price package and let a prospect book a 20-minute intake call." Acceptance: "a booking lands in the calendar with the prospect's name and sector." The metric is booked intakes.

## The artefact
Writes two files:

- `03-product/docs/PRD.md` in Markdown: the outcome sentence with its number, the numbered requirements (each with an acceptance test), the non-goals, and the success metric. Use `${CLAUDE_SKILL_DIR}/references/prd-template.md` as the skeleton.
- `03-product/docs/functional-spec.md` in Markdown: the screen-by-screen or step-by-step detail the build reads from. Use `${CLAUDE_SKILL_DIR}/references/functional-spec-template.md`.

What good looks like: someone who has never heard your pitch can read the PRD and build the right thing without asking you a single question. Every Must is a numbered R. Nothing in the non-goals sneaks back into a requirement. The metric is a number with a deadline.

## Done when
The checker passes: every Must from `requirements-moscow.md` maps to a numbered requirement in `PRD.md`, the non-goals section is non-empty, and the success metric contains a number. Both files exist and `functional-spec.md` names every field and every action on every screen or step.

## Log it
Append one line to `CHANGELOG.md` via the logbook helper, with the requirement count as the numeric result:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d3-prd \
  --artefact 03-product/docs/PRD.md \
  --result "<N> requirements, metric set"
```

Then update state via the journey-state helper, recording the Day 3 target:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"3":{"target":"Build brief written, <N> requirements"}}}'
```

Record any scope call you made (a Must you demoted, a Should you refused) in `DECISIONS.md` with one line of rationale.

## If it goes wrong
If you have more than 7 Must requirements, you have not cut hard enough. A five-day week builds 3 to 5 Musts well, or 8 Musts badly. Go back to `requirements-moscow.md`, demote the weakest Musts to Should, and note why in `DECISIONS.md`. If you cannot state the success metric as a number, the idea is still too fuzzy to build; return to Day 1's idea brief and sharpen the outcome before you write a line of code.
