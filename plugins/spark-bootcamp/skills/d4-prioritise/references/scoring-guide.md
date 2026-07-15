# Scoring guide: RICE and MoSCoW for the Friday build list

This is the reference behind d4-prioritise. Read it if the numbers feel arbitrary. Everything
here is a rule of thumb from shipping small things fast, not a law. When in doubt, favour the
change a paying customer asked for over the one that felt clever.

## Why two frameworks, not one

RICE ranks changes by value for effort, so the list sorts itself. MoSCoW ties that ranking to
the sale, so a cheap high-RICE change that nobody actually needs to buy does not sneak onto
Friday ahead of the thing the sale depends on. You need both. RICE gives you the order, MoSCoW
gives you the floor.

## RICE, field by field

Score = (Reach x Impact x Confidence) / Effort.

**Reach.** The count of people this change touches, drawn from your own testers and captured
enquirers. Use the real number. If four of nine testers hit the same wall, Reach is 4. Do not
extrapolate to a market you have not spoken to.

**Impact.** How hard this pushes someone from interested to paying.

| Score | Meaning |
| --- | --- |
| 3 | Massive. Without it they will not buy. |
| 2 | High. Clearly moves the decision. |
| 1 | Medium. Helps, not decisive. |
| 0.5 | Low. Minor polish. |
| 0.25 | Minimal. Barely noticed. |

**Confidence.** How sure you are, as a percentage, and be strict.

| Score | Meaning |
| --- | --- |
| 100% | You watched it block or convert someone in a session. |
| 80% | One clear account, stated plainly. |
| 50% | A hunch or a single offhand comment. |
| 20% | You are guessing. Say so. |

**Effort.** Person-days to build, honestly. Friday is one day. Half a day is 0.5. If a change
is more than one person-day, it almost certainly cannot be a Friday fix, so it should not be in
the top 3 no matter how high its RICE.

## MoSCoW

- **Must.** The sale dies without it. If a Hot tester named it as a blocker, it is a Must.
- **Should.** Strong pull, not fatal. Ships if there is room.
- **Could.** Nice, cheap, later. Parked with a clear conscience.
- **Won't.** Not this week. Written down so it is not lost, not deleted.

## Choosing the top 3

1. Sort by RICE, highest first.
2. Drop anything with Effort above 1.0 person-day. It cannot land on Friday.
3. If a Must sits just below the cut, promote it over a Should above it, and note the swap in
   DECISIONS.md.
4. Break ties by Effort: ship the cheapest, keep slack for the sale.

## Buying-signal scorecard

Four signals, 0 to 3 each, total out of 12.

| Signal | 0 | 3 |
| --- | --- | --- |
| Pain | mild annoyance | urgent and expensive |
| Budget | no spend, no mention | can spend, raised it themselves |
| Timing | someday | needs it now |
| Pull | passive | asked price, or left email / pre-order |

Bands: Hot 9 to 12, Warm 5 to 8, Cool 0 to 4.

Anyone from the live-page capture store already acted with intent, so start them at Pull 3 and
place them at the top of the warmth order within their band. A pre-order click outranks a warm
conversation every time.

## Worked example

Nine testers. Four hit a confusing onboarding step; you watched two of them give up.

- Change: "one-screen onboarding". Reach 4, Impact 3, Confidence 100%, Effort 0.5.
  RICE = (4 x 3 x 1.0) / 0.5 = 24. MoSCoW: Must. Flagged BUILD FRIDAY.
- Change: "dark mode". Reach 1, Impact 0.5, Confidence 50%, Effort 1.0.
  RICE = (1 x 0.5 x 0.5) / 1.0 = 0.25. MoSCoW: Won't.

Onboarding wins by a mile. Dark mode waits. That is the whole point.
