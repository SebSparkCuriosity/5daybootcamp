---
name: Synthesise Interviews
description: Reads a folder of interview records and pulls out the counted patterns: which assumptions the evidence validated or killed, the jobs, pains and gains, and who is worth a follow-up. Use once the interviews are done.
when_to_use: Day 1 discovery, after run-interview, to write discovery-findings.md. Also Day 4 product-test mode, to feed d4-prioritise. Takes a mode argument.
argument-hint: [discovery|product-test]
---

# Synthesise Interviews

**What this does.** Reads every interview record in a folder and turns them into findings backed by counts, not vibes: each riskiest assumption marked validated, killed or unclear against a tally of records, the jobs, pains and gains ranked by how often they came up, a sharpened segment, and the prospects who showed real buying signal tagged so their names carry into Day 4.
**Why it matters.** The interviews are worthless until you synthesise them, and most founders synthesise by memory, which means they remember the flattering bits and forget the ones that killed the idea. Counting fixes that. If seven of nine people described the same pain unprompted, that is a pattern you can build on. If one warm conversation is doing all the work, you need to know before you bet the week on it. Count the evidence, cite it by name, say no more than the records support.
**You are ready for this when.** `01-discovery/interviews/` holds at least one record (discovery mode), or `04-gtm/tests/sessions/` holds product-test sessions (product-test mode).

## Before you start
This skill runs in one of two modes. The argument sets it:

- **discovery** (Day 1, the default): reads `01-discovery/interviews/*.md`, writes `01-discovery/discovery-findings.md`.
- **product-test** (Day 4): reads `04-gtm/tests/sessions/*.md` (or `01-discovery/interviews/` if the founder saved tests there), writes `04-gtm/product-test-findings.md` to feed `d4-prioritise`.

If no mode is given, assume discovery.

Read two things before you write a word. First, `01-discovery/idea-brief.md`, for the riskiest assumptions you must mark against evidence. Second, the willingness-to-pay reference at `${CLAUDE_PLUGIN_ROOT}/skills/interview-method/references/wtp-signals.md`, so you score buying signal on what people gave up, not on how nice they were. The full method for both modes is in `${CLAUDE_SKILL_DIR}/references/synthesis-guide.md`. Read it now.

Guardrail: synthesis is a read-and-report job. Do not message any interviewee, do not promise anyone anything, do not spend money. Warm prospects get tagged for Day 4, not contacted today.

## Steps

1. **Count the records first, before you read for meaning.** The count decides how much you are allowed to claim. Run the scan:
   ```
   python3 ${CLAUDE_SKILL_DIR}/scripts/scan-interviews.py 01-discovery/interviews
   ```
   (In product-test mode, point it at `04-gtm/tests/sessions`.) It prints the number of records, a confidence band, and an index you cite by filename. 8 or more is strong. 5 to 7 is usable, flag the thinner base. 1 to 4 is weak, patterns are tentative. 0 means stop and go interview people.

2. **Read every record.** Do not skim. For each one, note the jobs the person is trying to get done, what actually hurts, what "done well" looks like to them, and whether they showed real buying signal. Anchor to behaviour and the past, per the interview method, not to opinions and the future.

3. **Mark each riskiest assumption against the count.** Pull the assumptions from the idea brief. For each, give one verdict: VALIDATED, KILLED, UNCLEAR or UNTESTED, and put the tally next to it, for example "6 of 9 records, cites (interviews/03-jane.md), (interviews/07-ravi.md)". One warm chat is not a verdict. A verdict needs the count. Log the important verdicts as decisions (see Log it).

4. **Rank jobs, pains and gains by frequency.** Most-cited first, each with its tally and its cited records. If a "pattern" rests on a single record, call it a hunch, not a pattern.

5. **Sharpen the segment.** One paragraph on who these people really are now the records have spoken. If the evidence points at a narrower or different buyer than the idea brief assumed, say so and recommend the change. This is the moment to be opinionated.

6. **Tag the warm prospects.** Anyone who asked the price, offered to pay or pilot, gave a firm next step, or named their decision-maker gets tagged STRONG buying signal. A polite "keep me posted" does not count. These names must reach Day 4, so record them both in the findings and in `.spark/state.json` as a `warm_prospects` list (see Log it), so `d4-gtm-plan` can read them without re-reading every transcript.

7. **Be honest about the gaps.** List what is still UNTESTED or UNCLEAR and the questions that would close it. Thin and honest beats confident and wrong.

### Product-test mode differs

Same discipline, different question. You are not testing an idea, you are testing a built thing (the deployed slice, the prototype, or the sample deliverable). For each element tested, tally the sessions where it worked, confused, or failed, each cited by session file. End with a ranked "fix first" list, most-cited problem at the top, count beside every item. That ranked order is exactly what `d4-prioritise` consumes, so make it explicit. The three paths converge here: whether the founder built software, hardware or a service, the synthesis reads the same way, sessions in, ranked fixes out.

## The artefact
**Discovery mode** writes `01-discovery/discovery-findings.md` in Markdown, in the order set out in the synthesis guide: base and confidence at the top, then assumptions marked against evidence, jobs, pains, gains, the sharpened segment, the warm-prospects list, and what you still do not know. Good looks like: every claim carries a tally and at least one cited record, and a reader can open any cited record and find the quote.

**Product-test mode** writes `04-gtm/product-test-findings.md` in Markdown: per-element tallies with session cites, and a ranked fix-first list feeding `d4-prioritise`.

## Done when
- The findings cite the available records: if the scan found N records, the findings reference them by filename, and cite 8 or more where 8 or more exist.
- Every riskiest assumption from the idea brief carries one verdict (VALIDATED, KILLED, UNCLEAR or UNTESTED) with a counted evidence tally beside it.
- If fewer than 5 records exist, the findings say so plainly at the top and mark patterns as tentative rather than over-reading them.
- Discovery mode: the `warm_prospects` list is written to both the findings and `.spark/state.json`.

## Log it
Append one line to CHANGELOG.md, register the artefact, and carry the warm prospects into state (discovery mode). Replace `<N>` with the record count the scan printed and `<PATH>` with the artefact you wrote.
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill synthesise-interviews \
  --artefact <PATH> \
  --result "<N> records synthesised"

python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --append-artefact '{"skill":"synthesise-interviews","path":"<PATH>","result":"<N> records synthesised"}'
```
Discovery mode also carries the warm prospects forward, so Day 4 can read them:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"warm_prospects":[{"name":"Jane","role":"Head of Ops","firm":"FundCo","signal":"asked the price, offered a pilot","record":"interviews/03-jane.md"}]}'
```
Record each material verdict as a decision with its rationale:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --decision "Killed the assumption that firms will pay to replace their spreadsheet" \
  --rationale "8 of 9 records said the spreadsheet works fine; nobody offered to pay"
```

## If it goes wrong
If the scan reports 0 records, do not write findings. Tell the founder plainly that there is nothing to synthesise yet and send them back to `run-interview`. If the folder is missing entirely, the scan says so and exits cleanly; create it and save the records first.

If the synthesis guide reference will not load, fall back to the discipline in one line: count the records, cite each claim by filename, mark every assumption with a verdict and a tally, and never claim more than the count supports. Warn the founder that the detailed guide could not be read, carry on, and flag it so the file can be restored.

If `01-discovery/idea-brief.md` is missing, you cannot mark assumptions against it. Write the jobs, pains, gains and segment from the records anyway, and note at the top that assumptions were not marked because the idea brief was absent.
