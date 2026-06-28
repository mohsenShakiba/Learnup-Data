# Fix Plan for Flagged Grammars

How to read this file:

- For each flagged grammar it gives a **recommended anchor story** (the story that should host the example), the **action**, and the **exact line(s) to add** in English with a Persian translation, ready to drop into that story's `sentences` array.
- **GAP** = the structure appears nowhere in the level; you must add the line(s).
- **WEAK** = one weak/borderline example exists; add a clean, unambiguous one so the lesson has a solid anchor.
- **MANUAL** = the point is stylistic/discourse-level and cannot be verified by pattern; it needs a human judgement call. Guidance and an optional example are given.

When inserting, keep the dialogue natural: assign the line to the right `person`, give it the next `order`, and renumber following sentences if needed.

---

## A1

### #3 Basic sentence order — MANUAL (no edit needed)
This is structural: every plain statement in every story is already Subject-Verb-Object. No story uses an exotic order, so there is nothing to "find" with a pattern.
- **Action:** No edit. Designate **`1 - Meeting Someone New`** as the anchor and teach the point from its existing opening statements (e.g. "I am a teacher.", "I live in London.").

### #10 There is / There are — WEAK
Only one "there is" example exists and no clean "there are".
- **Anchor:** `a1/31_at_the_train_station.json`
- **Action:** Add one `there are` line so both forms are present.
- **Add (person 2):**
  - EN: `There are two cafes near platform one.`
  - FA: دو کافه نزدیک سکوی یک هست.

---

## A2

### #10 First conditional basics — WEAK
One example exists ("If we work together, we'll finish fast."); add a second so the pattern is unmistakable.
- **Anchor:** `a2/14_weekend_chores.json`
- **Add (person 1):**
  - EN: `If it rains, we'll clean the garage instead.`
  - FA: اگر باران بیاید، در عوض گاراژ را تمیز می‌کنیم.

---

## B1

### #5 Defining relative clauses — WEAK
The single "match" is a false positive ("I like **that** we'd both get..." — that is a conjunction, not a relative pronoun). There is no clean defining relative clause.
- **Anchor:** `b1/32_discussing_online_shopping.json`
- **Add (person 1):**
  - EN: `I always buy from a shop that has good reviews.`
  - FA: من همیشه از فروشگاهی خرید می‌کنم که نظرات خوبی دارد.

### #7 Reported speech basics — GAP
The structure appears nowhere in B1, even though it is a B1 lesson.
- **Anchor:** `b1/12_a_polite_complaint.json` (relaying what staff said fits naturally)
- **Add two lines for contrast (say/tell):**
  - EN: `The waiter said that the kitchen was busy.`
    FA: پیشخدمت گفت که آشپزخانه شلوغ است.
  - EN: `He told me that they would bring a new dish.`
    FA: او به من گفت که یک غذای جدید می‌آورند.

---

## B2

### #1 Past perfect — GAP
- **Anchor:** `b2/4_talking_about_a_regret.json` (reflection naturally needs an earlier-past)
- **Add (person 1):**
  - EN: `By the time I applied, they had already filled the position.`
  - FA: تا وقتی درخواست دادم، آن‌ها قبلاً آن موقعیت را پر کرده بودند.

### #2 Present perfect continuous — GAP
- **Anchor:** `b2/10_discussing_mental_health.json`
- **Add (person 1):**
  - EN: `I have been feeling stressed for weeks.`
  - FA: چند هفته است که احساس استرس می‌کنم.

### #3 Future continuous and future perfect — GAP
- **Anchor:** `b2/12_planning_a_community_event.json`
- **Add (person 2):**
  - EN: `By next month we will have finished the prep, and on the day I will be coordinating the volunteers.`
  - FA: تا ماه بعد آماده‌سازی را تمام خواهیم کرد، و در روزِ برنامه من داوطلبان را هماهنگ خواهم کرد.

### #4 Second conditional — WEAK
Existing line uses "could" and is borderline; add a clear `would` form.
- **Anchor:** `b2/1_discussing_a_business_proposal.json`
- **Add (person 1):**
  - EN: `If we had more time, we would test the idea first.`
  - FA: اگر زمان بیشتری داشتیم، اول ایده را آزمایش می‌کردیم.

### #5 Third conditional — GAP
- **Anchor:** `b2/4_talking_about_a_regret.json`
- **Add (person 1):**
  - EN: `If I had known earlier, I would have made a different choice.`
  - FA: اگر زودتر می‌دانستم، تصمیم دیگری می‌گرفتم.

### #6 Passive across tenses — WEAK
One borderline example; add a line that shows the passive in two tenses at once.
- **Anchor:** `b2/11_negotiating_a_contract.json`
- **Add (person 2):**
  - EN: `The contract was reviewed last week, and the final version will be sent tomorrow.`
  - FA: قرارداد هفته گذشته بررسی شد، و نسخه نهایی فردا فرستاده خواهد شد.

