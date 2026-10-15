import requests 
import pandas as pd
import matplotlib 
from pathlib import Path 

file_path = Path.home() / 'INF201' / 'FrostID.txt' 
with open(file_path, "r") as f:
    client_id = f.read().strip()



endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN17850',
    'elements': 'mean(air_temperature P1D)',
    'referencetime': '2025-01-01/2025-12-31',
}

r = requests.get(endpoint, params=parameters, auth=(client_id, ''))
json= r.json()
