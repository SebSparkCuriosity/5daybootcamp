#!/usr/bin/env python3
"""Build the five Spark-branded facilitator decks for the bootcamp week.

One deck per bootcamp day, built from the timed session plan in
docs/session-plan.md against the real skill chain in
plugins/spark-bootcamp/skills/coach/references/journey-map.md. These are
Seb's own facilitator decks (teal cover, gold stat plates, Lighthouse mark),
not a founder's branded artefact, so they use the spark-branding skill's
deck engine rather than the plugin's generic house-style builder.

Usage:
    python3 build_day_decks.py [--out-dir docs/decks] [--skill-dir PATH]

--skill-dir points at the spark-branding skill's scripts/ folder (the one
holding spark_deck.py). It defaults to the SPARK_BRANDING_SKILL_DIR
environment variable, then a search of common Claude Code skill install
locations. Needs python-pptx (pip install python-pptx) plus Lora and Inter
installed for accurate layout measurement, same as any Spark deck.
"""
import argparse
import glob
import os
import sys

DEFAULT_SKILL_GLOBS = [
    os.path.expanduser("~/.claude/skills/synced/*/spark-branding/scripts"),
    os.path.expanduser("~/.claude/skills/spark-branding/scripts"),
    "/root/.claude/skills/synced/*/spark-branding/scripts",
]


def find_skill_dir():
    env = os.environ.get("SPARK_BRANDING_SKILL_DIR")
    if env and os.path.isdir(env):
        return env
    for pattern in DEFAULT_SKILL_GLOBS:
        matches = sorted(glob.glob(pattern))
        if matches:
            return matches[-1]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=os.path.join(os.path.dirname(__file__), "decks"))
    ap.add_argument("--skill-dir", default=None)
    args = ap.parse_args()

    skill_dir = args.skill_dir or find_skill_dir()
    if not skill_dir:
        sys.exit(
            "Could not find the spark-branding skill's scripts/ folder. "
            "Pass --skill-dir, or set SPARK_BRANDING_SKILL_DIR."
        )
    sys.path.insert(0, skill_dir)
    from spark_deck import SparkDeck  # noqa: E402

    os.makedirs(args.out_dir, exist_ok=True)

    SIGNATURE = (
        "Sebastian Lawson",
        "Spark AI Agency",
        ["seb@sparkcuriosityhq.com", "sparkconsulting.tech"],
    )

    for n, builder in enumerate(
        [build_day1, build_day2, build_day3, build_day4, build_day5], start=1
    ):
        d = SparkDeck(size="16x9")
        builder(d, SIGNATURE)
        path = os.path.join(args.out_dir, f"day-{n}.pptx")
        d.save(path)
        print(f"wrote {path}")


def schedule_section(d, rows):
    s = d.section("00", "Today's schedule", tone="light")
    s.table(["Time", "Block", "Skill(s)"], rows, widths=[0.18, 0.42, 0.40])
    return s


# ---------------------------------------------------------------------------
# Day 1: Idea and Discovery
# ---------------------------------------------------------------------------

def build_day1(d, signature):
    d.cover(
        eyebrow="Spark Bootcamp · Day 1",
        title="Day 1\nIdea and Discovery",
        deck="Develop the idea deep enough to test, then hold the interviews booked weeks ago.",
        stats=[("8–12", "Interviews booked"), ("6", "Sessions today"), ("09:00–17:30", "Runs today")],
        meta=["Facilitator deck · Spark AI Agency"],
        note="Internal use only",
    )

    schedule_section(d, [
        ["09:00–09:10", "Open", "Facilitator framing, coach on screen"],
        ["09:10–10:15", "Refine the idea", "d1-refine-idea"],
        ["10:15–10:30", "Break", "—"],
        ["10:30–11:15", "Plan the interviews", "d1-interview-plan"],
        ["11:15–12:00", "Write the script", "d1-write-script"],
        ["12:00–13:00", "Lunch + confirm today's slots", "—"],
        ["13:00–17:30", "Interviews, up to 8", "run-interview"],
    ])

    s = d.section("01", "Refine the idea", tone="light", deck="d1-refine-idea · idea-brief.md")
    s.para(
        "This afternoon's interviews test a bet, and the bet has to be genuinely "
        "yours. A brief you merely nodded at will not survive contact with a real "
        "customer; one you talked into existence will."
    )
    s.label("What we're after")
    s.bullets([
        "Where the idea came from",
        "What you believe, and the bet underneath it",
        "Whose problem it is, named",
        "One sentence: [product] helps [who] do [job] so they [get outcome]",
    ])
    s.quote("Ends with an idea brief written in your words, not Claude's.", attribution="d1-refine-idea")

    s = d.section("02", "Plan the interviews, write the script", tone="light")
    s.cards([
        ("Plan the interviews",
         "Ten minutes per booked name is what turns a diary of calls into a test "
         "of your riskiest assumption."),
        ("Write the script",
         "A question in your own voice survives a nervous first call; a perfect "
         "one in someone else's does not."),
    ], cols=2)
    s.panel(
        title="How the facilitator runs this",
        body="One question at a time, listen, reflect back, capture their phrases "
             "verbatim. Never write a line they haven't spoken to.",
        tone="gold",
    )

    s = d.section("03", "Interviews begin", tone="dark")
    s.numbered([
        ("Up to 8 in the room", "25-minute slots, 10 minutes between, capped by p0-schedule."),
        ("Overflow to Tuesday", "The ninth yes and beyond books Tuesday morning by default."),
        ("One record per session", "Each interview writes to 01-discovery/interviews/."),
    ])
    s.quote("The interviews matter more than the day.", attribution="p0-schedule")

    d.closing(
        title="Into Day 2",
        steps=[
            "Run every booked interview against the script",
            "Log each session under 01-discovery/interviews/",
            "Overflow past slot 8 books Tuesday morning",
        ],
        line="Tomorrow starts with synthesis, not a fresh idea.",
        signature=signature,
    )


