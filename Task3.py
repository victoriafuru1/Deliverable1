from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import requests

file_path = Path.home() / 'INF201' / 'FrostID.txt'
with open(file_path, "r") as f:
    client_id = f.read().strip()

endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters_100y = {
    'sources': 'SN17850',
    'elements': 'mean(air_temperature P1D)',
    'referencetime': '1925-01-01/1925-12-31',
}

r = requests.get(endpoint, params=parameters_100y, auth=(client_id, ''), timeout=10)
json_data = r.json()

if r.status_code == 200:
    xtime: list[str] = []
    ytemperature: list[float]= []

    for day in json_data['data']:
        date = day['referenceTime']
        temp = day['observations'][0]['value']
    
        xtime.append(date)
        ytemperature.append(temp)

    mean_year_temp = np.mean(ytemperature)
    median_year_temp = np.median(ytemperature)
    min_year_temp = np.min(ytemperature)
    max_year_temp = np.max(ytemperature)
        
    print("Summary of temperatures for year 1925 in Ås:")
    print(f"{'Mean temperature of the year:' :<33} {mean_year_temp:>13.1f}°C ")
    print(f"{'Median temperature of the year:' :<33} {median_year_temp:>13.1f}°C ")
    print(f"{'Lowest temperature of the year:' :<33} {min_year_temp:>13.1f}°C")
    print(f"{'Highest temperature of the year:' :<33} {max_year_temp:>13.1f}°C")

    plt.plot(xtime, ytemperature)
    plt.title('Daily mean temperatures in Ås, 1925')
    plt.xlabel('Date (January - December)')
    plt.ylabel('mean temperature in °C')
    plt.show()

else:
    print(f"Something happened! statuscode: {r.status_code}")
    print(json_data.get('error', {}).get('message'))


