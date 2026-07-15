# spark-bootcamp: build conventions

This repository is a Claude Code marketplace holding one plugin, `spark-bootcamp`, in
`plugins/spark-bootcamp/`. The plugin takes a founder from a raw idea to a first paying
customer in five days. These are the conventions every skill obeys. Read this before
editing or adding a skill.

## Voice (Spark house style, non-negotiable)

- British English: organise, recognise, behaviour, favour, prioritise, analyse.
- Never use em dashes anywhere. Use commas, colons, full stops or brackets instead.
- Direct. Open with the conclusion, the number or the claim.
- Opinionated. Give one recommendation, not a balanced menu.
- Pragmatic. "Does it actually work?" beats "is it cutting-edge?".
- Warm, first-name, short sentences. No corporate-speak, no throat-clearing.
- Every recommendation carries a number. Prose over bullets unless a comparison needs structure.

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
  "headline_target": "the founder's numeric outcome for the week, set on Monday",
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

Then run `/spark-bootcamp:doctor` once, then `/spark-bootcamp:start`. The `coach` skill tells
them the one next command at every step.
