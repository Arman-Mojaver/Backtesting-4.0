SHELL = /bin/bash

.PHONY: bash strategy run logs cov pytest gotest tests up in ing down clean ps status build build-go build-no-cache push pull ruff ruff-f mypy alembic-upgrade alembic-downgrade freeze pyupgrade db-development db-production db-development-size db-production-size



# Dev tools
bash:
	docker compose -f docker-compose.yaml run --rm -it -v ~/.bash_history:/root/.bash_history api bash

strategy:
	docker compose -f docker-compose.yaml run --rm -it -v ~/.bash_history:/root/.bash_history strategy bash

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

pytest:
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app api /bin/bash -c \
	"python -m pytest"


gotest:
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD)/go_context:/app strategy /bin/bash -c \
	"go test ./... -v"


tests: pytest gotest



# Docker commands
up:
	docker compose -f docker-compose.yaml up -d

in:
	docker compose -f docker-compose.yaml exec -it api /bin/bash

ing:
	docker compose -f docker-compose.yaml exec -it strategy /bin/bash

down:
	docker compose -f docker-compose.yaml down

clean: down

ps:
	docker compose ps

status: ps



# Docker image commands
build:
	docker image build -t armanmojaver/backtesting-api:latest .
	docker image build -t armanmojaver/backtesting-strategy:latest ./go_context

build-go:
	docker image build -t armanmojaver/backtesting-strategy:latest ./go_context

build-no-cache:
	docker image build --no-cache -t armanmojaver/backtesting-api:latest .
	docker image build --no-cache -t armanmojaver/backtesting-strategy:latest ./go_contex


push:
	cat .docker_password | docker login --username armanmojaver --password-stdin
	docker push armanmojaver/backtesting-api:latest
	docker push armanmojaver/backtesting-strategy:latest


pull:
	cat .docker_password | docker login --username armanmojaver --password-stdin
	docker pull armanmojaver/backtesting-api:latest
	docker pull armanmojaver/backtesting-strategy:latest



# Linting
ruff:
	ruff check

ruff-f:
	ruff format

mypy:
	mypy . --ignore-missing-imports --implicit-reexport --check-untyped-defs



# Alembic
alembic-upgrade:
	export ENVIRONMENT=development && \
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app api /bin/bash -c \
	"alembic upgrade head"

	export ENVIRONMENT=production && \
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app api /bin/bash -c \
	"alembic upgrade head"


alembic-downgrade:
	export ENVIRONMENT=development && \
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app api /bin/bash -c \
	"alembic downgrade -1"

	export ENVIRONMENT=production && \
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app api /bin/bash -c \
	"alembic downgrade -1"



# Other commands
freeze:
	pip freeze | grep -v "bt_cli" > requirements.txt

pyupgrade:
	pyup_dirs . --py313-plus --recursive



# DB
db-development:
	docker compose -f docker-compose.yaml exec -it db-development sh -c \
	"psql -U postgres"

db-production:
	docker compose -f docker-compose.yaml exec -it db-production sh -c \
	"psql -U postgres"

db-development-size:
	docker compose -f docker-compose.yaml exec -it db-development sh -c \
	"psql -U postgres -c \"SELECT pg_size_pretty(pg_database_size('db-development'));\""

db-production-size:
	docker compose -f docker-compose.yaml exec -it db-production sh -c \
	"psql -U postgres -c \"SELECT pg_size_pretty(pg_database_size('db-production'));\""
