import requests
import json
from pprint import pprint

users = 'HeelHook88'

main_link = 'https://api.github.com/users/{}/repos'.format(users)

response = requests.get(main_link)

if response.ok:
    data = json.loads(response.text)


with open("{}.json".format(users), "w") as file:
    json.dump(data, file)
