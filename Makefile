export SHELL := /bin/bash

test:
	pytest -n auto --doctest-modules my_code_base

coverage:
	pytest -n auto --doctest-modules --cov=seaborn --cov-config=.coveragerc my_code_base

lint:
	flake8 my_code_base
