import requests
import json

def fetch_data():
    vehicleids = [3708, 3266]
    base_url = 'https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id='
    data = {}
    for vehicleid in vehicleids:
        url = base_url + str(vehicleid)
        response = requests.get(url)
        if response.status_code == 200:
            data[f'vehicle_{vehicleid}'] = response.json()
        else:
            print(f'Failed to fetch data for vehicle {vehicleid}: {response.status_code}, {response.reason}')

    with open('bcsample.json', 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == '__main__':
    fetch_data()
