import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Set, Optional, List

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from src.tidal import Tidal


@dataclass
class ScrapedTrack:
    title: str
    artists: Set[str]
    version: Optional[str]


class Scraper(ABC):
    @abstractmethod
    def get_tidal_track_ids(self, tidal: Tidal) -> List[int]:
        pass


def get_page_props(url: str) -> dict:
    response = requests.get(url, timeout=30, headers={'User-Agent': UserAgent().random})
    soup = BeautifulSoup(response.content, 'html.parser')
    return json.loads(soup.find('script', attrs={'id': '__NEXT_DATA__'}).text)['props']['pageProps']
