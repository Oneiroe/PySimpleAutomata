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
    def setUp(self):
        self.maxDiff = None
        self.nfa_nfa_to_afw_test_01 = automata_IO.nfa_dot_importer('./dot/afw/nfa_nfa_to_afw_test_01.dot')
        self.afw_nfa_to_afw_test_01 = automata_IO.afw_json_importer('./json/afw/afw_nfa_to_afw_test_01.json')
        self.nfa_nfa_to_afw_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_states': set(),
            'accepting_states': set(),
            'transitions': {}
        }
        self.afw_nfa_to_afw_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_state': None,
            'accepting_states': set(),
            'transitions': {}
        }

    def test_nfa_to_afw_conversion(self):
        """ Tests a correct nfa to afw conversion """
        afw_01 = AFW.nfa_to_afw_conversion(self.nfa_nfa_to_afw_test_01)
        self.assertSetEqual(afw_01['alphabet'], self.afw_nfa_to_afw_test_01['alphabet'])
        self.assertSetEqual(afw_01['states'], self.afw_nfa_to_afw_test_01['states'])
        self.assertEqual(afw_01['initial_state'], self.afw_nfa_to_afw_test_01['initial_state'])
        self.assertSetEqual(afw_01['accepting_states'], self.afw_nfa_to_afw_test_01['accepting_states'])

        self.assertEqual(len(afw_01['alphabet']), len(self.afw_nfa_to_afw_test_01['alphabet']))
        # self.assertDictEqual(afw_01, self.afw_nfa_to_afw_test_01)
        # due to set-to-string serialization undecidability of items order, it is not possible to match the result
        # of the operation to a predetermined result without enlist all the possible combination of S^2
        # i.e a result may be 's2 or s5' or 's5 or s2' unpredictably

    def test_nfa_to_afw_conversion_empty_states(self):
        """ Tests converting an empty nfa """
        expected_solution = {
            'alphabet': set(),
            'states': {'s_root'},
            'initial_state': 's_root',
            'accepting_states': set(),
            'transitions': {}
        }
        self.assertDictEqual(AFW.nfa_to_afw_conversion(self.nfa_nfa_to_afw_test_empty), expected_solution)

    def test_nfa_to_afw_conversion_empty_transition(self):
        """ Tests converting an nfa without transition """
        expected_solution = {
            'alphabet': self.nfa_nfa_to_afw_test_01['alphabet'],
            'states': self.nfa_nfa_to_afw_test_01['states'].union({'s_root'}),
            'initial_state': 's_root',
            'accepting_states': self.nfa_nfa_to_afw_test_01['accepting_states'],
            'transitions': {}
        }
        self.nfa_nfa_to_afw_test_01['transitions'] = {}
        self.assertDictEqual(AFW.nfa_to_afw_conversion(self.nfa_nfa_to_afw_test_01), expected_solution)

    @unittest.expectedFailure
    def test_nfa_to_afw_conversion_wrong_input(self):
        """ Tests the function using an input different from a dict object. [EXPECTED FAILURE] """
        AFW.nfa_to_afw_conversion(0)

    @unittest.expectedFailure
    def test_nfa_to_afw_conversion_wrong_dict(self):
        """ Tests the function using an input different from a well formatted dict representing a afw. [EXPECTED FAILURE] """
        AFW.nfa_to_afw_conversion({'goofy': 'donald'})

    def test_nfa_to_afw_conversion_side_effects(self):
        """ Tests the function doesn't make any side effect on the input """
        before = copy.deepcopy(self.nfa_nfa_to_afw_test_01)
        AFW.nfa_to_afw_conversion(self.nfa_nfa_to_afw_test_01)
        self.assertDictEqual(before, self.nfa_nfa_to_afw_test_01)


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
