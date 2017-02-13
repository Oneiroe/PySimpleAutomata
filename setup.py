from setuptools import setup
# from distutils.core import setup
import venv

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='PySimpleAutomata',
    version='1.0.0',
    packages=['tests'],
    url='www.github.com/Oneiroe/PySimpleAutomata/',
    license=license,
    author='Alessio Cecconi',
    author_email='alessio.cecconi.1991@gmail.com',
    description='Python library to manage DFA, NFA and AFW automata',
    long_description=readme,
    requires=['graphviz', 'pydot']
)
