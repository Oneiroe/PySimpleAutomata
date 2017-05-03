"""
Module to manage AFW (Alternating Finite automaton on Words).

Formally a AFW (Alternating Finite automaton on Words) is a tuple
:math:`(Σ, S, s0, ρ, F )`, where:

 • Σ is a finite nonempty alphabet;
 • S is a finite nonempty set of states;
 • :math:`s0 ∈ S` is the initial state (notice that, as in dfas,
   we have a unique initial state);
 • F ⊆ S is the set of accepting states;
 • :math:`ρ : S × Σ → B+(S)` is a transition function.
   :math:`B+(X)` be the set of positive Boolean formulas
   over a given set X
   ex. of :math:`ρ: ρ(s, a) = (s1 ∧ s2) ∨ (s3 ∧ s4)`

In this module a AFW is defined as follows

 AFW = dict() with the following keys-values:

 • alphabet         => set()
 • states           => set()
 • initial_state    => 'state_0'
 • accepting_states => set()
 • transitions      => dict(), where
        **key** (state ∈ states, action ∈ alphabet)

        **value** [string representing a PYTHON boolean expression
                   over states; where we also allow the formulas
                   *True* and *False*]
"""

from PySimpleAutomata import NFA
import itertools
import re
from copy import deepcopy


def __recursive_acceptance(afw, state, remaining_word):
    """ Recursive call for word acceptance.

        :param dict afw: input AFW;
        :param str state: current state;
        :param list remaining_word: list containing the remaining
        words.
        :return: *(bool)*, True if the word is accepted, false
        otherwise.
        """
    # the word is accepted only if all the final states are
    # accepting states
    if len(remaining_word) == 0:
        if state in afw['accepting_states']:
            return True
        else:
            return False

    action = remaining_word[0]
    if (state, action) not in afw['transitions']:
        return False

    if afw['transitions'][state, action] == 'True':
        return True
    elif afw['transitions'][state, action] == 'False':
        return False

    transition = (state, action)
    # extract from the boolean formula of the transition the
    # states involved in it
    involved_states = list(
        set(
            re.findall(r"[\w']+", afw['transitions'][transition])
        ).difference({'and', 'or', 'True', 'False'})
    )
    possible_assignments = set(
        itertools.product([True, False], repeat=len(involved_states)))
    # For all possible assignment of the the transition (a
    # boolean formula over the states)
    for assignment in possible_assignments:
        mapping = dict(zip(involved_states, assignment))
        # If the assignment evaluation is positive
        if eval(afw['transitions'][transition], mapping):
            ok = True
            mapping.pop('__builtins__')  # removes useless entry
            # added by the function eval()

            # Check if the word is accepted in ALL the states
            # mapped to True by the assignment
            for mapped_state in mapping:
                if mapping[mapped_state] == False:
                    continue
                if not __recursive_acceptance(afw,
                                              mapped_state,
                                              remaining_word[1:]):
                    # if one positive state of the assignment
                    # doesn't accepts the word,the whole
                    # assignment is discarded
                    ok = False
                    break
            if ok:
                # If at least one assignment accepts the word,
                # the word is accepted by the afw
                return True
    return False


def afw_word_acceptance(afw: dict, word: list) -> bool:
    """ Checks if a **word** is accepted by input AFW, returning
    True/False.

    The word w is accepted by a AFW if exists at least an
    accepting run on w. A run for AFWs is a tree and
    an alternating automaton can have multiple runs on a given
    input.
    A run is accepting if all the leaf nodes are accepting states.

    :param dict afw: input AFW;
    :param list word: list of symbols ∈ afw['alphabet'].
    :return: *(bool)*, True if the word is accepted, False otherwise.
    """
    return __recursive_acceptance(afw, afw['initial_state'], word)


# Side effect on input afw
def afw_completion(afw):
    """ Side effect on input! Complete the afw adding not
    present transitions and marking them as False.

    :param dict afw: input AFW.
    """

    for state in afw['states']:
        for a in afw['alphabet']:
            if (state, a) not in afw['transitions']:
                afw['transitions'][state, a] = 'False'
    return afw


