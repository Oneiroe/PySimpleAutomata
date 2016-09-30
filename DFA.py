import io
import json
from copy import deepcopy
import itertools

# ###
# TO-DO
# TODO handle side-effects through input instead of manual handling in function:
#    pass as value of funtion a copy, not the data link

# A dfa, deterministic finite automaton, A is a tuple A = (Σ, S, s 0 , ρ, F ), where
# • Σ is a finite nonempty alphabet;
# • S is a finite nonempty set of states;
# • s 0 ∈ S is the initial state;
# • F ⊆ S is the set of accepting states;
# • ρ : S × Σ → S is a transition function, which can be a partial function. Intuitively,
#       s 0 = ρ(s, a) is the state that A can move into when it is in state s and it reads the
#       symbol a. (If ρ(s, a) is undefined then reading a leads to rejection.)


### DFA definition

# alphabet = set()
# states = set()
# initial_states = 0
# accepting_states = set()
# transitions = {}  # key (state in states, action in alphabet) value [arriving state in states]
#
# dfa = [alphabet, states, initial_state, final, transition]

# Guided DFA constructor
# TODO dfa_creator_assistant()
def dfa_creator_assistant():
    alphabet = set()
    states = set()
    initial_states = set()
    accepting_states = set()
    transitions = {}  # key [state in states, action in alphabet] value [arriving state in states]

    print('Insert states...')

    print('Which ones are initial states?')

    print('Which ones are final states?')

    print('Insert actions...')

    print('Insert transitions')

    return [alphabet, states, initial_states, accepting_states, transitions]


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
    transitions = {}  # key [state in states, action in alphabet] value [arriving state in states]
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
    # If run fist state is not an initial state return False
    if run[0] not in dfa['initial_states']:
        return False
    # If last run state is not an accepting state return False
    if run[-1] not in dfa['accepting_states']:
        return False
    for i in range(len(word) - 1):
        try:
            if dfa['transitions'][run[i], word[i]] != run[i + 1]:
                return False
        except KeyError:
            return False
    return True


### DFA completion
def dfa_completion(dfa, side_effect):
    if side_effect == True:
        dfa_t = dfa
    else:
        dfa_t = deepcopy(dfa)
    dfa_t['states'].add('sink')
    for s in dfa_t['states']:
        for a in dfa_t['alphabet']:
            try:
                dfa_t['transitions'][s, a]
            except KeyError:
                dfa_t['transitions'][s, a] = 'sink'
    return dfa_t


### DFA complementation
def dfa_complementation(dfa, side_effect):
    dfa = dfa_completion(dfa, side_effect)
    if side_effect == True:
        dfa_c = dfa
    else:
        dfa_c = deepcopy(dfa)

    dfa_c['accepting_states'] = dfa['states'].difference(dfa['accepting_states'])
    return dfa_c


### DFAs intersection
def dfa_intersection(dfa_1, dfa_2):
    # if dfa_1['alphabet'].difference(dfa_2['alphabet'])!=set():
    #     return False
    intersection = {}
    intersection['alphabet'] = dfa_1['alphabet']
    intersection['states'] = set(itertools.product(dfa_1['states'], dfa_2['states']))
    intersection['initial_states'] = set(itertools.product(dfa_1['initial_states'], dfa_2['initial_states']))
    intersection['accepting_states'] = set(itertools.product(dfa_1['accepting_states'], dfa_2['accepting_states']))

    intersection['transitions'] = {}
    for s in intersection['states']:
        for a in intersection['alphabet']:
            try:
                s1 = dfa_1['transitions'][s[0], a]
            except KeyError:
                continue
            try:
                s2 = dfa_2['transitions'][s[1], a]
            except KeyError:
                continue
            intersection['transitions'][s, a] = (s1, s2)
    return intersection


