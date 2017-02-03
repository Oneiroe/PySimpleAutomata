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
    def setUp(self):
        self.maxDiff = None
        self.nfa_union_1_test_01 = automata_IO.nfa_dot_importer('./dot/nfa/nfa_union_1_test_01.dot')
        self.nfa_union_2_test_01 = automata_IO.nfa_dot_importer('./dot/nfa/nfa_union_2_test_01.dot')
        self.nfa_union_3_test_01 = automata_IO.nfa_dot_importer('./dot/nfa/nfa_union_3_test_01.dot')
        self.nfa_union_test_01_solution = {
            'alphabet': {'a', 'b', 'c'},
            'states': {'s0', 's1', 's2', 's3', 's4', 't0', 't1', 't2', 't3', 't4'},
            'initial_states': {'s0', 't0'},
            'accepting_states': {'s2', 't0', 't4'},
            'transitions': {
                ('s3', 'b'): {'s4'}, ('s0', 'a'): {'s1'}, ('s4', 'a'): {'s4'},
                ('s2', 'b'): {'s0', 's2'}, ('s3', 'a'): {'s2'}, ('s1', 'b'): {'s2'},
                ('s4', 'b'): {'s0'}, ('s0', 'b'): {'s3'}, ('s1', 'a'): {'s4'},

                ('t3', 'c'): {'t0'}, ('t1', 'c'): {'t2', 't3'}, ('t4', 'c'): {'t0'},
                ('t0', 'a'): {'t2'}, ('t4', 'b'): {'t0'}, ('t0', 'b'): {'t1'},
                ('t3', 'a'): {'t1', 't4'}, ('t4', 'a'): {'t4'}, ('t2', 'a'): {'t4', 't2'},
                ('t3', 'b'): {'t0', 't3'}, ('t1', 'b'): {'t4'}, ('t2', 'b'): {'t1'}
            }
        }
        self.nfa_union_test_02_solution = {
            'alphabet': {'a', 'b', 'c'},
            'states': {'t0', 't1', 't2', 't3', 't4', 'c0', 'c4', 'c1', 'c2', 'c3'},
            'initial_states': {'t0', 'c0'},
            'accepting_states': {'t0', 't4', 'c4'},
            'transitions': {
                ('t0', 'a'): {'t2'},
                ('t0', 'b'): {'t1'},
                ('t1', 'b'): {'t4'},
                ('t1', 'c'): {'t2', 't3'},
                ('t2', 'a'): {'t4', 't2'},
                ('t2', 'b'): {'t1', 'c2'},
                ('t3', 'a'): {'t1', 't4'},
                ('t3', 'b'): {'t0', 't3'},
                ('t3', 'c'): {'t0', 'c4'},
                ('t4', 'a'): {'t4'},
                ('t4', 'b'): {'t0'},
                ('t4', 'c'): {'t0'},
                ('c0', 'a'): {'t1', 't2'},
                ('c0', 'b'): {'c1'},
                ('c1', 'c'): {'c3'},
                ('c2', 'c'): {'c3'},
                ('c3', 'a'): {'c4'},
                ('c3', 'b'): {'c4'}
            }
        }
        self.nfa_union_test_03_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_states': set(),
            'accepting_states': set(),
            'transitions': {}
        }

    def test_nfa_union_djsoint(self):
        """ Tests a nfa union between NFAs with no state in common """
        union = NFA.nfa_union(self.nfa_union_1_test_01, self.nfa_union_2_test_01)
        # automata_IO.nfa_graphviz_render(union, 'nfa_union')
        self.assertDictEqual(union, self.nfa_union_test_01_solution)

    def test_nfa_union_same(self):
        """ Tests a nfa union bewtween the same nfa """
        union = NFA.nfa_union(self.nfa_union_1_test_01, self.nfa_union_1_test_01)
        # automata_IO.nfa_graphviz_render(union, 'nfa_union_same')
        self.assertDictEqual(union, self.nfa_union_1_test_01)

    def test_nfa_union_intersecting(self):
        """ Tests a nfa union between NFAs with some state in common """
        union = NFA.nfa_union(self.nfa_union_2_test_01, self.nfa_union_3_test_01)
        # automata_IO.nfa_graphviz_render(union, 'nfa_union_intersecting')
        self.assertDictEqual(union, self.nfa_union_test_02_solution)

    def test_nfa_union_empty(self):
        """ Tests a nfa union where one of the input is an empty nfa """
        union = NFA.nfa_union(self.nfa_union_1_test_01, self.nfa_union_test_03_empty)
        self.assertDictEqual(union, self.nfa_union_1_test_01)

    @unittest.expectedFailure
    def test_nfa_union_wrong_input_1(self):
        """ Tests an input different from a dict() object. [EXPECTED FAILURE] """
        NFA.nfa_union(1, self.nfa_union_2_test_01)

    @unittest.expectedFailure
    def test_nfa_union_wrong_input_2(self):
        """ Tests an input different from a dict() object. [EXPECTED FAILURE] """
        NFA.nfa_union(self.nfa_union_2_test_01, 1)

    @unittest.expectedFailure
    def test_nfa_union_wrong_dict_1(self):
        """ Tests a dict() in input different from a well formatted dict() representing a NFA. [EXPECTED FAILURE]"""
        NFA.nfa_union({'goofy': 'donald'}, self.nfa_union_1_test_01)

    @unittest.expectedFailure
    def test_nfa_union_wrong_dict_2(self):
        """ Tests a dict() in input different from a well formatted dict() representing a NFA. [EXPECTED FAILURE]"""
        NFA.nfa_union(self.nfa_union_1_test_01, {'goofy': 'donald'})

    def test_dfa_union_side_effects(self):
        """ Tests that the union function doesn't make side effects on input NFAs """
        before_1 = copy.deepcopy(self.nfa_union_1_test_01)
        before_2 = copy.deepcopy(self.nfa_union_2_test_01)
        NFA.nfa_union(self.nfa_union_1_test_01, self.nfa_union_2_test_01)
        self.assertDictEqual(before_1, self.nfa_union_1_test_01)
        self.assertDictEqual(before_2, self.nfa_union_2_test_01)


