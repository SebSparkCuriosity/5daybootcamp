---
name: Close The Deal
description: Turns the Friday conversation into a committed yes, records the win at the highest tier that lands, sends the letter and invoice, and books kickoff. Use on Day 5 after the meeting.
when_to_use: Day 5, the final step. Straight after the Friday meeting, once the prospect has heard the proposal and price. This is where the week pays off.
---

# Close The Deal

**What this does.** Turns the conversation into a committed yes, then records the win at whichever tier lands: cash in full, a paid deposit, a signed paid pilot, or a signed letter of intent with a date and an amount.
**Why it matters.** A week of work is worth nothing until someone commits. Founders lose deals in the last ten minutes by never actually asking, or by leaving with a warm "let me think about it". This skill makes you ask clearly, take the highest commitment on offer, and get it in writing before the buyer's attention moves on.
**You are ready for this when.** `04-gtm/friday-meeting.md`, `PROPOSAL.md` and the files in `05-sale/paperwork/` exist, and you have just spoken to the prospect (or are about to).

## Before you start

Read these first:

- `04-gtm/friday-meeting.md`: what was said, and any objection you still need to answer.
- `PROPOSAL.md`: the package name and the exact price. You will restate both when you ask.
- `05-sale/paperwork/`: your engagement letter and invoice drafts, ready to fill and send.
- `.spark/state.json`: `founder`, `business_type` and `headline_target` for the week.

Two guardrails. First, human-in-the-loop: do not send the engagement letter, send the invoice, or take any payment until the founder has read the final wording and said yes. Prepare everything, then pause for that sign-off. Second, the engagement letter is a draft and carries this line: "This is a draft. Have a qualified lawyer review it before you rely on it. Spark does not warrant it."

## Steps

1. **Answer the last objection, once.** Look at `04-gtm/friday-meeting.md`. If one thing is still in the way, address it in a sentence, then stop talking. Do not re-pitch the whole thing.

2. **Ask for the sale, out loud, with the number.** Restate the package and the price from `PROPOSAL.md`, then ask for the highest tier: "The package is £X. I'll send the invoice now and we start Monday. Card or transfer?" Then go quiet. Silence after the ask is the founder's friend. Let the buyer fill it.

3. **Climb down one tier at a time, never past a real commitment.** The four tiers are ranked in `references/deal-tiers.md`. Reach for cash first. If they hesitate, ask for a deposit (30 to 50 percent). If a deposit is a stretch, sell a short paid pilot (two to four weeks, £500 minimum, never free). If money genuinely cannot move today, get a signed letter of intent with a specific amount and a specific start date. Stop the moment one lands. All four count as this week's win.

4. **Get proof, not a promise.** A yes is only banked when it is real: cash cleared, a deposit cleared, signed pilot terms plus the pilot fee raised, or a signed LOI with £ and a date. "Yes, let's do something soon" is not a win. If that is all you have, restate the number and ask again for the lowest real tier.

5. **Fill the paperwork.** Open the drafts in `05-sale/paperwork/` (templates in `references/engagement-letter-template.md` and `references/invoice-template.md` if the paperwork step did not produce them). Replace every placeholder: client, package, amount, dates, payment terms. For a deposit, the invoice line reads "Deposit (X percent of £Y)" and names the balance and when it falls due. Charge tax only if the founder is registered to; if not, say so and charge none. Never invent a tax number.

6. **Pause for sign-off, then send.** Show the founder the final letter and invoice. Only when they say yes, send both to the client and, where the tier is cash or deposit, share the payment link or bank details. This is the one point where you spend the founder's credibility, so get their explicit go-ahead.

7. **Book the kickoff.** Put a specific kickoff date and time in the diary with the client before you hang up. A deal with no start date drifts. Aim for within five working days.

8. **Record the win.** Run the helper to write `WON-DEAL.md`:

   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/record-win.py \
     --tier "cash|deposit|pilot|loi" --amount "2000" --currency GBP \
     --date "YYYY-MM-DD" --client "Client Ltd" --package "Package name" \
     --balance "balance and when" --kickoff "YYYY-MM-DD HH:MM" \
     --letter-sent yes --invoice-sent yes --project-root .
   ```

   Anything you leave out is written as TODO, so you can see at a glance what is still open.

### Branch by business path

The tier ranking is the same for everyone. The proof differs.

## For software
The win is usually cash up front (a first subscription or setup fee) or a paid pilot on the deployed slice. Proof is a paid Stripe receipt or the first invoice raised against the live URL.

## For hardware
The win is usually a paid deposit or a pre-order taking real payment intent, because the unit is not made yet. Proof is a cleared deposit and a one-line schedule for the balance on ship. A waitlist with no money is not a win.

## For services
The win is usually cash in full for the productised package, or a paid pilot delivering the sample deliverable for real. Proof is a signed engagement letter plus a paid or raised invoice.

## The artefact

Writes `05-sale/WON-DEAL.md` in Markdown, via the helper script. It records the tier reached, the client, the package, the amount, the date won, the balance schedule, whether the letter and invoice went out, and the booked kickoff. Good looks like: a named tier, a real number in £, a date, and every commitment box marked yes rather than TODO.

## Done when

A yes is recorded in `WON-DEAL.md` with a tier, a date and an amount; the engagement letter and invoice have been sent (both marked yes); and a kickoff is booked with a specific date and time. That is one paying (or committed) customer, the whole point of the week.

## Log it

Append one line to `CHANGELOG.md` via the logbook helper, with the numeric result (the amount won and the tier):

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d5-close --artefact 05-sale/WON-DEAL.md \
  --result "Won: deposit, GBP 2000, kickoff 2026-07-21"
```

Then update `.spark/state.json` via the journey-state helper: set `days.5.outcome` to the win and `days.5.complete` to true.

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"5":{"outcome":"Won: deposit, GBP 2000","complete":true}}}'
```

If the win clears the `headline_target`, say so plainly to the founder. That is the number the week was for. Record the reasoning behind the tier you accepted in `DECISIONS.md` (for example, why a pilot rather than cash).

## If it goes wrong

**No yes today.** If the buyer will not commit to any tier, do not force it and do not log a fake win. Book a specific follow-up date, note the exact blocker in `04-gtm/friday-meeting.md`, and move to the next-best prospect from Day 4. One warm maybe is not the week's target; a real commitment from someone else may be closer than you think.

**They say yes but the money cannot move.** Drop to a signed letter of intent with a named amount and start date. That still counts. Send the LOI for signature the same day while the intent is fresh.

**The helper cannot write the file.** The script prints the content to the screen so you can paste it into `05-sale/WON-DEAL.md` by hand. Nothing is lost.
