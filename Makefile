.PHONY: install test lint example reproduce clean

install:
	python3 -m pip install -e ".[dev]"

test:
	python3 -m pytest

lint:
	python3 -m ruff check .

example:
	python3 -m bg_pricing --steps 3 --branches 3 --replications 100 --seed 42

reproduce:
	python3 scripts/reproduce_table1.py --branches 10 --replications 20

clean:
	rm -rf build dist .pytest_cache .ruff_cache src/*.egg-info
