# Add Missing A1 Vocabs Task

This document describes how to make sure **every** conversation in `a1/` carries
enough new vocabulary for a learner — roughly **20-30 new words each** — by
adding suitable, easy A1 words to any conversation that is short on them. Use it
together with `agent.md` (story generation guidelines).

**Goal: every `a1/` conversation should teach about 20-30 new vocabs.** Walk the
`a1/` folder one conversation at a time. If a conversation already has enough new
vocabs, leave it alone. If it has fewer than ~20, add new A1-appropriate words
until it reaches the 20-30 range.

**Naturalness comes first.** A word only goes into a conversation where a real
person would actually say it. Never force a word in or invent an awkward sentence
to fit it. The natural, adult, everyday tone of the conversation must be
preserved — if a candidate word can't be woven in naturally, drop it and pick a
different one. Do not sacrifice the flow of the dialogue to hit the word count.

**Easy words only.** These are A1 (absolute beginner) conversations. Add common,
everyday, concrete beginner vocabulary. Avoid abstract, formal, technical, or
otherwise hard words — if a B1+ learner is the first who'd know it, it does not
belong here.

## The three tracking files

- **`vocabs/a1_vocabs.txt`** — the master list of every word already used across
  **all** A1 conversations. This is the source of truth for "has this word been
  used before." **A word you add must NOT already appear here** — every added
  word must be genuinely new to the A1 set, so it isn't taught twice in different
  conversations.
- **`added_vocabs.csv`** — the log of words this task has added, so later runs
  know a word is already placed and don't add it again. **Every time you add a
  word to a conversation, append it here.**
- **`progress.csv`** — the log of which conversations have already been
  processed, so each run knows which conversation to pick up next. **Every time
  you finish a conversation, append it here.**
- The conversation files themselves live in `a1/` (e.g.
  `41_at_the_bookstore.json`).

### `added_vocabs.csv` format

One row per added word:

```
WORD,CONVERSATION_FILE
```

e.g. `notebook,41_at_the_bookstore.json`. Create the file with this header row if
it doesn't exist yet:

```
word,conversation
```

### `progress.csv` format

One row per processed conversation:

```
CONVERSATION_FILE,STATUS
```

`STATUS` is `done` when the conversation reached ~20-30 words, or `skipped` when
it already had enough. Create the file with this header row if it doesn't exist
yet:

```
conversation,status
```

## How to do one batch

This task runs on a loop, so process a few conversations now and leave the rest
for the next iteration — don't try to do the whole `a1/` folder in one pass.

1. **Pick the next conversation(s)** in `a1/`. Read `progress.csv` and choose the
   next conversation(s) that aren't listed there yet. A batch of one or a couple
   of conversations is fine.
2. **Count the new vocabs it currently teaches** (its `words` focus list). If it
   already has ~20-30, skip it. If it has fewer than ~20, it needs more.
3. **Choose candidate words to add:**
   - They must fit the conversation's scenario naturally.
   - They must be **easy** A1 words (see above).
   - They must **not** already appear in `vocabs/a1_vocabs.txt` (not used in any
     other conversation).
   - They must not already be in `added_vocabs.csv`.
4. **Weave each word into the dialogue** (see `agent.md` for the full JSON
   format):
   - Use each word the way a real person would say it. Prefer **replacing** an
     existing word/sentence with one that uses the new vocabulary over just
     appending lines, but keep every story **above 20 words** and keep the tone
     natural.
   - Add each used word to the conversation's `words` focus list, bringing the
     list into the **20-30** range.
   - Add the matching Persian `translation` for every line you add or change.
   - Recompute `estimatedDuration`:
     `seconds = total_english_words / 140 * 60 + number_of_sentences`,
     `estimatedDuration = max(1, round(seconds / 60))`.
   - Keep the scenario natural, adult, and consistent.
5. **Log every added word** to `added_vocabs.csv` (`word,conversation_file`).
6. **Add every added word** to `vocabs/a1_vocabs.txt` too, so the master used-word
   list stays complete and future runs won't reuse the word elsewhere.
7. **Record the conversation in `progress.csv`** (`done` if you added words,
   `skipped` if it already had enough) so the next run moves on to the next one.

## Definition of done

Every conversation in `a1/` teaches roughly 20-30 new vocabs in its `words` list,
each word is used naturally in the dialogue with a matching Persian translation,
`estimatedDuration` is recomputed, and every word this task added is recorded in
both `added_vocabs.csv` and `vocabs/a1_vocabs.txt`.

## Notes

- Never reuse a word that's already in `vocabs/a1_vocabs.txt` — added words must
  be new to the whole A1 set.
- It's fine to touch a conversation more than once across different loop runs if
  it still hasn't reached ~20-30 words.
- Any story (new or existing) must stay above 20 words — replacing words is
  preferred over adding new ones for this reason.
- Naturalness beats hitting the number: it is better to land at 20 natural words
  than to pad to 30 with forced ones.
- Don't rename files unless the title changes.
