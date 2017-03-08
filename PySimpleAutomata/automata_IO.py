"""
Module to mange IO
"""

import json
import graphviz
import pydot
import re
import os


def __replace_all(repls: dict, input: str) -> str:
    """ Replaces from a string **input** all the occurrences of some
    symbols according to mapping **repls**.

    :param dict repls: where #key is the old character and
    #value is the one to substitute with;
    :param str input: original string where to apply the
    replacements;
    :return: *(str)* the string with the desired characters replaced
    """
    return re.sub('|'.join(re.escape(key) for key in repls.keys()),
                  lambda k: repls[k.group(0)], input)


####################################################################
# DFA ##############################################################

def dfa_json_importer(input_file: str) -> dict:
    """ Imports a DFA from a JSON file.

    :param str input_file: path + filename to json file;
    :return: *(dict)* representing a DFA.
    """
    file = open(input_file)
    json_file = json.load(file)

    transitions = {}  # key [state ∈ states, action ∈ alphabet]
    #                   value [arriving state ∈ states]
    for (origin, action, destination) in json_file['transitions']:
        transitions[origin, action] = destination

    dfa = {
        'alphabet': set(json_file['alphabet']),
        'states': set(json_file['states']),
        'initial_state': json_file['initial_state'],
        'accepting_states': set(json_file['accepting_states']),
        'transitions': transitions
    }
    return dfa


def dfa_to_json(dfa: dict, name: str, path: str = './'):
    """ Exports a DFA to a JSON file.

    If *path* do not exists, it will be created.

    :param dict dfa: DFA to export;
    :param str name: name of the output file;
    :param str path: path where to save the JSON file (default:
                     working directory)
    """
    out = {
        'alphabet': list(dfa['alphabet']),
        'states': list(dfa['states']),
        'initial_state': dfa['initial_state'],
        'accepting_states': list(dfa['accepting_states']),
        'transitions': list()
    }

    for t in dfa['transitions']:
        out['transitions'].append(
            [t[0], t[1], dfa['transitions'][t]])

    if not os.path.exists(path):
        os.makedirs(path)
    file = open(os.path.join(path, name + '.json'), 'w')
    json.dump(out, file, sort_keys=True, indent=4)
    file.close()


def dfa_dot_importer(input_file: str) -> dict:
    """ Imports a DFA from a DOT file.

    Of DOT files are recognized the following attributes:

      • nodeX   shape=doublecircle -> accepting node;
      • nodeX   root=true -> initial node;
      • edgeX   label="a" -> action in alphabet;
      • fake    [style=invisible] -> dummy invisible node pointing
                to initial state (they will be skipped);
      • fake-> S [style=bold] -> dummy transition to draw the arrow
                pointing to initial state (it will be skipped).

    Forbidden names:

      • 'fake'  used for graphical purpose to drawn the arrow of
        the initial state;
      • 'sink'  used as additional state when completing a DFA;
      • 'None'  used when no initial state is present.

    Forbidden characters:
      • "
      • '
      • (
      • )
      • spaces

    :param str input_file: path to the DOT file;
    :return: *(dict)* representing a DFA.
    """

    # pyDot Object
    g = pydot.graph_from_dot_file(input_file)[0]

    states = set()
    initial_state = None
    accepting_states = set()

    replacements = {'"': '', "'": '', '(': '', ')': '', ' ': ''}
    for node in g.get_nodes():
        if node.get_name() == 'fake' \
                or node.get_name() == 'None' \
                or node.get_name() == 'graph' \
                or node.get_name() == 'node':
            continue
        if 'style' in node.get_attributes() \
                and node.get_attributes()['style'] == 'invisible':
            continue
        node_reference = __replace_all(replacements,
                                       node.get_name()).split(',')
        if len(node_reference) > 1:
            node_reference = tuple(node_reference)
        else:
            node_reference = node_reference[0]
        states.add(node_reference)
        for attribute in node.get_attributes():
            if attribute == 'root':
                initial_state = node_reference
            if attribute == 'shape' and node.get_attributes()[
                'shape'] == 'doublecircle':
                accepting_states.add(node_reference)

    alphabet = set()
    transitions = {}
    for edge in g.get_edges():
        if edge.get_source() == 'fake':
            continue
        label = __replace_all(replacements, edge.get_label())
        alphabet.add(label)
        source = __replace_all(replacements,
                               edge.get_source()).split(',')
        if len(source) > 1:
            source = tuple(source)
        else:
            source = source[0]
        destination = __replace_all(replacements,
                                    edge.get_destination()).split(',')
        if len(destination) > 1:
            destination = tuple(destination)
        else:
            destination = destination[0]
        transitions[source, label] = destination

    dfa = {
        'alphabet': alphabet,
        'states': states,
        'initial_state': initial_state,
        'accepting_states': accepting_states,
        'transitions': transitions}
    return dfa


