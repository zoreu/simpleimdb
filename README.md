# simpleimdb

#### Installation
Whenever possible, please use the latest version from the repository::

```bash
pip install git+https://github.com/zoreu/simpleimdb
```

## Examples

```python

from simpleimdb import imdb
# movie example
movie = imdb.get_movie(imdb='tt1745960',lang='en') # for most speed use arg trailer=False
#all information from keys
print(movie.keys())
############################
movie_title = movie.get("title")
movie_description = movie.get("description")
movie_rating = movie.get("rating")
movie_votes = movie.get("votes")

# new movies list
movies, next = imdb.new_movies(count=3,lang='en')
# if next use:
movies, next = imdb.new_movies(count=3,lang='en',next=next)
# movies in threaters
movies, next = imdb.movies_in_threaters(count=3,lang='en')
# if next use:
movies, next = imdb.movies_in_threaters(count=3,lang='en',next=next)

### tvshow example
tvshow = imdb.get_tvshow(imdb='tt8103070', lang='en')
#all information from keys
print(tvshow.keys())
tvshow_title = tvshow.get("title") # title Legacies
#list seasons
seasons = [season.get("season") for season in tvshow.get("seasons")]
#select season 1   
episodes = [season.get("episodes") for season in tvshow.get("seasons") if season.get("season") == 1][0]
for i in episodes:
    episode_number = i.get("episode")
    episode_title = i.get("title")
    episode_description = i.get("description")
    episode_thumbnail = i.get("thumbnail")
    print(episode_title)

# new tvshows
tvshows, next = imdb.new_tvshows(count=5)
# for next:
tvshows, next = imdb.new_tvshows(count=5,next=next)

# most popular tvshows
tvshows, next = imdb.most_popular_tvshows(count=5)
# for next:
tvshows, next = imdb.most_popular_tvshows(count=5,next=next)
```

### License

simpleimdb is released under the GPL license, version 2 or later.
Read the included `LICENSE.txt`_ file for details.