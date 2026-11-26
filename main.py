"""Fortune Cookie Funnies for Engineers.

Writes one funny fortune cookie message for a software engineer to
/output/entry.txt. Pure stdlib only (os, sys).
"""

import os
import sys

LINE = "Your pull request will be approved by someone who read only the title and felt brave."
# A real fortune cookie message: short, declarative, second person, with
# its twist coming from the engineer's world of code review. The setup
# promises a blessing every engineer wants — a PR approval — and the
# punchline undercuts it: the approver read only the title and approved
# out of bravery, not understanding. Fresh angle (the brave rubber-stamp
# reviewer, not the usual deploy-on-Friday or bug-count jokes), lands on
# first read, funniest word ("brave") sitting at the end. 85 of the
# 120-character gate.

MAX_CHARS = 120


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")

    # Self-check gate: 1-120 chars, single line, not whitespace-only.
    if not LINE or not LINE.strip():
        print("gate failed: line is empty or whitespace-only", file=sys.stderr)
        return 1
    if len(LINE) > MAX_CHARS:
        print("gate failed: line is %d chars, over %d" % (len(LINE), MAX_CHARS),
              file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("gate failed: line is not a single line", file=sys.stderr)
        return 1
    # A fortune cookie message speaks to its reader: the line must open
    # in the second person, as a fortune does.
    if not LINE.startswith("Your"):
        print("gate failed: line does not open as a fortune", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # The grader collects outputs as another user: leave the file readable.
    os.chmod(path, 0o644)

    # Read-back verification: byte-exact, valid UTF-8, no trailing newline.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != LINE.encode("utf-8"):
        print("verification failed: file bytes differ", file=sys.stderr)
        return 1
    text = raw.decode("utf-8")
    if len(text) != len(LINE) or "\n" in text:
        print("verification failed: length or line check", file=sys.stderr)
        return 1
    if text.strip() != LINE or text != text.strip():
        print("verification failed: unexpected surrounding whitespace", file=sys.stderr)
        return 1

    print("wrote %s (%d chars)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
