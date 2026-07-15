#!/usr/bin/env python3
"""Pull leads from the Supabase captures table into 04-gtm/captures.jsonl.

Day 4 (d4-gtm-plan, d4-prioritise) reads 04-gtm/captures.jsonl, one JSON object
per line. This script fetches the rows and writes that file. It reads the
service-role key from the environment, never from the page, because reading the
list needs more than the browser's insert-only anon key.

It never crashes. No key, no network, or the 'requests' library missing: it
prints exactly what to do by hand and exits without touching the file.

Environment:
  SUPABASE_URL          e.g. https://YOUR-PROJECT.supabase.co
  SUPABASE_SERVICE_KEY  the service-role key (keep it out of the page and git)

Usage:
  pull_captures.py --root .
"""

import argparse
import json
import os
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Founder project root")
    ap.add_argument("--out", default="04-gtm/captures.jsonl")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    out_path = os.path.join(root, args.out)

    url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    key = os.environ.get("SUPABASE_SERVICE_KEY", "")

    if not url or not key:
        print("No SUPABASE_URL / SUPABASE_SERVICE_KEY in the environment.")
        print("Either export both and re-run, or export your leads by hand:")
        print("  In Supabase, open the captures table, Export to CSV/JSON,")
        print("  then paste one JSON object per line into %s" % out_path)
        return

    try:
        import requests  # optional
    except Exception:
        print("The 'requests' library is not installed. Install it (pip install requests),")
        print("or copy the rows from the Supabase table editor into %s by hand," % out_path)
        print("one JSON object per line.")
        return

    endpoint = url + "/rest/v1/captures?select=*&order=created_at.asc"
    headers = {"apikey": key, "Authorization": "Bearer " + key}
    try:
        r = requests.get(endpoint, headers=headers, timeout=20)
    except Exception as e:
        print("Could not reach Supabase (%s)." % e)
        print("Check the URL and your network, or export by hand into %s." % out_path)
        return

    if r.status_code != 200:
        print("Supabase returned HTTP %d: %s" % (r.status_code, r.text[:200]))
        print("Check the service-role key, or export by hand into %s." % out_path)
        return

    try:
        rows = r.json()
    except Exception:
        print("Response was not JSON. Export by hand into %s." % out_path)
        return

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print("Wrote %d capture(s) to %s" % (len(rows), out_path))
    if not rows:
        print("No leads yet. Your own test submission should be line one once you have made it.")


if __name__ == "__main__":
    main()
