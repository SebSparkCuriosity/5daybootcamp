---
name: House Style
description: The shared kit every Spark document skill reuses so the deck, brochure, one-pager and landing page all look like one company. Not user-invocable; other skills call it.
when_to_use: Whenever another skill builds a document, deck, brochure, one-pager or landing page and needs the Spark voice checklist, a branded template or the deck builder. Never triggered directly by the founder.
user-invocable: false
---

# House Style

**What this does.** Owns the four shared assets every document skill borrows: the voice checklist, the one-page template, the landing-page template and the deck builder.
**Why it matters.** A founder who ships a pitch deck, a sales deck, a brochure and a landing page in one week can end up with four documents that look like four different companies. That reads as amateur, and in a regulated Jersey sector amateur loses the deal. One shared kit means everything the founder sends out looks like it came from the same firm, because it did.
**You are ready for this when.** Another skill has called you. This skill produces no artefact of its own and the founder never runs it directly.

## Before you start
Read `.spark/brand/brand.json` for the founder's tokens (colours, fonts, name, logo, contact). If it is missing or half-written, do not stop: the templates and the deck builder fall back to safe Spark defaults and carry on. The default typeface stack is system-safe on purpose: Arial and Calibri for text, Georgia for the occasional serif, so a deck opens the same on the founder's laptop and the prospect's.

The four assets and who uses them:

1. `references/voice-checklist.md`: the Spark voice rules as a checklist. Any skill writing prose applies it before it saves the artefact.
2. `references/one-pager.md`: a branded one-page markdown template with token placeholders. The brochure and proposal skills fill it in.
3. `references/landing.html`: a clean, accessible, responsive single-page HTML template with a working lead-capture form, light and dark aware, brand tokens injected. The GTM and sale skills use it as the founder's live page.
4. `scripts/build_deck.py`: reads a YAML content file plus `brand.json` and emits a `.pptx`. If `python-pptx` is not installed it prints the install line and emits a self-contained reveal.js HTML deck instead, so the founder is never blocked.

## Steps
These are the instructions the calling skill follows. Pick the asset that matches the job.

### Applying the voice checklist (every prose artefact)
1. Read `${CLAUDE_SKILL_DIR}/references/voice-checklist.md`.
2. Run every line of the artefact against it before saving. The two hard rules first: British spelling throughout, and zero em dashes anywhere. Then the tone rules.
3. If the artefact fails a line, fix the artefact, not the checklist.

### Filling the one-pager (brochure, proposal)
1. Copy `${CLAUDE_SKILL_DIR}/references/one-pager.md` to the artefact path the calling skill owns.
2. Replace every `{{token}}` with a real value. Pull `{{brand.name}}`, `{{brand.primary}}`, `{{brand.contact_email}}` and the rest from `brand.json`. Where a token has no value in `brand.json`, use the fallback noted in the template, never a raw `{{token}}` left in the file.
3. Run the voice checklist over the finished prose.

### Building a landing page (GTM, sale)
1. Copy `${CLAUDE_SKILL_DIR}/references/landing.html` to the artefact path the calling skill owns.
2. Inject brand tokens into the `:root` CSS variables at the top and swap the copy blocks marked `<!-- COPY -->`.
3. The lead-capture form posts to a `data-endpoint` attribute on the `<form>`. Set it to the founder's form handler (a Supabase table endpoint, a Formspree URL, or similar). Until an endpoint is set the form stores submissions in the browser and shows a thank-you state, so the page never looks broken in a demo.
4. Human-in-the-loop: the page is not published and no money is spent from this skill. The GTM or sale skill handles deploy and asks the founder for sign-off first.

### Building a deck (pitch deck, sales deck)
1. Write the slide content as a YAML file. The shape is documented at the top of `scripts/build_deck.py` and mirrored in `references/deck-content.example.yaml`.
2. Run the builder:

   ```
   python3 "${CLAUDE_SKILL_DIR}/scripts/build_deck.py" \
     --content <path-to-content.yaml> \
     --brand .spark/brand/brand.json \
     --out <artefact-path-without-extension>
   ```

3. If `python-pptx` is present you get a `.pptx`. If it is not, you get a `.html` reveal.js deck and a printed install line. Either way the calling skill has a finished deck to hand the founder.

## The artefact
None of its own. This skill is the shared kit: `references/voice-checklist.md`, `references/one-pager.md`, `references/landing.html`, `references/deck-content.example.yaml` and `scripts/build_deck.py`. Other skills write the artefacts and own their paths. What good looks like: two documents built through this kit, opened side by side, are obviously from the same company.

## Done when
The asset the calling skill needed was produced without error, and it passes its own numeric check: the voice checklist returns zero em dashes and zero American spellings on the flagged words; the one-pager and landing page contain zero unreplaced `{{token}}` placeholders; the deck builder exits 0 and writes exactly one deck file (`.pptx` or `.html`) with the requested slide count.

## Log it
This skill does not log on its own, because it produces no artefact of its own. The calling skill logs the artefact it built, using the logbook helper:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill <caller-skill-id> \
  --artefact <artefact-path> \
  --result "<numeric result, e.g. 12-slide deck built>"
```

and updates `.spark/state.json` through the journey-state helper. House Style never writes state or the changelog itself.

## If it goes wrong
If `brand.json` is missing or malformed, everything still runs on Spark defaults (primary `#0B5FEF`, ink `#12141A`, Arial/Calibri/Georgia). Tell the founder their brand tokens were not found so they can run the brand skill, then carry on rather than blocking. If `python-pptx` is missing, the deck builder self-substitutes the reveal.js HTML deck and prints `pip install python-pptx` for next time. If a template still shows a `{{token}}`, that is a bug in the calling skill: fill it before saving.
