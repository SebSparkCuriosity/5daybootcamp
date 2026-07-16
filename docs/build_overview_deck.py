#!/usr/bin/env python3
"""Build the Spark Bootcamp plugin overview deck (PPTX)."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---- palette ----
INK    = RGBColor(0x14, 0x20, 0x2B)   # dark slate, primary text and dividers
SPARK  = RGBColor(0xF5, 0x8A, 0x23)   # warm amber accent
PAPER  = RGBColor(0xFF, 0xFF, 0xFF)
PANEL  = RGBColor(0xF4, 0xF6, 0xF8)   # very light grey-blue
MUTED  = RGBColor(0x5A, 0x6B, 0x7B)   # slate grey secondary text
LINE   = RGBColor(0xDD, 0xE3, 0xE8)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
ROWALT = RGBColor(0xF7, 0xF9, 0xFB)

FONT = "Calibri"
MONO = "Consolas"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = prs.slide_width, prs.slide_height
MARGIN = Inches(0.75)
CW = SW - 2 * MARGIN

def slide():
    return prs.slides.add_slide(BLANK)

def rect(s, x, y, w, h, fill, line=None, line_w=None, shape=MSO_SHAPE.RECTANGLE):
    sp = s.shapes.add_shape(shape, x, y, w, h)
    sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line
        sp.line.width = line_w or Pt(1)
    sp.shadow.inherit = False
    return sp

def textbox(s, x, y, w, h, lines, anchor=MSO_ANCHOR.TOP):
    """lines: list of dicts {text,size,color,bold,align,space_after,font}"""
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = ln.get("align", PP_ALIGN.LEFT)
        if ln.get("space_after") is not None:
            p.space_after = Pt(ln["space_after"])
        if ln.get("space_before") is not None:
            p.space_before = Pt(ln["space_before"])
        r = p.add_run(); r.text = ln["text"]
        f = r.font
        f.name = ln.get("font", FONT)
        f.size = Pt(ln.get("size", 18))
        f.bold = ln.get("bold", False)
        f.color.rgb = ln.get("color", INK)
    return tb

def footer(s, n):
    textbox(s, MARGIN, SH - Inches(0.5), CW, Inches(0.3),
            [{"text": "Spark Bootcamp  ·  a Claude Code plugin by Spark AI Agency", "size": 9, "color": MUTED}])
    textbox(s, SW - MARGIN - Inches(0.6), SH - Inches(0.5), Inches(0.6), Inches(0.3),
            [{"text": str(n), "size": 9, "color": MUTED, "align": PP_ALIGN.RIGHT}])

def header(s, kicker, title):
    rect(s, MARGIN, Inches(0.62), Inches(0.34), Inches(0.34), SPARK)  # spark tab
    textbox(s, MARGIN + Inches(0.5), Inches(0.6), CW - Inches(0.5), Inches(0.3),
            [{"text": kicker.upper(), "size": 12, "color": SPARK, "bold": True}])
    textbox(s, MARGIN + Inches(0.5), Inches(0.92), CW - Inches(0.5), Inches(0.7),
            [{"text": title, "size": 28, "color": INK, "bold": True}])
    rect(s, MARGIN + Inches(0.5), Inches(1.62), Inches(1.2), Pt(3), INK)

def bg(s, color=PAPER):
    rect(s, 0, 0, SW, SH, color)

# ---------- 1. TITLE ----------
s = slide(); bg(s, INK)
rect(s, 0, 0, Inches(0.55), SH, SPARK)                       # left accent stripe
rect(s, MARGIN + Inches(0.2), Inches(2.35), Inches(0.9), Pt(5), SPARK)
textbox(s, MARGIN + Inches(0.2), Inches(2.55), CW, Inches(2.2), [
    {"text": "Spark Bootcamp", "size": 54, "color": WHITE, "bold": True, "space_after": 6},
    {"text": "Five days from a raw idea to a first paying customer.", "size": 24, "color": RGBColor(0xC9,0xD4,0xDE)},
])
textbox(s, MARGIN + Inches(0.2), Inches(5.1), CW, Inches(1.4), [
    {"text": "A Claude Code plugin. 60 skills, one guided week.", "size": 16, "color": SPARK, "bold": True, "space_after": 4},
    {"text": "Built by Spark AI Agency for Digital Jersey's cohort.", "size": 14, "color": RGBColor(0xC9,0xD4,0xDE)},
    {"text": "sparkconsulting.tech", "size": 12, "color": MUTED},
])

# ---------- 2. WHAT IT IS ----------
s = slide(); bg(s); header(s, "What it is", "One plugin that walks a founder from idea to income")
textbox(s, MARGIN + Inches(0.5), Inches(1.95), CW - Inches(0.5), Inches(1.8), [
    {"text": "You install it, type one command a day, and it hand-holds you through the whole journey: validating "
             "the problem with real interviews, mapping the market, building a brand and a pitch deck, defining and "
             "building an MVP, testing it, and closing your first sale.", "size": 17, "color": INK, "space_after": 10},
    {"text": "It works whether you are building software, hardware or a service. Everything you produce is saved to "
             "your own project and logged, so you finish the week with a working product and an audit trail a "
             "regulator nods at rather than flinches from.", "size": 17, "color": INK},
])
facts = [("60", "skills"), ("5", "days"), ("3", "business paths"), ("£2,000+", "first sale, fixed price")]
fw = (CW - Inches(0.5) - Inches(0.6)) / 4
for i, (big, small) in enumerate(facts):
    x = MARGIN + Inches(0.5) + i * (fw + Inches(0.2))
    rect(s, x, Inches(4.5), fw, Inches(1.6), PANEL)
    rect(s, x, Inches(4.5), fw, Pt(4), SPARK)
    textbox(s, x, Inches(4.75), fw, Inches(1.2), [
        {"text": big, "size": 34, "color": INK, "bold": True, "align": PP_ALIGN.CENTER, "space_after": 2},
        {"text": small, "size": 13, "color": MUTED, "align": PP_ALIGN.CENTER},
    ], anchor=MSO_ANCHOR.MIDDLE)
footer(s, 2)

# ---------- 3. WEEK AT A GLANCE ----------
s = slide(); bg(s); header(s, "The week", "Five days, five numeric outcomes")
week = [
    ("Mon", "Discovery", "8 to 12 interviews synthesised, one validated problem, one named segment"),
    ("Tue", "Market & Proposition", "A market map, TAM/SAM/SOM, a proposition and USP, a brand, a hand-out pitch deck"),
    ("Wed", "Product & Build", "A working MVP live for a real prospect to act on, tracked in GitHub"),
    ("Thu", "Test & Go-to-Market", "5 usability tests, a sales deck, client processes, a funnel, a booked Friday meeting"),
    ("Fri", "Tweaks & First Sale", "Final fixes, pricing, and one committed yes with a date and an amount"),
]
y = Inches(2.05); rh = Inches(0.92)
for i, (day, theme, out) in enumerate(week):
    yy = y + i * (rh + Inches(0.06))
    rect(s, MARGIN + Inches(0.5), yy, CW - Inches(0.5), rh, PANEL if i % 2 == 0 else WHITE, line=LINE)
    rect(s, MARGIN + Inches(0.5), yy, Inches(1.15), rh, INK)
    textbox(s, MARGIN + Inches(0.5), yy, Inches(1.15), rh,
            [{"text": day, "size": 18, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, MARGIN + Inches(1.85), yy, Inches(2.9), rh,
            [{"text": theme, "size": 15, "color": INK, "bold": True}], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, MARGIN + Inches(4.9), yy, CW - Inches(5.4), rh,
            [{"text": out, "size": 12.5, "color": MUTED}], anchor=MSO_ANCHOR.MIDDLE)
footer(s, 3)

# ---------- 4. INSTALL & RUN ----------
s = slide(); bg(s); header(s, "Getting started", "Install, then three commands")
def code_block(s, x, y, w, lines, h=None):
    h = h or Inches(0.3 + 0.32 * len(lines))
    rect(s, x, y, w, h, INK)
    para = [{"text": l, "size": 13, "color": RGBColor(0xE6,0xED,0xF2), "font": MONO,
             "space_after": 3} for l in lines]
    textbox(s, x + Inches(0.2), y + Inches(0.15), w - Inches(0.4), h - Inches(0.3), para)
    return h
textbox(s, MARGIN + Inches(0.5), Inches(1.95), CW - Inches(0.5), Inches(0.3),
        [{"text": "1. Install the plugin (once)", "size": 15, "color": INK, "bold": True}])
code_block(s, MARGIN + Inches(0.5), Inches(2.32), CW - Inches(0.5),
           ["/plugin marketplace add SebSparkCuriosity/5daybootcamp",
            "/plugin install spark-bootcamp@spark"])
textbox(s, MARGIN + Inches(0.5), Inches(3.5), CW - Inches(0.5), Inches(0.3),
        [{"text": "2. Set up and start the week", "size": 15, "color": INK, "bold": True}])
code_block(s, MARGIN + Inches(0.5), Inches(3.87), CW - Inches(0.5),
           ["/spark-bootcamp:doctor    # checks your machine, lays out your project, lists the pre-work",
            "/spark-bootcamp:start     # captures your idea, path and numeric target for the week"])
textbox(s, MARGIN + Inches(0.5), Inches(5.05), CW - Inches(0.5), Inches(0.3),
        [{"text": "3. Every step after that", "size": 15, "color": INK, "bold": True}])
code_block(s, MARGIN + Inches(0.5), Inches(5.42), CW - Inches(0.5),
           ["/spark-bootcamp:coach     # where you are, and the one command to run next"])
textbox(s, MARGIN + Inches(0.5), Inches(6.35), CW - Inches(0.5), Inches(0.6),
        [{"text": "Start each day in a fresh session. Progress lives on disk, so coach picks up exactly where you "
                  "left off, and your Claude usage lasts the whole week.", "size": 12.5, "color": SPARK, "bold": True}])
footer(s, 4)

# ---------- 5. ARCHITECTURE ----------
s = slide(); bg(s); header(s, "How it is built", "A thin spine holds a guided journey together")
layers = [
    ("The five days", "Day 1 Discovery  ·  Day 2 Market & Proposition  ·  Day 3 Product & Build  ·  Day 4 Test & GTM  ·  Day 5 First Sale",
     "42 skills that do the daily work, each producing one concrete artefact", SPARK),
    ("The interview engine", "run-interview  ·  synthesise-interviews  ·  interview-method",
     "Built once, borrowed twice: discovery on Monday, product-testing on Thursday", RGBColor(0x2E,0x86,0xC1)),
    ("The spine (always on)", "state machine  ·  coach  ·  checkpoint  ·  logging  ·  brand  ·  guardrails  ·  data-protection",
     "15 skills that track where you are, log every step, and keep the week auditable", INK),
]
y = Inches(2.1); bh = Inches(1.45)
for i, (name, mid, sub, col) in enumerate(layers):
    yy = y + i * (bh + Inches(0.18))
    rect(s, MARGIN + Inches(0.5), yy, CW - Inches(0.5), bh, PANEL, line=LINE)
    rect(s, MARGIN + Inches(0.5), yy, Inches(0.14), bh, col)
    textbox(s, MARGIN + Inches(0.85), yy + Inches(0.16), CW - Inches(1.4), bh - Inches(0.3), [
        {"text": name, "size": 17, "color": INK, "bold": True, "space_after": 3},
        {"text": mid, "size": 13, "color": INK, "bold": True, "space_after": 3},
        {"text": sub, "size": 12, "color": MUTED},
    ])
footer(s, 5)

# ---------- table helper ----------
def _set_cell(cell, text, size, color, bold, fill, align=PP_ALIGN.LEFT, mono=False):
    cell.fill.solid(); cell.fill.fore_color.rgb = fill
    cell.margin_left = Pt(7); cell.margin_right = Pt(7)
    cell.margin_top = Pt(3); cell.margin_bottom = Pt(3)
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf = cell.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    f = r.font; f.name = MONO if mono else FONT
    f.size = Pt(size); f.bold = bold; f.color.rgb = color

def skill_table(s, rows, top=Inches(2.0), size=11.5):
    """rows: list of (skill_id, description)."""
    n = len(rows) + 1
    tbl_h = SH - top - Inches(0.65)
    x = MARGIN + Inches(0.5); w = CW - Inches(0.5)
    gtbl = s.shapes.add_table(n, 2, x, top, w, tbl_h).table
    gtbl.columns[0].width = Inches(3.05); gtbl.columns[1].width = w - Inches(3.05)
    # strip default banding style
    tblPr = gtbl._tbl.tblPr
    tblPr.set('firstRow', '0'); tblPr.set('bandRow', '0')
    _set_cell(gtbl.cell(0, 0), "Skill", 12, WHITE, True, INK)
    _set_cell(gtbl.cell(0, 1), "What it does", 12, WHITE, True, INK)
    gtbl.rows[0].height = Inches(0.4)
    for i, (sid, desc) in enumerate(rows, start=1):
        fill = ROWALT if i % 2 else WHITE
        _set_cell(gtbl.cell(i, 0), sid, size, INK, True, fill, mono=True)
        _set_cell(gtbl.cell(i, 1), desc, size, INK, False, fill)
        gtbl.rows[i].height = Inches(0.34)

def table_slide(kicker, title, rows, note=None, page=0, size=11.5):
    s = slide(); bg(s); header(s, kicker, title)
    top = Inches(2.0)
    if note:
        textbox(s, MARGIN + Inches(0.5), Inches(1.78), CW - Inches(0.5), Inches(0.3),
                [{"text": note, "size": 12.5, "color": SPARK, "bold": True}])
        top = Inches(2.18)
    skill_table(s, rows, top=top, size=size)
    footer(s, page)
    return s

# ---------- 6. SPINE ----------
table_slide("Architecture", "The spine: 13 skills, always on", [
    ("doctor", "One-time setup and pre-work check: machine, accounts, entity and bank, domain, budget"),
    ("start", "Registers your name, path, one-sentence idea and headline numeric target"),
    ("coach", "Tells you where you are and the one command to run next"),
    ("checkpoint", "Opens each day with a target, closes it with the actual number"),
    ("journey-state", "The state-machine helper every skill reads and writes (hidden)"),
    ("logbook", "The one logging format for the changelog and decision log (hidden)"),
    ("audit-pack", "Compiles the week's logs into a regulator or investor pack"),
    ("brand-register", "The canonical brand store every document reads from"),
    ("house-style", "Shared deck and page templates plus the voice checklist (hidden)"),
    ("business-profile", "The one software / hardware / services variance matrix (hidden)"),
    ("guardrails", "No fabricated numbers, human sign-off before send or spend (hidden)"),
    ("regulator-check", "Reviews any artefact for unsupported claims before it ships"),
    ("data-protection", "Draft privacy notice, consent wording and data-processing clause"),
], page=6, size=11)

# ---------- 7. ENGINE ----------
table_slide("Architecture", "The interview engine: built once, used twice", [
    ("interview-method", "The Mom Test, jobs-to-be-done and buying-signal knowledge base (hidden)"),
    ("run-interview", "Runs and captures one interview: discovery mode on Day 1, product-test mode on Day 4"),
    ("synthesise-interviews", "Pulls the patterns out of a folder of interview records"),
], note="Day 1 validates the problem. Day 4 tests the build. Same engine, one mode switch.", page=7, size=12.5)

# ---------- 8-12. DAYS ----------
table_slide("Day 1  ·  Monday", "Discovery", [
    ("d1-refine-idea", "Sharpen a raw idea into a testable problem and name the riskiest assumption"),
    ("d1-define-interviewees", "Decide the segment, the role and how many people to interview"),
    ("d1-build-list", "Turn the target into 20+ named, reachable people"),
    ("d1-write-outreach", "Messages that book interviews by asking for help, not selling"),
    ("d1-write-script", "A Mom Test-proof interview script and a how-to-run guide"),
    ("d1-validated-problem", "The persevere, pivot, or keep-interviewing call"),
], note="Outcome: 8 to 12 interviews synthesised, one validated problem, one named segment.", page=8, size=13)

table_slide("Day 2  ·  Tuesday", "Market & Proposition", [
    ("d2-market-map", "Name the players, the value chain and the substitutes"),
    ("d2-market-sizing", "Size TAM, SAM and SOM two ways and triangulate"),
    ("d2-competitor-scan", "Lay the rivals side by side and name the gap"),
    ("d2-positioning", "Fix where you win and state the one USP"),
    ("d2-proposition", "Turn jobs, pains and gains into one proposition, with a number"),
    ("d2-messaging", "A one-liner, three key messages and a 30-second pitch"),
    ("d2-brand-foundations", "Values, personality, naming and tone of voice"),
    ("d2-visual-identity", "A palette that passes contrast, two fonts and a simple logo"),
    ("d2-pitch-deck", "Assemble the day into a branded, evidence-traced pitch deck"),
], note="Outcome: a market map, market sizing, a proposition and USP, a brand, and a hand-out pitch deck.", page=9, size=11.5)

table_slide("Day 3  ·  Wednesday", "Product & Build", [
    ("d3-product-context", "Confirm your path and boil the MVP to one sentence"),
    ("d3-moscow", "Prioritise ruthlessly: at most 7 Musts, explicit Won'ts"),
    ("d3-story-map", "Sequence the Musts into one end-to-end slice"),
    ("d3-prd", "The build brief, with a numeric success metric"),
    ("d3-blueprint", "Model the structure once: data model or service blueprint"),
    ("d3-tech-stack", "One opinionated stack, with a monthly cost"),
    ("d3-github-setup", "A repo, a README and one issue per Must"),
    ("d3-mvp-build", "Build the thin slice live, one issue at a time"),
    ("d3-domain-email", "A real domain and a working business email"),
    ("d3-landing-site", "Your public shopfront with working lead capture"),
    ("d3-next-steps", "An honest, prioritised launch checklist"),
], note="Outcome: a working MVP live for a real prospect to act on, tracked in GitHub.", page=10, size=10.5)

table_slide("Day 4  ·  Thursday", "Test & Go-to-Market", [
    ("d4-usability-plan", "Reorient the interview engine and book 5 tests"),
    ("d4-prioritise", "Score the changes and rank testers by buying intent"),
    ("d4-icp-messaging", "Nail one ideal customer profile and the words that move them"),
    ("d4-sales-deck", "The deck that closes one named prospect"),
    ("d4-intake-process", "Proposal to delivery, with a signable template per stage"),
    ("d4-onboarding-pack", "Make a new client's first week feel handled"),
    ("d4-marketing-funnel", "Awareness to purchase, with named channels"),
    ("d4-gtm-plan", "Name the first 10 customers, ranked by warmth"),
    ("d4-book-sale", "Get the warmest prospect into a confirmed Friday slot"),
], note="Outcome: 5 usability tests, a sales deck, client processes, a funnel, a GTM plan, and a booked meeting.", page=11, size=11.5)

table_slide("Day 5  ·  Friday", "Tweaks & First Sale", [
    ("d5-triage", "Sort Day 4 feedback: Fix Now (max 3), Park, Roadmap"),
    ("d5-ship-fixes", "Ship the three fixes and prove the demo runs end to end"),
    ("d5-pricing-model", "Commit to one pricing model, with the reason written down"),
    ("d5-price-number", "Three packages, one recommended, floor £2,000"),
    ("d5-proposal", "A one-page offer: problem, target, price, next step"),
    ("d5-paperwork", "Draft engagement letter, terms, invoice and a way to get paid"),
    ("d5-rehearse", "Role-play the sale until the ask feels natural"),
    ("d5-close", "Turn the yes into a signature, recorded with a tier and amount"),
    ("d5-review", "Package the week and score it against your target"),
], note="Outcome: one committed yes (cash, deposit, paid pilot or signed LOI) with a date and an amount.", page=12, size=11.5)

# ---------- 13. THREE PATHS ----------
s = slide(); bg(s); header(s, "One plugin, three paths", "The build flexes to what you are making")
paths = [
    ("Software", "A deployed working slice on a public URL.", "Default stack: Next.js, Supabase, Vercel."),
    ("Hardware", "A prototype (CAD render or mock) plus a pre-order or waitlist page.", "Takes real payment intent."),
    ("Services", "A productised package with one sample deliverable.", "Plus a bookable intake page."),
]
cw3 = (CW - Inches(0.5) - Inches(0.6)) / 3
for i, (name, a, b) in enumerate(paths):
    x = MARGIN + Inches(0.5) + i * (cw3 + Inches(0.3))
    rect(s, x, Inches(2.15), cw3, Inches(2.9), PANEL, line=LINE)
    rect(s, x, Inches(2.15), cw3, Inches(0.7), INK)
    textbox(s, x, Inches(2.15), cw3, Inches(0.7),
            [{"text": name, "size": 19, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, x + Inches(0.25), Inches(3.05), cw3 - Inches(0.5), Inches(1.9), [
        {"text": a, "size": 14, "color": INK, "space_after": 8},
        {"text": b, "size": 13, "color": MUTED},
    ])
rect(s, MARGIN + Inches(0.5), Inches(5.5), CW - Inches(0.5), Inches(0.95), INK)
textbox(s, MARGIN + Inches(0.85), Inches(5.5), CW - Inches(1.2), Inches(0.95), [
    {"text": "The shared spine across all three:", "size": 13, "color": SPARK, "bold": True, "space_after": 3},
    {"text": "a live page a real prospect can act on. Skills that build or ship branch from one variance "
             "matrix, so the journey stays the same shape whatever you are making.", "size": 14, "color": WHITE},
], anchor=MSO_ANCHOR.MIDDLE)
footer(s, 13)

# ---------- 14. EFFICIENT & AUDITABLE ----------
s = slide(); bg(s); header(s, "By design", "Efficient to run, auditable to trust")
cols = [
    ("Built for a usage limit", [
        "Fresh session each day: state lives on disk, coach rebuilds it.",
        "Every skill logs once and reads compact state, not whole files.",
        "Scripts do the mechanical work in the background, not in tokens.",
        "Lean skills: bodies and triggers cut by a quarter to a half.",
    ]),
    ("Auditable by default", [
        "Every artefact is logged to a changelog with its numeric result.",
        "Decisions and their reasons are recorded as you go.",
        "audit-pack compiles it all into one regulator or investor pack.",
        "Human sign-off before any outreach is sent or money is spent.",
    ]),
]
cwx = (CW - Inches(0.5) - Inches(0.4)) / 2
for i, (title, items) in enumerate(cols):
    x = MARGIN + Inches(0.5) + i * (cwx + Inches(0.4))
    rect(s, x, Inches(2.1), cwx, Inches(4.3), PANEL, line=LINE)
    rect(s, x, Inches(2.1), cwx, Pt(4), SPARK)
    lines = [{"text": title, "size": 17, "color": INK, "bold": True, "space_after": 10}]
    for it in items:
        lines.append({"text": "•  " + it, "size": 13.5, "color": INK, "space_after": 8})
    textbox(s, x + Inches(0.3), Inches(2.4), cwx - Inches(0.6), Inches(3.8), lines)
footer(s, 14)

# ---------- 15. WHAT YOU WALK AWAY WITH ----------
s = slide(); bg(s); header(s, "By Friday", "What the founder walks away with")
items = [
    "A validated problem, backed by 8 to 12 real interviews",
    "A market map, market sizing and a hand-out pitch deck",
    "A brand: name, palette, logo and tone of voice",
    "A working MVP, live for a real prospect to act on",
    "A landing site, a sales deck and a go-to-market plan",
    "Client onboarding and intake processes, ready to use",
    "One paying customer, recorded with a date and an amount",
    "A full audit pack of everything built, and why",
]
half = (len(items) + 1) // 2
for col in range(2):
    x = MARGIN + Inches(0.5) + col * (CW / 2)
    chunk = items[col*half:(col+1)*half]
    lines = []
    for it in chunk:
        lines.append({"text": "✓   " + it, "size": 15, "color": INK, "bold": False, "space_after": 12})
    textbox(s, x, Inches(2.3), CW/2 - Inches(0.4), Inches(4), lines)
footer(s, 15)

# ---------- 16. CLOSING ----------
s = slide(); bg(s, INK)
rect(s, 0, 0, Inches(0.55), SH, SPARK)
textbox(s, MARGIN + Inches(0.4), Inches(2.4), CW, Inches(2), [
    {"text": "Idea to system, in five days.", "size": 40, "color": WHITE, "bold": True, "space_after": 10},
    {"text": "Install it, run doctor, then start. Coach takes it from there.", "size": 18, "color": RGBColor(0xC9,0xD4,0xDE)},
])
textbox(s, MARGIN + Inches(0.4), Inches(5.1), CW, Inches(1.4), [
    {"text": "Spark AI Agency", "size": 16, "color": SPARK, "bold": True, "space_after": 4},
    {"text": "seb@sparkcuriosityhq.com   ·   sparkconsulting.tech", "size": 14, "color": RGBColor(0xC9,0xD4,0xDE)},
])

import sys
out = sys.argv[1] if len(sys.argv) > 1 else "spark-bootcamp-overview.pptx"
prs.save(out)
print("Wrote", out, "with", len(prs.slides._sldIdLst), "slides")
