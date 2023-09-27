import json

from graphql import GraphQLError

def all_movies(_, info):
    with open('{}/data/movies.json'.format("."), "r") as file:
        data = json.load(file)
        return data['movies']

def movie_with_id(_, info, _id):
    with open('{}/data/movies.json'.format('./'), 'r') as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie
            
def add_movie(_, info, _id, _title, _rating, _director):
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies["movies"]:
            if movie["id"] == _id:
                raise GraphQLError('Movie already exists !')
        
        new_movie = {
            "id": _id,
            "title": _title,
            "rating": _rating,
            "director": _director
        }
        movies["movies"].append(new_movie)
        with open('{}/data/movies.json'.format("."), "w") as wfile:
            json.dump(movies, wfile)
        return new_movie

def update_movie_rate(_,info,_id,_rate):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie

def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data['actors'] if movie['id'] in actor['films']]
        return actors