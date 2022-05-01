import random
from typing import List

from core.entities.movie import Movie
from core.entities.watchlist_info import WatchlistInfo
from core.interfaces.watchlist_repository import WatchlistRepository
from core.utils import flatten


class WatchlistService:
    def __init__(self, repository: WatchlistRepository):
        self.repository = repository
        self.watchlist = []

    def get_watchlist(self, user_id: str):
        if not len(self.watchlist):
            self.watchlist = self.repository.get_watchlist(user_id)
        return self.watchlist

    def get_random_movie(self, user_id: str, _filter: WatchlistInfo) -> Movie:
        watchlist = self.get_watchlist(user_id)
        filtered_watchlist = self.filter_movies(watchlist, _filter)
        return random.choice(filtered_watchlist)

    def get_watchlist_info(self, user_id: str) -> WatchlistInfo:
        watchlist = self.get_watchlist(user_id)
        return WatchlistInfo(movie_count=len(watchlist),
                             max_rate=max(movie.rating for movie in watchlist),
                             min_rate=min(movie.rating for movie in watchlist),
                             max_year=max(movie.year for movie in watchlist),
                             min_year=min(movie.year for movie in watchlist),
                             genres=self.get_genres(watchlist),
                             title_types=self.get_title_types(watchlist))

    @staticmethod
    def get_genres(_watchlist) -> List[str]:
        return list(set(flatten(list(map(lambda x: x.genres, _watchlist)))))

    @staticmethod
    def get_title_types(_watchlist) -> List[str]:
        return list(set(list(map(lambda x: x.title_type, _watchlist))))

    @staticmethod
    def filter_movies(_watchlist, _filter):
        result = _watchlist
        if _filter['genres']:
            result = list(filter(lambda x: all(item in x.genres for item in _filter['genres']), _watchlist))
        return result
