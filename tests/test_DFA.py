from unittest import TestCase
import unittest
import DFA
import automata_IO

# Inputs
dfa = automata_IO.dfa_json_importer('../json/dfa_test.json')


class TestRunAcceptance(TestCase):
    def setUp(self):
        self.dfa = automata_IO.dfa_json_importer('../json/dfa_test.json')

    def tearDown(self):
        self.dfa = automata_IO.dfa_json_importer('../json/dfa_test.json')

    def test_run_acceptance(self):
        self.assertEqual(DFA.run_acceptance(self.dfa, ['s0', 's1', 's3', 's0'], ['5c', '10c', 'gum']), True)

    def test_run_acceptance_false(self):
        self.assertEqual(DFA.run_acceptance(self.dfa, ['s0', 's1', 's3'], ['5c', '10c']), False)

    @unittest.expectedFailure
    def test_run_acceptance_test_expected_failure(self):
        self.assertEqual(DFA.run_acceptance(self.dfa, ['s0', 's1', 's3'], ['5c', '10c']), True)


class TestWordAcceptance(TestCase):
    @unittest.skip("TestWordAcceptance TODO")
    def test_word_acceptance(self):
        self.assertEqual(DFA.word_acceptance(dfa, ['5c', '10c', 'gum', '5c', '10c', 'gum']), True)


class TestDfaCompletion(TestCase):
    @unittest.skip("TestDfaCompletion TODO")
    def test_dfa_completion(self):
        self.fail()


class TestDfaComplementation(TestCase):
    @unittest.skip("TestDfaComplementation TODO")
    def test_dfa_complementation(self):
        self.fail()


class TestDfaIntersection(TestCase):
    @unittest.skip("TestDfaIntersection TODO")
    def test_dfa_intersection(self):
        self.fail()


class TestDfaUnion(TestCase):
    @unittest.skip("TestDfaUnion TODO")
    def test_dfa_union(self):
        self.fail()


class TestDfaMinimization(TestCase):
    @unittest.skip("TestDfaMinimization TODO")
    def test_dfa_minimization(self):
        self.fail()


class TestDfaReachable(TestCase):
    @unittest.skip("TestDfaIntersection TODO")
    def test_dfa_reachable(self):
        self.fail()
