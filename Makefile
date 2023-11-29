.PHONY: help
help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  run        Start bot"
	@echo "  rd         Start bot dependencies"
	@echo "  stop       Stop bot"
	@echo "  test       Run tests"
	@echo "  lint       Run ruff"
	@echo "  logs       Show logs"
	@echo "  freeze     Make requirements.txt"
	@echo "  reqs       Show requirements"
	@echo "  generate   Generate migration"
	@echo "  migrate    Run migrations"
	@echo "  upgrade    Upgrade pip"
	@echo "  venv       Create virtual environment"

.PHONY: venv
venv:
	python -m venv venv
	pip install -r requirements.txt

.PHONY: upgrade
upgrade:
	python.exe -m pip install --upgrade pip

.PHONY: run
run:
	docker-compose up -d --build

.PHONY: stop
stop:
	docker-compose stop

.PHONY: rd
rd:
	docker-compose stop bot
	docker-compose up -d db redis scheduler

.PHONY: logs
logs:
	docker logs secrets-bot-1

.PHONY: test
test:
	make rd
	pytest -s -v

.PHONY: lint
lint:
	ruff src

.PHONY: freeze
freeze:
	pip freeze > requirements.txt

.PHONY: reqs
reqs:
	pip freeze

.PHONY: generate
generate:
	alembic revision --autogenerate

.PHONY: migrate
migrate:
	alembic upgrade head
