.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  run             Start backend"
	@echo "  run-deps        Start dependencies"
	@echo "  run-deps-alone  Start dependencies with stopping backend"
	@echo "  stop            Stop backend"
	@echo "  test            Run tests"
	@echo "  lint            Lint project"
	@echo "  format          Format project"
	@echo "  logs            Show logs"
	@echo "  freeze          Make requirements.txt"
	@echo "  generate        Generate migration"
	@echo "  migrate         Run migrations"
	@echo "  upgrade         Upgrade pip"
	@echo "  venv            Create virtual environment"

.PHONY: venv
venv:
	python -m venv venv
	@echo "Requirements installation is not implemented"

.PHONY: upgrade
upgrade:
	python.exe -m pip install --upgrade pip

.PHONY: run-deps
run-deps:
	docker-compose up -d db redis

.PHONY: run-deps-alone
run-deps-alone:
	@echo "Stop api"
	make stop
	@echo "Running dependencies"
	make run-deps

.PHONY: run
run:
	@echo "Run dependencies"
	make run-deps
	@echo "Run api"
	@echo "Not implemented"

.PHONY: stop
stop:
	docker-compose stop

.PHONY: logs
logs:
	@echo "Not implemented"

.PHONY: test
test:
	@echo "Lint project"
	make lint
	@echo "Run mypy"
	make mypy
	@echo "Run dependencies"
	make run-deps
	@echo "Run tests"
	pytest -s -v

.PHONY: lint
lint:
	ruff backend tests
	mypy backend tests

.PHONY: format
format:
	ruff format backend tests

.PHONY: freeze
freeze:
	pip freeze > requirements.txt

.PHONY: generate
generate:
	make run-deps-alone
	$Env:PYTHONPATH = "backend"
	alembic revision --autogenerate

.PHONY: migrate
migrate:
	make run-deps-alone
	$Env:PYTHONPATH = "backend"
	alembic upgrade head
