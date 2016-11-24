"""
Formally a DFA, Deterministic Finite Automaton, is a tuple A=(Σ,S,s_0,ρ,F), where
 • Σ is a finite nonempty alphabet;
 • S is a finite nonempty set of states;
 • s_0 ∈ S is the initial state;
 • F ⊆ S is the set of accepting states;
 • ρ: S × Σ → S is a transition function, which can be a partial function.
    Intuitively, s_0 = ρ(s, a) is the state that A can move into when it is in state s and it reads the symbol a. (If ρ(s, a) is undefined then reading a leads to rejection.)

In this module a DFA is defined as follows

 DFA = dict() with the following keys-values:
  • alphabet         => set() ;
  • states           => set() ;
  • initial_state    => 'state_0' ;
  • accepting_states => set() ;
  • transitions      => dict()  #key (state in states, action in alphabet) #value (arriving state in states) ;
"""

from itertools import product as cartesian_product
from copy import deepcopy
from copy import copy


# ###
# MEMO
# handle side-effects through input instead of manual handling in function:
#    pass as value of function a copy, not the data link
# copy() copy just the first level (a set in a dict remains a reference) so can lead to side effects,
#   use deepcopy for dict() objects [look dfa_projection() and try to substitute deepcopy with copy]


# ###
# TO-DO
# TODO handle side effects
# TODO lambda functions


def run_acceptance(dfa: dict, run: list, word: list) -> bool:
    """ Checks if the given 'run' of states in 'dfa' accepts the given 'word', returning True/False.

    A run r of DFA on a finite word w = a_0 · · · a_n−1 ∈ Σ∗ is a sequence s_0 · · · s_n of n+1 states in S
    such that s_0 = s_0 , and s_i+1 = ρ(s_i , a_i ) for 0 ≤ i ≤ n. Note that a deterministic automaton
    can have at most one run on a given input word. The run r is accepting if s_n ∈ F .

    :param dfa: dict() representing a dfa
    :param run: list() of states ∈ dfa['states']
    :param word: list() of actions ∈ dfa['alphabet']
    :return: bool, True if the word is accepted, False in the other case
    """

    if len(run) > 0:
        # If 'run' fist state is not an initial state return False
        if run[0] != dfa['initial_state']:
            return False
        # If last 'run' state is not an accepting state return False
        if run[-1] not in dfa['accepting_states']:
            return False
    else:
        # If empty input check if the initial state is also accepting
        if dfa['initial_state'] in dfa['accepting_states']:
            return True
        else:
            return False
    if len(word) != len(run) - 1:
        return False

    for i in range(len(word)):
        if (run[i], word[i]) in dfa['transitions']:
            if dfa['transitions'][run[i], word[i]] != run[i + 1]:
                return False
        else:
            return False
    return True


def word_acceptance(dfa: dict, word: list) -> bool:
    """ Checks if a given 'word' is accepted by a 'dfa', returning True/false.

    The word w is accepted by a DFA if DFA has an accepting run on w. Since A is deterministic, w ∈ L(A) if and only if ρ(s 0 , w) ∈ F .

    :param dfa: dict() representing a dfa
    :param word: list() of actions ∈ dfa['alphabet']
    :return: bool, True if the word is accepted, False in the other case
    """
    current_state = dfa['initial_state']
    for action in word:
        if (current_state, action) in dfa['transitions']:
            current_state = dfa['transitions'][current_state, action]
        else:
            return False
    if current_state in dfa['accepting_states']:
        return True
    else:
        return False


