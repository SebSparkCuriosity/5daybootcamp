---
name: Build The Funnel
description: Map awareness to purchase in four stages, each with a named Jersey channel, one asset and one metric. Day 4, after messaging.
when_to_use: Day 4, after d4-icp-messaging writes messaging.md. Triggers on "funnel", "channels", "how do people find and buy".
---

# Build The Funnel

**What this does.** Turns your message into the path a stranger walks from first hearing about you to paying, in four stages, each with a channel, an asset and a number.
**Why it matters.** A funnel forces the honest question at each step: how many arrive, and how many carry on, so you spot a leaky channel before you pour a week into it.
**You are ready for this when.** `04-gtm/messaging.md` exists.

## Before you start
Read: `04-gtm/messaging.md` (your promise and proof feed every asset), `02-market/*` (segment and buyer), `.spark/brand/brand.json` if it exists. Read `business_type`, `idea` and `headline_target` from `.spark/state.json` via the journey-state helper.

Guardrail: this plans the funnel only. It sends nothing and spends nothing. Outreach and ad spend wait for human sign-off in later skills.

## The four stages
1. **Awareness.** A stranger learns you exist.
2. **Interest.** They give you a way to reach them.
3. **Consideration.** They weigh you up against doing nothing or someone else.
4. **Purchase.** They pay, pre-order or sign the intake.

## Steps
1. Write top to bottom. Buyers move forward, so plan forward.
2. Ask the founder before naming any channel: where does your buyer already gather, and which of those could YOU actually work this week (who do you know there)? Then name ONE channel per stage from their answers and `references/jersey-channels.md`. In a regulated market favour high-trust channels (warm intro, professional body, named referrer) over cold reach.
3. Name ONE asset per stage: the thing that persuades. If it does not exist yet, mark it "to build" for Day 4 and 5.
4. Set ONE numeric metric with a target per stage. Work the arithmetic back from one sale using the ladder in `references/conversion-benchmarks.md`. Label these as assumptions; replace with real numbers when you have them.
5. Branch on business path for the bottom two stages (below).
6. Sanity-check against `headline_target`. If the top number needed exceeds the reachable Jersey pool, change channel or widen the segment.
7. Generate the diagram (see The artefact).

## For software
Consideration is a free trial or live demo of your Day 3 URL. Purchase is a Stripe checkout or paid pilot. Purchase metric: trials-to-paid, target one paying account.

## For hardware
Consideration is the CAD render or physical mock plus a spec sheet. Purchase is a pre-order or waitlist taking real payment intent (deposit or card on file). Purchase metric: pre-orders placed, target one with money committed.

## For services
Consideration is your one sample deliverable. Purchase is a booked, paid intake through your bookable page. Purchase metric: intakes booked and paid, target one.

## The artefact
Writes `04-gtm/funnel.md`: intro line, one section per stage (channel, asset, metric with target and whether real or assumption), the arithmetic tying the top number to one sale, then the embedded Mermaid diagram. The script also writes `04-gtm/funnel.mmd` so diagram and stages never drift.

```
python3 ${CLAUDE_SKILL_DIR}/scripts/funnel_diagram.py 04-gtm/funnel.md
```

The script reads the stage table, writes `funnel.mmd`, prints a Markdown block to paste back, and stops if any stage lacks a channel, asset or metric.

## Done when
`04-gtm/funnel.md` has four stages; each names one channel and one asset; each carries one numeric metric with a target; `04-gtm/funnel.mmd` exists; the script exits cleanly (all twelve fields filled).

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py --skill d4-marketing-funnel --artefact 04-gtm/funnel.md --result "<top-of-funnel N to reach 1 sale>"
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py --patch '{"days":{"4":{"outcome":"Funnel mapped: 4 stages, top-of-funnel <N> to reach 1 sale"}}}'
```
Record the channel choice and why in DECISIONS.md, especially any obvious channel you rejected.

## If it goes wrong
If the arithmetic needs more strangers than your reachable Jersey pool holds, do not inflate the conversion assumptions. Either pick a higher-trust, lower-volume channel (a warm referral converts far better, so you need fewer at the top) or widen the segment to Guernsey, the Isle of Man or UK firms. Change the funnel, then rerun the script. If the script cannot parse the table, it names the field it choked on: fix it and run again.