# ---------------------------------------------------------------------------
# Day 2: Market and Proposition
# ---------------------------------------------------------------------------

def build_day2(d, signature):
    d.cover(
        eyebrow="Spark Bootcamp · Day 2",
        title="Day 2\nMarket and Proposition",
        deck="Size the market, sharpen the proposition, hand out a pitch deck.",
        stats=[("11", "Skills today"), ("12", "Pitch deck slides"), ("09:00–17:00", "Runs today")],
        meta=["Facilitator deck · Spark AI Agency"],
        note="Internal use only",
    )

    schedule_section(d, [
        ["09:00–09:35", "Overflow interviews", "run-interview"],
        ["09:35–10:15", "Synthesise", "synthesise-interviews"],
        ["10:15–10:30", "Break", "—"],
        ["10:30–10:50", "Validate the problem, close Day 1", "d1-validated-problem"],
        ["10:50–11:20", "Market research", "d2-market-map, -sizing, -competitor-scan"],
        ["11:20–12:30", "Position and propose", "d2-positioning, d2-proposition"],
        ["12:30–13:30", "Lunch", "—"],
        ["13:30–13:40", "Messaging", "d2-messaging"],
        ["13:40–14:15", "Brand foundations", "d2-brand-foundations"],
        ["14:15–15:00", "Visual identity", "d2-visual-identity, brand-register"],
        ["15:00–15:15", "Break", "—"],
        ["15:15–15:55", "Brand book, pitch deck", "d2-brand-book, d2-pitch-deck"],
        ["15:55–17:00", "Pitch lightning round", "group share"],
    ])

    s = d.section("01", "Close Day 1 first", tone="light")
    s.label("Before market work starts")
    s.numbered([
        ("Overflow interviews", "Anyone who booked Tuesday morning runs first."),
        ("Synthesise", "synthesise-interviews turns the raw calls into discovery-findings.md."),
        ("Call the verdict", "d1-validated-problem forces persevere, pivot, or insufficient evidence."),
    ])
    s.quote(
        "This is the week's biggest decision: everything after Day 1 points at "
        "whatever you lock here.",
        attribution="d1-validated-problem",
    )

    s = d.section("02", "Market research", tone="light")
    s.cards([
        ("Market map", "Draw the board first: segments, value chain, named incumbents, substitutes."),
        ("Market sizing", "TAM, SAM, SOM, worked two independent ways and checked against each other."),
        ("Competitor scan", "Six or more real rivals, scored, ending on the sentence naming the gap you own."),
    ], cols=3)
    s.panel(
        title="TAM / SAM / SOM",
        body="Top-down flatters you, bottom-up keeps you honest. The gap between "
             "the two methods is the assumption you haven't thought through.",
        tone="cream",
    )

    s = d.section("03", "Position and propose", tone="light")
    s.heading("Positioning")
    s.para(
        "Positioning is the one decision that makes every later decision easier: "
        "it tells Day 3 what to build, Day 4 what to say, and Day 5 why a "
        "prospect pays you and not the incumbent."
    )
    s.label("The output")
    s.bullets([
        "A Geoffrey Moore positioning statement",
        "A 2x2 map with rivals plotted",
        "One USP under 20 words no rival can honestly claim",
    ])
    s.heading("Proposition")
    s.para(
        "A proposition is a promise you can prove: get it right and Day 3 knows "
        "what to build and Friday's pricing has a number to anchor to."
    )

    s = d.section("04", "Messaging", tone="light")
    s.quote("People buy the sentence they can repeat to someone else.", attribution="d2-messaging")
    s.bullets(["One line", "Three proof-backed messages", "A 30-second pitch"])

    s = d.section("05", "Brand foundations and visual identity", tone="light")
    s.cards([
        ("Brand foundations",
         "Decide once how you sound and what you stand for, and every email, "
         "page and pitch downstream sounds like the same firm."),
        ("Visual identity",
         "Three genuinely different logo concepts, one font pairing, a "
         "five-colour AA-safe palette, chosen by you in under an hour."),
    ], cols=2)
    s.panel(
        title="Brand book and pitch deck",
        body="A brand that lives in one founder's head dies at the first "
             "freelancer. The brand book is the handover; the pitch deck is "
             "tonight's homework.",
        tone="gold",
    )

    s = d.section("06", "Pitch lightning round", tone="dark")
    s.grid([
        "2 minutes, one slide, no notes.",
        "A stranger in the audience should follow the whole story.",
        "Feedback from the room, then move on.",
        "Every founder presents, no exceptions.",
    ], cols=2)

    d.closing(
        title="Into Day 3",
        steps=[
            "Ship the pitch deck to every founder tonight",
            "Sleep on the proposition before Wednesday",
            "Bring the brand board, Day 3 builds against it",
        ],
        line="A deck forces the week into one honest picture.",
        signature=signature,
    )


