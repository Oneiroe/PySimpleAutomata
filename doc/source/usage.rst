Usage
-----

Just import the desired module and use the functions.

Example::

    from PySimpleAutomata import DFA, automata_IO

    dfa_example = automata_IO.dfa_dot_importer('/PATH-IN/input.dot')

    DFA.dfa_completion(dfa_example)
    new_dfa=DFA.dfa_minimization(dfa_example)

    automata_IO.dfa_to_dot(new_dfa, 'output-name', '/PATH-OUT/')

See :doc:`modules` for the complete API explanation.

.. note::
    By design all the functions, except the predisposed one, will NOT return
    MINIMAL automata.

.. warning::
    States with the same name from different automata should not be considered
    the same entity. Avoid using automata with state names in common.
    When in doubt use `rename_X_states()` functions (where X=type of automaton)
    to rename the whole automaton states.

