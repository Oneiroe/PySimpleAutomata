================
PySimpleAutomata
================

.. Overview

PySimpleAutomata is a Python library to manage Deterministic Finite Automata (DFA),
Nondeterministic Finite Automata(NFA) and Alternate Finite state automata on Word (AFW).

This library is not meant for performance nor space consumption optimization,
but for academic purposes:
*PySimpleAutomata aims to be an easily readable but working representation of automata theory*.

.. Disclaimer

This project has been developed for "Process and Service Modelling and Analysis" class
of Master of Science in Engineering in Computer Science from Sapienza University of Rome.

---------
Structure
---------

::

   /PySimpleAutomata
   |
   +---/PySimpleAutomata : Library sources
   |   |
   |   +--- AFW.py : Functions to handle AFWs automata.
   |   |
   |   +--- automata_IO.py : Functions of IN/OUTput for all the automata types.
   |   |
   |   +--- DFA.py : Functions to handle DFAs automata.
   |   |
   |   +--- NFA.py : Functions to handle NFAs automata.
   |
   +---/doc : Documentation sources
   |
   +---/tests : Unit testing and test-cases inputs


------------
Requirements
------------

The project is **Python3 only**, tested on Python 3.5 and 3.6.

`Graphviz - Graph Visualization Software <http://graphviz.org//>`_ is required to be installed and
present on system path to input/output dot files, while
Python packages `pydot <https://pypi.python.org/pypi/pydot/>`_ and
`graphviz <https://pypi.python.org/pypi/graphviz>`_ are used to handle them (respectively input and output).

`Sphinx <http://www.sphinx-doc.org//>`_ is used to generate the documentation.

`Unittest <https://docs.python.org/3/library/unittest.html>`_ for Unit testing.


------------
Installation
------------

From `PyPi <https://pypi.python.org/pypi>`_ using pip::

   pip install pysimpleautomata

From source::

   python setup.py install
   pip install -r requirements.txt

It is advised in any case to use a `Python Virtual environment <https://docs.python.org/3/tutorial/venv.html>`_ instead of a global installation.

-------------
Documentation
-------------

For a detailed explanation of the library API consult the `online documentation <http://pysimpleautomata.readthedocs.io/>`_
or `download it <https://readthedocs.org/projects/pysimpleautomata/downloads/>`_.

-------
Licence
-------

This code is provided under `MIT Licence <https://github.com/Oneiroe/PySimpleAutomata/blob/master/LICENSE>`_.
