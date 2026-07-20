---
name: Develop Your Idea
description: The deepest conversation of the week. Draws out your story, your philosophy and your idea, then shapes them into one testable problem and the assumption that could kill it.
when_to_use: Day 1 morning, first thing, before the interview plan and script. Give it 90 minutes; the afternoon interviews test what it produces.
---

# Develop Your Idea

**What this does.** Develops your idea with you, out loud: where it came from, what you believe, whose problem it is, and the bet underneath it. Ends with an idea brief written in your words, not Claude's.
**Why it matters.** This afternoon's interviews test a bet, and the bet has to be genuinely yours. A brief you merely nodded at will not survive contact with a real customer; one you talked into existence will.
**You are ready for this when.** `.spark/state.json` has `idea` filled and `00-prework/interview-schedule.md` holds your booked calls.

## Before you start
Read state (`founder`, `business_type`, `idea`) and skim `00-prework/interview-target-spec.md` for who is booked. Then put the files down. This is a conversation, and the conversation is the work: one question at a time, listen, follow up on what they actually said, and never write a section the founder has not spoken to. The full arc lives in `references/conversation-guide.md`; read it before you ask anything.

## Steps
1. Run the five arcs from the conversation guide, in order: the origin story, their philosophy and approach, the person they picture, the evidence they have seen, and the bet underneath. Reflect back after each arc and keep their phrases verbatim.
2. Draft the problem hypothesis together, in their words: "I believe [specific person] struggles to [specific job] because [specific reason], and today they [current workaround]." If they cannot name the person, that is the morning's first finding, not a blank to fill.
3. Surface the assumptions from what they said, not from a checklist: "you said X, that assumes Y, agree?" Get at least five, push to eight, covering felt-often, reachable, would-pay and can-deliver.
4. Rank them together. The founder scores each 1 to 5 for damage if wrong and for uncertainty; you challenge scores that look kind; multiply; highest is riskiest. Ties break to what this afternoon's calls can test.
5. Agree the riskiest assumption and its kill condition in the founder's words: "I abandon or pivot if I hear ___ this afternoon." No kill condition, no brief.
6. Confirm `business_type` still fits how they would deliver a first fix. If it changed, note why in DECISIONS.md.
7. Read the whole brief back, ask "what have I got wrong?", edit until the founder says it is theirs. Then write it.

## The artefact
Writes `01-discovery/idea-brief.md` in Markdown, five sections in order:
1. **Where this idea comes from.** The founder's story and philosophy in two or three of their own sentences. Day 2 brand work and Friday's pitch feed off this.
2. **Problem hypothesis.** The sentence from step 2, plus the precise person and current workaround.
3. **Assumptions, ranked.** Table: assumption, damage (1-5), uncertainty (1-5), score, sorted highest first. At least five rows.
4. **Riskiest assumption.** The top row restated with its kill condition.
5. **Path.** The `business_type` and one line on why it fits.

Good looks like this: every line traceable to something the founder actually said.

## Done when
- One problem hypothesis sentence naming a specific person, in the founder's words.
- At least five assumptions ranked by damage times uncertainty.
- The riskiest assumption flagged with a written kill condition.
- The founder has explicitly said the brief is theirs.

## Log it
```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --skill d1-refine-idea \
  --artefact 01-discovery/idea-brief.md \
  --result "1 hypothesis, N assumptions ranked, riskiest flagged"
```
If you set or changed `business_type`, patch state and log the decision with its rationale.

## If it goes wrong
Answers stay general ("businesses waste time"): ask for the last specific time they saw it happen, and build from that story. The conversation sprawls past 90 minutes: park the weakest arc, write the brief from what is real, and note the gap. The sharpened idea no longer fits who you booked: do not cancel anyone; flag the mismatch for `d1-interview-plan` and treat the calls as paid-for learning about the adjacent segment.
