#!/usr/bin/env python3
"""Rank the founder's first prospects by warmth.

Merges three sources from the founder's project, de-duplicates by name and
email, scores each person 0 to 100 (see references/warmth-model.md), and writes
a ranked draft to 04-gtm/prospect-ranking.csv.

Degrades gracefully: any missing source is reported and skipped, never fatal.
Uses only the Python standard library.

Run from the founder's project root, or pass --root.
"""

import argparse
import csv
import os
import re
import sys

# ----- warmth model (mirrors references/warmth-model.md) -----

INTENT_POINTS = [
    (("deposit", "pre-order", "preorder", "paid", "payment"), 60),
    (("booked call", "booked", "intake", "call booked", "meeting"), 45),
    (("buying question", "how much", "when can i", "can i buy", "price"), 35),
    (("hit limit", "used slice", "hit a limit", "usage"), 30),
    (("replied to sample", "sample reply", "replied deliverable"), 30),
    (("waitlist", "mailing list", "signup", "sign up", "subscribed"), 15),
    (("opened", "clicked", "open", "click"), 5),
]

SEGMENT_POINTS = {"exact": 25, "sector": 12, "adjacent": 5, "off": 0}


def score_intent(text):
    t = (text or "").lower()
    best = 0
    label = "none"
    for keywords, pts in INTENT_POINTS:
        if any(k in t for k in keywords):
            if pts > best:
                best = pts
                label = keywords[0]
    return best, label


def score_segment(value):
    v = (value or "").strip().lower()
    if v in SEGMENT_POINTS:
        return SEGMENT_POINTS[v]
    # loose parsing of free text
    if "exact" in v or "perfect" in v:
        return 25
    if "sector" in v:
        return 12
    if "adjacent" in v or "maybe" in v:
        return 5
    return 0 if v in ("", "off", "off-target", "no") else 5


def score_depth(touches):
    try:
        n = int(touches)
    except (TypeError, ValueError):
        n = 1
    if n >= 3:
        return 15
    if n == 2:
        return 10
    return 5


# ----- source readers -----

