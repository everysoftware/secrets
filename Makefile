SOURCE_PATH = src
TEST_PATH = tests
APP = src.main:app
API_HOST = localhost
API_PORT = 8000

.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  run-dev         Start api in development mode"
	@echo "  run-prod        Start api in production mode"
	@echo "  run-deps        Start dependencies"
	@echo "  test            Run tests"
	@echo "  lint            Lint project"
	@echo "  format          Format project"
	@echo "  freeze          Make requirements.txt"
	@echo "  generate        Generate migration"
	@echo "  migrate         Run migrations"
	@echo "  pip             Upgrade pip"
	@echo "  venv            Create virtual environment"
	@echo "  help            Show this message"

.PHONY: venv
venv:
	powershell -Command "venv/Scripts/activate; pip install -r requirements.txt"

PHONY: pip
pip:
	python -m pip install --upgrade pip

.PHONY: run-deps
run-deps:
	docker-compose up -d

PHONY: run-dev
run-dev:
	@echo "Run dependencies"
	make run-deps
	@echo "Run api"
	uvicorn $(APP) --host $(API_HOST) --port $(API_PORT) --reload

PHONY: run-prod
run-prod:
	docker-compose -f docker-compose.yml -f docker-compose-prod.yml up -d --build

PHONY: kill
kill:
	TASKKILL /F /IM python.exe

PHONY: stop-prod
stop-prod:
	docker-compose -f docker-compose.yml -f docker-compose-prod.yml stop

PHONY: lint
lint:
	ruff --fix $(SOURCE_PATH) $(TEST_PATH)
	mypy $(SOURCE_PATH) $(TEST_PATH)

PHONY: format
format:
	black $(SOURCE_PATH) $(TEST_PATH)

PHONY: test
test:
	@echo "Format project"
	make format
	@echo "Lint project"
	make lint
	@echo "Run dependencies"
	make run-deps
	@echo "Run tests"
	pytest -s -v

PHONY: freeze
freeze:
	pip freeze > requirements.txt

PHONY: generate
generate:
	make run-deps
	alembic revision --autogenerate

PHONY: migrate
migrate:
	make run-deps
	alembic upgrade head
