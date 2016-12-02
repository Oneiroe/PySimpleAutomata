from unittest import TestCase
import unittest
import DFA
import NFA
import AFW
import automata_IO


class TestDfaDotImporter(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_test = {
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
        self.dfa_test_02 = {
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

    def test_dfa_dot_importer(self):
        """ Tests importing a dfa from a simple dot file"""
        dfa_01 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_1_test_01.dot')
        self.assertDictEqual(dfa_01, self.dfa_test)

    def test_intersection_dfa_dot_importer(self):
        """ Tests importing a dfa from a dot file derived from an intersection """
        dfa_02 = automata_IO.dfa_dot_importer('./img/graphviz_dfa_intersection_render_test.dot')
        self.assertDictEqual(dfa_02, self.dfa_test_02)


class TestPydotDfaRender(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_01 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_1_test_01.dot')
        self.dfa_02 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_2_test_01.dot')
        self.dfa_imported_intersect = automata_IO.dfa_dot_importer('./dot/automata_io_dfa_imported_intersection.dot')
        self.dfa_intersected = DFA.dfa_intersection(self.dfa_01, self.dfa_02)

    def test_pydot_dfa_render(self):
        """ Tests a simple dfa rendering thorough pydot library"""
        automata_IO.pydot_dfa_render(self.dfa_01, 'pydot_dfa_render_test')

    def test_pydot_dfa_intersection_render(self):
        automata_IO.pydot_dfa_render(self.dfa_intersected, 'pydot_dfa_intersection_render_test')


class TestGraphvizDfaRender(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_01 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_1_test_01.dot')
        self.dfa_02 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_2_test_01.dot')
        self.dfa_imported_intersect = automata_IO.dfa_dot_importer('./dot/automata_io_dfa_imported_intersection.dot')
        self.dfa_intersected = DFA.dfa_intersection(self.dfa_01, self.dfa_02)

    def test_graphviz_dfa_render(self):
        """ Tests a simple dfa render thorough graphiz library"""
        automata_IO.graphviz_dfa_render(self.dfa_01, 'graphviz_dfa_render_test')

    def test_graphviz_dfa_intersection_render(self):
        """ Tests a rendering of a dfa resulting from an intersection, so consisting in more complex nodes"""
        automata_IO.graphviz_dfa_render(self.dfa_intersected, 'graphviz_dfa_intersection_render_test')