def nfa_to_afw_conversion(nfa: dict) -> dict:
    """ Returns a AFW reading the same language of input NFA.

    Let :math:`A = (Σ,S,S^0, ρ,F)`  be an nfa. Then we define the
    afw AA such that :math:`L(AA) = L(A)` as follows
    :math:`AA = (Σ, S ∪ {s_0}, s_0 , ρ_A , F )` where :math:`s_0`
    is a new state and :math:`ρ_A` is defined as follows:

     • :math:`ρ_A(s, a)= ⋁_{(s,a,s')∈ρ}s'`, for all :math:`a ∈ Σ`
       and :math:`s ∈ S`
     • :math:`ρ_A(s^0, a)= ⋁_{s∈S^0,(s,a,s')∈ρ}s'`, for all
       :math:`a ∈ Σ`

    We take an empty disjunction in the definition of AA to be
    equivalent to false. Essentially,
    the transitions of A are viewed as disjunctions in AA . A
    special treatment is needed for the
    initial state, since we allow a set of initial states in
    nondeterministic automata, but only a
    single initial state in alternating automata.

    :param dict nfa: input NFA.
    :return: *(dict)* representing a AFW.
    """
    afw = {
        'alphabet': nfa['alphabet'].copy(),
        'states': nfa['states'].copy(),
        'initial_state': 'root',
        'accepting_states': nfa['accepting_states'].copy(),
        'transitions': dict()
    }

    # Make sure "root" node doesn't already exists, in case rename it
    i = 0
    while afw['initial_state'] in nfa['states']:
        afw['initial_state'] = 'root' + str(i)
        i += 1
    afw['states'].add(afw['initial_state'])

    for (state, action) in nfa['transitions']:
        boolean_formula = str()
        for destination in nfa['transitions'][state, action]:
            boolean_formula += destination + ' or '
        # strip last ' or ' from the formula string
        boolean_formula = boolean_formula[0:-4]
        afw['transitions'][state, action] = boolean_formula
        if state in nfa['initial_states']:
            afw['transitions'][afw['initial_state'], action] = boolean_formula

    return afw


def afw_to_nfa_conversion(afw: dict) -> dict:
    """ Returns a NFA reading the same language of input AFW.

    Let :math:`A = (Σ, S, s^0 , ρ, F )`  be an afw. Then we
    define the nfa :math:`A_N` such that :math:`L(A_N) = L(A)`
    as follows :math:`AN = (Σ, S_N , S^0_N , ρ_N , F_N )` where:

     • :math:`S_N = 2^S`
     • :math:`S^0_N= \{\{s^0 \}\}`
     • :math:`F_N=2^F`
     • :math:`(Q,a,Q') ∈ ρ_N` iff :math:`Q'` satisfies :math:`⋀_{
       s∈Q} ρ(s, a)`

     We take an empty conjunction in the definition of
     :math:`ρ_N` to be equivalent to true; thus, :math:`(∅, a,
     ∅) ∈ ρ_N`.

    :param dict afw: input AFW.
    :return: *(dict)* representing a NFA.
    """

    nfa = {
        'alphabet': afw['alphabet'].copy(),
        'initial_states': {(afw['initial_state'],)},
        'states': set(),
        'accepting_states': set(),
        'transitions': dict()
    }

    # State of the NFA are composed by the union of more states of the AFW
    for state in afw['states']:
        nfa['states'].add((state,))

    i = len(afw['states'])
    while i > 1:
        # all combination of i# states from the AFW
        nfa['states'].update(set(itertools.combinations(afw['states'], i)))
        i -= 1

    for state in nfa['states']:
        # The state is accepting only if composed exclusively of final states
        accepting_state = True
        for s in state:
            if s not in afw['accepting_states']:
                accepting_state = False
                break
        if accepting_state:
            nfa['accepting_states'].add(state)

        # NAIVE
        for action in nfa['alphabet']:
            boolean_formula = 'True'
            # Given an action
            # join the destinations of the single states in a boolean formula
            for s in state:
                if (s, action) not in afw['transitions']:
                    boolean_formula += ' and False'
                else:
                    boolean_formula += \
                        ' and (' + \
                        afw['transitions'][s, action] + \
                        ')'

            # evaluate that formula over all the possible NFA states
            mapping = dict.fromkeys(afw['states'], False)
            for evaluation in nfa['states']:
                for e in evaluation:
                    mapping[e] = True

                # If the formula is satisfied
                if eval(boolean_formula, mapping):
                    # add the transition to the resulting NFA
                    nfa['transitions'].setdefault((state, action), set()).add(
                        evaluation)

                for e in evaluation:
                    mapping[e] = False

    return nfa


def formula_dual(input_formula: str) -> str:
    """ Returns the dual of the input formula.

    The dual operation on formulas in :math:`B^+(X)` is defined as:
    the dual :math:`\overline{θ}` of a formula :math:`θ` is obtained from θ by
    switching :math:`∧` and :math:`∨`, and
    by switching :math:`true` and :math:`false`.

    :param str input_formula: original string.
    :return: *(str)*, dual of input formula.
    """
    conversion_dictionary = {
        'and': 'or',
        'or': 'and',
        'True': 'False',
        'False': 'True'
    }

    return re.sub(
        '|'.join(re.escape(key) for key in conversion_dictionary.keys()),
        lambda k: conversion_dictionary[k.group(0)], input_formula)


