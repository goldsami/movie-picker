import random

from core.interfaces.watchlist_repository import WatchlistRepository


class WatchlistService:
    def __init__(self, repository: WatchlistRepository):
        self.repository = repository
        self.watchlist = []

    def get_watchlist(self, user_id: str):
        if not len(self.watchlist):
            self.watchlist = self.repository.get_watchlist(user_id)
        return self.watchlist

    def get_random_movie(self, user_id: str):
        watchlist = self.get_watchlist(user_id)
        return random.choice(watchlist)
