from functools import lru_cache


class LevenshteinDistanceCalculator:

    @staticmethod
    def calculate(word_a: str, word_b: str) -> int:
        """Calculate and returns the Levenshtein distance between 2 words"""

        @lru_cache(maxsize=len(word_a) * len(word_b))
        def calc_dist(i, j):
            if i == 0 or j == 0:
                return max(i, j)
            elif word_a[i - 1] == word_b[j - 1]:
                return calc_dist(i - 1, j - 1)
            else:
                return 1 + min(
                    calc_dist(i, j - 1),
                    calc_dist(i - 1, j),
                    calc_dist(i - 1, j - 1)
                )

        return calc_dist(len(word_a), len(word_b))
