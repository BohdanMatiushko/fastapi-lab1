.PHONY: up up-d build rebuild down restart logs shell clean-cache clean-all

up:
	docker compose up

up-d:
	docker compose up -d

build:
	docker compose build

rebuild:
	docker compose build --no-cache
	docker compose up

down:
	docker compose down

restart:
	docker compose down
	docker compose up

logs:
	docker compose logs -f

shell:
	docker compose exec api sh

clean-cache:
	docker builder prune -f

clean-all:
	docker system prune -af