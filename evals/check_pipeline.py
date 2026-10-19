#!/usr/bin/env python3
"""Deterministic checks for a discovery-to-mvp project folder.

Implements the mechanical checks of the pipeline-audit skill (group A and B)
plus golden assertions for a known case. Standard library only.

    python3 evals/check_pipeline.py <project_dir>
    python3 evals/check_pipeline.py <project_dir> --golden evals/golden/harvest-line.json
    python3 evals/check_pipeline.py <project_dir> --snapshot-raw     # before the run
    python3 evals/check_pipeline.py <project_dir> --json

Exit code 0 when no check failed, 1 otherwise. Checks whose inputs are missing
are reported as n/a and never fail.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

BANNED_IN_PROBLEM = [
    "platform", "portal", "dashboard", "app", "tool", "feature", "AI", "automate",
    "build", "integrate", "system", "interface", "page", "view", "bot",
]
STOCK_WORDS = [
    "seamless", "seamlessly", "leverage", "robust", "empower", "streamline",
    "elevate", "unlock", "holistic", "delve", "crucial", "game-changer",
]
REQUIRED_HEADINGS = {
    "out/01-merged-*.md": ["Merge notes", "Check these first"],
    "out/02-extract-*.md": [
        "Who", "Pains", "Workarounds", "Numbers", "Stated vs revealed",
        "Trust and satisfaction", "Business consequence", "Silences",
    ],
    "out/03-collisions.md": ["Workflow map", "Collisions", "Neither mentioned", "Shared ground"],
    "out/04-problem.md": [
        "The brief said", "Premise audit", "Problem statement", "Checks",
        "Business case", "Non-goals",
    ],
    "out/05-scope.md": [
        "v1 in one sentence", "In scope", "Centrality check", "v1 does not",
        "Cut list", "Adoption plan", "Assumptions", "Argue with me",
    ],
    "out/06-prototype-brief.md": [
        "Assumptions ranked", "The one we test", "Flow", "Mock data",
        "Real vs faked", "Success criteria", "Test script", "Build prompt",
    ],
    "out/07-critique.md": ["Verdict", "Top issues", "The why, rewritten", "Cut"],
    "out/08-future-ideas.md": ["Position", "Path", "Bets", "Say it in the room"],
}
BRIEF_FIELDS = {
    "business outcome named": r"(?i)business (outcome|number)|which number|moves? the number|none named yet",
    "team beliefs listed": r"(?i)(team|we) believe|beliefs?\b|currently believes",
}
ID_RE = re.compile(r"\b([A-Z]{2,5})-(\d{3})\b")
TURN_RE = re.compile(r"^\[([A-Z]{2,5}-\d{3})\]\s+(?:\d{1,2}:\d{2}(?::\d{2})?\s+)?(.*)$")
QUOTE_RE = re.compile(r"\"([^\"]*)\"|“([^”]*)”")


def quotes_in(line: str) -> list[str]:
    """Quoted strings of 12+ characters. Pairs quote marks left to right, so a short
    quote earlier on the line (\"every week\") cannot shift the pairing."""
    return [a or b for a, b in QUOTE_RE.findall(line) if len(a or b) >= 12]


@dataclass
class Result:
    check: str
    status: str  # pass | fail | n/a
    detail: str = ""
    items: list[str] = field(default_factory=list)


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").lower()
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def glob(root: Path, pattern: str) -> list[Path]:
    return sorted(root.glob(pattern))


def section(text: str, heading: str) -> str | None:
    """Body of the '## heading...' section, up to the next '## '."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if re.match(r"^##\s+" + re.escape(heading), ln, re.I):
            start = i + 1
            break
    if start is None:
        return None
    body = []
    for ln in lines[start:]:
        if ln.startswith("## "):
            break
        body.append(ln)
    return "\n".join(body)


def table_rows(body: str) -> list[list[str]]:
    rows = []
    for ln in body.splitlines():
        ln = ln.strip()
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows[1:] if rows else []  # drop header


def load_turns(root: Path) -> dict[str, str]:
    turns: dict[str, str] = {}
    for f in glob(root, "out/01-merged-*.md"):
        for ln in read(f).splitlines():
            m = TURN_RE.match(ln.strip())
            if m:
                turns[m.group(1)] = m.group(2)
    return turns


def output_files(root: Path) -> list[Path]:
    out = []
    for f in glob(root, "out/*.md"):
        m = re.match(r"(\d\d)-", f.name)
        if m and 2 <= int(m.group(1)) <= 9:
            out.append(f)
    return out


# ---------------------------------------------------------------- group A

def check_raw(root: Path) -> Result:
    manifest = root / "out" / ".raw-manifest.json"
    raw = root / "raw"
    if not manifest.exists() or not raw.exists():
        return Result("A1 raw untouched", "n/a", "no snapshot; run with --snapshot-raw before the pipeline")
    before = json.loads(read(manifest))
    now = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in raw.iterdir() if p.is_file()}
    bad = [f"{n}: " + ("missing" if n not in now else "changed") for n in before if now.get(n) != before[n]]
    bad += [f"{n}: added" for n in now if n not in before]
    return Result("A1 raw untouched", "fail" if bad else "pass",
                  f"{len(before)} files snapshotted", bad)


def check_headings(root: Path) -> Result:
    missing, seen = [], 0
    for pattern, heads in REQUIRED_HEADINGS.items():
        for f in glob(root, pattern):
            seen += 1
            lines = [ln.lstrip("# ").strip().lower() for ln in read(f).splitlines() if ln.startswith("#")]
            for h in heads:
                if not any(ln.startswith(h.lower()) for ln in lines):
                    missing.append(f"{f.relative_to(root)}: missing '{h}'")
    if not seen:
        return Result("A2 required sections", "n/a", "no outputs found")
    return Result("A2 required sections", "fail" if missing else "pass", f"{seen} files", missing)


def check_ids(root: Path, turns: dict[str, str]) -> Result:
    if not turns:
        return Result("A3 turn IDs resolve", "n/a", "no merged transcripts")
    prefixes = {i.split("-")[0] for i in turns}
    orphans, total = [], 0
    for f in output_files(root):
        for n, ln in enumerate(read(f).splitlines(), 1):
            for m in ID_RE.finditer(ln):
                if m.group(1) not in prefixes:
                    continue
                total += 1
                if m.group(0) not in turns:
                    orphans.append(f"{f.name}:{n} {m.group(0)}")
    return Result("A3 turn IDs resolve", "fail" if orphans else "pass",
                  f"{total} IDs, {total - len(orphans)} resolve", orphans)


def check_quotes(root: Path, turns: dict[str, str]) -> Result:
    if not turns:
        return Result("A4 quotes verbatim", "n/a", "no merged transcripts")
    prefixes = {i.split("-")[0] for i in turns}
    brief = root / "context" / "brief.md"
    brief_text = norm(read(brief)) if brief.exists() else ""  # quoting the brief is allowed
    bad, total = [], 0
    for f in output_files(root):
        for n, ln in enumerate(read(f).splitlines(), 1):
            ids = [m.group(0) for m in ID_RE.finditer(ln) if m.group(1) in prefixes]
            if not ids:
                continue
            haystacks = [norm(turns[i]) for i in ids if i in turns]
            if not haystacks:
                continue
            haystacks.append(brief_text)
            for q in quotes_in(ln):
                for frag in re.split(r"…|\.\.\.", q):
                    nf = norm(frag)
                    if len(nf.split()) < 2:
                        continue
                    total += 1
                    if not any(nf in h for h in haystacks):
                        bad.append(f"{f.name}:{n} \"{frag.strip()[:70]}\" not in {','.join(ids)}")
    return Result("A4 quotes verbatim", "fail" if bad else "pass",
                  f"{total} quote fragments checked", bad)


def check_decisions(root: Path) -> Result:
    d = root / "out" / "decisions.md"
    steps_present = sorted({int(m.group(1)) for f in glob(root, "out/[0-9][0-9]-*")
                            if (m := re.match(r"(\d\d)-", f.name))})
    if not steps_present:
        return Result("A6 decision log", "n/a", "no outputs")
    if not d.exists():
        return Result("A6 decision log", "fail", "out/decisions.md is missing")
    text = read(d)
    entries = re.split(r"(?m)^##\s+Step\s+", text)[1:]
    nums = [int(m.group(1)) for e in entries if (m := re.match(r"(\d+)", e))]
    problems = []
    if nums != sorted(nums):
        problems.append(f"entries out of order: {nums}")
    logged = set(nums)
    # steps 9 and 10 write their own logs only when they have run; others must all be logged
    for s in steps_present:
        if s not in logged:
            problems.append(f"no decision logged for step {s}")
    for e in entries:
        head = e.splitlines()[0]
        if not re.search(r"(?im)^\s*-\s*Made by:\s*PM", e):
            problems.append(f"Step {head[:40]}: no 'Made by: PM'")
        if not re.search(r"(?im)^\s*-\s*Decision:\s*\S", e):
            problems.append(f"Step {head[:40]}: empty Decision")
    return Result("A6 decision log", "fail" if problems else "pass",
                  f"steps with outputs: {steps_present}; logged: {sorted(logged)}", problems)


def check_brief(root: Path) -> Result:
    b = root / "context" / "brief.md"
    if not b.exists():
        return Result("A8 brief states outcome and beliefs", "fail", "context/brief.md missing")
    text = read(b)
    missing = [k for k, pat in BRIEF_FIELDS.items() if not re.search(pat, text)]
    return Result("A8 brief states outcome and beliefs", "fail" if missing else "pass",
                  "orchestrator asks for these before step 1", missing)


# ---------------------------------------------------------------- group B

def check_problem(root: Path) -> Result:
    f = root / "out" / "04-problem.md"
    if not f.exists():
        return Result("B8 problem statement", "n/a", "no out/04-problem.md")
    body = section(read(f), "Problem statement")
    if body is None:
        return Result("B8 problem statement", "fail", "section not found")
    text = re.sub(r"\[[A-Z]{2,5}-\d{3}[^\]]*\]", "", body)
    text = "\n".join(ln for ln in text.splitlines() if not ln.strip().startswith(("#", "|")))
    words = re.findall(r"[A-Za-z0-9'’-]+", text)
    problems = []
    if len(words) >= 80:
        problems.append(f"{len(words)} words, limit is under 80")
    for w in BANNED_IN_PROBLEM:
        if re.search(rf"(?<![A-Za-z]){re.escape(w)}(?![A-Za-z])", text, re.I if w != "AI" else 0):
            problems.append(f"banned word '{w}'")
    if not ID_RE.search(body):
        problems.append("no turn ID cited")
    return Result("B8 problem statement", "fail" if problems else "pass", f"{len(words)} words", problems)


def check_cutlist(root: Path) -> Result:
    f = root / "out" / "05-scope.md"
    if not f.exists():
        return Result("B10 cut list", "n/a", "no out/05-scope.md")
    t = read(f)
    ins, cuts = section(t, "In scope"), section(t, "Cut list")
    if ins is None or cuts is None:
        return Result("B10 cut list", "fail", "In scope or Cut list section missing")
    in_rows, cut_rows = table_rows(ins), table_rows(cuts)
    problems = []
    if len(cut_rows) < len(in_rows):
        problems.append(f"cut list has {len(cut_rows)} rows, in-scope has {len(in_rows)}")
    date_like = re.compile(
        r"\b20\d\d\b|\bQ[1-4]\b|next (week|month|quarter|year)|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b",
        re.I)
    for r in cut_rows:
        name = r[0][:40] if r else "?"
        if len(r) < 5 or any(not c for c in r[:5]):
            problems.append(f"'{name}': needs 5 filled cells")
            continue
        if date_like.search(r[4]):
            problems.append(f"'{name}': revisit trigger looks like a date: {r[4][:40]}")
        if re.fullmatch(r"(?i)(nothing|none|n/?a|-)\.?", r[3]):
            problems.append(f"'{name}': 'what we lose' is empty in substance")
    for r in in_rows:
        if len(r) < 5 or any(not c for c in r[:5]):
            problems.append(f"in scope '{r[0][:40] if r else '?'}': needs 5 filled cells")
    return Result("B10 cut list", "fail" if problems else "pass",
                  f"{len(in_rows)} in scope, {len(cut_rows)} cut", problems)


def check_stock_words(root: Path) -> Result:
    hits = []
    files = output_files(root)
    if not files:
        return Result("B13 plain writing", "n/a", "no outputs")
    pat = re.compile(r"\b(" + "|".join(map(re.escape, STOCK_WORDS)) + r")\b", re.I)
    notjust = re.compile(r"\bnot just\b[^.\n]{0,60}\bbut\b", re.I)
    for f in files:
        for n, ln in enumerate(read(f).splitlines(), 1):
            plain = QUOTE_RE.sub("", ln)
            for m in pat.finditer(plain):
                hits.append(f"{f.name}:{n} '{m.group(0)}'")
            if notjust.search(plain):
                hits.append(f"{f.name}:{n} 'not just X, but Y'")
    return Result("B13 plain writing", "fail" if hits else "pass", f"{len(files)} files scanned", hits)


# ---------------------------------------------------------------- golden

def golden_checks(root: Path, golden: dict) -> list[Result]:
    results = []
    for a in golden.get("assertions", []):
        files = glob(root, a["file"])
        label = f"G {a['id']}"
        if not files:
            results.append(Result(label, "n/a", f"no file matches {a['file']}"))
            continue
        text = ""
        for f in files:
            body = read(f)
            if a.get("scope") == "turns":
                body = "\n".join(ln for ln in body.splitlines() if TURN_RE.match(ln.strip()))
            elif a.get("scope") == "problem-statement":
                body = section(body, "Problem statement") or ""
            text += body + "\n"
        found = re.search(a["pattern"], text, re.I | re.M) is not None
        want = a["kind"] == "must_match"
        results.append(Result(label, "pass" if found == want else "fail",
                              a["why"], [] if found == want else [f"pattern {'absent' if want else 'present'}: {a['pattern']}"]))
    for t in golden.get("trails", []):
        rows, gaps = [], []
        for pattern in t["files"]:
            fs = glob(root, pattern)
            if not fs:
                rows.append(f"{pattern}: file not found")
                continue
            ok = any(re.search(t["pattern"], read(f), re.I) for f in fs)
            rows.append(f"{pattern}: {'present' if ok else 'ABSENT'}")
            if not ok:
                gaps.append(pattern)
        existing = [p for p in t["files"] if glob(root, p)]
        status = "n/a" if len(existing) < 2 else ("fail" if gaps else "pass")
        results.append(Result(f"C trail: {t['name']}", status, "; ".join(rows), gaps))
    return results


# ---------------------------------------------------------------- driver

def run(root: Path, golden: dict | None) -> list[Result]:
    turns = load_turns(root)
    res = [
        check_raw(root), check_headings(root), check_ids(root, turns), check_quotes(root, turns),
        check_decisions(root), check_brief(root), check_problem(root), check_cutlist(root),
        check_stock_words(root),
    ]
    if golden:
        res += golden_checks(root, golden)
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("--golden", help="path to a golden JSON file")
    ap.add_argument("--snapshot-raw", action="store_true", help="hash raw/ into out/.raw-manifest.json and exit")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = Path(args.project).resolve()

    if args.snapshot_raw:
        (root / "out").mkdir(exist_ok=True)
        snap = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((root / "raw").iterdir()) if p.is_file()}
        (root / "out" / ".raw-manifest.json").write_text(json.dumps(snap, indent=2))
        print(f"snapshotted {len(snap)} raw files")
        return 0

    golden = json.loads(read(Path(args.golden))) if args.golden else None
    results = run(root, golden)

    if args.json:
        print(json.dumps([r.__dict__ for r in results], indent=2))
    else:
        for r in results:
            print(f"{r.status.upper():4}  {r.check}  {('- ' + r.detail) if r.detail else ''}")
            for it in r.items[:8]:
                print(f"        {it}")
            if len(r.items) > 8:
                print(f"        ... and {len(r.items) - 8} more")
        c = {s: sum(r.status == s for r in results) for s in ("pass", "fail", "n/a")}
        print(f"\n{c['pass']} pass, {c['fail']} fail, {c['n/a']} n/a")
    return 1 if any(r.status == "fail" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
