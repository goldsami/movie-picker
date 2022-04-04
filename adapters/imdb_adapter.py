import csv
import json
from typing import List
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from core.entities.movie import Movie
from core.interfaces.watchlist_repository import WatchlistRepository


class ImdbAdapter(WatchlistRepository):
    def get_watchlist(self, user_id: str):
        list_id = self.get_list_id(user_id)
        csv_resp = self.request_csv(list_id)
        movie_items = self.parse_watchlist_csv(csv_resp)
        filtered_items = [x for x in movie_items if (len(x))]
        return list(map(self.csv_line_to_movie, filtered_items))

    @staticmethod
    def request_csv(list_id: str):
        return requests.get(f'https://www.imdb.com/list/{list_id}/export')

    @staticmethod
    def parse_watchlist_csv(csv_str: str) -> List[str]:
        return list(csv.reader(csv_str.text.split('\n')))[1:]

    @staticmethod
    def csv_line_to_movie(scv_line: List[str]):
        return Movie(title=scv_line[5], url=scv_line[6], genres=scv_line[11].split(', '), year=scv_line[10],
                     rating=scv_line[8], directors=scv_line[14].split(', '), title_type=scv_line[7])

    # todo: refactor method
    @staticmethod
    def get_list_id(user_id: str) -> str:
        path = Path(__file__).parent / "./data.json"
        try:
            with path.open() as file:
                json_str = file.read()
                obj = json.loads(json_str)
        except Exception as e:
            # todo: create data.json
            print(e)
            obj = {}
        if 'listId' in obj.keys() and obj['listId']:
            list_id = obj['listId']
        else:
            r = requests.get(f'https://www.imdb.com/user/{user_id}/watchlist')
            parsed_html = BeautifulSoup(r.text)
            list_id = parsed_html.head.find('meta', attrs={'property': 'pageId'})['content']
            with path.open('r+') as file:
                file.write(json.dumps({
                    "listId": list_id
                }))
        return list_id
