# Add Missing A1 Vocabs Task

This document describes how to work `vocabs/missing_a1_vocabs.csv` down to empty
by weaving those words into the existing `a1/` conversations. Use it together
with `agent.md` (story generation guidelines).

## Tracking (`vocabs/missing_a1_vocabs.csv`)

The file lists words that should appear somewhere in the A1 conversations but
currently don't, one per line:

```
NUMBER<TAB>WORD
```

This file **is** the progress tracker. There is no separate status column —
when a word has been added to a conversation, **delete its line from the
CSV**. The task is done when the file is empty (or contains only a header/no
rows).

The conversation files live in `a1/` (40 files, e.g. `8_at_the_doctor.json`).

## How to do one batch

1. **Read `vocabs/missing_a1_vocabs.csv`** and take the next chunk of words
   from the top (e.g. 5-10 words — enough to naturally fit one conversation,
   not so many that the conversation feels stuffed).
2. **Pick a conversation** in `a1/` that could plausibly use some of those
   words in its scenario (e.g. "purple", "shopping" words fit
   `5_shopping_for_clothes.json`; "wheel", "ticket" words fit
   `21_buying_a_bus_ticket.json`). It's fine to spread one batch across more
   than one conversation, or to pick whichever conversation's topic best
   matches the available words — don't force unrelated words into a bad fit.
3. **Edit the conversation JSON**:
   - Add 1-3 sentences (or rework existing lines) so each chosen word is used
     naturally, the way a real person would say it.
   - Add each used word to the `words` focus list (keep the list at roughly
     10-20 words per `agent.md`; if it would grow past ~20, prefer replacing a
     less useful existing focus word over letting the list balloon).
   - Add the matching Persian `translation` for every line you add or change.
   - Recompute `estimatedDuration` using the formula in `agent.md`:
     `seconds = total_english_words / 140 * 60 + number_of_sentences`,
     `estimatedDuration = max(1, round(seconds / 60))`.
   - Keep the scenario natural, adult, and consistent with the rest of the
     conversation (see `agent.md`).
4. **Remove the completed word's line(s) from `vocabs/missing_a1_vocabs.csv`.**
   Only remove a line once the word is actually present in a conversation's
   `words` list and used in the dialogue text.
5. Not every word needs to be used. If a word isn't necessary or doesn't fit
   naturally into any conversation (too obscure, redundant, or would force an
   awkward sentence), just delete its line from the CSV without adding it
   anywhere. Don't force a bad fit just to use a word.

## Definition of done

`vocabs/missing_a1_vocabs.csv` has no remaining word rows — every word from
the original list has been added to some `a1/` conversation's `words` list
and dialogue, with matching translations and updated `estimatedDuration`.

## Notes

- Multiple words can go into the same conversation in one pass.
- It's fine to touch a conversation more than once across different loop runs.
- Don't rename files unless the title changes.
