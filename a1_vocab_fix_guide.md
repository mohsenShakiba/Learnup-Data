# A1 Vocabulary Audit — Fix Guide

Companion to `a1_vocab_audit.csv`. This explains **why** words were flagged and **what to do** about them.

## What "flagged" means

The course is **situation-ordered** (each lesson is a real-life scene), not **frequency-ordered**. That's a legitimate design — but it means every scene drags in a few words that are above true A1 priority just because the situation needs them. The CSV lists those words.

A word is flagged when its estimated level is **A2 or B1** *and* it is not core, high-frequency A1 vocabulary. Roughly three kinds show up:

1. **Abstract service/finance nouns** — `reservation`, `deposit`, `available`, `contract`, `account`. Real B1 words; common in these scenes but not A1 building blocks.
2. **Specialized signage / domain words** — `boarding`, `gate`, `platform`, `aisle`, `router`, `trim`. The learner only ever *recognizes* these on a sign or in one specific place; they don't transfer.
3. **Lower-frequency everyday words** — `weigh`, `abroad`, `ache`, `shelf`, `receipt`. Useful eventually, but not in a learner's first few hundred words.

> **Caveat on the levels.** The `est_cefr` column is my estimate based on general CEFR vocabulary banding (English Vocabulary Profile / Oxford 3000–5000 patterns), not a lookup against an authoritative database. Treat A2 flags as "borderline, your call" and B1 flags as "clearly above A1." Verify against your own reference list before acting on edits.

## Decide one thing first: what is the `words` list *for*?

The fix depends entirely on this:

- **If `words` = "new words to actively learn this lesson"** → flagged words don't belong there. Move or trim them (below).
- **If `words` = "all notable words appearing in the scene"** → flagging is informational only; just split active vs. passive so the UI can treat them differently.

Pick one and apply it consistently across all 40 lessons.

## How to fix a flagged lesson

For each flagged word, choose one of these actions:

### 1. Demote to "passive / recognition-only"
Best for signage and domain words (`boarding`, `gate`, `platform`, `aisle`, `router`). The learner should *recognize* them in context but isn't expected to produce them. Recommended: add a `passive_words` array (or a `recognition: true` flag per word) and move them out of the active `words` list.

### 2. Replace with an A1 equivalent
Where the scene can be reworded without losing meaning:
- `delay` → "the flight is **late**" (late = A1)
- `board / boarding` → "**get on** the plane" (phrasal, but simpler)
- `available` → "is there a **free** room/table?"
- `aisle` → "which **row**" or just point to the shelf item
- `trim` → "a little **cut**"

Edit both the `words` list **and** the dialogue `text`/`translation` so they stay in sync.

### 3. Keep, but flag the lesson as "stretch vocab"
For words the scene genuinely can't avoid (`passport`, `receipt`, `appointment`). Keep them, but tag the lesson so the UI/teacher knows these are above-level and can pre-teach them.

### 4. Drop entirely
For words that appear only inside a fixed phrase and aren't really being taught (e.g. `trip` in "Have a safe trip!"). Remove from `words`; the phrase still works as a chunk.

## Priority order for editing

1. **Lesson 11 (airport)** and **Lesson 31 (train station)** — heaviest concentration of above-A1 words (4 each). Best starting point.
2. **Lessons 22, 24, 32, 36** — 3 flags each.
3. Everything else — 1–2 flags; quick passes.

## Bigger structural question

If you want the course to *actually* front-load the highest-value words, situation-ordering alone won't do it — flagged words will keep leaking into A1 no matter how you order the scenes. Two options:

- **Keep situation order, manage leakage** — use the passive/active split (action 1) everywhere. Lowest effort, preserves the current design.
- **Re-sequence by frequency** — reorder the 40 scenes (and possibly swap some out) so common words land first. Higher effort, changes the whole spine.

The CSV gives you the data either way: words flagged `B1` are your leakage; the count per lesson tells you which scenes leak most.

## Suggested data-model change (optional)

```jsonc
{
  "words": ["ticket", "flight", "seat", "trip"],        // active A1 vocab
  "passive_words": ["boarding", "gate", "passport"],     // recognition-only
  "stretch": false                                        // true = lesson has above-level core vocab
}
```

This makes the flag durable in the data instead of living only in this audit.
