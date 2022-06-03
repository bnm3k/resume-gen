# =============================================================================
.DEFAULT_GOAL:=help
.SILENT:
SHELL:=/usr/bin/bash


# =============================================================================
# 			DEV
# =============================================================================
#
PROJECT_NAME=resume
VENV_DIR:=.venv
VENV_BIN:=.venv/bin/
ACTIVATE:=source .venv/bin/activate &&

.PHONY: help setup venv run lint format test build pre-commit coverage

help:
	echo -e "\nResume generator. Run make gen to generate resume\n"

venv:
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)

setup:
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	poetry install
	$(VENV_BIN)pre-commit install

build/resume.html: resume/resume.md resume/generate.py resume/style.css
	python resume/generate.py -d build

gen: build/resume.html

refresh: gen
	./refresh/reload-browser Firefox

watch: gen
	firefox build/resume.html
	ls resume/* | entr -c make refresh

lint:
	flake8 --show-source .
	bandit -q -r -c "pyproject.toml" .

format:
	black .

test:
	pytest

build:
	poetry build -q

pre-commit:
	pre-commit run --all-files

clean:
	rm -rf $(VENV_DIR) build/*
	find . -type d -name '__pycache__' -exec rm -rf {} +
# =============================================================================
