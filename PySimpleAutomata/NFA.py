"""
Module to manage NFA (Nondeterministic Finite Automata).

Formally a NFA, Nondeterministic Finite Automaton, is a tuple
:math:`(Σ, S, S^0 , ρ, F )`, where

 • Σ is a finite nonempty alphabet;
 • S is a finite nonempty set of states;
 • :math:`S^0` is the nonempty set of initial states;
 • F is the set of accepting states;
 • :math:`ρ: S × Σ × S` is a transition relation. Intuitively,
   :math:`(s, a, s' ) ∈ ρ` states that A can move from s
   into s' when it reads the symbol a. It is allowed that
   :math:`(s, a, s' ) ∈ ρ` and :math:`(s, a, s'' ) ∈ ρ`
   with :math:`S' ≠ S''` .

In this module a NFA is defined as follows

 NFA = dict() with the following keys-values:

  • alphabet         => set() ;
  • states           => set() ;
  • initial_states   => set() ;
  • accepting_states => set() ;
  • transitions      => dict(), where
        **key**: (state in states, action in alphabet)

        **value**: {set of arriving states in states}.

"""

from itertools import product as cartesian_product
from PySimpleAutomata import DFA
from copy import copy


def nfa_intersection(nfa_1: dict, nfa_2: dict) -> dict:
    """ Returns a NFA that reads the intersection of the NFAs in
    input.

    Let :math:`A_1 = (Σ,S_1,S_1^0,ρ_1,F_1)` and :math:`A_2 =(Σ,
    S_2,S_2^0,ρ_2,F_2)` be two NFAs.
    There is a NFA :math:`A_∧` that runs simultaneously both
    :math:`A_1` and :math:`A_2` on the input word,
    so :math:`L(A_∧) = L(A_1)∩L(A_2)`.
    It is defined as:

    :math:`A_∧ = ( Σ , S , S_0 , ρ , F )`

    where

    • :math:`S = S_1 × S_2`
    • :math:`S_0 = S_1^0 × S_2^0`
    • :math:`F = F_1 × F_2`
    • :math:`((s,t), a, (s_X , t_X)) ∈ ρ` iff :math:`(s, a,s_X )
      ∈ ρ_1` and :math:`(t, a, t_X ) ∈ ρ_2`

    :param dict nfa_1: first input NFA;
    :param dict nfa_2: second input NFA;
    :return: *(dict)* representing the intersected NFA.
    """
    intersection = {
        'alphabet': nfa_1['alphabet'].intersection(nfa_2['alphabet']),
        'states': set(cartesian_product(nfa_1['states'], nfa_2['states'])),
        'initial_states': set(cartesian_product(nfa_1['initial_states'],
                                                nfa_2['initial_states'])),
        'accepting_states': set(cartesian_product(nfa_1['accepting_states'],
                                                  nfa_2['accepting_states'])),
        'transitions': dict()
    }

    for (state_nfa_1, state_nfa_2) in intersection['states']:
        for a in intersection['alphabet']:
            if (state_nfa_1, a) not in nfa_1['transitions'] \
                    or (state_nfa_2, a) not in nfa_2['transitions']:
                continue
            s1 = nfa_1['transitions'][state_nfa_1, a]
            s2 = nfa_2['transitions'][state_nfa_2, a]

            for destination_1 in s1:
                for destination_2 in s2:
                    intersection['transitions'].setdefault(
                        ((state_nfa_1, state_nfa_2), a), set()).add(
                        (destination_1, destination_2))

    return intersection


