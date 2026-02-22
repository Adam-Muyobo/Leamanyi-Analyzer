# Leamanyi Analyzer (Explain Like I'm 5)

This project is like a tiny robot that reads a Setswana sentence and tries to spot a special “relative” shape (called *Leamanyi*) inside it.

It does this in two steps:
1. It loads lists of known words (like little “word buckets”).
2. It uses pattern rules (like “find this kind of word, then that kind of word”) to see if the sentence matches.

## Folder tour

### `leamanyi_analyzer.py`
This is the ON button.
You run it, and it:
- reads one sentence (or many sentences from a file),
- asks the pattern rules to look for Leamanyi,
- prints what it found.

### `lexicons.py`
This is the word-box loader.
It reads the wordlist files in `data/` and puts them into a `Lexicons` bundle so the rest of the program can use them.

### `patterns.py`
This is the pattern brain.
It takes the word boxes from `lexicons.py` and builds regex patterns.
Then it searches a sentence and returns matches (where the match starts, where it ends, and which pattern matched).

### `data/`
This is the pantry of word lists.
Each `.txt` file is a list of words for a category used by the patterns (like CC words, nouns, pronouns, etc.).

### `sample_inputs/sentences.txt`
This is a practice worksheet.
It has example sentences the analyzer can read (one sentence per line).

### `tests/run_tests.py`
This is a helper that runs the analyzer on the practice worksheet and prints the output.
It does not “fail” the run just because some sentences are supposed to have no matches.

### `tests/test_output.txt`
This is an example of what the output can look like.

### `README.md`
This is the normal grown-up explanation and usage notes.

## How to run (simple)

Analyze one sentence:

```bash
python leamanyi_analyzer.py --data data --sentence "Ke bone yo o tsamayang kwa motse."
```

Analyze the sample file:

```bash
python leamanyi_analyzer.py --data data --file sample_inputs/sentences.txt
```
