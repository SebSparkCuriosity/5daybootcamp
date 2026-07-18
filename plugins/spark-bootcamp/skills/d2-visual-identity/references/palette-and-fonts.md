# Palette and fonts: the pragmatic reference

You are not designing for an award. You are building an identity a non-designer can
ship today, that loads instantly, works offline, and passes a regulator's eye on a
projector. That rules out most of what a design agency would sell you. Good.

## The five colour roles

Fill exactly these five. Every document reads them by role, not by name, so you never
have to decide "which green" again.

| Role | What it does | The bar |
| --- | --- | --- |
| `surface` | The background. Almost always white. | n/a |
| `ink` | Body text. Very dark, near-black, tinted towards your primary. | 4.5:1 on surface |
| `primary` | Headings, links, the logo tile. Your brand colour. | 4.5:1 on surface |
| `accent` | Buttons, rules, one highlight. Used big, rarely as small text. | 3.0:1 on surface |
| `muted` | Secondary text, captions, borders. | 4.5:1 on surface |

Two colours do the heavy lifting: `primary` and `accent`. `ink` and `muted` are
near-neutrals. That is the whole palette. Resist a sixth.

## Why WCAG AA, and why we refuse to skip it

AA is the legal accessibility bar in the UK and the one a regulated buyer's own site
must meet. A ratio of 4.5:1 means normal text stays readable for the roughly 1 in 12
men with some colour-vision deficiency, and for everyone squinting at a shared screen.
The gold that looks premium on your Mac often sits at 2.4:1 on white and vanishes on a
projector. The build script measures it and refuses to ship a failure. That is the
feature, not the friction.

Quick rule: if a colour carries words a buyer must read, it must clear 4.5:1. If it is
a big block, a button fill or a rule, 3.0:1 is honest. A pale, pretty colour is welcome
as `accent`; it is never allowed as `ink`.

## Picking a primary that passes

Start from the feeling your archetype and tone set, then go dark enough to pass.

- Trust, finance, law, fund admin: deep green (`#0B3D2E`), navy (`#12294B`), slate
  (`#243447`). All clear 4.5:1 comfortably. Deep and calm reads as safe hands.
- Hospitality, construction, trades: burnt orange (`#9A3B12`), oxblood (`#6E1E1E`),
  forest (`#1F3D2B`). Warm, grounded, still legible.
- Accent: one warmer or brighter note used sparingly. Darken it until it clears 3.0:1.
  A rich amber (`#8A6D0A`) passes; a bright gold (`#C9A227`) does not.

If your heart is set on a pale brand colour, keep it as `accent` and choose a darker
sibling for `primary`. You lose nothing a buyer will notice.

## Fonts: use what every computer already has

Do not download a font this week. Two system-safe stacks cover everything, load with
zero delay, need no licence, and render identically on the buyer's machine. This is the
Spark default and you should take it unless you have a strong reason not to.

- Heading (serif, feels considered): `Georgia, 'Times New Roman', serif`
- Body (sans, feels clean and modern): `system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`

Offer the founder these three pairings by feel, one line each, and let them pick:

1. **Considered** (trust, law, finance): heading `Georgia, 'Times New Roman', serif`,
   body `system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`.
2. **Modern** (software, product): heading `'Segoe UI', system-ui, -apple-system, Roboto, Helvetica, Arial, sans-serif` set bold and large, body the same stack at text size.
3. **Editorial** (advisory, premium services): heading `Palatino, 'Palatino Linotype', 'Book Antiqua', Georgia, serif`, body `Verdana, Geneva, Tahoma, sans-serif` set slightly small.

That is two fonts. One for headings, one for body. You do not need a third. A web font
from a CDN adds load time, a licence question and a point of failure, for a difference
your buyer will not clock in a five-day sprint. If you genuinely need a signature web
font, that is a post-launch spend decision, not a Day 2 one. Flag it and move on.

## The tokens file shape

Write `02-market/brand/brand-tokens.json` in this shape. The build script reads it.

```json
{
  "name": "Ledgerly",
  "colours": {
    "ink": "#12211B",
    "primary": "#0B3D2E",
    "accent": "#8A6D0A",
    "muted": "#5B6B63",
    "surface": "#FFFFFF"
  },
  "fonts": {
    "heading": "Georgia, 'Times New Roman', serif",
    "body": "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
  },
  "tone": "Direct, warm, no jargon; we put a number on everything.",
  "tagline": "Trust accounts reconciled by Friday."
}
```

`name`, the five colours and the two fonts are required. `tone` and `tagline` come
straight from brand-foundations.md and make the brand board useful to a future writer.
