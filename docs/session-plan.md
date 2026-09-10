# Facilitator session plan

Six sessions run the bootcamp: pre-work (async, 2 to 4 weeks out) plus five
live days. Each live day runs 09:00 to 17:00 Jersey time (Day 1 runs to
17:30, see below), four working blocks, two 15-minute breaks, an hour for
lunch. That's an assumption, not a rule in the plugin: tell me your cohort's
actual hours and I'll rebuild the times.

Every block below maps to the real skill chain in
`plugins/spark-bootcamp/skills/coach/references/journey-map.md`, so the plan
never drifts from what the plugin actually does. Where a skill's SKILL.md
already states a "why it matters" line, that's the hook for its slide;
where it states "done when", that's the checklist slide at the end of the
day. Nothing here is invented content, it's the plugin's own copy laid out
against a clock.

**If you lose the thread mid-day:** run `/spark-bootcamp:coach` and read the
"your next move" line off the screen. That's the one thing the coach is
built for, live on the room's screen works as well as in a terminal.

## How this becomes five PowerPoints

1. This plan is the outline. Once you've signed off the timings and topics,
   the next step is one Spark-branded deck per day, `docs/decks/day-N.pptx`.
2. Build them with the `spark-branding` skill, not `house-style`'s
   `build_deck.py` directly: these are Spark's own facilitator decks (teal
   cover, gold stat plates, the Lighthouse mark), not a founder's branded
   artefact, so they want the real Spark template, not the generic
   `house-style` fallback that `d2-pitch-deck` and `d4-sales-deck` use for
   founders' own decks.
3. Say "build the Day 1 deck" (or all five) and I'll turn each day's slide
   outline below into a real `.pptx` in `docs/decks/`, the same pattern as
   `docs/build_overview_deck.py` for the plugin overview deck.

---

## Pre-work (async, T-minus 2 to 4 weeks): no deck

No room, no clock, so no slides. Milestones only, driven by `start` then
`coach`:

| Milestone | Skill | Target |
|---|---|---|
| Idea captured, path chosen, headline number set | `start` | Same day |
| Interview target spec written | `p0-interview-triage` | T-minus 4wk |
| Invite list built | `p0-invite-list` | T-minus 4wk |
| Invitations sent | `p0-invitations` | T-minus 3 to 4wk |
| Consent and privacy wording drafted | `data-protection` | Alongside invitations |
| 8 to 12 interviews booked for Day 1 | `p0-schedule` | T-minus 1wk (closes pre-work) |

Under 8 booked a week out: escalate per `p0-schedule`'s own fallback (more
invitations, wider geography, or a logged decision to accept 5 to 7). Under
5, pre-work stays open and Day 1 does not start.

---

## Day 1: Idea and Discovery

Target: the idea is sharp enough to test, then the booked interviews
actually happen. This is the one day that overflows the clock on purpose:
interviews run long, and the close-out (`synthesise-interviews`,
`d1-validated-problem`) slides into Tuesday morning. That's expected, the
plugin tracks it by artefact, not by calendar day.

| Time | Block | Skill(s) | Artefact |
|---|---|---|---|
| 09:00–09:10 | Open | Facilitator framing, `coach` on screen | — |
| 09:10–10:15 | Refine the idea | `d1-refine-idea` (deep) | `idea-brief.md` |
| 10:15–10:30 | Break | | |
| 10:30–11:15 | Plan the interviews | `d1-interview-plan` (deep) | `interview-plan.md` |
| 11:15–12:00 | Write the script | `d1-write-script` (deep) | `interview-script.md` |
| 12:00–13:00 | Lunch + confirm today's interview slots | | |
| 13:00–17:30 | Interviews | `run-interview` × up to 8 (25min + 10min gap) | one record per session, `01-discovery/interviews/` |

8 back-to-back 25-minute interviews with 10-minute gaps runs 4.5 hours,
hence the 17:30 finish. `p0-schedule` already caps Monday at 8 and routes
anything past that to Tuesday morning overflow, so don't fight the room for
a 17:00 finish on interview day, the interviews matter more than the clock.

