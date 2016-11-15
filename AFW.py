import json
from itertools import product as cartesian_product
import NFA
import itertools
import re


# ###
# TO-DO
# TODO correctness check of json imported automata
# TODO think of graphviz usage for these automata
# TODO change name to new initial state when creating AFWs:
#      possibly already existing, expecially if the afw used in the operation is the result of a precedent operation

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


# recursive call for word acceptance
def recursive_acceptance(afw, state, remaining_word):
    if len(remaining_word) == 0:
        if state in afw['accepting_states']:
            return True
        else:
            return False

    action = remaining_word[0]
    if (state, action) not in afw['transitions']:
        return False

    transition = (state, action)
    involved_states = list(
        set(re.findall(r"[\w']+", afw['transitions'][transition])).difference({'and', 'or', 'True', 'False'}))
    possible_assignments = set(itertools.product([True, False], repeat=len(involved_states)))
    for assignment in possible_assignments:
        mapping = dict(zip(involved_states, assignment))
        if eval(afw['transitions'][transition], mapping):
            ok = True
            mapping.pop('__builtins__')
            for mapped_state in mapping:
                if mapping[mapped_state] == False:
                    continue
                if not recursive_acceptance(afw, mapped_state, remaining_word[1:]):
                    ok = False
                    break
            if ok:
                return True
    return False


# - Checks if a word is accepted by a AFW
def word_acceptance(afw, word):
    # TODO check correctness
    return recursive_acceptance(afw, afw['initial_state'], word)


# - NFA to AFW conversion
def nfa_to_afw_conversion(nfa):
    afw = {}
    afw['alphabet'] = nfa['alphabet']
    afw['states'] = nfa['states']
    afw['states'].add('s_root')
    afw['initial_state'] = 's_root'
    afw['accepting_states'] = nfa['accepting_states']
    afw['transitions'] = {}

    for t in nfa['transitions']:
        boolean_formula = ''
        for state in nfa['transitions'][t]:
            boolean_formula += state + ' or '
        boolean_formula = boolean_formula[0:-4]
        afw['transitions'][t] = boolean_formula
        if t[0] in nfa['initial_states']:
            afw['transitions']['s_root', t[1]] = boolean_formula

    return afw


# - AFW to NFA conversion
def afw_to_nfa_conversion(afw):
    # TODO check correctness
    nfa = {}
    nfa['alphabet'] = afw['alphabet']
    nfa['initial_states'] = {afw['initial_state']}

    nfa['states'] = afw['states']
    nfa['accepting_states'] = afw['accepting_states']
    nfa['transitions'] = {}

    i = len(afw['states'])
    while i > 1:
        nfa['states'] = nfa['states'].union(set(itertools.combinations(afw['states'], i)))
        i -= 1

    i = len(afw['accepting_states'])
    while i > 1:
        nfa['accepting_states'] = nfa['accepting_states'].union(set(itertools.combinations(afw['accepting_states'], i)))
        i -= 1

    for transition in afw['transitions']:
        # NAIVE
        # mapping = dict.fromkeys(afw['states'], False)
        # for state in nfa['states']:
        #     for s in state:
        #         mapping[s] = True
        #     if eval(afw['transitions'][transition], mapping):
        #         nfa['transitions'].setdefault(transition, set()).add(state)
        #     for s in state:
        #         mapping[s] = False

        # SLIGHTLY BETTER
        # set with states involved in the boolean formula of the transition
        involved_states = list(
            set(re.findall(r"[\w']+", afw['transitions'][transition])).difference({'and', 'or', 'True', 'False'}))
        # all the possible True/False assignment to these states
        possible_assignments = list(itertools.product([True, False], repeat=len(involved_states)))
        for assignment in possible_assignments:
            mapping = dict(zip(involved_states, assignment))
            if eval(afw['transitions'][transition], mapping):
                for state in mapping:
                    if mapping[state] == True:
                        nfa['transitions'].setdefault(transition, set()).add(state)

    return nfa


