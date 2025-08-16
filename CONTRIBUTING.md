# Contributing

Thanks for helping to improve the ualf parser!

## Setup
- Python 3.9-3.13 supported
- Create a virtualenv and install dependencies:

```sh
pip install -e .[pandas]
```

## Tests
- Run unit tests:

```sh
python -m unittest discover -s tests -p "test_*py" -v
```

## Lint & Types

```sh
pip install ruff mypy
ruff check .
mypy ualf
```

## Release (maintainers)
- Bump `__version__` in `ualf/__init__.py`
- Create a tag `vX.Y.Z`
- CI will build and publish to PyPI using `PYPI_API_TOKEN`

## Principles
- Keep runtime deps small
- Use type hints; `py.typed` is included
- Small, focused PRs with tests