def dfa_to_dot(dfa: dict, name: str, path: str = './'):
    """ Generates a DOT file and a relative SVG image in **path**
    folder of the input DFA using graphviz library.

    :param dict dfa: DFA to export;
    :param str name: name of the output file;
    :param str path: path where to save the DOT/SVG files (default:
                     working directory)
    """
    g = graphviz.Digraph(format='svg')
    g.node('fake', style='invisible')
    for state in dfa['states']:
        if state == dfa['initial_state']:
            if state in dfa['accepting_states']:
                g.node(str(state), root='true',
                       shape='doublecircle')
            else:
                g.node(str(state), root='true')
        elif state in dfa['accepting_states']:
            g.node(str(state), shape='doublecircle')
        else:
            g.node(str(state))

    g.edge('fake', str(dfa['initial_state']), style='bold')
    for transition in dfa['transitions']:
        g.edge(str(transition[0]),
               str(dfa['transitions'][transition]),
               label=transition[1])

    if not os.path.exists(path):
        os.makedirs(path)

    g.render(filename=os.path.join(path, name + '.dot'))


@NotImplementedError
def dfa_conformance_check(dfa):
    """ Checks if the dfa is conformant to the specifications.

    :param dict dfa:
    :return: *(Bool)*
    """
    # check if there are just the right keys
    # checks all transition words are in alphabet and viceversa
    # checks all transition states are in states and viceversa
    # checks for forbidden symbols, words, names, etc
    # check iff one and only one initial state
    return


####################################################################
# NFA ##############################################################

def nfa_json_importer(input_file: str) -> dict:
    """ Imports a NFA from a JSON file.

    :param str input_file: path+filename to JSON file;
    :return: *(dict)* representing a NFA.
    """
    file = open(input_file)
    json_file = json.load(file)

    transitions = {}  # key [state in states, action in alphabet]
    #                   value [Set of arriving states in states]
    for p in json_file['transitions']:
        transitions.setdefault((p[0], p[1]), set()).add(p[2])

    nfa = {
        'alphabet': set(json_file['alphabet']),
        'states': set(json_file['states']),
        'initial_states': set(json_file['initial_states']),
        'accepting_states': set(json_file['accepting_states']),
        'transitions': transitions
    }

    return nfa


def nfa_to_json(nfa: dict, name: str, path: str = './'):
    """ Exports a NFA to a JSON file.

    :param dict nfa: NFA to export;
    :param str name: name of the output file;
    :param str path: path where to save the JSON file (default:
                     working directory).
    """
    transitions = list()  # key[state in states, action in alphabet]
    #                       value [Set of arriving states in states]
    for p in nfa['transitions']:
        for dest in nfa['transitions'][p]:
            transitions.append([p[0], p[1], dest])

    out = {
        'alphabet': list(nfa['alphabet']),
        'states': list(nfa['states']),
        'initial_states': list(nfa['initial_states']),
        'accepting_states': list(nfa['accepting_states']),
        'transitions': transitions
    }

    if not os.path.exists(path):
        os.makedirs(path)
    file = open(os.path.join(path, name + '.json'), 'w')
    json.dump(out, file, sort_keys=True, indent=4)
    file.close()