# Side effect on input dfa
def dfa_completion(dfa: dict) -> dict:
    """ [Side effect on input] It completes the dfa assigning to each state a transition for each letter in the alphabet (if not already defined).

    We say that a DFA is complete if its transition function ρ:S×Σ→S is a total function,
    that is, for all s ∈ S and all a ∈ Σ we have that exists a ρ(s,a)=s_x for some s_x ∈ S.
    Given an arbitrary DFA A, its completed version A_T is obtained as follows:
    A_T = (Σ, S ∪ {sink}, s_0 , ρ_T , F ) with ρ_T(s,a)=sink when ρ(s,a) is not defined in A and ρ_T=ρ in the other cases.

    :param dfa: dict() representing a dfa
    :return: dict() representing the completed dfa
    """
    dfa['states'].add('sink')
    for s in dfa['states']:
        for a in dfa['alphabet']:
            if (s, a) not in dfa['transitions']:
                dfa['transitions'][s, a] = 'sink'
    return dfa


def dfa_complementation(dfa: dict) -> dict:
    """ Generates a dfa that accepts any word but he one accepted by input 'dfa'.

    Let A be a completed DFA, Ā = (Σ, S, s_0 , ρ, S − F ) is the DFA that runs A but accepts whatever word A does not.

    :param dfa: dict() representing a dfa
    :return: dict() representing the complement of the input dfa
    """
    dfa_complemented = deepcopy(dfa_completion(dfa))
    dfa_complemented['accepting_states'] = dfa['states'].difference(dfa['accepting_states'])
    return dfa_complemented


def dfa_intersection(dfa_1: dict, dfa_2: dict) -> dict:
    """ Returns a dfa accepting the intersection of the dfas in input.

    Let A_1 = (Σ, S_1 , s_01 , ρ_1 , F_1 ) and A_2 = (Σ, S_2 , s_02 , ρ_2 , F_2 ) be two DFAs.
    Then there is a DFA A_∧ that runs simultaneously both A_1 and A_2 on the input word and accepts when both accept.
    It is defined as:

    A_∧ = (Σ, S_1 × S_2 , (s_01 , s_02 ), ρ, F_1 × F_2 )

    where

    ρ((s_1 , s_2 ), a) = (s_X1 , s_X2 ) iff s_X1 = ρ_1 (s_1 , a) and s_X2 = ρ_2 (s_2 , a)

    :param dfa_1: dict() representing a dfa
    :param dfa_2: dict() representing a dfa
    :return: dict() representing the intersected dfa
    """
    intersection = {
        'alphabet': copy(dfa_1['alphabet']),
        'states': set(cartesian_product(dfa_1['states'], dfa_2['states'])),
        'initial_state': (dfa_1['initial_state'], dfa_2['initial_state']),
        'accepting_states': set(cartesian_product(dfa_1['accepting_states'], dfa_2['accepting_states'])),
        'transitions': dict()
    }

    for s in intersection['states']:
        for a in intersection['alphabet']:
            if (s[0], a) in dfa_1['transitions'] and (s[1], a) in dfa_2['transitions']:
                s1 = dfa_1['transitions'][s[0], a]
                s2 = dfa_2['transitions'][s[1], a]
                intersection['transitions'][s, a] = (s1, s2)
            else:
                continue
    return intersection


def dfa_union(dfa_1: dict, dfa_2: dict) -> dict:
    """ Returns a dfa accepting the union of the dfas in input.

    Let A_1 = (Σ, S_1 , s_01 , ρ_1 , F_1 ) and A_2 = (Σ, S_2 , s_02 , ρ_2 , F_2 ) be two completed DFAs.
    Then there is a DFA A_∨ that runs simultaneously both A_1 and A_2 on the input word and accepts when one of them accepts.
    It is defined as:

    A_∨ = (Σ, S_1 × S_2 , (s_01 , s_02 ), ρ, (F_1 × S_2 ) ∪ (S_1 × F_2 ))

    where

    ρ((s_1 , s_2 ), a) = (s_X1 , s_X2 ) iff s_X1 = ρ_1 (s_1 , a) and s_X2 = ρ(s_2 , a)


    :param dfa_1: dict() representing a dfa
    :param dfa_2: dict() representing a dfa
    :return: dict() representing the united dfa
    """
    dfa_1 = dfa_completion(deepcopy(dfa_1))
    dfa_2 = dfa_completion(deepcopy(dfa_2))

    union = {
        'alphabet': dfa_1['alphabet'],
        'states': set(cartesian_product(dfa_1['states'], dfa_2['states'])),
        'initial_state': (dfa_1['initial_state'], dfa_2['initial_state']),
        'accepting_states': set(cartesian_product(dfa_1['accepting_states'], dfa_2['states'])).union(
            set(cartesian_product(dfa_1['states'], dfa_2['accepting_states']))),
        'transitions': {}
    }

    for s in union['states']:
        for a in union['alphabet']:
            s1 = dfa_1['transitions'][s[0], a]
            s2 = dfa_2['transitions'][s[1], a]
            union['transitions'][s, a] = (s1, s2)
    return union


