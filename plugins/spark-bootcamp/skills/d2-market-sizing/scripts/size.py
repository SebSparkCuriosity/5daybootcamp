#!/usr/bin/env python3
"""Size a market two ways and triangulate.

This does the arithmetic so you cannot fudge it. You give it your assumptions,
each with a source. It computes TAM, SAM and SOM top-down and bottom-up, prints
both sets side by side, and reports the gap between the two so you can see
whether your story holds together.

Two hard rules baked in:
  1. Every number is your assumption, not the script's. It invents nothing.
  2. Every assumption must carry a source string. Leave a source blank and the
     script flags it loudly as UNSOURCED so it cannot hide in a clean table.

Definitions used here (keep them straight):
  TAM  Total Addressable Market: everyone with the problem, if you owned 100%.
  SAM  Serviceable Addressable Market: the slice you can actually reach and
       serve, given geography, segment and product.
  SOM  Serviceable Obtainable Market: what you can realistically win, sensibly
       inside a year or two, given you are one small firm.

Two methods:
  Top-down   Start from a published total market value and cut it down by two
             fractions (addressable, then obtainable).
  Bottom-up  Start from a count of real customers and a price, and multiply up.

Usage:
  # Write a starter assumptions file you then fill in with YOUR numbers:
  size.py --template 02-market/market-sizing-inputs.json

  # Run the sizing once the file is filled in:
  size.py --assumptions 02-market/market-sizing-inputs.json \
          --out 02-market/market-sizing.md \
          --csv 02-market/market-sizing.csv

Needs nothing but the Python standard library. If you have no assumptions file
it prints the template and exits cleanly rather than crashing.
"""

import argparse
import json
import os
import sys


TEMPLATE = {
    "currency": "GBP",
    "market": "One line naming the market you are sizing",
    "top_down": {
        "total_market_value": 0,
        "total_market_value_source": "",
        "addressable_fraction": 0.0,
        "addressable_fraction_source": "",
        "obtainable_fraction": 0.0,
        "obtainable_fraction_source": ""
    },
    "bottom_up": {
        "total_customers": 0,
        "total_customers_source": "",
        "reachable_fraction": 0.0,
        "reachable_fraction_source": "",
        "win_fraction": 0.0,
        "win_fraction_source": "",
        "annual_revenue_per_customer": 0,
        "annual_revenue_per_customer_source": ""
    }
}

TEMPLATE_NOTES = {
    "total_market_value": "Published total spend in the whole market, per year. Source it.",
    "addressable_fraction": "Share of that total you could serve (your geography and segment). 0 to 1.",
    "obtainable_fraction": "Share of the addressable slice you could realistically win. 0 to 1.",
    "total_customers": "Count of every potential buyer who has this problem. A number you can defend.",
    "reachable_fraction": "Share of those buyers you can actually reach and serve. 0 to 1.",
    "win_fraction": "Share of the reachable buyers you win in year one. Be honest; 0.01 to 0.10 is common.",
    "annual_revenue_per_customer": "What one customer pays you per year, in the stated currency."
}


def fmt(currency, value):
    symbol = {"GBP": "£", "USD": "$", "EUR": "€"}.get(currency, currency + " ")
    return "%s%s" % (symbol, "{:,.0f}".format(value))


def write_template(path):
    payload = {"_notes": TEMPLATE_NOTES}
    payload.update(TEMPLATE)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print("Wrote a starter assumptions file to %s" % path)
    print("Fill in every number and every _source before you run the sizing.")


def collect_unsourced(assumptions):
    """Return a list of (field, value) where a number is set but its source is blank.
    A source is required for any non-zero number."""
    missing = []
    for block_name in ("top_down", "bottom_up"):
        block = assumptions.get(block_name, {})
        for key, val in list(block.items()):
            if key.endswith("_source"):
                continue
            source_key = key + "_source"
            if source_key in block:
                sourced = str(block.get(source_key, "")).strip()
                if val and not sourced:
                    missing.append("%s.%s" % (block_name, key))
    return missing


