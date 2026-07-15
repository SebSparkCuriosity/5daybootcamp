#!/usr/bin/env python3
"""Set up a GitHub repo for the Day 3 build.

Two modes:
  --check   Verify gh is installed and authenticated. Prints "ready" or a fix.
  --create  Create the repo, push a five-line README, open one issue per Must.

Reads (from the founder's project, cwd):
  03-product/requirements-moscow.md  (the Must list)
  03-product/tech-stack.md           (one-line description)
  .spark/state.json                  (founder, idea, business_type)

Writes:
  03-product/README.draft.md   (a copy of the README, so you keep it even if
                                gh fails and you fall back to the browser)
  03-product/github.md         (the audit record: URL, issue count, issue list)

Degrades gracefully: no third-party libraries, only the standard library and
the gh CLI. If gh is missing it explains exactly what to do and never crashes.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date

PROJECT = os.getcwd()
MOSCOW = os.path.join(PROJECT, "03-product", "requirements-moscow.md")
TECH = os.path.join(PROJECT, "03-product", "tech-stack.md")
STATE = os.path.join(PROJECT, ".spark", "state.json")
README_DRAFT = os.path.join(PROJECT, "03-product", "README.draft.md")
GITHUB_MD = os.path.join(PROJECT, "03-product", "github.md")


def run(cmd, capture=True):
    """Run a command, return (returncode, stdout, stderr). Never raises."""
    try:
        p = subprocess.run(
            cmd, capture_output=capture, text=True, timeout=120
        )
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except FileNotFoundError:
        return 127, "", f"{cmd[0]} not found"
    except subprocess.TimeoutExpired:
        return 124, "", "timed out"


def gh_installed():
    code, _, _ = run(["gh", "--version"])
    return code == 0


def gh_authed():
    code, _, _ = run(["gh", "auth", "status"])
    return code == 0


def load_state():
    try:
        with open(STATE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def read_musts(path=MOSCOW):
    """Pull every non-empty line under a 'Must' heading until the next heading.

    Tolerant: matches '## Must', '### Must have', 'Must-have', case-insensitive.
    Strips list markers and checkbox syntax so titles come out clean.
    """
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    musts, capturing = [], False
    heading = re.compile(r"^\s{0,3}#{1,6}\s")
    must_head = re.compile(r"^\s{0,3}#{1,6}\s*.*must", re.IGNORECASE)
    other_moscow = re.compile(
        r"^\s{0,3}#{1,6}\s*.*(should|could|won'?t|wont)", re.IGNORECASE
    )
    for line in lines:
        if must_head.match(line):
            capturing = True
            continue
        if capturing and (other_moscow.match(line) or heading.match(line)):
            break
        if capturing:
            text = line.strip()
            if not text:
                continue
            text = re.sub(r"^[-*+]\s+", "", text)
            text = re.sub(r"^\[[ xX]\]\s+", "", text)
            text = re.sub(r"^\d+[.)]\s+", "", text)
            if text:
                musts.append(text)
    return musts


def suggest_repo_name(state):
    idea = (state.get("idea") or state.get("founder") or "spark-build").lower()
    name = re.sub(r"[^a-z0-9]+", "-", idea).strip("-")
    words = name.split("-")
    return "-".join(words[:4]) or "spark-build"


def stack_line(state):
    bt = state.get("business_type", "software")
    if bt == "hardware":
        return "Docs, CAD and pre-order page."
    if bt == "services":
        return "Sample deliverable and intake page."
    # software default
    if os.path.exists(TECH):
        with open(TECH, encoding="utf-8") as f:
            head = f.read(400)
        m = re.search(r"(Next\.js|Supabase|Vercel|React|Python|Node)", head)
        if m:
            return "Stack: Next.js, Supabase, Vercel (see tech-stack.md)."
    return "Stack: Next.js, Supabase, Vercel."


def build_readme(state, repo_name):
    idea = state.get("idea", "A Day 3 build.")
    musts = read_musts()
    outcome = musts[0] if musts else "the one Must-have outcome"
    lines = [
        f"# {repo_name}",
        "",
        idea if idea.endswith(".") else idea + ".",
        f"For: the segment named in 01-discovery.",
        f"One Must-have outcome: {outcome}",
        stack_line(state),
        "Status: Day 3 build, in progress.",
    ]
    return "\n".join(lines) + "\n"


def do_check():
    if not gh_installed():
        print("FAIL: gh not installed.")
        print("Fix: see references/github-auth-walkthrough.md (step 1).")
        return 1
    if not gh_authed():
        print("FAIL: gh not authenticated.")
        print("Fix: run  gh auth login  (see the walkthrough), then re-check.")
        return 1
    code, out, _ = run(["gh", "api", "user", "--jq", ".login"])
    who = out if code == 0 else "unknown"
    print(f"ready: gh installed and authenticated as {who}.")
    return 0


def write_audit(repo_url, issues):
    os.makedirs(os.path.dirname(GITHUB_MD), exist_ok=True)
    with open(GITHUB_MD, "w", encoding="utf-8") as f:
        f.write("# GitHub repository\n\n")
        f.write(f"Repo: {repo_url}\n\n")
        f.write(f"Open Must issues: {len(issues)}\n\n")
        for num, title, url in issues:
            f.write(f"- #{num} {title} ({url})\n")
        f.write(f"\nRecorded {date.today().isoformat()}.\n")


def do_create():
    state = load_state()
    musts = read_musts()
    if not musts:
        print("FAIL: no Musts found in 03-product/requirements-moscow.md.")
        print("Fix the MoSCoW file (needs a Must heading with items), retry.")
        return 1

    suggested = suggest_repo_name(state)
    repo_name = input(f"Repo name [{suggested}]: ").strip() or suggested

    readme = build_readme(state, repo_name)
    os.makedirs(os.path.dirname(README_DRAFT), exist_ok=True)
    with open(README_DRAFT, "w", encoding="utf-8") as f:
        f.write(readme)
    print(f"\nDrafted README (saved to {README_DRAFT}):\n")
    print(readme)
    print(f"Found {len(musts)} Musts. That is {len(musts)} issues to open.\n")

    if not gh_installed() or not gh_authed():
        print("gh is not ready, so I cannot create the repo automatically.")
        print("Fall back to the browser: create the repo at github.com/new,")
        print("paste the README above, and open these issues by hand:")
        for m in musts:
            print(f"  - {m}")
        print("\nThen write 03-product/github.md with the URL and this list.")
        return 2

    if input("Create the repo now? [y/N]: ").strip().lower() != "y":
        print("Stopped. Nothing created.")
        return 0

    # Write README to disk in a temp build dir and create repo from it.
    code, login, _ = run(["gh", "api", "user", "--jq", ".login"])
    if code != 0:
        print("FAIL: could not read your GitHub login.")
        return 1

    # Create the repo (private by default), then push the README.
    code, out, err = run([
        "gh", "repo", "create", repo_name,
        "--private", "--description", state.get("idea", "Day 3 build")[:200],
    ])
    if code != 0:
        print(f"FAIL: repo not created. {err}")
        return 1
    repo_url = f"https://github.com/{login}/{repo_name}"
    print(f"Repo created: {repo_url}")

    # Push README via the contents API (no local git clone needed).
    import base64
    content = base64.b64encode(readme.encode("utf-8")).decode("ascii")
    code, _, err = run([
        "gh", "api", f"repos/{login}/{repo_name}/contents/README.md",
        "-X", "PUT", "-f", "message=Add README (Day 3)",
        "-f", f"content={content}",
    ])
    if code != 0:
        print(f"WARN: README not pushed via API. {err}")
        print(f"Paste it manually from {README_DRAFT}.")

    # Open one issue per Must.
    issues = []
    for m in musts:
        title = m if len(m) <= 80 else m[:77] + "..."
        code, out, err = run([
            "gh", "issue", "create", "--repo", f"{login}/{repo_name}",
            "--title", title, "--body", f"Must-have from MoSCoW: {m}",
        ])
        if code == 0 and out:
            url = out.splitlines()[-1]
            num = url.rstrip("/").split("/")[-1]
            issues.append((num, title, url))
            print(f"  issue #{num}: {title}")
        else:
            print(f"  WARN: issue not created for: {title} ({err})")

    write_audit(repo_url, issues)

    # Verify the done-condition.
    reachable = run(["gh", "repo", "view", f"{login}/{repo_name}",
                     "--json", "name"])[0] == 0
    readme_ok = run(["gh", "api",
                     f"repos/{login}/{repo_name}/contents/README.md"])[0] == 0
    count_ok = len(issues) == len(musts)
    print("\n----")
    print(f"repo reachable: {'yes' if reachable else 'no'}")
    print(f"README present: {'yes' if readme_ok else 'no'}")
    print(f"issues opened: {len(issues)} of {len(musts)} Musts")
    verdict = "PASS" if (reachable and readme_ok and count_ok) else "FAIL"
    print(f"RESULT: {verdict}")
    print(f"Audit record written to {GITHUB_MD}")
    return 0 if verdict == "PASS" else 1


def main():
    ap = argparse.ArgumentParser(description="Set up a GitHub repo for Day 3.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true",
                   help="verify gh is installed and authenticated")
    g.add_argument("--create", action="store_true",
                   help="create the repo, README and Must issues")
    args = ap.parse_args()
    if args.check:
        sys.exit(do_check())
    sys.exit(do_create())


if __name__ == "__main__":
    main()
