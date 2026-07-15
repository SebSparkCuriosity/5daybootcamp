---
name: Map The Story
description: Sequences your Musts into one end-to-end MVP slice and defines "done" for each. Day 3, after requirements-moscow.md exists.
when_to_use: Day 3 product, straight after d3-moscow, before you build or ship.
---

# Map The Story

**What this does.** Orders your Musts along the user's journey, draws one line through it as the MVP slice, and writes a testable "done" for every Must.
**Why it matters.** A MoSCoW list says what to build, not the order or the finish line, so without a map you end Friday with five half-features and nothing a customer can complete.
**You are ready for this when.** `03-product/requirements-moscow.md` exists with at most seven Musts.

## Before you start
Read `03-product/requirements-moscow.md` (the Musts and the one-line MVP statement) and `02-market/proposition.md`: the slice must deliver that promise end to end. Optional: `${CLAUDE_SKILL_DIR}/references/acceptance-criteria.md` for testable "done" lines.

## Steps
1. **Write the backbone.** List the ordered steps a user takes, landing to acting (arrive, understand, see it work, trust, act, confirm). Five to nine short verb phrases. Journey, not build plan.
2. **Hang each Must under its step.** Place every Must under the backbone step it serves. A Must that fits nowhere means a missing step or a fake Must. Fix it.
3. **Check every step has cover.** A step with no Must is a hole. Promote a Should to fill it, or cut the step. No gaps.
4. **Draw the MVP slice.** Tag `[MVP]` the thinnest set of Musts that lets one user complete the whole backbone once. If the slice needs more than seven Musts, go back to `d3-moscow`.
5. **Write acceptance criteria for every Must.** One to three lines each, form "Given [situation], when [action], then [observable result]". "Works" is not a criterion. See `${CLAUDE_SKILL_DIR}/references/acceptance-criteria.md`.
6. **Sanity-check against the proposition.** Read the slice as one sentence. If it delivers only half the promise in `proposition.md`, redraw the slice.

## For software
Backbone is the click-path on the public URL: land, see offer, give one input, see one result, leave email or payment intent, confirm. Write criteria anyone can pass/fail without you: data written, message shown, redirect happened.

## For hardware
Map both journeys. Usage: how a person encounters and uses the product to get the result the prototype proves. Buying (pre-order or waitlist page): land, see render, understand offer, leave deposit or intent, confirm. Criteria: "render shows the core mechanism without explanation", "page accepts a deposit and records who paid".

## For services
Backbone is a service blueprint: client steps above the line (enquire, see sample, understand scope and price, book, confirm), your delivery noted below. Map the one sample deliverable and the bookable intake page. Criteria: "sample lets a prospect judge quality without a meeting", "intake page takes a booking, captures name, need and contact".

## The artefact
Writes `03-product/story-map.md`. Backbone as ordered steps; Musts under each, MVP ones tagged `[MVP]`; an "Acceptance criteria" section with every Must's Given/When/Then; a one-line "The MVP slice, walked" at the top. Start from `${CLAUDE_SKILL_DIR}/references/story-map-template.md`. Good: every step has a Must, one coherent MVP slice tagged, every Must has a testable line.

## Done when
One unbroken `[MVP]` slice spans every backbone step, and every Must from `requirements-moscow.md` carries at least one Given/When/Then criterion.

## Log it
Append one line to CHANGELOG.md via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py --skill d3-story-map --artefact 03-product/story-map.md --result "<counts>"` (for example "6 backbone steps, 5 Musts with acceptance criteria"). Set day 3 progress via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py --patch`. If you moved a step or promoted a Should, note why in DECISIONS.md.

## If it goes wrong
Slice keeps growing past your Musts? Too many backbone steps. Cut to the shortest walk that still delivers the proposition (usually five) and defer the rest. Can't write an observable "done" for a Must? It's vague, not hard: rewrite it as a concrete thing a user does and sees, or demote to a Should.
