import logging
import traceback
from datetime import datetime, timedelta
from typing import Tuple, Dict, List

import awsgi
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from flask_injector import FlaskInjector
from injector import inject

from src.bucket import Bucket
from src.modules import LambdaModule, LocalModule

app = Flask(__name__)
CORS(app)


@inject
@app.route('/stations')
def __stations(bucket: Bucket):
    return jsonify([
        {
            'id': x['id'],
            'title': x['title'],
            'genre': x['genre']
        } for x in sorted(bucket.read_lines('channels.jsonl'), key=lambda x: (x['genre'], x['title']))
    ])


@inject
@app.route('/top-tracks/<station_id>')
def __channel(bucket: Bucket, station_id: str):
    days_back = int(request.args.get('days-back', 7))
    plays = bucket.read_lines(f'play_history/{station_id}.jsonl')
    earliest_date_iso = (datetime.utcnow() - timedelta(days=days_back)).isoformat()
    plays = [x for x in plays if x['at'] >= earliest_date_iso]
    grouped: Dict[Tuple[str, str], List[dict]] = {}
    for track in plays:
        key = (track['artist'], track['title'])
        if key not in grouped:
            grouped[key] = []
        grouped[key] = grouped.get(key, []) + [track]

    tracks = []
    for group in grouped.values():
        first_track = group[0]
        tracks.append({
            'artist': first_track['artist'],
            'title': first_track['title'],
            'plays': len(group),
            'last_played_at': sorted([x['at'] for x in group])[-1]
        })

    return jsonify(sorted(tracks, key=lambda t: (t['plays'], t['last_played_at']), reverse=True))


@inject
@app.errorhandler(500)
def __error(exception: Exception):
    logging.error(exception)
    return Response(traceback.format_exc(), status=500, mimetype='application/text')


def lambda_handler(event, context):
    FlaskInjector(app=app, modules=[LambdaModule])
    return awsgi.response(app, event, context)


if __name__ == '__main__':
    FlaskInjector(app=app, modules=[LocalModule])
    app.run(port=8080, debug=True)
