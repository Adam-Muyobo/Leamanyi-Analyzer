from __future__ import annotations

"""Regex patterns for detecting Leamanyi (Relative) structures.

This module converts the assignment's lexicons into compiled regular expressions and
searches a sentence for three supported relative-structure templates.

Key exports:
- `LeamanyiMatch`: a lightweight record of a match and its word-span.
- `find_leamanyi()`: runs all patterns and returns all matches.
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Pattern, Tuple
from lexicons import Lexicons

# CC pairs as per assignment (surface forms)
CC_PAIRS: List[Tuple[str, str]] = [
    ("yo", "o"),  # CC1 CC2
    ("ba", "ba"),  # CC3 CC3
    ("o", "o"),  # CC4 CC4
    ("le", "le"),  # CC5 CC5
    ("a", "a"),  # CC6 CC6
    ("se", "se"),  # CC7 CC7
    ("tse", "di"),  # CC8 CC9
    ("lo", "mo"),  # CC10 CC11
    ("mo", "go"),  # CC11 CC12
]


@dataclass(frozen=True)
class LeamanyiMatch:
    # Human-readable pattern label (e.g., "Pattern A (Vng)").
    pattern_name: str
    # Exact surface substring matched by the regex.
    matched_text: str
    # Start/end word indices within the normalized sentence token list.
    start_word: int
    end_word: int  # exclusive
    # Tokenized words of the matched span.
    words: List[str]


def _alt(words: List[str]) -> str:
    # Build a safe regex alternation for a list of literal tokens.
    # Sorting longer-first reduces partial matches when tokens share prefixes.
    escaped = [re.escape(w) for w in words]
    return "(?:" + "|".join(sorted(escaped, key=len, reverse=True)) + ")"


def build_patterns(lex: Lexicons) -> Dict[str, Pattern[str]]:
    # CC pairs are treated as a two-token sequence (e.g. "yo o").
    cc_pairs_alt = (
        "(?:"
        # Use a double backslash ("\\s+") so Python doesn't treat "\s" as an escape.
        + "|".join(f"(?:{re.escape(a)}\\s+{re.escape(b)})" for a, b in CC_PAIRS)
        + ")"
    )

    # Turn each lexicon list into an alternation group.
    L01 = _alt(lex.l01)
    L02 = _alt(lex.l02)
    L03 = _alt(lex.l03)

    # Single surface forms used explicitly in the assignment templates.
    CC12 = re.escape("go")
    CC5 = re.escape("le")

    # Verb/noun/pronoun alternations.
    Vng = _alt(lex.vng)
    Vnge = _alt(lex.vnge)
    Noun = _alt(lex.noun)
    PRO = _alt(lex.pro)

    # Optional segment in Pattern A: L02 CC12 L02 (with leading whitespace).
    opt_segment = f"(?:\\s+{L02}\\s+{CC12}\\s+{L02})?"

    # Compile patterns with:
    # - `(?i)` case-insensitive matching
    # - `\b` word boundaries to reduce substring matches inside longer tokens
    pat_a = re.compile(rf"(?i)\b{cc_pairs_alt}{opt_segment}\s+{Vng}\b")
    pat_b = re.compile(rf"(?i)\b{cc_pairs_alt}\s+{L01}\s+{Vnge}\b")
    pat_c = re.compile(rf"(?i)\b{cc_pairs_alt}\s+{L03}\s+{CC5}\s+(?:{Noun}|{PRO})\b")

    return {
        "Pattern A (Vng)": pat_a,
        "Pattern B (Vnge)": pat_b,
        "Pattern C (Noun|PRO)": pat_c,
    }


def find_leamanyi(sentence: str, lex: Lexicons) -> List[LeamanyiMatch]:
    # Compile patterns based on the current lexicons.
    pats = build_patterns(lex)

    # Normalize whitespace so word indexing is stable.
    normalized = " ".join(sentence.strip().split())
    words = normalized.split() if normalized else []

    results: List[LeamanyiMatch] = []
    for name, pat in pats.items():
        for m in pat.finditer(normalized):
            matched = m.group(0)

            # Convert character offsets into word offsets.
            # We count words in the prefix before the match begins.
            start_char, _ = m.span()
            prefix = normalized[:start_char].strip()
            start_word = 0 if not prefix else len(prefix.split())
            match_words = matched.split()
            end_word = start_word + len(match_words)
            results.append(
                LeamanyiMatch(name, matched, start_word, end_word, match_words)
            )

    # Sort for stable output: earliest match first; prefer longer spans at same start.
    results.sort(
        key=lambda r: (r.start_word, -(r.end_word - r.start_word), r.pattern_name)
    )
    return results
