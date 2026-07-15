# The capture store

Every lead your page collects lands in one place, the same way for all three
paths, so Day 4 (`d4-gtm-plan` and `d4-prioritise`) can read it without caring
whether you build software, hardware or services. The canonical shape is one
table, `captures`, and one local export file, `04-gtm/captures.jsonl`.

## The table

| column      | type        | notes                                              |
|-------------|-------------|----------------------------------------------------|
| id          | uuid        | default `gen_random_uuid()`, primary key           |
| created_at  | timestamptz | default `now()`                                    |
| kind        | text        | `signup`, `preorder`, `waitlist` or `booking`      |
| payload     | jsonb       | the whole form: name, email, and any variant field |

Keep names and emails in `payload`, not in named columns, so the same table
holds every path with no schema change. The privacy notice must already say you
collect this and where it lives.

## Default: Supabase

The default stack is Next.js, Supabase, Vercel, so use Supabase. Create the
table and an **insert-only** policy. The browser may write a lead but must never
read the list back, or anyone could scrape your prospects.

Run this once in the Supabase SQL editor (or via `apply_migration`):

```sql
create table if not exists public.captures (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  kind text not null,
  payload jsonb not null
);

alter table public.captures enable row level security;

-- Anyone (the anon key) may INSERT a lead. Nobody may SELECT from the browser.
create policy "anon can insert" on public.captures
  for insert to anon with check (true);
```

Then paste your project URL and the **anon / publishable** key (never the
service-role key) into the two placeholders near the top of `index.html`:

```js
window.SPARK_CAPTURE = {
  supabaseUrl: "https://YOUR-PROJECT.supabase.co",
  supabaseAnonKey: "YOUR-ANON-KEY",
  ...
};
```

The anon key is safe in the browser because the insert-only policy means it can
add a row and do nothing else. The service-role key is not safe and never goes
in a public page.

## Pull the leads down for Day 4

Day 4 reads `04-gtm/captures.jsonl`, one JSON object per line. Export from
Supabase whenever you want a fresh copy:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/pull_captures.py --root .
```

It reads leads with the service-role key from your environment
(`SUPABASE_URL` and `SUPABASE_SERVICE_KEY`) and writes them to
`04-gtm/captures.jsonl`. It degrades gracefully: no key, no network, or the
`requests` library missing, it tells you what to do by hand and never crashes.

## Fallback: Formspree (no backend)

No Supabase project yet, or the insert keeps failing? Use Formspree. Create a
free form, take the form id (the bit after `/f/`), and set it in `index.html`:

```js
window.SPARK_CAPTURE = { formspreeId: "abcdwxyz", kind: "waitlist", ... };
```

Leave `supabaseUrl` blank and the page falls through to Formspree
automatically. Each submission emails you. Paste the fields into
`04-gtm/captures.jsonl` by hand, one JSON object per line, so Day 4 still has a
list to work. Slower, but live in five minutes with no backend.

## What Day 4 expects to find

At minimum, one line per lead in `04-gtm/captures.jsonl`, each with `kind`,
`created_at`, and a `payload` holding at least an email. Your own test
submission counts as line one.
