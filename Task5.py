
from pathlib import Path

import matplotlib.pyplot as plt
import requests

file_path = Path.home() / 'INF201' / 'FrostID.txt'
with open(file_path, "r") as f:
    client_id = f.read().strip()


endpoint = 'https://frost.met.no/observations/v0.jsonld'

def calculate_moving_average():

    parameters = {
        'sources': 'SN17850',
        'elements': 'mean(air_temperature P1D)',
        'referencetime': '2025-01-01/2025-12-31',
    }
    r = requests.get(endpoint, params=parameters, auth=(client_id, ''), timeout=10)
    json_data = r.json()

    all_temps = []
    all_dates = []
    for d in json_data['data']:
        temps = d['observations'][0]['value']
        dates = d['referenceTime']

        all_temps.append(temps)
        all_dates.append(dates)

    print(len(all_temps))
calculate_moving_average()

