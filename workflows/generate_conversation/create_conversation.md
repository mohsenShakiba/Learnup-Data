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

1. **Vocab count.** Use **20–30 vocabs** drawn from the appropriate
   `vocabs/<level>.csv` for the course level you are writing for.
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

## Checklist before saving

- [ ] 20–30 target vocabs, all from `vocabs/<level>.csv`.
- [ ] None of the vocabs appears in an existing conversation's vocab line.
- [ ] Exactly two speakers; first turn is the woman, second is the man.
- [ ] Names used only where needed, and kept common and simple.
- [ ] Dialogue flows naturally; no word feels forced in.
- [ ] Line 1 = title, Line 2 = comma-separated vocab list, then the dialogue lines.
