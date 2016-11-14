import json
from itertools import product as cartesian_product
from copy import deepcopy
import graphviz
import pydot


# ###
# MEMO
# handle side-effects through input instead of manual handling in function:
#    pass as value of function a copy, not the data link


# ###
# TO-DO
# TODO check correctness of imported automata from json & DOT
# TODO check copy and deepCopy side-effects on structures like set of set or set in maps, ....
#         DECISAMENTE copy makes side effect, look dfa_projection() and try to substitute deepcopy with copy
# TODO move graph render in a separate file to take dfa function independent from it
# TODO lambda functions

# A dfa, deterministic finite automaton, A is a tuple A = (Σ, S, s_0 , ρ, F ), where
# • Σ is a finite nonempty alphabet;
# • S is a finite nonempty set of states;
# • s_0 ∈ S is the initial state;
# • F ⊆ S is the set of accepting states;
# • ρ : S × Σ → S is a transition function, which can be a partial function. Intuitively,
#       s_0 = ρ(s, a) is the state that A can move into when it is in state s and it reads the
#       symbol a. (If ρ(s, a) is undefined then reading a leads to rejection.)


### DFA definition

# alphabet = set()
# states = set()
# initial_state = 0
# accepting_states = set()
# transitions = {}  # key (state in states, action in alphabet) value [arriving state in states]
#
# dfa = [alphabet, states, initial_state, final, transition]

# Export a dfa "object" to a json file
# TODO dfa_to_json
def dfa_to_json(dfa):
    return


# Export a dfa "object" to a DOT file
# TODO dfa_to_dot
def dfa_to_dot(dfa):
    return


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
def dfa_dot_importer(input_file):
    # NOTE
    # shape=doublecircle -> accepting node
    # root=true -> initial node
    # label="a" -> action in alphabet
    # fake [style=invisible] -> skip this node, fake invisible one to initial state arrow
    # fake -> S [style=bold] -> skip this transition, just initial state arrow for graphical purpose

    # #pyDot Object
    g = pydot.graph_from_dot_file(input_file)[0]

    states = set()
    initial_state = 0
    accepting_states = set()
    for node in g.get_nodes():
        if node.get_name() == 'fake':
            continue
        states.add(node.get_name())
        for attribute in node.get_attributes():
            if attribute == 'root':
                initial_state = node.get_name()
            if attribute == 'shape' and node.get_attributes()['shape'] == 'doublecircle':
                accepting_states.add(node.get_name())

    alphabet = set()
    transitions = {}
    for edge in g.get_edges():
        if edge.get_source() == 'fake':
            continue
        alphabet.add(edge.get_label().replace('"', ''))
        transitions[edge.get_source(), edge.get_label().replace('"', '')] = edge.get_destination()

    # return map
    dfa = {}
    dfa['alphabet'] = alphabet
    dfa['states'] = states
    dfa['initial_state'] = initial_state
    dfa['accepting_states'] = accepting_states
    dfa['transitions'] = transitions
    return dfa


# Print in output a DOT file and an image of the given DFA
# graphviz library
def dfa_render(dfa, name):
    g = graphviz.Digraph(format='svg')
    for state in dfa['states']:
        g.node(state)
        # TODO case initial node
        # TODO case accepting node

    for transition in dfa['transitions']:
        g.edge(transition[0], dfa['transitions'][transition], label=transition[1])

    g.render(filename='img/' + name)


# Print in output a DOT file and an image of the given DFA
# pydot library
def pydot_dfa_render(dfa, name):
    # TODO special view for sink node?
    g = pydot.Dot(graph_type='digraph')

    fake = pydot.Node('fake', style='invisible')
    g.add_node(fake)
    for state in dfa['states']:
        node = pydot.Node(state)
        if state == dfa['initial_state']:
            node.set_root(True)
            g.add_edge(pydot.Edge(fake, node, style='bold'))

        if state in dfa['accepting_states']:
            node.set_shape('doublecircle')
        g.add_node(node)

    for transition in dfa['transitions']:
        g.add_edge(pydot.Edge(transition[0], dfa['transitions'][transition], label=transition[1]))

    g.write_svg('img/' + name + '.svg')
    g.write_dot('img/' + name + '.dot')


### Checks if a given dfa accepts a run on a given input word
def run_acceptance(dfa, run, word):
    # If 'run' fist state is not an initial state return False
    if run[0] != dfa['initial_state']:
        return False
    # If last 'run' state is not an accepting state return False
    if run[-1] not in dfa['accepting_states']:
        return False
    for i in range(len(word) - 1):
        if (run[i], word[i]) in dfa['transitions']:
            if dfa['transitions'][run[i], word[i]] != run[i + 1]:
                return False
        else:
            return False
    return True


### Checks if a given word is accepted by a dfa
def word_acceptance(dfa, word):
    current_state = dfa['initial_state']
    for action in word:
        if (current_state, action) in dfa['transitions']:
            current_state = dfa['transitions'][current_state, action]
        else:
            return False
    if current_state in dfa['accepting_states']:
        return True
    else:
        return False


