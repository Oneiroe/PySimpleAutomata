from unittest import TestCase
import unittest
import DFA
import automata_IO


class TestRunAcceptance(TestCase):
    def setUp(self):
        self.dfa_run_acceptance_test_01 = automata_IO.dfa_dot_importer('./dot/dfa_run_acceptance_test_01.dot')
        self.dfa_run_acceptance_test_02 = automata_IO.dfa_dot_importer('./dot/dfa_run_acceptance_test_02.dot')

    def test_run_acceptance(self):
        """ Tests a correct run """
        self.assertTrue(
            DFA.run_acceptance(self.dfa_run_acceptance_test_01, ['s0', 's1', 's3', 's0'], ['5c', '10c', 'gum']))

    def test_run_acceptance_false(self):
        """ Tests a non correct run, good alphabet"""
        self.assertFalse(DFA.run_acceptance(self.dfa_run_acceptance_test_01, ['s0', 's1', 's3'], ['5c', '10c']))

    def test_run_acceptance_wrong_alphabet(self):
        """ Tests a non correct run with letters not present in the alphabet"""
        self.assertFalse(
            DFA.run_acceptance(self.dfa_run_acceptance_test_01, ['s0', 's1', 's3', 's0'], ['5c', '10c', 'wrong']))

    def test_run_acceptance_wrong_states(self):
        """ Tests a non correct run with states not present in the dfa"""
        self.assertFalse(
            DFA.run_acceptance(self.dfa_run_acceptance_test_01, ['s0', 's1', 'fake', 's0'], ['5c', '10c', 'gum']))

    def test_run_acceptance_empty_run(self):
        """ Tests an empty run """
        self.assertFalse(
            DFA.run_acceptance(self.dfa_run_acceptance_test_02, [], []))

    def test_run_acceptance_wrong_sizes(self):
        """ Tests run and word with wrong sizes """
        self.assertFalse(
            DFA.run_acceptance(self.dfa_run_acceptance_test_02, ['s0', 's1', 's3'], ['5c']))

    @unittest.expectedFailure
    def test_word_acceptance_wrong_input_1(self):
        """ Tests an input different from a dict() object. [EXPECTED FAILURE]"""
        DFA.run_acceptance(1, ['s0', 's1', 's3', 's0'], ['5c', '10c', 'gum'])

    @unittest.expectedFailure
    def test_word_acceptance_wrong_input_2(self):
        """ Tests an input different from a list() object. [EXPECTED FAILURE]"""
        DFA.run_acceptance(self.dfa_run_acceptance_test_01, 1, ['5c', '10c', 'gum'])

    @unittest.expectedFailure
    def test_word_acceptance_wrong_input_3(self):
        """ Tests an input different from a list() object. [EXPECTED FAILURE]"""
        DFA.run_acceptance(self.dfa_run_acceptance_test_01, ['s0', 's1', 's3', 's0'], 1)

    @unittest.expectedFailure
    def test_word_acceptance_wrong_dict(self):
        """ Tests a dict() in input different from a well formatted dict() representing a DFA. [EXPECTED FAILURE]"""
        DFA.run_acceptance({'goofy': 'donald'}, ['s0', 's1', 's3', 's0'], ['5c', '10c', 'gum'])


