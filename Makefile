SHELL = /bin/bash


# Dev tools

bash:
	docker compose -f docker-compose.yaml run --rm -it -v ~/.bash_history:/root/.bash_history api bash

logs:
	docker compose logs --tail=100 -f



# Docker commands

up:
	docker compose -f docker-compose.yaml up -d && docker compose -f docker-compose.yaml exec -it api /bin/bash

down:
	docker compose -f docker-compose.yaml down

clean: down

ps:
	docker compose ps

status: ps



# Linting

ruff:
	ruff check

ruff-f:
	ruff format

mypy:
	mypy . --ignore-missing-imports
