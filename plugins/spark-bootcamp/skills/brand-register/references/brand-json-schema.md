# brand.json, the one source of brand truth

Every deck, brochure, sales deck and proposal reads its look from this file and
nowhere else. If a colour or font is not in here, no document may use it. That
is the whole point: one file, one look, no drift.

Path: `.spark/brand/brand.json`

## Shape

```json
{
  "primary": "#0B3D2E",
  "secondary": "#C9A227",
  "fonts": {
    "heading": "Fraunces",
    "body": "Inter"
  },
  "logo": ".spark/brand/logo.svg",
  "tone": "Direct, warm, no jargon. We put a number on everything.",
  "tagline": "Idea to system in five days.",
  "contrast": {
    "primary": {
      "colour": "#0B3D2E",
      "on_white": 12.2,
      "readable_text": "#FFFFFF",
      "readable_text_ratio": 12.2,
      "passes_aa_normal_on_white": true,
      "passes_aa_large_on_white": true
    },
    "secondary": {
      "colour": "#C9A227",
      "on_white": 2.42,
      "readable_text": "#000000",
      "readable_text_ratio": 8.68,
      "passes_aa_normal_on_white": false,
      "passes_aa_large_on_white": false
    }
  }
}
```

## Fields

- `primary`: hex, uppercase, `#RRGGBB`. Your dominant brand colour and your
  brand text colour. Must reach 4.5:1 as text on a white page.
- `secondary`: hex. An accent for fills, bars and highlights. It may sit below
  AA on white (bright accents usually do); use `readable_text` for text on top
  of it.
- `fonts.heading` / `fonts.body`: the two font names, exactly as a designer
  would type them (for example `Fraunces`, `Inter`). At least one must be set.
- `logo`: always `.spark/brand/logo.svg`. The build script copies your source
  logo there so every document points at one stable path.
- `tone`: one line, in Spark voice, that tells a writer how to sound.
- `tagline`: the one line that goes under the logo.
- `contrast`: written by the build script, not by hand. It is the audit trail
  for the WCAG check: the exact ratios, so a regulator or client can see the
  palette was tested, not guessed.

## The contrast rule, in plain English

WCAG AA asks normal text to reach a contrast ratio of at least 4.5:1 against
its background. Spark documents are white, so the primary (your text colour)
must clear 4.5:1 against white. The build script refuses to write a palette
whose primary fails, because a brand nobody can read is not a brand. The
secondary is an accent and is reported, not gated: pair it with the
`readable_text` colour the script names.
