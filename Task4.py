from pathlib import Path

import requests
import yaml

file_path = Path.home() / 'INF201' / 'FrostID.txt'
with open(file_path, "r") as f:
    client_id = f.read().strip()

endpoint = 'https://frost.met.no/observations/v0.jsonld'


def heatwave_count(station_id, station_name, year):
    """Count number of heatwaves in a year with data from frost.met.no. 
    
    A heatwave is defined here as 5 or more consecutive days above 27 °C. 
    Makes a summary YAML file with the findings.
    """
    parameters = {
        'sources': station_id,
        'elements': 'max(air_temperature P1D)',
        'referencetime': f'{year}-01-01/{year}-12-31',
    }

    r = requests.get(endpoint, params=parameters, auth=(client_id, ''), timeout=10)
    json_data = r.json()

    heatwave = 0
    consecutive_days = 0
    current_heatwave_dates = []
    actual_heatwave_dates = []
    if r.status_code == 200 and 'data' in json_data: 
        for d in json_data['data']:
            temp = d['observations'][0]['value']
            date = d['referenceTime'][:10]

            if temp >= 27: 
                consecutive_days += 1
                current_heatwave_dates.append(date)

                if consecutive_days == 5: 
                    heatwave += 1
            else:
                consecutive_days = 0
                if len(current_heatwave_dates) >= 5:
                    actual_heatwave_dates.append(current_heatwave_dates)
                current_heatwave_dates = []
        
        if len(current_heatwave_dates) >= 5:
            actual_heatwave_dates.append(current_heatwave_dates)
        
        summary = {
            'dates': [f"{wave[0]} - {wave[-1]}" for wave in actual_heatwave_dates],
            'station_id': station_id,
            'station_name': station_name,
            'year': year,
        }
    
        filename = f"Heatwaves_summary_{station_id},{year}.yml"
        with open(filename, 'w') as ymlfile:
            yaml.dump(summary, ymlfile, sort_keys=False, allow_unicode=True)
        
        return heatwave
    
    else:
        print(f"something went wrong, couldn't find data for {station_id} in {year}. Status: {r.status_code} ")
        return 0

print(f"number of heatwaves:{heatwave_count('SN17850', 'Ås', 2025)}")
