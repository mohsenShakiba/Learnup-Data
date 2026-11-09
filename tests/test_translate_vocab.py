"""Offline checks: python -m unittest discover -s tests -v"""

import argparse
import csv
import importlib.util
import io
import json
import sqlite3
import tempfile
import threading
import unittest
from contextlib import closing, redirect_stdout
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/translate_vocab.py"
SPEC = importlib.util.spec_from_file_location("translate_vocab", SCRIPT)
vocab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(vocab)


def entry(lemma="book", level="A1", parts=("noun", "verb")):
    return {
        "lemma": lemma, "level": level,
        "senses": [{
            "part_of_speech": pos, "translation_fa": "کتاب" if pos == "noun" else "رزرو کردن",
            "definition_en": "a set of printed pages" if pos == "noun" else "to reserve something",
            "example_en": "I read a book." if pos == "noun" else "Please book a table.",
            "example_fa": "من یک کتاب خواندم." if pos == "noun" else "لطفاً یک میز رزرو کنید.",
            "grammar_en": "Countable noun." if pos == "noun" else "Transitive: book something.",
            "grammar_fa": "اسم قابل شمارش." if pos == "noun" else "فعل گذرا؛ به مفعول نیاز دارد.",
            "word_forms": "plural: books" if pos == "noun" else (
                "third-person singular: books; past tense: booked; "
                "past participle: booked; present participle: booking"
            ),
            "pronunciation_uk": "/bʊk/", "pronunciation_us": "/bʊk/",
        } for pos in parts],
    }


def api_response(entries, finish_reason="end_turn"):
    return io.BytesIO(json.dumps({
        "stop_reason": finish_reason,
        "content": [{"type": "text", "text": json.dumps({"entries": entries})}],
    }).encode())


class TranslationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.args = argparse.Namespace(
            input=root / "input.csv", output=root / "output.csv", checkpoint=root / "progress.sqlite3",
            limit=None, delay=0, max_retries=1, timeout=10, workers=1,
            model="claude-sonnet-4-6", dry_run=False,
        )
        self.args.input.write_text("lemma,level\nbook,A1\nrun,A2\n", encoding="utf-8-sig")
        self.batch = [{"lemma": "book", "level": "A1"}]

    def test_ten_requests_overlap_and_results_are_saved(self):
        self.args.workers = 10
        items = [{"lemma": f"word{i}", "level": "A1"} for i in range(20)]
        barrier = threading.Barrier(10, timeout=5)
        saved = []
        caller = threading.get_ident()

        def translate(batch, key, args):
            barrier.wait()
            return [entry(batch[0]["lemma"])]

        def save(result):
            self.assertEqual(threading.get_ident(), caller)
            saved.append(result["lemma"])

        with patch.object(vocab, "translate_batch", side_effect=translate), redirect_stdout(io.StringIO()):
            vocab.translate_pending(items, "key", self.args, save)
        self.assertCountEqual(saved, [item["lemma"] for item in items])

    def test_parallel_failure_preserves_other_inflight_success(self):
        self.args.workers = 2
        barrier = threading.Barrier(2, timeout=5)
        saved = []

        def translate(batch, key, args):
            barrier.wait()
            if batch[0]["lemma"] == "book":
                raise RuntimeError("failed")
            return [entry("run", "A2")]

        with patch.object(vocab, "translate_batch", side_effect=translate), redirect_stdout(io.StringIO()), self.assertRaises(RuntimeError):
            vocab.translate_pending(vocab.load_vocabulary(self.args.input), "key", self.args, saved.append)
        self.assertEqual([item["lemma"] for item in saved], ["run"])

    def test_local_key_and_environment_precedence(self):
        with patch.object(vocab, "ROOT", self.args.input.parent), patch.dict(vocab.os.environ, {}, clear=True):
            self.assertEqual(vocab.load_api_key(), "")
            (vocab.ROOT / ".anthropic-api-key").write_text("local-key\n")
            self.assertEqual(vocab.load_api_key(), "local-key")
            with patch.dict(vocab.os.environ, {"ANTHROPIC_API_KEY": "environment-key"}):
                self.assertEqual(vocab.load_api_key(), "environment-key")

    def test_csv_bom_deduplication_and_invalid_input(self):
        self.args.input.write_text("lemma,level\nbook,a1\nbook,A1\nbook,B1\n", encoding="utf-8-sig")
        self.assertEqual(vocab.load_vocabulary(self.args.input), [
            {"lemma": "book", "level": "A1"}, {"lemma": "book", "level": "B1"},
        ])
        self.args.input.write_text("lemma,level\nbook,C2\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            vocab.load_vocabulary(self.args.input)

    def test_validation_rejects_missing_duplicate_and_mismatched_entries(self):
        for entries in ([], [entry(), entry()], [entry("other")], [entry(level="A2")]):
            with self.subTest(entries=entries), self.assertRaises(ValueError):
                vocab.validate_entries({"entries": entries}, self.batch)

    def test_validation_rejects_incomplete_or_non_persian_senses(self):
        for field, value in (("example_fa", "English only"), ("translation_fa", "book"),
                             ("definition_en", ""), ("part_of_speech", "noune")):
            invalid = entry()
            invalid["senses"][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                vocab.validate_entries({"entries": [invalid]}, self.batch)

    def test_request_uses_header_auth_and_structured_output(self):
        with patch.object(vocab, "urlopen", return_value=api_response([entry()])) as network:
            self.assertEqual(vocab.translate_batch(self.batch, "secret-key", self.args), [entry()])
        request = network.call_args.args[0]
        self.assertNotIn("secret-key", request.full_url)
        self.assertEqual(request.get_header("X-api-key"), "secret-key")
        body = json.loads(request.data)
        self.assertEqual(request.full_url, "https://api.anthropic.com/v1/messages")
        self.assertEqual(request.get_header("Anthropic-version"), "2023-06-01")
        self.assertEqual(body["model"], self.args.model)
        schema = body["output_config"]["format"]["schema"]
        self.assertFalse(schema["additionalProperties"])
        sense_schema = schema["properties"]["entries"]["items"]["properties"]["senses"]["items"]
        for field in ("grammar_en", "grammar_fa", "word_forms", "pronunciation_uk", "pronunciation_us"):
            self.assertIn(field, sense_schema["required"])
            self.assertEqual(sense_schema["properties"][field]["type"], "string")

    def test_new_dictionary_fields_cannot_be_missing_empty_or_nonstring(self):
        for field in ("grammar_en", "grammar_fa", "word_forms", "pronunciation_uk", "pronunciation_us"):
            for value in (None, " ", []):
                invalid = entry()
                invalid["senses"][0][field] = value
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    vocab.validate_entries({"entries": [invalid]}, self.batch)
            invalid = entry()
            del invalid["senses"][0][field]
            with self.subTest(missing=field), self.assertRaises(ValueError):
                vocab.validate_entries({"entries": [invalid]}, self.batch)
        invalid = entry()
        invalid["senses"][0]["grammar_fa"] = "Countable noun."
        with self.assertRaises(ValueError):
            vocab.validate_entries({"entries": [invalid]}, self.batch)

    def test_dictionary_fields_survive_checkpoint_append_and_export(self):
        expected = entry()
        # Different noun/verb pronunciations must remain attached to their senses.
        expected["senses"][0]["pronunciation_uk"] = "/ˈrek.ɔːd/"
        expected["senses"][1]["pronunciation_uk"] = "/rɪˈkɔːd/"
        with closing(vocab.open_checkpoint(self.args.checkpoint)) as db:
            with db:
                db.execute("INSERT INTO translations_v2 VALUES (?, ?, ?, ?)", (
                    "book", "A1", json.dumps(expected, ensure_ascii=False), self.args.model,
                ))
            completed = vocab.load_completed(db, self.batch)
        self.assertEqual(completed[("book", "A1")], expected)
        vocab.export_csv(self.args.output, self.batch, {})
        vocab.append_entry(self.args.output, expected)
        appended = self.args.output.read_bytes()
        vocab.export_csv(self.args.output, self.batch, completed)
        self.assertEqual(self.args.output.read_bytes(), appended)
        with self.args.output.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        for row, sense in zip(rows, expected["senses"]):
            for field in vocab.SENSE_FIELDS:
                self.assertEqual(row[field], sense[field])

    def test_legacy_checkpoint_is_preserved_and_word_regenerated_once(self):
        self.args.input.write_text("lemma,level\nbook,A1\n", encoding="utf-8")
        legacy = entry()
        for sense in legacy["senses"]:
            for field in ("grammar_en", "grammar_fa", "word_forms", "pronunciation_uk", "pronunciation_us"):
                del sense[field]
        legacy_json = json.dumps(legacy)
        with closing(sqlite3.connect(self.args.checkpoint)) as db:
            db.execute("CREATE TABLE translations_v1 (lemma TEXT, level TEXT, entry_json TEXT, model TEXT)")
            db.execute("INSERT INTO translations_v1 VALUES (?, ?, ?, ?)", ("book", "A1", legacy_json, "old-model"))
            db.commit()
        with patch.dict(vocab.os.environ, {"ANTHROPIC_API_KEY": "test-key"}), \
                patch.object(vocab, "translate_batch", return_value=[entry()]) as translate, \
                redirect_stdout(io.StringIO()):
            vocab.run(self.args)
            vocab.run(self.args)
        self.assertEqual(translate.call_count, 1)
        with closing(sqlite3.connect(self.args.checkpoint)) as db:
            self.assertEqual(db.execute("SELECT entry_json FROM translations_v1").fetchone()[0], legacy_json)
            self.assertEqual(db.execute("SELECT COUNT(*) FROM translations_v2").fetchone()[0], 1)

    def test_rate_limit_is_retried(self):
        rate_limit = HTTPError("https://example.test", 429, "rate limited", {"Retry-After": "3"}, io.BytesIO(b"quota"))
        with patch.object(vocab, "urlopen", side_effect=[rate_limit, api_response([entry()])]) as network, \
                patch.object(vocab.time, "sleep") as sleep:
            self.assertEqual(vocab.translate_batch(self.batch, "key", self.args), [entry()])
        self.assertEqual(network.call_count, 2)
        for call in network.call_args_list:
            self.assertEqual(json.loads(call.args[0].data)["model"], self.args.model)
        self.assertGreaterEqual(sleep.call_args.args[0], 3)

    def test_auth_error_is_not_retried_and_key_is_redacted(self):
        error = HTTPError("https://example.test", 403, "forbidden", {}, io.BytesIO(b"bad secret-key"))
        with patch.object(vocab, "urlopen", side_effect=error) as network, \
                self.assertRaises(RuntimeError) as caught:
            vocab.translate_batch(self.batch, "secret-key", self.args)
        self.assertNotIn("secret-key", str(caught.exception))
        self.assertEqual(network.call_count, 1)

    def test_truncated_generation_is_not_accepted(self):
        self.args.max_retries = 0
        with patch.object(vocab, "urlopen", return_value=api_response([entry()], "max_tokens")), \
                self.assertRaises(RuntimeError):
            vocab.translate_batch(self.batch, "key", self.args)

    def test_failure_exports_committed_batch_and_resume_skips_it(self):
        with patch.dict(vocab.os.environ, {"ANTHROPIC_API_KEY": "test-key"}), \
                patch.object(vocab, "translate_batch", side_effect=[
                    [entry()], RuntimeError("temporary failure"),
                ]), redirect_stdout(io.StringIO()), self.assertRaises(RuntimeError):
            vocab.run(self.args)
        with self.args.output.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 2)
        self.assertEqual({row["part_of_speech"] for row in rows}, {"noun", "verb"})
        self.assertEqual(rows[0]["translation_fa"], "کتاب")
        self.assertTrue(self.args.output.read_bytes().startswith(b"\xef\xbb\xbf"))
        with patch.dict(vocab.os.environ, {"ANTHROPIC_API_KEY": "test-key"}), \
                patch.object(vocab, "translate_batch", return_value=[entry("run", "A2")]) as translate, \
                redirect_stdout(io.StringIO()):
            self.assertEqual(vocab.run(self.args), 0)
        self.assertEqual(translate.call_args.args[0], [{"lemma": "run", "level": "A2"}])
        # Once complete, exporting needs no credentials or API calls.
        with patch.dict(vocab.os.environ, {}, clear=True), \
                patch.object(vocab, "translate_batch") as translate, redirect_stdout(io.StringIO()):
            self.assertEqual(vocab.run(self.args), 0)
        translate.assert_not_called()

    def test_limit_bounds_new_entries_and_resume_keeps_prior_entries(self):
        self.args.limit = 1
        with patch.dict(vocab.os.environ, {"ANTHROPIC_API_KEY": "test-key"}), \
                patch.object(vocab, "translate_batch", side_effect=[[entry()], [entry("run", "A2")]]) as translate, \
                redirect_stdout(io.StringIO()):
            vocab.run(self.args)
            vocab.run(self.args)
        self.assertEqual(translate.call_count, 2)
        with self.args.output.open(encoding="utf-8-sig", newline="") as handle:
            self.assertEqual(len(list(csv.DictReader(handle))), 4)

    def test_each_word_is_committed_and_exported_before_next_request(self):
        calls = []

        def translate(batch, api_key, args):
            self.assertEqual(len(batch), 1)
            item = batch[0]
            if calls:
                # A separate connection sees only committed transactions.
                with closing(sqlite3.connect(args.checkpoint)) as db:
                    self.assertEqual(db.execute("SELECT lemma FROM translations_v2").fetchall(), [("book",)])
                with args.output.open(encoding="utf-8-sig", newline="") as handle:
                    self.assertEqual([row["lemma"] for row in csv.DictReader(handle)], ["book", "book"])
            calls.append(item["lemma"])
            return [entry(item["lemma"], item["level"])]

        with patch.dict(vocab.os.environ, {"ANTHROPIC_API_KEY": "test-key"}), \
                patch.object(vocab, "translate_batch", side_effect=translate), redirect_stdout(io.StringIO()):
            self.assertEqual(vocab.run(self.args), 0)
        self.assertEqual(calls, ["book", "run"])

    def test_ctrl_c_and_partial_csv_resume_at_first_unfinished_word(self):
        with patch.dict(vocab.os.environ, {"ANTHROPIC_API_KEY": "test-key"}), \
                patch.object(vocab, "translate_batch", side_effect=[[entry()], KeyboardInterrupt]), \
                redirect_stdout(io.StringIO()), self.assertRaises(KeyboardInterrupt):
            vocab.run(self.args)
        # Simulate an abrupt stop leaving an incomplete CSV tail.
        with self.args.output.open("a", encoding="utf-8") as handle:
            handle.write('run,A2,"unfinished')

        def translate(batch, api_key, args):
            self.assertEqual(batch, [{"lemma": "run", "level": "A2"}])
            with args.output.open(encoding="utf-8-sig", newline="") as handle:
                self.assertEqual([row["lemma"] for row in csv.DictReader(handle)], ["book", "book"])
            return [entry("run", "A2")]

        with patch.dict(vocab.os.environ, {"ANTHROPIC_API_KEY": "test-key"}), \
                patch.object(vocab, "translate_batch", side_effect=translate) as translate_mock, \
                redirect_stdout(io.StringIO()):
            self.assertEqual(vocab.run(self.args), 0)
        self.assertEqual(translate_mock.call_count, 1)

    def test_dry_run_has_no_network_or_output(self):
        self.args.dry_run = True
        with patch.object(vocab, "translate_batch") as translate, redirect_stdout(io.StringIO()):
            self.assertEqual(vocab.run(self.args), 0)
        translate.assert_not_called()
        self.assertFalse(self.args.output.exists())
        self.assertFalse(self.args.checkpoint.exists())


if __name__ == "__main__":
    unittest.main()
