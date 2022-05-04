import random
from typing import List

from core.entities.movie import Movie
from core.entities.watchlist_info import WatchlistInfo
from core.interfaces.watchlist_repository import WatchlistRepository
from core.utils import flatten


class NoItemsFoundError:
    def __init__(self):
        self.error = "No items found. Try to change filters."


class WatchlistService:
    def __init__(self, repository: WatchlistRepository):
        self.repository = repository

    def get_watchlist(self, user_id: str):
        return self.repository.get_watchlist(user_id)

    def get_random_movie(self, user_id: str, _filter: WatchlistInfo) -> Movie:
        watchlist = self.get_watchlist(user_id)
        filtered_watchlist = self.filter_movies(watchlist, _filter)

        if len(filtered_watchlist) == 0:
            return NoItemsFoundError()

        return random.choice(filtered_watchlist)

    def get_watchlist_info(self, user_id: str) -> WatchlistInfo:
        watchlist = self.get_watchlist(user_id)
        return WatchlistInfo(movie_count=len(watchlist),
                             max_rate=max(movie.rating for movie in watchlist),
                             min_rate=min(movie.rating for movie in watchlist),
                             max_year=max(movie.year for movie in watchlist),
                             min_year=min(movie.year for movie in watchlist),
                             genres=self.get_genres(watchlist),
                             title_type=self.get_title_types(watchlist))

    @staticmethod
    def get_genres(_watchlist) -> List[str]:
        return list(set(flatten(list(map(lambda x: x.genres, _watchlist)))))

    @staticmethod
    def get_title_types(_watchlist) -> List[str]:
        return list(set(list(map(lambda x: x.title_type, _watchlist))))

    @staticmethod
    def filter_movies(_watchlist, _filter):
        result = _watchlist
        if 'genres' in _filter:
            result = WatchlistService.filter_by_genres(result, _filter['genres'])
        if 'min_rate' in _filter:
            result = WatchlistService.filter_by_min_rate(result, _filter['min_rate'])
        if 'max_rate' in _filter:
            result = WatchlistService.filter_by_max_rate(result, _filter['max_rate'])
        if 'min_year' in _filter:
            result = WatchlistService.filter_by_min_year(result, _filter['min_year'])
        if 'max_year' in _filter:
            result = WatchlistService.filter_by_max_year(result, _filter['max_year'])
        if 'title_type' in _filter:
            result = WatchlistService.filter_by_title_type(result, _filter['title_type'])
        return result

    @staticmethod
    def filter_by_genres(_watchlist, genres):
        return list(filter(lambda x: all(item in x.genres for item in genres), _watchlist))

    @staticmethod
    def filter_by_min_rate(_watchlist, min_rate):
        return list(filter(lambda x: x.rating > min_rate, _watchlist))

    @staticmethod
    def filter_by_max_rate(_watchlist, max_rate):
        return list(filter(lambda x: x.rating < max_rate, _watchlist))

    @staticmethod
    def filter_by_min_year(_watchlist, min_year):
        return list(filter(lambda x: x.year > min_year, _watchlist))

    @staticmethod
    def filter_by_max_year(_watchlist, max_year):
        return list(filter(lambda x: x.year < max_year, _watchlist))

    @staticmethod
    def filter_by_title_type(_watchlist, title_type):
        return list(filter(lambda x: x.title_type == title_type, _watchlist))