def replace_all(repls, str):
    # return re.sub('|'.join(repls.keys()), lambda k: repls[k.group(0)], str)
    return re.sub('|'.join(re.escape(key) for key in repls.keys()),
                  lambda k: repls[k.group(0)], str)


# - AFW complementation
def afw_complementation(afw):
    complemented_afw = {}
    complemented_afw['alphabet'] = afw['alphabet']
    complemented_afw['states'] = afw['states']
    complemented_afw['initial_state'] = afw['initial_state']
    complemented_afw['accepting_states'] = afw['states'].difference(afw['accepting_states'])
    complemented_afw['transitions'] = {}

    conversion_dictionary = {'and': 'or', 'or': 'and', 'True': 'False', 'False': 'True'}
    for transition in afw['transitions']:
        complemented_afw['transitions'][transition] = replace_all(conversion_dictionary, afw['transitions'][transition])

    return complemented_afw


# - AFW Union
def afw_union(afw_1, afw_2):
    # TODO check equality between AFWs alphabets
    union = {}
    union['alphabet'] = afw_1['alphabet']
    union['states'] = afw_1['states'].union(afw_2['states']).union({'s_root'})
    union['initial_state'] = 's_root'
    union['accepting_states'] = afw_1['accepting_states'].union(afw_2['accepting_states'])
    union['transitions'] = afw_1['transitions'].copy()

    for transition in afw_2['transitions']:
        if transition in union['transitions']:
            union['transitions'][transition] += ' or ' + afw_2['transitions'][transition]
        else:
            union['transitions'][transition] = afw_2['transitions'][transition]

    for action in union['alphabet']:
        if (afw_1['initial_state'], action) in afw_1['transitions']:
            union['transitions']['s_root', action] = afw_1['transitions'][afw_1['initial_state'], action]
            if (afw_2['initial_state'], action) in afw_2['transitions']:
                union['transitions']['s_root', action] += ' or ' + afw_2['transitions'][afw_2['initial_state'], action]
        elif (afw_2['initial_state'], action) in afw_2['transitions']:
            union['transitions']['s_root', action] = afw_2['transitions'][afw_2['initial_state'], action]

    return union


# - AFW Intersection
def afw_intersection(afw_1, afw_2):
    # unsure on correctness of the source material [lecture06a.pdf]
    # TODO check equality between AFWs alphabets
    intersection = {}
    intersection['alphabet'] = afw_1['alphabet']
    intersection['states'] = afw_1['states'].union(afw_2['states']).union({'s_root'})
    intersection['initial_state'] = 's_root'
    intersection['accepting_states'] = afw_1['accepting_states'].union(afw_2['accepting_states'])
    intersection['transitions'] = afw_1['transitions'].copy()

    for transition in afw_2['transitions']:
        if transition in intersection['transitions']:
            intersection['transitions'][transition] += ' or ' + afw_2['transitions'][transition]
        else:
            intersection['transitions'][transition] = afw_2['transitions'][transition]

    for action in intersection['alphabet']:
        if (afw_1['initial_state'], action) in afw_1['transitions']:
            intersection['transitions']['s_root', action] = afw_1['transitions'][afw_1['initial_state'], action]
            if (afw_2['initial_state'], action) in afw_2['transitions']:
                intersection['transitions']['s_root', action] += ' and ' + afw_2['transitions'][
                    afw_2['initial_state'], action]
        elif (afw_2['initial_state'], action) in afw_2['transitions']:
            intersection['transitions']['s_root', action] = afw_2['transitions'][afw_2['initial_state'], action]

    return intersection


# - AFW nonemptiness
def afw_nonemptiness_check(afw):
    nfa = afw_to_nfa_conversion(afw)
    return NFA.nfa_nonemptiness_check(nfa)


# - AFW nonuniversality
def afw_nonuniversality_check(afw):
    nfa = afw_to_nfa_conversion(afw)
    return NFA.nfa_nonemptiness_check(nfa)
