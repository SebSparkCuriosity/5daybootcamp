---
name: Choose The Stack
description: Pick one stack with a monthly cost, not a menu. Software default is Next.js plus Supabase plus Vercel. Use on Day 3 after the blueprint.
when_to_use: Day 3 product build, straight after the blueprint is written, before you scaffold or wire up anything. Use when you need to decide what to build on and what it costs per month.
---

# Choose The Stack

**What this does.** Turns your blueprint into one chosen stack, with a monthly cost, the accounts you need to open, and the MCP servers to connect.
**Why it matters.** Founders lose days comparing tools. You do not need the best stack, you need one that ships this week and costs almost nothing. One decision, made now, beats a week of tabs open.
**You are ready for this when.** `03-product/docs/product-context.md` and `03-product/docs/blueprint.md` both exist.

## Before you start
Read `03-product/docs/product-context.md` and `03-product/docs/blueprint.md`. Read `business_type` from `.spark/state.json` (via the journey-state helper). That one field decides which branch below you follow. Do not read all three branches, read yours.

No money is spent in this skill. You choose the stack and list the accounts. Opening paid accounts happens later, with your sign-off, in the build skills. Everything recommended here has a free tier that carries you to first paying customer.

## Steps
1. Confirm your path from `business_type`. Software, hardware or services.
2. Follow only your branch below. Take the recommendation as written unless the blueprint names a hard constraint (an existing system you must integrate with, a regulator rule, a payment method your buyers insist on). If it does, note the constraint and the one change you made, with a number, in `DECISIONS.md`.
3. Run the cost calculator to get a firm monthly figure: `python3 ${CLAUDE_SKILL_DIR}/scripts/stack-cost.py <software|hardware|services>`. It prints the free-tier total (usually £0) and the realistic paid total once you have real traffic or orders.
4. List every account you must open and whether it needs a card on file. A card on file is not a charge. It matters for regulated founders who need finance sign-off, so flag it.
5. List the MCP servers to connect in Claude Code, so the build skills can act directly. See `references/mcp-setup.md` for the exact connect steps.
6. Write the artefact. One stack, one cost, the accounts, the MCPs.

## For software
Recommendation: **Next.js on Vercel, with Supabase for the database and auth.** Monthly cost to first paying customer: **£0.** You stay inside free tiers until you have real users, then it steps to about £45 per month (Vercel Pro £16 plus Supabase Pro £19 plus a domain at around £10 a year, so £10 amortised).

Why this and not something else. Next.js and Vercel are made by the same firm, so deploying is one command and a public URL comes back in under two minutes. Supabase gives you a real Postgres database, login, and file storage without you managing a server. All three have generous free tiers and connect to Claude Code over MCP, so I can build and deploy for you rather than you copying steps.

The no-code branch. If your slice is a form, a booking, or a simple content page with no custom logic, do not write code. Use **Softr or Carrd on top of an Airtable base**, cost about £0 to £24 per month. You will ship in hours, not days. Choose this if the blueprint has no feature that needs real backend logic. Note the choice and the reason in `DECISIONS.md`. Be honest: if you picked no-code only because code feels scary, that is not a reason, I will do the code for you.

Accounts to open: GitHub (free), Vercel (free, card not needed for hobby tier), Supabase (free, card not needed for free tier). For no-code: Airtable plus Softr or Carrd.

MCP servers: GitHub and Supabase. Connect both now so the build skills can create the repo, run migrations and read logs directly.

## For hardware
Recommendation: **Onshape for the CAD render, plus a Carrd pre-order page wired to a Stripe payment link.** Monthly cost to first paying customer: **£0.** Onshape has a free plan for public documents, Carrd is free for one site (£15 a year for a custom domain if you want one), and Stripe charges nothing monthly, only 1.5 percent plus 20p per transaction when you actually take money.

Why this. Your Day 3 job is a demonstrable prototype and a page that takes real payment intent, not a finished product. Onshape runs in the browser so there is nothing to install, and it produces a clean render you can drop straight onto the page. A Stripe payment link is the fastest honest way to prove someone will pay: they enter card details, you take a small deposit or a full pre-order, and that is a real signal, not a "would you be interested" nod.

If you have a physical mock instead of CAD, that is fine and often better. A phone photo of a taped-together prototype on the page can outperform a render. Use whichever you can produce today. Note which in `DECISIONS.md`.

Accounts to open: Onshape (free), Carrd (free), Stripe (free to open, needs bank and identity details, this takes a day so start it now). Stripe needs a card and business details on file, flag this for finance sign-off if you are inside a regulated firm.

MCP servers: none required for the CAD work. If your pre-order page grows into a coded site, add the GitHub MCP later.

## For services
Recommendation: **Google Docs for the sample deliverable, a Carrd landing page, and Cal.com for the bookable intake.** Monthly cost to first paying customer: **£0.** All three have free tiers that carry you to a signed client. Cal.com free covers one-to-one bookings; Carrd free covers one site; Google Docs is free with any Google account.

Why this. Your product is a productised service, so the proof is one real sample deliverable plus a way for a prospect to book time. You do not need software, you need something a buyer can look at and act on. Google Docs lets me draft the sample deliverable with you and export a clean PDF. Cal.com puts a real "book a call" button on the page with your actual availability, which converts far better than "email me". Carrd holds it all together.

If you already run Microsoft 365, use Word and Bookings instead of Google and Cal.com. Same shape, one less account. Note it in `DECISIONS.md`.

Accounts to open: Google (free, likely have it), Carrd (free), Cal.com (free). No card on file needed for any of them.

MCP servers: none required. Everything here is document and page work I can do directly.

## The artefact
Writes `03-product/docs/tech-stack.md` in Markdown. It states, in prose:
- The one stack, named, in a single sentence.
- The monthly cost, as one number for the free tier (usually £0) and one realistic paid number once you have traffic or orders, each with its components.
- The accounts to open, and for each whether a card is needed on file.
- The MCP servers to connect, or "none required".
- Any deviation from the recommendation and why, cross-referenced to `DECISIONS.md`.

What good looks like: someone in your finance team reads it in two minutes and can approve the spend, because there is a number, not a shrug.

## Done when
Exactly one stack is chosen (not two, not a shortlist), the monthly cost is stated as a number, and the accounts and MCP servers are listed. If any of those three is missing or hedged, you are not done.

## Log it
Append one line to `CHANGELOG.md` via the logbook helper: date, `d3-tech-stack`, the artefact path, and the monthly cost as the numeric result. For example `python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py --skill d3-tech-stack --path 03-product/docs/tech-stack.md --result "£0/mo to first customer"`. Then update `.spark/state.json` via the journey-state helper: record the artefact and mark day 3 progress. If you deviated from the recommendation, the reasoning line goes in `DECISIONS.md`.

## If it goes wrong
Cannot decide between code and no-code for software, or CAD versus physical mock for hardware? Default to the faster one and ship. You can always rebuild on a stronger stack once someone has paid, and a paying customer funds that rebuild. The only wrong move on Day 3 is spending the day choosing. If the cost calculator will not run (no Python), the free-tier answer is £0 for all three paths as written above, so state that and move on.
