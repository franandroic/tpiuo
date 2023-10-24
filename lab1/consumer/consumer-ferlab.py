from azure.eventhub import EventHubConsumerClient

event_hub_connecion_str = "Endpoint=sb://ns-ferlab.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=F8QqEeScZ34WCPOVyZsWdIvzr8BFT5rrA+AEhMrVW1o="
event_hub_name = "eh-ferlab"
consumer_group = "$default"

def on_event_batch(partition_context, event_batch):

    for event in event_batch:
        print(event)

    partition_context.update_checkpoint()

def main():

    consumer_client = EventHubConsumerClient.from_connection_string(event_hub_connecion_str, consumer_group, eventhub_name=event_hub_name)

    with consumer_client:
        consumer_client.receive_batch(
            on_event_batch=on_event_batch,
            starting_position="-1"
        )

main()