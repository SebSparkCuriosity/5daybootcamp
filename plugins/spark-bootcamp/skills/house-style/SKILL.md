---
name: House Style
description: The shared kit every Spark document skill reuses so deck, brochure, one-pager and landing page look like one company. Not user-invocable.
when_to_use: When another skill builds a document, deck, brochure, one-pager or landing page and needs the Spark voice, template or deck builder.
user-invocable: false
---

# House Style

**What this does.** Owns the four shared assets every document skill borrows: voice checklist, one-page template, landing-page template and deck builder.
**Why it matters.** One shared kit means everything the founder sends out in the week looks like it came from the same firm, which in a regulated Jersey sector is the difference between winning and losing the deal.
**You are ready for this when.** Another skill has called you. No artefact of its own, never run directly.

## Before you start
Read `.spark/brand/brand.json` for tokens (colours, fonts, name, logo, contact). If missing or half-written, carry on: everything falls back to safe Spark defaults. Default typeface stack is system-safe (Arial, Calibri, Georgia) so decks open identically on both laptops.

The four assets:
1. `references/voice-checklist.md`: Spark voice rules as a checklist, applied by any prose skill before saving.
2. `references/one-pager.md`: branded one-page markdown template with token placeholders (brochure, proposal).
3. `references/landing.html`: accessible responsive single-page HTML with lead-capture form, light/dark aware, tokens injected (GTM, sale).
4. `scripts/build_deck.py`: reads a YAML content file plus `brand.json`, emits `.pptx`; falls back to a self-contained reveal.js HTML deck if `python-pptx` is absent.

## Steps
The calling skill follows these. Pick the asset matching the job.

### Applying the voice checklist (every prose artefact)
1. Read `${CLAUDE_SKILL_DIR}/references/voice-checklist.md`.
2. Run every line of the artefact against it before saving. Hard rules first: British spelling, zero em dashes. Then tone.
3. On a fail, fix the artefact, not the checklist.

### Filling the one-pager (brochure, proposal)
1. Copy `${CLAUDE_SKILL_DIR}/references/one-pager.md` to the caller's artefact path.
2. Replace every `{{token}}` with a real value from `brand.json` (`{{brand.name}}`, `{{brand.primary}}`, `{{brand.contact_email}}` etc). No value: use the template's fallback, never leave a raw `{{token}}`.
3. Run the voice checklist over the finished prose.

### Building a landing page (GTM, sale)
1. Copy `${CLAUDE_SKILL_DIR}/references/landing.html` to the caller's artefact path.
2. Inject tokens into the `:root` CSS variables and swap the `<!-- COPY -->` blocks.
3. Set the `<form>` `data-endpoint` to the founder's handler (Supabase table, Formspree URL). Until set, the form stores submissions locally and shows a thank-you state so demos never look broken.
4. Human-in-the-loop: this skill does not publish or spend. The GTM or sale skill deploys after founder sign-off.

### Building a deck (pitch deck, sales deck)
1. Write slide content as a YAML file (shape documented atop `scripts/build_deck.py`, mirrored in `references/deck-content.example.yaml`).
2. Run:
   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/build_deck.py" \
     --content <path-to-content.yaml> \
     --brand .spark/brand/brand.json \
     --out <artefact-path-without-extension>
   ```
3. With `python-pptx` you get a `.pptx`; without, a `.html` reveal.js deck plus a printed install line.

## The artefact
None of its own. The kit: `references/voice-checklist.md`, `references/one-pager.md`, `references/landing.html`, `references/deck-content.example.yaml`, `scripts/build_deck.py`. Callers write and own their artefact paths. Good: two documents built through the kit are obviously from the same company.

## Done when
The needed asset was produced without error and passes its numeric check: voice checklist returns zero em dashes and zero American spellings on flagged words; one-pager and landing page contain zero unreplaced `{{token}}`; deck builder exits 0 and writes exactly one deck file with the requested slide count.

## Log it
This skill does not log. The calling skill logs its artefact:
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill <caller-skill-id> \
  --artefact <artefact-path> \
  --result "<numeric result, e.g. 12-slide deck built>"
```

## If it goes wrong
Missing or malformed `brand.json`: run on Spark defaults (primary `#0B5FEF`, ink `#12141A`, Arial/Calibri/Georgia) and tell the founder to run the brand skill. Missing `python-pptx`: the builder emits reveal.js HTML and prints `pip install python-pptx`. A surviving `{{token}}` is a caller bug: fill it before saving.
