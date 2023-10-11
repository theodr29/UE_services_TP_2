# REST API
from flask import Flask, request, jsonify, make_response
import requests
import json
import time

# CALLING gRPC requests
import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc

"""
import booking_pb2
import booking_pb2_grpc
import movie_pb2
import movie_pb2_grpc
"""

app = Flask(__name__)

PORT = 3004
HOST = "0.0.0.0"

with open("{}/data/users.json".format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/", methods=["GET"])
def home():
    """This function returns a welcome message"""
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/users", methods=["GET"])
def get_users():
    """This function returns all the users"""
    return make_response(jsonify(users))


@app.route("/users/<userid>", methods=["GET"])
def get_user_by_id(userid):
    """This function returns the user with the given id"""
    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify(user))
    return make_response(jsonify({"error": "User not found"}), 400)


@app.route("/users/<userid>/movies", methods=["GET"])
def get_user_movies_by_id(userid):
    """This function returns the movies that the user has booked"""
    # First we need to check if the user exists
    userFound = False
    for user in users:
        if str(user["id"]) == str(userid):
            userFound = True
            break
    if userFound == False:  # If the user does not exist, we return an error
        return make_response(jsonify({"error": "User not found"}), 400)

    # We retrieve the bookings of the user
    booking_port = 3003
    with grpc.insecure_channel(f"booking:{booking_port}") as channel:
        stub = booking_pb2_grpc.BookingsStub(channel)
        bookings = stub.GetBookingsByUser(booking_pb2.Id(id=userid))
    channel.close()

    # Now we loop through the bookings and get the movies
    movies = []
    for date in bookings.dates:
        for movie in date.movies:
            # We ask the Movie service for the movie data
            req_movie = requests.post(
                "http://movie:3001/graphql",
                json={
                    "query": """query {
    movie_with_id(_id:\""""
                    + movie
                    + """\") {
        id
        title 
        rating
        director
    }
}"""
                },
            )

            # We add the movie to the list
            if req_movie.status_code == 200:
                movies.append(req_movie.json()["data"]["movie_with_id"])
    return make_response(jsonify(movies), 200)


@app.route("/users/<userid>", methods=["POST"])
def add_user(userid):
    """This function adds a new user"""

    # First we need to check if the user exists
    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify({"error": "User already exists"}), 400)

    # We confirmed that the user does not exist, so we add it
    user = request.json
    user["id"] = userid
    user["last_active"] = int(time.time())
    users.append(request.json)

    # Before rendering the response, we need to update the database of bookings
    booking_port = 3003
    with grpc.insecure_channel(f"booking:{booking_port}") as channel:
        stub = booking_pb2_grpc.BookingsStub(channel)
        stub.PostNewBookingUser(booking_pb2.Id(id=userid))
    channel.close()

    return make_response(jsonify(request.json), 200)


@app.route("/users/editLastUpdated/<userid>", methods=["PUT"])
def edit_lastupdated(userid):
    """This function edits the last active field of a user"""
    for user in users:
        if str(user["id"]) == str(userid):
            user["last_active"] = int(time.time())
            return make_response(jsonify(user), 200)
    return make_response(jsonify({"error": "User not found"}), 400)


@app.route("/users/<userid>", methods=["DELETE"])
def delete_user(userid):
    """This function deletes a user"""
    for user in users:
        if str(user["id"]) == str(userid):
            users.remove(user)
            return make_response(jsonify(user), 200)
    return make_response(jsonify({"error": "User not found"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT)
