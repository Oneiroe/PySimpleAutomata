Automata representation
-----------------------

For transparency, the automata are represented with Built-in Types
instead of an object structure.
More precisely an automata is a `dict <https://docs.python.org/3.6/library/stdtypes.html#mapping-types-dict>`_
with the following keys <'alphabet', 'states', 'initial_state(s)', 'accepting_states', 'transitions' >
which mapping vary depending on the specific automata type.

.. note::

    Being not a fixed object is up to the user to ensure the correctness of the data.




