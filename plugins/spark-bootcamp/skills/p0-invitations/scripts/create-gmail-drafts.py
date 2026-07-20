#!/usr/bin/env python3
"""Create Gmail drafts from the invitation pack. Drafts only, never sends.

Degrades gracefully: this environment exposes Gmail via MCP tools that this
script cannot call directly, so its job is to parse the pack into clean,
copy-ready message blocks and hand them back. If anything is missing it prints
a clear message and the raw text, and it never crashes.

Usage:
    python3 create-gmail-drafts.py 00-prework/invitation-pack.md
"""

import re
import sys
from pathlib import Path


def parse_messages(text):
    """Split the 'Personalised messages' section into per-contact blocks.

    Looks for level-3 headings (### Name) under a 'Personalised messages'
    heading. Returns a list of (heading, body) tuples. Best-effort only.
    """
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^#{1,6}\s+.*personalised messages", line, re.IGNORECASE):
            start = i + 1
            break
    if start is None:
        return []

    section = []
    for line in lines[start:]:
        # Stop at the next top-level section (## Something) that is not a contact.
        if re.match(r"^#{1,2}\s+\w", line) and "message" not in line.lower():
            break
        section.append(line)

    blocks = []
    current_head = None
    current_body = []
    for line in section:
        m = re.match(r"^#{3,6}\s+(.*)", line)
        if m:
            if current_head is not None:
                blocks.append((current_head, "\n".join(current_body).strip()))
            current_head = m.group(1).strip()
            current_body = []
        elif current_head is not None:
            current_body.append(line)
    if current_head is not None:
        blocks.append((current_head, "\n".join(current_body).strip()))
    return blocks


def main():
    if len(sys.argv) < 2:
        print("Give me the path to invitation-pack.md.")
        print("Usage: python3 create-gmail-drafts.py 00-prework/invitation-pack.md")
        return 0

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Could not find {path}. Run the invitations skill first to create it.")
        return 0

    text = path.read_text(encoding="utf-8", errors="replace")
    blocks = parse_messages(text)

    if not blocks:
        print("No personalised message blocks found under a 'Personalised messages'")
        print("heading. Here is the whole pack so you can copy it by hand:\n")
        print(text)
        return 0

    print(f"Found {len(blocks)} personalised messages in {path}.\n")
    print("This environment creates Gmail drafts through the connected Gmail tools,")
    print("not from this script. The clean blocks below are ready to paste, or ask")
    print("Claude to create a Gmail draft for each one. Nothing has been sent.\n")
    print("=" * 60)
    for i, (head, body) in enumerate(blocks, 1):
        print(f"\n[{i}] {head}\n{'-' * 40}\n{body}\n")
    print("=" * 60)
    print("\nReminder: drafts are not sent messages. You press send.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
