---
name: Regulator Check
description: Reviews any artefact for unsupported claims before it ships. Point it at a deck, a landing page or a proposal; it flags every numeric or comparative claim that is not sourced. Use before anything goes to a prospect.
when_to_use: Any day, before a deck, landing page, proposal or email goes out. Especially before Day 4 GTM outreach and the Day 5 sale, and any time the audience is a regulated Jersey firm.
argument-hint: [path to the file to check]
---

# Regulator Check

**What this does.** Reads one artefact you are about to ship, finds every numeric and comparative claim in it, and rules on each: sourced, soften, or red. It writes a compliance note beside the file so you fix the words before a prospect, or a regulator, reads them.
**Why it matters.** In finance, trust, law and fund admin, an unsupported claim is not marketing, it is a liability. "The fastest onboarding in Jersey" or "cut costs by 40%" reads fine until a client, or the JFSC, asks you to prove it and you cannot. This check catches those lines while they are still cheap to change. One overclaim in a deck can end a deal in a regulated sector.
**You are ready for this when.** The file you want to ship already exists on disk (a `.md`, `.html`, `.txt` or plain deck export).

## Before you start
Reads the one file you point it at (the target artefact). It also reads `.spark/state.json` via the journey-state helper to note your `business_type`, because the bar differs by path: a services proposal makes explicit promises to a named buyer, so it is held tightest.

Guardrail: this skill does not send anything. It reviews and reports. You still decide what to change, and no outreach leaves until you have signed off the fixes (see the human-in-the-loop rule on Day 4).

## Steps
1. Point the scanner at your file. Run it from the founder's project root:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/scan_claims.py --file <path-to-artefact> --root .
   ```
   It extracts every candidate claim: numbers, percentages, money, superlatives ("best", "leading", "fastest", "only", "#1"), comparatives ("cheaper", "more than", "faster than"), and regulated red-flag phrases ("guaranteed", "risk-free", "regulated", "compliant", "approved", "returns"). It writes a draft compliance note with one row per claim, each marked `UNRESOLVED`.
2. Open the draft note the script wrote at `.spark/deliverables/compliance-note-<artefact>.md`. Work down the table. For each claim, decide its verdict and write it in, replacing `UNRESOLVED`:
   - **SOURCED (green).** You can point to a real source: your own logged result, a named report, a client figure you are allowed to cite. Put the source in the note. A figure from your own CHANGELOG.md counts; a figure you half-remember does not.
   - **SOFTEN (amber).** The claim is true-ish but not provable as worded. Rewrite it into something defensible. "Cut costs by 40%" with no source becomes "designed to reduce manual processing time" or, better, a figure from one real pilot with the pilot named.
   - **RED.** The claim cannot be supported and cannot be softened without becoming meaningless. It comes out. Superlatives ("the best in Jersey") and any guarantee of a financial return are almost always red for a regulated audience.
3. For every amber and red row, write the exact replacement wording in the "Suggested fix" column, so editing the source file is copy and paste, not a fresh think.
4. Watch the regulated red flags hardest. Any promise of returns, any "risk-free", any "regulated by" or "compliant" you have not actually earned, and any superlative aimed at a finance, trust or law buyer. See `${CLAUDE_SKILL_DIR}/references/red-flags.md` for the phrases that end deals and why.
5. Apply the fixes to the original file yourself, then re-run the scanner. A claim is only closed when it reads as SOURCED, SOFTEN (with fix applied) or has been deleted. Nothing stays UNRESOLVED.

## For software
The usual offenders live on the landing page: "10x faster", "bank-grade security", uptime percentages, user counts. If you have not measured it or cannot cite the underlying provider (for example Supabase's own security posture rather than your own), soften it. Never claim a security certification you do not hold.

## For hardware
Spec claims are the risk: battery life, tolerances, throughput, "lasts twice as long". If the number comes from a datasheet, cite the datasheet. If it comes from one bench test, say "in early testing" and name the test. Pre-order pages must not imply a ship date you cannot hit.

## For services
Held tightest, because a proposal is a promise to a named person. Every outcome figure needs a source or a hedge: "typically" and "based on similar engagements" are honest when you have one prior engagement, dishonest when you have none. Fee and turnaround claims must match what you can actually deliver in the week.

## The artefact
Writes `.spark/deliverables/compliance-note-<artefact>.md` in Markdown. It holds: a one-line summary (claims found, and how many red), then a table with columns Claim, Where (line or section), Type, Verdict, Source or fix. It ends with the standard draft-and-review notice, because a compliance note is not legal advice.

What good looks like: a stranger reads the note, checks each row against the source file, and finds zero claims that would embarrass you in front of a regulator. Green rows carry a real source. Amber rows carry rewritten wording. No reds remain in the shipped file.

## Done when
Every claim in the note is resolved: marked SOURCED with a source, SOFTEN with the fix applied to the source file, or deleted. Concretely: re-running `scan_claims.py` reports `UNRESOLVED: 0` and `RED remaining in file: 0`. The scanner prints both counts.

## Log it
Append one line to CHANGELOG.md and record the artefact in state.json. Replace `<artefact>` and `<N>` with the file name and the claim count the scanner printed:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill regulator-check \
  --artefact .spark/deliverables/compliance-note-<artefact>.md \
  --result "<N> claims checked, 0 red remaining"

python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --append-artefact '{"skill":"regulator-check","path":".spark/deliverables/compliance-note-<artefact>.md","result":"<N> claims checked, 0 red remaining"}'
```
If a specific claim was cut for a reason worth remembering, log the decision too:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --decision "Cut '<claim>' from <artefact>" \
  --rationale "Unsupported return claim, red for a regulated audience"
```

## If it goes wrong
If the scanner cannot read the file (a binary deck, a PDF, an odd encoding), it says so and writes an empty note skeleton. Export the deck to plain text or Markdown first, or paste the copy into a `.md` file, then re-run.

If the scanner finds no candidate claims at all, either the file genuinely makes no claims (rare for anything selling something) or the copy is in a format it could not parse. Skim the file yourself before trusting a clean bill: read `${CLAUDE_SKILL_DIR}/references/red-flags.md` and check by eye.
