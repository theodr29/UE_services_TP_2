import grpc
from concurrent import futures
import showtime_pb2
import showtime_pb2_grpc
import json


class ShowtimeServicer(showtime_pb2_grpc.ShowtimesServicer):
    """Provides methods that override those from ShowtimesServicer"""

    def __init__(self):
        with open("{}/data/times.json".format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    def GetShowTimeByDate(self, request, content):
        """This function returns the showtimes for the given date"""

        for showtime in self.db:
            if request.date == showtime["date"]:
                return showtime_pb2.ShowTime(
                    date=showtime["date"], movies=showtime["movies"]
                )

        # If the date is not found, we return an empty showtime
        return showtime_pb2.ShowTime(date="", movies=[])

    def GetShowTimes(self, request, context):
        """This function returns all the showtimes as a stream"""
        for showtime in self.db:
            yield showtime_pb2.ShowTime(
                date=showtime["date"], movies=showtime["movies"]
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowtimesServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port("[::]:3002")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
