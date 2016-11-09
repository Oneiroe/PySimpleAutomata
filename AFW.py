import json
from itertools import product as cartesian_product
import NFA


# ###
# TO-DO
# TODO correctness check of json imported automata

# an afw (alternating finite automaton on words) is a tuple A = (Σ, S, s0, ρ, F ), where:
# • Σ is a finite nonempty alphabet;
# • S is a finite nonempty set of states;
# • s0 ∈ S is the initial state (notice that, as in dfas, we have a unique initial state);
# • F ⊆ S is the set of accepting states;
# • ρ : S × Σ → B+(S) is a transition function.
#           B+(X) be the set of positive Boolean formulas over a given set X
#           ex. of ρ:  ρ(s, a) = (s1 ∧ s2) ∨ (s3 ∧ s4)


### AFW definition

# alphabet = set()
# states = set()
# initial_state = 0
# accepting_states = set()
# transitions = {} # key (state ∈ states, action ∈ alphabet) value [string representing a PYTHON boolean expression
#   over states; where we also allow the formulas true and false]
#
# afw = [alphabet, states, initial_state, accepting_states, transitions]

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


# - AFW run acceptance

# - NFA to AFW conversion
def nfa_to_afw_conversion(nfa):
    afw = {}
    afw['alphabet'] = nfa['alphabet']
    afw['states'] = nfa['states']
    afw['states'].add('s_alpha')
    afw['initial_state'] = 's_alpha'
    afw['accepting_states'] = nfa['accepting_states']
    afw['transitions'] = {}

    for t in nfa['transitions']:
        boolean_formula = ''
        for state in nfa['transitions'][t]:
            boolean_formula = boolean_formula + state + ' or '
        boolean_formula = boolean_formula[0:-4]
        afw['transitions'][t] = boolean_formula
        if t[0] in nfa['initial_states']:
            afw['transitions']['s_alpha', t[1]] = boolean_formula

    return afw

# - AFW to NFA conversion
# - AFW complementation
# - AFW nonemptiness
# - AFW nonuniversality