def nfa_union(nfa_1: dict, nfa_2: dict) -> dict:
    """ Returns a NFA that reads the union of the NFAs in input.

    Let :math:`A_1 = (Σ,S_1,S_1^0,ρ_1,F_1)` and :math:`A_2 =(Σ,
    S_2,S_2^0,ρ_2,F_2)` be two NFAs. here is a NFA
    :math:`A_∨` that nondeterministically chooses :math:`A_1` or
    :math:`A_2` and runs it on the input word.
    It is defined as:

    :math:`A_∨ = (Σ, S, S_0 , ρ, F )`

    where:

    • :math:`S = S_1 ∪ S_2`
    • :math:`S_0 = S_1^0 ∪ S_2^0`
    • :math:`F = F_1 ∪ F_2`
    • :math:`ρ = ρ_1 ∪ ρ_2` , that is :math:`(s, a, s' ) ∈ ρ` if
      :math:`[ s ∈ S_1\ and\ (s, a, s' ) ∈ ρ_1 ]` OR :math:`[ s ∈
      S_2\ and\ (s, a, s' ) ∈ ρ_2 ]`

    Pay attention to avoid having the NFAs with state names in common, in case
    use :mod:`PySimpleAutomata.NFA.rename_nfa_states` function.

    :param dict nfa_1: first input NFA;
    :param dict nfa_2: second input NFA.
    :return: *(dict)* representing the united NFA.
    """
    union = {
        'alphabet': nfa_1['alphabet'].union(nfa_2['alphabet']),
        'states': nfa_1['states'].union(nfa_2['states']),
        'initial_states':
            nfa_1['initial_states'].union(nfa_2['initial_states']),
        'accepting_states':
            nfa_1['accepting_states'].union(nfa_2['accepting_states']),
        'transitions': nfa_1['transitions'].copy()}

    for trans in nfa_2['transitions']:
        for elem in nfa_2['transitions'][trans]:
            union['transitions'].setdefault(trans, set()).add(elem)

    return union


