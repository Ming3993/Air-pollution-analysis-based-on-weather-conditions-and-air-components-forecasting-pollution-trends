import pandas as pd
import re

# Đọc dữ liệu từ file (giả sử bạn đã thực hiện)
df = pd.read_csv('cleaned_data.csv')

# Tính toán và cập nhật 'Temperature Amplitude'
if 'Min Temprature (Kelvin)' in df.columns and 'Max Temprature (Kelvin)' in df.columns:
    df['Temperature Amplitude'] = df['Max Temprature (Kelvin)'] - df['Min Temprature (Kelvin)']


def extract_description(weather_desc):
    match = re.search(r'description:\s*([^,]+)', weather_desc)
    return match.group(1) if match else None

# Áp dụng hàm trích xuất cho cột 'Weather Description'
df['Weather Description'] = df['Weather details'].apply(extract_description)

df['Min Temprature (Kelvin)'] = df['Temperature Amplitude'].values
df['Weather details'] = df['Weather Description'].values

df.drop(columns=['Max Temprature (Kelvin)', 'Temperature Amplitude', 'Weather Description'], inplace=True)

df.rename(columns={'Min Temprature (Kelvin)': 'Temperature Amplitude', 'Weather details': 'Weather Description'}, inplace=True)

# Xuất DataFrame sau khi cập nhật (nếu cần)
df.to_csv('ProcessedData.csv', index=False)