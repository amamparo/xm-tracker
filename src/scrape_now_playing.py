from datetime import datetime, timedelta

import requests

from src.s3 import LocalS3


def main():
    s3 = LocalS3()
    channel_ids = [x['id'] for x in s3.read_lines('channels.jsonl')]
    lookaround = requests.get(
        'https://lookaround-cache-prod.streaming.siriusxm.com/contentservices/v1/live/lookAround'
    ).json()['channels']
    now = datetime.utcnow()
    one_week_ago_iso = (now - timedelta(days=7)).isoformat()
    for channel_id in channel_ids:
        cut = lookaround[channel_id]['cuts'][0]
        track = {
            'title': cut['name'],
            'artist': cut.get('artistName'),
            'at': now.isoformat()
        }
        key = f'play_history/{channel_id}.jsonl'
        tracks = s3.read_lines(key)
        most_recent = tracks[-1] if tracks else None
        if most_recent and most_recent['title'] == track['title'] and most_recent['artist'] == track['artist']:
            continue
        tracks.append(track)
        tracks = [x for x in tracks if x['at'] >= one_week_ago_iso]
        s3.write_lines(key, tracks)


if __name__ == '__main__':
    main()