class TestWordAcceptance(TestCase):
    def setUp(self):
        self.dfa_word_acceptance_test_01 = automata_IO.dfa_dot_importer('./dot/dfa_word_acceptance_test_01.dot')
        self.dfa_word_acceptance_test_02 = automata_IO.dfa_dot_importer('./dot/dfa_word_acceptance_test_02.dot')

    def test_word_acceptance(self):
        """ Tests a correct word """
        self.assertTrue(DFA.word_acceptance(self.dfa_word_acceptance_test_01, ['5c', '10c', 'gum', '5c', '10c', 'gum']))

    def test_word_acceptance_false(self):
        """ Tests a non correct word, with good alphabet"""
        self.assertFalse(DFA.word_acceptance(self.dfa_word_acceptance_test_01, ['5c', '10c', 'gum', '5c', '10c']))

    def test_word_acceptance_wrong_alphabet(self):
        """ Tests a non correct word, with letters not form the dfa alphabet """
        self.assertFalse(DFA.word_acceptance(self.dfa_word_acceptance_test_01, ['5c', '10c', 'wrong']))

    def test_word_acceptance_empty_word(self):
        """ Tests an empty word"""
        self.assertFalse(DFA.word_acceptance(self.dfa_word_acceptance_test_02, []))

    @unittest.expectedFailure
    def test_word_acceptance_wrong_input_1(self):
        """ Tests an input different from a dict() object. [EXPECTED FAILURE]"""
        DFA.word_acceptance(1, ['5c', '10c', 'gum', '5c', '10c'])

    @unittest.expectedFailure
    def test_word_acceptance_wrong_input_2(self):
        """ Tests an input different from a list() object. [EXPECTED FAILURE]"""
        DFA.word_acceptance(self.dfa_word_acceptance_test_01, 1)

    @unittest.expectedFailure
    def test_word_acceptance_wrong_dict(self):
        """ Tests a dict() in input different from a well formatted dict() representing a DFA. [EXPECTED FAILURE]"""
        DFA.word_acceptance({'goofy': 'donald'}, ['5c', '10c', 'gum', '5c', '10c'])


