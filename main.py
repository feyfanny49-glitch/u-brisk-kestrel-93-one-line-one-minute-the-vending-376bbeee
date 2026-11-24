#!/usr/bin/env python3
"""Vending machine pickup line entry (hardened final version).

Writes exactly one pickup line to /output/entry.txt as UTF-8 bytes with NO
trailing newline. The write is atomic: a uniquely named temporary file in the
same directory is written, flushed and fsynced, then renamed over the target,
so the grader can never observe a partial artifact.

Before writing, the entry is checked against the competition's sealed gate:
valid UTF-8 text, 1..200 characters inclusive, and not only whitespace.
"""

import hashlib
import os
import tempfile

ENTRY = "I light up when you walk by. It's just the motion sensor. Okay, fine — it's you."
OUTPUT_PATH = "/output/entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200


def validate(text: str) -> bytes:
    """Return the exact UTF-8 payload, or raise ValueError if the gate fails."""
    payload = text.encode("utf-8")          # guarantees valid UTF-8 bytes
    decoded = payload.decode("utf-8")       # round-trip guard
    if decoded != text:
        raise ValueError("entry is not clean UTF-8 text")
    length = len(text)
    if not (MIN_CHARS <= length <= MAX_CHARS):
        raise ValueError(f"entry length {length} outside {MIN_CHARS}..{MAX_CHARS}")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return payload


def write_atomically(payload: bytes) -> None:
    """Write payload to OUTPUT_PATH atomically, with cleanup on any failure."""
    output_dir = os.path.dirname(OUTPUT_PATH)
    os.makedirs(output_dir, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(prefix=".entry-", suffix=".tmp", dir=output_dir)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, OUTPUT_PATH)
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def main() -> None:
    payload = validate(ENTRY)
    write_atomically(payload)

    digest = hashlib.sha256(payload).hexdigest()
    print(
        "entry.txt written: "
        f"{len(payload)} bytes, {len(ENTRY)} chars, sha256 {digest}"
    )


if __name__ == "__main__":
    main()
