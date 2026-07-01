#!/usr/bin/env python3
"""Import the CEFR-J vocabulary profile CSV into the Vocab table.

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
        help="Also insert words that already exist in Vocab (by case-insensitive match). Default skips them.",
    )
    return parser.parse_args()


def load_words(csv_path: Path) -> dict[str, int]:
    """Read the CSV and return {headword: lowest CEFR level int}."""
    words: dict[str, int] = {}

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            headword = row["headword"].strip()
            cefr = row["CEFR"].strip().upper()
            level = CEFR_TO_LEVEL.get(cefr)

            if not headword or level is None:
                continue

            if headword not in words or level < words[headword]:
                words[headword] = level

    return words


def fetch_existing_words(cursor) -> set[str]:
    cursor.execute('SELECT LOWER("Word") FROM "Vocab"')
    return {row[0] for row in cursor.fetchall()}


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

    words = load_words(args.csv_path)
    print(f"Parsed {len(words)} unique words from {args.csv_path.name}.")

    conn = psycopg2.connect(database_url)
    try:
        with conn:
            with conn.cursor() as cur:
                existing = set() if args.include_existing else fetch_existing_words(cur)
                to_insert = [
                    (word, level)
                    for word, level in words.items()
                    if word.lower() not in existing
                ]
                skipped = len(words) - len(to_insert)

                print(f"Skipping {skipped} word(s) already present in Vocab.")
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
    finally:
        conn.close()

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