def size(assumptions):
    currency = assumptions.get("currency", "GBP")
    td = assumptions.get("top_down", {})
    bu = assumptions.get("bottom_up", {})

    # Top-down
    tam_td = float(td.get("total_market_value", 0) or 0)
    sam_td = tam_td * float(td.get("addressable_fraction", 0) or 0)
    som_td = sam_td * float(td.get("obtainable_fraction", 0) or 0)

    # Bottom-up
    customers = float(bu.get("total_customers", 0) or 0)
    arpc = float(bu.get("annual_revenue_per_customer", 0) or 0)
    reach = float(bu.get("reachable_fraction", 0) or 0)
    win = float(bu.get("win_fraction", 0) or 0)
    tam_bu = customers * arpc
    sam_bu = customers * reach * arpc
    som_bu = customers * reach * win * arpc

    return currency, {
        "TAM": (tam_td, tam_bu),
        "SAM": (sam_td, sam_bu),
        "SOM": (som_td, som_bu),
    }


def ratio(a, b):
    lo, hi = sorted([a, b])
    if lo <= 0:
        return None
    return hi / lo


def render(currency, results):
    lines = []
    lines.append("| Layer | Top-down | Bottom-up | Gap (larger / smaller) |")
    lines.append("| --- | --- | --- | --- |")
    for layer in ("TAM", "SAM", "SOM"):
        td, bu = results[layer]
        r = ratio(td, bu)
        gap = "n/a" if r is None else "%.1fx" % r
        lines.append("| %s | %s | %s | %s |" % (layer, fmt(currency, td), fmt(currency, bu), gap))
    return "\n".join(lines)


def csv_rows(currency, results):
    rows = ["layer,top_down,bottom_up,gap_ratio,currency"]
    for layer in ("TAM", "SAM", "SOM"):
        td, bu = results[layer]
        r = ratio(td, bu)
        gap = "" if r is None else "%.2f" % r
        rows.append("%s,%.0f,%.0f,%s,%s" % (layer, td, bu, gap, currency))
    return "\n".join(rows) + "\n"


def verdict(results):
    """Triangulate on SOM, the number that matters. Within 2x is a pass."""
    td, bu = results["SOM"]
    r = ratio(td, bu)
    if r is None:
        return "INCONCLUSIVE: one SOM is zero. Check your assumptions before you trust this."
    if r <= 2.0:
        return "TRIANGULATED: the two SOM figures are within %.1fx. Your story holds together." % r
    return ("WIDE GAP: the two SOM figures are %.1fx apart. That is your homework. Explain "
            "which assumption is wrong before you rely on either number." % r)


def main():
    ap = argparse.ArgumentParser(description="Size a market two ways and triangulate.")
    ap.add_argument("--assumptions", help="Path to the JSON assumptions file you filled in.")
    ap.add_argument("--template", help="Write a starter assumptions file to this path and exit.")
    ap.add_argument("--out", help="Write the sizing summary (Markdown table) to this path.")
    ap.add_argument("--csv", help="Write the sizing figures to this CSV path.")
    args = ap.parse_args()

    if args.template:
        write_template(args.template)
        return

    if not args.assumptions:
        print("No --assumptions file given. Run with --template <path> to get a starter, "
              "fill it in, then re-run with --assumptions <path>.")
        return

    if not os.path.exists(args.assumptions):
        print("Assumptions file not found: %s" % args.assumptions)
        print("Run: size.py --template %s to create one." % args.assumptions)
        sys.exit(1)

    try:
        with open(args.assumptions, "r", encoding="utf-8") as fh:
            assumptions = json.load(fh)
    except Exception as exc:
        print("Could not read the assumptions file as JSON: %s" % exc)
        sys.exit(1)

    unsourced = collect_unsourced(assumptions)
    if unsourced:
        print("WARNING: these numbers have no source and must not stand:")
        for field in unsourced:
            print("  UNSOURCED -> %s" % field)
        print("Add a source for each, or flag it in the write-up as an explicit assumption.\n")

    currency, results = size(assumptions)

    table = render(currency, results)
    print("Market: %s" % assumptions.get("market", "(unnamed)"))
    print(table)
    print("")
    print(verdict(results))

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write("<!-- Figures computed by size.py. Do not hand-edit; re-run the script. -->\n\n")
            fh.write(table + "\n\n")
            fh.write(verdict(results) + "\n")
        print("\nWrote summary table to %s" % args.out)

    if args.csv:
        with open(args.csv, "w", encoding="utf-8") as fh:
            fh.write(csv_rows(currency, results))
        print("Wrote figures to %s" % args.csv)


if __name__ == "__main__":
    main()
