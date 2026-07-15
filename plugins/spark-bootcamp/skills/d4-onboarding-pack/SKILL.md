---
name: Build The Onboarding Pack
description: Builds a 6-section onboarding pack that makes a new client's first week feel handled, with a week-1 timeline and a named contact, exported to PDF. Use on Day 4 after the intake process is mapped.
when_to_use: Day 4 go-to-market, after d4-intake-process, when you have a way for prospects to book but nothing to hand them once they say yes.
---

# Build The Onboarding Pack

**What this does.** Turns "you're in" into a document a new client can hold: 6 sections, a week-1 timeline they can follow, and a named human they can email, exported to a PDF.
**Why it matters.** The gap between a client saying yes and feeling looked after is where trust leaks out. A first week that feels handled is the cheapest retention you will ever buy, and in regulated Jersey sectors it doubles as evidence you take onboarding seriously. Say who does what, by when, and who to call. That is the whole job.
**You are ready for this when.** `04-gtm/ops/intake-process.md` exists.

## Before you start
Read these two files:
- `04-gtm/ops/intake-process.md`: how a prospect becomes a client, so the pack picks up exactly where intake ends.
- `.spark/brand/brand.json`: name, colours, contact details, so the pack looks like you and not a template.

If `brand.json` is missing, the pack still builds; it just uses plain styling. Do not block on it.

One guardrail: the named contact must be a real person with a real inbox. A pack that promises "your dedicated contact" and then bounces is worse than no pack. Confirm the name and email with the founder before you write them in.

## Steps
1. Fix the six sections. Every onboarding pack ships with the same six, in this order: **Welcome**, **What happens in week 1** (the timeline), **What we need from you**, **Your named contact**, **How we work** (communication, cadence, where things live), **What good looks like** (the first outcome and how you will measure it). Six sections is the number. Fewer and it feels thin, more and nobody reads it.
2. Write the welcome in three sentences. Name the client, name the outcome they bought, name the date week 1 starts. No throat-clearing.
3. Build the week-1 timeline as five dated rows, Monday to Friday. Each row: the day, what happens, and who owns it (you or them). This is the section clients actually read, so make it specific. "Mon: kick-off call, 30 mins, we send the link" beats "early in the week we align".
4. Write "what we need from you" as a short numbered checklist. Access, documents, a decision-maker's time. If you need it in week 1, it goes here.
5. Name the contact. A real first name, a real email, a real response time you can honestly hit (aim for "same working day"). Pull the details from `brand.json` where they exist.
6. Branch the "what good looks like" section by business path (below), because the first outcome differs.
7. Run the export script to produce the PDF.

### For software
The first outcome is the client live on the deployed slice. Timeline covers access provisioned, data loaded, first real use, and a check-in. "What good looks like" names the one metric the slice moves (for example "first 10 records processed by Friday") and where they will see it.

### For hardware
The first outcome is the client's pre-order confirmed and the prototype milestone they are waiting on made clear. Timeline covers order confirmation, expected build or render dates, and the next update they will receive. "What good looks like" names the delivery or demo date and what they get to see.

### For services
The first outcome is the first sample deliverable in their hands. Timeline covers kick-off, information gathering, drafting, and delivery of the sample. "What good looks like" names the deliverable and the standard you hold it to.

## The artefact
Writes `04-gtm/onboarding-pack.pdf` (PDF, exported from a markdown draft the script writes alongside it at `04-gtm/onboarding-pack.md`).

Run:
```
python3 ${CLAUDE_SKILL_DIR}/scripts/md_to_pdf.py 04-gtm/onboarding-pack.md 04-gtm/onboarding-pack.pdf
```

Use `${CLAUDE_SKILL_DIR}/references/onboarding-pack-template.md` as the starting structure. Fill every placeholder. What good looks like: a client could read it once and know what happens on Monday, what you need off them, and who to email when they are stuck.

## Done when
The pack has all 6 sections, the week-1 timeline has 5 dated rows, a real named contact with an email is present, and `04-gtm/onboarding-pack.pdf` exists on disk. (If no PDF library is installed the script writes `04-gtm/onboarding-pack.html` instead and tells you; that counts, note it in the changelog.)

## Log it
Append one line to `CHANGELOG.md` via the logbook helper, and update `.spark/state.json`:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d4-onboarding-pack \
  --artefact 04-gtm/onboarding-pack.pdf \
  --result "6 sections, 5-day week-1 timeline, named contact"

python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"4":{"outcome":"onboarding pack ready to hand to first client"}}}'
```

## If it goes wrong
No PDF library (weasyprint or fpdf) installed: the script falls back to HTML automatically and prints how to install one. The HTML is fine to send; convert it later. If `brand.json` is missing, styling defaults to plain black text on white, which still reads cleanly. If you cannot name a real contact yet, that is a signal, not a formatting problem: decide who owns new clients before you send anyone a pack.
