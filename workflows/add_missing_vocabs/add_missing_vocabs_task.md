# Add Missing A1 Vocabs Task

This document describes how to make sure **every** conversation in `a1/` carries
enough new vocabulary for a learner — roughly **20-30 new words each** — by
adding suitable, easy A1 words to any conversation that is short on them.

**Goal: every `a1/` conversation should teach about 20-30 new vocabs.** Walk the
`a1/` folder one conversation at a time. If a conversation already has enough new
vocabs, leave it alone. If it has fewer than ~20, add new A1-appropriate words
until it reaches the 20-30 range.

## Quality rules (these never bend)

- **Naturalness comes first.** A word only goes into a conversation where a real
  person would actually say it. Never force a word in or invent an awkward
  sentence to fit it. Prefer **replacing** an existing word/sentence with one that
  uses the new vocabulary over just appending lines. If a candidate can't be woven
  in naturally, drop it and pick another. Better to land at 20 natural words than
  pad to 30 with forced ones.
- **Easy words only.** These are A1 (absolute beginner) conversations. Add common,
  everyday, concrete beginner vocabulary. If a B1+ learner is the first who'd know
  it, it does not belong here.
- **Every added word must be genuinely new to the whole A1 set** — see the dedup
  set below. A word is never taught twice across different conversations.
- **Keep the whole dialogue above 20 words of English** and keep the tone natural,
  adult, and consistent.
- **Every added word must actually appear in the dialogue text**, and every
  line you add or change needs a matching Persian `translation`.

## The JSON format

Conversation files live in `a1/` (e.g. `41_at_the_bookstore.json`). Copy the shape
of any existing file: a `words` focus list, `Level`, `estimatedDuration`, and a
`sentences` array of `{order, person, text, translation}`. Don't rename a file
unless its `title` changes.

## The three tracking files

- **`vocabs/a1_vocabs.txt`** — the master list of every word already used across
  **all** A1 conversations. Kept one-word-per-line, **`LC_ALL=C` sorted and
  unique**. Source of truth for "has this word been used before."
- **`added_vocabs.csv`** — log of words this task has added (`word,conversation`),
  header row `word,conversation`.
- **`progress.csv`** — log of processed conversations (`conversation,status`),
  header row `conversation,status`. `status` is `done` (words were added) or
  `skipped` (it already had ~20-30).

## Do one batch (process 3-5 conversations per loop iteration)

### 1. Setup once, at the start of the iteration

Build the **dedup set** — the union of every already-used word — so you can check
candidates instantly instead of grepping two files per word:

```bash
cd <repo root>
# master list + column 1 (the word) of the added-words log, minus its header
{ cat vocabs/a1_vocabs.txt; tail -n +2 workflows/add_missing_vocabs/added_vocabs.csv | cut -d, -f1; } \
  | LC_ALL=C sort -u > "$CLAUDE_JOB_DIR/tmp/used_words.txt"
```

A candidate `W` is allowed iff `grep -Fxq "W" "$CLAUDE_JOB_DIR/tmp/used_words.txt"`
returns **false**. Read `progress.csv` and pick the next conversations in numeric
order (`1`, `2`, `3`, …) that aren't listed there yet.

### 2. For each conversation in the batch

1. Read it and count its `words` list. If it already has ~20-30, mark it
   `skipped` and move on. If fewer than ~20, it needs `20 - current` .. `30 -
   current` more.
2. Pick easy, scenario-appropriate candidate words **not in the dedup set**. Skim
   the whole batch's scenarios first so you don't waste a great word on the wrong
   conversation.
3. Weave each word into the dialogue naturally (replace where possible), extend
   the `words` list into the **20-30** range, and add/adjust Persian
   translations for every changed line.
4. Recompute `estimatedDuration`:
   `seconds = total_english_words / 140 * 60 + number_of_sentences`,
   `estimatedDuration = max(1, round(seconds / 60))`.
   (For these short A1 dialogues this is almost always `1`.)

### 3. Commit the batch's bookkeeping in one shot

After editing all files in the batch, update the trackers **once** rather than
per conversation:

- Append each added word to `added_vocabs.csv` (`word,conversation_file`).
- Append each added word to `vocabs/a1_vocabs.txt`, then re-normalize:
  `LC_ALL=C sort -u vocabs/a1_vocabs.txt -o vocabs/a1_vocabs.txt`.
- Append each processed conversation to `progress.csv` with its status.

### 4. Verify before finishing the iteration

Run these checks; fix anything that fails before moving on:

```bash
# a) every edited conversation is valid JSON, 20<=words<=30, duration present
for f in <edited files>; do
  python3 -c "import json; d=json.load(open('a1/$f')); assert 20<=len(d['words'])<=30, ('$f',len(d['words'])); assert d['estimatedDuration']>=1"
done
# b) every word you logged for a file actually appears in that file's text
# c) master list stays sorted & unique
LC_ALL=C sort -cu vocabs/a1_vocabs.txt
# d) no word appears twice in added_vocabs.csv
tail -n +2 workflows/add_missing_vocabs/added_vocabs.csv | cut -d, -f1 | LC_ALL=C sort | uniq -d   # must print nothing
```

## Definition of done

Every conversation in `a1/` teaches roughly 20-30 new vocabs in its `words` list,
each added word is used naturally in the dialogue with a matching Persian
translation, `estimatedDuration` is recomputed, and every added word is recorded
in both `added_vocabs.csv` and `vocabs/a1_vocabs.txt` (which stays `LC_ALL=C`
sorted and unique). `progress.csv` lists every conversation.

## Notes

- It's fine to touch a conversation again on a later run if it still hasn't reached
  ~20-30 words.
- If you ever find a word in `added_vocabs.csv` that isn't yet in
  `vocabs/a1_vocabs.txt`, add it — the master must stay complete so the dedup set
  is trustworthy.
