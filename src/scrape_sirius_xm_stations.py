import requests
from fake_useragent import UserAgent
from tqdm import tqdm

from src.s3 import LocalS3


def main():
    lookaround_ids = [
        x for x in requests.get(
            'https://lookaround-cache-prod.streaming.siriusxm.com/contentservices/v1/live/lookAround'
        ).json()['channels'].keys()
    ]
    raw_channels = [
        x for x in requests.get('https://www.siriusxm.com/channelfeed/SXM_S_1').json()['channels']
        if x['category'] == 'music' and x['availableToPackage']
    ]
    channels = []
    for channel in tqdm(raw_channels):
        redirect_location = requests.get(
            channel['deepLink'],
            allow_redirects=False,
            headers={
                'User-Agent': UserAgent().chrome
            }
        ).headers['Location']
        channel_id = redirect_location.split('/')[-1].split('?')[0]
        if channel_id not in lookaround_ids:
            continue

        channels.append({'id': channel_id, 'title': channel['displayName'], 'genre': channel['genreTitle']})

    LocalS3().write_lines('channels.jsonl', channels)


if __name__ == '__main__':
    main()
