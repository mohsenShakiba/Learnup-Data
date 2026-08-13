# A1 Vocabulary Tracking Workflow

## Purpose

Keep the A1 vocabulary list and its two lesson-coverage trackers in sync.

| File | Role |
| --- | --- |
| `vocabs/a1.csv` | Canonical list of permitted A1 lemmas. Add or remove a word here only when the A1 curriculum changes. |
| `lessons/a1_used_vocabs.csv` | A1 lemmas already used in A1 conversations in their simple/base form. |
| `lessons/a1_missing_vocabs.csv` | A1 lemmas not yet present in `a1_used_vocabs.csv`; this is the pool for future conversations. |
| `lessons/need_attention.csv` | Words found in conversations that are not currently covered by the intended level list and need a decision. It is not part of the used/missing split. |

## Rules

- Keep one `lemma` header and one lowercase lemma per row in the tracking CSVs.
- A word must appear in exactly one of `a1_used_vocabs.csv` or `a1_missing_vocabs.csv`.
- Together, the two trackers must contain every word in `vocabs/a1.csv` exactly once.
- Add a word to `a1_used_vocabs.csv` only when its simple/base form appears in an A1 conversation. For example, record `buy` when the dialogue contains `buy`, not merely `bought`.
- Keep `a1_used_vocabs.csv` alphabetically sorted. Keep `a1_missing_vocabs.csv` in the same order as `vocabs/a1.csv`.

## When to Update

### After editing or adding an A1 conversation

1. Identify A1 words newly used in their simple form.
2. Move each of those words from `a1_missing_vocabs.csv` to `a1_used_vocabs.csv`.
3. If a word in the conversation is not in `vocabs/a1.csv`, either:
   - rewrite the conversation with an A1 word, or
   - add the word to `vocabs/a1.csv` if it belongs in the curriculum, then classify it in one tracker.
4. If an edit removes a word's only simple-form use across all A1 conversations, move it back from `a1_used_vocabs.csv` to `a1_missing_vocabs.csv`.

### After changing `vocabs/a1.csv`

1. For every newly added lemma, place it in `a1_used_vocabs.csv` if it is already used in a conversation in simple form; otherwise place it in `a1_missing_vocabs.csv`.
2. Remove deleted lemmas from both tracker files.
3. Re-sort `a1_used_vocabs.csv`, preserve `a1_missing_vocabs.csv` in `a1.csv` order, and run the validation check below.

## Validation

Run this from the repository root after any vocabulary or A1-conversation change:

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

The check should produce no words in any section.
