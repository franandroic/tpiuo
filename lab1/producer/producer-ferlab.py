import requests
import asyncio
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
import json

'''
#App specifics
client_id = "0YQDH9MopcVypOK4ZE4d1Q"
client_secret = "y6LazDUW72esF8eNLZCPp8MQXJeDpw"

#Authentication
auth_url = "https://www.reddit.com/api/v1/access_token"
auth_data = {
    "grant_type": "client_credentials",
    "username": client_id,
    "password": client_secret
}

auth_response = requests.post(auth_url, data=auth_data, auth=(client_id, client_secret), headers=auth_headers)
auth_json = auth_response.json()
access_token = auth_json["access_token"]
'''

#Defining event hub parameters
event_hub_connection_str = "Endpoint=sb://ns-ferlab.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=F8QqEeScZ34WCPOVyZsWdIvzr8BFT5rrA+AEhMrVW1o="
event_hub_name = "eh-ferlab"

#Defining the user agent spoof
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
auth_headers = { "User-Agent": user_agent }

def fetch_post_batch(event_data_batch, after):

    #The Reddit URL containing the subreddit
    reddit_url = "https://www.reddit.com/r/politics/top.json?t=all"
    #Reddit API parameters
    parameters = {"after": after, "limit": 10}

    #Getting the data from Reddit
    response = requests.get(reddit_url, headers=auth_headers, params=parameters)

    if response.ok:
        data = response.json()
        for post in data["data"]["children"]:
            #Printing out some kind of identifier
            print(post["data"]["title"])
            #Adding events to the batch
            event_data_batch.add(EventData(json.dumps(post).encode('utf-8')))

        after = data["data"]["after"]
        return after

    else:
        print(response.status_code)
        return None

async def run():

    #Defining the "after" flag
    after_value = None

    #Creating a producer client
    producer = EventHubProducerClient.from_connection_string(
        conn_str=event_hub_connection_str, eventhub_name=event_hub_name
    )

    for _ in range(10):
        
        #Creating a batch
        event_data_batch = await producer.create_batch()

        after_value = fetch_post_batch(event_data_batch, after=after_value)
        if not after_value: break

        #Sending the batch to the event hub
        await producer.send_batch(event_data_batch)

        await asyncio.sleep(10)

def main():

    #Sending the data to event hub
    asyncio.run(run())

    while(True):
        continue

main()