**Day 1 deck (6 to 8 slides):** title/agenda, "why the idea has to fit one
sentence", the interview plan and what a good answer sounds like, the
script and how to stay quiet, then a single "you're in interviews now"
handoff slide. No slide needed for the interview block itself, it's a live
conversation, not a deck moment.

---

## Day 2: Market and Proposition

Target: size the market, sharpen the proposition, hand out a pitch deck.
Closes out Day 1 first.

| Time | Block | Skill(s) | Artefact |
|---|---|---|---|
| 09:00–09:35 | Overflow interviews (if any booked) | `run-interview` | remaining interview records |
| 09:35–10:15 | Synthesise | `synthesise-interviews` | `discovery-findings.md` |
| 10:15–10:30 | Break | | |
| 10:30–10:50 | Validate the problem, close Day 1 | `d1-validated-problem`, `checkpoint close` | `validated-problem.md` |
| 10:50–11:20 | Market research | `d2-market-map`, `d2-market-sizing`, `d2-competitor-scan` | `market-map.md`, `market-sizing.md`, `competitors.md` |
| 11:20–12:30 | Position and propose | `d2-positioning`, `d2-proposition` (working discussion) | `positioning.md`, `proposition.md` |
| 12:30–13:30 | Lunch | | |
| 13:30–13:40 | Messaging | `d2-messaging` | `messaging.md` |
| 13:40–14:15 | Brand foundations | `d2-brand-foundations` (working discussion) | `brand-foundations.md` |
| 14:15–15:00 | Visual identity | `d2-visual-identity`, `brand-register` | `brand-board.html`, `.spark/brand/brand.json` |
| 15:00–15:15 | Break | | |
| 15:15–15:55 | Brand book, pitch deck | `d2-brand-book`, `d2-pitch-deck` | `brand-book.html/.pdf`, `pitch-deck.pptx` |
| 15:55–17:00 | Pitch lightning round | group share, 2 min each + feedback; `checkpoint close` | — |

**Day 2 deck (8 to 10 slides):** agenda, the market snapshot template
(TAM/SAM/SOM placeholders founders fill live), the positioning canvas,
proposition one-liner formula, the brand foundations questions, then a
closing slide briefing the lightning round rules (2 minutes, one slide, no
notes).

---

## Day 3: Product and Build

Target: ship the smallest slice a real prospect can act on. Branches by
business path from here (`d3-mvp-build` is software: deployed URL,
hardware: prototype plus pre-order page, services: sample deliverable plus
intake page). The afternoon is a build sprint, not a talking session, so
the deck is lightest this day.

| Time | Block | Skill(s) | Artefact |
|---|---|---|---|
| 09:00–09:15 | Product context | `d3-product-context` | `product-context.md` |
| 09:15–10:15 | Prioritise and map | `d3-moscow`, `d3-story-map` (working discussion) | `requirements-moscow.md`, `story-map.md` |
| 10:15–10:30 | Break | | |
| 10:30–11:30 | Draft the technical trio | `d3-prd`, `d3-blueprint`, `d3-tech-stack` | `PRD.md`, `blueprint.md`, `tech-stack.md` |
| 11:30–12:30 | Explain-back and repo setup | founder pokes holes; `d3-github-setup` | `github.md` |
| 12:30–13:30 | Lunch | | |
| 13:30–16:30 | **Build sprint** | `d3-mvp-build` (branches by path), facilitator circulates 1:1 | `BUILD-LOG.md` + the real slice/prototype/deliverable |
| 16:30–16:50 | Domain, email, landing page | `d3-domain-email`, `d3-landing-site` | `domain-email.md`, `site/index.html` |
| 16:50–17:00 | Tomorrow's test plan, close Day 3 | `d3-next-steps`, `checkpoint close` | `NEXT-STEPS.md` |

**Day 3 deck (5 to 6 slides):** agenda, the MoSCoW/story-map framing, the
"draft first, you correct it" contract for the PRD/blueprint/tech-stack
block (so founders know why Claude moves fast here), then hand off to the
build sprint with one "what ships by 16:30" slide per path. Nothing needed
for the sprint itself.

