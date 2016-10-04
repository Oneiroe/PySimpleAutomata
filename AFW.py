import json
from itertools import product as cartesian_product


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
# transitions = {} # key (state ∈ states, action ∈ alphabet) value [list of disjointed sets of conjuncted states ∈ states]
#
# afw = [alphabet, states, initial_state, final, transition]

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

    transitions = {}  # key [state in states, action in alphabet] value [et of arriving states in states]
    for p in json_file['transitions']:
        transitions.setdefault((p[0], p[1]), list()).append(set(p[2]))

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

# - AFW definition
# - AFW to AFW conversion
# - AFW to AFW conversion
# - AFW complementation
# - AFW nonemptiness
# - AFW nonuniversality
