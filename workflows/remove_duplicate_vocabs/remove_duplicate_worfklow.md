# Remove Duplicate Vocab Workflow

Goal: make `duplicates.csv` empty by incrementally removing repeated vocab from later conversations.

## Source File

Use `duplicates.csv`.

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

After those removals are done, remove all `hotel` rows from `duplicates.csv`.

## Incremental Schedule

Do not process the whole file at once.

In each search loop or scheduled run:

1. Pick about 10 unique words from `duplicates.csv`.
2. For each word, find all listed `LessonId` values.
3. Keep the word in the lowest or earliest `LessonId`.
4. Remove the word from the new vocabs of every later conversation.
5. Confirm the removals are done.
6. Delete the processed word rows from `duplicates.csv`.
7. Save the updated `duplicates.csv`.
8. Commit the batch changes with a very short git commit message.

Repeat this schedule until `duplicates.csv` contains only the header row or is otherwise empty of duplicate entries.

## Batch Checklist

For every batch of about 10 words:

- Read the next unprocessed duplicate words from `duplicates.csv`.
- Group rows by `Word`.
- Sort each group by `LessonId`.
- Treat the first `LessonId` as the source to keep.
- Remove the word from all later conversation new-vocab records.
- Update `duplicates.csv` by removing rows for words fully processed in this batch.
- After 10 vocab words are completed and `duplicates.csv` is updated, run `git status`, stage only the completed batch changes, and commit with a very short description.
- Re-check `duplicates.csv` before the next batch.

## Important Notes

- Process about 10 words per loop or schedule run.
- Do not remove the earliest occurrence of a word.
- Only remove rows from `duplicates.csv` after the corresponding vocab removals are complete.
- If a word cannot be safely removed from a conversation, leave that word in `duplicates.csv` and continue with the next word.
- After each completed 10-word batch, commit the changes with a very short message, such as `Remove duplicate vocabs`.
- Continue incrementally until `duplicates.csv` is empty.
