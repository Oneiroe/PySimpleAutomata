import json
from itertools import product as cartesian_product
import itertools

# ###
# MEMO
# handle side-effects through input instead of manual handling in function:
#    pass as value of funtion a copy, not the data link


# ###
# TO-DO
# TODO change initial state from set to single element

# A dfa, deterministic finite automaton, A is a tuple A = (Σ, S, s_0 , ρ, F ), where
# • Σ is a finite nonempty alphabet;
# • S is a finite nonempty set of states;
# • s_0 ∈ S is the initial state;
# • F ⊆ S is the set of accepting states;
# • ρ : S × Σ → S is a transition function, which can be a partial function. Intuitively,
#       s_0 = ρ(s, a) is the state that A can move into when it is in state s and it reads the
#       symbol a. (If ρ(s, a) is undefined then reading a leads to rejection.)


### DFA definition

# alphabet = set()
# states = set()
# initial_state = 0
# accepting_states = set()
# transitions = {}  # key (state in states, action in alphabet) value [arriving state in states]
#
# dfa = [alphabet, states, initial_state, final, transition]

# Export a dfa "object" to a json file
# TODO dfa_to_json
def dfa_to_json(dfa):
    return


# Import a dfa from a json file
def dfa_json_importer(input_file):
    file = open(input_file)
    json_file = json.load(file)
    # TODO exception handling while JSON deconding/IO error
    alphabet = set(json_file['alphabet'])
    states = set(json_file['states'])
    initial_states = set(json_file['initial_states'])
    accepting_states = set(json_file['accepting_states'])
    transitions = {}  # key [state ∈ states, action ∈ alphabet] value [arriving state ∈ states]
    for p in json_file['transitions']:
        transitions[p[0], p[1]] = p[2]

    # return list
    # return [alphabet, states, initial_states, accepting_states, transitions]

    # return map
    dfa = {}
    dfa['alphabet'] = alphabet
    dfa['states'] = states
    dfa['initial_states'] = initial_states
    dfa['accepting_states'] = accepting_states
    dfa['transitions'] = transitions
    return dfa


### Checks if a given dfa accepts a run on a given input word
def run_acceptance(dfa, run, word):
    # If 'run' fist state is not an initial state return False
    if run[0] not in dfa['initial_states']:
        return False
    # If last 'run' state is not an accepting state return False
    if run[-1] not in dfa['accepting_states']:
        return False
    for i in range(len(word) - 1):
        if (run[i], word[i]) in dfa['transitions']:
            if dfa['transitions'][run[i], word[i]] != run[i + 1]:
                return False
        else:
            return False
    return True


### DFA completion
def dfa_completion(dfa):
    dfa['states'].add('sink')
    for s in dfa['states']:
        for a in dfa['alphabet']:
            if (s, a) not in dfa['transitions']:
                dfa['transitions'][s, a] = 'sink'
    return dfa


### DFA complementation
def dfa_complementation(dfa):
    dfa_complemented = dfa_completion(dfa)
    dfa_complemented['accepting_states'] = dfa['states'].difference(dfa['accepting_states'])
    return dfa_complemented


### DFAs intersection
def dfa_intersection(dfa_1, dfa_2):
    intersection = {}
    intersection['alphabet'] = dfa_1['alphabet']
    intersection['states'] = set(cartesian_product(dfa_1['states'], dfa_2['states']))
    intersection['initial_states'] = set(cartesian_product(dfa_1['initial_states'], dfa_2['initial_states']))
    intersection['accepting_states'] = set(cartesian_product(dfa_1['accepting_states'], dfa_2['accepting_states']))

    intersection['transitions'] = {}
    for s in intersection['states']:
        for a in intersection['alphabet']:
            if (s[0], a) in dfa_1['transitions'] and (s[1], a) in dfa_2['transitions']:
                s1 = dfa_1['transitions'][s[0], a]
                s2 = dfa_2['transitions'][s[1], a]
                intersection['transitions'][s, a] = (s1, s2)
            else:
                continue
    return intersection


