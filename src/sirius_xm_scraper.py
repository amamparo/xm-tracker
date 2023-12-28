import json
from typing import List

from src.scraper import Scraper, get_page_props
from src.tidal import Tidal


class SiriusXmScraper(Scraper):
    def __init__(self, xm_playlist_url: str):
        self.__xm_playlist_url = xm_playlist_url

    def get_tidal_track_ids(self, tidal: Tidal) -> List[int]:
        page_props = get_page_props(self.__xm_playlist_url)
        tidal_track_ids = []
        for x in page_props['recent']:
            for track in x:
                tidal_link = next((link['url'] for link in track['links'] if link['site'] == 'tidal'), None)
                if tidal_link:
                    tidal_track_ids.append(int(tidal_link.split('/')[-1]))
        return tidal_track_ids
