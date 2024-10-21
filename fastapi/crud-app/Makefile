# Makefile
.PHONY: install run-dev run-prod test

install:
	pip install -r requirements.txt

run-dev:
	ENV=dev uvicorn main:app --reload

run-prod:
	ENV=prod gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

test:
	pytest