---
name: Map Client Intake
description: Turns your proposition into a 4-stage intake (proposal, engagement, kickoff, delivery), each with an owner, an SLA and one signable template. Day 4.
when_to_use: Day 4 go-to-market, once the proposition is written and before a real prospect runs through it.
---

# Map Client Intake

**What this does.** Maps "yes, I am interested" to "work delivered" as four named stages, each with one owner, one SLA and one signable template.
**Why it matters.** Most first sales die in the gap between the nod and the kickoff because nobody owns the next step, and this closes that gap so your first paying customer does not fall through it.
**You are ready for this when.** `02-market/proposition.md` exists.

## Before you start
Read `02-market/proposition.md` (offer, price, promise) and `.spark/state.json` (`founder`, `business_type`). If `.spark/brand/brand.json` exists, note the business name for the templates. Two questions before drafting (5 minutes): how should a new client's first week feel, and what response times can the founder honestly keep alongside the day job? Their answers set the tone and the SLAs; the defaults below are the fallback, not the answer. The engagement letter is a legal document: it ships as a draft, so have a qualified lawyer review this before use.

## Steps
1. Name the four stages, exactly these, in order (the minimum that survives an audit): **proposal**, **engagement** (contract or engagement letter), **kickoff**, **delivery**. No fifth.
2. Give every stage one named owner. Solo founder: your name, four times.
3. Set a numeric SLA per stage. Defaults: proposal within 2 working days of the first call, engagement letter within 1 working day of a verbal yes, kickoff within 5 working days of a signed letter, first delivery within your proposition's window.
4. Copy the four templates from `${CLAUDE_SKILL_DIR}/references/` into your project and fill the bracketed fields with your real offer, price and name. One per stage: `proposal.md`, `engagement-letter.md`, `kickoff-agenda.md`, `delivery-checklist.md`.
5. Read the whole flow back as the prospect. Any stage without an owner, a number, or a template is not finished.

## For software
Delivery is the deployed slice going live. Acceptance line in `delivery-checklist.md`: "prospect can reach the public URL and complete the core action once". Kickoff captures their must-work flow.

## For hardware
Delivery is the prototype demo plus pre-order or waitlist confirmation. Acceptance line: "prospect has seen the working mock and their payment intent is captured". Kickoff confirms the spec pre-ordered against.

## For services
Delivery is the sample deliverable handed over. Acceptance line: "prospect has the sample deliverable and has confirmed it matches the brief". Kickoff pins down the brief.

## The artefact
Writes `04-gtm/ops/intake-process.md` (Markdown): a table of the four stages, each with owner, SLA and a link to its template. Writes `04-gtm/ops/templates/` holding `proposal.md`, `engagement-letter.md`, `kickoff-agenda.md`, `delivery-checklist.md`, filled with real details.

## Done when
`04-gtm/ops/intake-process.md` names 4 stages, each with an owner and a numeric SLA, and `04-gtm/ops/templates/` holds exactly 4 filled templates, one per stage.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d4-intake-process \
  --artefact 04-gtm/ops/intake-process.md \
  --result "4-stage intake process, 4 signable templates"

python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"4":{"outcome":"4-stage intake process, 4 signable templates"}}}'
```

## If it goes wrong
Cannot name an owner? Put your own name with an SLA of "TBC by first sale" and flag it in `DECISIONS.md`. Engagement letter feels too heavy for a small job? Keep it: a one-page signed letter is the cheapest audit trail you will buy.
