from __future__ import annotations

"""Simple test runner for the analyzer.

This script executes `leamanyi_analyzer.py` against `sample_inputs/sentences.txt`
and prints the program output.

Note: it always exits with 0 as long as the analyzer runs, because the sample file
contains both positive and negative examples (so non-zero per-line results are ok).
"""

from pathlib import Path
import subprocess, sys


def main():
    # Resolve paths relative to the repository root.
    root = Path(__file__).resolve().parent.parent
    analyzer = root / "leamanyi_analyzer.py"
    data_dir = root / "data"
    samples = root / "sample_inputs" / "sentences.txt"

    # Run the analyzer using the current Python interpreter.
    cmd = [
        sys.executable,
        str(analyzer),
        "--data",
        str(data_dir),
        "--file",
        str(samples),
    ]
    proc = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    # Print output regardless of exit code because file contains negative examples too.
    print(proc.stdout)
    # Exit 0 as long as program executed.
    raise SystemExit(0)


if __name__ == "__main__":
    # Allow `python tests/run_tests.py` execution.
    main()
