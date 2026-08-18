# A1 Grammar Progression Workflow

## Purpose

Every A1 lesson may use only grammar that is introduced in that lesson or in an earlier lesson. This applies to all learner-facing text, including dialogue, titles, instructions, examples, and exercises.

`grammars/a1_grammar_to_lessons.csv` is the source of truth for when a grammar point becomes available. A grammar point with no `conversation_id` is **not available** in any lesson until the CSV assigns it an introduction lesson.

## Determine a Lesson's Grammar Scope

1. Get the lesson number from its filename. For example, `lessons/a1/09_at_the_doctor.txt` is lesson 9 and `lessons/a1/01.5_a_nurse_and_an_umbrella.txt` is lesson 1.5.
2. Read `grammars/a1_grammar_to_lessons.csv`.
3. Include every row whose numeric `conversation_id` is less than or equal to the lesson number.
4. Treat the resulting grammar points as the lesson's permitted grammar inventory.
5. Do not use a grammar point whose introduction lesson is later than the lesson being written or edited. Rewrite the relevant wording so it uses only the permitted inventory.

Grammar that is not listed in the CSV is also out of scope unless its use is explicitly added to the mapping first.

## Current Introduction Order

| Introduced in lesson | Grammar available from that lesson onward |
| --- | --- |
| 1 | Subject pronouns and verb be |
| 1.5 | Articles |
| 2 | Present simple |
| 3 | Prepositions of place and time |
| 4 | Basic negatives and questions |
| 5 | There is / There are |
| 6 | Adverbs of frequency |
| 7 | Question words (wh-) |
| 8 | Basic sentence order |
| 9 | Should for advice |
| 10 | Past simple |
| 15 | Imperatives |
| 24 | Demonstratives |
| 26 | Singular and plural nouns |

The following rows have no introduction lesson and therefore cannot be used yet:

- Have got
- Possessive adjectives
- Possessive 's

## Authoring and Review Checklist

Before finalizing a lesson:

1. Calculate its permitted grammar inventory from the CSV.
2. Identify every grammar construction in the learner-facing text, including short answers and question forms.
3. Confirm that each construction belongs to the inventory for that lesson.
4. Check that the lesson's new grammar, if any, is the grammar mapped to that lesson number; do not introduce an unmapped or future point incidentally.
5. Replace or remove every future, unmapped, or unassigned grammar construction.
6. Recheck the complete lesson after revisions, since a rewrite can introduce a different out-of-scope construction.

## Maintaining the Mapping

When introducing a new grammar point, first add or update its row in `grammars/a1_grammar_to_lessons.csv` with the intended `conversation_id`. Then review that lesson and all earlier lessons against the updated order. Keep grammar names consistent with the corresponding files in `grammars/` so the curriculum can be audited easily.

## Quick Scope Check

Run this from the repository root to see the grammar permitted for a lesson. Change `$lessonNumber` as needed.

```powershell
$lessonNumber = 9

Import-Csv 'grammars/a1_grammar_to_lessons.csv' |
    Where-Object {
        $_.conversation_id -match '^\d+(\.\d+)?$' -and
        [decimal] $_.conversation_id -le $lessonNumber
    } |
    Sort-Object { [decimal] $_.conversation_id } |
    Select-Object conversation_id, grammar_name
```

This command establishes the permitted scope; the author or reviewer must still inspect the lesson text to confirm that it contains no other grammar.
