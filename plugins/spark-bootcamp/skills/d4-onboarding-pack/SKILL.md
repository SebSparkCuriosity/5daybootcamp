---
name: Build The Onboarding Pack
description: Builds a 6-section onboarding pack with a week-1 timeline and named contact, exported to PDF. Use on Day 4 after intake is mapped.
when_to_use: Day 4, after d4-intake-process, when prospects can book but you have nothing to hand them once they say yes.
---

# Build The Onboarding Pack

**What this does.** Turns "you're in" into a document a client can hold: 6 sections, a week-1 timeline, a named human to email, exported to PDF.
**Why it matters.** A first week that feels handled is the cheapest retention you will ever buy, and in regulated Jersey sectors it doubles as evidence you take onboarding seriously.
**You are ready for this when.** `04-gtm/ops/intake-process.md` exists.

## Before you start
Read `04-gtm/ops/intake-process.md` (where intake ends) and `.spark/brand/brand.json` (name, colours, contacts). If `brand.json` is missing, the pack builds with plain styling; do not block on it.

Guardrail: the named contact must be a real person with a real inbox. Confirm the name and email with the founder before writing them in.

## Steps
1. Fix the six sections, in this order: **Welcome**, **What happens in week 1** (timeline), **What we need from you**, **Your named contact**, **How we work** (cadence, where things live), **What good looks like** (first outcome and how you measure it).
2. Welcome in three sentences: name the client, the outcome they bought, the date week 1 starts.
3. Week-1 timeline as five dated rows, Monday to Friday. Each row: day, what happens, who owns it. Be specific.
4. "What we need from you" as a short numbered checklist: access, documents, decision-maker time.
5. Name the contact: real first name, real email, honest response time (aim for "same working day"). Pull from `brand.json` where present.
6. Branch the "what good looks like" section by business path (below).
7. Run the export script to produce the PDF.

### For software
First outcome is the client live on the deployed slice. Timeline: access, data loaded, first use, check-in. "What good looks like" names the one metric the slice moves and where they see it.

### For hardware
First outcome is the pre-order confirmed and the prototype milestone made clear. Timeline: order confirmation, build or render dates, next update. "What good looks like" names the delivery or demo date.

### For services
First outcome is the first sample deliverable in their hands. Timeline: kick-off, information gathering, drafting, delivery. "What good looks like" names the deliverable and the standard.

## The artefact
Writes `04-gtm/onboarding-pack.pdf` (from a markdown draft at `04-gtm/onboarding-pack.md`). Use `${CLAUDE_SKILL_DIR}/references/onboarding-pack-template.md` as the structure and fill every placeholder. Then run:
```
python3 ${CLAUDE_SKILL_DIR}/scripts/md_to_pdf.py 04-gtm/onboarding-pack.md 04-gtm/onboarding-pack.pdf
```

## Done when
All 6 sections, the timeline has 5 dated rows, a real named contact with email is present, and `04-gtm/onboarding-pack.pdf` exists. (No PDF library: the script writes `04-gtm/onboarding-pack.html` instead; that counts, note it.)

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d4-onboarding-pack \
  --artefact 04-gtm/onboarding-pack.pdf \
  --result "6 sections, 5-day week-1 timeline, named contact"

python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"4":{"outcome":"onboarding pack ready to hand to first client"}}}'
```

## If it goes wrong
No PDF library (weasyprint or fpdf): the script falls back to HTML and prints how to install one; the HTML is fine to send. If `brand.json` is missing, styling defaults to plain text, which reads cleanly. If you cannot name a real contact, decide who owns new clients before sending anyone a pack.
