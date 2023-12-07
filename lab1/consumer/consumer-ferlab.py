from azure.eventhub import EventHubConsumerClient
from azure.storage.filedatalake import DataLakeServiceClient, DataLakeDirectoryClient, DataLakeFileClient
from datetime import datetime

#Event Hub parameters
event_hub_connecion_str = "Endpoint=sb://ns-ferlab.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=F8QqEeScZ34WCPOVyZsWdIvzr8BFT5rrA+AEhMrVW1o="
event_hub_name = "eh-ferlab"
consumer_group = "$default"

#Data Lake parameters
storage_account_name = "saferlab"
storage_container_name = "datacon-ferlab"
storage_account_connection_str = "DefaultEndpointsProtocol=https;AccountName=saferlab;AccountKey=5Fivj1RJjf1Tt1MEGdbEwfv4yQ7U+UgRqiF2kzUrL+btlQRbF+X8UmP0qM0TyvO1fWUmQ4mjzvRC+ASt2vH9xQ==;EndpointSuffix=core.windows.net"
#service_client = DataLakeServiceClient(account_url=f"https://{storage_account_name}.dfs.core.windows.net", credential=storage_account_connection_str)
service_client = DataLakeServiceClient.from_connection_string(conn_str=storage_account_connection_str)
file_system_client = service_client.get_file_system_client(file_system=storage_container_name)


def on_event_batch(partition_context, event_batch):

    current_datetime = datetime.now()
    file_name = 0

    directory_client_year = file_system_client.get_directory_client(current_datetime.year)
    directory_client_month = directory_client_year.get_sub_directory_client(current_datetime.month)
    directory_client_day = directory_client_month.get_sub_directory_client(current_datetime.day)
    directory_client_hour = directory_client_day.get_sub_directory_client(current_datetime.hour)
    directory_client_minute = directory_client_hour.get_sub_directory_client(current_datetime.minute)

    for client in [directory_client_year,
                   directory_client_month,
                   directory_client_day,
                   directory_client_hour,
                   directory_client_minute]:
        if not client.get_directory_properties().metadata:
            client.create_directory()

    for event in event_batch:

        #print(event)

        file_client = directory_client_minute.get_file_client(str(file_name))
        event_bytes = str(event).encode("utf-8")

        file_client.append_data(event_bytes, offset=0, length=len(event_bytes))
        file_client.flush_data(len(event_bytes))

        file_name += 1

    #partition_context.update_checkpoint()

def main():

    consumer_client = EventHubConsumerClient.from_connection_string(event_hub_connecion_str, consumer_group, eventhub_name=event_hub_name)

    with consumer_client:
        consumer_client.receive_batch(
            on_event_batch=on_event_batch,
            starting_position="-1"
        )

main()