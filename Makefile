APP_NAME = app
TESTS_PATH = tests

.PHONY: run
run:
	docker-compose up db -d
	uvicorn $(APP_NAME):app --host 0.0.0.0 --port 8000 --reload

.PHONY: up
up:
	docker-compose up --build -d

.PHONY: up-prod
up-prod:
	docker-compose -f docker-compose.yml -f docker-compose-prod.yml up --build -d

.PHONY: psql
psql:
	docker-compose exec -it db psql -U postgres -d app

.PHONY: logs
logs:
	docker-compose logs --since 10m --follow

.PHONY: stop
stop:
	docker-compose stop

.PHONY: restart
restart:
	docker-compose restart

.PHONY: format
format:
	ruff format $(APP_NAME) $(TESTS_PATH)

.PHONY: lint
lint:
	ruff check $(APP_NAME) $(TESTS_PATH) --fix
	mypy $(APP_NAME) --install-types --enable-incomplete-feature=NewGenericSyntax

PHONY: generate
generate:
	docker-compose up db -d
	alembic revision --autogenerate

PHONY: upgrade
upgrade:
	docker-compose up db -d
	alembic upgrade head

PHONY: downgrade
downgrade:
	docker-compose up db -d
	alembic downgrade -1

PHONY: test
test:
	docker-compose up db -d
	pytest $(TESTS_PATH) -s -v

# Windows only
PHONY: kill
kill:
	TASKKILL /F /IM python.exe
