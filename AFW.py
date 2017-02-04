"""
Formally a AFW (Alternating Finite automaton on Words) is a tuple (Σ, S, s0, ρ, F ), where:
 • Σ is a finite nonempty alphabet;
 • S is a finite nonempty set of states;
 • s0 ∈ S is the initial state (notice that, as in dfas, we have a unique initial state);
 • F ⊆ S is the set of accepting states;
 • ρ : S × Σ → B+(S) is a transition function.
           B+(X) be the set of positive Boolean formulas over a given set X
           ex. of ρ:  ρ(s, a) = (s1 ∧ s2) ∨ (s3 ∧ s4)

In this module a AFW is defined as follows

 AFW = dict() with the following keys-values:
    alphabet         => set()
    states           => set()
    initial_state    => 'state_0'
    accepting_states => set()
    transitions      => dict() # key (state ∈ states, action ∈ alphabet) value [string representing a PYTHON boolean
                                 expression over states; where we also allow the formulas True and False]
"""

from itertools import product as cartesian_product
import NFA
import itertools
import re


# ###
# TO-DO
# TODO change name to new initial state when creating AFWs:
#      possibly already existing, expecially if the afw used in the operation is the result of a precedent operation


def __recursive_acceptance(afw, state, remaining_word):
    """ recursive call for word acceptance

        :param afw: dict() representing a afw
        :param state: str() current state
        :param remaining_word: list() containing the remaining word
        :return: bool, True if the word is accepted, false otherwise
        """
    # the word is accepted only if all the final states are accepting states
    if len(remaining_word) == 0:
        if state in afw['accepting_states']:
            return True
        else:
            return False

    action = remaining_word[0]
    if (state, action) not in afw['transitions']:
        return False

    transition = (state, action)
    # extract from the boolean formula of the transition the states involved in it
    involved_states = list(
        set(re.findall(r"[\w']+", afw['transitions'][transition])).difference({'and', 'or', 'True', 'False'}))
    possible_assignments = set(itertools.product([True, False], repeat=len(involved_states)))
    # For all possible assignment of the the transition (a boolean formula over the states)
    for assignment in possible_assignments:
        mapping = dict(zip(involved_states, assignment))
        # If the assignment evaluation is positive
        if eval(afw['transitions'][transition], mapping):
            ok = True
            mapping.pop('__builtins__')  # removes useless entry added by the function eval()
            # Check if the word is accepted in ALL the states mapped to True by the assignment
            for mapped_state in mapping:
                if mapping[mapped_state] == False:
                    continue
                if not __recursive_acceptance(afw, mapped_state, remaining_word[1:]):
                    # if one positive state of the assignment doesn't accepts the word,the whole assignment is discarded
                    ok = False
                    break
            if ok:
                # If at least one assignment accepts the word, the word is accepted by the afw
                return True
    return False


# TODO check correctness
def word_acceptance(afw: dict, word: list) -> bool:
    """ Checks if a word is accepted by input afw, returning True/False.

    TODO short-detailed explanation of AFWs word acceptance

    :param afw: dict() representing a afw
    :param word: list() of symbols ∈ afw['']
    :return: bool, True if the word is accepted, False otherwise
    """
    return __recursive_acceptance(afw, afw['initial_state'], word)


# TODO "We take an empty disjunction in the definition of AFW to be equivalent to False."
def nfa_to_afw_conversion(nfa: dict) -> dict:
    """ Returns a afw reading the same language of input nfa.

    TODO short-detailed explanation of NFAs to AFWs conversion

    :param nfa: dict() representing a nfa
    :return: dict() representing a afw
    """
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


