# Wordlister

A CLI tool that turns a small, manually curated list of target-related words (~30 lines) into a large, mangled wordlist for password auditing and penetration testing.

Given a short input file with names, dates, keywords, etc. related to a target, Wordlister applies case mutations, leet-speak substitutions, reversals, word fusion, and numeric/year/symbol suffixes to generate thousands of realistic password candidates.

> For use in authorized penetration testing and security research only.

## Features

- Case mutations (lower, UPPER, Capitalize, sWAP)
- Leet-speak substitutions (a→4, e→3, i→1, o→0, s→5, t→7)
- Word reversal
- Word fusion (pairwise concatenation with common separators)
- Numeric, year, and symbol suffixes/prefixes
- No external dependencies (pure Python 3 standard library)
- Configurable output length and value ranges via CLI flags

## Requirements

- Python 3.7+

## Installation

```bash
git clone https://github.com/opticGH/wordlister.git
cd Wordlister
```

No dependencies to install.

## Usage

```bash
python3 wordlister.py -i input.txt -o output.txt
```

### Input format

One piece of target information per line (names, surnames, dates, pet names, teams, hobbies, etc.):

```
Mario
Rossi
Milano
1985
Juventus
pizza
```

### Options

| Flag | Description | Default |
|---|---|---|
| `-i`, `--input` | Input file path | required |
| `-o`, `--output` | Output file path | required |
| `--no-leet` | Disable leet-speak substitutions | off |
| `--no-reverse` | Disable reversed words | off |
| `--no-fusion` | Disable word fusion | off |
| `--min-len` | Minimum length of final word | 4 |
| `--max-len` | Maximum length of final word | 24 |
| `--min-year` | Minimum year for numeric suffixes | 1980 |
| `--max-year` | Maximum year for numeric suffixes | 2030 |
| `--max-fuse-pairs` | Limit on word pairs to fuse | 60 |

### Example

```bash
python3 wordlister.py -i examples/example_input.txt -o wordlist.txt --min-year 1990 --max-year 2025
```

## Testing

```bash
python3 -m unittest discover tests
```

## License

MIT — see [LICENSE](LICENSE).