# ---------------------------------------------------------------------------
# Day 3: Product and Build
# ---------------------------------------------------------------------------

def build_day3(d, signature):
    d.cover(
        eyebrow="Spark Bootcamp · Day 3",
        title="Day 3\nProduct and Build",
        deck="Ship the smallest slice a real prospect can act on.",
        stats=[("3", "Business paths"), ("7", "Musts, capped"), ("13:30–16:30", "Build sprint")],
        meta=["Facilitator deck · Spark AI Agency"],
        note="Internal use only",
    )

    schedule_section(d, [
        ["09:00–09:15", "Product context", "d3-product-context"],
        ["09:15–10:15", "Prioritise and map", "d3-moscow, d3-story-map"],
        ["10:15–10:30", "Break", "—"],
        ["10:30–11:30", "Draft the technical trio", "d3-prd, d3-blueprint, d3-tech-stack"],
        ["11:30–12:30", "Explain-back, repo setup", "d3-github-setup"],
        ["12:30–13:30", "Lunch", "—"],
        ["13:30–16:30", "Build sprint", "d3-mvp-build"],
        ["16:30–16:50", "Domain, email, landing page", "d3-domain-email, d3-landing-site"],
        ["16:50–17:00", "Next steps, close Day 3", "d3-next-steps"],
    ])

    s = d.section("01", "Scope it down", tone="light")
    s.cards([
        ("MoSCoW",
         "Overscoping is the biggest reason a five-day build never ships. "
         "Musts, capped at seven."),
        ("Story map",
         "A MoSCoW list says what to build, not the order or the finish line. "
         "The map draws one line through it as the MVP slice."),
    ], cols=2)

    s = d.section("02", "The technical trio", tone="light")
    s.label("Claude drafts, you correct")
    s.para(
        "PRD, blueprint and tech stack move fast because this is a "
        "draft-then-explain skill: Claude drafts, then walks it through in "
        "plain English and asks you to poke holes with your domain knowledge. "
        "Your corrections reshape the draft."
    )
    s.numbered([
        ("PRD", "A single build brief Claude Code can build from without guessing."),
        ("Blueprint", "Diagrams: what it stores, how it fits together, what it is made of."),
        ("Tech stack", "One chosen stack, a monthly cost, the accounts to open, the MCP servers to connect."),
    ])
    s.quote("Done when the founder could retell the document to a friend.", attribution="Spark house style")

    s = d.section("03", "What ships by 16:30", tone="light")
    s.label("The build sprint, by path")
    s.cards([
        ("Software", "A deployed working slice on a public URL."),
        ("Hardware", "A demonstrable prototype (CAD render or physical mock) plus a pre-order or waitlist page taking real payment intent."),
        ("Services", "A productised service package (one sample deliverable) plus a bookable intake page."),
    ], cols=3)
    s.panel(
        title="The shared spine",
        body="A live page a real prospect can act on. That's true whatever you're building.",
        tone="cream",
    )

    s = d.section("04", "Handoff: build sprint", tone="dark")
    s.numbered([
        ("13:30", "Facilitator circulates 1:1, no group session."),
        ("16:30", "Domain, email, landing page go live."),
        ("16:50", "Next-steps list ranks the top 3 blockers."),
    ])
    s.quote(
        "This is the day the idea stops being a document and becomes a thing "
        "one real person can act on.",
        attribution="d3-mvp-build",
    )

    d.closing(
        title="Into Day 4",
        steps=[
            "Confirm the live URL, prototype or sample actually works end to end",
            "Book real users for tomorrow's usability tests",
            "Three blockers only, everything else waits",
        ],
        line="A ranked list with the three real blockers named is the difference between shipping and drifting.",
        signature=signature,
    )


