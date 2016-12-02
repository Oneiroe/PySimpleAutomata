import DFA, NFA, AFW
import json
import graphviz
import pydot
import re


# ###
# TO-DO
# TODO correctness check of json & DOT imported automata
# TODO automata conformance check (eg. all transition uses word in alphabet,all transition involved states in States,..)
# TODO ignore node "None" if present
# TODO for NFAs use multiple "fake" node for each initial state


def __replace_all(repls, str):
    return re.sub('|'.join(re.escape(key) for key in repls.keys()), lambda k: repls[k.group(0)], str)


# Import a dfa from a json file
def dfa_json_importer(input_file):
    file = open(input_file)
    json_file = json.load(file)
    # TODO exception handling while JSON deconding/IO error
    alphabet = set(json_file['alphabet'])
    states = set(json_file['states'])
    initial_state = json_file['initial_state']
    accepting_states = set(json_file['accepting_states'])
    transitions = {}  # key [state ∈ states, action ∈ alphabet] value [arriving state ∈ states]
    for p in json_file['transitions']:
        transitions[p[0], p[1]] = p[2]

    # return list
    # return [alphabet, states, initial_state, accepting_states, transitions]

    # return map
    dfa = {}
    dfa['alphabet'] = alphabet
    dfa['states'] = states
    dfa['initial_state'] = initial_state
    dfa['accepting_states'] = accepting_states
    dfa['transitions'] = transitions
    return dfa


# Import a dfa from a DOT file
def dfa_dot_importer(input_file: str) -> dict:
    """ Import a dfa from a .dot file

    Of .dot files are recognized the following attributes

      • nodeX   shape=doublecircle -> accepting node
      • nodeX   root=true -> initial node
      • edgeX   label="a" -> action in alphabet
      • fake    [style=invisible] -> skip this node, fake invisible one to initial state arrow
      • fake -> S [style=bold] -> skip this transition, just initial state arrow for graphical purpose

    Forbidden names:
      • 'fake'  used for graphical purpose to drawn the arrow of the initial state
      • 'sink'  used as additional state when completing a DFA
      • 'None'  used when no initial state is present
    Forbidden characters:
        '"' "'" '(' ')' ' '

    :param input_file: path to the .dot file
    :return: dict representing a dfa
    """

    # pyDot Object
    g = pydot.graph_from_dot_file(input_file)[0]

    states = set()
    initial_state = None
    accepting_states = set()

    replacements = {'"': '', "'": '', '(': '', ')': '', ' ': ''}
    for node in g.get_nodes():
        if node.get_name() == 'fake' or node.get_name() == 'graph' or node.get_name() == 'node':
            continue
        # states.add(node.get_name())

        node_reference = __replace_all(replacements, node.get_name()).split(',')
        if len(node_reference) > 1:
            node_reference = tuple(node_reference)
        else:
            node_reference = node_reference[0]
        states.add(node_reference)
        for attribute in node.get_attributes():
            if attribute == 'root':
                # if initial_state!=0:
                #   TODO raise exception for wrong formatted dfa: dfa accepts only one initial state
                initial_state = node_reference
            if attribute == 'shape' and node.get_attributes()['shape'] == 'doublecircle':
                accepting_states.add(node_reference)

    alphabet = set()
    transitions = {}
    for edge in g.get_edges():
        if edge.get_source() == 'fake':
            continue
        label = __replace_all(replacements, edge.get_label())
        alphabet.add(label)
        source = __replace_all(replacements, edge.get_source()).split(',')
        if len(source) > 1:
            source = tuple(source)
        else:
            source = source[0]
        destination = __replace_all(replacements, edge.get_destination()).split(',')
        if len(destination) > 1:
            destination = tuple(destination)
        else:
            destination = destination[0]
        # if (edge.get_source(), edge.get_label().replace('"', '')) in transitions:
        #   TODO raise exception for wrong formatted dfa: dfa accepts only one transition from a state given a letter
        transitions[source, label] = destination

    # if len(initial_state) == 0:
    #   TODO raise exception for wrong formatted dfa: there must be an initial state

    # if len(accepting_states)==0:
    #     TODO raise exception for wrong formatted dfa: there must be at least an accepting state

    # return map
    dfa = {
        'alphabet': alphabet,
        'states': states,
        'initial_state': initial_state,
        'accepting_states': accepting_states,
        'transitions': transitions}
    return dfa


