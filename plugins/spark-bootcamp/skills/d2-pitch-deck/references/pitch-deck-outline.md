# The 12-slide pitch deck outline

This is the Sequoia and Kawasaki shape, cut to 12 slides. It is a hand-out for
investors and partners: people who did not sit in your interviews and will read
it without you in the room. Every slide leads with the point. One claim per
slide, backed by a Day 1 quote or a sourced figure, never a hunch.

`build_deck.py` turns the first entry into a title slide (title plus subtitle),
then one slide per item in the `slides:` list. So slide 1 below is the title
block, and the 11 items in `slides:` are slides 2 to 12. Twelve in total.

## The twelve slides, in order

1. **Company purpose** (the title slide). One line that says what you do, for
   whom, and the outcome. This is the `title` plus `subtitle`, not a `slides:`
   entry. Example title: "Rekey once, file everywhere". Subtitle carries the
   who and the number.
2. **Problem.** The pain, in the customer's words. Lead with a verbatim Day 1
   quote. Name who has the problem and what it costs them today.
3. **Solution.** What you built or will build, in one plain sentence, then the
   before-and-after. No feature list. The outcome.
4. **Why now.** What changed that makes this possible or urgent this year: a
   rule, a cost, a technology, a behaviour. One reason, sourced.
5. **Market size.** TAM, SAM and SOM with a currency symbol on each, lifted
   from `02-market/market-sizing.md`. This slide must carry the TAM figure.
6. **Product.** How it works, in three steps a non-technical reader follows.
   For hardware, the render or mock. For services, the sample deliverable.
7. **Competition.** Who the buyer uses today (including "a spreadsheet" and
   "nothing"), and the one axis where you win. From `competitor-scan.md`.
8. **Business model.** What one customer pays and how often, from `pricing.md`.
   Spark default framing: fixed price from 2,000 pounds, live in one to six
   weeks. State the unit economics in one line.
9. **Go-to-market.** How the first ten customers hear about you. One channel
   you can actually work this week, not five you cannot.
10. **Traction and validation.** The proof you gathered on Day 1: interviews
    run, the count who confirmed the problem, and one more quote. Numbers, then
    a voice.
11. **Team.** Why you, in two or three lines. The unfair advantage: the sector
    you know, the network you have, the thing you have already shipped.
12. **The ask and next step.** What you want from this reader and what happens
    next. For investors, the raise and the use of funds. For partners, the
    pilot. Always a concrete next action with a date or a number.

## Traceability rule

Beside every hard claim in your `deck-content.yaml`, keep a `source:` note (the
builder ignores it, it is for your audit trail and the reviewer). A claim is
either a quote with a person's role attached, or a figure with a report, a
register, a URL or a named assumption behind it. If you cannot source it, cut
it. A deck of eight sourced claims beats twelve you cannot defend.
