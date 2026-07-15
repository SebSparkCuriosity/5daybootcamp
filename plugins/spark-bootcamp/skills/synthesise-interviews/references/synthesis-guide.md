# Synthesis guide

How to turn a folder of interview records into findings that hold up. Read this
before you write anything. The rule underneath all of it: count the evidence,
cite it by name, and never say more than the records support.

## The one discipline: evidence before conclusion

A pattern is not a pattern because it felt strong in the room. It is a pattern
because you can count the records that show it. So every claim in the findings
carries a tally: "5 of 9 records", "2 of 9, both in trust admin". If you cannot
put a number next to a claim, it is a hunch, and you label it a hunch.

Cite records by their file, for example `(interviews/03-jane-fundco.md)`. A
reader must be able to open the record and see the quote for themselves. That is
what makes the findings auditable rather than a story you told yourself.

## Marking a riskiest assumption

Your `01-discovery/idea-brief.md` flagged one or more riskiest assumptions. Each
one gets marked against the counted evidence, using exactly one of four verdicts:

- **VALIDATED**: the records back it. State the tally: "7 of 9 described this
  exact pain unprompted."
- **KILLED**: the records contradict it. State the tally: "8 of 9 said they
  already solve this with a spreadsheet and are happy."
- **UNCLEAR**: the records split or dodge it. State the split: "4 for, 3
  against, 2 never raised it." Unclear is an honest answer. Do not round it up.
- **UNTESTED**: no record touched it. Say so. This tells you what to ask next.

Never mark an assumption on the strength of one warm conversation. One record is
an anecdote. A verdict needs the count behind it.

## Reading buying signal (the tag that matters)

The willingness-to-pay reference (`interview-method/references/wtp-signals.md`)
is the authority here. In short: signal is what someone gave up, not what they
said. Money, a firm calendar slot, an intro to their boss, an offer to pilot.
Compliments are noise.

Tag a record STRONG buying signal only if the person did at least one of these:

1. Asked what it costs or when they can have it.
2. Offered to pay, pre-pay, or pilot.
3. Gave a real next step: a meeting, an intro, their decision-maker's name.
4. Described the pain as urgent and expensive, with a number attached.

A polite "sounds great, keep me posted" is not signal. It is noise. Do not tag it.

The founder needs these names on Day 4. The warmest prospects from discovery are
the first people the go-to-market plan should approach, so their names and roles
must survive into `d4-gtm-plan`. Record them twice: in the findings under a clear
"Warm prospects" heading, and in `.spark/state.json` as a `warm_prospects` list,
so Day 4 can read them without re-reading every transcript.

## The discovery-findings.md shape

Write `01-discovery/discovery-findings.md` in this order.

```
# Discovery findings

**Base:** <N> interview records read, in 01-discovery/interviews/.
**Confidence:** <strong | usable | weak> (see the count).
**Date:** <YYYY-MM-DD>

## Riskiest assumptions, marked against evidence
For each assumption from the idea brief:
- <assumption>. **VALIDATED / KILLED / UNCLEAR / UNTESTED**
  Evidence: <tally>. <one line>. Cites: (interviews/xx.md), (interviews/yy.md)

## Jobs to be done
The jobs customers are hiring this for, most-cited first.
- <job>: <N of N> records. Cites: ...

## Pains
What actually hurts, most-cited first, each with a tally and cites.

## Gains
What "done well" looks like to them, each with a tally and cites.

## The segment, sharpened
One paragraph. Who these people really are, now the records have spoken. If the
records point at a narrower or different segment than the idea brief assumed,
say so plainly and recommend the change.

## Warm prospects (carry to Day 4)
Everyone tagged STRONG buying signal: name, role, firm, the signal they gave,
and the record. These are the first calls in d4-gtm-plan.

## What we still do not know
The UNTESTED and UNCLEAR assumptions, and the questions to close them.
```

Good findings are short, counted, and cited. If a section has no evidence,
write "No record touched this" rather than padding it.

## Product-test mode

Same discipline, different input and output. You are reading product-test
sessions (a prospect using the built slice, prototype, or sample deliverable),
not discovery interviews. Read them from `04-gtm/tests/sessions/` if that
folder exists, otherwise from `01-discovery/interviews/` if the founder saved
tests there, and say which you read.

Write `04-gtm/product-test-findings.md`: for each thing tested, the tally of
sessions where it worked, where it confused, and where it failed, each cited by
session file. End with a ranked "fix first" list, most-cited problem at the top.
That ranked list is what `d4-prioritise` consumes, so make the order explicit and
put the count next to every item.

## When there are too few records

Under 5 records, you cannot claim a pattern. Say the base is small at the top of
the findings, mark assumptions as UNCLEAR or UNTESTED unless a record is truly
decisive, and recommend the founder run more interviews before betting the week
on the result. Honest and thin beats confident and wrong.
