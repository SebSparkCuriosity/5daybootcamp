---
name: Blueprint The Build
description: Model the structure once, in diagrams, so the build is mechanical. Software gets a data model and system diagram, hardware a system diagram and bill of materials, services a service blueprint. Use on Day 3.
when_to_use: Day 3 product, straight after d3-prd, before you write code, render CAD or draft the sample deliverable. The drawing you do so you never guess mid-build.
argument-hint: [path to blueprint.md, optional]
---

# Blueprint The Build

**What this does.** Turns your build brief into diagrams of the thing you are about to build: what it stores, how it fits together, what it is made of.
**Why it matters.** An hour drawing the structure saves a day of building the wrong structure. When the shape is on paper, building is mechanical: you are typing out a decision you have already made, not making decisions while you type. It also gives a prospect, a lawyer or a regulator one picture that says exactly what the thing is.
**You are ready for this when.** `03-product/docs/PRD.md` exists.

## Before you start
Read these:

- `03-product/docs/PRD.md`: the numbered requirements and the non-goals. The blueprint models the Musts and nothing else.
- `.spark/state.json`: `business_type` decides which diagrams you draw. `idea` and `headline_target` keep the model pointed at the outcome.

The templates you copy from live in `${CLAUDE_SKILL_DIR}/references/blueprint-templates.md`, one ready block per path. Open it alongside this skill.

One rule: only model what the PRD says you are building this week. If a table, a component or a step does not trace back to a requirement, leave it off. A blueprint that shows next quarter's product is how a five-day build becomes a five-week build.

Diagrams are in Mermaid, in fenced ```` ```mermaid ```` blocks. Mermaid renders on GitHub, in Claude Code and in most Markdown previewers, so your one file is both the working model and something you can show a prospect. Where a picture genuinely cannot carry the detail (a bill of materials, for one), use a Markdown table instead.

## Steps
1. Create `03-product/docs/blueprint.md` with a one-line heading: what this models and which path it is for.
2. Copy the block for your path from the templates file, then work through the path section below.
3. Replace every placeholder with the real thing from your PRD. No box, table row or lane survives that you cannot tie to a requirement.
4. Write one sentence under each diagram in plain English, so someone who cannot read Mermaid still gets it.
5. Run the checker: `python3 ${CLAUDE_SKILL_DIR}/scripts/check-blueprint.py 03-product/docs/blueprint.md`. It reads `business_type` from state, confirms the right diagrams are present for your path, and does a light render-safety check on every Mermaid block. Fix what it flags.

## For software
Draw two diagrams. First the **data model** as a Mermaid `erDiagram`: the tables the Day 3 slice reads or writes, their key fields, and how they relate. One or two tables is normal for a first slice; more than four means you are modelling next week's product. Second the **system diagram** as a `flowchart`: how a request flows from the visitor's browser through the Next.js page on Vercel to the Supabase table and back. Every box must be a real thing that exists by Friday. No box labelled "AI engine" or "future integration".

## For hardware
Draw the **system diagram** as a `flowchart`: the physical blocks (sensor, controller, power, radio, enclosure) and how they connect, plus any companion app. Then write the **bill of materials** as a Markdown table: one row per real part, with a real supplier price, a quantity and a line cost, ending in a total. That total is the number your pricing rests on, so it has to be real. Any part you have not sourced yet is flagged as an assumption in the notes column. Never invent a unit cost.

## For services
Draw one **service blueprint** as a Mermaid `flowchart` with lanes (subgraphs): frontstage (what the client sees, from booking to signing), backstage (what you do out of sight to deliver it), and support (the tools, templates and evidence behind it). Every frontstage step needs at least one backstage action delivering it; a promise with nothing behind it is a promise you cannot keep. A backstage action with no frontstage step is work nobody asked for. If lanes feel forced, a `sequenceDiagram` between Client, You and System also passes and reads well for a handover.

## The artefact
Writes `03-product/docs/blueprint.md` in Markdown with embedded Mermaid. What good looks like: someone who has never heard your pitch reads the one file and understands what you are building, what it stores or is made of, and how the parts connect, without asking you anything. For hardware, the bill of materials ends in a real total cost. Every diagram element traces back to a PRD requirement.

## Done when
The checker passes (exit 0): the diagrams required for your `business_type` are all present, every Mermaid block names a valid diagram type and has balanced brackets, and for hardware the bill of materials table carries a total. Concretely: software has 2 diagrams (ERD plus system), hardware has 1 diagram plus a costed BOM table, services has 1 service blueprint.

## Log it
Append one line to CHANGELOG.md via the logbook helper, with the diagram count as the numeric result:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py \
  --skill d3-blueprint \
  --artefact 03-product/docs/blueprint.md \
  --result "<N> diagrams, blueprint complete"
```

The logbook helper also registers the artefact in `.spark/state.json`. Then set Day 3 progress via the journey-state helper:

```
python3 ${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py \
  --patch '{"days":{"3":{"target":"Build blueprinted, <N> diagrams"}}}'
```

If you left a requirement out of the model on purpose, or chose a sequence diagram over lanes, note it in DECISIONS.md with one line of rationale.

## If it goes wrong
If the checker keeps flagging unbalanced brackets, the culprit is almost always a node label with punctuation: wrap labels that contain a colon, brackets or a comma in double quotes, for example `P["Next.js page on Vercel"]`. If a diagram will not render in your previewer but the checker passes, paste the block into the Mermaid Live editor to find the exact line. And if the model is sprawling past the sizes above, you are blueprinting more than the PRD asked for: cut back to the Musts, and move the rest to a "later" note at the bottom of the file, not into the diagram.
