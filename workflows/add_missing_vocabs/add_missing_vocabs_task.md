# Add Missing A1 Vocabs Task

This document describes how to work `vocabs/missing_a1_vocabs.csv` down to empty
by getting **every** missing word used in an `a1/` conversation — either by
weaving it into an existing conversation or by creating a new one. Use it
together with `agent.md` (story generation guidelines).

**Goal: use all the missing vocabs.** Every word on the list should end up in
some conversation. The list is done when it is empty, and the target is to get
there by *using* words, not by dropping them.

**Naturalness still comes first.** A word only goes into a conversation where a
real person would actually say it. Never force a word into a scenario or invent
an awkward sentence to fit it. If a word has no natural home in any existing
conversation, the answer is usually to **create a new conversation** built
around a cluster of words that belong together (see the bookstore example
below), not to stretch an existing one.

## Tracking (`vocabs/missing_a1_vocabs.csv`)

The file lists words that should appear in the A1 conversations but currently
don't, one per line:

```
NUMBER<TAB>NUMBER<TAB>WORD
```

This file **is** the progress tracker. When a word has been added to a
conversation, **delete its line from the CSV**. Only remove a line once the word
is actually present in a conversation's `words` list *and* used in the dialogue
text. The task is done when the file has no remaining word rows.

The conversation files live in `a1/` (e.g. `41_at_the_bookstore.json`).

## How to do one batch

This task runs on a loop, so process a chunk now and leave the rest for the next
iteration — don't try to clear the whole file in one pass.

1. **Read `vocabs/missing_a1_vocabs.csv`** and take the next chunk from the top —
   roughly 10-20 words is a good batch size.
2. **Group the words by scenario.** Look for words that naturally cluster into a
   topic (e.g. *bookstore, dictionary, magazine, notebook, pen, newspaper,
   writer, credit card*). Those clusters are your conversations.
3. **Find a home for each word:**
   - If an existing `a1/` conversation is a natural fit for a word, use it.
   - If a cluster of words has no good existing home, **create a new
     conversation** for it (next number in sequence, following `agent.md`). This
     is the main way to absorb words that don't fit anywhere yet — new
     conversations are expected and encouraged, not a last resort.
   - Only discard a word (delete its line without using it) if it is genuinely
     not A1-appropriate — not common everyday beginner vocabulary — or is
     effectively a duplicate of a word already covered. Discarding should be the
     exception, not the default.
4. **Edit / create the conversation JSON** (see `agent.md` for the full format):
   - Use each word naturally, the way a real person would say it. Prefer
     **replacing** an existing word/sentence with one that uses the new
     vocabulary over just appending lines, but keep every story **above 20
     words**.
   - Add each used word to the `words` focus list (keep it ~10-20 words).
   - Add the matching Persian `translation` for every line you add or change.
   - Recompute `estimatedDuration`:
     `seconds = total_english_words / 140 * 60 + number_of_sentences`,
     `estimatedDuration = max(1, round(seconds / 60))`.
   - Keep the scenario natural, adult, and consistent.
5. **Remove each used word's line from `vocabs/missing_a1_vocabs.csv`.**

## Definition of done

`vocabs/missing_a1_vocabs.csv` has no remaining word rows — every word has been
added to some `a1/` conversation's `words` list and dialogue (with matching
translations and updated `estimatedDuration`), or, in the rare case it wasn't
truly A1-appropriate, discarded.

## Notes

- A single loop can edit or create a couple of conversations if the batch's
  words split naturally across them.
- It's fine to touch a conversation more than once across different loop runs.
- Any story (new or existing) must stay above 20 words — replacing words is
  preferred over adding new ones for this reason.
- Don't rename files unless the title changes.
