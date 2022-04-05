import csv
import json
from typing import List

import requests
from bs4 import BeautifulSoup

from core.entities.movie import Movie
from core.interfaces.watchlist_repository import WatchlistRepository


class FileReader:
    def get_json_obj_from_file(self):
        raise NotImplementedError()

    def write_json_to_file(self, json_obj):
        raise NotImplementedError()


class ImdbAdapter(WatchlistRepository):
    def __init__(self, file_reader: FileReader):
        self.file_reader = file_reader

    def get_watchlist(self, user_id: str):
        list_id = self.get_list_id(user_id)
        csv_resp = self.request_csv(list_id)
        movie_items = self.parse_watchlist_csv(csv_resp)
        filtered_items = [x for x in movie_items if (len(x))]
        return list(map(self.csv_line_to_movie, filtered_items))

    def get_list_id_from_store(self, user_id):
        user_lists_map = self.file_reader.get_json_obj_from_file()
        if user_id in user_lists_map.keys() and user_lists_map[user_id]:
            return user_lists_map[user_id]
        else:
            return None

    def get_list_id_from_watchlist_page(self, user_id):
        page = self.fetch_watchlist_page(user_id)
        parsed_html = BeautifulSoup(page.text, features="html.parser")
        return parsed_html.head.find('meta', attrs={'property': 'pageId'})['content']

    def get_list_id(self, user_id: str) -> str:
        list_id = self.get_list_id_from_store(user_id)
        if list_id:
            return list_id
        else:
            list_id = self.get_list_id_from_watchlist_page(user_id)
            self.file_reader.write_json_to_file(json.dumps({
                user_id: list_id
            }))

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

    @staticmethod
    def fetch_watchlist_page(user_id):
        return requests.get(f'https://www.imdb.com/user/{user_id}/watchlist')
