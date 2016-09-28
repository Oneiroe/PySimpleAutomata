import io
import json


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
def dfa_creator_assistant():
    # TODO
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
def dfa_to_json(dfa):
    # TODO
    return


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

    return [alphabet, states, initial_states, accepting_states, transitions]


### accepting run function
def run_acceptance(automata, run):
    return True

### DFA completion

### DFA complementation

### DFAs intersection

### DFAs union

###*DFA minimization [greatest fix point]

### DFA trimming
# Reachable DFA
# Co-reachable DFA
# trimmed DFA

### DFA projection out ( the operation that removes from a word all occurrence of symbols in X )
# DFA -> NFA
