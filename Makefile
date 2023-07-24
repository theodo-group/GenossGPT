########################################################################################################################
# Quality checks
########################################################################################################################

test:
	poetry run pytest tests --cov genoss --cov-report term --cov-report=html --cov-report xml --junit-xml=tests-results.xml

black:
	poetry run black . --check

ruff:
	poetry run ruff check genoss tests

fix-ruff:
	poetry run ruff check genoss tests --fix

mypy:
	poetry run mypy genoss

########################################################################################################################
# Api
########################################################################################################################

start-api:
	docker compose up -d

run:
	docker build -t genoss .
	docker run -it --rm -p 4321:4321 genoss
