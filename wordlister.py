#!/usr/bin/env python3
"""
Wordlister - Generates targeted wordlists from a file of words/info about the target.

Usage:
    python3 wordlister.py -i input.txt -o output.txt
    python3 wordlister.py -i input.txt -o output.txt --no-leet --no-fusion
    python3 wordlister.py -i input.txt -o output.txt --min-len 6 --max-len 20 --min-year 1970 --max-year 2030
"""

import argparse
import itertools
import re
import sys

LEET_MAP = {
    'a': ['a', '4', '@'],
    'e': ['e', '3'],
    'i': ['i', '1', '!'],
    'o': ['o', '0'],
    's': ['s', '5', '$'],
    't': ['t', '7'],
}

SEPARATORS = ['', '_', '.', '-']
SYMBOLS = ['', '!', '!!', '?', '#', '.', '*']


def extract_tokens(lines):
    tokens = set()
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = re.split(r'[^a-zA-Z0-9]+', line)
        for p in parts:
            if p:
                tokens.add(p)
    return sorted(tokens)


def case_variants(word):
    variants = {word, word.lower(), word.upper(), word.capitalize()}
    if len(word) > 1:
        variants.add(word[0].upper() + word[1:].lower())
        variants.add(word.swapcase())
    return variants


def leet_variants(word, max_variants=6):
    variants = set()
    lower = word.lower()

    full_leet = lower
    for k, subs in LEET_MAP.items():
        full_leet = full_leet.replace(k, subs[1] if len(subs) > 1 else k)
    variants.add(full_leet)

    count = 0
    for k, subs in LEET_MAP.items():
        if k in lower and len(subs) > 1:
            variants.add(lower.replace(k, subs[1], 1))
            count += 1
        if count >= max_variants:
            break

    return variants


def reverse_variants(word):
    return {word[::-1]}


def fuse_words(tokens, max_pairs=60):
    fused = set()
    pairs = list(itertools.permutations(tokens, 2))[:max_pairs]
    for w1, w2 in pairs:
        for sep in SEPARATORS:
            fused.add(f"{w1}{sep}{w2}")
    return fused


def add_numbers_symbols(word, min_year, max_year, max_numbers=15):
    results = {word}

    for n in list(range(0, 10)) + list(range(0, 100, 10)) + [1, 12, 123, 1234, "007"]:
        results.add(f"{word}{n}")
        if len(results) > max_numbers:
            break

    for year in range(min_year, max_year + 1, 1):
        results.add(f"{word}{year}")

    for sym in SYMBOLS:
        if sym:
            results.add(f"{word}{sym}")
            results.add(f"{sym}{word}")

    return results


def generate_wordlist(tokens, args):
    all_words = set()

    base_pool = set()
    for t in tokens:
        base_pool |= case_variants(t)

    all_words |= base_pool

    if not args.no_leet:
        leet_pool = set()
        for w in list(base_pool):
            leet_pool |= leet_variants(w)
        all_words |= leet_pool
        base_pool |= leet_pool

    if not args.no_reverse:
        reverse_pool = set()
        for w in list(base_pool):
            reverse_pool |= reverse_variants(w)
        all_words |= reverse_pool

    if not args.no_fusion:
        fused = fuse_words(tokens, max_pairs=args.max_fuse_pairs)
        all_words |= fused
        for f in list(fused)[:200]:
            all_words |= case_variants(f)

    numbered = set()
    for w in list(all_words):
        numbered |= add_numbers_symbols(w, args.min_year, args.max_year)
    all_words |= numbered

    final = {w for w in all_words if args.min_len <= len(w) <= args.max_len}

    return sorted(final)


def main():
    parser = argparse.ArgumentParser(description="Wordlister - generates targeted wordlists from target info.")
    parser.add_argument('-i', '--input', required=True, help="Input file (lines with words/info about the target)")
    parser.add_argument('-o', '--output', required=True, help="Output file (generated wordlist)")
    parser.add_argument('--no-leet', action='store_true', help="Disable leet-speak substitutions")
    parser.add_argument('--no-reverse', action='store_true', help="Disable reversed words")
    parser.add_argument('--no-fusion', action='store_true', help="Disable word fusion")
    parser.add_argument('--min-len', type=int, default=4, help="Minimum length of final word")
    parser.add_argument('--max-len', type=int, default=24, help="Maximum length of final word")
    parser.add_argument('--min-year', type=int, default=1980, help="Minimum year for numeric suffixes")
    parser.add_argument('--max-year', type=int, default=2030, help="Maximum year for numeric suffixes")
    parser.add_argument('--max-fuse-pairs', type=int, default=60, help="Limit on word pairs to fuse")

    args = parser.parse_args()

    try:
        with open(args.input, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[!] File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    tokens = extract_tokens(lines)
    if not tokens:
        print("[!] No valid tokens found in the input file.", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Tokens extracted: {len(tokens)}")
    wordlist = generate_wordlist(tokens, args)

    with open(args.output, 'w', encoding='utf-8') as f:
        for w in wordlist:
            f.write(w + '\n')

    print(f"[+] Wordlist generated: {len(wordlist)} unique passwords -> {args.output}")


if __name__ == '__main__':
    main()
