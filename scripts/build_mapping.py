# -*- coding: utf-8 -*-
"""Rebuild grammar_story_mapping.csv from scratch.

Each grammar point is mapped to the conversation (story) in the same level that
best *demonstrates* it, based on reading every story's text. The mapping is
content-driven, not positional.

CSV columns: level, lesson_order, grammar_level, grammar_order
  - level / grammar_level : 1=a1 2=a2 3=b1 4=b2 5=c1   (always equal here)
  - lesson_order          : the conversation number (file prefix N_...)
  - grammar_order         : the grammar's order within its level

MAP[level][grammar_order] = story_number
"""

import csv, io, os

MAP = {
    # ---- Level 1 (A1) ----  grammar_order : story
    1: {
        1: 1,    # Subject pronouns        -> Meeting Someone New (I/you/we/from)
        2: 9,    # Verb be                 -> Weather (it is/was/'s)
        3: 17,   # Have got                -> Talking About Family (I have ...)
        4: 4,    # Articles                -> At a Restaurant (the menu, a salad)
        5: 6,    # Singular/plural nouns   -> Grocery Store (eggs, apples, bags)
        6: 22,   # Demonstratives          -> Post Office (this package, this letter)
        7: 12,   # There is / There are    -> Renting an Apartment (Is there a kitchen?)
        8: 10,   # Possessive adjectives   -> Hotel (your name, your key)
        9: 23,   # Possessive 's           -> Food Delivery (Tony's Pizza)
        10: 3,   # Prepositions place/time -> Directions (on Main St, at the corner)
        11: 30,  # Present simple          -> Hobbies (I like/play/love/go running)
        12: 18,  # Adverbs of frequency    -> Gym (how many times a week)
        13: 35,  # Basic sentence order    -> Planning a Trip (clear SVO statements)
        14: 5,   # Question words (wh-)    -> Shopping (What size/color, How much)
        15: 29,  # Basic negatives/quest.  -> Returning an Item (doesn't fit, Do you)
        16: 8,   # Imperatives             -> At the Doctor (Drink water, Take this)
    },
    # ---- Level 2 (A2) ----
    2: {
        1: 21,   # Present continuous      -> TV Series (are you watching ...)
        2: 1,    # Past simple             -> Last Weekend (visited/cooked/went)
        3: 6,    # Used to                 -> Hometown (grew up, it has changed)
        4: 3,    # Future with will        -> First Day at a Job (I'll show, will talk)
        5: 2,    # Going to                -> Future Plans (going to travel/learn)
        6: 29,   # Object pronouns         -> Best Friend (supports me, trust her)
        7: 36,   # Possessive pronouns     -> Pets (ownership theme)
        8: 40,   # Reflexive pronouns      -> Future Tech (drive themselves)
        9: 31,   # Countable/uncountable   -> Picnic (sandwiches, some fruit, drinks)
        10: 10,  # some/any/much/many      -> Time Off (some time, how many days)
        11: 33,  # some/any/no compounds   -> Recommendation (something Italian)
        12: 9,   # Comparatives/superlat.  -> Comparing Apartments (bigger/cheaper)
        13: 8,   # -ed / -ing adjectives   -> Discussing a Movie (exciting/boring)
        14: 22,  # Adjective order         -> Lost and Found (small black bag)
        15: 26,  # so/such/too/enough      -> Seasons (too hot, too cold)
        16: 5,   # Prepositions of movement-> Directions (go down, cross, turn)
        17: 4,   # Basic modal verbs       -> Complaint (Can I get a refund / we can)
        18: 12,  # must/have to/should     -> Healthy Habits (you should ...)
        19: 40,  # Tag questions           -> Future Tech (..., right?)
        20: 14,  # First conditional       -> Weekend Chores (If we work, we'll finish)
    },
    # ---- Level 3 (B1) ----
    3: {
        1: 9,    # Past continuous         -> Accident (I was driving when ...)
        2: 4,    # Present perfect         -> Achievement (I've finished, have you been)
        3: 26,   # Pres. perfect vs past   -> Memorable Trip (you've taken / scenery was)
        4: 31,   # Future time clauses     -> Public Transport (Until then, I'll rely)
        5: 1,    # Zero/first conditional  -> Negotiating Salary (If you accept, we'll add)
        6: 8,    # Adverbs/comparative adv -> Tech Habits (constantly, more productive)
        7: 24,   # Gerunds and infinitives -> Learning a Language (afraid of making)
        8: 33,   # Verb patterns           -> Personal Goals (want to read, trying not to)
        9: 28,   # Phrasal verbs           -> Money Habits (run out of, cut back)
        10: 14,  # Dependent prepositions  -> Performance Review (interested in)
        11: 32,  # Defining relative claus.-> Online Shopping (a shop that has reviews)
        12: 23,  # Basic passive           -> Customer Service (I was charged twice)
        13: 12,  # Reported speech basics  -> Restaurant Complaint (the waiter said that)
        14: 7,   # Indirect questions      -> Misunderstanding (that explains why I was)
        15: 6,   # Modals possibility/adv. -> Giving Advice (you should / I might)
        16: 29,  # Linkers                 -> City vs Country (though, but, I suppose)
    },
    # ---- Level 4 (B2) ----
    4: {
        1: 4,    # Past perfect            -> Regret (by the time I applied, they had)
        2: 6,    # Present perfect contin. -> Personal Finance (I've been trying to save)
        3: 12,   # Future cont. & perfect  -> Community Event (will have finished / will be)
        4: 1,    # Second conditional      -> Business Proposal (if we had time, we would)
        5: 2,    # Third conditional       -> Promotion (if you'd accepted, it might have)
        6: 15,   # Passive across tenses   -> Globalization (jobs get outsourced)
        7: 12,   # Non-defining rel. claus.-> Community Event (coordinator, who has run...)
        8: 11,   # Reported speech in full -> Contract (he said that they had reviewed)
        9: 38,   # Modal perfects          -> Self-Appraisal (I should have delegated)
        10: 4,   # Wish/if only/causatives -> Regret (I wish I'd taken / have it checked)
    },
    # ---- Level 5 (C1/C2) ----
    5: {
        1: 4,    # Word formation          -> Leadership (leadership/credibility/humility)
        2: 24,   # Advanced article use    -> Wisdom (zero article: knowledge is knowing)
        3: 30,   # Advanced determiners    -> Lifetime of Lessons (hardly any, most)
        4: 27,   # Nominalization          -> Business Strategy (assumptions, diversification)
        5: 13,   # Participle clauses      -> Identity (Having lived abroad, I feel)
        6: 1,    # Cleft / pseudo-cleft    -> Strategic Discussion (What I'm proposing is)
        7: 12,   # Advanced inversion      -> Policy Critique (Not only does the policy)
        8: 23,   # Ellipsis & substitution -> Optimism vs Realism (a cautious one)
        9: 11,   # Mixed conditionals      -> Happiness (if I'd saved, I would be now)
        10: 10,  # Advanced modality       -> Future of Work (will/must/may speculation)
        11: 9,   # Hedging and softening   -> Free Will (I admit, perhaps, may never)
        12: 7,   # Register & discourse    -> Difficult Conversation (formal, controlled)
    },
}


def main():
    rows = []
    for level in sorted(MAP):
        for gorder in sorted(MAP[level]):
            story = MAP[level][gorder]
            rows.append((level, story, level, gorder))
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["level", "lesson_order", "grammar_level", "grammar_order"])
    w.writerows(rows)
    out = os.path.join(os.path.dirname(__file__), "..", "grammar_story_mapping.csv")
    open(out, "w", encoding="utf-8", newline="").write(buf.getvalue())
    print(f"Wrote {len(rows)} rows to {os.path.abspath(out)}")


if __name__ == "__main__":
    main()