def afw_complementation(afw: dict) -> dict:
    """ Returns a AFW reading the complemented language read by
    input AFW.

    Let :math:`A = (Σ, S, s^0 , ρ, F )`. Define :math:`Ā = (Σ, S,
    s^0 , \overline{ρ}, S − F )`,
    where :math:`\overline{ρ}(s, a) = \overline{ρ(s, a)}` for all
    :math:`s ∈ S` and :math:`a ∈ Σ`.
    That is, :math:`\overline{ρ}` is the dualized transition
    function. It can be shown that :math:`L( Ā) = Σ^∗ − L(A)`.

    The input afw need to be completed i.e. each non existing
    transition must be added pointing to False.

    :param dict afw: input AFW.
    :return: *(dict)* representing a AFW.
    """
    completed_input = afw_completion(deepcopy(afw))

    complemented_afw = {
        'alphabet': completed_input['alphabet'],
        'states': completed_input['states'],
        'initial_state': completed_input['initial_state'],
        'accepting_states':
            completed_input['states'].difference(afw['accepting_states']),
        'transitions': dict()
    }

    for transition in completed_input['transitions']:
        complemented_afw['transitions'][transition] = \
            formula_dual(completed_input['transitions'][transition])
    return complemented_afw


def __replace_all(repls: dict, input: str) -> str:
    """ Replaces from the string **input** all the occurrence of the
    keys element of the dictionary **repls** with their relative
    value.

    :param dict repls: dictionary containing the mapping
                  between the values to be changed and their
                  appropriate substitution;
    :param str input: original string.
    :return: *(str)*, string with the appropriate values replaced.
    """
    return re.sub('|'.join(re.escape(key) for key in repls.keys()),
                  lambda k: repls[k.group(0)], input)


# SIDE EFFECTS
def rename_afw_states(afw: dict, suffix: str):
    """ Side effect on input! Renames all the states of the AFW
    adding a **suffix**.

    It is an utility function used during testing to avoid automata to have
    states with names in common.

    Avoid suffix that can lead to special name like "as", "and",...

    :param dict afw: input AFW.
    :param str suffix: string to be added at beginning of each state name.
    """
    conversion_dict = {}
    new_states = set()
    new_accepting = set()
    for state in afw['states']:
        conversion_dict[state] = '' + suffix + state
        new_states.add('' + suffix + state)
        if state in afw['accepting_states']:
            new_accepting.add('' + suffix + state)

    afw['states'] = new_states
    afw['initial_state'] = '' + suffix + afw['initial_state']
    afw['accepting_states'] = new_accepting

    new_transitions = {}
    for transition in afw['transitions']:
        new_transition = __replace_all(conversion_dict, transition[0])
        new_transitions[new_transition, transition[1]] = \
            __replace_all(conversion_dict, afw['transitions'][transition])
    afw['transitions'] = new_transitions


def afw_union(afw_1: dict, afw_2: dict) -> dict:
    """ Returns a AFW that reads the union of the languages read
    by input AFWs.

    Let :math:`A_1 = (Σ, S_1 , s^0_1, ρ_1 , F_1 )` and :math:`A_2
    = (Σ, S_2 , s^0_2, ρ_2 , F_2 )`
    be alternating automata accepting the languages :math:`L(
    A_1)` and :math:`L(A_2)`.
    Then, :math:`B_∪ = (Σ, S_1 ∪ S_2 ∪ {root}, ρ_∪ , root ,
    F_1 ∪ F_2 )` with
    :math:`ρ_∪ = ρ_1 ∪ ρ_2 ∪ [(root, a): ρ(s^0_1 , a) ∨ ρ(s^0_2 ,
    a)]` accepts :math:`L(A_1) ∪ L(A_2)`.

    Pay attention to avoid having the AFWs with state names in common, in case
    use :mod:`PySimpleAutomata.AFW.rename_afw_states` function.

    :param dict afw_1: first input AFW;
    :param dict afw_2: second input AFW;.
    :return: *(dict)* representing the united AFW.
    """
    # make sure new root state is unique
    initial_state = 'root'
    i = 0
    while initial_state in afw_1['states'] or initial_state in afw_2['states']:
        initial_state = 'root' + str(i)
        i += 1

    union = {
        'alphabet': afw_1['alphabet'].union(afw_2['alphabet']),
        'states':
            afw_1['states'].union(afw_2['states']).union({initial_state}),
        'initial_state': initial_state,
        'accepting_states':
            afw_1['accepting_states'].union(afw_2['accepting_states']),
        'transitions': deepcopy(afw_1['transitions'])
    }

    # add also afw_2 transitions
    union['transitions'].update(afw_2['transitions'])

    # if just one initial state is accepting, so the new one is
    if afw_1['initial_state'] in afw_1['accepting_states'] \
            or afw_2['initial_state'] in afw_2['accepting_states']:
        union['accepting_states'].add(union['initial_state'])

    # copy all transitions of initial states and eventually their conjunction
    # into the new initial state
    for action in union['alphabet']:
        if (afw_1['initial_state'], action) in afw_1['transitions']:
            union['transitions'][initial_state, action] = \
                '(' + \
                afw_1['transitions'][afw_1['initial_state'], action] + \
                ')'
            if (afw_2['initial_state'], action) in afw_2['transitions']:
                union['transitions'][initial_state, action] += \
                    ' or (' + \
                    afw_2['transitions'][afw_2['initial_state'], action] + \
                    ')'
        elif (afw_2['initial_state'], action) in afw_2['transitions']:
            union['transitions'][initial_state, action] = \
                '(' + \
                afw_2['transitions'][afw_2['initial_state'], action] + \
                ')'

    return union


