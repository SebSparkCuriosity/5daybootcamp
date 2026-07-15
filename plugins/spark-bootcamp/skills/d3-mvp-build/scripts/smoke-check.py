#!/usr/bin/env python3
"""Smoke-check a deployed URL for the Day 3 build.

Confirms a public URL is genuinely live: reports HTTP status and response time.
"It worked locally" is not shipped. This checks the real, public URL.

Usage:
    python3 smoke-check.py https://your-thing.vercel.app

Exit codes:
    0  URL returned HTTP 200, it is live
    1  URL reachable but returned a non-200 status
    2  URL could not be reached, or was not supplied

Degrades gracefully: uses only the Python standard library, so it runs
anywhere Python 3 does, with no pip install needed.
"""

import sys
import time
import ssl
from urllib import request, error


def check(url: str) -> int:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # A relaxed context so a fresh Vercel cert or proxy does not trip us up.
    # We are checking liveness, not auditing TLS.
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = request.Request(url, headers={"User-Agent": "spark-bootcamp-smoke-check"})
    start = time.time()
    try:
        with request.urlopen(req, timeout=15, context=ctx) as resp:
            elapsed = (time.time() - start) * 1000
            status = resp.getcode()
            print(f"URL:      {url}")
            print(f"Status:   {status}")
            print(f"Time:     {elapsed:.0f} ms")
            if status == 200:
                print("Result:   LIVE. A prospect can reach this. Now do the action yourself.")
                return 0
            print(f"Result:   Reachable but returned {status}, not 200. Fix the deploy before you log the day.")
            return 1
    except error.HTTPError as e:
        elapsed = (time.time() - start) * 1000
        print(f"URL:      {url}")
        print(f"Status:   {e.code}")
        print(f"Time:     {elapsed:.0f} ms")
        print(f"Result:   Server answered {e.code}, not 200. The page is up but erroring. Fix it before you log the day.")
        return 1
    except (error.URLError, TimeoutError, OSError) as e:
        print(f"URL:      {url}")
        reason = getattr(e, "reason", e)
        print(f"Result:   COULD NOT REACH ({reason}). This is not live yet. Check the deploy finished and the URL is right.")
        return 2


def main() -> int:
    if len(sys.argv) < 2:
        print("Give me a URL to check. Example:")
        print("  python3 smoke-check.py https://your-thing.vercel.app")
        return 2
    return check(sys.argv[1].strip())


if __name__ == "__main__":
    sys.exit(main())
