---
name: Brand Register
description: Locks your visual identity into one file every later document reads. Turns the Day 2 identity work into .spark/brand/brand.json and a stable logo. Use on Day 2 after d2-visual-identity.
when_to_use: Day 2 market, straight after d2-visual-identity. Run it before you build any deck, brochure, sales deck or proposal, because those skills read only from here.
---

# Brand Register

**What this does.** Takes your Day 2 identity work and writes it into one canonical file, `.spark/brand/brand.json`, plus a stable logo at `.spark/brand/logo.svg`, after checking the palette is legible.
**Why it matters.** Pick your colours and fonts once, in one place, and every document you build this week looks like the same company. Skip this and your deck, brochure and proposal drift into three different brands by Friday, which is exactly what a regulated buyer notices first. This file is the single source of truth: every later skill reads from it and nowhere else.
**You are ready for this when.** `d2-visual-identity` has run and there is something in `02-market/brand/`: at minimum a colour or two, two font names and a logo file.

## Before you start
Reads from the founder's project:
- `02-market/brand/` (whatever d2-visual-identity produced: colour notes, font choices, a logo file)
- `.spark/state.json` (via the journey-state helper, for the founder name and business type)

One guardrail: this skill does not invent a brand. If the identity work is thin (no logo, no colours), stop and finish `d2-visual-identity` first. A register built on guesses is worse than none, because every document downstream will inherit the guess.

## Steps
1. Read `02-market/brand/`. Pull out the primary colour, the secondary colour, the two font names (one for headings, one for body), the logo file and, if it is there, a tone line and a tagline. If any of these is missing, decide it now with the founder rather than leaving a blank.
2. Get the colours as hex. `#0B3D2E`, not "dark green". If d2 gave you a swatch image and no hex, read the hex off it or ask the founder. Documents need the exact value.
3. Name the two fonts exactly as a designer types them, for example `Fraunces` for headings and `Inter` for body. One font is fine if that is the real choice; the field for the other stays empty, it does not get a guess.
4. Write the tone line in Spark voice: one sentence that tells a future writer how to sound. For example, "Direct, warm, no jargon; we put a number on everything." Keep the tagline to one line.
5. Build and validate the file in one command. The script checks the palette, copies the logo to a stable path, and writes `brand.json`:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/build_brand.py --root . \
     --primary '#0B3D2E' --secondary '#C9A227' \
     --font-heading 'Fraunces' --font-body 'Inter' \
     --logo 02-market/brand/logo.svg \
     --tone 'Direct, warm, no jargon; we put a number on everything.' \
     --tagline 'Idea to system in five days.'
   ```
   Run it from the founder's project root, or pass `--root /path/to/project`.
6. Read what the script printed. It shows the primary's contrast on a white page and the secondary's. If the primary FAILS (below 4.5:1), it wrote nothing on purpose: pick a darker shade of your primary and run again. This is not fussiness. Every Spark document is white-backgrounded, and a heading nobody can read fails the regulator test on sight.
7. Colours and fonts do not branch by business path. Software, hardware and services founders all get the same one brand file, because the whole plugin reads from this one place. What differs later is what you build, not how it looks.

## The artefact
Writes two files:
- `.spark/brand/brand.json` (JSON): primary and secondary colours as hex, heading and body font names, the logo path, a one-line tone statement, the tagline, and a `contrast` block recording the WCAG ratios the script measured. Full field list in `${CLAUDE_SKILL_DIR}/references/brand-json-schema.md`.
- `.spark/brand/logo.svg`: your logo copied to one stable path, so every document points at the same file even if you rename the original.

What good looks like: a stranger opens `brand.json`, sees a real hex primary, two named fonts, a tagline that sounds like you, and a contrast block proving the palette was tested rather than guessed.

## Done when
The script exits 0 and prints "brand.json validates". Concretely: `.spark/brand/brand.json` exists with a non-empty `primary`, at least one non-empty font, `logo` set to `.spark/brand/logo.svg`, a non-empty `tone` line, and `contrast.primary.on_white` at 4.5:1 or higher (AA passed). `.spark/brand/logo.svg` exists.

## Log it
Append one line to CHANGELOG.md (the logbook helper also registers the artefact in state.json):
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill brand-register \
  --artefact .spark/brand/brand.json \
  --result "AA pass, primary <hex> at <ratio>:1"
```
Then record the choice, so the palette decision has a paper trail:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --decision "Locked brand: primary <hex>, fonts <heading>/<body>" \
  --rationale "<one line on why these colours and fonts fit the segment>"
```
Replace the angle-bracket values with what the build script printed.

## If it goes wrong
If the primary fails AA, the script writes nothing and tells you the ratio. Darken the primary until it clears 4.5:1 on white, then run again. If you are wedded to a pale brand colour, keep it as the `secondary` (accent) and choose a darker primary for text.

If the logo source is missing, the script still writes `brand.json` and records the standard logo path, then warns you. Drop the real logo into `02-market/brand/`, re-run with `--logo`, and it will copy it into place.

If `02-market/brand/` is empty, do not run this skill. Go back and finish `d2-visual-identity`; this skill only registers work that already exists.