class TestNfaDeterminization(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.nfa_determinization_test_01 = automata_IO.nfa_dot_importer('./dot/nfa/nfa_determinization_test_01.dot')
        self.nfa_determinization_test_02 = automata_IO.nfa_dot_importer('./dot/nfa/nfa_determinization_test_02.dot')
        self.nfa_determinization_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_states': set(),
            'accepting_states': set(),
            'transitions': {}
        }

    def test_nfa_determinization(self):
        """ Tests a correct nfa determinization """
        dfa_determined = NFA.nfa_determinization(self.nfa_determinization_test_01)
        # automata_IO.dfa_graphviz_render(dfa_determined, 'nfa_determined')
        self.assertEqual(len(dfa_determined['alphabet']), 2)
        self.assertEqual(len(dfa_determined['states']), 10)
        self.assertEqual(len(dfa_determined['accepting_states']), 6)
        self.assertEqual(len(dfa_determined['transitions']), 19)
        # due to set-to-string serialization undecidability of items order, it is not possible to match the result
        # of the operation to a predetermined result without enlist all the possible combination of S^2

    def test_nfa_determinization_bis(self):
        """ Tests an other correct nfa determinization """
        dfa_determined = NFA.nfa_determinization(self.nfa_determinization_test_02)
        # automata_IO.dfa_graphviz_render(dfa_determined, 'nfa_determined_2')
        self.assertEqual(len(dfa_determined['alphabet']), 3)
        self.assertEqual(len(dfa_determined['states']), 14)
        self.assertEqual(len(dfa_determined['accepting_states']), 11)
        self.assertEqual(len(dfa_determined['transitions']), 39)
        # due to set to string serialization undecidability of items order, it is not possible to match the result
        # of the operation to a predetermined result without enlist all the possible combination of S^2

    def test_nfa_determinization_empty_states(self):
        """ Tests a NFA determinization with an empty NFA """
        dfa_determined = NFA.nfa_determinization(self.nfa_determinization_test_empty)
        # automata_IO.dfa_graphviz_render(dfa_determined, 'nfa_determined_empty_States')
        self.assertDictEqual(dfa_determined, {'alphabet': set(),
                                              'states': set(),
                                              'initial_state': None,
                                              'accepting_states': set(),
                                              'transitions': {}
                                              }
                             )

    def test_nfa_determinization_empty_transitions(self):
        """ Tests a NFA determinization with a NFA without transitions """
        self.nfa_determinization_test_01['transitions'] = {}
        dfa_determined = NFA.nfa_determinization(self.nfa_determinization_test_01)
        # automata_IO.dfa_graphviz_render(dfa_determined, 'nfa_determined_empty_transition')
        self.assertDictEqual(dfa_determined, {'alphabet': self.nfa_determinization_test_01['alphabet'],
                                              'states': {str(self.nfa_determinization_test_01['initial_states'])},
                                              'initial_state': str(self.nfa_determinization_test_01['initial_states']),
                                              'accepting_states': set(),
                                              'transitions': {}
                                              }
                             )

    @unittest.expectedFailure
    def test_nfa_determinization_wrong_input(self):
        """ Tests the function using an input different from a dict object """
        NFA.nfa_determinization(0)

    @unittest.expectedFailure
    def test_nfa_determinization_wrong_dict(self):
        """ Tests the function using an input different from a well formatted dict representing a nfa """
        NFA.nfa_determinization({'goofy': 'donald'})

    def test_nfa_determinization_side_effects(self):
        """ Tests the function doesn't make any side effect on the input """
        before = copy.deepcopy(self.nfa_determinization_test_01)
        NFA.nfa_determinization(self.nfa_determinization_test_01)
        self.assertDictEqual(before, self.nfa_determinization_test_01)


