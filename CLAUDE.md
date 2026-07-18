# spark-bootcamp: build conventions

This repository is a Claude Code marketplace holding one plugin, `spark-bootcamp`, in
`plugins/spark-bootcamp/`. The plugin takes a founder from a raw idea to a first paying
customer: a pre-work phase 2 to 4 weeks out (idea captured, 8 to 12 interviews booked
for the bootcamp Monday), then five days. These are the conventions every skill obeys.
Read this before editing or adding a skill.

## Voice (Spark house style, non-negotiable)

- British English: organise, recognise, behaviour, favour, prioritise, analyse.
- Never use em dashes anywhere. Use commas, colons, full stops or brackets instead.
- Direct. Open with the conclusion, the number or the claim.
- Opinionated. Give one recommendation, not a balanced menu.
- Pragmatic. "Does it actually work?" beats "is it cutting-edge?".
- Warm, first-name, short sentences. No corporate-speak, no throat-clearing.
- Every recommendation carries a number. Prose over bullets unless a comparison needs structure.

## How each skill talks to the founder (four patterns)

The founder's thinking is the product, so no skill silently decides for them. But a day
holds 6 to 10 skills, so no skill holds them hostage either. Each skill follows one of four
patterns, chosen per skill on what the judgement is worth, never per day:

- **Deep conversation (30 to 90 minutes).** The thinking IS the artefact: `start`,
  `p0-interview-triage`, `d1-refine-idea`, `d1-interview-plan`, `d1-write-script`. One
  question at a time, listen, reflect back, capture the founder's phrases verbatim, never
  write a section they have not spoken to. Arcs live in `references/`; the session may run long.
- **Working discussion (15 to 25 minutes).** The call belongs to the founder and Claude
  argues like a partner: `d1-validated-problem`, `d2-positioning`, `d2-proposition`,
  `d2-brand-foundations`, `d2-visual-identity`, `d3-moscow`, `d3-story-map`, `d4-gtm-plan`,
  `d5-pricing-model`, `d5-price-number`. Socratic questions first, then a recommendation with a number, then the
  founder decides and their words go in the artefact.
- **Draft, then explain back (10 to 15 minutes).** For technical artefacts a non-technical
  founder must genuinely own: `d3-prd`, `d3-blueprint`, `d3-tech-stack`. Claude drafts fast,
  then walks it through in plain English and asks the founder to poke holes with their domain
  knowledge ("does a client ever have two properties?"). Their corrections reshape the draft.
  Done when the founder could retell the document to a friend.
- **Ask, then draft (5 to 10 minutes).** Two to four sharp questions, then Claude does the
  work and shows it once: the research, assembly and ops skills. Mechanical skills
  (scaffolds, registers, checks, log compiles) stay silent.

Three rules hold everywhere. "Skip" and "you decide" are always acceptable answers, logged in
DECISIONS.md so no artefact hides a call the founder never saw. One round of corrections, not
endless iteration. And the exchange ends with an explicit yes before the artefact is final.
For the deep tier the token-efficiency rules below bend: SKILL.md stays terse, the arcs live
in `references/`, and the session is allowed to be long.

## The founder's project layout (what skills read and write)

Skills operate inside the founder's own project, not this repo. They create and use:

```
<founder-project>/
├── .spark/
│   ├── state.json            # the journey state machine (see schema below)
│   ├── brand/
│   │   ├── brand.json         # canonical brand tokens, written once on Day 2
│   │   └── logo.svg
│   └── deliverables/          # audit-pack, compliance notes, launch package
├── CHANGELOG.md               # append-only log, one line per artefact produced
├── DECISIONS.md               # decision log, why each call was made
├── 00-prework/                # pre-work artefacts: triage, invite list, invitations, schedule
├── 01-discovery/              # Day 1 artefacts
├── 02-market/                 # Day 2 artefacts
├── 03-product/                # Day 3 artefacts
├── 04-gtm/                    # Day 4 artefacts
└── 05-sale/                   # Day 5 artefacts
```

## state.json schema

```json
{
  "founder": "string",
  "business_type": "software | hardware | services",
  "idea": "one sentence",
  "headline_target": "the founder's numeric outcome for the week, set in pre-work",
  "prework": {
    "bootcamp_monday": "ISO date of the bootcamp's Monday, e.g. 2026-09-14",
    "interviews_booked": 0,
    "complete": false
  },
  "current_day": 1,
  "days": {
    "1": { "target": "string", "outcome": "string", "complete": false },
    "2": { "target": "", "outcome": "", "complete": false },
    "3": { "target": "", "outcome": "", "complete": false },
    "4": { "target": "", "outcome": "", "complete": false },
    "5": { "target": "", "outcome": "", "complete": false }
  },
  "artefacts": [{ "skill": "string", "path": "string", "result": "string", "at": "ISO date" }]
}
```

