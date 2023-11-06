import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc
import json


def get_showtimes_by_date(stub, date):
    """This function returns the showtimes for the given date"""
    showtime = stub.GetShowTimeByDate(date)
    return showtime


class BookingServicer(booking_pb2_grpc.BookingsServicer):
    """Provides methods that override those from BookingsServicer"""

    def __init__(self):
        with open("{}/data/bookings.json".format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetBookings(self, request, context):
        """This function returns all the bookings as a stream"""

        for booking in self.db:
            yield booking_pb2.Booking(
                userid=booking["userid"],
                dates=[
                    booking_pb2.Dates(
                        date=booking["dates"][i]["date"],
                        movies=booking["dates"][i]["movies"],
                    )
                    for i in range(len(booking["dates"]))
                ],
            )

    def GetBookingsByUser(self, request, context):
        """This function returns the bookings of the user with the given id"""

        for booking in self.db:
            if booking["userid"] == request.id:
                return booking_pb2.Booking(
                    userid=booking["userid"],
                    dates=[
                        booking_pb2.Dates(
                            date=booking["dates"][i]["date"],
                            movies=booking["dates"][i]["movies"],
                        )
                        for i in range(len(booking["dates"]))
                    ],
                )
        return booking_pb2.Booking(
            userid="", dates=[booking_pb2.Dates(date="", movies=[])]
        )

    def PostNewBooking(self, request, context):
        """This function adds a new booking to the database"""

        for booking in self.db:
            # First we check if the user exists
            if booking["userid"] == request.userid:
                # Retrieving shows data for the given date
                showtime_port = 3002
                with grpc.insecure_channel(f"showtime:{showtime_port}") as channel:
                    stub = showtime_pb2_grpc.ShowtimesStub(channel)
                    showtimes = get_showtimes_by_date(
                        stub, date=showtime_pb2.Date(date=request.date)
                    )
                channel.close()
                movies = showtimes.movies

                # Now we check if the given movie is aired on the given date
                if request.movieid in movies:
                    # Now we check if the user has already booked the movie
                    dateFound = False
                    for date in booking["dates"]:
                        dateFound = False
                        # We check if the user already has a booking for the given date
                        if date["date"] == request.date:
                            dateFound = True
                            # If the user has already booked the movie, we return an empty booking
                            if request.movieid in date["movies"]:
                                return booking_pb2.Booking(
                                    userid="",
                                    dates=[booking_pb2.Dates(date="", movies=[])],
                                )
                            else:  # If the user has not booked the movie, we add it to the booking of this date
                                date["movies"].append(request.movieid)
                                return booking_pb2.Booking(
                                    userid=booking["userid"],
                                    dates=[
                                        booking_pb2.Dates(
                                            date=date["date"], movies=date["movies"]
                                        )
                                    ],
                                )

                    # If the user does not have a booking for the given date, we add it
                    if dateFound == False:
                        booking["dates"].append(
                            {"date": request.date, "movies": [request.movieid]}
                        )
                        return booking_pb2.Booking(
                            userid=request.userid,
                            dates=[
                                booking_pb2.Dates(
                                    date=request.date, movies=[request.movieid]
                                )
                            ],
                        )

        # If the user does not exist, we return an empty booking
        return booking_pb2.Booking(
            userid="", dates=[booking_pb2.Dates(date="", movies=[])]
        )

    def PostNewBookingUser(self, request, context):
        """This function adds a new user to the booking database"""

        # First we check if the user exists
        for booking in self.db:
            # If the user exists, we do nothing
            if booking["userid"] == request.id:
                return booking_pb2.Booking(
                    userid="", dates=[booking_pb2.Dates(date="", movies=[])]
                )

        # If the user does not exist, we add it
        self.db.append({"userid": request.id, "dates": []})
        return booking_pb2.Booking(
            userid=request.id, dates=[booking_pb2.Dates(date="", movies=[])]
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingsServicer_to_server(BookingServicer(), server)
    server.add_insecure_port("[::]:3003")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
