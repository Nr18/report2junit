SHELL = /bin/bash -c
VIRTUAL_ENV = $(shell poetry env info --path)
export BASH_ENV=$(VIRTUAL_ENV)/bin/activate

.PHONY: lint test install clean run build release complexity

lint: _black _mypy

test: lint complexity
	pytest --cov --mypy --cov-report term-missing --junitxml=reports/pytest.xml --cov-report xml:reports/coverage.xml

install: $(VIRTUAL_ENV)
	poetry install

clean:
	[[ -d "$(VIRTUAL_ENV)" ]] && rm -rf "$(VIRTUAL_ENV)" || true
	[[ -d .mypy_cache ]] && rm -rf .mypy_cache || true
	[[ -d .pytest_cache ]] && rm -rf .pytest_cache || true
	[[ -d dist ]] && rm -rf dist || true
	[[ -d reports ]] && rm -rf reports || true
	[[ -d report2junit/report2junit.egg-info ]] && rm -rf report2junit/report2junit.egg-info || true
	[[ -f .coverage ]] && rm .coverage || true

run:
	report2junit --ignore-failures ./sample-reports/cfn-guard.json ./sample-reports/cfn-nag.json

build:
	python setup.py sdist

release: build
	twine upload dist/*

complexity:
	$(info Maintenability index)
	radon mi --min A --max A --show --sort report2junit
	$(info Cyclomatic complexity index)
	xenon --max-absolute A --max-modules A --max-average A report2junit

.PHONY: _black _mypy

_black:
	$(info [*] Formatting python files...)
	black .

_mypy:
	$(info [*] Python static type checker...)
	mypy --junit-xml reports/typecheck.xml report2junit

$(VERBOSE).SILENT:
