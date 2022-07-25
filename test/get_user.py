import requests
import json

Host = "healthy-api.huakai.com.tw"
UUID = "a0dd03c0-f1c7-11ec-a3f6-1b708992358f"
api = "d69d3fc0-ga8r-e1hu-b803-6567760e2826"
Version = "1.0"
baseurl = f"https://{Host}/api/{Version}/partners/{UUID}"
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
