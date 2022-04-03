import csv
import random

import requests as requests
from flask import Flask, jsonify
from bs4 import BeautifulSoup
import json

app = Flask(__name__)


@app.route('/<userid>', methods=['POST', 'GET'])
def hello_world(userid):
    with open('data.json', 'r') as file:
        json_str = file.read()
        obj = json.loads(json_str)
    if obj['listId']:
        list_id = obj['listId']
    else:
        r = requests.get(f'https://www.imdb.com/user/{userid}/watchlist')
        parsed_html = BeautifulSoup(r.text)
        list_id = parsed_html.head.find('meta', attrs={'property': 'pageId'})['content']
        with open('data.json', 'r+') as file:
            file.write(json.dumps({
                "listId": list_id
            }))
    r2 = requests.get(f'https://www.imdb.com/list/{list_id}/export')
    r3 = csv.reader(r2.text.split('\n'))
    r4 = list(r3)[1:]
    r5 = random.choice(r4)
    return jsonify({
        "name": r5[5],
        "url": r5[6]
    })


if __name__ == '__main__':
    app.run()