class TestDfaCompletion(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_completion_test_01 = automata_IO.dfa_dot_importer('./dot/dfa_completion_test_01.dot')
        self.dfa_completion_test_02 = automata_IO.dfa_dot_importer('./dot/dfa_completion_test_02.dot')
        self.dfa_completion_test_03 = automata_IO.dfa_dot_importer('./dot/dfa_completion_test_03.dot')
        self.dfa_completion_test_01_completed = automata_IO.dfa_dot_importer(
            './dot/dfa_completion_test_01_completed.dot')
        self.dfa_completion_test_02_completed = automata_IO.dfa_dot_importer(
            './dot/dfa_completion_test_02_completed.dot')
        self.dfa_completion_test_03_completed = automata_IO.dfa_dot_importer(
            './dot/dfa_completion_test_03_completed.dot')

    def test_dfa_completion(self):
        """ Tests a correct completion """
        self.assertDictEqual(DFA.dfa_completion(self.dfa_completion_test_01), self.dfa_completion_test_01_completed)

    def test_dfa_completion_empty_states(self):
        """ Tests a completion of a dfa without states"""
        self.assertDictEqual(DFA.dfa_completion(self.dfa_completion_test_02), self.dfa_completion_test_02_completed)

    def test_dfa_completion_empty_transitions(self):
        """ Tests a completion of a dfa without transitions"""
        self.assertDictEqual(DFA.dfa_completion(self.dfa_completion_test_03), self.dfa_completion_test_03_completed)

    # @unittest.expectedFailure means that the code doesn't handle this situation/exception consciously
    @unittest.expectedFailure
    def test_dfa_completion_wrong_input(self):
        """ Tests an input different from a dict() object. [EXPECTED FAILURE]"""
        DFA.dfa_completion(1)

    @unittest.expectedFailure
    def test_dfa_completion_wrong_dict(self):
        """ Tests a dict() in input different from a well formatted dict() representing a DFA. [EXPECTED FAILURE]"""
        DFA.dfa_completion({'goofy': 'donald'})


class TestDfaComplementation(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_complementation_test_01 = automata_IO.dfa_dot_importer('./dot/dfa_complementation_test_01.dot')
        self.dfa_complementation_test_01_complemented = automata_IO.dfa_dot_importer(
            './dot/dfa_complementation_test_01_complemented.dot')
        self.dfa_complementation_test_02 = automata_IO.dfa_dot_importer('./dot/dfa_complementation_test_02.dot')
        self.dfa_complementation_test_02_complemented = automata_IO.dfa_dot_importer(
            './dot/dfa_complementation_test_02_complemented.dot')
        self.dfa_complementation_test_03 = automata_IO.dfa_dot_importer('./dot/dfa_complementation_test_03.dot')
        self.dfa_complementation_test_03_complemented = automata_IO.dfa_dot_importer(
            './dot/dfa_complementation_test_03_complemented.dot')

    def test_dfa_complementation(self):
        """ Tests a correct complementation. """
        self.assertDictEqual(DFA.dfa_complementation(self.dfa_complementation_test_01),
                             self.dfa_complementation_test_01_complemented)

    def test_dfa_complementation_empty_states(self):
        """ Tests a complementation on a DFA without states. """
        # TODO ask about this behaviour: shouldn't it returns a dfa that reads Σ* ?
        self.assertDictEqual(DFA.dfa_complementation(self.dfa_complementation_test_02),
                             self.dfa_complementation_test_02_complemented)

    def test_dfa_complementation_empty_transitions(self):
        """ Tests a complementation on a DFA without transitions. """
        # TODO ask about this behaviour: shouldn't it returns a dfa that reads Σ* ?
        self.assertDictEqual(DFA.dfa_complementation(self.dfa_complementation_test_03),
                             self.dfa_complementation_test_03_complemented)

    @unittest.expectedFailure
    def test_dfa_complementation_wrong_input(self):
        """ Tests an input different from a dict() object. [EXPECTED FAILURE]"""
        DFA.dfa_complementation(1)

    @unittest.expectedFailure
    def test_dfa_complementation_wrong_dict(self):
        """ Tests a dict() in input different from a well formatted dict() representing a DFA. [EXPECTED FAILURE]"""
        DFA.dfa_complementation({'goofy': 'donald'})


class TestDfaIntersection(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_intersection_1_test_01 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_1_test_01.dot')
        self.dfa_intersection_2_test_01 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_2_test_01.dot')
        self.dfa_intersection_test_01_intersection = automata_IO.dfa_dot_importer(
            './dot/dfa_intersection_test_01_intersection.dot')
        self.dfa_intersection_1_test_02 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_1_test_02.dot')
        self.dfa_intersection_2_test_02 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_2_test_02.dot')
        self.dfa_intersection_test_02_intersection = automata_IO.dfa_dot_importer(
            './dot/dfa_intersection_test_02_intersection.dot')

        self.dfa_test_disjoint = {
            'alphabet': {'5c', '10c', 'gum'},
            'states': {
                ('s3', 't2'),
                ('s3', 't3'),
                ('s0', 't3'),
                ('s2', 't3'),
                ('s2', 't0'),
                ('s1', 't2'),
                ('s0', 't0'),
                ('s1', 't4'),
                ('s0', 't1'),
                ('s0', 't5'),
                ('s2', 't1'),
                ('s2', 't5'),
                ('s3', 't4'),
                ('s3', 't0'),
                ('s0', 't2'),
                ('s2', 't2'),
                ('s1', 't0'),
                ('s1', 't3'),
                ('s1', 't5'),
                ('s3', 't1'),
                ('s0', 't4'),
                ('s2', 't4'),
                ('s3', 't5'),
                ('s1', 't1')
            },
            'initial_state': ('s0', 't0'),
            'accepting_states': {('s0', 't5'), ('s0', 't4')},
            'transitions': {
                (('s3', 't3'), 'gum'): ('s0', 't1'),
                (('s0', 't1'), '10c'): ('s2', 't2'),
                (('s3', 't2'), 'gum'): ('s0', 't4'),
                (('s0', 't1'), '5c'): ('s1', 't5'),
                (('s2', 't1'), '10c'): ('s3', 't2'),
                (('s1', 't0'), '5c'): ('s2', 't1'),
                (('s1', 't1'), '10c'): ('s3', 't2'),
                (('s2', 't0'), '5c'): ('s3', 't1'),
                (('s0', 't2'), '5c'): ('s1', 't3'),
                (('s1', 't1'), '5c'): ('s2', 't5'),
                (('s3', 't5'), 'gum'): ('s0', 't0'),
                (('s1', 't2'), '5c'): ('s2', 't3'),
                (('s2', 't2'), '5c'): ('s3', 't3'),
                (('s2', 't1'), '5c'): ('s3', 't5'),
                (('s0', 't0'), '5c'): ('s1', 't1')
            }
        }
        self.dfa_test_intersecting = {
            'alphabet': {'5c', '10c', 'gum'},
            'states': {
                ('s1', 'c2'), ('c3', 't2'), ('c2', 'c3'), ('c1', 'c1'), ('s1', 't2'), ('c1', 't2'), ('c3', 'c2'),
                ('s1', 't0'), ('c1', 'c2'), ('c2', 't1'), ('s0', 'c2'), ('c3', 't0'), ('s0', 't2'), ('s0', 'c4'),
                ('c4', 't2'), ('c3', 't1'), ('c4', 'c2'), ('s1', 't1'), ('c1', 'c3'), ('c2', 'c1'), ('s0', 't3'),
                ('c2', 'c4'), ('c4', 't0'), ('s0', 'c1'), ('s0', 't0'), ('c1', 't3'), ('c4', 't3'), ('c3', 'c1'),
                ('c4', 'c3'), ('c4', 't1'), ('c3', 'c4'), ('s1', 'c1'), ('s1', 'c4'), ('c1', 'c4'), ('c1', 't0'),
                ('s0', 't1'), ('s1', 't3'), ('s1', 'c3'), ('c1', 't1'), ('c3', 't3'), ('c2', 'c2'), ('c4', 'c1'),
                ('c3', 'c3'), ('c2', 't2'), ('c4', 'c4'), ('c2', 't0'), ('s0', 'c3'), ('c2', 't3')
            },
            'initial_state': ('s0', 't0'),
            'accepting_states': {('s1', 'c4'), ('s1', 't3'), ('c4', 't3'), ('c4', 'c4')},
            'transitions': {
                (('c2', 't2'), 'gum'): ('c4', 't0'), (('s0', 't0'), '5c'): ('c1', 'c1'),
                (('s0', 'c3'), 'gum'): ('s1', 'c1'), (('s0', 'c2'), '5c'): ('c1', 'c3'),
                (('s0', 't1'), '5c'): ('c1', 't2'), (('c1', 'c1'), '10c'): ('c2', 'c2'),
                (('c2', 't1'), '5c'): ('c3', 't2'), (('c1', 't0'), '10c'): ('c2', 't1'),
                (('c3', 't2'), 'gum'): ('c1', 't0'), (('s0', 't1'), 'gum'): ('s1', 't3'),
                (('c2', 'c2'), 'gum'): ('c4', 'c4'), (('s0', 't2'), 'gum'): ('s1', 't0'),
                (('c3', 'c3'), 'gum'): ('c1', 'c1'), (('c2', 'c3'), 'gum'): ('c4', 'c1'),
                (('c2', 'c2'), '5c'): ('c3', 'c3'), (('s0', 'c2'), 'gum'): ('s1', 'c4'),
                (('c3', 't1'), 'gum'): ('c1', 't3'), (('c2', 't1'), 'gum'): ('c4', 't3'),
                (('c3', 'c2'), 'gum'): ('c1', 'c4'), (('c2', 't0'), '5c'): ('c3', 'c1')
            }
        }
        self.dfa_test_equals = {
            'alphabet': {'5c', '10c', 'gum'},
            'states': {
                ('s1', 's0'), ('s0', 's1'), ('s3', 's3'), ('s2', 's2'), ('s0', 's0'), ('s1', 's1'), ('s1', 's3'),
                ('s0', 's3'), ('s1', 's2'), ('s2', 's3'), ('s0', 's2'), ('s2', 's0'), ('s2', 's1'), ('s3', 's0'),
                ('s3', 's1'), ('s3', 's2')
            },
            'initial_state': ('s0', 's0'),
            'accepting_states': {('s0', 's0')},
            'transitions': {
                (('s1', 's0'), '10c'): ('s3', 's2'), (('s0', 's1'), '10c'): ('s2', 's3'),
                (('s1', 's1'), '10c'): ('s3', 's3'), (('s0', 's2'), '5c'): ('s1', 's3'),
                (('s2', 's2'), '5c'): ('s3', 's3'), (('s2', 's2'), '10c'): ('s3', 's3'),
                (('s0', 's0'), '10c'): ('s2', 's2'), (('s1', 's2'), '5c'): ('s2', 's3'),
                (('s2', 's1'), '10c'): ('s3', 's3'), (('s0', 's2'), '10c'): ('s2', 's3'),
                (('s2', 's0'), '5c'): ('s3', 's1'), (('s2', 's0'), '10c'): ('s3', 's2'),
                (('s2', 's1'), '5c'): ('s3', 's2'), (('s1', 's0'), '5c'): ('s2', 's1'),
                (('s0', 's1'), '5c'): ('s1', 's2'), (('s3', 's3'), 'gum'): ('s0', 's0'),
                (('s1', 's1'), '5c'): ('s2', 's2'), (('s1', 's2'), '10c'): ('s3', 's3'),
                (('s0', 's0'), '5c'): ('s1', 's1')
            }
        }

        self.dfa_test_side_effect_1 = {
            'alphabet': {'5c', '10c', 'gum'},
            'states': {'s0', 's1', 's2', 's3'},
            'initial_state': 's0',
            'accepting_states': {'s0'},
            'transitions': {('s0', '5c'): 's1',
                            ('s0', '10c'): 's2',
                            ('s1', '5c'): 's2',
                            ('s1', '10c'): 's3',
                            ('s2', '5c'): 's3',
                            ('s2', '10c'): 's3',
                            ('s3', 'gum'): 's0'}
        }
        self.dfa_test_side_effect_2 = {
            'alphabet': {'5c', '10c', 'gum'},
            'states': {
                ('s3', 't2'),
                ('s3', 't3'),
                ('s0', 't3'),
                ('s2', 't3'),
                ('s2', 't0'),
                ('s1', 't2'),
                ('s0', 't0'),
                ('s1', 't4'),
                ('s0', 't1'),
                ('s0', 't5'),
                ('s2', 't1'),
                ('s2', 't5'),
                ('s3', 't4'),
                ('s3', 't0'),
                ('s0', 't2'),
                ('s2', 't2'),
                ('s1', 't0'),
                ('s1', 't3'),
                ('s1', 't5'),
                ('s3', 't1'),
                ('s0', 't4'),
                ('s2', 't4'),
                ('s3', 't5'),
                ('s1', 't1')
            },
            'initial_state': ('s0', 't0'),
            'accepting_states': {('s0', 't5'), ('s0', 't4')},
            'transitions': {
                (('s3', 't3'), 'gum'): ('s0', 't1'),
                (('s0', 't1'), '10c'): ('s2', 't2'),
                (('s3', 't2'), 'gum'): ('s0', 't4'),
                (('s0', 't1'), '5c'): ('s1', 't5'),
                (('s2', 't1'), '10c'): ('s3', 't2'),
                (('s1', 't0'), '5c'): ('s2', 't1'),
                (('s1', 't1'), '10c'): ('s3', 't2'),
                (('s2', 't0'), '5c'): ('s3', 't1'),
                (('s0', 't2'), '5c'): ('s1', 't3'),
                (('s1', 't1'), '5c'): ('s2', 't5'),
                (('s3', 't5'), 'gum'): ('s0', 't0'),
                (('s1', 't2'), '5c'): ('s2', 't3'),
                (('s2', 't2'), '5c'): ('s3', 't3'),
                (('s2', 't1'), '5c'): ('s3', 't5'),
                (('s0', 't0'), '5c'): ('s1', 't1')
            }
        }

    def test_dfa_intersection_disjoint(self):
        """ Tests a correct intersection between disjointed DFAs """
        # TODO ask: FORMALLY, should it returns a minimal dfa or this one with states not reached by initial state?
        self.assertDictEqual(DFA.dfa_intersection(self.dfa_intersection_1_test_01, self.dfa_intersection_2_test_01),
                             self.dfa_test_disjoint)

    def test_dfa_intersection_intersecting(self):
        """ Tests a correct intersection between DFAs partially intersected"""
        # TODO ask: FORMALLY, should it returns a minimal dfa or this one with states not reached by initial state?
        self.assertDictEqual(DFA.dfa_intersection(self.dfa_intersection_1_test_02, self.dfa_intersection_2_test_02),
                             self.dfa_test_intersecting)

    def test_dfa_intersection_equals(self):
        """ Tests a correct intersection between the same DFA """
        # TODO ask: FORMALLY, should it returns a minimal dfa or this one with states not reached by initial state?
        self.assertDictEqual(DFA.dfa_intersection(self.dfa_intersection_1_test_01, self.dfa_intersection_1_test_01),
                             self.dfa_test_equals)

    @unittest.expectedFailure
    def test_dfa_intersection_wrong_input_1(self):
        """ Tests an input different from a dict() object. [EXPECTED FAILURE] """
        DFA.dfa_intersection(1, self.dfa_intersection_2_test_01)

    @unittest.expectedFailure
    def test_dfa_intersection_wrong_input_2(self):
        """ Tests an input different from a dict() object. [EXPECTED FAILURE]"""
        DFA.dfa_intersection(self.dfa_intersection_1_test_01, 1)

    @unittest.expectedFailure
    def test_dfa_intersection_wrong_dict_1(self):
        """ Tests a dict() in input different from a well formatted dict() representing a DFA. [EXPECTED FAILURE]"""
        DFA.dfa_intersection({'goofy': 'donald'}, self.dfa_intersection_2_test_01)

    @unittest.expectedFailure
    def test_dfa_intersection_wrong_dict_2(self):
        """ Tests a dict() in input different from a well formatted dict() representing a DFA. [EXPECTED FAILURE]"""
        DFA.dfa_intersection(self.dfa_intersection_1_test_01, {'goofy': 'donald'})

    def test_dfa_intersection_side_effects(self):
        """ Tests that the intersection function doesn't makes side effects on input DFAs"""
        intersection = DFA.dfa_intersection(self.dfa_test_side_effect_1, self.dfa_test_side_effect_2)
        self.dfa_test_side_effect_1['alphabet'].pop()
        self.assertNotEquals(self.dfa_test_side_effect_1['alphabet'], intersection['alphabet'])


class TestDfaUnion(TestCase):
    def setUp(self):
        self.dfa = automata_IO.dfa_json_importer('../json/dfa_test.json')
        self.dfa_2 = automata_IO.dfa_json_importer('../json/dfa_f03_ai.json')
        self.dfa_3 = automata_IO.dfa_json_importer('../json/dfa_f03_ai.json')

    @unittest.skip("TestDfaUnion TODO")
    def test_dfa_union(self):
        self.fail()


class TestDfaMinimization(TestCase):
    def setUp(self):
        self.dfa = automata_IO.dfa_json_importer('../json/dfa_test.json')
        self.dfa_2 = automata_IO.dfa_json_importer('../json/dfa_f03_ai.json')
        self.dfa_3 = automata_IO.dfa_json_importer('../json/dfa_f03_ai.json')

    @unittest.skip("TestDfaMinimization TODO")
    def test_dfa_minimization(self):
        self.fail()


class TestDfaReachable(TestCase):
    def setUp(self):
        self.dfa = automata_IO.dfa_json_importer('../json/dfa_test.json')
        self.dfa_2 = automata_IO.dfa_json_importer('../json/dfa_f03_ai.json')
        self.dfa_3 = automata_IO.dfa_json_importer('../json/dfa_f03_ai.json')

    @unittest.skip("TestDfaIntersection TODO")
    def test_dfa_reachable(self):
        self.fail()
