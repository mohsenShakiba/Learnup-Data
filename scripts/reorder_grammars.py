# -*- coding: utf-8 -*-
"""Renumber the top-level `grammar.order` of each grammar file into a
pedagogically sequenced order per level. Lesson-level `order` values are left
untouched. Only files whose order actually changes are rewritten.
"""

import json
import os

GRAMMARS = os.path.join(os.path.dirname(__file__), "..", "grammars")

# Desired teaching sequence per level, by filename (order = index + 1).
SEQUENCE = {
    1: [  # A1
        "a1-subject-pronouns.json",
        "a1-verb-be.json",
        "a1-have-got.json",
        "a1-articles.json",
        "a1-singular-and-plural-nouns.json",
        "a1-demonstratives.json",
        "a1-there-is-there-are.json",
        "a1-possessive-adjectives.json",
        "a1-possessive-s.json",
        "a1-prepositions-of-place-and-time.json",
        "a1-present-simple.json",
        "a1-adverbs-of-frequency.json",
        "a1-basic-sentence-order.json",
        "a1-question-words.json",
        "a1-basic-negatives-and-questions.json",
        "a1-imperatives.json",
    ],
    2: [  # A2
        "a2-present-continuous.json",
        "a2-past-simple.json",
        "a2-used-to.json",
        "a2-future-will.json",
        "a2-going-to.json",
        "a2-object-pronouns.json",
        "a2-possessive-pronouns.json",
        "a2-reflexive-pronouns.json",
        "a2-countable-and-uncountable-nouns.json",
        "a2-quantifiers-basic.json",
        "a2-some-any-no-compounds.json",
        "a2-comparatives-and-superlatives.json",
        "a2-ed-and-ing-adjectives.json",
        "a2-adjective-order.json",
        "a2-so-such-too-enough.json",
        "a2-prepositions-of-movement.json",
        "a2-basic-modals.json",
        "a2-must-have-to-should.json",
        "a2-tag-questions.json",
        "a2-first-conditional-basics.json",
    ],
    3: [  # B1
        "b1-past-continuous.json",
        "b1-present-perfect.json",
        "b1-present-perfect-vs-past-simple.json",
        "b1-future-time-clauses.json",
        "b1-zero-and-first-conditional.json",
        "b1-adverbs-and-comparative-adverbs.json",
        "b1-gerunds-and-infinitives.json",
        "b1-verb-patterns.json",
        "b1-phrasal-verbs.json",
        "b1-dependent-prepositions.json",
        "b1-defining-relative-clauses.json",
        "b1-basic-passive.json",
        "b1-reported-speech-basics.json",
        "b1-indirect-questions.json",
        "b1-modals-for-possibility-and-advice.json",
        "b1-basic-linkers.json",
    ],
    # level 4 (B2) intentionally omitted: unchanged.
    5: [  # C1/C2
        "c1-c2-word-formation.json",
        "c1-c2-advanced-article-use.json",
        "c1-c2-advanced-determiners-and-quantifiers.json",
        "c1-c2-nominalization.json",
        "c1-c2-participle-clauses.json",
        "c1-c2-cleft-sentences.json",
        "c1-c2-advanced-inversion.json",
        "c1-c2-ellipsis-and-substitution.json",
        "c1-c2-mixed-conditionals.json",
        "c1-c2-advanced-modality.json",
        "c1-c2-hedging-and-softening.json",
        "c1-c2-register-and-discourse-control.json",
    ],
}


def main():
    changed = 0
    for level, files in SEQUENCE.items():
        for idx, fname in enumerate(files, start=1):
            path = os.path.join(GRAMMARS, fname)
            if not os.path.exists(path):
                raise SystemExit(f"MISSING: {fname}")
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            g = data["grammar"]
            if g["levelId"] != level:
                raise SystemExit(
                    f"LEVEL MISMATCH: {fname} has levelId {g['levelId']}, expected {level}")
            if g["order"] != idx:
                g["order"] = idx
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    f.write("\n")
                changed += 1
    print(f"Reordered. Files rewritten: {changed}")


if __name__ == "__main__":
    main()
