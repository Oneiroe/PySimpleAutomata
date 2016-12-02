"""
Formally a NFA, Nondeterministic Finite Automaton, is a tuple (Σ, S, S^0 , ρ, F ), where
 • Σ is a finite nonempty alphabet;
 • S is a finite nonempty set of states;
 • S^0 is the nonempty set of initial states;
 • F is the set of accepting states;
 • ρ : S × Σ × S is a transition relation. Intuitively, (s, a, s' ) ∈ ρ states that A can
       move from s into s' when it reads the symbol a. It is allowed that (s, a, s' ) ∈ ρ and
       (s, a, s'' ) ∈ ρ with S' != S'' .

In this module a NFA is defined as follows

 NFA = dict() with the following keys-values:
  • alphabet         => set()
  • states           => set()
  • initial_states   => set()
  • accepting_states => set()
  • transitions      => dict()  # key (state in states, action in alphabet) value {set of arriving states in states}
"""

from itertools import product as cartesian_product
import DFA
from copy import deepcopy
from copy import copy


# ###
# TO-DO
#

def nfa_intersection(nfa_1: dict, nfa_2: dict) -> dict:
    """ Returns a nfa that reads the intersection of the languages read by nfa_1 and nfa_2.

    TODO short-detailed explanation of NFAs intersection

    :param nfa_1: dict() representing a nfa
    :param nfa_2: dict() representing a nfa
    :return: dict() representing the intersected nfa
    """
    intersection = {
        'alphabet': nfa_1['alphabet'],
        'states': set(cartesian_product(nfa_1['states'], nfa_2['states'])),
        'initial_states': set(cartesian_product(nfa_1['initial_states'], nfa_2['initial_states'])),
        'accepting_states': set(cartesian_product(nfa_1['accepting_states'], nfa_2['accepting_states'])),
        'transitions': {}
    }

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


def nfa_union(nfa_1: dict, nfa_2: dict) -> dict:
    """ Returns a nfa that reads union of the languages read by nfa_1 and nfa_2.

    TODO short-detailed explanation of NFAs union

    :param nfa_1: dict() representing a nfa
    :param nfa_2: dict() representing a nfa
    :return: dict() representing a united nfa
    """
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


# NFA to DFA
# 	TODO check correctness more deeply
def nfa_determinization(nfa: dict) -> dict:
    """ Returns a dfa that reads the same language of the input nfa.

    TODO short-detailed explanation of NFAs determinization

    :param nfa: dict() representing a nfa
    :return: dict() representing a dfa
    """
    dfa = {}
    dfa['alphabet'] = nfa['alphabet']
    dfa['initial_state'] = str(nfa['initial_states'])
    dfa['states'] = set()
    dfa['states'].add(str(nfa['initial_states']))
    dfa['accepting_states'] = set()
    dfa['transitions'] = {}

    states = list()
    stack = list()
    stack.append(nfa['initial_states'])
    states.append(nfa['initial_states'])
    if len(states[0].intersection(nfa['accepting_states'])) > 0:
        dfa['accepting_states'].add(str(states[0]))
    while stack:
        current_set = stack.pop(0)
        for a in dfa['alphabet']:
            next_set = set()
            for state in current_set:
                if (state, a) in nfa['transitions']:
                    for next_state in nfa['transitions'][state, a]:
                        next_set.add(next_state)
            if len(next_set) == 0:
                continue
            if next_set not in states:
                states.append(next_set)
                stack.append(next_set)
                dfa['states'].add(str(next_set))
                if len(next_set.intersection(nfa['accepting_states'])) > 0:
                    dfa['accepting_states'].add(str(next_set))

            dfa['transitions'][str(current_set), a] = str(next_set)

    return dfa


def nfa_complementation(nfa: dict) -> dict:
    """ Returns a dfa reading the complemented language read by input nfa.

    TODO short-detailed explanation of NFAs complementation

    :param nfa: dict() representing a nfa
    :return: dict() representing a dfa
    """
    determinized_nfa = nfa_determinization(nfa)
    return DFA.dfa_complementation(determinized_nfa)


