# The journey map

This is the coach's routing table in plain English. The script
`scripts/coach-route.py` holds the same map in code and is the source of truth.
If a day's skills ship under different ids, change the map in the script and
mirror it here. Keep the two in step.

The coach walks a day's chain top to bottom and stops at the first step whose
artefact does not yet exist. That step's skill is the one command it hands the
founder.

## Day 1: Discovery (`01-discovery/`)
Target: prove real people feel the pain, from 8 to 12 interviews.

1. `d1-refine-idea` writes `01-discovery/idea-brief.md`
2. `d1-define-interviewees` writes `01-discovery/interview-target-spec.md`
3. `d1-contact-list` writes `01-discovery/contact-list.md`
4. `d1-run-interviews` writes `01-discovery/interview-notes.md`
5. `d1-synthesise` writes `01-discovery/discovery-synthesis.md`

## Day 2: Market (`02-market/`)
Target: size the market and stake out one position you can win.

1. `d2-market-map` writes `02-market/market-map.md`
2. `d2-competitors` writes `02-market/competitor-scan.md`
3. `d2-positioning` writes `02-market/positioning.md`
4. `d2-pricing` writes `02-market/pricing.md`

## Day 3: Product (`03-product/`)
Target: ship the smallest slice a real prospect can act on. Branches by path.

1. `d3-scope` writes `03-product/scope.md`
2. `d3-brand` writes `.spark/brand/brand.json`
3. `d3-build` writes `03-product/build-notes.md` (software: deployed slice; hardware: prototype plus pre-order page; services: sample deliverable plus intake page)

## Day 4: Go to market (`04-gtm/`)
Target: one live page and an outreach list ready to send.

1. `d4-offer` writes `04-gtm/offer.md`
2. `d4-landing` writes `04-gtm/landing-page.md`
3. `d4-outreach` writes `04-gtm/outreach-list.md`

## Day 5: The sale (`05-sale/`)
Target: hit your headline number, a real customer acts.

1. `d5-send` writes `05-sale/outreach-log.md`
2. `d5-close` writes `05-sale/sale.md`

## How completeness is judged

A step counts as done when its artefact exists on disk, or when the artefact
path appears in `state.artefacts[]`. A whole day counts as done only when
`state.days[n].complete` is `true`, which the day's closing skill sets after the
founder signs it off. So a day can have all its artefacts present and still not
be signed off; in that case the coach points back at the last skill in the chain
to confirm and close the day.
