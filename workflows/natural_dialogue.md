# Natural Dialogue Workflow

## Required Outcome

Each conversation must sound plausible for its speakers and situation, stay within its permitted vocabulary and grammar, and introduce **at least 10 new vocabulary lemmas**. All three requirements must pass together.

Natural dialogue requires a believable reason for each response. Track what has already happened, what each speaker knows, and what concern remains. Formal and informal speech can both meet this requirement; adding contractions or casual expressions does not establish it.

Use ordinary situations that people commonly encounter: shopping, meals, commuting, household tasks, work, or making plans. A small twist is optional and should arise from the situation. Choose a fresh set of suitable vocabulary when necessary; do not preserve an unusual premise just to retain its target words.

Use this workflow alongside [Vocabulary Tracking](vocab_tracking.md) and [Grammar Progression](grammar_progression.md) whenever writing or revising a conversation.

## Plan and Draft

1. Start with an everyday situation. Establish who the speakers are, where they are, and what each wants. Give them a concrete reason to talk, such as a noise complaint, a delivery deadline, or an invitation. Use a specialized or unusual activity only when it is specifically requested.
   - Check earlier conversations at this level and lower levels for the same main problem and resolution. A familiar topic can recur, but changing the speakers, destination, or target vocabulary does not make a repeated story a new situation.
2. Read the permitted grammar inventory and earlier active lessons. Choose at least 10 unused lemmas from the level's vocabulary CSV that fit this situation. Earlier use in dialogue counts even if an earlier `Vocabulary:` line omitted the word.
3. Write the exchange around the speakers' immediate needs. Each reply should respond to the preceding turn, react to something in the scene, or introduce information the other person needs.
4. If a target word needs an unlikely question, an unrelated topic change, or an awkward phrase, replace it with another unused lemma or develop a relevant part of the situation. Keep the minimum of 10; do not pad the vocabulary line with words absent from the dialogue.
5. Finish when the speakers have a practical next step or a natural reason to stop. A joke, twist, summary, or lesson about life is optional.

## Review the Whole Exchange

Read each speaker's lines aloud in sequence, or review them as spoken turns. Ask whether these particular people would say this, at this moment, for this reason.

- **The situation after each turn:** Work out what the previous line actually said, what action occurred, and what remains unresolved. Then check why the next speaker would give this particular response. Do not invent an unmentioned action to make a reply fit.
- **Actions already completed:** An instruction to repeat something the listener has just done needs a clear purpose. In a noise complaint, "Just knock next time" is an unmotivated instruction if the neighbour has already knocked and the speaker has not explained what the offer reassures them about. Acknowledge the concern and address the noise instead.
- **Reassurance that answers the concern:** Identify what the person is apologizing for or worried about. Reassure them about that specific issue. An apology for knocking late, a complaint about music, and a fear of another argument each call for a response suited to that concern.
- **Natural wording:** Prefer familiar spoken phrases and contractions where appropriate. Allow short answers such as "Here?" or "Twice a week." Do not make every reply a complete textbook sentence. Formal wording can fit a service worker or a formal situation; slang and fillers are not required.
- **A reason for each question:** Do not make speakers ask for information they already know merely to introduce a word. A beginner in English does not need to misunderstand an obvious real-world situation.
- **Connected replies:** Check that apologies, reassurance, requests, and reactions make sense as responses. Remove repeated questions or explanations that do not change the conversation.
- **Consistent actions:** Track what the speakers can see, hear, know, and do. For example, make clear that recording begins before someone wants to keep a filmed reaction. A reply about turning music off needs an offer or action involving turning it off, rather than only lowering the volume. A neighbour at the speaker's door cannot yet confirm how quiet their own bedroom is.
- **Plausible details:** Check prices, timing, and practical arrangements. A replacement box can have its own price. A delivery estimate should not become an unexplained guarantee. If a character quotes a percentage, give them a reason to know it, such as a figure on the bill.
- **Appropriate difficulty:** Keep the scene easy to follow through concrete actions and familiar language. Recheck the grammar mapping after edits; conversational wording can still introduce an unavailable construction.

These are review questions, not a template. Do not give every lesson the same misunderstanding, number of short replies, apology, or humorous ending.

## Final Checks

1. Review the complete dialogue again after vocabulary and grammar changes. Do not approve individual sentences without checking their neighbours.
2. Verify at least 10 distinct new canonical lemmas in each lesson's actual dialogue. Check earlier active lessons for previous use, including ordinary inflections. Do not count repeated forms as separate words, or infer that a shared spelling makes an unfamiliar meaning appropriate for the level.
3. Update `Vocabulary:` and the used/missing trackers using the vocabulary workflow. A removed word returns to missing only if no active lesson still uses it.
4. Run `scripts/level_check.py` for each edited lesson. Inspect unlisted words and inflections manually, and review the title separately. The script checks word lists; it cannot judge grammar, new-word counts, or natural tone.
5. Confirm the permitted grammar manually using the progression workflow. A lesson passes only after both the language checks and the whole-exchange review pass.
