from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import requests

file_path = Path.home() / 'INF201' / 'FrostID.txt'
with open(file_path, "r") as f:
    client_id = f.read().strip()



endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN17850',
    'elements': 'max(air_temperature P1D)',
    'referencetime': '2025-01-01/2025-12-31',
}
r = requests.get(endpoint, params=parameters, auth=(client_id, ''), timeout=10)
json_data = r.json() 

def heatwave_count():
    heatwave = []
    for d in json_data['data']:
        hot_day = d['observations'][0]['value']

        if hot_day >= 5: #hvordan få denne til å telle 5 sammenhengende dager? 
            heatwave.append(hot_day)
        print(heatwave)
        

    
    
    

