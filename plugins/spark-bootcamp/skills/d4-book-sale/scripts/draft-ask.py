#!/usr/bin/env python3
"""Draft the Friday-meeting ask and scaffold 04-gtm/friday-meeting.md.

Spark voice: British English, no em dashes. This script never sends anything
and never books anything. It drafts a message and writes a file for the
founder to review, sign off, and send themselves. Human in the loop.

Degrades gracefully: uses only the standard library. If run non-interactively
(no TTY), it prints the template with placeholders left in and still writes
the scaffold, so nothing crashes.
"""

import os
import sys
from datetime import date

CHANNELS = {
    "1": ("email", "finance, trust, law, accountancy, fund admin"),
    "2": ("linkedin", "professional services"),
    "3": ("text", "hospitality, construction, trades"),
}


def ask(prompt, fallback=""):
    """Prompt for input; return fallback if there is no interactive terminal."""
    if not sys.stdin.isatty():
        return fallback
    try:
        value = input(prompt).strip()
    except EOFError:
        return fallback
    return value or fallback


def build_message(channel, d):
    """Return the drafted ask for the chosen channel."""
    if channel == "email":
        return (
            f"Subject: 20 minutes on {d['pain']}?\n\n"
            f"Hi {d['first']},\n\n"
            f"{d['context']} I am {d['you']}, working on {d['prop']}.\n\n"
            f"I am talking to a handful of {d['role']}s this week about "
            f"{d['pain']}, and your view would genuinely help me get it right.\n\n"
            f"Could I borrow 20 minutes on Friday {d['fdate']}, either "
            f"{d['timeA']} or {d['timeB']}? Video or your office, whichever suits.\n\n"
            f"If the timing is wrong, no problem at all, just say and I will not chase.\n\n"
            f"Thanks,\n{d['you']}"
        )
    if channel == "linkedin":
        return (
            f"Hi {d['first']}, I am {d['you']}, working on {d['prop']}. "
            f"I am speaking to a few {d['role']}s this week about {d['pain']} and "
            f"would value 20 minutes of your thinking. Friday {d['fdate']}, "
            f"{d['timeA']} or {d['timeB']}? Happy to work around you. "
            f"If not, no worries at all."
        )
    return (
        f"Hi {d['first']}, {d['you']} here. Building something to fix {d['pain']} "
        f"for your kind of business. Could I grab 20 mins Friday, {d['timeA']} or "
        f"{d['timeB']}, to get your take? No sell, just questions. All good if not."
    )


def main():
    print("Book The Sale: draft the Friday ask.")
    print("This drafts a message only. You read it, then you send it. Nothing is sent for you.\n")

    print("Channel: 1) email  2) LinkedIn  3) text")
    ch_key = ask("Pick 1, 2 or 3 [1]: ", "1")
    channel, sector = CHANNELS.get(ch_key, CHANNELS["1"])

    d = {
        "first": ask("Prospect first name: ", "{first name}"),
        "role": ask("Their role (e.g. trust officer): ", "{their role}"),
        "firm": ask("Their firm: ", "{firm}"),
        "you": ask("Your name: ", "{your name}"),
        "prop": ask("Your one-line proposition: ", "{one-line proposition}"),
        "pain": ask("The one pain you remove for them: ", "{the pain}"),
        "context": ask("One line of context (how you know them / why them): ",
                       "{one line of context}"),
        "fdate": ask("Friday date (e.g. 17 July): ", "{date}"),
        "timeA": ask("First time offered (e.g. 10:00): ", "{time A}"),
        "timeB": ask("Fallback time (e.g. 14:00): ", "{time B}"),
    }

    message = build_message(channel, d)

    print("\n" + "=" * 60)
    print("DRAFT (read it out loud, cut anything that sounds like a pitch):")
    print("=" * 60)
    print(message)
    print("=" * 60)
    print("\nConfirmation line, send the moment they say yes:")
    print(f"Brilliant, thank you. Friday {d['fdate']} at {d['timeA']}, video or "
          f"office. I will send a calendar invite now so it is in your diary. "
          f"I will keep it to 20 minutes.")

    # Scaffold the artefact wherever the founder is working.
    out_dir = os.path.join(os.getcwd(), "04-gtm")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "friday-meeting.md")

    scaffold = (
        f"# Friday meeting\n\n"
        f"## Prospect\n"
        f"- Name: {d['first']}\n"
        f"- Role: {d['role']}\n"
        f"- Firm: {d['firm']}\n"
        f"- Channel: {channel}\n\n"
        f"## Times offered\n"
        f"- Friday {d['fdate']}, {d['timeA']} or {d['timeB']}, 20 minutes\n\n"
        f"## Message sent\n\n"
        f"```\n{message}\n```\n\n"
        f"## Reply\n"
        f"(paste their reply here)\n\n"
        f"## Confirmed slot\n"
        f"- Date: \n"
        f"- Time: \n"
        f"- Format: \n"
        f"- Calendar link: \n\n"
        f"Status: NOT YET CONFIRMED. Day 4 is done when this reads a specific "
        f"date and time, agreed in writing.\n"
    )

    if os.path.exists(out_path):
        print(f"\n{out_path} already exists. Not overwriting. Draft above, "
              f"copy in what you need.")
    else:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(scaffold)
        print(f"\nScaffold written: {out_path}")

    print("\nNext: send it yourself, then fill in the reply and confirmed slot.")


if __name__ == "__main__":
    main()
