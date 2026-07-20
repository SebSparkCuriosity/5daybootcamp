#!/usr/bin/env python3
"""Lint the spark-bootcamp plugin for broken cross-skill contracts.

Every skill is a node in a pipeline: it consumes artefacts other skills
produce, calls scripts and references by path, and names other skills. All of
that is mechanically checkable, so this linter checks it. Run from the repo
root:

    python3 tools/lint_plugin.py

Exit 0 when clean. Exit 1 on any FAIL. CI runs this on every push.

What it checks:
  1. Artefact contracts. Paths a SKILL.md consumes (outside its own
     "The artefact" section) must be produced somewhere: by a skill's
     artefact section, by the coach's routing tables, or by a known
     infrastructure path. A consumed path nobody produces is a ghost.
  2. Plugin file references. Every ${CLAUDE_SKILL_DIR}/... and
     ${CLAUDE_PLUGIN_ROOT}/skills/... reference must exist on disk.
  3. Skill id references. Every /spark-bootcamp:<id> and backticked
     p0-*/d[1-5]-* token must be a real skill folder.
  4. Routing. Every skill id in coach-route.py's tables must exist.
  5. Voice. No em dashes anywhere in a SKILL.md or reference.
  6. Frontmatter. name and description present; description length warned
     over 200 characters.
  7. Body length. Warn (not fail) when a SKILL.md body exceeds 60 lines.
"""

import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(REPO, "plugins", "spark-bootcamp", "skills")
COACH_ROUTE = os.path.join(SKILLS_DIR, "coach", "scripts", "coach-route.py")

# Paths that infrastructure (doctor, start, helpers) creates rather than a
# day skill's artefact section. Consumed references to these are fine.
INFRA_PATHS = {
    "CHANGELOG.md", "DECISIONS.md",
    ".spark/state.json", ".spark/prework.md", ".spark/doctor-report.txt",
    ".spark/brand/brand.json", ".spark/brand/logo.svg", ".spark/brand/",
    ".spark/deliverables/",
}
INFRA_DIR_PREFIXES = (".spark/deliverables/",)

# A consumed path token looks like a founder-project path.
PATH_RE = re.compile(
    r"(?:^|[\s`(\"'])((?:0[0-5]-[a-z]+|\.spark)/[A-Za-z0-9_./\-]*[A-Za-z0-9_/\-])",
)
SKILL_FILE_RE = re.compile(
    r"\$\{CLAUDE_SKILL_DIR\}/([A-Za-z0-9_./\-]+)")
PLUGIN_FILE_RE = re.compile(
    r"\$\{CLAUDE_PLUGIN_ROOT\}/skills/([A-Za-z0-9_./\-]+)")
CMD_ID_RE = re.compile(r"/spark-bootcamp:([a-z0-9\-]+)")
TICKED_ID_RE = re.compile(r"`((?:p0|d[1-5])-[a-z][a-z\-]+)`")


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def sections(text):
    """Split a SKILL.md into (heading, body) pairs; frontmatter under ''."""
    parts, current, buf = [], "", []
    for line in text.splitlines():
        if line.startswith("## "):
            parts.append((current, "\n".join(buf)))
            current, buf = line[3:].strip().lower(), []
        else:
            buf.append(line)
    parts.append((current, "\n".join(buf)))
    return parts


def clean_token(tok):
    tok = tok.rstrip(".,;:)`'\"")
    return tok


def path_tokens(text):
    out = set()
    for m in PATH_RE.finditer(text):
        tok = clean_token(m.group(1))
        if any(c in tok for c in "<>*[{$"):
            continue
        out.add(tok)
    return out


def is_dirlike(tok):
    last = tok.rstrip("/").rsplit("/", 1)[-1]
    return tok.endswith("/") or "." not in last


