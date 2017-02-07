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
import copy


# ###
# TO-DO
# TODO change name to new initial state when creating AFWs:
#      possibly already existing, expecially if the afw used in the operation is the result of a precedent operation
# TODO change doc to laTex math formula using :math:`MATH_HERE`

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

    if afw['transitions'][state, action] == 'True':
        return True
    elif afw['transitions'][state, action] == 'False':
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


# Side effect on input afw
def afw_completion(afw):
    """ [Side effect on input] Complete the afw adding not present transitions marking them as False

    :param afw: dict() representing an afw
    """

    for state in afw['states']:
        for a in afw['alphabet']:
            if (state, a) not in afw['transitions']:
                afw['transitions'][state, a] = 'False'
    return afw


def word_acceptance(afw: dict, word: list) -> bool:
    """ Checks if a word is accepted by input afw, returning True/False.

    The word w is accepted by a AFW if exists at least an accepting run on w. A run for AFWs is a tree and
    an alternating automaton can have multiple runs on a given input.
    A run is accepting if all the leaf nodes are accepting states.

    :param afw: dict() representing a afw
    :param word: list() of symbols ∈ afw['alphabet']
    :return: bool, True if the word is accepted, False otherwise
    """
    return __recursive_acceptance(afw, afw['initial_state'], word)


# TODO "We take an empty disjunction in the definition of AFW to be equivalent to False."
def nfa_to_afw_conversion(nfa: dict) -> dict:
    """ Returns a afw reading the same language of input nfa.

    Let :math:`A = (Σ,S,S^0, ρ,F)`  be an nfa. Then we define the afw AA such that :math:`L(AA) = L(A)` as follows
    :math:`AA = (Σ, S ∪ {s_0}, s_0 , ρ_A , F )` where :math:`s_0` is a new state and :math:`ρ_A` is defined as follows:

     • :math:`ρ_A(s, a)= ⋁_{(s,a,s')∈ρ}s'`, for all :math:`a ∈ Σ` and :math:`s ∈ S`
     • :math:`ρ_A(s^0, a)= ⋁_{s∈S^0,(s,a,s')∈ρ}s'`, for all :math:`a ∈ Σ`

    We take an empty disjunction in the definition of AA to be equivalent to false. Essentially,
    the transitions of A are viewed as disjunctions in AA . A special treatment is needed for the
    initial state, since we allow a set of initial states in nondeterministic automata, but only a
    single initial state in alternating automata.

    :param nfa: dict() representing a nfa
    :return: dict() representing a afw
    """
    afw = {
        'alphabet': copy.copy(nfa['alphabet']),
        'states': copy.copy(nfa['states']),
        'initial_state': 's_root',
        'accepting_states': copy.copy(nfa['accepting_states']),
        'transitions': {}
    }
    afw['states'].add('s_root')

    for t in nfa['transitions']:
        boolean_formula = str()
        for state in nfa['transitions'][t]:
            boolean_formula += state + ' or '
        boolean_formula = boolean_formula[0:-4]
        afw['transitions'][t] = boolean_formula
        if t[0] in nfa['initial_states']:
            afw['transitions']['s_root', t[1]] = boolean_formula

    return afw


# TODO "We take an empty conjunction in the definition of ρ N to be equivalent to true; thus (∅, a, ∅) ∈ NFA[trans.]
def afw_to_nfa_conversion(afw: dict) -> dict:
    """ Returns a nfa reading the same language of input afw.

    Let :math:`A = (Σ, S, s^0 , ρ, F )`  be an afw. Then we define the nfa :math:`A_N` such that :math:`L(A_N) = L(A)`
    as follows :math:`AN = (Σ, S_N , S^0_N , ρ_N , F_N )` where:

     • :math:`S_N = 2^S`
     • :math:`S^0_N= \{\{s^0 \}\}`
     • :math:`F_N=2^F`
     • :math:`(Q,a,Q') ∈ ρ_N` iff :math:`Q'` satisfies :math:`⋀_{s∈Q} ρ(s, a)`

     We take an empty conjunction in the definition of :math:`ρ_N` to be equivalent to true; thus, :math:`(∅, a, ∅) ∈ ρ_N`.

    :param afw: dict() representing a afw
    :return: dict() representing a nfa
    """

    nfa = {
        'alphabet': copy.copy(afw['alphabet']),
        'initial_states': {afw['initial_state']},
        'states': copy.copy(afw['states']),
        'accepting_states': copy.copy(afw['accepting_states']),
        'transitions': {}
    }

    i = len(afw['states'])
    while i > 1:
        nfa['states'] = nfa['states'].union(set(itertools.combinations(afw['states'], i)))
        i -= 1

    for state in nfa['states']:
        accepting_state = True
        for s in state:
            if s not in afw['accepting_states']:
                accepting_state = False
                break
        if accepting_state:
            nfa['accepting_states'].add(state)

    for state in nfa['states']:
        # NAIVE
        for action in nfa['alphabet']:
            boolean_formula = 'True'
            for s in state:
                if (s, action) not in afw['transitions']:
                    boolean_formula += ' and False'
                else:
                    boolean_formula += ' and (' + afw['transitions'][s, action] + ')'

            mapping = dict.fromkeys(afw['states'], False)
            for evaluation in nfa['states']:
                for e in evaluation:
                    mapping[e] = True

                if eval(boolean_formula, mapping):
                    nfa['transitions'].setdefault((state, action), set()).add(evaluation)

                for e in evaluation:
                    mapping[e] = False

    return nfa


