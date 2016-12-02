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

    def test_dfa_dot_importer_from_intersection(self):
        """ Tests importing a dfa from a dot file derived from an intersection """
        dfa_02 = automata_IO.dfa_dot_importer('./img/graphviz_dfa_intersection_render_test.dot')
        self.assertDictEqual(dfa_02, self.dfa_test_02)


class TestDfaPydotRender(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_01 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_1_test_01.dot')
        self.dfa_02 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_2_test_01.dot')
        self.dfa_imported_intersect = automata_IO.dfa_dot_importer('./dot/automata_io_dfa_imported_intersection.dot')
        self.dfa_intersected = DFA.dfa_intersection(self.dfa_01, self.dfa_02)

    def test_dfa_pydot_render(self):
        """ Tests a simple dfa rendering thorough pydot library"""
        automata_IO.dfa_pydot_render(self.dfa_01, 'pydot_dfa_render_test')

    def test_dfa_pydot_intersection_render(self):
        automata_IO.dfa_pydot_render(self.dfa_intersected, 'pydot_dfa_intersection_render_test')


class TestDfaGraphvizRender(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dfa_01 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_1_test_01.dot')
        self.dfa_02 = automata_IO.dfa_dot_importer('./dot/dfa_intersection_2_test_01.dot')
        self.dfa_imported_intersect = automata_IO.dfa_dot_importer('./dot/automata_io_dfa_imported_intersection.dot')
        self.dfa_intersected = DFA.dfa_intersection(self.dfa_01, self.dfa_02)

    def test_dfa_graphviz_render(self):
        """ Tests a simple dfa render thorough graphiz library"""
        automata_IO.dfa_graphviz_render(self.dfa_01, 'graphviz_dfa_render_test')

    def test_dfa_graphviz_intersection_render(self):
        """ Tests a rendering of a dfa resulting from an intersection, so consisting in more complex nodes"""
        automata_IO.dfa_graphviz_render(self.dfa_intersected, 'graphviz_dfa_intersection_render_test')


class TestNfaDotImporter(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.nfa_test_01 = {
            'alphabet': {'10c', '5c', 'gum'},
            'states': {'s0', 's1', 's2', 's3'},
            'initial_states': {'s0', 's3'},
            'accepting_states': {'s0'},
            'transitions': {
                ('s0', '10c'): {'s2'},
                ('s0', '5c'): {'s1', 's2'},
                ('s1', '10c'): {'s3'},
                ('s1', '5c'): {'s2', 's3'},
                ('s2', '10c'): {'s3'},
                ('s2', '5c'): {'s3'},
                ('s3', 'gum'): {'s0'}
            }
        }
        self.nfa_test_02 = {
            'alphabet': {'5c', '10c', 'gum'},
            'states': {
                ('c3', 't1'),
                ('s0', 't0'),
                ('c3', 'c1'),
                ('c1', 'c1'),
                ('c2', 'c2'),
                ('c4', 't3'),
                ('c4', 'c3'),
                ('c2', 't1'),
                ('c4', 't2'),
                ('s0', 't3'),
                ('c1', 'c4'),
                ('c2', 'c3'),
                ('c4', 'c4'),
                ('c2', 'c4'),
                ('c1', 't1'),
                ('s1', 'c2'),
                ('c1', 'c2'),
                ('s1', 't1'),
                ('s1', 't2'),
                ('c3', 't3'),
                ('c4', 'c2'),
                ('c3', 't2'),
                ('c2', 't2'),
                ('c4', 't1'),
                ('s0', 't1'),
                ('s0', 'c3'),
                ('s0', 't2'),
                ('s1', 'c4'),
                ('c2', 't3'),
                ('c2', 't0'),
                ('c4', 't0'),
                ('s0', 'c2'),
                ('c3', 'c4'),
                ('c1', 't0'),
                ('s0', 'c4'),
                ('c1', 't3'),
                ('s0', 'c1'),
                ('c1', 'c3'),
                ('c3', 't0'),
                ('s1', 't0'),
                ('c3', 'c2'),
                ('c4', 'c1'),
                ('c2', 'c1'),
                ('c1', 't2'),
                ('s1', 'c3'),
                ('s1', 't3'),
                ('s1', 'c1'),
                ('c3', 'c3')
            },
            'initial_states': {('s0', 't0')},
            'accepting_states': {('s1', 'c4'), ('c4', 'c4'), ('c4', 't3'), ('s1', 't3')},
            'transitions': {
                (('c2', 'c2'), 'gum'): {('c4', 'c4')},
                (('c2', 't0'), '5c'): {('c3', 'c1')},
                (('s0', 't1'), 'gum'): {('s1', 't3')},
                (('c2', 'c2'), '5c'): {('c3', 'c3')},
                (('c3', 't2'), 'gum'): {('c1', 't0')},
                (('s0', 't1'), '5c'): {('c1', 't2')},
                (('c2', 't1'), 'gum'): {('c4', 't3')},
                (('c3', 't1'), 'gum'): {('c1', 't3')},
                (('s0', 'c2'), 'gum'): {('s1', 'c4')},
                (('c2', 't1'), '5c'): {('c3', 't2')},
                (('c1', 'c1'), '10c'): {('c2', 'c2')},
                (('s0', 't0'), '5c'): {('c1', 'c1')},
                (('c1', 't0'), '10c'): {('c2', 't1')},
                (('s0', 'c2'), '5c'): {('c1', 'c3')},
                (('s0', 't2'), 'gum'): {('s1', 't0')},
                (('c3', 'c3'), 'gum'): {('c1', 'c1')},
                (('c2', 'c3'), 'gum'): {('c4', 'c1')},
                (('c2', 't2'), 'gum'): {('c4', 't0')},
                (('c3', 'c2'), 'gum'): {('c1', 'c4')},
                (('s0', 'c3'), 'gum'): {('s1', 'c1')}
            }
        }

    def test_nfa_dot_importer(self):
        """ Tests importing a nfa from a simple .dot file """
        nfa_01 = automata_IO.nfa_dot_importer('./dot/automata_io_nfa_dot_importer_test_01.dot')
        self.assertDictEqual(nfa_01, self.nfa_test_01)

    def test_nfa_dot_importer_intersection(self):
        """ Tests importing a nfa from a dot file derived from an intersection """
        nfa_02 = automata_IO.nfa_dot_importer('./dot/automata_io_nfa_imported_intersection.dot')
        self.assertDictEqual(nfa_02, self.nfa_test_02)

    def test_nfa_dot_importer_from_simple_pydot_render(self):
        """ Tests if a dfa imported from dot file generated by nfa_pydot_render() is correct """
        nfa_01 = automata_IO.nfa_dot_importer('./img/pydot_nfa_simple.dot')
        self.assertDictEqual(nfa_01, self.nfa_test_01)


class TestNfaPydotRender(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.nfa_test_01 = {
            'alphabet': {'10c', '5c', 'gum'},
            'states': {'s0', 's1', 's2', 's3'},
            'initial_states': {'s0', 's3'},
            'accepting_states': {'s0'},
            'transitions': {
                ('s0', '10c'): {'s2'},
                ('s0', '5c'): {'s1', 's2'},
                ('s1', '10c'): {'s3'},
                ('s1', '5c'): {'s2', 's3'},
                ('s2', '10c'): {'s3'},
                ('s2', '5c'): {'s3'},
                ('s3', 'gum'): {'s0'}
            }
        }
        self.nfa_test_02 = {
            'alphabet': {'5c', '10c', 'gum'},
            'states': {
                ('c3', 't1'),
                ('s0', 't0'),
                ('c3', 'c1'),
                ('c1', 'c1'),
                ('c2', 'c2'),
                ('c4', 't3'),
                ('c4', 'c3'),
                ('c2', 't1'),
                ('c4', 't2'),
                ('s0', 't3'),
                ('c1', 'c4'),
                ('c2', 'c3'),
                ('c4', 'c4'),
                ('c2', 'c4'),
                ('c1', 't1'),
                ('s1', 'c2'),
                ('c1', 'c2'),
                ('s1', 't1'),
                ('s1', 't2'),
                ('c3', 't3'),
                ('c4', 'c2'),
                ('c3', 't2'),
                ('c2', 't2'),
                ('c4', 't1'),
                ('s0', 't1'),
                ('s0', 'c3'),
                ('s0', 't2'),
                ('s1', 'c4'),
                ('c2', 't3'),
                ('c2', 't0'),
                ('c4', 't0'),
                ('s0', 'c2'),
                ('c3', 'c4'),
                ('c1', 't0'),
                ('s0', 'c4'),
                ('c1', 't3'),
                ('s0', 'c1'),
                ('c1', 'c3'),
                ('c3', 't0'),
                ('s1', 't0'),
                ('c3', 'c2'),
                ('c4', 'c1'),
                ('c2', 'c1'),
                ('c1', 't2'),
                ('s1', 'c3'),
                ('s1', 't3'),
                ('s1', 'c1'),
                ('c3', 'c3')
            },
            'initial_states': {('s0', 't0'), ('c1', 't3')},
            'accepting_states': {('s1', 'c4'), ('c4', 'c4'), ('c4', 't3'), ('s1', 't3')},
            'transitions': {
                (('c2', 'c2'), 'gum'): {('c4', 'c4')},
                (('c2', 't0'), '5c'): {('c3', 'c1')},
                (('s0', 't1'), 'gum'): {('s1', 't3')},
                (('c2', 'c2'), '5c'): {('c3', 'c3')},
                (('c3', 't2'), 'gum'): {('c1', 't0')},
                (('s0', 't1'), '5c'): {('c1', 't2')},
                (('c2', 't1'), 'gum'): {('c4', 't3')},
                (('c3', 't1'), 'gum'): {('c1', 't3')},
                (('s0', 'c2'), 'gum'): {('s1', 'c4')},
                (('c2', 't1'), '5c'): {('c3', 't2')},
                (('c1', 'c1'), '10c'): {('c2', 'c2')},
                (('s0', 't0'), '5c'): {('c1', 'c1')},
                (('c1', 't0'), '10c'): {('c2', 't1')},
                (('s0', 'c2'), '5c'): {('c1', 'c3')},
                (('s0', 't2'), 'gum'): {('s1', 't0')},
                (('c3', 'c3'), 'gum'): {('c1', 'c1')},
                (('c2', 'c3'), 'gum'): {('c4', 'c1')},
                (('c2', 't2'), 'gum'): {('c4', 't0')},
                (('c3', 'c2'), 'gum'): {('c1', 'c4')},
                (('s0', 'c3'), 'gum'): {('s1', 'c1')}
            }
        }

    def test_nfa_pydot_render(self):
        """ Tests a simple nfa rendering thorough pydot library"""
        automata_IO.nfa_pydot_render(self.nfa_test_01, 'pydot_nfa_simple')

    def test_nfa_pydot_intersection_render(self):
        """ Tests rendering through pydot library a nfa derived from an intersection """
        automata_IO.nfa_pydot_render(self.nfa_test_02, 'pydot_nfa_intersection')


class TestNfaGraphvizRender(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.nfa_test_01 = {
            'alphabet': {'10c', '5c', 'gum'},
            'states': {'s0', 's1', 's2', 's3'},
            'initial_states': {'s0', 's3'},
            'accepting_states': {'s0'},
            'transitions': {
                ('s0', '10c'): {'s2'},
                ('s0', '5c'): {'s1', 's2'},
                ('s1', '10c'): {'s3'},
                ('s1', '5c'): {'s2', 's3'},
                ('s2', '10c'): {'s3'},
                ('s2', '5c'): {'s3'},
                ('s3', 'gum'): {'s0'}
            }
        }
        self.nfa_test_02 = {
            'alphabet': {'5c', '10c', 'gum'},
            'states': {
                ('c3', 't1'),
                ('s0', 't0'),
                ('c3', 'c1'),
                ('c1', 'c1'),
                ('c2', 'c2'),
                ('c4', 't3'),
                ('c4', 'c3'),
                ('c2', 't1'),
                ('c4', 't2'),
                ('s0', 't3'),
                ('c1', 'c4'),
                ('c2', 'c3'),
                ('c4', 'c4'),
                ('c2', 'c4'),
                ('c1', 't1'),
                ('s1', 'c2'),
                ('c1', 'c2'),
                ('s1', 't1'),
                ('s1', 't2'),
                ('c3', 't3'),
                ('c4', 'c2'),
                ('c3', 't2'),
                ('c2', 't2'),
                ('c4', 't1'),
                ('s0', 't1'),
                ('s0', 'c3'),
                ('s0', 't2'),
                ('s1', 'c4'),
                ('c2', 't3'),
                ('c2', 't0'),
                ('c4', 't0'),
                ('s0', 'c2'),
                ('c3', 'c4'),
                ('c1', 't0'),
                ('s0', 'c4'),
                ('c1', 't3'),
                ('s0', 'c1'),
                ('c1', 'c3'),
                ('c3', 't0'),
                ('s1', 't0'),
                ('c3', 'c2'),
                ('c4', 'c1'),
                ('c2', 'c1'),
                ('c1', 't2'),
                ('s1', 'c3'),
                ('s1', 't3'),
                ('s1', 'c1'),
                ('c3', 'c3')
            },
            'initial_states': {('s0', 't0'), ('c1', 't3')},
            'accepting_states': {('s1', 'c4'), ('c4', 'c4'), ('c4', 't3'), ('s1', 't3')},
            'transitions': {
                (('c2', 'c2'), 'gum'): {('c4', 'c4')},
                (('c2', 't0'), '5c'): {('c3', 'c1')},
                (('s0', 't1'), 'gum'): {('s1', 't3')},
                (('c2', 'c2'), '5c'): {('c3', 'c3')},
                (('c3', 't2'), 'gum'): {('c1', 't0')},
                (('s0', 't1'), '5c'): {('c1', 't2')},
                (('c2', 't1'), 'gum'): {('c4', 't3')},
                (('c3', 't1'), 'gum'): {('c1', 't3')},
                (('s0', 'c2'), 'gum'): {('s1', 'c4')},
                (('c2', 't1'), '5c'): {('c3', 't2')},
                (('c1', 'c1'), '10c'): {('c2', 'c2')},
                (('s0', 't0'), '5c'): {('c1', 'c1')},
                (('c1', 't0'), '10c'): {('c2', 't1')},
                (('s0', 'c2'), '5c'): {('c1', 'c3')},
                (('s0', 't2'), 'gum'): {('s1', 't0')},
                (('c3', 'c3'), 'gum'): {('c1', 'c1')},
                (('c2', 'c3'), 'gum'): {('c4', 'c1')},
                (('c2', 't2'), 'gum'): {('c4', 't0')},
                (('c3', 'c2'), 'gum'): {('c1', 'c4')},
                (('s0', 'c3'), 'gum'): {('s1', 'c1')}
            }
        }

    def test_nfa_graphviz_render(self):
        """ Tests a simple nfa rendering thorough graphviz library"""
        automata_IO.nfa_graphviz_render(self.nfa_test_01, 'graphviz_nfa_simple')

    def test_nfa_graphviz_intersection_render(self):
        """ Tests rendering through graphviz library a nfa derived from an intersection """
        automata_IO.nfa_graphviz_render(self.nfa_test_02, 'graphviz_nfa_intersection')
