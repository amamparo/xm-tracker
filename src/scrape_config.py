from dataclasses import dataclass
from typing import List

from src.beatport_beatsource_scrapers import BeatsourceScraper, BeatportScraper
from src.scraper import Scraper
from src.sirius_xm_scraper import SiriusXmScraper


@dataclass
class ScrapeConfig:
    tidal_playlist_id: str
    scraper: Scraper


scrape_configs: List[ScrapeConfig] = [
    ScrapeConfig(
        tidal_playlist_id='aee03b59-bc45-4f8a-9a7b-27dc2c855795',
        scraper=SiriusXmScraper('https://xmplaylist.com/station/thebridge/most-heard?subDays=60')
    ),
    # ScrapeConfig(
    #     tidal_playlist_id='8c83a426-0f70-432b-b40b-d1bb69cc52d4',
    #     scraper=SiriusXmScraper('https://xmplaylist.com/station/theheat/most-heard?subDays=60')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='8cfa0e47-3b9d-4841-997d-cea301243b7b',
    #     scraper=SiriusXmScraper('https://xmplaylist.com/station/diplosrevolution/most-heard?subDays=60')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='58e57177-bfe7-4196-b885-98795377cca8',
    #     scraper=SiriusXmScraper('https://xmplaylist.com/station/flownacion/most-heard?subDays=60')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='93be7820-279a-405d-832b-57597e423dc5',
    #     scraper=SiriusXmScraper('https://xmplaylist.com/station/rockthebellsradio/most-heard?subDays=60')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='f39ed841-a0e8-4b16-9ca0-5b5b08d2fd68',
    #     scraper=SiriusXmScraper('https://xmplaylist.com/station/hiphopnation/most-heard?subDays=60')
    # ),
    ScrapeConfig(
        tidal_playlist_id='86f76a33-00c8-4c93-ad16-58b9cd44054a',
        scraper=SiriusXmScraper('https://xmplaylist.com/station/siriusxmfly/most-heard?subDays=60')
    ),
    # ScrapeConfig(
    #     tidal_playlist_id='2b4862c0-e2dc-4f7c-9af7-59cb29c83289',
    #     scraper=SiriusXmScraper('https://xmplaylist.com/station/siriusxmu/most-heard?subDays=60')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='e9b2e87a-2d03-4cc3-9e73-22aea049a8af',
    #     scraper=SiriusXmScraper('https://xmplaylist.com/station/1stwave/most-heard?subDays=60')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='80baba53-f22f-4718-9091-8aa9a7823c49',
    #     scraper=SiriusXmScraper('https://xmplaylist.com/station/alt2k/most-heard?subDays=60')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='e72eb1e2-764a-4a3b-9792-8979c28d4e31',
    #     scraper=SiriusXmScraper('https://xmplaylist.com/station/siriusxmchill/most-heard?subDays=60')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='158f6b29-f046-4a8a-8bfc-c533aa0cc967',
    #     scraper=SiriusXmScraper('https://xmplaylist.com/station/shade45/most-heard?subDays=60')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='d0e912af-ecf7-4a48-833a-a44eb9246cde',
    #     scraper=SiriusXmScraper('https://xmplaylist.com/station/flex2k/most-heard?subDays=60')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='55022b16-3b2c-4f20-af52-388d27cc48a3',
    #     scraper=SiriusXmScraper('https://xmplaylist.com/station/theflow/most-heard?subDays=60')
    # )
    # ScrapeConfig(
    #     tidal_playlist_id='b9317f74-d91c-4fb9-a9a6-2cf126e50da1',
    #     scraper=BeatsourceScraper('https://www.beatsource.com/genre/hip-hop/1')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='429dba62-377f-4efa-8af6-ee8dc13691bd',
    #     scraper=BeatsourceScraper('https://www.beatsource.com/genre/latin/5')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='8e794522-012d-4ec2-8296-fd704cbefbd5',
    #     scraper=BeatportScraper('https://www.beatport.com/genre/indie-dance/37/top-100')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='b77ff93f-b040-46a4-9665-a8e91e14ffd8',
    #     scraper=BeatportScraper('https://www.beatport.com/genre/organic-house-downtempo/93/top-100')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='2a06f4f1-fcce-4a89-9a1c-eed3ef11cfd3',
    #     scraper=BeatportScraper('https://www.beatport.com/genre/electro-classic-detroit-modern/94/top-100')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='aec3ee01-99f8-4ba6-b80e-1d191ead0efc',
    #     scraper=BeatportScraper('https://www.beatport.com/genre/afro-house/89/top-100')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='6c383dda-1b97-4857-bf72-21697676d615',
    #     scraper=BeatportScraper('https://www.beatport.com/genre/bass-club/85/top-100')
    # ),
    # ScrapeConfig(
    #     tidal_playlist_id='56276bc5-d15c-4261-9802-1225ff24ec02',
    #     scraper=BeatportScraper('https://www.beatport.com/genre/progressive-house/15/top-100')
    # ),
]
