SHELL = /bin/bash

.PHONY: bash run logs cov up down clean ps status ruff ruff-f mypy freeze

# Dev tools

bash:
	docker compose -f docker-compose.yaml run --rm -it -v ~/.bash_history:/root/.bash_history api bash

run:
	docker compose -f docker-compose.yaml run --rm -it \
	-v ~/.bash_history:/root/.bash_history api /bin/bash -c \
	"python run_script.py"

logs:
	docker compose logs --tail=100 -f


# Tests

cov:
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app api /bin/bash -c \
	"pytest --cov --cov-report html:coverage/html" \
	&& open coverage/html/index.html




# Docker commands

up:
	docker compose -f docker-compose.yaml up -d && \
	docker compose -f docker-compose.yaml exec -it api /bin/bash

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


# Other commands
freeze:
	pip freeze | grep -v "bt_cli" > requirements.txt
