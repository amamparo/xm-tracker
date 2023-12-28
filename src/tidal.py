import time
from dataclasses import dataclass
from typing import Optional, List, Set, Iterable
import requests

from fake_useragent import UserAgent
from requests import Response
from tidal_dl import TOKEN, loginByConfig


def _throttle(calls_per_second: int):
    min_interval = 1.0 / calls_per_second

    def decorator(func):
        last_called = [0.0]

        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            last_called[0] = time.time()
            return func(*args, **kwargs)

        return wrapper

    return decorator


@dataclass
class TidalTrack:
    id: int  # pylint: disable=C0103
    title: str
    artists: Set[str]
    duration: int
    version: Optional[str]


class Tidal:
    def __init__(self, refresh_token: str):
        TOKEN.accessToken = 'hack'
        TOKEN.refreshToken = refresh_token
        loginByConfig()
        self.__session = requests.Session()
        self.__session.headers.update({
            'Authorization': f'Bearer {TOKEN.accessToken}',
            'User-Agent': UserAgent().chrome,
            'Accept': 'application/json'
        })

    def search(self, query: str) -> List[TidalTrack]:
        items = self.__get(
            '/v1/search/tracks',
            params={
                'query': query,
                'countryCode': 'US',
                'limit': 100
            }
        ).json()['items']
        return [
            TidalTrack(
                id=item['id'],
                title=item['title'],
                version=item['version'],
                artists={x['name'] for x in item['artists']},
                duration=item['duration']
            ) for item in items
        ]

    def add_playlist_tracks(self, playlist_id: str, track_ids: List[int]) -> None:
        for track_id_batch in self.__batch(track_ids, 100):
            etag = self.__get(
                f'/v1/playlists/{playlist_id}',
                params={
                    'countryCode': 'US'
                }
            ).headers['Etag']
            self.__request(
                method='POST',
                endpoint=f'/v1/playlists/{playlist_id}/items',
                data={
                    'onArtifactNotFound': 'SKIP',
                    'onDupes': 'SKIP',
                    'trackIds': ','.join({str(x) for x in track_id_batch})
                },
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'If-None-Match': etag
                }
            ).json()

    @staticmethod
    def __batch(x: list, size: int) -> Iterable[list]:
        for i in range(0, len(x), size):
            yield x[i:i + size]

    def __get(self, endpoint: str, params: Optional[dict] = None) -> Response:
        return self.__request(method='GET', endpoint=endpoint, params=params)

    @_throttle(4)
    def __request(self, method: str, endpoint: str, params: Optional[dict] = None, data: Optional[dict] = None,
                  headers: Optional[dict] = None) -> Response:
        return self.__session.request(
            method=method,
            url=f'https://listen.tidal.com{endpoint}',
            params=params or {},
            data=data or {},
            headers=headers or {}
        )
