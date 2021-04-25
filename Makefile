export APP_NAME=spaces-naumen-backend
export CURRENT_BRANCH = $(shell git symbolic-ref --short HEAD)

run:
	python3 main.py

install-dependencies:
	@pip3 install -r requirements.txt

build-docker:
	@docker build \
		-t ${APP_NAME}:${CURRENT_BRANCH} \
		.

run-docker:
	docker run -p 5000:5000 -d ${APP_NAME}:${CURRENT_BRANCH}

run-all:
	docker-compose up -d

down-all:
	docker-compose down