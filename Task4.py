from pathlib import Path

import requests

file_path = Path.home() / 'INF201' / 'FrostID.txt'
with open(file_path, "r") as f:
    client_id = f.read().strip()



endpoint = 'https://frost.met.no/observations/v0.jsonld'

def heatwave_count(station_id, year):
    parameters = {
    'sources': station_id,
    'elements': 'max(air_temperature P1D)',
    'referencetime': f'{year}-01-01/{year}-12-31',
}
    r = requests.get(endpoint, params=parameters, auth=(client_id, ''), timeout=10)
    json_data = r.json()

    heatwave = 0
    consecutive_days = 0
    if r.status_code == 200 and 'data' in json_data: 
        for d in json_data['data']:
            temp = d['observations'][0]['value']

            if temp >= 27: 
                consecutive_days += 1 
                if consecutive_days == 5: 
                    heatwave +=1
            else:
                consecutive_days = 0
        return heatwave
    else:
        print(f"something went wrong, couldn't find data for {station_id} in {year}. Status: {r.status_code} ")
        return 0
print(f"number of heatwaves:{heatwave_count('SN17850', 2025)}")
       
        

    
    
    