### DFA completion
def dfa_completion(dfa):
    dfa['states'].add('sink')
    for s in dfa['states']:
        for a in dfa['alphabet']:
            if (s, a) not in dfa['transitions']:
                dfa['transitions'][s, a] = 'sink'
    return dfa


### DFA complementation
def dfa_complementation(dfa):
    dfa_complemented = dfa_completion(dfa)
    dfa_complemented['accepting_states'] = dfa['states'].difference(dfa['accepting_states'])
    return dfa_complemented


### DFAs intersection
def dfa_intersection(dfa_1, dfa_2):
    intersection = {}
    intersection['alphabet'] = dfa_1['alphabet']
    intersection['states'] = set(cartesian_product(dfa_1['states'], dfa_2['states']))
    intersection['initial_state'] = (dfa_1['initial_state'], dfa_2['initial_state'])
    intersection['accepting_states'] = set(cartesian_product(dfa_1['accepting_states'], dfa_2['accepting_states']))

    intersection['transitions'] = {}
    for s in intersection['states']:
        for a in intersection['alphabet']:
            if (s[0], a) in dfa_1['transitions'] and (s[1], a) in dfa_2['transitions']:
                s1 = dfa_1['transitions'][s[0], a]
                s2 = dfa_2['transitions'][s[1], a]
                intersection['transitions'][s, a] = (s1, s2)
            else:
                continue
    return intersection


### DFAs union
def dfa_union(dfa_1, dfa_2):
    dfa_1 = dfa_completion(dfa_1)
    dfa_2 = dfa_completion(dfa_2)

    union = {}
    union['alphabet'] = dfa_1['alphabet']
    union['states'] = set(cartesian_product(dfa_1['states'], dfa_2['states']))
    union['initial_state'] = (dfa_1['initial_state'], dfa_2['initial_state'])

    union['accepting_states'] = set(cartesian_product(dfa_1['accepting_states'], dfa_2['states'])).union(
        set(cartesian_product(dfa_1['states'], dfa_2['accepting_states']))
    )

    union['transitions'] = {}
    for s in union['states']:
        for a in union['alphabet']:
            s1 = dfa_1['transitions'][s[0], a]
            s2 = dfa_2['transitions'][s[1], a]
            union['transitions'][s, a] = (s1, s2)
    return union


###*DFA minimization [greatest fix point]
def dfa_minimization(dfa):
    dfa = dfa_completion(dfa)

    ##  Greatest-fixpoint

    # cartesian product of DFA states
    z_current = set(cartesian_product(dfa['states'], dfa['states']))

    z_next = z_current.copy();

    # First bisimulation condition check (can be done just once)
    # s ∈ F iff t ∈ F
    for element in z_current:
        if (element[0] in dfa['accepting_states'] and element[1] not in dfa['accepting_states']) or (
                        element[0] not in dfa['accepting_states'] and element[1] in dfa['accepting_states']):
            z_next.remove(element)
    z_current = z_next

    # Second and third condition of bisimularity check, while succeed or fail
    while z_current:
        z_next = z_current.copy();
        for element in z_current:
            # for all s0,a s.t. ρ(s, a) = s_0 , there exists t 0 s.t. ρ(t, a) = t 0 and (s_0 , t 0 ) ∈ Z i ;
            for a in dfa['alphabet']:
                if (element[0], a) in dfa['transitions'] and (element[1], a) in dfa['transitions']:
                    if (dfa['transitions'][element[0], a], dfa['transitions'][element[1], a]) not in z_current:
                        z_next.remove(element)
                        break
                else:
                    # action a not possible in state element[0] or element[1]
                    z_next.remove(element)

        if z_next == z_current:
            break
        z_current = z_next

    ## Equivalence Sets
    equivalence = {}
    for element in z_current:
        equivalence.setdefault(element[0], set()).add(element[1])

    ## Minimal DFA construction
    dfa_min = {}
    dfa_min['alphabet'] = dfa['alphabet'].copy()

    dfa_min['states'] = set()

    # select one element for each equivalence set
    for equivalence_set in equivalence.values():
        if dfa_min['states'].isdisjoint(equivalence_set):
            e = equivalence_set.pop()
            dfa_min['states'].add(e)
            equivalence_set.add(e)

    dfa_min['initial_state'] = dfa['initial_state']
    dfa_min['accepting_states'] = dfa_min['states'].intersection(dfa['accepting_states'])

    dfa_min['transitions'] = dfa['transitions'].copy()
    for p in dfa['transitions']:
        if p[0] not in dfa_min['states']:
            dfa_min['transitions'].pop(p)
        if dfa['transitions'][p] not in dfa_min['states']:
            dfa_min['transitions'][p] = equivalence[dfa['transitions'][p]].intersection(dfa_min['states']).pop()

    return dfa_min


