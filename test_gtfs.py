from google.transit import gtfs_realtime_pb2
import os

path = os.path.join(os.getcwd(), "vehicle_positions.pb")

feed = gtfs_realtime_pb2.FeedMessage()
with open(path, "rb") as f:
    feed.ParseFromString(f.read())

print("Entities:", len(feed.entity))

for e in feed.entity[:5]:
    print(e)
