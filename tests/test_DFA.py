from unittest import TestCase
import unittest
import DFA
import automata_IO
import copy


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

    def test_dfa_completion_side_effects(self):
        """ Tests the function correctly makes side effects on input """
        completed = DFA.dfa_completion(self.dfa_completion_test_01)
        completed['states'].pop()
        self.assertDictEqual(completed, self.dfa_completion_test_01)

    def test_dfa_completion_side_effects_copy(self):
        """ Tests the function doesn't make side effects if a copy is passed as input """
        completed = DFA.dfa_completion(copy.deepcopy(self.dfa_completion_test_01))
        self.assertNotEquals(completed, self.dfa_completion_test_01)


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

    def test_dfa_complementation_side_effects(self):
        """ Tests the function doesn't make side effects on input """
        complemented = DFA.dfa_complementation(self.dfa_complementation_test_01)
        complemented['states'].pop()
        self.assertNotEquals(complemented, self.dfa_complementation_test_01)


class TestDfaIntersection(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_intersection_1_test_01 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_1_test_01.dot')
        self.dfa_intersection_2_test_01 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_2_test_01.dot')
        self.dfa_intersection_1_test_02 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_1_test_02.dot')
        self.dfa_intersection_2_test_02 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_2_test_02.dot')

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

    def test_dfa_intersection_side_effects_alphabet(self):
        """ Tests that the intersection function doesn't make side effects on input DFAs alphabet"""
        intersection = DFA.dfa_intersection(self.dfa_test_side_effect_1, self.dfa_test_side_effect_2)
        self.dfa_test_side_effect_1['alphabet'].pop()
        self.assertNotEquals(self.dfa_test_side_effect_1['alphabet'], intersection['alphabet'])

    def test_dfa_intersection_side_effects_initial_state(self):
        """ Tests that the intersection function doesn't make side effects on input DFAs initial state"""
        intersection = DFA.dfa_intersection(self.dfa_test_side_effect_1, self.dfa_test_side_effect_2)
        self.dfa_test_side_effect_1['initial_state'] = 'pippo'
        result = self.dfa_test_side_effect_1['initial_state'] in intersection['initial_state']
        self.assertFalse(result)


class TestDfaUnion(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_union_1_test_01 = automata_IO.dfa_dot_importer('./dot/dfa_union_1_test_01.dot')
        self.dfa_union_2_test_01 = automata_IO.dfa_dot_importer('./dot/dfa_union_2_test_01.dot')
        self.dfa_union_1_test_02 = automata_IO.dfa_dot_importer('./dot/dfa_union_1_test_02.dot')
        self.dfa_union_2_test_02 = automata_IO.dfa_dot_importer('./dot/dfa_union_2_test_02.dot')

        self.dfa_test_disjoint = {
            'alphabet': {'5c', '10c', 'gum'},
            'states': {
                ('s3', 't4'), ('s2', 't5'), ('s0', 't5'), ('s1', 't0'), ('s0', 't1'), ('sink', 'sink'),
                ('s2', 't3'), ('s3', 't0'), ('sink', 't4'), ('sink', 't3'), ('s3', 'sink'), ('s1', 't5'),
                ('s3', 't2'), ('s1', 'sink'), ('s3', 't5'), ('s2', 't0'), ('s0', 't4'), ('s1', 't3'),
                ('s2', 't4'), ('s0', 't2'), ('sink', 't1'), ('sink', 't5'), ('s2', 't2'), ('s0', 'sink'),
                ('s2', 'sink'), ('sink', 't2'), ('s2', 't1'), ('s1', 't1'), ('s0', 't0'), ('sink', 't0'),
                ('s3', 't1'), ('s1', 't2'), ('s3', 't3'), ('s0', 't3'), ('s1', 't4')
            },
            'initial_state': ('s0', 't0'),
            'accepting_states': {
                ('s2', 't4'), ('s3', 't4'), ('s0', 't2'), ('s0', 't5'), ('s0', 't1'), ('s2', 't5'), ('s0', 'sink'),
                ('sink', 't5'), ('sink', 't4'), ('s0', 't0'), ('s1', 't5'), ('s3', 't5'), ('s0', 't4'), ('s0', 't3'),
                ('s1', 't4')
            },
            'transitions': {
                (('s3', 't3'), '10c'): ('sink', 'sink'), (('s3', 't2'), '5c'): ('sink', 't3'),
                (('s1', 't2'), '5c'): ('s2', 't3'), (('s3', 't5'), '10c'): ('sink', 'sink'),
                (('s0', 't0'), '10c'): ('s2', 'sink'), (('sink', 't0'), '5c'): ('sink', 't1'),
                (('sink', 't3'), '10c'): ('sink', 'sink'), (('sink', 't1'), '5c'): ('sink', 't5'),
                (('s2', 't2'), '10c'): ('s3', 'sink'), (('s1', 't5'), '10c'): ('s3', 'sink'),
                (('sink', 't3'), '5c'): ('sink', 'sink'), (('sink', 't5'), 'gum'): ('sink', 't0'),
                (('s0', 't1'), '10c'): ('s2', 't2'), (('s3', 't1'), '10c'): ('sink', 't2'),
                (('sink', 't5'), '5c'): ('sink', 'sink'), (('s2', 't1'), '10c'): ('s3', 't2'),
                (('s2', 't1'), '5c'): ('s3', 't5'), (('sink', 't1'), 'gum'): ('sink', 'sink'),
                (('sink', 't2'), '5c'): ('sink', 't3'), (('s0', 't4'), '10c'): ('s2', 'sink'),
                (('s3', 't0'), '10c'): ('sink', 'sink'), (('s2', 'sink'), '10c'): ('s3', 'sink'),
                (('s0', 't2'), 'gum'): ('sink', 't4'), (('s3', 't4'), '10c'): ('sink', 'sink'),
                (('s0', 't3'), '10c'): ('s2', 'sink'), (('s0', 't3'), '5c'): ('s1', 'sink'),
                (('s3', 't3'), 'gum'): ('s0', 't1'), (('sink', 't2'), 'gum'): ('sink', 't4'),
                (('s3', 't5'), '5c'): ('sink', 'sink'), (('s1', 'sink'), 'gum'): ('sink', 'sink'),
                (('s2', 't4'), '10c'): ('s3', 'sink'), (('s3', 'sink'), 'gum'): ('s0', 'sink'),
                (('s1', 't1'), '5c'): ('s2', 't5'), (('s1', 't0'), 'gum'): ('sink', 'sink'),
                (('s0', 'sink'), '10c'): ('s2', 'sink'), (('sink', 't5'), '10c'): ('sink', 'sink'),
                (('s0', 't1'), '5c'): ('s1', 't5'), (('s0', 't0'), 'gum'): ('sink', 'sink'),
                (('sink', 't4'), '5c'): ('sink', 'sink'), (('sink', 't3'), 'gum'): ('sink', 't1'),
                (('s1', 't4'), '10c'): ('s3', 'sink'), (('s0', 't5'), 'gum'): ('sink', 't0'),
                (('s1', 't2'), 'gum'): ('sink', 't4'), (('sink', 't0'), 'gum'): ('sink', 'sink'),
                (('s3', 't2'), 'gum'): ('s0', 't4'), (('s1', 't2'), '10c'): ('s3', 'sink'),
                (('s2', 't5'), 'gum'): ('sink', 't0'), (('s2', 't4'), '5c'): ('s3', 'sink'),
                (('s0', 't2'), '10c'): ('s2', 'sink'), (('s2', 't0'), '10c'): ('s3', 'sink'),
                (('sink', 'sink'), '5c'): ('sink', 'sink'), (('s1', 't4'), '5c'): ('s2', 'sink'),
                (('s1', 't1'), '10c'): ('s3', 't2'), (('s2', 't2'), '5c'): ('s3', 't3'),
                (('sink', 't1'), '10c'): ('sink', 't2'), (('s0', 't4'), 'gum'): ('sink', 'sink'),
                (('s3', 't0'), 'gum'): ('s0', 'sink'), (('sink', 't4'), '10c'): ('sink', 'sink'),
                (('s2', 'sink'), 'gum'): ('sink', 'sink'), (('s2', 't3'), '5c'): ('s3', 'sink'),
                (('s3', 't4'), 'gum'): ('s0', 'sink'), (('s1', 't0'), '10c'): ('s3', 'sink'),
                (('s0', 'sink'), 'gum'): ('sink', 'sink'), (('s3', 't1'), '5c'): ('sink', 't5'),
                (('s2', 't3'), 'gum'): ('sink', 't1'), (('sink', 't2'), '10c'): ('sink', 'sink'),
                (('s1', 'sink'), '10c'): ('s3', 'sink'), (('s3', 't5'), 'gum'): ('s0', 't0'),
                (('s0', 't3'), 'gum'): ('sink', 't1'), (('s2', 't2'), 'gum'): ('sink', 't4'),
                (('s3', 'sink'), '10c'): ('sink', 'sink'), (('s1', 't5'), 'gum'): ('sink', 't0'),
                (('s2', 't0'), '5c'): ('s3', 't1'), (('sink', 'sink'), 'gum'): ('sink', 'sink'),
                (('s1', 't3'), '10c'): ('s3', 'sink'), (('s3', 't2'), '10c'): ('sink', 'sink'),
                (('s2', 't5'), '10c'): ('s3', 'sink'), (('s2', 't5'), '5c'): ('s3', 'sink'),
                (('s2', 't0'), 'gum'): ('sink', 'sink'), (('s1', 't5'), '5c'): ('s2', 'sink'),
                (('s2', 't1'), 'gum'): ('sink', 'sink'), (('s0', 't5'), '5c'): ('s1', 'sink'),
                (('s0', 't5'), '10c'): ('s2', 'sink'), (('sink', 't0'), '10c'): ('sink', 'sink'),
                (('s1', 't4'), 'gum'): ('sink', 'sink'), (('sink', 't4'), 'gum'): ('sink', 'sink'),
                (('s0', 't0'), '5c'): ('s1', 't1'), (('s0', 't1'), 'gum'): ('sink', 'sink'),
                (('s3', 't1'), 'gum'): ('s0', 'sink'), (('s0', 'sink'), '5c'): ('s1', 'sink'),
                (('s3', 't4'), '5c'): ('sink', 'sink'), (('s3', 'sink'), '5c'): ('sink', 'sink'),
                (('s1', 't0'), '5c'): ('s2', 't1'), (('s1', 't1'), 'gum'): ('sink', 'sink'),
                (('s2', 'sink'), '5c'): ('s3', 'sink'), (('s2', 't3'), '10c'): ('s3', 'sink'),
                (('s1', 't3'), 'gum'): ('sink', 't1'), (('s0', 't4'), '5c'): ('s1', 'sink'),
                (('s1', 'sink'), '5c'): ('s2', 'sink'), (('s1', 't3'), '5c'): ('s2', 'sink'),
                (('s3', 't3'), '5c'): ('sink', 'sink'), (('s3', 't0'), '5c'): ('sink', 't1'),
                (('sink', 'sink'), '10c'): ('sink', 'sink'), (('s2', 't4'), 'gum'): ('sink', 'sink'),
                (('s0', 't2'), '5c'): ('s1', 't3')
            }
        }
        self.dfa_test_intersecting = {
            'alphabet': {'5c', '10c', 'gum'},
            'states': {
                ('c4', 'c2'), ('sink', 't0'), ('s0', 'c3'), ('s0', 't1'), ('sink', 'sink'), ('c2', 'c2'),
                ('c3', 'sink'), ('c1', 't2'), ('s0', 'c4'), ('c3', 't2'), ('s0', 't2'), ('s0', 't0'),
                ('s1', 't2'), ('s1', 'c4'), ('sink', 't3'), ('s1', 't0'), ('c3', 't1'), ('c2', 't1'),
                ('c1', 'c4'), ('c3', 'c1'), ('c3', 't0'), ('sink', 'c3'), ('c4', 't2'), ('c1', 't0'),
                ('c2', 'c1'), ('sink', 'c4'), ('c2', 't2'), ('c2', 't0'), ('c2', 'sink'), ('c3', 'c2'),
                ('c4', 't0'), ('sink', 'c2'), ('s1', 'c2'), ('c4', 't1'), ('c4', 'c4'), ('c4', 't3'),
                ('s0', 'c1'), ('c1', 'c2'), ('c1', 'sink'), ('c2', 't3'), ('c4', 'c3'), ('s1', 't3'),
                ('s0', 'sink'), ('sink', 't1'), ('s1', 'sink'), ('c2', 'c3'), ('c4', 'sink'), ('c1', 'c1'),
                ('c3', 'c3'), ('s0', 'c2'), ('c1', 't3'), ('s1', 'c3'), ('c1', 't1'), ('c2', 'c4'), ('c3', 't3'),
                ('c3', 'c4'), ('s1', 'c1'), ('c4', 'c1'), ('sink', 'c1'), ('s0', 't3'), ('c1', 'c3'),
                ('s1', 't1'), ('sink', 't2')
            },
            'initial_state': ('s0', 't0'),
            'accepting_states': {
                ('c4', 'c2'), ('c4', 't0'), ('s1', 'c2'), ('c4', 't1'), ('c4', 'c4'), ('c4', 't3'),
                ('s0', 'c4'), ('c2', 't3'), ('c4', 'c3'), ('s1', 't2'), ('s1', 'c4'), ('sink', 't3'),
                ('s1', 'sink'), ('s1', 't0'), ('c4', 'sink'), ('c1', 'c4'), ('c4', 't2'), ('s1', 'c3'),
                ('c1', 't3'), ('c2', 'c4'), ('s1', 'c1'), ('c3', 't3'), ('c3', 'c4'), ('c4', 'c1'),
                ('sink', 'c4'), ('s0', 't3'), ('s1', 't3'), ('s1', 't1')
            },
            'transitions': {
                (('s1', 'c2'), 'gum'): ('sink', 'c4'), (('sink', 't3'), '5c'): ('sink', 'sink'),
                (('s1', 'sink'), 'gum'): ('sink', 'sink'), (('s0', 'sink'), 'gum'): ('s1', 'sink'),
                (('c4', 't2'), 'gum'): ('sink', 't0'), (('s1', 'c3'), '10c'): ('sink', 'sink'),
                (('c2', 't0'), '5c'): ('c3', 'c1'), (('s1', 't3'), '5c'): ('sink', 'sink'),
                (('s1', 't2'), 'gum'): ('sink', 't0'), (('c3', 't0'), '5c'): ('sink', 'c1'),
                (('c2', 't0'), '10c'): ('sink', 't1'), (('c2', 'c2'), '5c'): ('c3', 'c3'),
                (('s0', 'c2'), '5c'): ('c1', 'c3'), (('sink', 't3'), 'gum'): ('sink', 'sink'),
                (('sink', 't1'), 'gum'): ('sink', 't3'), (('c3', 'c4'), '5c'): ('sink', 'sink'),
                (('c4', 't0'), '10c'): ('sink', 't1'), (('c4', 'c1'), '10c'): ('sink', 'c2'),
                (('s1', 'c1'), '10c'): ('sink', 'c2'), (('s1', 'c3'), 'gum'): ('sink', 'c1'),
                (('c1', 'c1'), '10c'): ('c2', 'c2'), (('c3', 't2'), 'gum'): ('c1', 't0'),
                (('c4', 'c1'), '5c'): ('sink', 'sink'), (('s1', 'c1'), '5c'): ('sink', 'sink'),
                (('c2', 't3'), 'gum'): ('c4', 'sink'), (('c4', 't3'), '10c'): ('sink', 'sink'),
                (('sink', 'sink'), '5c'): ('sink', 'sink'), (('c3', 't3'), 'gum'): ('c1', 'sink'),
                (('c1', 't3'), '10c'): ('c2', 'sink'), (('sink', 'c2'), '5c'): ('sink', 'c3'),
                (('s1', 'c2'), '10c'): ('sink', 'sink'), (('c4', 't3'), '5c'): ('sink', 'sink'),
                (('s0', 'c2'), '10c'): ('sink', 'sink'), (('s1', 't0'), '5c'): ('sink', 'c1'),
                (('c4', 't3'), 'gum'): ('sink', 'sink'), (('c3', 't2'), '5c'): ('sink', 'sink'),
                (('c3', 't0'), 'gum'): ('c1', 'sink'), (('s0', 't0'), '5c'): ('c1', 'c1'),
                (('s0', 't2'), '10c'): ('sink', 'sink'), (('sink', 'c4'), '10c'): ('sink', 'sink'),
                (('s0', 'c3'), '10c'): ('sink', 'sink'), (('s1', 't0'), '10c'): ('sink', 't1'),
                (('sink', 't3'), '10c'): ('sink', 'sink'), (('c1', 't0'), '5c'): ('sink', 'c1'),
                (('c4', 'c1'), 'gum'): ('sink', 'sink'), (('s0', 't2'), '5c'): ('c1', 'sink'),
                (('c2', 'c4'), '5c'): ('c3', 'sink'), (('s0', 't1'), 'gum'): ('s1', 't3'),
                (('c4', 'c2'), 'gum'): ('sink', 'c4'), (('c2', 'c1'), '10c'): ('sink', 'c2'),
                (('sink', 't1'), '5c'): ('sink', 't2'), (('sink', 'c1'), '5c'): ('sink', 'sink'),
                (('c1', 'sink'), 'gum'): ('sink', 'sink'), (('c2', 'c4'), '10c'): ('sink', 'sink'),
                (('c2', 'c2'), 'gum'): ('c4', 'c4'), (('s1', 'c4'), '5c'): ('sink', 'sink'),
                (('c1', 't2'), 'gum'): ('sink', 't0'), (('c1', 'c4'), '10c'): ('c2', 'sink'),
                (('c2', 'sink'), 'gum'): ('c4', 'sink'), (('s0', 'c4'), '5c'): ('c1', 'sink'),
                (('s0', 'c3'), 'gum'): ('s1', 'c1'), (('s1', 't0'), 'gum'): ('sink', 'sink'),
                (('c4', 'c3'), '5c'): ('sink', 'sink'), (('c3', 'c3'), '5c'): ('sink', 'sink'),
                (('c4', 'sink'), 'gum'): ('sink', 'sink'), (('s1', 't2'), '5c'): ('sink', 'sink'),
                (('c3', 't3'), '10c'): ('sink', 'sink'), (('c1', 'c4'), '5c'): ('sink', 'sink'),
                (('s0', 'sink'), '10c'): ('sink', 'sink'), (('s1', 'sink'), '5c'): ('sink', 'sink'),
                (('sink', 't0'), '10c'): ('sink', 't1'), (('c3', 'sink'), '5c'): ('sink', 'sink'),
                (('c3', 'c1'), '10c'): ('sink', 'c2'), (('c4', 't2'), '5c'): ('sink', 'sink'),
                (('c3', 'c3'), '10c'): ('sink', 'sink'), (('c1', 't1'), '10c'): ('c2', 'sink'),
                (('c3', 't3'), '5c'): ('sink', 'sink'), (('sink', 't2'), 'gum'): ('sink', 't0'),
                (('sink', 't0'), '5c'): ('sink', 'c1'), (('c2', 't2'), '10c'): ('sink', 'sink'),
                (('s1', 'c1'), 'gum'): ('sink', 'sink'), (('s1', 'c4'), 'gum'): ('sink', 'sink'),
                (('c2', 'sink'), '10c'): ('sink', 'sink'), (('s0', 'c4'), 'gum'): ('s1', 'sink'),
                (('c4', 'sink'), '10c'): ('sink', 'sink'), (('s0', 't1'), '10c'): ('sink', 'sink'),
                (('c4', 't0'), 'gum'): ('sink', 'sink'), (('c2', 'sink'), '5c'): ('c3', 'sink'),
                (('c2', 't1'), '5c'): ('c3', 't2'), (('sink', 'c1'), '10c'): ('sink', 'c2'),
                (('c1', 'c2'), '5c'): ('sink', 'c3'), (('c1', 't3'), '5c'): ('sink', 'sink'),
                (('sink', 'c3'), 'gum'): ('sink', 'c1'), (('c2', 'c4'), 'gum'): ('c4', 'sink'),
                (('c2', 'c3'), '5c'): ('c3', 'sink'), (('c2', 't1'), '10c'): ('sink', 'sink'),
                (('c1', 'c2'), '10c'): ('c2', 'sink'), (('sink', 't2'), '5c'): ('sink', 'sink'),
                (('c3', 'c4'), '10c'): ('sink', 'sink'), (('c3', 't1'), 'gum'): ('c1', 't3'),
                (('s1', 't3'), 'gum'): ('sink', 'sink'), (('s0', 't2'), 'gum'): ('s1', 't0'),
                (('sink', 'c4'), 'gum'): ('sink', 'sink'), (('s0', 't3'), '10c'): ('sink', 'sink'),
                (('c1', 'c3'), '5c'): ('sink', 'sink'), (('c2', 'c3'), '10c'): ('sink', 'sink'),
                (('sink', 't2'), '10c'): ('sink', 'sink'), (('c1', 'c3'), '10c'): ('c2', 'sink'),
                (('c4', 'c4'), 'gum'): ('sink', 'sink'), (('sink', 'sink'), '10c'): ('sink', 'sink'),
                (('c3', 'c3'), 'gum'): ('c1', 'c1'), (('c4', 'c4'), '5c'): ('sink', 'sink'),
                (('c3', 'c2'), '10c'): ('sink', 'sink'), (('c3', 'sink'), '10c'): ('sink', 'sink'),
                (('c1', 'c1'), '5c'): ('sink', 'sink'), (('c2', 't3'), '10c'): ('sink', 'sink'),
                (('s1', 'c2'), '5c'): ('sink', 'c3'), (('c4', 'c3'), 'gum'): ('sink', 'c1'),
                (('c3', 'c4'), 'gum'): ('c1', 'sink'), (('c4', 'c4'), '10c'): ('sink', 'sink'),
                (('c1', 't3'), 'gum'): ('sink', 'sink'), (('c1', 'c4'), 'gum'): ('sink', 'sink'),
                (('c3', 't1'), '5c'): ('sink', 't2'), (('s0', 't0'), '10c'): ('sink', 't1'),
                (('c4', 't1'), 'gum'): ('sink', 't3'), (('c2', 't3'), '5c'): ('c3', 'sink'),
                (('sink', 'c4'), '5c'): ('sink', 'sink'), (('c2', 'c3'), 'gum'): ('c4', 'c1'),
                (('c2', 'c2'), '10c'): ('sink', 'sink'), (('s1', 't1'), 'gum'): ('sink', 't3'),
                (('sink', 'c2'), '10c'): ('sink', 'sink'), (('c3', 't1'), '10c'): ('sink', 'sink'),
                (('s1', 't1'), '5c'): ('sink', 't2'), (('c2', 'c1'), '5c'): ('c3', 'sink'),
                (('c4', 't0'), '5c'): ('sink', 'c1'), (('s0', 'c1'), '10c'): ('sink', 'c2'),
                (('s1', 't1'), '10c'): ('sink', 'sink'), (('s1', 'c4'), '10c'): ('sink', 'sink'),
                (('s0', 't0'), 'gum'): ('s1', 'sink'), (('sink', 'c1'), 'gum'): ('sink', 'sink'),
                (('c1', 't0'), 'gum'): ('sink', 'sink'), (('s0', 'c4'), '10c'): ('sink', 'sink'),
                (('s0', 'c1'), '5c'): ('c1', 'sink'), (('c2', 't1'), 'gum'): ('c4', 't3'),
                (('c3', 't0'), '10c'): ('sink', 't1'), (('c4', 'c3'), '10c'): ('sink', 'sink'),
                (('sink', 'sink'), 'gum'): ('sink', 'sink'), (('sink', 't0'), 'gum'): ('sink', 'sink'),
                (('c3', 'c1'), 'gum'): ('c1', 'sink'), (('s0', 'sink'), '5c'): ('c1', 'sink'),
                (('s1', 't3'), '10c'): ('sink', 'sink'), (('c3', 'c1'), '5c'): ('sink', 'sink'),
                (('c1', 't1'), 'gum'): ('sink', 't3'), (('c1', 't2'), '5c'): ('sink', 'sink'),
                (('c3', 'sink'), 'gum'): ('c1', 'sink'), (('c1', 't1'), '5c'): ('sink', 't2'),
                (('c1', 'sink'), '5c'): ('sink', 'sink'), (('s0', 'c3'), '5c'): ('c1', 'sink'),
                (('c3', 'c2'), '5c'): ('sink', 'c3'), (('c3', 'c2'), 'gum'): ('c1', 'c4'),
                (('c1', 'c1'), 'gum'): ('sink', 'sink'), (('c3', 't2'), '10c'): ('sink', 'sink'),
                (('c1', 't0'), '10c'): ('c2', 't1'), (('s0', 't3'), 'gum'): ('s1', 'sink'),
                (('sink', 'c3'), '10c'): ('sink', 'sink'), (('c1', 'sink'), '10c'): ('c2', 'sink'),
                (('s0', 'c1'), 'gum'): ('s1', 'sink'), (('sink', 't1'), '10c'): ('sink', 'sink'),
                (('c4', 'sink'), '5c'): ('sink', 'sink'), (('s0', 'c2'), 'gum'): ('s1', 'c4'),
                (('c4', 'c2'), '10c'): ('sink', 'sink'), (('sink', 'c3'), '5c'): ('sink', 'sink'),
                (('c1', 'c3'), 'gum'): ('sink', 'c1'), (('c4', 't1'), '5c'): ('sink', 't2'),
                (('s1', 't2'), '10c'): ('sink', 'sink'), (('c4', 'c2'), '5c'): ('sink', 'c3'),
                (('c2', 'c1'), 'gum'): ('c4', 'sink'), (('c2', 't0'), 'gum'): ('c4', 'sink'),
                (('c1', 't2'), '10c'): ('c2', 'sink'), (('c4', 't1'), '10c'): ('sink', 'sink'),
                (('s0', 't3'), '5c'): ('c1', 'sink'), (('s1', 'sink'), '10c'): ('sink', 'sink'),
                (('sink', 'c2'), 'gum'): ('sink', 'c4'), (('c2', 't2'), 'gum'): ('c4', 't0'),
                (('c4', 't2'), '10c'): ('sink', 'sink'), (('s0', 't1'), '5c'): ('c1', 't2'),
                (('c2', 't2'), '5c'): ('c3', 'sink'), (('c1', 'c2'), 'gum'): ('sink', 'c4'),
                (('s1', 'c3'), '5c'): ('sink', 'sink')
            }
        }
        self.dfa_test_equals = {
            'alphabet': {'5c', '10c', 'gum'},
            'states': {
                ('s1', 's3'), ('s0', 'sink'), ('s0', 's3'), ('sink', 's0'), ('s0', 's1'), ('s2', 's0'), ('s2', 'sink'),
                ('s1', 'sink'), ('sink', 's1'), ('s2', 's3'), ('s0', 's0'), ('sink', 's3'), ('s3', 'sink'),
                ('s2', 's2'), ('s3', 's0'), ('s0', 's2'), ('s1', 's0'), ('sink', 's2'), ('s3', 's2'), ('s1', 's1'),
                ('s2', 's1'), ('s1', 's2'), ('s3', 's1'), ('s3', 's3'), ('sink', 'sink')
            },
            'initial_state': ('s0', 's0'),
            'accepting_states': {
                ('s0', 'sink'), ('s0', 's3'), ('sink', 's0'), ('s0', 's1'), ('s0', 's0'), ('s2', 's0'),
                ('s3', 's0'), ('s0', 's2'), ('s1', 's0')
            },
            'transitions': {
                (('s3', 'sink'), '5c'): ('sink', 'sink'), (('s3', 's1'), '5c'): ('sink', 's2'),
                (('s1', 's3'), '5c'): ('s2', 'sink'), (('s0', 's1'), '5c'): ('s1', 's2'),
                (('s3', 's3'), '5c'): ('sink', 'sink'), (('s0', 's1'), '10c'): ('s2', 's3'),
                (('s1', 's0'), 'gum'): ('sink', 'sink'), (('sink', 's0'), 'gum'): ('sink', 'sink'),
                (('s1', 's3'), 'gum'): ('sink', 's0'), (('s1', 'sink'), '10c'): ('s3', 'sink'),
                (('s3', 's2'), 'gum'): ('s0', 'sink'), (('sink', 's2'), '5c'): ('sink', 's3'),
                (('s3', 's0'), '10c'): ('sink', 's2'), (('s2', 's0'), 'gum'): ('sink', 'sink'),
                (('s3', 's2'), '10c'): ('sink', 's3'), (('s2', 's2'), '10c'): ('s3', 's3'),
                (('s2', 's1'), '10c'): ('s3', 's3'), (('s2', 'sink'), '10c'): ('s3', 'sink'),
                (('s0', 's2'), 'gum'): ('sink', 'sink'), (('sink', 's2'), 'gum'): ('sink', 'sink'),
                (('sink', 's3'), '5c'): ('sink', 'sink'), (('sink', 's3'), '10c'): ('sink', 'sink'),
                (('s0', 's3'), '10c'): ('s2', 'sink'), (('s1', 's1'), '10c'): ('s3', 's3'),
                (('s3', 's3'), '10c'): ('sink', 'sink'), (('s0', 's1'), 'gum'): ('sink', 'sink'),
                (('sink', 'sink'), 'gum'): ('sink', 'sink'), (('s1', 'sink'), 'gum'): ('sink', 'sink'),
                (('s2', 's2'), '5c'): ('s3', 's3'), (('s3', 's0'), 'gum'): ('s0', 'sink'),
                (('s2', 's3'), 'gum'): ('sink', 's0'), (('s3', 's0'), '5c'): ('sink', 's1'),
                (('s0', 'sink'), '5c'): ('s1', 'sink'), (('s0', 'sink'), '10c'): ('s2', 'sink'),
                (('s1', 'sink'), '5c'): ('s2', 'sink'), (('s3', 's1'), 'gum'): ('s0', 'sink'),
                (('s1', 's1'), '5c'): ('s2', 's2'), (('sink', 's1'), '10c'): ('sink', 's3'),
                (('s3', 'sink'), '10c'): ('sink', 'sink'), (('s1', 's2'), '10c'): ('s3', 's3'),
                (('s1', 's0'), '10c'): ('s3', 's2'), (('s0', 's0'), '10c'): ('s2', 's2'),
                (('s2', 's0'), '5c'): ('s3', 's1'), (('s2', 'sink'), '5c'): ('s3', 'sink'),
                (('s1', 's1'), 'gum'): ('sink', 'sink'), (('s0', 's3'), 'gum'): ('sink', 's0'),
                (('s2', 's1'), 'gum'): ('sink', 'sink'), (('sink', 's0'), '5c'): ('sink', 's1'),
                (('s0', 's3'), '5c'): ('s1', 'sink'), (('sink', 's2'), '10c'): ('sink', 's3'),
                (('s2', 'sink'), 'gum'): ('sink', 'sink'), (('s2', 's1'), '5c'): ('s3', 's2'),
                (('sink', 's3'), 'gum'): ('sink', 's0'), (('s1', 's0'), '5c'): ('s2', 's1'),
                (('s3', 's1'), '10c'): ('sink', 's3'), (('s0', 's2'), '5c'): ('s1', 's3'),
                (('s0', 's2'), '10c'): ('s2', 's3'), (('s1', 's3'), '10c'): ('s3', 'sink'),
                (('s2', 's0'), '10c'): ('s3', 's2'), (('sink', 's1'), 'gum'): ('sink', 'sink'),
                (('s2', 's2'), 'gum'): ('sink', 'sink'), (('s0', 's0'), '5c'): ('s1', 's1'),
                (('sink', 's0'), '10c'): ('sink', 's2'), (('s1', 's2'), '5c'): ('s2', 's3'),
                (('sink', 'sink'), '10c'): ('sink', 'sink'), (('s3', 's3'), 'gum'): ('s0', 's0'),
                (('s1', 's2'), 'gum'): ('sink', 'sink'), (('s0', 's0'), 'gum'): ('sink', 'sink'),
                (('s0', 'sink'), 'gum'): ('sink', 'sink'), (('sink', 's1'), '5c'): ('sink', 's2'),
                (('s3', 'sink'), 'gum'): ('s0', 'sink'), (('s2', 's3'), '5c'): ('s3', 'sink'),
                (('s2', 's3'), '10c'): ('s3', 'sink'), (('sink', 'sink'), '5c'): ('sink', 'sink'),
                (('s3', 's2'), '5c'): ('sink', 's3')
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

    def test_dfa_union_disjoint(self):
        """ Tests a correct union between disjointed DFAs"""
        # TODO ask: FORMALLY, should it returns a minimal dfa or this one with states not reached by initial state?
        self.assertDictEqual(DFA.dfa_union(self.dfa_union_1_test_01, self.dfa_union_2_test_01), self.dfa_test_disjoint)

    def test_dfa_union_intersecting(self):
        """ Tests a correct union between DFAs partially intersected"""
        # TODO ask: FORMALLY, should it returns a minimal dfa or this one with states not reached by initial state?
        self.assertDictEqual(DFA.dfa_union(self.dfa_union_1_test_02, self.dfa_union_2_test_02),
                             self.dfa_test_intersecting)

    def test_dfa_union_equals(self):
        """ Tests a correct union between the same DFA """
        # TODO ask: FORMALLY, should it returns a minimal dfa or this one with states not reached by initial state?
        self.assertDictEqual(DFA.dfa_union(self.dfa_union_1_test_01, self.dfa_union_1_test_01), self.dfa_test_equals)

    @unittest.expectedFailure
    def test_dfa_union_wrong_input_1(self):
        """ Tests an input different from a dict() object. [EXPECTED FAILURE] """
        DFA.dfa_union(1, self.dfa_union_2_test_01)

    @unittest.expectedFailure
    def test_dfa_union_wrong_input_2(self):
        """ Tests an input different from a dict() object. [EXPECTED FAILURE]"""
        DFA.dfa_union(self.dfa_union_1_test_01, 1)

    @unittest.expectedFailure
    def test_dfa_union_wrong_dict_1(self):
        """ Tests a dict() in input different from a well formatted dict() representing a DFA. [EXPECTED FAILURE]"""
        DFA.dfa_union({'goofy': 'donald'}, self.dfa_union_2_test_01)

    @unittest.expectedFailure
    def test_dfa_union_wrong_dict_2(self):
        """ Tests a dict() in input different from a well formatted dict() representing a DFA. [EXPECTED FAILURE]"""
        DFA.dfa_union(self.dfa_union_1_test_01, {'goofy': 'donald'})

    def test_dfa_union_side_effects(self):
        """ Tests that the union function doesn't make side effects on input DFAs"""
        dfa1_before = copy.deepcopy(self.dfa_test_side_effect_1)
        DFA.dfa_union(self.dfa_test_side_effect_1, self.dfa_test_side_effect_2)
        self.assertDictEqual(dfa1_before, self.dfa_test_side_effect_1)


class TestDfaMinimization(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_minimization_test_01 = automata_IO.dfa_dot_importer('./dot/dfa_minimization_test_01.dot')
        self.dfa_minimization_test_01_minimized = automata_IO.dfa_dot_importer('./dot/dfa_minimization_test_01.dot')
        self.dfa_minimization_test_02 = automata_IO.dfa_dot_importer('./dot/dfa_minimization_test_02.dot')
        self.dfa_minimization_test_02_minimized_s2 = automata_IO.dfa_dot_importer('./dot/dfa_minimization_test_01.dot')
        self.dfa_minimization_test_02_minimized_s4 = automata_IO.dfa_dot_importer(
            './dot/dfa_minimization_test_01_s4.dot')
        self.dfa_minimization_test_03 = automata_IO.dfa_dot_importer('./dot/dfa_minimization_test_03.dot')
        self.dfa_minimization_test_04 = automata_IO.dfa_dot_importer('./dot/dfa_minimization_test_04.dot')

    def test_dfa_minimization_already_minimized(self):
        """ Tests the minimization of a DFA already minimal"""
        self.assertDictEqual(DFA.dfa_minimization(self.dfa_minimization_test_01),
                             DFA.dfa_completion(self.dfa_minimization_test_01_minimized))

    def test_dfa_minimization(self):
        """ Tests correct DFA minimization """
        minimal = DFA.dfa_minimization(self.dfa_minimization_test_02)
        # the two solution are semantically equivalent as 's2' and 's4' are equivalent
        if 's4' in minimal['states']:
            self.assertDictEqual(minimal, DFA.dfa_completion(self.dfa_minimization_test_02_minimized_s4))
        else:
            self.assertDictEqual(minimal, DFA.dfa_completion(self.dfa_minimization_test_02_minimized_s2))

    def test_dfa_minimization_empty_states(self):
        """ Tests a minimization with a dfa without states"""
        minimal = DFA.dfa_minimization(copy.deepcopy(self.dfa_minimization_test_03))
        self.dfa_minimization_test_03['states'].add('sink')
        self.assertDictEqual(minimal, self.dfa_minimization_test_03)

    def test_dfa_minimization_empty_transitions(self):
        """ Tests a minimization with a dfa without transitions"""
        test = {
            'alphabet': set(),
            'states': {'s0'},
            'initial_state': 's0',
            'accepting_states': {'s0'},
            'transitions': dict()
        }
        minimal = DFA.dfa_minimization(copy.deepcopy(self.dfa_minimization_test_04))

        if 's1' in minimal['states']:
            test['states'].add('s1')
            self.assertEqual(minimal, test)
        elif 's2' in minimal['states']:
            test['states'].add('s2')
            self.assertEqual(minimal, test)
        elif 's3' in minimal['states']:
            test['states'].add('s3')
            self.assertEqual(minimal, test)

    @unittest.expectedFailure
    def test_dfa_minimization_wrong_input(self):
        """ Tests an input different from a dict() object. [EXPECTED FAILURE]"""
        DFA.dfa_minimization(1)

    @unittest.expectedFailure
    def test_dfa_minimization_wrong_dict(self):
        """ Tests a dict() in input different from a well formatted dict() representing a DFA. [EXPECTED FAILURE]"""
        DFA.dfa_minimization({'goofy': 'donald'})

    def test_dfa_minimization_side_effects(self):
        """ Tests the function doesn't make side effects on input """
        input_before = copy.deepcopy(self.dfa_minimization_test_02)
        DFA.dfa_minimization(self.dfa_minimization_test_02)
        self.assertDictEqual(input_before, self.dfa_minimization_test_02)


class TestDfaReachable(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_reachable_test_01 = automata_IO.dfa_dot_importer('./dot/dfa_reachable_test_01.dot')
        self.dfa_reachable_test_02 = automata_IO.dfa_dot_importer('./dot/dfa_reachable_test_02.dot')
        self.dfa_reachable_test_02_reachable = automata_IO.dfa_dot_importer('./dot/dfa_reachable_test_02_reachable.dot')
        self.dfa_reachable_test_03 = automata_IO.dfa_dot_importer('./dot/dfa_reachable_test_03.dot')
        self.dfa_reachable_test_04 = automata_IO.dfa_dot_importer('./dot/dfa_reachable_test_04.dot')
        self.dfa_reachable_test_05 = automata_IO.dfa_dot_importer('./dot/dfa_reachable_test_05.dot')
        self.dfa_reachable_test_intersected = automata_IO.dfa_dot_importer(
            './img/graphviz_dfa_intersection_intersecting.dot')

    def test_dfa_reachable_already_reachable(self):
        """ Tests making reachable a DFA even if its already completely reachable """
        test = copy.deepcopy(self.dfa_reachable_test_01)
        self.assertEqual(DFA.dfa_reachable(self.dfa_reachable_test_01), test)

    def test_dfa_reachable(self):
        """ Tests making correctly reachable a DFA """
        self.assertEqual(DFA.dfa_reachable(self.dfa_reachable_test_intersected),
                         self.dfa_reachable_test_02_reachable)

    def test_dfa_reachable_empty_states(self):
        """ Tests making reachable a DFA without states"""
        test = copy.deepcopy(self.dfa_reachable_test_03)
        test['states'].add(None)
        reach = DFA.dfa_reachable(self.dfa_reachable_test_03)
        self.assertEqual(reach, test)

    def test_dfa_reachable_empty_transitions(self):
        """ Tests making reachable a DFA without transitions"""
        test = {
            'alphabet': set(),
            'states': {'s0'},
            'initial_state': 's0',
            'accepting_states': {'s0'},
            'transitions': dict()
        }
        self.assertEqual(DFA.dfa_reachable(self.dfa_reachable_test_04), test)

    @unittest.expectedFailure
    def test_dfa_reachable_wrong_input(self):
        """ Tests an input different from a dict() object. [EXPECTED FAILURE]"""
        DFA.dfa_reachable(1)

    @unittest.expectedFailure
    def test_dfa_reachable_wrong_dict(self):
        """ Tests a dict() in input different from a well formatted dict() representing a DFA. [EXPECTED FAILURE]"""
        DFA.dfa_reachable({'goofy': 'donald'})

    def test_dfa_reachable_side_effects(self):
        """ Tests the function makes side effects on input """
        input_before = copy.deepcopy(self.dfa_reachable_test_intersected)
        DFA.dfa_reachable(self.dfa_reachable_test_intersected)
        self.assertNotEquals(input_before, self.dfa_reachable_test_intersected)

    def test_dfa_reachable_side_effects_copy(self):
        """ Tests the function doesn't make side effects if a copy is passed as input """
        input_before = copy.deepcopy(self.dfa_reachable_test_intersected)
        DFA.dfa_reachable(copy.deepcopy(self.dfa_reachable_test_intersected))
        self.assertEquals(input_before, self.dfa_reachable_test_intersected)

    def test_dfa_reachable_no_accepting_state_reachable(self):
        """ Tests making reachable a DFA where no accepting state is reached by the initial state"""
        self.assertEqual(DFA.dfa_reachable(self.dfa_reachable_test_05)['accepting_states'], set())


class TestDfaCoReachable(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_co_reachable_test_01 = automata_IO.dfa_dot_importer('./dot/dfa_co_reachable_test_01.dot')
        self.dfa_co_reachable_test_02 = automata_IO.dfa_dot_importer('./dot/dfa_co_reachable_test_02.dot')
        self.dfa_co_reachable_test_02_co_reachable = automata_IO.dfa_dot_importer(
            './dot/dfa_co_reachable_test_02_co_reachable.dot')
        self.dfa_co_reachable_test_03 = automata_IO.dfa_dot_importer('./dot/dfa_co_reachable_test_03.dot')
        self.dfa_co_reachable_test_04 = automata_IO.dfa_dot_importer('./dot/dfa_co_reachable_test_04.dot')
        self.dfa_co_reachable_test_05 = automata_IO.dfa_dot_importer('./dot/dfa_co_reachable_test_05.dot')
        self.dfa_co_reachable_test_06 = automata_IO.dfa_dot_importer('./dot/dfa_co_reachable_test_06.dot')

    def test_dfa_co_reachable_already_co_reachable(self):
        """ Tests making co_reachable a DFA even if its already completely co_reachable """
        test = copy.deepcopy(self.dfa_co_reachable_test_01)
        self.assertEqual(DFA.dfa_co_reachable(self.dfa_co_reachable_test_01), test)

    def test_dfa_co_reachable(self):
        """ Tests making correctly co_reachable a DFA """
        self.assertEqual(DFA.dfa_co_reachable(self.dfa_co_reachable_test_02),
                         self.dfa_co_reachable_test_02_co_reachable)

    def test_dfa_co_reachable_empty_states(self):
        """ Tests making co_reachable a DFA without states"""
        test = copy.deepcopy(self.dfa_co_reachable_test_03)
        co_reach = DFA.dfa_co_reachable(self.dfa_co_reachable_test_03)
        self.assertEqual(co_reach, test)

    def test_dfa_co_reachable_empty_transitions(self):
        """ Tests making co_reachable a DFA without transitions"""
        test = {
            'alphabet': set(),
            'states': {'s0'},
            'initial_state': 's0',
            'accepting_states': {'s0'},
            'transitions': dict()
        }
        self.assertEqual(DFA.dfa_co_reachable(self.dfa_co_reachable_test_04), test)

    @unittest.expectedFailure
    def test_dfa_co_reachable_wrong_input(self):
        """ Tests an input different from a dict() object. [EXPECTED FAILURE]"""
        DFA.dfa_co_reachable(1)

    @unittest.expectedFailure
    def test_dfa_co_reachable_wrong_dict(self):
        """ Tests a dict() in input different from a well formatted dict() representing a DFA. [EXPECTED FAILURE]"""
        DFA.dfa_co_reachable({'goofy': 'donald'})

    def test_dfa_co_reachable_side_effects(self):
        """ Tests the function makes side effects on input """
        input_before = copy.deepcopy(self.dfa_co_reachable_test_06)
        DFA.dfa_co_reachable(self.dfa_co_reachable_test_06)
        self.assertNotEquals(input_before, self.dfa_co_reachable_test_06)

    def test_dfa_co_reachable_side_effects_copy(self):
        """ Tests the function doesn't make side effects if a copy is passed as input """
        input_before = copy.deepcopy(self.dfa_co_reachable_test_06)
        DFA.dfa_co_reachable(copy.deepcopy(self.dfa_co_reachable_test_06))
        self.assertEquals(input_before, self.dfa_co_reachable_test_06)

    def test_dfa_co_reachable_no_accepting_state_co_reachable(self):
        """ Tests making co_reachable a DFA where the initial state doesn't reach any accepting state """
        test = {
            'alphabet': set(),
            'states': set(),
            'initial_state': None,
            'accepting_states': set(),
            'transitions': dict()
        }
        self.assertEqual(DFA.dfa_co_reachable(self.dfa_co_reachable_test_05), test)


class TestDfaTrimming(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_trimming_test_01 = automata_IO.dfa_dot_importer('./dot/dfa_trimming_test_01.dot')
        self.dfa_trimming_test_02 = automata_IO.dfa_dot_importer('./dot/dfa_trimming_test_02.dot')
        self.dfa_trimming_test_03 = automata_IO.dfa_dot_importer('./dot/dfa_trimming_test_03.dot')
        self.dfa_trimming_test_04 = automata_IO.dfa_dot_importer('./dot/dfa_trimming_test_04.dot')

    def test_dfa_trimming(self):
        """ Tests a correct trimming of a dfa"""
        automata_IO.graphviz_dfa_render(DFA.dfa_trimming(self.dfa_trimming_test_01), 'graphviz_dfa_trimming')

    def test_dfa_trimming_side_effects(self):
        """ Tests the function makes side effects on input """
        input_before = copy.deepcopy(self.dfa_trimming_test_01)
        DFA.dfa_trimming(self.dfa_trimming_test_01)
        self.assertNotEquals(input_before, self.dfa_trimming_test_01)

    def test_dfa_trimming_side_effects_copy(self):
        """ Tests the function doesn't make side effects if a copy is passed as input """
        input_before = copy.deepcopy(self.dfa_trimming_test_01)
        DFA.dfa_trimming(copy.deepcopy(self.dfa_trimming_test_01))
        self.assertEquals(input_before, self.dfa_trimming_test_01)

    def test_dfa_trimming_empty_states(self):
        """ Tests trimming a DFA without states"""
        test = copy.deepcopy(self.dfa_trimming_test_02)
        trimmed = DFA.dfa_trimming(self.dfa_trimming_test_02)
        self.assertEqual(trimmed, test)

    def test_dfa_trimming_empty_transitions(self):
        """ Tests trimming a DFA without transitions"""
        test = {
            'alphabet': set(),
            'states': {'s0'},
            'initial_state': 's0',
            'accepting_states': {'s0'},
            'transitions': dict()
        }
        self.assertEqual(DFA.dfa_trimming(self.dfa_trimming_test_03), test)

    def test_dfa_trimming_non_reachable_non_co_reachable(self):
        """ Tests trimming a DFA without transitions"""
        test = {
            'alphabet': set(),
            'states': set(),
            'initial_state': None,
            'accepting_states': set(),
            'transitions': dict()
        }
        self.assertEqual(DFA.dfa_trimming(self.dfa_trimming_test_04), test)


class TestDfaProjection(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_projection_test_01 = automata_IO.dfa_dot_importer('./dot/dfa_projection_1_test_01.dot')
        self.dfa_projection_test_01_solution = {
            'alphabet': {'10c', 'gum'},
            'states': {'s0', 's1', 's2', 's3'},
            'initial_states': {'s0', 's1', 's2', 's3'},
            'accepting_states': {'s0'},
            'transitions': {
                ('s0', '10c'): {'s2', 's3'},
                ('s0', 'gum'): {'s0', 's1', 's2', 's3'},
                ('s1', '10c'): {'s3'},
                ('s1', 'gum'): {'s0', 's1', 's2', 's3'},
                ('s2', '10c'): {'s3'},
                ('s2', 'gum'): {'s0', 's1', 's2', 's3'},
                ('s3', 'gum'): {'s0', 's1', 's2', 's3'}
            }
        }
        self.dfa_projection_test_02 = automata_IO.dfa_dot_importer('./dot/dfa_projection_1_test_02.dot')
        self.dfa_projection_test_02_solution = {
            'alphabet': set(),
            'states': {'s0', 's1', 's2', 's3'},
            'initial_states': {'s0', 's1', 's2', 's3'},
            'accepting_states': {'s0'},
            'transitions': dict()
        }

    def test_dfa_projection(self):
        """ Tests a correct dfa projection"""
        projection = DFA.dfa_projection(self.dfa_projection_test_01, {"5c"})
        self.assertDictEqual(projection, self.dfa_projection_test_01_solution)

    def test_dfa_projection_full_alphabet_projection(self):
        """ Tests a dfa projection where all the symbols of the alphabets got projected out """
        projection = DFA.dfa_projection(self.dfa_projection_test_02, {'5c', '10c', 'gum'})
        self.assertDictEqual(projection, self.dfa_projection_test_02_solution)
