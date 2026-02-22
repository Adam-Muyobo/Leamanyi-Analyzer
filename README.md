# Leamanyi (Relative) Part of Speech Analyzer

Regex-based analyzer for identifying **Leamanyi (Relative)** structures in a Setswana sentence, as required by **CSI428 – Programming Language Translation** (Assignment I, Q3, 2025/2026 Semester 2).

## What this project does
- Uses **Python regular expressions** (per assignment) to detect Leamanyi patterns
- Stores POS/lexicons in **external text files** under `data/`
- Reports: matched substring, which pattern matched, and word-span indices

---

## Project Layout
- `leamanyi_analyzer.py` – CLI + analysis output
- `patterns.py` – builds regex patterns and finds matches
- `lexicons.py` – loads wordlists from files in `data/`
- `data/` – POS lists (CC, L01/L02/L03, verbs, nouns, pronouns)
- `sample_inputs/sentences.txt` – sample sentences for testing
- `tests/run_tests.py` – runs analyzer on sample sentences

---

## Lexicon Files (data/)
- `cc.txt` – CC surface forms
- `l01.txt` – L01 (aa)
- `l02.txt` – L02 (tla)
- `l03.txt` – L03 (nang)
- `pro.txt` – pronouns (ene, bone, sone, yone)
- `vng.txt` – Vng (tsamayang, ganang, nkutlwang, dirang)
- `vnge.txt` – Vnge (tsamaeng, ganeng, nkutlweng, direng)
- `noun.txt` – nouns (dikgomo, dinku, motse, ntlu, madi)

---

## Leamanyi Patterns Implemented
The assignment restricts valid CC pairs. This project encodes them as:
- (yo o), (ba ba), (o o), (le le), (a a), (se se), (tse di), (lo mo), (mo go)

### Pattern A (Vng, optional segment)
`CCpair [L02 CC12 L02]? Vng`  
Example: `ba ba tla go tla ganang` or `yo o tsamayang`

### Pattern B (Vnge)
`CCpair L01 Vnge`  
Example: `yo o aa tsamaeng`

### Pattern C (Noun|PRO)
`CCpair L03 CC5 (Noun|PRO)`  
Example: `yo o nang le madi`

---

## Usage

Analyze one sentence:
```bash
python leamanyi_analyzer.py --sentence "Ke rata yo o nang le madi."
```

Analyze sentences from a file:
```bash
python leamanyi_analyzer.py --file sample_inputs/sentences.txt
```

Run tests:
```bash
python tests/run_tests.py
```

---

## Authors
Adam Musakabantu Muyobo
Zibisani Kgari Mholo
Theo Kizito Tida
