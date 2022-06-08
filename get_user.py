import requests
import json

UUID = "a0e03240-c69f-11ec-9140-05d9030e6400"
api = "7bafd854-fa0f-4f8f-8bc5-d287944ec46f"
Host = "35.187.158.248"
Version = "1.0"
baseurl = f"http://{Host}/api/{Version}/partners/{UUID}"
headers = {
    "Header-Auth-Key": api,
}
def get_uuid(token):
    authURL = baseurl + "/user-auth"
    r = requests.post(authURL, headers=headers, json={"token": token})
    response = {}
    return json.loads(r.text)

def temperature(data,uuid):
    measure = "body-temperature"
    newdataURL = f"{baseurl}/users/{uuid}/measure-types/{measure}/measurements"
    r = requests.post(newdataURL, headers=headers, json={"temperature": data["temperature"]})
    return r.status_code

def oxygen(data,uuid):
    measure = "blood-oxygen"
    newdataURL = f"{baseurl}/users/{uuid}/measure-types/{measure}/measurements"
    r = requests.post(newdataURL, headers=headers, json={"spo2": data['oxygen'], "pr": data['pulse']})
    return r.status_code

def pressure(data,uuid):
    measure = "blood-pressure"
    newdataURL = f"{baseurl}/users/{uuid}/measure-types/{measure}/measurements"
    r = requests.post(newdataURL, headers=headers, json={"systolic_pressure": data['pressure_S'], "diastolic_pressure": data['pressure_D']})
    return r.status_code

def weight(data,uuid):
    measure = "body-weight"
    newdataURL = f"{baseurl}/users/{uuid}/measure-types/{measure}/measurements"
    r = requests.post(newdataURL, headers=headers, json={"weight": data['weight']})
    return r.status_code
