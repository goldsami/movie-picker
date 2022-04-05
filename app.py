from flask import Flask, jsonify

from adapters.file_reader_adaprer import FileReaderAdapter
from adapters.imdb_adapter import ImdbAdapter
from core.watchlist_service import WatchlistService

app = Flask(__name__)


@app.route('/<userid>', methods=['POST', 'GET'])
def random_movie(userid):
    watchlist_service = WatchlistService(ImdbAdapter(FileReaderAdapter()))
    movie = watchlist_service.get_random_movie(userid)
    return str(movie)


if __name__ == '__main__':
    app.run()
