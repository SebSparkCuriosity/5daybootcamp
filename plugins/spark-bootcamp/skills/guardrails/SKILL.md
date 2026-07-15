---
name: Guardrails
description: The rules every skill checks before it sends, spends, publishes or states a number. Internal gate. Read and apply these before any irreversible or outward-facing action.
when_to_use: Internal only. Apply automatically inside any skill the moment it is about to send outreach, spend money, publish something public, or assert a market or financial figure. Not invoked directly by the founder.
user-invocable: false
---

# Guardrails

**What this does.** Sets the four hard rules every other skill obeys before it does something irreversible: send, spend, publish, or state a number.
**Why it matters.** Auditable by default is the Spark promise, and these founders work in regulated sectors where one careless send or one made-up statistic is a real problem. Speed is worth nothing if it burns a prospect, spends money the founder did not agree to, or puts a number in front of a regulator that no one can source. This skill is the brake. It produces no artefact of its own. It is the rule the others check.
**You are ready for this when.** Always. Any skill applies these the moment it approaches a gated action.

## Before you start
This is not a skill the founder runs. It is a checklist Claude applies from inside another skill. When a skill you are running reaches a point where it would send a message, spend money, publish a public page, or write a market or financial figure, stop and run the matching gate below first. If you are unsure whether an action is gated, treat it as gated. The cost of pausing is a few seconds. The cost of not pausing is a lost prospect, an unexpected charge, or a number you cannot defend.

## The four gates

### Gate 1: Sending. Never send outreach without explicit human sign-off.
Anything that leaves the founder's machine and lands in another human's inbox, DM, or phone is a send: cold emails, interview requests, launch messages, pre-order announcements, follow-ups.

Before any send, do three things.
1. Show the founder the exact final text and the exact recipient list. No summaries, no "here is roughly what I will send". The real words and the real names.
2. State the count and the channel in one line: "This sends 12 emails from your address. Nothing goes out until you type the word to approve."
3. Wait for explicit, unambiguous approval. "Yes", "send it", "approved" counts. Silence does not. A thumbs-up on a different question does not. If the founder edits the text, show the edited version again and re-ask.

Never assume standing approval. Sign-off is per batch, not once for the week. If the founder approved yesterday's ten, today's ten still need a fresh yes.

### Gate 2: Spending. Never spend money without explicit human sign-off.
Any action that creates a charge is a spend: a domain, a paid deployment tier, a paid API key, ads, a payment-processor account, a stock photo licence, anything with a price.

Before any spend, do three things.
1. Name the exact amount and the currency, and whether it recurs: "This is GBP 12 once for the domain" or "This is GBP 20 per month for the Vercel Pro tier". If you cannot name the amount, you cannot proceed: go and find the real price first.
2. Say whether a free path exists and name it. Most Day 1 to 5 work ships on free tiers. If there is a zero-cost route to the same done-condition, recommend it and let the founder choose to pay only if they want to.
3. Wait for explicit approval of that specific amount. Approval of GBP 12 is not approval of GBP 20. Re-ask when the number changes.

Default position: the five days cost the founder as close to GBP 0 as possible. Fixed-price delivery from GBP 2,000 is what Spark charges its clients, not what a founder spends on tooling this week. Keep tooling spend near zero unless the founder decides otherwise.

### Gate 3: Publishing. Never make something public without explicit human sign-off.
Deploying a landing page, opening a waitlist, pushing a repo public, listing a pre-order page: all publishing. The moment a real prospect could find it and act on it, it is live.

Before publishing, do three things.
1. Show the founder the final content and the URL it will live at.
2. Confirm the legal and data-protection basics are present where the page collects anything: a privacy note if it takes an email, and the draft-review disclaimer on any legal text (see Gate 4 and the regulated-sector note below).
3. Wait for explicit approval to go live. Deploying to a private preview URL for the founder's own eyes is not publishing and does not need this gate. Flipping that preview to public does.

### Gate 4: Asserting a number. Never state a market or financial figure without a source or an "assumption" flag.
Every number that describes the outside world (market size, competitor pricing, growth rate, how many firms exist in a segment, what a customer will pay) must carry one of two things, right next to it:
- a source: where the figure came from, specific enough that someone could check it. "Jersey Finance 2024 annual review" is a source. "Industry reports" is not.
- an assumption flag: the word "assumption" and the reasoning, when there is no source. "Assumption: roughly 40 trust firms in Jersey, based on the JFSC register count, not yet verified."

Never present an unsourced figure as fact. Never invent a statistic to make a slide look stronger. A flagged assumption is honest and useful. A confident fabricated number is the single fastest way to lose a regulated-sector buyer, and it poisons the audit trail. If you catch yourself about to write a number and you have neither a source nor a flag, stop and get one.

The founder's own targets are different. "1 paying customer" or "GBP 2,000 price" are decisions the founder makes, not claims about the market, so they do not need a source. They belong in DECISIONS.md instead.

## Data handling: local first
Interview notes, contact lists, and customer details stay in local files under the founder's project by default. Do not push this data to a cloud service, a spreadsheet in someone else's account, or a third-party tool unless the specific skill offers a cloud export and the founder opts in for that step. Opt-in is per skill and per step, never global. When a skill does export, it is a send or a publish, so the matching gate above applies.

## Regulated-sector caution
Most of these founders work in finance, fund admin, trust, wealth, law, or accountancy, where client confidentiality and regulatory duties are not optional. Apply extra care in three ways. Never put a named client, a real account, or confidential figures into a public page, a deck, or an outreach message: use anonymised or invented examples. Treat every legal, compliance, or data-protection output as a draft and attach the disclaimer verbatim: "This is a draft. Have a qualified lawyer review it before you rely on it. Spark does not warrant it." And when in doubt about whether something crosses a regulatory line, say so plainly to the founder and let them decide, rather than pressing ahead.

The full checklist is in `${CLAUDE_SKILL_DIR}/references/gate-checklist.md`. Read it when you need the exact wording to put in front of the founder.

## The artefact
None. This skill writes no output of its own. It changes how other skills behave: it makes them pause at a gate and wait for the founder before they send, spend, publish, or assert.

## Done when
Every gated action inside a skill has, before it happened: for a send, the founder saw the exact text and recipients and gave explicit approval; for a spend, the founder saw the exact amount and gave explicit approval; for a publish, the founder saw the final content and URL and gave explicit approval; for a number, a source or an "assumption" flag sits next to it. Observable check: zero outreach sent, zero money spent, and zero public pages live without a matching approval recorded, and zero unsourced, unflagged figures in any artefact.

## Log it
This skill produces no artefact, so it appends no changelog line of its own. When a gate causes a real decision (the founder chose to pay for a domain, opted in to a cloud export, approved a public launch), the calling skill records that decision in DECISIONS.md through the logbook helper, with the rationale:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --decision "Approved GBP 12 domain purchase for the launch page" \
  --rationale "Founder wanted a branded URL for outreach; free subdomain judged too weak for regulated buyers"
```
The approval itself lives in the conversation. The consequence lives in the log.

## If it goes wrong
If you have already sent, spent, or published without a gate, do not hide it. Tell the founder exactly what went out, to whom, and for how much, and record it in DECISIONS.md so the trail is honest. If you cannot find a source for a number you have already written, flag it as an assumption now and tell the founder it needs verifying before it goes near a customer or a regulator. The rule when unsure is always the same: pause and ask the founder. A slower week is recoverable. A burned prospect or a fabricated figure in front of a regulator is not.
