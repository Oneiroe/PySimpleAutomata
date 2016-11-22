from unittest import TestCase
import unittest
import DFA
import automata_IO


class TestRunAcceptance(TestCase):
    def setUp(self):
        self.dfa_run_acceptance_test_01 = automata_IO.dfa_dot_importer('./dot/dfa_run_acceptance_test_01.dot')
        self.dfa_run_acceptance_test_02 = automata_IO.dfa_dot_importer('./dot/dfa_run_acceptance_test_02.dot')

    # def tearDown(self):
    #     self.dfa = automata_IO.dfa_json_importer('./dot/dfa_run_acceptance_test_01.dot')

    def test_run_acceptance(self):
        """ Tests a correct run """
        self.assertEqual(
            DFA.run_acceptance(self.dfa_run_acceptance_test_01, ['s0', 's1', 's3', 's0'], ['5c', '10c', 'gum']), True)

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

    def test_run_acceptance_empty(self):
        """ Tests an empty run """
        self.assertFalse(
            DFA.run_acceptance(self.dfa_run_acceptance_test_02, [], []))

    def test_run_acceptance_wrong_sizes(self):
        """ Tests run and word with wrong sizes """
        self.assertFalse(
            DFA.run_acceptance(self.dfa_run_acceptance_test_02, ['s0', 's1', 's3'], ['5c']))


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
        """ Tests an input different from a dict() object. [EXPECTED FAILURE]"""
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
        self.dfa = automata_IO.dfa_json_importer('../json/dfa_test.json')
        self.dfa_2 = automata_IO.dfa_json_importer('../json/dfa_f03_ai.json')
        self.dfa_3 = automata_IO.dfa_json_importer('../json/dfa_f03_ai.json')

    @unittest.skip("TestDfaIntersection TODO")
    def test_dfa_intersection(self):
        self.fail()


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
