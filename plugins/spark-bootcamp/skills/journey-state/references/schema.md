# .spark/state.json field reference

The single source of truth for the journey state schema. Every skill reads and
writes these fields through the helper at
`${CLAUDE_PLUGIN_ROOT}/skills/journey-state/scripts/update-state.py`. Do not add
top-level keys casually: the whole plugin agrees on this shape.

## Top-level fields

| Field | Type | Meaning | Set by |
| --- | --- | --- | --- |
| `founder` | string | The founder's first name. | Day 0 / onboarding |
| `business_type` | string | Exactly `"software"`, `"hardware"` or `"services"`. Decides which path the build and ship skills follow. Set once. | Day 0 / onboarding |
| `idea` | string | One-line description of what they are building. | Day 1 |
| `headline_target` | string | The single numeric promise for the week, e.g. "one paying customer by Friday". | Day 0 / Day 1 |
| `current_day` | integer | Which day they are on, 1 to 5. | Every day skill |
| `days` | object | Five entries keyed `"1"` to `"5"`, each a day record (below). | Every day skill |
| `artefacts` | array | Append-only history of produced artefacts (record below). | Every skill that ships an artefact |

## Day record (`days["1"]` … `days["5"]`)

| Field | Type | Meaning |
| --- | --- | --- |
| `target` | string | The day's numeric goal, set at the start of the day. |
| `outcome` | string | What actually happened, filled in at the end of the day. |
| `complete` | boolean | `true` only when the day's done-condition is met. |

## Artefact record (each entry in `artefacts`)

| Field | Type | Meaning |
| --- | --- | --- |
| `skill` | string | The skill id that produced it, e.g. `"d1-define-interviewees"`. |
| `path` | string | Project-relative path to the artefact, e.g. `"01-discovery/interview-target-spec.md"`. |
| `result` | string | The numeric or observable result, e.g. `"10 interviews targeted"`. |
| `at` | string | ISO timestamp, added automatically by the helper if omitted. |

## Merge patch rules (RFC 7386)

The helper applies a JSON merge patch. The rules, in plain terms:

- An object merges key by key, recursively. Naming `days.1.complete` changes only that, leaving the other days and the other Day 1 fields untouched.
- A `null` value deletes that key. You will rarely want this here.
- Any scalar (string, number, boolean) or array replaces what was there.

Because arrays are replaced, never send `artefacts` inside `--patch`. To add an
artefact use `--append-artefact`, which appends one entry and preserves the rest
of the history. That is the only safe way to grow the list.

## Example: a mid-week state

```json
{
  "founder": "Seb",
  "business_type": "services",
  "idea": "Fixed-price AI workflow builds for Jersey trust firms",
  "headline_target": "one paying customer by Friday",
  "current_day": 3,
  "days": {
    "1": { "target": "10 interviews booked", "outcome": "11 booked", "complete": true },
    "2": { "target": "5 competitors mapped", "outcome": "6 mapped", "complete": true },
    "3": { "target": "1 sample deliverable built", "outcome": "", "complete": false },
    "4": { "target": "", "outcome": "", "complete": false },
    "5": { "target": "", "outcome": "", "complete": false }
  },
  "artefacts": [
    { "skill": "d1-define-interviewees", "path": "01-discovery/interview-target-spec.md", "result": "10 interviews targeted", "at": "2026-07-13T09:14:00" },
    { "skill": "d2-market-map", "path": "02-market/market-map.md", "result": "6 competitors mapped", "at": "2026-07-14T16:40:00" }
  ]
}
```
