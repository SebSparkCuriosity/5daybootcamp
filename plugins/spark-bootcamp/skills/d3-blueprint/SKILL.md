---
name: Blueprint The Build
description: Diagram the structure once so the build is mechanical. Software gets a data model and system diagram, hardware a diagram and BOM, services a blueprint. Day 3.
when_to_use: Day 3, straight after d3-prd, before you write code, render CAD or draft the sample deliverable.
argument-hint: [path to blueprint.md, optional]
---

# Blueprint The Build

**What this does.** Turns your build brief into diagrams: what it stores, how it fits together, what it is made of.
**Why it matters.** An hour drawing the structure saves a day building the wrong one, and gives a prospect, lawyer or regulator one picture that says exactly what the thing is.
**You are ready for this when.** `03-product/docs/PRD.md` exists.

## Before you start
Read `03-product/docs/PRD.md` (the Musts, and non-goals) and `.spark/state.json` (`business_type` picks your diagrams). Templates: `${CLAUDE_SKILL_DIR}/references/blueprint-templates.md`, one block per path.

Only model what the PRD says you build this week. Draft, then explain back (about 15 minutes): the founder cannot draw this, but only they know the world it models. After drafting, walk each diagram through in plain English and ask domain questions ("does a client ever have two properties?", "who updates this when it changes?"). Their answers reshape the model before the checker runs. Diagrams are Mermaid in fenced ```` ```mermaid ```` blocks; use a Markdown table where a picture cannot carry it (a BOM).

## Steps
1. Create `03-product/docs/blueprint.md` with a one-line heading: what it models and which path.
2. Copy your path's block from the templates file, then follow the path section below.
3. Replace every placeholder with the real thing from your PRD. Nothing survives that you cannot tie to a requirement.
4. Write one plain-English sentence under each diagram.
5. Run the checker: `python3 ${CLAUDE_SKILL_DIR}/scripts/check-blueprint.py 03-product/docs/blueprint.md`. Fix what it flags.

## For software
Two diagrams. A **data model** as a Mermaid `erDiagram`: the tables the Day 3 slice reads or writes, key fields, relations (one or two tables is normal; over four is next week's product). A **system diagram** as a `flowchart`: request flow from browser through the Next.js page on Vercel to the Supabase table and back. Every box is real by Friday, no "AI engine" placeholders.

## For hardware
A **system diagram** as a `flowchart`: physical blocks (sensor, controller, power, radio, enclosure), how they connect, plus any companion app. Then a **bill of materials** as a Markdown table: one row per real part with real supplier price, quantity, line cost, ending in a total. That total is what pricing rests on, so it must be real. Flag unsourced parts as assumptions. Never invent a unit cost.

## For services
One **service blueprint** as a Mermaid `flowchart` with lanes (subgraphs): frontstage (what the client sees, booking to signing), backstage (what you do to deliver), support (tools, templates, evidence). Every frontstage step needs a backstage action; no orphan lanes either way. If lanes feel forced, a `sequenceDiagram` between Client, You and System also passes.

## The artefact
`03-product/docs/blueprint.md` in Markdown with embedded Mermaid. Good: someone who never heard your pitch reads it and understands what you build, what it stores or is made of, how the parts connect. Hardware ends in a real total. Every element traces to a PRD requirement.

## Done when
Checker passes (exit 0): software has 2 diagrams (ERD plus system), hardware has 1 diagram plus a costed BOM table with a total, services has 1 service blueprint. Every Mermaid block names a valid type with balanced brackets.

## Log it
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d3-blueprint \
  --artefact 03-product/docs/blueprint.md \
  --result "<N> diagrams, blueprint complete"
```
Then set Day 3 progress:
```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"3":{"target":"Build blueprinted, <N> diagrams"}}}'
```
If you left a requirement out on purpose, or chose a sequence diagram over lanes, note it in DECISIONS.md.

## If it goes wrong
Unbalanced brackets are almost always a label with punctuation: wrap labels with a colon, brackets or comma in double quotes, e.g. `P["Next.js page on Vercel"]`. If it will not render but the checker passes, paste the block into Mermaid Live to find the line. If the model sprawls past the sizes above, cut to the Musts and move the rest to a "later" note at the bottom.
