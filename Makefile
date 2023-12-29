install:
	poetry install

stations:
	poetry run python -m src.scrape_stations

now_playing:
	poetry run python -m src.scrape_now_playing

top_tracks_api:
	poetry run python -m src.top_tracks_api

token:
	poetry run python -m src.create_tidal_token

lint:
	poetry run pylint src tests

test:
	poetry run python -m unittest discover -s 'tests' -p '*.py'

deploy:
	cdk deploy --require-approval never

sync:
	./sync_s3.sh