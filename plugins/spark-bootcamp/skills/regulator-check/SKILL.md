---
name: Regulator Check
description: Scans an artefact for unsupported numeric or comparative claims and rules on each before it ships to a prospect.
when_to_use: Before any deck, landing page, proposal or email goes out, especially Day 4 outreach and Day 5 sale.
argument-hint: [path to the file to check]
---

# Regulator Check

**What this does.** Reads one artefact, finds every numeric and comparative claim, and rules each sourced, soften, or red in a compliance note beside the file.
**Why it matters.** In finance, trust, law and fund admin an unsupported claim is a liability, and one overclaim in a deck can end a deal, so this catches those lines while they are still cheap to change.
**You are ready for this when.** The file you want to ship exists on disk (`.md`, `.html`, `.txt` or a plain deck export).

## Before you start
Reads the file you point it at and `.spark/state.json` (via journey-state) for `business_type`, since the bar differs by path. Rulings are proposals: walk every amber and red past the founder before applying a fix, because it is their name on the claim; an overruled amber is their call to defend, logged in DECISIONS.md. This skill reviews only, it sends nothing: you sign off fixes before any outreach leaves (Day 4 human-in-the-loop).

## Steps
1. Scan the file from the project root:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/scan_claims.py --file <path-to-artefact> --root .
   ```
   It extracts every candidate claim (numbers, percentages, money, superlatives, comparatives, regulated red-flags like "guaranteed", "risk-free", "regulated", "compliant", "returns") and writes a draft note with each row `UNRESOLVED`.
2. Open `.spark/deliverables/compliance-note-<artefact>.md` and rule each claim, replacing `UNRESOLVED`:
   - **SOURCED (green).** A real source: a logged result, a named report, a citable client figure. Record it. A figure from your CHANGELOG.md counts; a half-remembered one does not.
   - **SOFTEN (amber).** True-ish but not provable as worded. Rewrite it defensible, ideally to one named pilot's figure.
   - **RED.** Cannot be supported or softened. It comes out. Superlatives and any guarantee of a financial return are almost always red for a regulated audience.
3. Write the exact replacement into the "Suggested fix" column for every amber and red, so editing the source is copy-paste.
4. Watch the regulated red flags hardest. See `${CLAUDE_SKILL_DIR}/references/red-flags.md`.
5. Apply the fixes to the original file, then re-run the scanner. Nothing stays UNRESOLVED.

## For software
Landing-page offenders: "10x faster", "bank-grade security", uptime, user counts. Soften anything unmeasured. Never claim a security certification you do not hold.

## For hardware
Spec claims are the risk: battery life, tolerances, throughput. Cite the datasheet, or say "in early testing" and name the test. Pre-order pages must not imply a ship date you cannot hit.

## For services
Held tightest, a proposal is a promise to a named person. Every outcome figure needs a source or an honest hedge. Fee and turnaround claims must match what you can deliver in the week.

## The artefact
Writes `.spark/deliverables/compliance-note-<artefact>.md` in Markdown: a one-line summary (claims found, how many red), a table (Claim, Where, Type, Verdict, Source or fix), ending with the standard draft-and-review notice. Good looks like: a stranger checks each row against the file and finds zero claims that would embarrass you in front of a regulator, and no reds remain.

## Done when
Every claim is resolved (SOURCED with a source, SOFTEN with fix applied, or deleted). Re-running `scan_claims.py` reports `UNRESOLVED: 0` and `RED remaining in file: 0`.

## Log it
Replace `<artefact>` and `<N>` with the file name and claim count the scanner printed:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill regulator-check \
  --artefact .spark/deliverables/compliance-note-<artefact>.md \
  --result "<N> claims checked, 0 red remaining"
```

## If it goes wrong
If the scanner cannot read the file (binary deck, PDF, odd encoding), it writes an empty note skeleton: export to plain text or Markdown and re-run. If it finds no claims, skim the file by eye against `${CLAUDE_SKILL_DIR}/references/red-flags.md` before trusting a clean bill.
