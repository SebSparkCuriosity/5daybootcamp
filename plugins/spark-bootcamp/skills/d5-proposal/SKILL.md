---
name: Write The Proposal
description: Turns your week of work into a one-page offer for the named buyer: the problem, one numeric target, a 1 to 6 week timeline, one price, one next step. Use on Day 5 before the sale.
when_to_use: Day 5 sale, after the pricing model and demo script are done and the Friday buyer is named. The document you put in front of the buyer to get a yes.
argument-hint: [buyer-name]
---

# Write The Proposal

**What this does.** Writes a single page that a named buyer can say yes to: the problem in their words, one numeric target, a delivery window inside six weeks, one price, and one next step.
**Why it matters.** A proposal is where the whole week either lands or leaks away. Founders lose the sale here by writing three pages of features, three price options and no clear ask. The buyer, a busy trust officer or fund director, reads none of it. One page, one number, one price, one next step. Make the yes easy.
**You are ready for this when.** `01-discovery/validated-problem.md`, `02-market/proposition.md`, `05-sale/PRICING-MODEL.md` and `05-sale/DEMO-SCRIPT.md` all exist, and `04-gtm/friday-meeting.md` names the buyer.

## Before you start
Read these five, in this order. Each one gives you exactly one part of the page.
- `01-discovery/validated-problem.md`: the problem, in the buyer's words. Do not reword it into marketing.
- `02-market/proposition.md`: the success metric. This is your numeric target, stated as a before and after.
- `05-sale/PRICING-MODEL.md`: the chosen model and the price floor. This is your one price. If your pricing step produced a `05-sale/RATE-CARD.md` instead, read the price from there.
- `05-sale/DEMO-SCRIPT.md`: the value moment you will show. The proposal promises exactly what the demo proves, no more.
- `04-gtm/friday-meeting.md`: the named buyer (name, role, firm) and the confirmed slot. Read `.spark/state.json` for `business_type` and the founder name.

Read the template once: `${CLAUDE_SKILL_DIR}/references/proposal-template.md`.

Guardrail: this skill writes a document. It does not send it and it does not take a payment. The buyer sees it only after you have read it and said go. Human sign-off before it leaves your hands. That is a hard rule.

## Steps
1. Name the buyer at the top. One line: name, role, firm, from `friday-meeting.md`. If you type "To: the team" or a company name, stop. A proposal is to a person. This skill's argument is that person's name.
2. State the problem in three sentences, lifted from `validated-problem.md` in their language. Name the workflow that hurts and what it costs them now, in time, money or risk. No solution yet. They should nod before they read your offer.
3. State the target as a number. Pull the success metric from `proposition.md` and write it as "from X to Y, by when". "From three days to half a day" beats "significant time savings". If the metric is fuzzy, go back and sharpen it before you write another word. You cannot sell a feeling.
4. Set the timeline inside six weeks. Name one milestone the buyer will see and when. Spark ships in one to six weeks; if your scope needs longer, cut the scope, not the promise. Say the work is human-in-the-loop and changelogged, so their compliance people can follow every step.
5. State one price. Take it from `PRICING-MODEL.md`. One number, fixed, GBP. No ranges, no options, no day rates. Spark's floor is GBP 2,000; do not go below it without a reason written in DECISIONS.md. If you must mention a follow-on, do it in one sentence, not a second price.
6. Write one next step: one action, one owner, one date. Usually this rides on the Friday meeting: "We talk Friday at 10:00 for 20 minutes, then you decide." Or a straight ask: "Say yes by Friday and we start Monday." One decision, not a menu.
7. Add the draft disclaimer at the foot (the template carries it): this is a draft, have a lawyer review it, Spark does not warrant it.

Branch only where the "what you get" line differs by path:

### For software
Promise the deployed slice: live on a public URL, doing the one job the demo shows. Name the URL if it is up.

### For hardware
Promise the prototype plus the pre-order or waitlist page taking real payment intent. Name what the prototype proves and what the buyer reserves.

### For services
Promise the productised package: one named sample deliverable plus a bookable intake, so the buyer sees your standard before they commit.

8. Write `05-sale/PROPOSAL.md` from the template. Keep it to one page: 250 to 450 words. Then check it: `python3 ${CLAUDE_SKILL_DIR}/scripts/proposal_check.py 05-sale/PROPOSAL.md`. It prints PASS or names exactly what is missing (too long, no number, no timeline, no single price, no next step, no named buyer). Fix and re-run until it prints PASS.
9. Export the PDF with the shared helper: `python3 ${CLAUDE_SKILL_DIR}/scripts/md_to_pdf.py 05-sale/PROPOSAL.md 05-sale/proposal.pdf`. If no PDF library is installed it writes `05-sale/proposal.html` instead and tells you how to get a real PDF. The HTML is fine to send.

## The artefact
Writes `05-sale/PROPOSAL.md` (Markdown) and `05-sale/proposal.pdf` (PDF, or `proposal.html` as the graceful fallback), following `${CLAUDE_SKILL_DIR}/references/proposal-template.md`. What good looks like: one page a busy regulated buyer reads in ninety seconds, names them, states one numeric target, one delivery window inside six weeks, one fixed price, one next step, and carries the draft disclaimer. `proposal_check.py` prints PASS.

## Done when
`proposal_check.py` prints PASS: the file is under 500 words, names the buyer, and carries a numeric target, a 1 to 6 week timeline, exactly one price and one next step. The PDF (or HTML fallback) exists at `05-sale/proposal.pdf`.

## Log it
Append one line to CHANGELOG.md and update state, using the exact helper paths:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d5-proposal \
  --artefact 05-sale/PROPOSAL.md \
  --result "1-page proposal, target [X to Y], price GBP [n], [1-6] week timeline"

python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --append-artefact '{"skill":"d5-proposal","path":"05-sale/PROPOSAL.md","result":"proposal ready for named buyer"}'

python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days": {"5": {"outcome": "one-page proposal ready for [buyer]"}}}'
```
If the price or timeline forced a change to the scope, record it as a dated decision with its rationale in DECISIONS.md.

## If it goes wrong
If `proposal_check.py` will not run, `05-sale/PROPOSAL.md` is still the artefact of record: count the words and check the six parts by hand against Done when, then fix the script later. Never let a broken script block Day 5. If the buyer is not yet named because Friday is not booked, write the proposal to the warmest named prospect from `04-gtm/gtm-plan.md` and note in DECISIONS.md that the buyer is provisional. A proposal aimed at a real person beats a perfect one aimed at nobody.
