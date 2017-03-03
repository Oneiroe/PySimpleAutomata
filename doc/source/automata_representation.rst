Automata representation
-----------------------

For transparency, the automata are represented with Built-in Types
instead of an object structure.
More precisely an automata is a `dict <https://docs.python.org/3.6/library/stdtypes.html#mapping-types-dict>`_
with the following keys :

    - 'alphabet',
    - 'states',
    - 'initial_state(s)',
    - 'accepting_states',
    - 'transitions'

Respective mapping of each key varies depending on the specific automata type (mainly
`sets <https://docs.python.org/3.6/library/stdtypes.html#set-types-set-frozenset>`_).
See :doc:`DFA`, :doc:`NFA`, :doc:`AFW` for specifications.

.. note::

    Being not a fixed object is up to the user to ensure the correctness of the data.

DFA Example::

    dfa_example = {
        'alphabet': {'5c', '10c', 'gum'},
        'states': {'s1', 's0', 's2', 's3'},
        'initial_state': 's0',
        'accepting_states': {'s0'},
        'transitions': {
            ('s1', '5c'): 's2',
            ('s0', '5c'): 's1',
            ('s2', '10c'): 's3',
            ('s3', 'gum'): 's0',
            ('s2', '5c'): 's3',
            ('s0', '10c'): 's2',
            ('s1', '10c'): 's3'
        }
    }