def afw_to_nfa_conversion(afw: dict) -> dict:
    """ Returns a nfa reading the same language of input afw.

    TODO short-detailed explanation of AFWs to NFAs conversion

    :param afw: dict() representing a afw
    :return: dict() representing a nfa
    """
    # TODO check correctness
    # TODO "We take an empty conjunction in the definition of ρ N to be equivalent to true; thus (∅, a, ∅) ∈ NFA[trans.]
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
        mapping = dict.fromkeys(afw['states'], False)
        for state in nfa['states']:
            for s in state:
                mapping[s] = True
            if eval(afw['transitions'][transition], mapping):
                nfa['transitions'].setdefault(transition, set()).add(state)
            for s in state:
                mapping[s] = False

                # SLIGHTLY BETTER #TODO uncorrect for now, NAIVE is instead
                # # set with states involved in the boolean formula of the transition
                # involved_states = list(
                #     set(re.findall(r"[\w']+", afw['transitions'][transition])).difference({'and', 'or', 'True', 'False'}))
                # # all the possible True/False assignment to these states
                # possible_assignments = list(itertools.product([True, False], repeat=len(involved_states)))
                # for assignment in possible_assignments:
                #     mapping = dict(zip(involved_states, assignment))
                #     if eval(afw['transitions'][transition], mapping):
                #         mapping.pop('__builtins__')
                #         next_state = set()
                #         for state in mapping:
                #             if mapping[state] == True:
                #                 next_state.add(state)
                #         nfa['transitions'].setdefault(transition, set()).update(next_state)
                #         # TODO make a transition for each set of states leading to the conjunction of destination of the single states

    return nfa


def __replace_all(repls, str):
    # return re.sub('|'.join(repls.keys()), lambda k: repls[k.group(0)], str)
    return re.sub('|'.join(re.escape(key) for key in repls.keys()), lambda k: repls[k.group(0)], str)


def afw_complementation(afw: dict) -> dict:
    """ returns a afw reading the complemented language read by input afw.

    TODO short-detailed explanation of AFWs complementation

    :param afw: dict() representing a afw
    :return: dict() representing a afw
    """
    complemented_afw = {}
    complemented_afw['alphabet'] = afw['alphabet']
    complemented_afw['states'] = afw['states']
    complemented_afw['initial_state'] = afw['initial_state']
    complemented_afw['accepting_states'] = afw['states'].difference(afw['accepting_states'])
    complemented_afw['transitions'] = {}

    conversion_dictionary = {'and': 'or', 'or': 'and', 'True': 'False', 'False': 'True'}
    for transition in afw['transitions']:
        complemented_afw['transitions'][transition] = __replace_all(conversion_dictionary,
                                                                    afw['transitions'][transition])

    return complemented_afw


# TODO check equality between AFWs alphabets
def afw_union(afw_1: dict, afw_2: dict) -> dict:
    """ Returns a afw that reads the union of the languages read by input afws

    TODO short-detailed explanation of AFWs union

    :param afw_1: dict() representing a afw
    :param afw_2: dict() representing a afw
    :return: dict() representing a afw
    """
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
# unsure on correctness of the source material [lecture06a.pdf]
# TODO check equality between AFWs alphabets
def afw_intersection(afw_1: dict, afw_2: dict) -> dict:
    """ Returns a afw that reads the intersection of the languages read by input afws.

    TODO short-detailed explanation of AFWs intersection

    :param afw_1: dict() representing a afw
    :param afw_2: dict() representing a afw
    :return: dict() representing a afw
    """
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


def afw_nonemptiness_check(afw: dict) -> dict:
    """ Checks if the input afw reads any language other than the empty one, returning True/False.

    TODO short-detailed explanation of AFWs nonemptiness

    :param afw: dict() representing a afw
    :return: bool, True if input afw is nonempty, False otherwise
    """
    nfa = afw_to_nfa_conversion(afw)
    return NFA.nfa_nonemptiness_check(nfa)


# - AFW nonuniversality
def afw_nonuniversality_check(afw: dict) -> dict:
    """ Checks if the language read by the input afw is different from Σ∗, returning True/False.

    TODO short-detailed explanation of AFWs nonuniversality

    :param afw: dict() representing a afw
    :return: bool, True if input afw is nonuniversal, False otherwise
    """
    nfa = afw_to_nfa_conversion(afw)
    return NFA.nfa_nonemptiness_check(nfa)
