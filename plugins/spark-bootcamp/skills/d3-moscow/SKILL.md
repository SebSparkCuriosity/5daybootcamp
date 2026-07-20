---
name: MoSCoW Your Requirements
description: Sorts every feature into Must, Should, Could and Won't and caps Musts at seven so you build the smallest thing that sells. Day 3.
when_to_use: Day 3 product, after d3-product-context, with proposition.md in hand, before you scope the slice.
---

# MoSCoW Your Requirements

**What this does.** Sorts every requirement into Must, Should, Could and Won't, capping Musts at seven.
**Why it matters.** Overscoping is the biggest reason a five-day build never ships, so you make the cut now, on paper, before you waste build time.
**You are ready for this when.** `03-product/product-context.md` and `02-market/proposition.md` both exist.

## Before you start
Read `03-product/product-context.md` and `02-market/proposition.md`. The cut is a working discussion (about 20 minutes): you propose, challenge and count, the founder makes every call. A Must the founder cannot defend out loud is a Should. The proposition is the referee: every Must must deliver it. Bucket definitions: `${CLAUDE_SKILL_DIR}/references/moscow-rules.md`.

## Steps
1. Brain-dump every requirement together, the founder talking, you typing: no sorting, 15 to 25 lines.
2. Sort each line into one bucket. **Must**: without it the promise breaks and nobody pays. **Should**: painful to drop, promise survives, goes in v2. **Could**: cheap, only if time. **Won't**: out of scope this week, name at least three.
3. Cap the Musts at seven. Move the weakest down until seven remain.
4. Beside each Must, write the `proposition.md` words it delivers. No link means it is a Should. Demote it.
5. Per Must, ask the founder "would a paying customer walk away without this on day one?" and wait for their answer. If no, it is a Should. Challenge a kind answer once, with the proposition as referee, then let their call stand.
6. Write at least three explicit Won'ts. Login, dashboards, settings, integrations, mobile: usually Won't.
7. Branch only where the Musts differ. The method is identical.

### For software
Musts describe the one working slice on a public URL: one input, one action, one visible result, one prospect capture (email or payment intent). Auth, accounts, admin, settings: Won't.

### For hardware
Musts split across two artefacts: the demonstrable prototype (one CAD render or physical mock) and the pre-order or waitlist page taking real payment intent. Tolerances, packaging, second SKU: Won't.

### For services
Musts describe one sample deliverable plus a bookable intake page: the sample, a clear scope, a price, a way to book. Client portal, tiered packages, automated onboarding: Won't.

## The artefact
Writes `03-product/requirements-moscow.md`. Four headed sections in order (Must, Should, Could, Won't), each Must naming the requirement and, in brackets, the proposition words it delivers, plus a top line "The smallest thing a customer will pay for is: ...". Start from `${CLAUDE_SKILL_DIR}/references/moscow-template.md`.

## Done when
At most 7 Musts, at least 3 explicit Won'ts, every Must carries a bracketed proposition link.

## Log it
Append to CHANGELOG.md via `${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py` with `--skill d3-moscow --artefact 03-product/requirements-moscow.md --result` (the Must count, e.g. "5 Musts, 4 Won'ts"). Update day 3 progress via `${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py --patch`. Note contested calls in DECISIONS.md.

## If it goes wrong
Stuck above seven and all feel essential? You have two ideas fighting for one week. Keep the half that delivers the proposition most directly, move the rest to Should, note the split in DECISIONS.md. If you still cannot get below seven, your proposition is too broad: narrow `02-market/proposition.md` first.