# remove unreachable states from a dfa
def dfa_reachable(dfa):
    # set of reachable states from initial states
    s_r = set()
    s_r.add(dfa['initial_state'])
    s_r_stack = s_r.copy()
    while s_r_stack:
        s = s_r_stack.pop()
        for a in dfa['alphabet']:
            if (s, a) in dfa['transitions']:
                if dfa['transitions'][s, a] not in s_r:
                    s_r_stack.add(dfa['transitions'][s, a])
                    s_r.add(dfa['transitions'][s, a])
            else:
                pass
    dfa['states'] = s_r
    dfa['accepting_states'] = dfa['accepting_states'].intersection(dfa['states'])

    for p in dfa['transitions']:
        if p[0] not in dfa['states']:
            dfa['transitions'].remove(p)
        if dfa['transitions'][p] not in dfa['states']:
            dfa['transitions'].remove(p)

    return dfa


# remove states that do not reach a final state from dfa
def dfa_co_reachable(dfa):
    # set of states reaching final states
    s_r = dfa['accepting_states'].copy()
    s_r_stack = s_r.copy()

    # inverse transition function
    inv_transitions = {}
    for k, v in dfa['transitions'].items():
        inv_transitions.setdefault(v, set()).add(k)

    while s_r_stack:
        s = s_r_stack.pop()
        for s_app in inv_transitions[s]:
            if s_app[0] not in s_r:
                s_r_stack.add(s_app[0])
                s_r.add(s_app[0])

    dfa['states'] = s_r
    # TODO check non reachabilility
    # if dfa['initial_state'] not in dfa['states']:
    #     return False

    for p in dfa['transitions']:
        if p[0] not in dfa['states']:
            dfa['transitions'].remove(p)
        if dfa['transitions'][p] not in dfa['states']:
            dfa['transitions'].remove(p)

    return dfa


### DFA trimming
def dfa_trimming(dfa):
    # Reachable DFA
    dfa = dfa_reachable(dfa)
    # Co-reachable DFA
    dfa = dfa_co_reachable(dfa)
    # trimmed DFA
    return dfa


### DFA projection out ( the operation that removes from a word all occurrence of symbols in X )
# Given a dfa A = (Σ, S, s 0 , ρ, F ), we can define an nfa A π X that recognizes the language π X (L(A)).
# DFA -> NFA
def dfa_projection(dfa, X):
    nfa = dfa.copy()
    nfa['alphabet'] = dfa['alphabet'].difference(X)
    nfa['transitions'] = {}
    e_x = {}
    # ε_X ⊆ S×S formed by the pairs of states (s, s_0) such that s_0 is reachable from s through transition symbols ∈ X

    # mark each transition using symbol a ∈ X
    for transition in dfa['transitions']:
        if transition[1] not in nfa['alphabet']:
            # nfa['transitions'][transition[0], 'epsilon'] = dfa['transitions'][transition]
            e_x.setdefault(transition[0], set()).add(dfa['transitions'][transition])
            # nfa['transitions'].pop(transition)
        else:
            nfa['transitions'].setdefault(transition, set()).add(dfa['transitions'][transition])

    current = deepcopy(e_x)
    while True:
        for state in current.keys():
            for direct in current[state]:
                if direct in current:
                    for reached in current[direct]:
                        e_x[state].add(reached)
        if current == e_x:
            break
        current = deepcopy(e_x)

    # NFA initial states
    nfa.pop('initial_state')
    nfa['initial_states'] = e_x[dfa['initial_state']]
    nfa['initial_states'].add(dfa['initial_state'])

    # inverse transition function
    inv_e_x = {}
    for k, v in e_x.items():
        for s in v:
            inv_e_x.setdefault(s, set()).add(k)

    # NFA transitions
    for transition in dfa['transitions']:
        if transition[1] in nfa['alphabet']:
            nfa['transitions'].setdefault(transition, set()).add(dfa['transitions'][transition])

            # add all forward reachable set
            if dfa['transitions'][transition] in e_x:
                for reached in e_x[dfa['transitions'][transition]]:
                    nfa['transitions'].setdefault(transition, set()).add(reached)

            # link all states that reach transition[0] to forward reachable set
            for reached in nfa['transitions'][transition]:
                if transition[0] in inv_e_x:
                    for past in inv_e_x[transition[0]]:
                        nfa['transitions'].setdefault((past, transition[1]), set()).add(reached)

    return nfa


# - DFA nonemptiness
def dfa_nonemptiness_check(dfa):
    # BFS
    stack = [dfa['initial_state']]
    visited = set()
    visited.add(dfa['initial_state'])
    while stack:
        state = stack.pop()  # TODO tweak popping order (now the last element is chosen)
        for a in dfa['alphabet']:
            if (state, a) in dfa['transitions']:
                if dfa['transitions'][state, a] in dfa['accepting_states']:
                    return True
                if dfa['transitions'][state, a] not in visited:
                    stack.append(dfa['transitions'][state, a])
    return False