def dfa_minimization(dfa: dict) -> dict:
    """ Returns the minimization of the dfa in input through a greatest fix-point method.

    Given a completed DFA A (Σ, S, s_0 , ρ, F ) there exists a single minimal DFA A_m which is equivalent to A,
    i.e. reads the same language L(A) = L(A_m) and with a minimal number of states.
    To construct such a DFA we exploit bisimulation as a suitable equivalence relation between states.

    A bisimulation relation E ∈ S × S is a relation between states that satisfies the following condition:
    if (s, t) ∈ E then:
    • s ∈ F iff t ∈ F;
    • For all s_X,a such that ρ(s, a) = s_X , there exists t_X such that ρ(t, a) = t_X and (s_X , t_X ) ∈ E;
    • For all t_X,a such that ρ(t, a) = t_X , there exists s_X such that ρ(s, a) = s_X and (s_X , t_X ) ∈ E.

    :param dfa: dict() representing a dfa
    :return: dict() representing the minimized dfa
    """
    dfa = dfa_completion(deepcopy(dfa))

    ##  Greatest-fixpoint

    # cartesian product of DFA states
    z_current = set(cartesian_product(dfa['states'], dfa['states']))

    z_next = z_current.copy()

    # First bisimulation condition check (can be done just once)
    # s ∈ F iff t ∈ F
    for element in z_current:
        if (element[0] in dfa['accepting_states'] and element[1] not in dfa['accepting_states']) or (
                        element[0] not in dfa['accepting_states'] and element[1] in dfa['accepting_states']):
            z_next.remove(element)
    z_current = z_next

    # Second and third condition of bisimularity check, while succeed or fail
    while z_current:
        z_next = z_current.copy()
        for element in z_current:
            # for all s0,a s.t. ρ(s, a) = s_0 , there exists t 0 s.t. ρ(t, a) = t 0 and (s_0 , t 0 ) ∈ Z i ;
            for a in dfa['alphabet']:
                if (element[0], a) in dfa['transitions'] and (element[1], a) in dfa['transitions']:
                    if (dfa['transitions'][element[0], a], dfa['transitions'][element[1], a]) not in z_current:
                        z_next.remove(element)
                        break
                else:
                    # action a not possible in state element[0] or element[1]
                    z_next.remove(element)

        if z_next == z_current:
            break
        z_current = z_next

    ## Equivalence Sets
    equivalence = {}
    for element in z_current:
        equivalence.setdefault(element[0], set()).add(element[1])

    ## Minimal DFA construction
    dfa_min = {}
    dfa_min['alphabet'] = dfa['alphabet'].copy()

    dfa_min['states'] = set()

    # select one element for each equivalence set
    for equivalence_set in equivalence.values():
        if dfa_min['states'].isdisjoint(equivalence_set):
            e = equivalence_set.pop()
            dfa_min['states'].add(e)
            equivalence_set.add(e)

    dfa_min['initial_state'] = dfa['initial_state']
    dfa_min['accepting_states'] = dfa_min['states'].intersection(dfa['accepting_states'])

    dfa_min['transitions'] = dfa['transitions'].copy()
    for p in dfa['transitions']:
        if p[0] not in dfa_min['states']:
            dfa_min['transitions'].pop(p)
        if dfa['transitions'][p] not in dfa_min['states']:
            dfa_min['transitions'][p] = equivalence[dfa['transitions'][p]].intersection(dfa_min['states']).pop()

    return dfa_min