# NFA to DFA
def nfa_determinization(nfa: dict) -> dict:
    """ Returns a DFA that reads the same language of the input NFA.

    Let A be an NFA, then there exists a DFA :math:`A_d` such
    that :math:`L(A_d) = L(A)`. Intuitively, :math:`A_d`
    collapses all possible runs of A on a given input word into
    one run over a larger state set.
    :math:`A_d` is defined as:

    :math:`A_d = (Σ, 2^S , s_0 , ρ_d , F_d )`

    where:

    • :math:`2^S` , i.e., the state set of :math:`A_d` , consists
      of all sets of states S in A;
    • :math:`s_0 = S^0` , i.e., the single initial state of
      :math:`A_d` is the set :math:`S_0` of initial states of A;
    • :math:`F_d = \{Q | Q ∩ F ≠ ∅\}`, i.e., the collection of
      sets of states that intersect F nontrivially;
    • :math:`ρ_d(Q, a) = \{s' | (s,a, s' ) ∈ ρ\ for\ some\ s ∈ Q\}`.

    :param dict nfa: input NFA.
    :return: *(dict)* representing a DFA
    """
    dfa = {
        'alphabet': copy(nfa['alphabet']),
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
    """ Returns a DFA reading the complemented language read by
    input NFA.

    Complement a nondeterministic automaton is possible
    complementing the determinization of it.
    The construction is effective, but it involves an exponential
    blow-up, since determinization involves an unavoidable
    exponential blow-up (i.e., if NFA has n states,
    then the DFA has :math:`2^n` states).

    :param dict nfa: input NFA.
    :return: *(dict)* representing a completed DFA.
    """
    determinized_nfa = nfa_determinization(nfa)
    return DFA.dfa_complementation(determinized_nfa)


def nfa_nonemptiness_check(nfa: dict) -> bool:
    """ Checks if the input NFA reads any language other than the
    empty one, returning True/False.

    The language L(A) recognized by the automaton A is nonempty iff
    there are states :math:`s ∈ S_0` and :math:`t ∈ F` such that
    t is connected to s.
    Thus, automata nonemptiness is equivalent to graph reachability.

    A breadth-first-search algorithm can construct in linear time
    the set of all states connected to a state in :math:`S_0`. A
    is nonempty iff this set intersects F nontrivially.

    :param dict nfa: input NFA.
    :return: *(bool)*, True if the input nfa is nonempty, False
             otherwise.
    """
    # BFS
    stack = list()
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
    """ Checks if the language read by the input NFA is different
    from Σ∗ (i.e. contains all possible words), returning
    True/False.

    To test nfa A for nonuniversality, it suffices to test Ā (
    complementary automaton of A) for nonemptiness

    :param dict nfa: input NFA.
    :return: *(bool)*, True if input nfa is nonuniversal,
             False otherwise.
    """
    # NAIVE Very inefficient (exponential space) : simply
    # construct Ā and then test its nonemptiness
    complemented_nfa = nfa_complementation(nfa)
    return DFA.dfa_nonemptiness_check(complemented_nfa)

    # EFFICIENT:
    # construct Ā “on-the-fly”: whenever the nonemptiness
    # algorithm wants to move from a state t_1 of Ā to a state t_2,
    # the algorithm guesses t_2 and checks that it is directly
    # connected to t_1 . Once this has been verified,
    # the algorithm can discard t_1 .


def nfa_interestingness_check(nfa: dict) -> bool:
    """ Checks if the input NFA is interesting, returning True/False.

    An automaton is “interesting” if it defines an “interesting”
    language,
    i.e., a language that is neither empty nor contains all
    possible words.

    :param dict nfa: input NFA.
    :return: *(bool)*, True if the input nfa is interesting, False
             otherwise.
    """
    return nfa_nonemptiness_check(nfa) and nfa_nonuniversality_check(nfa)


def run_acceptance(nfa: dict, run: list, word: list) -> bool:
    """ Checks if a given **run** on a NFA accepts a given input
    **word**.

    A run r of NFA on a finite word :math:`w = a_0 · · · a_{n−1}
    ∈ Σ∗` is a sequence :math:`s_0 · · · s_n` of n+1
    states in S such that :math:`s_0 ∈ S^0` , and :math:`s_{i+1}
    ∈ ρ(s_i , a_i )` for :math:`0 ≤ i ≤ n`.
    Note that a nondeterministic automaton can have multiple run
    on a given input word.
    The run r is accepting if :math:`s_n ∈ F` .

    :param dict nfa: input NFA;
    :param list run: list of states ∈ nfa['states'];
    :param list word: list of symbols ∈ nfa['alphabet'];
    :return: *(bool)*, True if the run is accepted, False otherwise.
    """
    if len(run) > 0:
        # If 'run' fist state is not an initial state return False
        if run[0] not in nfa['initial_states']:
            return False
        # If last 'run' state is not an accepting state return False
        if run[-1] not in nfa['accepting_states']:
            return False
    else:
        # If empty input check if the initial state is also
        # accepting
        if len(nfa['initial_states'].intersection(nfa['accepting_states'])) > 0:
            return True
        else:
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
    """ Checks if a given word is accepted by a NFA.

    The word w is accepted by a NFA if exists at least an
    accepting run on w.

    :param dict nfa: input NFA;
    :param list word: list of symbols ∈ nfa['alphabet'];
    :return: *(bool)*, True if the word is accepted, False otherwise.
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


# SIDE EFFECTS
def rename_nfa_states(nfa: dict, suffix: str):
    """ Side effect on input! Renames all the states of the NFA
    adding a **suffix**.

    It is an utility function to be used to avoid automata to have
    states with names in common.

    Avoid suffix that can lead to special name like "as", "and",...

    :param dict nfa: input NFA.
    :param str suffix: string to be added at beginning of each state name.
    """
    conversion_dict = {}
    new_states = set()
    new_initials = set()
    new_accepting = set()
    for state in nfa['states']:
        conversion_dict[state] = '' + suffix + state
        new_states.add('' + suffix + state)
        if state in nfa['initial_states']:
            new_initials.add('' + suffix + state)
        if state in nfa['accepting_states']:
            new_accepting.add('' + suffix + state)

    nfa['states'] = new_states
    nfa['initial_states'] = new_initials
    nfa['accepting_states'] = new_accepting

    new_transitions = {}
    for transition in nfa['transitions']:
        new_arrival = set()
        for arrival in nfa['transitions'][transition]:
            new_arrival.add(conversion_dict[arrival])
        new_transitions[conversion_dict[transition[0]], transition[1]] = new_arrival
    nfa['transitions'] = new_transitions
    return nfa
