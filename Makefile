.PHONY: install test lint reproduce clean

install:
	python3 -m pip install -e ".[dev]"

test:
	python3 -m pytest

lint:
	python3 -m ruff check .

reproduce:
	python3 scripts/reproduce_table1.py --quick

clean:
	rm -rf build dist .pytest_cache .ruff_cache src/*.egg-info