### DFAs union
def dfa_union(dfa_1, dfa_2):
    dfa_1 = dfa_completion(dfa_1)
    dfa_2 = dfa_completion(dfa_2)

    union = {}
    union['alphabet'] = dfa_1['alphabet']
    union['states'] = set(cartesian_product(dfa_1['states'], dfa_2['states']))
    union['initial_states'] = set(cartesian_product(dfa_1['initial_states'], dfa_2['initial_states']))

    union['accepting_states'] = set(cartesian_product(dfa_1['accepting_states'], dfa_2['states'])).union(
        set(cartesian_product(dfa_1['states'], dfa_2['accepting_states']))
    )

    union['transitions'] = {}
    for s in union['states']:
        for a in union['alphabet']:
            s1 = dfa_1['transitions'][s[0], a]
            s2 = dfa_2['transitions'][s[1], a]
            union['transitions'][s, a] = (s1, s2)
    return union


###*DFA minimization [greatest fix point]
def dfa_minimization(dfa):
    dfa = dfa_completion(dfa)

    ##  Greatest-fixpoint

    # cartesian product of DFA states
    z_current = set(cartesian_product(dfa['states'], dfa['states']))

    z_next = z_current.copy();

    # First bisimulation condition check (can be done just once)
    # s ∈ F iff t ∈ F
    for element in z_current:
        if (element[0] in dfa['accepting_states'] and element[1] not in dfa['accepting_states']) or (
                        element[0] not in dfa['accepting_states'] and element[1] in dfa['accepting_states']):
            z_next.remove(element)
    z_current = z_next

    # Second and third condition of bisimularity check, while succeed or fail
    while z_current:
        z_next = z_current.copy();
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

    dfa_min['initial_states'] = dfa_min['states'].intersection(dfa['initial_states'])
    dfa_min['accepting_states'] = dfa_min['states'].intersection(dfa['accepting_states'])

    dfa_min['transitions'] = dfa['transitions'].copy()
    for p in dfa['transitions']:
        if p[0] not in dfa_min['states']:
            dfa_min['transitions'].pop(p)
        if dfa['transitions'][p] not in dfa_min['states']:
            dfa_min['transitions'][p] = equivalence[dfa['transitions'][p]].intersection(dfa_min['states']).pop()

    return dfa_min


# remove unreachable states from a dfa
def dfa_reachable(dfa):
    # set of reachable states from initial states
    s_r = dfa['initial_states'].copy()
    s_r_stack = s_r.copy()
    while s_r_stack:
        s = s_r_stack.pop()
        for a in dfa['alphabet']:
            if (s, a) in dfa['transitions']:
                if dfa['transitions'][s, a] not in s_r:
                    s_r_stack.add(dfa['transitions'][s, a])
                    s_r.add(dfa['transitions'][s, a])
            else:
                pass
    dfa['states'] = s_r
    dfa['accepting_states'] = dfa['accepting_states'].intersection(dfa['states'])

    for p in dfa['transitions']:
        if p[0] not in dfa['states']:
            dfa['transitions'].remove(p)
        if dfa['transitions'][p] not in dfa['states']:
            dfa['transitions'].remove(p)

    return dfa


# remove states that do not reach a final state from dfa
def dfa_co_reachable(dfa):
    # set of states reaching final states
    s_r = dfa['accepting_states'].copy()
    s_r_stack = s_r.copy()

    # inverse transition function
    inv_transitions = {}
    for k, v in dfa['transitions'].items():
        inv_transitions.setdefault(v, set()).add(k)

    while s_r_stack:
        s = s_r_stack.pop()
        for s_app in inv_transitions[s]:
            if s_app[0] not in s_r:
                s_r_stack.add(s_app[0])
                s_r.add(s_app[0])

    dfa['states'] = s_r
    dfa['initial_states'] = dfa['initial_states'].intersection(dfa['states'])

    for p in dfa['transitions']:
        if p[0] not in dfa['states']:
            dfa['transitions'].remove(p)
        if dfa['transitions'][p] not in dfa['states']:
            dfa['transitions'].remove(p)

    return dfa


### DFA trimming
def dfa_trimming(dfa):
    # Reachable DFA
    dfa = dfa_reachable(dfa)
    # Co-reachable DFA
    dfa = dfa_co_reachable(dfa)
    # trimmed DFA
    return dfa


### DFA projection out ( the operation that removes from a word all occurrence of symbols in X )
# Given a dfa A = (Σ, S, s 0 , ρ, F ), we can define an nfa A π X that recognizes the language π X (L(A)).
# DFA -> NFA
def dfa_projection(dfa, x, word):
    nfa = dfa.copy()
    nfa['alphabet'] = dfa['alphabet'].difference(x)

    for transition in dfa['transitions']:
        if transition[1] not in nfa['alphabet']:
            nfa['transitions'].remove(transition)

    e_x = set()

    # TODO

    return nfa