# Print in output a DOT file and an image of the given DFA
# pydot library
def dfa_pydot_render(dfa, name):
    """ Generates a .dot file and a relative .svg image in ./img/ folder of the input dfa using pydot library

    :param dfa: dict() representing a dfa
    :param name: str() string with the name of the output file
    """
    # TODO special view for sink node?
    g = pydot.Dot(graph_type='digraph')

    fake = pydot.Node('fake', style='invisible')
    g.add_node(fake)
    for state in dfa['states']:
        node = pydot.Node(str(state))
        if state == dfa['initial_state']:
            node.set_root(True)
            g.add_edge(pydot.Edge(fake, node, style='bold'))

        if state in dfa['accepting_states']:
            node.set_shape('doublecircle')
        g.add_node(node)

    for transition in dfa['transitions']:
        g.add_edge(pydot.Edge(str(transition[0]), str(dfa['transitions'][transition]), label=transition[1]))

    g.write_svg('img/' + name + '.svg')
    g.write_dot('img/' + name + '.dot')


# Print in output a DOT file and an image of the given DFA
# graphviz library
def dfa_graphviz_render(dfa, name):
    """ Generates a .dot file and a relative .svg image in ./img/ folder of the input dfa using graphviz library
    :param dfa: dict() representing a dfa
    :param name: str() string with the name of the output file
    """
    g = graphviz.Digraph(format='svg')
    g.node('fake', style='invisible')
    for state in dfa['states']:
        if state == dfa['initial_state']:
            if state in dfa['accepting_states']:
                g.node(str(state), root='true', shape='doublecircle')
            else:
                g.node(str(state), root='true')
        elif state in dfa['accepting_states']:
            g.node(str(state), shape='doublecircle')
        else:
            g.node(str(state))

    g.edge('fake', str(dfa['initial_state']), style='bold')
    for transition in dfa['transitions']:
        g.edge(str(transition[0]), str(dfa['transitions'][transition]), label=transition[1])

    g.render(filename='img/' + name + '.dot')


# Checks if the dfa is well formatted
# TODO dfa_conformance_check
def dfa_conformance_check(dfa):
    # check if there are just the right keys
    # checks all transition words are in alphabet and viceversa
    # checks all transition states are in states and viceversa
    # checks for forbidden symbols, words, names, etc
    return


# Export a dfa "object" to a json file
# TODO dfa_to_json
def dfa_to_json(dfa):
    return


# Export a dfa "object" to a DOT file
# TODO dfa_to_dot
def dfa_to_dot(dfa):
    return


# Import a nfa from a json file
def nfa_json_importer(input_file):
    file = open(input_file)
    json_file = json.load(file)
    # TODO exception handling while JSON deconding/IO error
    alphabet = set(json_file['alphabet'])
    states = set(json_file['states'])
    initial_states = set(json_file['initial_states'])
    accepting_states = set(json_file['accepting_states'])
    transitions = {}  # key [state in states, action in alphabet] value [et of arriving states in states]
    for p in json_file['transitions']:
        transitions.setdefault((p[0], p[1]), set()).add(p[2])

    # return list
    # return [alphabet, states, initial_states, accepting_states, transitions]

    # return map
    nfa = {}
    nfa['alphabet'] = alphabet
    nfa['states'] = states
    nfa['initial_states'] = initial_states
    nfa['accepting_states'] = accepting_states
    nfa['transitions'] = transitions
    return nfa