---

## Day 4: Test and Go to Market

Target: test the build for buying signals, then build the machine that
sells it. The morning is real users testing the real build, booked ahead
of the day, so it's a room full of parallel conversations, not a synced
talk track.

| Time | Block | Skill(s) | Artefact |
|---|---|---|---|
| 09:00–09:15 | Usability test plan | `d4-usability-plan` | `usability-test-plan.md` |
| 09:15–12:30 | **Usability tests** | founders run tests against real users, facilitator on call | raw notes per founder |
| 12:30–13:30 | Lunch | | |
| 13:30–14:00 | Synthesise feedback | `d4-prioritise` | `feedback-synthesis.md` |
| 14:00–14:45 | Messaging and pricing | `d4-icp-messaging`, `d4-pricing-model` (working discussion) | `messaging.md`, `PRICING-MODEL.md` |
| 14:45–15:00 | Break | | |
| 15:15–16:00 | Sales machine | `d4-sales-deck`, `d4-intake-process`, `d4-onboarding-pack`, `d4-marketing-funnel` | `sales-deck.pptx`, `intake-process.md`, `onboarding-pack.pdf`, `funnel.md` |
| 16:00–16:25 | GTM plan | `d4-gtm-plan` (working discussion) | `gtm-plan.md` |
| 16:25–16:45 | **Book the Friday meeting** | `d4-book-sale` | `friday-meeting.md` |
| 16:45–17:00 | Roll call, close Day 4 | who's booked; `checkpoint close` | — |

The 16:25 slot is the gate for the whole week: nobody leaves Thursday
without a real Friday meeting on the calendar. Put that on its own slide,
in the room, with names.

**Day 4 deck (7 to 8 slides):** agenda, what a usability test actually
tests for (buying signals, not bugs), the feedback triage rubric, the
pricing model options with a number attached to each, then the closing
"book it before you leave" slide with the gate stated as plainly as
possible.

---

## Day 5: Tweaks and First Sale

Target: hit the headline number, a real customer commits. This day is
staggered, not synced: each founder's Friday meeting was booked
individually on Day 4 and lands at a different time, so the afternoon is a
window, not a block everyone shares.

| Time | Block | Skill(s) | Artefact |
|---|---|---|---|
| 09:00–09:20 | Triage yesterday's feedback | `d5-triage` | `TRIAGE.md` |
| 09:20–10:30 | Ship the fixes | `d5-ship-fixes` | `DEMO-SCRIPT.md` |
| 10:30–10:45 | Break | | |
| 10:45–11:10 | Set the price | `d5-price-number` (working discussion) | `RATE-CARD.md` |
| 11:10–11:35 | Draft the proposal | `d5-proposal` | `PROPOSAL.md` |
| 11:35–12:30 | Paperwork | `d5-paperwork` | `05-sale/paperwork/` |
| 12:30–13:15 | Lunch (early, protects the afternoon) | | |
| 13:15–13:45 | Rehearse in pairs | `d5-rehearse` | `SALE-SCRIPT.md` |
| 13:45–16:00 | **Sale meetings** (staggered, per founder's booked time) | live, off the plugin | — |
| 16:00–16:20 | Log the outcome | `d5-close` | `WON-DEAL.md` |
| 16:20–16:50 | Compile the launch package | `d5-review` | `LAUNCH-PACKAGE.md` |
| 16:50–17:00 | Demo day: each founder states their number | group close | — |

**Day 5 deck (6 to 7 slides):** agenda, the triage rubric, the pricing
worksheet, a proposal checklist, the rehearsal brief (what to say when they
go quiet), then a blank "state your number" slide left for the room to fill
live at 16:50, that's the actual closing moment of the week.

---

## Open questions before I build the five decks

1. Confirm the 09:00 to 17:00 window (and the 17:30 finish on Day 1), or
   give me the real hours.
2. Confirm cap of 8 in-room interviews on Day 1 is what you want to run
   with, versus capping lower and pushing more to Tuesday overflow.
3. Say the word and I'll build all five as `.pptx` via the `spark-branding`
   skill into `docs/decks/`.