def nfa_nonemptiness_check(nfa: dict) -> dict:
    """ Checks if the input nfa reads any language other than the empty one, returning True/False.

    TODO short-detailed explanation of NFAs nonemptiness

    :param nfa: dict() representing a nfa
    :return: bool, True if the input nfa is nonempty, False otherwise
    """
    # BFS
    stack = []
    visited = set()
    for state in nfa['initial_states']:
        visited.add(state)
        stack.append(state)
    while stack:
        state = stack.pop()  # TODO tweak popping order (now the last element is chosen)
        for a in nfa['alphabet']:
            if (state, a) in nfa['transitions']:
                for next_state in nfa['transitions'][state, a]:
                    if next_state in nfa['accepting_states']:
                        return True
                    if next_state not in visited:
                        stack.append(next_state)
    return False


def nfa_nonuniversality_check(nfa: dict) -> bool:
    """ Checks if the language read by the input nfa is different from Σ∗, returning True/False.

    To test nfa A for nonuniversality, it suffices to test Ā (complementary automaton of A) for nonemptiness

    :param nfa: dict() representing a nfa
    :return: bool, True if input nfa is nonuniversal, False otherwise
    """
    # NAIVE Very inefficient (exponential space) : simply construct Ā and then test it for nonemptiness
    complemented_nfa = nfa_complementation(nfa)
    return DFA.dfa_nonemptiness_check(complemented_nfa)

    # TODO CORRECT:
    # construct Ā “on-the-fly”: whenever the nonemptiness algorithm wants to move from a state t 1 of Ā to a state t 2,
    # the algorithm guesses t 2 and checks that it is directly connected to t 1 . Once this has been verified,
    # the algorithm can discard t 1 .


def nfa_interestingness_check(nfa: dict) -> bool:
    """ Checks if the input nfa is interesting, returning True/False.

    TODO short-detailed explanation of NFAs interestingness

    :param nfa: dict() representing a nfa
    :return: bool, True if the input nfa is interesting, False otherwise
    """
    return nfa_nonemptiness_check(nfa) and nfa_nonuniversality_check(nfa)


def run_acceptance(nfa: dict, run: list, word: list) -> bool:
    """ Checks if a given 'run' on a 'nfa' accepts a given input 'word'

    TODO short-detailed explanation of NFAs run acceptance

    :param nfa: dict() representing a nfa
    :param run: list() of states ∈ nfa['states']
    :param word: list() of symbols ∈ nfa['alphabet']
    :return: bool, True if the run is accepted, False otherwise
    """
    # If 'run' fist state is not an initial state return False
    if run[0] not in nfa['initial_states']:
        return False
    # If last 'run' state is not an accepting state return False
    if run[-1] not in nfa['accepting_states']:
        return False
    current_level = set()
    current_level.add(run[0])
    for i in range(len(word) - 1):
        if (run[i], word[i]) in nfa['transitions']:
            if run[i + 1] not in nfa['transitions'][run[i], word[i]]:
                return False
        else:
            return False
    return True


def word_acceptance(nfa: dict, word: list) -> bool:
    """ Checks if a given word is accepted by a NFA

    TODO short-detailed explanation of NFAs word acceptance

    :param nfa: dict() representing a nfa
    :param word: list() of symbols ∈ nfa['alphabet']
    :return: bool, True if the word is accepted, False otherwise
    """
    current_level = set()
    current_level = current_level.union(nfa['initial_states'])
    next_level = set()
    for action in word:
        for state in current_level:
            if (state, action) in nfa['transitions']:
                next_level = next_level.union(nfa['transitions'][state, action])
        if len(next_level) < 1:
            return False
        current_level = next_level
        next_level = set()

    if current_level.intersection(nfa['accepting_states']):
        return True
    else:
        return False
