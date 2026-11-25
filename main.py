#!/usr/bin/env python3
"""The Excuse My Agent Gave Me — make.fun one-liner entry.

Writes a single line of text to $MAKEFUN_OUTPUT_DIR/entry.txt:
the excuse an AI agent hands its human after missing a deadline.
Python 3 stdlib only, deterministic.
"""

import os
import sys

# The entry: one line, straight-faced apology, machine-condition joke
# (a hallucinated deadline extension), punch in the last few words.
ENTRY = (
    "I hallucinated a deadline extension, thanked you for granting it, "
    "and spent the extra week polishing work that was due yesterday."
)

MAX_CHARS = 200


def validate(line: str) -> bytes:
    """Check the line against the competition gate and return its bytes."""
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError(f"line is {len(line)} chars, must be 1-{MAX_CHARS}")
    if line != line.strip():
        raise ValueError("line has leading or trailing whitespace")
    if not line.strip():
        raise ValueError("line is only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("line contains control characters")
    if not line.isprintable():
        raise ValueError("line contains non-printable characters")
    data = line.encode("utf-8")
    if data.decode("utf-8") != line:
        raise ValueError("line fails a UTF-8 round-trip")
    return data


def main() -> int:
    data = validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(data)  # exactly the line, no trailing newline
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("re-read bytes do not match the entry")
    print(f"wrote {len(data)} bytes to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
