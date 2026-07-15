---
name: Map Client Intake
description: Turns your proposition into a 4-stage intake process (proposal, engagement, kickoff, delivery) with an owner, an SLA and one signable template per stage. Use on Day 4.
when_to_use: Day 4 go-to-market, once the proposition is written and before you take a real prospect through it. The plumbing that carries a yes into paid, delivered work.
---

# Map Client Intake

**What this does.** Maps the journey from "yes, I am interested" to "work delivered" as four named stages, each with one owner, one SLA and one template you can actually sign or send.
**Why it matters.** A prospect saying yes is not a customer. A customer is someone you invoiced, delivered to, and could defend to a regulator. Most first sales die in the gap between the nod and the kickoff because nobody owns the next step. This skill closes that gap so your first paying customer does not fall through it.
**You are ready for this when.** `02-market/proposition.md` exists.

## Before you start
Read `02-market/proposition.md`: the offer, the price, the promise. Read `.spark/state.json` for `founder` and `business_type`. If a `brand.json` exists at `.spark/brand/brand.json`, note the business name so the templates carry it.

One guardrail up front: the engagement letter is a legal document. It ships as a draft and you must not send it to a real client until a qualified lawyer has read it. That warning is baked into the template.

## Steps
1. Name the four stages. Keep them exactly these, in this order, because they are the minimum that survives an audit: **proposal**, **engagement** (contract or engagement letter), **kickoff**, **delivery**. Do not add a fifth. Four is enough for a first sale.
2. Give every stage one owner. For a solo founder that is you, four times. Write your name anyway. An owner with no name is an owner with no accountability.
3. Set an SLA per stage: the promise for how fast that stage completes once the previous one finishes. Default to proposal within 2 working days of the first call, engagement letter within 1 working day of a verbal yes, kickoff within 5 working days of a signed letter, first delivery within the window your proposition promised. Numbers, not "quickly".
4. Copy the four templates from `${CLAUDE_SKILL_DIR}/references/` into your project and fill the bracketed fields with your real offer, price and name. One template per stage, no more.
5. Read the whole flow back once as if you were the prospect. If any stage has no owner, no number, or no template, it is not finished.

The four templates map one to one onto the stages:

| Stage | Template | Purpose |
| --- | --- | --- |
| Proposal | `proposal.md` | The one-page offer: problem, scope, price, promise. |
| Engagement | `engagement-letter.md` | The signable agreement. Draft, lawyer required. |
| Kickoff | `kickoff-agenda.md` | The first paid meeting, run to a fixed shape. |
| Delivery | `delivery-checklist.md` | What "done" means, ticked off in front of the client. |

## For software
Your delivery stage is the deployed slice going live for the client. In `delivery-checklist.md`, the acceptance line is "prospect can reach the public URL and complete the core action once". Kickoff captures their one must-work flow.

## For hardware
Your delivery stage is the prototype demo plus the pre-order or waitlist confirmation. In `delivery-checklist.md`, the acceptance line is "prospect has seen the working mock and their payment intent is captured". Kickoff confirms the spec they are pre-ordering against.

## For services
Your delivery stage is the sample deliverable handed over. In `delivery-checklist.md`, the acceptance line is "prospect has the sample deliverable and has confirmed it matches the brief". Kickoff pins down the brief so the sample lands first time.

## The artefact
Writes `04-gtm/ops/intake-process.md` in Markdown: a table of the four stages, each with its owner and SLA, plus a link to its template. And writes `04-gtm/ops/templates/` containing `proposal.md`, `engagement-letter.md`, `kickoff-agenda.md` and `delivery-checklist.md`, each filled with your real details.

What good looks like: a prospect could say yes this afternoon and you would know exactly who does what, by when, with which document, all the way to delivered. No improvising.

## Done when
`04-gtm/ops/intake-process.md` names 4 stages, each with a stated owner and a numeric SLA, and `04-gtm/ops/templates/` holds exactly 4 filled templates, one per stage.

## Log it
Append one line to `CHANGELOG.md` via the logbook helper: date, `d4-intake-process`, the artefact path, the result (for example "4-stage intake, 4 templates"). Then update `.spark/state.json` via the journey-state helper: record the artefact and mark Day 4 progress.

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d4-intake-process \
  --path 04-gtm/ops/intake-process.md \
  --result "4-stage intake process, 4 signable templates"

python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --add-artefact d4-intake-process 04-gtm/ops/intake-process.md "4 stages, owner and SLA each"
```

## If it goes wrong
If you cannot name an owner for a stage because you genuinely do not know who does it yet, put your own name and an SLA of "TBC by first sale", then flag it in `DECISIONS.md`. A named gap you can see beats a silent one that surprises you mid-sale. If the engagement letter feels too heavy for a small first job, keep it: a one-page signed letter is the cheapest audit trail you will ever buy.
