# Simplify Conversation Workflow

Convert every `a1/*.json` conversation into a plain text file in `a1_simp/`
containing only the title, vocabulary, and English dialogue.

## Contract

- Input: `a1/<name>.json`
- Output: `a1_simp/<name>.txt`
- Create `a1_simp/` if missing.
- Output is plain text, not JSON or Markdown.
- Do not modify files in `a1/`.

Each output file must use this exact shape:

```text
Title Without Number Prefix
vocab one, vocab two, vocab three
First speaker turn.
Second speaker turn.
First speaker turn again.
```

## Extraction Rules

- Title: read `title`, remove a leading number prefix, then trim whitespace.
- Vocab: read `words`, preserve order, join with `, `.
- Dialogue: read only `sentences[].text`, sorted by `sentences[].order`.
- Ignore all other fields, including `description`, `translation`, `Level`, and
  `estimatedDuration`.

Remove title prefixes matching these forms:

```text
1 - Meeting Someone New -> Meeting Someone New
1. Meeting Someone New  -> Meeting Someone New
1_Meeting Someone New   -> Meeting Someone New
1 Meeting Someone New   -> Meeting Someone New
```

## Dialogue Merge Rule

Build output dialogue lines in sorted sentence order:

1. Start with no current speaker.
2. For each sentence, trim `text`.
3. If `person` is the same as the previous sentence's `person`, append the text
   to the current output line with one space.
4. If `person` changes, start a new output line.
5. Preserve original punctuation and capitalization.

Do not output speaker labels, person IDs, order numbers, bullets, translations,
or blank lines between turns.

## Example

Input:

```json
{
  "title": "1 - Meeting Someone New",
  "words": ["hi", "name", "meet"],
  "sentences": [
    {"order": 0, "person": 1, "text": "Hi, my name is Anna."},
    {"order": 1, "person": 1, "text": "What is your name?"},
    {"order": 2, "person": 2, "text": "I'm Tom. Nice to meet you."}
  ]
}
```

Output:

```text
Meeting Someone New
hi, name, meet
Hi, my name is Anna. What is your name?
I'm Tom. Nice to meet you.
```

## Done

- `a1_simp/` exists.
- Each `a1/*.json` file has exactly one matching `a1_simp/*.txt` file.
- Each output file contains one title line, one vocab line, then dialogue lines.
- Consecutive entries from the same `person` are merged.
- No metadata, Persian text, JSON syntax, speaker labels, or extra blank lines
  appear in the output.
