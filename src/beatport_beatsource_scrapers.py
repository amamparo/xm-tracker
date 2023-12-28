from datetime import datetime, timedelta
from typing import List, Optional

from fuzzywuzzy import fuzz
from tqdm import tqdm

from src.scraper import ScrapedTrack, Scraper, get_page_props
from src.tidal import Tidal, TidalTrack


def _to_tidal_track_ids(tidal: Tidal, scraped_tracks: List[ScrapedTrack]) -> List[int]:
    tidal_track_ids = []
    for scraped_track in tqdm(scraped_tracks):
        base_query = f'{" ".join(scraped_track.artists)} {scraped_track.title}'
        search_results = []
        if scraped_track.version:
            search_results = tidal.search(base_query + ' ' + scraped_track.version)
        if not search_results:
            search_results = tidal.search(base_query)
        matching_tidal_track = _match(scraped_track, search_results)
        if matching_tidal_track:
            tidal_track_ids.append(matching_tidal_track.id)
    return tidal_track_ids


def _match(scraped_track: ScrapedTrack, tidal_tracks: List[TidalTrack]) -> Optional[TidalTrack]:
    if not tidal_tracks:
        return None

    filtered_tidal_tracks = []

    cleaned_scraped_artists = {x.lower() for x in scraped_track.artists}
    for tidal_track in tidal_tracks:
        cleaned_tidal_artists = {x.lower() for x in tidal_track.artists}
        required_intersection_size = min(len(cleaned_scraped_artists), len(cleaned_tidal_artists))
        intersection_size = len(cleaned_scraped_artists.intersection(cleaned_tidal_artists))
        if intersection_size >= required_intersection_size:
            filtered_tidal_tracks.append(tidal_track)

    tidal_tracks = filtered_tidal_tracks
    filtered_tidal_tracks = []
    for tidal_track in tidal_tracks:
        n_with_remix_in_title = len(
            [x for x in [tidal_track.title, scraped_track.version or ''] if 'remix' in x.lower()])
        if n_with_remix_in_title != 1:
            filtered_tidal_tracks.append(tidal_track)

    tidal_tracks = filtered_tidal_tracks

    def __score(_tidal_track: TidalTrack) -> float:
        tidal_title = _tidal_track.title.lower()
        if _tidal_track.version:
            tidal_title += f' ({_tidal_track.version.lower()})'

        scraped_title = scraped_track.title.lower()
        if scraped_track.version:
            scraped_title += f' ({scraped_track.version.lower()})'

        return fuzz.WRatio(tidal_title, scraped_title)

    sorted_tidal_tracks = sorted(tidal_tracks, key=__score, reverse=True)

    return sorted_tidal_tracks[0] if sorted_tidal_tracks else None


class BeatportScraper(Scraper):
    def __init__(self, top_100_url: str):
        self.__top_100_url = top_100_url

    def get_tidal_track_ids(self, tidal: Tidal) -> List[int]:
        queries = get_page_props(self.__top_100_url)['dehydratedState']['queries']
        query = next(x for x in queries if x['state']['data']['count'] == 100)
        scraped_tracks = [
            ScrapedTrack(
                title=result['name'].split('feat.')[0].strip(),
                version=result.get('mix_name'),
                artists={x['name'] for x in result['artists']}
            ) for result in query['state']['data']['results']
        ]
        return _to_tidal_track_ids(tidal, scraped_tracks)


class BeatsourceScraper(Scraper):
    def __init__(self, genre_url: str):
        self.__genre_url = genre_url

    def get_tidal_track_ids(self, tidal: Tidal) -> List[int]:
        playlists_url = f'{self.__genre_url}/playlists?per_page=100&order_by=-publish_date'
        page_props = get_page_props(playlists_url)
        genre_slug = page_props['genre']['slug']
        playlist_slugs = [
            f'{genre_slug}-top-picks-{(datetime.now() - timedelta(days=30 * (i + 1))).strftime("%B-%Y").lower()}'
            for i in range(12)
        ]
        playlist_urls = [
            f'https://www.beatsource.com/playlist/{x["slug"]}/{x["id"]}'
            for x in page_props['playlists']['results']
            if x['slug'] in playlist_slugs
        ]
        tracks = []
        for playlist_url in tqdm(playlist_urls):
            tracks += self.__scrape_playlist(playlist_url, 1)
        tracks = self.__deduplicate_tracks(tracks)
        return _to_tidal_track_ids(tidal, tracks)

    @staticmethod
    def __scrape_playlist(playlist_url: str, page: int) -> List[ScrapedTrack]:
        query_string = f'?per_page=100&page={page}'
        page_props = get_page_props(playlist_url + query_string)
        results = page_props['tracks'].get('results', [])
        if not results:
            return []
        return [
            ScrapedTrack(
                title=result['name'].split('feat.')[0].strip(),
                version=result.get('mix_name'),
                artists={x['name'] for x in result['artists']}
            ) for result in results
        ] + BeatsourceScraper.__scrape_playlist(playlist_url, page + 1)

    @staticmethod
    def __deduplicate_tracks(tracks: List[ScrapedTrack]) -> List[ScrapedTrack]:
        seen = set()
        unique_tracks = []
        for track in tracks:
            track.version = track.version if track.version == 'Remix' else None
            key = (track.title, frozenset(track.artists), track.version)
            if key not in seen:
                seen.add(key)
                unique_tracks.append(track)
        return unique_tracks
