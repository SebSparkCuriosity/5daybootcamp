---
name: Map The Story
description: Sequences your Musts into one end-to-end MVP slice and defines "done" for each. Use on Day 3 after requirements-moscow.md exists.
when_to_use: Day 3 product, straight after d3-moscow, before you build or ship anything. This is the last step before the build itself.
---

# Map The Story

**What this does.** Puts your Musts in the order a real user meets them, draws one line through the whole journey as the MVP slice, and writes a testable "done" for every Must so you know when to stop.
**Why it matters.** A MoSCoW list tells you what to build. It does not tell you the order, where the slice starts and ends, or how you will know a feature actually works. Without that, you build the fun bits, skip the joins, and on Friday you have five half-features and nothing a customer can complete start to finish. The story map fixes the sequence and defines "done" before you write a line, so the build has a spine and a finish line.
**You are ready for this when.** `03-product/requirements-moscow.md` exists and has at most seven Musts.

## Before you start
Read `03-product/requirements-moscow.md`, the Musts especially, and the one-line MVP statement at the top ("The smallest thing a customer will pay for is: ..."). Read `02-market/proposition.md` again: the slice you draw has to deliver that promise end to end, not in fragments.

Optional but recommended: read `${CLAUDE_SKILL_DIR}/references/acceptance-criteria.md` so your "done" lines are testable, not wishful.

## What a story map is, in one picture
Read left to right along the top: the steps a user takes, in order, from first arrival to the moment they act (pay, book, or leave real intent). That top row is the backbone. Under each step, stack the Musts that make that step work, most essential at the top. The MVP slice is a single horizontal line drawn across the stacks: one thing per step, the minimum that lets a user walk the whole backbone without falling through a gap.

The point of the slice is completeness, not size. Ten features that cover eight of ten steps is a broken product. One feature per step that covers all ten is a product someone can finish.

## Steps
1. **Write the backbone.** List the ordered steps a user takes, from landing to acting. Aim for five to nine steps. For example: arrive, understand the offer, see it work, trust it, act, get confirmation. Keep each step a short verb phrase. This is the user's journey, not your build plan.
2. **Hang each Must under the step it serves.** Take every Must from `requirements-moscow.md` and place it under the backbone step it belongs to. If a Must does not fit any step, your backbone is missing a step, or the Must is not really a Must. Fix one or the other now.
3. **Check every step has cover.** Walk the backbone left to right. Any step with no Must under it is a hole a user falls through. Either promote a Should to cover it, or cut the step if no user truly needs it. A backbone with a gap is not an MVP.
4. **Draw the MVP slice.** Mark the single thinnest set of Musts (mark them with `[MVP]`) that lets one user complete the whole backbone once, start to finish. Everything above the line is in the week; everything below waits. If the slice needs more than your seven Musts, go back to `d3-moscow`: the scope is still too wide.
5. **Write acceptance criteria for every Must.** For each Must, write one to three lines that state, observably, when it is done. Use the form "Given [situation], when [action], then [observable result]". "Works" is not a criterion. "Given a visitor on the page, when they submit their email, then a row appears in the table and they see a confirmation" is. See `${CLAUDE_SKILL_DIR}/references/acceptance-criteria.md`.
6. **Sanity-check the slice against the proposition.** Read the slice as one sentence: "a user arrives, does X, and ends by Y." Does that single walk-through deliver the promise in `proposition.md`? If it delivers only half the promise, the slice is wrong, not the promise. Redraw it.

## For software
The backbone is the user's click-path on the public URL: land, see the offer, give one input, see one result, leave email or payment intent, get confirmation. Acceptance criteria are the sharpest here: write them so you could hand them to anyone and they could tell you pass or fail without asking you. Data written, message shown, redirect happened. If you cannot observe it, it is not done.

## For hardware
The backbone spans two artefacts, so map both. First the usage journey: how a person encounters the product, uses it, and gets the result the prototype has to prove. Then the buying journey on the pre-order or waitlist page: land, see the render, understand the offer, leave a deposit or real intent, get confirmation. Acceptance criteria for the prototype are observable too: "the render shows [the core mechanism] clearly enough that a prospect understands it without explanation", "the page accepts a deposit and records who paid".

## For services
The backbone is a service blueprint: the client's steps above the line (enquire, see the sample, understand scope and price, book, get confirmed) and, noted below each, what you do to deliver it. Map the one sample deliverable as the artefact that proves quality, and the bookable intake page as the step where they act. Acceptance criteria: "the sample deliverable is complete enough that a prospect can judge quality without a meeting", "the intake page takes a booking and captures name, need and contact".

## The artefact
Writes `03-product/story-map.md` in Markdown. Structure: the backbone as an ordered list of steps; under each step, the Musts that serve it, with the MVP ones tagged `[MVP]`; then an "Acceptance criteria" section with every Must and its Given/When/Then lines; and a one-line "The MVP slice, walked" statement at the top that reads the whole journey as one sentence. Use `${CLAUDE_SKILL_DIR}/references/story-map-template.md` as the starting structure. What good looks like: every backbone step has at least one Must, exactly one coherent MVP slice is tagged, and every Must has at least one testable acceptance line.

## Done when
One end-to-end MVP slice is marked (`[MVP]` tags form an unbroken line across every backbone step), and every Must from `requirements-moscow.md` carries at least one Given/When/Then acceptance criterion. If any backbone step has no `[MVP]` Must under it, or any Must has no acceptance line, you are not done.

## Log it
Append one line to CHANGELOG.md via the logbook helper (`${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`): date, `d3-story-map`, the artefact path, and the counts as the numeric result (for example "6 backbone steps, 5 Musts with acceptance criteria"). Then update `.spark/state.json` via the journey-state helper (`${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`): register the artefact and set day 3 progress. If you moved a step or promoted a Should to close a gap, note why in DECISIONS.md.

## If it goes wrong
Slice keeps growing past your Musts every time you draw it? The backbone has too many steps for one week. Cut the journey to the shortest walk that still delivers the proposition, usually five steps, and defer the rest to next week's slice. If you cannot write an observable "done" for a Must, that Must is vague, not hard: rewrite it as a concrete thing a user does and sees, or demote it to a Should and move on.
