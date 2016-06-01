from __future__ import unicode_literals

import math
import unittest

from nose.tools import *


# sequence based similarity measures
from py_stringmatching.similarity_measure.affine import Affine
from py_stringmatching.similarity_measure.bag_distance import BagDistance
from py_stringmatching.similarity_measure.editex import Editex
from py_stringmatching.similarity_measure.hamming_distance import HammingDistance
from py_stringmatching.similarity_measure.jaro import Jaro
from py_stringmatching.similarity_measure.jaro_winkler import JaroWinkler
from py_stringmatching.similarity_measure.levenshtein import Levenshtein
from py_stringmatching.similarity_measure.needleman_wunsch import NeedlemanWunsch
from py_stringmatching.similarity_measure.smith_waterman import SmithWaterman
# token based similarity measures
from py_stringmatching.similarity_measure.cosine import Cosine
from py_stringmatching.similarity_measure.dice import Dice
from py_stringmatching.similarity_measure.jaccard import Jaccard
from py_stringmatching.similarity_measure.overlap_coefficient import OverlapCoefficient
from py_stringmatching.similarity_measure.soft_tfidf import SoftTfIdf
from py_stringmatching.similarity_measure.tfidf import TfIdf
from py_stringmatching.similarity_measure.tversky_index import TverskyIndex
# hybrid similarity measures
from py_stringmatching.similarity_measure.generalized_jaccard import GeneralizedJaccard
from py_stringmatching.similarity_measure.monge_elkan import MongeElkan
#phonetic similarity measures
from py_stringmatching.similarity_measure.soundex import Soundex


# ---------------------- sequence based similarity measures  ----------------------


class AffineTestCases(unittest.TestCase):
    def setUp(self):
        self.affine = Affine()
        self.affine_with_params1 = Affine(gap_start=2, gap_continuation=0.5)
        self.affine_with_params2 = Affine(gap_continuation=0.2,
                sim_score=lambda s1, s2: (int(1 if s1 == s2 else 0)))

    def test_valid_input(self):
        self.assertAlmostEqual(self.affine.get_raw_score('dva', 'deeva'), 1.5)
        self.assertAlmostEqual(self.affine_with_params1.get_raw_score('dva', 'deeve'), -0.5)
        self.assertAlmostEqual(self.affine_with_params2.get_raw_score('AAAGAATTCA', 'AAATCA'),
                               4.4)
        self.assertAlmostEqual(self.affine_with_params2.get_raw_score(' ', ' '), 1)
        self.assertEqual(self.affine.get_raw_score('', 'deeva'), 0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.affine.get_raw_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.affine.get_raw_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.affine.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.affine.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.affine.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.affine.get_raw_score(12.90, 12.90)


class BagDistanceTestCases(unittest.TestCase):
    def setUp(self):
        self.bd = BagDistance()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.bd.get_raw_score('a', ''), 1)
        self.assertEqual(self.bd.get_raw_score('', 'a'), 1)
        self.assertEqual(self.bd.get_raw_score('abc', ''), 3)
        self.assertEqual(self.bd.get_raw_score('', 'abc'), 3)
        self.assertEqual(self.bd.get_raw_score('', ''), 0)
        self.assertEqual(self.bd.get_raw_score('a', 'a'), 0)
        self.assertEqual(self.bd.get_raw_score('abc', 'abc'), 0)
        self.assertEqual(self.bd.get_raw_score('a', 'ab'), 1)
        self.assertEqual(self.bd.get_raw_score('b', 'ab'), 1)
        self.assertEqual(self.bd.get_raw_score('ac', 'abc'), 1)
        self.assertEqual(self.bd.get_raw_score('abcdefg', 'xabxcdxxefxgx'), 6)
        self.assertEqual(self.bd.get_raw_score('ab', 'a'), 1)
        self.assertEqual(self.bd.get_raw_score('ab', 'b'), 1)
        self.assertEqual(self.bd.get_raw_score('abc', 'ac'), 1)
        self.assertEqual(self.bd.get_raw_score('xabxcdxxefxgx', 'abcdefg'), 6)
        self.assertEqual(self.bd.get_raw_score('a', 'b'), 1)
        self.assertEqual(self.bd.get_raw_score('ab', 'ac'), 1)
        self.assertEqual(self.bd.get_raw_score('ac', 'bc'), 1)
        self.assertEqual(self.bd.get_raw_score('abc', 'axc'), 1)
        self.assertEqual(self.bd.get_raw_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 6)
        self.assertEqual(self.bd.get_raw_score('example', 'samples'), 2)
        self.assertEqual(self.bd.get_raw_score('sturgeon', 'urgently'), 2)
        self.assertEqual(self.bd.get_raw_score('bag_distance', 'frankenstein'), 6)
        self.assertEqual(self.bd.get_raw_score('distance', 'difference'), 5)
        self.assertEqual(self.bd.get_raw_score('java was neat', 'scala is great'), 6)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.bd.get_sim_score('a', ''), 0.0)
        self.assertEqual(self.bd.get_sim_score('', 'a'), 0.0)
        self.assertEqual(self.bd.get_sim_score('abc', ''), 0.0)
        self.assertEqual(self.bd.get_sim_score('', 'abc'), 0.0)
        self.assertEqual(self.bd.get_sim_score('', ''), 1.0)
        self.assertEqual(self.bd.get_sim_score('a', 'a'), 1.0)
        self.assertEqual(self.bd.get_sim_score('abc', 'abc'), 1.0)
        self.assertEqual(self.bd.get_sim_score('a', 'ab'), 1.0 - (1.0/2.0))
        self.assertEqual(self.bd.get_sim_score('b', 'ab'), 1.0 - (1.0/2.0))
        self.assertEqual(self.bd.get_sim_score('ac', 'abc'), 1.0 - (1.0/3.0))
        self.assertEqual(self.bd.get_sim_score('abcdefg', 'xabxcdxxefxgx'), 1.0 - (6.0/13.0))
        self.assertEqual(self.bd.get_sim_score('ab', 'a'), 1.0 - (1.0/2.0))
        self.assertEqual(self.bd.get_sim_score('ab', 'b'), 1.0 - (1.0/2.0))
        self.assertEqual(self.bd.get_sim_score('abc', 'ac'), 1.0 - (1.0/3.0))
        self.assertEqual(self.bd.get_sim_score('xabxcdxxefxgx', 'abcdefg'), 1.0 - (6.0/13.0))
        self.assertEqual(self.bd.get_sim_score('a', 'b'), 0.0)
        self.assertEqual(self.bd.get_sim_score('ab', 'ac'), 1.0 - (1.0/2.0))
        self.assertEqual(self.bd.get_sim_score('ac', 'bc'), 1.0 - (1.0/2.0))
        self.assertEqual(self.bd.get_sim_score('abc', 'axc'), 1.0 - (1.0/3.0))
        self.assertEqual(self.bd.get_sim_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 1.0 - (6.0/13.0))
        self.assertEqual(self.bd.get_sim_score('example', 'samples'), 1.0 - (2.0/7.0))
        self.assertEqual(self.bd.get_sim_score('sturgeon', 'urgently'), 1.0 - (2.0/8.0))
        self.assertEqual(self.bd.get_sim_score('bag_distance', 'frankenstein'), 1.0 - (6.0/12.0))
        self.assertEqual(self.bd.get_sim_score('distance', 'difference'), 1.0 - (5.0/10.0))
        self.assertEqual(self.bd.get_sim_score('java was neat', 'scala is great'), 1.0 - (6.0/14.0))

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.bd.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.bd.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.bd.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.bd.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.bd.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.bd.get_raw_score(12.90, 12.90)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.bd.get_sim_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.bd.get_sim_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.bd.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.bd.get_sim_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.bd.get_sim_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.bd.get_sim_score(12.90, 12.90)


