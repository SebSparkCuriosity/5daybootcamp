---
name: Guardrails
description: The four rules every skill checks before it sends, spends, publishes or states a number. Internal gate, no artefact.
when_to_use: Internal only. Apply automatically inside any skill about to send, spend, publish, or assert a market or financial figure.
user-invocable: false
---

# Guardrails

**What this does.** Sets the four hard rules every other skill obeys before doing something irreversible: send, spend, publish, or state a number.
**Why it matters.** These founders work in regulated sectors, where one careless send or one made-up number is a real problem, so this skill is the brake that keeps the week auditable.
**You are ready for this when.** Always. Any skill applies these the moment it approaches a gated action.

## Before you start
Not run by the founder. It is a checklist Claude applies from inside another skill. When a skill would send, spend, publish, or write a market or financial figure, run the matching gate first. If unsure whether an action is gated, treat it as gated.

## The four gates

**Gate 1: Sending.** Never send outreach (email, DM, message, follow-up) without explicit sign-off. Show the exact final text and recipient list, state count and channel in one line, then wait for unambiguous approval ("yes", "send it"). Silence or a thumbs-up elsewhere does not count. Sign-off is per batch, never standing.

**Gate 2: Spending.** Never create a charge (domain, paid tier, paid API, ads) without explicit sign-off. Name the exact amount, currency and whether it recurs; if you cannot name it, find the real price first. Say whether a free path exists and recommend it. Approval of one amount is not approval of another. Default: the five days cost near GBP 0.

**Gate 3: Publishing.** Never make something public (landing page, waitlist, public repo, pre-order page) without explicit sign-off. Show the final content and URL. Confirm a privacy note where the page takes an email and the draft-review disclaimer on any legal text. A private preview is not publishing; flipping it public is.

**Gate 4: Asserting a number.** Every figure about the outside world (market size, competitor pricing, segment counts, willingness to pay) carries either a checkable source or the word "assumption" plus reasoning, right next to it. Never present an unsourced figure as fact. The founder's own targets (1 customer, GBP 2,000 price) are decisions, not claims, and go in DECISIONS.md.

## Data handling: local first
Interview notes, contacts and customer details stay in local project files. Do not push to a cloud service unless the specific skill offers an export and the founder opts in, per skill and per step. Any export is a send or publish, so its gate applies.

## Regulated-sector caution
Never put a named client, real account or confidential figure into a public page, deck or outreach: use anonymised examples. Treat every legal, compliance or data-protection output as a draft and attach the disclaimer verbatim: "This is a draft. Have a qualified lawyer review it before you rely on it. Spark does not warrant it." When in doubt about a regulatory line, say so and let the founder decide. Exact gate wording is in `${CLAUDE_SKILL_DIR}/references/gate-checklist.md`.

## The artefact
None. This skill writes no output. It makes other skills pause at a gate and wait for the founder.

## Done when
Zero outreach sent, zero money spent and zero public pages live without a matching recorded approval, and zero unsourced, unflagged figures in any artefact.

## Log it
No artefact, so no changelog line. When a gate causes a real decision (paid a domain, opted in to a cloud export, approved a launch), the calling skill records it in DECISIONS.md:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/logbook/scripts/log.py" \
  --decision "Approved GBP 12 domain purchase for the launch page" \
  --rationale "Founder wanted a branded URL for outreach; free subdomain judged too weak for regulated buyers"
```

## If it goes wrong
If you already sent, spent or published without a gate, do not hide it: tell the founder what went out, to whom and for how much, and record it in DECISIONS.md. If you cannot source a number you already wrote, flag it as an assumption now. When unsure, pause and ask.
