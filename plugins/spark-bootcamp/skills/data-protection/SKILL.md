---
name: Data Protection
description: Drafts four data-protection documents a regulated firm needs in week one: privacy notice, lawful-basis note, consent wording and engagement-letter data clause.
when_to_use: Run Day 1, before the first interview or landing page. Feeds run-interview and d5-paperwork.
---

# Data Protection

**What this does.** Generates four DRAFT data-protection documents for your business, pre-filled from what we know, ready for a lawyer to check.
**Why it matters.** From Monday you collect real personal data, and in finance, trust, law and fund admin that data is the thing you are judged on, so get the paperwork drafted before the data arrives.
**You are ready for this when.** `.spark/state.json` exists. A `brand.json` helps but is not required.

## Before you start
Reads `.spark/state.json` and `.spark/brand/brand.json` via the safe helpers. Writes four drafts into `.spark/deliverables/data-protection/`.

Every document is a draft. Each is stamped: "This is a draft. Have a qualified lawyer review it before you rely on it. Spark does not warrant it." That line stays. The drafts are Jersey Data Protection Law 2018 and UK GDPR aware, not authoritative, and not legal advice.

## Steps
1. Generate the drafts from your project root:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/generate_docs.py --root .
   ```
   Writes `privacy-notice.md`, `consent.md`, `dpa-clause.md`, `lawful-basis.md`. Facts it cannot know become visible `[TO COMPLETE: ...]` markers.
2. Fill every `[TO COMPLETE]` marker: contact email, postal address, whether the landing page sets cookies. Leave none in anything you publish.
3. Read the privacy notice as the prospect. It must state plainly what you collect, why, where it lives, how long you keep it, how someone gets it back. Never claim a data practice you do not follow.
4. Check the storage default matches reality: drafts assume data sits in local files under your control, cloud only where told. If you plan a cloud tool, name it in the notice before collecting.
5. Complete the legitimate-interests check in the lawful-basis note for every row that relies on it. If you cannot name a basis for a field, do not collect that field.
6. Send all four drafts to a qualified lawyer before you rely on any of them. This is the sign-off gate.

## For software
The privacy notice goes public with the landing page. Any analytics, font or embedded widget is a third party seeing visitors: it needs consent and a line in the notice. Keep a bare Next.js and Supabase page tracking-free for launch, add tracking later with consent.

## For hardware
The pre-order or waitlist page needs the privacy notice live before its first sign-up. Payment details are held by your provider, not you: say so and name the provider. Waitlist emails are marketing: use the single unticked opt-in box, never pre-ticked.

## For services
You hold the most sensitive data: real client files on Friday. The engagement-letter data clause (`dpa-clause.md`) matters most and reads straight into `d5-paperwork`, so get it drafted and lawyer-checked this week. Fill the schedule naming the actual data categories before the letter goes out.

## The artefact
Four Markdown files in `.spark/deliverables/data-protection/`: `privacy-notice.md` (public notice), `consent.md` (interview, usability and marketing wording, reused by `run-interview`), `dpa-clause.md` (engagement-letter clause, read by `d5-paperwork`), `lawful-basis.md` (internal lawful-basis record). Good: a lawyer reads all four in fifteen minutes, no `[TO COMPLETE]` markers left, each carries the disclaimer.

## Done when
All four drafts exist and each carries the disclaimer. Confirm:
```
python3 ${CLAUDE_SKILL_DIR}/scripts/generate_docs.py --root . --check
```
Must print `CHECK_RESULT=OK all 4 drafts present, all carry the disclaimer`. 4 of 4, no exceptions.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill data-protection \
  --artefact .spark/deliverables/data-protection/privacy-notice.md \
  --result "4 data-protection drafts generated, all carry disclaimer"
```

## If it goes wrong
The generator never crashes on missing `state.json` or `brand.json`: it fills what it can, leaves the rest as `[TO COMPLETE]` markers, and writes all four. A missing template becomes a safe stub carrying the disclaimer and naming your business, and it tells you which. If `--check` fails, re-run generate: a clean generate always passes.
