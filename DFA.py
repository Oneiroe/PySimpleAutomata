import io
import json
from copy import deepcopy
import itertools


# A dfa, deterministic finite automaton, A is a tuple A = (Σ, S, s 0 , ρ, F ), where
# • Σ is a finite nonempty alphabet;
# • S is a finite nonempty set of states;
# • s 0 ∈ S is the initial state;
# • F ⊆ S is the set of accepting states;
# • ρ : S × Σ → S is a transition function, which can be a partial function. Intuitively,
#       s 0 = ρ(s, a) is the state that A can move into when it is in state s and it reads the
#       symbol a. (If ρ(s, a) is undefined then reading a leads to rejection.)


### DFA definition

# alphabet = set()
# states = set()
# initial_states = 0
# accepting_states = set()
# transitions = {}  # key (state in states, action in alphabet) value [arriving state in states]
#
# dfa = [alphabet, states, initial_state, final, transition]

# Guided DFA constructor
# TODO
def dfa_creator_assistant():
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


# Export a dfa "object" to a json file
# TODO
def dfa_to_json(dfa):
    return


# Import a dfa from a json file
def dfa_json_importer(input_file):
    file = open(input_file)
    json_file = json.load(file)
    # TODO exception handling while JSON deconding/IO error
    alphabet = set(json_file['alphabet'])
    states = set(json_file['states'])
    initial_states = set(json_file['initial_states'])
    accepting_states = set(json_file['accepting_states'])
    transitions = {}  # key [state in states, action in alphabet] value [arriving state in states]
    for p in json_file['transitions']:
        transitions[p[0], p[1]] = p[2]

    # return list
    # return [alphabet, states, initial_states, accepting_states, transitions]

    # return map
    dfa = {}
    dfa['alphabet'] = alphabet
    dfa['states'] = states
    dfa['initial_states'] = initial_states
    dfa['accepting_states'] = accepting_states
    dfa['transitions'] = transitions
    return dfa


### Checks if a given dfa accepts a run on a given input word
def run_acceptance(dfa, run, word):
    # If run fist state is not an initial state return False
    if run[0] not in dfa['initial_states']:
        return False
    # If last run state is not an accepting state return False
    if run[-1] not in dfa['accepting_states']:
        return False
    for i in range(len(word) - 1):
        try:
            if dfa['transitions'][run[i], word[i]] != run[i + 1]:
                return False
        except KeyError:
            return False
    return True


### DFA completion
def dfa_completion(dfa, side_effect):
    if side_effect == True:
        dfa_t = dfa
    else:
        dfa_t = deepcopy(dfa)
    dfa_t['states'].add('sink')
    for s in dfa_t['states']:
        for a in dfa_t['alphabet']:
            try:
                dfa_t['transitions'][s, a]
            except KeyError:
                dfa_t['transitions'][s, a] = 'sink'
    return dfa_t


### DFA complementation
def dfa_complementation(dfa, side_effect):
    dfa = dfa_completion(dfa, side_effect)
    if side_effect == True:
        dfa_c = dfa
    else:
        dfa_c = deepcopy(dfa)
    dfa_c['accepting_states'] = dfa['states'].difference(dfa['accepting_states'])
    return dfa_c


### DFAs intersection
def dfa_intersection(dfa_1, dfa_2):
    # if dfa_1['alphabet'].difference(dfa_2['alphabet'])!=set():
    #     return False
    intersection = {}
    intersection['alphabet'] = dfa_1['alphabet']
    intersection['states'] = set(itertools.product(dfa_1['states'], dfa_2['states']))
    intersection['initial_states'] = set(itertools.product(dfa_1['initial_states'], dfa_2['initial_states']))
    intersection['accepting_states'] = set(itertools.product(dfa_1['accepting_states'], dfa_2['accepting_states']))

    intersection['transitions'] = {}
    for s in intersection['states']:
        for a in intersection['alphabet']:
            try:
                s1 = dfa_1['transitions'][s[0], a]
            except KeyError:
                continue
            try:
                s2 = dfa_2['transitions'][s[1], a]
            except KeyError:
                continue
            intersection['transitions'][s, a] = (s1, s2)
    return intersection

### DFAs union

###*DFA minimization [greatest fix point]

### DFA trimming
# Reachable DFA
# Co-reachable DFA
# trimmed DFA

### DFA projection out ( the operation that removes from a word all occurrence of symbols in X )
# DFA -> NFA
