# docs

- `spark-bootcamp-overview.pptx`: a 17-slide overview of the plugin (what it is,
  the pre-work phase and five-day arc, install and run, the architecture, every
  skill by phase, the three business paths, the efficiency and audit design, and
  the Friday outcome).
- `build_overview_deck.py`: regenerates the deck. Needs `python-pptx`
  (`pip install python-pptx`), then `python3 build_overview_deck.py out.pptx`.
- `session-plan.md`: the facilitator's timed session plan for running the
  bootcamp live, pre-work plus all five days, mapped against the real skill
  chain. The source outline for the day-by-day decks below.
- `decks/`: the day-by-day facilitator decks, two versions, both built from
  `session-plan.md`:
  - `day-1.html` through `day-5.html`: the current version. Interactive,
    Digital Jersey-branded, self-contained single-file decks (keyboard,
    swipe and click navigation, a progress bar, an animated network
    background on gradient slides). Just open one in a browser.
    `build_day_html_decks.py` regenerates them; it reads the Cairo and Open
    Sans font files from `fonts/` and embeds them so each deck works
    offline with no installed fonts or network connection.
  - `day-1.pptx` through `day-5.pptx`: the earlier Spark-branded PowerPoint
    version, kept for reference. `build_day_decks.py` regenerates these via
    the `spark-branding` skill; needs `python-pptx` plus Lora and Inter
    installed for accurate layout.
- `fonts/`: Cairo and Open Sans WOFF2 files used by
  `build_day_html_decks.py` to make the HTML decks self-contained.