class EditexTestCases(unittest.TestCase):
    def setUp(self):
        self.ed = Editex()
        self.ed_with_params1 = Editex(match_cost=2)
        self.ed_with_params2 = Editex(mismatch_cost=2)
        self.ed_with_params3 = Editex(mismatch_cost=1)
        self.ed_with_params4 = Editex(mismatch_cost=3, group_cost=2)
        self.ed_with_params5 = Editex(mismatch_cost=3, group_cost=2, local=True)
        self.ed_with_params6 = Editex(local=True)

    def test_valid_input_raw_score(self):
        self.assertEqual(self.ed.get_raw_score('MARTHA', 'MARTHA'), 0)
        self.assertEqual(self.ed.get_raw_score('MARTHA', 'MARHTA'), 3)
        self.assertEqual(self.ed.get_raw_score('ALIE', 'ALI'), 1)
        self.assertEqual(self.ed_with_params1.get_raw_score('ALIE', 'ALI'), 7)
        self.assertEqual(self.ed_with_params2.get_raw_score('ALIE', 'ALIF'), 2)
        self.assertEqual(self.ed_with_params3.get_raw_score('ALIE', 'ALIF'), 1)
        self.assertEqual(self.ed_with_params4.get_raw_score('ALIP', 'ALIF'), 2)
        self.assertEqual(self.ed_with_params4.get_raw_score('ALIe', 'ALIF'), 3)
        self.assertEqual(self.ed_with_params5.get_raw_score('WALIW', 'HALIH'), 6)
        self.assertEqual(self.ed_with_params6.get_raw_score('niall', 'nihal'), 2)
        self.assertEqual(self.ed_with_params6.get_raw_score('nihal', 'niall'), 2)
        self.assertEqual(self.ed_with_params6.get_raw_score('neal', 'nihl'), 3)
        self.assertEqual(self.ed_with_params6.get_raw_score('nihl', 'neal'), 3)
        self.assertEqual(self.ed.get_raw_score('', ''), 0)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.ed.get_sim_score('MARTHA', 'MARTHA'), 1.0)
        self.assertEqual(self.ed.get_sim_score('MARTHA', 'MARHTA'), 1.0 - (3.0/12.0))
        self.assertEqual(self.ed.get_sim_score('ALIE', 'ALI'), 1.0 - (1.0/8.0))
        self.assertEqual(self.ed_with_params1.get_sim_score('ALIE', 'ALI'), 1.0 - (7.0/8.0))
        self.assertEqual(self.ed_with_params2.get_sim_score('ALIE', 'ALIF'), 1.0 - (2.0/8.0))
        self.assertEqual(self.ed_with_params3.get_sim_score('ALIE', 'ALIF'), 1.0 - (1.0/4.0))
        self.assertEqual(self.ed_with_params4.get_sim_score('ALIP', 'ALIF'), 1.0 - (2.0/12.0))
        self.assertEqual(self.ed_with_params4.get_sim_score('ALIe', 'ALIF'), 1.0 - (3.0/12.0))
        self.assertEqual(self.ed_with_params5.get_sim_score('WALIW', 'HALIH'), 1.0 - (6.0/15.0))
        self.assertEqual(self.ed_with_params6.get_sim_score('niall', 'nihal'), 1.0 - (2.0/10.0))
        self.assertEqual(self.ed_with_params6.get_sim_score('nihal', 'niall'), 1.0 - (2.0/10.0))
        self.assertEqual(self.ed_with_params6.get_sim_score('neal', 'nihl'), 1.0 - (3.0/8.0))
        self.assertEqual(self.ed_with_params6.get_sim_score('nihl', 'neal'), 1.0 - (3.0/8.0))
        self.assertEqual(self.ed.get_sim_score('', ''), 1.0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.ed.get_raw_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.ed.get_raw_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.ed.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.ed.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.ed.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.ed.get_raw_score(12.90, 12.90)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.ed.get_sim_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.ed.get_sim_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.ed.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.ed.get_sim_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.ed.get_sim_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.ed.get_sim_score(12.90, 12.90)


class JaroTestCases(unittest.TestCase):
    def setUp(self):
        self.jaro = Jaro()

    def test_valid_input_raw_score(self):
        # https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance
        self.assertAlmostEqual(self.jaro.get_raw_score('MARTHA', 'MARHTA'),
                               0.9444444444444445)
        self.assertAlmostEqual(self.jaro.get_raw_score('DWAYNE', 'DUANE'),
                               0.8222222222222223)
        self.assertAlmostEqual(self.jaro.get_raw_score('DIXON', 'DICKSONX'),
                               0.7666666666666666)
        self.assertEqual(self.jaro.get_raw_score('', 'deeva'), 0)

    def test_valid_input_sim_score(self):
        self.assertAlmostEqual(self.jaro.get_sim_score('MARTHA', 'MARHTA'),
                               0.9444444444444445)
        self.assertAlmostEqual(self.jaro.get_sim_score('DWAYNE', 'DUANE'),
                               0.8222222222222223)
        self.assertAlmostEqual(self.jaro.get_sim_score('DIXON', 'DICKSONX'),
                               0.7666666666666666)
        self.assertEqual(self.jaro.get_sim_score('', 'deeva'), 0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.jaro.get_raw_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.jaro.get_raw_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.jaro.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.jaro.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.jaro.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.jaro.get_raw_score(12.90, 12.90)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.jaro.get_sim_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.jaro.get_sim_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.jaro.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.jaro.get_sim_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.jaro.get_sim_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.jaro.get_sim_score(12.90, 12.90)


class JaroWinklerTestCases(unittest.TestCase):
    def setUp(self):
        self.jw = JaroWinkler()

    def test_valid_input_raw_score(self):
        # https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance
        self.assertAlmostEqual(self.jw.get_raw_score('MARTHA', 'MARHTA'),
                               0.9611111111111111)
        self.assertAlmostEqual(self.jw.get_raw_score('DWAYNE', 'DUANE'), 0.84)
        self.assertAlmostEqual(self.jw.get_raw_score('DIXON', 'DICKSONX'),
                               0.8133333333333332)

    def test_valid_input_sim_score(self):
        self.assertAlmostEqual(self.jw.get_sim_score('MARTHA', 'MARHTA'),
                               0.9611111111111111)
        self.assertAlmostEqual(self.jw.get_sim_score('DWAYNE', 'DUANE'), 0.84)
        self.assertAlmostEqual(self.jw.get_sim_score('DIXON', 'DICKSONX'),
                               0.8133333333333332)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.jw.get_raw_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.jw.get_raw_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.jw.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.jw.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.jw.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.jw.get_raw_score(12.90, 12.90)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.jw.get_sim_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.jw.get_sim_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.jw.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.jw.get_sim_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.jw.get_sim_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.jw.get_sim_score(12.90, 12.90)


class LevenshteinTestCases(unittest.TestCase):
    def setUp(self):
        self.lev = Levenshtein()

    def test_valid_input_raw_score(self):
        # http://oldfashionedsoftware.com/tag/levenshtein-distance/
        self.assertEqual(self.lev.get_raw_score('a', ''), 1)
        self.assertEqual(self.lev.get_raw_score('', 'a'), 1)
        self.assertEqual(self.lev.get_raw_score('abc', ''), 3)
        self.assertEqual(self.lev.get_raw_score('', 'abc'), 3)
        self.assertEqual(self.lev.get_raw_score('', ''), 0)
        self.assertEqual(self.lev.get_raw_score('a', 'a'), 0)
        self.assertEqual(self.lev.get_raw_score('abc', 'abc'), 0)
        self.assertEqual(self.lev.get_raw_score('a', 'ab'), 1)
        self.assertEqual(self.lev.get_raw_score('b', 'ab'), 1)
        self.assertEqual(self.lev.get_raw_score('ac', 'abc'), 1)
        self.assertEqual(self.lev.get_raw_score('abcdefg', 'xabxcdxxefxgx'), 6)
        self.assertEqual(self.lev.get_raw_score('ab', 'a'), 1)
        self.assertEqual(self.lev.get_raw_score('ab', 'b'), 1)
        self.assertEqual(self.lev.get_raw_score('abc', 'ac'), 1)
        self.assertEqual(self.lev.get_raw_score('xabxcdxxefxgx', 'abcdefg'), 6)
        self.assertEqual(self.lev.get_raw_score('a', 'b'), 1)
        self.assertEqual(self.lev.get_raw_score('ab', 'ac'), 1)
        self.assertEqual(self.lev.get_raw_score('ac', 'bc'), 1)
        self.assertEqual(self.lev.get_raw_score('abc', 'axc'), 1)
        self.assertEqual(self.lev.get_raw_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 6)
        self.assertEqual(self.lev.get_raw_score('example', 'samples'), 3)
        self.assertEqual(self.lev.get_raw_score('sturgeon', 'urgently'), 6)
        self.assertEqual(self.lev.get_raw_score('levenshtein', 'frankenstein'), 6)
        self.assertEqual(self.lev.get_raw_score('distance', 'difference'), 5)
        self.assertEqual(self.lev.get_raw_score('java was neat', 'scala is great'), 7)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.lev.get_sim_score('a', ''), 1.0 - (1.0/1.0))
        self.assertEqual(self.lev.get_sim_score('', 'a'), 1.0 - (1.0/1.0))
        self.assertEqual(self.lev.get_sim_score('abc', ''), 1.0 - (3.0/3.0))
        self.assertEqual(self.lev.get_sim_score('', 'abc'), 1.0 - (3.0/3.0))
        self.assertEqual(self.lev.get_sim_score('', ''), 1.0)
        self.assertEqual(self.lev.get_sim_score('a', 'a'), 1.0)
        self.assertEqual(self.lev.get_sim_score('abc', 'abc'), 1.0)
        self.assertEqual(self.lev.get_sim_score('a', 'ab'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('b', 'ab'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('ac', 'abc'), 1.0 - (1.0/3.0))
        self.assertEqual(self.lev.get_sim_score('abcdefg', 'xabxcdxxefxgx'), 1.0 - (6.0/13.0))
        self.assertEqual(self.lev.get_sim_score('ab', 'a'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('ab', 'b'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('abc', 'ac'), 1.0 - (1.0/3.0))
        self.assertEqual(self.lev.get_sim_score('xabxcdxxefxgx', 'abcdefg'), 1.0 - (6.0/13.0))
        self.assertEqual(self.lev.get_sim_score('a', 'b'), 1.0 - (1.0/1.0))
        self.assertEqual(self.lev.get_sim_score('ab', 'ac'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('ac', 'bc'), 1.0 - (1.0/2.0))
        self.assertEqual(self.lev.get_sim_score('abc', 'axc'), 1.0 - (1.0/3.0))
        self.assertEqual(self.lev.get_sim_score('xabxcdxxefxgx', '1ab2cd34ef5g6'), 1.0 - (6.0/13.0))
        self.assertEqual(self.lev.get_sim_score('example', 'samples'), 1.0 - (3.0/7.0))
        self.assertEqual(self.lev.get_sim_score('sturgeon', 'urgently'), 1.0 - (6.0/8.0))
        self.assertEqual(self.lev.get_sim_score('levenshtein', 'frankenstein'), 1.0 - (6.0/12.0))
        self.assertEqual(self.lev.get_sim_score('distance', 'difference'), 1.0 - (5.0/10.0))
        self.assertEqual(self.lev.get_sim_score('java was neat', 'scala is great'), 1.0 - (7.0/14.0))

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.lev.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.lev.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.lev.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.lev.get_raw_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.lev.get_raw_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.lev.get_raw_score(12.90, 12.90)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.lev.get_sim_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.lev.get_sim_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.lev.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.lev.get_sim_score('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.lev.get_sim_score(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.lev.get_sim_score(12.90, 12.90)


class HammingDistanceTestCases(unittest.TestCase):
    def setUp(self):
        self.hd = HammingDistance()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.hd.get_raw_score('-789', 'john'), 4)
        self.assertEqual(self.hd.get_raw_score('a', '*'), 1)
        self.assertEqual(self.hd.get_raw_score('b', 'a'), 1)
        self.assertEqual(self.hd.get_raw_score('abc', 'p q'), 3)
        self.assertEqual(self.hd.get_raw_score('karolin', 'kathrin'), 3)
        self.assertEqual(self.hd.get_raw_score('KARI', 'kari'), 4)
        self.assertEqual(self.hd.get_raw_score('', ''), 0)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.hd.get_sim_score('-789', 'john'), 1.0 - (4.0/4.0))
        self.assertEqual(self.hd.get_sim_score('a', '*'), 1.0 - (1.0/1.0))
        self.assertEqual(self.hd.get_sim_score('b', 'a'), 1.0 - (1.0/1.0))
        self.assertEqual(self.hd.get_sim_score('abc', 'p q'), 1.0 - (3.0/3.0))
        self.assertEqual(self.hd.get_sim_score('karolin', 'kathrin'), 1.0 - (3.0/7.0))
        self.assertEqual(self.hd.get_sim_score('KARI', 'kari'), 1.0 - (4.0/4.0))
        self.assertEqual(self.hd.get_sim_score('', ''), 1.0)

    def test_valid_input_compatibility_raw_score(self):
        self.assertEqual(self.hd.get_raw_score(u'karolin', u'kathrin'), 3)
        self.assertEqual(self.hd.get_raw_score(u'', u''), 0)
        # str_1 = u'foo'.encode(encoding='UTF-8', errors='strict')
        # str_2 = u'bar'.encode(encoding='UTF-8', errors='strict')
        # self.assertEqual(self.hd.get_raw_score(str_1, str_2), 3) # check with Ali - python 3 returns type error
        # self.assertEqual(self.hd.get_raw_score(str_1, str_1), 0) # check with Ali - python 3 returns type error

    def test_valid_input_compatibility_sim_score(self):
        self.assertEqual(self.hd.get_sim_score(u'karolin', u'kathrin'), 1.0 - (3.0/7.0))
        self.assertEqual(self.hd.get_sim_score(u'', u''), 1.0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.hd.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.hd.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.hd.get_raw_score(None, None)

    @raises(ValueError)
    def test_invalid_input4_raw_score(self):
        self.hd.get_raw_score('a', '')

    @raises(ValueError)
    def test_invalid_input5_raw_score(self):
        self.hd.get_raw_score('', 'This is a long string')

    @raises(ValueError)
    def test_invalid_input6_raw_score(self):
        self.hd.get_raw_score('ali', 'alex')

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.hd.get_raw_score('MA', 12)

    @raises(TypeError)
    def test_invalid_input8_raw_score(self):
        self.hd.get_raw_score(12, 'MA')

    @raises(TypeError)
    def test_invalid_input9_raw_score(self):
        self.hd.get_raw_score(12, 12)

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.hd.get_sim_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.hd.get_sim_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.hd.get_sim_score(None, None)

    @raises(ValueError)
    def test_invalid_input4_sim_score(self):
        self.hd.get_sim_score('a', '')

    @raises(ValueError)
    def test_invalid_input5_sim_score(self):
        self.hd.get_sim_score('', 'This is a long string')

    @raises(ValueError)
    def test_invalid_input6_sim_score(self):
        self.hd.get_sim_score('ali', 'alex')

    @raises(TypeError)
    def test_invalid_input7_sim_score(self):
        self.hd.get_sim_score('MA', 12)

    @raises(TypeError)
    def test_invalid_input8_sim_score(self):
        self.hd.get_sim_score(12, 'MA')

    @raises(TypeError)
    def test_invalid_input9_sim_score(self):
        self.hd.get_sim_score(12, 12)


class NeedlemanWunschTestCases(unittest.TestCase):
    def setUp(self):
        self.nw = NeedlemanWunsch()
        self.nw_with_params1 = NeedlemanWunsch(0.0)
        self.nw_with_params2 = NeedlemanWunsch(1.0,
            sim_score=lambda s1, s2: (2 if s1 == s2 else -1))
        self.nw_with_params3 = NeedlemanWunsch(gap_cost=0.5,
            sim_score=lambda s1, s2: (1 if s1 == s2 else -1))

    def test_valid_input(self):
        self.assertEqual(self.nw.get_raw_score('dva', 'deeva'), 1.0)
        self.assertEqual(self.nw_with_params1.get_raw_score('dva', 'deeve'), 2.0)
        self.assertEqual(self.nw_with_params2.get_raw_score('dva', 'deeve'), 1.0)
        self.assertEqual(self.nw_with_params3.get_raw_score('GCATGCUA', 'GATTACA'),
                         2.5)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.nw.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.nw.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.nw.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.nw.get_raw_score(['a'], 'b')

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.nw.get_raw_score('a', ['b'])

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.nw.get_raw_score(['a'], ['b'])


class SmithWatermanTestCases(unittest.TestCase):
    def setUp(self):
        self.sw = SmithWaterman()
        self.sw_with_params1 = SmithWaterman(2.2)
        self.sw_with_params2 = SmithWaterman(1,
            sim_score=lambda s1, s2: (2 if s1 == s2 else -1))
        self.sw_with_params3 = SmithWaterman(gap_cost=1,
            sim_score=lambda s1, s2: (int(1 if s1 == s2 else -1)))
        self.sw_with_params4 = SmithWaterman(gap_cost=1.4,
            sim_score=lambda s1, s2: (1.5 if s1 == s2 else 0.5))

    def test_valid_input(self):
        self.assertEqual(self.sw.get_raw_score('cat', 'hat'), 2.0)
        self.assertEqual(self.sw_with_params1.get_raw_score('dva', 'deeve'), 1.0)
        self.assertEqual(self.sw_with_params2.get_raw_score('dva', 'deeve'), 2.0)
        self.assertEqual(self.sw_with_params3.get_raw_score('GCATGCU', 'GATTACA'),
                         2.0)
        self.assertEqual(self.sw_with_params4.get_raw_score('GCATAGCU', 'GATTACA'),
                         6.5)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.sw.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.sw.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.sw.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.sw.get_raw_score('MARHTA', 12)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.sw.get_raw_score(12, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.sw.get_raw_score(12, 12)


class SoundexTestCases(unittest.TestCase):
    def setUp(self):
        self.sdx = Soundex()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.sdx.get_raw_score('Robert', 'Rupert'), 1)
        self.assertEqual(self.sdx.get_raw_score('Sue', 'S'), 1)
        self.assertEqual(self.sdx.get_raw_score('robert', 'rupert'), 1)
        self.assertEqual(self.sdx.get_raw_score('Gough', 'goff'), 0)
        self.assertEqual(self.sdx.get_raw_score('gough', 'Goff'), 0)
        self.assertEqual(self.sdx.get_raw_score('ali', 'a,,,li'), 1)
        self.assertEqual(self.sdx.get_raw_score('Jawornicki', 'Yavornitzky'), 0)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.sdx.get_sim_score('Robert', 'Rupert'), 1)
        self.assertEqual(self.sdx.get_sim_score('Sue', 'S'), 1)
        self.assertEqual(self.sdx.get_sim_score('robert', 'rupert'), 1)
        self.assertEqual(self.sdx.get_sim_score('Gough', 'goff'), 0)
        self.assertEqual(self.sdx.get_sim_score('gough', 'Goff'), 0)
        self.assertEqual(self.sdx.get_sim_score('ali', 'a,,,li'), 1)
        self.assertEqual(self.sdx.get_sim_score('Jawornicki', 'Yavornitzky'), 0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.sdx.get_raw_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.sdx.get_raw_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.sdx.get_raw_score(None, None)

    @raises(ValueError)
    def test_invalid_input4_raw_score(self):
        self.sdx.get_raw_score('a', '')

    @raises(ValueError)
    def test_invalid_input5_raw_score(self):
        self.sdx.get_raw_score('', 'This is a long string')

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.sdx.get_raw_score('xyz', [''])

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.sdx.get_sim_score('a', None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.sdx.get_sim_score(None, 'b')

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.sdx.get_sim_score(None, None)

    @raises(ValueError)
    def test_invalid_input4_sim_score(self):
        self.sdx.get_sim_score('a', '')

    @raises(ValueError)
    def test_invalid_input5_sim_score(self):
        self.sdx.get_sim_score('', 'This is a long string')

    @raises(TypeError)
    def test_invalid_input7_sim_score(self):
        self.sdx.get_sim_score('xyz', [''])


# ---------------------- token based similarity measures  ----------------------

# ---------------------- set based similarity measures  ----------------------
class OverlapCoefficientTestCases(unittest.TestCase):
    def setUp(self):
        self.oc = OverlapCoefficient()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.oc.get_raw_score([], []), 1.0)
        self.assertEqual(self.oc.get_raw_score(['data', 'science'], ['data']),
                         1.0 / min(2.0, 1.0))
        self.assertEqual(self.oc.get_raw_score(['data', 'science'],
                                               ['science', 'good']), 1.0 / min(2.0, 3.0))
        self.assertEqual(self.oc.get_raw_score([], ['data']), 0)
        self.assertEqual(self.oc.get_raw_score(['data', 'data', 'science'],
                                               ['data', 'management']), 1.0 / min(3.0, 2.0))

    def test_valid_input_sim_score(self):
        self.assertEqual(self.oc.get_sim_score([], []), 1.0)
        self.assertEqual(self.oc.get_sim_score(['data', 'science'], ['data']),
                         1.0 / min(2.0, 1.0))
        self.assertEqual(self.oc.get_sim_score(['data', 'science'],
                                               ['science', 'good']), 1.0 / min(2.0, 3.0))
        self.assertEqual(self.oc.get_sim_score([], ['data']), 0)
        self.assertEqual(self.oc.get_sim_score(['data', 'data', 'science'],
                                               ['data', 'management']), 1.0 / min(3.0, 2.0))

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.oc.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.oc.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.oc.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.oc.get_raw_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.oc.get_raw_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.oc.get_raw_score('MARTHA', 'MARTHA')

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.oc.get_sim_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.oc.get_sim_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.oc.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.oc.get_sim_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.oc.get_sim_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.oc.get_sim_score('MARTHA', 'MARTHA')


class DiceTestCases(unittest.TestCase):
    def setUp(self):
        self.dice = Dice()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.dice.get_raw_score(['data', 'science'], ['data']),
                         2 * 1.0 / 3.0)
        self.assertEqual(self.dice.get_raw_score(['data', 'science'], ['science', 'good']),
                         2 * 1.0 / 4.0)
        self.assertEqual(self.dice.get_raw_score([], ['data']), 0)
        self.assertEqual(self.dice.get_raw_score(['data', 'data', 'science'],
                                                 ['data', 'management']), 2 * 1.0 / 4.0)
        self.assertEqual(self.dice.get_raw_score(['data', 'management'],
                                                 ['data', 'data', 'science']), 2 * 1.0 / 4.0)
        self.assertEqual(self.dice.get_raw_score([], []), 1.0)
        self.assertEqual(self.dice.get_raw_score(['a', 'b'], ['b', 'a']), 1.0)
        self.assertEqual(self.dice.get_raw_score(set([]), set([])), 1.0)
        self.assertEqual(self.dice.get_raw_score({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}),
                         2 * 3.0 / 11.0)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.dice.get_sim_score(['data', 'science'], ['data']),
                         2 * 1.0 / 3.0)
        self.assertEqual(self.dice.get_sim_score(['data', 'science'], ['science', 'good']),
                         2 * 1.0 / 4.0)
        self.assertEqual(self.dice.get_sim_score([], ['data']), 0)
        self.assertEqual(self.dice.get_sim_score(['data', 'data', 'science'],
                                                 ['data', 'management']), 2 * 1.0 / 4.0)
        self.assertEqual(self.dice.get_sim_score(['data', 'management'],
                                                 ['data', 'data', 'science']), 2 * 1.0 / 4.0)
        self.assertEqual(self.dice.get_sim_score([], []), 1.0)
        self.assertEqual(self.dice.get_sim_score(['a', 'b'], ['b', 'a']), 1.0)
        self.assertEqual(self.dice.get_sim_score(set([]), set([])), 1.0)
        self.assertEqual(self.dice.get_sim_score({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}),
                         2 * 3.0 / 11.0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.dice.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.dice.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.dice.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.dice.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.dice.get_raw_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.dice.get_raw_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.dice.get_raw_score('MARHTA', 'MARTHA')

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.dice.get_sim_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.dice.get_sim_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.dice.get_sim_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.dice.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.dice.get_sim_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.dice.get_sim_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input7_sim_score(self):
        self.dice.get_sim_score('MARHTA', 'MARTHA')


class JaccardTestCases(unittest.TestCase):
    def setUp(self):
        self.jac = Jaccard()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.jac.get_raw_score(['data', 'science'], ['data']),
                         1.0 / 2.0)
        self.assertEqual(self.jac.get_raw_score(['data', 'science'],
                                                ['science', 'good']), 1.0 / 3.0)
        self.assertEqual(self.jac.get_raw_score([], ['data']), 0)
        self.assertEqual(self.jac.get_raw_score(['data', 'data', 'science'],
                             ['data', 'management']), 1.0 / 3.0)
        self.assertEqual(self.jac.get_raw_score(['data', 'management'],
                             ['data', 'data', 'science']), 1.0 / 3.0)
        self.assertEqual(self.jac.get_raw_score([], []), 1.0)
        self.assertEqual(self.jac.get_raw_score(set([]), set([])), 1.0)
        self.assertEqual(self.jac.get_raw_score({1, 1, 2, 3, 4},
                             {2, 3, 4, 5, 6, 7, 7, 8}), 3.0 / 8.0)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.jac.get_sim_score(['data', 'science'], ['data']),
                         1.0 / 2.0)
        self.assertEqual(self.jac.get_sim_score(['data', 'science'],
                                                ['science', 'good']), 1.0 / 3.0)
        self.assertEqual(self.jac.get_sim_score([], ['data']), 0)
        self.assertEqual(self.jac.get_sim_score(['data', 'data', 'science'],
                             ['data', 'management']), 1.0 / 3.0)
        self.assertEqual(self.jac.get_sim_score(['data', 'management'],
                             ['data', 'data', 'science']), 1.0 / 3.0)
        self.assertEqual(self.jac.get_sim_score([], []), 1.0)
        self.assertEqual(self.jac.get_sim_score(set([]), set([])), 1.0)
        self.assertEqual(self.jac.get_sim_score({1, 1, 2, 3, 4},
                             {2, 3, 4, 5, 6, 7, 7, 8}), 3.0 / 8.0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.jac.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.jac.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.jac.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.jac.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.jac.get_raw_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.jac.get_raw_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.jac.get_raw_score('MARTHA', 'MARTHA')

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.jac.get_sim_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.jac.get_sim_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.jac.get_sim_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.jac.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.jac.get_sim_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.jac.get_sim_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7_sim_score(self):
        self.jac.get_sim_score('MARTHA', 'MARTHA')


class GeneralizedJaccardTestCases(unittest.TestCase):
    def setUp(self):
        self.gen_jac = GeneralizedJaccard()
        self.gen_jac_with_jw = GeneralizedJaccard(sim_func=JaroWinkler().get_raw_score)
        self.gen_jac_with_jw_08 = GeneralizedJaccard(sim_func=JaroWinkler().get_raw_score,
                                                     threshold=0.8)
        self.gen_jac_invalid = GeneralizedJaccard(sim_func=NeedlemanWunsch().get_raw_score,
                                                  threshold=0.8)

    def test_valid_input_raw_score(self):
        self.assertEqual(self.gen_jac.get_raw_score([''], ['']), 1.0)  # need to check this

        self.assertEqual(self.gen_jac.get_raw_score([''], ['a']), 0.0)
        self.assertEqual(self.gen_jac.get_raw_score(['a'], ['a']), 1.0)

        self.assertEqual(self.gen_jac.get_raw_score([], ['Nigel']), 0.0)
        self.assertEqual(self.gen_jac.get_raw_score(['Niall'], ['Neal']), 0.7833333333333333)
        self.assertEqual(self.gen_jac.get_raw_score(['Niall'], ['Njall', 'Neal']), 0.43333333333333335)
        self.assertEqual(self.gen_jac.get_raw_score(['Niall'], ['Neal', 'Njall']), 0.43333333333333335)
        self.assertEqual(self.gen_jac.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.6800468975468975)

        self.assertEqual(self.gen_jac_with_jw.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.7220003607503608)
        self.assertEqual(self.gen_jac_with_jw.get_raw_score(
                ['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.7075277777777778)

        self.assertEqual(self.gen_jac_with_jw_08.get_raw_score(
                ['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.45810185185185187)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.gen_jac.get_sim_score([''], ['']), 1.0)  # need to check this

        self.assertEqual(self.gen_jac.get_sim_score([''], ['a']), 0.0)
        self.assertEqual(self.gen_jac.get_sim_score(['a'], ['a']), 1.0)

        self.assertEqual(self.gen_jac.get_sim_score([], ['Nigel']), 0.0)
        self.assertEqual(self.gen_jac.get_sim_score(['Niall'], ['Neal']), 0.7833333333333333)
        self.assertEqual(self.gen_jac.get_sim_score(['Niall'], ['Njall', 'Neal']), 0.43333333333333335)
        self.assertEqual(self.gen_jac.get_sim_score(['Niall'], ['Neal', 'Njall']), 0.43333333333333335)
        self.assertEqual(self.gen_jac.get_sim_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.6800468975468975)

        self.assertEqual(self.gen_jac_with_jw.get_sim_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.7220003607503608)
        self.assertEqual(self.gen_jac_with_jw.get_sim_score(
                ['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.7075277777777778)

        self.assertEqual(self.gen_jac_with_jw_08.get_sim_score(
                ['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.45810185185185187)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.gen_jac.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.gen_jac.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.gen_jac.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.gen_jac.get_raw_score("temp", "temp")

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.gen_jac.get_raw_score(['temp'], 'temp')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.gen_jac.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.gen_jac.get_raw_score('temp', ['temp'])

    @raises(ValueError)
    def test_invalid_sim_measure(self):
        self.gen_jac_invalid.get_raw_score(
                ['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'])

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.gen_jac.get_sim_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.gen_jac.get_sim_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.gen_jac.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.gen_jac.get_sim_score("temp", "temp")

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.gen_jac.get_sim_score(['temp'], 'temp')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.gen_jac.get_sim_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input7_sim_score(self):
        self.gen_jac.get_sim_score('temp', ['temp'])

    @raises(ValueError)
    def test_invalid_sim_measure_sim_score(self):
        self.gen_jac_invalid.get_sim_score(
                ['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'])


class CosineTestCases(unittest.TestCase):
    def setUp(self):
        self.cos = Cosine()

    def test_valid_input_raw_score(self):
        self.assertEqual(self.cos.get_raw_score(['data', 'science'], ['data']), 1.0 / (math.sqrt(2) * math.sqrt(1)))
        self.assertEqual(self.cos.get_raw_score(['data', 'science'], ['science', 'good']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(self.cos.get_raw_score([], ['data']), 0.0)
        self.assertEqual(self.cos.get_raw_score(['data', 'data', 'science'], ['data', 'management']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(self.cos.get_raw_score(['data', 'management'], ['data', 'data', 'science']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(self.cos.get_raw_score([], []), 1.0)
        self.assertEqual(self.cos.get_raw_score(set([]), set([])), 1.0)
        self.assertEqual(self.cos.get_raw_score({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}),
                         3.0 / (math.sqrt(4) * math.sqrt(7)))

    def test_valid_input_sim_score(self):
        self.assertEqual(self.cos.get_sim_score(['data', 'science'], ['data']), 1.0 / (math.sqrt(2) * math.sqrt(1)))
        self.assertEqual(self.cos.get_sim_score(['data', 'science'], ['science', 'good']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(self.cos.get_sim_score([], ['data']), 0.0)
        self.assertEqual(self.cos.get_sim_score(['data', 'data', 'science'], ['data', 'management']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(self.cos.get_sim_score(['data', 'management'], ['data', 'data', 'science']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(self.cos.get_sim_score([], []), 1.0)
        self.assertEqual(self.cos.get_sim_score(set([]), set([])), 1.0)
        self.assertEqual(self.cos.get_sim_score({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}),
                         3.0 / (math.sqrt(4) * math.sqrt(7)))

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.cos.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.cos.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.cos.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.cos.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.cos.get_raw_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.cos.get_raw_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.cos.get_raw_score('MARTHA', 'MARTHA')

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.cos.get_sim_score(1, 1)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.cos.get_sim_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.cos.get_sim_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.cos.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.cos.get_sim_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.cos.get_sim_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7_sim_score(self):
        self.cos.get_sim_score('MARTHA', 'MARTHA')


class TfidfTestCases(unittest.TestCase):
    def setUp(self):
        self.tfidf = TfIdf()
        self.tfidf_with_params1 = TfIdf([['a', 'b', 'a'], ['a', 'c'], ['a'], ['b']], True)
        self.tfidf_with_params2 = TfIdf([['a', 'b', 'a'], ['a', 'c'], ['a']])
        self.tfidf_with_params3 = TfIdf([['x', 'y'], ['w'], ['q']])

    def test_valid_input_raw_score(self):
        self.assertEqual(self.tfidf_with_params1.get_raw_score(['a', 'b', 'a'], ['a', 'c']),
                         0.11166746710505392)
        self.assertEqual(self.tfidf_with_params2.get_raw_score(['a', 'b', 'a'], ['a', 'c']),
                         0.17541160386140586)
        self.assertEqual(self.tfidf_with_params2.get_raw_score(['a', 'b', 'a'], ['a']),
                         0.5547001962252291)
        self.assertEqual(self.tfidf.get_raw_score(['a', 'b', 'a'], ['a']), 0.7071067811865475)
        self.assertEqual(self.tfidf_with_params3.get_raw_score(['a', 'b', 'a'], ['a']), 0.0)
        self.assertEqual(self.tfidf.get_raw_score(['a', 'b', 'a'], ['a']), 0.7071067811865475)
        self.assertEqual(self.tfidf.get_raw_score(['a', 'b', 'a'], ['a', 'b', 'a']), 1.0)
        self.assertEqual(self.tfidf.get_raw_score([], ['a', 'b', 'a']), 0.0)

    def test_valid_input_sim_score(self):
        self.assertEqual(self.tfidf_with_params1.get_sim_score(['a', 'b', 'a'], ['a', 'c']),
                         0.11166746710505392)
        self.assertEqual(self.tfidf_with_params2.get_sim_score(['a', 'b', 'a'], ['a', 'c']),
                         0.17541160386140586)
        self.assertEqual(self.tfidf_with_params2.get_sim_score(['a', 'b', 'a'], ['a']),
                         0.5547001962252291)
        self.assertEqual(self.tfidf.get_sim_score(['a', 'b', 'a'], ['a']), 0.7071067811865475)
        self.assertEqual(self.tfidf_with_params3.get_sim_score(['a', 'b', 'a'], ['a']), 0.0)
        self.assertEqual(self.tfidf.get_sim_score(['a', 'b', 'a'], ['a']), 0.7071067811865475)
        self.assertEqual(self.tfidf.get_sim_score(['a', 'b', 'a'], ['a', 'b', 'a']), 1.0)
        self.assertEqual(self.tfidf.get_sim_score([], ['a', 'b', 'a']), 0.0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.tfidf.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.tfidf.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.tfidf.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.tfidf.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.tfidf.get_raw_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.tfidf.get_raw_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.tfidf.get_raw_score('MARTHA', 'MARTHA')

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.tfidf.get_sim_score(1, 1)

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.tfidf.get_sim_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.tfidf.get_sim_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.tfidf.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.tfidf.get_sim_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.tfidf.get_sim_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7_sim_score(self):
        self.tfidf.get_sim_score('MARTHA', 'MARTHA')


class TverskyIndexTestCases(unittest.TestCase):
    def setUp(self):
        self.tvi = TverskyIndex()
        self.tvi_with_params1 = TverskyIndex(0.5, 0.5)
        self.tvi_with_params2 = TverskyIndex(0.7, 0.8)
        self.tvi_with_params3 = TverskyIndex(0.2, 0.4)
        self.tvi_with_params4 = TverskyIndex(0.9, 0.8)
        self.tvi_with_params5 = TverskyIndex(0.45, 0.85)

    def test_valid_input_raw_score(self):
        self.assertEqual(self.tvi_with_params1.get_raw_score(['data', 'science'], ['data']),
                         1.0 / (1.0 + 0.5*1 + 0.5*0))
        self.assertEqual(self.tvi.get_raw_score(['data', 'science'], ['science', 'good']),
                         1.0 / (1.0 + 0.5*1 + 0.5*1))
        self.assertEqual(self.tvi.get_raw_score([], ['data']), 0)
        self.assertEqual(self.tvi_with_params2.get_raw_score(['data', 'data', 'science'],
                                                             ['data', 'management']),
                         1.0 / (1.0 + 0.7*1 + 0.8*1))
        self.assertEqual(self.tvi_with_params3.get_raw_score(['data', 'management', 'science'],
                                                             ['data', 'data', 'science']),
                         2.0 / (2.0 + 0.2*1 + 0))
        self.assertEqual(self.tvi.get_raw_score([], []), 1.0)
        self.assertEqual(self.tvi_with_params4.get_raw_score(['a', 'b'], ['b', 'a']), 1.0)
        self.assertEqual(self.tvi.get_raw_score(['a', 'b'], ['b', 'a']), 1.0)
        self.assertEqual(self.tvi.get_raw_score(set([]), set([])), 1.0)
        self.assertEqual(self.tvi_with_params5.get_raw_score({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}),
                         3.0 / (3.0 + 0.45*1 + 0.85*4))

    def test_valid_input_sim_score(self):
        self.assertEqual(self.tvi_with_params1.get_sim_score(['data', 'science'], ['data']),
                         1.0 / (1.0 + 0.5*1 + 0.5*0))
        self.assertEqual(self.tvi.get_sim_score(['data', 'science'], ['science', 'good']),
                         1.0 / (1.0 + 0.5*1 + 0.5*1))
        self.assertEqual(self.tvi.get_sim_score([], ['data']), 0)
        self.assertEqual(self.tvi_with_params2.get_sim_score(['data', 'data', 'science'],
                                                             ['data', 'management']),
                         1.0 / (1.0 + 0.7*1 + 0.8*1))
        self.assertEqual(self.tvi_with_params3.get_sim_score(['data', 'management', 'science'],
                                                             ['data', 'data', 'science']),
                         2.0 / (2.0 + 0.2*1 + 0))
        self.assertEqual(self.tvi.get_sim_score([], []), 1.0)
        self.assertEqual(self.tvi_with_params4.get_sim_score(['a', 'b'], ['b', 'a']), 1.0)
        self.assertEqual(self.tvi.get_sim_score(['a', 'b'], ['b', 'a']), 1.0)
        self.assertEqual(self.tvi.get_sim_score(set([]), set([])), 1.0)
        self.assertEqual(self.tvi_with_params5.get_sim_score({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}),
                         3.0 / (3.0 + 0.45*1 + 0.85*4))

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.tvi.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.tvi.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.tvi.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.tvi.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.tvi.get_raw_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.tvi.get_raw_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.tvi.get_raw_score('MARHTA', 'MARTHA')

    @raises(TypeError)
    def test_invalid_input1_sim_score(self):
        self.tvi.get_sim_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_sim_score(self):
        self.tvi.get_sim_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input3_sim_score(self):
        self.tvi.get_sim_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input4_sim_score(self):
        self.tvi.get_sim_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_sim_score(self):
        self.tvi.get_sim_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input6_sim_score(self):
        self.tvi.get_sim_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input7_sim_score(self):
        self.tvi.get_sim_score('MARHTA', 'MARTHA')

    @raises(ValueError)
    def test_invalid_input8(self):
        tvi_invalid = TverskyIndex(0.5, -0.9)

    @raises(ValueError)
    def test_invalid_input9(self):
        tvi_invalid = TverskyIndex(-0.5, 0.9)

    @raises(ValueError)
    def test_invalid_input10(self):
        tvi_invalid = TverskyIndex(-0.5, -0.9)


# ---------------------- bag based similarity measures  ----------------------
# class CosineTestCases(unittest.TestCase):
#     def test_valid_input(self):
#         NONQ_FROM = 'The quick brown fox jumped over the lazy dog.'
#         NONQ_TO = 'That brown dog jumped over the fox.'
#         self.assertEqual(cosine([], []), 1) # check-- done. both simmetrics, abydos return 1.
#         self.assertEqual(cosine(['the', 'quick'], []), 0)
#         self.assertEqual(cosine([], ['the', 'quick']), 0)
#         self.assertAlmostEqual(cosine(whitespace(NONQ_TO), whitespace(NONQ_FROM)),
#                                4/math.sqrt(9*7))
#
#     @raises(TypeError)
#     def test_invalid_input1_raw_score(self):
#         cosine(['a'], None)
#     @raises(TypeError)
#     def test_invalid_input2_raw_score(self):
#         cosine(None, ['b'])
#     @raises(TypeError)
#     def test_invalid_input3_raw_score(self):
#         cosine(None, None)


# ---------------------- hybrid similarity measure  ----------------------

class Soft_TfidfTestCases(unittest.TestCase):
    def setUp(self):
        self.soft_tfidf = SoftTfIdf()
        self.soft_tfidf_with_params1 = SoftTfIdf([['a', 'b', 'a'], ['a', 'c'], ['a']],
                                                 sim_func=Jaro().get_raw_score,
                                                 threshold=0.8)
        self.soft_tfidf_with_params2 = SoftTfIdf([['a', 'b', 'a'], ['a', 'c'], ['a']],
                                                 threshold=0.9)
        self.soft_tfidf_with_params3 = SoftTfIdf([['x', 'y'], ['w'], ['q']])
        self.soft_tfidf_with_params4 = SoftTfIdf(sim_func=Affine().get_raw_score, threshold=0.6)

    def test_valid_input_raw_score(self):
        self.assertEqual(self.soft_tfidf_with_params1.get_raw_score(
                         ['a', 'b', 'a'], ['a', 'c']), 0.17541160386140586)
        self.assertEqual(self.soft_tfidf_with_params2.get_raw_score(
                         ['a', 'b', 'a'], ['a']), 0.5547001962252291)
        self.assertEqual(self.soft_tfidf_with_params3.get_raw_score(
                         ['a', 'b', 'a'], ['a']), 0.0)
        self.assertEqual(self.soft_tfidf_with_params4.get_raw_score(
                             ['aa', 'bb', 'a'], ['ab', 'ba']),
                         0.81649658092772592)
        self.assertEqual(self.soft_tfidf.get_raw_score(
                         ['a', 'b', 'a'], ['a', 'b', 'a']), 1.0)
        self.assertEqual(self.soft_tfidf.get_raw_score([], ['a', 'b', 'a']), 0.0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.soft_tfidf.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.soft_tfidf.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.soft_tfidf.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.soft_tfidf.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.soft_tfidf.get_raw_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.soft_tfidf.get_raw_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.soft_tfidf.get_raw_score('MARTHA', 'MARTHA')


class MongeElkanTestCases(unittest.TestCase):
    def setUp(self):
        self.me = MongeElkan()
        self.me_with_nw = MongeElkan(NeedlemanWunsch().get_raw_score)
        self.me_with_affine = MongeElkan(Affine().get_raw_score)

    def test_valid_input(self):
        self.assertEqual(self.me.get_raw_score([''], ['']), 1.0)  # need to check this

        self.assertEqual(self.me.get_raw_score([''], ['a']), 0.0)
        self.assertEqual(self.me.get_raw_score(['a'], ['a']), 1.0)

        self.assertEqual(self.me.get_raw_score(['Niall'], ['Neal']), 0.8049999999999999)
        self.assertEqual(self.me.get_raw_score(['Niall'], ['Njall']), 0.88)
        self.assertEqual(self.me.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            0.8364448051948052)
        self.assertEqual(self.me_with_nw.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']), 
            2.0)
        self.assertEqual(self.me_with_affine.get_raw_score(
                ['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']),
            2.25)
        self.assertEqual(self.me.get_raw_score(['Niall'], ['Niel']), 0.8266666666666667)
        self.assertEqual(self.me.get_raw_score(['Niall'], ['Nigel']), 0.7866666666666667)
        self.assertEqual(self.me.get_raw_score([], ['Nigel']), 0.0)

    @raises(TypeError)
    def test_invalid_input1_raw_score(self):
        self.me.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2_raw_score(self):
        self.me.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3_raw_score(self):
        self.me.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4_raw_score(self):
        self.me.get_raw_score("temp", "temp")

    @raises(TypeError)
    def test_invalid_input5_raw_score(self):
        self.me.get_raw_score(['temp'], 'temp')

    @raises(TypeError)
    def test_invalid_input6_raw_score(self):
        self.me.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input7_raw_score(self):
        self.me.get_raw_score('temp', ['temp'])