#!/usr/bin/env python3
"""Fast vocab dedup check.

Usage:
    python3 check_free.py word1 word2 ...

Prints, one per line, only the candidate words that are FREE (not already
used anywhere in the vocab universe). The universe is streamed here so the
caller never has to load the (large, growing) tracking files into context:

    - vocabs/a1_vocabs.txt        master A1 list
    - added_vocabs.csv (col 1)    every word added by this workflow
    - <level>_simp/*.txt line 2   words already taught in each conversation

Lookups are O(1) against an in-memory set; each file is read at most once.
Exit code is always 0; absence of output means every candidate is taken.
"""
import csv
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def norm(w: str) -> str:
    return w.strip().lower()


def build_used() -> set[str]:
    used: set[str] = set()

    a1 = os.path.join(ROOT, "vocabs", "a1_vocabs.txt")
    if os.path.exists(a1):
        with open(a1, encoding="utf-8") as f:
            used.update(norm(line) for line in f if line.strip())

    csv_path = os.path.join(ROOT, "workflows", "add_missing_vocabs", "added_vocabs.csv")
    if os.path.exists(csv_path):
        with open(csv_path, encoding="utf-8") as f:
            r = csv.reader(f)
            next(r, None)  # header
            for row in r:
                if row:
                    used.add(norm(row[0]))

    # words already taught on line 2 of every conversation, all levels.
    # Level dirs are named a1/a2/b1/b2/c1 (formerly *_simp); match both.
    paths = glob.glob(os.path.join(ROOT, "*_simp", "*.txt"))
    for lvl in ("a1", "a2", "b1", "b2", "c1"):
        paths.extend(glob.glob(os.path.join(ROOT, lvl, "*.txt")))
    for path in paths:
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
        if len(lines) >= 2:
            used.update(norm(w) for w in lines[1].split(",") if w.strip())

    used.discard("")
    return used


def main(argv: list[str]) -> int:
    candidates = [a for a in argv[1:] if a.strip()]
    if not candidates:
        print("usage: check_free.py word1 word2 ...", file=sys.stderr)
        return 2
    used = build_used()
    seen: set[str] = set()
    for c in candidates:
        n = norm(c)
        if n and n not in used and n not in seen:
            seen.add(n)
            print(c.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
