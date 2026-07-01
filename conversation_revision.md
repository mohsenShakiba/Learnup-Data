# Conversation Revision Task

This document describes how to revise each conversation so it feels natural and
follows the project rules. Use it together with `agent.md` (the story generation
guidelines) and `plan.csv` (the progress tracker).

## Tracking (`plan.csv`)

`plan.csv` lists every conversation across all levels, one per line:

```
LEVEL,NUMBER,UPDATED
```

- `LEVEL` — one of `A1`, `A2`, `B1`, `B2`, `C1`.
- `NUMBER` — the conversation number (matches the file's leading number, e.g. `8_at_the_doctor.json` → `8`).
- `UPDATED` — `0` = not yet revised, `1` = revised.

Levels and counts: A1 = 40, A2 = 40, B1 = 45, B2 = 40, C1 = 30 (195 total).

The files live in the level folders: `a1/`, `a2/`, `b1/`, `b2/`, `c1/`.

## How to revise one conversation

1. **Pick the next row** in `plan.csv` where `UPDATED` is `0`.
2. **Open the matching file** in the level folder (the file whose name starts with that number).
3. **Read the whole conversation** and judge every line against one question:
   *Would a native speaker actually say this, in this situation?*
   - Replace phrasing that is grammatically correct but unnatural
     (e.g. "Do you feel hot?" → "Do you have a fever?").
   - Keep it appropriate for the level: A1 = short, simple, common words and
     verb forms; higher levels may use richer vocabulary and longer sentences.
   - Keep the scenario adult and realistic (see `agent.md`).
4. **Update the Persian `translation`** for every line you change so it still matches.
5. **Keep data consistent** when wording changes:
   - Update the `words` focus list if a focus word was added or removed
     (e.g. removed "hot", added "fever"). Keep 10–20 focus words.
   - Ensure `Level` is set correctly for the folder.
   - Recompute `estimatedDuration` if the text changed, using the formula in `agent.md`:
     `seconds = total_english_words / 140 * 60 + number_of_sentences`,
     `estimatedDuration = max(1, round(seconds / 60))`.
   - If the title changes, rename the file so the filename matches (see `agent.md`).
6. **Mark it done**: set the row's last column to `1` in `plan.csv` (e.g. `A1,8,1`).
7. Move on to the next `0` row.

## Definition of done (per conversation)

- Every line sounds like something a real person would say in that situation.
- Persian translations match the revised English.
- `words` list is 10–20 focus words and aligned with the conversation.
- `Level` and `estimatedDuration` are present and correct.
- Filename matches the title.
- The `plan.csv` row is flipped to `1`.

## Example (already done)

`A1,8` — `a1/8_at_the_doctor.json`:
- "Hello. What's the problem?" → "Hello. What's wrong?"
- "Do you feel hot?" → "Do you have a fever?"
- Focus word "hot" → "fever"; added `Level: A1`.
- Row set to `A1,8,1`.
