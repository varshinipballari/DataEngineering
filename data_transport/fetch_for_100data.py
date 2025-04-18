import requests
import json
import datetime
import time

def fetch_all_vehicle_data():
    vehicle_ids = [
        2903, 2910, 2912, 2914, 2918, 2919, 2927, 2928, 2930, 2932,
        2935, 2936, 2940, 3006, 3008, 3011, 3022, 3024, 3026, 3028,
        3034, 3042, 3055, 3057, 3058, 3103, 3104, 3105, 3106, 3109,
        3114, 3115, 3116, 3118, 3119, 3121, 3123, 3125, 3127, 3137,
        3139, 3141, 3142, 3147, 3149, 3150, 3157, 3162, 3168, 3203,
        3205, 3207, 3210, 3211, 3212, 3215, 3217, 3221, 3223, 3227,
        3231, 3232, 3244, 3246, 3247, 3255, 3266, 3302, 3305, 3309,
        3312, 3313, 3323, 3324, 3326, 3327, 3328, 3330, 3405, 3408,
        3415, 3416, 3418, 3503, 3506, 3509, 3510, 3513, 3514, 3515,
        3523, 3524, 3526, 3527, 3530, 3536, 3537, 3543, 3546
    ]

    base_url = "https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id="
    all_data = []

    for vid in vehicle_ids:
        url = f"{base_url}{vid}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                vehicle_data = response.json()
                all_data.extend(vehicle_data)
                print(f" Collected data for vehicle ID {vid}, records: {len(vehicle_data)}")
            else:
                print(f"Failed to fetch data for vehicle ID {vid}: {response.status_code}")
        except Exception as e:
            print(f" Error fetching data for vehicle ID {vid}: {e}")
        time.sleep(0.1)  # avoid overwhelming the API

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"vehicaldata{today}.json"
    with open(filename, "w") as f:
        json.dump(all_data, f, indent=2)

    print(f"\n📁 Finished fetching data. Saved {len(all_data)} total records to {filename}.")

if __name__ == "__main__":
    fetch_all_vehicle_data()