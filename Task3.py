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

parameters_2025 = {
    'sources': 'SN17850',
    'elements': 'mean(air_temperature P1D)',
    'referencetime': '2025-01-01/2025-12-31',
}

r_100y = requests.get(endpoint, params=parameters_100y, auth=(client_id, ''), timeout=10)
json_data100 = r_100y.json()

r_2025 = requests.get(endpoint, params=parameters_2025, auth=(client_id, ''), timeout=10)
json_data25 = r_2025.json()

if r_100y.status_code == 200 and r_2025.status_code == 200:
    xtime100: list[str] = []
    ytemperature100: list[float]= []

    for day in json_data100['data']:
        date100 = day['referenceTime']
        temp100 = day['observations'][0]['value']
    
        xtime100.append(date100)
        ytemperature100.append(temp100)

    mean_year_temp100 = np.mean(ytemperature100)
    median_year_temp100 = np.median(ytemperature100)
    min_year_temp100 = np.min(ytemperature100)
    max_year_temp100 = np.max(ytemperature100)

    xtime: list[str] = []
    ytemperature: list[float] = []
    
    xtime_no_year: list[str] = []

    for day in json_data25['data']:
        full_date = day['referenceTime']
        temp = day['observations'][0]['value']
    
        date_no_year = full_date[5:10]
        
        xtime.append(full_date)
        ytemperature.append(temp)
    
        xtime_no_year.append(date_no_year)
    
    mean_year_temp = np.mean(ytemperature)
    median_year_temp = np.median(ytemperature)
    min_year_temp = np.min(ytemperature)
    max_year_temp = np.max(ytemperature)

    print("Summary of temperatures for year 1925 and 2025 in Ås:")
    print(f"{'Mean temperature for':<32}1925:  {mean_year_temp100:>4.1f}°C    2025:  {mean_year_temp:>4.1f}°C ")
    print(f"{'Median temperature for':<32}1925:  {median_year_temp100:>4.1f}°C    2025:  {median_year_temp:>4.1f}°C ")
    print(f"{'Lowest temperature for':<32}1925: {min_year_temp100:>4.1f}°C    2025: {min_year_temp:>4.1f}°C ")
    print(f"{'Highest temperature for':<32}1925:  {max_year_temp100:>4.1f}°C    2025:  {max_year_temp:>4.1f}°C ")

    plt.plot(xtime_no_year, ytemperature, xtime_no_year, ytemperature100)
    plt.legend(['2025', '1925'])
    plt.title('Daily mean temperatures in Ås, 1925 and 2025')
    plt.xlabel('Date (January - December)')
    plt.ylabel('temperature in °C')
    plt.show()


else:
    print(f"Something happened! statuscode 2025: {r_2025.status_code} statuscode 1925: {r_100y.status_code}")
    print(json_data25.get('error', {}).get('message'))
    print(json_data100.get('error', {}).get('message'))

    