def main():
    fails, warns = [], []

    skill_ids = sorted(
        d for d in os.listdir(SKILLS_DIR)
        if os.path.isdir(os.path.join(SKILLS_DIR, d)))

    # ---- Gather routing tables from coach-route.py -------------------------
    route_text = read(COACH_ROUTE)
    routed = [(sid, art) for sid, art in
              re.findall(r'\("([a-z0-9\-]+)",\s*"([^"]+)"\)', route_text)
              if "/" in art or "." in art]
    routed_ids = {sid for sid, _ in routed}
    produced = {clean_token(art) for _, art in routed}

    # ---- Gather produced artefacts from every skill's artefact section -----
    skills = {}
    for sid in skill_ids:
        p = os.path.join(SKILLS_DIR, sid, "SKILL.md")
        if not os.path.exists(p):
            fails.append(f"{sid}: no SKILL.md")
            continue
        skills[sid] = read(p)

    for sid, text in skills.items():
        for heading, body in sections(text):
            if heading.startswith("the artefact") or heading.startswith("log it"):
                produced |= path_tokens(body)

    produced |= INFRA_PATHS
    # Container dirs: only directories a skill DECLARES as its artefact (an
    # interviews/ folder, a kit/, a paperwork/). The six day folders are NOT
    # containers, otherwise any ghost file inside them would pass unseen.
    container_dirs = {t.rstrip("/") + "/" for t in produced if is_dirlike(t)}
    top_dirs = {"00-prework/", "01-discovery/", "02-market/",
                "03-product/", "04-gtm/", "05-sale/"}
    produced_stems = {p for p in produced}

    def is_produced(tok):
        bare = tok.rstrip("/")
        if tok in produced or bare in {p.rstrip("/") for p in produced}:
            return True
        if tok.startswith(INFRA_DIR_PREFIXES):
            return True
        if is_dirlike(tok):
            base = bare + "/"
            if base in top_dirs or base in container_dirs:
                return True
            # A dir-like token is fine if a produced path lives under it, or
            # if it is really a file stem (pitch-deck for pitch-deck.pptx).
            return (any(p.startswith(base) for p in produced) or
                    any(p.startswith(bare + ".") for p in produced_stems))
        # A file inside a declared container dir counts (session files etc).
        return any(tok.startswith(d) for d in container_dirs)

    # ---- Per-skill checks ---------------------------------------------------
    for sid, text in skills.items():
        loc = f"skills/{sid}/SKILL.md"

        # 5. Voice: no em dashes in the whole skill folder.
        for root, _, files in os.walk(os.path.join(SKILLS_DIR, sid)):
            for f in files:
                if f.endswith((".md", ".py", ".sh", ".json", ".yaml", ".csv", ".html")):
                    fp = os.path.join(root, f)
                    if "—" in read(fp):
                        fails.append(f"{os.path.relpath(fp, REPO)}: contains an em dash")

        # 6. Frontmatter.
        fm = re.search(r"^---\n(.*?)\n---", text, re.DOTALL)
        if not fm:
            fails.append(f"{loc}: missing frontmatter")
        else:
            front = fm.group(1)
            if "name:" not in front or "description:" not in front:
                fails.append(f"{loc}: frontmatter missing name or description")
            dm = re.search(r"description:\s*(.+)", front)
            if dm and len(dm.group(1)) > 200:
                warns.append(f"{loc}: description is {len(dm.group(1))} chars (aim under 200)")

        # 7. Body length (lines after frontmatter, excluding code fences).
        body_lines = [l for l in text.split("---", 2)[-1].splitlines() if l.strip()]
        if len(body_lines) > 60:
            warns.append(f"{loc}: body is {len(body_lines)} non-empty lines (house style aims ~45)")

        # 1. Consumed artefact paths must be produced somewhere. Ghosts in the
        # ready-when, before-you-start or done-when sections block founders,
        # so they FAIL; a stray path in steps or the fallback section WARNs.
        for heading, body in sections(text):
            if heading.startswith("the artefact") or heading.startswith("log it"):
                continue
            hard = (heading == "" or heading.startswith("before you start")
                    or heading.startswith("done when"))
            for tok in path_tokens(body):
                if not is_produced(tok):
                    msg = f"{loc} ({heading or 'header'}): consumes `{tok}` which nothing produces"
                    (fails if hard else warns).append(msg)

        # 2. Plugin file references must exist.
        for m in SKILL_FILE_RE.finditer(text):
            rel = clean_token(m.group(1))
            if any(c in rel for c in "<>*"):
                continue
            if not os.path.exists(os.path.join(SKILLS_DIR, sid, rel)):
                fails.append(f"{loc}: references ${{CLAUDE_SKILL_DIR}}/{rel} which does not exist")
        for m in PLUGIN_FILE_RE.finditer(text):
            rel = clean_token(m.group(1))
            if any(c in rel for c in "<>*"):
                continue
            if rel.endswith("/"):
                if not os.path.isdir(os.path.join(SKILLS_DIR, rel)):
                    fails.append(f"{loc}: references skills/{rel} which does not exist")
            elif not os.path.exists(os.path.join(SKILLS_DIR, rel)):
                fails.append(f"{loc}: references skills/{rel} which does not exist")

        # 3. Skill id references must exist.
        for m in CMD_ID_RE.finditer(text):
            rid = m.group(1)
            if rid not in skill_ids and rid != "checkpoint":
                fails.append(f"{loc}: references /spark-bootcamp:{rid} which is not a skill")
        for m in TICKED_ID_RE.finditer(text):
            rid = m.group(1)
            if rid not in skill_ids:
                fails.append(f"{loc}: references skill `{rid}` which does not exist")

    # 4. Routing table ids must exist.
    for rid in sorted(routed_ids):
        if rid not in skill_ids:
            fails.append(f"coach-route.py: routes to `{rid}` which is not a skill folder")

    # ---- Report -------------------------------------------------------------
    for w in sorted(set(warns)):
        print("WARN  " + w)
    for f in sorted(set(fails)):
        print("FAIL  " + f)
    print()
    print(f"{len(set(fails))} failures, {len(set(warns))} warnings, "
          f"{len(skill_ids)} skills, {len(routed)} routed steps.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
