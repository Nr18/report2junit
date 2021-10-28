SHELL = /bin/bash -c
VIRTUAL_ENV = $(shell poetry env info --path)
export BASH_ENV=$(VIRTUAL_ENV)/bin/activate

.PHONY: lint test install clean run release

lint: _black _mypy

test: lint
	pytest --cov --cov-report term-missing

install: $(VIRTUAL_ENV)
	poetry install
	pre-commit install

clean:
	[[ -d "$(VIRTUAL_ENV)" ]] && rm -rf "$(VIRTUAL_ENV)" || true
	[[ -d .mypy_cache ]] && rm -rf .mypy_cache || true
	[[ -d .pytest_cache ]] && rm -rf .pytest_cache || true
	[[ -d dist ]] && rm -rf dist || true
	[[ -d reports ]] && rm -rf reports || true
	[[ -d report2junit/report2junit.egg-info ]] && rm -rf report2junit/report2junit.egg-info || true
	[[ -f .coverage ]] && rm .coverage || true

run:
	report2junit --source-type cfn-guard ./sample-reports/cfn-guard.json
	report2junit --source-type cfn-nag ./sample-reports/cfn-nag.json

release:
	python setup.py sdist
	twine upload dist/*

.PHONY: _black _mypy

_black:
	$(info [*] Formatting python files...)
	black .

_mypy:
	$(info [*] Python static type checker...)
	mypy --junit-xml reports/typecheck.xml report2junit
#--cobertura-xml-report reports
# --html-report reports

$(VERBOSE).SILENT:
