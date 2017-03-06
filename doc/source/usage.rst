Usage
-----

Just import the desired module and use the functions.

Example::

    from PySimpleAutomata import DFA, automata_IO

    dfa_example = automata_IO.dfa_dot_importer('/PATH-IN/input.dot')

    DFA.dfa_completion(dfa_example)
    new_dfa=DFA.dfa_minimization(dfa_example)

    automata_IO.dfa_to_dot(new_dfa, '/PATH-OUT/output')

See :doc:`modules` for the complete API explanation.


