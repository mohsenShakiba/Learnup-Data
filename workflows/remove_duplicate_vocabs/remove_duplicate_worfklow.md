# Remove Duplicate Vocab Workflow

Goal: make `duplicate.csv` empty by incrementally removing repeated vocab from later conversations.

## Source File

Use `duplicate.csv`.

Expected format:

```csv
Word,LessonId
hotel,1
hotel,28
hotel,47
```

Each `Word` appears in more than one conversation or lesson. `LessonId` identifies the conversation where that vocab currently appears.

## Rule

For each duplicate word, keep the vocab only in the earliest conversation where it appears.

Example:

```csv
hotel,1
hotel,28
hotel,47
```

Keep `hotel` in conversation `1`.

Remove `hotel` from the new vocabs of conversations `28` and `47`.

After those removals are done, remove all `hotel` rows from `duplicate.csv`.

## Incremental Schedule

Do not process the whole file at once.

In each search loop or scheduled run:

1. Pick about 10 unique words from `duplicate.csv`.
2. For each word, find all listed `LessonId` values.
3. Keep the word in the lowest or earliest `LessonId`.
4. Remove the word from the new vocabs of every later conversation.
5. Confirm the removals are done.
6. Delete the processed word rows from `duplicate.csv`.
7. Save the updated `duplicate.csv`.

Repeat this schedule until `duplicate.csv` contains only the header row or is otherwise empty of duplicate entries.

## Batch Checklist

For every batch of about 10 words:

- Read the next unprocessed duplicate words from `duplicate.csv`.
- Group rows by `Word`.
- Sort each group by `LessonId`.
- Treat the first `LessonId` as the source to keep.
- Remove the word from all later conversation new-vocab records.
- Update `duplicate.csv` by removing rows for words fully processed in this batch.
- Re-check `duplicate.csv` before the next batch.

## Important Notes

- Process about 10 words per loop or schedule run.
- Do not remove the earliest occurrence of a word.
- Only remove rows from `duplicate.csv` after the corresponding vocab removals are complete.
- If a word cannot be safely removed from a conversation, leave that word in `duplicate.csv` and continue with the next word.
- Continue incrementally until `duplicate.csv` is empty.
