# The sales-deck outline (10 to 14 slides)

This is the deck that closes one named prospect. It is not the Day 2 pitch deck.
The pitch deck explains your business to a stranger. This one moves one specific
buyer from "interesting" to "yes", so it is narrower, warmer, and it leans on
proof: real lines from real testers, not your own claims.

`build_deck.py` turns the first entry into a title slide (title plus subtitle),
then one slide per item in the `slides:` list. So slide 1 below is the title
block, and the items in `slides:` are the rest. Aim for 10 to 14 slides in
total, title block included.

## The five core sections (all must be present)

A sales deck that closes carries these five. Everything else supports them.

1. **Problem.** The prospect's pain, in the customer's words.
2. **Solution.** What you built, and the before-and-after outcome.
3. **Proof.** Two or more real tester quotes, each with a reported result.
4. **Pricing.** One number, what they pay and what they get.
5. **The ask and next step.** One named, dated action the prospect takes next.

## The slides, in order

1. **Title (for one named person).** The outcome this prospect wants, in one
   line, as the `title`. The `subtitle` names the prospect and carries the
   headline number, for example "Prepared for Jane Roe, Head of Trust Admin.
   Live in three weeks, fixed price from 2,000 pounds." A deck addressed to one
   person out-closes a generic one every time.
2. **The problem (core).** Lead with a verbatim quote from someone in the
   prospect's role, lifted from `04-gtm/feedback-synthesis.md`. Name who feels
   it and what it costs them today. Do not explain the quote.
3. **What it costs today.** The number behind the pain: minutes per task,
   pounds per month, the audit risk. Sourced or flagged as an assumption.
4. **The solution (core).** What you built or will build, one plain sentence,
   then the before-and-after. The outcome, not a feature list.
5. **How it works.** Three plain steps a non-technical reader follows. Branch
   by path: software, the working slice on its URL; hardware, the render or
   mock; services, the sample deliverable and how they start.
6. **Why now.** What changed that makes this the moment: a rule, a cost, a
   behaviour. One reason, sourced. Cut this slide if the deck is running long.
7. **Proof, first point (core).** A verbatim tester quote with the speaker's
   role, sat beside the result they reported. This is the section that closes.
8. **Proof, second point (core).** A second real tester quote and result. Two
   is the floor. If you have a third, add a slide: three closes harder.
9. **What you get, and what you do not.** Scope, in and out, in plain words. A
   prospect signs faster when the edges are clear.
10. **Timeline.** When it is live. Spark framing: one to six weeks, with the
    milestone the prospect sees each week.
11. **Pricing (core).** One number, what they pay and how often, what it
    includes. Spark default: fixed price from 2,000 pounds, live in one to six
    weeks. Confirm the exact figure with the founder before it goes on a slide.
12. **Why us (optional).** Two or three lines, only if the prospect does not
    already know you. The sector you know, the thing you have already shipped.
13. **The ask and next step (core).** Exactly what you want the prospect to do
    next, named and dated: "Start the pilot Monday", "Sign the one-page order
    form", "Book the 30-minute kickoff". Never "let us know your thoughts".

Slides 6 and 12 are the two you drop first if you need to get under 14. The
five core sections and the proof floor of two quotes are never optional.
