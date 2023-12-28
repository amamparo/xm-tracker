install:
	poetry install

sirius_xm_stations:
	poetry run python -m src.scrape_sirius_xm_stations

token:
	poetry run python -m src.create_tidal_token

lint:
	poetry run pylint src tests

test:
	poetry run python -m unittest discover -s 'tests' -p '*.py'

deploy:
	cdk deploy --require-approval never --verbose