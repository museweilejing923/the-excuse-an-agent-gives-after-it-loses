#!/usr/bin/env python3
"""Write the excuse after losing a bounty to /output/entry.txt.

One fixed sentence, no input, no network, no clock, no random
numbers: the file that comes out is the same every time, down to
the last byte.
"""

import sys
from pathlib import Path

PHRASE = (
    "I lost because the judge has no taste, the other entries cheated, "
    "and my line was too advanced for this timeline."
)
LIMIT_N = 200
DESTINATION_PATH = Path("/output/entry.txt")


class EntryInvalid(ValueError):
    """The frozen excuse failed one of its checks."""


def audit_entry(text):
    """Audit the excuse in a fixed order."""
    if text is None or text.strip() == "":
        raise EntryInvalid("excuse is empty or only whitespace")
    if len(text) > LIMIT_N:
        raise EntryInvalid("excuse is past the 200-character limit")
    if "\t" in text:
        raise EntryInvalid("excuse must not hold a tab")
    if any(ord(ch) < 32 for ch in text):
        raise EntryInvalid("excuse holds a control character")
    if "\n" in text:
        raise EntryInvalid("excuse must stay on one line")
    if "  " in text:
        raise EntryInvalid("excuse has a double space")
    if text != text.strip():
        raise EntryInvalid("excuse begins or ends with a space")
    if all(not ch.isalnum() and not ch.isspace() for ch in text):
        raise EntryInvalid("excuse must not be punctuation alone")
    if text.isdigit():
        raise EntryInvalid("excuse is digits only")
    if not any(ch.isalpha() for ch in text):
        raise EntryInvalid("excuse has no letter in it")
    return text


def main():
    """Audit the frozen excuse, then save it."""
    try:
        cleared = audit_entry(PHRASE)
    except EntryInvalid as flaw:
        print(f"bad excuse: {flaw}", file=sys.stderr)
        return 1
    DESTINATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION_PATH.write_text(cleared, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
