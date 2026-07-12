.PHONY: install migrate seed test run lint format

install:
	pip install -r requirements.txt

migrate:
	python manage.py migrate

seed:
	python manage.py seed_data

test:
	pytest -v

run:
	python manage.py runserver

lint:
	flake8 .

format:
	black .

check: format lint test
