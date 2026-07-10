select v."Word", c."Code", l."Order"
from "LessonVocab"
         left join "Vocab" V on "LessonVocab"."VocabId" = V."Id"
         left join "Lesson" L on "LessonVocab"."LessonId" = L."Id"
                             left join "Course" C on L."CourseId" = C."Id"
where exists(select 1
             from "LessonVocab" lv
             where lv."LessonId" != "LessonVocab"."LessonId"
               and lv."VocabId" = "LessonVocab"."VocabId");