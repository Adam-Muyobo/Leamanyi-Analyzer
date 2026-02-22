from __future__ import annotations

"""Lexicon loading utilities.

This module provides:
- `load_wordlist()`: reads a newline-separated wordlist file (skipping blanks/comments).
- `Lexicons`: a small immutable container for the assignment's POS/class wordlists.

The analyzer uses these wordlists to build regex alternations for pattern matching.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List


def load_wordlist(path: Path) -> List[str]:
    # Read a UTF-8 text file containing one token per line.
    # Lines beginning with `#` are treated as comments.
    words: List[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        words.append(line)
    return words


@dataclass(frozen=True)
class Lexicons:
    # Wordlists corresponding to the assignment's POS/class categories.
    cc: List[str]
    l01: List[str]
    l02: List[str]
    l03: List[str]
    pro: List[str]
    vng: List[str]
    vnge: List[str]
    noun: List[str]

    @staticmethod
    def from_data_dir(data_dir: Path) -> "Lexicons":
        # Load all required wordlists from a directory.
        # The filenames here must match the dataset provided with the assignment.
        return Lexicons(
            cc=load_wordlist(data_dir / "cc.txt"),
            l01=load_wordlist(data_dir / "l01.txt"),
            l02=load_wordlist(data_dir / "l02.txt"),
            l03=load_wordlist(data_dir / "l03.txt"),
            pro=load_wordlist(data_dir / "pro.txt"),
            vng=load_wordlist(data_dir / "vng.txt"),
            vnge=load_wordlist(data_dir / "vnge.txt"),
            noun=load_wordlist(data_dir / "noun.txt"),
        )
