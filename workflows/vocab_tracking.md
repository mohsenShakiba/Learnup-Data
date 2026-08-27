# A1 Vocabulary Tracking Workflow

## Files

| File | Purpose |
| --- | --- |
| `vocabs/a1.csv` | Canonical permitted A1 lemmas. |
| `lessons/a1_used_vocabs.csv` | A1 lemmas introduced anywhere in A1 conversations. |
| `lessons/a1_missing_vocabs.csv` | A1 lemmas not introduced yet. |
| `lessons/need_attention.csv` | Conversation words not covered by the intended vocabulary lists. |

## Vocabulary Selection

- Each lesson's `Vocabulary:` line lists only **new A1 lemmas introduced for the first time in that lesson**.
- Count only active lesson files whose names begin with a numeric lesson ID, such as `40_talking_about_hobbies.txt`. Files beginning with `_` are inactive drafts and do not affect the trackers.
- Do not list words already introduced in earlier A1 lessons, even if they appear again.
- Use lemmas, not surface forms: `starts` -> `start`, `books` -> `book`.
- Do not count advanced/irregular forms as a simple lemma use: `bought` does not introduce `buy`.
- Do not track names, speaker labels, countries, punctuation, or basic function forms not in `vocabs/a1.csv`.
- If a useful conversation word is not in `vocabs/a1.csv`, either replace it or add it to `vocabs/a1.csv` and classify it.

## Tracker Rules

- `a1_used_vocabs.csv` and `a1_missing_vocabs.csv` must split `vocabs/a1.csv` exactly.
- Every A1 lemma must appear in exactly one of those two tracker files.
- Move a lemma from missing to used when it is first introduced in an A1 conversation.
- Move a lemma from used to missing only if it no longer appears in any A1 conversation.
- Keep `a1_used_vocabs.csv` alphabetically sorted.
- Keep `a1_missing_vocabs.csv` in the same order as `vocabs/a1.csv`.

## After Editing A1 Lessons

1. Identify the lesson's newly introduced A1 lemmas.
2. Update that lesson's `Vocabulary:` line with only those new lemmas.
3. Move newly introduced lemmas from `a1_missing_vocabs.csv` to `a1_used_vocabs.csv`.
4. Move removed lemmas back to missing only when no A1 conversation still uses them.
5. Remove covered words from `need_attention.csv`; add unresolved words there if needed.
6. Run validation.

## Validation

Run this from the repository root:

```powershell
$a1 = (Import-Csv 'vocabs/a1.csv').lemma
$used = (Import-Csv 'lessons/a1_used_vocabs.csv').lemma
$missing = (Import-Csv 'lessons/a1_missing_vocabs.csv').lemma

'Not tracked:'
$a1 | Where-Object { $_ -notin $used -and $_ -notin $missing } | Sort-Object -Unique
'In both trackers:'
$used | Where-Object { $_ -in $missing } | Sort-Object -Unique
'Not in a1.csv:'
($used + $missing) | Where-Object { $_ -notin $a1 } | Sort-Object -Unique
```

All three sections should be empty.
