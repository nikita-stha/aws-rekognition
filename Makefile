SHELL :=/bin/bash
CWD := $(PWD)
TMP_PATH := $(CWD)/.tmp
VENV_PATH := $(CWD)/.venv

.PHONY: clean
## Clean the pycache folder and pyc files.
clean:
	@rm -rf $(TMP_PATH) ./**/*.pyc __pycache__ **/__pycache__ .pytest_cache
	@find . -name '*.pyc' -delete

.PHONY: venv
## Create virtual environment for python.
venv:
	@virtualenv -p python3 $(VENV_PATH)

.PHONY: setup
## Setup the application by installing the packages.
setup:
	@pip install -U -e ./requirements.txt

.PHONY: format
## Format the code.
format:
	@black ./utils
	@black ./cli.py
	@black ./main.py

.PHONY: check
## Check the code.
check:
	@black --check --diff ./utils
	@black --check --diff ./cli.py
	@black --check --diff ./main.py

.DEFAULT_GOAL := help