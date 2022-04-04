import csv
import random

import requests as requests
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import json

from adapters.imdb_adapter import ImdbAdapter
from core.watchlist_service import WatchlistService

app = Flask(__name__)


@app.route('/<userid>', methods=['POST', 'GET'])
def hello_world(userid):
    watchlist_service = WatchlistService(ImdbAdapter())
    res = watchlist_service.get_random_movie(userid)
    return jsonify(res)


if __name__ == '__main__':
    app.run()
