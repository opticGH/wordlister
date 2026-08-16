import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wordlister import extract_tokens, case_variants, leet_variants, reverse_variants, fuse_words


class TestWordlister(unittest.TestCase):

    def test_extract_tokens(self):
        lines = ["John Smith", "# comment", "", "London-1985"]
        tokens = extract_tokens(lines)
        self.assertIn("John", tokens)
        self.assertIn("Smith", tokens)
        self.assertIn("London", tokens)
        self.assertIn("1985", tokens)

    def test_case_variants(self):
        variants = case_variants("john")
        self.assertIn("john", variants)
        self.assertIn("JOHN", variants)
        self.assertIn("John", variants)

    def test_leet_variants(self):
        variants = leet_variants("password")
        self.assertTrue(any("4" in v or "0" in v or "5" in v for v in variants))

    def test_reverse_variants(self):
        variants = reverse_variants("john")
        self.assertIn("nhoj", variants)

    def test_fuse_words(self):
        fused = fuse_words(["john", "smith"], max_pairs=10)
        self.assertTrue(any("john" in f and "smith" in f for f in fused))


if __name__ == '__main__':
    unittest.main()
