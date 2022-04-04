import csv
import json
from typing import List

import requests
from bs4 import BeautifulSoup

from core.interfaces.watchlist_repository import WatchlistRepository


class ImdbAdapter(WatchlistRepository):
    def get_watchlist(self, user_id: str):
        list_id = self.get_list_id(user_id)
        csv_str = requests.get(f'https://www.imdb.com/list/{list_id}/export')
        movie_items = list(csv.reader(csv_str.text.split('\n')))[1:]
        return map(self.csv_line_to_movie, movie_items)

    @staticmethod
    def csv_line_to_movie(scv_line: List[str]):
        # pass
        from core.entities.movie import Movie
        return Movie(title=scv_line[5], url=scv_line[6], genres=scv_line[11].split(', '), year=scv_line[10],
                     rating=scv_line[8], directors=scv_line[14].split(', '), title_type=[7])

    @staticmethod
    def get_list_id(user_id: str) -> str:
        with open('data.json', 'r') as file:
            json_str = file.read()
            obj = json.loads(json_str)
        if obj['listId']:
            list_id = obj['listId']
        else:
            r = requests.get(f'https://www.imdb.com/user/{user_id}/watchlist')
            parsed_html = BeautifulSoup(r.text)
            list_id = parsed_html.head.find('meta', attrs={'property': 'pageId'})['content']
            with open('data.json', 'r+') as file:
                file.write(json.dumps({
                    "listId": list_id
                }))
        return list_id
