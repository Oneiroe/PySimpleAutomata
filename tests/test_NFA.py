from unittest import TestCase
import unittest
import NFA
import automata_IO
import copy


class TestNfaIntersection(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.nfa_intersection_1_test_01 = automata_IO.nfa_dot_importer('./dot/nfa/nfa_intersection_1_test_01.dot')
        self.nfa_intersection_2_test_01 = automata_IO.nfa_dot_importer('./dot/nfa/nfa_intersection_2_test_01.dot')
        self.nfa_intersection_test_01_solution = {
            'alphabet': {'a', 'b'},
            'states': {
                ('s0', 't0'), ('s0', 't1'), ('s0', 't2'), ('s0', 't3'), ('s0', 't4'),
                ('s1', 't0'), ('s1', 't1'), ('s1', 't2'), ('s1', 't3'), ('s1', 't4'),
                ('s2', 't0'), ('s2', 't1'), ('s2', 't2'), ('s2', 't3'), ('s2', 't4'),
                ('s3', 't0'), ('s3', 't1'), ('s3', 't2'), ('s3', 't3'), ('s3', 't4'),
                ('s4', 't0'), ('s4', 't1'), ('s4', 't2'), ('s4', 't3'), ('s4', 't4')
            },
            'initial_states': {('s0', 't0')},
            'accepting_states': {('s2', 't0'), ('s2', 't4')},
            'transitions': {
                (('s0', 't0'), 'a'): {('s1', 't2')},
                (('s0', 't0'), 'b'): {('s3', 't1')},
                (('s0', 't1'), 'b'): {('s3', 't4')},
                (('s0', 't2'), 'a'): {('s1', 't2'), ('s1', 't4')},
                (('s0', 't2'), 'b'): {('s3', 't1')},
                (('s0', 't3'), 'a'): {('s1', 't1'), ('s1', 't4')},
                (('s0', 't3'), 'b'): {('s3', 't3'), ('s3', 't0')},
                (('s0', 't4'), 'a'): {('s1', 't4')},
                (('s0', 't4'), 'b'): {('s3', 't0')},
                (('s1', 't0'), 'a'): {('s4', 't2')},
                (('s1', 't0'), 'b'): {('s2', 't1')},
                (('s1', 't1'), 'b'): {('s2', 't4')},
                (('s1', 't2'), 'a'): {('s4', 't2'), ('s4', 't4')},
                (('s1', 't2'), 'b'): {('s2', 't1')},
                (('s1', 't3'), 'a'): {('s4', 't1'), ('s4', 't4')},
                (('s1', 't3'), 'b'): {('s2', 't3'), ('s2', 't0')},
                (('s1', 't4'), 'a'): {('s4', 't4')},
                (('s1', 't4'), 'b'): {('s2', 't0')},
                (('s2', 't0'), 'b'): {('s2', 't1'), ('s0', 't1')},
                (('s2', 't1'), 'b'): {('s2', 't4'), ('s0', 't4')},
                (('s2', 't2'), 'b'): {('s2', 't1'), ('s0', 't1')},
                (('s2', 't3'), 'b'): {('s2', 't3'), ('s0', 't3'), ('s2', 't0'), ('s0', 't0')},
                (('s2', 't4'), 'b'): {('s2', 't0'), ('s0', 't0')},
                (('s3', 't0'), 'a'): {('s2', 't2')},
                (('s3', 't0'), 'b'): {('s4', 't1')},
                (('s3', 't1'), 'b'): {('s4', 't4')},
                (('s3', 't2'), 'a'): {('s2', 't2'), ('s2', 't4')},
                (('s3', 't2'), 'b'): {('s4', 't1')},
                (('s3', 't3'), 'a'): {('s2', 't1'), ('s2', 't4')},
                (('s3', 't3'), 'b'): {('s4', 't3'), ('s4', 't0')},
                (('s3', 't4'), 'a'): {('s2', 't4')},
                (('s3', 't4'), 'b'): {('s4', 't0')},
                (('s4', 't0'), 'a'): {('s4', 't2')},
                (('s4', 't0'), 'b'): {('s0', 't1')},
                (('s4', 't1'), 'b'): {('s0', 't4')},
                (('s4', 't2'), 'a'): {('s4', 't2'), ('s4', 't4')},
                (('s4', 't2'), 'b'): {('s0', 't1')},
                (('s4', 't3'), 'a'): {('s4', 't1'), ('s4', 't4')},
                (('s4', 't3'), 'b'): {('s0', 't3'), ('s0', 't0')},
                (('s4', 't4'), 'a'): {('s4', 't4')},
                (('s4', 't4'), 'b'): {('s0', 't0')}
            }
        }
        self.nfa_intersection_test_02_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_states': set(),
            'accepting_states': set(),
            'transitions': {}
        }

    def test_nfa_intersection(self):
        """ Tests a correct NFAs intersection """
        intersection = NFA.nfa_intersection(self.nfa_intersection_1_test_01, self.nfa_intersection_2_test_01)
        automata_IO.nfa_graphviz_render(intersection, 'nfa_intersection')
        self.assertDictEqual(intersection, self.nfa_intersection_test_01_solution)

    def test_nfa_intersection_empty(self):
        """ Tests a NFAs intersection where one of them is empty """
        intersection = NFA.nfa_intersection(self.nfa_intersection_1_test_01, self.nfa_intersection_test_02_empty)
        self.assertDictEqual(intersection, self.nfa_intersection_test_02_empty)

    @unittest.expectedFailure
    def test_nfa_intersection_wrong_input_1(self):
        """ Tests an input different from a dict() object. [EXPECTED FAILURE] """
        NFA.nfa_intersection(0, self.nfa_intersection_2_test_01)

    @unittest.expectedFailure
    def test_nfa_intersection_wrong_input_2(self):
        """ Tests an input different from a dict() object. [EXPECTED FAILURE] """
        NFA.nfa_intersection(self.nfa_intersection_1_test_01, 0)

    @unittest.expectedFailure
    def test_nfa_intersection_wrong_dict_1(self):
        """ Tests a dict() in input different from a well formatted dict() representing a NFA. [EXPECTED FAILURE]"""
        NFA.nfa_intersection({'goofy': 'donald'}, self.nfa_intersection_2_test_01)

    @unittest.expectedFailure
    def test_nfa_intersection_wrong_dict_2(self):
        """ Tests a dict() in input different from a well formatted dict() representing a NFA. [EXPECTED FAILURE]"""
        NFA.nfa_intersection(self.nfa_intersection_1_test_01, {'goofy': 'donald'})

    def test_nfa_intersection_side_effects(self):
        """ Tests that the intersection function doesn't make side effects on input DFAs"""
        before_1 = copy.deepcopy(self.nfa_intersection_1_test_01)
        before_2 = copy.deepcopy(self.nfa_intersection_2_test_01)
        NFA.nfa_intersection(self.nfa_intersection_1_test_01, self.nfa_intersection_2_test_01)
        self.assertDictEqual(before_1, self.nfa_intersection_1_test_01)
        self.assertDictEqual(before_2, self.nfa_intersection_2_test_01)


