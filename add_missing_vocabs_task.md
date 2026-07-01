# Add Missing A1 Vocabs Task

This document describes how to work `vocabs/missing_a1_vocabs.csv` down to empty
by weaving those words into the existing `a1/` conversations. Use it together
with `agent.md` (story generation guidelines).

**Golden rule: only perfect fits get added.** A word should only be added to a
conversation if it slots into that conversation's scenario naturally — the
kind of thing a real person would actually say there. Never force a word into
a conversation just because it's on the list. If a word doesn't have an
obviously natural home, the correct outcome is to discard it (see step 6), not
to stretch a scenario or invent an awkward sentence to fit it in.

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

1. **Read `vocabs/missing_a1_vocabs.csv`** and take only the next chunk of
   words from the top — roughly 10-20 words is a good size for one batch/loop
   run; more is fine if a lot of them turn out to fit well, but don't grab
   the whole file at once. This task runs on a loop, so don't try to clear
   the whole file in one pass: process a chunk now, leave the rest for the
   next loop iteration.
2. **Filter for A1 level first, and be generous about discarding.** Only
   words that are *truly* appropriate for an A1 (absolute beginner) student —
   common, everyday, high-frequency, unambiguous vocabulary that clearly
   belongs in a beginner conversation — should ever be added. When in doubt,
   don't add it. It is always safe to discard a word: uncommon, low-frequency,
   overly specific, advanced, ambiguous, or awkward-to-use words (e.g.
   "yoghurt") should be deleted from the CSV straight away without adding them
   anywhere; see step 5. There is no quota or pressure to use every word —
   shrinking the list by discarding is just as much progress as adding a word
   to a conversation.
3. **Pick one or a few conversations** in `a1/` that are a *perfect* fit for
   some of those words in their scenario (e.g. "purple", "shopping" words fit
   `5_shopping_for_clothes.json`; "wheel", "ticket" words fit
   `21_buying_a_bus_ticket.json`). It's fine to update more than one
   conversation in the same pass when the batch's words naturally split
   across a couple of good-fit topics — but keep it to a small handful (2-3
   conversations, say), not a sweep across many files. Pick whichever
   conversation(s)' topic best matches the available words — "plausible" is
   not enough; if no conversation is a clear, natural home for a word, that
   word doesn't get added this pass (or ever — see step 6). It's expected and
   fine if not all, or even most, words in the batch fit anywhere; leave the
   rest for a later loop or discard them.
4. **Edit the conversation JSON**:
   - Add 1-3 sentences (or rework existing lines) so each chosen word is used
     naturally, the way a real person would say it. The dialogue must still
     read like a real, natural conversation — never sacrifice natural tone
     just to cram a word in; if a word can't be worked in naturally, leave it
     for another conversation or drop it per step 6.
   - Prefer **replacing** an existing word/sentence with one that uses the
     new vocabulary over simply appending new lines. Only add new sentences
     (or, rarely, a whole new story) if the story's total word count would
     stay above 20 words either way — a story must always end up with **more
     than 20 words**, so don't shrink it below that by trimming replacements
     too aggressively.
   - Add each used word to the `words` focus list (keep the list at roughly
     10-20 words per `agent.md`; if it would grow past ~20, prefer replacing a
     less useful existing focus word over letting the list balloon).
   - Add the matching Persian `translation` for every line you add or change.
   - Recompute `estimatedDuration` using the formula in `agent.md`:
     `seconds = total_english_words / 140 * 60 + number_of_sentences`,
     `estimatedDuration = max(1, round(seconds / 60))`.
   - Keep the scenario natural, adult, and consistent with the rest of the
     conversation (see `agent.md`).
5. **Remove the completed word's line(s) from `vocabs/missing_a1_vocabs.csv`.**
   Only remove a line once the word is actually present in a conversation's
   `words` list and used in the dialogue text.
6. **Most words will not need to be used, and that's fine.** Default to
   discarding: if a word isn't clearly A1-appropriate (too uncommon, too
   advanced, too niche, or ambiguous), isn't necessary, or doesn't fit
   naturally into the chosen conversation (redundant, or would force an
   awkward sentence), just delete its line from the CSV without adding it
   anywhere. Never force a bad fit just to use a word — a natural,
   truly-appropriate-word-only conversation is always better than one padded
   with marginal vocabulary. When a word's fit is questionable, discard it
   rather than stretch to include it.

## Definition of done

`vocabs/missing_a1_vocabs.csv` has no remaining word rows — every word from
the original list has either been added to some `a1/` conversation's `words`
list and dialogue (with matching translations and updated
`estimatedDuration`), or been discarded per steps 2/6 because it wasn't truly
A1-appropriate. Discarding is an expected, valid outcome for most words, not
a fallback to avoid.

## Notes

- A loop can edit a couple of conversations if the batch's words split
  naturally across them, but don't spread edits across many files at once —
  multiple words per conversation is preferred over touching many files.
- It's fine to touch a conversation more than once across different loop runs.
- New stories/conversations can be created if a batch of words doesn't fit
  any existing one, but any story (new or existing) must stay above 20 words
  — replacing words is preferred over adding new ones for this reason.
- Don't rename files unless the title changes.