### DFAs union
def dfa_union(dfa_1, dfa_2):
    dfa_completion(dfa_1, True)
    dfa_completion(dfa_2, True)
    # TODO handle side-effect on original DFAs

    union = {}
    union['alphabet'] = dfa_1['alphabet']
    union['states'] = set(itertools.product(dfa_1['states'], dfa_2['states']))
    union['initial_states'] = set(itertools.product(dfa_1['initial_states'], dfa_2['initial_states']))

    union['accepting_states'] = \
        set(itertools.product(dfa_1['accepting_states'], dfa_2['states'])).union(
            set(itertools.product(dfa_1['states'], dfa_2['accepting_states']))
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
    dfa_completion(dfa, True)
    # TODO handle side-effect on original DFA

    # Greatest-fixpoint

    # cartesian product of DFA states
    z_current = set(itertools.product(dfa['states'], dfa['states']))

    z_next = deepcopy(z_current);

    # First bisimulation condition check (can be done just once)
    # s ∈ F iff t ∈ F
    for element in z_current:
        if (element[0] in dfa['accepting_states'] and element[1] not in dfa['accepting_states']) or (
                        element[0] not in dfa['accepting_states'] and element[1] in dfa['accepting_states']):
            z_next.remove(element)
    z_current = z_next

    # Second and third condition of bisimularity check, while succeed or emptied
    while z_current:
        z_next = deepcopy(z_current);
        for element in z_current:
            # for all s0,a s.t. ρ(s, a) = s 0 , there exists t 0 s.t. ρ(t, a) = t 0 and (s 0 , t 0 ) ∈ Z i ;
            for a in dfa['alphabet']:
                try:
                    if (dfa['transitions'][element[0], a], dfa['transitions'][element[1], a]) not in z_current:
                        z_next.remove(element)
                        break
                except KeyError:
                    # action a not possible in state element[0] or element[1]
                    z_next.remove(element)

        if z_next == z_current:
            break
        z_current = z_next

    # Equivalence Sets
    equivalence = {}
    for element in z_current:
        if element[0] not in equivalence:
            equivalence[element[0]] = set()
        equivalence[element[0]].add(element[1])

    # Minimal DFA construction
    dfa_min = {}
    dfa_min['alphabet'] = dfa['alphabet']

    dfa_min['states'] = set()

    # select one element for each equivalence set
    for element in equivalence.values():
        if dfa_min['states'].isdisjoint(element):
            e = element.pop()
            dfa_min['states'].add(e)
            element.add(e)

    dfa_min['initial_states'] = dfa_min['states'].intersection(dfa['initial_states'])
    dfa_min['accepting_states'] = dfa_min['states'].intersection(dfa['accepting_states'])

    dfa_min['transitions'] = deepcopy(dfa['transitions'])
    for p in dfa['transitions']:
        if p[0] not in dfa_min['states']:
            dfa_min['transitions'].pop(p)
        if dfa['transitions'][p] not in dfa_min['states']:
            dfa_min['transitions'][p] = equivalence[dfa['transitions'][p]].intersection(dfa_min['states']).pop()

    return dfa_min


# remove unreachable states from a dfa
def dfa_reachable(dfa):
    # TODO handle side effect
    # set of reachable states from initial states
    s_r = dfa['initial_states'].copy()
    s_r_stack = s_r.copy()
    while s_r_stack:
        s = s_r_stack.pop()
        for a in dfa['alphabet']:
            try:
                if dfa['transitions'][s, a] in s_r:
                    pass
                else:
                    s_r_stack.add(dfa['transitions'][s, a])
                    s_r.add(dfa['transitions'][s, a])
            except KeyError:
                pass
    dfa['states'] = s_r
    dfa['final_states'] = dfa['accepting_states'].intersection(dfa['states'])

    for p in dfa['transitions']:
        if p[0] not in dfa['states']:
            dfa['transitions'].remove(p)
        if dfa['transitions'][p] not in dfa['states']:
            dfa['transitions'].remove(p)

    return dfa


# remove states that do not reach a final state from dfa
def dfa_co_reachable(dfa):
    # TODO handle side-effect
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
            try:
                if s_app[0] in s_r:
                    pass
                else:
                    s_r_stack.add(s_app[0])
                    s_r.add(s_app[0])
            except KeyError:
                pass
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
# DFA -> NFA
