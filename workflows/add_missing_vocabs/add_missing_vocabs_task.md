# Add Missing A1 Vocabs

**Goal:** every `a1/` conversation teaches ~20-30 new vocabs in its `words` list.
Each loop iteration handles **exactly one** conversation, end to end.

## Rules (never bend)

- **Natural first.** Only add a word where a real person would say it. Prefer
  *replacing* an existing word/line over appending. 20 natural words beats 30 forced.
- **Easy A1 words only** — common, concrete, beginner. Every added word must be
  **new to the whole A1 set** (see dedup set) and must **appear in the dialogue text**.
- Every added/changed line needs a matching Persian `translation`.

## One iteration

**1. Build the dedup set** (union of all used words):

```bash
cd <repo root>
{ cat vocabs/a1_vocabs.txt; tail -n +2 workflows/add_missing_vocabs/added_vocabs.csv | cut -d, -f1; } \
  | LC_ALL=C sort -u > /tmp/used.txt
```

**2. Pick the next conversation** — lowest number in `a1/` not yet in `progress.csv`:

```bash
comm -23 <(ls a1/ | sort) <(tail -n +2 workflows/add_missing_vocabs/progress.csv | cut -d, -f1 | sort) \
  | sort -t_ -k1 -n | head -1
```

**3. Process it.** Read the file. If `words` already has ~20-30 → status `skipped`,
go to step 5. Else pick easy candidates for *this scenario* and keep only the free
ones (print just those): `for w in a b c; do grep -Fxq "$w" /tmp/used.txt || echo "$w"; done`.
Weave them in (replace where you can), grow `words` into 20-30. Prefer targeted
`Edit`s over rewriting the whole file. Recompute:
`estimatedDuration = max(1, round((total_english_words/140*60 + n_sentences)/60))`
(almost always `1`).

**4. Bookkeeping:**

```bash
for w in <added words>; do
  printf '%s,%s\n' "$w" "<file>" >> workflows/add_missing_vocabs/added_vocabs.csv
  printf '%s\n' "$w" >> vocabs/a1_vocabs.txt
done
LC_ALL=C sort -u vocabs/a1_vocabs.txt -o vocabs/a1_vocabs.txt
printf '%s,%s\n' "<file>" done >> workflows/add_missing_vocabs/progress.csv   # or: skipped
```

**5. Verify** (fix anything that fails):

```bash
python3 -c "import json;d=json.load(open('a1/<file>'));assert 20<=len(d['words'])<=30;assert d['estimatedDuration']>=1"
LC_ALL=C sort -cu vocabs/a1_vocabs.txt
tail -n +2 workflows/add_missing_vocabs/added_vocabs.csv | cut -d, -f1 | LC_ALL=C sort | uniq -d   # prints nothing
```

Also confirm each added word appears in the file's text.

## Tracking files

- `vocabs/a1_vocabs.txt` — master list, `LC_ALL=C` sorted & unique. Source of truth.
- `added_vocabs.csv` — `word,conversation` (header `word,conversation`).
- `progress.csv` — `conversation,status` (`done` | `skipped`; header `conversation,status`).

If a word is in `added_vocabs.csv` but missing from `vocabs/a1_vocabs.txt`, add it.