def nfa_dot_importer(input_file: str) -> dict:
    """ Imports a NFA from a DOT file.

    Of .dot files are recognized the following attributes
      • nodeX   shape=doublecircle -> accepting node;
      • nodeX   root=true -> initial node;
      • edgeX   label="a" -> action in alphabet;
      • fakeX    style=invisible -> dummy invisible nodes pointing
                to initial state (it will be skipped);
      • fakeX->S [style=bold] -> dummy transitions to draw arrows
                pointing to initial states (they will be skipped).

    All invisible nodes are skipped.

    Forbidden names:
      • 'fake'  used for graphical purpose to drawn the arrow of
        the initial state
      • 'sink'  used as additional state when completing a NFA

    Forbidden characters:
      • "
      • '
      • (
      • )
      • spaces

    :param str input_file: Path to input DOT file;
    :return: *(dict)* representing a NFA.
    """

    # pyDot Object
    g = pydot.graph_from_dot_file(input_file)[0]

    states = set()
    initial_states = set()
    accepting_states = set()

    replacements = {'"': '', "'": '', '(': '', ')': '', ' ': ''}

    for node in g.get_nodes():
        attributes = node.get_attributes()
        if node.get_name() == 'fake' \
                or node.get_name() == 'None' \
                or node.get_name() == 'graph' \
                or node.get_name() == 'node':
            continue
        if 'style' in attributes \
                and attributes['style'] == 'invisible':
            continue

        node_reference = __replace_all(replacements,
                                       node.get_name()).split(',')
        if len(node_reference) > 1:
            node_reference = tuple(node_reference)
        else:
            node_reference = node_reference[0]
        states.add(node_reference)
        for attribute in attributes:
            if attribute == 'root':
                initial_states.add(node_reference)
            if attribute == 'shape' \
                    and attributes['shape'] == 'doublecircle':
                accepting_states.add(node_reference)

    alphabet = set()
    transitions = {}
    for edge in g.get_edges():
        source = __replace_all(replacements,
                               edge.get_source()).split(',')
        if len(source) > 1:
            source = tuple(source)
        else:
            source = source[0]
        destination = __replace_all(replacements,
                                    edge.get_destination()).split(',')
        if len(destination) > 1:
            destination = tuple(destination)
        else:
            destination = destination[0]

        if source not in states or destination not in states:
            continue

        label = __replace_all(replacements, edge.get_label())
        alphabet.add(label)

        transitions.setdefault((source, label), set()).add(
            destination)

    nfa = {
        'alphabet': alphabet,
        'states': states,
        'initial_states': initial_states,
        'accepting_states': accepting_states,
        'transitions': transitions
    }

    return nfa


def nfa_to_dot(nfa: dict, name: str, path: str = './'):
    """ Generates a DOT file and a relative SVG image in **path**
    folder of the input NFA using graphviz library.

    :param dict nfa: input NFA;
    :param str name: string with the name of the output file;
    :param str path: path where to save the DOT/SVG files (default:
                     working directory).
    """
    g = graphviz.Digraph(format='svg')

    fakes = []
    for i in range(len(nfa['initial_states'])):
        fakes.append('fake' + str(i))
        g.node('fake' + str(i), style='invisible')

    for state in nfa['states']:
        if state in nfa['initial_states']:
            if state in nfa['accepting_states']:
                g.node(str(state), root='true',
                       shape='doublecircle')
            else:
                g.node(str(state), root='true')
        elif state in nfa['accepting_states']:
            g.node(str(state), shape='doublecircle')
        else:
            g.node(str(state))

    for initial_state in nfa['initial_states']:
        g.edge(fakes.pop(), str(initial_state), style='bold')
    for transition in nfa['transitions']:
        for destination in nfa['transitions'][transition]:
            g.edge(str(transition[0]), str(destination),
                   label=transition[1])

    g.render(filename=os.path.join(path, name + '.dot'))


####################################################################
# AFW ##############################################################

def afw_json_importer(input_file: str) -> dict:
    """ Imports a AFW from a JSON file.

    :param str input_file: path+filename to input JSON file;
    :return: *(dict)* representing a AFW.
    """
    file = open(input_file)
    json_file = json.load(file)

    transitions = {}  # key [state in states, action in alphabet]
    #  value [string representing boolean expression]
    for p in json_file['transitions']:
        transitions[p[0], p[1]] = p[2]

    # return map
    afw = {
        'alphabet': set(json_file['alphabet']),
        'states': set(json_file['states']),
        'initial_state': json_file['initial_state'],
        'accepting_states': set(json_file['accepting_states']),
        'transitions': transitions
    }
    return afw


def afw_to_json(afw: dict, name: str, path: str = './'):
    """ Exports a AFW to a JSON file.

    :param dict afw: input AFW;
    :param str name: output file name;
    :param str path: path where to save the JSON file (default:
                     working directory).
    """

    out = {
        'alphabet': list(afw['alphabet']),
        'states': list(afw['states']),
        'initial_state': afw['initial_state'],
        'accepting_states': list(afw['accepting_states']),
        'transitions': list()
    }

    for t in afw['transitions']:
        out['transitions'].append(
            [t[0], t[1], afw['transitions'][t]])

    if not os.path.exists(path):
        os.makedirs(path)
    file = open(os.path.join(path, name + '.json'), 'w')
    json.dump(out, file, sort_keys=True, indent=4)
    file.close()
