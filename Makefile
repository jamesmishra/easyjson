POETRY?=poetry
PYTHON_PACKAGES?=easyjson tests


help:
	echo HELP
.PHONY: help


TEST_ARGS?=
test:
	$(POETRY) run python3 -m unittest $(TEST_ARGS)
.PHONY: test


ruff:
	$(POETRY) run ruff check
.PHONY: test


mypy:
	$(POETRY) run mypy --strict $(PYTHON_PACKAGES)
.PHONY: mypy


lint: ruff mypy
.PHONY: lint


ruff-fix:
	$(POETRY) run ruff check --fix
.PHONY: ruff-fix


isort:
	$(POETRY) run isort .
.PHONY: isort


fmt: isort ruff-fix
.PHONY: fmt
