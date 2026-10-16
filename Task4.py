from pathlib import Path

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
    heatwave = 0
    consecutive_days = 0
    
    for d in json_data['data']:
        temp = d['observations'][0]['value']

        if temp >= 27: 
            consecutive_days += 1 
            if consecutive_days == 5: 
                heatwave +=1
        else:
            consecutive_days = 0
    return heatwave
print(f"Antall hetebølger:{heatwave_count()}")
       
        

    
    
    

