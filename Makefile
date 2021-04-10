.PHONY: setup env run run-mock run-docker test test-mock lint

include .env
SHELL := /bin/bash

setup:
	python3 -m venv mailboxfsvenv && \
	source mailboxfsvenv/bin/activate && \
	pip install -e maaf && \
	pip install -r requirements.txt

env:
	sed 's/^/export /' .env > .env.bash

run: env
	source .env.bash && CONTAINER_MAILS_DIR=$(HOST_MAILS_DIR) python -m maaf.mailbox_fs.main

run-mock:
	MOCK=True python -m mailbox_fs.main

run-docker:
	docker build -t maaf:latest maaf/
	-mkdir $(HOST_MAILS_DIR)
	docker run --rm -it\
		--env-file .env -e CONTAINER_MAILS_DIR=/app/mails -e ACCOUNT=$(ACCOUNT) \
		--mount type=bind,source=$(HOST_MAILS_DIR),target=/app/mails \
		maaf:latest
	rm -ri $(HOST_MAILS_DIR)

test: env
	source .env.bash && python -m pytest maaf/mailbox_fs/test_* -v

test-mock:
	MOCK=True python -m pytest maaf/mailbox_fs/test_* -v

lint:
	mypy --ignore-missing-imports maaf/
