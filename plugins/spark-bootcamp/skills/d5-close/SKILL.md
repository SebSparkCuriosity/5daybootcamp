---
name: Close The Deal
description: Turn the Friday conversation into a committed yes, record the win at the highest tier that lands, send letter and invoice, book kickoff.
when_to_use: Day 5, final step, straight after the Friday meeting once price is on the table.
---

# Close The Deal

**What this does.** Turns the conversation into a committed yes, recorded at whichever tier lands: cash, deposit, signed paid pilot, or signed LOI with a date and amount.
**Why it matters.** A week of work is worth nothing until someone commits, and most deals die in the last ten minutes because the founder never actually asks.
**You are ready for this when.** `04-gtm/friday-meeting.md`, `PROPOSAL.md` and `05-sale/paperwork/` exist and you have just spoken to the prospect.

## Before you start
Read `04-gtm/friday-meeting.md` (what was said, any live objection), `PROPOSAL.md` (package name and exact price), `05-sale/paperwork/` (letter and invoice drafts), `.spark/state.json` (`founder`, `business_type`, `headline_target`).
Guardrails. Human-in-the-loop: do not send letter or invoice, or take payment, until the founder reads the final wording and says yes. The engagement letter is a draft: "This is a draft. Have a qualified lawyer review it before you rely on it. Spark does not warrant it."

## Steps
1. Answer the last objection in one sentence, then stop. Do not re-pitch.
2. Ask for the sale with the number. Restate package and price from `PROPOSAL.md`, ask for the top tier, then go quiet.
3. Climb down one tier at a time (ranked in `references/deal-tiers.md`): cash, then deposit (30 to 50 percent), then a short paid pilot (two to four weeks, £500 minimum, never free), then a signed LOI with a specific amount and start date. Stop the moment one lands. All four count.
4. Bank proof, not a promise: cash cleared, deposit cleared, signed pilot terms plus fee raised, or signed LOI with £ and date. "Let's do something soon" is not a win.
5. Fill the paperwork in `05-sale/paperwork/` (templates in `references/engagement-letter-template.md` and `references/invoice-template.md`). Replace every placeholder: client, package, amount, dates, terms. Deposit line reads "Deposit (X percent of £Y)" and names the balance and due date. Charge tax only if the founder is registered; never invent a tax number.
6. Show the founder the final letter and invoice. Only on their yes, send both to the client and share payment link or bank details for cash or deposit.
7. Book a specific kickoff date and time with the client before you hang up, within five working days.
8. Record the win into `WON-DEAL.md`:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/record-win.py \
     --tier "cash|deposit|pilot|loi" --amount "2000" --currency GBP \
     --date "YYYY-MM-DD" --client "Client Ltd" --package "Package name" \
     --balance "balance and when" --kickoff "YYYY-MM-DD HH:MM" \
     --letter-sent yes --invoice-sent yes --project-root .
   ```
   Anything omitted is written as TODO.

The tier ranking is the same for all paths. The proof differs.

## For software
Usually cash up front (first subscription or setup fee) or a paid pilot on the deployed slice. Proof: a paid Stripe receipt or first invoice against the live URL.

## For hardware
Usually a paid deposit or pre-order taking real payment intent. Proof: a cleared deposit plus a one-line schedule for the balance on ship. A free waitlist is not a win.

## For services
Usually cash in full for the package, or a paid pilot delivering the sample deliverable. Proof: a signed engagement letter plus a paid or raised invoice.

## The artefact
Writes `05-sale/WON-DEAL.md` via the helper: tier, client, package, amount, date won, balance schedule, letter and invoice sent, booked kickoff. Good looks like a named tier, a real £ number, a date, and every box yes not TODO.

## Done when
`WON-DEAL.md` records a yes with tier, date and amount; letter and invoice both sent (marked yes); kickoff booked with a specific date and time.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d5-close --artefact 05-sale/WON-DEAL.md \
  --result "Won: deposit, GBP 2000, kickoff 2026-07-21"
```
Then set the day outcome and completion:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"5":{"outcome":"Won: deposit, GBP 2000"}}}'
```
If the win clears `headline_target`, say so plainly. Record why you accepted that tier in `DECISIONS.md`.

## If it goes wrong
**No yes today.** Do not force it or log a fake win. Book a specific follow-up, note the blocker in `04-gtm/friday-meeting.md`, move to the next-best Day 4 prospect.
**Yes but money cannot move.** Drop to a signed LOI with a named amount and start date, sent for signature the same day.
**Helper cannot write the file.** The script prints the content so you paste it into `05-sale/WON-DEAL.md` by hand.
