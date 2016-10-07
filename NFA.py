import json
from copy import deepcopy
from itertools import product as cartesian_product
import pydot


# ###
# TO-DO
# 

# An nfa, nondeterministic finite automaton, A is a tuple A = (Σ, S, S^0 , ρ, F ), where
# • Σ is a finite nonempty alphabet;
# • S is a finite nonempty set of states;
# • S^0 is the nonempty set of initial states;
# • F is the set of accepting states;
# • ρ : S × Σ × S is a transition relation. Intuitively, (s, a, s' ) ∈ ρ states that A can
#       move from s into s' when it reads the symbol a. It is allowed that (s, a, s' ) ∈ ρ and
#       (s, a, s'' ) ∈ ρ with S' != S'' .


### NFA definition

# alphabet = set()
# states = set()
# initial_states = set()
# accepting_states = set()
# transitions = {}  # key (state in states, action in alphabet) value [set of arriving stateS in states]
#
# nfa = [alphabet, states, initial_state, final, transition]

# Export a nfa "object" to a json file
# TODO nfa_to_json
def nfa_to_json(nfa):
    return


# Export a dfa "object" to a DOT file
# TODO dfa_to_dot
def nfa_to_dot(dfa):
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
# TODO
def nfa_dot_importer(input_file):
    nfa = {}
    return nfa


# - NFAs intersection
def nfa_intersection(nfa_1, nfa_2):
    intersection = {}
    intersection['alphabet'] = nfa_1['alphabet']
    intersection['states'] = set(cartesian_product(nfa_1['states'], nfa_2['states']))
    intersection['initial_states'] = set(cartesian_product(nfa_1['initial_states'], nfa_2['initial_states']))
    intersection['accepting_states'] = set(cartesian_product(nfa_1['accepting_states'], nfa_2['accepting_states']))

    intersection['transitions'] = {}
    for s in intersection['states']:
        for a in intersection['alphabet']:
            if (s[0], a) not in nfa_1['transitions'] or (s[1], a) not in nfa_2['transitions']:
                continue
            s1 = nfa_1['transitions'][s[0], a]
            s2 = nfa_2['transitions'][s[1], a]

            for next_1 in s1:
                for next_2 in s2:
                    intersection['transitions'].setdefault((s, a), set()).add((next_1, next_2))

    return intersection


# - NFAs union
def nfa_union(nfa_1, nfa_2):
    union = {}
    union['alphabet'] = nfa_1['alphabet']
    union['states'] = nfa_1['states'].union(nfa_2['states'])
    union['initial_states'] = nfa_1['initial_states'].union(nfa_2['initial_states'])
    union['accepting_states'] = nfa_1['accepting_states'].union(nfa_2['accepting_states'])

    union['transitions'] = nfa_1['transitions'].copy()
    for transition in nfa_2['transitions']:
        for elem in nfa_2['transitions'][transition]:
            union['transitions'].setdefault(transition, set()).add(elem)

    return union

# - NFA determinization
# 	NFA -> DFA
# - NFA complementation
# - NFA nonemptiness
# - NFA nonuniversality
# - NFA interestingness check

# ### Checks if a given dfa accepts a run on a given input word
# def run_acceptance(dfa, run, word):
