from setuptools import setup, find_packages

# from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='PySimpleAutomata',
    version='0.1.1',
    author='Alessio Cecconi',
    author_email='alessio.cecconi.1991@gmail.com',
    url='https://github.com/Oneiroe/PySimpleAutomata',
    license=license,
    description='Python library to manage DFA, NFA and AFW automata',
    long_description=readme,
    packages=find_packages(exclude=['doc', 'tests']),
    requires=['graphviz', 'pydot'],
    data_files=[("", ["LICENSE"])],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='automata DFA NFA AFW',
)

