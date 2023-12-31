from ariadne import (
    graphql_sync,
    make_executable_schema,
    load_schema_from_path,
    ObjectType,
    QueryType,
    MutationType,
)
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, make_response, request, jsonify

import resolvers as r

PORT = 3001
HOST = "0.0.0.0"
app = Flask(__name__)

# Import and set up the graphql schema
type_defs = load_schema_from_path("movie.graphql")
query = QueryType()
mutation = MutationType()
movie = ObjectType("Movie")
actor = ObjectType("Actor")
query.set_field("movie_with_id", r.movie_with_id)
query.set_field("movie_with_title", r.movie_with_title)
query.set_field("movies_with_director", r.movies_with_director)
query.set_field("all_movies", r.all_movies)
movie.set_field("actors", r.resolve_actors_in_movie)
mutation.set_field("update_movie_rate", r.update_movie_rate)
mutation.set_field("add_movie", r.add_movie)
mutation.set_field("delete_movie", r.delete_movie)

schema = make_executable_schema(type_defs, movie, query, mutation, actor)


# root message
@app.route("/", methods=["GET"])
def home():
    """This function returns a welcome message"""
    return make_response(
        "<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200
    )


#####
# graphql entry points


@app.route("/graphql", methods=["GET"])
def playground():
    """This function returns the playground interface for the graphql server"""
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    """This function returns the response of the graphql server"""
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=None,
        debug=app.debug,
    )
    status_code = 200 if success else 400
    return make_response(jsonify(result), status_code)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
