docker-image:
	docker build -f ./Dockerfile -t "careapp:latest" .
.PHONY: docker-image

docker-compose-up: docker-image
	docker compose -f ./docker-compose.yml up --build -d
.PHONY: docker-compose-up

docker-compose-down:
	docker compose -f ./docker-compose.yml stop -t 1
	docker compose -f ./docker-compose.yml down
.PHONY: docker-compose-down

docker-compose-logs:
	docker compose -f ./docker-compose.yml logs -f
.PHONY: docker-compose-logs