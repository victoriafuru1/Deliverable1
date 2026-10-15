
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import requests

file_path = Path.home() / 'INF201' / 'FrostID.txt'
with open(file_path, "r") as f:
    client_id = f.read().strip()

endpoint = 'https://frost.met.no/observations/v0.jsonld'

parameters_temp = {
    'sources': 'SN17850',
    'elements': 'mean(air_temperature P1D)',
    'referencetime': '2025-01-01/2025-12-31',
}
parameters_precip = {
    'sources': 'SN17850',
    'elements': 'sum(precipitation_amount P1D)',
    'referencetime': '2025-01-01/2025-12-31',
}

r = requests.get(endpoint, params=parameters_temp, auth=(client_id, ''), timeout=10)
json_data = r.json()

r1 = requests.get(endpoint, params=parameters_precip, auth=(client_id, ''), timeout=10)
json_data1 = r1.json() 

if r.status_code == 200:
    xtime: list[str] = []
    ytemperature: list[float]= []

    for day in json_data['data']:
        date = day['referenceTime']
        temp = day['observations'][0]['value']
    
        xtime.append(date)
        ytemperature.append(temp)

if r1.status_code == 200:
    all_precipitation = []

    for precip in json_data['data']:
           precipitation = precip['observations'][0]['value']
           all_precipitation.append(precipitation)

else:
    print(f"Something happened! statuscode: {r.status_code}")
    print(json_data.get('error', {}).get('message'))


# Task 2
parameters_precip = {
    'sources': 'SN17850',
    'elements': 'sum(precipitation_amount P1D)',
    'referencetime': '2025-01-01/2025-12-31',
}
r1 = requests.get(endpoint, params=parameters_precip, auth=(client_id, ''), timeout=10)
json_data1 = r1.json()

if r1.status_code == 200:
    all_precipitation = []
    

    for precip in json_data1['data']:
        precipitation = precip['observations'][0]['value']
        all_precipitation.append(precipitation)

    
else:
    print(f"Something happened! statuscode: {r1.status_code}")
    print(json_data1.get('error', {}).get('message'))

fig, ax1 = plt.subplots()
ax1.plot(xtime,ytemperature, color='red', label = 'temperature')
plt.show()
