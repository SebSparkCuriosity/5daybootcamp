---
name: Start
description: The front door of the five-day sprint. Captures your name, your path, your idea in one sentence and your numeric target for the week, then opens the journey. Use this first.
when_to_use: Run this once, at the very beginning, before any other spark-bootcamp skill. It initialises .spark/state.json and hands you to the coach.
---

# Start

**What this does.** Sets up your sprint: your name, your business type, your idea in one sentence, and the one number you are chasing this week. It writes `.spark/state.json` and points you at the coach.
**Why it matters.** Five days is short. If the idea is woolly or the target is fuzzy, you will spend the week busy and end it with nothing a customer will pay for. This step forces three decisions now so the next five days aim at a real buyer. Spark takes no work with a fuzzy target, and neither should you.
**You are ready for this when.** You have a rough idea and roughly an hour. That is all. This skill reads nothing; the idea comes from you.

## Before you start
There is no prior artefact. This is step zero.

One guardrail: do not overthink the idea here. You are not committing to it forever. You are stating it clearly enough to test it. Days 1 and 2 exist precisely to prove it or kill it.

## Steps

1. **Get your name.** Ask the founder for their first name. Use it from here on. Warm, first-name, no titles.

2. **Pick the path.** Ask which of three the business is, and pick exactly one:
   - **software**: the thing you sell is code that runs. Apps, tools, dashboards, platforms.
   - **hardware**: the thing you sell is a physical object, possibly with software inside it. Devices, kit, products you ship in a box.
   - **services**: the thing you sell is your team's time and expertise, ideally productised. Advisory, done-for-you work, managed support.
   If it is genuinely a mix, choose the part that the customer pays for first. Record it as one of `software`, `hardware` or `services`. This single choice branches the whole rest of the week, so get it right.

3. **Write the idea as ONE sentence.** Not a paragraph. Not three sentences. One. Push for this shape: "[product] helps [who] do [job] so they [get outcome]." If the founder cannot say it in one sentence, the idea is not yet clear enough to sell. Draft it with them until it fits on one line.

4. **Set the headline target, and put a number on it.** This is the non-negotiable. Ask: "What does success look like by Friday, as a number?" A good target is observable and countable. Examples that pass: "one paying customer at GBP 2,000 or more", "3 signed pilot agreements", "10 pre-orders with card details taken", "GBP 5,000 in booked intake calls". A target that fails: "validate the market", "build momentum", "get some interest". If the answer has no number, do not proceed. Reshape it with the founder until it names a figure. Prefer one paying customer over any vanity metric.

5. **Read it back.** Say the four things aloud: name, path, one-sentence idea, numeric target. Get an explicit "yes, that's right" before writing anything. Human in the loop from the very first step.

6. **Initialise state.** Once the founder confirms, write `.spark/state.json` via the journey-state helper. Do not hand-edit the file. Run:

   ```
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py" \
     --patch '{"founder":"<first name>","business_type":"<software|hardware|services>","idea":"<the one sentence>","headline_target":"<the target with its number>","current_day":1}'
   ```

   The helper creates the `.spark/` folder and day folders if they do not exist, and sets `days` to the five-day skeleton with each day's `complete` flag `false`. See `references/state-shape.md` for the exact object it writes and the full field list.

## The artefact
Writes `.spark/state.json` in JSON, via the journey-state helper. What good looks like: `founder` is a name, `business_type` is exactly one of the three allowed strings, `idea` is a single sentence, `headline_target` contains a digit, and `current_day` is `1`. Validate it by reading it back after the write.

## Done when
All five are true:
1. `.spark/state.json` exists and parses as valid JSON.
2. `business_type` is exactly one of `software`, `hardware` or `services`.
3. `idea` is one sentence (one full stop, no line breaks).
4. `headline_target` contains at least one digit.
5. You have told the founder their next move: run `/spark-bootcamp:coach`.

## Log it
Append one line to `CHANGELOG.md` via the logbook helper, recording that the sprint was started and the numeric target captured:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill start \
  --artefact ".spark/state.json" \
  --result "<the headline target>"
```

The `update-state.py` call in step 6 already set `.spark/state.json`, so no separate state update is needed here. Then point the founder to the coach in plain words: "You are set up. Run `/spark-bootcamp:coach` and I will walk you into Day 1."

## If it goes wrong
- **The helper is missing or errors.** Do not fall back to hand-writing `.spark/state.json`; a malformed state file will break every skill after this one. Tell the founder the journey-state skill has not installed correctly and stop. The fix is reinstalling the plugin, not patching the file.
- **The founder resists a numeric target.** Do not proceed on a fuzzy one. Offer three sharp options for their path (for example, for services: "3 signed pilots", "GBP 5,000 booked", "1 paying client at GBP 2,000+") and let them pick or adapt. A named number is the entry ticket.
- **The idea will not fit in one sentence.** That is a signal, not a formatting problem. It usually means two ideas are tangled together. Ask which one a customer pays for first, and start with that.
