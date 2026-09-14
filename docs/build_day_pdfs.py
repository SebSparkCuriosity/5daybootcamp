#!/usr/bin/env python3
"""Export each day's HTML deck to a PDF handout for participants.

Reuses the same day-N.html files build_day_html_decks.py produces: the
`@media print` rules baked into their <style> block turn the interactive,
one-slide-at-a-time deck into a linear document, one page per slide,
landscape, matching the on-screen 16:9 shape. Reveal steps and flip cards
show fully expanded (there's no clicking a PDF), live countdowns collapse
to just the "Back at HH:MM" label, and the facilitator-only chrome
(nav arrows, dots, progress bar, the live pacing pill) is hidden.

Requires Playwright with a Chromium browser available. Needs
`pip install playwright` plus either a normal `playwright install
chromium`, or (as in this sandboxed session) PLAYWRIGHT_BROWSERS_PATH
already pointing at a pre-installed browser — pass its executable via
--chromium-path if Playwright can't find it automatically.

Usage:
    python3 build_day_pdfs.py [--decks-dir docs/decks] [--out-dir docs/decks]
                               [--chromium-path /opt/pw-browsers/chromium]
"""
import argparse
import os

HERE = os.path.dirname(os.path.abspath(__file__))

DAYS = [1, 2, 3, 4, 5]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--decks-dir", default=os.path.join(HERE, "decks"))
    ap.add_argument("--out-dir", default=os.path.join(HERE, "decks"))
    ap.add_argument("--chromium-path", default=os.environ.get("PLAYWRIGHT_CHROMIUM_PATH"))
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    os.makedirs(args.out_dir, exist_ok=True)

    with sync_playwright() as p:
        launch_kwargs = {}
        if args.chromium_path:
            launch_kwargs["executable_path"] = args.chromium_path
        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page(viewport={"width": 1400, "height": 850})

        for n in DAYS:
            html_path = os.path.join(args.decks_dir, f"day-{n}.html")
            pdf_path = os.path.join(args.out_dir, f"day-{n}.pdf")
            page.goto(f"file://{os.path.abspath(html_path)}")
            # Let the entrance animations and web fonts settle before the
            # print snapshot, even though @media print also force-completes
            # them, so nothing is caught mid-transition.
            page.wait_for_timeout(2000)
            page.emulate_media(media="print")
            page.pdf(
                path=pdf_path,
                width="13.333in",
                height="7.5in",
                print_background=True,
                margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            )
            print(f"wrote {pdf_path} ({os.path.getsize(pdf_path)/1024:.0f} KB)")

        browser.close()


if __name__ == "__main__":
    main()
