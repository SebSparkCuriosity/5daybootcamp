---
name: Brand Register
description: Locks your visual identity into one canonical file. Writes .spark/brand/brand.json and a stable logo on Day 2, after d2-visual-identity.
when_to_use: Day 2, right after d2-visual-identity. Run before any deck, brochure or proposal, which read only from here.
---

# Brand Register

**What this does.** Writes your Day 2 identity into one canonical file, `.spark/brand/brand.json`, plus a stable logo at `.spark/brand/logo.svg`, after checking the palette is legible.
**Why it matters.** Pick your colours and fonts once, in one place, so every document you build this week looks like the same company instead of drifting into three brands by Friday.
**You are ready for this when.** `d2-visual-identity` has run and `02-market/brand/` holds at least a colour, two font names and a logo.

## Before you start
Reads `02-market/brand/` and `.spark/state.json` (via journey-state, for founder name and business type).
Guardrail: do not invent a brand. If the identity work is thin (no logo, no colours), stop and finish `d2-visual-identity` first.

## Steps
1. Read `02-market/brand/`. Pull the primary and secondary colour, the heading and body font, the logo file, and any tone line or tagline. Decide anything missing with the founder now.
2. Get colours as hex (`#0B3D2E`, not "dark green"). If d2 gave only a swatch, read the hex off it or ask.
3. Name fonts exactly as a designer types them (`Fraunces`, `Inter`). One font is fine; leave the other empty rather than guessing.
4. Write a one-sentence tone line in Spark voice and a one-line tagline.
5. Build and validate in one command (run from project root, or pass `--root`):
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/build_brand.py --root . \
     --primary '#0B3D2E' --secondary '#C9A227' \
     --font-heading 'Fraunces' --font-body 'Inter' \
     --logo 02-market/brand/logo.svg \
     --tone 'Direct, warm, no jargon; we put a number on everything.' \
     --tagline 'Idea to system in five days.'
   ```
6. Read the printed contrast ratios. If the primary FAILS (below 4.5:1) the script wrote nothing: pick a darker shade and run again. Every Spark document is white-backgrounded.
7. No business-path branch. Software, hardware and services all get the same one brand file.

## The artefact
- `.spark/brand/brand.json`: hex primary and secondary, heading and body fonts, logo path, one-line tone, tagline, and a `contrast` block of the measured WCAG ratios. Field list in `${CLAUDE_SKILL_DIR}/references/brand-json-schema.md`.
- `.spark/brand/logo.svg`: logo copied to one stable path.

Next stop after this is `d2-brand-book`, which derives the full logo kit and the brand book from what you just locked.

## Done when
Script exits 0 and prints "brand.json validates": `brand.json` has a non-empty `primary`, at least one non-empty font, `logo` set to `.spark/brand/logo.svg`, a non-empty `tone`, and `contrast.primary.on_white` at 4.5:1 or higher. `.spark/brand/logo.svg` exists.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill brand-register \
  --artefact .spark/brand/brand.json \
  --result "AA pass, primary <hex> at <ratio>:1"
```
Then record the choice for the paper trail:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --decision "Locked brand: primary <hex>, fonts <heading>/<body>" \
  --rationale "<one line on why these colours and fonts fit the segment>"
```

## If it goes wrong
Primary fails AA: darken it past 4.5:1 on white, run again; keep a pale colour as `secondary` instead.
Logo missing: script writes `brand.json` and records the standard path, then warns. Drop the logo into `02-market/brand/` and re-run with `--logo`.
`02-market/brand/` empty: do not run; finish `d2-visual-identity` first.
