Requirements
------------

The project is **Python3 only**, tested on Python 3.5 and 3.6.

`Graphviz - Graph Visualization Software <http://graphviz.org//>`_ is required to be installed and
present on system path to input/output DOT files.

Relevant Python packages (included in the installation):
    - `pydot <https://pypi.python.org/pypi/pydot/>`_ for DOT import;
    - `graphviz <https://pypi.python.org/pypi/graphviz>`_ for DOT export;
    - `Sphinx <http://www.sphinx-doc.org//>`_ for documentation generation;
    - `Unittest <https://docs.python.org/3/library/unittest.html>`_ for Unit testing.


Installation
------------

From `PyPi <https://pypi.python.org/pypi>`_ using pip::

    pip install pysimpleautomata

From source::

    python setup.py install
    pip install -r requirements.txt

It is advised in any case to use a `Python Virtual environment <https://docs.python.org/3/tutorial/venv.html>`_ instead of a global installation.