# Import a nfa from a dot file
def nfa_dot_importer(input_file):
    """ Returns a nfa dict() object from a .dot file representing a dfa

    Of .dot files are recognized the following attributes
      • nodeX   shape=doublecircle -> accepting node
      • nodeX   root=true -> initial node
      • edgeX   label="a" -> action in alphabet
      • fakeX   style=invisible -> skip this node, fake invisible one to initial state arrow
      • fakeX -> S [style=bold] -> skip this transition, just initial state arrow for graphical purpose

    All invisible nodes are skipped.

    Forbidden names:
      • 'fake'  used for graphical purpose to drawn the arrow of the initial state
      • 'sink'  used as additional state when completing a DFA
    Forbidden characters:
        '"' "'" '(' ')' ' '

    :param input_file: Path to input .dot file
    :return: dict() representing a NFA
    """

    # pyDot Object
    g = pydot.graph_from_dot_file(input_file)[0]

    states = set()
    initial_states = set()
    accepting_states = set()

    replacements = {'"': '', "'": '', '(': '', ')': '', ' ': ''}

    for node in g.get_nodes():
        if node.get_name() == 'fake' or node.get_name() == 'graph' or node.get_name() == 'node':
            continue
        if 'style' in node.get_attributes() and node.get_attributes()['style'] == 'invisible':
            continue

        node_reference = __replace_all(replacements, node.get_name()).split(',')
        if len(node_reference) > 1:
            node_reference = tuple(node_reference)
        else:
            node_reference = node_reference[0]
        states.add(node_reference)
        for attribute in node.get_attributes():
            if attribute == 'root':
                initial_states.add(node_reference)
            if attribute == 'shape' and node.get_attributes()['shape'] == 'doublecircle':
                accepting_states.add(node_reference)

    alphabet = set()
    transitions = {}
    for edge in g.get_edges():
        source = __replace_all(replacements, edge.get_source()).split(',')
        if len(source) > 1:
            source = tuple(source)
        else:
            source = source[0]
        destination = __replace_all(replacements, edge.get_destination()).split(',')
        if len(destination) > 1:
            destination = tuple(destination)
        else:
            destination = destination[0]

        if source not in states or destination not in states:
            continue

        label = __replace_all(replacements, edge.get_label())
        alphabet.add(label)

        transitions.setdefault((source, label), set()).add(destination)

    nfa = {
        'alphabet': alphabet,
        'states': states,
        'initial_states': initial_states,
        'accepting_states': accepting_states,
        'transitions': transitions
    }

    return nfa


def nfa_pydot_render(nfa, name):
    """ Generates a .dot file and a relative .svg image in ./img/ folder of the input nfa using pydot library

    :param nfa: dict() representing a nfa
    :param name: str() string with the name of the output file
    """
    g = pydot.Dot(graph_type='digraph')

    fakes = []
    for i in range(len(nfa['initial_states'])):
        fakes.append(pydot.Node('fake' + str(i), style='invisible'))
        g.add_node(fakes[i])

    for state in nfa['states']:
        node = pydot.Node(str(state))
        if state in nfa['initial_states']:
            node.set_root(True)
            g.add_edge(pydot.Edge(fakes.pop(), node, style='bold'))

        if state in nfa['accepting_states']:
            node.set_shape('doublecircle')
        g.add_node(node)

    for transition in nfa['transitions']:
        for destination in nfa['transitions'][transition]:
            g.add_edge(pydot.Edge(str(transition[0]), str(destination), label=transition[1]))

    g.write_svg('img/' + name + '.svg')
    g.write_dot('img/' + name + '.dot')


def nfa_graphviz_render(nfa, name):
    """ Generates a .dot file and a relative .svg image in ./img/ folder of the input nfa using graphviz library

    :param nfa: dict() representing a nfa
    :param name: str() string with the name of the output file
    """
    g = graphviz.Digraph(format='svg')

    fakes = []
    for i in range(len(nfa['initial_states'])):
        fakes.append('fake' + str(i))
        g.node('fake' + str(i), style='invisible')

    for state in nfa['states']:
        if state in nfa['initial_states']:
            if state in nfa['accepting_states']:
                g.node(str(state), root='true', shape='doublecircle')
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
            g.edge(str(transition[0]), str(destination), label=transition[1])

    g.render(filename='img/' + name + '.dot')


# Export a nfa "object" to a json file
# TODO nfa_to_json
def nfa_to_json(nfa):
    return


# Export a nfa "object" to a DOT file
# TODO dfa_to_dot
def nfa_to_dot(dfa):
    return


# Export a afw "object" to a json file
# TODO afw_to_json
def afw_to_json(afw):
    return


# Import a afw from a json file
def afw_json_importer(input_file):
    file = open(input_file)
    json_file = json.load(file)
    # TODO exception handling while JSON deconding/IO error
    alphabet = set(json_file['alphabet'])
    states = set(json_file['states'])
    initial_state = json_file['initial_state']
    accepting_states = set(json_file['accepting_states'])

    transitions = {}  # key [state in states, action in alphabet] value [string representing boolean expression]
    for p in json_file['transitions']:
        transitions[p[0], p[1]] = p[2]

    # return list
    # return [alphabet, states, initial_state, accepting_states, transitions]

    # return map
    afw = {}
    afw['alphabet'] = alphabet
    afw['states'] = states
    afw['initial_state'] = initial_state
    afw['accepting_states'] = accepting_states
    afw['transitions'] = transitions
    return afw
