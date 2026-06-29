VENV = env #virtual environment 
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip #used for installing packages
CONFIG = config.txt


install:
	python -m venv $(VENV)
	$(PIP) install -e .
	$(PIP) install flake8 mypy

run:
	$(PYTHON) draw_maze.py $(CONFIG)

debug:
	$(PYTHON) -m pdb draw_maze.py $(CONFIG)

clean:
	rm -rf __pycache__ mazegen/__pycache__ .mypy_cache $(VENV) maze.txt #deleting env and cache files

lint: #check code style and type hints
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: #strict setting checking
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict