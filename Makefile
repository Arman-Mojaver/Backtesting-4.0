SHELL = /bin/bash

# Dev tools

ruff:
	ruff check

ruff-f:
	ruff format

mypy:
	mypy .