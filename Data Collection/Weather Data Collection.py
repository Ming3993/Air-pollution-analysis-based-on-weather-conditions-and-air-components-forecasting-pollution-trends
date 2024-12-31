# Necessary Packages
import time
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

CITY_ID = 1566083
API_KEY = "09c725826b2c9ff4656657f0c02075dd"
BASE_URL = "https://history.openweathermap.org/data/2.5/history/city"

def getChildData(parent: str, data_list, is_weather=False):
    data = []
    if not is_weather:
        for i in data_list[parent].values():
            data.append(i)
    else:
        # Collect all weather elements in a single string for each row
        weather_details = []
        for i in data_list[parent]:
            weather_info = f"id: {i.get('id')}, main: {i.get('main')}, description: {i.get('description')}, icon: {i.get('icon')}"
            weather_details.append(weather_info)
        data.append("\n".join(weather_details))  # Join all weather descriptions into one string

    return data

def collect_data(start_time: int, end_time: int, max_retries: int = 3, delay: int = 2) -> (pd.DataFrame, int):
    all_data = []
    params = {
        'id': CITY_ID,
        'type': 'hour',
        "start": start_time,
        "end": end_time,
        "appid": API_KEY
    }
    retries = 0
    lastest_time = 0

    while retries < max_retries:
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'list' in data and len(data['list']) > 0:
                for i in range(len(data['list'])):
                    data_list = data['list'][i]
                    if i == len(data['list']) - 1:
                        lastest_time = data_list['dt']
                    
                    ts = [data_list['dt']]
                    list_data = ts
                    
                    main_list = getChildData('main', data_list)

                    wind_list = getChildData('wind', data_list)
                    if len(wind_list) == 2:
                        wind_list.append(0)

                    clouds_list = getChildData('clouds', data_list)

                    rain_list = []
                    if 'rain' in data_list:
                        rain_list = getChildData('rain', data_list)
                    else:
                        rain_list.append(0)

                    weather_list = getChildData('weather', data_list, True)

                    list_data = list_data + main_list + wind_list + clouds_list + rain_list + weather_list
                    if (len(list_data) == 12):
                        None

                    all_data.append(list_data)
                break
            else:
                raise ValueError(f"Failed to retrieve data after {max_retries} retries")
                
        else:
            print(f"Request failed with status code {response.status_code}. Retrying in {delay} seconds...")
            retries += 1
            print(response.url)
            time.sleep(delay)
    
    # Construct the DataFrame with weather column capturing concatenated weather data
    if all_data:
        result = pd.DataFrame(all_data, columns=[
            'dt', 'main temp', 'main feels like', 'main pressure', 'main humidity',
            'main temp min', 'main temp max', 'wind speed', 'wind deg', 'wind gust', 'clouds all', 
             'rain 1h', 'weather details'
        ])
        result.fillna('NaN', inplace=True)
        return result, lastest_time
    else:
        raise ValueError("No data was retrieved; check the API response and parameters.")

def generate_weather_dataset() -> pd.DataFrame:
    data_frames = []
    start_time = 1717174800
    end_time = 1730390400
    while start_time <= end_time:
        try:
            df, start_time = collect_data(start_time,  end_time)
            data_frames.append(df)
            start_time += 3600
            
        except ValueError as e:
            print(f"Error collecting data: {e}")

    combined_data = pd.concat(data_frames, ignore_index=True)

    return combined_data

# TEST
data_weather = generate_weather_dataset()
assert data_weather.shape

# Save to csv file with name coutries.csv to grade
data_weather.to_csv("Weather.csv", sep=',', encoding='utf-8', index=False, header=True)