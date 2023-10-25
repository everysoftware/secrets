.PHONY: generate
generate:
	alembic revision --m="$(NAME)" --autogenerate

.PHONY: migrate
migrate:
	alembic upgrade head
