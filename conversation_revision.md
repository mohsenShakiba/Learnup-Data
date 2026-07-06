# Conversation Revision Task (A1)

Revise the conversations in `a1/` (64 files, numbered 1–64) so every line sounds
natural. Use with `agent.md` (story rules), `plan.csv` (revision log),
`added_words.csv` / `removed_words.csv` (word-change logs).

## One conversation per run

**Process exactly one conversation per run, then stop.** This task is meant to
be run repeatedly in a loop: each run picks the single next unlogged
conversation, revises only that one, logs it, and exits. Do not touch any other
conversation. When every conversation in `a1/` already appears in `plan.csv`,
there is nothing to do — report that and stop.

## Priority

Natural-sounding dialogue beats everything else — vocabulary count, the word
list, even the story itself. Change, add, remove, or delete whatever doesn't
sound natural.

## What's allowed

- Replace or delete a story entirely if it can't be made to sound natural.
- Add or remove focus words freely — keep the list at 10–30 words per story.
- Any wording change, as long as translations and the word list stay in sync.

## Logging word changes

Every word added to or removed from a story's `words` list must be logged
(append-only, like `plan.csv` — never edit existing lines):

- Added → append to `added_words.csv`: `WORD,NUMBER,DATE`
- Removed → append to `removed_words.csv`: `WORD,NUMBER,DATE`

## Steps

1. Pick the **single** next conversation number in `a1/` not yet logged in
   `plan.csv` (lowest unlogged number). If none remain, stop — you're done.
2. Read that one file fully. Ask: would a native speaker actually say this?
3. Rewrite unnatural lines. If the whole story doesn't work, replace or delete it.
4. Update the Persian `translation` for every changed line.
5. Update `words` (10–30 focus words); log every add/remove as above.
6. Set `Level: A1`; recompute `estimatedDuration` (formula in `agent.md`).
7. Rename the file if the title changed.
8. Append `NUMBER,DATE` to `plan.csv`.
9. Stop. Do not move on to the next conversation — that's the next run's job.

## Definition of done (for the one conversation this run)

- Exactly one conversation was revised this run; no other file was touched.
- Every line sounds natural — even if that meant changing/removing words or
  the story itself.
- Translations match; `words` list has 10–30 items; changes are logged.
- `Level`, `estimatedDuration`, and filename are correct.
- `plan.csv` has a new line for the conversation (unless it was deleted).

## Example (already done)

`a1/8_at_the_doctor.json`:
- "Hello. What's the problem?" → "Hello. What's wrong?"
- "Do you feel hot?" → "Do you have a fever?"
- Removed "hot" (→ `removed_words.csv`), added "fever" (→ `added_words.csv`).
- Appended `8,2026-07-06` to `plan.csv`.