def afw_intersection(afw_1: dict, afw_2: dict) -> dict:
    """ Returns a AFW that reads the intersection of the
    languages read by input AFWs.

    Let :math:`A_1 = (Σ, S_1 , s^0_1, ρ_1 , F_1 )` and :math:`A_2
    = (Σ, S_2 , s^0_2, ρ_2 , F_2 )`
    be alternating automata accepting the languages :math:`L(
    A_1)` and :math:`L(A_2)`.
    Then, :math:`B_∩ = (Σ, S_1 ∪ S_2 ∪ {root}, root, ρ_∩ , F_1 ∪
    F_2 )` with
    :math:`ρ_∩ = ρ_1 ∪ ρ_2 ∪ [(root, a): ρ(s^0_1 , a) ∧ ρ(s^0_2 ,
    a)]` accepts :math:`L(A_1) ∩ L(A_2)`.

    :param dict afw_1: first input AFW;
    :param dict afw_2: second input AFW.
    :return: *(dict)* representing a AFW.
    """
    # make sure new root state is unique
    initial_state = 'root'
    i = 0
    while initial_state in afw_1['states'] or initial_state in afw_2['states']:
        initial_state = 'root' + str(i)
        i += 1

    intersection = {
        'alphabet': afw_1['alphabet'].union(afw_2['alphabet']),
        'states':
            afw_1['states'].union(afw_2['states']).union({initial_state}),
        'initial_state': initial_state,
        'accepting_states':
            afw_1['accepting_states'].union(afw_2['accepting_states']),
        'transitions': deepcopy(afw_1['transitions'])
    }

    # add also afw_2 transitions
    intersection['transitions'].update(afw_2['transitions'])

    # if both initial states are accepting, so the new one is
    if afw_1['initial_state'] in afw_1['accepting_states'] \
            and afw_2['initial_state'] in afw_2['accepting_states']:
        intersection['accepting_states'].add(
            intersection['initial_state'])

    for action in intersection['alphabet']:
        if (afw_1['initial_state'], action) in afw_1['transitions']:
            intersection['transitions'][initial_state, action] = \
                '(' + \
                afw_1['transitions'][afw_1['initial_state'], action] + \
                ')'
            if (afw_2['initial_state'], action) in afw_2['transitions']:
                intersection['transitions'][initial_state, action] += \
                    ' and (' + \
                    afw_2['transitions'][afw_2['initial_state'], action] + \
                    ')'
            else:
                intersection['transitions'][
                    initial_state, action] += ' and False'
        elif (afw_2['initial_state'], action) in afw_2['transitions']:
            intersection['transitions'][initial_state, action] = \
                'False and (' + \
                afw_2['transitions'][afw_2['initial_state'], action] + \
                ')'

    return intersection


def afw_nonemptiness_check(afw: dict) -> bool:
    """ Checks if the input AFW reads any language other than the
    empty one, returning True/False.

    The afw is translated into a nfa and then its nonemptiness is
    checked.

    :param dict afw: input AFW.
    :return: *(bool)*, True if input afw is nonempty, False otherwise.
    """
    nfa = afw_to_nfa_conversion(afw)
    return NFA.nfa_nonemptiness_check(nfa)


def afw_nonuniversality_check(afw: dict) -> bool:
    """ Checks if the language read by the input AFW is different
    from Σ∗, returning True/False.

    The afw is translated into a nfa and then its nonuniversality
    is checked.

    :param dict afw: input AFW.
    :return: *(bool)*, True if input afw is nonuniversal, False
             otherwise.
    """
    nfa = afw_to_nfa_conversion(afw)
    return NFA.nfa_nonuniversality_check(nfa)
