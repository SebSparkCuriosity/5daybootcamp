---
name: Choose The Stack
description: "Pick one stack with a monthly cost, not a menu. Software default: Next.js, Supabase, Vercel. Day 3, after the blueprint."
when_to_use: "Day 3, straight after the blueprint, before you scaffold. Decide what to build on and what it costs per month."
---

# Choose The Stack

**What this does.** Turns your blueprint into one chosen stack, with a monthly cost, the accounts to open, and the MCP servers to connect.
**Why it matters.** You do not need the best stack, you need one that ships this week and costs almost nothing, and one decision now beats a week of open tabs.
**You are ready for this when.** `03-product/product-context.md` and `03-product/docs/blueprint.md` both exist.

## Before you start
Read both files above. Read `business_type` from `.spark/state.json` (via journey-state); it decides your branch. Follow only your branch. No money is spent here: you choose the stack and list accounts, paid accounts open later with your sign-off. Everything has a free tier that carries you to first paying customer.

## Steps
1. Confirm your path from `business_type`.
2. Follow only your branch below. Take the recommendation as written unless the blueprint names a hard constraint (existing system, regulator rule, payment method buyers insist on). If so, note the constraint and the one change, with a number, in `DECISIONS.md`.
3. Get a firm monthly figure: `python3 ${CLAUDE_SKILL_DIR}/scripts/stack-cost.py <software|hardware|services>`. It prints free-tier total (usually £0) and the realistic paid total.
4. List every account to open and whether it needs a card on file (a card on file is not a charge, but flag it for finance sign-off).
5. List the MCP servers to connect. See `references/mcp-setup.md` for connect steps.
6. Explain the stack back in plain English (5 minutes): what each piece does, what it costs monthly, what breaks first and who fixes it. The founder owns this stack after the week ends, so invite questions until they can say what they are paying for.
7. Write the artefact.

## For software
**Next.js on Vercel, Supabase for database and auth.** Cost to first customer: **£0**, stepping to about £45/mo with real users (Vercel Pro £16, Supabase Pro £19, domain ~£10/yr). Same-firm deploy is one command to a public URL in under two minutes, Supabase gives real Postgres, login and storage, and both connect to Claude Code over MCP so I build and deploy for you. No-code branch: if the slice is a form, booking or content page with no custom logic, use **Softr or Carrd on an Airtable base**, ~£0 to £24/mo, ship in hours. Note the choice in `DECISIONS.md`. Do not pick no-code just because code feels scary, I will do the code.
Accounts: GitHub (free), Vercel (free, no card on hobby), Supabase (free, no card). No-code: Airtable plus Softr or Carrd.
MCP servers: GitHub and Supabase. Connect both now.

## For hardware
**Onshape for the CAD render, plus a Carrd pre-order page wired to a Stripe payment link.** Cost to first customer: **£0** (Onshape free for public docs, Carrd free for one site, Stripe charges only 1.5% plus 20p per transaction). Your Day 3 job is a demonstrable prototype and a page taking real payment intent. A physical mock photo can beat a render, use whichever you can produce today, note which in `DECISIONS.md`.
Accounts: Onshape (free), Carrd (free), Stripe (free to open, needs bank and identity details, takes a day so start now, needs card and business details on file, flag for finance sign-off).
MCP servers: none required. Add GitHub MCP later if the page becomes a coded site.

## For services
**Google Docs for the sample deliverable, a Carrd landing page, Cal.com for the bookable intake.** Cost to first customer: **£0**, all three free-tiered to a signed client. The proof is one real sample deliverable plus a way to book time: Google Docs drafts it and exports clean PDF, Cal.com puts a real "book a call" button with your availability, Carrd holds it together. On Microsoft 365, use Word and Bookings instead, note it in `DECISIONS.md`.
Accounts: Google (free), Carrd (free), Cal.com (free). No card on file needed.
MCP servers: none required.

## The artefact
Writes `03-product/docs/tech-stack.md` in Markdown, in prose: the one named stack in a sentence; the monthly cost as one free-tier number (usually £0) and one realistic paid number, each with components; accounts to open and whether each needs a card; MCP servers or "none required"; any deviation cross-referenced to `DECISIONS.md`. Good: finance reads it in two minutes and approves, because there is a number.

## Done when
Exactly one stack is chosen (not a shortlist), the monthly cost is stated as a number, and the accounts and MCP servers are listed. If any is missing or hedged, you are not done.

## Log it
`python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py --skill d3-tech-stack --artefact 03-product/docs/tech-stack.md --result "£0/mo to first customer"`. If you deviated, the reasoning goes in `DECISIONS.md`.

## If it goes wrong
Cannot decide code versus no-code, or CAD versus physical mock? Default to the faster one and ship, a paying customer funds any rebuild. The only wrong move on Day 3 is spending the day choosing. If the cost calculator will not run, the free-tier answer is £0 for all three paths, so state that and move on.
