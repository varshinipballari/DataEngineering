from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import json
import time

project_id = "dataengineering-trimetproject"
subscription_id = "Datatransport-sub"
timeout = 500 
idle_timeout = 10  
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

messagecount = 0
start_time = None
last_message_time = None

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    global messagecount, last_message_time
    data_recived = message.data.decode("utf-8")
    message.ack()
    messagecount += 1
    last_message_time = time.time()
    if messagecount % 10000 == 0:
        print(f" Received {messagecount} messages")

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Subscriber listening on {subscription_path}...")

with subscriber:
    try:
        start_time = time.time()
        last_message_time = start_time
        while True:
            current_time = time.time()

            if current_time - start_time > timeout:
                break
            if current_time - last_message_time > idle_timeout:
                break

            time.sleep(1)

        streaming_pull_future.cancel()
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

end_time = time.time()
print(f" Total messages received: {messagecount}")
print(f"Time taken to receive all messages: {end_time - start_time:.2f} seconds")
