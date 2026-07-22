"""Flag conversation-body words that are above the target course level.

Usage:
    python scripts/level_check.py courses/a2/1_some_title.txt
    python scripts/level_check.py courses/b1/3_some_title.txt a1,a2,b1

The second argument is the comma-separated set of *allowed* levels (words at or
below the course level). It defaults to a1 + a2. Any body word whose home list is
higher than the allowed set is reported as ABOVE LEVEL and should be replaced with
a simpler synonym. Function words, names, and words in no list are shown separately
and are safe to ignore.
"""
import sys
import re
import os

VOCAB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vocabs")
LEVELS = ["a1", "a2", "b1", "b2", "c1", "c2"]


def load(level):
    p = os.path.join(VOCAB_DIR, f"{level}.csv")
    words = set()
    if not os.path.exists(p):
        return words
    with open(p, encoding="utf-8") as f:
        for i, line in enumerate(f):
            w = line.strip().lower()
            if not w or (i == 0 and w == "lemma"):
                continue
            words.add(w)
    return words


lists = {lv: load(lv) for lv in LEVELS}


def level_of(word):
    """Earliest level a word (or a simple de-inflection of it) appears in."""
    cands = {word}
    if word.endswith("s"):
        cands.add(word[:-1])
    if word.endswith("es"):
        cands.add(word[:-2])
    if word.endswith("ed"):
        cands.add(word[:-2])
        cands.add(word[:-1])
    if word.endswith("ing"):
        cands.add(word[:-3])
        cands.add(word[:-3] + "e")
    if word.endswith("ies"):
        cands.add(word[:-3] + "y")
    if word.endswith("ly"):
        cands.add(word[:-2])
    for lv in LEVELS:
        if cands & lists[lv]:
            return lv
    return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    target = sys.argv[1]
    allowed = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else {"a1", "a2"}

    with open(target, encoding="utf-8") as f:
        body = f.read().splitlines()[2:]  # skip title + vocab line

    tokens = re.findall(r"[a-zA-Z']+", " ".join(body).lower())
    above, unlisted = {}, set()
    for t in tokens:
        lv = level_of(t)
        if lv is None:
            unlisted.add(t)
        elif lv not in allowed:
            above[t] = lv

    print(f"Allowed levels: {sorted(allowed)}")
    print(f"\n[ABOVE LEVEL] body words that live in {sorted(set(LEVELS) - allowed)}:")
    if above:
        for w, lv in sorted(above.items(), key=lambda x: x[1]):
            print(f"   {lv.upper()}  {w}")
    else:
        print("   (none)")

    print("\n[UNLISTED] not in any level list (function words / names / unknown):")
    print("   " + ", ".join(sorted(unlisted)))

    sys.exit(1 if above else 0)


if __name__ == "__main__":
    main()
