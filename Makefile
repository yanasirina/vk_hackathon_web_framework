FLAKE8_CONFIG = .flake8
PYLINT_CONFIG = .pylintrc

.PHONY: lint
lint:
	@flake8 --append-config $(FLAKE8_CONFIG)
	@find . -type f -name "*.py" -not -path "./.venv/*" | xargs pylint --rcfile $(PYLINT_CONFIG)
	@find . -type f -name "*.py" -not -path "./.venv/*" | xargs mypy

.PHONY: docker-build
docker-build:
	@docker build -t web-playground .

.PHONY: docker-play
docker-play:
	@docker run --rm -p 8080:8080 --name web-playground-container web-playground

.PHONY: docker-run
docker-run: docker-build docker-play

.PHONY: docker-test
docker-test:
	@docker run --rm -p 8080:8080 -v $(shell pwd):/app --name web-playground-container web-playground coverage run -m pytest .

.PHONY: docker-test-report
docker-test-report:
	@docker run --rm -p 8080:8080 -v $(shell pwd):/app --name web-playground-container web-playground coverage report -m --include="*.py"

.PHONY: build
build:
	@pip install -e .

.PHONY: play
play:
	@python3 playground/main.py

.PHONY: deps
deps:
	@pip install -r requirements.txt
