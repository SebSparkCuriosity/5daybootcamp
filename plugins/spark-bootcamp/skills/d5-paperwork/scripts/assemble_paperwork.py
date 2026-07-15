#!/usr/bin/env python3
"""Assemble the four DRAFT paperwork documents from the reference templates.

Reads what we already know (state, brand, the proposal, the rate card, the
data-protection clause), substitutes {{TOKENS}} in each template under
references/, embeds the data-processing schedule inside the engagement letter,
and writes the results into 05-sale/paperwork/.

Design promises, matching the rest of the plugin:
  - Nothing crashes. A missing source (proposal, rate card, DPA clause, state,
    brand) prints a clear message and falls back to a visible [TO COMPLETE]
    marker. All four drafts are written regardless.
  - Every output carries the Spark lawyer-review disclaimer. If a template
    forgot it, the script prepends it, so the done-condition cannot silently
    fail.
  - Unknown facts (bank details, company number, registered office) are left
    as [TO COMPLETE: ...] markers, never guessed.
  - Pure standard library. No optional dependency to be missing.

Usage:
  assemble_paperwork.py --root .            # write all four drafts
  assemble_paperwork.py --root . --check    # verify the done-condition only
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys


DISCLAIMER = (
    "> This is a draft. Have a qualified lawyer review it before you rely on "
    "it. Spark does not warrant it."
)
DISCLAIMER_NEEDLE = "This is a draft."

# template file in references/  ->  output file in 05-sale/paperwork/
DOCS = {
    "engagement-letter.md": "engagement-letter.md",
    "terms.md": "terms.md",
    "invoice.md": "invoice.md",
    "payment-setup.md": "payment-setup.md",
}

OUT_SUBDIR = os.path.join("05-sale", "paperwork")
PROPOSAL_PATH = os.path.join("05-sale", "PROPOSAL.md")
RATECARD_PATH = os.path.join("05-sale", "RATE-CARD.md")
DPA_PATH = os.path.join(
    ".spark", "deliverables", "data-protection", "dpa-clause.md"
)

# Marker the check mode looks for to confirm the schedule really landed inside
# the letter rather than being left as a to-do.
DPA_EMBEDDED_NEEDLE = "## 4. Data-processing schedule"
DPA_MISSING_MARKER = "[TO COMPLETE: data-processing schedule"


def skill_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def todo(label):
    return "[TO COMPLETE: %s]" % label


def read_state(root):
    """Return the state dict, or {} on any failure. Prefer the journey-state
    helper (the sanctioned reader), then fall back to reading the file."""
    state_file = os.path.join(root, ".spark", "state.json")
    helper = os.path.normpath(
        os.path.join(skill_dir(), "..", "journey-state", "scripts",
                     "update-state.py")
    )
    if os.path.exists(helper):
        try:
            proc = subprocess.run(
                [sys.executable, helper, "--file", state_file, "--read"],
                capture_output=True, text=True, timeout=30,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                return json.loads(proc.stdout)
        except Exception:
            pass
    try:
        with open(state_file, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def read_brand(root):
    try:
        p = os.path.join(root, ".spark", "brand", "brand.json")
        with open(p, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {}


def read_text(root, rel):
    try:
        with open(os.path.join(root, rel), "r", encoding="utf-8") as fh:
            return fh.read()
    except Exception:
        return None


def first_price(text):
    """Pull the first sterling figure out of a document. Returns a string like
    'GBP 2,000' or None. Recognises 'GBP 2000', '£2,000' and 'GBP2,500'."""
    if not text:
        return None
    m = re.search(r"(?:GBP|£)\s*([0-9][0-9,]*)", text, re.IGNORECASE)
    if not m:
        return None
    return "GBP " + m.group(1).replace(" ", "")


def money_to_int(price):
    """'GBP 2,000' -> 2000, or None if it cannot be parsed."""
    if not price:
        return None
    m = re.search(r"([0-9][0-9,]*)", price)
    if not m:
        return None
    try:
        return int(m.group(1).replace(",", ""))
    except ValueError:
        return None


def fmt_gbp(n):
    return "GBP {:,}".format(n)


def extract_scope(proposal_text):
    """Best-effort scope block from the proposal. Grab the lines under a
    'scope', 'what we will do' or 'deliver' heading, else the first real
    paragraph. Falls back to a marker when there is no proposal."""
    if not proposal_text:
        return None, None
    lines = proposal_text.splitlines()
    # try to find a scope-ish heading and take the block under it
    heading_re = re.compile(
        r"^#{1,6}\s*(scope|what (we|you) (will )?(do|get)|deliverable"
        r"|the work)", re.IGNORECASE
    )
    for i, line in enumerate(lines):
        if heading_re.match(line.strip()):
            block = []
            for nxt in lines[i + 1:]:
                if nxt.strip().startswith("#"):
                    break
                block.append(nxt)
            block_text = "\n".join(block).strip()
            if block_text:
                oneliner = next(
                    (b.strip("-* ").strip() for b in block
                     if b.strip()), block_text
                )
                return block_text, oneliner
    # fall back: first non-heading, non-blank, non-disclaimer paragraph
    for line in lines:
        s = line.strip()
        if s and not s.startswith("#") and not s.startswith(">"):
            return s, s
    return None, None


def build_tokens(root):
    """Compute every {{TOKEN}} value and a list of warnings for missing
    sources. Returns (tokens, warnings, dpa_present)."""
    warnings = []
    state = read_state(root)
    brand = read_brand(root)

    founder = state.get("founder") or todo("your name")
    business_type = state.get("business_type") or "services"

    trading_entity = (
        brand.get("business_name")
        or brand.get("name")
        or state.get("business_name")
        or todo("your registered trading entity, e.g. Harbour Advisory Limited")
    )
    trading_as = (
        "Trading as %s" % (brand.get("brand_name") or brand.get("name"))
        if brand.get("brand_name") and brand.get("brand_name") != trading_entity
        else todo("trading-as name, or delete this line if none")
    )

    # sources
    proposal_text = read_text(root, PROPOSAL_PATH)
    if proposal_text is None:
        warnings.append(
            "no %s found: scope, target and timeline left as markers"
            % PROPOSAL_PATH
        )
    ratecard_text = read_text(root, RATECARD_PATH)
    if ratecard_text is None:
        warnings.append(
            "no %s found: price left as a marker" % RATECARD_PATH
        )
    dpa_text = read_text(root, DPA_PATH)
    dpa_present = dpa_text is not None
    if not dpa_present:
        warnings.append(
            "no %s found: run the data-protection skill, then re-run this. "
            "The letter carries a data-processing-schedule marker for now."
            % DPA_PATH
        )

    # price, preferring the rate card, then the proposal
    price = first_price(ratecard_text) or first_price(proposal_text)
    price_str = price or todo("the fixed price, e.g. GBP 2,000")
    price_int = money_to_int(price)
    deposit_pct = "50%"
    if price_int is not None:
        deposit_amount = fmt_gbp(round(price_int * 0.5))
        balance_amount = fmt_gbp(price_int - round(price_int * 0.5))
    else:
        deposit_amount = todo("50% of the price")
        balance_amount = todo("the remaining balance")

    scope_block, scope_oneliner = extract_scope(proposal_text)
    scope = scope_block or todo(
        "the exact scope, copied from 05-sale/PROPOSAL.md"
    )
    scope_oneliner = scope_oneliner or todo(
        "one-line scope for the invoice"
    )

    dpa_schedule = dpa_text.strip() if dpa_present else (
        DPA_MISSING_MARKER + ". Run the data-protection skill and re-run "
        "this assembler so the schedule lands here.]"
    )

    tokens = {
        "DISCLAIMER": DISCLAIMER,
        "DATE": datetime.date.today().isoformat(),
        "FOUNDER": founder,
        "TRADING_ENTITY": trading_entity,
        "TRADING_AS_LINE": trading_as,
        "REGISTERED_OFFICE": todo("registered office address"),
        "COMPANY_NUMBER": todo("company registration number, or 'sole trader'"),
        "JURISDICTION": todo("Jersey, or your jurisdiction"),
        "SCOPE": scope,
        "SCOPE_ONELINE": scope_oneliner,
        "TARGET": (state.get("headline_target")
                   or todo("the numeric outcome, from the proposal")),
        "TIMELINE": todo("the timeline, 1 to 6 weeks, from the proposal"),
        "PRICE": price_str,
        "DEPOSIT_PCT": deposit_pct,
        "DEPOSIT_AMOUNT": deposit_amount,
        "BALANCE_AMOUNT": balance_amount,
        "DPA_SCHEDULE": dpa_schedule,
    }
    return tokens, warnings, dpa_present


def render(template, tokens):
    out = template
    for key, val in tokens.items():
        out = out.replace("{{%s}}" % key, str(val))
    if DISCLAIMER_NEEDLE not in out:
        out = DISCLAIMER + "\n\n" + out
    return out


def write_docs(root):
    tokens, warnings, dpa_present = build_tokens(root)
    ref_dir = os.path.join(skill_dir(), "references")
    out_dir = os.path.join(root, OUT_SUBDIR)
    os.makedirs(out_dir, exist_ok=True)

    written = 0
    markers_total = 0
    for template_name, out_name in DOCS.items():
        tpl_path = os.path.join(ref_dir, template_name)
        try:
            with open(tpl_path, "r", encoding="utf-8") as fh:
                template = fh.read()
        except Exception:
            print("WARN: template missing, skipped: %s" % tpl_path)
            continue
        rendered = render(template, tokens)
        with open(os.path.join(out_dir, out_name), "w", encoding="utf-8") as fh:
            fh.write(rendered)
        written += 1
        markers_total += rendered.count("[TO COMPLETE")

    for w in warnings:
        print("WARN: " + w)
    print("Wrote %d/4 paperwork drafts to %s" % (written, OUT_SUBDIR))
    print("Data-processing schedule embedded in the letter: %s"
          % ("yes" if dpa_present else "NO, marker left, re-run after "
             "data-protection"))
    print("[TO COMPLETE] markers remaining across the pack: %d" % markers_total)
    print("Fill every marker before you send anything or ask for money.")
    return written


def check(root):
    """Verify the five mechanical done-conditions. Prints CHECK_RESULT=OK or a
    numbered list of what is missing. Exit 0 on OK, 1 on any failure."""
    out_dir = os.path.join(root, OUT_SUBDIR)
    fails = []

    def load(name):
        try:
            with open(os.path.join(out_dir, name), "r", encoding="utf-8") as fh:
                return fh.read()
        except Exception:
            return None

    letter = load("engagement-letter.md")
    terms = load("terms.md")
    invoice = load("invoice.md")
    payment = load("payment-setup.md")

    # 1. letter, terms, invoice present
    for label, doc in (("engagement-letter.md", letter),
                       ("terms.md", terms), ("invoice.md", invoice)):
        if doc is None:
            fails.append("%s is missing from %s" % (label, OUT_SUBDIR))

    # 2. each present doc carries the disclaimer
    for label, doc in (("engagement-letter.md", letter),
                       ("terms.md", terms), ("invoice.md", invoice),
                       ("payment-setup.md", payment)):
        if doc is not None and DISCLAIMER_NEEDLE not in doc:
            fails.append("%s does not carry the draft disclaimer" % label)

    # 3. a working payment method named in payment-setup.md
    if payment is None:
        fails.append("payment-setup.md is missing")
    elif "bank transfer" not in payment.lower():
        fails.append("payment-setup.md names no working payment method "
                     "(expected bank transfer)")

    # 4. invoice states a price
    if invoice is not None and not first_price(invoice):
        fails.append("invoice.md states no price (no GBP or £ figure found)")

    # 5. data-processing schedule embedded in the engagement letter
    if letter is not None:
        if DPA_EMBEDDED_NEEDLE not in letter:
            fails.append("engagement letter has no data-processing-schedule "
                         "section")
        elif DPA_MISSING_MARKER in letter:
            fails.append("data-processing schedule is still a marker in the "
                         "letter: run the data-protection skill, then re-run "
                         "this assembler")

    if fails:
        print("CHECK_RESULT=FAIL")
        for i, f in enumerate(fails, 1):
            print("  %d. %s" % (i, f))
        return 1
    print("CHECK_RESULT=OK letter, terms and invoice present; each carries "
          "the disclaimer; bank transfer set as payment method; invoice "
          "priced; data-processing schedule embedded in the letter (5 of 5)")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Assemble Spark Day 5 paperwork "
                                             "drafts")
    ap.add_argument("--root", default=".", help="project root holding .spark")
    ap.add_argument("--check", action="store_true",
                    help="verify the done-condition only, write nothing")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    if args.check:
        sys.exit(check(root))
    write_docs(root)
    print()
    print("Now run with --check to confirm the done-condition.")


if __name__ == "__main__":
    main()
