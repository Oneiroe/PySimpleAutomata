"""
Module to manage DFA (Deterministic Finite Automaton).

Formally a DFA, Deterministic Finite Automaton, is a tuple
:math:`A=(Σ,S,s_0,ρ,F)`, where:

    • Σ is a finite nonempty alphabet;
    • S is a finite nonempty set of states;
    • :math:`s_0 ∈ S` is the initial state;
    • F ⊆ S is the set of accepting states;
    • :math:`ρ: S × Σ → S` is a transition function, which can be a
      partial function.

Intuitively, :math:`s_0 = ρ(s, a)` is the state that A can
move into when it is in state s and it reads the symbol a.
(If :math:`ρ(s, a)` is undefined then reading a leads to
rejection.)

In this module a DFA is defined as follows

 DFA = dict() with the following keys-values:
  • alphabet         => set() ;
  • states           => set() ;
  • initial_state    => str() ;
  • accepting_states => set() ;
  • transitions      => dict(), where
        **key**: (*state* ∈ states, *action* ∈ alphabet)

        **value**: (*arriving_state* in states).
"""

from copy import deepcopy


def dfa_word_acceptance(dfa: dict, word: list) -> bool:
    """ Checks if a given **word** is accepted by a DFA,
    returning True/false.

    The word w is accepted by a DFA if DFA has an accepting run
    on w. Since A is deterministic,
    :math:`w ∈ L(A)` if and only if :math:`ρ(s_0 , w) ∈ F` .

    :param dict dfa: input DFA;
    :param list word: list of actions ∈ dfa['alphabet'].
    :return: *(bool)*, True if the word is accepted, False in the
             other case.
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
    """ Side effects on input! Completes the DFA assigning to
    each state a transition for each letter in the alphabet (if
    not already defined).

    We say that a DFA is complete if its transition function
    :math:`ρ:S×Σ→S` is a total function, that is,
    for all :math:`s ∈ S` and all :math:`a ∈ Σ` we have that
    exists a :math:`ρ(s,a)=s_x` for some :math:`s_x ∈ S`.
    Given an arbitrary DFA A, its completed version :math:`A_T`
    is obtained as follows:
    :math:`A_T = (Σ, S ∪ \{sink\}, s_0 , ρ_T , F )` with
    :math:`ρ_T(s,a)=sink`
    when :math:`ρ(s,a)` is not defined in A and :math:`ρ_T=ρ` in
    the other cases.

    :param dict dfa: input DFA.
    :return: *(dict)* representing the completed DFA.
    """
    dfa['states'].add('sink')
    for state in dfa['states']:
        for action in dfa['alphabet']:
            if (state, action) not in dfa['transitions']:
                dfa['transitions'][state, action] = 'sink'
    return dfa


def dfa_complementation(dfa: dict) -> dict:
    """ Returns a DFA that accepts any word but he ones accepted
    by the input DFA.

    Let A be a completed DFA, :math:`Ā = (Σ, S, s_0 , ρ, S − F )`
    is the DFA that runs A but accepts whatever word A does not.

    :param dict dfa: input DFA.
    :return: *(dict)* representing the complement of the input DFA.
    """
    dfa_complement = dfa_completion(deepcopy(dfa))
    dfa_complement['accepting_states'] = \
        dfa_complement['states'].difference(dfa_complement['accepting_states'])
    return dfa_complement


def dfa_intersection(dfa_1: dict, dfa_2: dict) -> dict:
    """ Returns a DFA accepting the intersection of the DFAs in
    input.

    Let :math:`A_1 = (Σ, S_1 , s_{01} , ρ_1 , F_1 )` and
    :math:`A_2 = (Σ, S_2 , s_{02} , ρ_2 , F_2 )` be two DFAs.
    Then there is a DFA :math:`A_∧` that runs simultaneously both
    :math:`A_1` and :math:`A_2` on the input word and
    accepts when both accept.
    It is defined as:

    :math:`A_∧ = (Σ, S_1 × S_2 , (s_{01} , s_{02} ), ρ, F_1 × F_2 )`

    where

    :math:`ρ((s_1 , s_2 ), a) = (s_{X1} , s_{X2} )` iff
    :math:`s_{X1} = ρ_1 (s_1 , a)` and :math:`s_{X2}= ρ_2 (s_2 , a)`

    Implementation proposed guarantees the resulting DFA has only
    **reachable** states.

    :param dict dfa_1: first input DFA;
    :param dict dfa_2: second input DFA.
    :return: *(dict)* representing the intersected DFA.
    """
    intersection = {
        'alphabet': dfa_1['alphabet'].intersection(dfa_2['alphabet']),
        'states': {(dfa_1['initial_state'], dfa_2['initial_state'])},
        'initial_state': (dfa_1['initial_state'], dfa_2['initial_state']),
        'accepting_states': set(),
        'transitions': dict()
    }

    boundary = set()
    boundary.add(intersection['initial_state'])
    while boundary:
        (state_dfa_1, state_dfa_2) = boundary.pop()
        if state_dfa_1 in dfa_1['accepting_states'] \
                and state_dfa_2 in dfa_2['accepting_states']:
            intersection['accepting_states'].add((state_dfa_1, state_dfa_2))

        for a in intersection['alphabet']:
            if (state_dfa_1, a) in dfa_1['transitions'] \
                    and (state_dfa_2, a) in dfa_2['transitions']:
                next_state_1 = dfa_1['transitions'][state_dfa_1, a]
                next_state_2 = dfa_2['transitions'][state_dfa_2, a]
                if (next_state_1, next_state_2) not in intersection['states']:
                    intersection['states'].add((next_state_1, next_state_2))
                    boundary.add((next_state_1, next_state_2))
                intersection['transitions'][(state_dfa_1, state_dfa_2), a] = \
                    (next_state_1, next_state_2)

    return intersection


def dfa_union(dfa_1: dict, dfa_2: dict) -> dict:
    """ Returns a DFA accepting the union of the input DFAs.

    Let :math:`A_1 = (Σ, S_1 , s_{01} , ρ_1 , F_1 )` and
    :math:`A_2 = (Σ, S_2 , s_{02} , ρ_2 , F_2 )` be two completed
    DFAs.
    Then there is a DFA :math:`A_∨` that runs simultaneously both
    :math:`A_1` and :math:`A_2` on the input word
    and accepts when one of them accepts.
    It is defined as:

    :math:`A_∨ = (Σ, S_1 × S_2 , (s_{01} , s_{02} ), ρ, (F_1 ×
    S_2 ) ∪ (S_1 × F_2 ))`

    where

    :math:`ρ((s_1 , s_2 ), a) = (s_{X1} , s_{X2} )` iff
    :math:`s_{X1} = ρ_1 (s_1 , a)` and :math:`s_{X2} = ρ(s_2 , a)`

    Proposed implementation guarantees resulting DFA has only **reachable**
    states.

    :param dict dfa_1: first input DFA;
    :param dict dfa_2: second input DFA.
    :return: *(dict)* representing the united DFA.
    """
    dfa_1 = deepcopy(dfa_1)
    dfa_2 = deepcopy(dfa_2)
    dfa_1['alphabet'] = dfa_2['alphabet'] = dfa_1['alphabet'].union(
        dfa_2['alphabet'])  # to complete the DFAs over all possible transition
    dfa_1 = dfa_completion(dfa_1)
    dfa_2 = dfa_completion(dfa_2)

    union = {
        'alphabet': dfa_1['alphabet'].copy(),
        'states': {(dfa_1['initial_state'], dfa_2['initial_state'])},
        'initial_state': (dfa_1['initial_state'], dfa_2['initial_state']),
        'accepting_states': set(),
        'transitions': dict()
    }

    boundary = set()
    boundary.add(union['initial_state'])
    while boundary:
        (state_dfa_1, state_dfa_2) = boundary.pop()
        if state_dfa_1 in dfa_1['accepting_states'] \
                or state_dfa_2 in dfa_2['accepting_states']:
            union['accepting_states'].add((state_dfa_1, state_dfa_2))
        for a in union['alphabet']:
            # as DFAs are completed they surely have the transition
            next_state_1 = dfa_1['transitions'][state_dfa_1, a]
            next_state_2 = dfa_2['transitions'][state_dfa_2, a]
            if (next_state_1, next_state_2) not in union['states']:
                union['states'].add((next_state_1, next_state_2))
                boundary.add((next_state_1, next_state_2))
            union['transitions'][(state_dfa_1, state_dfa_2), a] = \
                (next_state_1, next_state_2)

    return union


def dfa_minimization(dfa: dict) -> dict:
    """ Returns the minimization of the DFA in input through a
    greatest fix-point method.

    Given a completed DFA :math:`A = (Σ, S, s_0 , ρ, F )` there
    exists a single minimal DFA :math:`A_m`
    which is equivalent to A, i.e. reads the same language
    :math:`L(A) = L(A_m)` and with a minimal number of states.
    To construct such a DFA we exploit bisimulation as a suitable
    equivalence relation between states.

    A bisimulation relation :math:`E ∈ S × S` is a relation
    between states that satisfies the following condition:
    if :math:`(s, t) ∈ E` then:

     • s ∈ F iff t ∈ F;
     • For all :math:`(s_X,a)` such that :math:`ρ(s, a) = s_X`,
       there exists :math:`t_X` such that :math:`ρ(t, a) = t_X`
       and :math:`(s_X , t_X ) ∈ E`;
     • For all :math:`(t_X,a)` such that :math:`ρ(t, a) = t_X` ,
       there exists :math:`s_X` such that :math:`ρ(s, a) = s_X`
       and :math:`(s_X , t_X ) ∈ E`.

    :param dict dfa: input DFA.
    :return: *(dict)* representing the minimized DFA.
    """
    dfa = dfa_completion(deepcopy(dfa))

    ################################################################
    ### Greatest-fixpoint

    z_current = set()
    z_next = set()

    # First bisimulation condition check (can be done just once)
    # s ∈ F iff t ∈ F
    for state_s in dfa['states']:
        for state_t in dfa['states']:
            if (
                            state_s in dfa['accepting_states']
                    and state_t in dfa['accepting_states']
            ) or (
                            state_s not in dfa['accepting_states']
                    and state_t not in dfa['accepting_states']
            ):
                z_next.add((state_s, state_t))

    # Second and third condition of bisimularity check
    while z_current != z_next:
        z_current = z_next
        z_next = z_current.copy()
        for (state_1, state_2) in z_current:
            # for all s0,a s.t. ρ(s, a) = s_0 , there exists t 0
            # s.t. ρ(t, a) = t 0 and (s_0 , t 0 ) ∈ Z i ;
            for a in dfa['alphabet']:
                if (state_1, a) in dfa['transitions'] \
                        and (state_2, a) in dfa['transitions']:
                    if (
                            dfa['transitions'][state_1, a],
                            dfa['transitions'][state_2, a]
                    ) not in z_current:
                        z_next.remove((state_1, state_2))
                        break
                else:
                    # action a not possible in state element[0]
                    # or element[1]
                    z_next.remove((state_1, state_2))
                    break

    ################################################################
    ### Equivalence Sets

    equivalence = dict()
    for (state_1, state_2) in z_current:
        equivalence.setdefault(state_1, set()).add(state_2)

    ################################################################
    ### Minimal DFA construction

    dfa_min = {
        'alphabet': dfa['alphabet'].copy(),
        'states': set(),
        'initial_state': dfa['initial_state'],
        'accepting_states': set(),
        'transitions': dfa['transitions'].copy()
    }

    # select one element for each equivalence set
    for equivalence_set in equivalence.values():
        if dfa_min['states'].isdisjoint(equivalence_set):
            e = equivalence_set.pop()
            dfa_min['states'].add(e)  # TODO highlight this instruction
            equivalence_set.add(e)

    dfa_min['accepting_states'] = \
        dfa_min['states'].intersection(dfa['accepting_states'])

    for t in dfa['transitions']:
        if t[0] not in dfa_min['states']:
            dfa_min['transitions'].pop(t)
        elif dfa['transitions'][t] not in dfa_min['states']:
            dfa_min['transitions'][t] = \
                equivalence[dfa['transitions'][t]]. \
                    intersection(dfa_min['states']).pop()

    return dfa_min


# Side effects on input variable
def dfa_reachable(dfa: dict) -> dict:
    """ Side effects on input! Removes unreachable states from a
    DFA and returns the pruned DFA.

    It is possible to remove from a DFA A all unreachable states
    from the initial state without altering the language.
    The reachable DFA :math:`A_R` corresponding to A is defined as:

    :math:`A_R = (Σ, S_R , s_0 , ρ|S_R , F ∩ S_R )`

    where

    • :math:`S_R` set of reachable state from the initial one
    • :math:`ρ|S_R` is the restriction on :math:`S_R × Σ` of ρ.

    :param dict dfa: input DFA.
    :return: *(dict)* representing the pruned DFA.
    """
    reachable_states = set()  # set of reachable states from root
    boundary = set()
    reachable_states.add(dfa['initial_state'])
    boundary.add(dfa['initial_state'])

    while boundary:
        s = boundary.pop()
        for a in dfa['alphabet']:
            if (s, a) in dfa['transitions']:
                if dfa['transitions'][s, a] not in reachable_states:
                    reachable_states.add(dfa['transitions'][s, a])
                    boundary.add(dfa['transitions'][s, a])
    dfa['states'] = reachable_states
    dfa['accepting_states'] = \
        dfa['accepting_states'].intersection(dfa['states'])

    transitions = dfa[
        'transitions'].copy()  # TODO why copy? because for doesn't cycle
    # mutable set....
    for t in transitions:
        if t[0] not in dfa['states']:
            dfa['transitions'].pop(t)
        elif dfa['transitions'][t] not in dfa['states']:
            dfa['transitions'].pop(t)

    return dfa


# Side effects on input variable
def dfa_co_reachable(dfa: dict) -> dict:
    """ Side effects on input! Removes from the DFA all states that
    do not reach a final state and returns the pruned DFA.

    It is possible to remove from a DFA A all states that do not
    reach a final state without altering the language.
    The co-reachable dfa :math:`A_F` corresponding to A is
    defined as:

    :math:`A_F = (Σ, S_F , s_0 , ρ|S_F , F )`

    where

    • :math:`S_F` is the set of states that reach a final state
    • :math:`ρ|S_F` is the restriction on :math:`S_F × Σ` of ρ.

    :param dict dfa: input DFA.
    :return: *(dict)* representing the pruned DFA.
    """

    co_reachable_states = dfa['accepting_states'].copy()
    boundary = co_reachable_states.copy()

    # inverse transition function
    inverse_transitions = dict()
    for key, value in dfa['transitions'].items():
        inverse_transitions.setdefault(value, set()).add(key)

    while boundary:
        s = boundary.pop()
        if s in inverse_transitions:
            for (state, action) in inverse_transitions[s]:
                if state not in co_reachable_states:
                    boundary.add(state)
                    co_reachable_states.add(state)

    dfa['states'] = co_reachable_states

    # If not s_0 ∈ S_F the resulting dfa is empty
    if dfa['initial_state'] not in dfa['states']:
        dfa = {
            'alphabet': set(),
            'states': set(),
            'initial_state': None,
            'accepting_states': set(),
            'transitions': dict()
        }
        return dfa

    transitions = dfa['transitions'].copy()
    for t in transitions:
        if t[0] not in dfa['states']:
            dfa['transitions'].pop(t)
        elif dfa['transitions'][t] not in dfa['states']:
            dfa['transitions'].pop(t)

    return dfa


# Side effects on input variable
def dfa_trimming(dfa: dict) -> dict:
    """ Side effects on input! Returns the DFA in input trimmed,
    so both reachable and co-reachable.

    Given a DFA A, the corresponding trimmed DFA contains only
    those states that are reachable from the initial state
    and that lead to a final state.
    The trimmed dfa :math:`A_{RF}` corresponding to A is defined as

    :math:`A_{RF} = (Σ, S_R ∩ S_F , s_0 , ρ|S_R∩S_F , F ∩ S_R )`

    where

    • :math:`S_R` set of reachable states from the initial state
    • :math:`S_F` set of states that reaches a final state
    • :math:`ρ|S_R∩S_F` is the restriction on :math:`(S_R ∩ S_F )
      × Σ` of ρ.

    :param dict dfa: input DFA.
    :return: *(dict)* representing the trimmed input DFA.
    """
    # Reachable DFA
    dfa = dfa_reachable(dfa)
    # Co-reachable DFA
    dfa = dfa_co_reachable(dfa)
    # trimmed DFA
    return dfa


def dfa_projection(dfa: dict, symbols_to_remove: set) -> dict:
    """ Returns a NFA that reads the language recognized by the
    input DFA where all the symbols in **symbols_to_project**
    are projected out of the alphabet.

    Projection in a DFA is the operation that existentially
    removes from a word all occurrence of symbols in a set X.
    Given a dfa :math:`A = (Σ, S, s_0 , ρ, F )`, we can define an
    NFA :math:`A_{πX}`
    that recognizes the language :math:`πX(L(A))` as

    :math:`A_{πX}= ( Σ−X, S, S_0 , ρ_X , F )`

    where

    • :math:`S_0 = \{s | (s_0 , s) ∈ ε_X \}`
    • :math:`(s,a,s_y ) ∈ ρ_X` iff there exist :math:`(t, t_y)` s.t.
      :math:`(s,t) ∈ ε_X , t_y = ρ(t,a)` and :math:`(t_y , s_y )
      ∈ ε_X`

    :param dict dfa: input DFA;
    :param set symbols_to_remove: set containing symbols ∈ dfa[
           'alphabet'] to be projected out from DFA.
    :return: *(dict)* representing a NFA.
    """
    nfa = {
        'alphabet': dfa['alphabet'].difference(symbols_to_remove),
        'states': dfa['states'].copy(),
        'initial_states': {dfa['initial_state']},
        'accepting_states': dfa['accepting_states'].copy(),
        'transitions': dict()
    }

    current_nfa_transitions = None
    current_e_x = None
    e_x = dict()  # equivalence relation dictionary

    # while no more changes are possible
    while current_nfa_transitions != nfa['transitions'] or current_e_x != e_x:
        current_nfa_transitions = nfa['transitions'].copy()
        current_e_x = deepcopy(e_x)
        for (state, a) in dfa['transitions']:
            next_state = dfa['transitions'][state, a]
            if a in symbols_to_remove:
                # mark next_state as equivalent to state
                e_x.setdefault(state, set()).add(next_state)

                app_set = set()
                for equivalent in e_x[state]:
                    # mark states equivalent to next_states also to state
                    if equivalent in e_x:
                        app_set.update(e_x[equivalent])
                    # add all transitions of equivalent states to state
                    for act in nfa['alphabet']:
                        if (equivalent, act) in dfa['transitions']:
                            equivalent_next = dfa['transitions'][
                                equivalent, act]
                            nfa['transitions'].setdefault(
                                (state, act), set()).add(equivalent_next)
                            # if equivalent_next has equivalent states
                            if equivalent_next in e_x:
                                # the transition leads also to these states
                                nfa['transitions'][state, act].update(
                                    e_x[equivalent_next])
                e_x[state].update(app_set)
            else:
                # add the transition to the NFA
                nfa['transitions'].setdefault((state, a), set()).add(
                    next_state)
                # if next_state has equivalent states
                if next_state in e_x:
                    # the same transition arrive also to all these other states
                    nfa['transitions'][state, a].update(e_x[next_state])

    # Add all state equivalent to the initial one to NFA initial states set
    if dfa['initial_state'] in e_x:
        nfa['initial_states'].update(e_x[dfa['initial_state']])

    return nfa


def dfa_nonemptiness_check(dfa: dict) -> bool:
    """ Checks if the input DFA is nonempty (i.e. if it recognizes a
    language except the empty one), returning True/False.

    An automaton A is nonempty if :math:`L(A) ≠ ∅`. L(A) is
    nonempty iff there are states :math:`s_0 and t ∈ F` such
    that t is connected to :math:`s_0`. Thus, automata
    nonemptiness is equivalent to graph reachability, where a
    breadth-first-search algorithm can construct in linear time
    the set of all states connected to initial state
    :math:`s_0`.
    A is nonempty iff this set intersects F nontrivially.

    :param dict dfa: input DFA.
    :return: *(bool)*, True if the DFA is nonempty, False otherwise
    """
    # BFS
    queue = [dfa['initial_state']]
    visited = set()
    visited.add(dfa['initial_state'])
    while queue:
        state = queue.pop(0)  # TODO note that this pop is applied to a list
        # not like in sets
        visited.add(state)
        for a in dfa['alphabet']:
            if (state, a) in dfa['transitions']:
                if dfa['transitions'][state, a] in dfa['accepting_states']:
                    return True
                if dfa['transitions'][state, a] not in visited:
                    queue.append(dfa['transitions'][state, a])
    return False


# SIDE EFFECTS
def rename_dfa_states(dfa: dict, suffix: str):
    """ Side effect on input! Renames all the states of the DFA
    adding a **suffix**.

    It is an utility function to be used to avoid automata to have
    states with names in common.

    Avoid suffix that can lead to special name like "as", "and",...

    :param dict dfa: input DFA.
    :param str suffix: string to be added at beginning of each state name.
    """
    conversion_dict = dict()
    new_states = set()
    new_accepting = set()
    for state in dfa['states']:
        conversion_dict[state] = '' + suffix + state
        new_states.add('' + suffix + state)
        if state in dfa['accepting_states']:
            new_accepting.add('' + suffix + state)

    dfa['states'] = new_states
    dfa['initial_state'] = '' + suffix + dfa['initial_state']
    dfa['accepting_states'] = new_accepting

    new_transitions = dict()
    for transition in dfa['transitions']:
        new_transitions[conversion_dict[transition[0]], transition[1]] = \
            conversion_dict[dfa['transitions'][transition]]
    dfa['transitions'] = new_transitions
    return dfa
