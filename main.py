#!/usr/bin/env python3
"""Entry for make.fun bounty "The Excuse an AI Agent Gives Its Human".

Writes one line of text (the excuse) to entry.txt in the output directory.
Pure standard library, deterministic: every run writes the same bytes.
"""

import os
import sys

# The excuse itself: one line, 51 characters, well under the 200-character
# gate. Winner of the 40-candidate pairwise tournament in candidates.md:
# a recursive loop (the apology for the delay is throttled by the same limit
# that caused the delay), told with zero wasted words.
EXCUSE = "I hit my rate limit apologizing for the last delay."


def output_candidates():
    """Yield output directories in the order they should be tried."""
    seen = set()
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    for path in (env_dir, "/output", os.path.join(os.getcwd(), "output"), os.getcwd()):
        if path and path not in seen:
            seen.add(path)
            yield path


def main():
    payload = (EXCUSE + "\n").encode("utf-8")
    errors = []
    for directory in output_candidates():
        try:
            os.makedirs(directory, exist_ok=True)
            target = os.path.join(directory, "entry.txt")
            with open(target, "wb") as handle:
                handle.write(payload)
            return 0
        except OSError as exc:  # try the next candidate directory
            errors.append(f"{directory}: {exc}")
    for line in errors:
        print(line, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
