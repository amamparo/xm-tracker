from datetime import datetime, timedelta
from typing import Optional

import requests
from injector import Injector, inject

from src.bucket import Bucket
from src.modules import LocalModule, LambdaModule

@inject
def main(bucket: Bucket):
    channel_ids = [x['id'] for x in bucket.read_lines('channels.jsonl')]
    lookaround = requests.get(
        'https://lookaround-cache-prod.streaming.siriusxm.com/contentservices/v1/live/lookAround'
    ).json()['channels']
    now = datetime.utcnow()
    one_year_ago_iso = (now - timedelta(days=365)).isoformat()
    for channel_id in channel_ids:
        channel = lookaround.get(channel_id)
        if not channel:
            continue
        cuts = channel.get('cuts')
        if not cuts:
            continue
        cut = cuts[0]
        track = {
            'title': cut['name'],
            'artist': cut.get('artistName'),
            'at': now.isoformat()
        }
        key = f'play_history/{channel_id}.jsonl'
        tracks = bucket.read_lines(key)
        most_recent = tracks[-1] if tracks else None
        if most_recent and most_recent['title'] == track['title'] and most_recent['artist'] == track['artist']:
            continue
        tracks.append(track)
        tracks = [x for x in tracks if x['at'] >= one_year_ago_iso]
        bucket.write_lines(key, tracks)


def lambda_handler(event: Optional[dict] = None, context: Optional[dict] = None) -> None:
    Injector(LambdaModule).call_with_injection(main)


if __name__ == '__main__':
    Injector(LocalModule).call_with_injection(main)
