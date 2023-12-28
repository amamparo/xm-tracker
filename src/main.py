from os import environ

from dotenv import load_dotenv

from src.scrape_config import scrape_configs
from src.tidal import Tidal

load_dotenv()


def main():
    tidal = Tidal(environ.get('TIDAL_REFRESH_TOKEN'))
    for config in scrape_configs:
        tidal.add_playlist_tracks(config.tidal_playlist_id, config.scraper.get_tidal_track_ids(tidal))


if __name__ == '__main__':
    main()
