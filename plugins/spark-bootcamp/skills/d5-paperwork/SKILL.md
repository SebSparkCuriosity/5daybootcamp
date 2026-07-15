---
name: Prepare The Paperwork
description: "Drafts the docs to take money: engagement letter with data-processing schedule, terms, invoice from the right entity, working payment method. Day 5, after the proposal."
when_to_use: "Day 5, after d5-proposal and once RATE-CARD.md exists. Run before you send anything or ask for a penny."
---

# Prepare The Paperwork

**What this does.** Assembles four DRAFT documents to take real money this week: an engagement letter (data-processing schedule embedded), terms, an invoice from your correct trading entity, and a payment method that clears today.
**Why it matters.** A prospect says yes and then loses three days while you hunt for a template, a bank detail and a lawyer, and that gap kills more first sales than price ever does.
**You are ready for this when.** `05-sale/PROPOSAL.md`, `05-sale/RATE-CARD.md` and `.spark/deliverables/data-protection/dpa-clause.md` all exist.

## Before you start
Reads by path: `05-sale/PROPOSAL.md` (scope, target, agreed price), `05-sale/RATE-CARD.md` (price, deposit), `.spark/deliverables/data-protection/dpa-clause.md` (the schedule), `.spark/state.json` and `.spark/brand/brand.json`. Writes into `05-sale/paperwork/`.

Every document is a **draft** and carries: "This is a draft. Have a qualified lawyer review it before you rely on it. Spark does not warrant it." **Human-in-the-loop:** nothing is sent and no money requested until you have read every doc, filled every `[TO COMPLETE]` marker, and signed off. The invoice names a bank account: get it wrong and money lands nowhere.

## Steps
1. Assemble the four drafts from your project root:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/assemble_paperwork.py --root .
   ```
   It substitutes what it knows, embeds the schedule in the engagement letter, and writes `engagement-letter.md`, `terms.md`, `invoice.md`, `payment-setup.md`. Anything it cannot know it leaves as `[TO COMPLETE: ...]`. The last line reports markers left and whether the schedule made it in.
2. Fix the trading entity first, the one everyone gets wrong. Letter and invoice come from the legal entity with the bank account and any regulatory registration, not your brand name. Sole trader: say so, use your own name. Fill every entity marker before anything goes out.
3. Set payment for same-day cash. **Default to bank transfer with a deposit:** local sterling clears same-day; Stripe or GoCardless onboarding can take over a day. Put account name, sort code, IBAN and reference on the invoice, ask 50% on signature and balance on delivery. See `payment-setup.md`.
4. Match letter to proposal line by line: scope, numeric outcome, timeline and price identical. More than the proposal is a scope trap; less loses the sale.
5. Check the schedule is genuinely inside the engagement letter, not linked or "to follow". If it shows a `[TO COMPLETE: data-processing schedule]` marker, run the data-protection skill, then re-run the assembler.
6. Read `terms.md` as the customer: short and fair. What you do, what you need, how changes work, when they can stop, who owns what.
7. Send all four to a qualified lawyer before you rely on them. This is the sign-off gate.

## For software
Bill the deployed slice as a fixed-price build with a deposit, then a separate monthly line for hosting and support if agreed. If customer data sits in Supabase or another cloud service, check that processor is named in the schedule.

## For hardware
You are taking a pre-order or deposit against a prototype. State in black and white on letter and invoice: what the deposit secures, what happens to it if you cannot deliver, and the timeline. Be specific about refunds.

## For services
The main case. The engagement letter carries the most weight: name the single deliverable, number of revisions, what you need from the client to start, and the delivery date. Name the data categories, where they live, and how long you keep them after the work ends.

## The artefact
Four Markdown files in `05-sale/paperwork/`: `engagement-letter.md` (signable, scope and price matching the proposal, schedule as a numbered section), `terms.md` (short fair terms), `invoice.md` (correct entity, deposit, bank details), `payment-setup.md` (bank-transfer-plus-deposit default). Good: a lawyer reads all four in twenty minutes, every marker gone, each carries the disclaimer, invoice names the correct entity and a working account.

## Done when
All four exist and the check passes:
```
python3 ${CLAUDE_SKILL_DIR}/scripts/assemble_paperwork.py --root . --check
```
It prints `CHECK_RESULT=OK` with 5 of 5: letter, terms and invoice present; each carries the disclaimer; a payment method named in `payment-setup.md`; the invoice states a price; the schedule embedded in the letter. Scope matching the proposal you confirm by eye in step 4.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d5-paperwork \
  --artefact 05-sale/paperwork/engagement-letter.md \
  --result "4 paperwork drafts ready, deposit 50% on signature, DPA schedule embedded"

python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --decision "Bank transfer, 50% deposit on signature, balance on delivery" \
  --rationale "Same-day clearing; card and direct-debit onboarding can exceed a day and Friday has none to spare"
```

## If it goes wrong
The assembler never crashes on a missing source: it writes all four drafts, leaves a `[TO COMPLETE]` marker where a source was missing, and names which to produce. Missing schedule: run the data-protection skill, then re-run. No bank transfer in time: fall back to a signed engagement letter plus an agreed payment date within seven days, recorded in writing.
