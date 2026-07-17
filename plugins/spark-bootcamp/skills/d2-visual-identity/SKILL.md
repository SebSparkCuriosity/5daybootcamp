---
name: Visual Identity
description: Turn brand foundations into an AA-safe palette, two system fonts and one SVG wordmark. Day 2, after brand-foundations, before brand-register.
when_to_use: Day 2, after d2-brand-foundations, before brand-register. The one skill producing something you can see.
---

# Visual Identity

**What this does.** Turns your written brand into a five-colour AA-safe palette, two system fonts, one SVG wordmark and a one-page brand board.
**Why it matters.** This settles how you look in an hour, not a fortnight, so every page, deck and proposal downstream reads as the same firm, and a regulated buyer never spots inconsistency first.
**You are ready for this when.** `02-market/brand/brand-foundations.md` exists.

## Before you start
Read `02-market/brand/brand-foundations.md` (archetype, tone, values, name) and `.spark/state.json` via journey-state (`founder`, `idea`, `business_type`).
Open `${CLAUDE_SKILL_DIR}/references/palette-and-fonts.md`: colour roles, sector-safe primaries, default font stacks, exact token shape.
Non-negotiable: the palette must pass WCAG AA. The scripts refuse a failing palette.
Ask before you pick (5 minutes): offer two or three palette directions tied to the archetype, one sentence each, with a recommendation. The founder chooses in a minute; their taste wins everywhere the checks allow. Contrast is not a matter of taste.

## Steps
1. **Name five colours by role.** `surface` (background, usually white), `ink` (body text, near-black), `primary` (headings, links, logo), `accent` (buttons, one highlight), `muted` (secondary text, borders). Primary and accent carry the brand; no sixth. Sector-safe starts in the reference: deep green, navy or slate for finance, trust, law; warmer earth tones for hospitality and trades.
2. **Go dark enough to pass.** Text roles (`ink`, `primary`, `muted`) must clear 4.5:1 on surface; `accent` clears 3.0:1. A pale colour fails as text: keep it as `accent`, pick a darker `primary`.
3. **Take the two default fonts.** Heading `Georgia, 'Times New Roman', serif`; body `system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`. Zero load, no licence, no CDN. A web font is a post-launch spend, not a Day 2 one.
4. **Write the tokens file.** Create `02-market/brand/brand-tokens.json` in the reference shape: `name`, five `colours` as hex, two `fonts`, `tone`, `tagline`. Hex only (`#0B3D2E`). The scripts read this and nothing else.
5. **Check the palette.** `python3 ${CLAUDE_SKILL_DIR}/scripts/check_contrast.py --tokens 02-market/brand/brand-tokens.json`. On any FAIL, darken and rerun. Do not proceed on a fail.
6. **Build logo and board.** `python3 ${CLAUDE_SKILL_DIR}/scripts/build_identity.py --tokens 02-market/brand/brand-tokens.json`. Writes `logo.svg` (wordmark) and `brand-board.html`. It re-checks AA and refuses on failure.
7. **Eyeball the board.** Open `02-market/brand/brand-board.html`. Does it look like your foundations? Tone down a shouting accent; fix wordmark capitalisation in the tokens and rebuild.
8. **Hand off to brand-register.** It locks this raw identity into the one canonical file later documents read. Do not skip it.

### Where each path uses this
The identity does not branch; all three paths share it. Where assets land differs:
- **For software:** logo in app header and page top-left. Check it reads small.
- **For hardware:** logo on pre-order/waitlist page and CAD render or mock. Check it works on a photo background.
- **For services:** logo tops the sample deliverable and intake page. Check it prints in black and white.

## The artefact
Three files in `02-market/brand/`: `brand-tokens.json` (`name`, five hex `colours`, two `fonts`, `tone`, `tagline`; the single script input); `logo.svg` (portable wordmark, generic font family); `brand-board.html` (self-contained: palette with measured contrast, type specimen, logo, tone line). Good: a stranger could build an on-brand page from the board without asking a question.

## Done when
All four true: `check_contrast.py` exits 0, every text role clears 4.5:1 and accent clears 3.0:1; exactly two fonts (one heading, one body); a well-formed `02-market/brand/logo.svg` exists; `02-market/brand/brand-tokens.json` is valid JSON with five colours and two fonts filled.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d2-visual-identity \
  --artefact 02-market/brand/brand-tokens.json \
  --result "AA pass, 5 colours, 2 fonts, 1 wordmark"
```
If the palette was a genuine call, add one line to `DECISIONS.md`: primary and accent chosen, why the pale option lost.

## If it goes wrong
On an AA fail the scripts write nothing and print the ratio: darken the colour, or move a pale brand colour to `accent` and pick a darker `primary` (sector-safe options in the reference). If you cannot settle the logo, ship the plain wordmark; the proposition sells, not the mark. If the tokens will not parse, the scripts stop: re-check the shape in `${CLAUDE_SKILL_DIR}/references/palette-and-fonts.md` for a trailing comma or missing quote.
