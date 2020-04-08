import requests
import json
from pprint import pprint

url = 'https://api.vk.com/method/'
method = 'wall.get'
token = ''
owner_id = '-146628063'
count = '100'
version = '5.103'
domain = '142392141'

url_requests = url+method

response = requests.get(url_requests,
                        params={'access_token': token,
                                'v': version,
                                'owner_id': owner_id,
                                'count': count,
                                'domain': domain
                                }
                        )

print(response)
if response.ok:
    data = json.loads(response.text)

pprint(data)

with open("{}_{}.json".format(domain, method), "w") as file:
    json.dump(data, file)
