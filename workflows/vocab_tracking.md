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
| `vocabs/b1.csv` | Canonical permitted B1 lemmas; A1 and A2 vocabulary is also permitted. |
| `vocabs/b1_word_forms.json` | B1 form aliases and reviewed exceptions for unique-word counting. |
| `lessons/b1_used_vocabs.csv` | B1 lemmas introduced anywhere in B1 conversations. |
| `lessons/b1_missing_vocabs.csv` | B1 lemmas not introduced yet. |
| `vocabs/b2.csv` | Canonical permitted B2 lemmas; A1, A2, and B1 vocabulary is also permitted. |
| `lessons/b2_used_vocabs.csv` | B2 lemmas introduced anywhere in B2 conversations. |
| `lessons/b2_missing_vocabs.csv` | B2 lemmas not introduced yet. |
| `lessons/need_attention.csv` | Conversation words not covered by the intended vocabulary lists. |

## Vocabulary Selection

- Every conversation must introduce **at least 10 distinct new lemmas** from its level's canonical vocabulary CSV. Each must occur in the actual dialogue; a title or `Vocabulary:` entry alone does not satisfy the minimum.
- Each lesson's `Vocabulary:` line lists only **new lemmas from that lesson's CEFR vocabulary file, introduced for the first time at that level**.
- Count only active lesson files whose names begin with a numeric lesson ID, such as `40_talking_about_hobbies.txt`. Files beginning with `_` are inactive drafts and do not affect the trackers.
- Do not list words already introduced in earlier lessons at the same level, even if they appear again.
- Check earlier dialogue as well as vocabulary lines. A missing entry in an earlier lesson's `Vocabulary:` line does not make an already used word new.
- Use lemmas, not surface forms: `starts` -> `start`, `books` -> `book`.
- B1 uses one vocabulary credit per base word and its inflected or participial forms, including participles used as adjectives. For example, `annoy`, `annoyed`, and `annoying` count once; `qualified` introduces `qualify`, not a second word. An earlier occurrence in any of these forms uses up that word's first introduction.
- Use the reviewed aliases in `vocabs/b1_word_forms.json`. If the base is already taught at A1 or A2, its B1 form is not a new B1 word: for example, `fixed` -> `fix` and `relaxed` -> `relax`. If the base is unavailable at B1 or below, keep one existing family representative rather than automatically moving a higher-level verb into B1; for example, `disappointed` is grouped under `disappointing`.
- Do not automatically merge different derived words such as `breath`/`breathe`, `responsible`/`responsibility`, or adjectives and their `-ly` adverbs. Preserve independent meanings such as `goods` versus `good`; the reviewed exceptions are recorded in the alias file. `indoors` is not a plural of `indoor`, and `IT` is not the pronoun `it`.
- Do not infer irregular relationships by removing letters. Use an explicitly reviewed alias when one is provided, such as `frozen` -> `freeze`. Other advanced/irregular forms still need manual review; `bought` must not automatically introduce `buy`. Word-family counting does not unlock grammar or senses that are above the lesson's level.
- Do not track names, speaker labels, countries, punctuation, or basic function forms not in the level's vocabulary CSV.
- If a useful conversation word is not in the vocabulary available at that level or below, either replace it or add it to the appropriate vocabulary CSV and classify it.
- Follow [Natural Dialogue](natural_dialogue.md) when selecting and using target words. If a word forces awkward dialogue, choose another unused word or expand a relevant part of the scene while retaining at least 10 new lemmas. Do not add words to the canonical CSV merely to reach the minimum.

## Tracker Rules

- Each level's used and missing tracker files must split that level's canonical vocabulary CSV exactly.
- Every canonical lemma must appear in exactly one of the two tracker files for its level.
- Move a lemma from missing to used when it is first introduced in a conversation at that level.
- Move a lemma from used to missing only if it no longer appears in any active conversation at that level.
- Keep each used tracker alphabetically sorted.
- Keep each missing tracker in the same order as its canonical vocabulary CSV.

## After Editing Lessons

1. Identify the lesson's newly introduced lemmas from its level vocabulary CSV. Confirm at least 10 distinct new lemmas in the dialogue against earlier active lessons, not only their vocabulary lines.
2. Update that lesson's `Vocabulary:` line with only those new lemmas.
   - When consolidating duplicate forms, update affected earlier lessons too. A form may stay in the dialogue, but list and count only its canonical representative. Replace lost new-word credits with genuinely unused vocabulary that fits the scene.
3. Move newly introduced lemmas from that level's missing tracker to its used tracker.
4. Move removed lemmas back to missing only when no active conversation at that level still uses them.
5. Remove covered words from `need_attention.csv`; add unresolved words there if needed.
6. Run tracker validation and check that each listed new lemma appears in the dialogue. The tracker partition check below does not establish the new-word count or first use.
7. Complete the natural dialogue review and grammar scope review after the final edits.

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

For B1, substitute `b1.csv`, `b1_used_vocabs.csv`, and `b1_missing_vocabs.csv`. When checking dialogue difficulty with `scripts/level_check.py`, pass `a1,a2,b1` as the allowed levels.

For B2, substitute `b2.csv`, `b2_used_vocabs.csv`, and `b2_missing_vocabs.csv`. When checking dialogue difficulty with `scripts/level_check.py`, pass `a1,a2,b1,b2` as the allowed levels.
