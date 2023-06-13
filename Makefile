

docker-image:
	docker build -f ./Dockerfile -t "careapp:latest" .
.PHONY: docker-image

docker-compose-up: docker-image
	docker compose -f ./docker-compose.yml up --build -d postgres
	sleep 5
	@cat dumps/dump_13-06-2023_20_11_24.sql | docker exec -i 7544-aycdpi1-tp-postgres-1 psql -U postgres > /dev/null
	docker compose -f ./docker-compose.yml up --build -d app
.PHONY: docker-compose-up

docker-compose-down:
	docker compose -f ./docker-compose.yml stop -t 1
	docker compose -f ./docker-compose.yml down
.PHONY: docker-compose-down

docker-compose-logs:
	docker compose -f ./docker-compose.yml logs -f
.PHONY: docker-compose-logs