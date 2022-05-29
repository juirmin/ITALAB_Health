import requests
import json


def get_uuid(token):
    UUID = "a0e03240-c69f-11ec-9140-05d9030e6400"
    api = "7bafd854-fa0f-4f8f-8bc5-d287944ec46f"
    Host = "35.187.158.248"
    Version = "1.0"

    baseurl = f"http://{Host}/api/{Version}/partners/{UUID}"

    headers = {
        "Header-Auth-Key": api,
    }
    authURL = baseurl + "/user-auth"
    r = requests.post(authURL, headers=headers, json={"token": token})
    #print(r.status_code)
    response = {}
    return json.loads(r.text)
