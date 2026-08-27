# Vocabulary Tracking Workflow

## Files

| File | Purpose |
| --- | --- |
| `vocabs/a1.csv` | Canonical permitted A1 lemmas. |
| `lessons/a1_used_vocabs.csv` | A1 lemmas introduced anywhere in A1 conversations. |
| `lessons/a1_missing_vocabs.csv` | A1 lemmas not introduced yet. |
| `vocabs/a2.csv` | Canonical permitted A2 lemmas. |
| `lessons/a2_used_vocabs.csv` | A2 lemmas introduced anywhere in A2 conversations. |
| `lessons/a2_missing_vocabs.csv` | A2 lemmas not introduced yet. |
| `lessons/need_attention.csv` | Conversation words not covered by the intended vocabulary lists. |

## Vocabulary Selection

- Each lesson's `Vocabulary:` line lists only **new lemmas from that lesson's CEFR vocabulary file, introduced for the first time at that level**.
- Count only active lesson files whose names begin with a numeric lesson ID, such as `40_talking_about_hobbies.txt`. Files beginning with `_` are inactive drafts and do not affect the trackers.
- Do not list words already introduced in earlier lessons at the same level, even if they appear again.
- Use lemmas, not surface forms: `starts` -> `start`, `books` -> `book`.
- Do not count advanced/irregular forms as a simple lemma use: `bought` does not introduce `buy`.
- Do not track names, speaker labels, countries, punctuation, or basic function forms not in the level's vocabulary CSV.
- If a useful conversation word is not in the vocabulary available at that level or below, either replace it or add it to the appropriate vocabulary CSV and classify it.

## Tracker Rules

- Each level's used and missing tracker files must split that level's canonical vocabulary CSV exactly.
- Every canonical lemma must appear in exactly one of the two tracker files for its level.
- Move a lemma from missing to used when it is first introduced in a conversation at that level.
- Move a lemma from used to missing only if it no longer appears in any active conversation at that level.
- Keep each used tracker alphabetically sorted.
- Keep each missing tracker in the same order as its canonical vocabulary CSV.

## After Editing Lessons

1. Identify the lesson's newly introduced lemmas from its level vocabulary CSV.
2. Update that lesson's `Vocabulary:` line with only those new lemmas.
3. Move newly introduced lemmas from that level's missing tracker to its used tracker.
4. Move removed lemmas back to missing only when no active conversation at that level still uses them.
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

For A2, run the same validation with `a2.csv`, `a2_used_vocabs.csv`, and `a2_missing_vocabs.csv` substituted for the A1 paths.
