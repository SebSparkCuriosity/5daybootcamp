---
name: Brand Foundations
description: Set your values, personality, tone and name, executable by a non-designer. Use on Day 2 after the proposition and messaging are written.
when_to_use: Day 2 market work, after d2-proposition and d2-messaging, before any logo, colour or landing page work. Everything visual downstream reads this file.
---

# Brand Foundations

**What this does.** Turns your proposition into a brand you can act on: 3 to 5 values, one archetype, a tone rated on 4 dimensions, and a resolved name (or a clear direction and a shortlist).
**Why it matters.** A brand is not a logo. It is a set of decisions about how you sound and what you stand for, made once so every email, page and pitch downstream sounds like the same firm. Skip this and you will redecide your tone in every document you write. Get it right and the logo, the colours and the copy almost write themselves.
**You are ready for this when.** `02-market/proposition.md` and `02-market/messaging.md` both exist.

## Before you start
Read these first:
- `02-market/proposition.md`: who you serve and the promise you make them.
- `02-market/messaging.md`: the words you already use to describe the value.
- `.spark/state.json`: your `founder`, `idea` and `business_type`.

Your brand must fit the buyer in the proposition, not your own taste. A trust company brand and a beach cafe brand are not interchangeable. If you serve regulated Jersey firms, "trustworthy" is not a differentiator, it is the entry ticket. Push past it.

Reference material lives in `${CLAUDE_SKILL_DIR}/references/archetypes.md` (the 12 archetypes with an example each) and `${CLAUDE_SKILL_DIR}/references/tone-dimensions.md` (the 4 sliders explained). Read them when you reach steps 2 and 3.

## Steps
1. **Values: pick 3 to 5.** These are the things you will not trade away, written as what you do, not adjectives. "We ship in weeks, not quarters" beats "agile". "We show our working" beats "transparent". Fewer than 3 and you have said nothing; more than 5 and you will remember none of them. For each value write one sentence on how a customer would see it in practice. If a value does not change a single decision you make, cut it.

2. **Archetype: pick exactly one.** Open `${CLAUDE_SKILL_DIR}/references/archetypes.md`. It lists 12 recognised brand archetypes (the Sage, the Hero, the Creator, the Everyman and so on) with a one-line example of each. Pick the single one that matches how you want the buyer to feel about you. One, not two. A brand that is both the rebellious Outlaw and the reassuring Caregiver is neither. Write one sentence saying why that archetype fits your buyer.

3. **Tone: rate 4 dimensions.** Open `${CLAUDE_SKILL_DIR}/references/tone-dimensions.md`. Place yourself on each of these 4 sliders from 1 to 5 and note where and why:
   - Formal (1) to Casual (5)
   - Serious (1) to Playful (5)
   - Plain (1) to Expressive (5)
   - Reserved (1) to Bold (5)
   Regulated sectors usually sit 2 to 3 on formality and 1 to 2 on playful. That is fine. Bold and plain can still stand out inside those bounds. Write one example sentence in your voice so the numbers mean something.

4. **Name: resolve it or set a clear direction.** Follow the checklist in `${CLAUDE_SKILL_DIR}/references/naming-checklist.md`. Decide first whether you are keeping your working name, changing it, or choosing fresh. Then run every candidate through the five gates: says something true, easy to say aloud, spellable after hearing it once, .com or .je available or a close variant is, and not already trading in your sector on the island. Land on ONE name, or a shortlist of no more than 3 with the single reason each survives. Do a quick check for obvious clashes before you commit. Flag domain and trademark checks as "confirm before spending", they are a Day 4 spend decision, not a Day 2 one.

5. **Write the file** in the shape below and update state.

## The artefact
Writes `02-market/brand/brand-foundations.md` in Markdown, with these five sections in order:

1. **Values (3 to 5).** Each as a short claim plus one sentence on how a customer sees it.
2. **Archetype (one).** The name, and one sentence on why it fits the buyer.
3. **Tone (4 dimensions).** Each slider with its 1 to 5 rating and a note, plus one example sentence written in the resulting voice.
4. **Name.** The resolved name, or a shortlist of up to 3 with the reason each survives, and any checks flagged "confirm before spending".
5. **One-line summary.** "We are the [archetype] for [buyer], and we sound [tone in three words]."

What good looks like: a stranger could read this file and write an email that sounds like you. If two people could read it and disagree about how you sound, it is not specific enough.

## Done when
All four are true, and they are, count them:
- 3 to 5 values, each with a practice sentence.
- Exactly 1 archetype named, with a reason.
- 4 tone dimensions rated 1 to 5, with an example sentence.
- Naming resolved: one name, or a shortlist of at most 3 with reasons.

## Log it
Append one line to `CHANGELOG.md` via the logbook helper, with the numeric result (for example "5 values, 1 archetype, tone on 4 dimensions, name resolved"):

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d2-brand-foundations \
  --artefact 02-market/brand/brand-foundations.md \
  --result "5 values, 1 archetype, 4 tone dimensions, name resolved"
```

The logbook helper registers the artefact in `.spark/state.json` for you, so no separate state update is needed for it.

If the name choice was a genuine call between options, write one line in `DECISIONS.md`: the name you chose and why the others lost.

## If it goes wrong
If you cannot settle the name in one sitting, do not stall the whole week on it. Lock the values, archetype and tone, keep your working name, and record the naming direction plus the shortlist in the file. A name you can change later beats a week you spent naming. The proposition sells, not the name.
