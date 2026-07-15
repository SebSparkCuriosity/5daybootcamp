---
name: Data Protection
description: Drafts the data-protection documents a regulated firm needs from Monday: a privacy notice, a lawful-basis note, interview and usability consent wording, and an engagement-letter data clause. Use in week one, before you collect a single name.
when_to_use: Run early, ideally Day 1, before the first interview or the landing page goes live. Its consent wording feeds run-interview; its data clause feeds d5-paperwork. Re-run any time your business_type or brand name changes.
---

# Data Protection

**What this does.** Generates four DRAFT data-protection documents for your business, filled in with what we already know about you, ready for a lawyer to check.
**Why it matters.** From Monday you will collect real personal data: interview notes, an email on the landing page, a client file on Friday. In finance, trust, law and fund admin that data is not an afterthought, it is the thing you will be judged on. Get the paperwork drafted before the data arrives and you never have to apologise for collecting names with nowhere to put them. Leave it and you are one subject-access request away from an awkward call.
**You are ready for this when.** `.spark/state.json` exists (the `start` skill created it). A `brand.json` helps but is not required; the generator fills in what it can and marks the rest.

## Before you start
Reads `.spark/state.json` (for your name, idea and `business_type`) and `.spark/brand/brand.json` (for the registered business name), both via the safe helpers. It writes four drafts into `.spark/deliverables/data-protection/`.

Two hard rules, non-negotiable:

Every document here is a **draft**. The generator stamps each one with: "This is a draft. Have a qualified lawyer review it before you rely on it. Spark does not warrant it." That line stays. Spark drafts, a qualified lawyer signs off, you rely on it. Not the other way round.

These documents are **Jersey Data Protection Law 2018 and UK GDPR aware, not authoritative**. They point you at the right questions and the right regulator. They are not legal advice and Spark is not your lawyer.

## Steps
1. Generate the four drafts. Run from your project root:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/generate_docs.py --root .
   ```
   It reads your state and brand, substitutes what it knows, and writes `privacy-notice.md`, `consent.md`, `dpa-clause.md` and `lawful-basis.md`. Anything it cannot know for certain (your contact email, your postal address) it leaves as a visible `[TO COMPLETE: ...]` marker rather than guess. The last line tells you how many markers remain.
2. Open each file and fill every `[TO COMPLETE]` marker. These are the facts only you have: the email people write to about their data, your postal address, and whether the landing page sets any cookies. Do not leave a marker in a document you are about to publish.
3. Read the privacy notice as if you were the prospect, not the author. It must say plainly what you collect, why, where it lives, how long you keep it, and how someone gets their data back. If a line is not true of your business, change it. Never publish a claim about your data handling you do not actually follow.
4. Check the storage default matches reality. Every draft assumes interview and customer data sits in **local files under your control**, with a cloud service used only where a task needs it and the person has been told. If you already plan to put data straight into a cloud tool, say which tool, in the privacy notice, before you collect anything.
5. Read the lawful-basis note and complete the legitimate-interests check for every row that relies on it. If you cannot name the basis for a field, do not collect that field. Data you never collect is data you never have to protect.
6. Send all four drafts to a qualified lawyer for review before you rely on any of them. This is the sign-off gate: outreach and the landing page can go live once the privacy notice and consent wording are in place, but treat legal review as the thing that turns a draft into something you stand behind.

## For software
Your privacy notice goes live with the landing page, so it is public from day one. The cookies and analytics section is the part that bites: if the deployed slice loads any analytics, a font, or an embedded widget, that is a third party seeing your visitors, and it needs consent before it runs and a line in the notice. A bare Next.js and Supabase page with no analytics is the easy case, so keep it that way for launch and add tracking later, with consent.

## For hardware
A pre-order or waitlist page takes names and, for pre-orders, payment intent, so it needs the privacy notice live before it accepts a single sign-up. Payment details are handled by your payment provider, not stored by you, so say that plainly and name the provider. Waitlist emails are marketing: use the single unticked opt-in box from the consent draft, never a pre-ticked one.

## For services
You will hold the most sensitive data of the three paths, because a real client hands you real files on Friday. The engagement-letter data clause (`dpa-clause.md`) is the one that matters most: it is read straight into `d5-paperwork`, so get it drafted and lawyer-checked this week, not on Friday morning. Fill the schedule naming the actual data categories for your specific engagement before the letter goes out.

## The artefact
Writes four Markdown files into `.spark/deliverables/data-protection/`:

- `privacy-notice.md`: the public notice for the landing page.
- `consent.md`: interview, usability-test and marketing consent wording (reused by `run-interview`).
- `dpa-clause.md`: the data-processing clause for the engagement letter (read by `d5-paperwork`).
- `lawful-basis.md`: your internal record of the lawful basis for each kind of data.

What good looks like: a lawyer can read all four in fifteen minutes, every `[TO COMPLETE]` marker is gone, each document carries the disclaimer, and every claim in the privacy notice is something your business actually does.

## Done when
All four drafts exist in `.spark/deliverables/data-protection/` and each one carries the disclaimer. Confirm it mechanically:
```
python3 ${CLAUDE_SKILL_DIR}/scripts/generate_docs.py --root . --check
```
It must print `CHECK_RESULT=OK all 4 drafts present, all carry the disclaimer`. That is 4 of 4, no exceptions.

## Log it
Append one line to CHANGELOG.md and register the artefact in state.json:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill data-protection \
  --artefact .spark/deliverables/data-protection/privacy-notice.md \
  --result "4 data-protection drafts generated, all carry disclaimer"

python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --append-artefact '{"skill":"data-protection","path":".spark/deliverables/data-protection/","result":"4 drafts generated"}'
```
Record the decision on where data lives, because it shapes everything downstream:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --decision "Interview and customer data defaults to local files, cloud export opt-in only" \
  --rationale "Least data exposed for a regulated audience; matches the drafted privacy notice"
```

## If it goes wrong
If the generator cannot read `state.json` or `brand.json`, it does not crash: it fills what it can and leaves the rest as `[TO COMPLETE]` markers, then writes all four drafts anyway. Fill the markers by hand.

If a reference template is missing, the generator writes a safe stub for that document, still carrying the disclaimer and still naming your business, and tells you which one it stubbed. Fix the template or complete the stub by hand, then re-run.

If `--check` reports a failure, re-run the generate step. The generator forces the disclaimer onto every file it writes, so a clean generate always passes the check.
