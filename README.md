# movie-picker

API to get a random movie from your IMDB watchlist

## Requirements

You need to know your user id in IMDB and have your watchlist public.

## Usage

To run a project you need to run the following command:

```
python app.py
```

## API description

There are two endpoints in API:

### 1. Get watchlist info

``` 
GET /info/<user_id>
```

This will return your movie count and other statistic which you can use to filter your tandom movie request

### 2. Get random movie

```
GET /random
```

Body params: 

```
user_id
filter: {
  max_rate: float
  min_rate: float
  max_year: int
  min_year: int
  ganres: string[]
  title_type: string[]
}
```

`user_id` input is required, `filter` is optional