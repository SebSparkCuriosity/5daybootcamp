---
name: Synthesise Interviews
description: Reads a folder of interview records and pulls out counted patterns: assumptions validated or killed, jobs, pains, gains, and warm prospects.
when_to_use: Day 1 after run-interview, or Day 4 product-test mode to feed d4-prioritise. Takes a mode argument.
argument-hint: [discovery|product-test]
---

# Synthesise Interviews

**What this does.** Reads every interview record in a folder and turns it into findings backed by counts: each assumption marked validated, killed or unclear against a tally, jobs, pains and gains ranked by frequency, a sharpened segment, and warm prospects tagged for Day 4.
**Why it matters.** Founders synthesise by memory and remember the flattering bits, so counting the evidence is what keeps you from betting the week on one warm chat.
**You are ready for this when.** `01-discovery/interviews/` holds a record (discovery), or `04-gtm/tests/sessions/` holds sessions (product-test).

## Before you start
Mode from the argument, default discovery:
- **discovery** (Day 1): reads `01-discovery/interviews/*.md`, writes `01-discovery/discovery-findings.md`.
- **product-test** (Day 4): reads `04-gtm/tests/sessions/*.md`, writes `04-gtm/product-test-findings.md` to feed `d4-prioritise`.

Read `01-discovery/idea-brief.md` for the assumptions, the WTP reference at `${CLAUDE_PLUGIN_ROOT}/skills/interview-method/references/wtp-signals.md`, and the full method at `${CLAUDE_SKILL_DIR}/references/synthesis-guide.md`.

Guardrail: this is read-and-report only. Do not message interviewees, promise anything or spend money. Warm prospects get tagged for Day 4, not contacted.

## Steps
1. Count records first. Run `python3 ${CLAUDE_SKILL_DIR}/scripts/scan-interviews.py 01-discovery/interviews` (point at `04-gtm/tests/sessions` in product-test mode). 8+ is strong, 5-7 usable (flag the thin base), 1-4 tentative, 0 stop.
2. Read every record. Note jobs, real pains, what "done well" looks like, and buying signal. Anchor to past behaviour, not opinions.
3. Mark each riskiest assumption: one verdict (VALIDATED, KILLED, UNCLEAR, UNTESTED) with its tally and cited records, e.g. "6 of 9, cites (interviews/03-jane.md)". One chat is not a verdict. Before writing the findings, read each verdict and its tally to the founder: they heard tone the notes lost and may re-tag an UNCLEAR. The counts stand; the interpretation is shared. Log material verdicts as decisions (see Log it).
4. Rank jobs, pains and gains by frequency, each with tally and cited records. A single record is a hunch, not a pattern.
5. Sharpen the segment: one paragraph on who these people really are. If the evidence points at a narrower buyer than the brief assumed, say so.
6. Tag warm prospects. Anyone who asked price, offered to pay or pilot, gave a firm next step, or named their decision-maker gets STRONG. A polite "keep me posted" does not count. Write them to findings and to state (see Log it).
7. List what is still UNTESTED or UNCLEAR and the questions that would close it.

### Product-test mode differs
Testing a built thing, not an idea. For each element tested, tally the sessions where it worked, confused or failed, each cited by session file. End with a ranked "fix first" list, most-cited at top, count beside each item: that order is what `d4-prioritise` consumes. Software, hardware or service, the synthesis reads the same.

## The artefact
**Discovery**: `01-discovery/discovery-findings.md`, ordered per the synthesis guide (base and confidence, assumptions, jobs, pains, gains, segment, warm-prospects, gaps). Every claim carries a tally and a cited record.
**Product-test**: `04-gtm/product-test-findings.md`, per-element tallies with session cites and a ranked fix-first list.

## Done when
- Findings cite the available records by filename, and cite 8+ where 8+ exist.
- Every assumption carries one verdict with a counted tally.
- If fewer than 5 records exist, the findings say so at the top and mark patterns tentative.
- Discovery: the `warm_prospects` list is written to both findings and `.spark/state.json`.

## Log it
Replace `<N>` with the record count and `<PATH>` with the artefact.
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill synthesise-interviews \
  --artefact <PATH> \
  --result "<N> records synthesised"
```
Discovery mode also carries warm prospects into state:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"warm_prospects":[{"name":"Jane","role":"Head of Ops","firm":"FundCo","signal":"asked the price, offered a pilot","record":"interviews/03-jane.md"}]}'
```
Record each material verdict as a decision:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --decision "Killed the assumption that firms will pay to replace their spreadsheet" \
  --rationale "8 of 9 records said the spreadsheet works fine; nobody offered to pay"
```

## If it goes wrong
Scan reports 0 records: do not write findings, send the founder back to `run-interview`. Folder missing: create it and save records first.
Synthesis guide will not load: count the records, cite each claim by filename, mark every assumption with a verdict and tally, claim no more than the count supports. Warn the founder and flag it.
`01-discovery/idea-brief.md` missing: write jobs, pains, gains and segment anyway, and note at the top that assumptions were not marked.
