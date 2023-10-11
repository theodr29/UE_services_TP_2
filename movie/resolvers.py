import json

from graphql import GraphQLError


def all_movies(_, info):
    """Returns all the movies"""

    with open("{}/data/movies.json".format("."), "r") as file:
        data = json.load(file)
        return data["movies"]


def movie_with_id(_, info, _id):
    """Returns the movie with the given id"""

    with open("{}/data/movies.json".format("./"), "r") as file:
        movies = json.load(file)
        for movie in movies["movies"]:
            if movie["id"] == _id:
                return movie


def movie_with_title(_, info, _title):
    """Returns the movie with the given title"""

    with open("{}/data/movies.json".format("./"), "r") as file:
        movies = json.load(file)
        for movie in movies["movies"]:
            if movie["title"] == _title:
                return movie


def movies_with_director(_, info, _director):
    """Returns the movies with the given director"""

    with open("{}/data/movies.json".format("./"), "r") as file:
        movies = json.load(file)
        return [movie for movie in movies["movies"] if movie["director"] == _director]


def add_movie(_, info, _id, _title, _rating, _director):
    """Adds a new movie to the database"""

    with open("{}/data/movies.json".format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies["movies"]:
            if movie["id"] == _id:
                raise GraphQLError("Movie already exists !")

        new_movie = {
            "id": _id,
            "title": _title,
            "rating": _rating,
            "director": _director,
        }
        movies["movies"].append(new_movie)
        with open("{}/data/movies.json".format("."), "w") as wfile:
            json.dump(movies, wfile)
        return new_movie


def update_movie_rate(_, info, _id, _rate):
    """Updates the rating of the movie with the given id"""

    newmovies = {}
    newmovie = {}
    with open("{}/data/movies.json".format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies["movies"]:
            if movie["id"] == _id:
                movie["rating"] = _rate
                newmovie = movie
                newmovies = movies
    with open("{}/data/movies.json".format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie


def resolve_actors_in_movie(movie, info):
    """Returns the actors in the given movie"""

    with open("{}/data/actors.json".format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data["actors"] if movie["id"] in actor["films"]]
        return actors


def delete_movie(_, info, _id):
    """Deletes the movie with the given id"""

    newmovies = {}
    newmovie = {}
    with open("{}/data/movies.json".format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies["movies"]:
            if movie["id"] == _id:
                newmovie = movie
                movies["movies"].remove(movie)
                newmovies = movies
        with open("{}/data/movies.json".format("."), "w") as wfile:
            json.dump(newmovies, wfile)
        return newmovie
