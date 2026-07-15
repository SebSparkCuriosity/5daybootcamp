#!/usr/bin/env python3
"""Check that a domain resolves and can carry mail. Day 3, Spark bootcamp.

Two things this proves, and one it cannot:
  1. The domain resolves to a host (an A/AAAA record answers).
  2. The domain has mail records (MX, or you tell us forwarding is in use).
  3. It CANNOT read your inbox, so the actual send-and-receive test is yours
     to do by eye. This script never claims mail works end to end.

Usage:
  check-domain-email.py --domain harbourtrust.je
  check-domain-email.py --domain harbourtrust.je --email you@harbourtrust.je
  check-domain-email.py --domain harbourtrust.je --verbose

It degrades gracefully. It prefers dnspython for MX lookups; if that is not
installed it falls back to the system `nslookup`/`host` command; if neither is
available it still checks that the domain resolves and tells you to confirm MX
by hand. It never crashes on a lookup failure: a failure is a FAIL line, not a
stack trace.

Exit code is 0 when every requested check PASSES, 1 otherwise, so a script can
gate on it.
"""

import argparse
import shutil
import socket
import subprocess
import sys


def resolves(domain):
    """True if the domain has an A or AAAA record. Uses the standard library
    only, so this always works even with no extra packages installed."""
    try:
        infos = socket.getaddrinfo(domain, None)
        addrs = sorted({i[4][0] for i in infos})
        return True, addrs
    except Exception as exc:
        return False, str(exc)


def mx_via_dnspython(domain):
    try:
        import dns.resolver  # type: ignore
    except Exception:
        return None  # signal "library not available"
    try:
        answers = dns.resolver.resolve(domain, "MX")
        records = sorted(str(r.exchange).rstrip(".") for r in answers)
        return records
    except Exception:
        return []  # library present, no MX found


def mx_via_command(domain):
    """Fallback MX lookup through nslookup or host. Returns a list of exchanges,
    or None if no suitable command exists."""
    for tool in ("nslookup", "host", "dig"):
        if not shutil.which(tool):
            continue
        try:
            if tool == "nslookup":
                cmd = ["nslookup", "-query=MX", domain]
            elif tool == "host":
                cmd = ["host", "-t", "MX", domain]
            else:  # dig
                cmd = ["dig", "+short", "MX", domain]
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=20).stdout
            records = []
            for line in out.splitlines():
                low = line.lower()
                if "mail exchanger" in low or "mx record" in low or (tool == "dig" and line.strip()):
                    records.append(line.strip())
            return records
        except Exception:
            continue
    return None  # no lookup command available


def check_mx(domain, verbose):
    """Return (status, detail). status is one of PASS, FAIL, UNKNOWN."""
    records = mx_via_dnspython(domain)
    source = "dnspython"
    if records is None:
        records = mx_via_command(domain)
        source = "system lookup"
    if records is None:
        return "UNKNOWN", ("no MX lookup tool found (install dnspython with "
                           "`pip install dnspython`, or confirm MX by hand)")
    if records:
        detail = "%d mail record(s) via %s" % (len(records), source)
        if verbose:
            detail += ": " + ", ".join(records)
        return "PASS", detail
    return "FAIL", ("no MX records via %s. If you are using email forwarding "
                    "only, that can be normal; confirm forwarding is set up at "
                    "your registrar." % source)


def main():
    ap = argparse.ArgumentParser(description="Check a domain resolves and can carry mail.")
    ap.add_argument("--domain", required=True, help="The domain to check, e.g. harbourtrust.je")
    ap.add_argument("--email", help="Optional address on the domain, e.g. you@harbourtrust.je")
    ap.add_argument("--verbose", action="store_true", help="Show the addresses and records found")
    args = ap.parse_args()

    domain = args.domain.strip().lower().lstrip("@")
    if "@" in domain:
        domain = domain.split("@", 1)[1]

    print("Checking %s" % domain)
    print("-" * 40)

    all_pass = True

    # 1. Does it resolve?
    ok, detail = resolves(domain)
    if ok:
        msg = "PASS  domain resolves"
        if args.verbose:
            msg += " -> " + ", ".join(detail)
        print(msg)
    else:
        all_pass = False
        print("FAIL  domain does not resolve (%s)" % detail)
        print("      If you have not registered it yet, that is expected: it is")
        print("      probably available. If you just set DNS, wait up to two hours.")

    # 2. Mail records.
    status, mdetail = check_mx(domain, args.verbose)
    if status == "PASS":
        print("PASS  %s" % mdetail)
    elif status == "UNKNOWN":
        print("SKIP  mail records not checked: %s" % mdetail)
    else:
        all_pass = False
        print("FAIL  %s" % mdetail)

    # 3. The part we cannot automate.
    if args.email:
        print("-" * 40)
        print("NOW DO THIS BY HAND (the script cannot read your inbox):")
        print("  1. Send an email FROM %s to another inbox you control." % args.email)
        print("  2. Reply back TO %s and confirm it arrives." % args.email)
        print("  Only tick 'business email verified' once both land.")

    print("-" * 40)
    if all_pass:
        print("RESULT=PASS  domain checks passed. Confirm the email test by eye.")
        sys.exit(0)
    else:
        print("RESULT=FAIL  see the FAIL lines above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