class TestNfaComplementation(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.nfa_complementation_test_01 = automata_IO.nfa_dot_importer('./dot/nfa/nfa_complementation_test_01.dot')
        self.nfa_complementation_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_states': set(),
            'accepting_states': set(),
            'transitions': {}
        }

    def test_nfa_complementation(self):
        """ Tests a correct nfa complementation """
        dfa_complemented = NFA.nfa_complementation(self.nfa_complementation_test_01)
        self.assertEqual(len(dfa_complemented['alphabet']), 2)
        self.assertEqual(len(dfa_complemented['states']), 10 + 1)
        self.assertEqual(len(dfa_complemented['accepting_states']), 4 + 1)
        self.assertEqual(len(dfa_complemented['transitions']), 22)
        # due to set-to-string serialization undecidability of items order, it is not possible to match the result
        # of the operation to a predetermined result without enlist all the possible combination of S^2

    def test_nfa_complementation_empty_states(self):
        """ Tests a NFA complementation with an empty NFA """
        dfa_complemented = NFA.nfa_complementation(self.nfa_complementation_test_empty)
        automata_IO.dfa_graphviz_render(dfa_complemented, 'nfa_complemented_empty_States')
        self.assertDictEqual(dfa_complemented, {'alphabet': set(),
                                                'states': {'sink'},
                                                'initial_state': None,
                                                'accepting_states': {'sink'},
                                                'transitions': {}
                                                }
                             )

    def test_nfa_complementation_empty_transitions(self):
        """ Tests a NFA complementation with a NFA without transitions """
        self.nfa_complementation_test_01['transitions'] = {}
        dfa_complemented = NFA.nfa_complementation(self.nfa_complementation_test_01)
        automata_IO.dfa_graphviz_render(dfa_complemented, 'nfa_complemented_empty_transition')
        self.assertDictEqual(dfa_complemented, {'alphabet': self.nfa_complementation_test_01['alphabet'],
                                                'states': {str(self.nfa_complementation_test_01['initial_states']),
                                                           "sink"},
                                                'initial_state': str(
                                                    self.nfa_complementation_test_01['initial_states']),
                                                'accepting_states': {
                                                    str(self.nfa_complementation_test_01['initial_states']), "sink"},
                                                'transitions': {
                                                    ('sink', 'a'): 'sink',
                                                    ('sink', 'b'): 'sink',
                                                    (str(self.nfa_complementation_test_01['initial_states']),
                                                     'b'): 'sink',
                                                    (str(self.nfa_complementation_test_01['initial_states']),
                                                     'a'): 'sink'
                                                }
                                                }
                             )

    @unittest.expectedFailure
    def test_nfa_complementation_wrong_input(self):
        """ Tests the function using an input different from a dict object """
        NFA.nfa_complementation(0)

    @unittest.expectedFailure
    def test_nfa_complementation_wrong_dict(self):
        """ Tests the function using an input different from a well formatted dict representing a nfa """
        NFA.nfa_complementation({'goofy': 'donald'})

    def test_nfa_complementation_side_effects(self):
        """ Tests the function doesn't make any side effect on the input """
        before = copy.deepcopy(self.nfa_complementation_test_01)
        NFA.nfa_complementation(self.nfa_complementation_test_01)
        self.assertDictEqual(before, self.nfa_complementation_test_01)


