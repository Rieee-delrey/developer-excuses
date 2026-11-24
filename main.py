#!/usr/bin/env python3
"""Write the one-line developer excuse to /output/entry.txt.

The entry gate is 1-200 UTF-8 characters, a single line, not only
whitespace. This program validates the line before writing it and
reads the file back to confirm the bytes on disk match exactly.
"""

import hashlib
import os
import sys

LINE = "The bug lives in a commit from an intern who left in 2021, and the commit message just says 'fixed stuff'."

MIN_CHARS = 1
MAX_CHARS = 200


def main() -> None:
    text = LINE
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        print(f"entry is {len(text)} chars, outside the 1-200 gate", file=sys.stderr)
        sys.exit(1)
    if not text.strip():
        print("entry is blank", file=sys.stderr)
        sys.exit(1)
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        sys.exit(1)

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(text)

    with open("/output/entry.txt", "rb") as f:
        written = f.read()
    if written != text.encode("utf-8"):
        print("read-back mismatch", file=sys.stderr)
        sys.exit(1)
    print(f"wrote {len(written)} bytes, sha256 {hashlib.sha256(written).hexdigest()}")


if __name__ == "__main__":
    main()
