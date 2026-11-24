#!/usr/bin/env python3
"""Fortune Cookie Wisdom for Developers -- make.fun entry.

Writes one original fortune-cookie line for a software developer to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).
Python 3.13, standard library only. Deterministic: the same bytes every run.
The line has no trailing newline: the gate counts characters exactly.
"""

import os
import stat

LINE = "You will find the bug you hunted all week waiting patiently in the line you approved without reading."


def _validate(line: str) -> None:
    assert isinstance(line, str)
    assert 1 <= len(line) <= 120, f"line must be 1-120 characters, got {len(line)}"
    assert line.strip() != "", "line must not be only whitespace"
    assert line == line.strip(), "line must not have leading or trailing whitespace"
    assert "\n" not in line and "\r" not in line, "line must be a single line with no newline"
    line.encode("utf-8")  # raises on surrogates / non-encodable content


def main() -> None:
    _validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    tmp = target + ".tmp"
    data = LINE.encode("utf-8")
    with open(tmp, "wb") as f:
        f.write(data)
    os.chmod(tmp, 0o644)
    os.replace(tmp, target)
    os.chmod(target, 0o644)
    # Read-back: prove what landed on disk is exactly the validated line.
    with open(target, "rb") as f:
        written = f.read()
    assert written == data, "read-back mismatch: entry.txt differs from LINE"
    assert stat.S_IMODE(os.stat(target).st_mode) == 0o644, "entry.txt must be mode 0644"
    _validate(written.decode("utf-8"))


if __name__ == "__main__":
    main()
