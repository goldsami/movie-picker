import requests as requests
from flask import Flask
from bs4 import BeautifulSoup
import json

app = Flask(__name__)


@app.route('/<userid>', methods=['POST'])
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
    return list_id


if __name__ == '__main__':
    app.run()
