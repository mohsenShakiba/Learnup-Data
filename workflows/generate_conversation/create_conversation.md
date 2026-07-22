# Generating a Conversation

This guide describes how to create a new conversation for a course level (a1, a2,
b1, …). Each conversation is a short, natural dialogue that introduces a batch of
new vocabulary in context.

## File format

Each conversation lives in `courses/<level>/<n>_<snake_case_title>.txt` and has this
exact structure:

1. **Line 1** — the title (e.g. `Planning a Ski Day`).
2. **Line 2** — the comma-separated list of the new vocabs used in this
   conversation, lowercase (e.g. `ski, scared, pocket, accident, raise, …`).
3. **Line 3 onward** — the dialogue itself, one turn per line, with **no speaker
   labels**. Lines simply alternate between the two speakers.

## Rules for generation

1. **No fixed vocab count.** Do not aim for a set number of vocabs. Let the
   conversation decide naturally — write the dialogue first, then harvest whatever
   words from the appropriate `vocabs/<level>.csv` genuinely appear (see rule 8).
   The vocab line may end up short or long; a natural dialogue always wins over a
   word quota.
2. **No repeats.** Make sure the chosen vocabs have **not been used before** in any
   existing conversation of that level. Check the second line (the vocab list) of
   every existing `courses/<level>/*.txt` file and exclude any word already used.
3. **Two speakers only.** The conversation has exactly **two** speakers — no more.
4. **Fixed genders.** The **first speaker is always a woman**, and the **second
   speaker is always a man**. They alternate turns throughout.
5. **Names only when necessary.** Use names sparingly — only when the dialogue
   genuinely needs them (e.g. a first introduction). When a name is needed, use a
   **common, easy name**.
6. **Natural flow.** The conversation must read naturally, with a believable
   back-and-forth. Turns should respond to each other like real speech.
7. **Meaning over coverage.** **Do not force** vocab into the conversation. A
   natural, sensible dialogue matters more than hitting every target word. If a
   word does not fit naturally, drop it and pick another from the list.
8. **Write first, harvest second.** Do **not** start from the vocab list and bend
   the dialogue around it — that is what produces stilted lines and logical
   glitches. Instead: (a) write the natural conversation, then (b) fill the vocab
   line (line 2) with the `vocabs/<level>.csv` words that genuinely appear.
9. **Keep the body at level.** Rules 1–8 govern the vocab *line*, but the
   conversation *body* can accidentally pull in a word from a higher level (e.g. a
   b1 word in an a2 dialogue). After writing, run the level check and replace any
   flagged word with a simpler synonym:

   ```
   python scripts/level_check.py courses/<level>/<n>_<title>.txt <allowed-levels>
   ```

   `<allowed-levels>` is the comma-separated set of levels at or below the course
   level (default `a1,a2`; for a b1 conversation pass `a1,a2,b1`, and so on). The
   check reports **ABOVE LEVEL** words (must be replaced) separately from
   **UNLISTED** words (function words, names, everyday nouns not in any list —
   safe to ignore). It exits non-zero if any above-level word remains.

## Checklist before saving

- [ ] Vocab line words all come from `vocabs/<level>.csv` (no fixed count).
- [ ] None of the vocabs appears in an existing conversation's vocab line.
- [ ] Exactly two speakers; first turn is the woman, second is the man.
- [ ] Names used only where needed, and kept common and simple.
- [ ] Dialogue flows naturally; no word feels forced in.
- [ ] Line 1 = title, Line 2 = comma-separated vocab list, then the dialogue lines.
- [ ] `scripts/level_check.py` reports no ABOVE LEVEL words for the body.
