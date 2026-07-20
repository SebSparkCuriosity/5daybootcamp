---
name: Build The Brand Book
description: Assembles the locked identity into a full brand kit (logo variants, favicon, PNG exports) and an 8-section brand book as HTML and PDF. Day 2, after brand-register.
when_to_use: Day 2, straight after brand-register locks brand.json, before the pitch deck. Triggers on "brand book", "brand kit", "logo pack", "brand guidelines".
---

# Build The Brand Book

**What this does.** Turns the identity you chose into things you can hand over: a kit of logo variants (primary, mono, reversed, favicon, PNG exports where possible) and an 8-section brand book in HTML and PDF.
**Why it matters.** A brand that lives in one founder's head dies at the first freelancer, printer or new hire. This book is the handover: everything they need to make something look like you, on paper.
**You are ready for this when.** `.spark/brand/brand.json` exists (brand-register has run) and `02-market/brand/logo.svg` is the chosen master.

## Before you start
Reads `02-market/brand/brand-tokens.json`, `02-market/brand/logo.svg`, `.spark/brand/brand.json`, plus the judgement sources: `01-discovery/idea-brief.md` (the story section), `02-market/brand/brand-foundations.md` (values, archetype, tone sliders) and `02-market/messaging.md` (the pitch that seeds the voice example).

Ask, then draft (about 15 minutes total). The choices were made in visual-identity; this skill assembles, then walks the book with the founder. Nothing here is sent or spent.

## Steps
1. Copy `${CLAUDE_SKILL_DIR}/references/book-content-template.json` to `02-market/brand/book-content.json` and fill it from the sources above, in the founder's words, not yours. Two things to confirm out loud before writing: the email signature details (real name, real address) and the voice example.
2. Build kit and book in one pass from the project root:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/build_brand_book.py --root .
   ```
   It derives the logo variants from the chosen master, exports PNGs if a converter is on the machine, writes `brand-book.html`, and prints to `brand-book.pdf` via a headless browser where one exists. Read the `BOOK_RESULT` line.
3. Eyeball the derived variants in `02-market/brand/kit/`: recolouring is mechanical, so check the mono and reversed logos actually read. If one is wrong, fix the master SVG and re-run.
4. If `pdf=manual`, have the founder open `brand-book.html` in their browser and print to PDF (Cmd or Ctrl+P), saved as `02-market/brand/brand-book.pdf`. Two minutes, once. If PNG exports were skipped, `kit/png-export.html` downloads them from any browser, offline, whenever a platform demands one.
5. Walk the book with the founder, section by section, as if they were handing it to a freelancer tomorrow. One round of corrections (usually the story, the voice example or the signature), edit `book-content.json`, re-run the script. Get an explicit yes.

## The artefact
- `02-market/brand/kit/`: `logo-primary.svg`, `logo-mono.svg`, `logo-reversed.svg`, `favicon.svg`, a `png-export.html` that downloads PNGs from any browser, plus pre-baked `logo-primary-1200w.png`, `favicon-512.png`, `favicon-180.png`, `favicon-32.png` where a converter was on the machine.
- `02-market/brand/brand-book.html` and `02-market/brand/brand-book.pdf`: cover plus 8 sections (the brand, logo and rules, colour with measured contrast, typography, voice, applications, the kit index, keeping it), rendered from the filled `02-market/brand/book-content.json`.

Good: a freelancer who has never met the founder could produce an on-brand proposal from the book alone.

## Done when
1. The kit holds the four SVG variants and the founder has eyeballed mono and reversed.
2. `brand-book.html` exists with all 8 sections filled (no template placeholder text) and `brand-book.pdf` sits beside it.
3. The founder has said yes to the walked-through book.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d2-brand-book \
  --artefact 02-market/brand/brand-book.html \
  --result "brand book built, 8 sections, <N>-file kit, PDF <ok|manual>"
```

## If it goes wrong
Recoloured variant looks broken (a gradient or embedded image in the master): simplify the master SVG to flat fills, or hand-edit the variant once and note it. No headless browser and the founder cannot print today: the HTML is the artefact of record; log the PDF as owed and move to the pitch deck. Founder's own PNG-only logo: the kit keeps the PNG as primary, skips derived variants, and the book notes the limitation; suggest an SVG redraw as a post-launch task in DECISIONS.md.
