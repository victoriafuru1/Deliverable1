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

if r_100y.status_code == 200:
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

else:
    print(f"Something happened! statuscode: {r_100y.status_code}")
    print(json_data100.get('error', {}).get('message'))

if r_2025.status_code == 200:
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

else:
    print(f"Something happened! statuscode: {r_2025.status_code}")
    print(json_data25.get('error', {}).get('message'))

    
        
print("Summary of temperatures for year 1925 and 2025 in Ås:")
print(f"{'Mean temperature of 1925:' :<33} {mean_year_temp100:>8.1f}°C ")
print(f"{'Median temperature of 1925:' :<33} {median_year_temp100:>8.1f}°C ")
print(f"{'Lowest temperature of 1925:' :<33} {min_year_temp100:>8.1f}°C")
print(f"{'Highest temperature of 1925:' :<33} {max_year_temp100:>8.1f}°C")

plt.plot(xtime_no_year, ytemperature, ytemperature100)
plt.title('Daily mean temperatures in Ås, 1925 and 2025')
plt.xlabel('Date (January - December)')
plt.ylabel('temperature in °C')
plt.show()

"""
fig, ax1 = plt.subplots()
ax1.plot(xtime, ytemperature, color='red', label='temperature 2025')
ax1.set_ylabel('Daily mean temperature in °C 2025', color='red')

ax2 = ax1.twinx()
ax2.plot(xtime, ytemperature100, color='blue', label='temperature 1925')
ax2.set_ylabel("daily mean temperature in °C 1925", color='blue')

plt.xlabel('Date (January - December)')
plt.title("Daily mean temperature in Ås, 1925 and 2025")
plt.show()



plt.plot(xtime, ytemperature)
    plt.title('Daily mean temperatures in Ås, 1925')
    plt.xlabel('Date (January - December)')
    plt.ylabel('mean temperature in °C')
    plt.show()
"""



