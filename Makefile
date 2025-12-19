REPO ?= $(shell basename $(CURDIR))
TAG ?= latest

.PHONY: build docker-up run push

build:
	docker build -t $(REPO):$(TAG) .

docker-up:
	docker-compose up --build

run:
	python3 -m uvicorn src.app:app --host 0.0.0.0 --port 8000

push:
	@echo "Set DOCKER_REGISTRY and DOCKER_REPOSITORY env vars before pushing"
	docker build -t $(DOCKER_REGISTRY)/$(DOCKER_REPOSITORY):$(TAG) .
	docker push $(DOCKER_REGISTRY)/$(DOCKER_REPOSITORY):$(TAG)
