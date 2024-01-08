from azure.eventhub import EventHubConsumerClient
from azure.storage.filedatalake import DataLakeServiceClient
from datetime import datetime
from azure.core.exceptions import ResourceNotFoundError
import json

#Event Hub parameters
event_hub_connecion_str = "Endpoint=sb://fa-ehns-ferlab.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=EAEHb1bL9IGZzVR8B+dv/vOjGO48nrj0v+AEhA0XFhU="
event_hub_name = "FA-eh-ferlab"
consumer_group = "$default"

#Data Lake parameters
storage_account_name = "fasaferlabdatalake"
storage_container_name = "fa-con-ferlab"
storage_account_connection_str = "DefaultEndpointsProtocol=https;AccountName=fasaferlabdatalake;AccountKey=htB48MtOkNH5KpCv/CzEDSu5ReVEFjYE5OOIL1sYEGq+ypG/jc+yET4dyY1sZR15zbclfk4/nWPg+AStcY6DaQ==;EndpointSuffix=core.windows.net"
service_client = DataLakeServiceClient.from_connection_string(conn_str=storage_account_connection_str)
file_system_client = service_client.get_file_system_client(file_system=storage_container_name)


def on_event_batch(partition_context, event_batch):

    file_name = 0

    for event in event_batch:

        reddit_post = json.loads(event.body_as_str(encoding="UTF-8"))
        print(reddit_post["data"]["title"])

        creation_datetime = datetime.utcfromtimestamp(reddit_post["data"]["created_utc"])
        print(creation_datetime)

        directory_client = file_system_client.get_directory_client(f"{str(creation_datetime.year)}/{str(creation_datetime.month)}/{str(creation_datetime.day)}/{str(creation_datetime.hour)}/{str(creation_datetime.minute)}")

        try:
            print("Old directory: " + str(directory_client.get_directory_properties().name))
        except ResourceNotFoundError:
            directory_client.create_directory()
            print("New directory: " + str(directory_client.get_directory_properties().name))

        file_client = directory_client.get_file_client(str(file_name))
        file_client.create_file()
        event_bytes = str(event).encode("utf-8")

        file_client.append_data(event_bytes, offset=0, length=len(event_bytes))
        file_client.flush_data(len(event_bytes))

        file_name += 1

def main():

    consumer_client = EventHubConsumerClient.from_connection_string(event_hub_connecion_str, consumer_group, eventhub_name=event_hub_name)

    with consumer_client:
        consumer_client.receive_batch(
            on_event_batch=on_event_batch,
            starting_position="-1"
        )

main()