#!/usr/bin/env python3
"""Write one developer-excuse line to /output/entry.txt.

The line is validated before anything is written: it must be non-blank,
a single line, and within the 1-200 character gate. After writing, the
file is read back and its bytes must match the line exactly.
"""

import sys
from pathlib import Path

OUTPUT_PATH = Path("/output/entry.txt")

LINE = "The bug lives in a commit from an intern who left in 2021, and the commit message just says 'fixed stuff'."


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not LINE or not LINE.strip():
        fail("line is blank")
    if LINE != LINE.strip():
        fail("line has leading or trailing whitespace")
    if "\n" in LINE or "\r" in LINE:
        fail("line must be a single line")
    if not 1 <= len(LINE) <= 200:
        fail(f"line length {len(LINE)} is outside the 1-200 gate")

    encoded = LINE.encode("utf-8")
    if len(encoded) != len(LINE):
        fail("line must be plain ASCII so byte length equals character length")
    assert encoded == LINE.encode("ascii"), "line must be plain ASCII"

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_bytes(encoded)

    on_disk = OUTPUT_PATH.read_bytes()
    if on_disk != encoded:
        fail("bytes on disk do not match the validated line")
    if on_disk.endswith(b"\n"):
        fail("unexpected trailing newline on disk")

    print(f"wrote {len(on_disk)} bytes to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
