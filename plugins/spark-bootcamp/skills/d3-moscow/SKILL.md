---
name: MoSCoW Your Requirements
description: Sorts every feature into Must, Should, Could and Won't so you build the smallest thing that sells. Use on Day 3 after product-context.md exists.
when_to_use: Day 3 product, after d3-product-context and with proposition.md in hand, before you build or scope the working slice.
---

# MoSCoW Your Requirements

**What this does.** Sorts every requirement into four buckets, Must, Should, Could and Won't, and caps the Musts at seven so you build the smallest thing a real customer will pay for this week.
**Why it matters.** Overscoping is the single biggest reason a five-day build never ships. Every founder thinks their idea is one feature. It is usually twelve, and eight of them are opinions. MoSCoW forces the cut now, on paper, before you waste build time on things nobody asked for.
**You are ready for this when.** `03-product/product-context.md` and `02-market/proposition.md` both exist.

## Before you start
Read `03-product/product-context.md` (what you are building and for whom) and `02-market/proposition.md` (the promise you are making). The proposition is the referee. Every Must has to earn its place by delivering that promise. If a feature does not, it is not a Must, however much you love it.

Optional but recommended: read the bucket definitions in `${CLAUDE_SKILL_DIR}/references/moscow-rules.md` so you sort honestly rather than flattering your own idea.

## Steps
1. **Brain-dump every requirement first.** List everything the product could do, in one sitting, no sorting. Aim for 15 to 25 lines. You cannot prioritise a list you have not written down.
2. **Sort each line into one bucket.** Use the strict definitions below. Do not invent a fifth bucket. Do not leave anything unsorted.
   - **Must.** Without this, the product does not deliver the proposition and the customer will not pay. It is the promise, made real. If you can ship and still keep the promise without it, it is not a Must.
   - **Should.** Painful to leave out, but the promise survives without it. It goes in version two, next week.
   - **Could.** Nice. Cheap. Only if there is time left, which there will not be.
   - **Won't.** Explicitly out of scope for this week. Naming these is not admitting defeat, it is protecting the build. Write at least three.
3. **Cap the Musts at seven.** If you have more than seven, you have not prioritised, you have relabelled your wish-list. Move the weakest ones down until seven remain. Seven Musts is a week of work. Ten is a month.
4. **Tie every Must back to the proposition in one line.** Beside each Must, write the words from `proposition.md` it delivers. A Must with no line to the proposition is a Should in disguise. Demote it.
5. **Push the MVP boundary hard.** Read your Must list and ask, per line, "would a paying customer walk away without this on day one?" If the honest answer is no, it is a Should. The MVP is the line a customer will cross with a card, nothing past it.
6. **Write at least three explicit Won'ts.** The features you are proudest of are often the ones to park. Login flows, dashboards, settings pages, integrations, mobile apps: usually all Won't for week one. Say so out loud.
7. **Branch on your path only where the Musts differ.** The method is identical across all three. The typical Musts are not.

### For software
Your Musts describe the one working slice on a public URL. Typically: one input, one action, one visible result, and a way to capture the prospect (email or payment intent). Auth, accounts, admin panels and settings are almost always Won't for week one.

### For hardware
Your Musts split across two artefacts: the demonstrable prototype (one CAD render or one physical mock that proves the core idea) and the pre-order or waitlist page that takes real payment intent. Manufacturing tolerances, packaging, a second SKU: Won't. One convincing render plus a page that takes a deposit beats a perfect spec nobody has paid against.

### For services
Your Musts describe one sample deliverable that shows the quality, plus a bookable intake page. Typically: the sample itself, a clear scope of what the package includes, a price, and a way to book. A client portal, tiered packages, automated onboarding: all Won't for week one.

## The artefact
Writes `03-product/requirements-moscow.md` in Markdown. Four headed sections in order: Must, Should, Could, Won't. Under Must, each line names the requirement and, in brackets, the proposition words it delivers. What good looks like: at most 7 Musts, each tied to the proposition, at least 3 Won'ts, and a one-line MVP statement at the top that reads "The smallest thing a customer will pay for is: ...".

Use `${CLAUDE_SKILL_DIR}/references/moscow-template.md` as the starting structure.

## Done when
At most 7 Musts, at least 3 explicit Won'ts, and every single Must carries a bracketed line back to the proposition. If any Must has no proposition link, you are not done: demote it or cut it.

## Log it
Append one line to CHANGELOG.md via the logbook helper (`${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py`): date, `d3-moscow`, the artefact path, and the Must count as the numeric result (for example "5 Musts, 4 Won'ts"). Then update `.spark/state.json` via the journey-state helper (`${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`): record the artefact and set day 3 progress. If a scoping call was contested, note the rationale in DECISIONS.md.

## If it goes wrong
Stuck above seven Musts and every one feels essential? You have two ideas fighting for one week. Pick the half that delivers the proposition most directly, move the rest to Should, and note the split in DECISIONS.md. If you genuinely cannot get below seven, your proposition is too broad: go back to `02-market/proposition.md` and narrow the promise before you build a line of anything.