class TestNfaUnion(TestCase):
    @unittest.skip("TestNfaUnion TODO")
    def test_nfa_union(self):
        self.fail()


class TestNfaDeterminization(TestCase):
    @unittest.skip("TestNfaDeterminization TODO")
    def test_nfa_determinization(self):
        self.fail()


class TestNfaComplementation(TestCase):
    @unittest.skip("TestNfaComplementation TODO")
    def test_nfa_complementation(self):
        self.fail()


class TestNfaNonemptinessCheck(TestCase):
    @unittest.skip("TestNfaNonemptinessCheck TODO")
    def test_nfa_nonemptiness_check(self):
        self.fail()


class TestNfaNonuniversalityCheck(TestCase):
    @unittest.skip("TestNfaNonuniversalityCheck TODO")
    def test_nfa_nonuniversality_check(self):
        self.fail()


class TestNfaInterestingnessCheck(TestCase):
    @unittest.skip("TestNfaInterestingnessCheck TODO")
    def test_nfa_interestingness_check(self):
        self.fail()


class TestRunAcceptance(TestCase):
    @unittest.skip("TestRunAcceptance TODO")
    def test_run_acceptance(self):
        self.fail()


class TestWordAcceptance(TestCase):
    @unittest.skip("TestWordAcceptance TODO")
    def test_word_acceptance(self):
        self.fail()
