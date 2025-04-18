from google.cloud import pubsub_v1
import json
import time
import datetime

project_id = "dataengineering-trimetproject"
topic_id = "Datatransport"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

with open("bcsample.json", "r") as file:
    data = json.load(file)

messagecount = 0
futures = []

starttime = time.time()

for vehicle_records in data.values():
    for record in vehicle_records:
        data_str = json.dumps(record)
        encoded_data = data_str.encode("utf-8")
        future = publisher.publish(topic_path, encoded_data)
        futures.append(future)
        messagecount += 1

for future in futures:
    future.result()

stoptime = time.time()
timetaken = stoptime - starttime

print(f" Published {messagecount} messages to {topic_path}.")
print(f" Time taken to publish all messages: {timetaken:.2f} seconds")
