# Conversation Audit Loop Prompt

This file documents the prompt used by `scripts/codex_conversation_audit_loop.ps1`.

The loop runs Codex once per conversation. Each run must:

- Use `conversation_audit_plan.csv`, not `plan.csv`, to track audit progress.
- Audit exactly one `a1/NUMBER_*.json` file.
- Make only necessary naturalness fixes.
- Keep Persian translations, focus words, `Level`, and `estimatedDuration` in sync.
- Append added/removed focus-word changes to `added_words.csv` / `removed_words.csv`.
- Append `NUMBER,DATE` to `conversation_audit_plan.csv`.
- Stop after one conversation.
