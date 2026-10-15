import requests 
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path 
import numpy as np


file_path = Path.home() / 'INF201' / 'FrostID.txt' 
with open(file_path, "r") as f:
    client_id = f.read().strip()



endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN17850',
    'elements': 'mean(air_temperature P1D)',
    'referencetime': '2025-01-01/2025-12-31',
}

r = requests.get(endpoint, params=parameters, auth=(client_id, ''), timeout=10)
json= r.json()

if r.status_code == 200:
    xtime = []
    ytemperature = []

    for day in json['data']: 
        date = day['referenceTime']
        temp = day['observations'][0]['value']
    
        xtime.append(date)
        ytemperature.append(temp)

    plt.plot(xtime, ytemperature)
    plt.xlabel('Date')
    plt.ylabel('mean temperature')
    plt.show()
else: 
    print(f"Something happened! statuscode: {r.status_code}")
    print(json.get('error', {}).get('message'))