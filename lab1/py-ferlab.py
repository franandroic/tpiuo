import requests

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

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
auth_headers = { "User-Agent": user_agent }

#Getting the data from Reddit
reddit_url = "https://www.reddit.com/r/dataengineering/top.json?t=all&limit=10"
response = requests.get(reddit_url, headers=auth_headers)

if response.ok:
    data = response.json()
    print(data)
else:
    print(response.status_code)