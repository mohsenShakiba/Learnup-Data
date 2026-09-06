# Grammar Progression Workflow

## Purpose

Every lesson may use only grammar inherited from lower levels or introduced in that lesson or an earlier lesson at the same level. This applies to all learner-facing text, including dialogue, titles, instructions, examples, and exercises.

`grammars/<level>_grammar_to_lessons.csv` is the source of truth for when a grammar point becomes available at that level. A grammar point with no `conversation_id` is **not available** in that level's lessons until the CSV assigns it an introduction lesson. A2 lessons may also use grammar already available by the end of A1.

A lesson after the latest mapped introduction is a review lesson unless the mapping is extended first. A higher lesson number does not unlock additional grammar by itself.

## Determine a Lesson's Grammar Scope

1. Get the level and lesson number from its path and filename. For example, `lessons/a1/10_at_the_doctor.txt` is A1 lesson 10 and `lessons/a2/02_the_lost_phone.txt` is A2 lesson 2.
2. Read the mapping for the lesson's level, such as `grammars/a1_grammar_to_lessons.csv` or `grammars/a2_grammar_to_lessons.csv`.
3. Include every row whose numeric `conversation_id` is less than or equal to the lesson number.
4. Treat the resulting grammar points as the lesson's permitted grammar inventory.
5. Do not use a grammar point whose introduction lesson is later than the lesson being written or edited. Rewrite the relevant wording so it uses only the permitted inventory.

Grammar that is not listed in the CSV is also out of scope unless its use is explicitly added to the mapping first.

## Current A1 Introduction Order

| Introduced in lesson | Grammar available from that lesson onward |
| --- | --- |
| 1 | Subject pronouns and verb be |
| 2 | Articles |
| 3 | Present simple |
| 4 | Prepositions of place and time |
| 5 | Basic negatives and questions |
| 6 | There is / There are |
| 7 | Adverbs of frequency |
| 8 | Question words (wh-) |
| 9 | Basic sentence order |
| 10 | Should for advice |
| 11 | Past simple |
| 13 | Possessive adjectives |
| 14 | Demonstratives; Future will |
| 15 | Possessive 's |
| 16 | Can / cannot |
| 17 | Singular and plural nouns |
| 18 | Present continuous |
| 19 | Imperatives |

The following rows have no introduction lesson and therefore cannot be used yet:

- Have got

## Current A2 Introduction Order

| Introduced in lesson | Grammar available from that lesson onward |
| --- | --- |
| 1 | Present continuous |
| 2 | Past simple |
| 3 | Used to |
| 4 | Future with will |
| 5 | Going to |
| 6 | Object pronouns |
| 7 | Possessive pronouns |
| 8 | Reflexive pronouns |
| 9 | Countable and uncountable nouns |
| 10 | Some, any, much, many, a lot of |
| 11 | Some, any and no compounds |
| 12 | Comparatives and superlatives |
| 13 | -ed and -ing adjectives |
| 14 | Adjective order |
| 15 | So, such, too, enough |
| 16 | Prepositions of movement |

The remaining A2 grammar rows have no introduction lesson and therefore cannot be used yet. Their order in the grammar JSON files does not make them available by itself.

## Authoring and Review Checklist

Before finalizing a lesson:

1. Calculate its permitted grammar inventory from the CSV.
2. Identify every grammar construction in the learner-facing text, including short answers and question forms.
3. Confirm that each construction belongs to the inventory for that lesson.
4. Check that the lesson's new grammar, if any, is the grammar mapped to that lesson number; do not introduce an unmapped or future point incidentally.
5. Replace or remove every future, unmapped, or unassigned grammar construction.
6. Recheck the complete lesson after revisions, since a rewrite can introduce a different out-of-scope construction.

## Maintaining the Mapping

When introducing a new grammar point, first add or update its row in the appropriate level mapping with the intended `conversation_id`. Then review that lesson and all earlier lessons at that level against the updated order. Keep grammar names consistent with the corresponding files in `grammars/` so the curriculum can be audited easily.

## Quick Scope Check

Run this from the repository root to see the grammar permitted for a lesson. Change `$lessonNumber` as needed.

```powershell
$lessonNumber = 9
$level = 'a2'

Import-Csv "grammars/${level}_grammar_to_lessons.csv" |
    Where-Object {
        $_.conversation_id -match '^\d+(\.\d+)?$' -and
        [decimal] $_.conversation_id -le $lessonNumber
    } |
    Sort-Object { [decimal] $_.conversation_id } |
    Select-Object conversation_id, grammar_name
```

This command establishes the permitted scope; the author or reviewer must still inspect the lesson text to confirm that it contains no other grammar.
