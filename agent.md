# Story Generation Guidelines

Use these rules when creating or updating stories in this project.

## Goal

Create short English lessons for A1 English students. 

## File Format

Each conversation file should use this structure:

```json
{
    "title": "your awesome title",
    "description": "گفتگو با یک پزشک",
    "words": ["hi", "help"],
    "grammarId": 1 | null,
    "Level": "A1",
    "sentences" [
        {
            "order": 0,
            "person": 1,
            "text": "hi there",
            "translation": "سلام"
        },
        {
            "order": 1,
            "person": 2,
            "text": "hi, how can I help you",
            "translation": "سلام، چطور میتونم کمکتون کنم؟"
        },
    ]
}
```

Use the conversation number in the title. If the title changes, rename the file so the filename matches the new title, for example:

`1_warking_at_a_pet.json`

## Rules

- The conversation should be something people actually say in real world.
- The conversation is written for adult students so avoid childish scenarios.
- Use named characters when helpful.
- Use roughly 20 vocabulary words for each conversation, these dont include common vocabs like where, you, too or anything too common.
- Use any words associated with previous stories, for example if writing conversation #10 you can use all words from stories 1-9
- Use any common words, from common.csv
- It is okay to reuse words from other stories when needed.
- Keep the focus vocabulary list exactly aligned with the conversation's CSV entries.
- If replacing a conversation, remove the old `conversation id` from words that are no longer focus vocabulary for that conversation.
- Use an expression from `expressions.csv` if possible.
- Connect each story to 


## A1 Language Style

- Use short sentences.
- Use common grammar and simple verb forms.
- Use simple words based on conversation id, for example for conversation 1 use really easy and common words and for conversation 100 use hard words.
- Keep paragraphs short.


## Before Finishing

Check that:

- The conversation title, theme, focus vocabulary, and conversation text are present.
- The focus vocabulary list has 10-20 words.
- The conversation is understandable for an A1 student.
- The conversation filename matches the title.
