#!/usr/bin/env python3
"""Scaffold the two Day 1 interview files from their templates.

Writes:
  01-discovery/interview-script.md   (the discovery script)
  01-discovery/how-to-run.md         (how to run the call)

Both come from the templates in ../references/. The founder then fills the
slots and tests every question against the Mom Test.

It never crashes and never overwrites work:
  - If a target file already exists, it is left untouched and reported, so a
    second run cannot wipe questions you have already written.
  - If a template cannot be read, it writes a minimal built-in fallback for
    that file, warns which one, and carries on with the other.

Usage:
  scaffold.py --root .
  scaffold.py --root /path/to/project --force   # overwrite existing files
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REFS = os.path.normpath(os.path.join(HERE, "..", "references"))

# (template filename in references/, output path relative to project root)
FILES = [
    ("interview-script-template.md", "01-discovery/interview-script.md"),
    ("how-to-run-template.md", "01-discovery/how-to-run.md"),
]

# Minimal fallbacks, used only if a template will not load. The method still
# survives in one line so the founder is never left with a blank file.
FALLBACK = {
    "01-discovery/interview-script.md": (
        "# Discovery Interview Script\n\n"
        "Template could not be read, so this is a bare fallback. Write eight or\n"
        "more questions, every one about the past or their current behaviour,\n"
        "never a hypothetical. The one rule: opinions are worthless, facts about\n"
        "the past are gold. Ask only questions that cannot be flattered.\n\n"
        "1. Walk me through how you handle [the job] today, start to finish.\n"
        "2. Tell me about the last time [the problem] came up. What did you do?\n"
        "3. How long did that take, and what did it cost you?\n"
        "4. What are you using to deal with this today, and what does it cost?\n"
        "5. Have you tried to fix this before? What happened?\n"
        "6. Who else touches this decision or feels this problem?\n"
        "7. [Aim this one at your riskiest assumption, in the past tense.]\n"
        "8. [A second one at the assumption, from another angle.]\n\n"
        "Close: who else should I speak to, and may I come back to you?\n"
    ),
    "01-discovery/how-to-run.md": (
        "# How To Run A Discovery Call\n\n"
        "Template could not be read, so this is a bare fallback.\n\n"
        "Open: thank them, name the time, ask consent to record, say you are\n"
        "not selling. Avoid pitching: keep your idea in your pocket; turn\n"
        "\"what are you building?\" back to them. Record and transcribe: pick ONE\n"
        "default method (meeting-platform recording and auto-transcript for\n"
        "online calls, phone voice memo plus a transcription tool for in person),\n"
        "then paste the transcript into run-interview. Close: ask who else to\n"
        "speak to, and whether you can come back.\n"
    ),
}


def read_template(name):
    path = os.path.join(REFS, name)
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def main():
    ap = argparse.ArgumentParser(description="Scaffold the Day 1 interview files.")
    ap.add_argument("--root", default=".", help="Project root (default: current directory)")
    ap.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    out_dir = os.path.join(root, "01-discovery")
    os.makedirs(out_dir, exist_ok=True)

    wrote, skipped = [], []
    for template_name, rel_out in FILES:
        out_path = os.path.join(root, rel_out)
        if os.path.exists(out_path) and not args.force:
            skipped.append(rel_out)
            continue
        try:
            content = read_template(template_name)
        except Exception as exc:
            content = FALLBACK[rel_out]
            sys.stderr.write(
                "Could not read template %s (%s). Wrote a minimal fallback for %s.\n"
                % (template_name, exc, rel_out)
            )
        try:
            with open(out_path, "w", encoding="utf-8") as fh:
                fh.write(content)
            wrote.append(rel_out)
        except Exception as exc:
            sys.stderr.write("Could not write %s (%s).\n" % (rel_out, exc))

    if wrote:
        print("Wrote:")
        for p in wrote:
            print("  " + p)
    if skipped:
        print("Left untouched (already exist, use --force to overwrite):")
        for p in skipped:
            print("  " + p)
    print("\nNext: fill the slots, test every question against the Mom Test,")
    print("and choose one recording method in how-to-run.md.")


if __name__ == "__main__":
    main()