class TestNfaNonemptinessCheck(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.nfa_nonemptiness_test_01 = automata_IO.nfa_dot_importer('./dot/nfa/nfa_nonemptiness_test_01.dot')
        self.nfa_nonemptiness_test_02 = automata_IO.nfa_dot_importer('./dot/nfa/nfa_nonemptiness_test_02.dot')
        self.nfa_nonemptiness_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_states': set(),
            'accepting_states': set(),
            'transitions': {}
        }

    def test_nfa_nonemptiness_check(self):
        """ Tests a correct nfa nonemptiness check"""
        self.assertTrue(NFA.nfa_nonemptiness_check(self.nfa_nonemptiness_test_01))

    def test_nfa_nonemptiness_check_false(self):
        """ Tests a correct nfa nonemptiness check, where the nfa is empty"""
        self.assertFalse(NFA.nfa_nonemptiness_check(self.nfa_nonemptiness_test_02))

    def test_nfa_nonemptiness_check_empty(self):
        """ Tests the nonemptiness of an empty nfa"""
        self.assertFalse(NFA.nfa_nonemptiness_check(self.nfa_nonemptiness_test_empty))

    @unittest.expectedFailure
    def test_nfa_nonemptiness_check_wrong_dict(self):
        """ Tests the nonemptiness of an input dict different from a dict representing a nfa """
        self.assertFalse(NFA.nfa_nonemptiness_check({}))

    @unittest.expectedFailure
    def test_nfa_nonemptiness_check_wrong_input(self):
        """ Tests the nonemptines of an input different from a dict object """
        self.assertFalse(NFA.nfa_nonemptiness_check(0))

    def test_nfa_nonemptiness_check_side_effects(self):
        """ Tests that the function doesn't make any side effect on the input"""
        before = copy.deepcopy(self.nfa_nonemptiness_test_01)
        NFA.nfa_nonemptiness_check(self.nfa_nonemptiness_test_01)
        self.assertDictEqual(before, self.nfa_nonemptiness_test_01)


class TestNfaNonuniversalityCheck(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.nfa_nonuniversality_test_01 = automata_IO.nfa_dot_importer('./dot/nfa/nfa_nonuniversality_test_01.dot')
        self.nfa_nonuniversality_test_02 = automata_IO.nfa_dot_importer('./dot/nfa/nfa_nonuniversality_test_02.dot')
        self.nfa_nonuniversality_test_empty = {
            'alphabet': set(),
            'states': set(),
            'initial_states': set(),
            'accepting_states': set(),
            'transitions': {}
        }

    def test_nfa_nonuniversality_check(self):
        """ Tests a correct nfa nonuniversality check"""
        self.assertTrue(NFA.nfa_nonuniversality_check(self.nfa_nonuniversality_test_01))

    def test_nfa_nonuniversality_check_false(self):
        """ Tests a correct nfa nonuniversality check, where the nfa is universal"""
        self.assertFalse(NFA.nfa_nonuniversality_check(self.nfa_nonuniversality_test_02))

    def test_nfa_nonuniversality_check_empty(self):
        """ Tests the nonuniversality of an empty nfa"""
        self.assertFalse(NFA.nfa_nonuniversality_check(self.nfa_nonuniversality_test_empty))

    @unittest.expectedFailure
    def test_nfa_nonuniversality_check_wrong_dict(self):
        """ Tests the nonuniversality of an input dict different from a dict representing a nfa """
        self.assertFalse(NFA.nfa_nonuniversality_check({}))

    @unittest.expectedFailure
    def test_nfa_nonuniversality_check_wrong_input(self):
        """ Tests the nonemptines of an input different from a dict object """
        self.assertFalse(NFA.nfa_nonuniversality_check(0))

    def test_nfa_nonuniversality_check_side_effects(self):
        """ Tests that the function doesn't make any side effect on the input"""
        before = copy.deepcopy(self.nfa_nonuniversality_test_01)
        NFA.nfa_nonuniversality_check(self.nfa_nonuniversality_test_01)
        self.assertDictEqual(before, self.nfa_nonuniversality_test_01)


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
