import logging
import traceback

import awsgi
from flask import Flask, Response, jsonify
from flask_cors import CORS
from flask_injector import FlaskInjector
from injector import inject

from src.bucket import Bucket
from src.modules import LambdaModule, LocalModule

app = Flask(__name__)
CORS(app)


@inject
@app.route('/channels')
def __channels(bucket: Bucket):
    channels = sorted(bucket.read_lines('channels.jsonl'), key=lambda x: x['title'])
    genres = set(x['genre'] for x in channels)
    return jsonify({'genres': {
        genre: [
            {
                'id': x['id'],
                'title': x['title']
            } for x in channels if x['genre'] == genre
        ]
        for genre in genres
    }})


@inject
@app.route('/channel/<channel_id>')
def __channel(bucket: Bucket, channel_id: str):
    plays = bucket.read_lines(f'play_history/{channel_id}.jsonl')
    return jsonify(plays)


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
