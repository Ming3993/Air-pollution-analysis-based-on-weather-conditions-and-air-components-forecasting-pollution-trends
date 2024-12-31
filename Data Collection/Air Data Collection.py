# Necessary Packages
from datetime import datetime
import requests
import numpy as np
import pandas as pd

# Base URL của API
BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution/history"

# Các tham số để thay đổi
PARAMS = {
    "lat": 10.75,
    "lon": 106.666672,
    "start": 1717174800,
    "end": 1730393999,
    "appid": "7ce5aea8df6d1e5877540f47533dfe54"
}

PARAMS1 = {
    "lat": 10.75,
    "lon": 106.666672,
    "start": 1730768400,
    "end": 1732985999,
    "appid": "7ce5aea8df6d1e5877540f47533dfe54"
}

# Khởi tạo một dictionary để lưu dữ liệu
DATA_DICTIONARY = {
    "date": [],
    "aqi": [],
    "co": [],
    "no": [],
    "no2": [],
    "o3": [],
    "so2": [],
    "pm2_5": [],
    "pm10": [],
    "nh3": []
}

import pandas as pd
import requests
from datetime import datetime

# Khởi tạo dictionary để lưu dữ liệu
DATA_DICTIONARY = {
    "date": [],
    "aqi": [],
    "co": [],
    "no": [],
    "no2": [],
    "o3": [],
    "so2": [],
    "pm2_5": [],
    "pm10": [],
    "nh3": []
}

def collect_data(base_url, params1) -> pd.DataFrame:

    # Gửi request
    response = requests.get(base_url, params=params1)
    response.raise_for_status()
    data = response.json()

    if 'list' in data:
        for item in data['list']:
            # Trích xuất thông tin
            date = item['dt']
            aqi = item['main']['aqi']
            components = item['components']

            # Lưu dữ liệu vào dictionary
            DATA_DICTIONARY['date'].append(date)
            DATA_DICTIONARY['aqi'].append(aqi)
            DATA_DICTIONARY['co'].append(components['co'])
            DATA_DICTIONARY['no'].append(components['no'])
            DATA_DICTIONARY['no2'].append(components['no2'])
            DATA_DICTIONARY['o3'].append(components['o3'])
            DATA_DICTIONARY['so2'].append(components['so2'])
            DATA_DICTIONARY['pm2_5'].append(components['pm2_5'])
            DATA_DICTIONARY['pm10'].append(components['pm10'])
            DATA_DICTIONARY['nh3'].append(components['nh3'])
    else:
        # Nếu không có dữ liệu trong response, thoát vòng lặp
        print("No more data available.")

    # Tạo DataFrame từ dictionary
    df = pd.DataFrame(DATA_DICTIONARY)

    return df

# TEST
data_air_condition = collect_data(BASE_URL, PARAMS)
#assert data_countries.shape == (161, 13)

# Save to csv file with name coutries.csv to grade
data_air_condition.to_csv("Air.csv", sep=',', encoding='utf-8', index=False, header=True)