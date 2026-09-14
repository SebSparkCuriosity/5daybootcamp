#!/usr/bin/env python3
"""Render a day slide deck to a PDF, one slide per page.

The HTML deck is the thing you present on screen. This is the copy that sits
behind it: printable, e-mailable, and readable when the wifi dies.

The five day decks live as Claude artifacts, not in this repo. Save a deck's
HTML locally, then:

    pip install playwright pillow
    python3 docs/slides_to_pdf.py day1.html bootcamp-day1.pdf

It drives the deck's own slide navigation, freezes the transitions so every
capture is a settled frame, hides the presenter chrome, and writes one page
per slide at 16:9.
"""
import io, os, sys
from PIL import Image
from playwright.sync_api import sync_playwright

W, H = 1600, 900          # 16:9, matches the slide stage
# Playwright finds its own browser; set SLIDES_CHROME to override.
CHROME = os.environ.get('SLIDES_CHROME', '/opt/pw-browsers/chromium')


def render(src, out):
    shots = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            executable_path=CHROME if os.path.exists(CHROME) else None,
            args=['--no-sandbox', '--force-color-profile=srgb',
                  '--font-render-hinting=none'])
        page = browser.new_page(viewport={'width': W, 'height': H},
                                device_scale_factor=2)
        page.goto('file://' + os.path.abspath(src), wait_until='networkidle')
        page.wait_for_timeout(1200)          # fonts + first paint

        dots = page.query_selector_all('#dots .dot')
        if not dots:
            sys.exit(f'{src}: no slide navigation found')

        # kill the transitions so each capture is a settled frame
        page.add_style_tag(content="""
            .slide{transition:none!important;}
            .slide-inner,.slide-inner>*{animation:none!important;
              opacity:1!important;transform:none!important;}
            .chrome,.nav,.pace-wrap,#dots,.counter,
            #prevBtn,#nextBtn,.navbtn,.arrow,.progress{visibility:hidden!important;}
        """)

        for i in range(len(dots)):
            page.evaluate(f'document.querySelectorAll("#dots .dot")[{i}].click()')
            page.wait_for_timeout(450)
            shots.append(Image.open(io.BytesIO(page.screenshot())).convert('RGB'))
        browser.close()

    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    shots[0].save(out, 'PDF', save_all=True, append_images=shots[1:],
                  resolution=200.0)
    mb = os.path.getsize(out) / 1e6
    print(f'{os.path.basename(out)}: {len(shots)} pages, {mb:.1f} MB')


if __name__ == '__main__':
    render(sys.argv[1], sys.argv[2])
