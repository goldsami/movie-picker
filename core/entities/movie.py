import dataclasses

from typing import List


@dataclasses
class Movie:
    title: str
    url: str
    genres: List[str]
    year: int
    rating: float
    directors: List[str]
    title_type: str
