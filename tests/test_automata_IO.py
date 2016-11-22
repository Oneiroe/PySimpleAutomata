from unittest import TestCase
import unittest
import DFA
import NFA
import AFW
import automata_IO


class TestPydotDfaRender(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_01 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_1_test_01.dot')
        self.dfa_02 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_2_test_01.dot')
        self.dfa_imported_intersect = automata_IO.dfa_dot_importer('./dot/dfa_intersection_test_01_intersection.dot')
        self.dfa_intersected = DFA.dfa_intersection(self.dfa_01, self.dfa_02)

    def test_pydot_dfa_render(self):
        """ Tests a simple dfa rendering thorough pydot library"""
        automata_IO.pydot_dfa_render(self.dfa_01,'pydot_dfa_render_test')

    def test_pydot_dfa_intersection_render(self):
        automata_IO.pydot_dfa_render(self.dfa_intersected, 'pydot_dfa_intersection_render_test')


class TestGraphvizDfaRender(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_01 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_1_test_01.dot')
        self.dfa_02 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_2_test_01.dot')
        self.dfa_imported_intersect = automata_IO.dfa_dot_importer('./dot/dfa_intersection_test_01_intersection.dot')
        self.dfa_intersected = DFA.dfa_intersection(self.dfa_01, self.dfa_02)

    def test_graphviz_dfa_render(self):
        """ Tests a simple dfa render thorough graphiz library"""
        automata_IO.graphviz_dfa_render(self.dfa_01, 'graphviz_dfa_render_test')

    def test_graphviz_dfa_intersection_render(self):
        """ Tests a rendering of a dfa resulting from an intersection, so consisting in more complex nodes"""
        automata_IO.graphviz_dfa_render(self.dfa_intersected, 'graphviz_dfa_intersection_render_test')


class TestDfaJsonImporter(TestCase):
    @unittest.skip
    def test_dfa_json_importer(self):
        self.fail()


class TestDfaDotImporter(TestCase):
    @unittest.skip
    def test_dfa_dot_importer(self):
        self.fail()


class TestDfaToJson(TestCase):
    @unittest.skip
    def test_dfa_to_json(self):
        self.fail()


class TestDfaToDot(TestCase):
    @unittest.skip
    def test_dfa_to_dot(self):
        self.fail()
