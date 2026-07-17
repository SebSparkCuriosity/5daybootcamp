---
name: Brand Foundations
description: Set your values, personality, tone and name, executable by a non-designer. Use on Day 2 after the proposition and messaging are written.
when_to_use: Day 2, after d2-proposition and d2-messaging, before any logo, colour or landing page work.
---

# Brand Foundations

**What this does.** Turns your proposition into a brand you can act on: 3 to 5 values, one archetype, a tone rated on 4 dimensions, and a resolved name or shortlist.
**Why it matters.** Decide once how you sound and what you stand for, and every email, page and pitch downstream sounds like the same firm.
**You are ready for this when.** `02-market/proposition.md` and `02-market/messaging.md` both exist.

## Before you start
Read `02-market/proposition.md`, `02-market/messaging.md`, `.spark/state.json` (`founder`, `idea`, `business_type`), and the "Where this idea comes from" section of `01-discovery/idea-brief.md`: the founder already told you their philosophy on Day 1, so start from it. This is a working discussion (about 20 minutes): values are the founder's beliefs, not a menu. Ask before proposing: what would you refuse to do for a client, even paid? What should working with you feel like? Capture their answers verbatim. Fit the buyer in the proposition, not your own taste. For regulated Jersey firms, "trustworthy" is the entry ticket, not a differentiator: push past it.

## Steps
1. **Values: pick 3 to 5.** Written as what you do, not adjectives ("We ship in weeks, not quarters" beats "agile"). Add one sentence each on how a customer sees it in practice. Cut any value that changes no decision.
2. **Archetype: pick exactly one, together.** Open `${CLAUDE_SKILL_DIR}/references/archetypes.md` (12 archetypes, one example each). Offer the two that best match what the founder just said, one reason each; the founder picks. Write one sentence on why it fits.
3. **Tone: rate 4 dimensions.** Open `${CLAUDE_SKILL_DIR}/references/tone-dimensions.md`. Rate each slider 1 to 5 with a note: Formal to Casual, Serious to Playful, Plain to Expressive, Reserved to Bold. Regulated sectors usually sit 2 to 3 formal, 1 to 2 playful. Write one example sentence in your voice.
4. **Name: resolve it or set a direction.** Follow `${CLAUDE_SKILL_DIR}/references/naming-checklist.md`. Run each candidate through the five gates and land on ONE name, or a shortlist of at most 3 with the reason each survives. Flag domain and trademark checks as "confirm before spending" (a Day 4 spend, not Day 2).
5. **Write the file** and update state.

## The artefact
Writes `02-market/brand/brand-foundations.md` in Markdown, five sections in order: values (3 to 5, each a claim plus practice sentence); archetype (one, with reason); tone (4 sliders rated with notes, plus one example sentence); name (resolved, or shortlist of up to 3 with reasons and any "confirm before spending" flags); one-line summary. Good looks like: a stranger could read it and write an email that sounds like you.

## Done when
- 3 to 5 values, each with a practice sentence.
- Exactly 1 archetype named, with a reason.
- 4 tone dimensions rated 1 to 5, with an example sentence.
- Naming resolved: one name, or a shortlist of at most 3 with reasons.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d2-brand-foundations \
  --artefact 02-market/brand/brand-foundations.md \
  --result "5 values, 1 archetype, 4 tone dimensions, name resolved"
```
If the name was a genuine call between options, add one line to `DECISIONS.md`: the name chosen and why the others lost.

## If it goes wrong
Cannot settle the name in one sitting? Lock the values, archetype and tone, keep your working name, and record the direction plus shortlist. A name you can change later beats a week spent naming. The proposition sells, not the name.
