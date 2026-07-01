# PRD: Placement Test

## Overview
A short, self-scoring quiz that determines a learner's CEFR level (A1–C2) so the app can
route them to lessons matched to their ability. Content lives in `placement_test.json`.
UI text is Persian; test questions are in English.

## Goal
Place each learner at the correct starting level in one sitting, with no teacher required.

## Non-Goals
- Not a full proficiency exam (no writing, speaking, or listening).
- No adaptive/branching logic in v1 — questions are fixed and ordered.

## User Story
As a new learner, I answer a set of increasingly hard questions and immediately see my
level, so I start at lessons that are neither too easy nor too hard.

## Requirements

### Content
- 24 multiple-choice questions, 4 per CEFR band (A1, A2, B1, B2, C1, C2).
- Ordered easy → hard.
- Each question: `id`, `level`, `skill` (`grammar` | `vocabulary`), `prompt`,
  `options` (4), `answer` (must exactly match one option).
- Distractors are plausible near-misses, not obvious throwaways.

### Scoring
- Count correct answers per band.
- Place learner at the **highest band** where they answer **≥3 of 4** correct,
  **provided all lower bands are also passed**.
- A learner passing no band is placed at A1.

### UX
- Show instructions before starting.
- One question at a time; single-select; no going back required.
- Display final level on completion.

## Data Schema
```json
{
  "title": "string",
  "description": "string (Persian)",
  "instructions": "string",
  "scoring": {
    "method": "string",
    "bands": [{ "level": "A1", "questions": "1-4" }],
    "rule": "string"
  },
  "questions": [
    {
      "id": 1,
      "level": "A1",
      "skill": "grammar | vocabulary",
      "prompt": "string",
      "options": ["...", "...", "...", "..."],
      "answer": "string (matches one option)"
    }
  ]
}
```

## Acceptance Criteria
- File validates against the schema; every `answer` matches an option exactly.
- Exactly 24 questions, 4 per band, in ascending difficulty.
- Scoring produces a single deterministic level for any answer set.
- Result maps to a valid starting lesson band.

## Future
- Adaptive item selection to shorten the test.
- Add listening/reading item types.
- Store results to skip already-mastered lessons.
