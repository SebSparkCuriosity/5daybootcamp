---
name: Set The Product Context
description: Confirms your business path and boils your MVP to one sentence, so the whole of Day 3 builds the right thing for the right path. First step of Day 3, before you build anything.
when_to_use: Day 3 product, the very first step, after Day 2 wrote proposition.md and positioning.md. Everything you build on Day 3 branches from the track flag this sets.
---

# Set The Product Context

**What this does.** Locks in which of the three paths you are on (software, hardware or services), writes down what "live and actionable" means for that path, and pins your MVP to one sentence.
**Why it matters.** Day 3 is build day. Before you build, you need to know exactly what you are building and what "done" looks like for your kind of business. A software slice, a hardware prototype and a service sample are three different jobs. Get the context wrong now and you spend Wednesday building the wrong thing. This step is short on purpose: five minutes of clarity that steers the whole day.
**You are ready for this when.** `02-market/proposition.md` and `02-market/positioning.md` both exist.

## Before you start
Read three things:
- `.spark/state.json`, via the journey-state helper, for the `business_type` field. This is already set from Day 1. You are confirming it, not re-asking it.
- `02-market/proposition.md`, for the one-sentence proposition and the customer's success metric.
- `02-market/positioning.md`, for the buyer and the USP.

Then read the Day 3 row of the variance matrix, which tells you what "done" means for your path today:
`${CLAUDE_PLUGIN_ROOT}/skills/business-profile/references/variance-matrix.md`.

No money is spent and no message is sent in this step. It is a thinking-and-writing step only.

## Steps
1. Read the path from state. Run:
   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" --read
   ```
   Take the `business_type` field. It must be one of `software`, `hardware` or `services`. Do not ask the founder again: the path was set on Day 1 and re-asking wastes their time and invites a mid-week wobble. If, and only if, the field is missing or is not one of the three values, stop and send them back to Day 1 discovery to set it. Do not guess a default.
2. Confirm the path out loud to the founder in one line, so they can catch a genuine error before the day is built on it. For example: "You are on the services path, confirmed from Day 1. Everything today builds a productised service package with one real sample deliverable." One line, then move on.
3. Read the Day 3 cell for your path in the variance matrix. That cell is the authority on what "live and actionable" means for you today. Copy its definition of done into your notes. You will build against this, so get it exact.
4. Boil the MVP to one sentence. This is the heart of the step. Take the proposition and cut it down to the single core action or output your Day 3 build must deliver. Not three features. One. The test: a stranger reads the sentence and knows precisely what the thing does. Use the path-specific shape below.
5. Sanity-check the sentence against the success metric in `proposition.md`. If your MVP sentence does not plausibly move that number for the customer, it is the wrong MVP. Narrow it until it does.
6. Write the artefact, including the track flag (the confirmed path), so every later Day 3 skill reads one file and branches the same way.

### For software
Your MVP sentence names the one core action a stranger can complete end to end on a public URL. Shape: "A page where [this person] can [do this one thing] and get [this result], no login walkthrough needed." Example: "A page where a fund administrator pastes a trial balance and gets a flagged reconciliation in under a minute." Default stack is Next.js + Supabase + Vercel; note it if the founder has a reason to differ.

### For hardware
Your MVP sentence names the one thing the prototype must let a prospect see and understand. A CAD render or a physical mock, not a finished product. Shape: "A [render or mock] of [the thing] that shows [the one feature that matters] clearly enough that someone describes it correctly without being told." Example: "A CAD render of the tamper-evident sample case that shows the single-seal lid clearly enough to grasp on sight."

### For services
Your MVP sentence names the one sample deliverable you will produce in full, as a real finished output, not a description of one. Shape: "One completed [deliverable] for [this kind of client] that shows [the outcome], good enough to judge on sight." Example: "One completed month-end reconciliation pack for a small trust firm, finished to the standard a real client would sign off."

## The artefact
Writes `03-product/product-context.md` in Markdown. It contains, in this order:
- **Track flag**: the confirmed `business_type`, stated plainly at the top, for example `Track: services`. This is the line every later Day 3 skill reads to branch.
- **Path confirmation**: one sentence restating the path and where it came from (Day 1).
- **Definition of done for today**: the Day 3 cell for this path, copied from the variance matrix, so the day has one clear finish line.
- **The MVP in one sentence**: the single core action or output, written to the path-specific shape above.
- **Why this MVP**: one line tying the sentence to the customer's success metric from `proposition.md`.

Good looks like a page a stranger reads in thirty seconds and then knows exactly what you are building today and how you will know it worked.

## Done when
All three are true:
1. `business_type` is confirmed as exactly one of software, hardware or services, and the track flag is written to `03-product/product-context.md`.
2. The MVP is stated in one sentence (one core action or output, not a feature list).
3. The Day 3 definition of done for this path is copied in from the variance matrix.

`03-product/product-context.md` exists with the track flag on the first content line.

## Log it
Append one line to CHANGELOG.md via the logbook helper:
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill d3-product-context \
  --artefact 03-product/product-context.md \
  --result "Track: services; MVP set in 1 sentence"
```
Replace the track and keep the result to a short numeric or observable line. Then set Day 3 progress in state:
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
  --patch '{"current_day":3,"days":{"3":{"target":"Build the MVP live and actionable for the path","outcome":"product context set, MVP in one sentence"}}}'
```
If you narrowed the MVP in a way that changes what Day 3 builds, log it as a dated decision with its rationale in DECISIONS.md via the logbook helper's `--decision` and `--rationale` flags.

## If it goes wrong
If `business_type` is missing or malformed, do not pick a path to keep moving. Stop and send the founder back to Day 1 discovery, where the path is set with a reason. A path chosen silently on Wednesday is the most expensive mistake in the week, because everything after it is built on the guess. If the MVP sentence keeps sprawling into three features, that is a signal the proposition is still too broad: cut to the single pain the customer begged you to remove on Day 1 and build only that.
