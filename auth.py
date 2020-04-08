import requests
import json


client_id = 7347555
redirect_uri = 'https://oauth.vk.com/blank.html'
response_type = 'token'
version = '5.103'

url = F'https://oauth.vk.com/authorize?client_id={client_id}&' \
      F'display=page&redirect_uri={redirect_uri}&scope=friends&response_type={response_type}&v={version}'

response = requests.get(url)

data = json.dumps(response.text)

print(response)

