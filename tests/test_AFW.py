from unittest import TestCase
import unittest
import AFW
import automata_IO
import copy


class TestWordAcceptance(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.afw_word_acceptance_test_01 = automata_IO.afw_json_importer('./json/afw/afw_word_acceptance_test_01.json')
        self.afw_word_acceptance_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_states': set(),
            'accepting_states': set(),
            'transitions': {}
        }

    def test_word_acceptance(self):
        """ Tests a correct word acceptance """
        self.assertTrue(AFW.word_acceptance(self.afw_word_acceptance_test_01, ['a', 'b', 'b', 'a', 'a', 'b', 'a', 'a']))

    def test_word_acceptance_false(self):
        """ Tests a non correct word to be refused, with good alphabet """
        self.assertFalse(AFW.word_acceptance(self.afw_word_acceptance_test_01, ['a', 'b', 'a']))

    def test_word_acceptance_wrong_alphabet(self):
        """ Tests a non correct word, with letters not form the afw alphabet """
        self.assertFalse(AFW.word_acceptance(self.afw_word_acceptance_test_01, ['a', 'b', 'wrong']))

    def test_word_acceptance_empty_word(self):
        """ Tests an empty word"""
        self.afw_word_acceptance_test_01['initial_state'] = 'q1'
        self.assertFalse(AFW.word_acceptance(self.afw_word_acceptance_test_01, []))

    @unittest.expectedFailure
    def test_word_acceptance_wrong_input_1(self):
        """ Tests an input different from a dict() object. [EXPECTED FAILURE]"""
        AFW.word_acceptance(1, ['a', 'b', 'b', 'a', 'b'])

    @unittest.expectedFailure
    def test_word_acceptance_wrong_input_2(self):
        """ Tests an input different from a list() object. [EXPECTED FAILURE]"""
        AFW.word_acceptance(self.afw_word_acceptance_test_01, 1)

    @unittest.expectedFailure
    def test_word_acceptance_wrong_dict(self):
        """ Tests a dict() in input different from a well formatted dict() representing a AFW. [EXPECTED FAILURE]"""
        AFW.word_acceptance({'goofy': 'donald'}, ['a', 'b', 'b', 'a', 'b'])

    def test_word_acceptance_check_side_effects(self):
        """ Tests that the function doesn't make any side effect on the input"""
        before = copy.deepcopy(self.afw_word_acceptance_test_01)
        AFW.word_acceptance(self.afw_word_acceptance_test_01, ['a', 'b', 'b', 'a', 'a', 'b', 'a', 'a'])
        self.assertDictEqual(before, self.afw_word_acceptance_test_01)


class TestNfaToAfwConversion(TestCase):
    @unittest.skip("TestNfaToAfwConversion TODO")
    def test_nfa_to_afw_conversion(self):
        self.fail()


class TestAfwToNfaConversion(TestCase):
    @unittest.skip("TestAfwToNfaConversion TODO")
    def test_afw_to_nfa_conversion(self):
        self.fail()


class TestReplaceAll(TestCase):
    @unittest.skip("TestReplace_all TODO")
    def test___replace_all(self):
        self.fail()


class TestAfwComplementation(TestCase):
    @unittest.skip("TestAfwComplementation TODO")
    def test_afw_complementation(self):
        self.fail()


class TestAfwUnion(TestCase):
    @unittest.skip("TestAfwUnion TODO")
    def test_afw_union(self):
        self.fail()


class TestAfwIntersection(TestCase):
    @unittest.skip(" TODO")
    def test_afw_intersection(self):
        self.fail()


class TestAfwNonemptinessCheck(TestCase):
    @unittest.skip("TestAfwNonemptinessCheck TODO")
    def test_afw_nonemptiness_check(self):
        self.fail()


class TestAfwNonuniversalityCheck(TestCase):
    @unittest.skip("TestAfwNonuniversalityCheck TODO")
    def test_afw_nonuniversality_check(self):
        self.fail()