# Side effects on input variable
def dfa_reachable(dfa: dict) -> dict:
    """ [Side effects on input] Removes unreachable states of a dfa and returns the pruned dfa.

    It is possible to remove from a DFA A all unreachable states from the initial state without altering the language.
    The reachable DFA A_R corresponding to A is defined as:

    A_R = (Σ, S_R , s_0 , ρ|S_R , F ∩ S_R )

    where

    • S_R set of reachable state from the initial one
    • ρ|S_R is the restriction on S_R × Σ of ρ.

    :param dfa: dict() representing a dfa
    :return: dict() representing the pruned dfa
    """
    reachable_states = set()  # set of reachable states from initial states
    reachable_states.add(dfa['initial_state'])
    reachable_state_stack = reachable_states.copy()
    while reachable_state_stack:
        s = reachable_state_stack.pop()
        for a in dfa['alphabet']:
            if (s, a) in dfa['transitions']:
                if dfa['transitions'][s, a] not in reachable_states:
                    reachable_state_stack.add(dfa['transitions'][s, a])
                    reachable_states.add(dfa['transitions'][s, a])
            else:
                pass
    dfa['states'] = reachable_states
    dfa['accepting_states'] = dfa['accepting_states'].intersection(dfa['states'])

    transitions = dfa['transitions'].copy()
    for p in transitions:
        if p[0] not in dfa['states']:
            dfa['transitions'].pop(p)
        elif dfa['transitions'][p] not in dfa['states']:
            dfa['transitions'].pop(p)

    return dfa


# Side effects on input variable
def dfa_co_reachable(dfa: dict) -> dict:
    """ [Side effects on input] Removes states that do not reach a final state and returns the pruned dfa.

    It is possible to remove from a DFA A all states that do not reach a final state without altering the language.
    The co-reachable dfa A_F corresponding to A is defined as:

    A_F = (Σ, S_F , s_0 , ρ|S_F , F )

    where

    • S_F is the set of states that reach a final state
    • ρ|S_F is the restriction on S_F × Σ of ρ.

    :param dfa: dict() representing a dfa
    :return: dict() representing the pruned dfa
    """
    co_reachable_states = dfa['accepting_states'].copy()  # set of states reaching final states
    co_reachable_states_stack = co_reachable_states.copy()

    # inverse transition function
    inverse_transitions = {}
    for k, v in dfa['transitions'].items():
        inverse_transitions.setdefault(v, set()).add(k)

    while co_reachable_states_stack:
        s = co_reachable_states_stack.pop()
        if s in inverse_transitions:
            for s_app in inverse_transitions[s]:
                if s_app[0] not in co_reachable_states:
                    co_reachable_states_stack.add(s_app[0])
                    co_reachable_states.add(s_app[0])

    dfa['states'] = co_reachable_states

    # If not s_0 ∈ S_F the resulting dfa is empty
    if dfa['initial_state'] not in dfa['states']:
        return {
            'alphabet': set(),
            'states': set(),
            'initial_state': None,
            'accepting_states': set(),
            'transitions': dict()
        }

    transitions = dfa['transitions'].copy()
    for p in transitions:
        if p[0] not in dfa['states']:
            dfa['transitions'].pop(p)
        elif dfa['transitions'][p] not in dfa['states']:
            dfa['transitions'].pop(p)

    return dfa


