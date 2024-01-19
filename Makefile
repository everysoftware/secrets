SOURCEPATH = backend
TESTPATH = tests
APP = backend.interfaces.rest.app:app
API_HOST = 0.0.0.0
API_PORT = 8000
CELERY_APP = backend.infrastructure.tasks.app

.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  run             Start api"
	@echo "  run-prod        Start api in production mode"
	@echo "  run-deps        Start dependencies"
	@echo "  test            Run tests"
	@echo "  lint            Lint project"
	@echo "  format          Format project"
	@echo "  logs            Show logs"
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

PHONY: celery
celery:
	set PYTHONPATH=$(SOURCEPATH) && celery -A $(CELERY_APP) worker --loglevel=info --pool=solo

PHONY: flower
flower:
	set PYTHONPATH=$(SOURCEPATH) && celery -A $(CELERY_APP) flower

.PHONY: run-deps
run-deps:
	docker-compose up -d

PHONY: run
run:
	@echo "Run dependencies"
	make run-deps
	@echo "Run api"
	set PYTHONPATH=$(SOURCEPATH) && uvicorn $(APP) --host $(API_HOST) --port $(API_PORT) --reload

PHONY: run-prod
run-prod:
	docker-compose -f docker-compose.yml -f docker-compose-prod.yml up --build

PHONY: logs
logs:
	@echo "Not implemented"

PHONY: lint
lint:
	ruff --fix $(SOURCEPATH) $(TESTPATH)
	mypy $(SOURCEPATH) $(TESTPATH)

PHONY: format
format:
	black $(SOURCEPATH) $(TESTPATH)

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
	set PYTHONPATH=$(SOURCEPATH) && alembic revision --autogenerate

PHONY: migrate
migrate:
	make run-deps
	set PYTHONPATH=$(SOURCEPATH) && alembic upgrade head
