from azure.eventhub import EventHubConsumerClient
from azure.storage.filedatalake import DataLakeServiceClient
from datetime import datetime
from azure.core.exceptions import ResourceNotFoundError

#Event Hub parameters
event_hub_connecion_str = "Endpoint=sb://ns-ferlab.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=F8QqEeScZ34WCPOVyZsWdIvzr8BFT5rrA+AEhMrVW1o="
event_hub_name = "eh-ferlab"
consumer_group = "$default"

#Data Lake parameters
storage_account_name = "saferlab"
storage_container_name = "datacon-ferlab"
storage_account_connection_str = "DefaultEndpointsProtocol=https;AccountName=saferlab;AccountKey=5Fivj1RJjf1Tt1MEGdbEwfv4yQ7U+UgRqiF2kzUrL+btlQRbF+X8UmP0qM0TyvO1fWUmQ4mjzvRC+ASt2vH9xQ==;EndpointSuffix=core.windows.net"
service_client = DataLakeServiceClient.from_connection_string(conn_str=storage_account_connection_str)
file_system_client = service_client.get_file_system_client(file_system=storage_container_name)


def on_event_batch(partition_context, event_batch):

    current_datetime = datetime.now()
    file_name = 0
    
    directory_client = file_system_client.get_directory_client(f"{str(current_datetime.year)}/{str(current_datetime.month)}/{str(current_datetime.day)}/{str(current_datetime.hour)}/{str(current_datetime.minute)}")

    try:
        print("Old directory: " + str(directory_client.get_directory_properties().name))
    except ResourceNotFoundError:
        directory_client.create_directory()
        print("New directory: " + str(directory_client.get_directory_properties().name))

    for event in event_batch:

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