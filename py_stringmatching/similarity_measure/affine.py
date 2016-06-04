"""Affine measure"""

import numpy as np

from py_stringmatching import utils
from py_stringmatching.compat import _range
from py_stringmatching.similarity_measure.sequence_similarity_measure import \
                                                    SequenceSimilarityMeasure


def sim_ident(char1, char2):
    return int(char1 == char2)


class Affine(SequenceSimilarityMeasure):
    """Affine similarity measure class.

    Parameters:
        gap_start (float): Cost for the gap at the start (defaults to 1)
        gap_continuation (float): Cost for the gap continuation (defaults to 0.5)
        sim_score (function): Function computing similarity score between two chars, represented as strings
                              (defaults to identity).
    """
    def __init__(self, gap_start=1, gap_continuation=0.5, sim_score=sim_ident):
        self.gap_start = gap_start
        self.gap_continuation = gap_continuation
        self.sim_score = sim_score
        super(Affine, self).__init__()

    def get_raw_score(self, string1, string2):
        """
        Computes the Affine gap score between two strings.

        The Affine gap measure is an extension of the Needleman-Wunsch measure that handles the longer gaps more
        gracefully.

        For more information refer to string matching chapter in the DI book.

        Args:
            string1,string2 (str) : Input strings

        Returns:
            Affine gap score (float)

        Raises:
            TypeError : If the inputs are not strings or if one of the inputs is None.

        Examples:
            >>> aff = Affine()
            >>> aff.get_raw_score('dva', 'deeva')
            1.5
            >>> aff = Affine(gap_start=2, gap_continuation=0.5)
            >>> aff.get_raw_score('dva', 'deeve')
            -0.5
            >>> aff = Affine(gap_continuation=0.2, sim_score=lambda s1, s2: (int(1 if s1 == s2 else 0)))
            >>> aff.get_raw_score('AAAGAATTCA', 'AAATCA')
            4.4
        """
        # input validations
        utils.sim_check_for_none(string1, string2)
        utils.tok_check_for_string_input(string1, string2)

        # if one of the strings is empty return 0
        if utils.sim_check_for_empty(string1, string2):
            return 0

        gap_start = -self.gap_start
        gap_continuation = -self.gap_continuation
        m = np.zeros((len(string1) + 1, len(string2) + 1), dtype=np.float)
        x = np.zeros((len(string1) + 1, len(string2) + 1), dtype=np.float)
        y = np.zeros((len(string1) + 1, len(string2) + 1), dtype=np.float)

        # DP initialization
        for i in _range(1, len(string1) + 1):
            m[i][0] = -float("inf")
            x[i][0] = gap_start + (i - 1) * gap_continuation
            y[i][0] = -float("inf")

        # DP initialization
        for j in _range(1, len(string2) + 1):
            m[0][j] = -float("inf")
            x[0][j] = -float("inf")
            y[0][j] = gap_start + (j - 1) * gap_continuation

        # affine gap calculation using DP
        for i in _range(1, len(string1) + 1):
            for j in _range(1, len(string2) + 1):
                # best score between x_1....x_i and y_1....y_j
                # given that x_i is aligned to y_j
                m[i][j] = (self.sim_score(string1[i - 1], string2[j - 1]) +
                           max(m[i - 1][j - 1], x[i - 1][j - 1],
                               y[i - 1][j - 1]))

                # the best score given that x_i is aligned to a gap
                x[i][j] = max(gap_start + m[i - 1][j],
                              gap_continuation + x[i - 1][j])

                # the best score given that y_j is aligned to a gap
                y[i][j] = max(gap_start + m[i][j - 1],
                              gap_continuation + y[i][j - 1])

        return max(m[len(string1)][len(string2)], x[len(string1)][len(string2)],
                   y[len(string1)][len(string2)])
