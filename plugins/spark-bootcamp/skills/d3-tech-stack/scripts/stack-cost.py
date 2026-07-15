#!/usr/bin/env python3
"""Monthly cost for the chosen Spark stack, one path at a time.

Usage: python3 stack-cost.py <software|hardware|services>

Prints the free-tier total (what you pay to reach a first paying customer)
and a realistic paid total once you have real traffic or orders. Figures are
list prices as of July 2026, converted to GBP at rough parity where a tool
prices in USD. They are estimates, not quotes. Confirm on each provider's
pricing page before you rely on them.

No external libraries. If run with no argument it prints all three paths.
"""

import sys

# Each line: (component, free_tier_gbp_per_month, paid_gbp_per_month, note)
STACKS = {
    "software": [
        ("GitHub", 0, 0, "free tier fine to first customer"),
        ("Vercel", 0, 16, "free hobby tier, Pro when you need real traffic"),
        ("Supabase", 0, 19, "free tier, Pro at 8GB and daily backups"),
        ("Domain", 0, 10, "about £10/yr, so ~£1/mo, rounded for a card-on-file buffer"),
    ],
    "hardware": [
        ("Onshape", 0, 0, "free plan for public documents"),
        ("Carrd", 0, 1, "free for one site, ~£15/yr for a custom domain"),
        ("Stripe", 0, 0, "no monthly fee, 1.5% + 20p per transaction only"),
    ],
    "services": [
        ("Google Docs", 0, 0, "free with any Google account"),
        ("Carrd", 0, 1, "free for one site, ~£15/yr for a custom domain"),
        ("Cal.com", 0, 0, "free tier covers one-to-one bookings"),
    ],
}


def print_path(path):
    rows = STACKS[path]
    free = sum(r[1] for r in rows)
    paid = sum(r[2] for r in rows)
    print(f"\n=== {path.upper()} stack ===")
    for name, f, p, note in rows:
        print(f"  {name:<12} free £{f:<3}  paid £{p:<3}  {note}")
    print(f"  {'-' * 44}")
    print(f"  Free tier total (to first paying customer): £{free}/mo")
    print(f"  Realistic paid total (with real usage):     £{paid}/mo")
    if path == "hardware":
        print("  Plus Stripe fees: 1.5% + 20p per transaction, charged only on real payments.")
    print("  Figures are estimates as of July 2026. Confirm on each provider's pricing page.")


def main():
    if len(sys.argv) < 2:
        print("No path given. Showing all three. Usage: stack-cost.py <software|hardware|services>")
        for path in STACKS:
            print_path(path)
        return
    path = sys.argv[1].strip().lower()
    if path not in STACKS:
        print(f"Unknown path '{path}'. Choose one of: software, hardware, services.")
        sys.exit(1)
    print_path(path)


if __name__ == "__main__":
    main()
