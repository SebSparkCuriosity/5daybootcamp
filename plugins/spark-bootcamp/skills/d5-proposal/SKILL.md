---
name: Write The Proposal
description: "Turns the week into a one-page offer for the named buyer: problem, one numeric target, a 1 to 6 week timeline, one price, one next step."
when_to_use: Day 5 sale, after pricing and demo script done and the Friday buyer is named.
argument-hint: [buyer-name]
---

# Write The Proposal

**What this does.** Writes a single page a named buyer can say yes to: their problem, one numeric target, a delivery window inside six weeks, one price, one next step.
**Why it matters.** This is where the week lands or leaks away, so make the yes easy: one page, one number, one price, one ask, not three pages of features a busy buyer never reads.
**You are ready for this when.** `01-discovery/validated-problem.md`, `02-market/proposition.md`, `05-sale/PRICING-MODEL.md`, `05-sale/DEMO-SCRIPT.md` exist and `04-gtm/friday-meeting.md` names the buyer.

## Before you start
Read each for one part of the page:
- `01-discovery/validated-problem.md`: the problem in the buyer's words.
- `02-market/proposition.md`: the success metric, your numeric target.
- `05-sale/PRICING-MODEL.md`: the price (or `05-sale/RATE-CARD.md` if that was produced instead).
- `05-sale/DEMO-SCRIPT.md`: the value moment. Promise only what the demo proves.
- `04-gtm/friday-meeting.md`: named buyer and slot. Read `.spark/state.json` for `business_type` and founder.

Read `${CLAUDE_SKILL_DIR}/references/proposal-template.md` once.

Guardrail: this writes a document, it does not send it or take payment. Human sign-off before it leaves your hands. Hard rule.

## Steps
1. Name the buyer at the top: name, role, firm, from `friday-meeting.md`. A proposal is to a person, not a team.
2. State the problem in three sentences from `validated-problem.md`, in their language. Name the workflow that hurts and its cost. No solution yet.
3. State the target as a number from `proposition.md`: "from X to Y, by when". If it is fuzzy, sharpen it first.
4. Set the timeline inside six weeks with one milestone the buyer sees and when. Say the work is human-in-the-loop and changelogged. If scope needs longer, cut scope.
5. State one price from `PRICING-MODEL.md`: fixed, GBP, no ranges or options. Floor is GBP 2,000; below it needs a reason in DECISIONS.md.
6. Write one next step: one action, one owner, one date.
7. Add the draft disclaimer at the foot (the template carries it): this is a draft, have a qualified lawyer review it before use, Spark does not warrant it.

Branch only on the "what you get" line:

### For software
Promise the deployed slice: live on a public URL doing the demo's one job. Name the URL if up.

### For hardware
Promise the prototype plus the pre-order or waitlist page taking real payment intent. Name what it proves and what the buyer reserves.

### For services
Promise the productised package: one named sample deliverable plus a bookable intake.

8. Write `05-sale/PROPOSAL.md` from the template, one page, 250 to 450 words. Check it: `python3 ${CLAUDE_SKILL_DIR}/scripts/proposal_check.py 05-sale/PROPOSAL.md`. Fix and re-run until PASS.
9. Export the PDF: `python3 ${CLAUDE_SKILL_DIR}/scripts/md_to_pdf.py 05-sale/PROPOSAL.md 05-sale/proposal.pdf`. If no PDF library, it writes `05-sale/proposal.html` instead, which is fine to send.

## The artefact
Writes `05-sale/PROPOSAL.md` (Markdown) and `05-sale/proposal.pdf` (or `proposal.html` fallback), per `${CLAUDE_SKILL_DIR}/references/proposal-template.md`. Good: one page read in ninety seconds, names the buyer, one numeric target, one window inside six weeks, one fixed price, one next step, the draft disclaimer. `proposal_check.py` prints PASS.

## Done when
`proposal_check.py` prints PASS: under 500 words, names the buyer, carries a numeric target, a 1 to 6 week timeline, exactly one price and one next step. The PDF (or HTML fallback) exists at `05-sale/proposal.pdf`.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d5-proposal \
  --artefact 05-sale/PROPOSAL.md \
  --result "1-page proposal, target [X to Y], price GBP [n], [1-6] week timeline"

python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days": {"5": {"outcome": "one-page proposal ready for [buyer]"}}}'
```
If price or timeline forced a scope change, record it as a dated decision in DECISIONS.md.

## If it goes wrong
If `proposal_check.py` will not run, `05-sale/PROPOSAL.md` is still the record: count words and check the six parts by hand against Done when. Never let a broken script block Day 5. If no buyer is named because Friday is not booked, write to the warmest named prospect from `04-gtm/gtm-plan.md` and note in DECISIONS.md that the buyer is provisional.
