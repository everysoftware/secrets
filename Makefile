.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  run             Start"
	@echo "  run-bot         Start bot"
	@echo "  run-api         Start api"
	@echo "  run-deps        Start dependencies"
	@echo "  run-deps-alone  Start dependencies without bot and api"
	@echo "  stop            Stop all"
	@echo "  test            Run tests"
	@echo "  enhance         Enhance code (lint, format, mypy, isort)"
	@echo "  lint            Run ruff"
	@echo "  format          Run black"
	@echo "  mypy            Run mypy"
	@echo "  isort           Run isort"
	@echo "  logs            Show logs"
	@echo "  freeze          Make requirements.txt"
	@echo "  generate        Generate migration"
	@echo "  migrate         Run migrations"
	@echo "  upgrade         Upgrade pip"
	@echo "  venv            Create virtual environment"

.PHONY: venv
venv:
	python -m venv venv
	pip install -r requirements.txt

.PHONY: upgrade
upgrade:
	python.exe -m pip install --upgrade pip

.PHONY: run-deps
run-deps:
	@echo "Running dependencies"
	docker-compose up -d db redis scheduler

.PHONY: run-deps-alone
run-deps-alone:
	@echo "Running dependencies alone"
	@echo "Stop bot"
	docker-compose stop bot
	@echo "Stop api"
	make run-deps

.PHONY: run-bot
run-bot:
	make run-deps
	@echo "Running bot"
	docker-compose build bot
	docker-compose up -d bot

.PHONY: run-api
run-api:
	make run-deps
	@echo "Running api"

.PHONY: stop
stop:
	docker-compose stop

.PHONY: logs
logs:
	docker logs secrets-bot-1

.PHONY: test
test:
	make run-deps
	pytest -s -v

.PHONY: lint
lint:
	ruff app

.PHONY: format
format:
	black app

.PHONY: mypy
mypy:
	mypy app

.PHONY: isort
isort:
	isort app

.PHONY: enhance
enhance:
	make format
	make isort
	make lint
	make mypy

.PHONY: freeze
freeze:
	pip freeze > requirements.txt

.PHONY: generate
generate:
	alembic revision --autogenerate

.PHONY: migrate
migrate:
	alembic upgrade head