# ---------------------------------------------------------------------------
# Day 4: Test and Go to Market
# ---------------------------------------------------------------------------

def build_day4(d, signature):
    d.cover(
        eyebrow="Spark Bootcamp · Day 4",
        title="Day 4\nTest and Go to Market",
        deck="Test the build for buying signals, then build the machine that sells it.",
        stats=[("5", "Usability sessions"), ("10", "GTM prospects ranked"), ("16:25", "Book Friday")],
        meta=["Facilitator deck · Spark AI Agency"],
        note="Internal use only",
    )

    schedule_section(d, [
        ["09:00–09:15", "Usability test plan", "d4-usability-plan"],
        ["09:15–12:30", "Usability tests", "live, real users"],
        ["12:30–13:30", "Lunch", "—"],
        ["13:30–14:00", "Synthesise feedback", "d4-prioritise"],
        ["14:00–14:45", "Messaging and pricing", "d4-icp-messaging, d4-pricing-model"],
        ["14:45–15:00", "Break", "—"],
        ["15:15–16:00", "Sales machine", "d4-sales-deck, intake, onboarding, funnel"],
        ["16:00–16:25", "GTM plan", "d4-gtm-plan"],
        ["16:25–16:45", "Book the Friday meeting", "d4-book-sale"],
        ["16:45–17:00", "Roll call, close Day 4", "—"],
    ])

    s = d.section("01", "Usability, not bug hunting", tone="light")
    s.para(
        "You now have a thing, so the question changes from 'is the pain real?' "
        "to 'does my build remove it, and is that worth money?' Watching five "
        "people fumble it teaches you more than fifty surveys."
    )
    s.label("What we're watching for")
    s.bullets([
        "Real tasks on the live URL, not a demo you drive",
        "Three probes reading whether they would actually pay",
        "Five sessions, booked ahead",
    ])

    s = d.section("02", "Triage the feedback", tone="light")
    s.quote(
        "By Friday you can build three things not thirty and phone a handful "
        "of people, so numbers decide, not the loudest voice.",
        attribution="d4-prioritise",
    )
    s.bullets([
        "Score every requested change with RICE and MoSCoW",
        "Rank every tester by likelihood to buy",
    ])

    s = d.section("03", "Messaging and pricing", tone="light")
    s.cards([
        ("ICP and messaging",
         "On Friday you reach only a handful of people and say roughly the "
         "same thing to each, so fuzzy targeting costs you half of them."),
        ("Pricing model",
         "How you charge decides who buys and how fast they say yes. The "
         "model and floor get fixed now; the exact number is Friday's first job."),
    ], cols=2)

    s = d.section("04", "The sales machine", tone="light")
    s.grid([
        "Sales deck: a prospect who hears their own words read back is a prospect who signs.",
        "Intake process: most first sales die in the gap between the nod and the kickoff.",
        "Onboarding pack: a first week that feels handled is the cheapest retention you will ever buy.",
        "Marketing funnel: how many arrive, and how many carry on.",
    ], cols=2)

    s = d.section("05", "GTM plan", tone="light")
    s.quote(
        "The warmest prospect closes far faster than a cold one, so you start "
        "there, not at the top of an alphabet.",
        attribution="d4-gtm-plan",
    )

    s = d.section("06", "The gate: book the Friday meeting", tone="dark")
    s.numbered([
        ("Right person", "Not just any contact, the warmest one from today's ranking."),
        ("Specific time", "A slot on the table, not 'sometime Friday.'"),
        ("A reply that says yes", "Confirmed before anyone leaves the room."),
    ])
    s.quote(
        "Regulated buyers rarely take a same-day meeting, so you ask on "
        "Thursday for Friday with a time already on the table.",
        attribution="d4-book-sale",
    )
    s.panel(
        title="Nobody leaves without it",
        body="Roll call at 16:45: read every name and their booked time out loud.",
    )

    d.closing(
        title="Into Day 5",
        steps=[
            "Confirm your Friday meeting time and channel",
            "Rehearse the price out loud tonight",
            "Bring your three-item fix list, not a feature wishlist",
        ],
        line="On Day 5 you have hours and one job: get a real prospect to act on your live page.",
        signature=signature,
    )


