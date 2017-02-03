"""
Formally a NFA, Nondeterministic Finite Automaton, is a tuple (Σ, S, S^0 , ρ, F ), where
 • Σ is a finite nonempty alphabet;
 • S is a finite nonempty set of states;
 • S^0 is the nonempty set of initial states;
 • F is the set of accepting states;
 • ρ: S × Σ × S is a transition relation. Intuitively, (s, a, s' ) ∈ ρ states that A can move from s into s' when it reads the symbol a. It is allowed that (s, a, s' ) ∈ ρ and (s, a, s'' ) ∈ ρ with S' != S'' .

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
# TODO Handle Side effects

def nfa_intersection(nfa_1: dict, nfa_2: dict) -> dict:
    """ Returns a NFA that reads the intersection of the of the NFAs in input.

    Let A 1 = (Σ,S_1,S_1^0,ρ_1,F_1) and A 2 =(Σ,S_2,S_2^0,ρ_2,F_2) be two NFAs.
    There is a NFA A_∧ that runs simultaneously both A_1 and A_2 on the input word, so L(A_∧) = L(A_1)∩L(A_2).
    It is defined as:

    A_∧ = ( Σ , S , S_0 , ρ , F )

    where

    • S = S_1 × S_2
    • S_0 = S_1^0 × S_2^0
    • F = F_1 × F_2
    • ((s,t), a, (s_X , t_X)) ∈ ρ iff (s, a, s_X ) ∈ ρ_1 and (t, a, t_X ) ∈ ρ_2

    :param nfa_1: dict() representing a nfa
    :param nfa_2: dict() representing a nfa
    :return: dict() representing the intersected nfa
    """
    intersection = {
        'alphabet': nfa_1['alphabet'].intersection(nfa_2['alphabet']),
        'states': set(cartesian_product(nfa_1['states'], nfa_2['states'])),
        'initial_states': set(cartesian_product(nfa_1['initial_states'], nfa_2['initial_states'])),
        'accepting_states': set(cartesian_product(nfa_1['accepting_states'], nfa_2['accepting_states'])),
        'transitions': dict()
    }

    for (state_nfa_1, state_nfa_2) in intersection['states']:
        for a in intersection['alphabet']:
            if (state_nfa_1, a) not in nfa_1['transitions'] or (state_nfa_2, a) not in nfa_2['transitions']:
                continue
            s1 = nfa_1['transitions'][state_nfa_1, a]
            s2 = nfa_2['transitions'][state_nfa_2, a]

            for destination_1 in s1:
                for destination_2 in s2:
                    intersection['transitions'].setdefault(((state_nfa_1, state_nfa_2), a), set()).add(
                        (destination_1, destination_2))

    return intersection


def nfa_union(nfa_1: dict, nfa_2: dict) -> dict:
    """ Returns a NFA that reads the union of the NFAs in input.

    Let A 1 = (Σ,S_1,S_1^0,ρ_1,F_1) and A 2 =(Σ,S_2,S_2^0,ρ_2,F_2) be two NFAs.
    There is a NFA A_∨ that nondeterministically chooses A_1 or A_2 and runs it on the input word.
    It is defined as:

    A_∨ = (Σ, S, S_0 , ρ, F )

    where:

    • S = S_1 ∪ S_2
    • S_0 = S_1^0 ∪ S_2^0
    • F = F_1 ∪ F_2
    • ρ = ρ_1 ∪ ρ_2 , that is (s, a, s' ) ∈ ρ if [ s ∈ S_1 and (s, a, s' ) ∈ ρ_1 ] OR [ s ∈ S_2 and (s, a, s' ) ∈ ρ_2 ]

    :param nfa_1: dict() representing a nfa
    :param nfa_2: dict() representing a nfa
    :return: dict() representing a united nfa
    """
    union = {
        'alphabet': nfa_1['alphabet'].union(nfa_2['alphabet']),
        'states': nfa_1['states'].union(nfa_2['states']),
        'initial_states': nfa_1['initial_states'].union(nfa_2['initial_states']),
        'accepting_states': nfa_1['accepting_states'].union(nfa_2['accepting_states']),
        'transitions': nfa_1['transitions'].copy()}

    for transition in nfa_2['transitions']:
        for elem in nfa_2['transitions'][transition]:
            union['transitions'].setdefault(transition, set()).add(elem)

    return union


# NFA to DFA
def nfa_determinization(nfa: dict) -> dict:
    """ Returns a dfa that reads the same language of the input nfa.

    Let A be an NFA, then there exists a DFA A_d such that L(A_d) = L(A). Intuitively, A d collapses all possible runs
    of A on a given input word into one run over a larger state set.
    A_d is defined as:

    A_d = (Σ, 2^S , s_0 , ρ_d , F_d )

    where:

    • 2^S , i.e., the state set of A_d , consists of all sets of states S in A;
    • s_0 = S^0 , i.e., the single initial state of A_d is the set S_0 of initial states of A;
    • F_d = {Q | Q ∩ F != ∅}, i.e., the collection of sets of states that intersect F nontrivially;
    • ρ_d(Q, a) = {s' | (s, a, s' ) ∈ ρ for some s ∈ Q}.

    :param nfa: dict() representing a nfa
    :return: dict() representing a dfa
    """
    dfa = {
        'alphabet': nfa['alphabet'],
        'initial_state': None,
        'states': set(),
        'accepting_states': set(),
        'transitions': dict()
    }

    if len(nfa['initial_states']) > 0:
        dfa['initial_state'] = str(nfa['initial_states'])
        dfa['states'].add(str(nfa['initial_states']))

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

    Complement a nondeterministic automaton is possible complementing the determinization of it.
    The construction is effective, but it involves an exponential blow-up,
    since determinization involves an unavoidable exponential blow-up
    (i.e., if NFA has n states, then the DFA has 2^n states).

    :param nfa: dict() representing a nfa
    :return: dict() representing a dfa
    """
    determinized_nfa = nfa_determinization(nfa)
    return DFA.dfa_complementation(determinized_nfa)


def nfa_nonemptiness_check(nfa: dict) -> dict:
    """ Checks if the input nfa reads any language other than the empty one, returning True/False.

    The language L(A) recognized by the automaton A is nonempty iff
    there are states s ∈ S_0 and t ∈ F such that t is connected to s.
    Thus, automata nonemptiness is equivalent to graph reachability.

    A breadth-first-search algorithm can construct in linear time
    the set of all states connected to a state in S_0. A is nonempty iff this set intersects F nontrivially.

    :param nfa: dict() representing a nfa
    :return: bool, True if the input nfa is nonempty, False otherwise
    """
    # BFS
    stack = []
    visited = set()
    for state in nfa['initial_states']:
        visited.add(state)
        stack.insert(0, state)
    while stack:
        state = stack.pop()
        visited.add(state)
        for a in nfa['alphabet']:
            if (state, a) in nfa['transitions']:
                for next_state in nfa['transitions'][state, a]:
                    if next_state in nfa['accepting_states']:
                        return True
                    if next_state not in visited:
                        stack.insert(0, next_state)
    return False


def nfa_nonuniversality_check(nfa: dict) -> bool:
    """ Checks if the language read by the input nfa is different from Σ∗ (i.e. contains all possible words), returning True/False.

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