# Side effects on input variable
def dfa_trimming(dfa: dict) -> dict:
    """ [Side effects on input] Returns the dfa in input trimmed, so both reachable and co-reachable.

    Given a DFA A, the corresponding trimmed DFA contains only those states that are reachable from the initial state
    and that lead to a final state.
    The trimmed dfa A_RF corresponding to A is defined as

    A_RF = (Σ, S_R ∩ S_F , s_0 , ρ|S_R∩S_F , F ∩ S_R )

    where

    • S_R set of reachable states from the initial state
    • S_F set of states that reaches a final state
    • ρ|S_R∩S_F is the restriction on (S_R ∩ S_F ) × Σ of ρ.

    :param dfa: dict() representing a dfa
    :return: dict() representing the trimmed input dfa
    """
    # Reachable DFA
    dfa = dfa_reachable(dfa)
    # Co-reachable DFA
    dfa = dfa_co_reachable(dfa)
    # trimmed DFA
    return dfa


def dfa_projection(dfa: dict, symbols_to_project: set) -> dict:
    """ Returns a NFA that reads the language recognized by the input dfa where all the symbols in X are projected out.

    Projection in a dfa is the operation that existentially removes from a word all occurrence of symbols in X )
    Given a dfa A = (Σ, S, s 0 , ρ, F ), we can define an nfa A π X that recognizes the language π X (L(A)).

    :param dfa: dict() representing a dfa
    :param symbols_to_project: set() containing symbols ∈ dfa['alphabet'] to be projected out from dfa
    :return: dict() representing a NFA
    """
    nfa = dfa.copy()
    nfa['alphabet'] = dfa['alphabet'].difference(symbols_to_project)
    nfa['transitions'] = {}
    # ε_X ⊆ S×S formed by the pairs of states (s, s_0) such that s_0 is reachable from s through transition symbols ∈ X
    e_x = {}

    # mark each transition using symbol a ∈ symbols_to_project
    for transition in dfa['transitions']:
        if transition[1] not in nfa['alphabet']:
            # nfa['transitions'][transition[0], 'epsilon'] = dfa['transitions'][transition]
            e_x.setdefault(transition[0], set()).add(dfa['transitions'][transition])
            # nfa['transitions'].pop(transition)
        else:
            nfa['transitions'].setdefault(transition, set()).add(dfa['transitions'][transition])

    current = deepcopy(e_x)
    while True:
        for state in current.keys():
            for direct in current[state]:
                if direct in current:
                    for reached in current[direct]:
                        e_x[state].add(reached)
        if current == e_x:
            break
        current = deepcopy(e_x)

    # NFA initial states
    nfa.pop('initial_state')
    nfa['initial_states'] = e_x[dfa['initial_state']]
    nfa['initial_states'].add(dfa['initial_state'])

    # inverse transition function
    inv_e_x = {}
    for k, v in e_x.items():
        for s in v:
            inv_e_x.setdefault(s, set()).add(k)

    # NFA transitions
    for transition in dfa['transitions']:
        if transition[1] in nfa['alphabet']:
            nfa['transitions'].setdefault(transition, set()).add(dfa['transitions'][transition])

            # add all forward reachable set
            if dfa['transitions'][transition] in e_x:
                for reached in e_x[dfa['transitions'][transition]]:
                    nfa['transitions'].setdefault(transition, set()).add(reached)

            # link all states that reach transition[0] to forward reachable set
            for reached in nfa['transitions'][transition]:
                if transition[0] in inv_e_x:
                    for past in inv_e_x[transition[0]]:
                        nfa['transitions'].setdefault((past, transition[1]), set()).add(reached)

    return nfa


def dfa_nonemptiness_check(dfa: dict) -> bool:
    """ Checks if the input dfa is nonempty, so if it recognize at least a language except the empty one

    :param dfa: dict() representing a dfa
    :return: bool, True if the dfa is nonempty, False in the other case
    """
    # BFS
    stack = [dfa['initial_state']]
    visited = set()
    visited.add(dfa['initial_state'])
    while stack:
        state = stack.pop()  # TODO tweak popping order (now the last element is chosen)
        for a in dfa['alphabet']:
            if (state, a) in dfa['transitions']:
                if dfa['transitions'][state, a] in dfa['accepting_states']:
                    return True
                if dfa['transitions'][state, a] not in visited:
                    stack.append(dfa['transitions'][state, a])
    return False
