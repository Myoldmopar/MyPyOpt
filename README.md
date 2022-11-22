# MyPyOpt
Python version of my simple optimization app from school

## Documentation [![](https://readthedocs.org/projects/mypyopt/badge/?version=latest)](http://mypyopt.readthedocs.org/en/latest/)

Documentation is hosted on [ReadTheDocs](http://mypyopt.readthedocs.org/en/latest/).  
The docs are completely bare right now.  
To build the documentation, enter the docs/ subdirectory and execute `make html`; then open `/docs/_build/html/index.html` to see the documentation.
In addition to that documentation, the repo contains a set of demos to show off how the library can be used.

## Testing

[![Flake8](https://github.com/Myoldmopar/MyPyOpt/actions/workflows/flake8.yml/badge.svg)](https://github.com/Myoldmopar/MyPyOpt/actions/workflows/flake8.yml)
[![Run Tests](https://github.com/Myoldmopar/MyPyOpt/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/Myoldmopar/MyPyOpt/actions/workflows/unit_tests.yml)

The source is tested using the python unittest framework.  To execute all the unit tests, just run `nosetests` from the project root.

## Installation

GitHub Actions is used to package up each release into a wheel and post on PyPi here: https://pypi.org/project/my-py-opt/.
Therefore it can be installed using `pip install my-py-opt`.
