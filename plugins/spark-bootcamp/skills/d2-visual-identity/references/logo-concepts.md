# The logo conversation: three concepts, one choice, two rounds

You are designing with the founder, not for them. The logo is the one identity decision
they will look at every day, so they choose it from real options, out loud, in about 15
minutes. No design tools, no spend: every concept is clean SVG you write by hand.

## Ask before you draw (3 questions, one at a time)

1. "When someone sees your logo for the first time, what should they feel in one word?"
   (Safe hands? Sharp? Warm? Their word steers every choice below.)
2. "Show me or describe a logo you hate, and one you envy. What is it about each?"
3. "Where will it live most: an email signature, a report header, an app corner, a van?"
   (The smallest home decides how simple the mark must be.)

Reflect their answers back before drawing anything.

## The three concepts (always these three shapes, never three of a kind)

Draw one of each so the choice is between genuinely different ideas, not shades of one:

- **A. Wordmark.** The name set with care: weight, spacing, one deliberate detail (a
  clipped letter, an accent full stop, a joined pair). Best when the name itself sells.
- **B. Monogram or abstract mark.** An initial tile, a geometric mark, or a simple
  pictorial shape drawn from the idea's world (a ledger line, a keystone, a channel
  marker). Paired small with the name. Best when the name is long or the brand needs
  a mark that works alone at 16 pixels.
- **C. Combination.** Mark plus wordmark locked together, the safest all-rounder.

## SVG craft rules (non-negotiable)

- Geometric and few-pointed: rects, circles, simple paths. No gradients, no filters,
  no clip-path trickery, no embedded raster images.
- Must survive one colour: the mark drawn in `primary` alone must still read.
- Must survive 16 pixels: squint test at favicon size before showing it.
- Generic or system font families only inside the SVG, so it renders identically
  everywhere without a font download.
- Use the palette roles from brand-tokens.json (`primary`, `accent`, `ink`), never
  hard-coded colours the palette does not hold.
- viewBox tight to the artwork, background transparent (no surface rect in the master).

## Showing and choosing

Save the three as `02-market/brand/concepts/concept-a.svg`, `-b.svg`, `-c.svg`, then
build the side-by-side sheet:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/concept_sheet.py --dir 02-market/brand/concepts \
  --out 02-market/brand/logo-concepts.html
```

The sheet shows each concept large, at 32 pixels, and on a dark panel. Open it with the
founder and ask which one they would be proud to put on an invoice. One pick.

## Refining (two rounds, then stop)

Round one: change what they name ("heavier", "less corporate", "closer letters").
Round two: fine trim. After two rounds the improvements get imaginary and the day moves
on: ship it, note any wish in DECISIONS.md as a post-launch tweak. Save the winner as
`02-market/brand/logo.svg` (the master, transparent background).

## The side door: an existing logo

A founder who already has a logo skips all of this. Drop the file at
`02-market/brand/logo.svg` (SVG preferred; a high-resolution PNG works but limits the
kit) and carry on from the palette step. Note the provenance in DECISIONS.md so the
brand book credits it correctly.
