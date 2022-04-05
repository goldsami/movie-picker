class Movie:
    def __init__(self, title, url, genres, year, rating, directors, title_type):
        self.title = title
        self.url = url
        self.genres = genres
        self.year = year
        self.rating = rating
        self.directors = directors
        self.title_type = title_type

    def __str__(self):
        return f'name: {self.title}; \n url: {self.url} \n'
