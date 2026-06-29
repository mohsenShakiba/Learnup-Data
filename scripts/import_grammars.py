#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import all JSON grammar files in a directory through the Learnup API."
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="Directory containing grammar .json files.",
    )
    parser.add_argument(
        "--base-url",
        default="http://localhost:5050",
        help="Learnup API base URL. Default: http://localhost:5000",
    )
    parser.add_argument(
        "--token",
        help="Optional bearer token for authenticated environments.",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Read .json files recursively.",
    )
    return parser.parse_args()


def load_payload(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("top-level JSON value must be an object")

    return data if "grammar" in data else {"grammar": data}


def post_json(url: str, payload: dict, token: str | None) -> str:
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
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

    pattern = "**/*.json" if args.recursive else "*.json"
    files = sorted(directory.glob(pattern))

    if not files:
        print(f"No JSON files found in {directory}", file=sys.stderr)
        return 1

    endpoint = urljoin(args.base_url.rstrip("/") + "/", "Admin/Import/grammars")
    failed = 0

    for path in files:
        try:
            payload = load_payload(path)
            response = post_json(endpoint, payload, args.token)
            print(f"OK     {path.name}: grammar id {response}")
        except json.JSONDecodeError as exception:
            failed += 1
            print(f"FAILED {path.name}: invalid JSON: {exception}", file=sys.stderr)
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
    print(f"Imported {imported}/{len(files)} grammar file(s).")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
