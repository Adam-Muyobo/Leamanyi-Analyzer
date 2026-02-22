from __future__ import annotations

"""Command-line entry point for the Leamanyi (Relative) structure analyzer.

This script wires together:
- lexicon loading (wordlists under `data/`), and
- regex-based pattern matching (defined in `patterns.py`).

It can analyze a single sentence (`--sentence`) or a file of sentences (`--file`).
"""

import argparse
from pathlib import Path

from lexicons import Lexicons
from patterns import find_leamanyi


def analyze_sentence(sentence: str, data_dir: Path) -> int:
    # Load POS/word-class lexicons from the provided data directory.
    lex = Lexicons.from_data_dir(data_dir)

    # Run all supported Leamanyi patterns against the sentence.
    matches = find_leamanyi(sentence, lex)

    # User-facing report.
    print("Sentence:", sentence.strip())
    if not matches:
        print("Result: NO Leamanyi (Relative) structure detected.")
        return 1

    print(f"Result: FOUND {len(matches)} match(es).")
    for i, m in enumerate(matches, 1):
        # Each match includes: which pattern, the matched surface text, and word indices.
        print(f"  {i}. {m.pattern_name}")
        print(f"     Span: words[{m.start_word}:{m.end_word}]")
        print(f"     Match: {m.matched_text!r}")
        print(f"     Words: {m.words}")
    return 0


def main():
    # CLI parsing.
    ap = argparse.ArgumentParser(
        description="CSI428 Q3 Leamanyi (Relative) POS Analyzer (Regex-based)"
    )
    ap.add_argument(
        "--data",
        default="data",
        help="Directory containing POS wordlists (default: data/)",
    )

    # Exactly one input mode is required.
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--sentence", help="Analyze a single Setswana sentence")
    g.add_argument(
        "--file", help="Path to a text file containing sentences (one per line)"
    )
    args = ap.parse_args()

    # Resolve the directory containing the assignment wordlists.
    data_dir = Path(args.data)

    if args.sentence:
        # Single sentence mode.
        raise SystemExit(analyze_sentence(args.sentence, data_dir))

    # File mode: read sentences line-by-line.
    path = Path(args.file)
    exit_code = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        # Treat blank lines and comments as separators/notes.
        if not line.strip() or line.strip().startswith("#"):
            continue
        code = analyze_sentence(line, data_dir)

        # Keep the highest (worst) exit code across all sentences.
        exit_code = max(exit_code, code)
        print("-" * 80)
    raise SystemExit(exit_code)


if __name__ == "__main__":
    # Allow `python leamanyi_analyzer.py ...` execution.
    main()
