---
name: Prepare The Paperwork
description: Drafts the documents to actually take money: an engagement letter with the data-processing schedule baked in, terms, an invoice from the right trading entity, and a working payment method. Use on Day 5 after the proposal.
when_to_use: Day 5 sale, straight after d5-proposal and once RATE-CARD.md exists. The last thing between a yes and money in the account. Run before you send anything or ask for a penny.
---

# Prepare The Paperwork

**What this does.** Assembles four DRAFT documents that let you take real money this week: an engagement letter (with your data-processing schedule inside it), terms, an invoice from your correct trading entity, and a payment method that actually clears today.
**Why it matters.** A prospect says yes and then nothing happens for three days because you are hunting for a template, a bank detail and a lawyer. That gap kills more first sales than price ever does. A regulated customer, a trust company, a law firm, a fund administrator, cannot sign an engagement without a data-processing schedule attached, so the schedule is not an optional annex, it is the reason the letter is signable at all. Draft it all now, get it lawyer-checked, and the moment someone says yes you send one clean pack and ask for the deposit.
**You are ready for this when.** `05-sale/PROPOSAL.md` and `05-sale/RATE-CARD.md` both exist, and the data-protection skill has produced `.spark/deliverables/data-protection/dpa-clause.md`.

## Before you start
Reads, all via the safe helpers and by path:

- `05-sale/PROPOSAL.md`: the scope, the numeric target, the price you already agreed. The letter must match this exactly.
- `05-sale/RATE-CARD.md`: the price and any deposit terms.
- `.spark/deliverables/data-protection/dpa-clause.md`: the data-processing schedule, embedded straight into the engagement letter.
- `.spark/state.json` (founder, `business_type`, idea) and `.spark/brand/brand.json` (business name), for filling in what we already know.

Writes into `05-sale/paperwork/`.

Two hard rules, non-negotiable.

Every document here is a **draft**. Each one carries: "This is a draft. Have a qualified lawyer review it before you rely on it. Spark does not warrant it." That line stays until a qualified lawyer has read it. Spark drafts, a lawyer signs off, then you rely on it.

**Human-in-the-loop.** Nothing here is sent and no money is requested until you have read every document, filled every `[TO COMPLETE]` marker, and given explicit sign-off. The invoice in particular names a bank account. Get that wrong and the money lands nowhere.

