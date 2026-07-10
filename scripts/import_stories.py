#!/usr/bin/env python3
import argparse
import mimetypes
import sys
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Import all story .txt files in a directory through the Learnup API. "
            "Each file name must start with the lesson order, like 1_meeting_someone.txt. "
            "The file format is: line 1 title, line 2 comma separated words, "
            "then one sentence per line."
        )
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="Directory containing story .txt files.",
    )
    parser.add_argument(
        "--course-id",
        type=int,
        required=True,
        help="Course id to create lessons under.",
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:5050",
        help="Learnup API base URL. Default: http://localhost:5050",
    )
    parser.add_argument(
        "--token",
        help="Optional bearer token for authenticated environments.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Read .txt files recursively.",
    )
    return parser.parse_args()


def get_lesson_order(path: Path) -> int:
    lesson_order_text = path.stem.split("_", 1)[0]

    try:
        lesson_order = int(lesson_order_text)
    except ValueError as exception:
        raise ValueError(
            "file name must start with a numeric lesson order followed by '_'"
        ) from exception

    if lesson_order <= 0:
        raise ValueError("lesson order in file name must be greater than zero")

    return lesson_order


def build_multipart(path: Path) -> tuple[bytes, str]:
    boundary = uuid.uuid4().hex
    content_type = mimetypes.guess_type(path.name)[0] or "text/plain"
    file_bytes = path.read_bytes()

    lines = [
        f"--{boundary}".encode("utf-8"),
        (
            f'Content-Disposition: form-data; name="File"; filename="{path.name}"'
        ).encode("utf-8"),
        f"Content-Type: {content_type}".encode("utf-8"),
        b"",
        file_bytes,
        f"--{boundary}--".encode("utf-8"),
        b"",
    ]

    body = b"\r\n".join(lines)
    return body, boundary


def post_file(url: str, path: Path, token: str | None) -> str:
    body, boundary = build_multipart(path)
    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Accept": "application/json",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(url, data=body, headers=headers, method="POST")

    with urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


def main() -> int:
    args = parse_args()
    directory = args.directory.resolve()

    if not directory.is_dir():
        print(f"Directory not found: {directory}", file=sys.stderr)
        return 1

    pattern = "**/*.txt" if args.recursive else "*.txt"

    def sort_key(path: Path) -> tuple[int, int, str]:
        # Files are ordered by their leading numeric id (1_, 2_, ... 10_).
        # Files without a valid numeric id are pushed to the end but still imported.
        try:
            return (0, get_lesson_order(path), path.name)
        except ValueError:
            return (1, 0, path.name)

    files = sorted(directory.glob(pattern), key=sort_key)

    if not files:
        print(f"No txt files found in {directory}", file=sys.stderr)
        return 1

    failed = 0

    for path in files:
        try:
            lesson_order = get_lesson_order(path)
            endpoint = urljoin(
                args.base_url.rstrip("/") + "/",
                f"Admin/Import/stories/{args.course_id}/{lesson_order}",
            )
            response = post_file(endpoint, path, args.token)
            print(
                f"OK     {path.name}: course id {args.course_id}, "
                f"lesson order {lesson_order}, story id {response}"
            )
        except ValueError as exception:
            failed += 1
            print(f"FAILED {path.name}: {exception}", file=sys.stderr)
        except HTTPError as exception:
            failed += 1
            details = exception.read().decode("utf-8", errors="replace")
            print(
                f"FAILED {path.name}: HTTP {exception.code} {exception.reason}: {details}",
                file=sys.stderr,
            )
        except URLError as exception:
            failed += 1
            print(f"FAILED {path.name}: request failed: {exception.reason}", file=sys.stderr)

    imported = len(files) - failed
    print(f"Imported {imported}/{len(files)} story file(s).")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
