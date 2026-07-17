# The journey map

This is the coach's routing table in plain English. The script
`scripts/coach-route.py` holds the same map in code and is the source of truth.
If a day's skills ship under different ids, change the map in the script and
mirror it here. Keep the two in step.

The coach walks a day's chain top to bottom and stops at the first step whose
artefact does not yet exist. That step's skill is the one command it hands the
founder. Pre-work gates the whole week: until `state.prework.complete` is true,
the coach routes inside the pre-work chain and never points at a day skill.

## Pre-work (`00-prework/`), 2 to 4 weeks before the bootcamp Monday
Target: idea captured, and 8 to 12 interviews booked for the bootcamp Monday.
Nobody is free for an interview tomorrow, so invitations go out weeks ahead.

1. `p0-interview-triage` writes `00-prework/interview-target-spec.md`
2. `p0-invite-list` writes `00-prework/invite-list.csv`
3. `p0-invitations` writes `00-prework/invitation-pack.md`
4. `p0-schedule` writes `00-prework/interview-schedule.md`, keeps
   `state.prework.interviews_booked` current, and sets `state.prework.complete`
   once 8+ interviews are booked (or the founder consciously accepts 5 to 7).

## Day 1: Idea and Discovery (`01-discovery/`)
Target: develop the idea deep enough to test, then hold the interviews booked
in pre-work (Monday afternoon, with Tuesday morning as overflow).

1. `d1-refine-idea` writes `01-discovery/idea-brief.md`
2. `d1-interview-plan` writes `01-discovery/interview-plan.md`
3. `d1-write-script` writes `01-discovery/interview-script.md`
4. `run-interview` writes one record per session under `01-discovery/interviews/`
5. `synthesise-interviews` writes `01-discovery/discovery-findings.md`
6. `d1-validated-problem` writes `01-discovery/validated-problem.md`

## Day 2: Market and Proposition (`02-market/`)
Target: size the market, sharpen the proposition, hand out a pitch deck.

1. `d2-market-map` writes `02-market/market-map.md`
2. `d2-market-sizing` writes `02-market/market-sizing.md`
3. `d2-competitor-scan` writes `02-market/competitors.md`
4. `d2-positioning` writes `02-market/positioning.md`
5. `d2-proposition` writes `02-market/proposition.md`
6. `d2-messaging` writes `02-market/messaging.md`
7. `d2-brand-foundations` writes `02-market/brand/brand-foundations.md`
8. `d2-visual-identity` writes `02-market/brand/brand-board.html`
9. `brand-register` writes `.spark/brand/brand.json` (read by every document after it)
10. `d2-pitch-deck` writes `02-market/pitch-deck.pptx`

## Day 3: Product and Build (`03-product/`)
Target: ship the smallest slice a real prospect can act on. Branches by path.

1. `d3-product-context` writes `03-product/product-context.md`
2. `d3-moscow` writes `03-product/requirements-moscow.md`
3. `d3-story-map` writes `03-product/story-map.md`
4. `d3-prd` writes `03-product/docs/PRD.md`
5. `d3-blueprint` writes `03-product/docs/blueprint.md`
6. `d3-tech-stack` writes `03-product/docs/tech-stack.md`
7. `d3-github-setup` writes `03-product/github.md`
8. `d3-mvp-build` writes `03-product/BUILD-LOG.md` (software: deployed slice; hardware: prototype plus pre-order page; services: sample deliverable plus intake page)
9. `d3-domain-email` writes `03-product/domain-email.md`
10. `d3-landing-site` writes `03-product/site/index.html`
11. `d3-next-steps` writes `03-product/NEXT-STEPS.md`

## Day 4: Test and Go to Market (`04-gtm/`)
Target: test the build for buying signals, then build the machine that sells it.

1. `d4-usability-plan` writes `04-gtm/tests/usability-test-plan.md`
2. `d4-prioritise` writes `04-gtm/feedback-synthesis.md`
3. `d4-icp-messaging` writes `04-gtm/messaging.md`
4. `d4-sales-deck` writes `04-gtm/sales-deck.pptx`
5. `d4-intake-process` writes `04-gtm/ops/intake-process.md`
6. `d4-onboarding-pack` writes `04-gtm/onboarding-pack.pdf`
7. `d4-marketing-funnel` writes `04-gtm/funnel.md`
8. `d4-gtm-plan` writes `04-gtm/gtm-plan.md`
9. `d4-book-sale` writes `04-gtm/friday-meeting.md` (the booked Friday meeting, the Thursday gate)

## Day 5: Tweaks and First Sale (`05-sale/`)
Target: hit your headline number, a real customer commits.

1. `d5-triage` writes `05-sale/TRIAGE.md`
2. `d5-ship-fixes` writes `05-sale/DEMO-SCRIPT.md`
3. `d5-pricing-model` writes `05-sale/PRICING-MODEL.md`
4. `d5-price-number` writes `05-sale/RATE-CARD.md`
5. `d5-proposal` writes `05-sale/PROPOSAL.md`
6. `d5-paperwork` writes the files under `05-sale/paperwork/`
7. `d5-rehearse` writes `05-sale/SALE-SCRIPT.md`
8. `d5-close` writes `05-sale/WON-DEAL.md`
9. `d5-review` writes `05-sale/LAUNCH-PACKAGE.md`

## How completeness is judged

A step counts as done when its artefact exists on disk, or when the artefact
path appears in `state.artefacts[]`. A whole day counts as done only when
`state.days[n].complete` is `true`, which `checkpoint close` sets after the
founder signs it off. So a day can have all its artefacts present and still not
be signed off; in that case the coach points back at the last skill in the chain
to confirm and close the day.

Pre-work is different: its artefacts can all exist while bookings still trickle
in, so it closes on `state.prework.complete`, set by `p0-schedule` when 8 or
more interviews are booked. Until then the coach keeps pointing at
`p0-schedule` on every run.