## Steps
1. Assemble the four drafts. Run from your project root:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/assemble_paperwork.py --root .
   ```
   It reads your proposal, rate card, data-protection clause, state and brand, substitutes what it knows, embeds the data-processing schedule inside the engagement letter, and writes `engagement-letter.md`, `terms.md`, `invoice.md` and `payment-setup.md` into `05-sale/paperwork/`. Anything it cannot know for certain (your company registration number, your bank details, your registered address) it leaves as a visible `[TO COMPLETE: ...]` marker rather than guess. The last line tells you how many markers remain and whether the data-processing schedule made it in.

2. Fix the trading entity first, because it is the one everyone gets wrong. The invoice and the engagement letter must come from the legal entity that actually has the bank account and, where relevant, the regulatory registration. Your brand name is not your trading entity. If you trade as "Harbour Advisory" through "Harbour Advisory Limited", the letter and invoice say the limited company, with the registration number and registered office, and note the brand as "trading as". If you are a sole trader, say so plainly and use your own name. Fill every entity marker before anything goes out.

3. Set the payment method so cash lands the same day. **Default to bank transfer with a deposit.** A local sterling transfer clears same-day; card and direct-debit onboarding (Stripe, GoCardless) can take more than a day to verify a new account, which is a day you do not have on a Friday. So: put your account name, sort code, IBAN and reference on the invoice, ask for a deposit of 50% on signature and the balance on delivery, and only add cards later once you have time to verify. `payment-setup.md` walks through this and the numbers.

4. Match the letter to the proposal, line by line. Open `05-sale/PROPOSAL.md` next to `engagement-letter.md`. The scope, the numeric outcome, the timeline (one to six weeks) and the price must be identical. A letter that promises more than the proposal is a scope trap; one that promises less loses you the sale you already made. The assembler pulls the proposal scope in for you to compare; do not skip the comparison.

5. Check the data-processing schedule is genuinely inside the engagement letter, not linked, not "to follow". Regulated buyers sign the letter and the schedule together, as one document. If `dpa-clause.md` was missing when you ran step 1, the letter carries a `[TO COMPLETE: data-processing schedule]` marker: go and run the data-protection skill, then re-run the assembler.

6. Read `terms.md` as the customer. It should be short and fair: what you will do, what you need from them, how change requests work, when they can stop, and who owns what at the end. Long terms frighten a small buyer. Fair terms close.

7. Send all four to a qualified lawyer before you rely on them. This is the sign-off gate. The pack can be ready to send the moment they come back clean.

## For software
Your invoice can bill the deployed slice as a fixed-price build with a deposit, then a small monthly figure for hosting and support if you agreed one. Name the monthly line separately so the customer sees exactly what recurs. If any customer data will sit in Supabase or another cloud service, the data-processing schedule must name that processor; the assembler carries it through from `dpa-clause.md`, so check the processor is listed.

## For hardware
You are usually taking a pre-order or deposit against a prototype, not billing a finished product. Say that in black and white on both the letter and the invoice: what the deposit secures, what happens to it if you cannot deliver, and the expected timeline. A deposit taken against a promise you have not yet built is exactly the thing a customer, and a regulator, will scrutinise, so be specific about refunds.

## For services
This is your main case and the one the whole day points at. You are selling a productised service package with a defined deliverable, so the engagement letter carries the most weight of the three paths. The scope section must name the single deliverable, the number of revisions, what you need from the client to start, and the date you deliver. The data-processing schedule matters most here too, because a real client hands you real files: name the categories of data, where they live, and how long you keep them after the work ends.

## The artefact
Writes four Markdown files into `05-sale/paperwork/`:

- `engagement-letter.md`: the signable letter, scope and price matching the proposal, with the data-processing schedule embedded as a numbered section.
- `terms.md`: short, fair terms of business.
- `invoice.md`: a real invoice from your trading entity, with the deposit figure and bank details.
- `payment-setup.md`: how to take the money today, with the bank-transfer-plus-deposit default and the reason.

What good looks like: a lawyer reads all four in twenty minutes, every `[TO COMPLETE]` marker is gone, each document carries the disclaimer, the invoice names the correct legal entity and a working account, and the engagement letter's scope is word-for-word the proposal's.

## Done when
All four files exist in `05-sale/paperwork/`, and the mechanical check passes:
```
python3 ${CLAUDE_SKILL_DIR}/scripts/assemble_paperwork.py --root . --check
```
It must print `CHECK_RESULT=OK` with all five conditions met: engagement letter, terms and invoice present; each carries the disclaimer; a working payment method is named in `payment-setup.md`; the invoice states a price; and the data-processing schedule is embedded in the engagement letter. That is 5 of 5, no exceptions. The one condition the script cannot judge for you, scope matching the proposal, you confirm by eye in step 4.

## Log it
Append one line to CHANGELOG.md and register the artefact in state.json. Use the exact helper paths:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d5-paperwork \
  --artefact 05-sale/paperwork/engagement-letter.md \
  --result "4 paperwork drafts ready, deposit 50% on signature, DPA schedule embedded"

python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --append-artefact '{"skill":"d5-paperwork","path":"05-sale/paperwork/","result":"4 paperwork drafts ready"}'
```
Record the payment decision, because it governs whether you get paid this week:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --decision "Bank transfer, 50% deposit on signature, balance on delivery" \
  --rationale "Same-day clearing; card and direct-debit onboarding can exceed a day and Friday has none to spare"
```

## If it goes wrong
If the assembler cannot read the proposal, rate card or data-protection clause, it does not crash. It writes all four drafts anyway, leaves a clear `[TO COMPLETE]` marker wherever a source was missing, and tells you which one to go and produce. If the data-processing schedule is missing, run the data-protection skill first, then re-run the assembler so the schedule lands inside the letter. If you genuinely cannot get a bank transfer set up in time, fall back to a signed engagement letter plus an agreed payment date within seven days, recorded in writing, so the yes is locked even if the cash lands next week.
