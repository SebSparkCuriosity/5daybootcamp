---
name: Visual Identity
description: Turn your brand foundations into a palette, two fonts and a simple logo a non-designer can ship. Use on Day 2 after brand-foundations, before brand-register.
when_to_use: Day 2 market work, straight after d2-brand-foundations and before brand-register. The one skill that produces something you can see.
---

# Visual Identity

**What this does.** Turns your written brand into things you can see: a five-colour palette that passes accessibility, two system-safe fonts, and one SVG wordmark logo, plus a one-page brand board that shows them off.
**Why it matters.** Your foundations file says how you sound. This says how you look, and it does it in an hour, not a fortnight with a designer. Pick your colours and fonts once, prove they are legible, and every page, deck and proposal downstream looks like the same firm. A regulated buyer notices inconsistency before they notice anything else.
**You are ready for this when.** `02-market/brand/brand-foundations.md` exists.

## Before you start
Read these first:
- `02-market/brand/brand-foundations.md`: your archetype, tone, values and resolved name. The look must fit the feeling you already wrote down.
- `.spark/state.json` (via the journey-state helper): your `founder`, `idea` and `business_type`.

Open the reference before you choose anything: `${CLAUDE_SKILL_DIR}/references/palette-and-fonts.md`. It gives you the five colour roles, safe primaries per sector, the two default font stacks and the exact tokens shape. It saves you every dead end.

One rule that is not negotiable: the palette must pass WCAG AA. The scripts here refuse to build a palette that fails. That is deliberate. A heading nobody can read on a projector fails the buyer test on sight, and AA is the accessibility bar a regulated firm's own site must meet.

## Steps
1. **Name your five colours by role, not by taste.** Fill `surface` (your background, almost always white), `ink` (body text, near-black), `primary` (headings, links, the logo), `accent` (buttons and one highlight) and `muted` (secondary text and borders). Two colours carry the brand, `primary` and `accent`. The other three are near-neutrals. Do not add a sixth. Sector-safe starting points are in the reference: deep green, navy or slate for finance, trust and law; warmer earth tones for hospitality and trades.

2. **Go dark enough to pass.** Text roles (`ink`, `primary`, `muted`) must clear 4.5:1 on your surface. `accent` must clear 3.0:1. The pretty pale colour you had in mind almost certainly fails as text; keep it as `accent` and pick a darker sibling for `primary`. You will check this in step 5, so do not agonise now, just lean darker.

3. **Take the two default fonts unless you have a real reason not to.** Heading `Georgia, 'Times New Roman', serif`; body `system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`. These sit on every computer already: zero load time, no licence, no CDN, identical on the buyer's machine. That is two fonts, one for headings, one for body. You do not need a third. A downloaded web font is a post-launch spend decision, not a Day 2 one. Flag it and move on.

4. **Write the tokens file.** Create `02-market/brand/brand-tokens.json` in the exact shape in the reference: `name`, the five `colours` as hex, the two `fonts`, and `tone` plus `tagline` copied from your foundations file. Hex values, `#0B3D2E`, not "dark green". The scripts read this file and nothing else.

5. **Check the palette.** Run the validator. It reads your tokens and tells you, in plain English, which colours pass AA and which fail, with the exact ratio:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/check_contrast.py \
     --tokens 02-market/brand/brand-tokens.json
   ```
   If anything says FAIL, darken that colour and run again. Do not proceed on a fail. A green heading at 3.1:1 looks fine to you and disappears for the buyer squinting at a shared screen.

6. **Build the logo and brand board.** Once the check passes, run the builder. It writes `logo.svg` (a clean wordmark: your initial in a rounded tile, the name in ink, an accent full stop) and `brand-board.html` (palette swatches with hex and measured contrast, a font specimen, the logo and your tone line):
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/build_identity.py \
     --tokens 02-market/brand/brand-tokens.json
   ```
   The builder re-checks AA itself and refuses to write if the palette fails, so you cannot ship a broken palette by accident.

7. **Eyeball the board.** Open `02-market/brand/brand-board.html` in a browser. Does it look like the firm you described in your foundations file? A trust company should not look like a beach cafe. If the accent is shouting, tone it down. If the wordmark reads wrong, adjust the name capitalisation in the tokens and rebuild. Ten minutes here saves a week of drift.

8. **Hand off to brand-register.** This skill produces the raw identity in `02-market/brand/`. The next skill, `brand-register`, locks it into the one canonical file every later document reads. Do not skip it, or your deck and proposal will drift into different brands by Friday.

### Where each path uses this
The palette, fonts and logo do not branch by business type. Software, hardware and services founders all get the same one identity, because consistency is the whole point. What differs is where the assets land later, so keep it in mind as you eyeball the board:

- **For software:** the logo sits in your app header and the deployed page's top-left. Check it reads at small sizes.
- **For hardware:** the logo fronts your pre-order or waitlist page and sits on the CAD render or mock. Check it works on a photo background, not just white.
- **For services:** the logo tops your sample deliverable and your intake page. Check it prints cleanly in black and white on a proposal cover.

## The artefact
Writes three files into `02-market/brand/`:
- `brand-tokens.json` (JSON): `name`, five `colours` as hex, two `fonts`, `tone`, `tagline`. The single input to both scripts.
- `logo.svg` (SVG): one portable wordmark using a generic font family, so it renders anywhere with no font install.
- `brand-board.html` (self-contained HTML): a one-page reference showing the palette with measured contrast ratios, a type specimen, the logo and your tone line. No external files, opens offline.

What good looks like: a stranger opens the brand board, sees five real hex colours each marked PASS, two named fonts, a legible wordmark and a tone line that sounds like you, and could build an on-brand page from it without asking you a single question.

## Done when
All four are true:
- The palette passes WCAG AA: `check_contrast.py` exits 0 and every text role clears 4.5:1, the accent clears 3.0:1.
- There are exactly two fonts set, one heading and one body.
- One SVG wordmark exists at `02-market/brand/logo.svg` and is well-formed.
- `02-market/brand/brand-tokens.json` is valid JSON with the five colours and two fonts filled.

## Log it
Append one line to CHANGELOG.md via the logbook helper, with the numeric result:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d2-visual-identity \
  --artefact 02-market/brand/brand-tokens.json \
  --result "AA pass, 5 colours, 2 fonts, 1 wordmark"
```
Then register the artefacts in the journey state:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --append-artefact '{"skill": "d2-visual-identity", "path": "02-market/brand/brand-board.html", "result": "brand board built, palette passes AA"}'
```
If the palette was a genuine call between options, write one line in `DECISIONS.md`: the primary and accent you chose and why the pale option lost.

## If it goes wrong
If a colour fails AA, the scripts write nothing and print the exact ratio. Darken the failing colour until it clears its bar, then run the check and the builder again. If you are wedded to a pale brand colour, move it to `accent` and choose a darker `primary`; the reference lists sector-safe darker options.

If you cannot settle the logo, ship the plain wordmark the builder produces. It is clean, legible and enough for a five-day sprint. A logo you refine after launch beats a week spent on a logo. The proposition sells, not the mark.

If the tokens file will not parse, the scripts tell you it is not valid JSON and stop. Re-check against the shape in `${CLAUDE_SKILL_DIR}/references/palette-and-fonts.md`, usually a trailing comma or a missing quote.
