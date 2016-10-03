import io
import json
from copy import deepcopy
import itertools


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

# Guided NFA constructor
# TODO nfa_creator_assistant()
def nfa_creator_assistant():
    alphabet = set()
    states = set()
    initial_states = set()
    accepting_states = set()
    transitions = {}  # key [state in states, action in alphabet] value [arriving state in states]

    print('Insert states...')

    print('Which ones are initial states?')

    print('Which ones are final states?')

    print('Insert actions...')

    print('Insert transitions')

    return [alphabet, states, initial_states, accepting_states, transitions]


# Export a nfa "object" to a json file
# TODO nfa_to_json
def nfa_to_json(nfa):
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


# - NFAs intersection
def nfa_intersection(nfa_1, nfa_2):
    intersection = {}
    intersection['alphabet'] = nfa_1['alphabet']
    intersection['states'] = set(itertools.product(nfa_1['states'], nfa_2['states']))
    intersection['initial_states'] = set(itertools.product(nfa_1['initial_states'], nfa_2['initial_states']))
    intersection['accepting_states'] = set(itertools.product(nfa_1['accepting_states'], nfa_2['accepting_states']))

    intersection['transitions'] = {}
    for s in intersection['states']:
        for a in intersection['alphabet']:
            try:
                s1 = nfa_1['transitions'][s[0], a]
            except KeyError:
                continue
            try:
                s2 = nfa_2['transitions'][s[1], a]
            except KeyError:
                continue
            for next_1 in s1:
                for next_2 in s2:
                    intersection['transitions'].setdefault((s, a), set()).add((next_1, next_2))

    return intersection

# - NFAs union
# - NFA determinization
# 	NFA -> DFA
# - NFA complementation
# - NFA nonemptiness
# - NFA nonuniversality
# - NFA interestingness check
