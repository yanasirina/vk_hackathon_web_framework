.PHONY: build
build:
	@pip install -e .

.PHONY: play
play:
	@python3 playground/main.py

.PHONY: deps
deps:
	@pip install -r requirements.txt

.PHONY: docker-build
docker-build:
	@docker build -t web-playground .

.PHONY: docker-play
docker-play:
	@docker run --rm -p 8080:8080 --name web-playground-container web-playground

.PHONY: docker-run
docker-run: docker-build docker-play
