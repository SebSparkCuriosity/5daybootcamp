---
name: Set The Product Context
description: Confirms your business path and boils your MVP to one sentence, so Day 3 builds the right thing. First step of Day 3.
when_to_use: Day 3 product, first step, after Day 2 wrote proposition.md and positioning.md.
---

# Set The Product Context

**What this does.** Locks in your path (software, hardware or services), writes what "live and actionable" means for it, and pins your MVP to one sentence.
**Why it matters.** Wednesday is build day, and five minutes of clarity now stops you spending it building the wrong thing.
**You are ready for this when.** `02-market/proposition.md` and `02-market/positioning.md` both exist.

## Before you start
Read via journey-state: `.spark/state.json` for `business_type` (set on Day 1, confirm it). Read `02-market/proposition.md` for the proposition and success metric, `02-market/positioning.md` for buyer and USP. Read the Day 3 row of `${CLAUDE_PLUGIN_ROOT}/skills/business-profile/references/variance-matrix.md`. No money spent, no message sent.

## Steps
1. Read the path: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" --read`. Take `business_type`; it must be `software`, `hardware` or `services`. If missing or invalid, stop and send them back to Day 1. Do not re-ask or guess.
2. Confirm the path to the founder in one line so they can catch a genuine error.
3. Copy the Day 3 variance-matrix cell for your path: that is the day's definition of done.
4. Boil the MVP to one sentence: the single core action or output the build must deliver, not three features. A stranger reads it and knows exactly what the thing does. Use the path shape below.
5. Sanity-check against the success metric in `proposition.md`. If the sentence does not plausibly move that number, narrow it until it does.
6. Write the artefact with the track flag so every later Day 3 skill branches the same way.

### For software
Name the one core action a stranger completes end to end on a public URL. Shape: "A page where [person] can [do one thing] and get [result]." Default stack Next.js + Supabase + Vercel; note any deviation.

### For hardware
Name the one thing the prototype (CAD render or physical mock) must let a prospect see and understand. Shape: "A [render or mock] of [thing] that shows [the feature that matters] clearly enough to grasp on sight."

### For services
Name the one sample deliverable you will produce in full, a real finished output. Shape: "One completed [deliverable] for [client type] that shows [outcome], good enough to judge on sight."

## The artefact
Writes `03-product/product-context.md`, in order: **Track flag** (e.g. `Track: services`, first content line); **Path confirmation** (one sentence, from Day 1); **Definition of done for today** (Day 3 variance cell); **MVP in one sentence** (path shape above); **Why this MVP** (one line tying it to the success metric).

## Done when
1. `business_type` confirmed as exactly one of software, hardware or services, track flag written to `03-product/product-context.md`.
2. MVP stated in one sentence (one action or output, not a list).
3. Day 3 definition of done copied from the variance matrix.

## Log it
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill d3-product-context \
  --artefact 03-product/product-context.md \
  --result "Track: services; MVP set in 1 sentence"
```
Then set Day 3 progress:
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
  --patch '{"current_day":3,"days":{"3":{"target":"Build the MVP live and actionable for the path","outcome":"product context set, MVP in one sentence"}}}'
```
If you narrowed the MVP in a way that changes what Day 3 builds, log it via the logbook helper's `--decision` and `--rationale` flags in DECISIONS.md.

## If it goes wrong
If `business_type` is missing or malformed, stop and send the founder back to Day 1; a path chosen silently on Wednesday is the week's most expensive mistake. If the MVP sentence keeps sprawling into three features, the proposition is too broad: cut to the single pain from Day 1 and build only that.