def _read_csv(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except Exception as e:  # noqa: BLE001
        print(f"  ! could not read {path}: {e}")
        return None


def _get(row, *names):
    """Case-insensitive column lookup with fallbacks."""
    lower = {k.lower().strip(): v for k, v in row.items() if k}
    for n in names:
        if n.lower() in lower and lower[n.lower()]:
            return lower[n.lower()].strip()
    return ""


def load_scorecard(root):
    path = os.path.join(root, "03-product", "buying-signal-scorecard.csv")
    rows = _read_csv(path)
    people = []
    if rows is None:
        print("  - scorecard missing (03-product/buying-signal-scorecard.csv), skipping")
        return people
    for r in rows:
        name = _get(r, "name", "prospect", "person")
        if not name:
            continue
        people.append({
            "name": name,
            "email": _get(r, "email"),
            "source": "scorecard",
            "signal_text": _get(r, "signal", "buying_signal", "note", "notes"),
            "segment": _get(r, "segment", "segment_match", "match"),
            "touches": _get(r, "touches", "interactions") or "1",
        })
    print(f"  + scorecard: {len(people)} rows")
    return people


def load_captures(root):
    path = os.path.join(root, "04-gtm", "landing-captures.csv")
    rows = _read_csv(path)
    people = []
    if rows is None:
        print("  - landing captures missing (04-gtm/landing-captures.csv), skipping")
        return people
    for r in rows:
        name = _get(r, "name", "full_name") or _get(r, "email")
        if not name:
            continue
        action = _get(r, "action", "signal", "type") or "waitlist signup"
        people.append({
            "name": name,
            "email": _get(r, "email"),
            "source": "landing",
            "signal_text": action,
            "segment": _get(r, "segment", "segment_match"),
            "touches": _get(r, "touches") or "1",
        })
    print(f"  + landing captures: {len(people)} rows")
    return people


def load_interviews(root):
    """Pull interviewees tagged with a strong buying signal.

    Reads a CSV if present, otherwise scans interview-notes.md for lines tagged
    'strong' or 'buying signal'.
    """
    people = []
    csv_path = os.path.join(root, "01-discovery", "interviews.csv")
    rows = _read_csv(csv_path)
    if rows is not None:
        for r in rows:
            tag = _get(r, "buying_signal", "signal", "tag").lower()
            if "strong" not in tag and "high" not in tag:
                continue
            name = _get(r, "name", "interviewee")
            if not name:
                continue
            people.append({
                "name": name,
                "email": _get(r, "email"),
                "source": "interview",
                "signal_text": _get(r, "signal", "note") or "buying question",
                "segment": _get(r, "segment") or "exact",
                "touches": _get(r, "touches") or "1",
            })
        print(f"  + interviews.csv: {len(people)} strong-signal rows")
        return people

    md_path = os.path.join(root, "01-discovery", "interview-notes.md")
    if not os.path.exists(md_path):
        print("  - interviews missing (01-discovery/interviews.csv or interview-notes.md), skipping")
        return people
    try:
        with open(md_path, encoding="utf-8") as f:
            for line in f:
                low = line.lower()
                if "strong" in low and ("signal" in low or "buying" in low):
                    # grab a name: first bolded or capitalised token group
                    m = re.search(r"\*\*(.+?)\*\*", line) or re.search(r"([A-Z][a-z]+(?: [A-Z][a-z]+)?)", line)
                    if m:
                        people.append({
                            "name": m.group(1).strip(),
                            "email": "",
                            "source": "interview",
                            "signal_text": "strong buying signal (interview)",
                            "segment": "exact",
                            "touches": "1",
                        })
        print(f"  + interview-notes.md: {len(people)} strong-signal lines")
    except Exception as e:  # noqa: BLE001
        print(f"  ! could not read {md_path}: {e}")
    return people


# ----- merge, score, rank -----

def dedupe_key(p):
    email = (p.get("email") or "").strip().lower()
    if email:
        return email
    return re.sub(r"\s+", " ", (p.get("name") or "").strip().lower())


def merge(people_lists):
    merged = {}
    for people in people_lists:
        for p in people:
            key = dedupe_key(p)
            if not key:
                continue
            if key in merged:
                existing = merged[key]
                # keep richest signal, bump touch count, remember every source
                existing["_sources"].add(p["source"])
                try:
                    existing["touches"] = str(int(existing["touches"]) + int(p["touches"]))
                except ValueError:
                    pass
                # keep the strongest-intent signal, not merely the longest text
                if score_intent(p.get("signal_text"))[0] > score_intent(existing.get("signal_text"))[0]:
                    existing["signal_text"] = p["signal_text"]
                if not existing.get("email") and p.get("email"):
                    existing["email"] = p["email"]
                if not existing.get("segment") and p.get("segment"):
                    existing["segment"] = p["segment"]
            else:
                p = dict(p)
                p["_sources"] = {p["source"]}
                merged[key] = p
    return list(merged.values())


def score(p):
    intent, intent_label = score_intent(p.get("signal_text"))
    seg = score_segment(p.get("segment"))
    depth = score_depth(p.get("touches"))
    total = min(100, intent + seg + depth)
    return total, intent_label, intent, seg, depth


def main():
    ap = argparse.ArgumentParser(description="Rank first prospects by warmth.")
    ap.add_argument("--root", default=os.getcwd(), help="Founder project root (default: cwd)")
    ap.add_argument("--top", type=int, default=10, help="How many to keep (default: 10)")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    print(f"Reading sources under {root}")
    people = merge([
        load_scorecard(root),
        load_captures(root),
        load_interviews(root),
    ])

    if not people:
        print("\nNo prospects found in any source. Widen the funnel and re-run.")
        print("See 'If it goes wrong' in SKILL.md.")
        return 0

    ranked = []
    for p in people:
        total, label, intent, seg, depth = score(p)
        ranked.append({
            "name": p["name"],
            "email": p.get("email", ""),
            "source": "+".join(sorted(p["_sources"])),
            "segment_match": p.get("segment", ""),
            "warmth": total,
            "intent_signal": label,
            "breakdown": f"intent {intent} / segment {seg} / depth {depth}",
            "next_action": "",  # founder fills this per path
        })
    ranked.sort(key=lambda r: r["warmth"], reverse=True)
    ranked = ranked[: args.top]

    out_dir = os.path.join(root, "04-gtm")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "prospect-ranking.csv")
    fields = ["rank", "name", "email", "source", "segment_match", "warmth",
              "intent_signal", "breakdown", "next_action"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, r in enumerate(ranked, 1):
            r["rank"] = i
            w.writerow(r)

    print(f"\nWrote {len(ranked)} ranked prospects to {out_path}")
    print("\nTop of the queue:")
    for r in ranked[:5]:
        print(f"  {r['rank']:>2}. {r['name']:<24} warmth {r['warmth']:>3}  ({r['intent_signal']})")
    if len(ranked) < args.top:
        print(f"\n! Only {len(ranked)} real prospects found, not {args.top}. "
              "Your top of funnel is narrow. Widen it before Day 5 (see SKILL.md).")
    print("\nNow write the next action for each in 04-gtm/gtm-plan.md, "
          "branching by business path, and name #1 with a reason.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
