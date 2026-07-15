---
name: Build The Funnel
description: Map awareness to purchase in four stages, each with a named Jersey-appropriate channel, one asset and one numeric metric. Use on Day 4 after messaging is written.
when_to_use: Day 4 go-to-market, after d4-icp-messaging produces messaging.md, before you write outreach or spend on ads. Triggers on "funnel", "channels", "how do people find and buy".
---

# Build The Funnel

**What this does.** Turns your message into a path a stranger walks from first hearing about you to paying you, in four stages, each with a named channel, one asset and one number to watch.
**Why it matters.** Most founders confuse "being busy" with "selling". A funnel forces the honest question at each step: how many people arrive, and how many carry on to the next stage. If you cannot put a number on a stage, you cannot tell whether it works, and you will pour a week into a channel that leaks. In a small market like Jersey, where the pool is a few thousand firms not a few million, a leaky funnel is fatal.
**You are ready for this when.** `04-gtm/messaging.md` exists.

## Before you start
Read these first:
- `04-gtm/messaging.md`: your one-line promise and proof points feed every asset here.
- `.spark/state.json`: read `business_type`, `idea` and `headline_target` via the journey-state helper.
- `02-market/*`: the segment and buyer you settled on. The funnel starts where those buyers already spend attention, not where you wish they did.
- `.spark/brand/brand.json` if it exists: assets should carry your brand tokens.

Guardrail: this skill plans the funnel. It does not send anything or spend anything. Outreach and ad spend wait for explicit human sign-off in later skills.

## The four stages
Every funnel here has exactly four stages. Learn them once:

1. **Awareness.** A stranger learns you exist.
2. **Interest.** They lean in and give you a way to reach them (an email, a reply, a booked slot).
3. **Consideration.** They weigh you up against doing nothing or using someone else.
4. **Purchase.** They pay, pre-order, or sign the intake.

For each stage you name three things: the channel (where it happens), the asset (what does the work), and one metric (the number that tells you the stage is holding).

## Steps
1. Write the funnel top to bottom, one stage at a time. Do not start at purchase and work back. Buyers move forward, so plan forward.
2. For each stage, name ONE channel. Not a menu of five. The one you can actually run this week with the hours and money you have. Jersey-specific guidance is in `references/jersey-channels.md`: read it, it saves you a day. In a regulated market, favour channels where trust is already high (a warm introduction, a professional body, a named referrer) over cold reach.
3. For each stage, name ONE asset: the thing that does the persuading. A LinkedIn post, a one-page explainer, a demo call, a Stripe checkout. If the asset does not exist yet, note it as "to build" so Day 4 and 5 pick it up.
4. For each stage, set ONE numeric metric with a target. Use the honest arithmetic: if you need one paying customer this week and each stage typically passes a fraction forward, work out how many strangers you must reach at the top. The default assumption ladder is in `references/conversion-benchmarks.md`. These are assumptions, not promises: label them as such and replace them with your own numbers the moment you have real ones.
5. Branch on your business path for the bottom two stages, where the three paths genuinely differ. See below.
6. Sanity-check the whole thing against your `headline_target`. If the top-of-funnel number needed to hit one sale exceeds the reachable pool in Jersey, the funnel is telling you to change channel or widen the segment. Listen to it.
7. Generate the diagram with the script (step in "The artefact"). A picture of the funnel makes the leaks obvious.

## For software
Consideration is a free trial or a live demo of your deployed slice, so the asset is the working URL from Day 3. Purchase is a Stripe checkout or a paid pilot agreement. Metric at purchase: trials-to-paid conversion, target one paying account.

## For hardware
Consideration is the CAD render or physical mock plus a spec sheet, because buyers cannot hold the thing yet. Purchase is a pre-order or waitlist taking real payment intent (a deposit or a card on file). Metric at purchase: pre-orders placed, target one with money committed.

## For services
Consideration is your one sample deliverable, the productised proof that you do the work well. Purchase is a booked, paid intake through your bookable page. Metric at purchase: intakes booked and paid, target one.

## The artefact
Writes `04-gtm/funnel.md` in Markdown: a short intro line, then one section per stage (channel, asset, metric with its target and whether it is a real number or an assumption), then the arithmetic that ties the top number to one sale, then the embedded Mermaid diagram.

Also writes `04-gtm/funnel.mmd`, the Mermaid source, generated by the script so the diagram and the written stages never drift apart.

Generate the diagram:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/funnel_diagram.py 04-gtm/funnel.md
```

The script reads the stage table from `funnel.md`, writes `04-gtm/funnel.mmd`, and prints a Markdown block to paste back into `funnel.md`. If a stage is missing a channel, an asset or a metric, it tells you which one and stops, so the done-condition is checked for you.

What good looks like: four stages, each with a real named channel (not "social media" but "LinkedIn, posting to the Jersey finance community"), a named asset, and one number per stage. A reader who has never met you can see exactly how a stranger becomes a customer, and where the plan will leak first.

## Done when
`04-gtm/funnel.md` has four stages; every stage names one channel and one asset; every stage carries one numeric metric with a target; and `04-gtm/funnel.mmd` exists. The script exits cleanly, which means all twelve required fields (four stages times three) are filled.

## Log it
Append one line to CHANGELOG.md via the logbook helper: date, `d4-marketing-funnel`, `04-gtm/funnel.md`, and the numeric result (the top-of-funnel number you must reach to land one sale). Then update `.spark/state.json` through the journey-state helper: set the Day 4 outcome and mark progress.

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py --skill d4-marketing-funnel --artefact 04-gtm/funnel.md --result "<top-of-funnel N to reach 1 sale>"
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py --patch '{"days":{"4":{"outcome":"Funnel mapped: 4 stages, top-of-funnel <N> to reach 1 sale"}}}'
```

Record the channel choice and why in DECISIONS.md, especially if you rejected an obvious channel. Future you will want to know why.

## If it goes wrong
If the arithmetic says you need more strangers than exist in your reachable Jersey pool, do not inflate the conversion assumptions to make the sum work. That is lying to yourself. Instead do one of two things: pick a higher-trust, lower-volume channel (a warm referral converts far better than a cold post, so you need fewer at the top), or widen the segment to include Guernsey, the Isle of Man or UK firms. Change the funnel, then rerun the script.

If the script cannot parse your stage table, it prints the exact stage and field it choked on. Fix that field in `funnel.md` and run it again. The script never guesses a missing value for you, because a fabricated metric is worse than a blank one.