# ---------------------------------------------------------------------------
# Day 5: Tweaks and First Sale
# ---------------------------------------------------------------------------

def build_day5(d, signature):
    d.cover(
        eyebrow="Spark Bootcamp · Day 5",
        title="Day 5\nTweaks and First Sale",
        deck="Hit the headline number, a real customer commits.",
        stats=[("3", "Fixes, ruthlessly"), ("3", "Price tiers"), ("13:45–16:00", "Sale meetings")],
        meta=["Facilitator deck · Spark AI Agency"],
        note="Internal use only",
    )

    schedule_section(d, [
        ["09:00–09:20", "Triage yesterday's feedback", "d5-triage"],
        ["09:20–10:30", "Ship the fixes", "d5-ship-fixes"],
        ["10:30–10:45", "Break", "—"],
        ["10:45–11:10", "Set the price", "d5-price-number"],
        ["11:10–11:35", "Draft the proposal", "d5-proposal"],
        ["11:35–12:30", "Paperwork", "d5-paperwork"],
        ["12:30–13:15", "Lunch, early", "—"],
        ["13:15–13:45", "Rehearse in pairs", "d5-rehearse"],
        ["13:45–16:00", "Sale meetings, staggered", "live, off the plugin"],
        ["16:00–16:20", "Log the outcome", "d5-close"],
        ["16:20–16:50", "Compile the launch package", "d5-review"],
        ["16:50–17:00", "Demo day: state your number", "group close"],
    ])

    s = d.section("01", "Triage and ship", tone="light")
    s.quote(
        "On Day 5 you have hours and one job: get a real prospect to act on "
        "your live page, so fixing everything means shipping nothing.",
        attribution="d5-triage",
    )
    s.para(
        "Friday is not for new features: it is for making one clean route "
        "work so a real person can watch it and believe it."
    )
    s.numbered([
        ("Triage", "A ruthless three-item fix list, everything else parked or roadmapped."),
        ("Ship", "Build the three fixes, run the demo once end to end, commit with a timestamp."),
    ])

    s = d.section("02", "Set the price", tone="light")
    s.quote(
        "Founders freeze on price, and a buyer decides in seconds whether it "
        "feels fair, so we anchor on value and engineer the middle package to win.",
        attribution="d5-price-number",
    )
    s.bullets([
        "Three named packages: good, better, best",
        "One recommended",
        "Every price tied to a value assumption you can defend out loud",
    ])

    s = d.section("03", "Proposal and paperwork", tone="light")
    s.cards([
        ("Proposal",
         "One page a named buyer can say yes to: their problem, one numeric "
         "target, a delivery window inside six weeks, one price, one next step."),
        ("Paperwork",
         "An engagement letter, terms, an invoice from the correct trading "
         "entity, and a payment method that clears today. Drafts only."),
    ], cols=2)
    s.panel(
        title="Have a qualified lawyer review this before use",
        body="Every legal and data-protection output in the plugin is a draft. Spark does not warrant them.",
        tone="cream",
    )

    s = d.section("04", "Rehearse", tone="light")
    s.quote(
        "The sale is won by naming the price without flinching and answering "
        "'it's too expensive' without apologising.",
        attribution="d5-rehearse",
    )
    s.bullets([
        "A full sales role-play",
        "8+ objections drilled",
        "Say the price out loud until it stops wobbling",
    ])

    s = d.section("05", "Sale meetings", tone="dark")
    s.para(
        "Each founder's Friday meeting was booked individually on Day 4. The "
        "room runs as a window, not a block everyone shares."
    )
    s.label("13:45–16:00")

    s = d.section("06", "Close and review", tone="light")
    s.quote(
        "A week of work is worth nothing until someone commits, and most "
        "deals die in the last ten minutes because the founder never actually asks.",
        attribution="d5-close",
    )
    s.bullets([
        "Record the outcome at whichever tier lands: cash, deposit, signed paid pilot, or signed LOI",
        "Compile LAUNCH-PACKAGE.md: every headline number, target versus achieved",
    ])

    d.closing(
        title="Demo day",
        steps=[
            "State your number, whatever it is",
            "One honest link: MVP, pitch deck, sales deck, live page, launch checklist",
            "Decide together what Monday looks like",
        ],
        line="By Friday your week is scattered across five folders; this gives one honest link.",
        signature=signature,
    )


if __name__ == "__main__":
    main()
