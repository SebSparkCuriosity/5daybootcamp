---
name: Visual Identity
description: Choose your whole look with the founder: 3 logo concepts to pick from, a font pairing, an AA-safe palette. Day 2, after brand-foundations, before brand-register.
when_to_use: Day 2, after d2-brand-foundations, before brand-register and the brand book. The skill where the founder chooses logo, colours and fonts.
---

# Visual Identity

**What this does.** Walks the founder through choosing everything visual: three genuinely different logo concepts (they pick one and refine it twice), one of three font pairings, and a five-colour AA-safe palette.
**Why it matters.** This settles how you look in under an hour, not a fortnight, and because you chose each piece yourself, you can defend the look to anyone. A regulated buyer never spots inconsistency first.
**You are ready for this when.** `02-market/brand/brand-foundations.md` exists.

## Before you start
Read `02-market/brand/brand-foundations.md` (archetype, tone, values, name) and `.spark/state.json` (`founder`, `idea`, `business_type`). Open `${CLAUDE_SKILL_DIR}/references/palette-and-fonts.md` (colour roles, pairings menu, token shape) and `${CLAUDE_SKILL_DIR}/references/logo-concepts.md` (the logo conversation).

A working discussion, about 25 minutes in three choices: logo, colours, fonts. The founder picks each from real options with a recommendation on the table; their taste wins everywhere the checks allow. Non-negotiable: the palette must pass WCAG AA. The scripts refuse a failing palette. Founder already has a logo? Drop it at `02-market/brand/logo.svg`, note it in DECISIONS.md, and start at step 4.

## Steps
1. **Ask the three logo questions** from `logo-concepts.md`: what should it make people feel, what do you hate and envy, where will it live most. Reflect the answers back.
2. **Design three concepts as SVG**, one of each shape (wordmark, monogram or mark, combination), following the craft rules in the reference. Save to `02-market/brand/concepts/`, then build the choice sheet:
   `python3 ${CLAUDE_SKILL_DIR}/scripts/concept_sheet.py --dir 02-market/brand/concepts --out 02-market/brand/logo-concepts.html`
3. **The founder picks one and you refine it, twice at most.** Round one changes what they name; round two trims. Save the winner as `02-market/brand/logo.svg` (transparent background) and log the choice in DECISIONS.md: which concept won and why the others lost.
4. **Choose colours.** Offer two or three palette directions tied to the archetype, one sentence each, with a recommendation. Fill the five roles (`surface`, `ink`, `primary`, `accent`, `muted`) from the sector-safe starts in the reference. Text roles must clear 4.5:1 on surface, `accent` 3.0:1: a pale favourite lives as `accent`, never as text.
5. **Choose fonts.** Offer the three pairings from the reference by feel (considered, modern, editorial); the founder picks in a minute. System stacks only: zero load, no licence. A signature web font is a post-launch spend, noted and moved past.
6. **Write the tokens file** `02-market/brand/brand-tokens.json` in the reference shape: `name`, five `colours` as hex, two `fonts`, `tone`, `tagline`.
7. **Check and build.** `python3 ${CLAUDE_SKILL_DIR}/scripts/check_contrast.py --tokens 02-market/brand/brand-tokens.json`, darken and rerun on any FAIL. Then `python3 ${CLAUDE_SKILL_DIR}/scripts/build_identity.py --tokens 02-market/brand/brand-tokens.json`: it keeps your chosen `logo.svg` and writes `brand-board.html` (pass `--force-wordmark` only if no concept was chosen and you want the generated fallback).
8. **Eyeball the board together.** Open `brand-board.html`. Does it look like the foundations? One round of corrections, then an explicit yes. Hand off to `brand-register`, which locks this into the canonical `.spark/brand/brand.json`; the brand book skill then builds the full kit from it. Do not skip either.

## The artefact
Writes `02-market/brand/concepts/` (three SVG concepts) and `02-market/brand/logo-concepts.html` (the choice sheet); `02-market/brand/logo.svg` (the chosen master, transparent background); `02-market/brand/brand-tokens.json` (the single script input); `02-market/brand/brand-board.html` (palette with measured contrast, type specimen, logo, tone line). Good: the founder can say why each piece won.

## Done when
All five true: three concepts exist and one is chosen as `logo.svg` (or the founder's own logo sits there, logged); `check_contrast.py` exits 0 with every text role at 4.5:1 and accent at 3.0:1; exactly two fonts chosen from a real choice; `brand-tokens.json` is valid JSON with five colours and two fonts; the founder has said yes to the board.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d2-visual-identity \
  --artefact 02-market/brand/brand-tokens.json \
  --result "logo chosen from 3 concepts, AA pass, 5 colours, 2 fonts"
```
Log the logo and palette calls in DECISIONS.md: which concept and colours won, why the others lost.

## If it goes wrong
On an AA fail the scripts write nothing and print the ratio: darken the colour, or move a pale brand colour to `accent` and pick a darker `primary`. Founder cannot choose between two concepts: ask which they would put on an invoice today, and park the loser in DECISIONS.md as the v2 candidate. Two refinement rounds done and still itchy: ship it; the proposition sells, not the mark. Tokens will not parse: check the shape in `palette-and-fonts.md` for a trailing comma or missing quote.
