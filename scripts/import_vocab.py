#!/usr/bin/env python3
"""Import CEFR-J or level-specific vocabulary CSVs into the Vocab table.

Requires DATABASE_URL to be set (env var or .env file), e.g.:
    DATABASE_URL=postgresql://postgres:password@host:5432/Learnup
"""
import argparse
import csv
import os
import sys
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

CEFR_TO_LEVEL = {
    "A1": 1,
    "A2": 2,
    "B1": 3,
    "B2": 4,
    "C1": 5,
    "C2": 6,
}

ENGLISH_LANGUAGE_ID = 1
DEFAULT_STATUS = 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import CEFR-J vocabulary CSV (word, CEFR level) into the Vocab table."
    )
    parser.add_argument(
        "csv_path",
        type=Path,
        nargs="?",
        default=Path(__file__).resolve().parent.parent / "vocabs" / "cefrj-vocabulary-profile-1.5.csv",
        help="Path to the cefrj-vocabulary-profile-1.5.csv file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and report what would be inserted without writing to the database.",
    )
    parser.add_argument(
        "--include-existing",
        action="store_true",
        help="Deprecated; existing words are updated rather than inserted.",
    )
    parser.add_argument(
        "--level",
        choices=CEFR_TO_LEVEL,
        metavar="CEFR",
        help="Required level for a single-column lemma CSV (for example, --level A1).",
    )
    parser.add_argument(
        "--no-update",
        action="store_true",
        help="Do not update the Level of words that already exist in Vocab. Default updates them to match the CSV.",
    )
    return parser.parse_args()


def load_words(csv_path: Path, single_column_level: str | None = None) -> dict[str, int]:
    """Read CEFR-J or one-column vocabulary CSVs as {word: lowest CEFR level}."""
    words: dict[str, int] = {}

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError("CSV must have a header row.")

        fieldnames = set(reader.fieldnames)
        is_cefrj_csv = {"headword", "CEFR"}.issubset(fieldnames)
        is_word_list = "lemma" in fieldnames
        if not is_cefrj_csv and not is_word_list:
            raise ValueError(
                "CSV must contain headword and CEFR columns, or a lemma column."
            )

        level = None
        if is_word_list and not is_cefrj_csv:
            level = CEFR_TO_LEVEL.get(single_column_level or "")
            if level is None:
                raise ValueError(
                    "A CSV with a lemma column requires a level. Use --level A1."
                )

        for row in reader:
            if is_cefrj_csv:
                headword = row["headword"].strip()
                cefr = row["CEFR"].strip().upper()
                word_level = CEFR_TO_LEVEL.get(cefr)
            else:
                headword = row["lemma"].strip()
                word_level = level

            if not headword or word_level is None:
                continue

            if headword not in words or word_level < words[headword]:
                words[headword] = word_level

    return words


def fetch_existing_words(cursor) -> dict[str, int]:
    """Return {lower(word): current Level} for every row in Vocab."""
    cursor.execute('SELECT LOWER("Word"), "Level" FROM "Vocab"')
    return {row[0]: row[1] for row in cursor.fetchall()}


def main() -> int:
    args = parse_args()

    if not args.csv_path.is_file():
        print(f"CSV file not found: {args.csv_path}", file=sys.stderr)
        return 1

    load_dotenv()
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL is not set (env var or .env file).", file=sys.stderr)
        return 1

    try:
        words = load_words(args.csv_path, args.level)
    except ValueError as error:
        print(f"Invalid CSV: {error}", file=sys.stderr)
        return 1
    print(f"Parsed {len(words)} unique words from {args.csv_path.name}.")

    conn = psycopg2.connect(database_url)
    try:
        with conn:
            with conn.cursor() as cur:
                existing = fetch_existing_words(cur)

                if args.include_existing:
                    print("--include-existing is deprecated and has no effect; existing words are updated.")

                to_insert = [
                    (word, level) for word, level in words.items() if word.lower() not in existing
                ]
                to_update = [] if args.no_update else [
                    (word, level)
                    for word, level in words.items()
                    if word.lower() in existing and existing[word.lower()] != level
                ]

                skipped = len(words) - len(to_insert) - len(to_update)

                print(f"Skipping {skipped} word(s) already present with the correct level.")
                print(f"Updating {len(to_update)} existing word(s) to match the CSV level.")
                print(f"Inserting {len(to_insert)} word(s).")

                if args.dry_run:
                    print("Dry run, no changes written.")
                    return 0

                rows = [
                    (word, level, ENGLISH_LANGUAGE_ID, DEFAULT_STATUS)
                    for word, level in to_insert
                ]
                execute_values(
                    cur,
                    'INSERT INTO "Vocab" ("Word", "Level", "LanguageId", "Status") VALUES %s',
                    rows,
                )

                if to_update:
                    execute_values(
                        cur,
                        'UPDATE "Vocab" AS v SET "Level" = data.level '
                        'FROM (VALUES %s) AS data(word, level) '
                        'WHERE LOWER(v."Word") = LOWER(data.word)',
                        to_update,
                    )
    finally:
        conn.close()

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