def __replace_all(repls, str):
    """ Replace from the string str all the occurrence of the keys element of the dictionary repls with their relative value.

    :param repls: dict(), dictionary containing the mapping between the values to be changed and their appropriate substitution
    :param str: str(), original string
    :return: str(), string with the appropriate values replaced
    """
    # return re.sub('|'.join(repls.keys()), lambda k: repls[k.group(0)], str)
    return re.sub('|'.join(re.escape(key) for key in repls.keys()), lambda k: repls[k.group(0)], str)


# TODO shouldn't an empty afw complementation result in an afw reading everything?
def afw_complementation(afw: dict) -> dict:
    """ returns a afw reading the complemented language read by input afw.

    Let :math:`A = (Σ, S, s^0 , ρ, F )`. Define :math:`Ā = (Σ, S, s^0 , \overline{ρ}, S − F )`,
    where :math:`\overline{ρ}(s, a) = \overline{ρ(s, a)}` for all :math:`s ∈ S` and :math:`a ∈ Σ`.
    That is, :math:`\overline{ρ}` is the dualized transition function. It can be shown that :math:`L( Ā) = Σ^∗ − L(A)`.

    The input afw need to be completed i.e. each non existing transition must be added pointing to False

    :param afw: dict() representing a afw
    :return: dict() representing a afw
    """
    completed_input = afw_completion(copy.deepcopy(afw))

    complemented_afw = {
        'alphabet': copy.copy(completed_input['alphabet']),
        'states': copy.copy(completed_input['states']),
        'initial_state': copy.copy(completed_input['initial_state']),
        'accepting_states': completed_input['states'].difference(afw['accepting_states']),
        'transitions': {}
    }

    conversion_dictionary = {'and': 'or', 'or': 'and', 'True': 'False', 'False': 'True'}
    for transition in completed_input['transitions']:
        complemented_afw['transitions'][transition] = __replace_all(conversion_dictionary,
                                                                    completed_input['transitions'][transition])
    return complemented_afw


# TODO states with the same name but from different afw should be considered as distinct state!
# TODO Documentation
def afw_union(afw_1: dict, afw_2: dict) -> dict:
    """ Returns a afw that reads the union of the languages read by input afws

    Let :math:`A_1 = (Σ, S_1 , s^0_1, ρ_1 , F_1 )` and :math:`A_2 = (Σ, S_2 , s^0_2, ρ_2 , F_2 )`
    be alternating automata accepting the languages :math:`L(A_1)` and :math:`L(A_2)`.
    Then, :math:`B_∪ = (Σ, S_1 ∪ S_2 ∪ {root}, ρ_∪ , root , F_1 ∪ F_2 )` with
    :math:`ρ_∪ = ρ_1 ∪ ρ_2 ∪ [(root, a): ρ(s^0_1 , a) ∨ ρ(s^0_2 , a)]` accepts :math:`L(A_1) ∪ L(A_2)`.

    :param afw_1: dict() representing a afw
    :param afw_2: dict() representing a afw
    :return: dict() representing a afw
    """
    # Reference Lecture6a Lemma 6
    union = {
        'alphabet': afw_1['alphabet'].union(afw_2['alphabet']),
        'states': afw_1['states'].union(afw_2['states']).union({'s_root'}),
        'initial_state': 's_root',
        'accepting_states': afw_1['accepting_states'].union(afw_2['accepting_states']),
        'transitions': afw_1['transitions'].copy()
    }

    if afw_1['initial_state'] in afw_1['accepting_states'] or afw_2['initial_state'] in afw_2['accepting_states']:
        union['accepting_states'].add(union['initial_state'])

    for transition in afw_2['transitions']:
        if transition in union['transitions']:
            union['transitions'][transition] += ' or (' + afw_2['transitions'][transition] + ')'
        else:
            union['transitions'][transition] = '(' + afw_2['transitions'][transition] + ')'

    for action in union['alphabet']:
        if (afw_1['initial_state'], action) in afw_1['transitions']:
            union['transitions']['s_root', action] = '(' + afw_1['transitions'][afw_1['initial_state'], action] + ')'
            if (afw_2['initial_state'], action) in afw_2['transitions']:
                union['transitions']['s_root', action] += ' or (' + afw_2['transitions'][
                    afw_2['initial_state'], action] + ')'
        elif (afw_2['initial_state'], action) in afw_2['transitions']:
            union['transitions']['s_root', action] = '(' + afw_2['transitions'][afw_2['initial_state'], action] + ')'

    return union


# - AFW Intersection
# unsure on correctness of the source material [lecture06a.pdf lemma 6]
# TODO check equality between AFWs alphabets
def afw_intersection(afw_1: dict, afw_2: dict) -> dict:
    """ Returns a afw that reads the intersection of the languages read by input afws.


    Let :math:`A_1 = (Σ, S_1 , s^0_1, ρ_1 , F_1 )` and :math:`A_2 = (Σ, S_2 , s^0_2, ρ_2 , F_2 )`
    be alternating automata accepting the languages :math:`L(A_1)` and :math:`L(A_2)`.
    Then, :math:`B_∩ = (Σ, S_1 ∪ S_2 ∪ {root}, root, ρ_∩ , F_1 ∪ F_2 )` with
    :math:`ρ_∩ = ρ_1 ∪ ρ_2 ∪ [(root, a): ρ(s^0_1 , a) ∧ ρ(s^0_2 , a)]` accepts :math:`L(A_1) ∩ L(A_2)`.


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
