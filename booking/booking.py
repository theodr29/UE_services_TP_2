import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import showtime_pb2
import showtime_pb2_grpc
import json

def get_showtimes_by_date(stub, date):
    showtime = stub.GetShowTimeByDate(date)
    return showtime


class BookingServicer(booking_pb2_grpc.BookingsServicer):
    def __init__(self):
        with open("{}/data/bookings.json".format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetBookings(self, request, context):
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
            userid="", dates=[booking_pb2.Date(date="", movies=[])]
        )

    def PostNewBooking(self, request, context):
        for booking in self.db:
            if booking["userid"] == request.userid:
                # Retrieving shows data
                showtime_port = 3002
                with grpc.insecure_channel(f'showtime:{showtime_port}') as channel:
                    stub = showtime_pb2_grpc.ShowtimesStub(channel)
                    showtimes = get_showtimes_by_date(stub, request.date)
                print(showtimes)
                movies = showtimes.json()["movies"]

                for date in booking.dates:
                    dateFound = False
                    if date["date"] == request.date :
                        dateFound = True
                        if request.movieid in date["movies"]:
                            return booking_pb2.Booking(
                            userid="", dates=[booking_pb2.Date(date="", movies=[])]
                            )
                        else:
                            date["movies"].append(request.movieid)
                            return booking_pb2.Booking(userid=request.userid, dates=request.dates)
                if dateFound == False:
                    booking["dates"].append({date:request.date, movies:[request.movieid]})
                    return booking_pb2.Booking(
                    userid="", dates=[booking_pb2.Date(date="", movies=[])]
                    )

        return booking_pb2.Booking(
        userid="", dates=[booking_pb2.Date(date="", movies=[])]
        )
    
    def PostNewBookingUser(self, request, context):
        for booking in self.db:
            if booking['userid'] == request.id:
                return booking_pb2.Booking(
                userid="", dates=[booking_pb2.Date(date="", movies=[])]
                )
        
        self.db.append({"userid": request.id, "dates": []})
        return booking_pb2.Booking(
            userid=request.id, dates=[booking_pb2.Date(date="", movies=[])]
        )
        


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingsServicer_to_server(BookingServicer(), server)
    server.add_insecure_port("[::]:3003")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
