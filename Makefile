SHELL = /bin/bash

.PHONY: help bash run logs cov pytest tests up in down ps \
        build build-rust build-no-cache push pull ruff format fmt mypy pyupgrade \
        alembic-upgrade alembic-downgrade freeze timer clean-flower db-development \
        db-production db-size db-dump db-load db-dump-development db-load-development \
        server

.DEFAULT_GOAL := help



help: ## Show this help message
	@echo "Available targets:"
	@grep -E '(^[a-zA-Z_-]+:.*?##|^# [A-Za-z])' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; \
	/^# / {printf "\n%s\n", substr($$0, 3); next} \
	{printf "  %-20s %s\n", $$1, $$2}'



# Dev tools
bash:  ## Start a bash shell in api container
	docker compose -f docker-compose.yaml run --rm -it -v ~/.bash_history:/root/.bash_history -v $(PWD):/app api bash

run:  ## Run run_script.py file in api container
	docker compose -f docker-compose.yaml run --rm -it \
	-v ~/.bash_history:/root/.bash_history api /bin/bash -c \
	"python run_script.py"

logs:  ## Display docker-compose logs
	docker compose logs --tail=100 -f



# Tests
cov:  ## Run tests and make coverage report
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app api /bin/bash -c \
	"pytest --cov --cov-report html:coverage/html" \
	&& open coverage/html/index.html

pytest:  ## Run pytest
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app api /bin/bash -c \
	"python -m pytest tests/pure -n 4 && pytest tests/other"



# Docker commands
up:  ## Start containers
	docker compose -f docker-compose.yaml up -d

in:  ## Start a bash shell in started api container
	docker compose -f docker-compose.yaml exec -it api /bin/bash

down:  ## Remove containers
	docker compose -f docker-compose.yaml down

ps:  ## Display containers
	docker compose ps



# Docker image commands
build:  ## Build images (python + rust)
	docker image build -t armanmojaver/backtesting-api:latest .
	docker image build -t armanmojaver/rust-http:latest ./rust_http

build-rust:  ## Build rust image
	docker image build -t armanmojaver/rust-http:latest ./rust_http

build-no-cache:  ## Build images, no cache (python + rust)
	docker image build --no-cache -t armanmojaver/backtesting-api:latest .
	docker image build --no-cache -t armanmojaver/rust-http:latest ./rust_http

push:  ## Push images (python + rust)
	cat .docker_password | docker login --username armanmojaver --password-stdin
	docker push armanmojaver/backtesting-api:latest
	docker push armanmojaver/rust-http:latest

pull:  ## Pull images (python + rust)
	cat .docker_password | docker login --username armanmojaver --password-stdin
	docker pull armanmojaver/backtesting-api:latest
	docker push armanmojaver/rust-http:latest



# Linting
ruff:  ## Run ruff check
	ruff check

format:  ## Run ruff format
	ruff format

fmt:  ## Run rust formatter
	cd $(PWD)/rust_http && cargo fmt

mypy: ## Run mypy
	mypy . --ignore-missing-imports --implicit-reexport --check-untyped-defs

pyupgrade: ## Run pyupgrade
	pyup_dirs . --py313-plus --recursive



# Alembic
alembic-upgrade:  ## Run alembic upgrades (development + production)
	export ENVIRONMENT=development && \
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app api /bin/bash -c \
	"alembic upgrade head"

	export ENVIRONMENT=production && \
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app api /bin/bash -c \
	"alembic upgrade head"


alembic-downgrade:  ## Run alembic downgrade -1 (development + production)
	export ENVIRONMENT=development && \
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app api /bin/bash -c \
	"alembic downgrade -1"

	export ENVIRONMENT=production && \
	docker compose -f docker-compose.yaml run --rm -it -v $(PWD):/app api /bin/bash -c \
	"alembic downgrade -1"



# Other commands
freeze:  ## Run pip freeze (requirements.txt)
	pip freeze | grep -v "bt_cli" > requirements.txt

timer: ## Run timer (Goes to sleep after 10 mins of inactivity)
	sudo python utils/timer.py

clean-flower: ## Delete current task existing in flower and restart service
	rm -r compose/flower/flower_data
	docker compose restart flower


# DB
db-development:  ## Start a bash shell in db-development
	docker compose -f docker-compose.yaml exec -it db-development sh -c \
	"psql -U postgres"

db-production:  ## Start a bash shell in db-production
	docker compose -f docker-compose.yaml exec -it db-production sh -c \
	"psql -U postgres"

db-size:  ## Get size of db-development and db-production
	@echo "db-development"
	docker compose -f docker-compose.yaml exec -it db-development sh -c \
	"psql -U postgres -c \"SELECT pg_size_pretty(pg_database_size('db-development'));\""

	@echo "db-production"
	docker compose -f docker-compose.yaml exec -it db-production sh -c \
	"psql -U postgres -c \"SELECT pg_size_pretty(pg_database_size('db-production'));\""


db-dump:  ## Dump the production database to a custom format file
	./scripts/db.sh dump production

db-load:  ## Load the dump back into the production database
	./scripts/db.sh load production

db-dump-development:  ## Dump the development database to a custom format file
	./scripts/db.sh dump development

db-load-development:  ## Load the dump back into the development database
	./scripts/db.sh load development