Read and write it only through the `journey-state` helper so concurrent skills never clobber it.

## Logging (auditable by default)

Every skill that produces an artefact appends one line to `CHANGELOG.md` via the `logbook`
helper: date, skill id, artefact path, the numeric result. Decisions with a rationale go in
`DECISIONS.md`. The week ends with `audit-pack` compiling both into a regulator or investor pack.

## The three business paths

One plugin, three paths, chosen in `start` and read from `state.business_type`. Skills that
build or ship must branch. The shared spine across all three is "a live page a real prospect
can act on":

- **software**: a deployed working slice on a public URL (default stack: Next.js + Supabase + Vercel).
- **hardware**: a demonstrable prototype (CAD render or physical mock) plus a pre-order or waitlist page taking real payment intent.
- **services**: a productised service package (one sample deliverable) plus a bookable intake page.

The `business-profile` skill holds the one variance matrix, one row per day per path, so a new
day skill needs one new row, not three copies.

## Efficiency conventions (the cohort has a usage limit)

Founders pay for tokens, so every skill earns its keep. The rules:

- **Body under ~45 lines.** Three-line header (what, one warm why, ready-when), then terse
  numbered steps. No hedging, no repetition, no restating the obvious.
- **One log call.** `log.py --skill --artefact --result` already registers the artefact in
  state. Only add an `update-state.py --patch` when the skill sets a day target, outcome or
  completion (checkpoint and day-closing skills). Never log the same thing twice.
- **Read compact, not whole.** Read `.spark/state.json` for context. Read a prior artefact only
  when the skill transforms its content, and only the part it needs. Let scripts extract inputs.
- **Scripts do the mechanical work.** Reading, scaffolding, validating and checking done-conditions
  belong in `scripts/`, which run in Bash and never enter the model context. Claude fills only the
  judgement gaps the script marks. Scripts print PASS or a short "missing: ..." list, nothing more.
- **No inline templates.** Long templates live in `references/` (loaded on demand) or inside the
  scaffold script, never pasted into SKILL.md.
- **Fresh-session friendly.** Never rely on chat history. Always read from disk, so a founder can
  start each day in a clean session and `coach` rebuilds from `state.json`.
- **Tight frontmatter.** `description` under 160 characters, `when_to_use` under 120. These sit in
  context on every turn, so they carry the trigger and nothing else.

## SKILL.md house structure

Every skill is `plugins/spark-bootcamp/skills/<skill-id>/SKILL.md` with this frontmatter and shape:

```markdown
---
name: Title Case Name
description: Trigger sentence in Spark voice. Lead with what it does and when to use it. Under ~200 chars.
when_to_use: Extra trigger phrases and where in the week this sits.
argument-hint: [optional]
---

# Title

**What this does.** One line.
**Why it matters.** One or two plain-English sentences: the purpose, before the how.
**You are ready for this when.** The prior artefact exists.

## Before you start
Inputs it reads (paths). Any guardrail: pause for human sign-off before sending or spending.

## Steps
Numbered, imperative, opinionated. Branch by business path where the work differs.

## The artefact
Writes `<path>` in `<format>`. What good looks like.

## Done when
Numeric or observable condition(s).

## Log it
Append to CHANGELOG.md and update .spark/state.json.

## If it goes wrong
The fallback, where one is needed.
```

- Keep SKILL.md under ~500 lines. Long templates and reference material go in `references/`,
  helper scripts in `scripts/`, reached via `${CLAUDE_SKILL_DIR}`.
- Hidden knowledge skills (used by Claude, not run by the founder) set `user-invocable: false`.
- Legal and data-protection outputs are drafts and must carry a "have a qualified lawyer review
  this before use" disclaimer. Spark does not warrant them.
- Never fabricate market numbers. Every figure is sourced or flagged as an assumption.
- Human-in-the-loop before any outreach is sent or any money is spent.

## Distribution

Founders install with:

```
/plugin marketplace add SebSparkCuriosity/5daybootcamp
/plugin install spark-bootcamp@spark
```

Then run `/spark-bootcamp:doctor` once, then `/spark-bootcamp:start`, ideally 2 to 4 weeks
before the bootcamp Monday so the interview invitations can go out in time. The `coach` skill
tells them the one next command at every step, starting with the pre-work chain.