### #7 Non-defining relative clauses — GAP
- **Anchor:** `b2/12_planning_a_community_event.json`
- **Add (person 1):**
  - EN: `Our coordinator, who has run festivals before, will lead the team.`
  - FA: هماهنگ‌کننده ما، که قبلاً جشنواره برگزار کرده است، تیم را رهبری خواهد کرد.

### #8 Reported speech in full — GAP
- **Anchor:** `b2/11_negotiating_a_contract.json`
- **Add (person 1):**
  - EN: `He said that they had reviewed our offer and would respond by Friday.`
  - FA: او گفت که پیشنهاد ما را بررسی کرده‌اند و تا جمعه پاسخ خواهند داد.

### #9 Modal perfects — WEAK
"That must have been hard." exists; add an advice/criticism perfect for range.
- **Anchor:** `b2/38_a_self_appraisal.json`
- **Add (person 2):**
  - EN: `You should have asked for feedback sooner.`
  - FA: باید زودتر بازخورد می‌خواستی.

### #10 Wish, if only, and causatives — WEAK
A `wish` line exists but no causative. Add a causative so both halves of the lesson are covered.
- **Anchor:** `b2/4_talking_about_a_regret.json`
- **Add (person 1):**
  - EN: `Next time I will have my application checked before I send it.`
  - FA: دفعه بعد قبل از فرستادن، درخواستم را می‌دهم بررسی کنند.

---

## C1

### #1 Mixed conditionals — GAP
- **Anchor:** `c1/11_a_conversation_about_happiness.json`
- **Add (person 1):**
  - EN: `If I had saved more when I was young, I would be more relaxed now.`
  - FA: اگر در جوانی بیشتر پس‌انداز کرده بودم، الان آرام‌تر بودم.

### #2 Advanced inversion — GAP
- **Anchor:** `c1/12_critiquing_a_policy.json`
- **Add (person 1):**
  - EN: `Not only does the policy raise costs, but it also ignores small businesses.`
  - FA: این سیاست نه‌تنها هزینه‌ها را بالا می‌برد، بلکه کسب‌وکارهای کوچک را هم نادیده می‌گیرد.

### #3 Cleft and pseudo-cleft sentences — WEAK
A pseudo-cleft ("What I'm proposing is...") exists; add an `it`-cleft for the other half.
- **Anchor:** `c1/1_a_strategic_business_discussion.json`
- **Add (person 1):**
  - EN: `It was the timing, not the idea, that worried me.`
  - FA: این زمان‌بندی بود، نه ایده، که مرا نگران می‌کرد.

### #4 Ellipsis and substitution — GAP
- **Anchor:** `c1/10_the_future_of_work.json`
- **Add as a two-line exchange:**
  - EN (person 1): `I expect a lot of change.`
    FA: انتظار تغییر زیادی دارم.
  - EN (person 2): `So do I — and sooner than most people think.`
    FA: من هم همینطور — و زودتر از آنچه بیشتر مردم فکر می‌کنند.

### #7 Nominalization — MANUAL
Not a single-sentence pattern; it is a register choice (turning verbs/clauses into noun phrases). A human should convert one or two verb-heavy lines into nominalized style.
- **Anchor:** `c1/12_critiquing_a_policy.json`
- **Example transformation:** "They implemented the policy badly and everyone got confused." -> use the nominalized version below.
  - EN: `The poor implementation of the policy caused widespread confusion.`
  - FA: اجرای ضعیف این سیاست باعث سردرگمی گسترده شد.

### #8 Participle clauses — WEAK
"Having lived abroad..." exists; add a past-participle clause for variety.
- **Anchor:** `c1/19_reflecting_on_reinvention.json`
- **Add (person 1):**
  - EN: `Faced with redundancy, I decided to retrain.`
  - FA: روبه‌رو با تعدیل نیرو، تصمیم گرفتم دوباره آموزش ببینم.

### #10 Register and discourse control — MANUAL
Not a grammatical form but control of formality and discourse markers across a turn. A human should confirm the anchor story actually shifts register or signposts, and add markers if not.
- **Anchor:** `c1/12_critiquing_a_policy.json`
- **Optional additions (discourse signposting):**
  - EN: `That said, the intention behind it is sound.`
    FA: با این حال، نیتِ پشت آن درست است.
  - EN: `To sum up, the goal is right but the method is flawed.`
    FA: در مجموع، هدف درست است اما روش ایراد دارد.

---

## Summary of work

| Category | Count | Effort |
|----------|-------|--------|
| GAP (must add example) | 10 | ~1-2 lines each |
| WEAK (add a cleaner example) | 9 | ~1 line each |
| MANUAL (human review) | 3 | judgement + optional line |

All other 28 grammars already have a solid anchor in `grammar_story_mapping.md` and need no story edits.
