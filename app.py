import json

from flask import Flask, jsonify, request

from adapters.file_reader_adaprer import FileReaderAdapter
from adapters.imdb_adapter import ImdbAdapter
from core.watchlist_service import WatchlistService

app = Flask(__name__)

watchlist_service = WatchlistService(ImdbAdapter(FileReaderAdapter()))


@app.route('/random', methods=['POST'])
def random_movie():
    request_data = request.get_json()
    user_id = request_data['user_id']
    movies_filter = request_data['filter']
    movie = watchlist_service.get_random_movie(user_id, movies_filter)
    return json.dumps(movie.__dict__)


@app.route('/info/<userid>', methods=['GET'])
def test(userid):
    info = watchlist_service.get_watchlist_info(userid)
    return json.dumps(info.__dict__)


if __name__ == '__main__':
    app.run()
